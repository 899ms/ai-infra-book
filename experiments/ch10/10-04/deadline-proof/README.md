# Deadline rejection without inventing missing overhead

For each selected candidate, the communication-free GPipe makespan in units of matrix work is:

`sum(F_stage)+sum(B_stage)+(microbatches−1)*(max(F_stage)+max(B_stage))`.

All jobs have the same per-stage matrix work; the forward fill barrier precedes backward drain. A separate integer dynamic-programming grid reproduces this closed form exactly for all eight candidates. Backward work includes the declared layer recomputation. Dividing by a uniform effective matrix rate gives the optimistic step time. Communication, nonmatrix operations, loss, optimizer, data, checkpointing, outages and allocation costs are all set to zero for this proof. A whole final batch is charged as in the schedule runner.

The archived A10080GB and A80080GB SXM specification text lists312TFLOP/s BF16 dense (624 is structured-sparse). Using312 as an ideal100%-of-peak rate makes this an optimistic lower bound, not a prediction of achievable training speed. It is not used as an H20 specification. The earlier explicit H20 assumptions50/100/150TFLOP/s are below this ceiling and also fail these deadlines.

| Model | PP | Microbatches | Optimistic days at312TF/card | Necessary TF/card for30days, even without communication | Workspace headroom80GB | Workspace headroom96GB |
|---|---:|---:|---:|---:|---:|---:|
| qwen3-8b | 4 | 8 | 134.003 | 1393.628 | 17.676GB | 33.676GB |
| qwen3-8b | 4 | 32 | 109.427 | 1138.040 | -40.306GB | -24.306GB |
| qwen3-8b | 8 | 8 | 91.525 | 951.861 | 40.159GB | 56.159GB |
| qwen3-8b | 8 | 32 | 62.398 | 648.938 | 7.946GB | 23.946GB |
| qwen3-235b-a22b | 47 | 8 | 130.013 | 1352.139 | -21.969GB | -5.969GB |
| qwen3-235b-a22b | 47 | 32 | 55.799 | 580.310 | -25.190GB | -9.190GB |
| qwen3-235b-a22b | 94 | 8 | 122.484 | 1273.837 | 23.347GB | 39.347GB |
| qwen3-235b-a22b | 94 | 32 | 47.463 | 493.619 | 21.737GB | 37.737GB |

Every candidate fails100B tokens/30days under these conditions. Therefore measuring omitted nonnegative overhead or temporary workspace cannot turn one of them into a deadline-feasible choice. Positive workspace headroom remains only a conditional memory allowance; this proof does not call such candidates memory-feasible. Negative headroom already rules out capacity before temporary allocations.

These results describe the selected PP-only candidates and GPipe policy, not every possible training design. More GPUs, different parallelism, a different microbatch/schedule choice, shorter task, or a relaxed deadline can change the answer and must be recalculated. No claim is made that Qwen training generally requires these particular PP counts.

## What can change a choice

Capacity changes when unaccounted peak workspace crosses the per-candidate headroom above; negative headroom cannot be repaired by a faster interconnect. The compute deadline threshold is the necessary effective rate in the table; actual required rates including omitted work cannot be smaller. Link/fabric lower bounds are also saved: each physical resource must transmit its counted payload within30days, so `payload/deadline` is a necessary bandwidth. Shared cross-node traffic is counted across every crossing, rather than giving each transfer a full independent fabric. Passing these separate necessary tests is not sufficient for a full schedule.

The scheduled-comparison artifact already holds compute, capacity, work, topology and policy fixed between A100/A800 and changes only the declared2:3 effective local-link rate. In the measured-work analytical candidates, matrix work and the long GPipe fill/drain dominate that particular link-rate change. This is a result of the declared candidates, not a claim that interconnect never dominates training. As compute grows faster, payload grows, bandwidth shrinks or more boundaries share the fabric, the link resource bound becomes limiting.

This closes the negative deadline decision for the selected candidates without requiring fabricated complete-step measurements. It does not replace the original source-review finding that matched actual A100/A800/H20 Qwen training traces are absent.
