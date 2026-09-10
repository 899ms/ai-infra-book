import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
B=Path(__file__).absolute().parent;x=json.loads((B/'analysis.json').read_text())
fig,axs=plt.subplots(1,3,figsize=(12,3.8))
for stack,color in [('baseline','#666666'),('queqiao','#0072B2')]:
 full=[r for r in x['conditions'] if r['stack']==stack and not r['intentional_cancel']]
 cancel=[r for r in x['conditions'] if r['stack']==stack and r['intentional_cancel']]
 axs[0].plot([r['round'] for r in full],[r['first_complete_frame_ms'] for r in full],'-o',color=color,label=stack)
 axs[1].plot([r['round'] for r in full],[r['software_sink_start_ms'] for r in full],'-o',color=color,label=stack)
 axs[2].plot([r['round'] for r in cancel],[r['cancel_to_origin_observation_ms'] for r in cancel],'-o',color=color,label=stack)
for ax,title in zip(axs,['First complete 20 ms PCM frame','Software sink start (3-frame buffer)','Client close to origin observation']):
 ax.set_title(title,fontsize=10);ax.set_xticks(range(4),['0: on','1: off','2: off','3: on']);ax.set_xlabel('Round: Queqiao pool');ax.set_ylabel('Elapsed time (ms)');ax.set_ylim(bottom=0);ax.grid(alpha=.2);ax.legend(fontsize=8)
fig.suptitle('Fixed Fish PCM over native transports; warm connections, emulated 40 ms RTT')
fig.tight_layout();fig.savefig(B/'audio-tunnel.png',dpi=150);fig.savefig(B/'audio-tunnel.svg')
