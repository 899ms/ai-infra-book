import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=Path(__file__).absolute().parent;rows=json.loads((r/'analysis.json').read_text());fig,axes=plt.subplots(1,2,figsize=(10,4),layout='constrained')
for ax,phase in zip(axes,['decode','prefill']):
 data=[x for x in rows if x['phase']==phase];xx=[0,1]
 for j,(stage,label,color) in enumerate([(0,'Cold call','#4779b3'),(1,'Subsequent call','#d78336')]):
  values=[x['absolute_peak_increments'][stage]/2**20 for x in data]
  bars=ax.bar([i+(j-.5)*.34 for i in xx],values,width=.34,label=label,color=color)
  ax.bar_label(bars,fmt='%.2f',padding=3,fontsize=9)
 ax.set_xticks(xx,['INT8 partial sums','Dequantize + BF16']);ax.set_ylabel('Peak allocated above empty context (MiB)');ax.set_title('Actual decode M=1' if phase=='decode' else 'Prefill M=512');ax.set_ylim(0,50);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
axes[0].legend(loc='upper left',fontsize=8)
fig.suptitle('Same INT8 weights; PyTorch allocator only',fontsize=13)
for ext in ['png','svg','pdf']:fig.savefig(r/('workspace.'+ext),dpi=160)
