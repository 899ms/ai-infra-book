import hashlib,json,statistics
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;V=json.loads((R/'verification.json').read_text());assert V['verified'] and V['total_requests']==324
S={w:json.loads((R/f'{w}-summary.json').read_text()) for w in ['image','asr','tts','computer']}
for w,title in [('image','Complete image'),('asr','Complete ASR transcript'),('tts','Complete TTS audio'),('computer','Complete Computer Use trace')]:
 key='trace_samples_s' if w=='computer' else 'samples_s';fig,axes=plt.subplots(1,2,figsize=(10,4.5),sharey=True);top=max(max(c[key]) for c in S[w]['conditions'])*1.12
 for ax,proto in zip(axes,['h1','h3']):
  for i,mode in enumerate(['default','64k','4m']):
   c=next(c for c in S[w]['conditions'] if c['mode']==mode and c['protocol']==proto);values=c[key];n=len(values);xx=[i-.13+.26*j/(n-1) for j in range(n)]
   ax.scatter(xx,values,color='#167d9a',s=30);ax.plot([i-.25,i+.25],[statistics.median(values)]*2,color='#bc5739',linewidth=2)
  ax.set_title('HTTP/1.1 + TLS 1.3' if proto=='h1' else 'HTTP/3');ax.set_xticks(range(3),['Default','64 KiB','4 MiB']);ax.set_ylim(0,top);ax.grid(axis='y',alpha=.2)
 axes[0].set_ylabel('Seconds');fig.suptitle(title+' — receive limits with TCP_NODELAY=1')
 fig.text(.5,.015,('Three eight-round traces' if w=='computer' else 'Six formal requests')+' per cell; recorded source service, actual transport. Old socket batches are not pooled.',ha='center',fontsize=9);fig.tight_layout(rect=[0,.04,1,.94])
 for ext in ['png','svg','pdf']:fig.savefig(R/f'{w}-results.{ext}',dpi=160)
 plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(10,4.5),sharey=True);top=max(max(c['first_frame_samples_ms']) for c in S['tts']['conditions'])*1.12
for ax,proto in zip(axes,['h1','h3']):
 for i,mode in enumerate(['default','64k','4m']):
  c=next(c for c in S['tts']['conditions'] if c['mode']==mode and c['protocol']==proto);v=c['first_frame_samples_ms'];ax.scatter([i-.13+.26*j/5 for j in range(6)],v,color='#167d9a',s=30);ax.plot([i-.25,i+.25],[c['first_frame_ms']]*2,color='#bc5739',linewidth=2)
 ax.set_title('HTTP/1.1 + TLS 1.3' if proto=='h1' else 'HTTP/3');ax.set_xticks(range(3),['Default','64 KiB','4 MiB']);ax.set_ylim(0,top);ax.grid(axis='y',alpha=.2)
axes[0].set_ylabel('First complete20ms PCM available (ms)');fig.suptitle('TTS first-frame availability — TCP_NODELAY=1');fig.text(.5,.015,'Client PCM availability, not acoustic playback. Six formal requests per cell; source release trace held fixed.',ha='center',fontsize=9);fig.tight_layout(rect=[0,.04,1,.94])
for ext in ['png','svg','pdf']:fig.savefig(R/f'tts-first-frame.{ext}',dpi=160)
plt.close(fig)
s='''# Receive-window comparison with matched TCP socket settings

All324 exchanges passed independent verification:54 image,54 ASR,54 TTS and162 Computer Use rounds (252 formal,72 warmups). Every data-carrying TCP socket uses explicit TCP_NODELAY=1 and IPPROTO_TCP metadata,checked at client ready/close,server upload records/samples and the listener. This matches the setting reproduced for the earlier implicit asyncio client path. All36 own Docker containers were removed.

The [fresh socket diagnostic](../socket-defaults/README.md) explains why this full rerun was necessary:manual proto0 sockets in the earlier window batches bypassed asyncio's NODELAY default. Those earlier results remain intact and qualified. This rerun includes all protocols/configurations,including unchanged QUIC; old/new batches are not pooled. The diagnostic proves socket-option behavior,not that every old/new latency difference was caused solely by NODELAY.

Each workload uses three position-balanced receive-mode orders:default/64k/4m,64k/4m/default,4m/default/64k. TCP changes only SO_RCVBUF across modes; QUIC changes initial connection and stream credit on both endpoints. TCP readback doubles explicit requests to131072/8388608 bytes; default buffers may grow. QUIC defaults are1MiB each and credits may grow dynamically. A buffer bound is not an advertised wire window,and QUIC credit is not TCP congestion window.

## Complete usable-result timing

| Workload | Protocol | Default median seconds |64KiB median seconds |4MiB median seconds |
|---|---|---:|---:|---:|
'''
for w in S:
 for proto in ['h1','h3']:
  values=[next(c['median_trace_s' if w=='computer' else 'median_s'] for c in S[w]['conditions'] if c['mode']==m and c['protocol']==proto) for m in ['default','64k','4m']]
  s+=f'| {w} | {proto} | '+' | '.join(f'{v:.3f}' for v in values)+' |\n'
