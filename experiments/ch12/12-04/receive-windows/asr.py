import io,os,socket
from PIL import Image
import argparse,asyncio,datetime,gzip,hashlib,importlib.metadata,ipaddress,json,platform,random,ssl,time
from pathlib import Path
import h11
from aioquic.asyncio import connect,serve,QuicConnectionProtocol
from aioquic.h3.connection import H3Connection,H3_ALPN
from aioquic.h3.events import HeadersReceived,DataReceived
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import HandshakeCompleted,ConnectionTerminated
from aioquic.quic.logger import QuicLogger
from cryptography import x509
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID
R=Path(__file__).resolve().parent
SOURCE=R.parent/'speech-records'
MODE=os.environ['BOOK_WINDOW_MODE'];WINDOW={'default':None,'64k':65536,'4m':4194304}[MODE]
FIXTURE=json.loads((SOURCE/'asr-fixture.json').read_text());PAYLOAD=(SOURCE/FIXTURE['upload_file']).read_bytes();RESPONSE=(SOURCE/FIXTURE['response_file']).read_bytes();HASH=hashlib.sha256(PAYLOAD).hexdigest();RESPONSE_HASH=hashlib.sha256(RESPONSE).hexdigest();SERVICE_S=FIXTURE['service_s']
assert HASH==FIXTURE['upload_sha256'] and RESPONSE_HASH==FIXTURE['response_sha256']
REQUEST_TIMEOUT=120
NOW=time.perf_counter

def socket_record(sock):
 assert sock.getsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY)==1 and sock.proto==socket.IPPROTO_TCP
 return dict(tcp_nodelay=sock.getsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY),python_socket_proto=sock.proto,rcvbuf=sock.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF),sndbuf=sock.getsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF),tcp_info_hex=sock.getsockopt(socket.IPPROTO_TCP,socket.TCP_INFO,256).hex())

def window_config(config):
 if WINDOW is not None:config.max_data=WINDOW;config.max_stream_data=WINDOW
 return config


