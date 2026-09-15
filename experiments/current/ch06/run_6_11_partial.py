"""Verified parts a,c,f; other subparts deliberately remain unfinished."""
from pathlib import Path
import json,hashlib,importlib.util,math
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
s=importlib.util.spec_from_file_location('supernode',ROOT/'calculations/supernode_inference.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
c=json.loads((ROOT/'calculations/scenarios/supernode-inference-example.json').read_text());arch=json.loads((ROOT/'calculations/results/supernode-inference-book.json').read_text());model=m.load_model(c)
assert model==arch['model']
rows=[]
for size,ref in zip(c['supernode_sizes'],arch['results']):
 baseline=m.evaluate(c,model,size)
 assert baseline==ref
 changed=m.evaluate(dict(c,tpot_s=.020),model,size)
 cap=changed['sessions'];n=changed['served']['sessions_per_card']
 assert changed['served']['step_s']<=.020
 assert n==cap or m.step_time(c,model,size,(n+1)*size)['step_s']>.020
 rows.append(dict(size=size,capacity_sessions=cap,weights_bytes=changed['weights_per_card_bytes'],served_20ms=n,step_s=changed['served']['step_s'],binding=changed['binding'],next_capacity_used_bytes=changed['weights_per_card_bytes']+c['workspace_bytes']+(cap+1)*model['kv_resident_bytes']))
base=m.evaluate(c,model,64,remote=8);newc=dict(c,remote_alpha_s=2e-6,nic_Bps=100e9)
remote=m.evaluate(newc,model,64,remote=8);local=m.evaluate(c,model,64)
assert base['served']==arch['rdma']['served']
# Compare identical batch, not a speedup manufactured by reducing sessions.
assert remote['served']['sessions_per_card']==local['served']['sessions_per_card']
lookup=[]
for name,step in [('H100',arch['gpu_row']['token_s']),('ROM',arch['rom']['rows'][0]['token_s'])]:
 window=step/model['layers'];threshold=model['layers']*2e-6
 assert math.isclose(threshold/model['layers'],2e-6)
 lookup.append(dict(machine=name,baseline_step_s=step,baseline_hide_window_s=window,rtt_s=2e-6,critical_step_s=threshold,critical_tokens_s=1/threshold,baseline_lookup_hidden=2e-6<=window))
files=['manuscripts/06-超节点.md','calculations/supernode_inference.py','calculations/scenarios/supernode-inference-example.json','calculations/results/supernode-inference-book.json','calculations/configs/hardware.json',c['opentallas']['excerpt']]
# All consumed model headers and local model/KV implementations are pinned as evidence.
files+= [str(x.relative_to(ROOT)) for x in (ROOT/'calculations/sources/deepseek-v4.1-flash').rglob('*') if x.is_file() and (x.name.endswith('.header.bin') or x.name=='model.safetensors.index.json')]
files+= ['calculations/src/infra_calc/topics/kv_comparison.py','calculations/src/infra_calc/topics/v41_forward.py']
out=dict(exercise='6-11',completed_parts=['a','c','f'],pending_parts=['b','d','e'],capacity_20ms=rows,remote64=dict(original_step_s=base['served']['step_s'],new_step_s=remote['served']['step_s'],new_comm_s=remote['served']['comm_s'],local_step_s=local['served']['step_s'],local_comm_s=local['served']['comm_s'],sessions_per_card=remote['served']['sessions_per_card'],matches_local=remote['served']['step_s']<=local['served']['step_s']),engram=lookup,source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files})
(P/'6-11-partial-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'},indent=2))
