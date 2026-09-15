import hashlib,json,statistics
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;S=json.loads((R/'summary.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(10,4.5),sharey=True);top=max(max(c['trace_samples_s']) for c in S['conditions'])*1.12
for ax,proto in zip(axes,['h1','h3']):
 for i,mode in enumerate(['default','64k','4m']):
  c=next(c for c in S['conditions'] if c['protocol']==proto and c['mode']==mode);ax.scatter([i-.1,i,i+.1],c['trace_samples_s'],s=35,color='#167d9a');ax.plot([i-.25,i+.25],[c['median_trace_s']]*2,color='#bc5739',linewidth=2)
 ax.set_xticks(range(3),['Default','64 KiB','4 MiB']);ax.set_ylim(0,top);ax.grid(axis='y',alpha=.2);ax.set_title('HTTP/1.1 + TLS 1.3' if proto=='h1' else 'HTTP/3')
axes[0].set_ylabel('Complete eight-round trace (seconds)');fig.suptitle('Computer Use recorded trace: receive configuration')
fig.text(.5,.015,'Three traces per cell; actual screenshot/action bytes with recorded model-service waits. No new browser task.',ha='center',fontsize=9)
fig.tight_layout(rect=[0,.04,1,.94])
for ext in ['png','svg','pdf']:fig.savefig(R/f'computer-window-results.{ext}',dpi=160)
plt.close(fig)
s='''# Computer Use receive configuration across the complete trace

All162 real network exchanges passed independent verification (144 formal,18 warmups). Each formal condition transfers all eight screenshot/instruction requests and actual action responses from the first successful structured Qwen3-VL-8B browser trial in [source records](../computer-use/README.md). The measured per-round model-service waits are replayed after complete upload; no new GPU calls or browser actions occur in these transport trials.

![Every eight-round trace completion time](computer-window-results.png)

| Mode | Protocol | Median validated round ms | Three complete trace times, seconds | Median trace seconds |
|---|---|---:|---|---:|
'''
for c in S['conditions']:s+=f"| {c['mode']} | {c['protocol']} | {1000*c['median_s']:.3f} | "+' / '.join(f'{t:.3f}' for t in c['trace_samples_s'])+f" | {c['median_trace_s']:.3f} |\n"
s+='''
Each cell includes three traces,24 formal rounds with different screenshot/instruction sizes and service times. The sequence is identical across all settings. A trace uses one fresh connection followed by seven reused requests; round medians mix both and are not pure warm latency. Trace time runs from group start through final action-JSON validation, excluding group connection cleanup and source browser screenshot/action execution. The fixed3.158439950s sum of source model-service time is common to each trace. Smaller differences among these three-sample cells do not establish statistical significance or general protocol superiority.

## Intervention and proof

Three trials use position-balanced mode order default/64k/4m,64k/4m/default,4m/default/64k. Each fresh Docker container holds network-none/NET_ADMIN,2CPU/2GiB,netem80ms RTT,20Mbit/s,0.1% random loss. One step0 warmup per protocol precedes each subrun's two formal traces; warmups are excluded from table statistics. There is no concurrent round execution.

TCP sets SO_RCVBUF before client connect and on the listener before accept; defaults leave receive autotuning available,64KiB/4MiB read back as131072/8388608 bytes. QUIC sets initial connection and stream credit on both endpoints, verified by qlogs; those credits may grow. These are different receive mechanisms and do not change the congestion algorithm. Raw TCP_INFO,readbacks,QUIC negotiated parameters and MAX frames are retained in each subrun and summary.json.

Independent verification checks all eight source request/response file hashes, every actual server upload hash and per-step service wait, parsed action JSON and response hash, complete step order, fresh/reused connection identities,TLS/ALPN,all81 HTTP/3 response headers,transport receive settings,netem drain,container resources and all nine container removals. Source screenshots and task state remain in the original live-model report. Correctly replaying a stored action does not establish safe action retries or new semantic model success.

The client and server share a container event loop; qlog/TCP sampling overhead,host scheduling and stochastic packet loss affect these measurements. Absolute times must not be pooled with other runners that use different request/cleanup boundaries. Revalidate with python analyze.py; regenerate the figure/report with the matplotlib environment and python report.py. PROTOCOL.md and orchestrate.py define reproduction. Window comparisons now cover the four stated workload types; missing chunking/recovery cells and final contribution review remain listed in ../COVERAGE-REVIEW.md. Acoustic playback is still unmeasured.
'''
(R/'README.md').write_text('> Socket-default qualification: see [TCP_NODELAY diagnostic](SOCKET-DEFAULTS.md). A full matched rerun is complete in ../receive-windows; do not pool this batch with earlier implicit-socket TCP timings.\n\n'+s)
files={str(p.relative_to(R)):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in R.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
(R/'manifest.json').write_text(json.dumps(dict(scope='Complete Computer Use record receive-configuration comparison; no new model/browser task',files=files),indent=2)+'\n')
