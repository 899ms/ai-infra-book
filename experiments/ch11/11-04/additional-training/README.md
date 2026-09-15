# Raw new-batch training

All12 new logical samples completed independent one-step adapter checkpoints: 3141 output positions across 3 distinct prompt/output streams (789 distinct-content output positions). Source hashes, finite gradients, actual parameter changes, fsync/reload, saved Adam moments and first-step updates were verified. The launcher exited zero with an empty GPU compute-process list.

This pass trains the actual received streams, including289-token RTX extractions versus242-token Mac extractions. No original checkpoint is relabeled. The canonical pass is separately retained for comparing identical effective training data. Do not add the two alternative passes as if they were one required pipeline.

Consumer preparation: 38.641187s; process window: 39.764563s. Per-sample step/checkpoint timings and provenance are in summary.json. The model is fixed Qwen3-8B BF16 with a rank4 final-q_proj adapter, reset for every sample. This is supervised consumption, not on-policy RL,12 sequential steps or demonstrated quality improvement.

Recheck from repository root with `python3 experiments/ch11/11-04/additional-training/analyze.py`. The independent checkpoint verifier uses compatible torch and is recorded in verify_checkpoints.py.
