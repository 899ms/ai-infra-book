import sys,importlib.metadata,argparse,asyncio,hashlib,io,json,random,time,wave
from pathlib import Path
from fixtures import load
from producer import Operation
from transport import Network
R=Path(__file__).resolve().parent;NOW=time.perf_counter
async def main(workload,O):
 O.mkdir(exist_ok=False);fixtures=load(workload);operations={};rows=[];faults=[]
 def prepare(h,body):
  identity=h['x-operation'];step=int(h['x-step']);assert 0<=step<len(fixtures);f=fixtures[step];path=h[':path']
  if path=='/start':
   assert body==f['request'] and identity not in operations;operations[identity]=Operation(identity,f,body);return operations[identity],0
  assert path.startswith('/resume/') and not body and identity in operations;op=operations[identity];assert op.fixture is f;offset=int(path.split('/')[-1]);assert 0<=offset<len(f['response']);return op,offset
 net=Network(O,prepare);await net.start()
 order=[dict(trial=-1,protocol=p,policy='uninterrupted',warmup=True) for p in ['h1','h3']]
 for trial in range(3):
  cc=[dict(trial=trial,protocol=p,policy=k,warmup=False) for p in ['h1','h3'] for k in ['uninterrupted','restart','resume']];random.Random(120407+trial).shuffle(cc);order.extend(cc)
 (O/'order.json').write_text(json.dumps(order,indent=2)+'\n');(O/'environment.json').write_text(json.dumps(dict(workload=workload,python=sys.version,packages={k:importlib.metadata.version(k) for k in ['aioquic','h11','cryptography']},certificate_sha256=net.certificate_sha256,sources=[f['source'] for f in fixtures],source_sha256={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['run.py','producer.py','transport.py','fixtures.py','PROTOCOL.md','../image-records/run_network120.py']},scope='Recorded model producer survives client connection loss; actual transfers, no fresh GPU inference or browser actions'),indent=2)+'\n')
 try:
  for episode,c in enumerate(order):
   row=dict(**c,episode=episode,start_s=NOW(),rounds=[],delivered_steps=[],actions=[]);steps=[0] if c['warmup'] else range(len(fixtures))
   try:
    for step in steps:
     f=fixtures[step];identity=f'e{episode}-s{step}';target=3 if workload=='computer' else 0;inject=c['policy']!='uninterrupted' and step==target;fault=('frame' if workload=='tts' else 'headers') if inject else None
     part,first=await net.exchange(c['protocol'],'/start',identity,step,f['request'],fault);rr=dict(step=step,start_s=first['start_s'],connections=[first['connection']],source_response_sha256=hashlib.sha256(f['response']).hexdigest())
     if inject:
      assert not first['stream_ended']
      if workload=='tts':assert 1808<=len(part)<len(f['response']) and part==f['response'][:len(part)]
      else:assert not part
      faults.append(dict(episode=episode,operation=identity,connection=first['connection'],close_start_s=first['close_start_s']));rr['prefix_bytes']=len(part);rr['prefix_sha256']=hashlib.sha256(part).hexdigest()
      if c['policy']=='restart':tail,last=await net.exchange(c['protocol'],'/start',identity+'-retry',step,f['request'],None);complete=tail
      else:
       tail,last=await net.exchange(c['protocol'],f'/resume/{len(part)}',identity,step,b'',None);hh=dict(last['headers']);assert hh[':status']==('206' if part else '200')
       if part:assert hh['content-range']==f'bytes {len(part)}-{len(f["response"])-1}/{len(f["response"])}'
       complete=part+tail
      assert first['closed_s']<=last['start_s'] and first['local']!=last['local'];rr['connections'].append(last['connection'])
     else:complete=part;last=first
     hh=dict(last['headers']);assert last['stream_ended'] and hh['etag']=='"'+hashlib.sha256(f['response']).hexdigest()+'"' and complete==f['response']
     if workload=='tts':
      with wave.open(io.BytesIO(complete),'rb') as w:fmt=[w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes()];pcm=w.readframes(w.getnframes())
      assert fmt==[1,2,44100,591872];rr.update(wav_format=fmt,pcm_sha256=hashlib.sha256(pcm).hexdigest())
     elif workload=='computer':action=json.loads(complete);assert action==f['source']['action'];row['actions'].append(action)
     else:assert complete.decode('utf-8')==f['response'].decode('utf-8')
     rr.update(validation_end_s=NOW(),complete_bytes=len(complete),complete_sha256=hashlib.sha256(complete).hexdigest());row['rounds'].append(rr);row['delivered_steps'].append(step)
    assert row['delivered_steps']==list(steps);row['result_valid']=True
   except Exception as e:row.update(result_valid=False,error=repr(e))
   row['validation_end_s']=NOW();rows.append(row)
   with (O/'progress.jsonl').open('a') as out:out.write(json.dumps(row)+'\n')
   print(episode,c,row['result_valid'],flush=True)
   if c['warmup'] and not row['result_valid']:raise RuntimeError('warmup failed; formal trials not started')
 finally:
  await asyncio.gather(*(op.task for op in operations.values()))
  await net.stop()
  for f in faults:
   op=operations[f['operation']];f.update(producer_done_s=op.done_s,during_production=f['close_start_s']<op.done_s)
  for row in rows:
   ff=[f for f in faults if f['episode']==row['episode']];row['protocol_valid']=all(f['during_production'] for f in ff);row['valid']=row['result_valid'] and row['protocol_valid']
  (O/'requests.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows));(O/'operations.json').write_text(json.dumps([op.record() for op in operations.values()],indent=2)+'\n');(O/'faults.json').write_text(json.dumps(faults,indent=2)+'\n');(O/'completion.json').write_text(json.dumps(dict(tasks=len(rows),valid=sum(r['valid'] for r in rows),exchanges=len(net.connections),operations=len(operations),faults=len(faults),listeners_closed=True))+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--workload',choices=['asr','tts','computer'],required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();asyncio.run(main(a.workload,a.output))
