import subprocess,time,json,sys,shlex,hashlib,socket
from pathlib import Path
P=Path(__file__).resolve().parent;out=P/'http-result.json';assert not out.exists()
with socket.socket() as s:s.bind(('127.0.0.1',18796))
log=(P/'store.log').open('w');store=subprocess.Popen([sys.executable,str(P.parent/'store.py'),'--root',str(P/'http-store'),'--port','18796'],stdout=log,stderr=subprocess.STDOUT)
remote='''import urllib.request,struct,json,os,hashlib,time
url="http://127.0.0.1:18797/"
b=os.urandom(2359296);sha=hashlib.sha256(b).hexdigest();key="diagnostic-page"
def rpc(op,meta,body=b""):
 h=json.dumps(meta).encode();data=struct.pack("!I",len(h))+h+body;t=time.monotonic()
 with urllib.request.urlopen(urllib.request.Request(url+op,data=data),timeout=25) as r:answer=r.read()
 n=struct.unpack("!I",answer[:4])[0];return json.loads(answer[4:4+n]),answer[4+n:],time.monotonic()-t
m,_,put=rpc("set",dict(entries=[dict(key=key,bytes=len(b),sha256=sha)]),b)
m,got,get=rpc("get",dict(keys=[key]));assert got==b
print(json.dumps(dict(bytes=len(b),sha256=sha,set_s=put,get_s=get,valid=True)))
'''
try:
 for _ in range(50):
  if store.poll() is not None:raise RuntimeError('store exited')
  try:
   with socket.create_connection(('127.0.0.1',18796),timeout=.1):break
  except OSError:time.sleep(.1)
 args=['ssh','-o','BatchMode=yes','-o','ExitOnForwardFailure=yes','-o','ControlMaster=no','-o','ControlPath=none','-o','Compression=no','-R','127.0.0.1:18797:127.0.0.1:18796','rtx-pro','python3 -c '+shlex.quote(remote)]
 start=time.monotonic();r=subprocess.run(args,text=True,capture_output=True,timeout=60)
 result=dict(rc=r.returncode,stdout=r.stdout,stderr=r.stderr,total_s=time.monotonic()-start,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest());out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
finally:
 store.terminate();store.wait(timeout=5);log.close();(P/'http-cleanup.json').write_text(json.dumps(dict(store_pid=store.pid,exit_code=store.returncode))+'\n')
