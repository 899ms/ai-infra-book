import argparse,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--model',required=True);a=p.parse_args();r=Path(__file__).absolute().parent
for script,output,guard,analyzer in [('run.py','results','run','analyze.py'),('run_regression.py','results-regression','run-regression','analyze_regression.py')]:
 subprocess.run([sys.executable,str(r/'resource_guard.py'),'--out',str(r/guard),'--',sys.executable,str(r/script),'--model',a.model,'--output',str(r/output)],cwd=r,check=True)
 subprocess.run([sys.executable,str(r/analyzer)],cwd=r,check=True)
