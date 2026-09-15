import collections,gzip,hashlib,json,statistics,struct
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'results/asr';order=json.loads((O/'order.json').read_text());offsets=json.loads((R/'tcp-offsets.json').read_text());F=json.loads((R.parent/'speech-records/asr-fixture.json').read_text())
assert order==[dict(trial=t,mode=m) for t in range(3) for m in (['whole','16k','64k'][t:]+['whole','16k','64k'][:t])]
def verify_chunks(ledger,data,size,lower,upper):
 expected_size=size or len(data);assert len(ledger)==(len(data)+expected_size-1)//expected_size
 offset=0;last=lower
 for item in ledger:
  part=data[offset:offset+expected_size];assert item['offset']==offset and item['bytes']==len(part) and item['sha256']==hashlib.sha256(part).hexdigest()
  assert last<=item['before_s']<=item['queued_s']<=item['complete_s']<=upper;last=item['complete_s'];offset+=len(part)
 assert offset==len(data)
def tcp_info(r):
 b=bytes.fromhex(r['tcp_info_hex']);out={}
 for name,offset in offsets.items():
  if name=='sizeof':continue
  size=8 if name in ['tcpi_rwnd_limited','tcpi_sndbuf_limited','tcpi_busy_time'] else 4
  assert len(b)>=offset+size;out[name]=int.from_bytes(b[offset:offset+size],'little')
 return out
image=json.loads((O/'image-inspect.json').read_text())[0];assert image['Id']=='sha256:bc544dc84aa48ca11602c4840b9f9642c129fa882ce24d4579dedf80c6026396'
allrows=[];evidence=[]
for c in order:
 name=f"trial{c['trial']}-{c['mode']}";D=O/name;expected=None
 ci=json.loads((O/f'{name}-container.json').read_text())[0];hc=ci['HostConfig'];assert ci['Image']==image['Id'] and hc['NetworkMode']=='none' and hc['NanoCpus']==2000000000 and hc['Memory']==2147483648 and 'NET_ADMIN' in [cap.removeprefix('CAP_') for cap in hc['CapAdd']];assert (O/f'{name}-removed.txt').read_text().strip()=='book-chunks1204'
 for phase in ['before','after']:
  q=json.loads((O/f'{name}-{phase}.json').read_text());assert len(q)==1 and q[0]['kind']=='netem';q=q[0];assert q['options']['delay']['delay']==.04 and q['options']['rate']['rate']==2500000 and q['options']['loss-random']['loss']==.001;assert q['backlog']==0 and q['qlen']==0
 env=json.loads((D/'environment.json').read_text());assert env['machine']=='x86_64';assert env['mode']==c['mode'] and env['requested_window']==expected and env['fixture']==F and not env['smoke'];assert env['source_sha256']==hashlib.sha256((R/'asr.py').read_bytes()).hexdigest();assert env['quic_max_data']==env['quic_max_stream_data']==(1048576 if expected is None else expected)
 rows=[json.loads(s) for s in (D/'requests.jsonl').read_text().splitlines()];assert len(rows)==6
 conn={r['id']:r for r in json.loads((D/'connections.json').read_text())};assert len(conn)==4
 groups=json.loads((D/'groups.json').read_text());assert len(groups)==4
 assert not json.loads((D/'server-errors.json').read_text())
 for proto in ['h1','h3']:
  server=json.loads((D/(proto+'-server.json')).read_text());assert len(server)==3
  for r in server:assert r['sha256']==F['upload_sha256'] and r['bytes']==env['payload_bytes'] and r['service_end']-r['service_start']>=F['service_s']
 for r in rows:
  assert r['valid'] and r['error'] is None and r['sha256']==F['response_sha256'] and r['decoded_text']==(R.parent/'speech-records/transcript.txt').read_text();assert r['bytes']==env['response_bytes'];assert dict(r['headers'])[':status']=='200'
  assert r['start']<=r['connection_ready']<=r['send']<=r['first_headers']<=r['first_data']<=r['end']<=r['validation_end'];assert conn[r['connection']]['protocol']==r['protocol']
  allrows.append(dict(**r,mode=c['mode'],outer_trial=c['trial'],subrun=name))
 for g in groups:
  rr=[r for r in rows if all(r[k]==g[k] for k in ['trial','protocol','reuse','concurrency','warmup'])];assert len(rr)==g['requests']==(1 if g['warmup'] else 2) and not g['errors'];assert len({r['connection'] for r in rr})==1
  assert g['start']<=rr[0]['start'] and rr[-1]['validation_end']<=g['requests_complete']<=g['cleanup_complete'];assert all(a['validation_end']<=b['start'] for a,b in zip(rr,rr[1:]))
  assert rr[0]['fresh'] and (len(rr)==1 or not rr[1]['fresh'])
 socket_rows=json.loads((D/'socket-samples.json').read_text());assert socket_rows
 assert env['listener_settings']['tcp_nodelay']==1 and env['listener_settings']['python_socket_proto']==6
 assert all(r['tcp_nodelay']==1 and r['python_socket_proto']==6 for r in socket_rows)
 tcp=[]
 for r in conn.values():
  assert r['start']<=r['ready']<=r['closed'] and not r['session_resumed']
  if r['protocol']=='h1':
   assert r['tls']=='TLSv1.3' and r['alpn']=='http/1.1' and r['certificate_sha256']==env['certificate_sha256']
   for key in ['socket_ready','socket_close']:
    assert r[key]['tcp_nodelay']==1 and r[key]['python_socket_proto']==6
    if expected is not None:assert r[key]['rcvbuf']==2*expected
   tcp.append(dict(connection=r['id'],ready=tcp_info(r['socket_ready']),close=tcp_info(r['socket_close'])))
   for key in ['tcpi_rwnd_limited','tcpi_busy_time','tcpi_sndbuf_limited','tcpi_total_retrans']:assert tcp[-1]['close'][key]>=tcp[-1]['ready'][key]
  else:assert r['alpn']=='h3' and not r['early_data_accepted']
 if expected is not None:
  assert env['listener_settings']['rcvbuf']==2*expected;assert all(r['rcvbuf']==2*expected for r in socket_rows)
 samples=[tcp_info(r) for r in socket_rows]
 parameters=[];frames=collections.Counter();limits=collections.defaultdict(list);responses=0
 for p in D.glob('qlog-*.json.gz'):
  q=json.load(gzip.open(p,'rt'));assert q['qlog_version']=='0.3'
  for t in q['traces']:
   for e in t['events']:
    if e['name']=='transport:parameters_set':parameters.append(e['data'])
    if e['name'] in ['transport:packet_sent','transport:packet_received']:
     for f in e['data'].get('frames',[]):
      kind=f['frame_type'];frames[kind]+=1
      if kind in ['max_data','max_stream_data']:limits[kind].append(f['maximum'])
    if e['name']=='http:frame_parsed' and e['data']['frame']['frame_type']=='headers':
     assert {h['name']:h['value'] for h in e['data']['frame']['headers']}[':status']=='200';responses+=1
 assert responses==3 and len(parameters)==4
 for p in parameters:
  assert p['initial_max_data']==env['quic_max_data'];assert p['initial_max_stream_data_bidi_local']==p['initial_max_stream_data_bidi_remote']==env['quic_max_stream_data']
 evidence.append(dict(**c,name=name,tcp_client_rwnd_limited_us=sum(t['close']['tcpi_rwnd_limited']-t['ready']['tcpi_rwnd_limited'] for t in tcp),tcp_client_busy_us=sum(t['close']['tcpi_busy_time']-t['ready']['tcpi_busy_time'] for t in tcp),tcp_buffers=sorted({r['rcvbuf'] for r in socket_rows}),tcp_connections=tcp,server_tcp_sample_count=len(samples),server_peer_window_range=[min(s['tcpi_snd_wnd'] for s in samples),max(s['tcpi_snd_wnd'] for s in samples)],quic_initial=env['quic_max_data'],quic_parameters=parameters,quic_frame_counts=dict(frames),quic_limit_ranges={k:[min(v),max(v)] for k,v in limits.items()}))

