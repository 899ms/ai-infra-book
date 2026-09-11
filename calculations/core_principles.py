#!/usr/bin/env python3
"""Recompute the cross-chapter counterfactuals from the locked Qwen3 configuration."""
from pathlib import Path
import json,hashlib,math
ROOT=Path(__file__).resolve().parents[1]
config=ROOT/'calculations/configs/models/qwen3-8b/config.json'
index=ROOT/'calculations/sources/qwen3-8b/model.safetensors.index.json'
c=json.loads(config.read_text());weights=json.loads(index.read_text())['metadata']['total_size']
w=weights-c['vocab_size']*c['hidden_size']*2
kv_per_token=2*c['num_hidden_layers']*c['num_key_value_heads']*c['head_dim']*2
k=kv_per_token*8192;workspace=2*2**30;capacity=24*10**9
assert weights==16381470720 and w==15136811008
assert kv_per_token==147456 and k==1207959552
rows=[dict(batch=b,old_hbm_read_bytes=w+b*k,new_hbm_read_bytes=b*k,memory_only_ratio=(w+b*k)/(b*k),old_per_output_bytes=w/b+k,new_per_output_bytes=k) for b in [1,16]]
result=dict(assumptions=['BF16 Qwen3-8B; no weight tying','One active dense weight scan per batch; excludes token embedding lookup, KV writes and other traffic','8192 historical positions; no prefix sharing','ROM independent and sufficiently fast; memory-only ratio is not measured end-to-end speedup','24 decimal GB, 2 GiB fixed workspace; admission is a static state bound'],sources=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [config,index]],weights_bytes=weights,active_weight_scan_bytes=w,kv_per_token_bytes=kv_per_token,kv_8k_bytes=k,batches=rows,weight_kv_crossover_8k=w/k,weight_kv_crossover_32k=w/(4*k),old_static_capacity=(capacity-workspace-weights)//k,new_static_capacity=(capacity-workspace)//k,bf16_parameter_bound_fixed_4x8k=(capacity-workspace-4*k)/2,kv_bandwidth_at_10000_tokens_per_second=k*10000,host_overlap_step_us=[max(20,100),max(20,10)],network_us={'1MB_100GBps':5+1e6/1e11*1e6,'1MB_200GBps':5+1e6/2e11*1e6,'10KB_100GBps':5+1e4/1e11*1e6,'10KB_200GBps':5+1e4/2e11*1e6},pd_instances={'before':[1,4],'after_decode_4x':[1,1]},environment_cold_prepare_s=2+2**31/(25e9/8),environment_extra_wait_s=[max(0,2+2**31/(25e9/8)-6),max(0,2+2**31/(25e9/8)-1)],task_seconds=[8+2,8/10+2,2],task_speedup=10/2.8)
assert result['old_static_capacity']==4 and result['new_static_capacity']==18
assert math.isclose(result['bf16_parameter_bound_fixed_4x8k'],8510339072)
p=ROOT/'calculations/results/core-principles.json';p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(p)
