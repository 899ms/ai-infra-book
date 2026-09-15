import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent
d=json.loads((R/'summary.json').read_text())
s='''# TTS chunk-policy comparison

Completed90 real HTTP transfers:72 formal requests plus18 protocol warmups, in nine subruns. Three outer trials shuffle the three chunk policies; every subrun repeats both protocols and reuse off/on. The recorded294-release control is newly executed in this batch, not transplanted from an earlier timing run. The other policies use20 releases (44-byte header then64KiB PCM groups) or one whole-response release.

All policies use the same actual WAV and source byte-availability trace. Coalescing waits until every byte in a group is available; whole-response buffering waits until the final source bytes at878.237ms. There is no new TTS generation. The effects combine release timing and actual application write sizes; they do not isolate kernel packet sizes or congestion behavior. HTTP/TLS/QUIC may packetize writes differently.

| Policy | Protocol | Reuse | First body ms | First20ms PCM ms | Three-frame readiness ms | Full response ms |
|---|---|---|---:|---:|---:|---:|
'''
for r in d['groups']:
    s+=f"| {r['mode']} | {r['protocol']} | {r['reuse']} | {r['first_body_ms']:.3f} | {r['first_frame_ms']:.3f} | {r['three_frames_ms']:.3f} | {r['complete_ms']:.3f} |\n"
s+='''
Each table cell is the median of six formal requests. Reuse-on includes the first fresh request and the second reused request of each pair; it is not a pure warm-connection statistic. First body may contain only a WAV header. A complete20ms frame requires1764 PCM bytes beyond that44-byte header. No acoustic playback or microphone recording is part of this experiment.

Docker network-none,2CPU/2GiB and the same image are used throughout. Each subrun resets only its loopback netem to40ms per traversal,20Mbit/s and0.1% random loss; settings, seeds, counters and empty final queue are archived. Previously measured RTT is approximately80.12ms. Random drops and scheduling may differ between subruns, so the descriptive medians do not establish statistical significance or universal protocol superiority.

Verification passed all90 waveform hashes, upload hashes, source-availability/no-early-release constraints, every client byte offset and playable-frame threshold, TLS/ALPN, qlogs and connection-reuse identities. All nine runner exit codes are zero; container absence is recorded in container-after.txt. [Protocol](PROTOCOL.md), results/order.json and results/executions.json bind the ordering and actual runs.

Revalidate with `python3 prepare.py` then `python3 analyze.py`. run_network.py selects its pinned fixture by BOOK_CHUNK_MODE and outer trial by BOOK_TRIAL; orchestrate.py executes the recorded plan in a fresh /results directory inside the controlled-network Docker image. The experiment does not modify host networking.

This completes the TTS chunking factor. TCP/QUIC window sizing, interrupted recovery and the remaining image/Computer Use workloads are still required for experiment12-4.
'''
(R/'README.md').write_text(s)
files={str(p.relative_to(R)):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in R.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
(R/'manifest.json').write_text(json.dumps(dict(scope='Real TTS chunk-policy transport with source availability replay; parent incomplete',files=files),indent=2)+'\n')
