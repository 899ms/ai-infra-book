"""Verify matched input/arrival identities and include every formal request in costs."""
from pathlib import Path
import json,hashlib,re,statistics as st,math
P=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text())
lines=lambda p:[json.loads(x) for x in p.read_text().splitlines()]
inputs=load(P/'inputs.json');tasks={t['id']:t for t in inputs['tasks']};protocol=load(P/'protocol.json')
for t in tasks.values():
 records=dict(re.findall(r'^(k\d+) = (\d{6})$',t['messages'][-1]['content'],re.M))
 assert all(records[k]==v for k,v in t['expected'].items())
def unique(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate key')
  d[k]=v
 return d
results=[];paired={};configs=[]
for tag in ('B-001','E-001'):
 d=P/'runs'/tag;run=d/'results';assert load(d/'exit.json')['exit_code']==0
 assert load(run/'completion.json')==dict(groups=3,formal_requests=48,warmup_requests=8)
 assert (run/'inputs.json').read_bytes()==(P/'inputs.json').read_bytes()
 assert (run/'protocol.json').read_bytes()==(P/'protocol.json').read_bytes()
 env=load(run/'environment.json');assert env['source_sha256']==hashlib.sha256((P/'run.py').read_bytes()).hexdigest();configs.append(env['config'])
 req=[r for r in lines(run/'requests.jsonl') if r['group']!='warm'];assert len(req)==48 and len({r['id'] for r in req})==48
 groups=lines(run/'groups.jsonl');stats=lines(run/'stats.jsonl');checked=[]
 for g in groups:
  planned=next(x for x in protocol['groups'] if x['id']==g['id']);rs=[r for r in req if r['group']==g['id']];assert len(rs)==16
  for i,tid in enumerate(planned['tasks']):
   r=next(r for r in rs if r['id']==g['id']+f'-{i}');assert r['task_id']==tid
   assert abs(r['intended_arrival_s']-(g['start_s']+i/4))<1e-8
   ev=r['events'];times=[e[0] for e in ev];counts=[e[1] for e in ev]
   assert times==sorted(times) and counts==sorted(counts) and counts[-1]==len(r['output_ids'])
   assert r['intended_arrival_s']<=r['actual_arrival_s']<=r['submitted_s']<=times[0]<=times[-1]<=r['end_s']<=g['end_s']
   try:correct=json.loads(r['text'],object_pairs_hook=unique)==tasks[tid]['expected']
   except (ValueError,TypeError):correct=False
   latency=r['end_s']-r['intended_arrival_s'];qualified=correct and latency<=7
   checked.append(dict(id=r['id'],task_id=tid,correct=correct,qualified=qualified,latency_s=latency,TTFT_s=times[0]-r['intended_arrival_s'],output_tokens=len(r['output_ids']),cached_tokens=r['cached_tokens']))
  cr=[r for r in checked if r['id'].startswith(g['id']+'-')];duration=g['end_s']-g['start_s'];good=sum(r['qualified'] for r in cr)
  results.append(dict(run=tag,group=g['id'],duration_s=duration,correct=sum(r['correct'] for r in cr),qualified=good,completed=16,effective_requests_per_s=good/duration,completed_requests_per_s=16/duration,GPU_seconds_per_qualified=duration/good if good else None,p95_latency_s=sorted(r['latency_s'] for r in cr)[15]))
 samples=[s for s in lines(d/'gpu.jsonl') if s['returncode']==0 and s['values']];peak=max(float(s['values'].split(',')[0]) for s in samples)
 kv=max(s['scheduler']['kv_cache_usage'] for s in stats if s['scheduler'])
 paired[tag]=dict(requests=checked,outputs={r['id']:r['output_ids'] for r in req},sampled_whole_device_peak_MiB=peak,sampled_KV_usage_peak_fraction=kv,scope='GPU sample covers process lifecycle; scheduler snapshots include warmup and priming; not exact per-request allocation peaks')
a,b=configs;assert {k for k in set(a)|set(b) if a.get(k)!=b.get(k)}=={'speculative_config'}
assert b['speculative_config']['method']=='ngram'
output_differences=[id for id,v in paired['B-001']['outputs'].items() if v!=paired['E-001']['outputs'][id]]
for p in paired.values():p.pop('outputs')
out=dict(groups=results,runs=paired,paired_output_differences=output_differences,scope='One engine per condition, B then E; three repeated windows with evolving warm cache; sampled peaks, not causal performance guarantee')
(P/'analysis.json').write_text(json.dumps(out,indent=2)+'\n')
for tag,r in paired.items():print(tag,'correct',sum(x['correct'] for x in r['requests']),'qualified',sum(x['qualified'] for x in r['requests']),'GPUpeak',r['sampled_whole_device_peak_MiB'],'KVpeak',r['sampled_KV_usage_peak_fraction'])
for r in results:print(json.dumps(r))
print('Output differences',len(output_differences))
