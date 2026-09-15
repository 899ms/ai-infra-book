"""Exact capacity and expected expert reuse for current exercise 6-1."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,math
P=Path(__file__).resolve().parent;ROOT=P.parents[2];C=ROOT/'calculations'
c=json.loads((C/'configs/models/qwen3-235b-a22b/config.json').read_text())
placement=json.loads((C/'results/qwen235-placement-tp8-kv-replica.json').read_text())
for src in placement['sources']: assert hashlib.sha256((C/src['file']).read_bytes()).hexdigest()==src['sha256']
hardware=json.loads((C/'configs/hardware.json').read_text());devices=hardware if isinstance(hardware,list) else hardware['devices'];h=next(x for x in devices if x['id']=='h100-sxm')
bw=int(h['memory']['bandwidth_bytes_per_second']);rate=next(x for x in h['peak_rates'] if x['input_precision'] in ('BF16','FP16') and x['sparsity']=='dense' and x['execution_unit']=='tensor');peak=F(str(rate['tera_ops_per_second']))*10**12
L=c['num_hidden_layers'];H=c['hidden_size'];D=c['head_dim'];heads=c['num_key_value_heads'];E=c['num_experts'];k=c['num_experts_per_tok'];I=c['moe_intermediate_size'];kv=2*L*heads*D*2
kvrows=[dict(tokens=n,bytes=kv*n,GiB=float(F(kv*n,2**30)),GB=kv*n/1e9) for n in (4096,8192,16384)]
weights=[]
for rank in placement['ranks']:
 w=sum(next(s['total_bytes'] for s in t['storage'] if s['bits']==16) for t in rank['tensors']);weights.append(w)
assert len(weights)==8 and set(weights)=={58959617024}
cap=80*10**9;workspace=2**31;per_session=kv*32768//heads
limit=(cap-max(weights)-workspace)//per_session
assert max(weights)+workspace+limit*per_session<=cap<max(weights)+workspace+(limit+1)*per_session
# Independently reconstruct global and replicated tensor counts.
global_bytes=sum(math.prod(t['global_shape'])*t['copies']*2 for t in placement['ranks'][0]['tensors'])
assert global_bytes==placement['evidence']['official_index_bf16_bytes']==470187269120
rows=[]
for m in (1,64,8192):
 expected=F(E)*(1-F(E-k,E)**m) if m!=8192 else F(E)
 # 8192 uses the manuscript's all-experts-selected prefill assumption.
 flops=2*m*k*3*H*I;reads=expected*3*H*I*2
 compute=F(flops)/peak;memory=reads/bw;base=max(compute,memory);half=max(compute,2*memory)
 rows.append(dict(tokens=m,selected_experts=float(expected),selection='uniform independent tokens, each chooses k distinct experts' if m!=8192 else 'all 128 experts selected, manuscript prefill assumption',matrix_flops=flops,weight_read_bytes=float(reads),compute_s=float(compute),read_s=float(memory),bound='compute' if compute>memory else 'memory',call_s=float(base),half_bandwidth_read_s=float(2*memory),half_bandwidth_call_s=float(half),half_bandwidth_bound='compute' if compute>2*memory else 'memory',slowdown=float(half/base),increase_percent=float((half/base-1)*100)))
sources=['manuscripts/06-超节点.md','calculations/configs/models/qwen3-235b-a22b/config.json','calculations/configs/hardware.json','calculations/results/qwen235-placement-tp8-kv-replica.json']+['calculations/'+x['file'] for x in placement['sources']]
out=dict(exercise='6-1',kv_bytes_per_token=kv,KV=kvrows,capacity=dict(per_card_weights_bytes=weights,workspace_bytes=workspace,per_card_session_32768_bytes=per_session,max_sessions=limit,used_bytes_at_limit=max(weights)+workspace+limit*per_session,next_session_used_bytes=max(weights)+workspace+(limit+1)*per_session,free_bytes_at_limit=cap-max(weights)-workspace-limit*per_session,global_unique_weight_bytes=global_bytes,aggregate_8card_weight_bytes=sum(weights)),expert_layer=rows,scope='One-layer expert matrix/selected-weight roofline using one H100 resource rate, not full model latency, not TP8 executed throughput; capacity bound excludes extra runtime state beyond the declared workspace',source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in sources})
(P/'6-1-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
