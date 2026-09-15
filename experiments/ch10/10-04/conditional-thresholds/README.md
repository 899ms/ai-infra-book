# Conditional deadline thresholds — partial10-4 calculation

The original exercise permits assumed effective performance for H20. These calculations use existing model-specific matrix work, not inference throughput and not6ND for MoE. Both tasks declare100B tokens and30 days. Qwen8 uses the archived32768-token workload; Qwen235 uses8192 tokens with balanced routing. They are separate tasks, not a matched cross-model speed benchmark. Within each task all hardware cases hold work fixed.

Persistent state is18bytes/parameter: BF16 weights plus FP32 gradients, master weights and two Adam moments. Ideal even division is a lower bound only; it excludes tensor/replica placement, activations, buffers, communication workspace and imbalance. No candidate is called memory-feasible on this basis.

For a sequence, let W be its recorded matrix FLOPs, G cards, b the deadline's allowed sequence time, and c the exposed communication time. Required effective matrix progress per card is W/[G(b−c)], if b>c. Otherwise the communication budget alone makes the deadline impossible. The exact rational inverse is independently checked for every feasible row. Effective progress here excludes the separately added exposed communication; using an MFU measured over total step time would double-count communication.

The100/150GB/s rates are explicit illustrative effective per-device bandwidths, not measured A800/A100 throughput. They model the same2:3 ratio as the archived400/600GB/s NVLink aggregate specifications; directionality, topology and actual efficiency still require verification for a concrete layout. Exposed1/10/100GB per sequence is a sensitivity input, not derived collective traffic. H20 must be compared to the required effective rate using measured or explicitly assumed values, not an invented specification.

| Model | Cards | Ideal persistent GB/card | Required effective TFLOP/s/card, no exposed communication |
|---|---:|---:|---:|
| qwen3-8b | 16 | 9.215 | 179.399 |
| qwen3-8b | 32 | 4.607 | 89.700 |
| qwen3-8b | 64 | 2.304 | 44.850 |
| qwen3-8b | 128 | 1.152 | 22.425 |
| qwen3-235b-a22b | 16 | 264.480 | 403.308 |
| qwen3-235b-a22b | 32 | 132.240 | 201.654 |
| qwen3-235b-a22b | 64 | 66.120 | 100.827 |
| qwen3-235b-a22b | 128 | 33.060 | 50.413 |

results.json contains all64 conditions, including explicit communication-impossible cases. These are conditional thresholds and do not close10-4. Remaining work is to bind actual candidate layouts to per-card state/activation peaks and communication volume, compare matched-form A100/A800 with only the checked interconnect variable changed, and evaluate explicit H20 assumptions against those layouts. Source calculation files are read-only and unchanged.
