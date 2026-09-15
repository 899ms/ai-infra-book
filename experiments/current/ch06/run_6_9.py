"""Exact capacity conservation and remote-window/caching service budgets."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,math
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
cap=80*10**9;demand=[100*10**9,60*10**9,40*10**9,40*10**9];before=[min(cap,d) for d in demand];after=[80*10**9,80*10**9,40*10**9,40*10**9];borrow=20*10**9
assert sum(after)==sum(demand) and sum(after)-sum(before)==borrow
rows=[];path=50*10**9;local=3350*10**9;q=256
for ns in (7520,15040):
 L=F(ns,10**9);need=math.ceil(path*L/q);assert (need-1)*q<path*L<=need*q
 for u in (128,4096):
  rate=min(F(path),F(u*q)/L);t=F(borrow)/rate;local_t=F(borrow,local);cross=t/(t-local_t);first=math.floor(cross)+1
  assert (first-1)*t<=t+(first-1)*local_t and first*t>t+first*local_t
  rows.append(dict(rtt_ns=ns,inflight=u,minimum_for_path=need,window_bytes_s=float(F(u*q)/L),usable_bytes_s=float(rate),read_s=float(t),serial_reads_per_s=float(1/t),cache_crossover_reads_exact=str(cross),minimum_cache_beneficial_reads=first,ten_remote_reads_s=float(10*t),fetch_plus_ten_local_reads_s=float(t+10*local_t)))
files=['manuscripts/06-超节点.md','manuscripts/ch06/continuity_model.py','manuscripts/ch06/continuity-model.json']
out=dict(exercise='6-9',demand_bytes=demand,physical_before_bytes=before,unplaced_bytes=borrow,physical_after_bytes=after,other_nodes_free_before_bytes=[cap-x for x in before[1:]],all_nodes_free_after_bytes=[cap-x for x in after],rows=rows,local_cache_required_bytes=borrow,local_read_s=float(F(borrow,local)),scope='Analytical bandwidth/window assumptions, not RDMA or UB measurement; original borrower has no room for extra20GB local cache without making space',source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files})
(R/'6-9-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(rows,indent=2))
