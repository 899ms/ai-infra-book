import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parent;s=json.loads((R/'results.json').read_text());feedback=json.loads((P/'feedback-route/summary.json').read_text())
t=f'''# Bounded feedback route

Eight logical tasks completed, with {feedback['generation_attempts']} actual target generation attempts. First-attempt successes: {feedback['initial_successes']}; final successes: {feedback['successes']}. Every task retains the initial candidate, its actual validation results, the feedback prompt IDs and final candidate. The same specification and six checks are used; the feedback budget is one additional attempt only.

All warm/cold first-attempt cache conditions and background queue conditions passed verification. The second attempt reuses conversation prefixes, so its cache hits are not mislabeled as the initial case's cold-cache result. Total verified-usable latency starts with the first attempt and remains null on final failure. Both attempts are charged in the separate declared-price replay.

The engine and launcher exited zero and the GPU process list was empty. These are repeated trials on one known task, not independent task-quality samples. Run `python3 experiments/ch11/11-08/feedback-route/analyze.py` to verify source identity, order, both candidates, actual checks, cache/queue conditions and complete-route timing.
'''
(P/'feedback-route/README.md').write_text(t)
t='''# Historical11-7: budgets, cache, queue and quality-constrained cost

The complete measured candidate set contains48 logical task evaluations:32 Qwen3-8B budget/cache/queue cases, eight one-shot Qwen3-VL-30B-A3B-Instruct-FP8 cases, and eight bounded two-attempt feedback cases. The latter adds16 actual target calls. All cases use the same repair specification and six acceptance checks. **No candidate passed the full gate.** This is a negative experimental result; it does not imply those models fail other tasks.

The recipe set was expanded after earlier failures; this is a documented exploratory experiment, not a blind model benchmark. Routing decisions use repetition0 only and are evaluated on repetition1 for the same known task and cache/queue state. Repetitions are not held-out tasks.

## Declared prices and decisions

Teaching prices per million input/cached/output tokens are0.1/0.025/0.3 for8B and0.4/0.1/1.2 for both MoE recipes. These are explicit estimates, not provider prices, bills or current market recommendations. Reasoning tokens are included once in generated-output charges. Target, warmup and background costs are recorded separately; failed attempts are charged. Validation compute, model initialization, taxes and other fees are unpriced.

| Policy | Evaluated requests | No feasible-route states | Successes | Observed failure fraction | Teaching evaluation spend | Teaching cost per success |
|---|---:|---:|---:|---|---:|---|
'''
for a in s['aggregate']:t+=f'| {a["policy"]} | {a["evaluated_attempts"]} | {a["no_route_states"]} | {a["successes"]} | {a["failure_rate"]} | {a["teaching_spent"]:.8f} | Undefined: zero successes |\n'
t+=f'\nCalibration target+warmup acquisition costs {s["calibration_dataset_target_plus_warmup_cost"]:.8f} teaching units. All recorded target+warmup usage costs {s["all_recorded_target_plus_warmup_cost"]:.8f}, with background load another {s["all_recorded_background_cost"]:.8f}. These acquisition totals are separate from policy evaluation spend; abstention is not a claim that collecting the evidence was free.\n'
t+='''
Fixed routing chooses8B thinking/cap1000. Lowest output-token price ties choose8B no-thinking/cap1000 by the preregistered order. Both evaluated choices fail every state. The quality-constrained rule admits only recipes that passed all six checks during calibration; none do, so it issues no evaluation request in all four states. It has no successful completion cost or failure fraction over issued requests. Its behavior is abstention, not a zero-cost successful answer.

First visible token, first post-thinking candidate segment, model+validation completion and verified-usable latency are retained for every case. All verified-usable fields are null because quality never passed. A quick first token or natural model stop is not a successful result.

## Two requested hand calculations

For100 versus1000 reasoning tokens while answer length and all other usage stay fixed, the extra900 tokens cost0.00027 teaching units at the8B output rate, or0.00108 at the MoE rate. This is the marginal arithmetic example, not the measured total-generation-cap intervention. Actual100/1000 thinking-cap outputs truncate; the4096 cap produces longer completed candidates that still fail. Actual reasoning-before-close counts are stored rather than assumed equal to the cap.

For a cache hit behind a queue, use observed native queue plus measured complete latency. The JSON includes12 same-recipe/repetition warm-busy versus cold-idle comparisons. For example,8B no-thinking median cold-idle completion is1.879s, while warm-busy is4.706s despite160 cached tokens. Native warm-busy median queue is2.811s. This illustrates how queueing can outweigh short-prompt reuse; it is not a pure cache-effect estimate. Larger-thinking-budget outputs differ across cache states, so generation changes also affect their times.

Both examples explain why the cheapest token unit or highest cache hit is not by itself a feasible quality-constrained choice. Under these measured candidates, no cost/routing rule can manufacture a passing result. More retries, revised prompts or other models would be a new experiment and are not silently introduced into the final comparison.

## Verification and limits

Run `python3 experiments/ch11/11-08/cost-routing/run.py` and `python3 experiments/ch11/11-08/cost-routing/verify.py` from repository root. Underlying reports: [8B measurements](../cache-queue/README.md), [MoE candidate](../model-choice-moe/README.md), [bounded feedback](../feedback-route/README.md). Source hashes,48 logical records, calibration/evaluation split,12 decisions, failed-attempt charges and marginal arithmetic are checked. All GPU runs are terminal and their cleanup records are retained.

The original question's estimate-then-offline-replay scope is complete. Real billed costs remain unknown because this is local hardware with declared token-price scenarios; observed zero-success denominators remain undefined for mathematical reasons. Neither is replaced with a fabricated number. No production SLA, general failure-rate estimate or model-quality ranking is asserted.
'''
t+='\n![Measured cases and separate assumed crossover](comparison.svg)\n\n[PDF figure](comparison.pdf). The shaded panel reuses the current calculations/results/routing-cost-book.json assumptions:79.5249% cost crossover and91.8367% joint deadline threshold. It is not a measured API/model result. Figure source hashes are in plot-sources.json; SVG/PDF/PNG exported and PNG visually checked.\n'
(R/'README.md').write_text(t)
for d in [P/'feedback-route',R]:
 files=[p for p in d.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts]
 (d/'manifest.json').write_text(json.dumps({str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},indent=2)+'\n')
