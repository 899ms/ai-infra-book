"""Exact occupancy distribution and finite-message packet reordering."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('07-*.md'))
def distribution(n,m):
 cdf=[]
 for cap in range(n+1):
  dp=[1]+[0]*n
  for box in range(m):dp=[sum(comb(k,j)*dp[k-j] for j in range(min(cap,k)+1)) for k in range(n+1)]
  cdf.append(F(dp[n],m**n))
 assert cdf[-1]==1 and cdf[0]==0
 pmf=[cdf[k]-(cdf[k-1] if k else 0) for k in range(n+1)]
 expectation=sum((1-cdf[k] for k in range(n)),F(0));assert expectation==sum(k*v for k,v in enumerate(pmf))
 return dict(flows=n,uplinks=m,expected_max=float(expectation),expected_max_exact=str(expectation),relative_speed_inverse_mean=float(1/expectation),mean_inverse_max=float(sum(pmf[k]/k for k in range(1,n+1))),probability_max=[str(x) for x in pmf])
def spray(packet,last):
 count=8*2**20//packet;tau=F(packet,50000);arrivals={}
 for seq in range(count):
  path=seq%8;time=(seq//8+1)*tau+1+F(path,7)*(last-1)
  arrivals.setdefault(time,[]).append(seq)
 pending=set();nextseq=0;peak=0;peak_at=None
 for time,seqs in sorted(arrivals.items()):
  pending.update(seqs)
  while nextseq in pending:pending.remove(nextseq);nextseq+=1
  if len(pending)>peak:peak=len(pending);peak_at=time
 assert nextseq==count and not pending
 return dict(packet_bytes=packet,packet_count=count,last_delay_us=last,complete_us=float(max(arrivals)),peak_reorder_packets=peak,peak_reorder_bytes=peak*packet,peak_first_us=float(peak_at),arrival_events=[dict(us=float(t),seqs=s) for t,s in sorted(arrivals.items())])
baseline=spray(4096,8);assert baseline['peak_reorder_packets']==339
rows=[spray(packet,30) for packet in (4096,1024)]
single=F(8*2**20,50000)+1;critical=single-F(2**20,50000)
assert critical+F(2**20,50000)==single
out=dict(exercise='7-14',hashing=[distribution(8,16),distribution(16,32)],spraying=rows,original_4KiB_1to8us_peak=baseline['peak_reorder_packets'],single_path_us=float(single),critical_slowest_delay_us=float(critical),scope='Independent uniform per-flow hashes; round-robin per-packet routing on eight independent 50GB/s serializers, full-packet arrivals and immediate prefix delivery; speed metric matches inverse expected bottleneck load',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'7-14-results.json').write_text(json.dumps(out,indent=2)+'\n')
print([(x['flows'],x['uplinks'],x['expected_max'],x['relative_speed_inverse_mean']) for x in out['hashing']]);print([{k:v for k,v in r.items() if k!='arrival_events'} for r in rows]);print('critical',float(critical))
