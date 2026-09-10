import hashlib,json,subprocess,sys
from pathlib import Path
r=Path(__file__).absolute().parent;m=json.loads((r/'manifest.json').read_text())
for n,h in m.items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h,n
s=json.loads((r/'run/supervisor.json').read_text());assert s['exit_code']==0 and s['reason'] is None and s['leftovers']=={}
subprocess.run([sys.executable,str(r/'analyze.py')],check=True)
print('PASS:',len(m),'files; controlled inputs, complete timing/trace records and fixed quality threshold')
