# Concrete PP candidate memory and transfers

Eight candidates place every parameter of the pinned Qwen3-8B and Qwen3-235B configurations. This is a conditional analytical comparison, not a claim that these high-PP layouts have run or are efficient. All ranks have TP=DP=EP=1. Qwen8 uses PP4/8; Qwen235 uses PP47/94. Keeping whole transformer layers and all experts on their owning stage avoids an invented perfectly even parameter split or unmodeled expert all-to-all. Contiguous layer counts differ by at most one. Embedding belongs to the first rank; separate LM head and final norm to the last.

The selected schedule is full fill/drain GPipe,8 or32 microbatches,one sequence per microbatch. Training state is18bytes/parameter. Retained layer-input checkpoints are BF16 and kept for every microbatch through forward fill. Each layer is recomputed during backward, so its forward matrix work is charged again. Two extra full BF16 boundary receive buffers per rank are conservatively counted without aliasing. This changes the earlier no-recompute matrix-work budget; it must not be priced as free memory savings.

| Model | PP | Microbatches | Peak accounted GB | Minimum unaccounted workspace headroom,80GB | Same,96GB |
|---|---:|---:|---:|---:|---:|
| qwen3-8b | 4 | 8 | 62.324 | 17.676 | 33.676 |
| qwen3-8b | 4 | 32 | 120.306 | -40.306 | -24.306 |
| qwen3-8b | 8 | 8 | 39.841 | 40.159 | 56.159 |
| qwen3-8b | 8 | 32 | 72.054 | 7.946 | 23.946 |
| qwen3-235b-a22b | 47 | 8 | 101.969 | -21.969 | -5.969 |
| qwen3-235b-a22b | 47 | 32 | 105.190 | -25.190 | -9.190 |
| qwen3-235b-a22b | 94 | 8 | 56.653 | 23.347 | 39.347 |
| qwen3-235b-a22b | 94 | 32 | 58.263 | 21.737 | 37.737 |

A negative headroom rejects the candidate even before temporary workspace. A positive value is the maximum remaining allowance, not a proof of fit: recomputation intermediates, attention kernels, logits/loss, optimizer workspace, allocator fragmentation and framework allocations are unbounded here. Full memory feasibility therefore remains unproven.

Per link, each microbatch sends one BF16 `[tokens,4096]` forward activation and one same-shaped BF16 gradient backward. The rank list and every link's bytes are saved. For Qwen8's32768-token sequence each message is268435456bytes; for Qwen235's8192-token sequence it is67108864bytes. No DP collective is implied by DP1; no expert traffic crosses stages under EP1. Summing all links is network work, not elapsed time: stage dependencies, overlapping links and topology must be scheduled before bandwidth produces a completion time. Boundary gradient dtype is an explicit BF16 activation-gradient assumption, independent of FP32 parameter-gradient storage.

Exact parameter totals agree with the prior archived model calculations, and all stage work/state sums and forward/backward transfer identities are checked. Calculation sources are only read. Run `python run.py` to reproduce. Remaining10-4 work is the memory-workspace bound and a schedule/topology-based matched A100/A800 comparison with explicit H20 effective-performance assumptions; this partial result does not close the exercise.
