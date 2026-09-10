import hashlib,json
from pathlib import Path
r=Path(__file__).absolute().parent;m=json.loads((r/'manifest.json').read_text())
for n,h in m.items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h,n
s=json.loads((r/'run/supervisor.json').read_text());assert s['exit_code']==0 and s['reason'] is None and s['leftovers']=={}
a=json.loads((r/'analysis.json').read_text());assert len(a)==4
for x in a:
 assert x['relative_l2']<=.02 and len(x['peaks'])==4 and len(set(x['peaks'][1:]))==1
 assert all(v>=x['resident_bytes'] for v in x['absolute_peak_increments'])
for n,h in json.loads((r/'provenance.json').read_text()).items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h
print('PASS:',len(m),'files; four independent conditions, sixteen measured calls and snapshots')
