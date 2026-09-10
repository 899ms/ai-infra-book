"""Run both KV conditions on Linux with the installed vLLM interpreter."""
import argparse, subprocess, sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--model',required=True);a=p.parse_args()
r=Path(__file__).absolute().parent
for name,dtype in [('bf16','auto'),('fp8','fp8_e4m3')]:
 subprocess.run([sys.executable,str(r/'resource_guard.py'),'--out',str(r/'runs'/name),'--',sys.executable,str(r/'run.py'),'--model',a.model,'--output',str(r/'results'/name),'--kv-dtype',dtype],cwd=r,check=True)
subprocess.run([sys.executable,str(r/'analyze.py')],cwd=r,check=True)
