import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=Path(__file__).absolute().parent;s=json.loads((r/'analysis.json').read_text());values=[]
for mode in ['off','on']:
 raw=[json.loads(x) for x in (r/'reference'/mode/'scheduler.jsonl').read_text().splitlines()]
 values.append((max(x['kv_usage'] for x in raw)*100,sum(x['preemptions'] for x in raw)))
values +=[(s[m]['peak_kv_usage']*100,s[m]['preemptions']) for m in ['off','on']]
fig,axes=plt.subplots(1,2,figsize=(10,4),layout='constrained');labels=['Serial\nAPC off','Serial\nAPC on','4 in flight\nAPC off','4 in flight\nAPC on']
for i,ax in enumerate(axes):
 bars=ax.bar(labels,[v[i] for v in values],color=['#9aabbc','#9aabbc','#4c83b7','#d68a42']);ax.bar_label(bars,fmt='%.2f' if i==0 else '%.0f',padding=3);ax.set_ylim(0,115 if i==0 else 4);ax.set_ylabel('Peak sampled KV pool usage (%)' if i==0 else 'Observed request preemptions');ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
fig.suptitle('Same prompts and answers; finite KV capacity (single run per condition)')
for ext in ['png','svg','pdf']:fig.savefig(r/('concurrency.'+ext),dpi=160)
