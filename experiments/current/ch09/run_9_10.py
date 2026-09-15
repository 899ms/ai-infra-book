"""Mixed workload sizing and deterministic fluid tandem queue (not GPU timing)."""
from pathlib import Path
from fractions import Fraction as F
from collections import deque
import sys,json,hashlib,math
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.topics.stage_rates import device_rates
rates={}
for dev in ['a100-80gb-sxm','h20-sxm5-96gb']:
 rates[dev]={str(g):device_rates(device=dev,output_tokens=g) for g in [1025,4097]}
ps=[];ds=[];ratios=[]
for r in rates.values():
 ps.append(F(r['1025']['prefill']['seconds_exact']))
 pair=[F(r[str(g)]['decode']['seconds_per_request_exact']) for g in [1025,4097]]
 avg=sum(pair)/2;ds.append(avg);ratios.append([x/avg for x in pair])
assert ratios[0]==ratios[1] # both decode classes remain bandwidth bound
rows=[]
for a in range(5):
 for h in range(5):
  pp=a/ps[0]+h/ps[1];dd=(4-a)/ds[0]+(4-h)/ds[1];link=F(25*10**9,1207959552);mu=min(pp,dd,link)
  rows.append(dict(P_A100=a,P_H20=h,P_rate=float(pp),D_rate=float(dd),link_rate=float(link),mu=float(mu),mu_exact=str(mu)))
best=max(rows,key=lambda x:F(x['mu_exact']));mu=F(best['mu_exact']);arrival=F(7,2)
nsteady=int(arrival//mu)+1 # strict service margin
nrecover=math.ceil((arrival*60/50)/mu)
assert (nsteady-1)*mu<=arrival<nsteady*mu
assert (nrecover-1)*mu<arrival*60/50<=nrecover*mu
print('D averages',list(map(float,ds)),'best',best,'groups',nsteady,nrecover)
# Replicated group includes an independent link. Shared-link alternative checked in report.
# FIFO fluid parcels: P consumes request counts; D consumes normalized mean-D work.
weights=list(map(float,ratios[0]))
def simulate(groups,startup,dt):
 pq=deque();dq=deque();pcount=0.;dcount=0.;dwork=0.;trace=[];first_clear=None;peak=0.;peak_t=0.;arrived=0.;completed=0.
 pr=groups*best['P_rate'];dr=groups*best['D_rate']
 for k in range(round(180/dt)):
  t=k*dt
  # 105 long requests/minute in first 10s, 105 short uniformly over minute.
  for kind,rate in [(0,1.75),(1,10.5 if (k*dt)%60<10-1e-9 else 0.)]:
   amount=rate*dt
   if amount:pq.append([kind,amount]);pcount+=amount;arrived+=amount
  budget=pr*dt if t>=startup-1e-9 else 0.
  while pq and budget>1e-12:
   kind,amount=pq[0];take=min(amount,budget);pq[0][1]-=take;budget-=take;pcount-=take
   if dq and dq[-1][0]==kind:dq[-1][1]+=take
   else:dq.append([kind,take])
   dcount+=take;dwork+=take*weights[kind]
   if pq[0][1]<1e-12:pq.popleft()
  budget=dr*dt if t>=startup-1e-9 else 0.
  while dq and budget>1e-12:
   kind,amount=dq[0];take=min(amount,budget/weights[kind]);dq[0][1]-=take;budget-=take*weights[kind];dcount-=take;dwork-=take*weights[kind];completed+=take
   if dq[0][1]<1e-12:dq.popleft()
  assert abs(arrived-completed-pcount-dcount)<1e-7
  total=max(0.,pcount+dcount)
  if total>peak:peak=total;peak_t=t+dt
  if t+dt>10 and first_clear is None and total<1e-7:first_clear=t+dt
  if k%round(.1/dt)==0:trace.append(dict(t=round(t+dt,6),P_requests=max(0,pcount),D_requests=max(0,dcount),D_mean_work=max(0,dwork),total_requests=total))
 return dict(groups=groups,startup_s=startup,dt=dt,peak_requests=peak,peak_time_s=peak_t,first_clear_after_burst_s=first_clear,end_requests=total,trace=trace)
sims=[simulate(n,s,.01) for n,s in [(nsteady,0),(nsteady,10),(nrecover,10)]]
convergence=[]
for x in sims:
 y=simulate(x['groups'],x['startup_s'],.005)
 delta=abs(x['peak_requests']-y['peak_requests'])
 assert delta<.2
 if x['first_clear_after_burst_s'] is not None:assert abs(x['first_clear_after_burst_s']-y['first_clear_after_burst_s'])<.1
 convergence.append(dict(groups=x['groups'],startup=x['startup_s'],peak_delta=delta,fine_first_clear=y['first_clear_after_burst_s']))
 print('burst',x['groups'],x['startup_s'],x['peak_requests'],x['first_clear_after_burst_s'],x['end_requests'])
files=[next((ROOT/'manuscripts').glob('09-*.md')),ROOT/'calculations/src/infra_calc/topics/stage_rates.py']
for rs in rates.values():
 for r in rs.values():
  for s in r['sources']:
   f=ROOT/'calculations'/s['file']
   if f.exists():files.append(f)
out=dict(exercise='9-10',rates=rates,mean_D_GPU_s=list(map(float,ds)),D_class_weights=weights,allocations=rows,best=best,minimum_groups_steady=nsteady,minimum_groups_recover60=nrecover,constant_mixed_startup_clear_s={str(n):float(10+35/(n*mu-arrival)) for n in {nsteady,nrecover} if n*mu>arrival},burst_assumptions='Short arrivals 1.75/s throughout; long 10.5/s in first 10s each minute; FIFO fluid P then D; fixed mean-mix routing; no per-request prefill latency or kernel scheduling; independent links per group; link capacity exceeds P peak output.',simulations=sims,convergence=convergence,source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
(P/'9-10-results.json').write_text(json.dumps(out,indent=2)+'\n')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axes=plt.subplots(3,1,figsize=(10,10),sharex=True)
for ax,x in zip(axes,sims):
 ts=[r['t'] for r in x['trace']]
 for key,label in [('P_requests','P queue'),('D_requests','D queue'),('total_requests','Total')]:ax.plot(ts,[r[key] for r in x['trace']],label=label)
 for t in [0,60,120]:ax.axvspan(t,t+10,color='orange',alpha=.12)
 ax.set(title=f"{x['groups']} groups; startup {x['startup_s']} s",ylabel='Queued requests (fluid)');ax.legend();ax.grid(alpha=.2)
axes[-1].set_xlabel('Time (s); orange = long-output arrival burst')
fig.tight_layout();fig.savefig(P/'9-10-queues.png',dpi=160);plt.close(fig)
