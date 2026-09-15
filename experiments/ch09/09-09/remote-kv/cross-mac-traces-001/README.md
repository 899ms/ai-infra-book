# Default-threshold multi-turn remote cache

Actual Qwen3-8B BF16 SGLang producer and fresh consumer engines on RTX PRO, with native KV pages stored on the Mac over SSH. Fixed recorded inputs, one generated token per turn. All paired outputs equal: True. Published pages: 213; GET page operations: 110; conflicting duplicate writes: 0.

| Phase | Requests | Request hit rate | Token-weighted hit rate | Device / host / storage hit tokens | Sum of request seconds | Requests with GET | Sample p95 GET sum per fetching request |
|---|---:|---:|---:|---|---:|---:|---:|
| chat-producer | 4 | 75.00% | 63.75% | 480 / 0 / 0 | 1.253077 | 0 | N/A |
| chat-consumer | 4 | 75.00% | 63.75% | 480 / 0 / 0 | 1.178861 | 0 | N/A |
| agent-producer | 12 | 91.67% | 83.37% | 16304 / 0 / 0 | 3.490569 | 0 | N/A |
| agent-consumer | 12 | 91.67% | 92.37% | 16304 / 0 / 1760 | 145.086910 | 5 | 24.467310 s |

All fetched page hashes match the Mac files. Native chained page hashes are independently recalculated from the exact input token IDs; each publication barrier confirms the required keys. Every client GET is assigned to a request interval on the same remote monotonic clock. GET time excludes existence checks, queueing and model computation; no clocks are subtracted across hosts. Per-turn records include the replay interval since the previous response, which includes publication instrumentation and is not original user/tool think time.

The installed backend defaults to a 256-token prefetch threshold (source hash and matching lines in installed-threshold-source.json). All Chat inputs are shorter than 256, so the default consumer performs no remote GET. The Agent consumer fetches 110 pages in five turns; higher token hit rate accompanies much longer measured request time. The producer already reuses device prefixes across turns and is not an independent cold control. The separate threshold16 Chat variant and cache-disabled control address these distinctions.

All engines and SSH commands exited zero, final GPU compute-process listings were empty, and each Mac store was terminated and waited. Raw responses, per-page client traces, Mac ledger, publication barriers and source hashes are retained.

Scope: one replay per trace/configuration; quantiles use nearest rank and are descriptive small-sample values. One-token outputs cannot establish task quality; source Agent task failure and Chat arithmetic errors remain documented. These results add actual remote retrieval to the existing routing evidence, but the matched remote-aware three-policy comparison remains pending.

Recheck from repository root with `python3 experiments/ch09/09-09/remote-kv/cross-mac-traces-001/analyze.py`.
