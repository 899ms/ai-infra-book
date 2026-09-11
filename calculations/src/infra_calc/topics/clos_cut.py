"""Folded Clos reach and cut bandwidth, rail-aligned two-server AllReduce, switch-side reduction.

Archived text used for the topology rules (quoted so the module does not transcribe tables):
- references/text/fat-tree.txt, lines 210-220: "organize a k-ary fat-tree ... There are k pods,
  each containing two layers of k/2 switches. Each k-port switch in the [edge layer] ... There are
  (k/2)^2 k-port core switches. ... In general, a fat-tree built with k-port switches supports
  k^3/4 hosts."  The two-tier (leaf/spine) case is the same folded Clos with one fewer level.
- references/text/nvidia-nvlink-spec.txt, line 317: "each NVLink Switch has engines for NVIDIA
  Scalable Hierarchical Aggregation and Reduction Protocol (SHARP) for in-network reductions";
  references/text/nvidia-h100.txt, line 481: "SHARP in-network reductions".  Only the operation
  count (send once, receive once, one round) is taken from these lines; no switch throughput is.

Oversubscription is applied at the leaf (edge) tier only: with radix k and ratio r the leaf has
d = k*r/(1+r) downlinks and u = k/(1+r) uplinks, both required to be whole numbers.  Higher tiers
stay non-blocking with respect to the leaf uplinks, so endpoints grow by d/(k/2) and every cut
bandwidth shrinks by 1/r relative to the non-blocking k-ary fat-tree.
"""
from fractions import Fraction
import json
from math import prod

from ..declared import exact, input_sources as _sources
from ..models import qwen3
from ..paths import PROJECT
from ..sources import model_config, provenance
from ..units import ceil_div, positive_int


