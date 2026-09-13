#!/usr/bin/env python3
"""Fixed-GPU decode of DeepSeek V4.1 Flash: supernode size, ROM weights and SRAM-only KV.

Section 6.7.4. One inference instance per supernode; attention data-parallel,
routed experts expert-parallel across the instance. Numbers come from the pinned
checkpoint headers, the kv-comparison and v41-forward results, hardware.json and
an excerpt of the OpenTallas V4.1 roofline study.
"""
import argparse
import json
import math
import struct
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'calculations/src'))
from infra_calc.sources import model_config, read_source  # noqa: E402
from infra_calc.topics import kv_comparison, v41_forward  # noqa: E402


def checkpoint_groups(model):
    """Bytes of the pinned checkpoint by placement group, from the safetensors headers."""
    index = json.loads(read_source(f'sources/{model}/model.safetensors.index.json'))
    groups, embed = Counter(), 0
    for shard in sorted(set(index['weight_map'].values())):
        raw = read_source(f'sources/{model}/headers/{shard}.header.bin')
        if struct.unpack('<Q', raw[:8])[0] != len(raw) - 8:
            raise ValueError('Safetensors header length mismatch')
        for name, t in json.loads(raw[8:]).items():
            if name == '__metadata__':
                continue
            start, end = t['data_offsets']
            if name.startswith('mtp.'):
                group = 'dspark'
            elif name.startswith(('vision.', 'aligner.', 'image_')):
                group = 'vision'
            elif '.engram.' in name:
                group = 'engram'
            elif '.ffn.experts.' in name:
                group = 'routed_expert'
            else:
                group = 'replicated'
            groups[group] += end - start
            if name == 'embed.weight':
                embed = end - start
    if not embed:
        raise ValueError('embedding table not found')
    return dict(groups), embed


def all_to_all_s(alpha, bytes_out, link_Bps):
    return alpha + bytes_out / link_Bps


def step_time(c, m, S, B, remote=None):
    """Decode step for one instance of S cards serving B sessions; n is the busiest card's share."""
    n = math.ceil(B / S)
    hw = m['hw']
    coverage = 1 - (1 - m['experts_per_token'] / m['experts']) ** B
    per_layer_expert_bytes = max(m['expert_bytes'], m['experts'] / S * m['expert_bytes'] * coverage)
    weight_bytes = m['replicated_read_bytes'] + m['layers'] * per_layer_expert_bytes
    kv_bytes = n * m['kv_read_bytes']
    memory_s = (weight_bytes + kv_bytes) / hw['hbm_Bps']
    compute_s = n * m['flops_per_token'] / hw['peak_Fps']
    local_s = max(memory_s, compute_s)
    vector = n * m['experts_per_token'] * m['hidden'] * c['activation_bytes']
    if remote is None:
        comm_one = all_to_all_s(c['local_alpha_s'], vector * (1 - 1 / S), c['local_Bps'])
    else:
        leaving_server = 1 - remote / S
        comm_one = all_to_all_s(c['remote_alpha_s'], vector * leaving_server, c['nic_Bps'])
    comm_s = 2 * m['layers'] * comm_one
    return dict(sessions_per_card=n, instance_batch=B, expert_coverage=coverage,
                weight_bytes=weight_bytes, kv_bytes=kv_bytes, memory_s=memory_s, compute_s=compute_s,
                local_s=local_s, comm_s=comm_s, step_s=local_s + comm_s)


def capacity_sessions(c, m, S, engram_on_host=False):
    hw = m['hw']
    engram = 0 if engram_on_host else m['engram_bytes']
    resident = m['replicated_bytes'] + (m['routed_bytes'] + engram) / S + c['workspace_bytes']
    free = hw['capacity_bytes'] - resident
    return dict(weights_per_card_bytes=resident - c['workspace_bytes'], free_bytes=free,
                sessions=max(0, math.floor(free / m['kv_resident_bytes'])))


def evaluate(c, m, S, remote=None, label=None, engram_on_host=False):
    cap = capacity_sessions(c, m, S, engram_on_host)
    best = None
    for n in range(1, cap['sessions'] + 1):
        t = step_time(c, m, S, n * S, remote)
        if t['step_s'] > c['tpot_s']:
            break
        best = t
    if best is None:
        raise ValueError(f'no feasible session count for supernode {S}')
    binding = 'capacity' if best['sessions_per_card'] == cap['sessions'] else 'tpot'
    single = step_time(c, m, S, 1, remote)
    return dict(label=label or f'{S} 卡超节点', supernode_gpus=S, instances=c['gpus_total'] // S,
                remote_servers=None if remote is None else S // remote, **cap,
                served=best, binding=binding, tokens_per_s_per_gpu=best['sessions_per_card'] / best['step_s'],
                tokens_per_s_total=best['sessions_per_card'] / best['step_s'] * c['gpus_total'],
                batch1=single, batch1_per_user_tokens_s=1 / single['step_s'])


