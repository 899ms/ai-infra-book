# Completed-result full trace audit

`check-full-trace.py` reads a completed result and checks its byte hash before/after the audit. It imports no candidate module and does not replay a transport engine. Root must confirm process completion before supplying the path; filenames and manifests alone are not proof that a run finished. The source-lock remediation reruns must be audited after the root's completion notification.

Example:

```sh
python3 calculations/research/media-feedback-loop-review/check-full-trace.py \
  calculations/research/media-feedback-loop/runs/book-image-baseline-result.json \
  --image-baseline \
  --output calculations/research/media-feedback-loop-review/book-image-baseline-independent.json
```

For mixed scenarios omit `--image-baseline` and use a distinct report filename for each completed result. Mixed quality can legitimately be incomplete: the script separately reports offered application bytes, unique sent bytes, physically received unique bytes, complete delivered message bytes, screenshot usability, and TTS slot playback/missing duration. It does not infer success from empty queues or from all packets having ceased transmission.

Checks cover:

- Per-direction nonoverlapping physical serialization, exact wire-byte/rate duration and propagation; no received flag on dropped data or a future arrival.
- Unique actual PN identities and exact correspondence to sender sent events; byte slices map to the declared application message/STREAM coordinates. Retransmitted ranges deduplicate in business byte accounting, and atomic DATAGRAM identities never repeat.
- Every sender ACK event is backed by an actually arrived reverse ACK; its ranges cover only packets received before that ACK started serialization. Aggregated ranges agree with the recorded send snapshot.
- Wire bytes and horizon-truncated serialization; application offered/sent/received/delivered conservation; per-message full byte availability at claimed delivery, plus reliable stream contiguous-prefix availability. Later duplicate arrivals do not invalidate an earlier complete delivery.
- Reliable receive memory reconstructed from interval unions and actual consume events; atomic datagram transient occupancy, expiry and receiver-memory admission; reported peak memory matches.
- Message/task dependencies precede actual start, compute duration equals the declared service demand, finished work has an actual completion time and per-resource compute does not overlap.
- STREAM highest sent offsets include holes, sum into connection MAX_DATA consumption, and do not double count retransmission.
- Image/ASR completion matches required message delivery. Screenshot usability uses only its local version at result delivery. TTS slot use requires timely complete unit delivery and distinguishes scheduled end from an end reached by the horizon.

The image baseline flag additionally requires30800 data packets,35000000 application bytes with offered=sent=received=delivered, all messages delivered, and one0.3s compute task. This derives from1400 retained25KB blocks, each split21×1168+472 bytes, not from the result's own summary.

Limits: the current auditor explicitly rejects router-enabled inputs, because the simple propagation assertion would otherwise misidentify router delay. It does not independently replay congestion-controller numerical state, pacing debt, loss-detection formulas or reliable-audio stall policy; those retain separate small/state oracles. The audit reports TTS actual played duration and checks slot loss, not a generic model quality score.
