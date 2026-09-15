"""Conditional accounting coefficients; explicitly not a computed invoice."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[3];src=P.parent/'results/analysis.json';x=json.loads(src.read_text());u=x['raw_usage_field_sums']
assert x['logs']==len(x['rows'])==21
for r in x['rows']:
 v=r['reported_usage'];assert v['cached_input_tokens']<=v['input_tokens'];assert v['reasoning_output_tokens']<=v['output_tokens']
coeff=dict(uncached_input=u['input_tokens']-u['cached_input_tokens'],cached_input=u['cached_input_tokens'],output_including_reasoning=u['output_tokens'])
assert coeff['uncached_input']+coeff['cached_input']==u['input_tokens']
# This identity avoids double-counting subset fields; it does not prove vendor semantics.
assert coeff['output_including_reasoning']-u['reasoning_output_tokens']==322067
out=dict(scope='conditional algebra on observed field sums; no invoice or monthly comparison',observed_turns=x['logs'],threads=x['distinct_thread_ids'],conditional_price_coefficients_tokens=coeff,price_units='currency per million tokens',formula='(1987545*p_uncached + 45657216*p_cached + 402591*p_output)/1000000',conditions=['The input field includes cached input, and output includes reasoning output.','All usage records cover non-overlapping billable intervals.','All records use one identified model/version, price snapshot, currency and channel.','No missing fees, attempts or separately charged cache writes/storage.'],observed_billed_total=None,accepted_monthly_tasks=None,quota_blocked_tasks=None,subscription_api_crossing_tasks=None,reseller_api_crossing_tasks=None,missing_fields=['monthly task IDs and quality acceptance','subscription plan, price, quota and concurrency behavior','API model, price snapshot and billable usage semantics','reseller identity, fees, usage semantics and matched task results','turn recovery interval deduplication'],source_sha256={str(src.relative_to(ROOT)):hashlib.sha256(src.read_bytes()).hexdigest()})
(P/'results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(coeff))