def load_model(c):
    model = c['model']
    cfg = model_config(model)
    cfg = cfg.get('text_config', cfg)
    groups, embed = checkpoint_groups(model)
    hw_row = next(d for d in json.loads((ROOT / 'calculations/configs/hardware.json').read_text())['devices'] if d['id'] == c['gpu_id'])
    peak = next(r for r in hw_row['peak_rates'] if r['input_precision'] in ('BF16', 'FP16') and r['sparsity'] == 'dense' and r['execution_unit'] == 'tensor')
    hw = dict(name=hw_row['name'], capacity_bytes=hw_row['memory']['nominal_capacity'] * 1e9,
              hbm_Bps=hw_row['memory']['bandwidth_bytes_per_second'], peak_Fps=peak['tera_ops_per_second'] * 1e12)
    kv = next(r for r in kv_comparison.calculate(c['context_tokens'], 1)['rows'] if r['model'] == model)
    forward = v41_forward.calculate(1, 1, c['context_tokens'], 'ced', 'candidate')
    layers, experts, k = cfg['num_hidden_layers'], cfg['n_routed_experts'], cfg['num_experts_per_tok']
    return dict(
        hw=hw, layers=layers, experts=experts, experts_per_token=k, hidden=cfg['hidden_size'],
        checkpoint_bytes=sum(groups.values()), groups=groups,
        replicated_bytes=groups['replicated'], routed_bytes=groups['routed_expert'], engram_bytes=groups['engram'],
        replicated_read_bytes=groups['replicated'] - embed, embedding_bytes=embed,
        expert_bytes=groups['routed_expert'] / (layers * experts),
        kv_resident_bytes=kv['global_history_bytes'] + kv['local_window_bytes'],
        kv_read_bytes=kv['decode_selected_history_read_bytes'],
        flops_per_token=forward['summary']['matrix_flops'],
        forward_scenario=forward['scenario'])


