import subprocess,sys
from pathlib import Path
r=Path(__file__).absolute().parent
subprocess.run([sys.executable,str(r/'resource_guard.py'),'--out',str(r/'run'),'--',sys.executable,str(r/'run.py'),'--out',str(r/'results')],cwd=r,check=True)
subprocess.run([sys.executable,str(r/'analyze.py')],check=True)
subprocess.run([sys.executable,str(r/'audit.py')],check=True)
