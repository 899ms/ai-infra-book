# Historical experiment 9-9 completion review

The original requirement in archive/outlines/09-分布式推理.md allows calculation / real system records and makes multiple deployed instances optional. Completion below is within that stated scope, not a claim of a production remote-routing system.

| Original requirement | Authoritative evidence | Coverage / limit |
|---|---|---|
| Multi-turn Chat and Agent records | chat-replay/results/prompts.json; router-lifecycle/agent-prompts.json; remote-kv/trace-inputs.json and source hashes | Four Chat and twelve Agent inputs; fixed recorded contexts. Chat originally has arithmetic errors and Agent originally failed; no quality improvement claimed. |
| Cache tokens and reuse intervals | Existing Chat/Agent response records; remote-kv/cross-mac-traces-001/summary.json and threshold16 counterpart | Native counters, per-turn start/end and interval since previous response. Remote intervals include publication barriers, not original human/tool delays. |
| Queue observations | queue-pressure/summary.json and raw load samples; policy-comparison results | Two live workers, sampled waiting counts and actual residual times. Remote replay explicitly transplants these residuals as scenarios. |
| Remote retrieval cost | remote-kv/cross-mac-005; cross-mac-traces-001; cross-mac-chat-threshold16-001 | Actual Mac–RTX page transfer, native storage counters, complete returned outputs, hashed pages and terminal cleanup. Default threshold suppresses short Chat fetches; sensitivity run admits them. |
| Queue-first, cache-first, predicted-completion comparison | policy-comparison/README.md and summary.json; remote-kv/routing-record-replay/README.md and results.json | Earlier live18-group comparison plus1152 independent remote-aware record scenarios. The latter is calculation, not a new live concurrent deployment. |
| Request- and token-weighted hits | Existing native-router/Chat summaries; both multi-turn remote summaries; routing replay summary | Both denominators and selected device/host/storage totals retained. |
| Hit levels and p95 retrieval | Remote summaries' native levels and per-request GET sums; page RPCs in raw remote.jsonl | Descriptive nearest-rank sample p95, explicitly excluding exists checks and model work. No stable production p95 inference from small samples. |

Additional previously documented lifecycle gaps also have actual evidence in eviction-restart and router-lifecycle: natural capacity pressure, cold restarted worker, health failure/recovery and native routing observations. They are not inferred from explicit flush alone.

The matched recomputation control completed48 zero-hit requests in three shuffled passes, with identical output tokens to remote requests. The remote comparison verifier checks all1152 unique scenarios, calibrated decision rules, source hashes and aggregation. It preserves estimation errors rather than selecting an oracle policy after seeing realized service.

Historical9-9 is delivered in its original calculation / real-record scope. A live distributed remote-aware router, full task-quality evaluation, concurrent GPU-interference model and statistically established production SLO remain outside what these results establish. Those limitations must accompany use of the results; they are not silently treated as measured outcomes.
