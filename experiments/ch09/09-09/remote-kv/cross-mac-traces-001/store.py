"""Experiment-owned, loopback-only remote KV page store with framed bulk I/O."""
import argparse,hashlib,json,os,re,struct,threading,time
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer

def pack(meta,blobs=()):
 h=json.dumps(meta).encode();return struct.pack('!I',len(h))+h+b''.join(blobs)
def unpack(data):
 n=struct.unpack('!I',data[:4])[0];return json.loads(data[4:4+n]),data[4+n:]
def main(a):
 a.root.mkdir(parents=True,exist_ok=False);lock=threading.Lock();ledger=a.root/'ledger.jsonl'
 def path(key):
  assert re.fullmatch(r'[A-Za-z0-9_.-]{1,400}',key) and key not in ['.','..'];return a.root/(key+'.bin')
 class Handler(BaseHTTPRequestHandler):
  def log_message(self,*args):pass
  def do_POST(self):
   start=time.monotonic();length=int(self.headers.get('Content-Length','0'));assert 0<length<512*1024**2
   data=self.rfile.read(length);meta,body=unpack(data);status=200;info={};blobs=[]
   try:
    with lock:
     if self.path=='/exists':info=dict(exists=[path(k).exists() for k in meta['keys']])
     elif self.path=='/get':
      entries=[]
      for k in meta['keys']:
       p=path(k);b=p.read_bytes() if p.exists() else b'';blobs.append(b);entries.append(dict(key=k,found=p.exists(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
      info=dict(entries=entries)
     elif self.path=='/set':
      offset=0;entries=[]
      for e in meta['entries']:
       n=e['bytes'];b=body[offset:offset+n];offset+=n;assert len(b)==n and hashlib.sha256(b).hexdigest()==e['sha256']
       p=path(e['key']);existed=p.exists()
       stored_sha=hashlib.sha256(p.read_bytes()).hexdigest() if existed else e['sha256']
       collision=existed and stored_sha!=e['sha256']
       if collision:
        c=a.root/'collisions';c.mkdir(exist_ok=True);(c/(e['key']+'-'+e['sha256'][:12]+'.bin')).write_bytes(b)
       if not existed:
        temp=p.with_suffix('.tmp');temp.write_bytes(b);temp.replace(p)
       entries.append(dict(key=e['key'],bytes=n,sha256=stored_sha,incoming_sha256=e['sha256'],collision=collision,new_write=not existed))
      assert offset==len(body);info=dict(entries=entries)
     elif self.path=='/inventory':info=dict(files=[dict(key=p.stem,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(a.root.glob('*.bin'))])
     else:raise ValueError('unknown endpoint')
     response=pack(info,blobs)
     with ledger.open('a') as f:f.write(json.dumps(dict(start_s=start,end_s=time.monotonic(),path=self.path,request_bytes=len(data),response_bytes=len(response),request=meta,response=info))+'\n')
   except Exception as e:status=400;response=pack(dict(error=repr(e)))
   self.send_response(status);self.send_header('Content-Length',str(len(response)));self.end_headers();self.wfile.write(response)
 server=ThreadingHTTPServer(('127.0.0.1',a.port),Handler);print('ready',a.port,flush=True);server.serve_forever()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--port',type=int,default=18798);main(p.parse_args())
