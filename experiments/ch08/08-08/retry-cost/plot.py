import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=Path(__file__).absolute().parent
s=[json.loads((r/name/'summary.json').read_text()) for name in ['results','results-regression']]
fig,ax=plt.subplots(1,2,figsize=(9,4),layout='constrained');labels=['16 new documents\n32 task executions','4 regression documents\n8 task executions']
for i,k in enumerate(['first_correct','final_correct']):
 values=[x[k]/x['tasks'] for x in s];bars=ax[0].bar([j+(i-.5)*.32 for j in range(2)],values,.32,label=['First attempt','After policy'][i])
 for bar,x in zip(bars,s):ax[0].text(bar.get_x()+bar.get_width()/2,bar.get_height()+.01,f"{x[k]}/{x['tasks']}",ha='center',fontsize=9)
ax[0].set_xticks(range(2),labels);ax[0].set_ylim(0,1.22);ax[0].set_ylabel('Exact-answer fraction');ax[0].legend(loc='upper center',ncol=2,fontsize=8)
first=[x['first_generation_s']/x['tasks'] for x in s];retry=[(x['formal_generation_s']-x['first_generation_s'])/x['tasks'] for x in s];overhead=[(x['formal_total_s']-x['formal_generation_s'])/x['tasks'] for x in s]
ax[1].bar(range(2),first,label='First generation');ax[1].bar(range(2),retry,bottom=first,label='Retry generation');ax[1].bar(range(2),overhead,bottom=[a+b for a,b in zip(first,retry)],label='Switch/check/observation')
ax[1].set_xticks(range(2),labels);ax[1].set_ylabel('Mean observed seconds per task');ax[1].legend(fontsize=8)
fig.suptitle('Known-answer retry policy / separate workload groups / shared GPU')
for ext in ['png','svg','pdf']:fig.savefig(r/f'retry-cost.{ext}',dpi=160)