def _tier(radix, down, up, tier, link):
    if tier == 2:
        leaves = radix
        switches = dict(leaf=radix, spine=up)
        pods = None
    elif tier == 3:
        leaves = radix * radix // 2
        switches = dict(edge=radix * radix // 2, aggregation=radix * up, core=up * radix // 2)
        pods = radix
    else:
        raise ValueError('tiers must contain only 2 or 3')
    endpoints = leaves * down
    uplinks = leaves * up
    bisection = Fraction(uplinks, 2) * link
    full = Fraction(endpoints, 2) * link
    return dict(tiers=tier, leaf_switches=leaves, pods=pods, switches=switches,
                total_switches=sum(switches.values()), endpoints=endpoints,
                endpoints_per_pod=(radix // 2) * down if pods else None,
                leaf_uplinks_total=uplinks,
                bisection_bytes_per_second_exact=str(bisection),
                nonblocking_bisection_bytes_per_second_exact=str(full),
                bisection_fraction_of_nonblocking_exact=str(bisection / full))


def _partition(radix, down, up, tier, link, endpoints):
    leaves_used = ceil_div(endpoints, down)
    leaf_cut = leaves_used * up
    if tier == 3:
        per_pod = (radix // 2) * down
        pods_used = ceil_div(endpoints, per_pod)
        pod_cut = pods_used * up * (radix // 2)
        cut_links = min(leaf_cut, pod_cut)
    else:
        pods_used, pod_cut, cut_links = None, None, leaf_cut
    return dict(tiers=tier, partition_endpoints=endpoints, leaves_used=leaves_used,
                pods_used=pods_used, leaf_uplinks_in_cut=leaf_cut, pod_core_links_in_cut=pod_cut,
                cut_links=cut_links, cut_bytes_per_second_exact=str(cut_links * link),
                cut_bytes_per_second_per_endpoint_exact=str(Fraction(cut_links * link, endpoints)))


def _clos(radix, oversubscription, tiers, link_bytes_per_second, partition_endpoints, supernode_scenario):
    positive_int(radix, 'radix')
    ratio = exact(oversubscription, 'oversubscription')
    link = exact(link_bytes_per_second, 'link_bytes_per_second')
    positive_int(partition_endpoints, 'partition_endpoints')
    if radix % 2:
        raise ValueError('radix must be even for a folded Clos with k/2 up and down ports')
    down = Fraction(radix) * ratio / (1 + ratio)
    up = Fraction(radix) / (1 + ratio)
    if down.denominator != 1 or up.denominator != 1 or down < 1 or up < 1:
        raise ValueError('oversubscription must split the radix into whole down and up ports')
    down, up = int(down), int(up)
    if not isinstance(tiers, (list, tuple)) or not tiers:
        raise ValueError('tiers must be a nonempty list of 2 or 3')
    rows = [_tier(radix, down, up, tier, link) for tier in tiers]
    cuts = []
    for tier, row in zip(tiers, rows):
        if partition_endpoints <= row['endpoints']:
            cuts.append(_partition(radix, down, up, tier, link, partition_endpoints))
    supernodes = None
    if supernode_scenario:
        scenario = json.loads((PROJECT / supernode_scenario).read_text())
        gpus = positive_int(scenario['gpus'], 'gpus')
        nic = exact(scenario['nic_Bps'], 'nic_Bps')
        exported = {}
        results_path = PROJECT / 'results/supernode-scaling-book.json'
        if results_path.is_file():
            for item in json.loads(results_path.read_text())['results']:
                if item['profile'] == scenario['profiles'][0]['name']:
                    exported[item['supernode_gpus']] = item['per_supernode_remote_bytes']
        supernodes = []
        for size in scenario['supernode_sizes']:
            positive_int(size, 'supernode size')
            if gpus % size:
                raise ValueError('supernode size must divide the cluster')
            nominal = size * nic
            egress = nominal / ratio
            row = dict(supernode_gpus=size, supernodes=gpus // size,
                       nominal_nic_egress_bytes_per_second_exact=str(nominal),
                       oversubscribed_egress_bytes_per_second_exact=str(egress),
                       egress_per_gpu_bytes_per_second_exact=str(egress / size),
                       per_supernode_remote_bytes=exported.get(size),
                       remote_seconds_at_nominal=None, remote_seconds_at_oversubscribed=None)
            if size in exported:
                row['remote_seconds_at_nominal'] = exported[size] / float(nominal)
                row['remote_seconds_at_oversubscribed'] = exported[size] / float(egress)
            supernodes.append(row)
        supernodes = dict(scenario_file=supernode_scenario, gpus=gpus, nic_bytes_per_second=scenario['nic_Bps'],
                          results_file='results/supernode-scaling-book.json' if exported else None, rows=supernodes)
    summary = dict(radix=radix, oversubscription=str(ratio), leaf_downlinks=down, leaf_uplinks=up)
    for row in rows:
        summary[f"tier{row['tiers']}_endpoints"] = row['endpoints']
        summary[f"tier{row['tiers']}_total_switches"] = row['total_switches']
        summary[f"tier{row['tiers']}_bisection_bytes_per_second"] = float(Fraction(row['bisection_bytes_per_second_exact']))
        summary[f"tier{row['tiers']}_bisection_fraction_of_nonblocking"] = row['bisection_fraction_of_nonblocking_exact']
    if cuts:
        summary['partition_endpoints'] = partition_endpoints
        summary['partition_cut_bytes_per_second'] = float(Fraction(cuts[0]['cut_bytes_per_second_exact']))
        summary['partition_cut_bytes_per_second_per_endpoint'] = float(Fraction(cuts[0]['cut_bytes_per_second_per_endpoint_exact']))
    if supernodes:
        for row in supernodes['rows']:
            summary[f"supernode{row['supernode_gpus']}_egress_bytes_per_second"] = float(Fraction(row['oversubscribed_egress_bytes_per_second_exact']))
    return dict(leaf=dict(radix=radix, oversubscription_exact=str(ratio), downlinks=down, uplinks=up,
                          link_bytes_per_second_exact=str(link)),
                tiers=rows, partition_cuts=cuts, supernode_egress=supernodes, summary=summary)


def _rail(rails, servers, nic_bytes_per_second, startup_ns, pairing, model, gradient_dtype):
    positive_int(rails, 'rails'); positive_int(servers, 'servers'); positive_int(startup_ns, 'startup_ns', allow_zero=True)
    nic = exact(nic_bytes_per_second, 'nic_bytes_per_second')
    if servers != 2:
        raise ValueError('The rail example is the two-server hierarchical AllReduce')
    if pairing not in ('aligned', 'shifted'):
        raise ValueError('pairing must be aligned (rank i <-> rank i) or shifted (rank i <-> rank i+1 mod rails)')
    if gradient_dtype not in ('FP32', 'BF16'):
        raise ValueError('gradient_dtype must be FP32 or BF16')
    config = model_config(model)
    tensor = next(w for w in qwen3.weights(config) if w.name == 'model.layers.{layer}.mlp.gate_proj.weight')
    width = {'FP32': 4, 'BF16': 2}[gradient_dtype]
    gradient = prod(tensor.shape) * width
    if gradient % (2 * rails):
        raise ValueError('gradient must divide into whole shards and halves without padding')
    shard = gradient // rails
    half = shard // 2
    pairs = []
    spine_bytes = 0
    for rank in range(rails):
        peer = rank if pairing == 'aligned' else (rank + 1) % rails
        rail_out, rail_in = rank, peer
        crosses = rail_out != rail_in
        spine_bytes += shard if crosses else 0
        pairs.append(dict(server0_rank=rank, server1_rank=peer, nic_rail_server0=rail_out, nic_rail_server1=rail_in,
                          crosses_rails=crosses, reduce_scatter_bytes_each_direction=half,
                          all_gather_bytes_each_direction=half, bytes_each_direction=shard))
    per_rail_seconds = shard / nic + 2 * Fraction(startup_ns, 10**9)
    single = rails * shard / nic + 2 * Fraction(startup_ns, 10**9)
    return dict(sources=provenance(model),
                gradient=dict(parameter='model.layers.0.mlp.gate_proj.weight', shape=list(tensor.shape),
                              bytes_per_element=width, bytes=gradient, local_ranks=rails, shard_bytes=shard),
                pairs=pairs,
                summary=dict(rails=rails, servers=servers, pairing=pairing,
                             cross_server_rounds=2, bytes_per_rail_each_direction=shard,
                             bytes_all_rails_each_direction=rails * shard,
                             spine_crossing_bytes=spine_bytes,
                             per_rail_seconds_exact=str(per_rail_seconds),
                             single_nic_counterfactual_seconds_exact=str(single),
                             rail_parallel_speedup_exact=str(single / per_rail_seconds)))


def _in_network(nic_bytes_per_second, startup_ns, results_glob, server_counts):
    positive_int(startup_ns, 'startup_ns', allow_zero=True)
    default_nic = exact(nic_bytes_per_second, 'nic_bytes_per_second')
    rows = []
    for path in sorted((PROJECT / 'results').glob(results_glob)):
        result = json.loads(path.read_text())
        if result.get('calculation') != 'hierarchical-gradient' or result['scenario'].get('algorithm') != 'hierarchical':
            continue
        ranks = len(result['rank_mapping'])
        servers = len({m['server'] for m in result['rank_mapping']})
        local = ranks // servers
        gradient = result['gradient']['bytes_per_rank']
        if gradient % local:
            raise ValueError('Gradient must divide into whole local shards')
        shard = gradient // local
        nic = default_nic
        for resource in result.get('resources', []):
            if 'nic' in resource['resource'] and resource['resource'].endswith('.tx'):
                nic = Fraction(resource['bandwidth_bytes_per_second'])
                break
        cross = next((s for s in result['stages'] if 'cross_server' in s['stage']), None)
        sharp_seconds = shard / nic + Fraction(startup_ns, 10**9)
        row = dict(result_file=str(path.relative_to(PROJECT)), gradient_dtype=result['scenario']['gradient_dtype'],
                   nics_per_server=result['scenario']['nics_per_server'], ranks=ranks, servers=servers,
                   local_ranks=local, gradient_bytes_per_rank=gradient, shard_bytes=shard,
                   nic_bytes_per_second_exact=str(nic),
                   switch_reduce=dict(rounds=1, send_bytes_per_rank=shard, receive_bytes_per_rank=shard,
                                      cross_server_bytes=shard * ranks,
                                      per_nic_seconds_exact=str(sharp_seconds)),
                   hierarchical=None)
        if cross:
            hier_seconds = Fraction(cross['barrier_lower_seconds_exact'])
            row['hierarchical'] = dict(stage=cross['stage'], rounds=cross['rounds'],
                                       cross_server_send_bytes=cross['remote_send_bytes'],
                                       barrier_lower_seconds_exact=cross['barrier_lower_seconds_exact'],
                                       total_remote_send_bytes=result['summary']['remote_send_bytes'],
                                       total_rounds=result['summary']['rounds'],
                                       serial_barrier_lower_seconds_exact=result['summary']['serial_barrier_lower_seconds_exact'])
            row['switch_reduce']['cross_server_bytes_ratio_to_hierarchical_exact'] = str(Fraction(shard * ranks, cross['remote_send_bytes']))
            row['switch_reduce']['seconds_ratio_to_hierarchical_exact'] = str(sharp_seconds / hier_seconds) if hier_seconds else None
        # Generalize the cross-server phase to S servers: ring AllReduce among the S owners of one
        # shard moves 2(S-1)/S x shard per NIC in 2(S-1) rounds; the switch reduction stays at shard, 1 round.
        sweep = []
        for count in server_counts:
            positive_int(count, 'server count')
            ring_bytes = Fraction(2 * (count - 1), count) * shard
            ring_rounds = 2 * (count - 1)
            ring_seconds = ring_bytes / nic + ring_rounds * Fraction(startup_ns, 10**9)
            sweep.append(dict(servers=count, ranks=count * local,
                              ring_per_nic_bytes_exact=str(ring_bytes), ring_rounds=ring_rounds,
                              ring_seconds_exact=str(ring_seconds), ring_seconds=float(ring_seconds),
                              switch_per_nic_bytes=shard, switch_rounds=1,
                              switch_seconds_exact=str(sharp_seconds), switch_seconds=float(sharp_seconds),
                              switch_over_ring_exact=str(sharp_seconds / ring_seconds)))
        row['servers_sweep'] = sweep
        rows.append(row)
    summary = dict(results_found=len(rows))
    for row in rows:
        tag = f"{row['gradient_dtype'].lower()}_nic{row['nics_per_server']}"
        summary[f'{tag}_switch_cross_server_bytes'] = row['switch_reduce']['cross_server_bytes']
        summary[f'{tag}_switch_per_nic_seconds'] = float(Fraction(row['switch_reduce']['per_nic_seconds_exact']))
        if row['hierarchical']:
            summary[f'{tag}_hierarchical_cross_server_bytes'] = row['hierarchical']['cross_server_send_bytes']
            summary[f'{tag}_hierarchical_cross_server_seconds'] = float(Fraction(row['hierarchical']['barrier_lower_seconds_exact']))
            summary[f'{tag}_hierarchical_cross_server_rounds'] = row['hierarchical']['rounds']
        summary[f'{tag}_switch_over_ring_at_{row["servers_sweep"][-1]["servers"]}_servers'] = float(Fraction(row['servers_sweep'][-1]['switch_over_ring_exact']))
    return dict(results_glob=results_glob, rows=rows, results_found=len(rows), summary=summary)


def calculate(mode='clos', radix=64, oversubscription='1', tiers=(2, 3), link_bytes_per_second=50 * 10**9,
              partition_endpoints=1024, supernode_scenario='scenarios/supernode-scaling-example.json',
              rails=8, servers=2, nic_bytes_per_second=50 * 10**9, startup_ns=2000, pairing='aligned',
              model='qwen3-8b', gradient_dtype='FP32', results_glob='gradient-*.json', server_counts=(2, 4, 8, 16, 32),
              input_sources=None):
    inputs = {k: v for k, v in locals().items() if k != 'input_sources'}
    sources = _sources(inputs, input_sources)
    if mode not in ('clos', 'rail', 'in_network'):
        raise ValueError('mode must be clos, rail or in_network')
    body = (_clos(radix, oversubscription, list(tiers), link_bytes_per_second, partition_endpoints, supernode_scenario)
            if mode == 'clos' else _rail(rails, servers, nic_bytes_per_second, startup_ns, pairing, model, gradient_dtype)
            if mode == 'rail' else _in_network(nic_bytes_per_second, startup_ns, results_glob, list(server_counts)))
    assumptions = {
        'clos': [
            'k 端口交换机的折叠 Clos：叶层每台 d 下行、u 上行，d/u 为声明的超额订阅比；上层保持对叶上行不阻塞。二层为叶—脊，三层沿用 fat-tree 论文的 pod 结构（每 pod k/2 台边缘交换机）。',
            '半分带宽按顶层链路计：所有叶上行数的一半乘每链路速率；不模拟具体流的路由、ECMP 冲突或队列。',
            '分区割集只对占用整数个叶（或 pod）的分区成立；不足一叶时按向上取整计入整叶上行。每端点份额 = 割集/端点数。',
            '超节点出口取 supernode-scaling 场景的每卡 NIC 速率乘卡数，再除以超额订阅比；跨域字节读取已有结果文件，本模块不重算梯度同步。',
        ],
        'rail': [
            '两台服务器各 8 卡，每卡一张网卡接到对应轨道（rail）的叶交换机；分层 AllReduce 的跨服务器阶段是两 rank 的 ReduceScatter + AllGather，各发送半个分片。',
            '梯度取 Qwen3-8B 第一层 gate_proj 一份参数梯度（与 hierarchical-gradient 相同的张量），FP32 时 192 MiB；分片 = 梯度/本地 rank 数。',
            'aligned 配对时每对只经过自己的轨道叶交换机；shifted 配对时每对跨两个轨道，全部字节须经脊层。时间只计网卡串行发送与每轮启动，不含本地 NVLink 阶段、传播或交换机排队。',
        ],
        'in_network': [
            '交换机侧归约（SHARP 类）：本地 ReduceScatter 后每 rank 把自己的分片发给交换机一次、收回归约结果一次，跨服务器阶段只有一轮；本地 RS/AG 阶段与分层方案相同，不重复计。',
            '对照数据直接读取 results/ 中的 hierarchical-gradient 结果（跨服务器阶段的轮数、字节与屏障下界），本模块不重算环。网卡速率取该结果声明的 nic0.tx 速率。',
            '不声称交换机归约引擎的吞吐、精度或可用性；时间只是每网卡分片串行发送加一次启动的下界。',
            'servers_sweep 把跨服务器阶段推广到 S 台服务器：同一分片的 S 个持有者做环形 AllReduce，每网卡 2(S-1)/S×分片、2(S-1) 轮；交换机归约保持 1 个分片、1 轮。两台服务器时字节相同，只省一轮启动；服务器越多差距越大。',
        ],
    }[mode]
    return dict(schema_version=1, calculation='clos-cut', scenario=inputs, declared_input_sources=sources,
                mode=mode, **body, assumptions=assumptions)
