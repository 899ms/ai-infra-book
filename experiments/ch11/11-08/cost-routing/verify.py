import hashlib,json,math
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parent;s=json.loads((R/'results.json').read_text())
for p,h in s['source_sha256'].items():assert hashlib.sha256((P/p).read_bytes()).hexdigest()==h
assert len(s['records'])==48 and len(s['decisions'])==12 and len(s['cache_queue_comparison'])==12
recipes=[('8B',False,1000),('8B',True,100),('8B',True,1000),('8B',True,4096),('MoE',False,1000),('MoE_feedback',False,1000)]
for d in s['decisions']:
 eligible=[r for r in s['records'] if r['rep']==0 and r['warm']==d['warm'] and r['busy']==d['busy'] and r['passed']]
 if d['policy']=='quality_constrained':
  if not eligible:assert d['selected'] is None and d['evaluation'] is None;continue
  best=sorted(eligible,key=lambda r:(r['attempt_cost'],recipes.index((r['model'],r['thinking'],r['budget']))))[0];assert d['selected']==[best['model'],best['thinking'],best['budget']]
 elif d['policy']=='fixed':assert d['selected']==['8B',True,1000]
 else:assert d['selected']==['8B',False,1000]
 e=d['evaluation'];assert e['rep']==1 and [e['model'],e['thinking'],e['budget']]==d['selected'] and e['warm']==d['warm'] and e['busy']==d['busy']
for a in s['aggregate']:
 selected=[d['evaluation'] for d in s['decisions'] if d['policy']==a['policy'] and d['evaluation'] is not None];passed=sum(r['passed'] for r in selected)
 assert a['successes']==passed and a['evaluated_attempts']==len(selected)
 total=sum(r['target_cost']+r['warmup_cost'] for r in selected);assert math.isclose(total,a['teaching_spent'])
 assert a['teaching_cost_per_success_including_failures']==(total/passed if passed else None) and a['real_provider_billed_cost'] is None
for model,p in s['prices_units_per_million'].items():assert math.isclose(s['reasoning100_vs1000_fixed_answer_marginal_teaching_cost'][model],(1000-100)*p['output']/1e6)
print('Verified source identity, repetition split,12 policy decisions, failure-inclusive success cost and reasoning marginal arithmetic.')
