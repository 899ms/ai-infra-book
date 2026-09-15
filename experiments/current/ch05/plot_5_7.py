from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;d=json.loads((R/'5-7-results.json').read_text());names=['generic','bucket','specialized'];colors=['#2878b5','#d99b26','#279269']
fig,axes=plt.subplots(1,2,figsize=(13,4.7),layout='constrained')
ax=axes[0]
for i,s in enumerate(names):
 prep={'generic':100,'bucket':400,'specialized':900}[s];t=d['cases']['8']['groups'][s]['group_ms']
 ax.barh(i,prep,color='#c7cbd2',height=.55)
 for r in range(70):ax.barh(i,t,left=prep+r*t,color=colors[i],edgecolor='white',linewidth=.2,height=.55)
 ax.text(prep+70*t+12,i,f'{prep+70*t:.1f} ms',va='center',fontsize=9)
ax.set(yticks=range(3),yticklabels=names,xlabel='Time (ms)',title='Original example: preparation + 70 groups',xlim=(0,1650));ax.invert_yaxis();ax.grid(axis='x',alpha=.2)
ax.text(.02,.03,'Gray: preparation. Each colored segment: one group.',transform=ax.transAxes,fontsize=9)
ax=axes[1]
for s,c in zip(names,colors):
 for mode,ls in [('cold','-'),('bucket_cached','--')]:
  if mode=='bucket_cached' and s!='bucket':continue
  rows=d['cases']['4']['winners'][mode][:350]
  ax.plot([r['groups'] for r in rows],[r['total_ms'][s] for r in rows],color=c,ls=ls,label=s+(' (cached)' if mode!='cold' else ''))
ax.set(xlabel='Repeated groups (4 small + 2 large calls)',ylabel='Preparation + execution (ms)',title='Changed mixture: pairwise crossings and minimum');ax.legend();ax.grid(alpha=.2)
for ext in ('svg','png'):fig.savefig(R/f'5-7-timeline.{ext}',dpi=160)
