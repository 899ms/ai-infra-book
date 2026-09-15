from pathlib import Path
import json,hashlib,statistics
P=Path(__file__).resolve().parent;d=json.loads((P/'results.json').read_text())
assert d['source_sha256']==hashlib.sha256((P/'run.py').read_bytes()).hexdigest()
assert len(d['rows'])==84
summary=[]
for size in (4*2**20,64*2**20):
 for mode in ('transfer','compute','shared'):
  rows=[r for r in d['rows'] if r['bytes']==size and r['mode']==mode and not r['warmup']]
  assert sorted(r['trial'] for r in rows)==list(range(11))
  summary.append(dict(bytes=size,mode=mode,trials=11,median_makespan_ms=statistics.median(r['makespan_ms'] for r in rows),median_events={key:{mark:statistics.median(r['events'][key][mark] for r in rows) for mark in ('ready_ms','start_ms','end_ms','duration_ms')} for key in rows[0]['events']}))
overlaps=[]
for r in d['rows']:
 assert r['transfer_exact'] is not False and r['compute_exact'] is not False
 assert set(r['events'])==({'transfer','compute'} if r['mode']=='shared' else {r['mode']})
 for e in r['events'].values():
  assert e['ready_ms']==0 and e['end_ms']>=e['start_ms']>=0
  assert abs(e['duration_ms']-(e['end_ms']-e['start_ms']))<1e-5
 if r['mode']=='shared' and not r['warmup']:
  events=list(r['events'].values()); overlap=max(0,min(e['end_ms'] for e in events)-max(e['start_ms'] for e in events));assert overlap>0
  overlaps.append(dict(bytes=r['bytes'],trial=r['trial'],overlap_ms=overlap))
out=dict(status='verified',total_cases=84,formal_cases=66,warmup_cases=18,shared_formal_cases_with_positive_event_overlap=len(overlaps),summary=summary,overlaps=overlaps,source_sha256={name:hashlib.sha256((P/name).read_bytes()).hexdigest() for name in ('run.py','results.json','run.log','gpu-after.txt')})
(P/'analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print('Verified all 84 cases, 66 formal cases, 22 positive shared event overlaps; source hash matches.')
