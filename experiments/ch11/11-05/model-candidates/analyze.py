from pathlib import Path
import hashlib,json,statistics
P=Path(__file__).resolve().parent;O=P/'validation-v2';protocol=json.loads((O/'protocol.json').read_text());spec={j['id']:j for j in protocol['tasks']}
for name,digest in protocol['source_sha256'].items():assert hashlib.sha256((P/name).read_bytes()).hexdigest()==digest
for j in spec.values():assert hashlib.sha256((P/'generation'/f"{j['id']}.json").read_bytes()).hexdigest()==j['source_sha256']
assert json.loads((O/'cleanup.json').read_text())['remaining']==[]
raw=[json.loads(l) for l in (O/'raw.jsonl').read_text().splitlines()];assert len(raw)==9
rows=[]
for case in raw:
 assert len(case['tasks'])==6 and {r['id'] for r in case['tasks']}==set(spec)
 ticks=[]
 for r in case['tasks']:
  assert case['start_s']+spec[r['id']]['arrival_s']<=r['dispatch_s']<=r['container_ready_s']<=r['feedback_s']<=r['exit_observed_s']<=r['release_s']
  assert not r['state']['Running'] and r['state']['ExitCode']==0
  events=r['events'];assert events[0]['event']=='worker_start' and events[-1]['event']=='feedback'
  assert all(a['at_s']<=b['at_s'] for a,b in zip(events,events[1:]))
  for e in events:assert e['at_s']<=e['host_received_s']
  status=events[-1]['status'];assert status in ['pass','timeout','wrong','error']
  if status=='pass':assert events[-1]['actual']==events[-1]['expected']
  ticks.extend([(r['dispatch_s'],1,r['batch']),(r['release_s'],-1,r['batch'])])
 counts={'A':0,'B':0}
 for _,delta,batch in sorted(ticks):
  counts[batch]+=delta;assert 0<=sum(counts.values())<=2
  if case['policy']=='fixed_quota':assert max(counts.values())<=1
 for d in case['decisions']:
  key=(lambda id:(id[0]!='A',spec[id]['arrival_s'],id)) if case['policy']=='batch_A_first' else (lambda id:(spec[id]['arrival_s'],id))
  assert d['chosen']==min(d['eligible'],key=key)
  expected={id for id,j in spec.items() if case['start_s']+j['arrival_s']<=d['at_s'] and id not in d['running'] and not any(t['id']==id and t['dispatch_s']<d['at_s'] for t in case['tasks'])}
  if case['policy']=='fixed_quota':expected={id for id in expected if id[0] not in {x[0] for x in d['running']}}
  assert set(d['eligible'])==expected,(d,expected)
 row=dict(trial=case['trial'],policy=case['policy'],batch_feedback_s={b:max(t['feedback_s'] for t in case['tasks'] if t['batch']==b)-case['start_s'] for b in ['A','B']},all_released_s=max(t['release_s'] for t in case['tasks'])-case['start_s'],slot_seconds=sum(t['release_s']-t['dispatch_s'] for t in case['tasks']),outcomes={t['id']:t['events'][-1]['status'] for t in case['tasks']},queue_seconds={t['id']:t['dispatch_s']-case['start_s']-t['arrival_s'] for t in case['tasks']},feedback_to_release_s={t['id']:t['release_s']-t['feedback_s'] for t in case['tasks']})
 rows.append(row)
metrics=[]
for policy in ['fixed_quota','fifo','batch_A_first']:
 r=[x for x in rows if x['policy']==policy];assert sorted(x['trial'] for x in r)==[0,1,2]
 metrics.append(dict(policy=policy,A_feedback_s=statistics.median(x['batch_feedback_s']['A'] for x in r),B_feedback_s=statistics.median(x['batch_feedback_s']['B'] for x in r),all_released_s=statistics.median(x['all_released_s'] for x in r),slot_seconds=statistics.median(x['slot_seconds'] for x in r)))
out=dict(verified_cases=9,verified_containers=54,metrics=metrics,rows=rows,actual_training=False)
(P/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(metrics,indent=2))
