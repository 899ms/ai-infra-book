import asyncio,hashlib,importlib.util,inspect,json,socket,ssl,sys
from pathlib import Path
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('transport',R.parent/'image-records/run_network120.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
def info(s):return dict(family=int(s.family),type=int(s.type),proto=s.proto,nodelay=s.getsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY),rcvbuf=s.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF))
async def main():
 O=R/'results';O.mkdir(exist_ok=False);b.certificate(O);rows=[]
 sc=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);sc.minimum_version=sc.maximum_version=ssl.TLSVersion.TLSv1_3;sc.load_cert_chain(O/'certificate.pem',O/'fixture-private-key.pem')
 cc=ssl.create_default_context(cafile=str(O/'certificate.pem'));cc.minimum_version=cc.maximum_version=ssl.TLSVersion.TLSv1_3
 for mode in ['implicit','manual-proto0','manual-tcp6']:
  received=asyncio.get_running_loop().create_future()
  async def handler(reader,writer):
   v=info(writer.get_extra_info('socket'));body=await reader.readexactly(4);writer.write(body);await writer.drain();writer.close();await writer.wait_closed();received.set_result(v)
  if mode=='implicit':server=await asyncio.start_server(handler,'127.0.0.1',0,ssl=sc)
  else:
   listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0 if mode=='manual-proto0' else socket.IPPROTO_TCP);listener.bind(('127.0.0.1',0));listener.listen();listener.setblocking(False);server=await asyncio.start_server(handler,sock=listener,ssl=sc)
  port=server.sockets[0].getsockname()[1]
  if mode=='implicit':reader,writer=await asyncio.open_connection('127.0.0.1',port,ssl=cc,server_hostname='localhost')
  else:
   sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM,0 if mode=='manual-proto0' else socket.IPPROTO_TCP);sock.setblocking(False);await asyncio.get_running_loop().sock_connect(sock,('127.0.0.1',port));reader,writer=await asyncio.open_connection(sock=sock,ssl=cc,server_hostname='localhost')
  client=info(writer.get_extra_info('socket'));writer.write(b'test');await writer.drain();assert await reader.readexactly(4)==b'test';writer.close();await writer.wait_closed();accepted=await received;server.close();await server.wait_closed();rows.append(dict(mode=mode,client=client,server=accepted))
 for r in rows:assert r['client']['nodelay']==r['server']['nodelay']==(0 if r['mode']=='manual-proto0' else 1)
 out=dict(python=sys.version,asyncio_set_nodelay_source=inspect.getsource(asyncio.base_events._set_nodelay),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),rows=rows,scope='Fresh socket-creation-path diagnostic in same pinned Docker image; not retrospective reads of completed benchmark sockets')
 (O/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
asyncio.run(main())
