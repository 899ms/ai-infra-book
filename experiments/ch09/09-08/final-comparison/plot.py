import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = Path(__file__).resolve().parent
P = HERE.parent
sources = [P/'agent-policy-replay/results.json', P/'v4-state-accounting/results.json']
dense, v4 = [json.loads(p.read_text()) for p in sources]
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
fig, axes = plt.subplots(3, 2, figsize=(13, 12))
ax = axes[0, 0]
ax.set_axis_off()
ax.set_title('A  Recovery path and state contract', loc='left', weight='bold')
labels = ['HBM', 'DRAM', 'Local disk', 'Remote pool']
for i, label in enumerate(labels):
    x = .025+i*.245
    ax.add_patch(FancyBboxPatch((x, .60), .19, .16, boxstyle='round,pad=0.012',
                               transform=ax.transAxes, facecolor='#e3edf5', edgecolor='#385b77'))
    ax.text(x+.095, .68, label, ha='center', va='center', transform=ax.transAxes)
    if i < 3:
        ax.annotate('', xy=(x+.24, .68), xytext=(x+.195, .68), xycoords='axes fraction',
                    arrowprops=dict(arrowstyle='->', color='#385b77'))
ax.text(.025, .43, 'Search a continuous prefix; first missing page → recompute.\nWorker restart drops volatile tiers; invalidation drops all indexes.',
        transform=ax.transAxes, va='top', linespacing=1.6)
ax.text(.025, .18, 'V4 complete snapshot = window + compressed/index history\n+ FP32 compressor buffers + identity/position metadata.',
        transform=ax.transAxes, va='top', linespacing=1.6)

styles = [('full', 'Every turn', '#20639b'), ('periodic4', 'Every 4 turns', '#d27b21'), ('recompute', 'Recompute', '#66746b')]
panels = [(axes[0,1], 'B  Dense-page replay: token hit rate', 'token_hit_rate', 100, 'Token hits (%)'),
          (axes[1,0], 'C  Dense-page replay: checkpoint writes', 'write_bytes', 1/2**20, 'Written MiB'),
          (axes[1,1], 'D  Dense-page replay: completion proxy', 'estimated_trace_completion_s', 1, 'Composed trace seconds')]
for ax, title, metric, scale, ylabel in panels:
    for policy, label, color in styles:
        rows = [r for r in dense['scenarios'] if r['policy']==policy and r['fault']=='restart7'
                and r['capacity_pages']['hbm']==r['capacity_pages']['dram']==r['capacity_pages']['remote']==0]
        rows.sort(key=lambda r:r['capacity_pages']['local'])
        y = [(r[metric]['local'] if metric=='write_bytes' else r[metric])*scale for r in rows]
        ax.plot([r['capacity_pages']['local'] for r in rows], y, 'o-', label=label, color=color)
    ax.set(title=title, xlabel='Local retained pages (2.25 MiB each)', ylabel=ylabel)
    ax.set_xticks([0,64,256]);ax.grid(alpha=.2);ax.legend(fontsize=9)

ax = axes[2,0]
x = [r['turn']+1 for r in v4['endpoints']]
keys = ['window_history_bytes', 'compressed_history_bytes', 'index_history_bytes']
series = [[r['components'][k]/2**20 for r in v4['endpoints']] for k in keys]
series.append([r['summary']['compressor_buffer_bytes']/2**20 for r in v4['endpoints']])
ax.stackplot(x, *series, labels=['Window', 'Compressed', 'Index', 'FP32 buffers'],
             colors=['#20639b','#44a5a1','#98ca83','#dba053'])
ax.set(title='E  V4 layout calculation: full snapshot', xlabel='Agent-shaped turn', ylabel='Logical tensor MiB')
ax.legend(fontsize=9, loc='upper left');ax.grid(alpha=.2)
ax = axes[2,1]
for policy, label, color in styles:
    rows = [r for r in v4['scenarios'] if r['policy']==policy and r['fault']=='invalidate7']
    ax.plot([r['budget_mib'] for r in rows], [r['recompute_tokens'] for r in rows], 'o-', label=label, color=color)
ax.set(title='F  V4 layout calculation: recovery work', xlabel='Complete-snapshot budget (MiB)', ylabel='Recomputed input positions')
ax.set_xticks([0,16,32,64]);ax.grid(alpha=.2);ax.legend(fontsize=9)
fig.suptitle('Figure 9-7 · Multi-level cache retention and recovery', fontsize=17, weight='bold')
fig.text(.06, .025, 'B–D: defined page-LRU replay, restart before turn 7; timing calibrated from actual dense-Qwen records.\n'
         'E–F: pinned V4 layout on the same token-count/prefix fixture, not V4 inference or tokenizer output.\n'
         'F restarts every request and invalidates storage before turn 7. Logical budgets exclude the execution working set.', fontsize=10)
fig.tight_layout(rect=(0,.085,1,.96), h_pad=2.5)
for ext in ['svg','pdf','png']:
    fig.savefig(HERE/f'figure-9-7.{ext}', dpi=150)
sources.append(Path(__file__).resolve())
(HERE/'plot-sources.json').write_text(json.dumps({str(p.relative_to(P.parents[2])):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},indent=2)+'\n')
