#!/usr/bin/env python3
"""实验 9-2：A100＋H20 的 PD 分离。

分开 prefill 和 decode 的收益何时被抵消？以 A100 80GB SXM 做 prefill、
H20 SXM5 96GB 做 decode，比较共置、同构 PD、异构 PD 与角色对换；
沿同一 Qwen3-8B 扫描输入长度、输出长度、缓存命中、到达率与池规模，
分别评价首 token、逐 token 延迟及费用。

本实验不重算：由 `calculations/calc.py pd-pool` 现场生成。
阶段能力由硬件表峰值乘 50% 效率、经 Qwen3-8B 逐算子账的 Roofline 推出；
50% 以第 8 章 RTX PRO 6000 批量 64 的实测输出间隔校准。
"""
import json
import os
import subprocess
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
CALC = os.path.join(ROOT, 'calculations', 'calc.py')
RESULTS = os.path.join(HERE, 'results')

# 每张卡按硬件表峰值 ×50% 推出阶段能力；decode 批量 32。A100 算力强，H20 带宽强。
A100 = dict(name='A100', device='a100-80gb-sxm', decode_batch=32, compute_efficiency=0.5, bandwidth_efficiency=0.5)
H20 = dict(name='H20', device='h20-sxm5-96gb', decode_batch=32, compute_efficiency=0.5, bandwidth_efficiency=0.5)
LINK = 25_000_000_000

LAYOUTS = [
    ('共置（8 张 A100 都做两件事）', [dict(A100, count=8)]),
    ('同构 PD（A100 4＋4）', [dict(A100, count=8)]),
    ('异构 PD（A100 4 做 prefill，H20 4 做 decode）', [dict(A100, count=4), dict(H20, count=4)]),
    ('全 H20（8 张）', [dict(H20, count=8)]),
]

SCANS = [
    ('输入 8K／输出 1024／无命中', 8192, 1025, 0, '7/2'),
    ('输入 8K／输出 128／无命中', 8192, 129, 0, '7/2'),
    ('输入 8K／输出 4096／无命中', 8192, 4097, 0, '7/2'),
    ('输入 8K／输出 1024／命中 6K 前缀', 8192, 1025, 6144, '7/2'),
    ('输入 2K／输出 1024／无命中', 2048, 1025, 0, '7/2'),
    ('输入 32K／输出 1024／无命中', 32768, 1025, 0, '1'),
]


def main() -> int:
    os.makedirs(RESULTS, exist_ok=True)
    rows = []
    for li, (layout_name, workers) in enumerate(LAYOUTS):
        for si, (scan_name, prompt, outputs, cached, arrival) in enumerate(SCANS):
            cfg = dict(model='qwen3-8b', prompt_tokens=prompt, output_tokens=outputs,
                       cached_prefix_tokens=cached, workers=workers,
                       network_bytes_per_second=LINK,
                       arrival_requests_per_second=arrival)
            ipath = os.path.join(RESULTS, 'input-%d-%d.json' % (li, si))
            opath = os.path.join(RESULTS, 'pool-%d-%d.json' % (li, si))
            json.dump(cfg, open(ipath, 'w'), indent=1)
            proc = subprocess.run([sys.executable, CALC, 'pd-pool', '--inputs', ipath,
                                   '--format', 'json', '--output', opath],
                                  capture_output=True, text=True)
            if proc.returncode != 0:
                rows.append(dict(layout=layout_name, scan=scan_name,
                                 error=(proc.stderr.strip().splitlines() or [''])[-1]))
                continue
            s = json.load(open(opath))['summary']
            rows.append(dict(layout=layout_name, scan=scan_name, summary=s,
                             pd_bound=float(F(s['best_pd_bound_requests_per_second_exact'])),
                             colocated_bound=float(F(s['colocated_bound_requests_per_second_exact'])),
                             ratio=float(F(s['pd_to_colocated_bound_ratio_exact'])),
                             network_capacity=float(F(s['network_capacity_requests_per_second_exact'])),
                             transfer_bytes=s['pd_transfer_bytes_per_request'],
                             bottlenecks=s['best_bottlenecks'],
                             best_prefill_workers=s['best_prefill_workers'],
                             best_decode_workers=s['best_decode_workers']))

    result = dict(schema_version=1, experiment='9-2', title='A100＋H20 的 PD 分离',
                  worker_devices=dict(a100=A100, h20=H20,
                                      note='阶段能力由硬件表峰值乘 50% 效率推出，逐卡明细见各 pool-*.json 的 derived_stage_rates。'),
                  link_bytes_per_second=LINK, rows=rows,
                  source_note='由 calculations/calc.py pd-pool 现场生成。',
                  python_version=sys.version)
    json.dump(result, open(os.path.join(RESULTS, 'pd.json'), 'w'), indent=2, ensure_ascii=False)

    lines = ['# 实验 9-2 结果：A100＋H20 的 PD 分离', '',
             '阶段能力：A100 80GB SXM（312 TFLOP/s、2039 GB/s）与 H20 SXM5 96GB（148 TFLOP/s、4096 GB/s）'
             '峰值乘 50%%，decode 批量 32。链路 %.0f GB/s。' % (LINK / 1e9), '',
             '| 布局 | 场景 | 每请求交接 | PD 上界 | 共置上界 | PD/共置 | 链路容量 | 瓶颈 | 最优分工 |',
             '| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |']
    for r in rows:
        if 'error' in r:
            lines.append('| %s | %s | 调用失败：%s | — | — | — | — | — | — |' % (
                r['layout'], r['scan'], r['error']))
            continue
        assign = 'P:' + ','.join('%s×%d' % (k, v) for k, v in r['best_prefill_workers'].items() if v)
        assign += ' D:' + ','.join('%s×%d' % (k, v) for k, v in r['best_decode_workers'].items() if v)
        lines.append('| %s | %s | %.3f GiB | %.3f req/s | %.3f req/s | %.2f× | %.3f req/s | %s | %s |' % (
            r['layout'], r['scan'], r['transfer_bytes'] / 2 ** 30,
            r['pd_bound'], r['colocated_bound'], r['ratio'],
            r['network_capacity'], '、'.join(r['bottlenecks']), assign))
    lines.append('')
    open(os.path.join(RESULTS, 'pd.md'), 'w').write('\n'.join(lines))
    print('\n'.join(lines))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
