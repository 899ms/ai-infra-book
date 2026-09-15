"""Render audited timelines on common axes; source values remain in results JSON."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
R=Path(__file__).resolve().parent;d=json.loads((R/'4-4-results.json').read_text())
plt.rcParams.update({'font.size':9,'svg.fonttype':'none'})
fig,axes=plt.subplots(4,2,figsize=(14,11),sharex=True,layout='constrained')
for j,compute in enumerate((128,64)):
 for i in range(4):
  ax=axes[i,j];p=next(x for x in d['pipelines'] if x['input_slots']==i+1 and x['compute_ticks']==compute and x['extra_latency_ticks']==128)
  for c in p['chunks']:
   y=c['chunk'];ax.barh(y,c['slot_released']-c['issue_start'],left=c['issue_start'],height=.72,color='#e0e3e7')
   ax.barh(y,64,left=c['issue_start'],height=.32,color='#2878b5')
   ax.barh(y,compute,left=c['compute_start'],height=.32,color='#26905b')
   ax.plot([c['data_ready']]*2,[y-.37,y+.37],color='#c56900',lw=1.5)
  ax.set(title=f'{i+1} slot(s), compute {compute}: finish {p["finish_tick"]}',yticks=range(4),yticklabels=[f'Block {k}' for k in range(4)],xlim=(0,1320));ax.invert_yaxis();ax.grid(axis='x',alpha=.2)
for ax in axes[-1,:]:ax.set_xlabel('Teaching ticks (common scale)')
fig.suptitle('Input pipeline: transfer 64 + additional latency 128; slot released after compute')
fig.legend(handles=[Patch(color=c,label=l) for c,l in [('#e0e3e7','Slot occupied'),('#2878b5','Transfer'),('#26905b','Compute'),('#c56900','Data ready marker')]],loc='outside lower center',ncol=4)
for ext in ('png','svg'):fig.savefig(R/f'4-4-input.{ext}',dpi=160)
plt.close(fig)
fig,axes=plt.subplots(5,1,figsize=(14,12),sharex=True,layout='constrained')
colors={'qk':'#2878b5','scores':'#a58ac1','softmax':'#e3a235','probabilities':'#8065a0','pv':'#26905b'}
for ax,h in zip(axes,d['handoff']):
 s=h['scenario'];groups=h['summary']['groups']
 for o in h['slot_ownership']:ax.barh(o['group'],o['release_tick']-o['start_tick'],left=o['start_tick'],height=.8,color='#e0e3e7')
 for t in h['timeline']:
  g,stage=t['id'].split('.');ax.barh(int(g[1:]),t['duration_ticks'],left=t['start_tick'],height=.48,color=colors[stage])
 ax.set(title=f'{s["path"]}, {s["group_rows"]} rows/group, {s["slots"]} slot(s): first Softmax {h["summary"]["first_vector_start_tick"]}, finish {h["summary"]["finish_tick"]}',yticks=range(groups),yticklabels=[f'Group {k}' for k in range(groups)],xlim=(0,5300));ax.invert_yaxis();ax.grid(axis='x',alpha=.2)
axes[-1].set_xlabel('Teaching ticks (common scale)');fig.suptitle('Complete query-row groups: QK → scores → Softmax → probabilities → PV')
fig.legend(handles=[Patch(color=c,label=k) for k,c in colors.items()],loc='outside lower center',ncol=5)
for ext in ('png','svg'):fig.savefig(R/f'4-4-handoff.{ext}',dpi=160)
plt.close(fig)
