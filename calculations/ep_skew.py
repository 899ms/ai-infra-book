#!/usr/bin/env python3
"""Deterministic EP traffic/compute lower bounds; no GPU measurement implied."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def evaluate(case):
    a = case['assignments']
    if not a or not a[0] or any(len(row) != len(a[0]) for row in a):
        raise ValueError('assignments must be a nonempty rectangular matrix')
    if any(not isinstance(v, int) or v < 0 for row in a for v in row):
        raise ValueError('assignment counts must be nonnegative integers')
    rows = [sum(row) for row in a]
    cols = [sum(row[j] for row in a) for j in range(len(a[0]))]
    total = sum(rows)
    if total != case['tokens'] * case['top_k'] or total == 0:
        raise ValueError('assignment count must equal tokens * top_k > 0')
    for key in ('dispatch_bytes', 'combine_bytes', 'endpoint_Bps', 'cut_Bps', 'compute_Fps', 'flops_per_assignment'):
        if case[key] <= 0:
            raise ValueError(f'{key} must be positive')
    def phase(size, sends, receives):
        bounds = {'send_s': max(sends)*size/case['endpoint_Bps'],
                  'receive_s': max(receives)*size/case['endpoint_Bps'],
                  'cut_s': total*size/case['cut_Bps']}
        return dict(bounds, lower_s=max(bounds.values()), total_bytes=total*size)
    dispatch = phase(case['dispatch_bytes'], rows, cols)
    combine = phase(case['combine_bytes'], cols, rows)
    compute = [v*case['flops_per_assignment']/case['compute_Fps'] for v in cols]
    d, c, r = dispatch['lower_s'], max(compute), combine['lower_s']
    # Two equal microbatches on three independent resources: one pass through every stage plus the longest stage once more.
    pipeline = (d+c+r+max(d, c, r))/2
    # Factor by which dispatch and combine (or compute) must both stretch before the pipeline stops beating the barrier.
    comm_stretch = (2*(d+r)+c)/(d+r+max(d, r))
    if comm_stretch*max(d, r) < c:
        comm_stretch = 2
    compute_stretch = (d+r+2*c)/(2*c)
    if compute_stretch*c < max(d, r):
        compute_stretch = (min(d, r)+2*c)/c
    return {'name': case['name'], 'send_assignments': rows, 'expert_assignments': cols,
            'expert_skew': max(cols)/(total/len(cols)),
            'dispatch': dispatch, 'combine': combine, 'compute_s': compute,
            'barrier_lower_s': dispatch['lower_s']+max(compute)+combine['lower_s'],
            'resource_batch_rate_upper': 1/max(dispatch['lower_s'], max(compute), combine['lower_s']),
            'two_microbatch_pipeline_s': pipeline,
            'pipeline_break_even_comm_stretch': comm_stretch,
            'pipeline_break_even_compute_stretch': compute_stretch}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario', type=Path, default=ROOT/'calculations/scenarios/ep-skew-example.json')
    parser.add_argument('--output-dir', type=Path, default=ROOT/'calculations/results')
    args=parser.parse_args()
    scenario=json.loads(args.scenario.read_text())
    results=[evaluate(dict(scenario['common'], **case)) for case in scenario['cases']]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir/'ep-skew-book.json').write_text(json.dumps({'assumptions':scenario['assumptions'],'results':results},ensure_ascii=False,indent=2)+'\n')
    lines=['# 大 EP 与专家分离的偏斜算例','', '运行：`python3 calculations/ep_skew.py`。输入见 [固定场景](../scenarios/ep-skew-example.json)。','', *scenario['assumptions'], '', '| 场景 | 专家 skew | dispatch 下界 ms | 计算下界 ms | combine 下界 ms | 阶段屏障总下界 ms |', '|---|---:|---:|---:|---:|---:|']
    for r in results:
        lines.append(f"| {r['name']} | {r['expert_skew']:.2f} | {r['dispatch']['lower_s']*1000:.3f} | {max(r['compute_s'])*1000:.3f} | {r['combine']['lower_s']*1000:.3f} | {r['barrier_lower_s']*1000:.3f} |")
    lines.extend(['', '两个等大微批次在三项独立资源上流水：总时间为单个微批次三段之和再加一次最长段；打平倍数是 dispatch 与 combine（或计算）同时被拉长多少倍时流水不再快于整批屏障。', '', '| 场景 | 整批屏障 ms | 两微批流水 ms | 通信打平倍数 | 计算打平倍数 |', '|---|---:|---:|---:|---:|'])
    for r in results:
        lines.append(f"| {r['name']} | {r['barrier_lower_s']*1000:.3f} | {r['two_microbatch_pipeline_s']*1000:.3f} | {r['pipeline_break_even_comm_stretch']:.3f} | {r['pipeline_break_even_compute_stretch']:.3f} |")
    (args.output_dir/'ep-skew-book.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
