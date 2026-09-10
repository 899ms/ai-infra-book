import json,statistics
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=Path(__file__).absolute().parent;s=json.loads((r/'results/summary.json').read_text())
fig,axs=plt.subplots(1,3,figsize=(13,4),layout='constrained')
for cfg in s['configurations']:
 for mode,style in [('natural','-o'),('fixed','--s')]:
  groups=[[b for b in cfg['batches'] if b['concurrency']==c and b['mode']==mode and b['trial']!='warm'] for c in [7,8,15,16,20]]
  label=cfg['name'].upper()+' KV / '+mode
  for ax,key in zip(axs,['preemptions','peak_waiting','median_latency_s']):
   ax.plot([7,8,15,16,20],[statistics.mean(b[key] for b in g) for g in groups],style,label=label)
for ax in axs:ax.set_xlabel('Simultaneously submitted requests');ax.set_xticks([7,8,15,16,20]);ax.grid(alpha=.2)
axs[0].set_ylabel('Preemptions (mean over 2 runs)');axs[1].set_ylabel('Peak waiting (mean over 2 runs)');axs[2].set_ylabel('Median request time (s, mean over 2 runs)')
axs[0].legend(fontsize=7)
fig.suptitle('Online FP8 weights / 8 GiB KV / 7,239 input tokens / shared GPU')
for ext in ['png','svg','pdf']:fig.savefig(r/f'concurrency.{ext}',dpi=160)
