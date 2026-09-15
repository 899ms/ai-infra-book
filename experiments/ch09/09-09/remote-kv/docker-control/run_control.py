"""Reproduce the executed Docker control orchestration in a fresh directory."""
import subprocess,os,json,time,urllib.request
from pathlib import Path
from store import pack,unpack
r=Path(__file__).resolve().parent;os.chdir(r);records=[];name='book909-remote-control-001';cid=None
assert not (r/'docker-execution.json').exists()
def cmd(a):
 p=subprocess.run(a,capture_output=True,text=True);records.append(dict(command=a,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,time=time.time()));assert p.returncode==0,records[-1];return p.stdout.strip()
try:
 image=cmd(['docker','image','inspect','python:3.11-slim','--format','{{.Id}}'])
 cid=cmd(['docker','create','--name',name,'--label','book.experiment=909-remote-control-001','--user',f'{os.getuid()}:{os.getgid()}','--network','host','--cpus','1','--memory','512m','--memory-swap','512m','--read-only','--tmpfs','/tmp','--mount',f'type=bind,source={r},target=/experiment',image,'python','-u','/experiment/store.py','--root','/experiment/docker-store','--port','18799'])
 cmd(['docker','start',cid]);deadline=time.monotonic()+20
 while True:
  try:
   q=urllib.request.Request('http://127.0.0.1:18799/inventory',data=pack({}))
   with urllib.request.urlopen(q,timeout=3) as f:assert unpack(f.read())[0]=={'files':[]}
   break
  except Exception:
   if time.monotonic()>deadline:raise
   time.sleep(.1)
 with (r/'launch.log').open('x') as f:code=subprocess.call(['/home/ubuntu/ai-infra-book-experiments/tools/sglang0513-venv/bin/python','-u','launch.py'],stdout=f,stderr=subprocess.STDOUT)
 records.append(dict(launch_exit_code=code,time=time.time()));assert code==0
 with (r/'analysis.log').open('x') as f:subprocess.run(['python3','analyze.py'],stdout=f,stderr=subprocess.STDOUT,check=True)
finally:
 if cid:
  (r/'docker-store.log').write_text(cmd(['docker','logs',cid]))
  (r/'docker-inspect.json').write_text(cmd(['docker','inspect',cid])+'\n')
  cmd(['docker','rm','-f',cid])
 (r/'docker-execution.json').write_text(json.dumps(records,indent=2)+'\n')
