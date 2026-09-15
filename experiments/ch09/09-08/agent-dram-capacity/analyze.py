import hashlib,json,random,statistics,math
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'results'
def read(p):return json.loads(p.read_text())
def lines(p):return [json.loads(l) for l in p.read_text().splitlines()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ex=read(O/'execution.json');assert len(ex['rows'])==2 and all(x['exit_code']==0 for x in ex['rows']) and not ex['after_gpu'].strip()
source=read(R/'inputs.json')
for p,h in source['source_sha256'].items():assert sha(Path(p))==h
inputs=[x for x in source['requests'] if x['kind']=='agent'];rng=random.Random(908);pressure=[[rng.randrange(1000,10000) for _ in range(3584)] for _ in inputs];records=[];outputs={};groups=[]
for setting in ['1.01','1.25']:
 capacity=4096;ratio=float(setting)
 d=O/setting;raw=read(d/'raw.json');rows=lines(d/'requests.jsonl');assert raw['status']=='all_requests_returned' and raw['config']['max_total_tokens']==capacity and len(rows)==36 and rows==raw['requests']
 assert raw['server_info']['max_total_num_tokens']==capacity
 for n,h in raw['source_hashes'].items():assert sha(R/n)==h
 for index,(item,other) in enumerate(zip(inputs,pressure)):
  pair=[]
  for j,(phase,ids) in enumerate([('target_before',item['input_ids']),('pressure',other),('target_after',item['input_ids'])]):
   row=rows[index*3+j];assert row['turn']==item['turn'] and row['phase']==phase and row['input_ids']==ids
   response=row['response'];m=response['meta_info'];assert m['prompt_tokens']==len(ids) and m['completion_tokens']==1 and m['num_retractions']==0
   detail={k:(m.get('cached_tokens_details') or {}).get(k,0) for k in ['device','host','storage']};assert m['cached_tokens']==sum(detail[k] for k in ['device','host','storage']) and detail['storage']==0
   r=dict(capacity=capacity,host_ratio=ratio,turn=item['turn'],phase=phase,input_tokens=len(ids),cached_tokens=m['cached_tokens'],levels=detail,complete_request_s=row['end_s']-row['start_s']);records.append(r)
   if phase!='pressure':pair.append(tuple(response['output_ids']));outputs.setdefault(item['turn'],[]).append(tuple(response['output_ids']))
  assert len(pair)==2
 for phase in ['target_before','target_after']:
  a=[x for x in records if x['capacity']==capacity and x['host_ratio']==ratio and x['phase']==phase];times=sorted(x['complete_request_s'] for x in a)
  groups.append(dict(capacity=capacity,host_ratio=ratio,phase=phase,requests=len(a),request_hit_rate=sum(x['cached_tokens']>0 for x in a)/len(a),token_hit_rate=sum(x['cached_tokens'] for x in a)/sum(x['input_tokens'] for x in a),levels={k:sum(x['levels'][k] for x in a) for k in ['device','host','storage']},request_median_s=statistics.median(times),request_sample_p95_s=times[math.ceil(.95*len(times))-1],sum_request_s=sum(times)))
assert all(read(O/setting/'raw.json')['config']['hicache_ratio']==float(setting) for setting in ['1.01','1.25'])
result=dict(status='native_agent_dram_capacity_verified',requests=72,target_requests=48,pressure_requests=24,all_target_outputs_equal_across_capacities=all(len(set(a))==1 for a in outputs.values()),per_turn_outputs={str(k):v for k,v in outputs.items()},groups=groups,records=records,scope='Native device/host hit counters under explicit unrelated pressure; one trace pass/capacity in fixed order. Complete request timing is not isolated host transfer or representative recovery p95. No storage backend, task-quality or bitwise KV claim.')
reference=R.parent/'agent-host-capacity/summary.json'
baseline=read(reference)
result['ratio2_reference_sha256']=sha(reference)
result['all_targets_equal_to_ratio2_reference']=all(all(list(x)==baseline['per_turn_outputs'][str(k)][0] for x in a) for k,a in outputs.items())
(R/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(groups,indent=2))
