"""Per-step service and event schedule; deadlines, restart and resource cost."""
from pathlib import Path
import json,hashlib,importlib.util,math,csv
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
spec=importlib.util.spec_from_file_location('continuity',ROOT/'manuscripts/ch06/continuity_model.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
arch=json.loads((ROOT/'manuscripts/ch06/continuity-model.json').read_text())

def calculate(history,p,stall=None):
 steps=[]
 for j in range(8):
  positions=history+j+1
  local=(m.WEIGHT_READ/p+m.KV_TOKEN*positions/min(p,m.KVH))/m.H100['hbm_Bps']
  compute=(m.WEIGHT_READ+4*m.QH*m.D*positions*m.L)/p/m.H100['matrix_flops_per_s']
  comm=128*(0 if p==1 else 2*(p-1)*m.PARAMS['nvlink_alpha_s']+2*(p-1)/p*m.MESSAGE/m.PARAMS['nvlink_Bps'])
  total=max(local,compute)+comm
  assert math.isclose(total,m.step(p,history+j)['total_s'],abs_tol=1e-14)
  steps.append(dict(step=j+1,positions=positions,local_s=local,compute_s=compute,comm_s=comm,total_s=total))
 service=sum(x['total_s'] for x in steps)*1000
 instances=8//p;clocks=[0.]*instances;events=[]
 for session in range(4):
  inst=session%instances
  if inst==0 and clocks[inst]==0 and stall is not None:
   assert service>20 # fault occurs before first completion; restart entire service
   clocks[inst]=20+stall
  start=clocks[inst];clocks[inst]+=service
  events.append(dict(session=session,instance=inst,start_ms=start,end_ms=clocks[inst]))
 required=math.ceil(4/instances);fit=m.max_sessions(p,history+8)>=required
 end=max(x['end_ms'] for x in events);gpu_s=8*end/1000
 checks=[]
 for deadline in (100,130,170):
  ontime=sum(x['end_ms']<=deadline for x in events)
  checks.append(dict(deadline_ms=deadline,ontime=ontime,eligible=fit and ontime>=3,gpu_s_per_ontime=gpu_s/ontime if ontime else None))
 return dict(tp=p,history=history,stall_ms=stall,instances=instances,capacity_sessions_per_instance=m.max_sessions(p,history+8),assigned_sessions_per_instance=required,capacity_fits=fit,steps=steps,service_ms=service,events=events,gpu_s=gpu_s,energy_upper_j=10200*end/1000,deadlines=checks)
rows=[calculate(h,p,stall) for h in (131064,32760) for stall in (None,40,10) for p in (1,2,4,8)]
for h,key in [(131064,'candidates'),(32760,'candidates_32k')]:
 for p in (1,2,4,8):
  ref=next(x for x in arch[key] if x['tp']==p)
  for stall,phase in [(None,'healthy'),(40,'fault')]:
   row=next(x for x in rows if x['history']==h and x['tp']==p and x['stall_ms']==stall)
   assert math.isclose(row['service_ms'],ref['service_ms'],abs_tol=1e-10)
   assert all(math.isclose(x['end_ms'],y,abs_tol=1e-10) for x,y in zip(row['events'],ref[phase+'_completion_ms']))
   assert row['capacity_fits']==ref['capacity_fits']
   assert math.isclose(row['gpu_s'],ref[phase+'_gpu_seconds'],abs_tol=1e-12)
# Re-read the smallest archived correct two-server message >= actual 10 KiB.
records=[x for x in csv.DictReader((ROOT/'experiments/ch07/07-03/rows.csv').open()) if x['run']=='hgx2' and x['mode']=='out_of_place' and x['row_correct']=='True' and int(x['size_bytes'])>=m.MESSAGE]
record=min(records,key=lambda x:int(x['size_bytes']));assert int(record['nranks'])==16
raw=(ROOT/'experiments/ch07/07-03'/record['source']).read_text().splitlines()[int(record['line'])-1].split()
assert int(raw[0])==int(record['size_bytes']) and float(raw[5])==float(record['time_us']) and float(raw[8])==0
ar=float(record['time_us'])*1e-6
service16=0;steps16=[]
for j in range(8):
 local=(m.WEIGHT_READ/16+m.KV_TOKEN*(131064+j+1)/8)/m.H100['hbm_Bps'];compute=(m.WEIGHT_READ+4*m.QH*m.D*(131064+j+1)*m.L)/16/m.H100['matrix_flops_per_s'];total=max(local,compute)+128*ar
 service16+=total;steps16.append(total)
assert math.isclose(service16,sum(m.step(16,131064+j,'measured_two_servers')['total_s'] for j in range(8)),abs_tol=1e-12)
power=[]
for ceiling in (10000,10200,12000):
 for r in rows:
  if r['history']!=32760 or r['stall_ms'] is not None:continue
  time_ok=next(x for x in r['deadlines'] if x['deadline_ms']==130)['ontime']>=3
  power.append(dict(power_cap_w=ceiling,tp=r['tp'],capacity_pass=r['capacity_fits'],deadline_pass=time_ok,power_pass=10200<=ceiling,eligible=r['capacity_fits'] and time_ok and 10200<=ceiling))
sources=['manuscripts/06-超节点.md','manuscripts/ch06/continuity_model.py','manuscripts/ch06/continuity-model.json','calculations/configs/hardware.json','calculations/configs/models/qwen3-32b/config.json','experiments/ch07/07-03/rows.csv','experiments/ch07/07-03/'+record['source']]
out=dict(exercise='6-10',rows=rows,TP16=dict(record=record,step_s=steps16,service_ms=service16*1000,meets_50ms=service16<=.05),power_scenarios=power,scope='Analytical schedules, fixed eight allocated cards billed until final completion, restart first service from beginning; system maximum power is a budget envelope, not metered energy; TP16 uses archived nearest-larger message',source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in sources})
(P/'6-10-results.json').write_text(json.dumps(out,indent=2)+'\n')
for r in rows:
 print(r['history'],r['stall_ms'],r['tp'],round(r['service_ms'],6),[round(x['end_ms'],6) for x in r['events']],round(r['gpu_s'],6),[(d['deadline_ms'],d['ontime'],d['eligible']) for d in r['deadlines']])
print('TP16 ms',service16*1000,'record',record)
