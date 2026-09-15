"""Exact link accounting, NUMA paths and a fully populated two-level fabric."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,importlib.util,itertools
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
s=importlib.util.spec_from_file_location('model',ROOT/'manuscripts/ch06/continuity_model.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
a=m.step(8,131064);b=m.step(16,131064,'measured_two_servers');threshold=(a['total_s']-max(b['local_s'],b['compute_s']))/128
assert abs(max(b['local_s'],b['compute_s'])+128*threshold-a['total_s'])<1e-14
ports=[dict(down=d,up=u,up_GBps=u*25,per_down_GBps=float(F(u*25,d)),oversubscription=float(F(d,u))) for d,u in ((32,32),(48,16))]
loads={f'{i}->{(i+1)%16}':[] for i in range(16)}
for src in range(16):
 for hop in range(4):loads[f'{(src+hop)%16}->{(src+hop+1)%16}'].append(src)
assert all(len(v)==4 for v in loads.values())
node=lambda rank:'A' if rank<2 else 'B'
numa=[]
for label,order,local in [('all_buffers_A',[0,1,2,3],False),('local_buffers_grouped',[0,1,2,3],True),('local_buffers_alternating',[0,2,1,3],True)]:
 transfers=[];traffic={'A->B':0,'B->A':0}
 for src,dst in zip(order,order[1:]+order[:1]):
  buf=node(src) if local else 'A';path=[node(src),buf,node(dst)];cross=[]
  for x,y in zip(path,path[1:]):
   if x!=y:traffic[x+'->'+y]+=12*2**20;cross.append(x+'->'+y)
  transfers.append(dict(src=src,dst=dst,buffer_node=buf,crossings=cross,bytes=12*2**20))
 numa.append(dict(label=label,order=order,transfers=transfers,UPI_bytes=traffic))
assert [x['UPI_bytes']['A->B']//2**20 for x in numa]==[24,12,24]
torus=[]
for side in (4,8):
 n=side**3;dist=[sum(min(v,side-v) for v in xyz) for xyz in itertools.product(range(side),repeat=3)]
 mean=F(sum(dist),n-1);load=mean/6
 torus.append(dict(side=side,cards=n,diameter=max(dist),mean_hops_other_destinations=str(mean),directed_links=6*n,per_link_M=str(load),manuscript_approx_mean_hops=3*side/4,manuscript_approx_per_link_M=side/8,physical_links=3*n))
# Six identical independent planes; each endpoint contributes one link per plane.
leaves=16;spines=8;parallel=4
assert leaves*32==512 and spines*parallel==32 and leaves*parallel==64
fabric=dict(planes=6,per_plane_leaf_chips=leaves,per_leaf_down_ports=32,per_leaf_up_ports=32,per_plane_spine_chips=spines,links_per_leaf_spine_pair=parallel,total_chips=6*(leaves+spines),endpoint_links=512*6,leaf_spine_links=6*leaves*32,total_physical_links=512*6+6*leaves*32)
files=['manuscripts/06-超节点.md','manuscripts/ch06/continuity_model.py','calculations/configs/hardware.json','calculations/configs/models/qwen3-32b/config.json','experiments/ch07/07-03/rows.csv']
out=dict(exercise='6-6',TP=dict(tp8_step_s=a['total_s'],tp16_local_s=b['local_s'],tp16_step_s=b['total_s'],measured_allreduce_s=b['allreduce_s'],equality_allreduce_s=threshold),ports=ports,third_round_clockwise_sources_per_link=loads,third_round_total_physical_MiB=64,numa=numa,torus=torus,fabric=fabric,scope='Analytical paths and byte counts; full-bisection routable fabric assumes striped traffic across equal-capacity planes and parallel uplinks; no multi-GPU runtime measurement',source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files})
(P/'6-6-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ('TP','ports','torus','fabric')},indent=2))
