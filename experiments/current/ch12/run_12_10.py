"""Independent binomial and geometric-tail checks of the WAN loss exercise."""
from pathlib import Path
from fractions import Fraction as F
from math import comb,sqrt,ceil
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
k=245;mss=1448;payload=354640;rate=333000000;rtt=F('.2');serial=F('.2385')
assert ceil(payload/mss)==k and payload==k*mss-120
sources=[ROOT/'manuscripts/12-端边云协同.md']
def success(repair,p):
 n=k+repair
 return sum((comb(n,i)*p**i*(1-p)**(n-i) for i in range(repair+1)),F(0))
rows=[]
for label in ['0.14','0.036']:
 p=F(label);cdf=[(1-p**n)**k for n in range(21)]
 expected=sum((1-c for c in cdf),F(0))
 # Remaining E[N] tail <= sum_{n=21}^infinity k*p^n by union bound.
 tail_bound=k*p**21/(1-p);assert tail_bound<F(1,10**14)
 p99=next(n for n,c in enumerate(cdf) if c>=F('.99'))
 repair=0
 while success(repair,p)<F('.999'):repair+=1
 prob=success(repair,p);previous=success(repair-1,p)
 assert previous<F('.999')<=prob
 mathis=mss*8/.2/sqrt(float(p))
 fecbytes=(k+repair)*mss
 fec=F('.23')+F(fecbytes*8,rate)
 archived=ROOT/'calculations/results'/('wan-loss-model-book.json' if label=='0.14' else 'wan-loss-model-p036.json')
 a=json.loads(archived.read_text());assert a['summary']['fec_repair_symbols']==repair and a['summary']['p99_rounds']==p99
 assert abs(a['summary']['mathis_mbit_per_second']-mathis/1e6)<1e-12
 sources.append(archived)
 rows.append(dict(loss_probability=label,mathis_Mbps=mathis/1e6,mathis_send_s=payload*8/mathis,expected_initial_losses=float(k*p),round_cdf=[dict(n=n,prob=float(c)) for n,c in enumerate(cdf[:9])],expected_rounds=float(expected),expected_rounds_truncation_error_bound=float(tail_bound),expected_completion_s=float(serial+(expected-1)*rtt),p99_rounds=p99,p99_completion_s=float(serial+(p99-1)*rtt),fec_repair_packets=repair,fec_redundancy=float(F(repair,k)),fec_success=float(prob),one_fewer_repair_success=float(previous),fec_total_wire_payload_bytes=fecbytes,fec_completion_s=float(fec),fixed63_repair_success=float(success(63,p))))
out=dict(exercise='12-10',kind='analytical_independent_loss_ideal_repair',rows=rows,fixed63_at_loss20pct_success=float(success(63,F('.2'))),source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sources})
(P/'12-10-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
