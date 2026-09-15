# Conditional cost boundaries for historical10-10

72 A100/H100/B200 cases and72 pairwise price boundaries were calculated from the archived Qwen8/Qwen235 and1T/5T/10T Dense cases. The exact rational checks establish equal modeled cost at every boundary. Original calculation files are only read; no rental price, invoice or quality result is invented.

Let H be modeled compute GPU-hours, G the necessary card count and d the deadline days. Immediate release after modeled computation costs `p*H`; reserving all G cards through the deadline costs `p*G*d*24`. For two devices A/B, B costs less iff `p_B/p_A < H_A/H_B` in the first convention, or below the reserved-hour ratio in the second. Currency, task, precision, quality and included charges must agree. These are conditions, not a recommendation that the aggregate lower-bound card counts form a feasible cluster.

| Task | MFU/effectiveness | Deadline days | Pair A→B | Break-even B/A price, compute-only | Same, full-deadline reservation |
|---|---|---:|---|---:|---:|
| dense-10T | 2/5 | 90 | a100-80gb-sxm → h100-sxm | 3.171154 | 3.171154 |
| dense-10T | 2/5 | 90 | a100-80gb-sxm → b200-sxm | 7.211538 | 7.211532 |
| dense-10T | 2/5 | 90 | h100-sxm → b200-sxm | 2.274106 | 2.274104 |
| dense-10T | 2/5 | 180 | a100-80gb-sxm → h100-sxm | 3.171154 | 3.171156 |
| dense-10T | 2/5 | 180 | a100-80gb-sxm → b200-sxm | 7.211538 | 7.211538 |
| dense-10T | 2/5 | 180 | h100-sxm → b200-sxm | 2.274106 | 2.274104 |
| dense-1T | 2/5 | 90 | a100-80gb-sxm → h100-sxm | 3.171154 | 3.171129 |
| dense-1T | 2/5 | 90 | a100-80gb-sxm → b200-sxm | 7.211538 | 7.211466 |
| dense-1T | 2/5 | 90 | h100-sxm → b200-sxm | 2.274106 | 2.274100 |
| dense-1T | 2/5 | 180 | a100-80gb-sxm → h100-sxm | 3.171154 | 3.171155 |
| dense-1T | 2/5 | 180 | a100-80gb-sxm → b200-sxm | 7.211538 | 7.211103 |
| dense-1T | 2/5 | 180 | h100-sxm → b200-sxm | 2.274106 | 2.273968 |
| dense-5T | 2/5 | 90 | a100-80gb-sxm → h100-sxm | 3.171154 | 3.171156 |
| dense-5T | 2/5 | 90 | a100-80gb-sxm → b200-sxm | 7.211538 | 7.211538 |
| dense-5T | 2/5 | 90 | h100-sxm → b200-sxm | 2.274106 | 2.274104 |
| dense-5T | 2/5 | 180 | a100-80gb-sxm → h100-sxm | 3.171154 | 3.171156 |
| dense-5T | 2/5 | 180 | a100-80gb-sxm → b200-sxm | 7.211538 | 7.211538 |
| dense-5T | 2/5 | 180 | h100-sxm → b200-sxm | 2.274106 | 2.274104 |
| qwen3-235b-a22b | 2/5 | 30 | a100-80gb-sxm → h100-sxm | 3.171154 | 1.083333 |
| qwen3-235b-a22b | 2/5 | 30 | a100-80gb-sxm → b200-sxm | 7.211538 | 2.476190 |
| qwen3-235b-a22b | 2/5 | 30 | h100-sxm → b200-sxm | 2.274106 | 2.285714 |
| qwen3-8b | 2/5 | 30 | a100-80gb-sxm → h100-sxm | 3.171154 | 2.833333 |
| qwen3-8b | 2/5 | 30 | a100-80gb-sxm → b200-sxm | 7.211538 | 5.666667 |
| qwen3-8b | 2/5 | 30 | h100-sxm → b200-sxm | 2.274106 | 2.000000 |

All30%/40%/50% cases remain in results.json; this table shows40%. The fixed task's ideal compute GPU-hours are independent of card count in this linear model. Capacity floors and integer card rounding can change the reservation ratio considerably, especially for Qwen235: a faster device may sit idle within a fixed reservation. A real scheduler's release behavior determines which accounting applies.

Preparation, data stalls, checkpoint pauses, restart and lost work are not silently set to zero in an actual bill. If not already included in the efficiency denominator, their allocated GPU-hours and other costs must be added using allocation intervals; after recovery, only newly completed work is credited. Existing public-training records demonstrate why cumulative tokens cannot be divided by one resumed run's duration. Actual resource intervals, prices and non-GPU costs remain unknown here.

Quality acceptance and complete per-card layout feasibility remain null in every row. A finite arithmetic price boundary is not a quality-qualified cost frontier. No V4 row is substituted with V3 or dense6ND: the matching full V4 training task/work and quality/calibration evidence still need explicit treatment. This artifact completes the conditional price algebra for the available tasks; it does not close historical10-10.
