"""Check the original profiled hotspot for measured concurrent GPU work."""
import hashlib
import json
from pathlib import Path
R=Path(__file__).resolve().parent
ROOT=R.parents[2]
p=ROOT/'experiments/ch08/08-08/profiles/analysis.json'
evidence=json.loads((R/'trace-evidence.json').read_text())
assert hashlib.sha256(p.read_bytes()).hexdigest()==evidence['sha256']
config=next(c for c in json.loads(p.read_text())['configurations'] if c['name']=='bf16')
hot=evidence['kernels'];assert len(hot)==72
assert all(h in config['kernels'] for h in hot)
rows=[]
for i,h in enumerate(hot):
    kernels=[dict(index=j,name=k['name'],stream=k['stream'],overlap_ns=min(h['end_ns'],k['end_ns'])-max(h['start_ns'],k['start_ns']))
        for j,k in enumerate(config['kernels']) if k!=h and max(h['start_ns'],k['start_ns'])<min(h['end_ns'],k['end_ns'])]
    copies=[dict(index=j,overlap_ns=min(h['end_ns'],c['end'])-max(h['start_ns'],c['start']))
        for j,c in enumerate(config['copies']) if max(h['start_ns'],c['start'])<min(h['end_ns'],c['end'])]
    rows.append(dict(index=i,start_ns=h['start_ns'],end_ns=h['end_ns'],stream=h['stream'],overlapping_kernels=kernels,overlapping_copies=copies))
report=dict(source=str(p.relative_to(ROOT)),source_sha256=evidence['sha256'],hotspots=72,
    compared_kernels=len(config['kernels']),compared_copies=len(config['copies']),
    hotspots_with_overlap=sum(bool(r['overlapping_kernels'] or r['overlapping_copies']) for r in rows),rows=rows,
    interpretation='Conditional contention requirement applies to original paths with concurrent GPU work. This checks all captured kernels and copies, not uncaptured external processes or other serving schedules.')
(R/'results/original-hotspot-concurrency.json').write_text(json.dumps(report,indent=2)+'\n')
print({k:v for k,v in report.items() if k!='rows'})
