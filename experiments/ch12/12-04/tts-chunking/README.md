# TTS chunk-policy comparison

Completed90 real HTTP transfers:72 formal requests plus18 protocol warmups, in nine subruns. Three outer trials shuffle the three chunk policies; every subrun repeats both protocols and reuse off/on. The recorded294-release control is newly executed in this batch, not transplanted from an earlier timing run. The other policies use20 releases (44-byte header then64KiB PCM groups) or one whole-response release.

All policies use the same actual WAV and source byte-availability trace. Coalescing waits until every byte in a group is available; whole-response buffering waits until the final source bytes at878.237ms. There is no new TTS generation. The effects combine release timing and actual application write sizes; they do not isolate kernel packet sizes or congestion behavior. HTTP/TLS/QUIC may packetize writes differently.

| Policy | Protocol | Reuse | First body ms | First20ms PCM ms | Three-frame readiness ms | Full response ms |
|---|---|---|---:|---:|---:|---:|
| recorded | h1 | False | 245.560 | 558.737 | 560.289 | 1279.741 |
| recorded | h1 | True | 163.322 | 477.683 | 478.468 | 1196.833 |
| recorded | h3 | False | 169.670 | 482.160 | 483.661 | 1259.215 |
| recorded | h3 | True | 124.866 | 437.408 | 439.036 | 1334.958 |
| coalesce64k | h1 | False | 246.685 | 575.540 | 575.540 | 1259.296 |
| coalesce64k | h1 | True | 164.889 | 497.356 | 497.356 | 1214.342 |
| coalesce64k | h3 | False | 170.574 | 483.164 | 484.654 | 1265.824 |
| coalesce64k | h3 | True | 126.221 | 439.055 | 440.699 | 1195.956 |
| whole | h1 | False | 1143.131 | 1143.133 | 1143.133 | 1810.084 |
| whole | h1 | True | 1064.016 | 1064.019 | 1064.019 | 1642.554 |
| whole | h3 | False | 1049.789 | 1050.091 | 1058.464 | 1813.540 |
| whole | h3 | True | 1004.352 | 1004.732 | 1009.578 | 3253.863 |

Each table cell is the median of six formal requests. Reuse-on includes the first fresh request and the second reused request of each pair; it is not a pure warm-connection statistic. First body may contain only a WAV header. A complete20ms frame requires1764 PCM bytes beyond that44-byte header. No acoustic playback or microphone recording is part of this experiment.

Docker network-none,2CPU/2GiB and the same image are used throughout. Each subrun resets only its loopback netem to40ms per traversal,20Mbit/s and0.1% random loss; settings, seeds, counters and empty final queue are archived. Previously measured RTT is approximately80.12ms. Random drops and scheduling may differ between subruns, so the descriptive medians do not establish statistical significance or universal protocol superiority.

Verification passed all90 waveform hashes, upload hashes, source-availability/no-early-release constraints, every client byte offset and playable-frame threshold, TLS/ALPN, qlogs and connection-reuse identities. All nine runner exit codes are zero; container absence is recorded in container-after.txt. [Protocol](PROTOCOL.md), results/order.json and results/executions.json bind the ordering and actual runs.

Revalidate with `python3 prepare.py` then `python3 analyze.py`. run_network.py selects its pinned fixture by BOOK_CHUNK_MODE and outer trial by BOOK_TRIAL; orchestrate.py executes the recorded plan in a fresh /results directory inside the controlled-network Docker image. The experiment does not modify host networking.

This completes the TTS chunking factor. TCP/QUIC window sizing, interrupted recovery and the remaining image/Computer Use workloads are still required for experiment12-4.
