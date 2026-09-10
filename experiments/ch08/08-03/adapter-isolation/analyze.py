import collections,hashlib,json,struct
from pathlib import Path
r=Path(__file__).absolute().parent
load=lambda p:json.loads(p.read_text())
def lines(p):return list(map(json.loads,p.read_text().splitlines()))
sup=load(r/'run/supervisor.json');assert sup['exit_code']==0 and not sup['leftovers'] and sup['reason'] is None
adapters={}
for name in ['a','b']:
 d=r/'adapters'/name;raw=(d/'adapter_model.safetensors').read_bytes();meta=load(d/'provenance.json');assert hashlib.sha256(raw).hexdigest()==meta['sha256']
 length=struct.unpack('<Q',raw[:8])[0];header=json.loads(raw[8:8+length]);assert len(header)==72;nonzero=0
 for key,v in header.items():
  assert v['dtype']=='BF16';part=key.split('lora_')[1][0];assert v['shape']==([8,4096] if part=='A' else [4096,8])
  begin,end=v['data_offsets'];view=memoryview(raw)[8+length+begin:8+length+end].cast('H');nonzero+=sum(bool(x&0x7fff) for x in view)
 assert nonzero==meta['nonzero'] and nonzero>0
 adapters[name]=dict(tensors=72,nonzero=nonzero,sha256=meta['sha256'])
assert adapters['a']['sha256']!=adapters['b']['sha256']
rows=lines(r/'results/requests.jsonl');assert [x['adapter'] for x in rows]==['base','base','a','a','b','b','a','base'];shots=lines(r/'results/blocks.jsonl');seen=collections.Counter()
for shot in shots:
 owners=collections.defaultdict(set);refs={}
 for q in shot['requests']:
  row=next(x for x in rows if q['id'].startswith(x['id']));name=row['adapter'];expected=None if name=='base' else 'book-control-'+name+'-v1';assert q['lora_name']==expected;assert q['lora_id']==(None if name=='base' else 80301 if name=='a' else 80302);seen[name]+=1
  assert len(q['blocks'])==1
  for b in q['blocks'][0]:owners[b['id']].add(q['id']);refs[b['id']]=b['refs']
 assert all(refs[k]==len(v) for k,v in owners.items())
 assert shot['free_blocks']+len(owners)+1==shot['total_blocks']
assert all(seen[n] for n in ['base','a','b']) and not shots[-1]['requests'] and shots[-1]['free_blocks']==shots[-1]['total_blocks']-1
first={};checks=[]
for x in rows:
 name=x['adapter'];assert len(x['output_ids'])==64
 state=x['adapter_state'];assert len(state)==1 and len(state[0]['gpu_slot_ids'])==1
 if name!='base':assert state[0]['gpu_slot_ids']==[80301 if name=='a' else 80302]
 checks.append(dict(id=x['id'],adapter=name,cached_tokens=x['cached_tokens'],same_as_first=x['output_ids']==first.get(name,x['output_ids']),same_as_base=x['output_ids']==rows[0]['output_ids'],gpu_slot=state[0]['gpu_slot_ids'],registered=state[0]['registered']))
 first.setdefault(name,x['output_ids'])
summary=dict(requests=8,snapshots=len(shots),adapters=adapters,cases=checks,first_use_cache_isolated=all(rows[i]['cached_tokens']==0 for i in [0,2,4]),repeat_outputs_stable=all(x['same_as_first'] for x in checks),final_free_blocks=shots[-1]['free_blocks'],scope='Untrained nonzero adapter controls; identity and one GPU slot, not model quality or authentication')
(r/'analysis.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
