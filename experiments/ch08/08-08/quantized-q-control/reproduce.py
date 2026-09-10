import argparse,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--model',required=True);a=p.parse_args();r=Path(__file__).absolute().parent
subprocess.run([sys.executable,str(r/'resource_guard.py'),'--out',str(r/'runs/fp8_qbf16'),'--',sys.executable,str(r/'run.py'),'--model',a.model,'--output',str(r/'results/fp8_qbf16'),'--kv-dtype','fp8_e4m3'],cwd=r,check=True)
subprocess.run([sys.executable,str(r/'analyze.py')],cwd=r,check=True)