for c in order:
 D=O/f"trial{c['trial']}-{c['mode']}";env=json.loads((D/'environment.json').read_text());size={'whole':0,'16k':16384,'64k':65536}[c['mode']];assert env['chunk_bytes']==size
 rr=[json.loads(line) for line in (D/'requests.jsonl').read_text().splitlines()]
 for r in rr:
  UPLOAD=(R.parent/'speech-records'/F['upload_file']).read_bytes()
  verify_chunks(r['upload_chunks'],UPLOAD,size,r['send'],r['validation_end'])
 for proto in ['h1','h3']:
  for r in json.loads((D/(proto+'-server.json')).read_text()):
   RESPONSE=(R.parent/'speech-records'/F['response_file']).read_bytes()
   verify_chunks(r['response_chunks'],RESPONSE,size,r['service_end'],max(x['complete_s'] for x in r['response_chunks']))
conditions=[]
for mode in ['whole','16k','64k']:
 for proto in ['h1','h3']:
  rr=[r for r in allrows if not r['warmup'] and r['mode']==mode and r['protocol']==proto]
  assert len(rr)==6
  conditions.append(dict(mode=mode,protocol=proto,count=len(rr),median_s=statistics.median(r['validation_end']-r['start'] for r in rr),samples_s=[r['validation_end']-r['start'] for r in rr],fresh_median_s=statistics.median(r['validation_end']-r['start'] for r in rr if r['fresh']),reused_median_s=statistics.median(r['validation_end']-r['start'] for r in rr if not r['fresh'])))
summary=dict(requests=len(allrows),formal_requests=sum(not r['warmup'] for r in allrows),valid=sum(r['valid'] for r in allrows),conditions=conditions,evidence=evidence)
(R/'asr-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(dict(requests=summary['requests'],valid=summary['valid'],conditions=conditions),indent=2))
