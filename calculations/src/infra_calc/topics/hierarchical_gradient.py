"""One real Qwen gradient, exact chunk ownership, declared hierarchical paths.

Two servers hold ``ranks_per_server`` ranks each.  When every rank has its own
NIC (``nics_per_server == ranks_per_server``) a remote message leaves through
the sender's NIC and enters through the receiver's NIC.  With fewer NICs than
ranks a remote message is striped over the server's NICs and, when declared,
squeezed through a shared server egress/ingress.  No framework bucket,
floating-point equivalence or measured runtime claim.
"""
from collections import Counter
from fractions import Fraction
from math import prod
import json
from ..models import qwen3
from ..sources import model_config, provenance, read_source
from .ring_collective import schedule
from ..traffic import account
from ..units import positive_int


def calculate(model='qwen3-8b', gradient_dtype='FP32', algorithm='hierarchical',
              ranks_per_server=8, nics_per_server=8,
              nic_bytes_per_second=50_000_000_000,
              local_bytes_per_second=450_000_000_000,
              shared_egress_bytes_per_second=None,
              bandwidth_overrides=None, startup_ns=2000, budget_ns=3_000_000):
    if model != 'qwen3-8b':
        raise ValueError('This fixed experiment selects Qwen3-8B first-layer gate gradient')
    if gradient_dtype not in ('FP32', 'BF16'):
        raise ValueError('Gradient dtype must be FP32 or BF16')
    if algorithm not in ('flat_contiguous', 'flat_interleaved', 'hierarchical'):
        raise ValueError('Unknown organization')
    if type(ranks_per_server) is not int or ranks_per_server not in (4, 8):
        raise ValueError('Each server holds four or eight ranks')
    if type(nics_per_server) is not int or not 1 <= nics_per_server <= ranks_per_server:
        raise ValueError('NIC count must be an integer between one and the ranks per server')
    positive_int(nic_bytes_per_second, 'nic_bytes_per_second')
    positive_int(local_bytes_per_second, 'local_bytes_per_second')
    if shared_egress_bytes_per_second is not None:
        positive_int(shared_egress_bytes_per_second, 'shared_egress_bytes_per_second')
    positive_int(startup_ns, 'startup_ns', allow_zero=True)
    positive_int(budget_ns, 'budget_ns', allow_zero=True)
    config = model_config(model)
    sources = provenance(model)
    for row in sources:
        read_source(row['file'])
    tensor = next(w for w in qwen3.weights(config)
                  if w.name == 'model.layers.{layer}.mlp.gate_proj.weight')
    elements = prod(tensor.shape)  # One occurrence, never multiply layer copies.
    width = {'FP32': 4, 'BF16': 2}[gradient_dtype]
    R = ranks_per_server
    p = 2 * R
    per_rank_nic = nics_per_server == R
    stripes_per_message = 1 if per_rank_nic else nics_per_server
    if elements % (p * stripes_per_message):
        raise ValueError('Gradient must divide into whole-element chunks and NIC stripes; no padding')
    chunk_elements = elements // p
    payload = elements * width
    chunk_bytes = chunk_elements * width
    if algorithm == 'flat_interleaved':
        order = [rank for pair in zip(range(R), range(R, p)) for rank in pair]
    else:
        order = list(range(p))
    mapping = [dict(rank=r, server=r // R, card=r % R, nic=(r % R if per_rank_nic else None)) for r in range(p)]
    states = [{c: {rank} for c in range(p)} for rank in range(p)]
    rounds, boundaries, paths, bandwidths = [], [], {}, {}
    reduction_adds = 0
    cut_rate = nics_per_server * nic_bytes_per_second
    if shared_egress_bytes_per_second is not None:
        cut_rate = min(cut_rate, shared_egress_bytes_per_second)

    def resource(name, default):
        bandwidths.setdefault(name, default)
        return name

    def remote_path(sender, receiver, nic_out, nic_in):
        a, b = sender // R, receiver // R
        path = [resource(f'rank{sender}.tx', local_bytes_per_second),
                resource(f'server{a}.nic{nic_out}.tx', nic_bytes_per_second)]
        if shared_egress_bytes_per_second is not None:
            path.append(resource(f'server{a}.egress', shared_egress_bytes_per_second))
        path += [resource(f'cut.{a}->{b}', cut_rate),
                 resource('shared_cut.bidirectional', 2 * cut_rate)]
        if shared_egress_bytes_per_second is not None:
            path.append(resource(f'server{b}.ingress', shared_egress_bytes_per_second))
        path += [resource(f'server{b}.nic{nic_in}.rx', nic_bytes_per_second),
                 resource(f'rank{receiver}.rx', local_bytes_per_second)]
        return path

    def physical_stripes(sender, receiver, start, stop):
        remote = sender // R != receiver // R
        if not remote:
            path = [resource(f'rank{sender}.tx', local_bytes_per_second),
                    resource(f'local.{sender}->{receiver}', local_bytes_per_second),
                    resource(f'rank{receiver}.rx', local_bytes_per_second)]
            key = (f'r{sender}:local', f'r{receiver}:local')
            if key in paths and paths[key] != path:
                raise ValueError('Ambiguous virtual endpoint path')
            paths[key] = path
            return [dict(sender=key[0], receiver=key[1], bytes=(stop - start) * width, nic=None,
                         element_start=start, element_stop=stop, path=path)]
        if per_rank_nic:
            lanes = [(sender % R, receiver % R)]
        else:
            lanes = [(nic, nic) for nic in range(nics_per_server)]
        if (stop - start) % len(lanes):
            raise ValueError('Whole-element NIC striping required')
        result = []
        for index, (nic_out, nic_in) in enumerate(lanes):
            begin = start + index * ((stop - start) // len(lanes))
            end = begin + (stop - start) // len(lanes)
            source = f'r{sender}:nic{nic_out}'
            target = f'r{receiver}:nic{nic_in}'
            path = remote_path(sender, receiver, nic_out, nic_in)
            key = (source, target)
            if key in paths and paths[key] != path:
                raise ValueError('Ambiguous virtual endpoint path')
            paths[key] = path
            result.append(dict(sender=source, receiver=target, bytes=(end - begin) * width,
                               nic=nic_out, element_start=begin, element_stop=end, path=path))
        return result

    def snapshot(label):
        boundaries.append(dict(after=label, round_count=len(rounds), ranks=[
            dict(rank=r, chunks=[dict(chunk=c, contributors=sorted(contributors))
                                for c, contributors in sorted(state.items())])
            for r, state in enumerate(states)]))

    def run_phase(stage, phase, groups):
        """Group consists of physical ranks and chunk-lists per logical chunk."""
        nonlocal reduction_adds
        participants = len(groups[0][0])
        plans = [r for r in schedule(participants, 1) if r['phase'] == phase]
        for plan in plans:
            messages, physical = [], []
            # Read all messages from the pre-round state before any receives.
            for ranks, chunks in groups:
                for edge in plan['edges']:
                    sender, receiver = ranks[edge['sender']], ranks[edge['receiver']]
                    pieces = chunks[edge['chunk']]
                    if pieces != list(range(min(pieces), max(pieces) + 1)):
                        raise ValueError('Message gradient interval must be contiguous')
                    start, stop = min(pieces) * chunk_elements, (max(pieces) + 1) * chunk_elements
                    contributions = [dict(chunk=c, contributors=sorted(states[sender][c])) for c in pieces]
                    stripes = physical_stripes(sender, receiver, start, stop)
                    message = dict(sender=sender, receiver=receiver,
                                   operation='reduce' if phase == 'reduce_scatter' else 'copy',
                                   chunks=pieces, element_start=start, element_stop=stop,
                                   bytes=(stop - start) * width, contributions=contributions,
                                   remote=sender // R != receiver // R, stripes=stripes)
                    messages.append(message); physical.extend(stripes)
            for message in messages:
                dst = states[message['receiver']]
                for item in message['contributions']:
                    c, incoming = item['chunk'], set(item['contributors'])
                    if message['operation'] == 'reduce':
                        if c not in dst or incoming & dst[c]:
                            raise ValueError('Reduction duplicates/misses an input contribution')
                        dst[c] = dst[c] | incoming
                        reduction_adds += chunk_elements
                    else:
                        if c in dst:
                            raise ValueError('All-gather overwrites an already-owned chunk')
                        dst[c] = incoming
            rounds.append(dict(round=len(rounds), stage=stage, phase=phase,
                               step=plan['step'], messages=messages, edges=physical))
        if phase == 'reduce_scatter':
            for ranks, chunks in groups:
                for logical, rank in enumerate(ranks):
                    keep = chunks[(logical + 1) % participants]
                    states[rank] = {c: states[rank][c] for c in keep}
        snapshot(stage + ':' + phase)

    snapshot('initial')
    if algorithm != 'hierarchical':
        groups = [(order, [[c] for c in range(p)])]
        run_phase('flat', 'reduce_scatter', groups)
        run_phase('flat', 'all_gather', groups)
    else:
        local = [(list(range(server * R, server * R + R)), [[2 * c, 2 * c + 1] for c in range(R)])
                 for server in range(2)]
        run_phase('local_reduce_scatter', 'reduce_scatter', local)
        # Local ring owner of coarse chunk c is logical rank (c-1) modulo R.
        remote = [([(c - 1) % R, R + (c - 1) % R], [[2 * c], [2 * c + 1]]) for c in range(R)]
        run_phase('cross_server_allreduce', 'reduce_scatter', remote)
        run_phase('cross_server_allreduce', 'all_gather', remote)
        run_phase('local_all_gather', 'all_gather', local)
    if any(set(s) != set(range(p)) or any(v != set(range(p)) for v in s.values()) for s in states):
        raise ValueError('Final gradient does not contain every rank contribution')
    if bandwidth_overrides is not None:
        if not isinstance(bandwidth_overrides, dict):
            raise ValueError('Bandwidth overrides must map existing resource IDs to positive integer rates')
        if set(bandwidth_overrides) - set(bandwidths):
            raise ValueError('Bandwidth override references unused/unknown resource')
        for name, value in bandwidth_overrides.items():
            positive_int(value, name + ' bandwidth')
            bandwidths[name] = value
    traffic = account(rounds, paths, bandwidths, startup_ns)
    totals = Counter()
    stage_rows = {}
    exact_barrier = Fraction(0)
    for row, counted in zip(rounds, traffic['rounds']):
        counts = Counter()
        for stripe in row['edges']:
            for name in stripe['path']:
                counts[name] += stripe['bytes']
        if dict(counts) != counted['resource_bytes']:
            raise ValueError('Physical path recount disagrees with public traffic account')
        totals.update(counts)
        bottleneck = max((Fraction(n, bandwidths[name]) for name, n in counts.items()), default=Fraction(0))
        bound = bottleneck + Fraction(startup_ns, 10**9)
        row['resource_bytes'] = dict(counts)
        row['resource_lower_seconds_exact'] = str(bottleneck)
        row['barrier_lower_seconds_exact'] = str(bound)
        row['barrier_start_seconds_exact'] = str(exact_barrier)
        exact_barrier += bound
        row['barrier_finish_seconds_exact'] = str(exact_barrier)
        stage_row = stage_rows.setdefault(row['stage'], dict(stage=row['stage'], rounds=0, send_bytes=0, remote_send_bytes=0, seconds=Fraction(0)))
        stage_row['rounds'] += 1
        stage_row['send_bytes'] += sum(m['bytes'] for m in row['messages'])
        stage_row['remote_send_bytes'] += sum(m['bytes'] for m in row['messages'] if m['remote'])
        stage_row['seconds'] += bound
    aggregate = max(Fraction(n, bandwidths[name]) for name, n in totals.items())
    largest = [name for name, n in sorted(totals.items()) if Fraction(n, bandwidths[name]) == aggregate]
    sends = sum(m['bytes'] for r in rounds for m in r['messages'])
    remote_sends = sum(m['bytes'] for r in rounds for m in r['messages'] if m['remote'])
    expected_remote = {'flat_contiguous': Fraction(4 * (p - 1), p), 'flat_interleaved': 2 * (p - 1),
                       'hierarchical': 2}[algorithm] * payload
    if sends != 2 * (p - 1) * payload or remote_sends != expected_remote or reduction_adds != (p - 1) * elements:
        raise ValueError('Ring/hierarchy conservation self-check failed')
    if exact_barrier < aggregate or traffic['logical_send_bytes'] != sends:
        raise ValueError('Resource bound or stripe conservation failed')
    remote_nics_used = sorted({stripe['nic'] for r in rounds for stripe in r['edges'] if stripe['nic'] is not None})
    remote_edges = sum(1 for m in rounds[0]['messages'] if m['remote']) if rounds else 0
    return dict(calculation='hierarchical-gradient',
        scenario=dict(model=model, gradient_dtype=gradient_dtype, algorithm=algorithm,
            ranks_per_server=ranks_per_server, nics_per_server=nics_per_server,
            nic_bytes_per_second=nic_bytes_per_second, local_bytes_per_second=local_bytes_per_second,
            shared_egress_bytes_per_second=shared_egress_bytes_per_second,
            nic_assignment='one NIC per rank' if per_rank_nic else 'messages striped over server NICs',
            startup_ns=startup_ns, budget_ns=budget_ns, bandwidth_overrides=bandwidth_overrides), sources=sources,
        gradient=dict(parameter='model.layers.0.mlp.gate_proj.weight', template=tensor.name,
            shape=list(tensor.shape), elements=elements, bytes_per_element=width,
            bytes_per_rank=payload, selected_parameter_copies=1, template_layer_copies=tensor.copies,
            initial_contributors_per_rank=1, participants=p, chunks=p, chunk_elements=chunk_elements,
            chunk_bytes=chunk_bytes),
        rank_mapping=mapping, flat_ring_order=order if algorithm != 'hierarchical' else None,
        rounds=rounds, ownership_boundaries=boundaries,
        resources=[dict(resource=name, bytes=n, bandwidth_bytes_per_second=bandwidths[name],
                        service_seconds_exact=str(Fraction(n, bandwidths[name]))) for name, n in sorted(totals.items())],
        stages=[{**{k: v for k, v in r.items() if k != 'seconds'}, 'barrier_lower_seconds_exact': str(r['seconds'])} for r in stage_rows.values()],
        traffic_account=traffic,
        summary=dict(network_send_bytes=sends, local_send_bytes=sends - remote_sends,
            remote_send_bytes=remote_sends, remote_send_bytes_per_direction=remote_sends // 2,
            reduction_scalar_adds=reduction_adds,
            final_gradient_bytes_per_rank=[payload] * p, rounds=len(rounds),
            first_round_remote_edges=remote_edges, remote_nics_used_per_server=len(remote_nics_used),
            aggregate_resource_lower_seconds_exact=str(aggregate), largest_aggregate_resources=largest,
            serial_barrier_lower_seconds_exact=str(exact_barrier),
            necessary_budget_not_excluded=exact_barrier <= Fraction(budget_ns, 10**9),
            actual_training_deadline_feasible=None, measured_seconds=None),
        assumptions=[
            'One real first-layer gate parameter gradient per rank; each rank contributes different sample data to the same coordinates. Not activations, whole-model gradients, or framework buckets.',
            'FP32/BF16 are declared gradient wire/operand widths. Rank contribution identities prove algebraic sum coverage, not floating-point reassociation equivalence or backend accumulation precision.',
            f'Two servers each own {R} fixed ranks. Hierarchy executes local RS over {R} ranks, corresponding-owner two-rank AR, local AG with stage/round barriers; no overlapping stages or unmodeled algorithm substitutions.',
            ('Every rank owns one NIC: a remote message leaves through the sender NIC and enters through the receiver NIC, never striped or relayed.' if per_rank_nic else
             f'Remote messages stripe disjoint whole-element intervals over the {nics_per_server} server NIC(s), never duplicate payload.')
            + ' The switch cut between the servers carries the aggregate NIC rate' + (' capped by the declared shared server egress/ingress.' if shared_egress_bytes_per_second is not None else '; no shared server egress is declared.'),
            'All rates and startup are declared inputs. Each round bound is max(resource bytes/rate)+startup; serialized barrier bounds omit reduction work, propagation, buffering, topology latency and interference. They are not executable timing or deadline guarantees.',
            'Logical network sends count payload once. Endpoint receive, NIC, ingress and cut counters represent distinct resource demands; their sum is not additional gradient payload or HBM traffic.',
            'No padding is introduced. Missing paths/resources or invalid rates reject. Budget pass only means this communication lower bound has not excluded the candidate; real training feasibility remains unknown.'])


def markdown(result):
    """Readable phase and physical-resource tables, with complete replay data."""
    g, summary, sc = result['gradient'], result['summary'], result['scenario']
    lines = ['# 真实梯度的两级集合通信', '',
             f"参数：`{g['parameter']}`；形状 {g['shape']}；每rank {g['bytes_per_rank']:,} bytes；参与者 {g['participants']}。",
             f"组织：{sc['algorithm']}；每服务器 {sc['ranks_per_server']} rank、{sc['nics_per_server']} NIC（{sc['nic_assignment']}）；"
             f"NIC {sc['nic_bytes_per_second']:,} bytes/s，本地 {sc['local_bytes_per_second']:,} bytes/s，共享出口 {sc['shared_egress_bytes_per_second']}。",
             '', '| 阶段 | 轮数 | 发送 bytes | 跨服务器发送 bytes | 串行屏障下界 seconds（精确） |',
             '| --- | ---: | ---: | ---: | ---: |']
    for row in result['stages']:
        lines.append(f"| {row['stage']} | {row['rounds']} | {row['send_bytes']} | {row['remote_send_bytes']} | {row['barrier_lower_seconds_exact']} |")
    lines += ['', f"全网发送 {summary['network_send_bytes']:,} bytes；跨服务器 {summary['remote_send_bytes']:,} bytes（每方向 {summary['remote_send_bytes_per_direction']:,}）；标量归约加法 {summary['reduction_scalar_adds']:,} 次；每服务器用到 {summary['remote_nics_used_per_server']} 张 NIC。",
              f"串行屏障下界 {summary['serial_barrier_lower_seconds_exact']} seconds；预算未被此必要下界排除：{summary['necessary_budget_not_excluded']}。实际训练期限是否可行仍未知。", '',
              '| 物理资源 | bytes | 声明 bytes/s | 必要服务 seconds（精确） |', '| --- | ---: | ---: | ---: |']
    for row in result['resources']:
        lines.append(f"| {row['resource']} | {row['bytes']} | {row['bandwidth_bytes_per_second']} | {row['service_seconds_exact']} |")
    lines += ['', *['- ' + item for item in result['assumptions']], '', '完整逐轮消息、NIC区间和贡献身份：', '', '```json', json.dumps(result, ensure_ascii=False, indent=2), '```', '']
    return '\n'.join(lines)
