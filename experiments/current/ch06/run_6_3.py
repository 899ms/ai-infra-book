"""Explicit expert routes, collective payloads and native-format PP8 placement."""
from pathlib import Path
import json,hashlib,re,collections
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
expert=3*4096*1536*2; flop_task=2*3*4096*1536
routes={'balanced':[[((t*8+j)%128) for j in range(8)] for t in range(64)],'hot_concentrated':[list(range(8)) for t in range(64)],'hot_redistributed':[list(range(8)) for t in range(64)]}
rows=[]
for name,batch in routes.items():
 counts=collections.Counter(e for row in batch for e in row);loads=[0]*4;weights=[0]*4
 for e,n in counts.items():
  group=e//2 if name=='hot_redistributed' else e//32;loads[group]+=n;weights[group]+=expert
 assert sum(loads)==512 and all(len(set(r))==8 for r in batch)
 rows.append(dict(name=name,active_experts=len(counts),group_tasks=loads,group_weight_bytes=weights,total_weight_bytes=sum(weights),busiest_group_tasks=max(loads),busiest_group_flops=max(loads)*flop_task,busiest_TP2_rank_flops=max(loads)*flop_task//2,total_flops=512*flop_task))
kv=[dict(context=n,per_card_bytes=2*94*2*128*2*n,all_eight_cards_bytes=8*2*94*2*128*2*n) for n in (8192,16384)]
comm=[dict(tokens=n,fp32_vector_bytes=n*4096*4,attention_TP_send_per_rank=n*16384,expert_TP_send_per_rank=n*16384,EP_send_per_rank=n*24576,total_send_per_rank=n*57344,all_ranks_send=n*458752) for n in (1,8192)]
base=ROOT/'calculations/sources/deepseek-v4-flash';config_path=ROOT/'calculations/configs/models/deepseek-v4-flash/config.json';cfg=json.loads(config_path.read_text());index=json.loads((base/'model.safetensors.index.json').read_text());headers=sorted((base/'headers').glob('*.json'))
# PP8 consecutive layer blocks 6,6,6,5,5,5,5,5; MTP stays on final stage.
sizes=[6,6,6,5,5,5,5,5];owner={};at=0
stages=[]
for rank,size in enumerate(sizes):
 for layer in range(at,at+size):owner[layer]=rank
 stages.append(dict(rank=rank,layers=list(range(at,at+size)),weights=collections.Counter(),dtype_bytes=collections.Counter()))
 at+=size
assert at==43
seen=set();total=0
for file in headers:
 for name,t in json.loads(file.read_text()).items():
  if name=='__metadata__':continue
  assert name not in seen and index['weight_map'][name]+'.json'==file.name;seen.add(name)
  size=t['data_offsets'][1]-t['data_offsets'][0];total+=size
  match=re.match(r'layers\.(\d+)\.',name)
  rank=owner[int(match[1])] if match else (0 if name=='embed.weight' else 7)
  category='routed_experts' if '.ffn.experts.' in name else 'shared_experts' if '.ffn.shared_experts.' in name else 'attention' if '.attn.' in name else 'other_including_embeddings_norms_MTP'
  stages[rank]['weights'][category]+=size;stages[rank]['dtype_bytes'][t['dtype']]+=size
assert seen==set(index['weight_map']) and total==index['metadata']['total_size']
for stage in stages:
 kvbytes=sum((min(8192,cfg['sliding_window'])*584+(8192//cfg['compress_ratios'][l]*(584+(68 if cfg['compress_ratios'][l]==4 else 0)) if cfg['compress_ratios'][l] else 0)) for l in stage['layers'])
 stage.update(attention_state_bytes=kvbytes,workspace_bytes=2**31,total_weight_bytes=sum(stage['weights'].values()))
 stage['budget_bytes']=stage['total_weight_bytes']+kvbytes+2**31;stage['fits_H100_80GB']=stage['budget_bytes']<=80e9
 assert stage['fits_H100_80GB'] and stage['weights']['shared_experts']>0
files=['manuscripts/06-超节点.md',str(config_path.relative_to(ROOT)),str((base/'model.safetensors.index.json').relative_to(ROOT))]+[str(f.relative_to(ROOT)) for f in headers]
out=dict(exercise='6-3',routes=rows,KV=kv,communication=comm,V4_Flash_PP8=dict(format='Exact published checkpoint tensor dtypes and scales, no dequantization expansion; FP8/BF16 main KV 584 bytes per entry, MXFP4 index 68 bytes; 8192-token one active request',checkpoint_bytes=total,tensors_verified=len(seen),stages=stages,scope='Capacity placement only; whole model preserved including MTP weights but MTP execution disabled; 2GiB workspace is an explicit planning allowance, not profiled peak; PP8 physical execution deferred'),source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files})
(P/'6-3-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(rows,indent=2));print('PP8',[(s['rank'],s['total_weight_bytes'],s['budget_bytes'],s['dtype_bytes']) for s in stages])
