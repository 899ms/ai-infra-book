# Cross-Mac KV recovery: verified

A fresh Qwen3-8B BF16 SGLang producer on RTX PRO published 65 KV pages to the local Mac. A separate fresh consumer fetched 64 pages (144 MiB of KV data) through HTTP over SSH reverse forwarding. Both engines returned three responses; all six generated token sequences were identical, with zero retractions. The first consumer response reported 1008 storage-cache tokens and zero device/host-cache tokens. Subsequent responses reported 1008 device-cache tokens.

| Request | Complete request time |
|---|---:|
| Producer cold | 1.825171 s |
| Producer warm, two requests | 0.213614 / 0.186027 s |
| Fresh consumer, remote recovery | 82.641923 s |
| Consumer warm, two requests | 0.343936 / 0.306595 s |

Remote recovery was substantially slower than the cold producer request in this run. The 64 GET RPCs totaled 45.664344 s and 151,015,360 HTTP payload bytes including framing/metadata. Their median was 0.645103 s and nearest-rank p95 1.021702 s. This is page-RPC latency within one recovery, not independent request p95; complete recovery also includes existence checks and model work. These observations do not establish a production routing policy or representative network performance.

All fetched hashes and published file sizes were independently verified. The first-write-wins store retained one conflicting duplicate payload for a key outside the fetched set; it was saved under mac-store/collisions and its hash was checked. Output equality does not establish bitwise equivalence of all computed KV pages.

The remote launcher and SSH command exited zero, GPU compute-process listing was empty after both engines, and the local Mac HTTP store was terminated and waited. Source hashes, request responses, client RPC timings, server ledger, GPU samples and transport command are retained. Earlier failed cross-Mac attempts remain in the parent directory.

Recheck with `python3 experiments/ch09/09-09/remote-kv/cross-mac-005/analyze.py`. This closes the basic cross-Mac recovery feasibility gap. The original multi-turn Chat/Agent remote-cache routing comparison remains unfinished. Docker on RTX remains the substitute for E2B in sandbox experiments; this page store is deliberately on the Mac to exercise an actual inter-host connection.
