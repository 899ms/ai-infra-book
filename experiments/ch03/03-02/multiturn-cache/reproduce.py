import argparse,subprocess,sys
from pathlib import Path
r=Path(__file__).absolute().parent;p=argparse.ArgumentParser();p.add_argument('--model',required=True);a=p.parse_args()
for mode in ['off','on']:
 cmd=[sys.executable,str(r/'resource_guard.py'),'--out',str(r/(mode+'-run')),'--',sys.executable,str(r/'run.py'),'--model',a.model,'--out',str(r/mode)]
 if mode=='on':cmd.append('--apc')
 subprocess.run(cmd,cwd=r,check=True)

subprocess.run([sys.executable,str(r/'resource_guard.py'),'--out',str(r/'grouped-run'),'--',sys.executable,str(r/'run_grouped.py'),'--apc','--model',a.model,'--out',str(r/'grouped')],cwd=r,check=True)
