Completion update: parent experiment is delivered in its request-replay/storage-record scope; see [final coverage review](../COMPLETION-REVIEW.md). Earlier pending-work notes below are historical.

# Agent GPU/host capacity scan

Completed 108 actual model calls: 72 Agent target calls and 36 unrelated pressure calls. All target output IDs agree across before/after pressure and scanned settings: **True**. This is a fixed one-token replay of the same12 original Agent inputs, not a task-quality run.

| GPU token pool | Host ratio | Target phase | Device hit tokens | Host hit tokens | Request hit rate | Token hit rate | Target time sum (s) |
|---:|---:|---|---:|---:|---:|---:|---:|
| 4096 | 2 | target_before | 16304 | 0 | 91.67% | 83.37% | 2.150863 |
| 4096 | 2 | target_after | 2224 | 17232 | 100.00% | 99.49% | 0.850548 |
| 8192 | 2 | target_before | 16304 | 0 | 91.67% | 83.37% | 2.118154 |
| 8192 | 2 | target_after | 19456 | 0 | 100.00% | 99.49% | 0.736715 |
| 16384 | 2 | target_before | 16304 | 0 | 91.67% | 83.37% | 2.090995 |
| 16384 | 2 | target_after | 19456 | 0 | 100.00% | 99.49% | 0.713954 |

Storage hits are zero throughout; no storage backend is configured. The native SGLang counters establish actual host reuse, rather than an inferred hit based on file existence. The analyzer checks effective GPU capacity from server_info, exact seeded3584-token pressure inputs,36 calls per fresh engine,16-token-page counters, input/source hashes and terminal engine/GPU cleanup.

At4096 GPU tokens, the12 post-pressure targets reuse2224 device tokens and17232 host tokens. At8192 and16384, all19456 reusable target tokens stay on device. This sweep holds host ratio2, so absolute host capacity grows too; the separate agent-dram-capacity run fixes GPU4096 and varies host capacity alone.

Per-turn complete-request times and descriptive nearest-rank sample p95 are in summary.json. They include model work, so they are not isolated host-copy latency or physical memory bandwidth. Each capacity has one pass in fixed order; first requests may include startup/JIT effects. Equal one-token outputs do not prove bitwise-equal KV tensors. All prior file/remote/failure records remain separate.

Historical9-8 remains open for the remaining storage-capacity/save-policy/V4-state comparison. Recheck from repository root with `python3 experiments/ch09/09-08/agent-host-capacity/analyze.py`.

![Native capacity hit levels](../agent-host-capacity/capacity.svg)

The ratio2 comparison point is reused from the first sweep, not an additional independent repetition. SVG/PNG were visually checked.
