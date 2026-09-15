"""Reconstruct exact ROM communication and context-dependent KV capacities."""
from pathlib import Path
import json,math,hashlib,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[2];sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.topics import kv_comparison
from infra_calc.sources import model_config
ex=json.loads((ROOT/'calculations/sources/opentallas/v41-flash-roofline-n5-vs-b200.json').read_text());arch=json.loads((ROOT/'calculations/results/supernode-inference-book.json').read_text());r=arch['rom']['rows'][0]
links=ex['technology']['links'];hidden=ex['model_summary']['hidden_size'];activation=hidden*2
alpha=links['on_wafer_n5']['hop_latency_s']['value'];bw=links['on_wafer_n5']['bytes_s']['value'];span=57
traversals=1.1*2*(math.ceil(math.sqrt(span))-1)
on_latency=80*traversals*alpha;on_transfer=80*activation*3*(span-1)/span/bw
inter_latency=links['inter_wafer']['hop_latency_s']['value'];inter_transfer=activation/links['inter_wafer']['bytes_s']['value']
old=on_latency+on_transfer+inter_latency+inter_transfer
assert math.isclose(old,r['link_s'],abs_tol=1e-15)
new=on_latency/2+on_transfer+inter_latency+inter_transfer
service=max(r['weight_read_s'],r['kv_read_s'],r['compute_s'])/.9
assert math.isclose(service,r['storage_compute_s'],abs_tol=1e-15)
total=service+new+r['fixed_s']
cfg=model_config('deepseek-v4.1-flash');cfg=cfg.get('text_config',cfg)
kv=[]
for n in (200000,1000000,1048576):
 row=next(x for x in kv_comparison.calculate(n,1)['rows'] if x['model']=='deepseek-v4.1-flash')
 # Independently reproduce compressed owner history and fixed SWA window.
 global_bytes=sum(n//cfg['compress_ratios'][layer]*356 for layer in cfg['kv_source_layer_ids'])
 local_bytes=cfg['num_hidden_layers']*min(n,cfg['sliding_window'])*528
 assert global_bytes==row['global_history_bytes'] and local_bytes==row['local_window_bytes']
 state=global_bytes+local_bytes;capacities=[]
 for design in arch['rom']['rows'][:2]:
  cap=int(design['kv_capacity_bytes']);count=cap//state
  assert count*state<=cap<(count+1)*state
  if n==200000:assert count==int(design['resident_sessions'])
  capacities.append(dict(store=design['kv_store'],capacity_bytes=cap,sessions=count,next_session_bytes=(count+1)*state))
 kv.append(dict(context_tokens=n,global_bytes=global_bytes,window_bytes=local_bytes,state_bytes=state,capacity=capacities))
files=['calculations/configs/models/deepseek-v4.1-flash/config.json','manuscripts/06-超节点.md','calculations/sources/opentallas/v41-flash-roofline-n5-vs-b200.json','calculations/results/supernode-inference-book.json','calculations/src/infra_calc/topics/kv_comparison.py','experiments/current/ch06/sources/opentallas-roofline.py']
out=dict(exercise='6-11',completed_parts=['d','e'],ROM=dict(on_wafer_latency_s=on_latency,on_wafer_payload_s=on_transfer,inter_wafer_latency_s=inter_latency,inter_wafer_payload_s=inter_transfer,old_communication_s=old,new_communication_s=new,storage_compute_s=service,fixed_s=r['fixed_s'],new_token_s=total,new_tokens_s=1/total,new_communication_share=new/total),KV=kv,scope='Fixed original ROM/HBM/SRAM capacities, no redesign; decimal 1M primary and binary 1Mi alternative; halve only on-wafer propagation, preserve payload and off-wafer latency',source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files})
(P/'6-11-de-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'},indent=2))
