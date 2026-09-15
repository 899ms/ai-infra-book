"""Recompute all integer PD placements using the book's operator/hardware model."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.topics import pd_pool
V=1207959552
cases={}
for name,kwargs in [('base',{}),('limited_link',{'network_bytes_per_second':V}),('prefix_hit',{'cached_prefix_tokens':6144}),('short_output',{'output_tokens':129}),('efficiency40',{'workers':[dict(name=n,count=4,device=d,decode_batch=32,compute_efficiency=.4,bandwidth_efficiency=.4) for n,d in [('A100','a100-80gb-sxm'),('H20','h20-sxm5-96gb')]]})]:
 r=pd_pool.calculate(arrival_requests_per_second='3.5',**kwargs)
 assert len(r['pool_assignments'])==25
 best=F(r['summary']['best_pd_bound_requests_per_second_exact'])
 # Independently check every row from its resource demands.
 for row in r['pool_assignments']:
  pp=dd=F(0)
  for w in r['pool_worker_rates']:
   n=row['prefill_workers'][w['name']]
   pp+=n/F(w['prefill_service_seconds_exact']);dd+=(4-n)/F(w['decode_service_seconds_exact'])
  assert F(row['bound_requests_per_second_exact'])==min(pp,dd,F(r['summary']['network_capacity_requests_per_second_exact']))
 r['all_best_prefill_workers']=[x['prefill_workers'] for x in r['pool_assignments'] if F(x['bound_requests_per_second_exact'])==best]
 cases[name]=r
 print(name,float(best),r['summary']['best_prefill_workers'],'co',float(F(r['summary']['colocated_bound_requests_per_second_exact'])))
assert F(cases['limited_link']['summary']['best_pd_bound_requests_per_second_exact'])==1
assert {(x['A100'],x['H20']) for x in cases['limited_link']['all_best_prefill_workers']}=={(a,h) for a in range(5) for h in range(5)}-{(0,0),(0,1),(3,4),(4,4)}
for old,new in zip(cases['base']['pool_worker_rates'],cases['efficiency40']['pool_worker_rates']):
 for field in ['prefill_service_seconds_exact','decode_service_seconds_exact']:assert F(new[field])==F(old[field])*F(5,4)
assert F(cases['efficiency40']['summary']['best_pd_bound_requests_per_second_exact'])>F(7,2)
source=next((ROOT/'manuscripts').glob('09-*.md'))
files=[source,*[ROOT/'calculations/src/infra_calc/topics'/x for x in ['pd_pool.py','stage_rates.py']]]
for r in cases.values():
 for s in r['sources']:
  f=ROOT/'calculations'/s['file']
  if f.exists():files.append(f)
out=dict(exercise='9-2',cases=cases,limited_link_queue=dict(arrival_requests_per_s=1,capacity_requests_per_s=1,initial_extra_requests=10,samples=[dict(seconds=t,backlog_requests=10) for t in [0,1,10,60,600]],drain_time='infinite under constant fluid arrival'),source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
(P/'9-2-results.json').write_text(json.dumps(out,indent=2)+'\n')
