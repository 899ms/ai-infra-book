import subprocess,json,time,os,signal,hashlib
from pathlib import Path
os.environ['PATH']='/home/ubuntu/ai-infra-book-experiments/tools/criu-4.2.1/criu:/home/ubuntu/ai-infra-book-experiments/tools/docker-24.0.9/docker:'+os.environ['PATH']
P=Path(__file__).resolve().parent;assert not (P/'daemon.log').exists()
config={'experimental':True,'debug':True,'data-root':str(P/'data'),'exec-root':'/run/book1102-c421v2','pidfile':str(P/'daemon.pid'),'hosts':['unix://'+'/run/book1102-c421v2.sock'],'bridge':'none','iptables':False,'ip6tables':False,'ip-forward':False,'ip-masq':False,'containerd-namespace':'book1102','containerd-plugins-namespace':'plugins.book1102'}
config['containerd']='/run/book1102-c421v2-ctd.sock'
ctlog=(P/'containerd.log').open('w')
ct=subprocess.Popen(['containerd','--root',str(P/'containerd-root'),'--state','/run/book1102-c421v2-ctd','--address',config['containerd']],stdout=ctlog,stderr=subprocess.STDOUT)
for _ in range(100):
 if Path(config['containerd']).exists():break
 if ct.poll() is not None:raise RuntimeError('containerd exited')
 time.sleep(.1)
else:ct.terminate();ct.wait();raise RuntimeError('containerd timeout')
(P/'daemon.json').write_text(json.dumps(config,indent=2)+'\n')
log=(P/'daemon.log').open('w');proc=subprocess.Popen(['dockerd','--config-file',str(P/'daemon.json')],stdout=log,stderr=subprocess.STDOUT)
commands=[]
def cmd(a,timeout=120):
 p=subprocess.run(a,capture_output=True,text=True,timeout=timeout);r=dict(args=a,rc=p.returncode,stdout=p.stdout,stderr=p.stderr);commands.append(r);(P/'commands.json').write_text(json.dumps(commands,indent=2)+'\n');return r
host='unix://'+'/run/book1102-c421v2.sock'
try:
 for _ in range(100):
  if proc.poll() is not None:raise RuntimeError('daemon exited')
  if Path('/run/book1102-c421v2.sock').exists() and cmd(['docker','-H',host,'info','--format','{{.DockerRootDir}}'])['rc']==0:break
  time.sleep(.2)
 else:raise RuntimeError('daemon readiness timeout')
 assert cmd(['/usr/bin/docker','image','save','-o',str(P/'base.tar'),'python:3.11-slim'])['rc']==0
 assert cmd(['docker','-H',host,'image','load','-i',str(P/'base.tar')])['rc']==0
 (P/'base.tar').unlink()
 r=cmd(['python3',str(P/'probe.py')]);(P/'probe-output.json').write_text(json.dumps(r,indent=2)+'\n')
finally:
 proc.terminate()
 try:proc.wait(timeout=30)
 except subprocess.TimeoutExpired:proc.kill();proc.wait()
 log.close();(P/'cleanup.json').write_text(json.dumps(dict(daemon_pid=proc.pid,daemon_exit_code=proc.returncode),indent=2)+'\n')

ct.terminate();ct.wait(timeout=30);ctlog.close()
(P/'containerd-cleanup.json').write_text(json.dumps(dict(pid=ct.pid,exit_code=ct.returncode))+'\n')
