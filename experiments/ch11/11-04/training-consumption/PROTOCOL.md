# Recovered rollout → durable training consumption

Use all12 formal logical request snapshots, including baseline/restart/preserve and both cut positions for two tasks. The dataset has3000 logical output positions but only two distinct prompt/output contents (500 output positions); do not call them12 independent tasks. Source SHA, seq order, EOS and exact token identities are retained.

On RTX PRO load fixed Qwen3-8B BF16 revision b968826d9c46dd6066d109eabc6255188de91218. Generation was Mac MLX4bit revision383413e909f3bc5303ce195ebbdf0339c5a1a2a3; these are explicitly different precision/model artifacts. Tokenizer must decode the exact stored IDs identically to the verified source text. This is downstream supervised adapter consumption of recovered samples, not on-policy RL or proof of reward improvement.

Freeze base weights. Add rank4 LoRA to the last layer q_proj, scale1, seed1105, A normal std0.01/B zero. For each logical sample reset adapter and AdamW to the identical initial state, compute causal cross-entropy on output tokens including EOS with prompt labels masked, backward and one optimizer step at learning rate0.001. Require finite loss/gradients, nonzero adapter update and exact number of active output labels. Save adapter+optimizer+sample identity atomically, fsync file and directory, reload and verify tensor equality and step1. Only then mark that sample's output positions completed_training_tokens. This verifies12 independent one-step checkpoints, not a12-step sequential trajectory or full-model training.

Record preparation, forward/backward/update/checkpoint times and actual allocated window separately. One GPU process, no simultaneous experiments. Preserve raw failures and do not infer completion from loss calculation alone.
