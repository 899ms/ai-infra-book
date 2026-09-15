"""Verify SwiGLU partition identities and deterministic pipeline schedules."""
from pathlib import Path
import json,hashlib,importlib.util
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
spec=importlib.util.spec_from_file_location('continuity',ROOT/'manuscripts/ch06/continuity_model.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
rng=np.random.default_rng(602);X=rng.normal(size=(6,4));g=rng.normal(size=(4,8));u=rng.normal(size=(4,8));down=rng.normal(size=(8,4))
silu=lambda x:x/(1+np.exp(-x))
full=(silu(X@g)*(X@u))@down
parts=[(silu(X@g[:,i:i+4])*(X@u[:,i:i+4]))@down[i:i+4,:] for i in (0,4)]
combined=parts[0]+parts[1];assert np.allclose(combined,full,atol=1e-12,rtol=1e-12)
# Reduce-scatter on token rows; pointwise residual and per-row RMSNorm stay local.
residual=rng.normal(size=full.shape)
norm=lambda x:x/np.sqrt(np.mean(x*x,axis=1,keepdims=True)+1e-6)
shards=[combined[:3],combined[3:]]
local=[norm(shards[i]+residual[i*3:(i+1)*3]) for i in range(2)]
assert np.allclose(np.concatenate(local),norm(full+residual),atol=1e-12,rtol=1e-12)
rows=[]
for p in (1,2,4,8):
 s=m.step(p,131064);rows.append(dict(tp=p,local_ms=s['local_s']*1000,communication_ms=s['communication_s']*1000,total_ms=s['total_s']*1000,compute_ms=s['compute_s']*1000,capacity_sessions=m.max_sessions(p,131072)))
for i,r in enumerate(rows):
 r['local_speedup']=rows[0]['local_ms']/r['local_ms'];r['total_speedup']=rows[0]['total_ms']/r['total_ms'];r['local_saved_on_doubling_ms']=None if i==0 else rows[i-1]['local_ms']-r['local_ms'];r['total_saved_on_doubling_ms']=None if i==0 else rows[i-1]['total_ms']-r['total_ms']
schedules=[]
for duration in ([1,1,1,1],[1,1,2,1]):
 end=np.zeros((4,8),dtype=int);events=[]
 for stage in range(4):
  for batch in range(8):
   ready=int(end[stage-1,batch]) if stage else 0
   start=max(ready,int(end[stage,batch-1]) if batch else 0);finish=start+duration[stage];end[stage,batch]=finish
   events.append(dict(stage=stage+1,micro_batch=batch+1,ready_ms=ready,start_ms=start,end_ms=finish,queue_ms=start-ready))
 assert int(end[-1,-1])==sum(duration)+7*max(duration)
 schedules.append(dict(stage_ms=duration,total_ms=int(end[-1,-1]),events=events))
fig,axes=plt.subplots(2,1,figsize=(11,5.6),layout='constrained')
for ax,s in zip(axes,schedules):
 for e in s['events']:
  ax.barh(e['stage'],e['end_ms']-e['start_ms'],left=e['start_ms'],height=.72,color=plt.cm.tab10((e['micro_batch']-1)%10))
  ax.text((e['start_ms']+e['end_ms'])/2,e['stage'],str(e['micro_batch']),ha='center',va='center',fontsize=8)
 ax.set(yticks=[1,2,3,4],yticklabels=['Stage 1','Stage 2','Stage 3','Stage 4'],xlim=(0,20),xticks=range(21),xlabel='Time (ms)',title=f"Stage durations {s['stage_ms']} ms; finish {s['total_ms']} ms")
 ax.invert_yaxis();ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True)
fig.savefig(P/'6-2-pipeline.png',dpi=150);fig.savefig(P/'6-2-pipeline.svg');plt.close(fig)
sources=['manuscripts/06-超节点.md','manuscripts/ch06/continuity_model.py','calculations/configs/models/qwen3-32b/config.json','calculations/configs/hardware.json']
out=dict(exercise='6-2',tensor_check=dict(seed=602,shape=[6,4,8],max_abs_error=float(np.max(np.abs(full-combined))),row_sharded_norm_max_abs_error=float(np.max(np.abs(np.concatenate(local)-norm(full+residual))))),TP=rows,pipelines=schedules,scope='FP64 small-tensor partition verification, analytic H100 first step and zero-transfer-latency forward pipeline, not physical multi-GPU execution',source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in sources})
(P/'6-2-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(rows,indent=2));print('Pipeline finishes:',[s['total_ms'] for s in schedules])
