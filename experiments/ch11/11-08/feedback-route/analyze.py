import hashlib,json,random,statistics
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'results'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ex=read(R/'execution.json');env=read(O/'environment.json');rows=[json.loads(l) for l in (O/'raw.jsonl').read_text().splitlines()];assert ex['exit_code']==0 and not ex['after_gpu'].strip() and len(rows)==8
for n,h in env['source_hashes'].items():assert sha(R/n)==h
rng=random.Random(1107);order=[]
for rep in range(2):
 a=[dict(rep=rep,thinking=False,budget=1000,warm=w,busy=b) for w in [False,True] for b in [False,True]];rng.shuffle(a);order+=a
assert order==read(O/'order.json');records=[]
def verify_result(result,path):
 if 'validation' in result:
  c=json.loads(result['validation']['stdout']);assert len(c['cases'])==6
  passed=all(x.get('actual')==x['expected'] and x.get('unchanged') is True for x in c['cases']);assert passed==c['passed']==result['passed'];assert sha(path)==result['write']['sha256']
 else:assert not result['passed']
for i,(r,c) in enumerate(zip(rows,order)):
 assert r==read(O/f'case{i}/record.json') and r['index']==i and all(r[k]==v for k,v in c.items())
 initial=r['initial_stage'];first=initial['target'];last=r['target'];retry=not initial['result']['passed'];calls=[first,last] if retry else [first]
 verify_result(initial['result'],O/f'case{i}/initial-candidate.py');verify_result(r['result'],O/f'case{i}/intervals.py')
 for t in calls:
  assert len(t['output_ids'])<=1000 and t['metrics']['num_generation_tokens']==len(t['output_ids']) and not t['metrics']['is_corrupted'] and t['events'][-1]['token_count']==len(t['output_ids'])
 if retry:assert first['end_s']<=initial['done_s']<=last['start_s'] and len(last['input_ids'])>len(first['input_ids'])
 if c['warm']:assert r['warmup']['input_ids']==first['input_ids'] and len(r['warmup']['output_ids'])==1 and first['cached_tokens']>0
 else:assert r['warmup'] is None and first['cached_tokens']==0
 m=first['metrics'];queue=m['scheduled_ts']-m['queued_ts'];assert queue>=0
 if c['busy']:
  b=r['background'];assert len(b['output_ids'])==128 and b['events'][0]['time_s']<=first['start_s']<b['end_s'] and m['scheduled_ts']>=b['metrics']['last_token_ts'] and queue>.1
 else:assert r['background'] is None
 total=r['done_s']-first['start_s'];assert r['verified_usable_s']==(total if r['result']['passed'] else None)
 records.append(dict(index=i,**c,initial_passed=initial['result']['passed'],attempts=len(calls),passed=r['result']['passed'],input_tokens=sum(len(t['input_ids']) for t in calls),output_tokens=sum(len(t['output_ids']) for t in calls),cached_tokens=sum(t['cached_tokens'] for t in calls),reasoning_tokens=0,queue_s=queue,first_token_s=first['events'][0]['time_s']-first['start_s'],first_answer_segment_s=first['events'][0]['time_s']-first['start_s'],total_s=total,verified_usable_s=r['verified_usable_s']))
result=dict(status='bounded_feedback_route_verified',logical_tasks=8,generation_attempts=sum(x['attempts'] for x in records),initial_successes=sum(x['initial_passed'] for x in records),successes=sum(x['passed'] for x in records),records=records,scope='At most two actual attempts on same task/checker, with actual validation feedback. All initial failures and costs retained. One known task, not broad model quality.')
(R/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
