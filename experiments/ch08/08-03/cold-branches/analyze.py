import collections,hashlib,json
from pathlib import Path
r=Path(__file__).absolute().parent
load=lambda p:json.loads(p.read_text())
def lines(p):return list(map(json.loads,p.read_text().splitlines()))
for n,h in load(r/'reference-sha.json').items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h
s=load(r/'run/supervisor.json');assert s['exit_code']==0 and s['reason'] is None and not s['leftovers']
assert load(r/'reference/environment.json')['config']==load(r/'results/environment.json')['config']
assert load(r/'reference/input.json')==load(r/'results/input.json')
for n,h in load(r/'results/environment.json')['hashes'].items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h
warm_source=(r/'reference/run.py').read_text()
assert hashlib.sha256((r/'reference/run.py').read_bytes()).hexdigest()==load(r/'reference/environment.json')['hashes']['run.py']
assert (r/'run.py').read_text()==warm_source.replace("[('primer',1),('branches',4),('after',1)]","[('branches',4),('after',1)]").replace('requests=3,sequences=6','requests=2,sequences=5')
summary={}
for label,folder in [('cold','results'),('warm','reference')]:
 shots=lines(r/folder/'blocks.jsonl');observed=[];peak=0;first=None;scheduled=0
 assert shots[0]['event']=='init' and not shots[0]['requests'] and shots[0]['free_blocks']==shots[0]['total_blocks']-1
 for i,x in enumerate(shots):
  owners=collections.defaultdict(set);refs={}
  for q in x['requests']:
   assert len(q['blocks'])==1
   for b in q['blocks'][0]:
    owners[b['id']].add(q['id'])
    if b['id'] in refs:assert refs[b['id']]==b['refs']
    refs[b['id']]=b['refs']
  assert all(refs[k]==len(v) for k,v in owners.items())
  assert x['free_blocks']+len(owners)+1==x['total_blocks']
  branch=[q for q in x['requests'] if 'branches' in q['id']]
  if branch:
   peak=max(peak,len(owners));shared=[k for k,o in owners.items() if len(o)>1]
   scheduled+=sum(v for k,v in x.get('scheduled_tokens',{}).items() if 'branches' in k)
   if shared and first is None:first=dict(snapshot=i,event=x['event'],shared_blocks=len(shared),requests=[dict(id=q['id'],computed=q['computed'],blocks=len(q['blocks'][0]),status=q['status']) for q in branch])
   observed.append(dict(snapshot=i,unique_blocks=len(owners),shared_blocks=len(shared),shared_by_four=sum(len(o)==4 for o in owners.values()),references=sum(len(q['blocks'][0]) for q in branch)))
 assert not shots[-1]['requests'] and shots[-1]['free_blocks']==shots[-1]['total_blocks']-1
 requests=lines(r/folder/'requests.jsonl');branch_request=next(x for x in requests if x['id']=='branches');assert branch_request['n']==4 and len(branch_request['outputs'])==4
 assert all(len(o['ids'])==128 for x in requests for o in x['outputs'])
 if label=='cold':assert [x['id'] for x in requests]==['branches','after']
 summary[label]=dict(snapshots=len(shots),first_shared=first,peak_unique_owned=peak,max_shared_by_four=max(x['shared_by_four'] for x in observed),branch_scheduled_tokens=scheduled,final_free_blocks=shots[-1]['free_blocks'],observations=observed,branch_outputs=[o['ids'] for o in sorted(branch_request['outputs'],key=lambda x:x['index'])])
summary['comparison']=dict(same_branch_outputs=sum(x==y for x,y in zip(summary['cold']['branch_outputs'],summary['warm']['branch_outputs'])),scope='Fresh-engine n=4 versus prior warmed-prefix n=4; actual ownership/scheduling, not physical-copy or latency claim')
(r/'analysis.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:{n:v for n,v in x.items() if n not in ('observations','branch_outputs')} for k,x in summary.items()},indent=2))
