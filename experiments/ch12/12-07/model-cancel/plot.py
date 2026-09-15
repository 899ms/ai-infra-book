import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

R = Path(__file__).resolve().parent
data = json.loads((R/'summary.json').read_text())
events = [json.loads(x) for x in (R/'results/events.jsonl').read_text().splitlines()]
rows = [r for r in data['rows'] if r['request_id']!='warmup']
fig, ax = plt.subplots(figsize=(11,5))
for i, row in enumerate(rows):
    rid = row['request_id']
    start = next(e['time_ns'] for e in events if e['request_id']==rid and e['event']=='client_start')
    terminal = row['semantic_terminal_ms']/1000
    ax.barh(i, terminal, height=.40, color='#bbd1e2')
    if row['cancel']:
        cancel = next((e['time_ns']-start)/1e9 for e in events if e['request_id']==rid and e['event']=='client_cancel_begin')
        ax.barh(i, terminal-cancel, left=cancel, height=.40, color='#dc9558')
        ax.plot(cancel,i,'kx',ms=8,label='Client close' if i==1 else None)
    ax.plot(row['handler_exit_ms']/1000,i,'|',color='#23533b',ms=18,mew=2,label='HTTP handler exit' if i==0 else None)
    ax.plot(terminal,i,'o',color='#385c7a',ms=5,label='Natural model terminal' if i==0 else None)
ax.set_yticks(range(len(rows)),[r['request_id'] for r in rows]);ax.invert_yaxis()
ax.set(xlabel='Seconds from request start (same-host monotonic clock)',
       title='HTTP response cancellation leaves the semantic job running')
ax.grid(axis='x',alpha=.2);ax.legend(loc='lower right',fontsize=9)
fig.text(.08,.025,'Orange: time after client close until natural model terminal. Fish1.5, eager execution with CUDA-sync observation.\n'
         'Loopback backend probe; this is not a live Queqiao cancellation latency or an acoustic measurement.',fontsize=9)
fig.tight_layout(rect=(0,.10,1,1))
for ext in ['svg','png']:
    fig.savefig(R/f'model-cancel.{ext}',dpi=150)
