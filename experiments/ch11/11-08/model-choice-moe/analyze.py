import hashlib,json,math,random,statistics
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'results'
def read(p):return json.loads(p.read_text())
def lines(p):return [json.loads(l) for l in p.read_text().splitlines()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ex=read(R/'execution.json');env=read(O/'environment.json');rows=lines(O/'raw.jsonl');assert ex['exit_code']==0 and not ex['after_gpu'].strip() and len(rows)==8
for n,h in env['source_hashes'].items():assert sha(R/n)==h
order=[];rng=random.Random(1107)
for rep in range(2):
 cases=[dict(rep=rep,thinking=think,budget=cap,warm=warm,busy=busy) for think,cap in [(False,1000)] for warm in [False,True] for busy in [False,True]];rng.shuffle(cases);order+=cases
assert order==read(O/'order.json');records=[]
for i,(r,c) in enumerate(zip(rows,order)):
 assert r==read(O/f'case{i}/record.json') and r['index']==i and all(r[k]==v for k,v in c.items())
 t=r['target'];m=t['metrics'];assert len(t['output_ids'])<=c['budget'] and m['num_generation_tokens']==len(t['output_ids']) and not m['is_corrupted']
 assert t['events'][-1]['token_count']==len(t['output_ids']) and all(a['time_s']<=b['time_s'] and a['token_count']<=b['token_count'] for a,b in zip(t['events'],t['events'][1:]))
 queue=m['scheduled_ts']-m['queued_ts'];assert queue>=0
 if c['warm']:assert r['warmup']['input_ids']==t['input_ids'] and len(r['warmup']['output_ids'])==1 and t['cached_tokens']>0
 else:assert r['warmup'] is None and t['cached_tokens']==0
 if c['busy']:
  b=r['background'];assert len(b['output_ids'])==128 and b['events'][0]['time_s']<=t['start_s']<b['end_s'] and m['scheduled_ts']>=b['metrics']['last_token_ts'] and queue>.1
 else:assert r['background'] is None
 if r['thinking_closed']:
  pos=t['output_ids'].index(env['thinking_close_token']);assert pos==r['reasoning_tokens_before_close'] and '</think>' in t['text']
 else:assert r['reasoning_tokens_before_close']==(len(t['output_ids']) if c['thinking'] else 0)
 result=r['result'];passed=result['passed']
 if 'validation' in result:
  check=json.loads(result['validation']['stdout']);assert len(check['cases'])==6
  independently=all(x.get('actual')==x['expected'] and x.get('unchanged') is True for x in check['cases']);assert independently==check['passed']==passed
  assert sha(O/f'case{i}/intervals.py')==result['write']['sha256']
 assert r['verified_usable_s']==(r['done_s']-t['start_s'] if passed else None)
 records.append(dict(index=i,**c,input_tokens=len(t['input_ids']),output_tokens=len(t['output_ids']),reasoning_tokens=r['reasoning_tokens_before_close'],cached_tokens=t['cached_tokens'],queue_s=queue,first_token_s=t['events'][0]['time_s']-t['start_s'],first_answer_segment_s=r['first_answer_segment_s']-t['start_s'] if r['first_answer_segment_s'] is not None else None,total_s=r['done_s']-t['start_s'],verified_usable_s=r['verified_usable_s'],passed=passed,finish_reason=t['finish_reason'],warmup_output_tokens=1 if c['warm'] else 0,background_output_tokens=128 if c['busy'] else 0))
groups=[]
for thinking,budget in [(False,1000)]:
 for warm in [False,True]:
  for busy in [False,True]:
   a=[x for x in records if (x['thinking'],x['budget'],x['warm'],x['busy'])==(thinking,budget,warm,busy)];assert len(a)==2
   groups.append(dict(thinking=thinking,budget=budget,warm=warm,busy=busy,passed=sum(x['passed'] for x in a),attempts=2,failure_rate=sum(not x['passed'] for x in a)/2,median_queue_s=statistics.median(x['queue_s'] for x in a),median_total_s=statistics.median(x['total_s'] for x in a),output_tokens=[x['output_tokens'] for x in a],cached_tokens=[x['cached_tokens'] for x in a]))
result=dict(status='moe_cache_queue_measurements_verified',targets=8,successes=sum(x['passed'] for x in records),groups=groups,records=records,scope='One controlled task, two repetitions, one model. Cap is total generation, not independent reasoning quota. First post-thinking segment is not verified usable output; failed verified_usable remains null. No real provider pricing or cross-model routing in this run.')
(R/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(groups,indent=2))
