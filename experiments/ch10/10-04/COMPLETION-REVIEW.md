# Historical10-4 completion review

Complete as an explicitly conditional calculation and negative deadline result, as allowed by the original requirement. No matched A100/A800/H20 training run is claimed.

The frozen requirement asks for Qwen3-8B and Qwen3-235B candidate partitions; a same-form A100/A800 comparison changing checked interconnect conditions; H20 training-step evidence **or explicitly assumed effective performance**; capacity/compute/interconnect regimes; and thresholds that change the decision. It permits calculation/public records. Requiring new matched raw training runs in every case was stricter than that wording.

| Requirement | Evidence | Finding |
|---|---|---|
| Both concrete Qwen candidates | candidate-layouts configs, exact per-stage parameters and existing shape-derived matrix work | Eight PP-only GPipe candidates; embedding/head placement, checkpoint storage, recomputation and every boundary message explicitly counted. TP/DP/EP1 avoids unmodeled expert collectives. |
| Same-form A100/A800 comparison | Archived80GB SXM specification texts; scheduled-comparison96 cases | Same candidate/work/effective compute/capacity/topology, local effective link150→100GB/s in the checked600:400 aggregate-specification ratio. Effective rates are declared assumptions, not measured link rates. |
| H20 comparison | Explicit50/100/150 effective matrix TFLOP/s and96GB capacity scenarios | Permitted assumed-performance route. No inference throughput, LoRA screenshot or unknown H20 specification is substituted for measured full training. |
| Capacity regime | Per-stage18byte parameter state, retained checkpoints, two extra boundary buffers, remaining workspace allowances | Several candidates exceed capacity before temporary workspace. Positive remaining allowance is not claimed to prove a full implementation fits. |
| Compute and communication regimes | Resource/DAG-verified289920 events, concrete link/fabric payloads and deadline-proof resource lower bounds | Independent links and eight-rank-node shared25GB/s fabric are explicit topology cases. Communication is scheduled, not blindly added across links or counted twice through total-step MFU. |
| Deadline and decision thresholds |64 initial sensitivity cases,96 schedules,8 exact optimistic deadline proofs | All selected100B-token/30-day candidates fail even at312TF/card with zero communication/other overhead. Necessary effective rates493.619–1393.628TF/card exceed that ideal ceiling; H20's declared rates fail too. |
| Explain when choices change | deadline-proof tables and formulas | Workspace must stay below per-candidate headroom; compute must exceed the necessary rate; each link/shared fabric must meet payload/deadline. Passing separate bounds is not sufficient. Changed task, schedule, layout or hardware needs a new comparison. |

The final negative proof resolves the earlier remaining-work concern: omitted nonnegative costs or additional workspace cannot make a rejected deadline feasible. It is unnecessary to invent or measure every omitted cost to establish this rejection. This does not turn matrix-only durations into complete-step forecasts or establish memory feasibility for the positive-headroom candidates.

Validation: stage parameter/work totals exactly match the archived calculations; transfer byte conservation holds;96 schedules verify dependencies, resource exclusion and durations; the communication-free critical-path formula matches an independent integer dynamic-programming grid for all8 candidates. The comparative plot was visually inspected with legends outside the data. Original calculations were not modified. Source identities and manifests accompany each artifact.

The result is bounded to the chosen candidates, sequences,100B tokens,30days,GPipe and checkpoint policy. It does not prove that no other parallelization could meet30days or compare training quality after changing batch size. Public-source omissions remain valid findings in the original report. Hardware measurements would extend this result, but are not required to complete the explicitly allowed calculation route.
