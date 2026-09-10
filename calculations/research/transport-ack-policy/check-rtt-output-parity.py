"""Full archived/new payload comparison for the additive raw RTT audit export."""
from pathlib import Path
import importlib.util
import json
import hashlib
import gc
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('compare_util',ROOT.parent/'transport-controller-loop/integration/check-network-public.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
code={f:m.filehash(ROOT/f) for f in ('calculate.py','receiver.py')}
checks=[]
for name in ('newreno','cubic_hystart','bbr'):
 path=ROOT/('book-aggregate-'+name+'-result.json')
 actual=json.loads(path.read_text())
 samples=actual.pop('rtt_samples')
 counts={d:len(x) for d,x in samples.items()}
 reader=m.Reader(ROOT/'pre-rtt-output'/path.name)
 count=dict(scalars=0,list_items=0)
 m.compare(reader,actual,(),count);reader.f.close()
 checks.append(dict(scenario=name,status='passed',rtt_samples=counts,comparison=count,old_sha256=m.filehash(ROOT/'pre-rtt-output'/path.name),new_sha256=m.filehash(path)))
 del actual,samples
 gc.collect()
old=json.loads((ROOT/'pre-rtt-output/result.json').read_text());new=json.loads((ROOT/'result.json').read_text())
for name, result in new.items():
 assert 'rtt_samples' in result
 result.pop('rtt_samples')
 assert result == old[name]
assert code=={f:m.filehash(ROOT/f) for f in code}
(ROOT/'rtt-output-parity.json').write_text(json.dumps(dict(status='passed',code_hashes=code,big_checks=checks,small_cases=list(new),excluded_added_field='rtt_samples'),indent=2)+'\n')
print('all 7 small + 3 full large old mathematical payloads unchanged',flush=True)
