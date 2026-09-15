"""Independent phase changes and draft preparation break-even, exact arithmetic."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('08-*.md'))
base={'prefill':F(20),'decode':F(50),'tools_and_wait':F(30)};total=sum(base.values());rows=[]
for phase in base:
 changed={k:(v/2 if k==phase else v) for k,v in base.items()};t=sum(changed.values())
 assert total-t==base[phase]/2
 rows.append(dict(halved_phase=phase,phase_seconds={k:float(v) for k,v in changed.items()},total_seconds=float(t),speedup_exact=str(total/t),speedup=float(total/t)))
fixed=base['prefill']+base['decode']/4+base['tools_and_wait'];prep=F(8);threshold=total-fixed
assert fixed+threshold==total and fixed+threshold+F(1,1000)>total and fixed+threshold-F(1,1000)<total
out=dict(exercise='8-8',independent_halving=rows,decode_fourfold=dict(before_preparation_seconds=float(fixed),preparation_seconds=float(prep),total_seconds=float(fixed+prep),saved_seconds=float(total-fixed-prep),net_speedup_exact=str(total/(fixed+prep)),net_speedup=float(total/(fixed+prep)),preparation_break_even_seconds=float(threshold)),scope='Serial task phases; changes evaluated separately against original 100s; preparation paid once per task and not overlapped',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'8-8-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
