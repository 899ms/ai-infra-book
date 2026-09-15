import json,os,signal,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parent
E='/home/ubuntu/vllm023-venv/bin/python'
def gpu():return subprocess.check_output(['nvidia-smi','--query-compute-apps=pid,used_memory','--format=csv,noheader'],text=True)
assert not gpu().strip();p=None;state=dict(start_unix=time.time())
try:
 with (R/'model.log').open('x') as f,(R/'gpu.jsonl').open('x') as g:
  p=subprocess.Popen([E,'-u',str(R/'run.py')],stdout=f,stderr=subprocess.STDOUT,start_new_session=True,env={**os.environ,'OMP_NUM_THREADS':'4'});state['pid']=p.pid
  deadline=time.monotonic()+1800
  while p.poll() is None:
   g.write(json.dumps(dict(time=time.time(),apps=gpu()))+'\n');g.flush()
   if time.monotonic()>deadline:raise TimeoutError('training')
   time.sleep(1)
  state['exit_code']=p.returncode
finally:
 if p is not None and p.poll() is None:
  os.killpg(p.pid,signal.SIGTERM)
  try:p.wait(timeout=15)
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=15)
 state.update(end_unix=time.time(),after_gpu=gpu());(R/'execution.json').write_text(json.dumps(state,indent=2)+'\n')
assert state.get('exit_code')==0 and not state['after_gpu'].strip()
