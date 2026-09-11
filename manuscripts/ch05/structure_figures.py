"""Chapter-five mechanism figures added in the structure revision (book figure style)."""
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
import numpy as np
from figure_style import COL, STYLE, Exporter, canvas, plot, box, text, arrow
from figure_style.typography import configure_font

ROOT = Path(__file__).resolve().parents[2]


def cut(ax, p, q):
    ax.plot([p[0], q[0]], [p[1], q[1]], ls=(0, (5, 3)), lw=1.6, color=COL['ink'])


def draw(here):
    here = Path(here); out = Exporter(here)
    with plt.rc_context(STYLE):
        # 5.1.2 Copy paths between host memory and device memory.
        f, a = canvas(3.6)
        for x, title in [(.02, '主机内存（CPU）'), (.56, '显存（GPU）')]:
            a.add_patch(Rectangle((x, .06), .42, .82, facecolor=COL['white'], edgecolor=COL['line'], lw=.9, ls=(0, (1, 2))))
            text(a, x + .21, .93, title, 12, ha='center')
        box(a, .06, .66, .34, .16, '普通内存\n页面可被换出', 'gray', 11)
        box(a, .06, .42, .34, .16, '锁页缓冲\n驻留，可直接搬运', 'blue', 11)
        box(a, .06, .14, .34, .16, '结果缓冲', 'green', 11)
        box(a, .60, .66, .34, .16, '权重\n加载一次，长期驻留', 'gray', 11)
        box(a, .60, .42, .34, .16, '输入缓冲', 'blue', 11)
        box(a, .60, .14, .34, .16, '输出', 'green', 11)
        arrow(a, (.23, .66), (.23, .58)); text(a, .26, .625, '主机内复制', 11)
        arrow(a, (.40, .50), (.60, .50)); text(a, .50, .55, 'H2D', 11, ha='center')
        arrow(a, (.60, .22), (.40, .22)); text(a, .50, .27, 'D2H', 11, ha='center')
        box(a, .68, .335, .18, .07, 'kernel', 'white', 11)
        arrow(a, (.77, .42), (.77, .405)); arrow(a, (.77, .335), (.77, .30))
        out.save(f, 'figure-5-copy-paths')

        # 5.1.3 Two streams ordered by events; a slot is reused only after its reader finishes.
        f, a = canvas(3.4)
        text(a, .0, .70, '复制流', 12); text(a, .0, .32, '计算流', 12)
        box(a, .14, .62, .20, .16, 'H2D 批 0\n写入槽 A', 'blue', 11)
        box(a, .38, .62, .20, .16, 'H2D 批 1\n写入槽 B', 'green', 11)
        box(a, .76, .62, .20, .16, 'H2D 批 2\n写入槽 A', 'blue', 11)
        box(a, .38, .24, .30, .16, '计算 批 0\n读取槽 A', 'blue', 11)
        box(a, .72, .24, .24, .16, '计算 批 1\n读取槽 B', 'green', 11)
        arrow(a, (.34, .62), (.40, .40), 'control'); text(a, .10, .49, '事件：批 0 已传完', 11)
        arrow(a, (.68, .40), (.76, .62), 'control'); text(a, .44, .53, '事件：批 0 已用完', 11)
        a.plot([.14, .96], [.10, .10], color=COL['line'], lw=.8); text(a, .96, .05, '时间', 11, ha='right')
        out.save(f, 'figure-5-stream-event')

        # 5.5.1 Host preparation and accelerator compute: serial, pipelined, faster accelerator.
        f, a = canvas(4.6)
        scale = .80 / 160; x0 = .16
        panels = [(.70, '串行：每段准备 20 μs、计算 20 μs，四段共 160 μs', 40, 20, 20, 0),
                  (.38, '流水：准备下一段与计算当前段同时进行，共 100 μs', 20, 20, 20, 20),
                  (.06, '加速器提速到 5 μs：主机仍每 20 μs 才准备好一段，共 85 μs', 20, 20, 5, 20)]
        for y, title, period, host, acc, lag in panels:
            text(a, .0, y + .27, title, 11)
            text(a, .0, y + .175, '主机准备', 11); text(a, .0, y + .045, '加速器计算', 11)
            for i in range(4):
                hx = x0 + scale * period * i
                box(a, hx, y + .13, scale * host - .004, .09, str(i), 'orange', 11)
                ax_ = x0 + scale * (period * i + (host if lag == 0 else lag))
                box(a, ax_, y, scale * acc - .004, .09, str(i), 'blue', 11)
        a.plot([x0, .96], [.015, .015], color=COL['line'], lw=.8)
        for t in (0, 40, 80, 120, 160):
            text(a, x0 + scale * t, -.01, f'{t}', 11, ha='center')
        out.save(f, 'figure-5-host-pipeline')

        # 5.5.2 Ordinary submission versus graph replay: launches change, kernels do not.
        f, a = canvas(3.2)
        for x, title, host_label in [(.03, '普通提交', '主机：六次 kernel launch'), (.53, '图重放', '主机：一次 graph launch')]:
            text(a, x, .93, title, 12); text(a, x, .80, host_label, 11); text(a, x, .08, '加速器：六个 kernel', 11)
            for i in range(6):
                bx = x + .072 * i
                box(a, bx, .18, .06, .14, str(i + 1), 'blue', 11)
                if x < .5:
                    box(a, bx, .56, .06, .14, str(i + 1), 'orange', 11); arrow(a, (bx + .03, .56), (bx + .03, .32))
        box(a, .53, .56, .16, .14, '图', 'orange', 11)
        a.plot([.56, .95], [.38, .38], color=COL['line'], lw=1)
        for i in range(6): a.plot([.56 + .072 * i, .56 + .072 * i], [.38, .34], color=COL['line'], lw=1)
        arrow(a, (.61, .56), (.61, .38))
        out.save(f, 'figure-5-launch-vs-graph')

        # 5.5.3 Real row counts padded into two buckets.
        f, a = plot(3.0, left=.30, bottom=.25); f.subplots_adjust(top=.80)
        rows = [256, 1536, 2048]; buckets = [512, 2048, 2048]; labels = ['256 行，8 次', '1536 行，1 次', '2048 行，1 次']
        a.barh(range(3), rows, color=COL['blue'], edgecolor=COL['line'], height=.55, label='实际行数')
        a.barh(range(3), [b - r for b, r in zip(buckets, rows)], left=rows, color=COL['gray'], edgecolor=COL['line'], height=.55, label='补齐到桶')
        for i, b in enumerate(buckets): a.text(b + 40, i, f'桶 {b}', va='center', fontsize=11)
        a.set(yticks=range(3), yticklabels=labels, xlim=(0, 2500), xlabel='每次调用执行的行数'); a.invert_yaxis()
        a.legend(frameon=False, ncol=2, loc='lower center', bbox_to_anchor=(.5, 1.0))
        out.save(f, 'figure-5-shape-buckets')

        # 5.2.4 Three ways to split one matrix multiply (moved here from chapter six).
        f, a = canvas(4.8)
        for row, (title, left, right, result, c) in enumerate([
                ('切 M：输出行', '输入行分片', '权重复制', '不同输出行', 'blue'),
                ('切 N：输出列', '输入复制', '权重列分片', '不同输出列', 'green'),
                ('切 K：归约维', '输入列分片', '权重行分片', '同一输出的部分和', 'orange')]):
            y = .71 - row * .30
            text(a, .04, y + .19, title, 13)
            box(a, .04, y, .26, .13, left, c, 11); box(a, .36, y, .26, .13, right, c, 11); box(a, .70, y, .27, .13, result, c, 11)
            text(a, .33, y + .065, '×', 13, ha='center'); arrow(a, (.62, y + .065), (.70, y + .065))
        text(a, .50, .04, '输出分片按需收集；归约分片必须求和', 12, ha='center')
        out.save(f, 'figure-5-split-axes')
    (here / 'structure-layout-validation.json').write_text(json.dumps(out.checks, ensure_ascii=False, indent=2) + '\n')
    return out.outputs


if __name__ == '__main__':
    _, family = configure_font()
    plt.rcParams.update({'font.family': [family, 'DejaVu Sans'], 'axes.unicode_minus': False, 'svg.hashsalt': 'ch05-structure'})
    draw(ROOT / 'manuscripts/ch05')
