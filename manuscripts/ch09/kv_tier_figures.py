"""Section 9.5.2: per-GPU KV tiers, retention versus reuse window, hit-rate ceiling,
layer-wise preloading and queue-aware prefetch. All numbers come from
calculations/results/kv-tiers-book.json (python3 calculations/calc.py kv-tiers)."""
from fractions import Fraction
from pathlib import Path
import json
import matplotlib.pyplot as plt
from figure_style import COL, STYLE, Exporter, canvas, plot, box, text, arrow

ROOT = Path(__file__).resolve().parents[2]
LINE = {'blue': '#267398', 'orange': '#a56c28', 'green': '#28856a', 'purple': '#7a5c99', 'gray': '#777777'}


def num(v):
    return float(Fraction(str(v)))


def draw(here):
    r = json.loads((ROOT / 'calculations/results/kv-tiers-book.json').read_text())
    s = r['summary']
    tiers = {t['tier']: t for t in r['tiers']}
    out = Exporter(here)
    with plt.rc_context(STYLE):
        # 1. Tier ladder for one A100 of a DGX A100.
        f, a = canvas(4.6)
        text(a, .02, .95, '一张 A100 可用的 KV 存储层次', 13)
        rows = [('HBM', f"≤ {num(tiers['HBM']['capacity_bytes'])/1e9:.1f} GB", 'green', .24, '已在 GPU 上', '取回 0 ms'),
                ('主机内存', f"{num(tiers['host DRAM']['capacity_bytes'])/1024**3:.0f} GiB", 'blue', .34,
                 'PCIe 4.0 x16，25 GB/s', f"取回 {num(tiers['host DRAM']['read_s_exact'])*1e3:.1f} ms"),
                ('本地 SSD', f"{num(tiers['local NVMe']['capacity_bytes'])/1e12:.2f} TB", 'orange', .44,
                 'SSD 顺序读 7.1 GB/s', f"取回 {num(tiers['local NVMe']['read_s_exact'])*1e3:.0f} ms"),
                ('远端存储池', '随节点数增加', 'purple', .54,
                 '网卡 25 GB/s，再经 PCIe', f"取回 {num(tiers['remote pool']['read_s_exact'])*1e3:.1f} ms")]
        for i, (name, cap, c, w, path, t) in enumerate(rows):
            y = .70 - i * .19
            box(a, .31 - w / 2, y, w, .15, f'{name}\n{cap}', c, 12)
            text(a, .63, y + .105, path, 11)
            text(a, .63, y + .045, t, 11)
        text(a, .02, .05, f"对照：在 A100 上重算这份 8K 前缀约 {num(s['prefill_prefix_s_exact'])*1e3:.0f} ms", 11)
        out.save(f, 'figure-9-kv-tiers')

        # 2. Capacity needed to cover a reuse interval, C = r * T.
        rate = num(s['kv_production_bytes_per_second_exact']) / 1e9
        f, a = plot(4.2, left=.16, bottom=.17)
        xs = [1, 3600]
        a.plot(xs, [rate * x for x in xs], color=LINE['blue'], lw=1.6)
        a.set_xscale('log'); a.set_yscale('log')
        for name, cap, c in [('HBM', num(tiers['HBM']['capacity_bytes']) / 1e9, 'green'),
                             ('主机内存', num(tiers['host DRAM']['capacity_bytes']) / 1e9, 'blue'),
                             ('本地 SSD', num(tiers['local NVMe']['capacity_bytes']) / 1e9, 'orange')]:
            a.axhline(cap, color=LINE[c], ls='--', lw=1)
            a.text(1.25, cap * 1.18, f'{name} {cap:,.0f} GB' if cap > 100 else f'{name} {cap:.1f} GB', fontsize=11, color=LINE[c])
        for w in r['reuse_windows']:
            x = w['window_s']; y = num(w['required_bytes_exact']) / 1e9
            a.axvline(x, color=LINE['gray'], ls=':', lw=1)
            a.scatter([x], [y], color=LINE['blue'], zorder=3, s=22)
            a.annotate(f'{y:.1f} GB' if y < 100 else f'{y:.0f} GB', (x, y), xytext=(x * 1.25, y / 2.1), fontsize=11)
        a.text(10 * 1.12, 1100, 'API：80% 的复用\n在 10 s 内', fontsize=11)
        a.text(600 / 1.12, 1.3, '对话：80% 的复用\n在 10 min 内', fontsize=11, ha='right')
        a.set(xlim=(1, 3600), ylim=(1, 20000), xlabel='同一前缀两次使用的间隔（s，对数刻度）', ylabel='所需容量（GB，对数刻度）',
              xticks=[1, 10, 60, 600, 3600], xticklabels=['1', '10', '60', '600', '3600'])
        a.minorticks_off()
        out.save(f, 'figure-9-kv-capacity')

        # 3. Mooncake trace: LRU hit rate saturates with capacity.
        m = r['mooncake_lru_capacity']
        f, a = plot(3.7, left=.15, bottom=.19)
        xs = [row['qwen_bytes'] / 1e12 for row in m]; ys = [num(row['lru_hit_rate']) * 100 for row in m]
        a.plot(xs, ys, color=LINE['blue'], marker='o', lw=1.6)
        a.axhline(51, color=LINE['orange'], ls='--', lw=1)
        a.text(.075, 53, '容量不限时也只有 51%', fontsize=11, color=LINE['orange'])
        place = {1000: (1.08, -5, 'left'), 10000: (1.08, -5, 'left'), 30000: (1.08, -6, 'left'),
                 50000: (1.05, -5, 'left'), 100000: (1, 3, 'right')}
        for x, y, row in zip(xs, ys, m):
            fx, dy, ha = place[row['blocks']]
            a.annotate(f"{row['blocks']:,} 块", (x, y), xytext=(x * fx, y + dy), fontsize=11, ha=ha)
        a.set_xscale('log')
        a.set(xlim=(.05, 12), ylim=(20, 60), xlabel='缓存容量（换算为 Qwen3-8B 的 KV，TB）', ylabel='LRU 命中率（%）',
              xticks=[.1, 1, 10], xticklabels=['0.1', '1', '10'])
        a.minorticks_off()
        out.save(f, 'figure-9-kv-hit')

        # 4. Loading history from host memory while the 256-token suffix is computed.
        t = tiers['host DRAM']; L = s['layers']
        ld = num(t['load_per_layer_s_exact']) * 1e3; cp = num(t['compute_per_layer_s_exact']) * 1e3
        k = t['preload_layers_for_full_overlap']

        def schedule(mode):
            reads, comps = [], []
            if mode == 'serial':
                reads = [(i * ld, ld) for i in range(L)]
                start = L * ld
                comps = [(start + i * cp, cp) for i in range(L)]
            else:
                pre = k if mode == 'preload' else 0
                reads = [(-(pre - i) * ld, ld) for i in range(pre)] + [(j * ld, ld) for j in range(L - pre)]
                done = 0.
                for i in range(L):
                    ready = 0. if i < pre else (i - pre + 1) * ld
                    st = max(done, ready); comps.append((st, cp)); done = st + cp
            return reads, comps

        for mode, name, total in [('serial', 'serial', num(t['serial_s_exact'])),
                                  ('layer', 'layerwise', num(t['layer_pipelined_s_exact'])),
                                  ('preload', 'preload', num(s['warm_suffix_s_exact']))]:
            reads, comps = schedule(mode)
            f, a = plot(2.5, left=.20, bottom=.27)
            a.broken_barh(reads, (.6, .7), facecolors=COL['orange'], edgecolors='white', linewidth=.3)
            a.broken_barh(comps, (-.35, .7), facecolors=COL['green'], edgecolors='white', linewidth=.3)
            a.axvline(0, color=LINE['gray'], lw=.8)
            a.axvline(total * 1e3, color=LINE['blue'], ls='--', lw=1)
            a.text(total * 1e3 + 1.2, .45, f'{total*1e3:.1f} ms', fontsize=11, color=LINE['blue'], va='center')
            if mode == 'preload':
                a.text(-k * ld / 2, 1.62, f'提前读入 {k} 层', fontsize=11, ha='center')
            a.set(xlim=(-22, 90), ylim=(-.6, 1.9), yticks=[0, .95], yticklabels=['GPU 计算', 'PCIe 读取'],
                  xlabel='从这个请求开始执行起计时（ms）')
            a.spines['left'].set_visible(False); a.tick_params(axis='y', length=0)
            out.save(f, f'figure-9-kv-load-{name}')

        # 5. Queue-aware prefetch and eviction between host memory and SSD.
        f, a = canvas(4.0)
        a.set_ylim(0, .88)
        text(a, .02, .66, '等待队列', 12)
        for i, j in enumerate(['J1', 'J2', 'J3', 'J4', 'J5', 'J6']):
            box(a, .20 + i * .13, .60, .11, .12, j + ('\n执行中' if i == 0 else ''), 'green' if i == 0 else 'gray', 11)
        a.plot([.33, .33, .59, .59], [.745, .77, .77, .745], color=COL['line'], lw=.9)
        text(a, .46, .82, '接下来的请求：J2—J4', 11, ha='center')
        text(a, .02, .40, '主机内存', 12)
        for i, lab in enumerate(['KV J2', 'KV J4', '空位', 'KV J6']):
            box(a, .20 + i * .15, .34, .13, .12, lab, 'white' if lab == '空位' else 'blue', 11)
        text(a, .02, .10, '本地 SSD', 12)
        for i, lab in enumerate(['KV J5', 'KV J8', 'KV J3', '空位']):
            box(a, .20 + i * .15, .04, .13, .12, lab, 'white' if lab == '空位' else 'orange', 11)
        arrow(a, (.565, .16), (.565, .34))
        text(a, .575, .25, '读入 J3', 11)
        arrow(a, (.715, .34), (.715, .16))
        text(a, .725, .25, '换出 J6', 11)
        out.save(f, 'figure-9-kv-prefetch')
    (here / 'kv-tier-layout-validation.json').write_text(json.dumps(out.checks, ensure_ascii=False, indent=2) + '\n')
    return out.outputs
