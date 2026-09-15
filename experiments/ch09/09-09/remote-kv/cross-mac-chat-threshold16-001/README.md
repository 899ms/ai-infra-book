# Short-Chat remote prefetch at 16 tokens

Actual Qwen3-8B BF16 SGLang producer and fresh consumer engines on RTX PRO, with native KV pages stored on the Mac over SSH. Fixed recorded inputs, one generated token per turn. All paired outputs equal: True. Published pages: 15; GET page operations: 15; conflicting duplicate writes: 0.

| Phase | Requests | Request hit rate | Token-weighted hit rate | Device / host / storage hit tokens | Sum of request seconds | Requests with GET | Sample p95 GET sum per fetching request |
|---|---:|---:|---:|---|---:|---:|---:|
| chat-producer | 4 | 75.00% | 63.75% | 480 / 0 / 0 | 2.797243 | 0 | N/A |
| chat-consumer | 4 | 100.00% | 95.62% | 480 / 0 / 240 | 18.468865 | 4 | 5.728505 s |

All fetched page hashes match the Mac files. Native chained page hashes are independently recalculated from the exact input token IDs; each publication barrier confirms the required keys. Every client GET is assigned to a request interval on the same remote monotonic clock. GET time excludes existence checks, queueing and model computation; no clocks are subtracted across hosts. Per-turn records include the replay interval since the previous response, which includes publication instrumentation and is not original user/tool think time.

This separate run changes prefetch_threshold to16 and starts from a new empty Mac store. Compare with the preserved default-threshold Chat run. It tests admission of short prefixes; the default is not silently changed in the original records.

All engines and SSH commands exited zero, final GPU compute-process listings were empty, and each Mac store was terminated and waited. Raw responses, per-page client traces, Mac ledger, publication barriers and source hashes are retained.

Scope: one replay per trace/configuration; quantiles use nearest rank and are descriptive small-sample values. One-token outputs cannot establish task quality; source Agent task failure and Chat arithmetic errors remain documented. These results add actual remote retrieval to the existing routing evidence, but the matched remote-aware three-policy comparison remains pending.

Recheck from repository root with `python3 experiments/ch09/09-09/remote-kv/cross-mac-chat-threshold16-001/analyze.py`.
