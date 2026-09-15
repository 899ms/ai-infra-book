"""Cross-workload synthesis: comparisons remain within their original batches."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent;sources={}
def load(name):
 p=R/name;sources[name]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
for folder in ['receive-windows','transfer-chunks','workload-recovery']:assert load(folder+'/verification.json')['verified']
s='''# Experiment12-4: measured contributions across workloads

The tables compare changes within each declared experiment batch. Source image, transcript, audio and action bytes are fixed within their workload. Network transfers are real; model/CPU service and TTS availability are replays of separately measured source computation. These are descriptive results with small sample counts and independent random-loss realizations. Differences between medians are not paired fault costs, confidence intervals or a general protocol ranking. The rows cannot be added to predict a combined optimized system: no full-factor interaction experiment was performed.

## Connection reuse

Configured80ms RTT/20Mbit/s/0.1% loss. Image/ASR/TTS have six formal requests per cell; Computer Use has three eight-round traces. Reused image/ASR/TTS groups include both fresh and warm requests. The table uses each runner's complete-result boundary; Computer timing covers the complete trace.

| Workload | Protocol | No reuse seconds | Reuse seconds | Reuse minus no-reuse seconds |
|---|---|---:|---:|---:|
'''
for w,path in [('image','image-records/loss0.1-summary.json'),('asr','speech-records/loss0.1-summary.json'),('tts','tts-network/loss0.1-playable.json'),('computer','computer-use/network-summary.json')]:
 d=load(path);cs=d.get('conditions',d.get('groups'))
 for proto in ['h1','h3']:
  vals=[]
  for reuse in [False,True]:
   c=next(c for c in cs if c['protocol']==proto and c['reuse']==reuse);vals.append(c['median_trace_s'] if w=='computer' else c['complete_ms' if w=='tts' else 'median_attempt_ms']/1000)
  s+=f'| {w} | {proto} | {vals[0]:.3f} | {vals[1]:.3f} | {vals[1]-vals[0]:+.3f} |\n'
s+='''
Reuse reduced complete-trace latency for both Computer Use paths and the complete-result median for the TCP image/ASR/TTS paths in these batches. The HTTP3 image and ASR reuse medians were higher; those observations remain visible and are not interpreted as proof that reuse intrinsically harms QUIC. Request sizes, losses, implementation scheduling and slow samples affect these measurements.

## Receive limits with matched socket settings

All324 exchanges verified. Default/64KiB/4MiB configurations use explicit TCP_NODELAY1/proto6 and position-balanced mode orders. TCP SO_RCVBUF and QUIC initial stream/connection credit are different controls; QUIC credit can grow. Older manual-proto0 window batches are excluded. Complete-result medians follow the matched runner boundaries.

| Workload | Protocol | Default seconds | 64KiB seconds | 4MiB seconds |
|---|---|---:|---:|---:|
'''
for w in ['image','asr','tts','computer']:
 cs=load(f'receive-windows/{w}-summary.json')['conditions']
 for proto in ['h1','h3']:
  vals=[next(c['median_trace_s' if w=='computer' else 'median_s'] for c in cs if c['protocol']==proto and c['mode']==m) for m in ['default','64k','4m']]
  s+=f'| {w} | {proto} | '+' | '.join(f'{x:.3f}' for x in vals)+' |\n'
s+='''
A small fixed TCP receive buffer can increase full-result time, especially for the large image. The default and large-buffer cases must still be compared using their retained samples. QUIC initial credit is not a TCP congestion or advertised receive window, so equal numeric labels do not imply identical constraints.

## Application write size

All270 exchanges verified, with default receive configuration and NODELAY1. Sizes apply to writes in both request and response directions after the full body is available. Every piece has a source-slice hash and timing ledger; that instrumentation is included in elapsed time. Write size is not wire packet or TLS record size.

| Workload | Protocol | Whole seconds |16KiB seconds |64KiB seconds |
|---|---|---:|---:|---:|
'''
for w in ['image','asr','computer']:
 cs=load(f'transfer-chunks/{w}-summary.json')['conditions']
 for proto in ['h1','h3']:
  vals=[next(c['median_trace_s' if w=='computer' else 'median_s'] for c in cs if c['protocol']==proto and c['mode']==m) for m in ['whole','16k','64k']]
  s+=f'| {w} | {proto} | '+' | '.join(f'{x:.3f}' for x in vals)+' |\n'
s+='''
TCP medians changed little across these application write sizes. HTTP3 samples show workload-dependent differences and slow tails; smaller writes did not establish a universal improvement. The tiny transcript/action responses remain one write, while their uploads and the large image exercise the selected policy.

## TTS source availability and first usable PCM

This is a separate90-exchange release-policy matrix: original294 source-read availability segments,64KiB coalescing,or a whole response released only when all source bytes are ready. The table uses reused-connection groups, six formal requests per cell. First body may contain only a WAV header; the reported threshold is the first complete20ms PCM frame.

| Protocol | Policy | First20ms PCM milliseconds | Complete WAV milliseconds |
|---|---|---:|---:|
'''
for c in load('tts-chunking/summary.json')['groups']:
 if c['reuse']:s+=f"| {c['protocol']} | {c['mode']} | {c['first_frame_ms']:.3f} | {c['complete_ms']:.3f} |\n"
s+='''
Whole-response buffering delays usable PCM because it withholds already available audio. Header arrival is therefore an unsuitable first-play proxy. These are byte availability measurements; physical speaker onset and microphone capture remain unmeasured.

## Interrupted application recovery

All image20 tasks/32 exchanges and ASR/TTS/Computer60 tasks/222 exchanges verified. Three formal tasks per protocol/policy. Every exchange opens a new connection and task time includes connection close, response persistence and validation, unlike request-only timing above. Image faults occur after at least1MiB of JPEG; TTS after at least20ms PCM; ASR and Computer round3 fault after headers during production. Different fault locations prevent cross-workload causal ranking.

| Workload | Protocol | Uninterrupted seconds | Restart seconds | Resume seconds |
|---|---|---:|---:|---:|
'''
for w in ['image','asr','tts','computer']:
 cs=load('interrupted-recovery/summary.json' if w=='image' else f'workload-recovery/{w}-summary.json')['conditions']
 for proto in ['h1','h3']:
  vals=[next(c['median_s'] for c in cs if c['protocol']==proto and c['policy']==m) for m in ['uninterrupted','restart','resume']]
  s+=f'| {w} | {proto} | '+' | '.join(f'{x:.3f}' for x in vals)+' |\n'
s+='''
Restart reuploads the input and repeats source work. Resume depends on an explicit application operation identifier, surviving server state and retained client bytes; it avoids that duplicated source job. The byte/job accounting and all timing samples are in the component reports. A lower recovery median than an uninterrupted median in an independent random-loss batch is not a negative failure penalty. These protocols do not recover server/GPU process loss. Computer Use only tests failure before action delivery, not safe retries of effects whose acknowledgments were lost. Exact PCM reconstruction does not establish glitch-free playback.

## Evidence and remaining scope

Each table is generated from the named verified component summaries, bound by SHA256 in contribution-sources.json. Component reports retain per-sample plots, raw exchanges, source identities, transport negotiation, failures, calibration and cleanup evidence. The figures in receive-windows, transfer-chunks and workload-recovery should be read with the medians to see dispersion.

The default clients here are the archived h11/aioquic implementations; the findings do not cover all browser defaults. All controlled comparisons use one isolated CPU-limited Docker benchmark at a time, and qlog/sampling/shared event-loop overhead is part of the setup. Source RAW processing, Whisper recognition, Fish synthesis and screenshot-driven Qwen task have separate live-computation records and quality limitations. This synthesis closes the contribution-analysis deliverable for the measured network factors. The permitted first-play calculation is completed in playback-records/README.md: measured arrivals feed an explicit three-frame playback policy, with sample preservation and independently checked stalls. Actual acoustic onset remains unmeasured. The complete requirement audit is in COVERAGE-REVIEW.md.
'''
(R/'CONTRIBUTIONS.md').write_text(s)
(R/'contribution-sources.json').write_text(json.dumps(dict(scope='Within-batch descriptive comparisons; no combined-factor prediction',source_sha256=sources),indent=2)+'\n')
