# Cache-disabled matched-input recomputation

All 48 requests completed: three shuffled passes across the same four Chat and twelve Agent inputs. Each response generated one token, reported zero cached tokens and zero retractions. All repeated outputs matched, and all outputs also matched the corresponding remote consumer responses. The fresh engine exited zero and the final GPU compute-process listing was empty.

| Trace | Turn | Input tokens | Complete request median (seconds) |
|---|---:|---:|---:|
| chat | 0 | 116 | 0.032459 |
| chat | 1 | 168 | 0.033556 |
| chat | 2 | 217 | 0.030846 |
| chat | 3 | 252 | 0.030499 |
| agent | 0 | 210 | 0.027395 |
| agent | 1 | 316 | 0.033193 |
| agent | 2 | 670 | 0.046398 |
| agent | 3 | 884 | 0.051110 |
| agent | 4 | 1233 | 0.091053 |
| agent | 5 | 1447 | 0.086867 |
| agent | 6 | 1796 | 0.099109 |
| agent | 7 | 2010 | 0.105989 |
| agent | 8 | 2359 | 0.126012 |
| agent | 9 | 2573 | 0.149346 |
| agent | 10 | 2922 | 0.154244 |
| agent | 11 | 3136 | 0.191720 |

The original model revision, BF16 dtype, eager attention settings, exact input tokens and one-token output budget are shared with the remote traces. Radix caching is disabled and hierarchical storage is not enabled. This isolates recomputation service from remote storage operations; it does not measure a busy worker or queueing.

All three timing samples per input are retained, including first-pass warmup, in summary.json. matched-comparison.json joins these values to actual remote consumer measurements and checks token equality. Remote runs have one sample per turn and a different execution order; do not infer a statistically established speedup or subtract these measurements as pure network time.

Recheck from repository root with `python3 experiments/ch09/09-09/remote-kv/trace-cold-control-001/analyze.py`. Source hashes, shuffled order, responses and process cleanup are verified by the analyzer. The subsequent three-policy record comparison remains pending.
