import collections,gzip,hashlib,json,statistics
from pathlib import Path
R=Path(__file__).resolve().parent;D=R/'network-results/loss0.1';F=json.loads((R/'network-fixture.json').read_text());steps=F['steps'];n=len(steps)
for phase in ['before','after']:
 q=json.loads((R/'network-results'/f'{phase}.json').read_text());assert len(q)==1 and q[0]['kind']=='netem';q=q[0];assert q['options']['delay']['delay']==.04 and q['options']['rate']['rate']==2500000 and q['options']['loss-random']['loss']==.001;assert q['backlog']==0 and q['qlen']==0
E=json.loads((D/'environment.json').read_text());assert E['fixture']==F and E['body_request_deadline_s']==120 and not E['smoke'];assert E['source_sha256']==hashlib.sha256((R/'run_network.py').read_bytes()).hexdigest()
for f in steps:
 assert hashlib.sha256((R/f['upload_file']).read_bytes()).hexdigest()==f['upload_sha256'];assert hashlib.sha256((R/f['response_file']).read_bytes()).hexdigest()==f['response_sha256']
 req=json.loads((R/f['upload_file']).read_bytes());assert req['id']==f"t0-s{f['step']}"
rows=[json.loads(s) for s in (D/'requests.jsonl').read_text().splitlines()];assert len(rows)==12*n+2
cs={c['id']:c for c in json.loads((D/'connections.json').read_text())};assert len(cs)==6*n+8
groups=json.loads((D/'groups.json').read_text());assert len(groups)==14
assert not json.loads((D/'server-errors.json').read_text())
for proto in ['h1','h3']:
 sr=json.loads((D/(proto+'-server.json')).read_text());assert len(sr)==6*n+1
 for r in sr:
  f=steps[r['step']];assert r['sha256']==f['upload_sha256'] and r['bytes']==f['upload_bytes'];assert r['service_end']-r['service_start']>=f['service_s']
for c in cs.values():
 assert c['start']<=c['ready']<=c['closed'] and not c['session_resumed']
 if c['protocol']=='h1':assert c['alpn']=='http/1.1' and c['tls']=='TLSv1.3' and c['certificate_sha256']==E['certificate_sha256']
 else:assert c['alpn']=='h3' and not c['early_data_accepted']
for r in rows:
 f=steps[r['step']];assert r['valid'] and r['error'] is None and r['bytes']==f['response_bytes'] and r['sha256']==f['response_sha256'] and r['action']==f['action'];assert dict(r['headers'])[':status']=='200'
 assert r['start']<=r['connection_ready']<=r['send']<=r['first_headers']<=r['first_data']<=r['end']<=r['validation_end'];assert cs[r['connection']]['protocol']==r['protocol']
for g in groups:
 rr=sorted([r for r in rows if all(r[k]==g[k] for k in ['trial','protocol','reuse','concurrency','warmup'])],key=lambda r:r['index']);assert len(rr)==g['requests']==(1 if g['warmup'] else n) and not g['errors'];assert [r['step'] for r in rr]==list(range(len(rr)))
 assert len({r['connection'] for r in rr})==(1 if g['reuse'] or g['warmup'] else n)
 assert g['start']<=rr[0]['start'] and rr[-1]['validation_end']<=g['requests_complete']<=g['cleanup_complete']
 assert all(a['validation_end']<=b['start'] for a,b in zip(rr,rr[1:]))
events=collections.Counter();responses=0
for p in D.glob('qlog-*.json.gz'):
 q=json.load(gzip.open(p,'rt'));assert q['qlog_version']=='0.3'
 for t in q['traces']:
  for e in t['events']:
   events[e['name']]+=1
   if e['name']=='http:frame_parsed' and e['data']['frame']['frame_type']=='headers':
    assert {h['name']:h['value'] for h in e['data']['frame']['headers']}[':status']=='200';responses+=1
assert responses==6*n+1
conditions=[]
for proto in ['h1','h3']:
 for reuse in [False,True]:
  rr=[r for r in rows if not r['warmup'] and r['protocol']==proto and r['reuse']==reuse];gg=[g for g in groups if not g['warmup'] and g['protocol']==proto and g['reuse']==reuse]
  conditions.append(dict(protocol=proto,reuse=reuse,requests=len(rr),median_round_ms=statistics.median((r['validation_end']-r['start'])*1000 for r in rr),trace_s=[g['requests_complete']-g['start'] for g in gg],median_trace_s=statistics.median(g['requests_complete']-g['start'] for g in gg)))
summary=dict(requests=len(rows),valid=sum(r['valid'] for r in rows),connections=len(cs),qlog_responses=responses,qlog_events=dict(events),source_model_service_total_s=sum(f['service_s'] for f in steps),conditions=conditions)
(R/'network-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
