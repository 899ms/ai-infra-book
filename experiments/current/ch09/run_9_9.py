"""Routing bandwidth equalities and inverse-CDF quantiles."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('09-*.md'));V=1207959552
host=F(V,25*10**9);lookup=F(1,100);suffix=F(309,10000)
def remote(bw):return max(F(20,1000),lookup+F(V,bw)+host)+suffix
cross_A=F(V)/(F(250,1000)-lookup-host)
cross_B=F(V)/(F(907,1000)-suffix-lookup-host)
assert remote(cross_A)==F(250,1000)+suffix and remote(cross_B)==F(907,1000)
rows=[]
for p in (F(1,2),F(9,10),F(99,100)):
 mean=p*F(1109,10)+(1-p)*F(9672,10)
 rows.append(dict(hit_probability=float(p),mean_ms=float(mean),inverse_CDF_p99_ms=110.9 if p>=F(99,100) else 967.2))
assert max(F(80,1000),host)+suffix==F(1109,10000)
out=dict(exercise='9-9',snapshot_bytes=V,host_transfer_ms=float(host*1000),remote_tie_with_A_GBps=float(cross_A/10**9),remote_tie_with_B_recompute_GBps=float(cross_B/10**9),two_point_distribution=rows,CPU_fallback_overlapped_ms=float((max(F(80,1000),host)+suffix)*1000),scope='Route crossover uses rounded worked-example 887ms full recompute; probability exercise uses its separately given 110.9/967.2ms atoms; CPU fallback assumes valid copy and immediate independent transfer',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'9-9-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
