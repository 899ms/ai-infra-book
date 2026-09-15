# Budget × cache × queue measurement

Same controlled interval-repair task and six checks as the preserved original failed run. Qwen3-8B BF16 vLLM0.23, one running sequence, eager, APC enabled. Four settings: thinking cap100, thinking cap1000, thinking cap4096, no-thinking cap1000. Cap is total generated tokens, not an exact reasoning quota. Two repetitions of cache cold/warm ×queue idle/busy ×four settings,32 target requests; order shuffled seed1107.

Reset APC before every case and require reset success. Warm cases first submit the exact target prompt with one forced output token; count this separate preparation request/cost. Busy cases submit an unrelated background with128 forced tokens, wait for its first token, then submit the target while the background remains unfinished. Retain both request timelines and native scheduler metrics; max_num_seqs1 forces serialization. No background is sent to a different GPU.

Before running, the existing original record predicts cap100/1000 thinking will truncate and no-thinking will fail the six-check quality gate. Larger cap outcome is unknown. Cache saves only short prompt prefill (~157/161tokens); queued background can dominate it. These are estimates to test, not acceptance criteria.

Record actual prompt/output/reasoning-before-close token counts, native cached tokens, queue wait, first visible token, first post-thinking answer segment, total model+validation completion and first verified usable result (null on failure). Invalid, truncated or failed answers remain counted. All conditions use the same checker; no task edits in response to failures. No actual provider price is assigned. Later cost replay must declare teaching prices and include failed attempts and warmup separately.
