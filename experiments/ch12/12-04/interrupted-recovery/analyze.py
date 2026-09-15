import collections,gzip,hashlib,io,json,statistics
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parent;O=R/'results';D=O/'loss0.1';F=json.loads((R.parent/'image-records/image-fixture.json').read_text());RAW=(R.parent/'image-records'/F['upload_file']).read_bytes();JPEG=(R.parent/'image-records'/F['response_file']).read_bytes()
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha(RAW)==F['upload_sha256'] and sha(JPEG)==F['response_sha256']
E=json.loads((D/'environment.json').read_text());assert E['fixture']==F and E['fault_bytes']==1048576;assert E['source_sha256']==sha((R/'run.py').read_bytes());assert E['transport_source_sha256']==sha((R.parent/'image-records/run_network120.py').read_bytes())
image=json.loads((O/'image-inspect.json').read_text())[0];ci=json.loads((O/'container-inspect.json').read_text())[0];hc=ci['HostConfig'];assert ci['Image']==image['Id']=='sha256:bc544dc84aa48ca11602c4840b9f9642c129fa882ce24d4579dedf80c6026396';assert hc['NetworkMode']=='none' and hc['NanoCpus']==2000000000 and hc['Memory']==2147483648 and 'NET_ADMIN' in [c.removeprefix('CAP_') for c in hc['CapAdd']]
assert (O/'container-removed.txt').read_text().strip()=='book-recovery1204';assert not (R/'container-after.txt').read_text().strip()
for phase in ['before','after']:
 q=json.loads((O/f'{phase}.json').read_text());assert len(q)==1 and q[0]['kind']=='netem';q=q[0];assert q['options']['delay']['delay']==.04 and q['options']['rate']['rate']==2500000 and q['options']['loss-random']['loss']==.001;assert q['backlog']==0 and q['qlen']==0
rows=[json.loads(s) for s in (D/'requests.jsonl').read_text().splitlines()];order=json.loads((D/'order.json').read_text());assert len(rows)==len(order)==20
assert {(r['trial'],r['protocol'],r['policy']) for r in rows if not r['warmup']}=={(t,p,k) for t in range(3) for p in ['h1','h3'] for k in ['uninterrupted','restart','resume']}
conn={c['connection']:c for c in json.loads((D/'connections.json').read_text())};assert len(conn)==32
server=json.loads((D/'server-records.json').read_text());assert len(server)==32
fault_ops=set();verified=[];service_calls=0
for r,c in zip(rows,order):
 assert all(r[k]==c[k] for k in c);assert r['valid'] and 'error' not in r
 es=[conn[i] for i in r['exchanges']];assert len(es)==(1 if r['policy']=='uninterrupted' else 2)
 ss=[s for s in server if s['operation']==r['operation']];assert len(ss)==len(es)
 parts=[]
 for e,s in zip(es,ss):
  assert e['protocol']==s['protocol']==r['protocol'] and e['operation']==r['operation'] and e['path']==s['path']
  assert r['start_s']<=e['start_s']<=e['ready_s']<=s['received_s']<=s['prepared_s']<=e['first_data']<=e['end']<=e['close_start_s']<=e['closed_s']<=r['validation_end_s']
  assert not e['session_resumed']
  if r['protocol']=='h1':assert e['tls']=='TLSv1.3' and e['alpn']=='http/1.1' and e['certificate_sha256']==E['certificate_sha256']
  else:assert e['alpn']=='h3' and not e['early_data_accepted']
  part=(D/f"response-{e['connection']}.bin").read_bytes();assert len(part)==e['received_bytes'] and sha(part)==e['received_sha256'];parts.append(part)
  h=dict(e['headers']);assert h['etag']=='"'+F['response_sha256']+'"' and int(h['content-length'])==s['response_bytes']
  if e['path']=='/image':
   assert e['upload_bytes']==s['request_bytes']==len(RAW) and e['upload_sha256']==s['request_sha256']==sha(RAW);assert s['offset']==0 and s['status']==200 and h[':status']=='200';assert s['service_end_s']-s['service_start_s']>=F['service_s'];assert s['response_sha256']==sha(JPEG);service_calls+=1
  else:
   offset=int(e['path'].split('/')[-1]);assert e['upload_bytes']==s['request_bytes']==0 and e['upload_sha256']==s['request_sha256']==sha(b'');assert s['offset']==offset and s['status']==206 and h[':status']=='206';assert h['content-range']==f'bytes {offset}-{len(JPEG)-1}/{len(JPEG)}';assert s['response_sha256']==sha(JPEG[offset:]);assert 'service_start_s' not in s
  assert len(part)<=s['response_bytes']
 if r['policy']=='uninterrupted':assert not es[0]['fault_requested'] and es[0]['stream_ended'];complete=parts[0]
 else:
  fault_ops.add(r['operation']);assert es[0]['fault_requested'] and not es[0]['stream_ended'] and not es[1]['fault_requested'] and es[1]['stream_ended'];assert 1048576<=len(parts[0])<len(JPEG) and parts[0]==JPEG[:len(parts[0])]
  assert r['interrupted_prefix_bytes']==len(parts[0]) and r['interrupted_prefix_sha256']==sha(parts[0]);assert es[0]['closed_s']<=es[1]['start_s'];assert es[0]['local']!=es[1]['local']
  if r['policy']=='restart':assert es[1]['path']=='/image';complete=parts[1]
  else:assert es[1]['path']==f'/resume/{len(parts[0])}';complete=parts[0]+parts[1]
 assert complete==JPEG and r['sha256']==sha(complete) and r['bytes']==len(complete)
 with Image.open(io.BytesIO(complete)) as im:im.load();rgb=im.convert('RGB');assert [rgb.height,rgb.width,3]==F['shape'];assert sha(rgb.tobytes())==r['decoded_sha256']==F['decoded_sha256']
 verified.append(dict(trial=r['trial'],protocol=r['protocol'],policy=r['policy'],warmup=r['warmup'],elapsed_s=r['validation_end_s']-r['start_s'],upload_bytes=sum(e['upload_bytes'] for e in es),client_retained_bytes=sum(len(p) for p in parts),prepared_response_bytes=sum(s['response_bytes'] for s in ss),service_calls=sum('service_start_s' in s for s in ss),prefix_bytes=len(parts[0]) if len(parts)==2 else None,recovery_s=r['validation_end_s']-es[0]['close_start_s'] if len(es)==2 else None,close_s=sum(e['closed_s']-e['close_start_s'] for e in es)))
