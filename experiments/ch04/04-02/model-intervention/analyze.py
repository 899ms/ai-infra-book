"""Strict full-answer quality and independent CPU FP64 replacement audit."""
import hashlib,json
from pathlib import Path
import torch,numpy as np
r=Path(__file__).absolute().parent;torch.set_num_threads(4)
load=lambda p:json.loads(p.read_text())
requests=[json.loads(x) for x in (r/'results/requests.jsonl').read_text().splitlines()]
ref={x['id']:x for x in map(json.loads,(r/'reference/requests.jsonl').read_text().splitlines())}
tasks={x['id']:x for x in load(r/'tasks.json')}
assert len(requests)==8 and len({x['id'] for x in requests})==8
rows=[]
for x in requests:
 mode,key=x['id'].split('-',1);base=ref[key]
 try:answer=json.loads(x['text'])
 except json.JSONDecodeError:answer=None
 routes=np.load(r/'results'/x['route_file']);br=np.load(r/'reference'/base['route_file'])
 assert routes.shape[1:]==(48,8) and x['prompt_ids']==base['prompt_ids']
 rows.append(dict(id=x['id'],correct=answer==tasks[key]['expected'],finish_reason=x['finish_reason'],output_tokens=len(x['output_ids']),output_identical=x['output_ids']==base['output_ids'],routes_identical=np.array_equal(routes,br),layer0_routes_identical=np.array_equal(routes[:,0],br[:,0]),changed_route_slots=int((routes!=br).sum()) if routes.shape==br.shape else None))
w=torch.load(r/'reference-expert.pt',weights_only=True,map_location='cpu');qw=w['int8_weight'].double();sw=w['int8_scale'].double();dw=qw*sw
records=list(map(json.loads,(r/'results/interventions.jsonl').read_text().splitlines()));audit=[]
for rec in records:
 t=torch.load(r/'results'/rec['file'],weights_only=True,map_location='cpu');ids=t['topk_ids'];pos=(ids==0).nonzero()
 assert torch.equal(pos,t['positions']) and rec['unselected_exact'] and rec['weight_verified']
 x=t['input_bf16'].float();m=x.shape[0]
 assert m==rec['selected_rows'] and t['replacement'].shape==(m,1536)
 error=0.
 if m:
  v=x.reshape(m,16,128);sx=v.abs().amax(2,keepdim=True).clamp_min(1e-12)/127;q=(v/sx).round().clamp(-127,127)
  dx=(q*sx).reshape(m,2048)
  if rec['mode']=='dequant':dx=dx.to(torch.bfloat16).double();weight=dw.to(torch.bfloat16).double()
  else:dx=dx.double();weight=dw
  expected=dx@weight;actual=t['replacement'].double();error=float(torch.linalg.vector_norm(actual-expected)/torch.linalg.vector_norm(expected))
  assert error<.004,(rec['file'],error)
 audit.append(dict(file=rec['file'],selected_rows=m,relative_l2_vs_cpu_fp64=error))
for x in rows:
 recs=[z for z in records if z['case']==x['id']];assert recs and sum(z['selected_rows'] for z in recs)>0
 assert [z['step'] for z in recs]==list(range(len(recs)))
 x['calls']=len(recs);x['selected_rows']=sum(z['selected_rows'] for z in recs)
 captured=torch.cat([torch.load(r/'results'/z['file'],weights_only=True,map_location='cpu')['topk_ids'] for z in recs]).numpy()
 request=next(z for z in requests if z['id']==x['id']);routes=np.load(r/'results'/request['route_file'])
 assert np.array_equal(captured,routes[:,0,:]),'captured assignment rows differ from returned layer-0 routes'
 x['changed_output_calls']=sum(not torch.equal((t:=torch.load(r/'results'/z['file'],weights_only=True,map_location='cpu'))['native'],t['replacement']) for z in recs)
 assert x['changed_output_calls']>0
s=dict(cases=rows,intervention_calls=len(records),selected_rows=sum(x['selected_rows'] for x in records),max_cpu_audit_relative_l2=max(x['relative_l2_vs_cpu_fp64'] for x in audit),tensor_audit=audit,scope='Four frozen retrieval tasks, one layer/expert gate_up only. Not whole-model INT8 or performance evidence.')
(r/'analysis.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps({k:v for k,v in s.items() if k!='tensor_audit'},indent=2))
