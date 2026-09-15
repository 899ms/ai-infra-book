"""State capacity and first-overflow boundaries, without floating roots."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('07-*.md'))
L=64;e=256;r=64;t=1024
one=dict(endpoints=L,targets=1,endpoint_bytes=L*e,binding_bytes=L*r,private_transport_bytes=L*t,shared_transport_bytes=t,private_total=L*e+L*(r+t),shared_total=L*e+L*r+t)
targets=128;capacity=2**21;fixed=L*e+L*targets*r;unit=targets*t;groups=(capacity-fixed)//unit
assert fixed+groups*unit<=capacity<fixed+(groups+1)*unit and groups<=L
bounds=[]
for name,fn in [('pair',lambda n:512*n*n+32*n),('endpoint_channel',lambda n:108*n)]:
 n=1
 while fn(n)<=2**20:n+=1
 assert fn(n-1)<=2**20<fn(n)
 bounds.append(dict(kind=name,first_overflow_N=n,last_fit_N=n-1,last_fit_bytes=fn(n-1),first_overflow_bytes=fn(n)))
out=dict(exercise='7-9',one_target=one,isolation=dict(fixed_bytes=fixed,per_group_bytes=unit,max_groups=groups,at_max_bytes=fixed+groups*unit,next_group_bytes=fixed+(groups+1)*unit,capacity_bytes=capacity),implementation_N_equals_M=bounds,scope='Declared byte-based context residency, not simulator entry-count limits or measured latency',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'7-9-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
