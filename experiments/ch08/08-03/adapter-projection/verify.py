import hashlib,json,subprocess,sys
from pathlib import Path
r=Path(__file__).absolute().parent;m=json.loads((r/'manifest.json').read_text())
for n,h in m.items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h,n
subprocess.run([sys.executable,str(r/'analyze.py'),'--check'],check=True)
print('PASS:',len(m),'sealed files; actual QKV tensors and independent CPU reconstruction checked')
