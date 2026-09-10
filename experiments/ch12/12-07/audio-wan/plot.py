import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
B=Path(__file__).absolute().parent;x=json.loads((B/'analysis.json').read_text())
fig,axs=plt.subplots(1,3,figsize=(12,3.9))
for stack,color in [('baseline','#666666'),('queqiao','#0072B2')]:
 full=[r for r in x['conditions'] if r['stack']==stack and not r['intentional_cancel']]
 cancel=[r for r in x['conditions'] if r['stack']==stack and r['intentional_cancel']]
 for ax,key,rows,factor in [(axs[0],'source_starvation_bytes',full,1/88.2),(axs[1],'buffer_at_start',full,1/88.2),(axs[2],'pipe_eof_to_abort_return_ms',cancel,1)]:
  ax.plot([r['round'] for r in rows],[r[key]*factor for r in rows],'-o',color=color,label=stack)
for ax,title in zip(axs,['Missing source audio at callbacks','Actual device-start prebuffer','Pipe EOF to device abort return']):
 ax.set_title(title,fontsize=10);ax.set_xticks(range(4),['0: on','1: off','2: off','3: on']);ax.set_xlabel('Round: Queqiao pool');ax.set_ylabel('Milliseconds');ax.set_ylim(bottom=0);ax.grid(alpha=.2);ax.legend(fontsize=8)
fig.suptitle('Mac ↔ RTX through current OS route (utun1024); real device callbacks, muted')
fig.tight_layout();fig.savefig(B/'wan-audio.png',dpi=150);fig.savefig(B/'wan-audio.svg')
