# Media feedback application inputs

`normalized-inputs.json` contains sixteen executable application input descriptions converted from the frozen `shared-media-transport/scenarios.json`. `normalize.py` is a converter and packet-slice iterator, not a network simulator. It does not assign packet numbers, send/arrival times, ACKs, RTT, cwnd, loss or completion outcomes. The existing research and public engines are unchanged.

Run from the checkout root:

```sh
python3 calculations/research/media-feedback-inputs/normalize.py --output /tmp/media-inputs.json
python3 calculations/research/media-feedback-inputs/normalize.py --scenario screenshot-complete --packets --output /tmp/screenshot-slices.json
python3 calculations/research/media-feedback-inputs/check.py
```

The CLI verifies `inputs.lock.json` before reading the sealed sixteen scenarios. The lock pins the scenario JSON, original engine (for its defaults), business input provenance document, and NEXT-SCOPE document. The importable `normalize(name, source, packet_payload=1168)` accepts an in-memory source DAG; `packet_view(message, packet_payload=1168)` yields byte slices lazily. The saved unified JSON keeps a compact packetization description, so downstream consumers need not store tens of thousands of expanded slice dictionaries just to parse inputs.

## Consumer contract

Messages retain original business-block IDs, order, bytes and logical offsets. `sender`/`receiver` are client/server; `transport` is stream or datagram; `flow_id` identifies the application stream/flow. `stream_offset` is null for datagrams, whose `application_offset` is only a logical media coordinate and consumes no reliable stream credit. All ready/deadline/duration values are exact rational seconds serialized as strings. They are lower eligibility bounds, not precomputed execution timestamps.

Every dependency is `{id, event, endpoint}`. A message dependency means complete application delivery of that business message at the receiver; a compute dependency means completion of the task at its declared endpoint. Reliable message completion requires all byte slices and ordered stream availability, not the arrival of the last fragment alone. A consumer may act only at its own endpoint. The converter rejects cross-end dependency shortcuts that would need a real notification. In particular, server `tts-produce-0` depends on server `asr-model` completion, not on the client's receipt of `asr-text`.

Compute tasks retain the original engine's defaults: endpoint `server`, resource named `server`, one nonpreemptive task at a time per `(endpoint, resource)`. This resource is an existing abstract service queue, not an identified GPU, model kernel or FLOP budget. The independent `compute` scheduler is preserved (`fifo` by default); changing the send scheduler does not silently change compute scheduling. The eight TTS tasks each cost the declared 0.012 seconds and form a dependency chain. They are not a language-model prefill/decode or a codec-token-to-wire conversion.

`business_observers` retain image completeness, ASR result, playback blocks/slots, and screenshot expected version. Their endpoint is the actual destination of the required messages. Screenshot `version_changes` are local endpoint events; no remote endpoint may read that future/current client state without a message. The `version` field on the observer is the expected business version, not a transport sequence number. Requirements reference messages, and message/task dependencies connect the versioned result back to its input screenshot.

`on_delivery_cancel_tags` acts only after the complete cancellation message is delivered at its receiver; `cancel_tag` identifies matching local tasks or outgoing messages. Cancelling waiting work must not erase running compute, a started packet, already transmitted bytes or outstanding congestion flight. The converter preserves tags and scope but does not execute cancellation. Reliable messages cannot silently expire; datagrams may have `allow_expire` and an absolute business deadline. A deadline alone is not permission to abandon a reliable file.

## Packet view is not a protocol encoder

The default 1,168 B slice is application payload capacity for the next network's declared 1,200 B UDP-payload layout; this converter adds no header, padding, UDP/IP bytes or ACK cost. Those belong to the actual network serializer/accountant. The old 25,000 B teaching packet becomes one message with 22 slices: 21×1,168+472=25,000. Boundaries are retained, and adjacent messages are not coalesced. Therefore 1,200 upload blocks produce 26,400 slices and 200 final blocks produce 4,400, totalling 30,800; this is deliberately different from splitting a newly merged 35 MB byte array. The old block boundaries can affect network overhead and must remain visible in comparisons.

All frozen unreliable messages fit one 1,168 B slice. Oversized datagrams are rejected: splitting an atomic unit would require an application reassembly/quality policy not supplied here. Small reliable screenshot messages may span multiple slices and complete only after all their bytes are usable. For example 3,443 B becomes 1,168+1,168+1,107.

## Preserved business quantities and their provenance

| Declaration | Preserved amount | Provenance/meaning |
| --- | ---: | --- |
| Image upload/final | 30,000,000 / 5,000,000 B | Existing book workload assumption; decimal MB, not measured universal model output |
| Image model task | 0.3 s | Existing declared service time, not an official throughput claim |
| ASR input | 8×640=5,120 B | Existing PCM16 mono/16kHz/20ms workload: 16,000×0.02×2=640; ready 0.02 through 0.16 s |
| ASR task/text | 0.05 s / 64 B | Existing declared service time and response payload |
| TTS output | 8×960=7,680 B | Existing PCM16 mono/24kHz/20ms workload: 24,000×0.02×2=960; output is PCM, not embeddings or codec-token storage |
| TTS production | 8×0.012=0.096 s | Existing serial service work, plus unchanged contention/dependencies; no computed finish time |
| Screenshot/action/cancel | 3,443 / 64 / 32 B | One archived PNG size and existing action/cancel assumptions used by the frozen mixed scenario |
| Preview | 20×25,000=500,000 B and extra 0.05 s | Separate existing extra output/work declaration; not a free partial final image |

The mixed scenario totals **30,008,595 B client→server** (image+ASR+screenshot+cancel) and **5,007,808 B server→client** (final+ASR text+TTS+action), or **35,016,403 B**. Preview increases the total to **35,516,403 B**. These are declared application bytes before cancellation/expiry, not sent wire bytes or delivered quality. The related provenance document also discusses 3,545/3,708 B PNGs, but the frozen sixteen scenarios do not use those screenshots; the converter does not manufacture a three-screenshot workload.

## Legacy fields requiring explicit network decisions

`external_legacy_assumptions` preserves all original teaching-network configuration and per-message `drop_first`/`recovery_ready` values, outside the consumable application messages. Specifically:

- `shared_credit_bytes`, `reliable_receive_credit_bytes`, `stream_credit_bytes` are not automatically initial cwnd, MAX_DATA or MAX_STREAM_DATA. The next network must declare actual shared controller/pacer, connection and stream limits, receive memory and consumption.
- `header_bytes` and `ack_bytes` from one-byte teaching examples are not valid QUIC layouts. Configure real packet/ACK budgets independently.
- `recovery_ready` is a prescribed teaching recovery instant, not sender-visible loss/PTO evidence. `drop_first` targets an old business block; after fragmentation a real PN/attempt selector must be supplied rather than silently dropping all fragments or selecting the first.
- `delivery_mode=connection` is retained as a historical HOL replay choice, not implemented as QUIC cross-stream blocking. The feedback experiment must explicitly choose an application delivery policy; a feedback-coupled comparison is no longer the old fixed-trace replay.

Link bandwidth/propagation and connection-ready offset are preserved as separate potential inputs, but no controller/ACK/router/MTU/flow-control defaults are invented. `connection_ready_seconds` constrains sending; it is not a handshake simulation or a reason to delay local compute independently.

`check-result.json` records byte/slice conservation for all sixteen scenarios and fixed hand totals. It does not assert that a feedback engine already consumes this schema or that any of the original teaching completion times remain unchanged after real packetization and feedback.
