"""Bisection enumeration, cross-host groups and exact connection state/setup."""
from pathlib import Path
import json,hashlib,itertools
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
tori=[]
for k in (4,8):
 nodes=list(itertools.product(range(k),repeat=3));cut=[]
 for v in nodes:
  for axis in range(3):
   w=list(v);w[axis]=(w[axis]+1)%k;w=tuple(w)
   if (v[0]<k//2)!=(w[0]<k//2):cut.append([v,w])
 assert len(cut)==2*k*k
 tori.append(dict(k=k,chips=k**3,bisection_physical_links=len(cut),one_direction_cut_GBps=len(cut)*50,one_direction_GBps_per_sending_chip=len(cut)*50/(k**3//2),cut_edges=cut))
state=[]
for cache in (256*1024,1024**2):
 for kind,base,slope in [('pair',32*64,512*64**2),('endpoint_channel',52*64,56)]:
  hosts=1+(cache-base)//slope
  assert base+slope*(hosts-1)<=cache<base+slope*hosts
  state.append(dict(cache_bytes=cache,kind=kind,max_hosts=hosts,used_at_max=base+slope*(hosts-1),next_host_bytes=base+slope*hosts,hosts192_bytes=base+slope*191,hosts192_fits=base+slope*191<=cache))
setup=[]
for rtt in (500,50):
 pair=1024**2*(4*5+rtt);ub=1024*5+1024*(5+rtt)
 setup.append(dict(rtt_us=rtt,pair_serial_s=pair/1e6,pair_32core_ideal_s=pair/32e6,endpoint_channel_serial_s=ub/1e6,endpoint_channel_32core_ideal_s=ub/32e6))
groups=dict(host0=[0,1,2,3],host1=[4,5,6,7],TP=[[0,1],[2,3],[4,5],[6,7]],EP=[[0,2,4,6],[1,3,5,7]])
for group in groups['TP']:assert len({x//4 for x in group})==1
for group in groups['EP']:assert {x//4 for x in group}=={0,1}
files=['manuscripts/06-超节点.md']
out=dict(exercise='6-8',torus=tori,connection_state=state,setup=setup,groups=groups,scope='Declared connection-state and serial setup model with ideal 32-way scaling; schematic topology, not hardware benchmark',source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files})
(P/'6-8-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(state=state,setup=setup),indent=2))
