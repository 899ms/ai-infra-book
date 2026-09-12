#!/usr/bin/env python3
"""Busiest-card load relative to the mean as the EP group grows; row counts only, no GPU measurement implied."""
import argparse
import json
import random
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def hot_case(s, ep):
    """One hot expert, the rest equal: exact fractions."""
    E, total, hot = s['experts'], s['tokens']*s['top_k'], s['hot_expert_rows']
    per_card = E//ep
    other = Fraction(total-hot, E-1)
    busiest = hot+(per_card-1)*other
    mean = Fraction(total, ep)
    return {'experts_per_card': per_card, 'mean_rows': mean, 'busiest_rows': busiest,
            'other_expert_rows': other, 'ratio': busiest/mean}


def random_ratios(s, rng):
    """Uniform top-k without replacement, contiguous expert placement; the same batches serve every EP size."""
    E, n, k = s['experts'], s['tokens'], s['top_k']
    ratios = {ep: [] for ep in s['ep_sizes']}
    for _ in range(s['trials']):
        rows = [0]*E
        for _ in range(n):
            for e in rng.sample(range(E), k):
                rows[e] += 1
        for ep in s['ep_sizes']:
            m = E//ep
            ratios[ep].append(max(sum(rows[c*m:(c+1)*m]) for c in range(ep))/(n*k/ep))
    out = {}
    for ep, r in ratios.items():
        r.sort()
        out[ep] = {'mean_ratio': sum(r)/len(r), 'p99_ratio': r[min(len(r)-1, int(.99*len(r)))]}
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario', type=Path, default=ROOT/'calculations/scenarios/ep-scale-skew-example.json')
    parser.add_argument('--output-dir', type=Path, default=ROOT/'calculations/results')
    args = parser.parse_args()
    s = json.loads(args.scenario.read_text())
    if s['experts'] % max(s['ep_sizes']) or s['tokens']*s['top_k'] <= s['hot_expert_rows']:
        raise ValueError('EP sizes must divide the expert count; hot rows must be below the total')
    rand = random_ratios(s, random.Random(s['seed']))
    rows = []
    for ep in s['ep_sizes']:
        h = hot_case(s, ep)
        r = rand[ep]
        rows.append({'ep': ep, 'experts_per_card': h['experts_per_card'],
                     'mean_rows': float(h['mean_rows']), 'hot_busiest_rows': float(h['busiest_rows']),
                     'hot_ratio': float(h['ratio']), 'hot_ratio_exact': str(h['ratio']),
                     'hot_other_expert_rows': float(h['other_expert_rows']),
                     'random_mean_ratio': r['mean_ratio'], 'random_p99_ratio': r['p99_ratio']})
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir/'ep-scale-skew-book.json').write_text(
        json.dumps({'assumptions': s['assumptions'], 'scenario': s, 'results': rows}, ensure_ascii=False, indent=2)+'\n')
    lines = ['# EP 规模与最忙卡负载', '', '运行：`python3 calculations/ep_scale_skew.py`。输入见 [固定场景](../scenarios/ep-scale-skew-example.json)。', '',
             *s['assumptions'], '',
             '| EP | 每卡专家数 | 每卡平均行数 | 热点：最忙卡行数 | 热点：最忙÷平均 | 随机：最忙÷平均（均值） | 随机：99 分位 |',
             '|---:|---:|---:|---:|---:|---:|---:|']
    for r in rows:
        lines.append(f"| {r['ep']} | {r['experts_per_card']} | {r['mean_rows']:.0f} | {r['hot_busiest_rows']:.1f} | {r['hot_ratio']:.2f} | {r['random_mean_ratio']:.2f} | {r['random_p99_ratio']:.2f} |")
    (args.output_dir/'ep-scale-skew-book.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
