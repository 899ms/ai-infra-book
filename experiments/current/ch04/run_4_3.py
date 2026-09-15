"""Reconcile pinned storage ledger; extend it with an explicit transaction window."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
p=ROOT/'calculations/results/storage-generation-qwen8-235.json';d=json.loads(p.read_text());rows=[];work=[]
for w in d['workloads']:
 t=w['tensors'];assert sum(x['payload_bytes']+x['scale_bytes'] for x in t)==w['resident_weight_bytes']
 parts=w['payload_components_bytes'];assert sum(parts.values())==w['accounted_payload_bytes']
 assert sum(x['step_payload_read_bytes'] for x in t)==parts['weight_payload']
 assert sum(x['step_metadata_read_bytes'] for x in t)==parts['weight_scales']
 if w['expert_counts'] is not None:
  assert sum(w['expert_counts'])==w['batch']*8
 work.append({k:v for k,v in w.items() if k not in ('tensors','sources')})
 for label,cap,bw in [('base',80*10**9,3350*10**9),('capacity160',160*10**9,3350*10**9),('capacity640',640*10**9,3350*10**9),('bandwidth2',80*10**9,6700*10**9),('capacity640_bandwidth2',640*10**9,6700*10**9)]:
  available=cap-w['resident_weight_bytes']-w['declared_workspace_bytes'];maximum=max(0,available//w['kv_bytes_per_request'])
  if maximum:assert w['resident_weight_bytes']+w['declared_workspace_bytes']+maximum*w['kv_bytes_per_request']<=cap
  assert w['resident_weight_bytes']+w['declared_workspace_bytes']+(maximum+1)*w['kv_bytes_per_request']>cap
  fits=w['resident_budget_bytes']<=cap
  for slots in (128,4096,32768):
   latency_ns=500;s=128;required=(bw*latency_ns+s*10**9-1)//(s*10**9)
   window=slots*s*10**9//latency_ns;rate=min(bw,window)
   assert (required-1)*s*10**9<bw*latency_ns<=required*s*10**9
   rows.append(dict(workload=w['id'],resources=label,capacity_bytes=cap,bandwidth_bytes_s=bw,maximum_requests=maximum,fits=fits,transaction_bytes=s,latency_ns=latency_ns,independent_transactions=slots,required_transactions=required,effective_bandwidth_upper_bytes_s=rate,limiter='capacity' if not fits else ('transaction_window' if window<bw else 'bandwidth'),payload_service_seconds=w['accounted_payload_bytes']/bw,capacity_qualified_window_seconds=max(latency_ns/1e9,w['accounted_payload_bytes']/rate) if fits else None))
files=[p,ROOT/'calculations/src/infra_calc/topics/storage_generation_comparison.py',ROOT/'calculations/src/infra_calc/topics/memory_concurrency.py',ROOT/'manuscripts/04-加速器架构.md']
out=dict(exercise='4-3',scope='Conditional analytical resource comparison; no GPU measurement or deployment claim',workloads=work,rows=rows,source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
(R/'4-3-results.json').write_text(json.dumps(out,indent=2)+'\n');print('verified',len(work),'storage workloads and',len(rows),'capacity/bandwidth/window scenarios')
for model,bits in [('qwen3-8b',16),('qwen3-235b-a22b',4),('qwen3-235b-a22b',16)]:
 for batch in (1,8,32):
  for w in work:
   if w['model']==model and w['matrix_storage_bits']==bits and w['batch']==batch and w['history']==8191:
    a=[x for x in rows if x['workload']==w['id'] and x['independent_transactions']==32768 and x['resources'] in ('base','capacity160','capacity640')]
    print(model,bits,batch,w['routing'],'residentW',w['resident_weight_bytes']/1e9,'payloadGB',w['accounted_payload_bytes']/1e9,'max',[x['maximum_requests'] for x in a],'ms',a[0]['payload_service_seconds']*1000)
