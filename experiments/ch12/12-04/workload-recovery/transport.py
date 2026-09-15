"""Actual TLS/H3 exchanges and client-triggered interruption; no model execution."""
import asyncio,gzip,hashlib,importlib.util,json,socket,ssl,time
from pathlib import Path
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('transport_base',R.parent/'image-records/run_network120.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
NOW=time.perf_counter

def tcp_info(writer):
 s=writer.get_extra_info('socket');n=s.getsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY);assert n==1 and s.proto==6
 return dict(tcp_nodelay=n,python_socket_proto=s.proto,local=writer.get_extra_info('sockname'))
class H3(b.QuicConnectionProtocol):
 def __init__(self,*args,server=False,respond=None,**kw):
  super().__init__(*args,**kw);self.http=b.H3Connection(self._quic);self.server=server;self.respond=respond;self.states={};self.handshake=None
 def quic_event_received(self,event):
  if isinstance(event,b.HandshakeCompleted):self.handshake=dict(alpn=event.alpn_protocol,session_resumed=event.session_resumed,early_data_accepted=event.early_data_accepted)
  if isinstance(event,b.ConnectionTerminated):
   for s in self.states.values():
    if 'future' in s and not s['future'].done():s['future'].set_exception(RuntimeError(str(event)))
  for e in self.http.handle_event(event):
   if not isinstance(e,(b.HeadersReceived,b.DataReceived)):continue
   s=self.states.setdefault(e.stream_id,dict(body=bytearray(),headers=None,first_data=None,arrivals=[]))
   if not self.server and s.get('future') is not None and s['future'].done():continue
   if isinstance(e,b.HeadersReceived):s['headers']=[(k.decode(),v.decode()) for k,v in e.headers];s['headers_s']=NOW()
   else:
    if e.data and s['first_data'] is None:s['first_data']=NOW()
    s['body'].extend(e.data);s['arrivals'].append(dict(at_s=NOW(),bytes=len(e.data),total=len(s['body'])))
   if self.server:
    if e.stream_ended:asyncio.create_task(self.respond(self,e.stream_id,s));del self.states[e.stream_id]
   else:
    fault=s.get('fault');trigger=(fault=='headers' and s['headers'] is not None) or (fault=='frame' and len(s['body'])>=1808)
    if trigger or e.stream_ended:
     s['end_s']=NOW();s['stream_ended']=e.stream_ended
     if not s['future'].done():s['future'].set_result(s)
 async def request(self,path,op,step,data,fault):
  stream=self._quic.get_next_available_stream_id();future=asyncio.get_running_loop().create_future();self.states[stream]=dict(future=future,fault=fault,body=bytearray(),headers=None,first_data=None,arrivals=[])
  self.http.send_headers(stream,[(b':method',b'POST'),(b':scheme',b'https'),(b':authority',b'localhost'),(b':path',path.encode()),(b'x-operation',op.encode()),(b'x-step',str(step).encode()),(b'content-length',str(len(data)).encode())]);self.http.send_data(stream,data,end_stream=True);self.transmit()
  result=await asyncio.wait_for(future,120);out={k:v for k,v in result.items() if k!='future'};out['body']=bytes(out['body']);return out
