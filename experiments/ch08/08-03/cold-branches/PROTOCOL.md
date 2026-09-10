# Cold native four-branch admission

Same prompt/model/config/sampling/observer as sealed warmed branch-sharing. Fresh engine, no primer: n=4 then n=1 after completion, each128 outputs. Only remove primer; reuse complete warm trace rather than rerun. Track actual shared ownership across scheduling, first computed shared blocks and final release. A cold engine can form a shared prefix during execution; do not assume zero sharing. Parent cached-token output need not describe each child. No natural-quality/COW/performance claim.
