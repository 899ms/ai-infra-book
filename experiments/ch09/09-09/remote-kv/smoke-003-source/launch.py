"""Sequential fresh SGLang engines with own process-group cleanup."""
import json,os,signal,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'results-smoke-003'
O.mkdir(exist_ok=False)
E=Path('/home/ubuntu/ai-infra-book-experiments/tools/sglang0513-venv');cuda=E/'lib/python3.10/site-packages/nvidia/cu13'
env=os.environ.copy();env.update(CUDA_HOME=str(cuda),PATH=str(cuda/'bin')+':'+env['PATH'],LD_LIBRARY_PATH=str(cuda/'lib'),TVM_FFI_CACHE_DIR='/home/ubuntu/ai-infra-book-experiments/ch09/09-08/jit-cache-cu13-v2',OMP_NUM_THREADS='4')
def gpu():return subprocess.check_output(['nvidia-smi','--query-compute-apps=pid,used_memory','--format=csv,noheader'],text=True)
assert not gpu().strip();rows=[];active=None
try:
 for phase in ['producer','consumer']:
  cmd=[str(E/'bin/python'),'-u',str(R/'run.py'),'--phase',phase,'--output',str(O/phase)];start=time.monotonic()
  with (O/f'{phase}.log').open('x') as f,(O/f'{phase}-gpu.jsonl').open('x') as m:
   active=subprocess.Popen(cmd,env=env,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
   while active.poll() is None:
    m.write(json.dumps(dict(time=time.time(),apps=gpu()))+'\n');m.flush()
    if time.monotonic()-start>1200:raise TimeoutError(phase)
    time.sleep(1)
  rows.append(dict(phase=phase,command=cmd,exit_code=active.returncode,elapsed_s=time.monotonic()-start));assert active.returncode==0
  assert not gpu().strip();active=None
finally:
 if active is not None and active.poll() is None:
  os.killpg(active.pid,signal.SIGTERM)
  try:active.wait(timeout=15)
  except subprocess.TimeoutExpired:os.killpg(active.pid,signal.SIGKILL);active.wait(timeout=15)
 (O/'execution.json').write_text(json.dumps(dict(rows=rows,after_gpu=gpu()),indent=2)+'\n')
