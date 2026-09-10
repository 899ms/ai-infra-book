import collections,hashlib,json,statistics
from pathlib import Path
r=Path(__file__).absolute().parent
load=lambda p:json.loads(p.read_text())
def lines(p):return list(map(json.loads,p.read_text().splitlines()))
summary={};allrows={}
for slots in [1,2]:
 d=r/f'slots{slots}';sup=load(r/f'slots{slots}-run/supervisor.json');assert sup['exit_code']==0 and sup['reason'] is None and not sup['leftovers']
 for n,h in load(d/'environment.json')['hashes'].items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h
 rows=lines(d/'requests.jsonl');assert len(rows)==14;formal=[x for x in rows if x['wave']>=0];assert len(formal)==12 and len({x['id'] for x in rows})==14
 for x in rows:assert len(x['output_ids'])==(1 if x['wave']<0 else 64)
 shots=lines(d/'blocks.jsonl');max_ids=max_running=max_waiting=peak_owned=0;first={};preempted=set();identity_sets=[]
 for shot in shots:
  owners=collections.defaultdict(set);refs={};identities={};running=[];waiting=[]
  for q in shot['requests']:
   match=next(x for x in rows if q['id'].startswith(x['id']));name=match['adapter'];assert q['lora_name']=='book-control-'+name+'-v1' and q['lora_id']==(80301 if name=='a' else 80302)
   identities[q['id']]=name
   if q['status']=='RUNNING':
    running.append(q);first.setdefault(match['id'],shot['time_s'])
   elif q['status'].startswith('WAITING'):waiting.append(q)
   elif q['status']=='PREEMPTED':preempted.add(q['id'])
   assert len(q['blocks'])==1
   for b in q['blocks'][0]:owners[b['id']].add(q['id']);refs[b['id']]=b['refs']
  for bid,holders in owners.items():
   assert refs[bid]==len(holders)
   assert len({identities[h] for h in holders})==1,'KV block shared across adapters'
  assert shot['free_blocks']+len(owners)+1==shot['total_blocks']
  distinct=len({q['lora_id'] for q in running});assert distinct<=slots
  max_ids=max(max_ids,distinct);max_running=max(max_running,len(running));max_waiting=max(max_waiting,len(waiting));peak_owned=max(peak_owned,len(owners))
  if distinct:identity_sets.append(sorted({q['lora_id'] for q in running}))
 assert not shots[-1]['requests'] and shots[-1]['free_blocks']==shots[-1]['total_blocks']-1
 for wave in range(3):
  group=[x for x in formal if x['wave']==wave];assert len(group)==4 and max(x['start'] for x in group)<min(x['end'] for x in group)
  if wave:assert min(x['start'] for x in group)>=max(x['end'] for x in formal if x['wave']==wave-1)
 cases=[]
 for x in formal:
  cases.append(dict(id=x['id'],adapter=x['adapter'],wave=x['wave'],cached_tokens=x['cached_tokens'],wall_s=x['end']-x['start'],first_running_observation_s=first[x['id']]-x['start'],ttft_s=next(t for t,n in x['events'] if n>0)-x['start']))
 summary[str(slots)]=dict(snapshots=len(shots),formal_requests=12,max_distinct_running_adapters=max_ids,max_running_requests=max_running,max_waiting_requests=max_waiting,observed_preempted_requests=len(preempted),peak_unique_owned_blocks=peak_owned,final_free_blocks=shots[-1]['free_blocks'],cases=cases,per_adapter={a:dict(requests=6,median_wall_s=statistics.median(x['wall_s'] for x in cases if x['adapter']==a),max_wall_s=max(x['wall_s'] for x in cases if x['adapter']==a)) for a in ['a','b']})
 allrows[slots]={x['id']:x for x in formal}
 assert all(len(x['state'][0]['gpu_slot_ids'])==slots for x in lines(d/'slots.jsonl'))
assert load(r/'slots1/input.json')==load(r/'slots2/input.json')
a=load(r/'slots1/environment.json')['config'];b=load(r/'slots2/environment.json')['config'];a.pop('max_loras');b.pop('max_loras');assert a==b
summary['comparison']=dict(same_outputs=sum(allrows[1][k]['output_ids']==allrows[2][k]['output_ids'] for k in allrows[1]),pairs=12,scope='Two untrained control identities; fixed sequential engine configurations, not production tail latency')
(r/'analysis.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:{n:v for n,v in x.items() if n!='cases'} for k,x in summary.items()},indent=2))
