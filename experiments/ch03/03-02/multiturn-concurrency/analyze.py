import hashlib,json
from pathlib import Path
r=Path(__file__).absolute().parent
load=lambda p:json.loads(p.read_text())
def lines(p):return list(map(json.loads,p.read_text().splitlines()))
for n,h in load(r/'reference-sha.json').items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h
summary={}
for mode in ['off','on']:
 s=load(r/(mode+'-run')/'supervisor.json');assert s['exit_code']==0 and not s['leftovers'] and s['reason'] is None
 rows=lines(r/mode/'requests.jsonl');assert len(rows)==12;by={x['id']:x for x in rows};assert len(by)==12
 ref={x['id']:x for x in lines(r/'reference'/mode/'requests.jsonl')};cases=[]
 for c in range(4):
  prev=None
  for turn in range(3):
   x=by[f'c{c}-t{turn}'];assert x['client']==c and x['turn']==turn
   if prev:assert x['messages'][:-1]==prev['messages']+[dict(role='assistant',content=prev['text'])]
   try:correct=json.loads(x['text'])==x['expected']
   except json.JSONDecodeError:correct=False
   assert x['events'][-1][1]==len(x['output_ids']) and 0<=x['cached_tokens']<=len(x['prompt_ids'])
   task=load(r/mode/'tasks.json')[c];assert x['expected']=={k:task['values'][k] for k in task['groups'][turn]}
   b=ref[x['id']];cases.append(dict(id=x['id'],correct=correct,cached_tokens=x['cached_tokens'],prompt_tokens=len(x['prompt_ids']),output_tokens=len(x['output_ids']),finish_reason=x['finish_reason'],same_prompt=x['prompt_ids']==b['prompt_ids'],same_output=x['output_ids']==b['output_ids']))
   prev=x
 waves=[]
 for turn in range(3):
  group=[x for x in rows if x['turn']==turn];assert len(group)==4 and max(x['start'] for x in group)<min(x['end'] for x in group)
  if turn:assert min(x['start'] for x in group)>=max(x['end'] for x in rows if x['turn']==turn-1)
  waves.append(dict(turn=turn,dispatch_span_s=max(x['start'] for x in group)-min(x['start'] for x in group),completion_span_s=max(x['end'] for x in group)-min(x['start'] for x in group)))
 stats=lines(r/mode/'scheduler.jsonl');assert stats
 cfg=load(r/mode/'environment.json')['config'];original=load(r/'reference'/mode/'environment.json')['config'];assert cfg.pop('max_num_seqs')==4 and original.pop('max_num_seqs')==1 and cfg==original
 summary[mode]=dict(requests=12,correct=sum(x['correct'] for x in cases),identical_reference_prompts=sum(x['same_prompt'] for x in cases),identical_reference_outputs=sum(x['same_output'] for x in cases),cached_tokens=sum(x['cached_tokens'] for x in cases),prompt_tokens=sum(x['prompt_tokens'] for x in cases),preemptions=sum(x['preemptions'] for x in stats),max_waiting=max(x['waiting'] for x in stats),max_running=max(x['running'] for x in stats),peak_kv_usage=max(x['kv_usage'] for x in stats),cases=cases,waves=waves)
(r/'analysis.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:{n:v for n,v in x.items() if n!='cases'} for k,x in summary.items()},indent=2))
