import hashlib,json,subprocess,sys
from pathlib import Path
r=Path(__file__).absolute().parent;m=json.loads((r/'manifest.json').read_text())
for n,h in m.items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h,n
for name in ['run','run-regression']:
 s=json.loads((r/name/'supervisor.json').read_text());assert s['exit_code']==0 and s['reason'] is None and s['leftovers']=={}
for script in ['analyze.py','analyze_regression.py']:subprocess.run([sys.executable,str(r/script)],check=True)
print('PASS:',len(m),'files; actual attempts, known-answer checks, bounded retries and complete task costs')
