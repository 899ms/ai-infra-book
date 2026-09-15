"""Declared B200-like matrix/transfer microtask: two versus three weight slots."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,math
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def run(batch,slots):
 released=[0]*slots;port=matrix=0;trace=[]
 for i in range(4):
  slot=i%slots;issue=max(port,released[slot]);ready=issue+192;start=max(matrix,ready);end=start+2*batch
  assert issue>=released[slot] and issue>=port and start>=ready and start>=matrix
  trace.append(dict(block=i,slot=slot,issue=issue,ready=ready,start=start,end=end));port=issue+64;matrix=released[slot]=end
 return dict(batch=batch,slots=slots,finish_tick=matrix,trace=trace,weight_buffer_bytes=slots*16384,activation_and_final_output_bytes=1152*batch)
rows=[]
for b in range(1,257):
 a=run(b,2);z=run(b,3);rows.append(dict(batch=b,before=a,after=z,saved_ticks=a['finish_tick']-z['finish_tick']))
assert rows[63]['saved_ticks']==64 and rows[63]['before']['finish_tick']==768 and rows[63]['after']['finish_tick']==704
threshold=next(r['batch'] for r in rows if all(s['saved_ticks']==0 for s in rows[r['batch']-1:]))
assert threshold==96 and rows[94]['saved_ticks']>0
clock=1850*10**6;price=F(1);fixed=F(1000);delta=F(64,clock*3600)*price;volume=fixed/delta;rate=F(clock,704);year=365*24*3600
cost=[]
for u,life in [(F(1,2),year),(F(1,4),year),(F(1,2),year//2)]:
 per=rate*u*life;cost.append(dict(utilization=float(u),lifetime_s=life,per_machine_tasks=float(per),minimum_machines=math.ceil(volume/per)))
out=dict(exercise='4-7',scope='Hypothetical resource change and explicitly declared teaching prices; not measured B200 or commercial design ROI',task='Four sequential 64x128 BF16 weight-block GEMMs with shared Bx64 activation; output Bx512; isolate weight transfer and matrix service',matrix_flops_per_tick=8192,transfer_bytes_per_tick=256,extra_latency_ticks=128,baseline_batch=64,additional_weight_buffer_bytes=16384,no_benefit_from_batch=threshold,rows=rows,cost=dict(clock_hz=clock,incremental_fixed_usd=float(fixed),machine_usd_per_hour=float(price),saved_usd_per_task=float(delta),breakeven_tasks_exact=str(volume),breakeven_tasks_ceiling=math.ceil(volume),optimized_tasks_per_active_second=float(rate),scenarios=cost),source_sha256={'manuscripts/04-加速器架构.md':hashlib.sha256((ROOT/'manuscripts/04-加速器架构.md').read_bytes()).hexdigest()})
(R/'4-7-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
