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
 for ax,key,rows in [(axs[0],'buffer_at_start',full),(axs[1],'first_pipe_to_callback_ms',full),(axs[2],'pipe_eof_to_abort_return_ms',cancel)]:
  factor=1/88.2 if key=='buffer_at_start' else 1
  ax.plot([r['round'] for r in rows],[r[key]*factor for r in rows],'-o',color=color,label=stack)
for ax,title in zip(axs,['Actual prebuffer at stream start','First pipe bytes to first callback','Pipe EOF to Pa_AbortStream return']):
 ax.set_title(title,fontsize=10);ax.set_xticks(range(4),['0: on','1: off','2: off','3: on']);ax.set_xlabel('Round: Queqiao pool');ax.set_ylabel('Milliseconds');ax.set_ylim(bottom=0);ax.grid(alpha=.2);ax.legend(fontsize=8)
fig.suptitle('Muted MacBook Pro Speakers / PortAudio callbacks; loopback + emulated path')
fig.tight_layout();fig.savefig(B/'device-clock.png',dpi=150);fig.savefig(B/'device-clock.svg')
