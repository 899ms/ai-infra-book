import argparse,hashlib,json,time
from pathlib import Path
import torch
from safetensors import safe_open
p=argparse.ArgumentParser();p.add_argument('--snapshot',type=Path,required=True);a=p.parse_args();r=Path(__file__).absolute().parent
assert not (r/'expert.pt').exists();torch.set_num_threads(4)
key='model.language_model.layers.0.mlp.experts.gate_up_proj';index=json.loads((a.snapshot/'model.safetensors.index.json').read_text());shard=index['weight_map'][key];assert index['weight_map'][key+'_scale_inv']==shard
with safe_open(a.snapshot/shard,framework='pt',device='cpu') as f:
 q=f.get_slice(key)[0].clone().contiguous();scale=f.get_slice(key+'_scale_inv')[0].clone().contiguous()
assert q.shape==(2048,1536) and scale.shape==(16,12)
reference=q.float()*scale.repeat_interleave(128,0).repeat_interleave(128,1)
start=time.perf_counter();sw=reference.abs().amax(0).clamp_min(1e-12)/127;qw=(reference/sw).round().clamp(-127,127).to(torch.int8).contiguous();end=time.perf_counter()
torch.save(dict(checkpoint_fp8=q,checkpoint_scale=scale,reference_fp32=reference,int8_weight=qw,int8_scale=sw),r/'expert.pt')
def digest(t):return hashlib.sha256(t.contiguous().view(torch.uint8).numpy().tobytes()).hexdigest()
meta=dict(snapshot=str(a.snapshot),checkpoint_key=key,expert_index=0,shard=shard,shape=list(q.shape),scale_shape=list(scale.shape),block_shape=[128,128],
 original_dtype=str(q.dtype),cpu_pack_s=end-start,cpu_threads=4,pack_scope='FP32 column scale/requantize/clamp/INT8 cast on CPU; excludes source reading and FP8 decode',
 hashes={k:hashlib.sha256((a.snapshot/k).read_bytes()).hexdigest() for k in ['config.json','model.safetensors.index.json']},
 tensor_hashes={k:digest(v) for k,v in dict(checkpoint_fp8=q,checkpoint_scale=scale,reference_fp32=reference,int8_weight=qw,int8_scale=sw).items()},
 artifact_sha256=hashlib.sha256((r/'expert.pt').read_bytes()).hexdigest(),scope='Actual first expert gate_up checkpoint matrix; source is already FP8, not original pre-quantization BF16; activations remain synthetic.')
(r/'provenance.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta))
