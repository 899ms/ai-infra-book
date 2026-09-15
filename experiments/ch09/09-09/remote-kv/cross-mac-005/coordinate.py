"""Keep the Mac page store alive until the bounded remote launcher exits."""
import json,socket,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parent
remote='/home/ubuntu/ai-infra-book-experiments/ch09/09-09/remote-kv/cross-mac-005'
state={};server=None;ssh=None
try:
 with (R/'store.log').open('x') as out:
  server=subprocess.Popen([sys.executable,'-u',str(R/'store.py'),'--root',str(R/'mac-store'),'--port','18796'],stdout=out,stderr=subprocess.STDOUT)
  for _ in range(100):
   assert server.poll() is None
   try:
    with socket.create_connection(('127.0.0.1',18796),timeout=1):break
   except OSError:time.sleep(.1)
  else:raise TimeoutError('store readiness')
  cmd=['ssh','-o','BatchMode=yes','-o','ExitOnForwardFailure=yes','-o','ControlMaster=no','-o','ControlPath=none','-o','Compression=no','-o','ServerAliveInterval=15','-o','ServerAliveCountMax=4','-R','127.0.0.1:18797:127.0.0.1:18796','rtx-pro',f'cd {remote} && python3 -u launch.py']
  state.update(command=cmd,start_unix=time.time())
  with (R/'ssh.log').open('x') as log:
   ssh=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT);state['ssh_exit']=ssh.wait()
  state['end_unix']=time.time()
finally:
 if server is not None:
  server.terminate();server.wait(timeout=15);state['store_exit']=server.returncode
 (R/'transport-execution.json').write_text(json.dumps(state,indent=2)+'\n')
 subprocess.run(['rsync','-a',f'rtx-pro:{remote}/results/',str(R/'results')+'/'],check=True)
print(json.dumps(state,indent=2))
assert state['ssh_exit']==0
