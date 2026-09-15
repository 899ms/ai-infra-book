"""Own-container restore diagnostics; never modifies daemon or unrelated containers."""
import subprocess,json,time,uuid,threading,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;O=P/'results';O.mkdir(exist_ok=False)
commands=[]
def cmd(args):
 t=time.monotonic();p=subprocess.run(args,text=True,capture_output=True,timeout=45)
 r=dict(args=args,start=t,end=time.monotonic(),rc=p.returncode,stdout=p.stdout,stderr=p.stderr)
 commands.append(r);(O/'commands.json').write_text(json.dumps(commands,indent=2)+'\n');return r
base=cmd(['docker','image','inspect','python:3.11-slim','--format','{{.Id}}'])['stdout'].strip();assert base.startswith('sha256:')
rows=[]
for mode in ['default','unconfined']:
 name='book1102-probe-'+uuid.uuid4().hex[:10];cid=None;logs={};stop=threading.Event()
 try:
  args=['docker','create','--name',name,'--label','book.experiment=restore-probe','--network','host','--memory','128m','--cpus','1']
  if mode=='unconfined':args+=['--security-opt','seccomp=unconfined','--security-opt','apparmor=unconfined']
  r=cmd(args+[base,'python','-u','-c','import time,uuid; print(uuid.uuid4().hex,flush=True); time.sleep(3600)']);assert r['rc']==0;cid=r['stdout'].strip()
  assert cmd(['docker','start',cid])['rc']==0
  before=cmd(['docker','logs',cid]);capture=cmd(['docker','checkpoint','create',cid,'probe'])
  def watch():
   roots=[Path('/run/docker/runtime-runc/moby')/cid,Path('/run/containerd/io.containerd.runtime.v2.task/moby')/cid,Path('/run/docker/containerd/daemon/io.containerd.runtime.v2.task/moby')/cid,Path('/var/lib/docker/containers')/cid]
   while not stop.is_set():
    for root in roots:
     for f in root.rglob('*.log'):
      try:logs[str(f)]=f.read_text(errors='replace')
      except OSError:pass
    time.sleep(.005)
  watcher=threading.Thread(target=watch);watcher.start()
  restore=cmd(['docker','start','--checkpoint','probe',cid]) if capture['rc']==0 else None
  stop.set();watcher.join()
  state=cmd(['docker','inspect','--format','{{json .State}}',cid])
  row=dict(mode=mode,cid=cid,before=before,capture=capture,restore=restore,state=state)
  (O/(mode+'-logs.json')).write_text(json.dumps(logs,indent=2)+'\n');rows.append(row)
 finally:
  stop.set()
  if cid:cmd(['docker','rm','-f',cid])
(O/'result.json').write_text(json.dumps(dict(rows=rows,base_image=base,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n')
print(json.dumps([dict(mode=r['mode'],capture_rc=r['capture']['rc'],restore_rc=r['restore']['rc'] if r['restore'] else None,restore_error=r['restore']['stderr'] if r['restore'] else None) for r in rows],indent=2))
