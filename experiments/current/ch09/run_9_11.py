"""Exercise 9-11: fixed-stage MLA/AF sensitivity, exact rational arithmetic."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
source=next((ROOT/'manuscripts').glob('09-*.md'))
V=8192*61*(512+64)*2
AF=36*2*4096*2
alpha=F(5,10**6)
p_rate=4*F(9566,8192);d=F(1024,1166);d_rate=4/d
rows=[]
for B in [25*10**9,50*10**9]:
 pd=F(V,B)+alpha;af=F(AF,B)+72*alpha;cross=F(V-AF,71*B)
 assert F(V,B)+cross==F(AF,B)+72*cross
 assert af<pd
 rows.append(dict(bandwidth_GBps=B/10**9,PD_payload_ms=float(F(V,B)*1000),PD_with_startup_ms=float(pd*1000),AF_one_step_ms=float(af*1000),link_requests_per_s=float(F(B,V)),alpha_crossover_us=float(cross*10**6),decode=[dict(output_tokens=n+1,steps=n,AF_cumulative_ms=float(n*af*1000),AF_to_PD_ratio=float(n*af/pd)) for n in [1024,4096]]))
extra=F(205*10**7,74*10**12)
new_d=d+1024*extra
new_rate=4/new_d
limit=(F(4,1)/F(7,2)-d)/1024
assert new_rate>F(7,2) and 3/new_d<F(7,2)
assert 4/(d+1024*limit)==F(7,2)
out=dict(exercise='9-11',state_bytes=V,state_MiB=V/2**20,bytes_per_token=61*576*2,AF_bytes_per_step=AF,P_requests_per_s=float(p_rate),D_requests_per_s=float(d_rate),network_bottleneck_threshold_GBps=float(min(p_rate,d_rate)*V/10**9),links=rows,query_transform=dict(extra_per_request_step_us=float(extra*10**6),extra_batch32_step_ms=float(32*extra*1000),extra_1024_steps_ms=float(1024*extra*1000),original_D_GPU_s=float(d),new_D_GPU_s=float(new_d),new_four_H20_requests_per_s=float(new_rate),new_three_H20_requests_per_s=float(3/new_d),relative_capacity_loss=float(1-new_rate/d_rate),four_card_extra_step_limit_us=float(limit*10**6),arrival_requests_per_s=3.5,minimum_D_cards=4),scope='Fixed exercise stage rates 9566 and 1166, not a full DeepSeek-V3 deployment model. Serial exposed query transform; bandwidth link term excludes startup per specified equation. AF comparison includes decode only.',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'9-11-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
