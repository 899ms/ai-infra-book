import collections,hashlib,itertools,json,math,statistics
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[3];P=R.parent;K=P.parent/'09-09/remote-kv';C=K/'cross-mac-traces-001';sources={}
def read(p):
 sources[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
def lines(p):
 sources[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();return [json.loads(l) for l in p.read_text().splitlines()]
inputs=lines(C/'results/agent-producer/requests.jsonl');io=read(P/'agent-storage-io/summary.json');cold=read(K/'trace-cold-control-001/summary.json');native=read(P/'agent-host-capacity/summary.json');remote=lines(C/'results/agent-producer/remote.jsonl')+lines(C/'results/agent-consumer/remote.jsonl');page=io['page_bytes'];assert page==2359296
write={};get={}
for r in remote:
 assert r['error'] is None
 if r['op']=='set':
  assert len(r['meta']['entries'])==1;write.setdefault(r['meta']['entries'][0]['key'],[]).append(r['end_s']-r['start_s'])
 if r['op']=='get':
  assert len(r['meta']['keys'])==1;get.setdefault(r['meta']['keys'][0],[]).append(r['end_s']-r['start_s'])
get_fallback=statistics.median(x for a in get.values() for x in a)
class Cache:
 def __init__(self,n):self.n=n;self.items=collections.OrderedDict();self.evictions=0
 def find(self,k):
  if k not in self.items:return False
  self.items.move_to_end(k);return True
 def put(self,k):
  if not self.n:return False
  new=k not in self.items;self.items[k]=True;self.items.move_to_end(k)
  if len(self.items)>self.n:self.items.popitem(last=False);self.evictions+=1
  return new
 def clear(self):self.items.clear()
scenarios=[]
for caps in itertools.product([0,64,256],repeat=4):
 for policy,fault in itertools.product(['full','periodic4','recompute'],['none','restart7','invalidate7']):
  tiers={n:Cache(c) for n,c in zip(['hbm','dram','local','remote'],caps)};requests=[]
  for index,item in enumerate(inputs):
   if index==6 and fault!='none':
    for n,t in tiers.items():
     if fault=='invalidate7' or n in ['hbm','dram']:t.clear()
   keys=item['expected_reusable_keys'];hits={n:0 for n in tiers};read_s=0.;write_s=0.;writes={n:0 for n in ['local','remote']};fallback=0
   for key in keys:
    found=None
    for n,t in tiers.items():
     if t.find(key):found=n;break
    if found is None:break
    hits[found]+=16
    if found=='local':read_s+=statistics.median(io['per_page'][key+'.bin']['read_samples_s'])
    if found=='remote':read_s+=statistics.median(get[key]) if key in get else get_fallback;fallback+=int(key not in get)
   matched=sum(hits.values());full=matched==len(keys)*16
   if full:
    cap=4096 if hits['dram'] else 8192
    compute=next(x['complete_request_s'] for x in native['records'] if x['capacity']==cap and x['phase']=='target_after' and x['turn']==item['turn']);profile='host_profile' if hits['dram'] else 'gpu_warm_profile'
   else:compute=next(x['median_s'] for x in cold['per_input'] if x['kind']=='agent' and x['turn']==item['turn']);profile='full_cold_proxy'
   for key in keys:
    tiers['hbm'].put(key);tiers['dram'].put(key)
   checkpoint=policy=='full' or (policy=='periodic4' and (index+1)%4==0)
   if checkpoint:
    for key in keys:
     for n in ['local','remote']:
      if tiers[n].put(key):
       writes[n]+=page
       if n=='local':write_s+=io['per_page'][key+'.bin']['write_s']
       else:assert key in write;write_s+=statistics.median(write[key])
   assert all(len(t.items)<=t.n for t in tiers.values())
   requests.append(dict(turn=item['turn'],input_tokens=item['input_tokens'],hit_tokens=matched,tier_hits=hits,recompute_tokens=item['input_tokens']-matched,first_missing_page=matched//16 if not full else None,checkpoint=checkpoint,write_bytes=writes,storage_read_component_s=read_s,storage_write_component_s=write_s,model_profile=profile,model_profile_s=compute,estimated_request_s=compute+read_s+write_s,remote_read_fallback_pages=fallback))
  times=sorted(x['storage_read_component_s'] for x in requests if x['storage_read_component_s']>0)
  scenarios.append(dict(capacity_pages=dict(zip(tiers,caps)),policy=policy,fault=fault,requests=requests,request_hit_rate=sum(x['hit_tokens']>0 for x in requests)/12,token_hit_rate=sum(x['hit_tokens'] for x in requests)/sum(x['input_tokens'] for x in requests),write_bytes={n:sum(x['write_bytes'][n] for x in requests) for n in ['local','remote']},storage_read_sample_p95_s=times[math.ceil(.95*len(times))-1] if times else None,estimated_trace_completion_s=sum(x['estimated_request_s'] for x in requests),evictions={n:t.evictions for n,t in tiers.items()}))
assert len(scenarios)==729
for n in ['run.py','PROTOCOL.md']:sources[str((R/n).relative_to(ROOT))]=hashlib.sha256((R/n).read_bytes()).hexdigest()
(R/'results.json').write_text(json.dumps(dict(status='same_agent_page_policy_replay_complete',scenario_count=729,request_records=8748,page_bytes=page,remote_unseen_read_median_s=get_fallback,source_sha256=sources,scenarios=scenarios,scope='Defined inclusive page-LRU retention simulation, synchronous barriers and measured timing proxies. Not native tree policy, real four-tier execution, V4 state or production p95.'),indent=2)+'\n');print('729 scenarios,8748 request records completed')
