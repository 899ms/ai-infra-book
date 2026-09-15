import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parent
prices={'8B':dict(input=.1,cached=.025,output=.3),'MoE':dict(input=.4,cached=.1,output=1.2),'MoE_feedback':dict(input=.4,cached=.1,output=1.2)}
recipes=[('8B',False,1000),('8B',True,100),('8B',True,1000),('8B',True,4096),('MoE',False,1000),('MoE_feedback',False,1000)]
sources={};records=[]
def load(p):
 sources[str(p.relative_to(P))]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
def cost(t,price):
 if t is None:return 0.
 n=len(t['input_ids']);cached=t['cached_tokens'];assert 0<=cached<=n
 return ((n-cached)*price['input']+cached*price['cached']+len(t['output_ids'])*price['output'])/1e6
for model,dirname in [('8B','cache-queue'),('MoE','model-choice-moe'),('MoE_feedback','feedback-route')]:
 summary=load(P/dirname/'summary.json');rawpath=P/dirname/'results/raw.jsonl';sources[str(rawpath.relative_to(P))]=hashlib.sha256(rawpath.read_bytes()).hexdigest();raw=[json.loads(l) for l in rawpath.read_text().splitlines()]
 for r,metrics in zip(raw,summary['records']):
  assert r['index']==metrics['index'];price=prices[model]
  target=cost(r['target'],price)
  if model=='MoE_feedback' and not r['initial_stage']['result']['passed']:target+=cost(r['initial_stage']['target'],price)
  warm=cost(r['warmup'],price);bg=cost(r['background'],price)
  records.append(dict(model=model,thinking=r['thinking'],budget=r['budget'],rep=r['rep'],warm=r['warm'],busy=r['busy'],target_cost=target,warmup_cost=warm,background_cost=bg,attempt_cost=target+warm,warmup_s=(r['warmup']['end_s']-r['warmup']['start_s']) if r['warmup'] else 0.,passed=r['result']['passed'],verified_usable_s=r['verified_usable_s'],first_token_s=metrics['first_token_s'],first_answer_segment_s=metrics['first_answer_segment_s'],total_s=metrics['total_s'],queue_s=metrics['queue_s'],cached_tokens=metrics['cached_tokens'],output_tokens=metrics['output_tokens'],reasoning_tokens=metrics['reasoning_tokens'],source_index=r['index']))
assert len(records)==48
decisions=[]
for warm in [False,True]:
 for busy in [False,True]:
  calibration=[r for r in records if r['rep']==0 and r['warm']==warm and r['busy']==busy];assert len(calibration)==6
  recipe=lambda r:(r['model'],r['thinking'],r['budget'])
  cheapest=min(recipes,key=lambda k:(prices[k[0]]['output'],recipes.index(k)))
  eligible=[r for r in calibration if r['passed']]
  quality=recipe(min(eligible,key=lambda r:(r['attempt_cost'],recipes.index(recipe(r))))) if eligible else None
  for policy,choice in [('fixed',('8B',True,1000)),('lowest_token_unit_price',cheapest),('quality_constrained',quality)]:
   row=dict(policy=policy,warm=warm,busy=busy,calibration_successful_recipes=[recipe(r) for r in eligible],selected=choice)
   if choice is None:row.update(status='no_feasible_calibrated_route',evaluation=None)
   else:
    result=next(r for r in records if r['rep']==1 and r['warm']==warm and r['busy']==busy and recipe(r)==choice);row.update(status='evaluated',evaluation=result)
   decisions.append(row)
aggregate=[]
for policy in ['fixed','lowest_token_unit_price','quality_constrained']:
 selected=[r['evaluation'] for r in decisions if r['policy']==policy and r['evaluation'] is not None];successes=sum(r['passed'] for r in selected);spent=sum(r['attempt_cost'] for r in selected)
 aggregate.append(dict(policy=policy,evaluated_attempts=len(selected),no_route_states=4-len(selected),successes=successes,failure_rate=sum(not r['passed'] for r in selected)/len(selected) if selected else None,teaching_spent=spent,teaching_cost_per_success_including_failures=spent/successes if successes else None,real_provider_billed_cost=None))
queue_comparison=[]
for model,think,budget in recipes:
 for rep in [0,1]:
  cold=next(r for r in records if (r['model'],r['thinking'],r['budget'],r['rep'],r['warm'],r['busy'])==(model,think,budget,rep,False,False));queued=next(r for r in records if (r['model'],r['thinking'],r['budget'],r['rep'],r['warm'],r['busy'])==(model,think,budget,rep,True,True))
  queue_comparison.append(dict(model=model,thinking=think,budget=budget,rep=rep,cold_idle_total_s=cold['total_s'],warm_busy_total_s=queued['total_s'],warm_busy_native_queue_s=queued['queue_s'],warm_cached_tokens=queued['cached_tokens'],warm_busy_slower=queued['total_s']>cold['total_s'],scope='Actual outputs may differ; full latency difference is not a pure cache effect'))
for n in ['run.py','PROTOCOL.md']:sources['cost-routing/'+n]=hashlib.sha256((R/n).read_bytes()).hexdigest()
result=dict(status='declared_price_routing_replay_verified',calibration_dataset_target_plus_warmup_cost=sum(r['attempt_cost'] for r in records if r['rep']==0),all_recorded_target_plus_warmup_cost=sum(r['attempt_cost'] for r in records),all_recorded_background_cost=sum(r['background_cost'] for r in records),prices_units_per_million=prices,reasoning100_vs1000_fixed_answer_marginal_teaching_cost={m:900*p['output']/1e6 for m,p in prices.items()},records=records,decisions=decisions,aggregate=aggregate,cache_queue_comparison=queue_comparison,source_sha256=sources,scope='One known task; repetition0 selection and repetition1 evaluation; declared prices only. Output includes reasoning once. No general model-quality guarantee, market pricing or independent production failure-rate estimate.')
(R/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(aggregate,indent=2))
