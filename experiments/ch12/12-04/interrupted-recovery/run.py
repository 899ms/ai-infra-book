import argparse,asyncio,gzip,hashlib,importlib.util,json,random,ssl,time
from pathlib import Path
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('image_transport',R.parent/'image-records/run_network120.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
NOW=time.perf_counter;FAULT_BYTES=1024**2
class H3(b.QuicConnectionProtocol):
 def __init__(self,*args,server=False,respond=None,**kwargs):
  super().__init__(*args,**kwargs);self.http=b.H3Connection(self._quic);self.server=server;self.respond=respond;self.states={};self.handshake=None
 def quic_event_received(self,event):
  if isinstance(event,b.HandshakeCompleted):self.handshake=dict(alpn=event.alpn_protocol,session_resumed=event.session_resumed,early_data_accepted=event.early_data_accepted)
  if isinstance(event,b.ConnectionTerminated):
   for s in self.states.values():
    if 'future' in s and not s['future'].done():s['future'].set_exception(RuntimeError(str(event)))
  for e in self.http.handle_event(event):
   if not isinstance(e,(b.HeadersReceived,b.DataReceived)):continue
   s=self.states.setdefault(e.stream_id,dict(body=bytearray(),headers=None,first_data=None))
   if isinstance(e,b.HeadersReceived):s['headers']=[(k.decode(),v.decode()) for k,v in e.headers]
   else:
    if e.data and s['first_data'] is None:s['first_data']=NOW()
    s['body'].extend(e.data)
   if self.server:
    if e.stream_ended:asyncio.create_task(self.reply(e.stream_id,s));del self.states[e.stream_id]
   elif (s.get('fault') and len(s['body'])>=FAULT_BYTES) or e.stream_ended:
    s['end']=NOW();s['stream_ended']=e.stream_ended
    if not s['future'].done():s['future'].set_result(s)
 async def reply(self,stream,state):
  status,headers,data=await self.respond('h3',state['headers'],bytes(state['body']))
  self.http.send_headers(stream,[(b':status',str(status).encode())]+headers);self.http.send_data(stream,data,end_stream=True);self.transmit()
 async def request(self,path,op,data,fault):
  stream=self._quic.get_next_available_stream_id();future=asyncio.get_running_loop().create_future();self.states[stream]=dict(future=future,fault=fault,body=bytearray(),headers=None,first_data=None)
  self.http.send_headers(stream,[(b':method',b'POST'),(b':scheme',b'https'),(b':authority',b'localhost'),(b':path',path.encode()),(b'x-operation',op.encode()),(b'content-length',str(len(data)).encode())]);self.http.send_data(stream,data,end_stream=True);self.transmit()
  result=await asyncio.wait_for(future,120);out={k:v for k,v in result.items() if k!='future'};out['body']=bytes(out['body']);return out
async def main(O):
 O.mkdir(exist_ok=False);fingerprint=b.certificate(O);server_records=[];server_errors=[];materialized={};connections=[];rows=[];listeners=[]
 sc=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);sc.minimum_version=sc.maximum_version=ssl.TLSVersion.TLSv1_3;sc.set_alpn_protocols(['http/1.1']);sc.load_cert_chain(O/'certificate.pem',O/'fixture-private-key.pem')
 cc=ssl.create_default_context(cafile=str(O/'certificate.pem'));cc.minimum_version=cc.maximum_version=ssl.TLSVersion.TLSv1_3;cc.set_alpn_protocols(['http/1.1'])
 async def respond(proto,headers,body):
  h=dict(headers);op=h['x-operation'];path=h[':path'];rec=dict(protocol=proto,operation=op,path=path,request_bytes=len(body),request_sha256=hashlib.sha256(body).hexdigest(),received_s=NOW());server_records.append(rec)
  if path=='/image':
   assert body==b.PAYLOAD;rec['service_start_s']=NOW();await asyncio.sleep(b.SERVICE_S);rec['service_end_s']=NOW();materialized[op]=b.RESPONSE;offset=0;status=200
  else:
   assert path.startswith('/resume/') and not body and op in materialized;offset=int(path.split('/')[-1]);assert 0<offset<len(b.RESPONSE);status=206
  data=materialized[op][offset:];rec.update(offset=offset,status=status,response_bytes=len(data),response_sha256=hashlib.sha256(data).hexdigest(),prepared_s=NOW())
  hh=[(b'content-length',str(len(data)).encode()),(b'content-type',b'image/jpeg'),(b'etag',('"'+b.RESPONSE_HASH+'"').encode())]
  if offset:hh.append((b'content-range',f'bytes {offset}-{len(b.RESPONSE)-1}/{len(b.RESPONSE)}'.encode()))
  return status,hh,data
 async def h1_server(reader,writer):
  conn=b.h11.Connection(b.h11.SERVER);body=bytearray();headers=[]
  try:
   while True:
    e=await b.h1_event(conn,reader)
    if isinstance(e,b.h11.Request):headers=[(k.decode(),v.decode()) for k,v in e.headers]+[(':path',e.target.decode())]
    elif isinstance(e,b.h11.Data):body.extend(e.data)
    elif isinstance(e,b.h11.EndOfMessage):break
    elif isinstance(e,b.h11.ConnectionClosed):return
   status,hh,data=await respond('h1',headers,bytes(body))
   for e in [b.h11.Response(status_code=status,headers=hh),b.h11.Data(data=data),b.h11.EndOfMessage()]:writer.write(conn.send(e))
   await writer.drain()
  except Exception as e:server_errors.append(dict(time_s=NOW(),headers=headers,error=repr(e)))
  finally:
   writer.close()
   try:await writer.wait_closed()
   except Exception as e:server_errors.append(dict(time_s=NOW(),headers=headers,error=repr(e),phase='wait_closed'))
 tcp=await asyncio.start_server(h1_server,'127.0.0.1',0,ssl=sc);port=tcp.sockets[0].getsockname()[1]
 qc=b.QuicConfiguration(is_client=False,alpn_protocols=b.H3_ALPN);qc.load_cert_chain(O/'certificate.pem',O/'fixture-private-key.pem');udp=await b.serve('127.0.0.1',0,configuration=qc,create_protocol=lambda *a,**kw:H3(*a,server=True,respond=respond,**kw));qport=udp._transport.get_extra_info('sockname')[1]
 async def exchange(proto,path,op,data,fault):
  rec=dict(connection=len(connections),protocol=proto,path=path,operation=op,upload_bytes=len(data),upload_sha256=hashlib.sha256(data).hexdigest(),fault_requested=fault,start_s=NOW());connections.append(rec);body=None
  if proto=='h1':
   reader,writer=await asyncio.wait_for(asyncio.open_connection('127.0.0.1',port,ssl=cc,server_hostname='localhost'),20);ss=writer.get_extra_info('ssl_object');rec.update(ready_s=NOW(),alpn=ss.selected_alpn_protocol(),tls=ss.version(),session_resumed=ss.session_reused,local=writer.get_extra_info('sockname'),certificate_sha256=hashlib.sha256(ss.getpeercert(binary_form=True)).hexdigest());conn=b.h11.Connection(b.h11.CLIENT)
   async def transfer():
    for e in [b.h11.Request(method='POST',target=path,headers=[('Host','localhost'),('x-operation',op),('Content-Length',str(len(data)))]),b.h11.Data(data=data),b.h11.EndOfMessage()]:writer.write(conn.send(e))
    await writer.drain();state=dict(body=bytearray(),headers=None,first_data=None,stream_ended=False)
    while True:
     e=await b.h1_event(conn,reader)
     if isinstance(e,b.h11.Response):state['headers']=[(':status',str(e.status_code))]+[(k.decode(),v.decode()) for k,v in e.headers]
     elif isinstance(e,b.h11.Data):
      if e.data and state['first_data'] is None:state['first_data']=NOW()
      state['body'].extend(e.data)
      if fault and len(state['body'])>=FAULT_BYTES:break
     elif isinstance(e,b.h11.EndOfMessage):state['stream_ended']=True;break
     elif isinstance(e,b.h11.ConnectionClosed):raise RuntimeError('premature EOF')
    state['end']=NOW();state['body']=bytes(state['body']);return state
   try:state=await asyncio.wait_for(transfer(),120)
   finally:
    rec['close_start_s']=NOW();writer.transport.abort() if fault else writer.close()
    try:await writer.wait_closed()
    except (ConnectionResetError,BrokenPipeError):pass
    rec['closed_s']=NOW()
  else:
   qlog=b.QuicLogger();cfg=b.QuicConfiguration(is_client=True,alpn_protocols=b.H3_ALPN,server_name='localhost',verify_mode=ssl.CERT_REQUIRED,cafile=str(O/'certificate.pem'),quic_logger=qlog);ctx=b.connect('127.0.0.1',qport,configuration=cfg,create_protocol=H3,wait_connected=True);p=await asyncio.wait_for(ctx.__aenter__(),20);rec.update(ready_s=NOW(),**p.handshake,local=p._transport.get_extra_info('sockname'))
   try:state=await p.request(path,op,data,fault)
   finally:
    rec['close_start_s']=NOW();await ctx.__aexit__(None,None,None);rec['closed_s']=NOW()
    with gzip.open(O/f"qlog-{rec['connection']}.json.gz",'wt') as f:json.dump(qlog.to_dict(),f)
  body=state.pop('body');hh=dict(state['headers']);assert hh['etag']=='\"'+b.RESPONSE_HASH+'\"' and hh[':status']==('206' if path.startswith('/resume/') else '200');rec.update(**state,received_bytes=len(body),received_sha256=hashlib.sha256(body).hexdigest());(O/f"response-{rec['connection']}.bin").write_bytes(body);return body,rec
 order=[]
 for proto in ['h1','h3']:order.append(dict(trial=-1,protocol=proto,policy='uninterrupted',warmup=True))
 for trial in range(3):
  cells=[dict(trial=trial,protocol=p,policy=k,warmup=False) for p in ['h1','h3'] for k in ['uninterrupted','restart','resume']];random.Random(120406+trial).shuffle(cells);order.extend(cells)
 (O/'order.json').write_text(json.dumps(order,indent=2)+'\n');(O/'environment.json').write_text(json.dumps(dict(source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),transport_source_sha256=hashlib.sha256((R.parent/'image-records/run_network120.py').read_bytes()).hexdigest(),fixture=b.FIXTURE,certificate_sha256=fingerprint,fault_bytes=FAULT_BYTES,scope='Actual connection interruption and image-byte recovery; recorded CPU service; in-memory retained final object'),indent=2)+'\n')
 try:
  for index,c in enumerate(order):
   op=f'op{index}';start=NOW();row=dict(**c,operation=op,start_s=start,exchanges=[])
   try:
    part,rec=await exchange(c['protocol'],'/image',op,b.PAYLOAD,c['policy']!='uninterrupted');row['exchanges'].append(rec['connection'])
    if c['policy']=='uninterrupted':complete=part
    else:
     assert FAULT_BYTES<=len(part)<len(b.RESPONSE) and not rec['stream_ended'];row['interrupted_prefix_bytes']=len(part);row['interrupted_prefix_sha256']=hashlib.sha256(part).hexdigest()
     if c['policy']=='restart':tail,nextrec=await exchange(c['protocol'],'/image',op,b.PAYLOAD,False);complete=tail
     else:
      tail,nextrec=await exchange(c['protocol'],f'/resume/{len(part)}',op,b'',False);hh=dict(nextrec['headers']);assert hh[':status']=='206' and hh['content-range']==f'bytes {len(part)}-{len(b.RESPONSE)-1}/{len(b.RESPONSE)}';complete=part+tail
     row['exchanges'].append(nextrec['connection'])
    assert complete==b.RESPONSE
    with b.Image.open(b.io.BytesIO(complete)) as im:im.load();rgb=im.convert('RGB');shape=[rgb.height,rgb.width,3];pixel_hash=hashlib.sha256(rgb.tobytes()).hexdigest()
    assert shape==b.FIXTURE['shape'] and pixel_hash==b.FIXTURE['decoded_sha256'];row.update(valid=True,decoded_sha256=pixel_hash,bytes=len(complete),sha256=hashlib.sha256(complete).hexdigest())
   except Exception as e:row.update(valid=False,error=repr(e))
   row['validation_end_s']=NOW();rows.append(row)
   with (O/'requests.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
   print(index,c,row['valid'],flush=True)
   if c['warmup'] and not row['valid']:raise RuntimeError('warmup failed; formal trials not started')
 finally:
  tcp.close();await tcp.wait_closed();udp.close();await asyncio.sleep(.2)
  for name,value in [('connections',connections),('server-records',server_records),('server-errors',server_errors)]: (O/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
  (O/'completion.json').write_text(json.dumps(dict(requests=len(rows),valid=sum(r['valid'] for r in rows),listeners_closed=True))+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();asyncio.run(main(args.output))
