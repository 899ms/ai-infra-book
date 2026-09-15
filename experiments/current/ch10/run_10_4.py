"""Reproduce pipeline schedules and verify event dependencies/resource exclusion."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import sys,json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2];sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.topics.training_pipeline_schedule import calculate
runs={};files=[next((ROOT/'manuscripts').glob('10-*.md')),ROOT/'calculations/src/infra_calc/topics/training_pipeline_schedule.py']
for name,policy in [('1f1b-m8','1f1b'),('interleaved-m8','interleaved_1f1b'),('zero-bubble-m8','zero_bubble')]:
 r=calculate(policy=policy);p=ROOT/f'calculations/results/training-pipeline-{name}.json';old=json.loads(p.read_text());files.append(p)
 assert r['events']==old['events'] and r['summary']==old['summary']
 byid={e['id']:e for e in r['events']};resources=defaultdict(list)
 for e in r['events']:
  assert abs(e['end']-e['start']-e['duration'])<1e-10
  for dep in e['dependencies']:assert byid[dep]['end']<=e['start']+1e-10
  if e['duration']>0:resources[e['resource']].append(e)
 for events in resources.values():
  events.sort(key=lambda e:e['start'])
  for a,b in zip(events,events[1:]):assert a['end']<=b['start']+1e-10
 runs[name]=dict(summary=r['summary'],forward_messages=sum(e['kind']=='A' for e in r['events']),gradient_messages=sum(e['kind']=='G' for e in r['events']),events_verified=len(r['events']))
 if policy=='1f1b':
  gap=[byid[i] for i in ['B:3:1','F:2:2','A:2:2','F:3:2']]
  assert abs(byid['B:3:1']['end']-.093)<1e-10 and abs(byid['F:3:2']['start']-.095)<1e-10
out=dict(exercise='10-4',ideal=[dict(microbatches=m,compute_per_stage_ms=m*30,bubble_ms=90,total_ms=(m+3)*30,utilization=float(F(m,m+3))) for m in [1,4,8,16]],bubble_bounds_ms=dict(oneFoneB=90,interleaved_v2=45,ZB_H1=30),schedules=runs,gap_events=gap,rebuild=dict(original_MiB=4*9*10,one_at_time_workspace_MiB=10,net_peak_reduction_MiB=350,two_at_time_workspace_MiB=20,two_at_time_net_reduction_MiB=340),source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
(P/'10-4-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(runs,indent=2))