class Network:
 def __init__(self,out,prepare):self.out=out;self.prepare=prepare;self.connections=[];self.server_errors=[];self.server_records=[];self.writers=set();self.tasks=set()
 async def start(self):
  self.certificate_sha256=b.certificate(self.out)
  self.sc=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);self.sc.minimum_version=self.sc.maximum_version=ssl.TLSVersion.TLSv1_3;self.sc.set_alpn_protocols(['http/1.1']);self.sc.load_cert_chain(self.out/'certificate.pem',self.out/'fixture-private-key.pem')
  self.cc=ssl.create_default_context(cafile=str(self.out/'certificate.pem'));self.cc.minimum_version=self.cc.maximum_version=ssl.TLSVersion.TLSv1_3;self.cc.set_alpn_protocols(['http/1.1'])
  self.tcp=await asyncio.start_server(self.h1_server,'127.0.0.1',0,ssl=self.sc);self.port=self.tcp.sockets[0].getsockname()[1]
  qc=b.QuicConfiguration(is_client=False,alpn_protocols=b.H3_ALPN);qc.load_cert_chain(self.out/'certificate.pem',self.out/'fixture-private-key.pem');self.udp=await b.serve('127.0.0.1',0,configuration=qc,create_protocol=lambda *a,**kw:H3(*a,server=True,respond=self.h3_server,**kw));self.qport=self.udp._transport.get_extra_info('sockname')[1]
 def prepare_response(self,proto,headers,body):
  received=NOW();op,offset=self.prepare(dict(headers),body);f=op.fixture;rec=dict(protocol=proto,operation=op.identity,step=f['step'],request_bytes=len(body),request_sha256=hashlib.sha256(body).hexdigest(),received_s=received,offset=offset,emissions=[]);self.server_records.append(rec)
  status=206 if offset else 200;hh=[(b'content-length',str(len(f['response'])-offset).encode()),(b'etag',('"'+hashlib.sha256(f['response']).hexdigest()+'"').encode()),(b'x-operation',op.identity.encode())]
  if offset:hh.append((b'content-range',f"bytes {offset}-{len(f['response'])-1}/{len(f['response'])}".encode()))
  rec['headers_s']=NOW();return op,offset,status,hh,rec
 async def h1_server(self,reader,writer):
  task=asyncio.current_task();self.tasks.add(task);self.writers.add(writer);headers=[];conn=b.h11.Connection(b.h11.SERVER);body=bytearray()
  try:
   sock=tcp_info(writer)
   while True:
    e=await b.h1_event(conn,reader)
    if isinstance(e,b.h11.Request):headers=[(k.decode(),v.decode()) for k,v in e.headers]+[(':path',e.target.decode())]
    elif isinstance(e,b.h11.Data):body.extend(e.data)
    elif isinstance(e,b.h11.EndOfMessage):break
    elif isinstance(e,b.h11.ConnectionClosed):return
   op,offset,status,hh,rec=self.prepare_response('h1',headers,bytes(body));rec['socket']=sock;writer.write(conn.send(b.h11.Response(status_code=status,headers=hh)));await writer.drain()
   async for start,data in op.suffix_parts(offset):
    sent=NOW();writer.write(conn.send(b.h11.Data(data=data)));await writer.drain();rec['emissions'].append(dict(offset=start,bytes=len(data),before_s=sent,after_s=NOW()))
   writer.write(conn.send(b.h11.EndOfMessage()));await writer.drain();rec['complete_s']=NOW()
  except Exception as e:self.server_errors.append(dict(headers=headers,error=repr(e),at_s=NOW()))
  finally:
   writer.close()
   try:await writer.wait_closed()
   except Exception as e:self.server_errors.append(dict(headers=headers,error=repr(e),phase='wait_closed',at_s=NOW()))
   self.writers.discard(writer);self.tasks.discard(task)
 async def h3_server(self,p,stream,state):
  task=asyncio.current_task();self.tasks.add(task)
  try:
   op,offset,status,hh,rec=self.prepare_response('h3',state['headers'],bytes(state['body']));p.http.send_headers(stream,[(b':status',str(status).encode())]+hh);p.transmit()
   async for start,data in op.suffix_parts(offset):
    before=NOW();p.http.send_data(stream,data,end_stream=start+len(data)==len(op.fixture['response']));p.transmit();rec['emissions'].append(dict(offset=start,bytes=len(data),before_s=before,after_s=NOW()))
   rec['complete_s']=NOW()
  except Exception as e:self.server_errors.append(dict(headers=state['headers'],error=repr(e),at_s=NOW()))
  finally:self.tasks.discard(task)
 async def exchange(self,proto,path,op,step,data,fault):
  rec=dict(connection=len(self.connections),protocol=proto,path=path,operation=op,step=step,upload_bytes=len(data),upload_sha256=hashlib.sha256(data).hexdigest(),fault_requested=fault,start_s=NOW());self.connections.append(rec)
  if proto=='h1':
   reader,writer=await asyncio.wait_for(asyncio.open_connection('127.0.0.1',self.port,ssl=self.cc,server_hostname='localhost'),20);ss=writer.get_extra_info('ssl_object');rec.update(ready_s=NOW(),alpn=ss.selected_alpn_protocol(),tls=ss.version(),session_resumed=ss.session_reused,certificate_sha256=hashlib.sha256(ss.getpeercert(binary_form=True)).hexdigest(),**tcp_info(writer));conn=b.h11.Connection(b.h11.CLIENT)
   async def transfer():
    for e in [b.h11.Request(method='POST',target=path,headers=[('Host','localhost'),('x-operation',op),('x-step',str(step)),('Content-Length',str(len(data)))]),b.h11.Data(data=data),b.h11.EndOfMessage()]:writer.write(conn.send(e))
    await writer.drain();state=dict(body=bytearray(),headers=None,first_data=None,stream_ended=False,arrivals=[])
    while True:
     e=await b.h1_event(conn,reader)
     if isinstance(e,b.h11.Response):
      state['headers']=[(':status',str(e.status_code))]+[(k.decode(),v.decode()) for k,v in e.headers];state['headers_s']=NOW()
      if fault=='headers':break
     elif isinstance(e,b.h11.Data):
      if e.data and state['first_data'] is None:state['first_data']=NOW()
      state['body'].extend(e.data);state['arrivals'].append(dict(at_s=NOW(),bytes=len(e.data),total=len(state['body'])))
      if fault=='frame' and len(state['body'])>=1808:break
     elif isinstance(e,b.h11.EndOfMessage):state['stream_ended']=True;break
     elif isinstance(e,b.h11.ConnectionClosed):raise RuntimeError('premature EOF')
    state['end_s']=NOW();state['body']=bytes(state['body']);return state
   try:state=await asyncio.wait_for(transfer(),120)
   finally:
    rec['close_start_s']=NOW();writer.transport.abort() if fault else writer.close()
    try:await writer.wait_closed()
    except (ConnectionResetError,BrokenPipeError):pass
    rec['closed_s']=NOW()
  else:
   qlog=b.QuicLogger();cfg=b.QuicConfiguration(is_client=True,alpn_protocols=b.H3_ALPN,server_name='localhost',verify_mode=ssl.CERT_REQUIRED,cafile=str(self.out/'certificate.pem'),quic_logger=qlog);ctx=b.connect('127.0.0.1',self.qport,configuration=cfg,create_protocol=H3,wait_connected=True);p=await asyncio.wait_for(ctx.__aenter__(),20);rec.update(ready_s=NOW(),**p.handshake,local=p._transport.get_extra_info('sockname'))
   try:state=await p.request(path,op,step,data,fault)
   finally:
    rec['close_start_s']=NOW();await ctx.__aexit__(None,None,None);rec['closed_s']=NOW()
    with gzip.open(self.out/f"qlog-{rec['connection']}.json.gz",'wt') as f:json.dump(qlog.to_dict(),f)
  body=state.pop('body');rec.update(**state,retained_bytes=len(body),retained_sha256=hashlib.sha256(body).hexdigest());(self.out/f"response-{rec['connection']}.bin").write_bytes(body);assert dict(rec['headers'])['x-operation']==op;return body,rec
 async def stop(self):
  self.tcp.close();await self.tcp.wait_closed();self.udp.close()
  for w in list(self.writers):w.close()
  if self.tasks:await asyncio.wait_for(asyncio.gather(*list(self.tasks),return_exceptions=True),10)
  for n,v in [('connections',self.connections),('server-records',self.server_records),('server-errors',self.server_errors)]:(self.out/(n+'.json')).write_text(json.dumps(v,indent=2)+'\n')
