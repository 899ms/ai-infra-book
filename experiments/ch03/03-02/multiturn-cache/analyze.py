import json,hashlib,statistics
from pathlib import Path
r=Path(__file__).absolute().parent
def load(p):return json.loads(p.read_text())
def lines(p):return list(map(json.loads,p.read_text().splitlines()))
def lcp(a,b):
 for i,(x,y) in enumerate(zip(a,b)):
  if x!=y:return i
 return min(len(a),len(b))
allrows={};summary={}
for mode in ['off','on','grouped']:
 sup=load(r/(mode+'-run')/'supervisor.json');assert sup['exit_code']==0 and sup['reason'] is None and not sup['leftovers']
 rows=lines(r/mode/'requests.jsonl');assert len(rows)==12 and [x['id'] for x in rows]==([f'c{c}-t{t}' for c in range(4) for t in range(3)] if mode=='grouped' else [f'c{c}-t{t}' for t in range(3) for c in range(4)])
 prior={};out=[]
 for x in rows:
  c=x['client'];history=x['messages'];assert len(history)==2+2*x['turn']
  previous=prior.get(c)
  if previous:
   assert history[:-1]==previous['messages']+[dict(role='assistant',content=previous['text'])]
   prefix=lcp(previous['prompt_ids'],x['prompt_ids'])
  else:prefix=0
  expected=load(r/mode/'tasks.json')[c]['values'];assert all(expected[k]==v for k,v in x['expected'].items())
  try:correct=json.loads(x['text'])==x['expected']
  except json.JSONDecodeError:correct=False
  assert x['events'][-1][1]==len(x['output_ids']) and 0<=x['cached_tokens']<=len(x['prompt_ids'])
  if mode=='off':assert x['cached_tokens']==0
  out.append(dict(id=x['id'],correct=correct,finish_reason=x['finish_reason'],prompt_tokens=len(x['prompt_ids']),output_tokens=len(x['output_ids']),cached_tokens=x['cached_tokens'],previous_prompt_lcp=prefix,wall_s=x['end']-x['start']))
  prior[c]=x
 stats=lines(r/mode/'scheduler.jsonl');assert stats
 summary[mode]=dict(correct=sum(x['correct'] for x in out),requests=12,cached_tokens=sum(x['cached_tokens'] for x in out),prompt_tokens=sum(x['prompt_tokens'] for x in out),preemptions=sum(x['preemptions'] for x in stats),max_waiting=max(x['waiting'] for x in stats),peak_kv_usage=max(x['kv_usage'] for x in stats),cases=out)
 allrows[mode]=rows
cfg=[load(r/m/'environment.json')['config'] for m in ['off','on']];cfg[0].pop('enable_prefix_caching');cfg[1].pop('enable_prefix_caching');assert cfg[0]==cfg[1]
summary['comparison']=dict(identical_prompts=sum(x['prompt_ids']==y['prompt_ids'] for x,y in zip(allrows['off'],allrows['on'])),identical_outputs=sum(x['output_ids']==y['output_ids'] for x,y in zip(allrows['off'],allrows['on'])),scope='Four synthetic clients, actual answer history, fixed sequential round robin; not production ServeGen or latency ranking')
on={x['id']:x for x in allrows['on']};group={x['id']:x for x in allrows['grouped']}
assert load(r/'on/environment.json')['config']==load(r/'grouped/environment.json')['config']
summary['grouped_comparison']=dict(identical_prompts=sum(on[k]['prompt_ids']==group[k]['prompt_ids'] for k in on),identical_outputs=sum(on[k]['output_ids']==group[k]['output_ids'] for k in on))
(r/'analysis.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:{n:v for n,v in x.items() if n!='cases'} for k,x in summary.items()},indent=2))
