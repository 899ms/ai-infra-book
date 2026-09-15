# Actual ASR records and controlled-network replay

The fixed Fish Speech audio from12-7 was recognized by the cached faster-whisper-base.en checkpoint on the RTX GPU. One warmup and three formal FP16 runs completed; the formal service times were0.623/0.610/0.639s. Model load is recorded separately. The input is the original13.4-second mono44100Hz PCM with corrected WAV lengths, not a synthetic echo buffer.

All four recognition strings agree. Relative to the intended42-word synthesis text, the normalized result has44 words and two extra tokens (`in`, `8`), giving word edit distance2/42=4.76%. This is comparison with the intended TTS text, not an independently human-transcribed acoustic reference, so it does not isolate ASR errors from synthesis artifacts. Word/segment times and probabilities remain in asr-results/requests.json. No perfect-recognition claim is made.

## Transport of the actual speech result

Two Docker network-none profiles configure80ms RTT,20Mbit/s rate and0/0.1% loss, using the prior measured calibration. Each runs26 requests:24 formal plus2 protocol warmups. Three shuffled repetitions compare HTTP1.1/TLS1.3 and HTTP3 with reuse off/on; two sequential requests per cell. Each request uploads the actual WAV and returns the exact recognition-result UTF-8 bytes.

The server replays0.622926892s of measured GPU service with an asynchronous wait. This is an explicitly calibrated network-record experiment, not52 new GPU inferences. Upload reception precedes the service wait; the full transcript is then returned. One active request avoids inventing parallel model capacity. Actual wait start/end are retained and checked; transport timing uses the client's single clock.

| Protocol | Reuse | Median complete request ms, loss0 | Median complete request ms, loss0.1% |
|---|---|---:|---:|
| h1 | False | 1553.544 | 1553.096 |
| h1 | True | 1386.565 | 1386.654 |
| h3 | False | 1560.495 | 1671.249 |
| h3 | True | 1388.579 | 1799.123 |

Each table cell contains six formal requests. Complete-request time includes connection acquisition, actual upload, calibrated model wait, actual response and byte validation. Both profiles passed all26 upload/result hashes, TLS/ALPN, connection reuse, timing, service-wait and qlog checks. Source, checkpoint and input/result hashes are retained. These few samples do not establish a production p95 or universal protocol ranking. Netem's configured link rate differs from measured application goodput and stochastic loss positions.

GPU process cleanup is in cleanup.json; transport container absence is in network-container-after.txt. The recognition process and the network replay are separate executions. No microphone access, speaker changes or enrollment files were used. GPU service was not inferred from the duration of the sound.

Revalidate with `python3 analyze_asr.py`, `python3 analyze_network.py loss0`, and `python3 analyze_network.py loss0.1`. run_asr.py requires the recorded cached model and installed CUDA/CTranslate2 environment. run_network.py uses the prior controlled-network Docker image and expects the pinned audio, transcript and asr-fixture.json; use a fresh output directory. [Protocol](PROTOCOL.md) specifies the source and scope.

This completes the ASR input/result preparation and transport-record stage. TTS first-playable delivery, image refinement, Computer Use and individual window/chunk/recovery comparisons remain part of experiment12-4's outstanding work.
