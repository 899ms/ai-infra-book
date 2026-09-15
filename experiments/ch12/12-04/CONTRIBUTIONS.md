# Experiment12-4: measured contributions across workloads

The tables compare changes within each declared experiment batch. Source image, transcript, audio and action bytes are fixed within their workload. Network transfers are real; model/CPU service and TTS availability are replays of separately measured source computation. These are descriptive results with small sample counts and independent random-loss realizations. Differences between medians are not paired fault costs, confidence intervals or a general protocol ranking. The rows cannot be added to predict a combined optimized system: no full-factor interaction experiment was performed.

## Connection reuse

Configured80ms RTT/20Mbit/s/0.1% loss. Image/ASR/TTS have six formal requests per cell; Computer Use has three eight-round traces. Reused image/ASR/TTS groups include both fresh and warm requests. The table uses each runner's complete-result boundary; Computer timing covers the complete trace.

| Workload | Protocol | No reuse seconds | Reuse seconds | Reuse minus no-reuse seconds |
|---|---|---:|---:|---:|
| image | h1 | 7.549 | 7.300 | -0.248 |
| image | h3 | 17.415 | 22.037 | +4.623 |
| asr | h1 | 1.553 | 1.387 | -0.166 |
| asr | h3 | 1.671 | 1.799 | +0.128 |
| tts | h1 | 1.266 | 1.197 | -0.069 |
| tts | h3 | 1.273 | 1.199 | -0.073 |
| computer | h1 | 6.353 | 4.417 | -1.936 |
| computer | h3 | 6.686 | 4.523 | -2.162 |

Reuse reduced complete-trace latency for both Computer Use paths and the complete-result median for the TCP image/ASR/TTS paths in these batches. The HTTP3 image and ASR reuse medians were higher; those observations remain visible and are not interpreted as proof that reuse intrinsically harms QUIC. Request sizes, losses, implementation scheduling and slow samples affect these measurements.

## Receive limits with matched socket settings

All324 exchanges verified. Default/64KiB/4MiB configurations use explicit TCP_NODELAY1/proto6 and position-balanced mode orders. TCP SO_RCVBUF and QUIC initial stream/connection credit are different controls; QUIC credit can grow. Older manual-proto0 window batches are excluded. Complete-result medians follow the matched runner boundaries.

| Workload | Protocol | Default seconds | 64KiB seconds | 4MiB seconds |
|---|---|---:|---:|---:|
| image | h1 | 7.364 | 17.311 | 7.154 |
| image | h3 | 24.347 | 23.185 | 24.279 |
| asr | h1 | 1.439 | 2.326 | 1.303 |
| asr | h3 | 1.557 | 1.570 | 1.558 |
| tts | h1 | 1.197 | 1.692 | 1.191 |
| tts | h3 | 1.517 | 1.743 | 1.212 |
| computer | h1 | 4.417 | 4.617 | 4.356 |
| computer | h3 | 4.519 | 4.990 | 4.566 |

A small fixed TCP receive buffer can increase full-result time, especially for the large image. The default and large-buffer cases must still be compared using their retained samples. QUIC initial credit is not a TCP congestion or advertised receive window, so equal numeric labels do not imply identical constraints.

## Application write size

All270 exchanges verified, with default receive configuration and NODELAY1. Sizes apply to writes in both request and response directions after the full body is available. Every piece has a source-slice hash and timing ledger; that instrumentation is included in elapsed time. Write size is not wire packet or TLS record size.

| Workload | Protocol | Whole seconds |16KiB seconds |64KiB seconds |
|---|---|---:|---:|---:|
| image | h1 | 7.406 | 7.269 | 7.365 |
| image | h3 | 21.531 | 23.509 | 25.133 |
| asr | h1 | 1.389 | 1.389 | 1.390 |
| asr | h3 | 1.410 | 1.637 | 2.518 |
| computer | h1 | 4.423 | 4.422 | 4.423 |
| computer | h3 | 4.533 | 4.790 | 4.608 |

