import json,hashlib
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;P=R.parent
one=json.loads((R/'summary.json').read_text());two=json.loads((P/'agent-dram-capacity/summary.json').read_text());left=[g for g in one['groups'] if g['phase']=='target_after'];right=[g for g in two['groups'] if g['phase']=='target_after']+[left[0]]
fig,axes=plt.subplots(1,2,figsize=(10.5,4.7))
for ax,groups,labels,title in [(axes[0],left,['4096','8192','16384'],'GPU capacity; host ratio 2'),(axes[1],right,['1.01','1.25','2 (reference)'],'Host ratio; GPU capacity 4096')]:
 total=sum(r['input_tokens'] for r in one['records'] if r['capacity']==4096 and r['phase']=='target_after');device=[g['levels']['device']/total*100 for g in groups];host=[g['levels']['host']/total*100 for g in groups]
 ax.bar(labels,device,label='Device',color='#397cab');ax.bar(labels,host,bottom=device,label='Host RAM',color='#d9983e');ax.set_ylim(0,110);ax.set_ylabel('Hit tokens / input tokens (%)');ax.set_title(title)
 for i,g in enumerate(groups):ax.text(i,device[i]+host[i]+1,f'{g["token_hit_rate"]:.2%}',ha='center',fontsize=9)
 ax.spines[['top','right']].set_visible(False);ax.set_axisbelow(True);ax.grid(axis='y',alpha=.2)
axes[0].legend(loc='upper left',bbox_to_anchor=(0,-.13),ncol=2)
fig.suptitle('Same Agent targets after 3,584-token pressure: native cache counters');fig.tight_layout();fig.savefig(R/'capacity.svg');fig.savefig(R/'capacity.png',dpi=150);plt.close(fig)
(R/'plot-sources.json').write_text(json.dumps({str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [R/'summary.json',P/'agent-dram-capacity/summary.json',R/'plot.py']},indent=2)+'\n')
