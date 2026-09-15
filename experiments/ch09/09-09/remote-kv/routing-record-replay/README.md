# Remote-aware routing: real-record comparison

Completed within the original exercise’s calculation / real-system-record scope. This final comparison composes measured Chat/Agent service, cache levels and earlier measured queue residuals into independent additive scenarios. It does not claim a newly deployed concurrent remote router.

There are 16 input states ×6 observed queue residuals ×2 busy-worker orientations ×2 held-out recomputation passes ×3 policies =1152 decisions. Repetition expands scenarios, not independent measurements. Calibration uses the earlier full-page remote recovery and cold-control pass0; evaluation uses passes1/2. The cache service samples come from the full recorded multi-turn consumers. Candidate output tokens match for every input.

| Trace | Busy candidate | Policy | Mean scenario completion (s) | Mean oracle regret (s) | Cache choices / decisions |
|---|---|---|---:|---:|---:|
| chat | cache | queue_first | 0.031637 | 0.000000 | 0 / 48 |
| chat | cache | cache_first | 6.065243 | 6.033606 | 48 / 48 |
| chat | cache | predicted_completion | 0.031637 | 0.000000 | 0 / 48 |
| chat | cold | queue_first | 4.617216 | 3.137552 | 48 / 48 |
| chat | cold | cache_first | 4.617216 | 3.137552 | 48 / 48 |
| chat | cold | predicted_completion | 1.555779 | 0.076114 | 6 / 48 |
| agent | cache | queue_first | 0.096012 | 0.000000 | 0 / 144 |
| agent | cache | cache_first | 13.327418 | 13.231405 | 132 / 144 |
| agent | cache | predicted_completion | 0.096012 | 0.000000 | 0 / 144 |
| agent | cold | queue_first | 12.090576 | 11.338602 | 144 / 144 |
| agent | cold | cache_first | 12.090576 | 11.338602 | 144 / 144 |
| agent | cold | predicted_completion | 0.751974 | 0.000000 | 84 / 144 |

When the cache candidate is busy, the idle recomputation candidate wins in these records. When recomputation is busy, always selecting the idle cache candidate can pay a much larger remote-read cost. The completion estimator usually avoids that cost, while preserving cheap device hits in Agent states. Its mean Chat regret is0.0761s in the busy-recomputation orientation; it is not an oracle. Prediction error is retained per decision, including missing existence-check cost and pass0 warmup.

The results JSON also reports request-weighted and token-weighted hit rates, device/host/storage totals, and descriptive selected-GET quantiles. Original (nonduplicated) remote retrieval samples and per-turn replay intervals are in the [default trace report](../cross-mac-traces-001/README.md) and [short-Chat report](../cross-mac-chat-threshold16-001/README.md). Those intervals contain publication barriers and are not original human/tool think times. GET sums exclude existence checks and model work. Queue residuals originate in the earlier actual two-worker run; their application to these inputs is an explicit scenario assumption.

Limitations: one-token outputs measure routing/cache behavior rather than task quality; the original Agent failure and Chat arithmetic errors remain documented. Snapshot decisions do not evolve cache state or model concurrent GPU interference. Sample p95 values do not establish production tail latency. The earlier live three-policy test remains the evidence for actual dispatch and queueing behavior.

Reproduce from repository root:

```sh
python3 experiments/ch09/09-09/remote-kv/routing-record-replay/run.py
python3 experiments/ch09/09-09/remote-kv/routing-record-replay/verify.py
```

The protocol records ties, calibration, independent-state assumptions and all1152 combinations. The verifier checks source hashes, complete unique coverage, decisions, regret and summary aggregation.
