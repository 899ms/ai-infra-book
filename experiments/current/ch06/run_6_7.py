"""Discrete server/group power ceilings and matched TP8 service capacity."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,importlib.util
R=Path(__file__).resolve().parent;ROOT=R.parents[2];power=F(51,5)
def total(servers,switch):return power*(servers+(1 if switch and servers>8 else 0))
base=[dict(gpus=g,servers=g//8,power_kw=float(total(g//8,False)),fits_120kw=total(g//8,False)<=120) for g in (64,72,96)]
limits=[]
for label,budget,switch,unit in [('a',150,False,1),('b',120,True,1),('c',120,True,4)]:
 allowed=[n for n in range(0,101,unit) if total(n,switch)<=budget];n=max(allowed);assert total(n+unit,switch)>budget
 limits.append(dict(part=label,budget_kw=budget,servers_per_expansion=unit,servers=n,gpus=8*n,total_power_kw=float(total(n,switch)),next_expansion_power_kw=float(total(n+unit,switch))))
spec=importlib.util.spec_from_file_location('continuity',ROOT/'manuscripts/ch06/continuity_model.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
service=sum(m.step(8,m.PARAMS['history']+i)['total_s'] for i in range(8));arch=json.loads((ROOT/'manuscripts/ch06/continuity-model.json').read_text());ref=next(r for r in arch['candidates'] if r['tp']==8);assert abs(service*1000-ref['service_ms'])<1e-10 and m.max_sessions(8,131072)>=1
capacity=[dict(gpus=g,TP8_instances=g//8,eight_token_session_service_s=service,sessions_per_s_upper=(g//8)/service,output_tokens_per_s_upper=8*(g//8)/service) for g in (64,80)]
files=['manuscripts/06-超节点.md','manuscripts/ch06/continuity_model.py','manuscripts/ch06/continuity-model.json','calculations/configs/hardware.json']
out=dict(exercise='6-7',server_power_kw=float(power),base=base,ceilings=limits,capacity=capacity,scope='Power-envelope installation arithmetic and analytic independent TP8 instances, not installed racks or measured aggregate service',source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files})
(R/'6-7-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
