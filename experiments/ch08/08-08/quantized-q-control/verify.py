import hashlib,json,subprocess,sys
from pathlib import Path
r=Path(__file__).absolute().parent;m=json.loads((r/'manifest.json').read_text())
for name,digest in m.items():assert hashlib.sha256((r/name).read_bytes()).hexdigest()==digest,name
s=json.loads((r/'runs/fp8_qbf16/supervisor.json').read_text());assert s['exit_code']==0 and s['reason'] is None and s['leftovers']=={}
subprocess.run([sys.executable,str(r/'analyze.py')],check=True)
print('PASS:',len(m),'files; reference identity, actual Q dtype, weights and scales matched')
