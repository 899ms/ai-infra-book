# Independent small media-network review

`check-network-independent.py` now executes twelve small cases through the actual candidate network and stores `network-independent.json`. No recovery_ready or completion timestamp is supplied. Original conditional timing/causal requirements remain in `oracles.json`.

The following cases passed at the hashes recorded in the JSON:

- Shared initial2400B cwnd with three independent streams: actual data start0,1,4 and total3960 wire bytes; streams do not multiply the initial connection allowance.
- A zero-credit stream remains blocked after another stream's data and ACK finish.
- Actual receiver consumption generates a real reverse MAX packet carrying both absolute limits; neither local consumption nor ACK of the MAX is treated as its arrival.
- Dropped DATAGRAM is transmitted once, consumes no reliable credit, and is not delivered; a second unit succeeds independently.
- A sole dropped DATAGRAM produces a real sender PTO and a new empty-frame PING, never retransmission of that unit.
- Dropped reliable cancellation prefix is recovered through real sender feedback. Cancellation bytes arrive before ordered application delivery; only the latter suppresses waiting server work. Running server work and same-tag client work finish.
- Cancelling an unsent middle message leaves its reliable stream hole. Later bytes may transmit and consume highest-offset credit300 while the later message remains undelivered.
- FIFO and priority both preserve the first started packet; the priority case serves the higher numeric priority voice at1 rather than2.
- Reverse full data holds an ACK until307/23. Under explicit count_or_timer/every1/max_delay0, the actual ACK snapshot records raw delay261/23 and encoded delay1418478.
- The same complete screenshot and inference run yields a usable current-version action and an unusable stale-version action; transport success does not imply usability.

## Defect found and repaired

The initial candidate sorted positive business priority in ascending order. A voice message(priority100, ready0.5) incorrectly waited behind bulk-1(priority0), so priority behaved like FIFO and voice arrived4 rather than the prewritten3. This was reported to the network author/root. After the author's correction, the same expectation passes. The first failure report is preserved as `network-independent-before-priority-fix.json`.

That initial report also contains a test-mode issue, not an implementation defect: the legacy immediate ACK path deliberately has no encoded ACK snapshot. The reverse-queue encoding test now explicitly selects count_or_timer with every1/max_delay0. This preserves the hand timeline while exercising the new snapshot API.

## Additional MAX arithmetic clarification

The added consumption test initially omitted ACK serialization for the received MAX. Its corrected hand expectation explicitly counts that control ACK:

- Data arrives2. Reverse ACK starts2 and finishes3.
- Padded MAX starts3, serializes307/23 seconds, and reaches the sender399/23.
- MAX authorizes the second100B range immediately on that arrival.
- Its pure ACK starts at the same time, occupies the up serializer23/307 seconds, and then the second data starts at399/23+23/307=123022/7061.

This correction concerns the added case's physical premise, not a change to the original eight prewritten oracle requirements. There is no implementation report alleging the MAX must wait for its own ACK to authorize data. All actually sent control/data bytes are retained in the result.

## Scope limits

These are finite real-network checks, not complete validation of every event permutation, the whole normalized sixteen-scenario collection or the30MB media workload. The stream-limit arrival algebra is also independently covered by the sender review. Exact same-time screenshot version changes remain governed by the application's declared event rule, rather than inferred from future server state. The report records each case's candidate hashes and detects source changes within each run. No public or candidate implementation was edited here.
