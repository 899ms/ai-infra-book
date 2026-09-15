import hashlib,json,math
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[3];source=R.parent/'candidate-layouts/results.json';cs=json.loads(source.read_text())['candidates'];rows=[]
for c in cs:
 m=c['microbatches'];n=c['pp'];fw=[s['forward_matrix_flops'] for s in c['stages']];bw=[s['training_with_layer_recompute_matrix_flops']-s['forward_matrix_flops'] for s in c['stages']]
 def grid(costs):
  end={}
  for j in range(m):
   for rank,work in enumerate(costs):end[rank,j]=max(end.get((rank-1,j),0),end.get((rank,j-1),0))+work
  return end[n-1,m-1]
 closed=sum(fw)+sum(bw)+(m-1)*(max(fw)+max(bw));assert closed==grid(fw)+grid(list(reversed(bw)))
 steps=math.ceil(F(100_000_000_000,c['effective_tokens_per_full_step']));deadline=30*86400
 required=F(closed*steps,deadline*10**12);days=F(closed*steps,312*10**12*86400);assert days>30 and required>312
 linkbytes=c['links'][0]['total_bytes_per_step']*steps;cross=sum((l['source']+1)%8==0 for l in c['links'])
 rows.append(dict(model=c['model'],pp=n,microbatches=m,steps=steps,critical_path_work_exact=closed,optimistic_312_tflops_days=float(days),optimistic_312_days_exact=str(days),necessary_effective_tflops_for_30_days=float(required),necessary_rate_exact=str(required),deadline_impossible_at_312=True,minimum_workspace_headroom_80GB=c['minimum_workspace_headroom_80GB']/1e9,minimum_workspace_headroom_96GB=c['minimum_workspace_headroom_96GB']/1e9,necessary_each_link_GB_s=float(F(linkbytes,deadline*10**9)),cross_node_links=cross,necessary_shared_fabric_GB_s=float(F(cross*linkbytes,deadline*10**9))))
sources={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()}
for name in ['references/outline-checks/2026-09-07/systems-cases/a800-lenovo.txt','references/text/nvidia-a100-80-spec.txt']:
 p=ROOT/name;assert '312' in p.read_text();sources[name]=hashlib.sha256(p.read_bytes()).hexdigest()
(R/'results.json').write_text(json.dumps(dict(scope='Negative feasibility proof for declared candidates/tasks, not all possible partitions',source_sha256=sources,rows=rows),indent=2)+'\n')
s='''# Deadline rejection without inventing missing overhead

For each selected candidate, the communication-free GPipe makespan in units of matrix work is:

`sum(F_stage)+sum(B_stage)+(microbatches−1)*(max(F_stage)+max(B_stage))`.

All jobs have the same per-stage matrix work; the forward fill barrier precedes backward drain. A separate integer dynamic-programming grid reproduces this closed form exactly for all eight candidates. Backward work includes the declared layer recomputation. Dividing by a uniform effective matrix rate gives the optimistic step time. Communication, nonmatrix operations, loss, optimizer, data, checkpointing, outages and allocation costs are all set to zero for this proof. A whole final batch is charged as in the schedule runner.

The archived A10080GB and A80080GB SXM specification text lists312TFLOP/s BF16 dense (624 is structured-sparse). Using312 as an ideal100%-of-peak rate makes this an optimistic lower bound, not a prediction of achievable training speed. It is not used as an H20 specification. The earlier explicit H20 assumptions50/100/150TFLOP/s are below this ceiling and also fail these deadlines.

| Model | PP | Microbatches | Optimistic days at312TF/card | Necessary TF/card for30days, even without communication | Workspace headroom80GB | Workspace headroom96GB |
|---|---:|---:|---:|---:|---:|---:|
'''
for r in rows:s+=f"| {r['model']} | {r['pp']} | {r['microbatches']} | {r['optimistic_312_tflops_days']:.3f} | {r['necessary_effective_tflops_for_30_days']:.3f} | {r['minimum_workspace_headroom_80GB']:.3f}GB | {r['minimum_workspace_headroom_96GB']:.3f}GB |\n"
s+='''
Every candidate fails100B tokens/30days under these conditions. Therefore measuring omitted nonnegative overhead or temporary workspace cannot turn one of them into a deadline-feasible choice. Positive workspace headroom remains only a conditional memory allowance; this proof does not call such candidates memory-feasible. Negative headroom already rules out capacity before temporary allocations.

These results describe the selected PP-only candidates and GPipe policy, not every possible training design. More GPUs, different parallelism, a different microbatch/schedule choice, shorter task, or a relaxed deadline can change the answer and must be recalculated. No claim is made that Qwen training generally requires these particular PP counts.

## What can change a choice

Capacity changes when unaccounted peak workspace crosses the per-candidate headroom above; negative headroom cannot be repaired by a faster interconnect. The compute deadline threshold is the necessary effective rate in the table; actual required rates including omitted work cannot be smaller. Link/fabric lower bounds are also saved: each physical resource must transmit its counted payload within30days, so `payload/deadline` is a necessary bandwidth. Shared cross-node traffic is counted across every crossing, rather than giving each transfer a full independent fabric. Passing these separate necessary tests is not sufficient for a full schedule.

The scheduled-comparison artifact already holds compute, capacity, work, topology and policy fixed between A100/A800 and changes only the declared2:3 effective local-link rate. In the measured-work analytical candidates, matrix work and the long GPipe fill/drain dominate that particular link-rate change. This is a result of the declared candidates, not a claim that interconnect never dominates training. As compute grows faster, payload grows, bandwidth shrinks or more boundaries share the fabric, the link resource bound becomes limiting.

This closes the negative deadline decision for the selected candidates without requiring fabricated complete-step measurements. It does not replace the original source-review finding that matched actual A100/A800/H20 Qwen training traces are absent.
'''
(R/'README.md').write_text(s);(R/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in R.iterdir() if p.is_file() and p.name!='manifest.json'},indent=2)+'\n');print('8 exact deadline rejections verified')
