"""Paired RPC evidence with separate, unsynchronized host timelines."""
from pathlib import Path
import hashlib,json,statistics as st
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;ROOT=P.parents[2];raw=ROOT/'experiments/ch07/07-04';source=next((ROOT/'manuscripts').glob('07-*.md'))
for name,h in json.loads((raw/'results/raw-manifest.json').read_text()).items():assert hashlib.sha256((raw/name).read_bytes()).hexdigest()==h
rows=[json.loads(s) for s in (raw/'results/client/requests.jsonl').read_text().splitlines()];server={r['id']:r for r in map(json.loads,(raw/'results/server/requests.jsonl').read_text().splitlines())}
selected=[];pairs=[]
ck=['start_ns','encode_end_ns','prepare_end_ns','send_end_ns','receive_end_ns','end_ns'];cn=['Encode','Prepare','Send call','Response wait','Decode + verify']
sk=['recv_start_ns','recv_end_ns','decode_start_ns','decode_end_ns','submit_ns','worker_start_ns','worker_end_ns','complete_observed_ns'];sn=['Receive body','Dispatch gap','Decode/materialize','Submit gap','Queue','Execute SHA256','Completion notice']
def timeline(r,keys,names):
 t=[r[k] for k in keys];assert t==sorted(t)
 return [dict(stage=n,start_ms=(a-t[0])/1e6,duration_ms=(b-a)/1e6) for n,a,b in zip(names,t,t[1:])]
for trial in range(20):
 pair=[next(r for r in rows if r['size']==2**20 and r['trial']==trial and r['mode']==m) for m in (0,1)]
 assert pair[0]['payload_sha256']==pair[1]['payload_sha256']
 for r in pair:assert r['server']==server[r['id']]
 durations=[(r['end_ns']-r['start_ns'])/1e6 for r in pair]
 pairs.append(dict(trial=trial,ids=[r['id'] for r in pair],json_ms=durations[0],binary_ms=durations[1],saved_ms=durations[0]-durations[1]))
 if trial==0:
  for r in pair:
   ct=timeline(r,ck,cn);sv=timeline(r['server'],sk,sn);total=(r['end_ns']-r['start_ns'])/1e6
   assert abs(sum(v['duration_ms'] for v in ct)-total)<1e-9
   f=ct[0]['duration_ms']/total
   selected.append(dict(id=r['id'],mode=r['name'],payload_sha256=r['payload_sha256'],client=ct,server=sv,total_ms=total,client_cpu_ms=r['client_cpu_ns']/1e6,request_bytes=r['request_application_bytes'],encode_fraction=f,client_encode_only_zero_cost_speedup=1/(1-f)))
n=2**20;base64_bytes=4*((n+2)//3);assert base64_bytes==1398104
assert selected[0]['request_bytes']==17+14+base64_bytes and selected[1]['request_bytes']==17+n
byte_info=dict(payload_bytes=n,base64_bytes=base64_bytes,base64_only_saved_bytes=base64_bytes-n,json_wrapper_bytes=14,frame_bytes=17,total_request_saved_bytes=selected[0]['request_bytes']-selected[1]['request_bytes'],fraction_original_request_saved=(selected[0]['request_bytes']-selected[1]['request_bytes'])/selected[0]['request_bytes'])
files=[source,raw/'client.py',raw/'server.py',raw/'results/raw-manifest.json',raw/'results/client/requests.jsonl',raw/'results/server/requests.jsonl']
out=dict(exercise='7-7',selection='First formal 1MiB trial (trial 0), modes JSON copy worker and binary copy worker; no timing-based selection',selected=selected,bytes=byte_info,all_20_pairs=pairs,binary_faster_pairs=sum(r['saved_ms']>0 for r in pairs),median_paired_saved_ms=st.median(r['saved_ms'] for r in pairs),clock_caveat='Separate host-relative origins; server timestamps cannot be positioned inside client send/wait without clock alignment. Server execution is already part of the RPC critical path.',source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
(P/'7-7-results.json').write_text(json.dumps(out,indent=2)+'\n')
fig,axes=plt.subplots(2,2,figsize=(12,6))
colors=plt.get_cmap('tab10').colors
for col,r in enumerate(selected):
 for row,key in enumerate(('client','server')):
  ax=axes[row,col]
  for i,v in enumerate(r[key]):ax.barh(i,v['duration_ms'],left=v['start_ms'],color=colors[i])
  ax.set_yticks(range(len(r[key])),[v['stage'] for v in r[key]]);ax.invert_yaxis();ax.set_xlabel(f"ms from this {key}'s first recorded event");ax.grid(axis='x',alpha=.2)
  ax.set_title(f"{r['mode']} — {key}")
  limit=max(sum(v['duration_ms'] for v in q[key]) for q in selected)*1.15
  ax.set_xlim(0,limit)
  for i,v in enumerate(r[key]):ax.text(v['start_ms']+v['duration_ms']+limit*.006,i,f"{v['duration_ms']:.3f}",va='center',fontsize=7)
fig.suptitle('Same 1 MiB payload, first formal pair; host clocks are NOT aligned')
fig.tight_layout();fig.savefig(P/'7-7-timelines.png',dpi=160);fig.savefig(P/'7-7-timelines.svg');plt.close(fig)
print(json.dumps(dict(selected=selected,bytes=byte_info,binary_faster_pairs=out['binary_faster_pairs'],median_paired_saved_ms=out['median_paired_saved_ms']),indent=2))
