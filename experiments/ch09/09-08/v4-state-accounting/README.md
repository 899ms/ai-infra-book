Completion update: parent experiment is delivered in its request-replay/storage-record scope; see [final coverage review](../COMPLETION-REVIEW.md). Earlier pending-work notes below are historical.

# V4 checkpoint payload / recovery accounting

Completed 24 analytical scenarios and 288 request recovery records, using the recorded twelve-turn Agent token-count and chained-prefix fixture with the pinned V4-Flash backbone layout. This does not execute V4 or claim its tokenizer produces the Qwen trace lengths. See [protocol](PROTOCOL.md), [results](results.json), and [verification](verify.py).

The complete first snapshot is 19,260,416 bytes; the last is 39,300,096 bytes. Every snapshot includes 12,206,080 bytes of allocated FP32 compressor buffers. The first snapshot therefore does not fit a 16 MiB budget. The 43 backbone layers include 2 window-only, 21 CSA and 20 HCA layers. A completed CSA boundary still retains its preceding overlap group; compressed history alone cannot recover the exact continuation state.

The table uses a worker restart before each request, with additional store invalidation before turn 7. Bytes are logical, unshared tensor payloads; snapshots are immutable and evicted oldest-first. Restores require compatible complete prefix identity. No checkpoint may restore future or incompatible state.

| Snapshot budget MiB | Policy | Written bytes | Read bytes | Recomputed positions |
|---:|---|---:|---:|---:|
| 0 | full | 0 | 0 | 19,556 |
| 0 | periodic4 | 0 | 0 | 19,556 |
| 0 | recompute | 0 | 0 | 19,556 |
| 16 | full | 0 | 0 | 19,556 |
| 16 | periodic4 | 0 | 0 | 19,556 |
| 16 | recompute | 0 | 0 | 19,556 |
| 32 | full | 201,228,288 | 222,686,208 | 7,924 |
| 32 | periodic4 | 55,468,032 | 174,114,816 | 9,796 |
| 32 | recompute | 0 | 0 | 19,556 |
| 64 | full | 347,860,992 | 259,129,344 | 5,220 |
| 64 | periodic4 | 94,768,128 | 174,114,816 | 9,796 |
| 64 | recompute | 0 | 0 | 19,556 |

A history-only checkpoint is deliberately rejected under this contract: without the window and main/index compressor state, the fallback recomputes the full input. The pending compressor positions alone do not establish a valid replay start. Exact positions and full allocated buffer bytes are both retained in results, and should not be confused.

No V4 save/restore or model latency is inferred from dense Qwen page measurements; those timing fields are null. Position/model/prefix metadata must also be serialized in an implementation, and its encoding overhead is outside this tensor ledger. Weights, MTP, allocator padding and temporary workspaces are excluded. This accounting complements the existing native dense-cache and four-tier page-policy experiments; overall 9-8 coverage and figure integration remain pending.

Reproduce locally: `python3 experiments/ch09/09-08/v4-state-accounting/run.py`, then `python3 experiments/ch09/09-08/v4-state-accounting/verify.py`. Verification passed source SHA checks, a separate closed-form layer payload calculation and all causal recovery/budget invariants. No changes were made to calculations/.
