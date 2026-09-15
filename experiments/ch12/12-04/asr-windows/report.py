import hashlib,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;S=json.loads((R/'summary.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(10,4.4),sharey=True)
for ax,proto,title in zip(axes,['h1','h3'],['HTTP/1.1 + TLS 1.3','HTTP/3']):
 for i,mode in enumerate(['default','64k','4m']):
  c=next(c for c in S['conditions'] if c['protocol']==proto and c['mode']==mode)
  ax.scatter([i-.12,i-.04,i+.04,i+.12,i-.08,i+.08],c['samples_s'],color='#167d9a',s=32,zorder=3)
  ax.plot([i-.25,i+.25],[c['median_s']]*2,color='#bc5739',linewidth=2.5)
 ax.set_xticks(range(3),['Default','64 KiB','4 MiB']);ax.set_title(title);ax.set_xlabel('Receive configuration');ax.grid(axis='y',alpha=.2);ax.set_ylim(0,max(max(c['samples_s']) for c in S['conditions'])*1.1)
axes[0].set_ylabel('Complete transcript validation (seconds)')
fig.suptitle('ASR result delivery: receive configuration comparison')
fig.text(.5,.015,'Six formal transfers per cell; dots = samples, line = median. Includes 0.623 s recorded GPU service.',ha='center',fontsize=9)
fig.tight_layout(rect=[0,.04,1,.94])
for ext in ['png','svg','pdf']:fig.savefig(R/f'asr-window-results.{ext}',dpi=160)
plt.close(fig)
s='''# ASR receive configuration and complete transcript delivery

This experiment uses the exact actual1,183,788-byte WAV and Whisper transcript from [ASR source records](../speech-records/README.md). Each real request uploads the complete WAV, waits the measured0.622926892s GPU-service replay and returns/validates the complete original UTF8 transcript. These are not54 new model calls, and transport configuration does not imply improved recognition quality.

Three trials use position-balanced mode order: default/64KiB/4MiB,64KiB/4MiB/default,4MiB/default/64KiB. Each setting occupies each position once. Nine fresh Docker containers use netem80ms RTT,20Mbit/s,0.1% random loss,2CPUs/2GiB. Each protocol/configuration has one fresh and one reused formal request per repetition, plus a separately connected warmup. All54 exchanges (36 formal,18 warmups) passed upload/transcript identity,UTF8 validation,TLS/ALPN,reuse,service waits,qlogs and netem/resource/cleanup checks.

![All formal ASR result times](asr-window-results.png)

| Receive setting | Protocol | Median complete seconds | Fresh median | Reused median |
|---|---|---:|---:|---:|
'''
for c in S['conditions']:s+=f"| {c['mode']} | {c['protocol']} | {c['median_s']:.3f} | {c['fresh_median_s']:.3f} | {c['reused_median_s']:.3f} |\n"
s+='''
Dots retain all six formal values per cell; median splits contain only three values each. The mode order is position-balanced, but random packet-drop positions and temporal/host variation remain; three repetitions do not establish statistical significance. These small, stochastic batches describe this implementation and controlled loopback path. They do not establish statistical significance or a general best protocol/window. The pair-wide median mixes fresh and reused requests.

## What actually changed

TCP changes only SO_RCVBUF before connect and on the listener before accept. Defaults leave Linux receive autotuning available; explicit settings lock that buffer choice. Linux reports double the requested buffer size:131072 bytes for64KiB and8388608 bytes for4MiB. This readback is not the advertised TCP window. The default observed buffer can grow. Actual TCP_INFO records are retained at client ready/close and sampled on server sockets every100ms. Offsets were compiled from the RTX host linux/tcp.h with tcp_offsets.c; source header, kernel identity and raw bytes are archived. tcpi_snd_wnd reports the peer advertised receive window, tcpi_snd_cwnd is segments, and the limit timers are microseconds.

QUIC changes both initial connection max_data and stream max_stream_data on both endpoints. Default aioquic1.3.0 values are1MiB each. Qlogs verify local/remote advertised initial limits and subsequent MAX_DATA/MAX_STREAM_DATA updates; limits grow dynamically, so64KiB is not a permanent ceiling. TCP buffer sizing and QUIC credit sizing are distinct mechanisms. This experiment does not change the congestion algorithm or equate the two settings.

| Trial/config | Observed server TCP buffer bytes | Sampled peer window min–max bytes | QUIC initial limit bytes | Observed MAX_DATA min–max |
|---|---|---|---:|---|
'''
for e in S['evidence']:
 s+=f"| {e['name']} | {[min(e['tcp_buffers']),max(e['tcp_buffers'])]} | {e['server_peer_window_range']} | {e['quic_initial']} | {e['quic_limit_ranges'].get('max_data')} |\n"
s+='''
| Trial/config | Client receive-window-limited time µs | Client busy time µs | Ratio |
|---|---:|---:|---:|
'''
for e in S['evidence']:
 ratio=e['tcp_client_rwnd_limited_us']/e['tcp_client_busy_us'] if e['tcp_client_busy_us'] else 0
 s+=f"| {e['name']} | {e['tcp_client_rwnd_limited_us']} | {e['tcp_client_busy_us']} | {100*ratio:.1f}% |\n"
s+='''
These cumulative client counter deltas include the TCP warmup connection and the two-request formal connection. The ratio describes time marked receive-window-limited by the kernel among its busy time; it is not a fraction of total end-to-end task time, nor a separate throughput measurement.

The sampled peer-window range includes handshake/idle and active phases; do not read its minimum as a sustained transfer limit. Per-connection TCP counters and QUIC frame counts in summary.json provide further diagnostics. Fixed source identity, readbacks and negotiated parameters verify the intervention; they alone do not prove the cause of every latency difference.

The client/server share one container event loop; qlog and100ms TCP sampling overhead is present in every batch. Random drop placement, congestion recovery, CPU scheduling and receive behavior can differ. The ASR request has a moderate audio upload and a very small complete text response. These results cannot stand in for TTS first-play or Computer Use screenshot-round behavior. Previous profile calibration is in ../controlled-network. No host route/sysctl changes were made. All nine own containers were removed.

Reproduce with orchestrate.py on the RTX, preserving the sibling speech-records fixture. Revalidate with python analyze.py; generate the figure/report with the local matplotlib environment and python report.py. Fresh result directories are required. PROTOCOL.md records the design before execution. Window configuration is now measured for ASR as well as the separate image workload. TTS/Computer Use receive configurations and other unmeasured workload/factor cells remain open in12-4/COVERAGE-REVIEW.md.
'''
(R/'README.md').write_text('> Socket-default qualification: see [TCP_NODELAY diagnostic](SOCKET-DEFAULTS.md). A full matched rerun is complete in ../receive-windows; do not pool this batch with earlier implicit-socket TCP timings.\n\n'+s)
files={str(p.relative_to(R)):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in R.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
(R/'manifest.json').write_text(json.dumps(dict(scope='Actual ASR network receive-configuration comparison; parent incomplete',files=files),indent=2)+'\n')
