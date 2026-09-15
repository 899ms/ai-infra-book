# Recovered samples consumed by durable optimizer steps

Twelve logical samples from the original Mac rollout experiment were consumed by12 independently initialized adapter-training steps on RTX PRO. Every checkpoint was atomically saved, file/directory fsynced, reloaded and checked before its token positions were counted as trained. A second verifier checked saved Adam moments against gradient norms and reconstructed the first B-matrix update.

| Token ledger | Count |
|---|---:|
| Originally sampled output tokens |3256|
| Manager-committed logical output positions |3000|
| Duplicate deliveries |256|
| Output positions covered by completed optimizer checkpoints |3000|
| Distinct prompt/output contents |2|
| Output positions across the two distinct contents |500|

The3000 positions belong to12 logical requests; they are not3000 distinct content tokens or12 independent tasks. Per-request generated, received, prefix-rebuilt and trained counts are in summary.json. Prefix rebuilding executes the model but is not counted as new output sampling.

Qwen3-8B BF16 revision b968826d9c46dd6066d109eabc6255188de91218 consumed the exact recovered IDs. Tokenizer decoding matched the original verified text. Generation used the previously documented Mac MLX4bit artifact; these precision/model artifacts differ. The base model was frozen, with32768 trainable rank4 parameters on final-layer q_proj. Each sample reset the adapter and AdamW, masked prompt labels and trained all output positions including EOS for one step.

Preparation took42.944747s; the training process window was44.106246s. Peak PyTorch CUDA allocation was17,496,262,656bytes. These are this consumer's measurements, not generation-to-training live-pipeline latency or a complete training run. Per-step timings include checkpoint verification and are retained separately.

All six sequence checkpoints have identical adapter tensor hashes. Extraction losses are identical across six paths, but their adapter tensors are not bitwise identical: the largest pairwise absolute difference is1.4551915228366852e-11, largest relative L2 difference1.1929374155172923e-10. Full pairwise results are preserved in checkpoint-comparison.json. No root cause is assigned from these observations, and bitwise training determinism is not claimed.

The training launcher exited zero and the final GPU compute-process list was empty. All raw events, checkpoints, model/source identities and GPU samples are retained. `export.py` independently reads immutable SQLite snapshots and verifies ordered output IDs against the earlier quality-checked results. `analyze.py` verifies the joined token ledger, checkpoint file hashes, source hashes, counts and lifecycle. The torch-based `verify_checkpoints.py` and `compare_checkpoints.py` run in the recorded RTX environment and also work with compatible CPU torch.

Scope: downstream supervised adapter consumption, not on-policy RL, reward improvement, full-model optimization or12 sequential training steps. The historical11-5 additional-resource expansion experiment remains open. The earlier cost-replay null training counts describe what was known then; this later consumption evidence must be joined explicitly rather than backdated into those observations.
