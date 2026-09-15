import hashlib,json,statistics
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;v=json.loads((R/'verification.json').read_text());assert v['verified']
s='''# Interrupted workload recovery

Independent verification passed for 60 tasks (54 formal), 222 exchanges and 36 injected interruptions. This is an application recovery experiment using actual HTTP/1.1 + TLS and HTTP/3 transfers under container loopback netem: configured 80ms RTT, 20Mbit/s and 0.1% loss. Each workload ran serially in its own pinned Docker container with 2 CPUs and 2GiB RAM. All own containers were removed.

The independent producer replays recorded source availability and survives a client disconnect. ASR disconnects after upload and response headers, before the transcript; Computer Use disconnects at that boundary only in round3 of its eight-round trace. TTS disconnects after retaining at least one complete20ms PCM frame, including any read overshoot. Every fault is checked to occur before its producer finishes.

Restart creates a new operation and replays source service; resume retrieves the original operation with no request-body reupload. TTS resume requests the exact retained-byte offset and concatenates only the remaining suffix. Already delivered Computer actions are retained. This does not simulate an action that executed but lost its acknowledgment, nor establish idempotence of arbitrary browser side effects.

Every final transcript, WAV/PCM stream and action sequence is reconstructed from raw received files and checked against the original fixed source. Producer release times and response emissions are independently checked against recorded availability. No fresh GPU inference or browser task occurs during these transport replays. TTS continuity here means exact bytes; it does not establish uninterrupted audible playback.

| Workload | Protocol | Uninterrupted median seconds | Restart median seconds | Resume median seconds |
|---|---|---:|---:|---:|
'''
for w in ['asr','tts','computer']:
 data=json.loads((R/f'{w}-summary.json').read_text());fig,axes=plt.subplots(1,2,figsize=(10,4.5),sharey=True);top=max(max(c['samples_s']) for c in data['conditions'])*1.12
 for ax,proto in zip(axes,['h1','h3']):
  med=[]
  for i,policy in enumerate(['uninterrupted','restart','resume']):
   c=next(c for c in data['conditions'] if c['protocol']==proto and c['policy']==policy);vals=c['samples_s'];m=statistics.median(vals);med.append(m)
   ax.scatter([i-.12,i,i+.12],vals,color='#167d9a');ax.plot([i-.25,i+.25],[m,m],color='#bc5739',linewidth=2)
  s+=f'| {w} | {proto} | '+' | '.join(f'{m:.3f}' for m in med)+' |\n'
  ax.set_title('HTTP/1.1 + TLS 1.3' if proto=='h1' else 'HTTP/3');ax.set_xticks(range(3),['Uninterrupted','Restart','Resume']);ax.set_ylim(0,top);ax.grid(axis='y',alpha=.2)
 axes[0].set_ylabel('Complete task (seconds)');fig.suptitle(w.upper()+' — connection interruption and recovery');fig.text(.5,.015,'Three formal tasks per cell. Includes connection close and retry; recorded producer, actual transport.',ha='center',fontsize=9);fig.tight_layout(rect=[0,.04,1,.94])
 for ext in ['png','svg','pdf']:fig.savefig(R/f'{w}-results.{ext}',dpi=160)
 plt.close(fig)
s+='''
Each cell has three formal tasks. Computer Use timing covers all eight rounds. Each exchange opens a fresh connection; task timing includes connection teardown, recovery setup and result validation. The earlier reuse/window/chunk runners use different connection and cleanup boundaries, so these absolute timings are not pooled. Source work can finish while a connection is closing; recovery does not assume that the original operation is still pending when the retry starts.

'''
for w in ['asr','tts','computer']:s+=f'![{w} recovery samples]({w}-results.png)\n\n'
s+='| Workload | Protocol | Policy | Upload bytes per task | Retained bytes per task | Discarded prefix bytes per task | Source jobs per task |\n|---|---|---|---|---|---|---|\n'
for w in ['asr','tts','computer']:
 for c in json.loads((R/f'{w}-summary.json').read_text())['conditions']:
  cells=[str([a[k] for a in c['accounting']]) for k in ['upload_bytes','retained_response_bytes','discarded_prefix_bytes','source_jobs']]
  s+=f"| {w} | {c['protocol']} | {c['policy']} | "+' | '.join(cells)+' |\n'
s+='\nRetained/discarded application bytes do not count wire overhead or bytes already queued by the server. Post-interruption and connection-close durations are retained per task in the summary accounting.\n\n'

s+='''All samples are retained. Descriptive medians from three trials do not establish statistical significance or a general protocol ranking. Expected server reset/broken-pipe errors are retained and accepted only for deliberately interrupted operations; other server errors fail verification. The release/emission ledger is not a wire-packet trace.

Run `python verify_all.py` to reconstruct outcomes, validate operation counts, fault timing, source and response identities, release schedules, TLS/ALPN, TCP_NODELAY/proto metadata, QUIC parameters, resource isolation and cleanup. Run `python report.py` with matplotlib for this report and figures. Source bindings and the artifact manifest support reproduction. Physical acoustic measurement and the parent exercise's final contribution review have separate status.
'''
(R/'README.md').write_text(s)
files={str(p.relative_to(R)):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in R.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
(R/'manifest.json').write_text(json.dumps(dict(scope='ASR/TTS/Computer recorded-producer recovery; parent status separate',files=files),indent=2)+'\n')
