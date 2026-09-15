"""Padding FLOPs, strict replica payback, and per-device capacity gate."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('09-*.md'))
params=18874368;loads=[32,16,8,4,2,1,1,0];effective=sum(loads)
padding=[dict(policy=label,rows=n,matrix_flops=2*n*params,relative_to_effective=float(F(n,effective))) for label,n in [('effective_only',effective),('nonempty_to_32',sum(x>0 for x in loads)*32),('all_to_32',8*32)]]
saved=F(402784256,1675*10**9);copies=[]
for b in (450,50):
 copy=7*F(5,10**6)+F(7*36*2**20,b*10**9);n=copy//saved+1
 assert (n-1)*saved<=copy<n*saved
 copies.append(dict(link_GBps=b,copy_ms=float(copy*1000),saved_per_batch_ms=float(saved*1000),first_strictly_profitable_batch=n,net_savings_ms={str(k):float((k*saved-copy)*1000) for k in (16,64)}))
out=dict(exercise='9-6',padding=padding,payback=copies,capacity=dict(replica_MiB_per_receiver=36,receivers=7,total_copy_MiB=252,original_free_MiB_per_receiver=64,reduced_free_MiB_per_receiver=32,deficit_MiB_per_receiver=4,feasible_with_32=False),scope='Fixed replica-route model; padding counts model GEMM work, no new multi-GPU timing; gain must be on the request critical path',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'9-6-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
