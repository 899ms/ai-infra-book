# Controlled Docker transport profiles

This is an additional transport stage for experiment12-4. The full image-refinement, ASR/TTS and Computer Use comparisons remain unfinished.

Docker on RTX uses its own network namespace (`--network none`) and NET_ADMIN. Only the container loopback qdisc is changed; host interfaces and routing are untouched. The image build log, image identity, package inventory, commands and calibration raw output are retained.

Calibration: ten pings and one three-second TCP transfer per profile. The configured40ms traversal delay produced mean RTT80.126ms at zero loss and80.120ms at0.1% configured loss. TCP receiver goodput was17.723 and17.388Mbit/s under the20Mbit/s configured rate. Rate is a link setting, not a promise of equal application goodput. The unshaped loopback control measured0.037ms mean RTT. These are short measurements, not a WAN characterization. Netem loss is stochastic; configured loss must be distinguished from observed qdisc drops and TCP retransmissions.

The unchanged prior HTTP1.1/TLS1.3 and HTTP3 runner is used for two profiles, each with192 formal requests plus2 warmups. Three shuffled repetitions vary connection reuse and1/4 concurrent lanes. The64KiB echo payload, certificate validation, negotiated ALPN, per-request hashes and qlogs are retained. This stage does not supply application results or claim HTTP2,0RTT,session resumption, window/chunk tuning or application-level recovery.

See [calibration](calibration-summary.json) and [protocol](PROTOCOL.md). Both profile processes terminated successfully and their Docker containers were removed. All388 requests (384 formal +4 warmups) passed byte, TLS/ALPN, connection-reuse and qlog validation. Netem settings were checked before/after each profile, with zero residual queue backlog.

| Protocol | Reuse | Concurrent lanes | Median request ms, loss0 | Median request ms, loss0.1% |
|---|---|---:|---:|---:|
| h1 | False | 1 | 296.631 | 296.475 |
| h1 | False | 4 | 400.989 | 407.281 |
| h1 | True | 1 | 133.364 | 133.172 |
| h1 | True | 4 | 311.381 | 311.303 |
| h3 | False | 1 | 565.790 | 565.001 |
| h3 | False | 4 | 588.310 | 591.271 |
| h3 | True | 1 | 137.016 | 137.246 |
| h3 | True | 4 | 443.597 | 443.420 |

Each cell contains24 formal requests across three shuffled repetitions. The request clock includes connection acquisition, payload transfer and validation. H3 can be slower here; these results do not establish protocol-wide superiority. The0.1% profile reports19 actual netem drops over38149 transmitted qdisc packets; this observation is not substituted for the configured random-drop parameter. Full records retain handshake times, per-trial medians, qlogs and source hashes.

Revalidate with `python3 analyze_calibration.py`, `python3 analyze_profile.py loss0`, and `python3 analyze_profile.py loss0.1`. Docker source uses a tagged base; the resolved built image ID and package inventory are archived, so rebuilds must compare those identities. Payloads remain synthetic echo data. Application artifacts, tuned TCP windows, chunking and application recovery are still required for12-4.
