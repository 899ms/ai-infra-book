"""Reconstruct recovery outcomes from source bytes and raw transport records."""
import argparse,gzip,hashlib,json,random,statistics
from pathlib import Path
from fixtures import load
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def analyze(workload):
 O=R/'results'/workload;D=O/'run';fixtures=load(workload)
 env=read(D/'environment.json');assert env['workload']==workload
 for n,h in env['source_sha256'].items():assert sha((R/n).read_bytes())==h
 assert env['sources']==[f['source'] for f in fixtures]
 rows=[json.loads(x) for x in (D/'requests.jsonl').read_text().splitlines()];cc=read(D/'connections.json');ss=read(D/'server-records.json');ops=read(D/'operations.json');faults=read(D/'faults.json')
 expected_ex=158 if workload=='computer' else 32;expected_ops=152 if workload=='computer' else 26
 assert len(rows)==20 and len(cc)==len(ss)==expected_ex and len(ops)==expected_ops and len(faults)==12
 order=[dict(trial=-1,protocol=p,policy='uninterrupted',warmup=True) for p in ['h1','h3']]
 for trial in range(3):
  batch=[dict(trial=trial,protocol=p,policy=k,warmup=False) for p in ['h1','h3'] for k in ['uninterrupted','restart','resume']];random.Random(120407+trial).shuffle(batch);order.extend(batch)
 assert read(D/'order.json')==order
 opmap={o['identity']:o for o in ops};assert len(opmap)==len(ops)
 for op in ops:
  step=int(op['identity'].split('-s')[1].split('-')[0]);f=fixtures[step];assert op['source_request_sha256']==sha(f['request']) and op['response_sha256']==sha(f['response'])
  assert op['release_plan']==f['release_plan'] and op['available']==len(f['response']) and len(op['releases'])==len(f['release_plan'])
  prev=op['start_s']
  for plan,release in zip(f['release_plan'],op['releases']):
   assert release['offset']==plan['offset'] and release['bytes']==plan['bytes']
   assert release['at_s']>=prev and release['at_s']-op['start_s']+1e-6>=plan['ready_s'];prev=release['at_s']
  assert op['done_s']>=prev
 used=[];fault_connections=[]
 for i,(row,cond) in enumerate(zip(rows,order)):
  assert row['episode']==i and all(row[k]==v for k,v in cond.items()) and row['valid'] and row['result_valid'] and row['protocol_valid']
  steps=[0] if cond['warmup'] else list(range(len(fixtures)));assert row['delivered_steps']==steps and len(row['rounds'])==len(steps)
  if workload=='computer':assert row['actions']==[fixtures[j]['source']['action'] for j in steps]
  for step,rr in zip(steps,row['rounds']):
   f=fixtures[step];identity=f'e{i}-s{step}';inject=cond['policy']!='uninterrupted' and step==(3 if workload=='computer' else 0)
   assert rr['step']==step and len(rr['connections'])==(2 if inject else 1)
   connections=[cc[j] for j in rr['connections']];used.extend(rr['connections']);first=connections[0];last=connections[-1]
   assert first['operation']==identity and first['path']=='/start' and first['upload_sha256']==sha(f['request'])
   prefix=(D/f"response-{first['connection']}.bin").read_bytes()
   if inject:
    fault_connections.append(first['connection']);assert not first['stream_ended'];assert first['closed_s']<=last['start_s'] and first['local']!=last['local']
    assert first['close_start_s']<opmap[identity]['done_s'];assert rr['prefix_bytes']==len(prefix) and rr['prefix_sha256']==sha(prefix)
    if workload=='tts':assert 1808<=len(prefix)<len(f['response']) and prefix==f['response'][:len(prefix)] and first['fault_requested']=='frame'
    else:assert prefix==b'' and first['fault_requested']=='headers'
    if cond['policy']=='restart':assert last['operation']==identity+'-retry' and last['path']=='/start';complete=(D/f"response-{last['connection']}.bin").read_bytes()
    else:
     assert last['operation']==identity and last['path']==f'/resume/{len(prefix)}' and last['upload_bytes']==0
     complete=prefix+(D/f"response-{last['connection']}.bin").read_bytes()
   else:assert first['fault_requested'] is None;complete=prefix
   assert complete==f['response'] and last['stream_ended'] and last['fault_requested'] is None
   assert rr['complete_bytes']==len(complete) and rr['complete_sha256']==rr['source_response_sha256']==sha(complete)
   assert rr['start_s']==first['start_s'] and rr['validation_end_s']>=last['closed_s'] and row['validation_end_s']>=rr['validation_end_s']
 assert used==list(range(expected_ex))
 for c in cc:
  f=fixtures[c['step']];offset=int(c['path'].split('/')[-1]) if c['path'].startswith('/resume/') else 0;upload=b'' if c['path'].startswith('/resume/') else f['request']
  assert c['upload_bytes']==len(upload) and c['upload_sha256']==sha(upload)
  body=(D/f"response-{c['connection']}.bin").read_bytes();assert len(body)==c['retained_bytes'] and sha(body)==c['retained_sha256'] and body==f['response'][offset:offset+len(body)]
  assert c['start_s']<=c['ready_s']<=c['headers_s']<=c['end_s']<=c['close_start_s']<=c['closed_s']
  total=0;prev=c['headers_s']
  for a in c['arrivals']:total+=a['bytes'];assert a['total']==total and prev<=a['at_s']<=c['end_s'];prev=a['at_s']
  assert total==len(body)
  hh=dict(c['headers']);assert hh[':status']==('206' if offset else '200') and int(hh['content-length'])==len(f['response'])-offset and hh['etag']=='"'+sha(f['response'])+'"' and hh['x-operation']==c['operation']
  if offset:assert hh['content-range']==f'bytes {offset}-{len(f["response"])-1}/{len(f["response"])}'
  matching=[s for s in ss if s['protocol']==c['protocol'] and s['operation']==c['operation'] and s['offset']==offset and s['request_sha256']==sha(upload)]
  assert len(matching)==1;s=matching[0];op=opmap[c['operation']]
  assert s['request_bytes']==len(upload) and c['ready_s']<=s['received_s']<=s['headers_s']<=c['headers_s']
  if c['path']=='/start':assert s['received_s']<=op['start_s']<=s['headers_s']
  expected=[dict(offset=max(offset,p['offset']),bytes=p['offset']+p['bytes']-max(offset,p['offset']),at_s=r['at_s']) for p,r in zip(op['release_plan'],op['releases']) if p['offset']+p['bytes']>offset]
  assert len(s['emissions'])<=len(expected)
  for e,p in zip(s['emissions'],expected):assert e['offset']==p['offset'] and e['bytes']==p['bytes'] and p['at_s']<=e['before_s']<=e['after_s']
  if c['fault_requested'] is None:assert len(s['emissions'])==len(expected) and 'complete_s' in s
  for a in c['arrivals']:
   if a['bytes']:assert next(r['at_s'] for p,r in zip(op['release_plan'],op['releases']) if p['offset']+p['bytes']>=offset+a['total'])<=a['at_s']
  assert not c['session_resumed']
  if c['protocol']=='h1':
   assert c['alpn']=='http/1.1' and c['tls']=='TLSv1.3' and c['certificate_sha256']==env['certificate_sha256']
   for x in [c,s['socket']]:assert x['tcp_nodelay']==1 and x['python_socket_proto']==6
  else:
   assert c['alpn']=='h3' and not c['early_data_accepted'];q=json.load(gzip.open(D/f"qlog-{c['connection']}.json.gz",'rt'));assert q['qlog_version']=='0.3'
   events=[e for t in q['traces'] for e in t['events']];params=[e['data'] for e in events if e['name']=='transport:parameters_set'];assert len(params)==2
   for p in params:assert p['initial_max_data']==1048576 and p['initial_max_stream_data_bidi_local']==p['initial_max_stream_data_bidi_remote']==1048576
   headers=[e for e in events if e['name']=='http:frame_parsed' and e['data']['frame']['frame_type']=='headers'];assert len(headers)==1
 assert sorted(f['connection'] for f in faults)==sorted(fault_connections)
 for f in faults:assert f['during_production'] and f['close_start_s']==cc[f['connection']]['close_start_s'] and f['producer_done_s']==opmap[f['operation']]['done_s']
 errors=read(D/'server-errors.json')
 for e in errors:
  h=dict(e['headers']);assert any(c['operation']==h['x-operation'] and c['fault_requested'] is not None for c in cc)
  assert e['error'].startswith(('ConnectionResetError(', 'BrokenPipeError(')),e
 image=read(O/'image-inspect.json')[0];assert image['Id']=='sha256:bc544dc84aa48ca11602c4840b9f9642c129fa882ce24d4579dedf80c6026396'
 container=read(O/'container-inspect.json')[0];h=container['HostConfig'];assert h['NetworkMode']=='none' and h['NanoCpus']==2000000000 and h['Memory']==2147483648 and 'NET_ADMIN' in [x.removeprefix('CAP_') for x in h['CapAdd']]
 for n in ['before','after']:
  netem=next(x for x in read(O/f'{n}.json') if x['kind']=='netem');opts=netem['options'];assert opts['delay']['delay']==.04 and opts['rate']['rate']==2500000 and abs(opts['loss-random']['loss']-.001)<1e-8
  assert netem['backlog']==0 and netem['qlen']==0
 assert (O/'container-removed.txt').read_text().strip()=='book-workload-recovery1204'
 completion=read(D/'completion.json');assert completion==dict(tasks=20,valid=20,exchanges=expected_ex,operations=expected_ops,faults=12,listeners_closed=True)
 conditions=[]
 for proto in ['h1','h3']:
  for policy in ['uninterrupted','restart','resume']:
   values=[r['validation_end_s']-r['start_s'] for r in rows if not r['warmup'] and r['protocol']==proto and r['policy']==policy];assert len(values)==3
   selected=[r for r in rows if not r['warmup'] and r['protocol']==proto and r['policy']==policy]
   accounting=[]
   for row in selected:
    xc=[cc[j] for rr in row['rounds'] for j in rr['connections']]
    fc=[c for c in xc if c['fault_requested'] is not None]
    accounting.append(dict(episode=row['episode'],upload_bytes=sum(c['upload_bytes'] for c in xc),retained_response_bytes=sum(c['retained_bytes'] for c in xc),discarded_prefix_bytes=sum(c['retained_bytes'] for c in fc) if policy=='restart' else 0,source_jobs=len({c['operation'] for c in xc}),close_s=sum(c['closed_s']-c['close_start_s'] for c in xc),post_interruption_s=row['validation_end_s']-fc[0]['close_start_s'] if fc else None))
   conditions.append(dict(protocol=proto,policy=policy,samples_s=values,median_s=statistics.median(values),accounting=accounting))
 result=dict(verified=True,workload=workload,tasks=20,formal_tasks=18,exchanges=expected_ex,operations=expected_ops,faults=12,expected_disconnect_errors=errors,conditions=conditions)
 (R/f'{workload}-summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--workload',required=True,choices=['asr','tts','computer']);analyze(p.parse_args().workload)
