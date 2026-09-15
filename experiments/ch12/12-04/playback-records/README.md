# Playback calculated from measured TTS arrivals

All196 complete TTS network traces (156 formal,40 warmups) were replayed through an explicit playback calculation. The input is the measured arrival ledger for the exact mono44100Hz PCM16 WAV, covering reuse (both loss profiles), release/coalescing and matched receive-window matrices. No new network/model execution or speaker/microphone measurement is claimed.

Policy: collect three complete20ms frames, start immediately, consume frames in order at44100Hz, and wait when the next full frame is unavailable. Waiting preserves samples and adds stall time; no samples are dropped or silently replaced. The final100-byte partial frame keeps its exact duration. Header bytes are excluded. Device startup latency, scheduling jitter and acoustic latency are absent from this declared calculation.

| Matrix | Mode | Protocol | Reuse | Formal n | First play ms | Median stall ms | Max stall ms | Finish seconds |
|---|---|---|---|---:|---:|---:|---:|---:|
| release | coalesce64k | h1 | False | 6 | 575.540 | 0.000 | 0.000 | 13.997 |
| release | coalesce64k | h1 | True | 6 | 497.356 | 0.000 | 0.000 | 13.918 |
| release | coalesce64k | h3 | False | 6 | 484.654 | 0.000 | 29.453 | 13.906 |
| release | coalesce64k | h3 | True | 6 | 440.699 | 0.000 | 0.000 | 13.862 |
| release | recorded | h1 | False | 6 | 560.289 | 0.000 | 0.000 | 13.981 |
| release | recorded | h1 | True | 6 | 478.468 | 0.000 | 0.000 | 13.900 |
| release | recorded | h3 | False | 6 | 483.661 | 0.000 | 0.000 | 13.905 |
| release | recorded | h3 | True | 6 | 439.036 | 0.000 | 0.000 | 13.860 |
| release | whole | h1 | False | 6 | 1143.133 | 0.000 | 0.000 | 14.564 |
| release | whole | h1 | True | 6 | 1064.019 | 0.000 | 0.000 | 14.485 |
| release | whole | h3 | False | 6 | 1058.464 | 0.000 | 0.000 | 14.480 |
| release | whole | h3 | True | 6 | 1009.578 | 0.000 | 0.000 | 14.431 |
| reuse | loss0 | h1 | False | 6 | 561.206 | 0.000 | 0.000 | 13.982 |
| reuse | loss0 | h1 | True | 6 | 478.297 | 0.000 | 0.000 | 13.899 |
| reuse | loss0 | h3 | False | 6 | 483.273 | 0.000 | 0.000 | 13.904 |
| reuse | loss0 | h3 | True | 6 | 439.961 | 0.000 | 0.000 | 13.861 |
| reuse | loss0.1 | h1 | False | 6 | 560.793 | 0.000 | 0.000 | 13.982 |
| reuse | loss0.1 | h1 | True | 6 | 478.912 | 0.000 | 0.000 | 13.900 |
| reuse | loss0.1 | h3 | False | 6 | 483.771 | 0.000 | 0.000 | 13.905 |
| reuse | loss0.1 | h3 | True | 6 | 440.345 | 0.000 | 0.000 | 13.861 |
| window | 4m | h1 | True | 6 | 478.725 | 0.000 | 0.000 | 13.900 |
| window | 4m | h3 | True | 6 | 439.965 | 0.000 | 0.000 | 13.861 |
| window | 64k | h1 | True | 6 | 478.470 | 0.000 | 0.000 | 13.900 |
| window | 64k | h3 | True | 6 | 439.986 | 0.000 | 0.000 | 13.861 |
| window | default | h1 | True | 6 | 478.608 | 0.000 | 0.000 | 13.900 |
| window | default | h3 | True | 6 | 440.365 | 0.000 | 0.000 | 13.861 |

Every trace retains all672 frame availability/start times and every stall interval. A sequential event calculation is checked against an independent max-plus expression; finish minus start equals exact audio duration plus stalls. No frame starts before its last source byte arrives. Full source/result SHA, arrival conservation and temporal order are checked before playback calculation.

These results satisfy the playback-analysis form allowed by the original calculation/network-record condition. They do not turn calculated first play into measured audible onset or prove that a particular real player has this buffering policy. The adjacent12-7 actual muted device measurements demonstrate why hardware feed starvation and driver flags need separate observation. Recovery playback is outside this uninterrupted-trace table: a full restart can repeat audio already played, even when the final stored WAV is byte-exact.

Run `python run.py` to regenerate this table and results from the bound source ledgers. Original transport verifiers and reports remain the authority for those experiments' protocol checks.

During report development, grouping initially included warmup-only receive-window/reuse=false cells, which have no formal samples. Group keys now come only from formal records; all warmups remain in the196-record output. No source traces or playback policy changed.
