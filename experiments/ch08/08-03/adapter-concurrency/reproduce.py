import argparse,subprocess,sys
from pathlib import Path
r=Path(__file__).absolute().parent;p=argparse.ArgumentParser();p.add_argument('--model',required=True);a=p.parse_args()
for slots in [1,2]:
 subprocess.run([sys.executable,str(r/'resource_guard.py'),'--out',str(r/f'slots{slots}-run'),'--',sys.executable,str(r/'run.py'),'--slots',str(slots),'--model',a.model,'--out',str(r/f'slots{slots}')],cwd=r,check=True)
