# Native branch sharing

Fixed 1536-token synthetic prompt, Qwen3-8B BF16, APC enabled,1GiBKV,maxlen2048,maxseq4,chunk512,eager. Three sequential calls: one128-token primer, native n=4 temperature0.8/seed803 128-token branches, one128-token post-completion reuse. Six sequences, forced length; no natural task-quality claim.

Use existing read-only ObservedScheduler. Inspect actual block identities and refcounts with overlapping owners; private tail versus shared completed prompt blocks; final requests removed and blocks returned to free list. Cached content can remain in free blocks. Do not assume copy-on-write occurred: no copy claim without an observed copy. Guard own processes only, output directory refuses overwrite.

The initial greedy n=4 parameter combination was rejected by native SamplingParams after primer; final configuration uses supported seeded sampling. Output identity is observed, not required for branch ownership validation.
