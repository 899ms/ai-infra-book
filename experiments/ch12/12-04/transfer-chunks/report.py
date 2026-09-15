import hashlib,json,statistics
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent
v=json.loads((R/'verification.json').read_text());assert v['verified'] and v['total_requests']==270
s='''# Application write-size experiment

All 270 exchanges passed independent verification: 54 ASR, 162 Computer Use rounds and 54 image exchanges, including 216 formal exchanges and 54 warmups. Each workload used nine fresh Docker containers, with position-balanced whole/16KiB/64KiB write orders across three trials. Final container absence and every subrun removal are verified.

Both request and response bodies use the selected application write size. Small transcript/action responses fit in one write. Every write has an offset, length, source-slice hash and timing ledger. These sizes describe application writes, not HTTP chunked encoding, TLS records or QUIC packets. Per-write hashing and timing overhead are included. Source input is fully available before upload; recorded service starts after full upload; the full response becomes available after service. TTS source-availability/coalescing is covered separately in ../tts-chunking.

TCP_NODELAY=1 and IPPROTO_TCP=6 are verified. Receive buffers use the default policy, and QUIC initial connection/stream credit stays at 1MiB. Each isolated container uses 2 CPUs, 2GiB RAM and loopback netem configured for 80ms round-trip delay, 20Mbit/s and 0.1% loss. No new GPU inference or browser actions occur in these fixed-source transport runs.

| Workload | Protocol | Whole median seconds | 16KiB median seconds | 64KiB median seconds |
|---|---|---:|---:|---:|
'''
for w in ['asr','computer','image']:
 summary=json.loads((R/f'{w}-summary.json').read_text());key='trace_samples_s' if w=='computer' else 'samples_s'
 fig,axes=plt.subplots(1,2,figsize=(10,4.5),sharey=True);top=max(max(c[key]) for c in summary['conditions'])*1.12
 for ax,proto in zip(axes,['h1','h3']):
  med=[]
  for i,mode in enumerate(['whole','16k','64k']):
   c=next(c for c in summary['conditions'] if c['mode']==mode and c['protocol']==proto);vals=c[key];m=statistics.median(vals);med.append(m)
   ax.scatter([i-.13+.26*j/(len(vals)-1) for j in range(len(vals))],vals,color='#167d9a');ax.plot([i-.25,i+.25],[m,m],color='#bc5739',linewidth=2)
  s+=f'| {w} | {proto} | '+' | '.join(f'{m:.3f}' for m in med)+' |\n'
  ax.set_title('HTTP/1.1 + TLS 1.3' if proto=='h1' else 'HTTP/3');ax.set_xticks(range(3),['Whole','16 KiB','64 KiB']);ax.set_ylim(0,top);ax.grid(axis='y',alpha=.2)
 axes[0].set_ylabel('Complete usable result (seconds)');fig.suptitle(w.upper()+' — application write size')
 fig.text(.5,.015,('Three eight-round traces' if w=='computer' else 'Six formal requests')+' per cell. Points: all samples; bars: medians. Recorded service, actual transport.',ha='center',fontsize=9)
 fig.tight_layout(rect=[0,.04,1,.94])
 for ext in ['png','svg','pdf']:fig.savefig(R/f'{w}-results.{ext}',dpi=160)
 plt.close(fig)
s+='''
Image and ASR cells contain three fresh/reused pairs. Computer Use cells contain three complete eight-round traces, each with one fresh connection followed by seven reused requests. All samples, including slow tails, remain in the summaries and figures. These descriptive medians do not establish significance or a general protocol ranking. Earlier receive-window or reuse batches are not pooled with this batch.

Complete-result timing ends after source-result verification: exact transcript, JPEG/RGB identity, or the last stored action JSON in the trace. Group connection cleanup is excluded. Per-write enqueue/drain timestamps are not wire-delivery timestamps. Source quality limitations remain those of the original computation records.

'''
for w in ['asr','computer','image']:s+=f'![{w} samples]({w}-results.png)\n\n'
s+='''Analyzers independently check every application piece against source bytes, full response identity and semantic format, service waits, arrival conservation, connection reuse, TLS/ALPN, TCP socket settings, QUIC logs, container limits and cleanup. Run `python verify_all.py`, then `python report.py` with matplotlib installed. This completes the declared chunk-size matrix; recovery, cross-workload contribution review and acoustic measurements have separate status.
'''
(R/'README.md').write_text(s)
files={str(p.relative_to(R)):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in R.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
(R/'manifest.json').write_text(json.dumps(dict(scope='Application write-size matrix; parent exercise status separate',files=files),indent=2)+'\n')