TCP medians changed little across these application write sizes. HTTP3 samples show workload-dependent differences and slow tails; smaller writes did not establish a universal improvement. The tiny transcript/action responses remain one write, while their uploads and the large image exercise the selected policy.

## TTS source availability and first usable PCM

This is a separate90-exchange release-policy matrix: original294 source-read availability segments,64KiB coalescing,or a whole response released only when all source bytes are ready. The table uses reused-connection groups, six formal requests per cell. First body may contain only a WAV header; the reported threshold is the first complete20ms PCM frame.

| Protocol | Policy | First20ms PCM milliseconds | Complete WAV milliseconds |
|---|---|---:|---:|
| h1 | recorded | 477.683 | 1196.833 |
| h3 | recorded | 437.408 | 1334.958 |
| h1 | coalesce64k | 497.356 | 1214.342 |
| h3 | coalesce64k | 439.055 | 1195.956 |
| h1 | whole | 1064.019 | 1642.554 |
| h3 | whole | 1004.732 | 3253.863 |

Whole-response buffering delays usable PCM because it withholds already available audio. Header arrival is therefore an unsuitable first-play proxy. These are byte availability measurements; physical speaker onset and microphone capture remain unmeasured.

## Interrupted application recovery

All image20 tasks/32 exchanges and ASR/TTS/Computer60 tasks/222 exchanges verified. Three formal tasks per protocol/policy. Every exchange opens a new connection and task time includes connection close, response persistence and validation, unlike request-only timing above. Image faults occur after at least1MiB of JPEG; TTS after at least20ms PCM; ASR and Computer round3 fault after headers during production. Different fault locations prevent cross-workload causal ranking.

| Workload | Protocol | Uninterrupted seconds | Restart seconds | Resume seconds |
|---|---|---:|---:|---:|
| image | h1 | 7.670 | 14.129 | 8.407 |
| image | h3 | 23.504 | 36.711 | 18.452 |
| asr | h1 | 1.556 | 2.490 | 1.556 |
| asr | h3 | 2.495 | 4.389 | 2.719 |
| tts | h1 | 1.270 | 1.844 | 1.527 |
| tts | h3 | 1.951 | 3.074 | 2.970 |
| computer | h1 | 6.026 | 6.389 | 6.029 |
| computer | h3 | 9.460 | 10.429 | 10.020 |

Restart reuploads the input and repeats source work. Resume depends on an explicit application operation identifier, surviving server state and retained client bytes; it avoids that duplicated source job. The byte/job accounting and all timing samples are in the component reports. A lower recovery median than an uninterrupted median in an independent random-loss batch is not a negative failure penalty. These protocols do not recover server/GPU process loss. Computer Use only tests failure before action delivery, not safe retries of effects whose acknowledgments were lost. Exact PCM reconstruction does not establish glitch-free playback.

## Evidence and remaining scope

Each table is generated from the named verified component summaries, bound by SHA256 in contribution-sources.json. Component reports retain per-sample plots, raw exchanges, source identities, transport negotiation, failures, calibration and cleanup evidence. The figures in receive-windows, transfer-chunks and workload-recovery should be read with the medians to see dispersion.

The default clients here are the archived h11/aioquic implementations; the findings do not cover all browser defaults. All controlled comparisons use one isolated CPU-limited Docker benchmark at a time, and qlog/sampling/shared event-loop overhead is part of the setup. Source RAW processing, Whisper recognition, Fish synthesis and screenshot-driven Qwen task have separate live-computation records and quality limitations. This synthesis closes the contribution-analysis deliverable for the measured network factors. The permitted first-play calculation is completed in playback-records/README.md: measured arrivals feed an explicit three-frame playback policy, with sample preservation and independently checked stalls. Actual acoustic onset remains unmeasured. The complete requirement audit is in COVERAGE-REVIEW.md.
