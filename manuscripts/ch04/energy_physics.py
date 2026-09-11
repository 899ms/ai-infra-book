"""Section 4.1.3 chip physics and energy: four derivation figures at final book width.

Inputs: calculations/results/energy-ledger-book.json (per-byte energies with source lines,
Qwen3-8B decode-step split, LogicFolding ratios) and the H100 whitepaper table
(references/text/nvidia-h100.txt: BF16 dense 989.4 TFLOPS line 699, TDP 700 W line 1355;
bandwidth 3.35 TB/s from the datasheet, references/text/nvidia-h100-spec.txt line 383).
"""
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from figure_style import COL, canvas, plot, text, box, arrow

ROOT = Path(__file__).resolve().parents[2]
H100_PEAK_BF16_FLOPS = 989.4e12   # whitepaper table, dense
H100_HBM_BYTES_PER_S = 3350e9     # datasheet 3.35 TB/s, the form used throughout chapter 4
H100_TDP_W = 700.0                # whitepaper table and datasheet


def draw(out):
    led = json.loads((ROOT/'calculations/results/energy-ledger-book.json').read_text())
    epb = led['energy_per_byte']; ref = led['energy_per_byte_references']
    ladder = led['joules_per_token']['by_level_if_all_bytes_came_from_that_level']
    split = led['joules_per_token']['per_token_split_weights_kv_compute']
    pj_flop = led['joules_per_token']['compute']['pj_per_flop']
    v_ratio = led['voltage_scaling']['dynamic_power_ratio']
    p_ratio = float(led['power_density']['power_ratio'].split('/')[0])/float(led['power_density']['power_ratio'].split('/')[1])
    a_ratio = float(led['power_density']['projected_area_ratio'].split('/')[0])/float(led['power_density']['projected_area_ratio'].split('/')[1])
    d_ratio = led['power_density']['density_ratio']

    # Figure A: wire capacitance mechanism plus the two LogicFolding ratios.
    f = plt.figure(figsize=(420/72, 5.2))
    a = f.add_axes([.03, .50, .94, .48]); a.set(xlim=(0, 1), ylim=(0, 1)); a.axis('off')
    text(a, .02, .95, '横向连线：数百 μm，电容沿长度累积', 13)
    box(a, .02, .60, .16, .16, '驱动门', 'green', 11); box(a, .82, .60, .16, .16, '接收门', 'green', 11)
    a.plot([.18, .82], [.68, .68], color=COL['line'], lw=1.6)
    for x in np.linspace(.26, .74, 5):
        a.plot([x, x], [.68, .56], color=COL['line'], lw=1)
        a.plot([x-.03, x+.03], [.56, .56], color=COL['line'], lw=1.4)
        a.plot([x-.03, x+.03], [.51, .51], color=COL['line'], lw=1.4)
        a.plot([x, x], [.51, .45], color=COL['line'], lw=1)
        a.plot([x-.02, x+.02], [.45, .45], color=COL['line'], lw=1.2)
    text(a, .50, .36, '每次 0→1 充电从电源取走 C·V² 的能量', 12, ha='center')
    text(a, .02, .19, '折叠后：上下两层之间的垂直连接只有数 μm', 13)
    box(a, .30, .00, .18, .11, '上层', 'blue', 11); box(a, .52, .00, .18, .11, '下层', 'blue', 11)
    arrow(a, (.48, .055), (.52, .055))
    b = f.add_axes([.14, .12, .82, .32])
    labels = ['基线', '降压后\n动态功耗', '折叠后\n功耗', '折叠后\n投影面积', '折叠后\n功率密度']
    vals = [1.0, v_ratio, p_ratio, a_ratio, d_ratio]
    colors = [COL['gray'], COL['blue'], COL['green'], COL['orange'], COL['purple']]
    b.bar(range(5), vals, color=colors, edgecolor=COL['line'], width=.62)
    b.axhline(1.0, ls=':', color='#777777', lw=1)
    for i, v in enumerate(vals):
        b.text(i, v+.04, f'{v:.2f}', ha='center', fontsize=11)
    b.set(xticks=range(5), xticklabels=labels, ylim=(0, 1.55), ylabel='相对基线')
    b.tick_params(labelsize=11); b.spines[['top', 'right']].set_visible(False)
    out.save(f, 'figure-4-energy-wire')

    # Figure B: pJ/byte ladder (log scale) and one decode step in joules.
    f = plt.figure(figsize=(420/72, 5.6))
    a = f.add_axes([.30, .60, .66, .36])
    rows = [('KB 级局部 SRAM', epb['shared_l1']['pj_per_byte']), ('NVLink-C2C 链路', epb['nvlink']['pj_per_byte']),
            ('MB 级片上 SRAM', epb['l2']['pj_per_byte']), ('HBM2', epb['hbm']['pj_per_byte']),
            ('LPDDR DRAM', ref['dram_lpddr_45nm']['pj_per_byte'])]
    ys = range(len(rows)); vs = [r[1] for r in rows]
    a.barh(ys, vs, color=[COL['green'], COL['purple'], COL['green'], COL['blue'], COL['blue']], edgecolor=COL['line'], height=.62)
    for y, v in zip(ys, vs):
        a.text(v*1.12, y, f'{v:g}', va='center', fontsize=11)
    a.set_xscale('log'); a.set(xlim=(1, 400), yticks=list(ys), yticklabels=[r[0] for r in rows], xlabel='每 byte 能耗（pJ，对数坐标）')
    a.invert_yaxis(); a.tick_params(labelsize=11); a.spines[['top', 'right']].set_visible(False)
    b = f.add_axes([.30, .10, .66, .36])
    names = ['实际分账（HBM）', '若全部来自 KB 级 SRAM', '若全部来自 NVLink-C2C', '若全部来自 MB 级 SRAM', '若全部来自 HBM2']
    w, k, c = split['weight_joules'], split['kv_joules'], split['compute_joules']
    b.barh(0, w, color=COL['blue'], edgecolor=COL['line'], height=.62, label='权重读取')
    b.barh(0, k, left=w, color=COL['green'], edgecolor=COL['line'], height=.62, label='KV 读取')
    b.barh(0, c, left=w+k, color=COL['orange'], edgecolor=COL['line'], height=.62, label='矩阵计算')
    b.text(w+k+c+.012, 0, f'{w+k+c:.3f} J', va='center', fontsize=11)
    lv = [ladder['shared_l1']['weight_plus_kv_joules'], ladder['nvlink']['weight_plus_kv_joules'],
          ladder['l2']['weight_plus_kv_joules'], ladder['hbm']['weight_plus_kv_joules']]
    b.barh(range(1, 5), lv, color=COL['gray'], edgecolor=COL['line'], height=.62)
    for y, v in zip(range(1, 5), lv):
        b.text(v+.012, y, f'{v:.3f} J', va='center', fontsize=11)
    b.set(xlim=(0, .72), yticks=range(5), yticklabels=names, xlabel='一步 decode 的能量（J，单请求、8K 上下文）')
    b.invert_yaxis(); b.tick_params(labelsize=11); b.spines[['top', 'right']].set_visible(False)
    b.legend(frameon=False, fontsize=11, loc='center right', bbox_to_anchor=(1.0, .55))
    out.save(f, 'figure-4-energy-ladder')

    # Figure C: package top view with two reticle-limited dies and eight HBM stacks on an interposer.
    f, a = canvas(4.6)
    text(a, .5, .95, '每颗 die 的面积不能超过光罩一次曝光的面积（H100：814 mm²）', 12, ha='center')
    box(a, .05, .13, .90, .74, '', 'gray')
    text(a, .07, .17, '中介层（interposer）', 11)
    box(a, .32, .30, .17, .46, 'die 0', 'orange', 12); box(a, .51, .30, .17, .46, 'die 1', 'orange', 12)
    a.plot([.49, .51], [.53, .53], color=COL['line'], lw=2.2)
    text(a, .50, .81, 'die 间链路', 11, ha='center')
    for i in range(4):
        y = .24 + i*.14
        box(a, .09, y, .17, .11, 'HBM', 'blue', 11); box(a, .74, y, .17, .11, 'HBM', 'blue', 11)
        a.plot([.26, .32], [y+.055, y+.055], color=COL['line'], lw=1)
        a.plot([.68, .74], [y+.055, y+.055], color=COL['line'], lw=1)
    text(a, .5, .05, '每堆带宽 = 1024 引脚 × 引脚速率；每堆容量 = 层数 × 每层容量；堆沿 die 边缘排列', 11, ha='center')
    out.save(f, 'figure-4-energy-package')

    # Figure D: sustained-frequency ratio versus e/b (energy per FLOP over the per-FLOP budget at peak rate).
    # The budget b itself is stated in the text: (TDP - HBM full-bandwidth power) / peak FLOP rate.
    p_hbm = H100_HBM_BYTES_PER_S*epb['hbm']['pj_per_byte']*1e-12
    budget = H100_TDP_W-p_hbm
    b_pj = budget/H100_PEAK_BF16_FLOPS*1e12
    x = np.linspace(1.0, 3.0, 200)
    example = 1.5
    f, a = plot(3.9, left=.16, bottom=.20)
    a.plot(x, 1/x, color='#527fa0', lw=2, label='电压不变：P ∝ f，持续频率比 = b/e')
    a.plot(x, x**(-1/3), color='#a56c28', lw=2, label='电压随频率下降：P ∝ f³，持续频率比 = (b/e)^(1/3)')
    a.axhline(1.0, ls=':', color='#777777', lw=1)
    a.axvline(example, ls=':', color='#777777', lw=1)
    for r, dy in [(1/example, -16), (example**(-1/3), 6)]:
        a.plot(example, r, 'o', color='#2b6d4f')
        a.annotate(f'{r:.2f}', (example, r), xytext=(6, dy), textcoords='offset points', fontsize=11)
    a.text(1.9, .955, 'e ≤ b：峰值频率可以持续', fontsize=11)
    a.set(xlim=(1.0, 3.0), ylim=(.3, 1.05), xlabel='实际每 FLOP 能耗 e ÷ 预算 b', ylabel='持续频率 ÷ 峰值频率')
    a.tick_params(labelsize=11); a.legend(frameon=False, fontsize=11, loc='lower left')
    out.save(f, 'figure-4-energy-power-cap')
    record=dict(dynamic_power_ratio=v_ratio, density_ratio=d_ratio, step_joules=w+k+c, ladder_joules=lv,
                hbm_full_bandwidth_w=p_hbm, compute_budget_w=budget,
                pj_per_flop_budget_tdp=H100_TDP_W/H100_PEAK_BF16_FLOPS*1e12, pj_per_flop_budget_after_hbm=b_pj,
                reference_pj_per_flop_45nm=pj_flop,
                example_e_over_b=example, sustained_ratio_v_fixed_at_example=1/example, sustained_ratio_v_scaled_at_example=example**(-1/3),
                inputs=dict(ledger='calculations/results/energy-ledger-book.json', h100_peak_bf16_flops=H100_PEAK_BF16_FLOPS, h100_hbm_bytes_per_s=H100_HBM_BYTES_PER_S, h100_tdp_w=H100_TDP_W))
    (Path(__file__).resolve().parent/'energy-figure-data.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
    return record
