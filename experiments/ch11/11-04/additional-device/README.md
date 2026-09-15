# Adding the RTX server to a Mac rollout batch

Three matched two-task comparisons completed. Fixed allocation runs sequence then extraction on the Mac; additional allocation runs Mac sequence and RTX extraction with overlapping worker intervals. All12 task outputs pass the strict JSON/content checks, and all model workers exit. This adds an actual physical device, with explicitly heterogeneous backends.

| Repetition | Mac-only batch (s) | Mac+RTX batch (s) | Time saved by adding RTX (s) | Extra teaching cost (units) |
|---|---:|---:|---:|---:|
| 0 | 13.431185 | 82.324322 | -68.893138 | 0.03809481 |
| 1 | 13.481022 | 79.406697 | -65.925675 | 0.03646515 |
| 2 | 13.648449 | 79.532276 | -65.883827 | 0.03647608 |

Teaching price is1 unit per reserved Mac-hour and1 unit per requested RTX-hour. Mac reservation covers the whole batch; RTX reservation uses the controller's SSH command window. These are declared accounting assumptions, not GPU busy-time measurements or a vendor bill. All three paired trials cost more and finish later with this fresh-process additional-device arrangement. This does not predict the result for an already warm RTX worker or longer task stream.

The batch clock runs on the Mac and includes fresh model startup, generation, SSH completion, result retrieval and the receiving SQLite transaction. Per-host model preparation/generation times are separately recorded without subtracting clocks across hosts. Existing weight files were cached on both hosts; weight distribution was not measured. RTX results are admitted only after transfer and transaction commit. The four separate artifact-retrieval commands and their connection overhead are part of this implementation's measured latency.

Mac uses the original MLX4bit revision; RTX uses Qwen3-8B BF16 revision b968826d9c46dd6066d109eabc6255188de91218. Exact stored prompt IDs are reused. Each Mac extraction emits242 tokens; each RTX extraction emits289 because its JSON contains additional spacing. All parsed24-key mappings and key order match. Sequence emits258 tokens and matches its original token reference. Thus the same effective tasks complete, but the heterogeneous output-token sequences are not identical and token throughput is not compared as equivalent work.

All generated-token streams match their committed receiver databases. Nine Mac samples use the original per-token durable manager; three RTX samples use post-completion transfer and receipt. The latter is not a streaming manager or recovered partial output. The analyzers retain this difference. These12 newly generated logical samples have no new training-consumption checkpoint yet: completed_training_tokens remains null, and prior checkpoints are not relabeled as theirs.

This completes the additional-physical-device measurement for the baseline two-task batch. The original formal run still supplies actual interrupted restart/preserve measurements. Integrating the arrangements with resource lifetime, matched training completion and total cost remains the open historical11-5 work; this directory alone does not close it.

Recheck from repository root with `python3 experiments/ch11/11-04/additional-device/analyze.py`. Raw per-token logs, task definitions, SQLite receipts/snapshots, source hashes, randomized run order, process exits and GPU samples are retained. Re-running the controller requires a new local and remote directory because result paths deliberately reject overwrite.
