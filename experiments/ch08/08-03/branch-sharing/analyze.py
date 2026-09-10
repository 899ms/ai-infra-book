import json,collections,hashlib
from pathlib import Path
r=Path(__file__).absolute().parent
load=lambda p:json.loads(p.read_text())
def lines(p):return list(map(json.loads,p.read_text().splitlines()))
sup=load(r/'run/supervisor.json');assert sup['exit_code']==0 and sup['reason'] is None and not sup['leftovers']
for n,h in load(r/'results/environment.json')['hashes'].items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h
requests=lines(r/'results/requests.jsonl');assert [x['n'] for x in requests]==[1,4,1]
ref=requests[0]['outputs'][0]['ids'];assert len(ref)==128
for x in requests:
 assert len(x['outputs'])==x['n'] and all(len(o['ids'])==128 for o in x['outputs'])
shots=lines(r/'results/blocks.jsonl');four=[];peak=0
for i,s in enumerate(shots):
 owners=collections.defaultdict(set);refs={}
 for q in s['requests']:
  assert len(q['blocks'])==1
  for b in q['blocks'][0]:
   owners[b['id']].add(q['id'])
   if b['id'] in refs:assert refs[b['id']]==b['refs']
   refs[b['id']]=b['refs']
 for bid,o in owners.items():assert refs[bid]==len(o),(i,bid,refs[bid],len(o))
 assert s['free_blocks']+len(owners)+1==s['total_blocks'],i
 peak=max(peak,len(owners))
 branch=[q for q in s['requests'] if 'branches' in q['id'] and q['blocks'][0]]
 if len(branch)==4:
  sets=[set(b['id'] for b in q['blocks'][0]) for q in branch];common=set.intersection(*sets);private=[len(a-set.union(*(b for b in sets if b is not a))) for a in sets]
  four.append(dict(snapshot=i,time_s=s['time_s'],shared_by_four=len(common),private_blocks=private,request_owned_blocks=len(owners),summed_block_references=sum(len(a) for a in sets)))
assert four and max(x['shared_by_four'] for x in four)>0 and any(all(n>0 for n in x['private_blocks']) for x in four)
last=shots[-1];assert not last['requests'] and last['free_blocks']==last['total_blocks']-1
summary=dict(snapshots=len(shots),sequences=6,all_outputs_identical=all(o['ids']==ref for x in requests for o in x['outputs']),distinct_branch_outputs=len({tuple(o['ids']) for o in requests[1]['outputs']}),four_branch_snapshots=len(four),max_shared_by_four=max(x['shared_by_four'] for x in four),peak_unique_owned_blocks=peak,total_blocks=last['total_blocks'],final_free_blocks=last['free_blocks'],cached_tokens=[x['cached_tokens'] for x in requests],branch_observations=four,scope='Native n=4 with warmed APC prefix; ownership/refcount observation, not proof of copy-on-write or natural quality')
(r/'analysis.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items() if k!='branch_observations'},indent=2))