s+='''
Image/ASR/TTS cells each have six formal requests (three fresh/reused pairs). Computer Use cells have three complete eight-round traces,each one fresh connection followed by seven reused requests. Its pooled round medians are also saved, but the table uses complete trace duration. These are descriptive medians; all samples and slow tails are retained. Small differences do not establish statistical significance or a general protocol ranking.

Image completes after JPEG/RGB verification; ASR after exact UTF8 verification; TTS after complete WAV/PCM verification; Computer trace after the final stored action JSON validates. Request/trace timing excludes group connection cleanup. The original model/CPU service is replayed after complete upload,with no new GPU calls or browser actions. Source identities and quality limitations are unchanged from their live-computation records. Absolute timings with different cleanup/processing boundaries must not be pooled.

'''
for w in S:s+=f'![{w} complete-result samples]({w}-results.png)\n\n'
s+='''## TTS first playable bytes

The original294-part source client-read availability schedule is replayed,not replaced with a single model wait. First response body may be only the WAV header. Complete20ms/three-frame thresholds are1808/5336 bytes for the fixed mono44100Hz PCM16 WAV.

| Protocol | Mode | First body ms | First20ms PCM ms | Three frames ms |
|---|---|---:|---:|---:|
'''
for c in S['tts']['conditions']:s+=f"| {c['protocol']} | {c['mode']} | {c['first_body_ms']:.3f} | {c['first_frame_ms']:.3f} | {c['three_frames_ms']:.3f} |\n"
s+='''
![TTS first-frame samples](tts-first-frame.png)

These are client byte-availability measurements. No speaker onset,microphone capture or physical acoustic closure is established.

## Execution and validation

Every subrun used the same pinned Docker image,network-none/NET_ADMIN,2CPU/2GiB,loopback netem40ms per traversal/20Mbit/s/0.1% random loss. Only one own benchmark container ran at a time. Previous short calibration is in ../controlled-network; configured rate is not identical to application goodput. Random drop positions,host scheduling and shared client/server event loop can affect results. Qlog and TCP sampling overhead is present in all conditions.

Workload analyzers verify exact source/result bytes and semantic format,the complete8-step Computer ordering or294-part TTS release plan,service waits/arrival conservation,TLS/ALPN/reuse,qlog headers/initial limits/MAX updates,TCP receive-buffer/TCP_INFO/NODELAY/proto readbacks,container resources and per-subrun cleanup. verify_all.py additionally requires final container absence and all324 valid exchanges. verification.json binds analyzer/runtime sources. Revalidate with python verify_all.py and regenerate figures/report with the matplotlib environment using python report.py.

This closes receive-limit coverage for the four workload types under the declared transport implementations. It does not replace remaining chunking/recovery cells or the final contribution review in ../COVERAGE-REVIEW.md. Fixed-trace delivery is not a new model-quality or live-browser benchmark.
'''
(R/'README.md').write_text(s)
files={str(p.relative_to(R)):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in R.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
(R/'manifest.json').write_text(json.dumps(dict(scope='Matched NODELAY1 four-workload receive-limit comparison; parent incomplete',files=files),indent=2)+'\n')
