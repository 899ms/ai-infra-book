# Independent media feedback acceptance contract

These expectations were written before reading any media-feedback candidate output. `oracles.json` is the prewritten specification; `check-hand-arithmetic.py` checks rational/byte constants without importing an engine. A successful arithmetic check is **not** a successful network acceptance check.

The reviewed input is `media-feedback-inputs/normalize.py` and its frozen sixteen business DAGs, together with `transport-controller-loop/NEXT-SCOPE.md`. Existing public `topics/transport_sender.py` already accounts for multiple STREAM highest offsets and DATAGRAM identity. Existing public `topics/transport_closed_loop.py` supplies the actual serializer/arrival/ACK/pacer/RTT mechanism; the next media layer must connect the DAG without replacing sender feedback with prior teaching credit.

## Confirmed interfaces

Network author proposes `{application: normalized_dag, network: {...}}`, with directional links, horizon, optional controller, existing ACK policy, connection/stream limits, receive memory, consumption delay, initial cwnd and padding. Every in-flight application unit uses the declared 1,200 B QUIC UDP payload plus 28 B network overhead in these isolated comparisons; usable application payload is at most 1,168 B. DATAGRAM is atomic and never application-fragmented. Pure ACK is 64+28 B. These are input budgets, not a complete protocol encoding.

Network author confirmed `consume_delay=null` or omitted disables consumption/MAX advertisements; hand timeline cases require this plus pregranted sufficient flow credit and receive memory. A nonnegative consume_delay enables actual consumption and MAX updates; that is a separate case and must count each control packet's serializer/ACK effect. Thus the exact 0,1,4 three-message schedule is not compared to a scenario that inserts extra MAX messages.

Sender author confirmed inputs `initial_max_data` and `initial_max_stream_data:{flow:limit}`; state exposes `stream_highest_sent_offsets`, `max_data_consumed`, and `max_stream_data`. DATA frames use stream/offset/length or datagram id/length. Only a real arrived MAX changes authorization. Datagram IDs are unique per direction and cannot be retransmitted; PTO with no retransmittable STREAM must use a distinct PING/probe. Tests must inspect actual identity/frame records, not merely an aggregate byte count.

## Event and endpoint boundaries

Confirmed network priority is router completion -1, arrival 0, task completion 1, ACK deadline 1, feedback/sender timer 2, pump 3. A just-arrived ACK therefore affects a same-time pump, and ACK deadlines cannot race ahead of same-time arrivals. Tasks and serialization are nonpreemptive. Send policy FIFO/priority changes selection at actual start, while compute selection remains its original separate policy.

A cancellation message has ordinary reliable stream ordering: out-of-order receipt is not application delivery. Cancellation affects only its receiver's matching waiting tasks and outgoing not-yet-started message slices. It cannot abort running work, interrupt serialization, refund sender flight or stop recovery of already-sent reliable ranges. No RESET_STREAM is implemented in this scope. Cancelled unsent slices may therefore leave a real stream hole that prevents later reliable message delivery. The expected accounting is highest offset including holes, distinct from bytes actually transmitted.

A screenshot expected version belongs to a client business observer; client version changes are local events. Server compute must not peek at client current/future version. Oracle arrival times .07 and .09 avoid the .08 equality boundary intentionally: the author must specify local-version-event tie order before an equality case receives an expected outcome.

## Levels of the eight oracles

1. Shared cwnd and FIFO/priority cases give conditional complete/initial network timelines with explicit physical and flow premises. The shared-cwnd case expects three ACKs and no extra MAX/probe packets. Initial NewReno mode is permitted to grow from actual ACKs; no artificial constant cwnd is imposed.
2. STREAM/MAX authorization is a sender-local state obligation. A test can inject sender events for that level, but a full network test must show the exact control packet that arrived before allowing a new stream range. Never claim a free local MAX event is a network observation.
3. DATAGRAM loss is an all-trace identity/conservation oracle, with no prescribed recovery timestamp. A real drop selector names the PN/attempt actually emitted. Additional PTO probe/ACK wire traffic is counted separately, not hidden in the two-data-packet 2,456 B subtotal.
4. Cancel gap and cancelled-unsent-range cases supply receiver/application observations to isolate ordering and endpoint logic; they do **not** claim that the underlying network recovers at t=4. A future network test must produce the observations through real loss detection/recovery and may have a different time.
5. Reverse ACK competition gives exact queue and encoding arithmetic, with prior RTT variance20 explicitly selected to keep PTO after the queued ACK. ACK delay does not let the sender subtract the entire queue delay; its negotiated cap and first/prior sample rules still apply.
6. Version usability is evaluated from local state at action receipt/use, independently of whether transport succeeded. It cannot be reduced to a latency-only completion flag.

## Required candidate output before executable integration checks

Expose each actually started frame's direction/PN/id/stream interval/bytes, serializer start/end, arrival/drop, and ACK snapshot/ranges/actual arrival. Expose sender before/after flight and flow-limit state at attempted send/ACK/MAX/loss; a per-stream window must never be multiplied into total connection credit. Expose message byte intervals received versus ordered application delivery, task start/finish/cancel events with endpoint/resource, and local business version/use decisions. Probe frames must be distinguishable from datagram units.

Remaining contract questions must be resolved explicitly before matching all-trace outputs: local version-event tie order; rejection/wait semantics when sender validation returns several block reasons; whether loss selectors target PN or message-fragment/attempt with exact mapping; end-of-horizon status for incomplete reliable holes. These do not justify altering the prewritten byte or causal requirements to match whatever a candidate prints.

This directory changes no public engine, scenario, source lock, plan or book text. Later candidate checks should record candidate hashes, oracle hashes and precise coverage; preserve a failure when an implementation violates a precondition rather than quietly recomputing expected output from that implementation.
