import collections,gzip,hashlib,json,statistics,argparse
from pathlib import Path
R=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('profile',choices=['loss0.1']);args=parser.parse_args()
D=R/'network-results'/args.profile
for phase in ['before','after']:
 shaping=json.loads((R/'network-results'/(args.profile+'-'+phase+'.json')).read_text())
 assert len(shaping)==1 and shaping[0]['kind']=='netem'
 options=shaping[0]['options']
 assert options['delay']['delay']==.04 and options['rate']['rate']==2500000
 assert options.get('loss-random',{}).get('loss',0)==(.001 if args.profile=='loss0.1' else 0)
 assert shaping[0]['backlog']==0 and shaping[0]['qlen']==0
env=json.loads((D/'environment.json').read_text());assert env['smoke'] is False
assert env['fixture']==json.loads((R/'image-fixture.json').read_text())
assert env['payload_sha256']==hashlib.sha256((R/'iss030e122639.NEF').read_bytes()).hexdigest()
assert env['response_sha256']==hashlib.sha256((R/'final.jpg').read_bytes()).hexdigest()
assert hashlib.sha256((R/'run_network.py').read_bytes()).hexdigest()==env['source_sha256']
assert hashlib.sha256((D/'payload.bin').read_bytes()).hexdigest()==env['payload_sha256']
raw=[json.loads(s) for s in (D/'requests.jsonl').read_text().splitlines()];assert len(raw)==26
connections={r['id']:r for r in json.loads((D/'connections.json').read_text())};assert len(connections)==20
groups=json.loads((D/'groups.json').read_text());assert len(groups)==14
assert not json.loads((D/'server-errors.json').read_text())
for protocol in ['h1','h3']:
 servers=json.loads((D/(protocol+'-server.json')).read_text());assert len(servers)==13
 assert all(r['bytes']==env['payload_bytes'] and r['sha256']==env['payload_sha256'] and r['service_end']-r['service_start']>=env['service_time_replay_s'] for r in servers)
for c in connections.values():
 assert c['start']<=c['ready']<=c['closed'] and c['session_resumed'] is False
 if c['protocol']=='h1':assert c['alpn']=='http/1.1' and c['tls']=='TLSv1.3' and c['certificate_sha256']==env['certificate_sha256']
 else:assert c['alpn']=='h3' and not c['early_data_accepted']
for r in raw:
 assert r['valid'] and r['error'] is None and r['bytes']==env['response_bytes'] and r['sha256']==env['response_sha256']
 assert dict(r['headers'])[':status']=='200'
 assert r['start']<=r['connection_ready']<=r['send']<=r['first_headers']<=r['first_data']<=r['end']<=r['validation_end']
 assert connections[r['connection']]['protocol']==r['protocol']
 if r['protocol']=='h3':assert r['stream']%4==0
for g in groups:
 rr=[r for r in raw if all(r[k]==g[k] for k in ['trial','protocol','reuse','concurrency','warmup'])]
 assert len(rr)==g['requests'] and g['errors']==0
 assert g['start']<=min(r['start'] for r in rr)<=max(r['validation_end'] for r in rr)<=g['requests_complete']<=g['cleanup_complete']
 expected=1 if g['warmup'] else g['concurrency'] if g['reuse'] else 2
 assert len({r['connection'] for r in rr})==expected
 for lane in range(g['concurrency']):
  ll=sorted((r for r in rr if r['lane']==lane),key=lambda r:r['index'])
  assert all(a['validation_end']<=b['start'] for a,b in zip(ll,ll[1:]))
qlog_events=collections.Counter();drops=collections.Counter();http_responses=0
for path in D.glob('qlog-*.json.gz'):
 q=json.load(gzip.open(path,'rt'));assert q['qlog_version']=='0.3'
 for trace in q['traces']:
  for e in trace['events']:
   qlog_events[e['name']]+=1
   if e['name']=='transport:packet_dropped':drops[e['data'].get('trigger','unknown')]+=1
   if e['name']=='http:frame_parsed' and e['data']['frame']['frame_type']=='headers':
    headers={h['name']:h['value'] for h in e['data']['frame']['headers']};assert headers[':status']=='200';http_responses+=1
assert http_responses==13
result=[]
for protocol in ['h1','h3']:
 for reuse in [False,True]:
  for concurrency in [1]:
   rr=[r for r in raw if not r['warmup'] and (r['protocol'],r['reuse'],r['concurrency'])==(protocol,reuse,concurrency)]
   assert len(rr)==6
   result.append(dict(protocol=protocol,reuse=reuse,concurrency=concurrency,requests=len(rr),valid=sum(r['valid'] for r in rr),connections=len({r['connection'] for r in rr}),median_attempt_ms=statistics.median((r['validation_end']-r['start'])*1000 for r in rr),median_ready_to_body_complete_ms=statistics.median((r['end']-r['send'])*1000 for r in rr),median_request_to_first_body_ms=statistics.median((r['first_data']-r['send'])*1000 for r in rr),per_trial_attempt_median_ms=[statistics.median((r['validation_end']-r['start'])*1000 for r in rr if r['trial']==t) for t in range(3)]))
summary=dict(status='26/26 complete RAW/final-JPEG record replays under Docker netem including 2 warmups; processing service is a calibrated CPU wait',conditions=result,handshake_median_ms={p:statistics.median((c['ready']-c['start'])*1000 for c in connections.values() if c['protocol']==p) for p in ['h1','h3']},qlog_events=dict(qlog_events),qlog_drop_triggers=dict(drops),configured_loss_percent=0.1 if args.profile=='loss0.1' else 0,configured_rtt_ms=80,configured_rate_mbit_s=20,calibration_file='../controlled-network/calibration-summary.json',model_service_replay_s=env['service_time_replay_s'])
(R/(args.profile+'-summary.json')).write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))

for row in raw:
 assert row['end']<=row['decode_start']<=row['decode_end']<=row['validation_end']
 assert row['decoded_shape']==env['fixture']['shape']
 assert row['decoded_sha256']==env['fixture']['decoded_sha256']
print('All26 complete JPEG decodes and full-resolution pixel hashes verified.')
