"""Cost sensitivity on measured, quality-checked recovery paths; no fabricated billing."""
from pathlib import Path
import hashlib,json,math
P=Path(__file__).resolve().parent;ROOT=P.parents[3];src=P.parent/'formal/summary.json';x=json.loads(src.read_text());assert x['paths']==12 and x['quality_passed']==12 and x['all_mechanism_checks_passed']
records=x['results'];rows=[]
for r in records:
 assert r['unique_tokens']==len(r['token_ids']) and r['sampled_tokens']==sum(w['sampled_tokens'] for w in r['workers'])
 assert r['sampled_tokens']-r['unique_tokens']==r['duplicate_deliveries']
 rows.append(dict(request_id=r['request_id'],task=r['task'],cut=r['cut'],strategy=r['strategy'],wall_s=r['wall_s'],generated_tokens=r['sampled_tokens'],manager_unique_tokens=r['unique_tokens'],duplicate_deliveries=r['duplicate_deliveries'],prefix_rebuilt_tokens=sum(w['prefix_rebuild_tokens'] for w in r['workers']),completed_training_tokens=None,teaching_cost_at1unit_per_hour=r['wall_s']/3600))
comparisons=[]
for task in ['sequence','extract']:
 for cut in [32,96]:
  group={r['strategy']:r for r in rows if r['task']==task and r['cut']==cut};b=group['baseline'];restart=group['restart'];preserve=group['preserve']
  comparisons.append(dict(task=task,cut=cut,preserve_time_saved_vs_restart_s=restart['wall_s']-preserve['wall_s'],preserve_cost_saved_at1unit_per_hour=(restart['wall_s']-preserve['wall_s'])/3600,preserve_max_price_ratio_to_restart=restart['wall_s']/preserve['wall_s'],restart_max_price_ratio_to_baseline=b['wall_s']/restart['wall_s'],preserve_max_price_ratio_to_baseline=b['wall_s']/preserve['wall_s']))
# Explicit teaching model: new optional resource must load full weights over the declared link.
identity=P.parent/'model-identity.json';weight=sum(v['bytes'] for n,v in json.loads(identity.read_text())['files'].items() if n.endswith('.safetensors'));assert weight==4351884216
prep=weight/10**9;v=100;p_fixed=1;p_extra=.3
threshold=prep/(1-p_extra/p_fixed)
life=[]
for L in [2,5,10,20,40]:
 useful=max(0,L-prep)*v
 life.append(dict(lifetime_s=L,preparation_s=prep,generated_token_budget=useful,full_samples=None,training_tokens=None,resource_cost_units=p_extra*L/3600,cost_per_generated_token=None if useful==0 else p_extra*L/3600/useful,cheaper_than_fixed_variable_work=useful>0 and p_extra*L < p_fixed*(L-prep)))
assert not (p_extra*threshold < p_fixed*(threshold-prep)-1e-12)
out=dict(measured_rows=rows,paired_comparisons=comparisons,teaching_model=dict(weight_bytes=weight,declared_link_bytes_s=10**9,declared_tokens_s=v,fixed_price_units_hour=p_fixed,optional_price_units_hour=p_extra,strictly_cheaper_lifetime_threshold_s=threshold,rows=life),source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [src,identity]},limits=['Path wall time is an explicit allocated-resource billing assumption, not GPU busy time or an invoice.','Additional-resource rows are an analytical scenario, not simultaneous worker measurements.','Generated tokens are not necessarily full samples or training tokens.'])
(P/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(comparisons=comparisons,threshold_s=threshold),indent=2))
