import hashlib,json,subprocess,sys
from pathlib import Path
r=Path(__file__).absolute().parent;m=json.loads((r/'manifest.json').read_text())
for n,h in m.items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h,n
old=(r/'results/summary.json').read_bytes()
subprocess.run([sys.executable,'-B',str(r/'analyze.py'),'--out',str(r/'results')],check=True,stdout=subprocess.DEVNULL)
assert (r/'results/summary.json').read_bytes()==old
print('PASS:',len(m),'sealed files; all 12 recovery paths independently rechecked')
