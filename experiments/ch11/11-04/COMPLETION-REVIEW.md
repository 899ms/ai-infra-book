# Historical11-5 completion review

The original source archive/outlines/11-资源调度与运行环境.md specifies calculation/short-script scope. The audit's stronger actual-generation/preemption/recovery work is also present. Completion does not imply production RL or a single end-to-end four-arm live trial.

| Requirement | Evidence and exact scope |
|---|---|
| Qwen3 weights and network throughput | model-identity.json records4,351,884,216-byte MLX4bit weights; final-comparison/rtx-weight-identity.json records separate BF16 sizes. Network1GB/s is explicitly declared teaching sensitivity, not observed transfer. |
| Generation records and preemption times | formal contains12 actual paths,20 workers,eight SIGKILLs at32/96 committed non-EOS positions before ACK; original analyzer verified6778 invariants. |
| Fixed versus extra rollout capacity | additional-device contains three physical Mac-only/Mac+RTX paired batches with randomized order,12 accepted tasks, real overlapping process intervals and actual receiver commits. Startup and retrieval are charged; backends differ and raw outputs differ in formatting. |
| Retaining partial responses | formal restart/preserve paths restore actual committed prefixes, rebuild KV, finish at natural EOS and match baseline token IDs. Preservation cost is measured, not assumed free. |
| Generated / manager received / recovered / trained tokens | Original and new ledgers distinguish sampled positions, commits, duplicates, prefix rebuilding and actual optimizer checkpoint completion. Raw new3141-position training and canonical3000-position training are separate alternatives, not summed as unique work. |
| Same effective sample batch time and cost | canonical-training normalizes accepted JSON to original fixed serialization and verifies exact prompt/output SHA sets; each row trains the same500-position/two-task batch through new durable checkpoints. final-comparison explicitly composes measured generation and cold-consumer stages, preserving differences in run conditions. |
| Resource lifetime and when extra resources stop paying | final-comparison includes21 actual-timeline cutoff replays,18 teaching price/weight-transfer scenarios, continuous boundaries and exact finite complete-task cost checks. These are stated calculations, not new injected faults or stationary-throughput measurements. |
| Rollout/training SVG timeline | final-comparison/timeline.svg and plot_timeline.py show composed training stages and actual load/SIGKILL/recovery events with clock scope labeled; PNG visually checked. |
| Paper configuration versus teaching prices | All reports label local model/device variants and declared hourly prices. They do not label these runs as reproduction of a paper-scale cluster or actual invoices. |

Independent checkpoint verifiers reconstruct Adam's first update and check saved moments; source/token/checkpoint manifests and process exits are retained. Original extraction adapter updates have a tiny recorded non-bitwise difference despite equal loss; no deterministic-training guarantee is inferred. Canonical equality means input streams, not guaranteed identical GPU arithmetic.

Historical11-5 is delivered within its original calculation/short-script scope. The final report states all composition, heterogeneity, normalization, repeated-task and lifetime assumptions and must be read with those limits.
