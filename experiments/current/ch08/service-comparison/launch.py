"""Bounded subprocess with device samples and terminal status; preserves each run."""
from pathlib import Path
import subprocess,time,json,sys,os,signal
p=Path(__file__).resolve().parent;variant=sys.argv[1];tag=sys.argv[2];d=p/'runs'/tag;d.mkdir(parents=True,exist_ok=False)
cmd=[sys.executable,'-u',str(p/'run.py'),'--variant',variant,'--model','/home/ubuntu/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218','--out',str(d/'results')]
(d/'launch.json').write_text(json.dumps(dict(command=cmd,start_wall=time.time()),indent=2))
with (d/'run.log').open('w') as log,(d/'gpu.jsonl').open('w',buffering=1) as gpu:
 proc=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,start_new_session=True);start=time.monotonic();reason=None
 (d/'pid.json').write_text(json.dumps(dict(supervisor=os.getpid(),child=proc.pid)))
 while proc.poll() is None:
  r=subprocess.run(['nvidia-smi','--query-gpu=memory.used,utilization.gpu','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=10)
  gpu.write(json.dumps(dict(monotonic_s=time.monotonic(),values=r.stdout.strip(),returncode=r.returncode))+'\n')
  if time.monotonic()-start>600:
   reason='600s limit';os.killpg(proc.pid,signal.SIGTERM)
   try:proc.wait(timeout=15)
   except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL)
   break
  time.sleep(.25)
 code=proc.wait()
(d/'exit.json').write_text(json.dumps(dict(exit_code=code,reason=reason,elapsed_s=time.monotonic()-start),indent=2)+'\n')
