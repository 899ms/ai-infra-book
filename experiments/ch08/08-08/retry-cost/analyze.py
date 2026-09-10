import hashlib,json,math,re,statistics
from pathlib import Path
r=Path(__file__).absolute().parent;p=r/'results';env=json.loads((p/'environment.json').read_text())
for n,h in env['hashes'].items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h
assert hashlib.sha256((p/'inputs.json').read_bytes()).hexdigest()==env['input_sha256']
inp=json.loads((p/'inputs.json').read_text());tasks={x['id']:x for x in inp['tasks']};assert len(tasks)==16
for t in tasks.values():
 doc=dict(re.findall(r'^(k\d{4}) = (\d{6})$',t['messages'][1]['content'],re.M));assert len(doc)==512
 assert all(doc[k]==v for k,v in t['expected'].items());assert len(t['prompt_token_ids'])==7239
 assert t['seed']==8808000+int(t['id'].split('-')[1])
ref=json.loads((r/'reference-snapshot.json').read_text());snap=json.loads((p/'snapshots.json').read_text())
assert snap['weights']==ref['weights']
assert snap['armed']==snap['observed_layers']==[36]
assert snap['calibrated'][0]['scales']==snap['after'][0]['scales']==ref['after_calibration'][0]['scales']
assert all(not x['calculate'] and math.isfinite(x['k']) and math.isfinite(x['v']) for x in snap['after'][0]['scales'])
a=[json.loads(x) for x in (p/'attempts.jsonl').read_text().splitlines()];attempts={x['id']:x for x in a};assert len(a)==len(attempts)
t=[json.loads(x) for x in (p/'tasks.jsonl').read_text().splitlines()];assert len(t)==32
assert [x['task_id'] for x in t]==[f'heldout-{i:02d}' for order in inp['orders'] for i in order]
assert {(x['trial'],x['task_id']) for x in t}=={(i,k) for i in [0,1] for k in tasks}

def strict(text,expected):
 def unique(pairs):
  d={}
  for k,v in pairs:
   if k in d:raise ValueError()
   d[k]=v
  return d
 try:return json.loads(text,object_pairs_hook=unique)==expected
 except (ValueError,TypeError):return False

used=[];rows=[]
for task in t:
 ids=task['attempt_ids'];assert len(ids) in [1,2];group=[attempts[k] for k in ids];used+=ids
 assert ids[0]==task['id']+'-first'
 first,last=group[0],group[-1]
 assert len(group)==(1 if first['correct'] else 2)
 assert task['first_correct']==first['correct'] and task['final_correct']==last['correct']
 for j,x in enumerate(group):
  assert x['task_id']==task['task_id'] and x['mode']==('fp8' if j==0 else 'bf16')
  assert x['correct']==strict(x['text'],tasks[task['task_id']]['expected'])
  assert task['start_s']<=x['start_s']<=x['end_s']<=x['check_begin_s']<=x['check_end_s']<=task['end_s']
  q=x['q_observation'];assert len(q)==1 and len(q[0])==36
  expected='torch.float8_e4m3fn' if j==0 else 'torch.bfloat16'
  assert all(k.endswith(':'+expected) and n>0 for k,n in q[0].items())
  if j:assert x['id']==task['id']+'-retry' and group[j-1]['check_end_s']<=x['start_s']
 total=task['end_s']-task['start_s'];generation=sum(x['end_s']-x['start_s'] for x in group);assert total>=generation
 rows.append(dict(id=task['id'],task_id=task['task_id'],trial=task['trial'],attempts=len(group),first_correct=first['correct'],final_correct=last['correct'],
  total_s=total,first_generation_s=first['end_s']-first['start_s'],generation_s=generation,overhead_s=total-generation,
  tokens=sum(len(x['output_ids']) for x in group),first_tokens=len(first['output_ids']),finish_reasons=[x['finish_reason'] for x in group]))
assert len(used)==len(set(used)) and set(attempts)-set(used)=={'calibration','warm-fp8','warm-bf16'}
repeat_differences=[k for k,x in attempts.items() if k.startswith('0-') and '1-'+k[2:] in attempts and x['output_ids']!=attempts['1-'+k[2:]]['output_ids']]
summary=dict(repeat_output_differences=repeat_differences,tasks=32,distinct_documents=16,first_correct=sum(x['first_correct'] for x in rows),final_correct=sum(x['final_correct'] for x in rows),
 retries=sum(x['attempts']==2 for x in rows),total_model_calls=len(a),formal_model_calls=len(used),
 formal_total_s=sum(x['total_s'] for x in rows),formal_generation_s=sum(x['generation_s'] for x in rows),
 first_generation_s=sum(x['first_generation_s'] for x in rows),all_output_tokens=sum(x['tokens'] for x in rows),first_output_tokens=sum(x['first_tokens'] for x in rows),
 successful_task_total_s=sum(x['total_s'] for x in rows if x['final_correct']),
 failed_task_total_s=sum(x['total_s'] for x in rows if not x['final_correct']),
 median_success_s=statistics.median(x['total_s'] for x in rows if x['final_correct']) if any(x['final_correct'] for x in rows) else None,
 records=rows,scope='Known-answer synthetic validator; includes actual failed attempts, switching and observation RPC overhead; excludes engine initialization, calibration and warmup. Serial tasks on shared GPU.')
(p/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='records'},indent=2))
