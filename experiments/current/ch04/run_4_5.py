"""Q projection intensity and matched device resource service budgets."""
import hashlib,json,sys,math
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[2];sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc import hardware
curves=[dict(rows=m,flops=2*m*4096**2,bytes=2*(4096**2+2*m*4096),intensity=float(F(m*4096,4096+2*m))) for m in range(1,257)]
for c in curves:assert abs(c['flops']/c['bytes']-c['intensity'])<1e-12
profiles=[];crossings=[];projection=[];attention=[];experts=[]
for name in ('rtx4090','h100-sxm'):
 h=hardware.select_device(name);p=hardware.select_peak(h,'BF16','FP32','tensor','dense');rate=F(str(p['tera_ops_per_second']))*10**12;bw=F(str(h['memory']['bandwidth_bytes_per_second']))
 profiles.append(dict(id=name,matrix_flops_s=float(rate),memory_bytes_s=float(bw),source_ids=h['source_ids']))
 for label,cm,bm in [('base',1,1),('matrix2',2,1),('bandwidth2',1,2)]:
  ratio=rate*cm/(bw*bm);cross=ratio*4096/(4096-2*ratio) if 2*ratio<4096 else None
  if cross:
   first=math.ceil(cross)
   intensity=lambda m:F(m*4096,4096+2*m)
   assert intensity(first)>=ratio and intensity(first-1)<ratio
  crossings.append(dict(device=name,change=label,continuous_rows_exact=str(cross) if cross else None,continuous_rows=float(cross) if cross else None,first_integer_compute_dominated=math.ceil(cross) if cross else None))
  for c in curves:
   ct=float(F(c['flops'],1)/(rate*cm));mt=float(F(c['bytes'],1)/(bw*bm))
   projection.append(dict(device=name,change=label,rows=c['rows'],compute_s=ct,memory_s=mt,bound_s=max(ct,mt),limiter='compute' if ct>=mt else 'memory'))
 for b in (1,32):
  for s in (8192,32768):
   flop=4*b*32*s*128;kv=4*b*8*s*128
   # Q and final O, each B*32*128 BF16; scores/probabilities not materialized here.
   payload=kv+4*b*32*128
   attention.append(dict(device=name,batch=b,context=s,matrix_flops=flop,kv_read_bytes=kv,logical_Q_KV_O_bytes=payload,exponentials=b*32*s,comparisons=b*32*(s-1),compute_s=float(flop/rate),memory_s=float(payload/bw),conditional_matrix_memory_s=max(float(flop/rate),float(payload/bw)),nonmatrix_time=None))
 for policy,active,tokens in [('balanced',128,2),('concentrated',8,32)]:
  k=4096;n=1536;flop=active*2*tokens*k*n;payload=active*2*(k*n+tokens*(k+n))
  assert active*tokens==32*8
  experts.append(dict(device=name,batch=32,policy=policy,active_experts=active,rows_per_active_expert=tokens,expert_up_shape=[tokens,k,n],matrix_flops=flop,logical_interface_bytes=payload,per_expert_intensity=float(F(2*tokens*k*n,2*(k*n+tokens*(k+n)))),compute_s=float(flop/rate),memory_s=float(payload/bw),conditional_aggregate_service_s=max(float(flop/rate),float(payload/bw))))
files=['calculations/configs/hardware.json','calculations/configs/models/qwen3-8b/config.json','manuscripts/04-加速器架构.md']
out=dict(exercise='4-5',scope='Analytical interface and compute service budgets, not measured whole-task latency',curves=curves,profiles=profiles,crossings=crossings,projection=projection,attention=attention,experts=experts,source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files})
(R/'4-5-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(profiles=profiles,crossings=crossings,examples=[r for r in projection if r['rows'] in (1,256) and r['change']=='base'],experts=experts),indent=2))
