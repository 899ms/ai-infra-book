# Four-client three-turn control

Four fixed 512-record documents, seeds302900..302903. Three disjoint three-key queries per client, round-robin sequential dispatch. Every next turn contains that client's actual prior model answers, not expected/teacher-forced answers. No tool think-time or production arrival claim.

One engine per APC off/on, fixed off then on, 12 requests each. Same BF16 Qwen3-8B snapshot,2GiBKV,maxlen8192,chunk2048,eager,maxseq1,temperature0,maxoutput128,thinkingdisabled. Save full histories/tokenIDs/answers/metrics/cachehits/scheduler state. Validate strict answers and per-client continuity; compare prompt equality between modes before interpreting cache and times. No failed-quality retry. No throughput or causal latency ranking from this one fixed-order pair. Public ServeGen anonymous IDs are not reconstructed into real token histories.
