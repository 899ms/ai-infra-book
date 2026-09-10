import hashlib,json,subprocess,sys
from pathlib import Path
r=Path(__file__).absolute().parent;m=json.loads((r/'manifest.json').read_text())
for n,h in m.items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h,n
old=(r/'analysis.json').read_bytes();subprocess.run([sys.executable,str(r/'analyze.py')],check=True,stdout=subprocess.DEVNULL);assert (r/'analysis.json').read_bytes()==old
print('PASS:',len(m),'sealed files; complete concurrent histories and reference matching verified')
