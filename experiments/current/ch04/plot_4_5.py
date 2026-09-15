import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;d=json.loads((R/'4-5-results.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(13,4.5),layout='constrained')
ax=axes[0];ax.plot([x['rows'] for x in d['curves']],[x['intensity'] for x in d['curves']],color='#2878b5',label='Q projection')
for h,c in zip(d['profiles'],('#e09a23','#26905b')):
 ax.axhline(h['matrix_flops_s']/h['memory_bytes_s'],color=c,ls='--',label=h['id']+' P/BW')
ax.set(xlabel='Input rows M',ylabel='FLOPs per logical byte',title='BF16 Q projection: K=N=4096',xlim=(1,256));ax.legend();ax.grid(alpha=.2)
ax=axes[1]
for h,c in zip(d['profiles'],('#e09a23','#26905b')):
 for label,ls in [('base','-'),('matrix2','--'),('bandwidth2',':')]:
  rows=[r for r in d['projection'] if r['device']==h['id'] and r['change']==label]
  ax.plot([r['rows'] for r in rows],[r['bound_s']*1e6 for r in rows],color=c,ls=ls,label=h['id']+' '+label)
ax.set(xlabel='Input rows M',ylabel='Conditional service budget (µs)',title='Independent compute and bandwidth changes',xlim=(1,256));ax.legend(fontsize=8);ax.grid(alpha=.2)
for ext in ('svg','png'):fig.savefig(R/f'4-5-projection.{ext}',dpi=160)
