import hashlib,json
from pathlib import Path
import numpy as np
import torch
r=Path(__file__).absolute().parent;p=r/'results';torch.set_num_threads(4)
info=json.loads((p/'capture-info.json').read_text());assert len(info)==1
assert info[0]['observer_sha256']==hashlib.sha256((r/'capture_probe.py').read_bytes()).hexdigest()
env=json.loads((p/'environment.json').read_text());assert env['driver_sha256']==hashlib.sha256((r/'run.py').read_bytes()).hexdigest()
requests={x['id']:x for x in map(json.loads,(p/'requests.jsonl').read_text().splitlines())};ref={x['id']:x for x in map(json.loads,(r/'reference/requests.jsonl').read_text().splitlines())}
cases=json.loads((p/'cases.json').read_text());assert len(requests)==len(cases)==4
records=[json.loads(x) for x in (p/'activations.jsonl').read_text().splitlines()];summaries=[];first_inputs=[]
for c in cases:
 name=c['id'];req=requests[name];assert json.loads(req['text'])==c['expected']
 assert req['prompt_ids']==ref[name]['prompt_ids'] and req['output_ids']==ref[name]['output_ids']
 routes=np.load(p/req['route_file']);reference=np.load(r/'reference'/ref[name]['route_file']);assert np.array_equal(routes,reference)
 group=[x for x in records if x['case']==name];assert [x['step'] for x in group]==list(range(len(group)))
 all_ids=[];selected=0;tokens=0
 for row in group:
  data=torch.load(p/row['file'],map_location='cpu',weights_only=True);ids=data['topk_ids'];pos=(ids==0).any(dim=1).nonzero().flatten()
  assert torch.equal(pos,data['token_positions'])
  x=data['input_bf16'];assert x.dtype==torch.bfloat16 and x.shape==(len(pos),2048)
  assert row['selected_rows']==len(pos) and row['input_rows']==ids.shape[0] and not row['apply_router_weight_on_input']
  assert row['prepared_dtype']=='torch.float8_e4m3fn'
  all_ids.append(ids.numpy());selected+=len(pos);tokens+=ids.shape[0]
  if name=='n512-r0':first_inputs.append(x)
 assert np.array_equal(np.concatenate(all_ids).astype(np.uint8),routes[:,0,:])
 assert tokens==7280 and selected==int((routes[:,0,:]==0).sum())
 summaries.append(dict(case=name,calls=len(group),tokens=tokens,selected_rows=selected,outputs_and_routes_equal=True))
w=torch.load(p/'runtime-expert.pt',map_location='cpu',weights_only=True);old=torch.load(r/'reference-expert.pt',map_location='cpu',weights_only=True)
assert torch.equal(w['weight'].T.contiguous().view(torch.uint8),old['checkpoint_fp8'].view(torch.uint8))
assert torch.equal(w['scale'].T.contiguous(),old['checkpoint_scale'])
x=torch.cat(first_inputs);assert x.shape[0]>=512
if (r/'activation-pool.pt').exists():assert torch.equal(torch.load(r/'activation-pool.pt',map_location='cpu',weights_only=True)['input_bf16'],x)
else:torch.save(dict(input_bf16=x,case='n512-r0',selection='All native layer-0 expert-0 routed rows, original call/token order; timing uses first M rows'),r/'activation-pool.pt')
result=dict(cases=summaries,total_calls=len(records),selected_rows=sum(x['selected_rows'] for x in summaries),runtime_weight_matches_checkpoint_transpose=True,
 activation_pool_rows=x.shape[0],scope='Read-only observer; full outputs and all 48-layer routes match prior 4GiB-KV reference; current KV budget 2GiB; no performance attribution across runs.')
(r/'capture-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
