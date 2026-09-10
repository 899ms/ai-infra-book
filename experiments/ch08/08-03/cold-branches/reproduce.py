import argparse,subprocess,sys
from pathlib import Path
r=Path(__file__).absolute().parent;p=argparse.ArgumentParser();p.add_argument('--model',required=True);a=p.parse_args()
subprocess.run([sys.executable,str(r/'resource_guard.py'),'--out',str(r/'run'),'--',sys.executable,str(r/'run.py'),'--model',a.model,'--out',str(r/'results')],cwd=r,check=True)
subprocess.run([sys.executable,str(r/'analyze.py')],cwd=r,check=True)
