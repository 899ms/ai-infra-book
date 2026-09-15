"""Round/resource accounting for the full example and shared-slot port sweep."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('07-*.md'))
M=192*2**20; alpha=F(833,10**9)
def calculate(g,local,remote,shared,algorithm):
 p=2*g; rounds=[]
 if algorithm in ('continuous','interleaved'):
  order=list(range(p)) if algorithm=='continuous' else [j for i in range(g) for j in (i,i+g)]
  cross=sum((order[i]//g)!=(order[(i+1)%p]//g) for i in range(p))
  for i in range(2*(p-1)):
   b=M//p; load=(cross//2*b if shared else b)
   seconds=max(F(b,local) if cross<p else F(0),F(load,remote))
   rounds.append(dict(phase='ring',logical_bytes=p*b,cross_bytes=cross*b,critical_serialization_s=float(seconds),duration_s=float(alpha+seconds)))
 else:
  for phase,n,b in [('local_reduce_scatter',g-1,M//g),('cross_allreduce',2,M//(2*g)),('local_allgather',g-1,M//g)]:
   for i in range(n):
    cross=phase=='cross_allreduce';seconds=F((g*b if shared else b),remote) if cross else F(b,local)
    rounds.append(dict(phase=phase,logical_bytes=p*b,cross_bytes=p*b if cross else 0,critical_serialization_s=float(seconds),duration_s=float(alpha+seconds)))
 assert sum(r['logical_bytes'] for r in rounds)==2*(p-1)*M
 return dict(gpus_per_server=g,local_GBps=local/10**9,remote_GBps=remote/10**9,shared_slot=shared,algorithm=algorithm,rounds=rounds,total_logical_MiB=sum(r['logical_bytes'] for r in rounds)/2**20,total_cross_both_directions_MiB=sum(r['cross_bytes'] for r in rounds)/2**20,time_ms=1000*sum(r['duration_s'] for r in rounds),startup_ms=float(len(rounds)*alpha*1000))
base=[calculate(8,450*10**9,50*10**9,False,a) for a in ('continuous','interleaved','hierarchical')]
assert [r['total_cross_both_directions_MiB'] for r in base]==[720,5760,384]
assert base[0]['time_ms']==base[1]['time_ms'] and base[2]['time_ms']<3<base[0]['time_ms']
sweep=[]
for local in (32,300):
 for ports in (1,2,3):
  for a in ('continuous','hierarchical'):
   r=calculate(4,local*10**9,min(25*ports,32)*10**9,True,a);r['ports']=ports;sweep.append(r)
for local in (32,300):
 for a in ('continuous','hierarchical'):
  xs=[r['time_ms'] for r in sweep if r['local_GBps']==local and r['algorithm']==a]
  assert xs[0]>xs[1]==xs[2]
# Equality in the region where the continuous ring is network limited.
threshold_shared=F(288*2**20)/(F(144*2**20,32*10**9)+6*alpha)
# Independent NICs: weighted local+remote cost cannot exceed the flat ring's max.
for local in (1,10,32,49,50,64,300,450,1000):
 assert calculate(8,local*10**9,50*10**9,False,'hierarchical')['time_ms'] < calculate(8,local*10**9,50*10**9,False,'continuous')['time_ms']
out=dict(exercise='7-5',alpha_us=float(alpha*10**6),baseline=base,shared_slot_sweep=sweep,shared_slot_local_crossover_GBps=float(threshold_shared/10**9),independent_NIC_ordering='hierarchical faster for all positive local bandwidths in this round model',scope='Synchronous round payload and startup model, no physical multi-GPU benchmark; 300GB/s on every local ring edge is a counterfactual',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'7-5-results.json').write_text(json.dumps(out,indent=2)+'\n')
fig,axes=plt.subplots(1,2,figsize=(10,4),sharey=True)
for ax,local in zip(axes,(32,300)):
 for a in ('continuous','hierarchical'):
  rs=[r for r in sweep if r['local_GBps']==local and r['algorithm']==a]
  ax.plot([r['ports'] for r in rs],[r['time_ms'] for r in rs],'o-',label=a.capitalize())
 ax.set(title=f'Local links: {local} GB/s',xlabel='Active 25 GB/s ports',xticks=[1,2,3],ylim=(0,19));ax.grid(alpha=.25);ax.legend()
axes[0].set_ylabel('AllReduce time (ms)')
fig.suptitle('Two four-GPU servers; each NIC shares one 32 GB/s slot')
fig.tight_layout();fig.savefig(P/'7-5-ports.png',dpi=160);fig.savefig(P/'7-5-ports.svg');plt.close(fig)
print(json.dumps(dict(baseline=[(r['algorithm'],r['time_ms']) for r in base],sweep=[(r['local_GBps'],r['ports'],r['algorithm'],r['time_ms']) for r in sweep],threshold_shared=float(threshold_shared/10**9)),indent=2))
