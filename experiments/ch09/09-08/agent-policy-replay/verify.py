import hashlib,itertools,json,math
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[3];s=json.loads((R/'results.json').read_text())
for p,h in s['source_sha256'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
p=ROOT/'experiments/ch09/09-09/remote-kv/cross-mac-traces-001/results/agent-producer/requests.jsonl';inputs=[json.loads(l) for l in p.read_text().splitlines()];seen=set();page=s['page_bytes']
for case in s['scenarios']:
 caps=case['capacity_pages'];key=tuple(caps.values())+(case['policy'],case['fault']);assert key not in seen;seen.add(key);rows=case['requests'];assert len(rows)==12
 assert rows[0]['hit_tokens']==0
 for r,i in zip(rows,inputs):
  assert r['turn']==i['turn'] and r['input_tokens']==i['input_tokens']
  assert sum(r['tier_hits'].values())==r['hit_tokens'] and r['hit_tokens']%16==0 and 0<=r['hit_tokens']<=len(i['expected_reusable_keys'])*16
  assert r['recompute_tokens']==r['input_tokens']-r['hit_tokens']>=1
  for tier,cap in caps.items():
   if cap==0:assert r['tier_hits'][tier]==0
  for tier in ['local','remote']:
   assert r['write_bytes'][tier]%page==0
   if caps[tier]==0 or case['policy']=='recompute':assert r['write_bytes'][tier]==0
  assert math.isclose(r['estimated_request_s'],r['model_profile_s']+r['storage_read_component_s']+r['storage_write_component_s'])
  assert r['checkpoint']==(case['policy']=='full' or case['policy']=='periodic4' and (r['turn']+1)%4==0)
 if case['fault']=='invalidate7' or case['fault']=='restart7' and caps['local']==caps['remote']==0:assert rows[6]['hit_tokens']==0
 assert math.isclose(case['token_hit_rate'],sum(r['hit_tokens'] for r in rows)/sum(r['input_tokens'] for r in rows))
 for tier in ['local','remote']:
  assert case['write_bytes'][tier]==sum(r['write_bytes'][tier] for r in rows)
  if caps[tier]==256:
   epochs=[inputs[:6],inputs[6:]] if case['fault']=='invalidate7' else [inputs];expected=0
   for epoch in epochs:
    persisted={k for i in epoch if case['policy']=='full' or case['policy']=='periodic4' and (i['turn']+1)%4==0 for k in i['expected_reusable_keys']};expected+=len(persisted)*page
   assert case['write_bytes'][tier]==expected
assert seen=={caps+(policy,fault) for caps in itertools.product([0,64,256],repeat=4) for policy,fault in itertools.product(['full','periodic4','recompute'],['none','restart7','invalidate7'])}
print('Verified729 unique scenarios, source hashes, prefix/token conservation, fault reset behavior, checkpoint schedule and no-eviction durable-write identities.')
