"""Reproduce the two-host authenticated UDP experiment in fresh local/remote dirs."""
import argparse,json,os,shlex,shutil,subprocess,time
from pathlib import Path
B=Path(__file__).absolute().parent
p=argparse.ArgumentParser();p.add_argument('--remote-root',required=True);a=p.parse_args()
remote=a.remote_root.rstrip('/');assert remote.startswith('/home/ubuntu/') and '..' not in Path(remote).parts
assert not (B/'runs').exists(),'Use a fresh experiment copy; original records are protected'
def ssh(args,**kw):return subprocess.run(['ssh','rtx-pro',shlex.join(args)],check=True,**kw)
ssh(['test','!','-e',remote])
subprocess.run(['python3',str(B/'probe/run.py')],check=True)
for name in ['result.json','peer.jsonl','default-route.txt','scoped-route.txt']:
 shutil.copyfile(B/'probe/runs'/name,B/'interface-reference'/name)
subprocess.run(['python3',str(B/'build.py')],check=True)
env=os.environ.copy();env['BOOK_WAN_PRIVATE']=str(B/'private')
with (B/'runs/setup.log').open('w') as f:subprocess.run([str(B/'runs/client.test'),'-test.run=^TestBookWANSetup$'],env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
ssh(['mkdir','-p',remote+'/runs/server'])
subprocess.run(['rsync','-a',str(B)+'/',f'rtx-pro:{remote}/'],check=True)
cmd=['env','BOOK_WAN_PRIVATE='+remote+'/private','BOOK_WAN_SERVER_OUT='+remote+'/runs/server','BOOK_AUDIO_WAV='+remote+'/fixture/audio.wav',remote+'/runs/server.test','-test.run=^TestBookWANServer$','-test.v','-test.timeout=13m']
log=(B/'runs/ssh-control.log').open('w');server=subprocess.Popen(['ssh','-o','ServerAliveInterval=15','-o','ServerAliveCountMax=3','rtx-pro',shlex.join(cmd)+' > '+shlex.quote(remote+'/runs/server.log')+' 2>&1'],stdout=log,stderr=subprocess.STDOUT)
ready=None
try:
 deadline=time.monotonic()+30
 while True:
  if server.poll() is not None:raise RuntimeError('Server stopped before ready; inspect server.log')
  r=subprocess.run(['ssh','rtx-pro',shlex.join(['cat',remote+'/runs/server/ready.json'])],capture_output=True)
  if r.returncode==0:
   ready=json.loads(r.stdout);break
  assert time.monotonic()<deadline,'Server readiness deadline; do not restart blindly'
  time.sleep(1)
 subprocess.run(['python3',str(B/'client.py')],check=True)
finally:
 ssh(['touch',remote+'/runs/server/STOP'])
 code=server.wait(timeout=30);log.close()
 deadline=time.monotonic()+10
 while ready is not None:
  state=subprocess.run(['ssh','rtx-pro',shlex.join(['test','!','-d','/proc/'+str(ready['pid'])])],capture_output=True)
  if state.returncode==0:break
  assert time.monotonic()<deadline,'Original peer still present; inspect it, do not restart'
  time.sleep(.5)
 subprocess.run(['rsync','-a',f'rtx-pro:{remote}/runs/server.log',str(B/'runs/server.log')],check=True)
 native_pass=(B/'runs/server.log').read_text().rstrip().endswith('PASS')
 (B/'runs/server-exit.json').write_text(json.dumps(dict(ssh_observation_exit_code=code,native_log_passed=native_pass,server_process_absent=True))+'\n')
 subprocess.run(['rsync','-a',f'rtx-pro:{remote}/runs/server/',str(B/'runs/server')+'/'],check=True)
 # Only our temporary authentication material and build artifacts.
 shutil.rmtree(B/'private')
 ssh(['rm','-rf',remote+'/private'])
 for name in ['client.test','server.test']:
  (B/'runs'/name).unlink();ssh(['rm','-f',remote+'/runs/'+name])
assert native_pass
