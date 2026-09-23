#!/usr/bin/env python3
"""Draw MiMo event timelines and cost estimates from the archived public log."""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent))
from figure_style.typography import configure_font


def draw(language="zh", output_dir=None):
    english = language == "en"
    output_dir = Path(output_dir) if output_dir else HERE
    _, family = configure_font()
    plt.rcParams.update({'font.family': [family, 'DejaVu Sans'], 'font.size': 11,
                         'axes.unicode_minus': False, 'svg.fonttype': 'path',
                         'svg.hashsalt': 'mimo-interruptions-v1', 'pdf.fonttype': 42,
                         'text.color': '#203c48', 'axes.labelcolor': '#203c48',
                         'xtick.color': '#546e7a', 'ytick.color': '#203c48'})
    source = ROOT/'references/files/documents/mimo-v26-rl-run-log/recalculated.json'
    data = json.loads(source.read_text())['runs']
    blue, red, orange, grey = '#286b98', '#a94c52', '#bc722b', '#dce3e7'
    fig = plt.figure(figsize=(420/72, 340/72), facecolor='white')
    ax = fig.add_axes([.14, .565, .80, .275])
    legend = [Patch(facecolor=blue, label='Completed steps' if english else "完成步驟"), Patch(facecolor=red, label='Interrupted' if english else "中斷區間"),
              Patch(facecolor='#fbf0e5', edgecolor=orange, hatch='////', label='Rolled back' if english else "回滾作廢"),
              Patch(facecolor=grey, label='Wrap-up' if english else "收尾")]
    fig.legend(handles=legend, loc='upper center', bbox_to_anchor=(.54, .99),
               ncol=4, frameon=False, fontsize=11, handlelength=1.0, columnspacing=.8)
    for run, y, label in [('pro', 1, 'Pro'), ('flash', 0, 'Flash')]:
        d = data[run]
        fig.text(.14, .86 if y else .705,
                 (f"{label} · {d['restarts']} restarts · {d['wall_seconds']/3600:.1f} h total" if english else
                  f"{label}  ·  {d['restarts']} 次重啟  ·  總執行 {d['wall_seconds']/3600:.1f} 小時"),
                 fontsize=12, weight='bold')
        wasted = d['pre_restart_seconds'] + d['superseded_step_seconds']
        fig.text(.14, .825 if y else .67,
                 (f"Wasted: {wasted/3600:.1f} h ({wasted/d['wall_seconds']:.1%} of total)" if english else
                  f"浪費約 {wasted/3600:.1f} 小時（佔總時間 {wasted/d['wall_seconds']:.1%}）"),
                 fontsize=11, color=red, weight='bold')
        for seg in d['segments']:
            x, width = (seg['start']-d['run_start'])/3600, seg['seconds']/3600
            kind = seg['kind']
            color = {'step': blue, 'interruption': red, 'rollback': '#fbf0e5', 'tail': grey}[kind]
            ax.add_patch(Rectangle((x,y-.16),width,.32,facecolor=color,
                                  edgecolor=orange if kind=='rollback' else 'white',
                                  linewidth=.7, hatch='////' if kind=='rollback' else None))
            if kind == 'interruption':
                ax.plot(x+width,y+.20,marker='v',color=red,markersize=4,clip_on=False)
        ax.text(d['wall_seconds']/3600+1,y,'30 steps' if english else "30 步",va='center',fontsize=11)
    ax.set(xlim=(0,141), ylim=(-.48,1.5), yticks=[], xticks=range(0,131,20), xlabel='Elapsed time from each launch (hours)' if english else "各自啟動後經過的時間 / 小時")
    ax.grid(axis='x',color='#dce3e7',linewidth=.6);ax.set_axisbelow(True)
    for edge in ['top','left','right']:ax.spines[edge].set_visible(False)
    ax.spines['bottom'].set_color('#c3d0d7')
    fig.text(.14,.40,'Estimated interruption and rollback costs' if english else "中斷與回滾對應的費用估算",fontsize=12,weight='bold')
    cost = fig.add_axes([.14,.17,.80,.19])
    for run,y,label in [('pro',1,'Pro'),('flash',0,'Flash')]:
        c=data[run]['costs']; v=c['interruption_window_usd']/10000; w=c['rollback_window_usd']/10000
        cost.barh(y,v,height=.36,color=red)
        if w:cost.barh(y,w,left=v,height=.36,color='#fbf0e5',edgecolor=orange,hatch='////')
        cost.text(v+w+1.4,y,f'${(v+w)*10:.0f}k' if english else f'{v+w:.1f} 萬美元',va='center',fontsize=11,weight='bold')
    cost.set(yticks=[1,0],yticklabels=['Pro','Flash'],xlim=(0,81),ylim=(-.5,1.5),
             xticks=[0,20,40,60],xlabel='Cost (USD thousands)' if english else "費用 / 萬美元")
    if english:
        cost.set_xticklabels(['0', '200', '400', '600'])
    cost.grid(axis='x',color='#dce3e7',linewidth=.6);cost.set_axisbelow(True)
    for edge in ['top','left','right']:cost.spines[edge].set_visible(False)
    cost.spines['bottom'].set_color('#c3d0d7');cost.tick_params(axis='y',length=0,pad=8)
    fig.text(.14,.028,"Halving Pro's interruption time saves ~15 h / ~$310k." if english else "Pro 中斷時間減少一半：約省 15 小時、31 萬美元。",
             fontsize=11,color='#16857b',weight='bold')
    fig.canvas.draw()
    renderer=fig.canvas.get_renderer()
    outside=[]
    for t in fig.findobj(matplotlib.text.Text):
        if t.get_visible() and t.get_text():
            b=t.get_window_extent(renderer)
            if b.x0<0 or b.y0<0 or b.x1>fig.bbox.width or b.y1>fig.bbox.height:
                outside.append(t.get_text())
    assert not outside, outside
    outputs=[]
    for ext in ('svg','png','pdf'):
        p=output_dir/f'figure-10-mimo-interruptions.{ext}'
        fig.savefig(p,dpi=220,facecolor='white',metadata={'Creator':'AI Infra Book'})
        if ext == 'svg':
            p.write_text('\n'.join(line.rstrip() for line in p.read_text().splitlines())+'\n')
        outputs.append(p)
    check = dict(figure='figure-10-mimo-interruptions', width_pt=fig.get_figwidth()*72,
                 min_label_pt=min(t.get_fontsize() for t in fig.findobj(matplotlib.text.Text)
                                  if t.get_visible() and t.get_text()),
                 text_extent_warnings=outside)
    plt.close(fig)
    return outputs, check


if __name__ == '__main__':
    outputs, check = draw()
    check_path = HERE/'teaching-layout-validation.json'
    checks = json.loads(check_path.read_text())
    checks = [r for r in checks if r['figure'] != check['figure']] + [check]
    order = {Path(r['file']).stem: r['number'] for r in json.loads((HERE/'figure-index.json').read_text())}
    checks.sort(key=lambda r: order[r['figure']])
    check_path.write_text(json.dumps(checks, ensure_ascii=False, indent=2)+'\n')
    for path in outputs:
        print(path.relative_to(ROOT))
