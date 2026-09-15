# 30B MoE model candidate

Completed 8 target requests on the fixed interval-repair task. 0 passed all six unchanged checks. Exact task messages, tokenizer IDs, emitted outputs, scheduler metrics, cache counters and validation records are retained. Every engine exited zero and the final GPU process list was empty.

| Thinking | Total cap | Warm cache | Background queue | Passes /2 | Median queue (s) | Median target+validation (s) | Output tokens |
|---|---:|---|---|---:|---:|---:|---|
| False | 1000 | False | False | 0 | 0.000022 | 14.117983 | [175, 175] |
| False | 1000 | False | True | 0 | 9.920864 | 24.318497 | [175, 175] |
| False | 1000 | True | False | 0 | 0.000016 | 14.968724 | [175, 175] |
| False | 1000 | True | True | 0 | 9.908169 | 23.844810 | [175, 175] |

All warm targets have positive native prefix-cache hits; cold targets have zero. For every busy case the background emitted its first token before target submission, remained unfinished then, and its last-token scheduler time precedes target scheduling. Native queue waits exceed0.1s. APC is reset before every case. Warmup and128-token background requests are separate records and must not be omitted from workload cost.

This text-only candidate is Qwen3-VL-30B-A3B-Instruct-FP8 at the recorded fixed revision, with its native tokenizer/template and no-thinking cap1000. It is a different architecture/precision, not an isolated parameter-count comparison. Task contents and checker are unchanged from the8B run.

First visible token and first post-thinking token segment are candidate latency metrics; neither proves usefulness. verified_usable_s is the completion of passing validation and stays null on failure. Two repetitions of one known task do not establish general model quality or production failure rates. No provider prices or monetary invoices are inferred here; declared-price routing belongs to the separate cost-routing report.

Run `python3 experiments/ch11/11-08/model-choice-moe/analyze.py` from the repository root. Its checks cover source identity, randomized order, case copies, cache/queue conditions, output count, unchanged six-test results and successful/failed usable-time semantics.
