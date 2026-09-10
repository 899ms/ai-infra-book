import hashlib,json
from pathlib import Path
r=Path(__file__).absolute().parent
manifest=json.loads((r/'manifest.json').read_text())
for name,digest in manifest.items():assert hashlib.sha256((r/name).read_bytes()).hexdigest()==digest,name
assert set(manifest)=={str(p.relative_to(r)) for p in r.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='manifest.json'}
print(f'PASS: {len(manifest)} sealed files; CPU numerical recheck: python analyze.py --check')
