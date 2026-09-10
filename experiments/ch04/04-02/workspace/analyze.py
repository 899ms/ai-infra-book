"""CPU value audit and allocator snapshot reconciliation for all repetitions."""
from pathlib import Path
import json,pickle,torch
r=Path(__file__).absolute().parent;torch.set_num_threads(4)
w=torch.load(r/'expert.pt',weights_only=True,map_location='cpu')['reference_fp32'].double();rows=[]
for phase in ['decode','prefill']:
 for mode in ['direct','dequant']:
  d=r/'results'/(phase+'-'+mode);v=json.loads((d/'measurement.json').read_text());t=torch.load(d/'output.pt',weights_only=True,map_location='cpu')
  ref=t['x'].double()@w;error=float(torch.linalg.vector_norm(t['output'].double()-ref)/torch.linalg.vector_norm(ref))
  assert error<=.02
  assert v['resident_increment_bytes']>=sum(v['logical'].values())
  for rec in v['records']:
   snap=pickle.loads((d/(rec['stage']+'-snapshot.pickle')).read_bytes())
   allocated=sum(b['size'] for s in snap['segments'] for b in s['blocks'] if b['state']=='active_allocated')
   reserved=sum(s['total_size'] for s in snap['segments'])
   assert allocated==rec['end']['allocated'] and reserved==rec['end']['reserved']
   assert rec['end']['peak_allocated']>=allocated and rec['peak_increment_bytes']>=rec['output_bytes']
   assert any(t['action']=='alloc' for trace in snap['device_traces'] for t in trace)
  rows.append(dict(phase=phase,mode=mode,m=v['m'],relative_l2=error,resident_bytes=v['resident_increment_bytes'],logical=v['logical'],peaks=[x['peak_increment_bytes'] for x in v['records']],reserved_peaks=[x['end']['peak_reserved'] for x in v['records']],retained_after_release=[x['after_output_release']['allocated']-v['resident']['allocated'] for x in v['records']],absolute_peak_increments=[x['end']['peak_allocated']-v['baseline']['allocated'] for x in v['records']]))
(r/'analysis.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
