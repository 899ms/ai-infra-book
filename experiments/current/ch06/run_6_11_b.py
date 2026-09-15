"""Attention-head TP8 only: preserve non-attention work and replicated latent KV."""
from pathlib import Path
import json,hashlib,math,struct
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
arch=json.loads((ROOT/'calculations/results/supernode-inference-book.json').read_text());model=arch['model'];base=arch['results'][0]['batch1']
cfg=json.loads((ROOT/'calculations/configs/models/deepseek-v4.1-flash/config.json').read_text());cfg=cfg.get('text_config',cfg)
assert cfg['num_attention_heads']%8==0 and cfg['o_groups']%8==0
headers=sorted((ROOT/'calculations/sources/deepseek-v4.1-flash/headers').glob('*.header.bin'))
shards=[];replicated=0;read=0
for file in headers:
 raw=file.read_bytes();assert struct.unpack('<Q',raw[:8])[0]==len(raw)-8
 for name,t in json.loads(raw[8:]).items():
  if name=='__metadata__' or name.startswith(('mtp.','vision.','aligner.','image_')) or '.engram.' in name or '.ffn.experts.' in name:continue
  size=t['data_offsets'][1]-t['data_offsets'][0];replicated+=size
  if name=='embed.weight':continue
  read+=size
  if any('.attn.'+key in name for key in ('wq_b.','wo_a.','wo_b.')) or name.endswith('.attn.attn_sink'):
   # Direct attention projections only; indexer.wq_b deliberately excluded.
   assert size%8==0
   shards.append(dict(name=name,shape=t['shape'],global_bytes=size,per_rank_bytes=size//8))
assert replicated==model['replicated_bytes'] and read==model['replicated_read_bytes']
assert len({x['name'].split('.')[1] for x in shards})==40
shard_bytes=sum(x['global_bytes'] for x in shards)
new_weights=base['weight_bytes']-shard_bytes*7/8
memory=(new_weights+base['kv_bytes'])/model['hw']['hbm_Bps']
# Even the unpartitioned total compute bound is below memory, so retaining it
# avoids credit for sharding the unchanged shared experts/output head.
assert base['compute_s']<memory
alpha=8.33e-7;bw=450e9;message=4*model['hidden'];ring=14*alpha+1.75*message/bw
extra=model['layers']*ring;total=memory+base['comm_s']+extra
files=['manuscripts/06-超节点.md','calculations/results/supernode-inference-book.json','calculations/configs/models/deepseek-v4.1-flash/config.json','calculations/sources/deepseek-v4.1-flash/inference/model.py']+[str(f.relative_to(ROOT)) for f in headers]
out=dict(exercise='6-11',completed_parts=['b'],design='Main attention query heads and output groups TP8; query low-rank projection, shared latent KV, compressor and complete indexer replicated. Shared experts/output head/EP paths unchanged. FP32 attention output reduction once per layer.',sharded_tensors=shards,shardable_attention_weight_bytes=shard_bytes,unsharded_replicated_read_bytes=read-shard_bytes,new_total_weight_read_bytes=new_weights,KV_read_bytes_unchanged=base['kv_bytes'],memory_s=memory,unsharded_compute_upper_bound_s=base['compute_s'],existing_EP_communication_s=base['comm_s'],new_attention_allreduce_message_bytes=message,new_attention_allreduce_s=ring,new_attention_communication_s=extra,new_token_s=total,new_tokens_s=1/total,baseline_tokens_s=1/base['step_s'],speedup=base['step_s']/total,scope='Conditional byte/roofline model with explicitly replicated indexer; not an executed native world_size=8 run, which also shards indexer and changes other modules; no blanket division of all replicated weights or KV by eight',source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files})
(P/'6-11-b-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256','sharded_tensors')},indent=2))
