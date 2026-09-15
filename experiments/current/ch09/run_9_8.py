"""Audit retained recovery evidence; no new GPU measurement is claimed."""
from pathlib import Path
import hashlib,json,subprocess,sys
P=Path(__file__).resolve().parent
ROOT=P.parents[2]
base=ROOT/'experiments/ch09/09-08'
checks=['verify_manifest.py','missing-pages/analyze.py','missing-pages/verify_manifest.py','truncated-request/verify.py','truncated-request/verify_manifest.py','storage-contract/verify.py','storage-contract/verify_manifest.py']
checked=[]
for name in checks:
 r=subprocess.run([sys.executable,str(base/name)],cwd=ROOT,text=True,capture_output=True,check=True)
 checked.append({'script':str((base/name).relative_to(ROOT)),'exit_code':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest()})
s=json.loads((base/'summary.json').read_text())
assert s['read_calls']==64 and s['read_file_bytes']==150994944
assert s['requests'][3]['details']['storage']==1008
m=json.loads((base/'missing-pages/summary.json').read_text())
assert [x['requests'][0]['cached_tokens'] for x in m['cases']]==[0,512]
assert all(x['omitted_file_restored'] for x in m['cases'])
files=[next((ROOT/'manuscripts').glob('09-*.md')),base/'summary.json',base/'missing-pages/summary.json',base/'truncated-request/README.md',base/'storage-contract/README.md']
out={'exercise':'9-8','read_tokens':1024,'reused_tokens':1008,'read_pages':64,'reused_pages':63,'bytes_per_token':147456,'file_read_bytes':150994944,'reused_state_bytes':148635648,'unused_read_bytes':2359296,'token_reuse_fraction':1008/1024,'missing_page_cases':m['cases'],'verification':checked,'scope':'Current explanatory exercise supported by retained GPU runs and CPU backend observations. No end-to-end version incompatibility experiment or physical disk byte claim. Historical full protocol remains incomplete.','source_sha256':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}}
assert out['file_read_bytes']-out['reused_state_bytes']==out['unused_read_bytes']
(P/'9-8-results.json').write_text(json.dumps(out,indent=2)+'\n')
print('Verified recovery evidence and token/page accounting for exercise 9-8')
