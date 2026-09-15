import hashlib,json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parent
assert not (R/'container-after.txt').read_text().strip()
counts={};sources={}
for w,n in [('asr',54),('computer',162),('image',54)]:
 subprocess.run([sys.executable,str(R/f'analyze_{w}.py')],check=True,stdout=(R/f'{w}-analysis.log').open('w'))
 s=json.loads((R/f'{w}-summary.json').read_text());assert s['requests']==s['valid']==n
 counts[w]=dict(requests=n,formal=s['formal_requests'])
 for p in [R/f'{w}.py',R/f'analyze_{w}.py']:sources[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
assert sum(c['requests'] for c in counts.values())==270 and sum(c['formal'] for c in counts.values())==216
(R/'verification.json').write_text(json.dumps(dict(verified=True,counts=counts,total_requests=270,total_formal=216,all_subrun_removals_verified=True,final_container_absence_verified=True,source_sha256=sources),indent=2)+'\n')
print('All270 exchanges, application chunk ledgers, explicit TCP_NODELAY1, source results, transport and cleanup verified')
