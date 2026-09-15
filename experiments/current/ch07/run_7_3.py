"""Clos counts and exact-ratio integer-port versus proportional cut budgets."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
P=Path(__file__).resolve().parent; ROOT=P.parents[2]
source=next((ROOT/'manuscripts').glob('07-*.md')); bw=50*10**9
rows=[]
for k in (64,128):
 for levels,endpoints,switches in ((2,k*k//2,3*k//2),(3,k**3//4,5*k*k//4)):
  rows.append(dict(ports=k,levels=levels,endpoints=endpoints,switches=switches,bisection_one_direction_TBps=float(F(endpoints*bw,2*10**12))))
assert rows[0]['endpoints']==2048 and rows[1]['switches']==5120
leaves=(1024+41)//42; uplinks=leaves*21
assert leaves*42>=1024>(leaves-1)*42 and 42==2*21 and 42+21==63
volume=F(2*7,8)*8*8*10**9
nominal=F(128*bw,2); exact=4*21*bw
local=F(2,3)
assert (1-local)*bw==F(bw,3) and (1-(local-F(1,1000)))*bw>F(bw,3)
out=dict(exercise='7-3',clos=rows,partition_1024=dict(exact_ratio=dict(down_ports=42,up_ports=21,unused_ports_per_leaf=1,leaves=leaves,unused_down_slots=leaves*42-1024,uplinks=uplinks,cut_TBps=float(F(uplinks*bw,10**12)),per_card_GBps=float(F(uplinks*50,1024))),proportional_model=dict(cut_TBps=25.6,per_card_GBps=25)),supernode_128=dict(cross_domain_send_bytes=int(volume),nominal_2_to_1_egress_TBps=float(nominal/10**12),pure_transfer_ms=float(volume/nominal*1000),startup_rounds=14,alpha_us=0.833,with_startup_ms=float(volume/nominal*1000+F(14*833,10**6)),dedicated_four_leaf_alternative=dict(egress_TBps=float(F(exact,10**12)),pure_transfer_ms=float(volume/exact*1000))),minimum_local_fraction_at_ratio_3=str(local),scope='Analytical exercise; one-direction payload bandwidth; no physical Clos or multi-GPU measurement',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'7-3-results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
