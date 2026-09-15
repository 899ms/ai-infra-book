import json,hashlib,math
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parent;s=json.loads((R/'results.json').read_text())
for p,h in s['source_sha256'].items():assert hashlib.sha256((P/p).read_bytes()).hexdigest()==h
assert len(s['arrangements'])==10 and len(s['lifetime_replay'])==21 and len(s['price_lifetime_sensitivity'])==18
for row in s['arrangements']:
 assert row['completed_tasks']==2 and row['trained_output_positions']==500
 assert math.isclose(row['composed_total_s'],row['generation_s']+row['composed_training_s'])
 assert row['trained_output_positions']==500
for r in s['price_lifetime_sensitivity']:
 ratio=r['extra_to_mac_price_ratio'];g=r['rtx_seconds_per_task'];m=r['mac_seconds_per_task'];D=r['preparation_s'];b=r['fluid_strict_boundary_s']
 if ratio*g>=m:assert b is None
 else:
  assert math.isclose(ratio*b/(b-D),m/g,rel_tol=1e-12)
  assert ratio*(b+.01)/(b+.01-D)<m/g
 for x in r['rows']:
  n=max(0,math.floor((x['lifetime_s']-D)/g));assert n==x['complete_task_budget']
  assert math.isclose(x['extra_cost'],ratio*x['lifetime_s']/3600)
  assert x['cheaper']==(n>0 and ratio*x['lifetime_s']<n*m)
for rep in range(3):
 a=[r for r in s['lifetime_replay'] if r['rep']==rep]
 assert all(x['generated_tokens']<=y['generated_tokens'] for x,y in zip(a,a[1:]))
 assert all(x['receivable_output_positions']==(289 if x['completed_artifact_before_cutoff'] else 0) for x in a)
print('Verified all source hashes,10 arrangement compositions,21 cutoffs and18 continuous/discrete price sensitivities.')
