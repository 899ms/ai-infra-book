# 8B budget/cache/queue measurement

Completed 32 target requests on the fixed interval-repair task. 0 passed all six unchanged checks. Exact task messages, tokenizer IDs, emitted outputs, scheduler metrics, cache counters and validation records are retained. Every engine exited zero and the final GPU process list was empty.

| Thinking | Total cap | Warm cache | Background queue | Passes /2 | Median queue (s) | Median target+validation (s) | Output tokens |
|---|---:|---|---|---:|---:|---:|---|
| True | 100 | False | False | 0 | 0.000021 | 1.397568 | [100, 100] |
| True | 100 | False | True | 0 | 1.714225 | 3.184385 | [100, 100] |
| True | 100 | True | False | 0 | 0.000011 | 1.715033 | [100, 100] |
| True | 100 | True | True | 0 | 2.485185 | 4.405122 | [100, 100] |
| True | 1000 | False | False | 0 | 0.000017 | 16.999193 | [1000, 1000] |
| True | 1000 | False | True | 0 | 2.018926 | 18.079117 | [1000, 1000] |
| True | 1000 | True | False | 0 | 0.000016 | 18.214938 | [1000, 1000] |
| True | 1000 | True | True | 0 | 1.775925 | 21.325043 | [1000, 1000] |
| True | 4096 | False | False | 0 | 0.000016 | 51.325078 | [2524, 2524] |
| True | 4096 | False | True | 0 | 2.747733 | 52.465101 | [2524, 2524] |
| True | 4096 | True | False | 0 | 0.000013 | 22.328155 | [1326, 1326] |
| True | 4096 | True | True | 0 | 2.422748 | 29.731194 | [1326, 1326] |
| False | 1000 | False | False | 0 | 0.000015 | 1.879120 | [84, 84] |
| False | 1000 | False | True | 0 | 2.412940 | 4.133753 | [84, 84] |
| False | 1000 | True | False | 0 | 0.000015 | 1.130730 | [84, 84] |
| False | 1000 | True | True | 0 | 2.810698 | 4.705714 | [84, 84] |

All warm targets have positive native prefix-cache hits; cold targets have zero. For every busy case the background emitted its first token before target submission, remained unfinished then, and its last-token scheduler time precedes target scheduling. Native queue waits exceed0.1s. APC is reset before every case. Warmup and128-token background requests are separate records and must not be omitted from workload cost.

The100/1000 thinking caps are total generated-token limits, not independent thinking quotas. Increasing the cap to4096 lets answers finish in this dataset but does not fix the full task. Cold and warm large-budget outputs differ in both length and code, so their full latency difference cannot be interpreted as an isolated prefill speedup. Earlier failed runs are preserved in the parent report.

First visible token and first post-thinking token segment are candidate latency metrics; neither proves usefulness. verified_usable_s is the completion of passing validation and stays null on failure. Two repetitions of one known task do not establish general model quality or production failure rates. No provider prices or monetary invoices are inferred here; declared-price routing belongs to the separate cost-routing report.

Run `python3 experiments/ch11/11-08/cache-queue/analyze.py` from the repository root. Its checks cover source identity, randomized order, case copies, cache/queue conditions, output count, unchanged six-test results and successful/failed usable-time semantics.
