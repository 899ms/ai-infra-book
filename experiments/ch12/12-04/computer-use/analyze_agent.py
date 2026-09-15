import hashlib,json,statistics
from pathlib import Path
R=Path(__file__).resolve().parent
summary={}
for label,agent,server in [('unconstrained','agent-results','server-results'),('structured','structured-agent-results','structured-server-results')]:
 A=R/agent;S=R/server
 rows=[json.loads(s) for s in (S/'raw.jsonl').read_text().splitlines()];byid={r['id']:r for r in rows};assert len(byid)==len(rows)
 env=json.loads((S/'environment.json').read_text());source='server.py' if label=='unconstrained' else 'server_structured.py';assert env['source_sha256']==hashlib.sha256((R/source).read_bytes()).hexdigest()
 warm=json.loads((A/'warmup.json').read_text());assert warm['response']==byid['warmup'] and len(byid['warmup']['output_ids'])==1
 trials=[];count=1
 for trial in range(3):
  D=A/f'trial{trial}';result=json.loads((D/'result.json').read_text());records=[json.loads(p.read_text()) for p in sorted(D.glob('step*.json'))];history=[]
  for step,r in enumerate(records):
   count+=1;response=r['response'];assert response==byid[f't{trial}-s{step}']
   assert r['screenshot_sha256']==response['image_sha256']==hashlib.sha256((D/f'step{step:02d}.png').read_bytes()).hexdigest()
   assert response['image_size']==[1280,960] and response['start_s']<=response['end_s']
   assert r['screenshot_start_s']<=r['screenshot_end_s']<=r['request_start_s']<=r['response_end_s']
   assert r['request_instruction'].split('Previous actions: ')[1]==json.dumps(history)
   assert r['request_instruction'] in response['prompt']
   if 'action' in r:
    assert json.loads(response['text'])==r['action'];history.append(r['action']);assert r['response_end_s']<=r['action_start_s']<=r['action_end_s']
   else:assert 'action_error' in r
  assert history==result['actions'];assert result['passed']==(result['final_state']==result['target'])
  trials.append(dict(trial=trial,passed=result['passed'],reason=result['reason'],steps=len(records),elapsed_s=result['elapsed_s'],model_service_s=sum(r['response']['end_s']-r['response']['start_s'] for r in records),final_state=result['final_state']))
 assert len(rows)==count
 summary[label]=dict(trials=trials,successes=sum(t['passed'] for t in trials),formal_model_calls=count-1,median_task_s=statistics.median(t['elapsed_s'] for t in trials))
(R/'agent-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
