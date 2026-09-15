import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;rows=json.loads((R/'results.json').read_text())['rows'];fig,axes=plt.subplots(1,2,figsize=(12,5))
profiles=['A100-assumed','A800-assumed','H20-assumed-100'];colors=['#167d9a','#e68a33','#8776aa']
for ax,model in zip(axes,['qwen3-8b','qwen3-235b-a22b']):
 selected=[r for r in rows if r['model']==model and r['topology']=='eight-gpu-nodes-shared25'];ids=sorted({r['candidate'] for r in selected});labels=[]
 for i,idx in enumerate(ids):
  for j,(p,color) in enumerate(zip(profiles,colors)):
   r=next(r for r in selected if r['candidate']==idx and r['profile']==p);x=i+(j-1)*.24;ax.bar(x,r['conditional_matrix_transfer_days'],width=.22,color=color,label=p if i==0 else None)
   if r['capacity_rejected']:ax.scatter([x],[r['conditional_matrix_transfer_days']],marker='x',color='red',s=45,zorder=4)
  labels.append(f"PP{r['pp']} / m{r['microbatches']}")
 ax.set_xticks(range(len(ids)),labels);ax.set_title(model);ax.set_ylabel('Conditional matrix + transfer days');ax.grid(axis='y',alpha=.2)
fig.suptitle('100B tokens — declared GPipe schedule and assumed effective rates')
fig.text(.5,.02,'Eight-GPU nodes with shared25GB/s cross-node fabric. Red ×: memory already exceeded. No bar proves full training feasibility.',ha='center',fontsize=9)
handles,labels=axes[0].get_legend_handles_labels()
fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.925),ncol=3,fontsize=9)
fig.tight_layout(rect=[0,.05,1,.84])
for ext in ['png','svg','pdf']:fig.savefig(R/f'comparison.{ext}',dpi=150)
