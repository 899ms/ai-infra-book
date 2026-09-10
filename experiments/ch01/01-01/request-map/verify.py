import hashlib,json,subprocess,sys
from pathlib import Path
r=Path(__file__).absolute().parent;m=json.loads((r/'manifest.json').read_text())
for n,h in m.items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h,n
old=(r/'result.json').read_bytes();subprocess.run([sys.executable,str(r/'run.py')],cwd=r,check=True);assert (r/'result.json').read_bytes()==old
print('PASS:',len(m),'sealed files and reproducible request evidence checks')
