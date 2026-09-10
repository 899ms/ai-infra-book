# Concurrent four-client control

Reuse exact task generation and prior sequential off/on reference evidence. New off/on runs: same Qwen3-8B BF16 snapshot,2GiB KV,maxlen8192,chunk2048, but max_num_seqs=4. At each of three turns dispatch all four clients concurrently with asyncio.gather; wait for all four before next turn. Preserve actual per-client output in next history, no teacher forcing. Fixed off then on, each once; no quality retry, no production arrival model or performance ranking.

Save every request, full histories/token IDs/answers, engine metrics, all scheduler callbacks with active request set. Verify customer continuity and completed tasks. Compare prompts/outputs with sequential reference by ID; if changed, mark and do not call it an identical-prompt comparison. Record observed waiting/preemptions/peak usage, not inferred NIC/device traffic. Guard only own process tree.
