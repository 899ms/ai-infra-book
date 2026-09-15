"""Declared GPipe resource/dependency schedule; not a hardware measurement."""
import gzip,hashlib,heapq,json,math
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parent/'candidate-layouts/results.json';candidates=json.loads(P.read_text())['candidates']
PROFILES=[('A100-assumed',150,150,80),('A800-assumed',150,100,80),('H20-assumed-50',50,100,96),('H20-assumed-100',100,100,96),('H20-assumed-150',150,100,96),('H20-assumed-150-link150',150,150,96)]
def schedule(c,tf,gb,topology):
 n=c['pp'];m=c['microbatches'];nodes={}
 def add(key,duration,resource,deps,kind,rank,mb,work=0,size=0):nodes[key]=dict(id=key,duration_s=duration,resource=resource,deps=deps,kind=kind,rank=rank,microbatch=mb,matrix_flops=work,payload_bytes=size)
 def link(s):
  cross=(s+1)%8==0 and topology=='eight-gpu-nodes-shared25'
  return ('shared-fabric' if cross else f'link{s}',25 if cross else gb)
 for j in range(m):
  for s in range(n):
   deps=[]
   if j:deps.append(f'SF{s}-{j-1}' if s<n-1 else f'F{s}-{j-1}')
   if s:deps.append(f'SF{s-1}-{j}')
   work=c['stages'][s]['forward_matrix_flops'];add(f'F{s}-{j}',work/(tf*1e12),f'gpu{s}',deps,'forward',s,j,work)
   if s<n-1:
    resource,rate=link(s);size=c['links'][s]['forward_bytes_per_microbatch'];deps=[f'F{s}-{j}']
    if j:deps.append(f'F{s+1}-{j-1}')
    add(f'SF{s}-{j}',size/(rate*1e9),resource,deps,'activation',s,j,size=size)
 barrier=[f'F{n-1}-{m-1}']
 for k,j in enumerate(reversed(range(m))):
  for s in reversed(range(n)):
   deps=list(barrier)+[f'F{s}-{j}']
   if k:deps.append(f'SB{s}-{j+1}' if s else f'B{s}-{j+1}')
   if s<n-1:deps.append(f'SB{s+1}-{j}')
   work=c['stages'][s]['training_with_layer_recompute_matrix_flops']-c['stages'][s]['forward_matrix_flops'];add(f'B{s}-{j}',work/(tf*1e12),f'gpu{s}',deps,'backward+recompute',s,j,work)
   if s:
    resource,rate=link(s-1);size=c['links'][s-1]['backward_bytes_per_microbatch'];deps=[f'B{s}-{j}']
    if k:deps.append(f'B{s-1}-{j+1}')
    add(f'SB{s}-{j}',size/(rate*1e9),resource,deps,'gradient',s,j,size=size)
 successors={k:[] for k in nodes};remaining={k:len(v['deps']) for k,v in nodes.items()}
 for k,v in nodes.items():
  for dep in v['deps']:assert dep in nodes;successors[dep].append(k)
 ready={k for k,v in remaining.items() if v==0};ends={};resources={};events=[]
 while ready:
  def start(k):return max(resources.get(nodes[k]['resource'],0),max((ends[d] for d in nodes[k]['deps']),default=0))
  k=min(ready,key=lambda k:(start(k),k));ready.remove(k);v=nodes[k];begin=start(k);end=begin+v['duration_s'];ends[k]=end;resources[v['resource']]=end;events.append(dict(**v,start_s=begin,end_s=end))
  for target in successors[k]:
   remaining[target]-=1
   if remaining[target]==0:ready.add(target)
 assert len(events)==len(nodes)==2*m*n+2*m*(n-1)
 # Independently audit DAG, service durations, payload/work conservation and resources.
 byid={e['id']:e for e in events};intervals={}
 for e in events:
  assert abs(e['end_s']-e['start_s']-e['duration_s'])<1e-9
  assert all(byid[d]['end_s']<=e['start_s']+1e-10 for d in e['deps'])
  intervals.setdefault(e['resource'],[]).append(e)
 for stream in intervals.values():
  stream.sort(key=lambda e:e['start_s']);assert all(a['end_s']<=b['start_s']+1e-10 for a,b in zip(stream,stream[1:]))
 assert sum(e['payload_bytes'] for e in events)==c['total_link_payload_bytes_per_step']
 assert sum(e['matrix_flops'] for e in events)==m*sum(s['training_with_layer_recompute_matrix_flops'] for s in c['stages'])
 finish=max(ends.values());assert finish>=max(sum(e['duration_s'] for e in stream) for stream in intervals.values())-1e-9
 return finish,events
