# Actual TTS audio availability through controlled HTTP paths

Completed52 network requests using the actual Fish Speech audio from12-7:26 per netem profile, including4 total warmups. All returned WAV bytes match the corrected source WAV; its PCM is unchanged. The server replays294 recorded source-client availability segments, and actual HTTP1.1/TLS1.3 or HTTP3 carries the released bytes through Docker netem.

This is a network-record replay, not52 new GPU syntheses. The source read trace includes its original loopback/server/read overhead; it is not native model chunk timing. Its clock is restarted after the new upload completes, explicitly adding an availability trace after the transport's request arrival. One request is active at a time.

The source WAV header was readable at0.755ms; the first4096 PCM bytes at312.007ms; the final bytes at878.237ms. HTTP headers or the44-byte WAV header do not establish that audio is playable. The client records below separately measure first body, one complete20ms frame (1764 PCM bytes after the WAV header), three-frame readiness and complete validated response. These are client-availability times, not physical speaker onset.

| Loss profile | Protocol | Reuse | First body ms | First PCM frame ms | Three frames ms | Full response ms |
|---|---|---|---:|---:|---:|---:|
| loss0 | h1 | False | 246.667 | 559.639 | 561.206 | 1266.217 |
| loss0 | h1 | True | 163.365 | 476.727 | 478.297 | 1196.475 |
| loss0 | h3 | False | 169.293 | 481.783 | 483.273 | 1247.305 |
| loss0 | h3 | True | 126.354 | 438.322 | 439.961 | 1204.878 |
| loss0.1 | h1 | False | 245.803 | 559.255 | 560.793 | 1266.379 |
| loss0.1 | h1 | True | 163.873 | 477.325 | 478.912 | 1196.951 |
| loss0.1 | h3 | False | 169.944 | 482.027 | 483.771 | 1272.701 |
| loss0.1 | h3 | True | 127.360 | 438.728 | 440.345 | 1199.480 |

Each table cell is the median of six formal requests in three shuffled repetitions. Reuse is the changed factor in this stage; chunk sizes and release availability are fixed. The two profiles configure80ms RTT,20Mbit/s and0/0.1% random loss. Earlier calibration measured approximately80.12ms RTT and17.4–17.7Mbit/s short TCP goodput; these are not physical WAN samples or equal guaranteed application throughput.

Reuse-enabled pairs include the first request that opens the connection and the second that reuses it. Their median is therefore a pair-level workload statistic, not a pure warm-connection latency. Per-request fresh flags and connection identities remain available for that distinction.

Verification checks source/upload/response hashes, TLS/ALPN, connection reuse, qlogs, client byte-offset conservation, full20ms/three-frame thresholds, and every source release's offset/length/no-earlier-than-ready time. The qdisc settings and empty final queue are checked before/after. Client first-body times are retained even when they appear much faster than first-frame times. Timing instrumentation, scheduling and stochastic packet loss remain part of these observations.

The original GPU synthesis records remain in12-7/tts-stream. There is no new microphone recording, speaker playback or enrolled voice. The prior actual device-callback and model-cancellation measurements are separate evidence, not injected into this timing table. The Docker transport process exited and the container was removed, as recorded in container-after.txt.

Revalidate with `python3 prepare.py`, `python3 analyze_network.py loss0`, and `python3 analyze_network.py loss0.1`. run_network.py requires the pinned controlled-network Docker image/dependencies, the fixture files and a fresh output directory. [Protocol](PROTOCOL.md) records the planned scope.

This completes fixed-TTS byte delivery and first-playable availability measurement for12-4's record-replay path. Actual acoustic playback remains unmeasured. Image refinement, Computer Use and individual window/chunk/recovery comparisons remain outstanding for the parent experiment.
