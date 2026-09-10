import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=Path(__file__).absolute().parent
s=json.loads((r/'results/summary.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(10,4),layout='constrained')
for i,c in enumerate(s['configurations']):
 rows=[x for x in c['summary'] if x['mode']=='natural']
 x=[j+(i-.5)*.35 for j in range(4)]
 label={'bf16':'BF16 KV','fp8':'FP8 KV'}[c['name']]
 axes[0].bar(x,[v['correct'] for v in rows],.35,label=label)
 axes[1].bar(x,[v['median_latency_s'] for v in rows],.35,label=label)
for ax in axes:
 ax.set_xticks(range(4),['128 / 1','128 / 4','512 / 1','512 / 4']);ax.set_xlabel('Document rows / concurrency');ax.legend()
axes[0].set_ylabel('Exact answers / 8');axes[0].set_ylim(0,8.8)
axes[1].set_ylabel('Median request time (s)')
fig.suptitle('Online FP8 weights; 8 GiB KV budget; shared RTX PRO 6000')
for ext in ['png','svg','pdf']:fig.savefig(r/f'quantized-kv.{ext}',dpi=160)
