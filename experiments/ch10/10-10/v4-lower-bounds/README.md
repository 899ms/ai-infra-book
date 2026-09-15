# V4-Flash resource lower bounds and missing training coverage

The archived MoE calculation covers a128-token fixed-selection main-loss forward/backward path with router scores, shared expert and routed experts. Repeating this architectural component across43 main layers gives a **subset**, not total V4 work. The3 hash layers still retain router scores under the recorded contract. Selection-boundary derivatives, quantized-training equivalence, MTP and full training quality are not established.

The mHC result covers86 outer wrappers and requires inner derivatives from the caller. The attention result covers a fixed-index tied-KV core; it explicitly excludes the complete attention layer/compressor backward. Adding these files as if they were disjoint complete layers would double-count some pieces and omit others. Their coverage flags are retained in results.json.

The MoE parameter subset is **278,152,609,792 parameters**. A declared16bytes/parameter mixed-precision Adam state implies **4,450,441,756,672bytes** before attention, embeddings/head, mHC, activations, optimizer/kernel workspace or communication buffers. This is a necessary aggregate capacity bound, not a feasible placement. It assumes this declared full-parameter optimizer; it is not inferred from the inference checkpoint's quantized size.

MoE matrix work alone is **45,720,010,752FLOPs/token** under the source128-token fixed-selection contract. Rows evaluate declared100B/1T-token tasks at90/180days and30%/40%/50% matrix efficiency. These efficiencies are hypotheses, not measured V4 MFU. Larger context/compression and whole-model work remain uncounted. The source's one-layer real-arithmetic calculation is not promoted to an actual full-model training benchmark.

| Device | MoE-state-only card floor | Other memory included? |
|---|---:|---|
| a100-80gb-sxm | 56 | No |
| h100-sxm | 56 | No |
| b200-sxm | 25 | No |

All36 compute/state boundary cases check both n and n−1 exactly. Combined necessary counts are saved, but full training cards, full duration and quality-qualified cost remain null. Since MoE persistent state alone exceeds the local96GB GPU by orders of magnitude, the full declared optimizer task cannot be validated there by relabeling an inference/offload run as training.

To complete10-10's V4 portion, the missing full attention/compressor derivative and work contract, activation lifetime/placement, optimizer update, task/quality objective and allocation/data/checkpoint/recovery assumptions must be supplied or implemented. A supported original training trace can calibrate those quantities. More GPUs alone do not fill the missing semantics. This artifact quantifies a resource floor and identifies the missing components; it does not close10-10 or claim these floor-sized fleets suffice.

Run `python run.py` to reproduce. Existing calculation files are read-only.
