# Historical11-7 completion review

Original scope: estimate first, then offline replay using records with actual usage fields; no fabricated measurements. This review closes the experiment as a negative result, not as a claim that any candidate achieved a usable repair.

| Requirement | Evidence and interpretation |
|---|---|
| Actual usage and versions | cache-queue, model-choice-moe and feedback-route retain prompt/output IDs, generated-token counts, thinking-close position, cache counters, vLLM/Torch/model revision and source hashes. |
| Change reasoning budget |8B thinking total caps100/1000/4096 and no-thinking1000; actual reasoning tokens separately recorded. Total cap is explicitly not an independent reasoning quota. |
| Cache hit and backend queue | Cold/warm APC ×idle/actual128-token background. Cache reset/warmup and native queued/scheduled metrics verify each condition, including cache hits while waiting. |
| Model/recipe candidates | Fixed8B BF16 and cached30B MoE FP8, with the same task/checker; additionally a bounded two-attempt feedback route. Distinct architectures/templates and exploratory selection are disclosed. |
| Fixed, lowest unit-price and quality-constrained routing | cost-routing uses declared prices, fixed tie rules and repetition0 calibration/repetition1 evaluation across four cache/queue states. No passing calibrated recipe means abstention in all states, not fabricated success. |
| Success cost, first usable time, completion and failure | All48 logical tasks fail the unchanged six-check gate. Failed costs remain charged; cost per success and verified-usable time are undefined/null because the success denominator is zero. First visible/candidate tokens and actual target+validation completion remain recorded. No general quality inference from one known task. |
|100 versus1000 thinking tokens | Fixed-answer marginal900-token arithmetic is reported separately from measured total-cap interventions, with reasoning charged once. |
| Cache hit but queued hand example | Native queue plus full measured completion and12 recipe/repetition cold-idle versus warm-busy comparisons; output changes are retained, not attributed solely to cache savings. |
| SVG/PDF cost/time, reasoning/cache/queue and assumed crossing/deadline | cost-routing/comparison.svg and comparison.pdf show measured negative results in three panels and the existing book assumptions in a clearly separate panel. Current calculation artifact is read-only and source-hashed; crossing79.5249%, deadline threshold91.8367%. PNG visually checked. |

Three GPU jobs completed and cleaned up. The48 logical evaluations contain56 target model calls, plus24 warmup and24 background calls. Underlying analyzers verify outputs, both feedback attempts, tests and native scheduling evidence. Cost verifier checks source identity, repetition split, twelve decisions and zero-success semantics. These are declared teaching price estimates, not provider bills; calibration/background acquisition cost is separately retained.

Historical11-7 is delivered in its estimate/offline-replay scope. No positive quality result, real invoice, production SLA or broad model ranking is claimed. Further models or retries would be a new preregistered experiment rather than rewriting this candidate set until it passes.
