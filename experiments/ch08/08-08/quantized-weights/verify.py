"""Verify sealed evidence and rerun independent record checks."""
import hashlib,json,subprocess,sys
from pathlib import Path
r=Path(__file__).absolute().parent
manifest=json.loads((r/'manifest.json').read_text())
for name,digest in manifest.items():
 assert hashlib.sha256((r/name).read_bytes()).hexdigest()==digest,name
for name in ['bf16','fp8']:
 s=json.loads((r/'runs'/name/'supervisor.json').read_text())
 assert s['exit_code']==0 and s['reason'] is None and s['leftovers']=={},s
subprocess.run([sys.executable,str(r/'analyze.py')],check=True)
print('PASS:',len(manifest),'files; both completed runs; matched quantized weights and inputs')
