"""CPU-only inspection of retained conflicting BF16 page bytes, on RTX host."""
import hashlib,json
from pathlib import Path
import torch
R=Path(__file__).resolve().parent;S=R/'docker-store';ledger=[json.loads(l) for l in (S/'ledger.jsonl').read_text().splitlines()];out=[]
for row in ledger:
 if row['path']!='/set':continue
 for e in row['response']['entries']:
  if not e.get('collision'):continue
  a=S/(e['key']+'.bin');b=S/'collisions'/(e['key']+'-'+e['incoming_sha256'][:12]+'.bin')
  aa=a.read_bytes();bb=b.read_bytes();assert len(aa)==len(bb)==e['bytes']
  assert hashlib.sha256(aa).hexdigest()==e['sha256'] and hashlib.sha256(bb).hexdigest()==e['incoming_sha256']
  x=torch.frombuffer(bytearray(aa),dtype=torch.bfloat16).float();y=torch.frombuffer(bytearray(bb),dtype=torch.bfloat16).float()
  assert torch.isfinite(x).all() and torch.isfinite(y).all()
  unequal=x!=y;diff=(x-y).abs();idx=unequal.nonzero().flatten()
  out.append(dict(key=e['key'],stored_sha256=e['sha256'],incoming_sha256=e['incoming_sha256'],bytes=len(aa),bf16_elements=x.numel(),different_bytes=sum(a!=b for a,b in zip(aa,bb)),different_values=int(unequal.sum()),max_absolute_difference=float(diff.max()),relative_l2_difference=float(torch.linalg.vector_norm(x-y)/torch.linalg.vector_norm(x)),first_different_value=int(idx[0]) if idx.numel() else None,last_different_value=int(idx[-1]) if idx.numel() else None))
for row in out:
 row['client_operations']={}
 for phase in ('producer','consumer'):
  trace=[json.loads(l) for l in (R/'results'/phase/'remote.jsonl').read_text().splitlines()]
  for op in ('set','get'):
   entries=[e for t in trace if t['op']==op for e in (t['meta'].get('entries') or t['meta'].get('keys',[]))]
   row['client_operations'][phase+'_'+op]=dict(total_entries=len(entries),matching_zero_based_indices=[i for i,e in enumerate(entries) if (e.get('key') if isinstance(e,dict) else e)==row['key']])
dictout=dict(collision_events=len(out),unique_keys=len({r['key'] for r in out}),rows=out,interpretation='Actual byte/value differences under retained-first-value storage. Identical generated outputs do not establish bitwise KV equality. No cause inferred from these aggregate statistics.')
(R/'collision-analysis.json').write_text(json.dumps(dictout,indent=2)+'\n');print(json.dumps(dictout,indent=2))
