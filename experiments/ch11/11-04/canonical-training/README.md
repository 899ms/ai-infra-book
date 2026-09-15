# Canonical new-batch training

All12 new logical samples completed independent one-step adapter checkpoints: 3000 output positions across 2 distinct prompt/output streams (500 distinct-content output positions). Source hashes, finite gradients, actual parameter changes, fsync/reload, saved Adam moments and first-step updates were verified. The launcher exited zero with an empty GPU compute-process list.

This is an explicit normalization pass. All accepted JSON contents first match their original task baseline; the fixed baseline serialization supplies canonical output IDs. Exact prompt/output SHA sets match the original training-consumption dataset. normalization.json preserves raw3141→canonical3000 position counts and all identities. RTX formatting tokens were generated and received, but are not part of this canonical training stream. This pass has new checkpoints and is a separate alternative to raw training, not an additional stage charged to that pipeline.

Consumer preparation: 39.928758s; process window: 41.516994s. Per-sample step/checkpoint timings and provenance are in summary.json. The model is fixed Qwen3-8B BF16 with a rank4 final-q_proj adapter, reset for every sample. This is supervised consumption, not on-policy RL,12 sequential steps or demonstrated quality improvement.

Recheck from repository root with `python3 experiments/ch11/11-04/canonical-training/analyze.py`. The independent checkpoint verifier uses compatible torch and is recorded in verify_checkpoints.py.