def rom_rows(c, m):
    ex = json.loads((ROOT / c['opentallas']['excerpt']).read_text())
    balance = ex['technology']['efficiencies']['stage_balance']['value']
    rows = []
    for d in c['opentallas']['designs']:
        p = next(p for p in ex['points'] if p['design'].split('/')[-1] == d['name'] and p['batch_size'] == 1)
        t = p['component_times_s']
        if 'share one memory system' in p['overlap_rule']:
            store = t['weight_read'] + t['kv_read']
        else:
            store = max(t['weight_read'], t['kv_read'])
        service = max(store, t['compute']) / (balance if p['device_count'] > 1 else 1)
        token_s = service + t['link_latency'] + t['layer_fixed_latency']
        if not math.isclose(1 / token_s, p['per_user_tokens_s'], rel_tol=1e-6):
            raise ValueError(f"composition rule does not reproduce {d['name']}")
        rows.append(dict(label=d['label'], design=d['name'], devices=p['device_count'], weight_read_s=t['weight_read'], kv_read_s=t['kv_read'],
                         compute_s=t['compute'], storage_compute_s=service, link_s=t['link_latency'], fixed_s=t['layer_fixed_latency'],
                         token_s=token_s, per_user_tokens_s=p['per_user_tokens_s'], link_share=t['link_latency'] / token_s,
                         resident_sessions=p['max_resident_users'], kv_capacity_bytes=p['kv_capacity_bytes'], kv_store=p['kv_store'],
                         hops=p['hop_breakdown'], binding=p['binding_constraint']))
    return dict(commit=ex['source']['commit'], context_tokens=ex['model_summary']['context_tokens'],
                engaged_weight_bytes=ex['points'][0]['engaged_weight_bytes'], rows=rows,
                sram_only_wafers=math.ceil(m['checkpoint_bytes'] / c['sram_only_bytes']))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--scenario', type=Path, default=ROOT / 'calculations/scenarios/supernode-inference-example.json')
    p.add_argument('--output-dir', type=Path, default=ROOT / 'calculations/results')
    args = p.parse_args()
    c = json.loads(args.scenario.read_text())
    m = load_model(c)
    results = [evaluate(c, m, S) for S in c['supernode_sizes']]
    ep = c['rdma_case']['ep_gpus']
    rdma = evaluate(c, m, ep, remote=c['server_gpus'], label=f"{ep} 卡跨 {ep // c['server_gpus']} 台服务器")
    engram_host = evaluate(c, m, c['supernode_sizes'][0], label=f"{c['supernode_sizes'][0]} 卡超节点，Engram 表在主机内存", engram_on_host=True)
    rom = rom_rows(c, m)
    # H100 row of the ROM comparison: the 8-card supernode at batch 1.
    h100 = results[0]['batch1']
    gpu_row = dict(label=f"8 张 {m['hw']['name']}，权重在 HBM", weight_read_s=(h100['weight_bytes']) / m['hw']['hbm_Bps'], kv_read_s=h100['kv_bytes'] / m['hw']['hbm_Bps'],
                   compute_s=h100['compute_s'], storage_compute_s=h100['local_s'], link_s=h100['comm_s'], fixed_s=0.0, token_s=h100['step_s'],
                   per_user_tokens_s=1 / h100['step_s'], link_share=h100['comm_s'] / h100['step_s'], resident_sessions=results[0]['sessions'] * 8, kv_store='hbm')
    out = dict(assumptions=c['assumptions'], model=m, results=results, rdma=rdma, engram_host=engram_host, rom=rom, gpu_row=gpu_row)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / 'supernode-inference-book.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    L = ['# 固定 256 卡 decode 与超节点大小：DeepSeek V4.1 Flash', '',
         '运行：`python3 calculations/supernode_inference.py`。输入见 [固定场景](../scenarios/supernode-inference-example.json)。', '', *c['assumptions'], '',
         '## 模型与硬件输入', '',
         f"- checkpoint 共 {m['checkpoint_bytes']/1e9:.2f} GB：每卡复制部分 {m['replicated_bytes']/1e9:.2f} GB（其中嵌入表 {m['embedding_bytes']/1e9:.2f} GB 只查表），路由专家 {m['routed_bytes']/1e9:.2f} GB，Engram {m['engram_bytes']/1e9:.2f} GB，另有视觉与 DSpark 不参与文本 decode。",
         f"- 每层每个专家 {m['expert_bytes']/1e6:.2f} MB；{m['layers']} 层，每层 {m['experts']} 个路由专家，每 token 选 {m['experts_per_token']} 个；隐藏维 {m['hidden']}。",
         f"- {c['context_tokens']} 上下文：每会话驻留 KV {m['kv_resident_bytes']/1e6:.2f} MB，每 token 读取 {m['kv_read_bytes']/1e6:.2f} MB；每 token 矩阵运算 {m['flops_per_token']/1e9:.2f} GFLOP。",
         f"- {m['hw']['name']}：{m['hw']['capacity_bytes']/1e9:.0f} GB，{m['hw']['hbm_Bps']/1e9:.0f} GB/s，{m['hw']['peak_Fps']/1e12:.1f} TFLOP/s。",
         f"- 每步每卡读取的复制权重 {m['replicated_read_bytes']/1e9:.2f} GB；batch 1 的关键路径权重 {results[0]['batch1']['weight_bytes']/1e9:.2f} GB。",
         '- 每卡分到的路由专家与 Engram：' + '；'.join(f"{r['supernode_gpus']} 卡 {m['routed_bytes']/r['supernode_gpus']/1e9:.1f} + {m['engram_bytes']/r['supernode_gpus']/1e9:.1f} GB" for r in results) + '。', '',
         '## 超节点大小与每卡吞吐（TPOT 50 ms）', '',
         '| 部署 | 每卡权重 GB | 每卡可容纳会话 | 每卡会话数 | 实例 batch | 权重读取 ms | KV 读取 ms | 计算 ms | 通信 ms | 步时间 ms | 限制 | 每卡 token/s | 256 卡合计 token/s | batch 1 单用户 token/s |',
         '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|']
    for r in results + [rdma, engram_host]:
        s = r['served']
        L.append(f"| {r['label']} | {r['weights_per_card_bytes']/1e9:.1f} | {r['sessions']} | {s['sessions_per_card']} | {s['instance_batch']} | {s['weight_bytes']/m['hw']['hbm_Bps']*1e3:.2f} | {s['kv_bytes']/m['hw']['hbm_Bps']*1e3:.2f} | {s['compute_s']*1e3:.2f} | {s['comm_s']*1e3:.2f} | {s['step_s']*1e3:.2f} | {r['binding']} | {r['tokens_per_s_per_gpu']:.0f} | {r['tokens_per_s_total']:.0f} | {r['batch1_per_user_tokens_s']:.0f} |")
    L += ['', f"## 权重固定为 ROM（OpenTallas commit {rom['commit'][:7]}，{rom['context_tokens']} 上下文，batch 1）", '',
          f"每 token 参与计算的权重 {rom['engaged_weight_bytes']/1e9:.2f} GB。把 checkpoint 全部放入 {c['sram_only_bytes']/1e9:.0f} GB 的片上 SRAM 需要 {rom['sram_only_wafers']} 片晶圆。", '',
          '| 机器 | 权重读取 μs | KV 读取 μs | 计算 μs | 存储与计算取较慢者 μs | 集合通信 μs | 固定延迟 μs | 每 token μs | 通信占比 | 单用户 token/s | 驻留会话 |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for r in [gpu_row] + rom['rows']:
        L.append(f"| {r['label']} | {r['weight_read_s']*1e6:.1f} | {r['kv_read_s']*1e6:.1f} | {r['compute_s']*1e6:.1f} | {r['storage_compute_s']*1e6:.1f} | {r['link_s']*1e6:.1f} | {r['fixed_s']*1e6:.1f} | {r['token_s']*1e6:.1f} | {r['link_share']*100:.0f}% | {r['per_user_tokens_s']:.0f} | {r['resident_sessions']:.0f} |")
    L += ['', '通信路径：']
    for r in rom['rows']:
        L.append(f"- {r['label']}：{r['hops']}")
    (args.output_dir / 'supernode-inference-book.md').write_text('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