def certificate(out):
 key=ec.generate_private_key(ec.SECP256R1());name=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'localhost')]);now=datetime.datetime.now(datetime.timezone.utc)
 cert=(x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(now-datetime.timedelta(minutes=5)).not_valid_after(now+datetime.timedelta(days=2)).add_extension(x509.SubjectAlternativeName([x509.DNSName('localhost'),x509.IPAddress(ipaddress.ip_address('127.0.0.1'))]),critical=False).add_extension(x509.BasicConstraints(ca=True,path_length=None),critical=True).sign(key,hashes.SHA256()))
 (out/'certificate.pem').write_bytes(cert.public_bytes(serialization.Encoding.PEM));(out/'fixture-private-key.pem').write_bytes(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
 return cert.fingerprint(hashes.SHA256()).hex()

class H3(QuicConnectionProtocol):
 def __init__(self,*args,server=False,log=None,**kwargs):
  super().__init__(*args,**kwargs);self.http=H3Connection(self._quic);self.server=server;self.states={};self.handshake=None;self.log=log
 def quic_event_received(self,event):
  if isinstance(event,HandshakeCompleted):self.handshake=dict(at=NOW(),alpn=event.alpn_protocol,session_resumed=event.session_resumed,early_data_accepted=event.early_data_accepted)
  if isinstance(event,ConnectionTerminated):
   for state in self.states.values():
    if 'future' in state and not state['future'].done():state['future'].set_exception(RuntimeError(str(event)))
  for e in self.http.handle_event(event):
   if not isinstance(e,(HeadersReceived,DataReceived)):continue
   state=self.states.setdefault(e.stream_id,dict(body=bytearray(),headers=None,first_headers=None,first_data=None))
   if isinstance(e,HeadersReceived):state['headers']=[(k.decode(),v.decode()) for k,v in e.headers];state['first_headers']=NOW()
   else:
    if e.data and state['first_data'] is None:state['first_data']=NOW()
    state['body'].extend(e.data)
   if not e.stream_ended:continue
   if self.server:
    data=bytes(state['body']);record=dict(stream=e.stream_id,at=NOW(),bytes=len(data),sha256=hashlib.sha256(data).hexdigest());self.log.append(record)
    asyncio.create_task(self.reply(e.stream_id,record));del self.states[e.stream_id]
   else:
    state['end']=NOW()
    if not state['future'].done():state['future'].set_result(state)
 async def reply(self,stream,record):
  record['service_start']=NOW();await asyncio.sleep(SERVICE_S);record['service_end']=NOW()
  self.http.send_headers(stream,[(b':status',b'200'),(b'content-length',str(len(RESPONSE)).encode()),(b'content-type',b'text/plain; charset=utf-8')]);self.http.send_data(stream,RESPONSE,end_stream=True);self.transmit()
 async def request(self):
  stream=self._quic.get_next_available_stream_id();future=asyncio.get_running_loop().create_future();self.states[stream]=dict(future=future,body=bytearray(),headers=None,first_headers=None,first_data=None)
  send=NOW();self.http.send_headers(stream,[(b':method',b'POST'),(b':scheme',b'https'),(b':authority',b'localhost'),(b':path',b'/echo'),(b'content-length',str(len(PAYLOAD)).encode())]);self.http.send_data(stream,PAYLOAD,end_stream=True);self.transmit()
  result=await asyncio.wait_for(future,REQUEST_TIMEOUT);result=dict(result);del result['future'];del self.states[stream];return send,stream,result

async def h1_event(conn,reader):
 while True:
  event=conn.next_event()
  if event is h11.NEED_DATA:
   data=await reader.read(65536);conn.receive_data(data)
  else:return event

async def main(out,smoke):
 out.mkdir(exist_ok=False);fingerprint=certificate(out)
 server_rows=[];server_errors=[];h1_writers=set();h3_server_rows=[];socket_samples=[]
 async def sample_sockets():
  while True:
   for w in list(h1_writers):
    if not w.is_closing():socket_samples.append(dict(time_s=NOW(),side="server",local=w.get_extra_info("sockname"),peer=w.get_extra_info("peername"),**socket_record(w.get_extra_info("socket"))))
   await asyncio.sleep(.1)
 sampler=asyncio.create_task(sample_sockets())
 sc=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);sc.minimum_version=sc.maximum_version=ssl.TLSVersion.TLSv1_3;sc.set_alpn_protocols(['http/1.1']);sc.load_cert_chain(out/'certificate.pem',out/'fixture-private-key.pem')
 cc=ssl.create_default_context(cafile=str(out/'certificate.pem'));cc.minimum_version=cc.maximum_version=ssl.TLSVersion.TLSv1_3;cc.set_alpn_protocols(['http/1.1'])
 async def h1_server(reader,writer):
  h1_writers.add(writer);conn=h11.Connection(h11.SERVER)
  try:
   while True:
    body=bytearray();headers=None
    while True:
     event=await h1_event(conn,reader)
     if isinstance(event,h11.ConnectionClosed):return
     if isinstance(event,h11.Request):headers=[(k.decode(),v.decode()) for k,v in event.headers]
     elif isinstance(event,h11.Data):body.extend(event.data)
     elif isinstance(event,h11.EndOfMessage):break
    record=dict(at=NOW(),bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),headers=headers,peer=writer.get_extra_info('peername'),socket_after_upload=socket_record(writer.get_extra_info('socket')));server_rows.append(record)
    record['service_start']=NOW();await asyncio.sleep(SERVICE_S);record['service_end']=NOW()
    for event in [h11.Response(status_code=200,headers=[(b'content-length',str(len(RESPONSE)).encode()),(b'content-type',b'text/plain; charset=utf-8')]),h11.Data(data=RESPONSE),h11.EndOfMessage()]:writer.write(conn.send(event))
    await writer.drain();conn.start_next_cycle()
  except Exception as e:server_errors.append(repr(e))
  finally:writer.close();await writer.wait_closed();h1_writers.discard(writer)
 listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP);listener.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1);listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
 if WINDOW is not None:listener.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,WINDOW)
 listener.bind(('127.0.0.1',0));listener.listen();listener.setblocking(False);listener_settings=socket_record(listener)
 tcp=await asyncio.start_server(h1_server,sock=listener,ssl=sc);tcp_port=tcp.sockets[0].getsockname()[1]
 qc=window_config(QuicConfiguration(is_client=False,alpn_protocols=H3_ALPN));qc.load_cert_chain(out/'certificate.pem',out/'fixture-private-key.pem')
 udp=await serve('127.0.0.1',0,configuration=qc,create_protocol=lambda *a,**k:H3(*a,server=True,log=h3_server_rows,**k));udp_port=udp._transport.get_extra_info('sockname')[1]
 env=dict(python=platform.python_version(),platform=platform.platform(),machine=platform.machine(),openssl=ssl.OPENSSL_VERSION,packages={p:importlib.metadata.version(p) for p in ['aioquic','h11','cryptography','pylsqpack']},certificate_sha256=fingerprint,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),mode=MODE,requested_window=WINDOW,listener_settings=listener_settings,quic_max_data=qc.max_data,quic_max_stream_data=qc.max_stream_data,tcp_port=tcp_port,udp_port=udp_port,payload_bytes=len(PAYLOAD),payload_sha256=HASH,response_bytes=len(RESPONSE),response_sha256=RESPONSE_HASH,service_time_replay_s=SERVICE_S,fixture=FIXTURE,smoke=smoke,server_and_client_same_event_loop=True,body_request_deadline_s=REQUEST_TIMEOUT)
 (out/'environment.json').write_text(json.dumps(env,indent=2));connections=[];rows=[];groups=[];next_id=0
 async def open_conn(proto):
  nonlocal next_id
  ident=next_id;next_id+=1;begin=NOW()
  if proto=='h1':
   sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM,socket.IPPROTO_TCP);sock.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1);sock.setblocking(False)
   if WINDOW is not None:sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,WINDOW)
   await asyncio.wait_for(asyncio.get_running_loop().sock_connect(sock,('127.0.0.1',tcp_port)),20)
   reader,writer=await asyncio.wait_for(asyncio.open_connection(sock=sock,ssl=cc,server_hostname='localhost'),20);obj=writer.get_extra_info('ssl_object');ready=NOW()
   record=dict(id=ident,protocol=proto,start=begin,ready=ready,alpn=obj.selected_alpn_protocol(),tls=obj.version(),cipher=obj.cipher(),session_resumed=obj.session_reused,certificate_sha256=hashlib.sha256(obj.getpeercert(binary_form=True)).hexdigest(),local=writer.get_extra_info('sockname'),socket_ready=socket_record(writer.get_extra_info('socket')))
   conn=dict(record=record,reader=reader,writer=writer,h11=h11.Connection(h11.CLIENT))
  else:
   qlog=QuicLogger();config=window_config(QuicConfiguration(is_client=True,alpn_protocols=H3_ALPN,server_name='localhost',verify_mode=ssl.CERT_REQUIRED,cafile=str(out/'certificate.pem'),quic_logger=qlog))
   ctx=connect('127.0.0.1',udp_port,configuration=config,create_protocol=H3,wait_connected=True);protocol=await asyncio.wait_for(ctx.__aenter__(),20);ready=NOW();record=dict(id=ident,protocol=proto,start=begin,ready=ready,**protocol.handshake,local=protocol._transport.get_extra_info('sockname'))
   conn=dict(record=record,ctx=ctx,protocol=protocol,qlog=qlog)
  connections.append(record);return conn
 async def close_conn(conn):
  if conn['record']['protocol']=='h1':
   conn['record']['socket_close']=socket_record(conn['writer'].get_extra_info('socket'));conn['writer'].close();await conn['writer'].wait_closed()
  else:
   await conn['ctx'].__aexit__(None,None,None)
   with gzip.open(out/f"qlog-{conn['record']['id']}.json.gz",'wt') as f:json.dump(conn['qlog'].to_dict(),f)
  conn['record']['closed']=NOW()
 async def request(conn):
  if conn['record']['protocol']=='h3':return await conn['protocol'].request()
  c=conn['h11'];send=NOW()
  for e in [h11.Request(method='POST',target='/echo',headers=[('Host','localhost'),('Content-Length',str(len(PAYLOAD)))]),h11.Data(data=PAYLOAD),h11.EndOfMessage()]:conn['writer'].write(c.send(e))
  await conn['writer'].drain();state=dict(body=bytearray(),first_headers=None,first_data=None,headers=None)
  while True:
   e=await asyncio.wait_for(h1_event(c,conn['reader']),REQUEST_TIMEOUT)
   if isinstance(e,h11.Response):state['first_headers']=NOW();state['headers']=[(':status',str(e.status_code))]+[(k.decode(),v.decode()) for k,v in e.headers]
   elif isinstance(e,h11.Data):
    if state['first_data'] is None:state['first_data']=NOW()
    state['body'].extend(e.data)
   elif isinstance(e,h11.EndOfMessage):state['end']=NOW();c.start_next_cycle();return send,None,state
   elif isinstance(e,h11.ConnectionClosed):raise RuntimeError('premature close')
 async def group(trial,proto,reuse,concurrency,count,warmup=False):
  begin=NOW();opened=[];gr=[]
  async def lane(lane_id):
   conn=None
   for index in range(lane_id,count,concurrency):
    rec=dict(trial=trial,protocol=proto,reuse=reuse,concurrency=concurrency,index=index,lane=lane_id,warmup=warmup,start=NOW())
    try:
     fresh=conn is None or not reuse
     if fresh:conn=await open_conn(proto);opened.append(conn)
     send,stream,result=await asyncio.wait_for(request(conn),REQUEST_TIMEOUT);data=bytes(result.pop('body'));decode_start=NOW()
     decoded=data.decode('utf-8');decode_end=NOW();rec.update(decoded_text=decoded,decode_start=decode_start,decode_end=decode_end,connection=conn['record']['id'],fresh=fresh,connection_ready=conn['record']['ready'] if fresh else rec['start'],send=send,stream=stream,**result,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),valid=(data==RESPONSE and decoded==RESPONSE.decode('utf-8') and dict(result['headers']).get(':status')=='200'),validation_end=NOW(),error=None)
    except Exception as e:
     rec.update(error=repr(e),valid=False,validation_end=NOW())
     if conn is not None:
      await close_conn(conn);opened.remove(conn);conn=None;rec['failed_connection_closed']=True
    gr.append(rec);rows.append(rec)
    with (out/'requests.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
  await asyncio.gather(*(lane(i) for i in range(concurrency)));complete=NOW()
  await asyncio.gather(*(close_conn(c) for c in opened));groups.append(dict(trial=trial,protocol=proto,reuse=reuse,concurrency=concurrency,warmup=warmup,start=begin,requests_complete=complete,cleanup_complete=NOW(),requests=len(gr),errors=sum(not r['valid'] for r in gr)))
 try:
  for proto in ['h1','h3']:await group(-1,proto,False,1,1,True)
  order=[dict(trial=0,protocol=p,reuse=True,concurrency=1) for p in ['h1','h3']]
  random.Random(120405+int(os.environ['BOOK_WINDOW_TRIAL'])).shuffle(order)
  (out/'order.json').write_text(json.dumps(order,indent=2))
  for c in order:await group(c['trial'],c['protocol'],c['reuse'],c['concurrency'],2)
 finally:
  sampler.cancel()
  try:await sampler
  except asyncio.CancelledError:pass
  (out/"socket-samples.json").write_text(json.dumps(socket_samples))
  tcp.close();await tcp.wait_closed();udp.close()
  for writer in list(h1_writers):writer.close()
  await asyncio.sleep(.05)
  for name,data in [('connections',connections),('groups',groups),('h1-server',server_rows),('h3-server',h3_server_rows),('server-errors',server_errors)]: (out/(name+'.json')).write_text(json.dumps(data,indent=2))
  (out/'completion.json').write_text(json.dumps(dict(done=True,requests=len(rows),failures=sum(not r['valid'] for r in rows),listeners_closed=True)))
 print(json.dumps(dict(requests=len(rows),failures=sum(not r['valid'] for r in rows),server_errors=server_errors)))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--smoke',action='store_true');args=p.parse_args();asyncio.run(main(args.output,args.smoke))
