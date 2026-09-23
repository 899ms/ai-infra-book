"""Where each parallelism cuts a transformer: one overview, then one figure per method."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from figure_style import COL, STYLE, Exporter, canvas, plot, box, text, arrow
from figure_style.typography import configure_font

ROOT = Path(__file__).resolve().parents[1]


def cut(ax, p, q):
    """A cut through data or model; drawn as a wide dash so it differs from control arrows."""
    ax.plot([p[0], q[0]], [p[1], q[1]], ls=(0, (5, 3)), lw=1.6, color=COL['ink'])


def draw(here):
    here = Path(here); out = Exporter(here)
    with plt.rc_context(STYLE):
        # Overview: activation dimensions on the left, model structure on the right.
        f, a = canvas(4.6)
        text(a, .04, .96, "啟用：樣本 B、序列位置 S、特徵 H", 12)
        for k in (2, 1, 0):
            x0 = .06 + .025 * k; y0 = .36 + .025 * k
            a.add_patch(Rectangle((x0, y0), .28, .34, facecolor=COL['white'] if k else COL['blue'], edgecolor=COL['line'], lw=.9))
        for i in range(1, 4):
            a.plot([.06 + .07 * i] * 2, [.36, .70], color=COL['line'], lw=.5)
            a.plot([.06, .34], [.36 + .085 * i] * 2, color=COL['line'], lw=.5)
        cut(a, (.20, .33), (.20, .73)); text(a, .20, .29, "TP 切 H：權重的列或行、注意力頭", 11, ha='center')
        cut(a, (.03, .53), (.37, .53)); text(a, .015, .53, "SP／CP 切 S：序列位置", 11, ha='center', rotation=90)
        cut(a, (.0725, .7125), (.3525, .7125)); text(a, .23, .81, "DP 切 B：樣本", 11, ha='center')
        text(a, .54, .96, "模型結構：層 L、專家 E", 12)
        for i in range(4):
            x = .54 + .11 * i; box(a, x, .70, .09, .12, f'層 {i}', 'green', 11)
            if i < 3: arrow(a, (x + .09, .76), (x + .11, .76))
        cut(a, (.75, .64), (.75, .87)); text(a, .75, .905, "PP 切 L：層", 11, ha='center')
        a.add_patch(Rectangle((.54, .09), .43, .42, facecolor=COL['white'], edgecolor=COL['line'], lw=.9, ls=(0, (1, 2))))
        text(a, .755, .465, "一層的 FFN 由 E 個專家組成", 11, ha='center')
        box(a, .665, .32, .18, .09, "路由器", 'gray', 11)
        for i in range(4):
            x = .555 + .105 * i; box(a, x, .13, .09, .12, f'專家 {i}', 'green', 11)
            arrow(a, (.755, .32), (x + .045, .25))
        cut(a, (.7575, .11), (.7575, .30)); text(a, .7575, .045, "EP 切 E：專家", 11, ha='center')
        out.save(f, 'figure-6-parallel-map')

        # DP: model copied, samples split; gradients meet only in training.
        f, a = canvas(3.4)
        box(a, .03, .40, .15, .22, "輸入 batch\n樣本 0–7", 'gray', 11)
        for r, (y, col, s, o) in enumerate([(.66, 'blue', "樣本 0–3", "輸出 0–3"), (.12, 'green', "樣本 4–7", "輸出 4–7")]):
            text(a, .25, y + .27 if r == 0 else y - .07, f'卡 {r}', 12)
            arrow(a, (.18, .51), (.24, y + .10))
            box(a, .24, y, .14, .20, s, col, 11); arrow(a, (.38, y + .10), (.42, y + .10))
            box(a, .42, y, .30, .20, "完整模型\n全部層的權重", col, 11); arrow(a, (.72, y + .10), (.76, y + .10))
            box(a, .76, y, .14, .20, o, col, 11)
        box(a, .42, .37, .30, .16, "訓練：梯度 AllReduce", 'orange', 11)
        arrow(a, (.57, .66), (.57, .53)); arrow(a, (.57, .32), (.57, .37))
        out.save(f, 'figure-6-dp')

        # TP: one layer, attention by heads, FFN by intermediate width; two AllReduces per layer.
        f, a = canvas(5.0)
        panels = [(.95, .58, "注意力子層：按頭切分，輸出投影產生部分和", "X\n每卡\n一份",
                   [("QKV 投影(列)\n頭 0–15", "注意力\n頭 0–15", "輸出投影(行)\n部分和 m×h"), ("QKV 投影(列)\n頭 16–31", "注意力\n頭 16–31", "輸出投影(行)\n部分和 m×h")]),
                  (.47, .10, "FFN 子層：按中間維切分，下投影產生部分和", "X′\n每卡\n一份",
                   [("上投影(列)\n前半中間維", "SiLU ⊙ 乘法\n本地", "下投影(行)\n部分和 m×h"), ("上投影(列)\n後半中間維", "SiLU ⊙ 乘法\n本地", "下投影(行)\n部分和 m×h")])]
        for ytitle, ybase, title, inp, rows in panels:
            text(a, .02, ytitle, title, 12)
            box(a, .02, ybase, .11, .30, inp, 'gray', 11)
            box(a, .745, ybase, .225, .30, "AllReduce\n求和後每卡\n得到 m×h", 'orange', 11)
            for r, labels in enumerate(rows):
                y = ybase + .17 - .17 * r; col = 'blue' if r == 0 else 'green'
                arrow(a, (.13, ybase + .15), (.16, y + .065))
                for j, label in enumerate(labels):
                    x = .16 + .195 * j; box(a, x, y, .16, .13, label, col, 11)
                    if j < 2: arrow(a, (x + .16, y + .065), (x + .195, y + .065))
                arrow(a, (.71, y + .065), (.745, y + .065))
        out.save(f, 'figure-6-tp-layer')

        # SP: per-token operators keep sequence shards; linear layers use the TP layout.
        f, a = canvas(3.4)
        for xc, label in [(.15, "序列分片"), (.53, "全部位置：特徵分片、部分和"), (.885, "序列分片")]:
            text(a, xc, .93, label, 11, ha='center')
        for x0, x1 in [(.07, .23), (.35, .69), (.80, .97)]:
            a.plot([x0, x1], [.87, .87], color=COL['line'], lw=.8)
        box(a, .255, .16, .07, .62, 'All\nGather', 'orange', 11)
        box(a, .715, .16, .07, .62, 'Reduce\nScatter', 'orange', 11)
        for r, (y, col, pos) in enumerate([(.56, 'blue', "位置 0–3"), (.16, 'green', "位置 4–7")]):
            text(a, .0, y + .08, f'卡 {r}', 12)
            box(a, .07, y, .16, .16, f'LayerNorm\n{pos}', col, 11); arrow(a, (.23, y + .08), (.255, y + .08))
            arrow(a, (.325, y + .08), (.35, y + .08)); box(a, .35, y, .16, .16, "列並行線性\n位置 0–7", col, 11)
            arrow(a, (.51, y + .08), (.53, y + .08)); box(a, .53, y, .16, .16, "行並行線性\n部分和", col, 11)
            arrow(a, (.69, y + .08), (.715, y + .08)); arrow(a, (.785, y + .08), (.80, y + .08))
            box(a, .80, y, .17, .16, f'殘差\n{pos}', col, 11)
        out.save(f, 'figure-6-sp')

        # CP: one sequence split by position; remote K/V must still reach the queries.
        f, a = canvas(3.5)
        box(a, .02, .38, .14, .24, "一個序列\n位置 0–7", 'gray', 11)
        for r, (y, col, pos, kv) in enumerate([(.68, 'blue', "位置 0–3", 'K/V 0–3'), (.14, 'green', "位置 4–7", 'K/V 0–7')]):
            text(a, .21, y + .24 if r == 0 else y - .07, f'卡 {r}', 12)
            arrow(a, (.16, .50), (.21, y + .085))
            box(a, .21, y, .17, .17, f'Q/K/V\n{pos}', col, 11); arrow(a, (.38, y + .085), (.43, y + .085))
            box(a, .43, y, .27, .17, f'注意力\n查詢 {pos[3:]} · {kv}', col, 11); arrow(a, (.70, y + .085), (.75, y + .085))
            box(a, .75, y, .21, .17, f'輸出\n{pos}', col, 11)
        box(a, .43, .42, .27, .14, "傳 K/V 位置 0–3", 'orange', 11)
        arrow(a, (.295, .68), (.50, .56)); arrow(a, (.565, .42), (.565, .31))
        out.save(f, 'figure-6-cp')

        # PP: layers split into stages; activations cross the boundary per microbatch.
        f, a = canvas(2.9)
        box(a, .02, .44, .10, .18, "輸入", 'gray', 11); arrow(a, (.12, .53), (.15, .53))
        box(a, .15, .34, .28, .36, "卡 0\n層 0–31 的權重", 'blue', 11); arrow(a, (.43, .53), (.46, .53))
        box(a, .46, .44, .10, .18, "啟用", 'orange', 11); arrow(a, (.56, .53), (.59, .53))
        box(a, .59, .34, .28, .36, "卡 1\n層 32–63 的權重", 'green', 11); arrow(a, (.87, .53), (.90, .53))
        box(a, .90, .44, .08, .18, "輸出", 'gray', 11)
        arrow(a, (.59, .27), (.43, .27)); text(a, .51, .16, "訓練：梯度沿相同邊界反向傳遞", 11, ha='center')
        out.save(f, 'figure-6-pp')

        # Topology case: hops in one torus plane versus one switch stage.
        f, a = canvas(3.8)
        text(a, .04, .95, "三維環面的一層（4×4）", 12); text(a, .58, .95, "交換網路", 12)
        cx = [.06 + .115 * i for i in range(4)]; cy = [.16 + .19 * j for j in range(4)]; w, h = .08, .11
        for i in range(4):
            for j in range(4):
                if i < 3: a.plot([cx[i] + w, cx[i + 1]], [cy[j] + h / 2] * 2, color=COL['line'], lw=.9)
                if j < 3: a.plot([cx[i] + w / 2] * 2, [cy[j] + h, cy[j + 1]], color=COL['line'], lw=.9)
            a.plot([cx[0] - .03, cx[0]], [cy[i] + h / 2] * 2, color=COL['line'], lw=.9, ls=(0, (2, 2)))
            a.plot([cx[3] + w, cx[3] + w + .03], [cy[i] + h / 2] * 2, color=COL['line'], lw=.9, ls=(0, (2, 2)))
            a.plot([cx[i] + w / 2] * 2, [cy[0] - .05, cy[0]], color=COL['line'], lw=.9, ls=(0, (2, 2)))
            a.plot([cx[i] + w / 2] * 2, [cy[3] + h, cy[3] + h + .05], color=COL['line'], lw=.9, ls=(0, (2, 2)))
        path = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
        for (i0, j0), (i1, j1) in zip(path, path[1:]):
            a.plot([cx[i0] + w / 2, cx[i1] + w / 2], [cy[j0] + h / 2, cy[j1] + h / 2], color=COL['ink'], lw=2.6)
        for i in range(4):
            for j in range(4):
                box(a, cx[i], cy[j], w, h, '', 'orange' if (i, j) in ((0, 0), (2, 2)) else 'blue')
        text(a, .27, .06, "四跳；第三個維度再加兩跳", 11, ha='center')
        sx = [.575 + .05 * i for i in range(8)]
        box(a, .60, .64, .36, .14, "交換晶片", 'orange', 12)
        for i, x in enumerate(sx):
            a.plot([x + .02, x + .02], [.30, .64], color=COL['line'], lw=.9)
        for i in (0, 5):
            a.plot([sx[i] + .02, sx[i] + .02], [.30, .64], color=COL['ink'], lw=2.6)
        for i, x in enumerate(sx):
            box(a, x, .19, .04, .11, '', 'orange' if i in (0, 5) else 'blue')
        text(a, .78, .06, "兩條鏈路加一次交換", 11, ha='center')
        out.save(f, 'figure-6-topology-hops')

        # Topology case: link-load lower bounds for two traffic patterns.
        f, a = plot(3.2, left=.17, bottom=.24); f.subplots_adjust(top=.82)
        labels = ["沿維度歸約\n64 卡", "均勻 All-to-All\n64 卡", "均勻 All-to-All\n512 卡"]
        torus = [223.7, 335.5, 671.1]; switch = [223.7, 111.8, 111.8]
        x = np.arange(3)
        a.bar(x - .18, torus, .34, color=COL['blue'], edgecolor=COL['line'], label="三維環面")
        a.bar(x + .18, switch, .34, color=COL['green'], edgecolor=COL['line'], label="無阻塞交換網路")
        for xi, v in zip(x - .18, torus): a.text(xi, v + 12, f'{v:.0f}', ha='center', fontsize=11)
        for xi, v in zip(x + .18, switch): a.text(xi, v + 12, f'{v:.0f}', ha='center', fontsize=11)
        a.set(xticks=x, xticklabels=labels, ylabel="傳輸時間下界（μs）", ylim=(0, 760))
        a.legend(frameon=False, ncol=2, loc='lower center', bbox_to_anchor=(.5, 1.0))
        out.save(f, 'figure-6-topology-patterns')

        # EP: experts split across cards; tokens travel to experts and back.
        f, a = canvas(4.0)
        box(a, .10, .82, .80, .12, "注意力與路由器：每卡處理自己持有的 token", 'gray', 11)
        arrow(a, (.50, .82), (.50, .74))
        box(a, .10, .64, .80, .10, "All-to-All dispatch：按所選專家的所在卡傳送輸入", 'orange', 11)
        for r, (x, col) in enumerate([(.10, 'blue'), (.52, 'green')]):
            arrow(a, (x + .19, .64), (x + .19, .56))
            box(a, x, .30, .38, .26, '', col); text(a, x + .19, .515, f'卡 {r}', 12, ha='center')
            for i in range(4):
                box(a, x + .015 + .0925 * i, .33, .08, .13, f'E{4 * r + i}', 'white', 11)
            arrow(a, (x + .19, .30), (x + .19, .24))
        box(a, .10, .14, .80, .10, "All-to-All 返回：結果回到 token 所在卡，按路由權重合並", 'orange', 11)
        out.save(f, 'figure-6-ep')
    (here / 'parallel-layout-validation.json').write_text(json.dumps(out.checks, ensure_ascii=False, indent=2) + '\n')
    return out.outputs


if __name__ == '__main__':
    _, family = configure_font()
    plt.rcParams.update({'font.family': [family, 'DejaVu Sans'], 'axes.unicode_minus': False, 'svg.hashsalt': 'parallel-book'})
    draw(ROOT / 'manuscripts/ch06')
