"""Current 4-4: recompute schedules and independently verify resource/slot lifetimes."""
import hashlib,importlib.util,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.topics.matrix_vector_handoff import calculate
spec=importlib.util.spec_from_file_location('ch4derive',ROOT/'manuscripts/ch04/derive.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
pipelines=[]
for compute,latency in ((128,128),(64,128),(128,256)):
 for slots in range(1,5):
  p=mod.pipeline(slots,compute,latency);chunks=p['chunks']
  for i,c in enumerate(chunks):
   assert c['data_ready']==c['issue_start']+64+latency
   assert c['compute_start']>=c['data_ready'] and c['compute_end']==c['compute_start']+compute
   assert c['slot_released']==c['compute_end']
   if i:assert c['issue_start']>=chunks[i-1]['transfer_end'] and c['compute_start']>=chunks[i-1]['compute_end']
   if i>=slots:assert c['issue_start']>=chunks[i-slots]['slot_released']
  p['continuous_after_first']=all(chunks[i]['compute_start']==chunks[i-1]['compute_end'] for i in range(1,4))
  p['inter_compute_idle_ticks']=sum(chunks[i]['compute_start']-chunks[i-1]['compute_end'] for i in range(1,4))
  pipelines.append(p)
assert [p['finish_tick'] for p in pipelines[:4]]==[1280,768,704,704]
assert [p['finish_tick'] for p in pipelines[4:8]]==[1024,576,512,448]
assert [min(p['input_slots'] for p in pipelines if p['compute_ticks']==c and p['extra_latency_ticks']==128 and p['continuous_after_first']) for c in (128,64)]==[3,4]
handoff=[]
for path,rows,slots in [('staged',128,1),('staged',32,1),('staged',32,2),('direct',32,2),('direct',32,4)]:
 d=calculate(group_rows=rows,slots=slots,path=path);by={x['id']:x for x in d['timeline']}
 original=json.loads((ROOT/f'calculations/results/matrix-vector-{path}-rows{rows}-slots{slots}.json').read_text())
 assert d['timeline']==original['timeline'] and d['summary']==original['summary']
 for x in d['timeline']:
  assert x['end_tick']-x['start_tick']==x['duration_ticks']
  for dep in x['scheduled_predecessors']:assert by[dep]['end_tick']<=x['start_tick']
 for resource in ('matrix','vector','handoff'):
  ts=sorted((t for t in d['timeline'] if t['resource']==resource),key=lambda t:t['start_tick'])
  assert all(a['end_tick']<=b['start_tick'] for a,b in zip(ts,ts[1:]))
 for i in range(128//rows):
  chain=[by[f'g{i}.{stage}'] for stage in ('qk','scores','softmax','probabilities','pv')]
  assert all(a['end_tick']<=b['start_tick'] for a,b in zip(chain,chain[1:]))
  if i>=slots:assert by[f'g{i-slots}.pv']['end_tick']<=chain[0]['start_tick']
  assert d['slot_ownership'][i]['release_tick']==chain[-1]['end_tick']
 handoff.append(d)
assert [d['summary']['finish_tick'] for d in handoff]==[5118,5120,3200,3008,3008]
capacity=[]
for cap in (24,48,64,96):
 for rows in (16,32,64,128):
  per=rows*128*6;capacity.append(dict(capacity_kib=cap,group_rows=rows,bytes_per_group=per,maximum_resident_groups=cap*1024//per,maximum_useful_groups=min(128//rows,cap*1024//per)))
files=['manuscripts/ch04/derive.py','manuscripts/04-加速器架构.md','calculations/src/infra_calc/topics/matrix_vector_handoff.py','calculations/src/infra_calc/topics/request_dag.py']
result=dict(exercise='4-4',scope='Declared finite-slot teaching schedules, not GPU measurements',pipelines=pipelines,handoff=handoff,capacity=capacity,source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files})
(R/'4-4-results.json').write_text(json.dumps(result,indent=2)+'\n');print('Verified 12 input schedules, 5 handoff schedules, 16 capacity conditions')
