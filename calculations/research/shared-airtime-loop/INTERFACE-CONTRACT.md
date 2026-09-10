# Shared-airtime network integration contract (before implementation)

This candidate extends the frozen public media `Network` with a single nonpreemptive client↔AP wireless service and the original directional AP↔server WAN. It imports the public Application, sender, ACK receiver, controller and pacer; it does not fork their algorithms. No wireless option (or enabled=false) delegates directly to the public calculate and preserves the complete old result. Only this research directory changes.

## Causal topology and ACK correction

Up: source client actual wireless DATA transmission → AP receive → WAN queue/serialization/propagation → server transport receive. Down: source server WAN serialization/propagation → AP wireless queue → client receive. Original links are WAN rates and delays, not PHY rates; they are not removed or counted twice. Wireless exchange includes separate access wait, DATA PPDU, propagation, SIFS/MAC ACK and sender-known completion.

**A transport ACK freezes at its transport source's first actual transmission:** client ACK at wireless DATA start; server ACK at WAN start. An AP forwarding an already sent server ACK cannot refresh its ranges from the server's later state. This explicitly narrows the earlier input/NEXT-SCOPE shorthand “snapshot at wireless start”; applying that shorthand to downlink AP forwarding would require nonexistent instantaneous remote knowledge. Both freeze and later wireless forwarding times remain in the trace.

MAC ACK is local radio feedback, never a sender.ack event, RTT update or flow credit. A DATA PPDU may deliver at its receiver before its transmitter learns MAC success. MAC ACK loss therefore permits same-PN retries and receiver deduplication; end-to-end ACK may arrive while a MAC retry is still pending. A later end-to-end recovery has a new PN, unlike MAC recovery.

## Input contract

Existing `{application,network}` remains. Optional `network.wireless_access` contains enabled, mode/profile, max_attempts, retry_wait and failures (direction, pn, one-based attempt, outcome data_lost/mac_ack_lost). Exact profile validation comes from root-owned airtime.py; unknown complete failure timeout rejects. The source's 45us RXSTART watchdog is not a complete ACK timeout. A declared teaching completion wait is valid only when labeled as such.

First candidate permits a global FIFO arbitration, client before AP for exact ties, no random DCF, hidden nodes, RTS/CTS, aggregation or adaptive PHY. Fixed access wait reserves the chosen direction nonpreemptively, then the actual source packet/ACK snapshot is selected at DATA start using current sender eligibility and application cancellation. The inherited FIFO/priority selection still chooses the source's eligible message. Already serialized/downlink AP packets cannot be changed or canceled retroactively. Source and AP queues and MAC retries share the one radio; source congestion/flow/pacer eligibility is checked only for first sends, never charged again for a same-PN MAC retry.

A DATA success forwards at receive time. Duplicate same-PN wireless deliveries do not forward duplicate WAN traffic or repeat application work. A duplicate is filtered below transport in either direction; it causes neither another transport ACK nor another application delivery. Its MAC ACK still consumes local service. MAC failure is known only after its actual modeled timeout; retries become eligible after explicit retry_wait, bounded by max_attempts. Exhaustion cannot instantly inform the remote endpoint or free sender flight. QUIC recovery remains driven by real ACK/loss/PTO.

## Implementation boundaries

Subclass public Network. Reuse public pump to assign PN, commit sender.sent, charge pacer and snapshot ACK; intercept only source link scheduling. Public run event dispatch may be mirrored to add wireless/WAN events; its final result construction remains inherited. Do not copy controller or recovery math. Source transmission records keep first on-source-link start/end, and add WAN/air-hop audit fields. Distinguish one end-to-end packet's existing wire_bytes from every MAC attempt's PSDU/airtime; never count retries as new unique payload.

Run existing app/feedback/consume/timer event priorities unchanged. Wireless DATA receive is a receive-priority event, exchange release precedes same-time arbitration, source ACK snapshot follows all same-time received updates. Any in-progress exchange remains nonpreemptive beyond the observation horizon; only observed prefixes count as observed airtime. Packet budget and radio-attempt budget are separately finite. Sources and runtime dependencies are hash verified; errors reject rather than silently coerce physical fields.

## Required staged evidence

First compare wireless-disabled to all 19 frozen media results (small first, five full after core review). Enabled small cases independently fix airtime arithmetic, bidirectional exclusion, source ACK freeze vs AP forwarding, duplicate MAC delivery, failure knowledge, MAC exhaustion→real end-to-end probe, and prefix-at-horizon. Use explicit finite WAN serialization in each hand oracle, or a separately labeled zero-service teaching topology if later authorized; do not quietly treat a very large finite rate as infinity.

Then preserve the original full30MB/5MB and mixed FIFO/priority×ACK-policy workload; no smaller pilot substitutes for it. Reference OFDM and second-scale teaching profiles are separate modes. Results are a declared wireless-service calculation, not a measured WLAN, full ns-3 execution, TCP/TACK implementation, or whole C69 completion.
