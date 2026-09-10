import subprocess,sys,argparse
from pathlib import Path
r=Path(__file__).absolute().parent;p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
for phase in ['decode','prefill']:
 for mode in ['direct','dequant']:
  subprocess.run([sys.executable,str(r/'measure.py'),'--phase',phase,'--mode',mode,'--out',str(a.out/(phase+'-'+mode))],check=True)
