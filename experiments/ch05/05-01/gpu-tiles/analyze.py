"""Independent CPU numerical reconstruction plus counter and timing audit."""
import argparse,csv,hashlib,json,math,statistics
from pathlib import Path
import torch
p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
r=Path(__file__).absolute().parent;torch.set_num_threads(4)
raw=json.loads((r/'results/raw.json').read_text());assert raw['source_sha256']==hashlib.sha256((r/'run.py').read_bytes()).hexdigest()
assert raw['configs']==[[32,64,32,4],[64,64,32,4],[128,128,32,8]] and raw['stages']==2
collection=json.loads((r/'counters/collection.json').read_text());assert len(collection['records'])==6
for name in ['measurement']+[f'm{m}-c{c}' for m in [1,1024] for c in range(3)]:
 s=json.loads((r/'runs'/name/'supervisor.json').read_text());assert s['exit_code']==0 and s['reason'] is None and not s['leftovers']
rows=[]
assert len(raw['timing'])==54
for shape in raw['shapes']:
 m=shape['m'];assert shape['n']==12288 and shape['k']==4096
 inp=torch.load(r/f'results/input-m{m}.pt',map_location='cpu',weights_only=True)
 assert inp['a'].shape==(m,4096) and inp['b'].shape==(4096,12288)
 assert inp['a'].dtype==inp['b'].dtype==torch.bfloat16
 reference=inp['a'].double()@inp['b'].double()
 stored=torch.load(r/f'results/reference-m{m}.pt',map_location='cpu',weights_only=True)
 torch.testing.assert_close(stored,reference,rtol=1e-10,atol=1e-9)
 previous=None
 for c,check in enumerate(shape['checks']):
  assert check['config']==c
  output=torch.load(r/f'results/output-m{m}-c{c}.pt',map_location='cpu',weights_only=True)
  assert output.shape==(m,12288) and output.dtype==torch.bfloat16
  if previous is not None:assert torch.equal(previous,output)
  previous=output
  err=output.double()-reference
  relative=(err.norm()/reference.norm()).item();scaled=(err.abs()/(.05+.01*reference.abs())).max().item()
  assert math.isclose(relative,check['relative_l2'],rel_tol=1e-9,abs_tol=1e-12)
  assert math.isclose(scaled,check['scaled_max'],rel_tol=1e-9,abs_tol=1e-12)
  assert check['pass_quality']==(relative<.005 and scaled<=1)
  samples=[x['ms_per_call'] for x in raw['timing'] if x['m']==m and x['config']==c];assert len(samples)==9
  for trial in range(9):
   group=[x for x in raw['timing'] if x['m']==m and x['trial']==trial]
   assert sorted(x['position'] for x in group)==[0,1,2] and sorted(x['config'] for x in group)==[0,1,2]
   assert all(x['repeats']==20 and x['ms_per_call']>0 for x in group)
  csvrows=list(csv.DictReader((r/f'counters/m{m}-c{c}.csv').open()));assert len(csvrows)==2
  units,data=csvrows;assert data['Kernel Name']=='gemm'
  metrics={}
  for key in collection['metrics']:
   unit='%' if key.startswith('sm__') else 'ns' if key.startswith('gpu__') else 'byte'
   assert units[key]==unit,(key,units[key]);metrics[key]=float(data[key].replace(',',''));assert metrics[key]>=0
  rec=next(x for x in collection['records'] if x['m']==m and x['config']==c)
  for flag,value in [('--cache-control','none'),('--clock-control','none'),('--profile-from-start','off'),('--replay-mode','kernel'),('--launch-count','1')]:assert rec['command'][rec['command'].index(flag)+1]==value
  launch={key:float(value.replace(',','')) for key,value in data.items() if key in ['launch__registers_per_thread','launch__registers_per_thread_allocated','launch__shared_mem_per_block','launch__shared_mem_per_block_driver','launch__shared_mem_per_block_dynamic','launch__occupancy_limit_registers','launch__occupancy_limit_shared_mem']}
  assert launch['launch__registers_per_thread']==check['registers'] and launch['launch__shared_mem_per_block_dynamic']==check['shared_bytes']
  rows.append(dict(m=m,config=c,quality=check,launch=launch,median_ms=statistics.median(samples),min_ms=min(samples),max_ms=max(samples),metrics=metrics,grid=data['Grid Size'],block=data['Block Size'],replay_passes=data['profiler__replayer_passes']))
summary=dict(rows=rows,all_outputs_equal_within_shape=True,cpu_fp64_reference_verified=True)
text=json.dumps(summary,indent=2)+'\n'
if a.check:assert json.loads((r/'analysis.json').read_text())==summary;print('PASS: full CPU FP64 reference, six outputs, 54 timings and six hardware reports')
else:(r/'analysis.json').write_text(text);print(text)
