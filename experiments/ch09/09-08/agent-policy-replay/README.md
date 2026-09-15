Completion update: parent experiment is delivered in its request-replay/storage-record scope; see [final coverage review](../COMPLETION-REVIEW.md). Earlier pending-work notes below are historical.

# Same-Agent capacity/checkpoint record replay

Completed729 explicitly defined scenarios and8748 per-request records:0/64/256 retained pages independently in four tiers, full/periodic4/no-persistence policies, and normal/restart-before-turn7/invalidation-before-turn7 conditions. Input prefixes and197 page identities come from the verified12-turn Agent trace.

This is an inclusive page-LRU reference replay, not native SGLang tree eviction or a new live four-tier service. Retention budgets exclude a sufficient execution working set; zero retained HBM is not zero physical GPU memory. Search stops at the first missing prefix page, so surviving suffix pages are not counted as reusable context.

The example below uses no volatile retention, no remote storage and a worker restart before turn7. Local-only timing uses measured direct-I/O page primitives and the documented model timing proxies.

| Local retained pages | Policy | Token hit rate | Logical bytes written | Estimated trace seconds |
|---:|---|---:|---:|---:|
| 0 | full | 0.00% | 0 | 1.162435 |
| 0 | periodic4 | 0.00% | 0 | 1.162435 |
| 0 | recompute | 0.00% | 0 | 1.162435 |
| 64 | full | 10.39% | 2569273344 | 9.508382 |
| 64 | periodic4 | 18.00% | 754974720 | 3.772373 |
| 64 | recompute | 0.00% | 0 | 1.162435 |
| 256 | full | 83.37% | 464781312 | 3.505444 |
| 256 | periodic4 | 58.91% | 460062720 | 3.242846 |
| 256 | recompute | 0.00% | 0 | 1.162435 |

A64-page LRU store can evict the root while streaming a larger full prefix. In this defined policy, the smaller periodic checkpoint can preserve a usable beginning and produce more hits than full saving. This illustrates why total resident bytes alone do not establish recoverability; it is not an observation about SGLang's native eviction algorithm.

All729 rows retain tier hit counts, recomputation-token counts, checkpoint writes, eviction counts, storage-read quantiles and estimated completion components. Page-local read/write times are measured. Remote timings come from actual SSH/HTTP page RPCs; unobserved page reads use a measured median and their fallback counts are explicit. Synchronous checkpoint costs are added without async overlap. Complete-prefix model service uses measured GPU-warm/host profiles; incomplete prefixes use measured full-cold request time, with no proportional partial-prefill speedup assumption. These are timing proxies, not observed full-task completion or guaranteed bounds.

Storage-read sample p95 is a quantile of repeated composed records, not independent production p95. Local writes include file/directory fsync; remote publication did not fsync. Storage persistence here means surviving a model-worker restart while the stores remain intact, not equal power-loss durability. Restart/invalidation events are simulated; prior native recovery/fault runs remain the actual execution evidence.

This completes the dense-page capacity/save-policy reference replay. Historical9-8 still needs the V4 compression/window-state accounting and final requirement integration. No compressed V4 tensors or V4 model execution are claimed by this Qwen-page replay.

Reproduce from repository root with `python3 experiments/ch09/09-08/agent-policy-replay/run.py` and `python3 experiments/ch09/09-08/agent-policy-replay/verify.py`. Verification checks all729 unique settings, input/source hashes, token conservation, fault reset invariants, checkpoint schedule and closed-form no-eviction write identities. It does not turn the stated reference policy into a measured native implementation.
