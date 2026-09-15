"""Recompute matched projection evidence from raw tensors, trials and counter CSVs."""
import hashlib,importlib.util,json
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[2];E=ROOT/'experiments/ch04/04-06'
def call(name):
 spec=importlib.util.spec_from_file_location(name,E/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m.analyze()
p=call('analyze_projection');t=call('analyze_counters')
assert p==json.loads((E/'results/projection-summary.json').read_text())
assert t==json.loads((E/'results/projection-traffic.json').read_text())
rows=[]
for m in (1,256):
 for mode in ('reused','rotating'):
  mac=next(x for x in p if x['device']=='mps' and x['m']==m and x['mode']==mode)
  gpu=next(x for x in p if x['device']=='cuda' and x['m']==m and x['mode']==mode)
  traffic=next(x for x in t['rows'] if x['m']==m and x['mode']==mode)
  logical=2*(4096*4096+2*m*4096)
  assert abs(mac['predicted_memory_service_us']-logical/400e9*1e6)<1e-9
  assert abs(gpu['predicted_memory_service_us']-logical/1792e9*1e6)<1e-9
  rows.append(dict(m=m,mode=mode,mac_wall_us=mac['wall_median_us'],rtx_wall_us=gpu['wall_median_us'],mac_to_rtx_wall_ratio=mac['wall_median_us']/gpu['wall_median_us'],logical_input_weight_output_bytes=logical,flops=2*m*4096**2,counters=traffic))
files=[E/'analyze_projection.py',E/'analyze_counters.py',E/'results/projection-summary.json',E/'results/projection-traffic.json',E/'results/projection-manifest.json',E/'results/counter-manifest.json']
out=dict(exercise='4-6',scope='Independent reanalysis of recorded synthetic matched projections, not a new timing run',rows=rows,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},gates='Original raw tensors and FP64 reference recalculated, identical inputs, 11 trial medians, source hashes, counter units and kernel sums verified by original analyzers')
(R/'4-6-results.json').write_text(json.dumps(out,indent=2)+'\n');print('Verified eight timing conditions and four counter captures from raw artifacts')
