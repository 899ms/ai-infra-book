"""Offload capacity after staging buffers and repeated transfer lower bounds."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('08-*.md'))
unit=288*2**20;volume=9*unit;rows=[]
for buffers in (1,2):
 saved=volume-buffers*unit;states=[]
 for mib in (1152,1188):
  size=mib*2**20;n=saved//size
  assert n*size<=saved<(n+1)*size
  states.append(dict(state_MiB=mib,additional_complete_states=n,remaining_MiB=(saved-n*size)//2**20))
 rows.append(dict(buffers=buffers,buffer_MiB=buffers*288,net_saved_MiB=saved//2**20,states=states))
transfers=[dict(bandwidth_GBps=b,per_step_ms=float(F(volume,b*10**9)*1000),all_255_steps_seconds=float(F(255*volume,b*10**9))) for b in (64,450)]
minimum=255*volume
assert F(255*volume,minimum)==1 and F(255*volume,minimum-1)>1
out=dict(exercise='8-5',capacity=rows,per_step_copy_bytes=volume,all_255_steps_copy_bytes=minimum,transfer_lower_bounds=transfers,minimum_one_direction_GBps_for_1s=float(F(minimum,10**9)),scope='Given full nine-weight stream every decode step; buffers reused, not persistent weight caching; transfer busy-time lower bound, not measured or necessarily exposed request delay',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'8-5-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
