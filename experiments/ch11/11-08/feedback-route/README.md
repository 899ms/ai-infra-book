# Bounded feedback route

Eight logical tasks completed, with 16 actual target generation attempts. First-attempt successes: 0; final successes: 0. Every task retains the initial candidate, its actual validation results, the feedback prompt IDs and final candidate. The same specification and six checks are used; the feedback budget is one additional attempt only.

All warm/cold first-attempt cache conditions and background queue conditions passed verification. The second attempt reuses conversation prefixes, so its cache hits are not mislabeled as the initial case's cold-cache result. Total verified-usable latency starts with the first attempt and remains null on final failure. Both attempts are charged in the separate declared-price replay.

The engine and launcher exited zero and the GPU process list was empty. These are repeated trials on one known task, not independent task-quality samples. Run `python3 experiments/ch11/11-08/feedback-route/analyze.py` to verify source identity, order, both candidates, actual checks, cache/queue conditions and complete-route timing.
