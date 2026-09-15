"""Verify saved write observation and substitute its cost in the book design."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[3];r=json.loads((P/'formal-001/result.json').read_text());clean=json.loads((P/'formal-001/cleanup.json').read_text())
assert r['status']=='completed' and r['bytes']==14*8190735360
assert r['source_sha256']==hashlib.sha256((P/'run.py').read_bytes()).hexdigest()
assert abs(r['write_s']+r['fsync_s']-r['total_write_fsync_s'])<1e-9
assert abs(r['bytes']/r['total_write_fsync_s']/1e9-r['effective_GBps'])<1e-12
assert len(r['sample_checks'])==6 and all(x['bytes']==65536 and len(x['sha256'])==64 for x in r['sample_checks'])
assert clean['generated_payload_removed'] and not (P/'formal-001/payload.bin').exists()
design=json.loads((ROOT/'manuscripts/ch10/design-case.json').read_text());a=design['assumptions'];rows=[]
for d in design['candidates']:
 n=d['devices'];old=d['total_loss'];new=r['total_write_fsync_s']/1800+n/a['device_mtbf_seconds']*(900+120)
 step=float(F(d['base_step_exact']));days=5+design['updates']*step*(1+new)/86400
 eta=float(F(d['local_seconds_exact']))*.4/(25*86400/design['updates']/(1+new)-float(F(d['overhead_seconds_exact'])))
 rows.append(dict(cards=n,old_save_s=design['checkpoint_seconds'],measured_save_payload_s=r['total_write_fsync_s'],new_extra_fraction=new,finish_days=days,meets30days=days<=30,GPU_hours_if_allocated_throughout=n*days*24,required_compute_efficiency_for30days=eta))
out=dict(status='observed_write_verified',cases=rows,scope='Single local full-size synthetic payload write+fsync substitutes save cost only. Excludes serialization, model staging, commit metadata and distributed coordination; not a full checkpoint latency or replicated workload benchmark.')
(P/'analysis.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
