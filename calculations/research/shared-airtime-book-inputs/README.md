# Shared-airtime full workload input preparation

Status: five full inputs derived and constructor-validated. Subsequently, all four mixed full workloads were explicitly authorized and executed successfully; see the execution record below. This is an explicit unaggregated legacy OFDM reference selection, not a measured WLAN, browser default, full DCF simulation, or TACK implementation. The upstream source/profile review remains separate from this input validation.

`book-inputs.json` contains the original image baseline and mixed FIFO/priority × immediate/aggregate four cells. Every application field and existing network field is byte-value equivalent to its sealed media-feedback-loop input. The sole added path is `network.wireless_access`. `input-differences.json` records each case's exact counts, WAN values, horizon, and structural equality check.

The current original is 30,000,000-byte upload / 5,000,000-byte image response, **WAN 20 Mbps up / 100 Mbps down**, 50 ms propagation each way. The 5 MB response is a byte quantity, not a 5 Mbps WAN rate. Images retain 25 KB application blocks with independent 1168-byte packetization: 26,400 upload packets + 4,400 response packets = **30,800**, rather than the 29,966 of a continuously packetized stream. Mixed inputs retain 1,420 messages and 30,822 declared fragments (26,412 up / 4,410 down), with 30,008,595 / 5,007,808 declared application bytes. Expiration and cancellation may reduce actual sends; declared totals are not delivery claims.

The original NewReno controller, initial cwnd 12,000 bytes, all flow limits, receive memory, no scheduled application consumption, numeric quantum, ACK policy, DAG, priorities, deadlines and model task durations remain unchanged. Reference wireless uses one global nonpreemptive FIFO channel, 54 Mbps DATA and 6 Mbps MAC ACK, no aggregation, no encryption, no random contention, selected 34 µs pre-exchange idle and 16 µs SIFS. Both transport DATA and pure QUIC ACK traverse their own MAC exchanges. Complete MAC ACK failure timeout remains `null`; `failures=[]`, `max_attempts=1`, and no retry wait are explicit. No unknown timeout is substituted from the RXSTART watchdog.

For each padded transport DATA: IP 1228 B → PSDU 1264 B → DATA PPDU 208 µs; normal MAC ACK PPDU is 44 µs; reserved success exchange is **302 µs**. A QUIC ACK is IP 92 B → PSDU 128 B → 40 µs PPDU, with **134 µs** reserved exchange. These MAC-frame bytes are distinct from WAN wire bytes and QUIC acknowledgment counts. Upstream official originals and URLs/revisions are referenced in `sources.lock.json`, without copying or rewriting public locks.

Assuming all declared data are sent once, image DATA WAN wire is 37,822,400 B and air service 9.3016 s. Its no-retry/no-probe/no-MAX ACK conditional upper ledger is 30,800 ACKs, 2,833,600 WAN bytes and 4.1272 s air service. Mixed DATA wire is 37,849,416 B and air service 9.308244 s; the corresponding conditional ACK ledger is at most 30,822, 2,835,624 B and 4.130148 s. Aggregate ACK count must be measured from the actual trace, not inferred as ceil(data/2). MAC ACK count, pure QUIC ACK count and sender-reported loss of old pure ACK identities must remain separate.

The unchanged 60-second horizon preserves fairness with the original baseline. Rough serialized WAN plus wireless service totals leave substantial room at this scale, but are **not a completion bound** for feedback, deadlines, or PTO. Future runs must report unfinished work and actual completion separately. If 60 seconds proves insufficient, create a new paired experiment extending both old and wireless inputs; do not silently change only one side.

Run validation only:

```sh
python calculations/research/shared-airtime-book-inputs/run-book.py --ready
```

Future explicitly authorized full execution, one case per process:

```sh
python calculations/research/shared-airtime-book-inputs/run-book.py --run --case image-baseline
```

The runner writes effective inputs, full result JSON, manifest, and compact summary under `runs/`. It refuses overwriting an existing manifest, verifies input/source locks and full public Python package inventory before and after calculation, and records elapsed time and hashes. A source change rejects the run; `prepare.py` is an explicit resealing operation, never performed automatically by the runner. The successful-run status only states stable identity, not independent mathematical acceptance. Initial preparation exercised `--ready` and all five constructors only. The later authorized full runs below exercised the full execution path without resealing inputs or changing the runner.

## Authorized four-cell execution

All four original handles returned exit code 0; no restart, kernel edit, input reseal, or horizon change occurred. `run-completion.json` records the actual session IDs, elapsed wall time, complete-result hashes, manifest hashes and business/wireless summaries. All result files were independently rehashed after completion and matched their manifests; before/after source maps were equal. This verifies execution and artifact identity, not an independent replay of every network event.

| Case | Session | Wall seconds | Transmissions | Reserved air seconds | Image complete seconds |
|---|---:|---:|---:|---:|---:|
| mixed-fifo-immediate | 9067 | 171.665181 | 61626 | 13.434468 | 15.993881866 |
| mixed-fifo-aggregate | 19108 | 102.210199 | 44279 | 11.109970 | 15.669243112 |
| mixed-priority-immediate | 47948 | 162.030922 | 61642 | 13.437956 | 15.920135004 |
| mixed-priority-aggregate | 12157 | 103.249077 | 44291 | 11.112922 | 15.585252555 |

Both FIFO cases miss all eight TTS blocks (0.16 seconds missing audio). Both priority cases deliver all eight TTS blocks, with actual playback from 0.4 to 0.56 seconds. Image and ASR observers complete in all four cells. The computer-use observer remains incomplete/unusable, so all four global `complete` flags are false despite zero pending packets. No MAC retry attempts occurred. The compact summaries do not replace the full `runs/*-result.json` traces. The image baseline is run separately by the root agent and is not included in this four-handle execution claim.
