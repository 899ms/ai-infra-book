"""Native checkpoint placement and explicit synthetic CPU expert-load scenarios."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
import hashlib,json,re
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
base=ROOT/'calculations/sources/deepseek-v4-flash';cp=ROOT/'calculations/configs/models/deepseek-v4-flash/config.json';cfg=json.loads(cp.read_text());ip=base/'model.safetensors.index.json';index=json.loads(ip.read_text())
experts=Counter();gpu=Counter();seen=set();headers=sorted((base/'headers').glob('*.json'))
for path in headers:
 for name,t in json.loads(path.read_text()).items():
  if name=='__metadata__':continue
  assert name not in seen and index['weight_map'][name]+'.json'==path.name;seen.add(name)
  size=t['data_offsets'][1]-t['data_offsets'][0]
  m=re.match(r'layers\.(\d+)\.ffn\.experts\.(\d+)\.',name)
  if m:experts[(int(m[1]),int(m[2]))]+=size
  else:gpu['shared' if '.ffn.shared_experts.' in name else 'other_attention_embeddings_norms_MTP']+=size
assert seen==set(index['weight_map'])
assert len(experts)==43*256 and len(set(experts.values()))==1
host=[sum(v for (l,e),v in experts.items() if e//128==n) for n in [0,1]]
assert sum(host)+sum(gpu.values())==index['metadata']['total_size']
param=3*cfg['hidden_size']*cfg['moe_intermediate_size'];expanded=param*2
# CPU expert execution: native packed weights stay in host; one expanded expert per NUMA worker.
# Double-buffer input/output activations, max 256 simultaneous rows, BF16.
activation=2*2*256*4096*2
host_budget=[h+expanded+activation+2**30 for h in host]
state_per_session=sum(min(9216,cfg["sliding_window"])*584+(9216//r*(584+(68 if r==4 else 0)) if r else 0) for r in cfg["compress_ratios"])
assert 128*state_per_session<=8*2**30
gpu_budget=sum(gpu.values())+activation+8*2**30+4*2**30
rows=[]
for b in [1,8,32,64,256]:
 exp=256*(1-(F(250,256))**b)
 patterns={ 'spread': [[(6*t+j)%256 for j in range(6)] for t in range(b)],'hot': [list(range(6)) for _ in range(b)]}
 for name,route in patterns.items():
  c=Counter(e for token in route for e in token);loads=[sum(n for e,n in c.items() if e//128==node) for node in [0,1]]
  assert sum(loads)==6*b
  rows.append(dict(batch=b,pattern=name,distinct_experts=len(c),per_expert_rows={str(e):c[e] for e in range(256)},NUMA_rows=loads,NUMA_native_weight_read_bytes=[sum(experts[(3,e)] for e in c if e//128==node) for node in [0,1]],busiest_nodes=[i for i,v in enumerate(loads) if v==max(loads)],uniform_independent_expected_distinct=float(exp),uniform_expected_rows_per_expert=float(F(6*b,256))))
# Conservative overload witness using only one routed layer's six hot experts.
work=9216*6*2*param;cpu=18*10**11;mu=F(cpu,work);arrival=F(1)
assert arrival>mu
out=dict(exercise='9-5',config_summary={k:cfg[k] for k in ['hidden_size','moe_intermediate_size','n_routed_experts','num_experts_per_tok','num_hidden_layers','num_hash_layers']},checkpoint_bytes=index['metadata']['total_size'],native_bytes_per_expert=next(iter(experts.values())),expert_parameters=param,expert_BF16_expansion_bytes=expanded,CPU_native_weight_bytes_by_NUMA=host,GPU_weight_bytes_by_category=dict(gpu),CPU_budget_by_NUMA=host_budget,CPU_capacity_per_NUMA=96*2**30,GPU_budget_bytes=gpu_budget,GPU_capacity_bytes=96*2**30,activation_double_buffer_bytes=activation,attention_state_9216_per_session_bytes=state_per_session,max_active_sessions=128,routing_cases=rows,overload=dict(request_input_tokens=8192,request_output_tokens=1025,processed_tokens=9216,hot_layer=3,hot_experts=list(range(6)),NUMA0_matrix_FLOPs_per_request=work,assumed_NUMA0_effective_FLOPs_s=cpu,service_upper_bound_requests_s=float(mu),arrival_requests_s=1,backlog_growth_lower_bound_requests_s=float(arrival-mu),backlog_after60_lower_bound=float(60*(arrival-mu))),scope='Capacity design and explicit synthetic routes, not a native FP4 CPU kernel implementation or measured routing distribution. CPU compute uses expanded BF16 expert; dequantization and transfer may further reduce capacity. MTP weights retained on GPU but MTP execution disabled.',source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [cp,ip,*headers,next((ROOT/'manuscripts').glob('09-*.md'))]})
assert all(v<=96*2**30 for v in host_budget) and gpu_budget<=96*2**30
(P/'9-5-results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['routing_cases','source_sha256']},indent=2))
print([(r['batch'],r['pattern'],r['distinct_experts'],r['NUMA_rows']) for r in rows])