rows=[];trace_dir=R/'traces';trace_dir.mkdir(exist_ok=True)
for idx,c in enumerate(candidates):
 for name,tf,gb,capacity in PROFILES:
  for topology in ['independent-links','eight-gpu-nodes-shared25']:
   finish,events=schedule(c,tf,gb,topology);key=f'{idx}-{name}-{topology}';raw=json.dumps(events,separators=(',',':')).encode();(trace_dir/(key+'.json.gz')).write_bytes(gzip.compress(raw,mtime=0))
   steps=math.ceil(100_000_000_000/c['effective_tokens_per_full_step']);headroom=capacity*10**9-c['peak_accounted_bytes'];rows.append(dict(candidate=idx,model=c['model'],pp=c['pp'],microbatches=c['microbatches'],profile=name,assumed_effective_matrix_tflops=tf,assumed_local_link_gb_s=gb,topology=topology,step_s=finish,full_steps_charged=steps,charged_tokens=steps*c['effective_tokens_per_full_step'],conditional_matrix_transfer_days=steps*finish/86400,workspace_headroom_bytes=headroom,capacity_rejected=headroom<0,full_feasibility_proven=False,events=len(events),trace='traces/'+key+'.json.gz',trace_sha256=hashlib.sha256((trace_dir/(key+'.json.gz')).read_bytes()).hexdigest()))
assert len(rows)==96
# Matched-form pair changes only the declared local-link service rate.
for idx in range(len(candidates)):
 for topo in ['independent-links','eight-gpu-nodes-shared25']:
  a=next(r for r in rows if r['candidate']==idx and r['topology']==topo and r['profile']=='A100-assumed');b=next(r for r in rows if r['candidate']==idx and r['topology']==topo and r['profile']=='A800-assumed');assert a['workspace_headroom_bytes']==b['workspace_headroom_bytes'] and a['charged_tokens']==b['charged_tokens']
(R/'results.json').write_text(json.dumps(dict(scope='Conditional matrix+transfer GPipe schedules; omitted costs and workspace prevent full completion prediction',candidate_source_sha256=hashlib.sha256(P.read_bytes()).hexdigest(),rows=rows),indent=2)+'\n')
s='''# Dependency-aware conditional hardware comparison

All96 schedules passed dependency, exclusive-resource, duration, matrix-work and payload checks. They reuse the eight concrete PP candidates and retain every compute/transfer event. The scheduler selects the earliest-ready operation, then its stable ID; this is a declared list schedule, not a proof of optimal scheduling. Forward fill completes before backward drain. Layer recomputation is charged. A stage waits for its preceding send before reusing its outbound buffer; each incoming transfer waits for the preceding consumer operation before reusing the receive buffer.

Compute uses one exclusive resource per GPU; transfer uses one exclusive resource per physical modeled link. Compute and DMA may overlap when dependencies permit. The independent-links model gives every PP boundary its own declared bandwidth. The eight-GPU-node model uses the same internal links but all boundaries crossing an eight-rank group share one25GB/s fabric resource. This is a stated topology assumption, not evidence that a94-GPU cluster has NVLink between every adjacent stage.

A100/A800 profiles hold candidate, compute rate150TFLOP/s effective matrix work,80GB capacity and topology fixed; only local-link effective bandwidth changes150→100GB/s. These are assumed effective rates, informed only by the archived2:3 NVLink specification ratio, not measured throughput. H20 profiles explicitly sweep50/100/150TFLOP/s with96GB and stated link rates; none is a hardware specification or measured training step.

| Model | PP | Microbatches | A100 assumed days | A800 assumed days | H20 assumed100TF days | Minimum workspace headroom80GB |
|---|---:|---:|---:|---:|---:|---:|
'''
for idx,c in enumerate(candidates):
 selected=[next(r for r in rows if r['candidate']==idx and r['topology']=='eight-gpu-nodes-shared25' and r['profile']==p) for p in ['A100-assumed','A800-assumed','H20-assumed-100']]
 s+=f"| {c['model']} | {c['pp']} | {c['microbatches']} | "+' | '.join(f"{r['conditional_matrix_transfer_days']:.3f}" for r in selected)+f" | {selected[0]['workspace_headroom_bytes']/1e9:.3f}GB |\n"
s+='''
The100B-token task charges a whole final batch, with charged_tokens saved. These times include modeled matrix compute, layer recompute and PP transfer; they exclude embedding/nonmatrix work, loss, optimizer update, data input, validation, checkpoint I/O, outages and framework overhead. They are conditional matrix/transfer durations, not full training completion forecasts. Effective compute rates exclude the modeled communication, avoiding double counting it as total-step MFU.

Negative memory headroom rejects a candidate even before workspace. Positive headroom still needs the temporary activation/attention/logit/optimizer/kernel allocations bounded. No row is labeled fully feasible or a completed hardware calibration. All profiles preserve invalid candidates for diagnosis rather than silently ranking them. Thus the original10-4 full comparison remains open pending these boundaries; this artifact replaces illustrative traffic amounts with concrete transfers and explicitly scheduled dependencies.

Run `python run.py` to regenerate all traces and tables. Raw source calculations remain unchanged.
'''
(R/'README.md').write_text(s)
(R/'manifest.json').write_text(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in R.rglob('*') if p.is_file() and p.name!='manifest.json'},indent=2)+'\n')
print({'schedules':96,'events':sum(r['events'] for r in rows),'capacity_rejected':sum(r['capacity_rejected'] for r in rows)})
