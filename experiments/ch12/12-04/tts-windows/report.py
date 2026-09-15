import hashlib,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;S=json.loads((R/'summary.json').read_text())
fig,axes=plt.subplots(2,2,figsize=(10,7),sharex=True)
for row,(key,ylabel) in enumerate([('first_frame_samples_ms','First 20ms PCM frame available (ms)'),('samples_s','Complete WAV validated (seconds)')]):
 top=max(max(c[key]) for c in S['conditions'])*1.1
 for col,proto in enumerate(['h1','h3']):
  ax=axes[row,col]
  for i,mode in enumerate(['default','64k','4m']):
   c=next(c for c in S['conditions'] if c['protocol']==proto and c['mode']==mode);values=c[key]
   import statistics
   ax.scatter([i-.12,i-.04,i+.04,i+.12,i-.08,i+.08],values,s=28,color='#167d9a');ax.plot([i-.25,i+.25],[statistics.median(values)]*2,color='#bc5739',linewidth=2)
  ax.set_xticks(range(3),['Default','64 KiB','4 MiB']);ax.set_ylim(0,top);ax.grid(axis='y',alpha=.2)
  if col==0:ax.set_ylabel(ylabel)
  if row==0:ax.set_title('HTTP/1.1 + TLS 1.3' if proto=='h1' else 'HTTP/3')
fig.suptitle('TTS receive configuration: first playable frame and complete audio')
fig.text(.5,.015,'Six formal transfers per cell; recorded source release timing. PCM availability is not acoustic playback.',ha='center',fontsize=9)
fig.tight_layout(rect=[0,.04,1,.96])
for ext in ['png','svg','pdf']:fig.savefig(R/f'tts-window-results.{ext}',dpi=160)
plt.close(fig)
s='''# TTS receive configuration and playable PCM availability

All54 actual network exchanges passed independent verification (36 formal,18 warmups). They use the unchanged Fish WAV/PCM and294-part source client-read availability trace from [TTS network records](../tts-network/README.md). Source timing is replayed after complete request receipt. No new synthesis, native GPU chunk timestamps or acoustic onset is claimed.

![All formal first-frame and complete-audio times](tts-window-results.png)

| Mode | Protocol | First response body ms | First complete20ms PCM ms | Three PCM frames ms | Complete WAV seconds |
|---|---|---:|---:|---:|---:|
'''
for c in S['conditions']:s+=f"| {c['mode']} | {c['protocol']} | {c['first_body_ms']:.3f} | {c['first_frame_ms']:.3f} | {c['three_frames_ms']:.3f} | {c['median_s']:.3f} |\n"
s+='''
Every cell has six formal observations, spanning three repetitions and one fresh plus one reused request per pair. The medians therefore mix connection setup and warm reuse. All samples, including slow tails, are retained. Three trials do not establish statistical significance or a universal best receive setting. First response body can contain only the WAV header; the complete20ms PCM threshold is1808 bytes (44-byte header+1764 PCM bytes), and three frames require5336 bytes. Those are client byte-availability thresholds, not an audio-device or speaker measurement.

## Fixed intervention and verification

Each of nine fresh Docker containers uses network-none/NET_ADMIN,2CPU/2GiB,loopback netem40ms per traversal,20Mbit/s,0.1% random loss. Mode order is position-balanced across trials:default/64k/4m,64k/4m/default,4m/default/64k. No two benchmark containers overlap. The same source audio and release plan are used in all conditions.

TCP sets only SO_RCVBUF before connect and on the listener before accept. Explicit64KiB/4MiB settings read back as131072/8388608 bytes on Linux. Defaults permit receive-buffer growth. Readbacks are buffer bounds, not wire-window sizes; raw server TCP_INFO samples and client ready/close values remain in results and summary.json. QUIC sets initial connection and stream receive credit on both endpoints; qlogs verify local/remote parameters and MAX updates. These credits can grow dynamically, so a64KiB initial limit is not a permanent ceiling. TCP buffers and QUIC credits are distinct mechanisms, and no congestion algorithm is changed.

The verifier checks every complete WAV hash,mono44100Hz PCM16 format/591872 frames,complete PCM SHA,all294 per-response release offsets/lengths/no-early timestamps,arrival byte conservation and first-frame/three-frame timestamps. It also checks source identity,TLS/ALPN,reuse,QUIC response headers and flow-control parameters,TCP buffers/counters,container resources,netem queues and all nine container removals. The checksum evidence binds the recorded releases to the original audio; it does not prove physical playback.

Revalidate with python analyze.py and regenerate the figure/report with the matplotlib environment using python report.py. orchestrate.py and PROTOCOL.md preserve the execution design. The parent experiment remains open for other workload/factor cells and final contribution analysis listed in ../COVERAGE-REVIEW.md.
'''
(R/'README.md').write_text('> Socket-default qualification: see [TCP_NODELAY diagnostic](SOCKET-DEFAULTS.md). A full matched rerun is complete in ../receive-windows; do not pool this batch with earlier implicit-socket TCP timings.\n\n'+s)
files={str(p.relative_to(R)):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in R.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
(R/'manifest.json').write_text(json.dumps(dict(scope='TTS receive-configuration and client PCM availability; no acoustics',files=files),indent=2)+'\n')