assert service_calls==26 and len(fault_ops)==12
errors=json.loads((D/'server-errors.json').read_text())
for e in errors:
 h=dict(e['headers']);assert h['x-operation'] in fault_ops and h[':path']=='/image';assert any(k in e['error'] for k in ['ConnectionResetError','BrokenPipeError','APPLICATION_DATA_AFTER_CLOSE_NOTIFY'])
qlog_headers=0;close_frames=0
for p in D.glob('qlog-*.json.gz'):
 q=json.load(gzip.open(p,'rt'));assert q['qlog_version']=='0.3';ident=int(p.stem.split('-')[1].split('.')[0]);c=conn[ident];assert c['protocol']=='h3';status=[];closes=0
 for t in q['traces']:
  for e in t['events']:
   if e['name']=='http:frame_parsed' and e['data']['frame']['frame_type']=='headers':status.append({h['name']:h['value'] for h in e['data']['frame']['headers']}[':status'])
   if e['name']=='transport:packet_sent':closes+=sum(f['frame_type']=='connection_close' for f in e['data'].get('frames',[]))
 assert status==[dict(c['headers'])[':status']];assert closes>=1;qlog_headers+=len(status);close_frames+=closes
assert qlog_headers==16
conditions=[]
for proto in ['h1','h3']:
 for policy in ['uninterrupted','restart','resume']:
  rr=[r for r in verified if not r['warmup'] and r['protocol']==proto and r['policy']==policy];assert len(rr)==3
  conditions.append(dict(protocol=proto,policy=policy,samples_s=[r['elapsed_s'] for r in rr],median_s=statistics.median(r['elapsed_s'] for r in rr),upload_bytes=sorted({r['upload_bytes'] for r in rr}),client_retained_bytes=[r['client_retained_bytes'] for r in rr],median_recovery_s=statistics.median(r['recovery_s'] for r in rr) if policy!='uninterrupted' else None,median_close_s=statistics.median(r['close_s'] for r in rr)))
summary=dict(tasks=len(rows),valid=len(verified),formal=18,exchanges=len(conn),injected_interruptions=12,service_replays=service_calls,qlog_headers=qlog_headers,close_frames=close_frames,expected_server_close_errors=errors,conditions=conditions,verified=verified)
(R/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k not in ['verified','expected_server_close_errors']},indent=2))
