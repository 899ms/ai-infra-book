"""Exact current chapter-two exercise calculations; fixed manuscript inputs."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
R=Path(__file__).resolve().parent
ROOT=R.parents[2]
source=ROOT/'manuscripts/02-模型架构.md'
comparison=ROOT/'calculations/results/chapter2-model-comparison.json'
models=json.loads(comparison.read_text())['models']
L,d,f,hq,hkv,dh,vocab=36,4096,12288,32,8,128,151936
kv=2*L*hkv*dh*2
assert kv==144*1024
projection_parameters=2*d*d+2*d*hkv*dh+3*d*f

def matrix(B,S,P):
    pairs=B*(S*P+P*(P+1)//2)
    row=dict(B=B,S=S,P=P,projection_rows=B*P,causal_pairs=pairs,
        projection_and_ffn_flops=2*L*B*P*projection_parameters,
        attention_flops=4*L*hq*dh*pairs,vocab_flops=2*B*d*vocab)
    row['total_matrix_flops']=sum(row[k] for k in ['projection_and_ffn_flops','attention_flops','vocab_flops'])
    return row
full=matrix(1,0,8192);reuse=matrix(1,6144,2048)
assert full['total_matrix_flops']==next(m['prefill_matrix_flops'] for m in models if m['model_id']=='qwen3-8b')
result={}
# Explicit DAG dynamic programming checks the longest dependency chain.
dags={}
for kind in ['rnn','transformer']:
    depths={};edges=[]
    for layer in range(1,4):
        for token in range(1,5):
            node=f'L{layer}T{token}';deps=[]
            if kind=='rnn':
                if token>1:deps.append(f'L{layer}T{token-1}')
                if layer>1:deps.append(f'L{layer-1}T{token}')
            elif layer>1:deps.extend(f'L{layer-1}T{t}' for t in range(1,token+1))
            depths[node]=1+max((depths[p] for p in deps),default=0)
            edges.extend([p,node] for p in deps)
    dags[kind]=dict(depths=depths,edges=edges,longest_chain=max(depths.values()))
    lines=['flowchart LR']+[f'    {n}["layer {n[1]} / token {n[3]} / finish {t}"]' for n,t in depths.items()]
    lines += [f'    {a} --> {b}' for a,b in edges]
    lines += ['    L3T4 --> Sample["sample next token"]','    Sample --> L1T5["new position: layer 1"]']
    (R/f'{kind}-dependencies.mmd').write_text('\n'.join(lines)+'\n')
assert dags['rnn']['longest_chain']==6 and dags['transformer']['longest_chain']==3
result['2-1']=dags
result['2-2']=dict(same_rows=[matrix(4,4096,1024),matrix(1,4096,4096)],full=full,reuse=reuse,
    matrix_saving_fraction=F(full['total_matrix_flops']-reuse['total_matrix_flops'],full['total_matrix_flops']))
result['2-3']=[]
for G in [513,1025]:
    n=G-1;old=n*8192+n*(n-1)//2
    result['2-3'].append(dict(G=G,decode_calls=n,final_positions=8192+n,added_kv_bytes=n*kv,
        final_kv_bytes=(8192+n)*kv,cumulative_old_positions=old,cumulative_old_kv_read_bytes=old*kv))
result['2-4']=dict(kv_per_token_before_bytes=kv,kv_per_token_after_bytes=kv//2,
    kv_8192_after_bytes=8192*kv//2,kv_projection_parameters_per_layer_before=2*d*8*dh,
    kv_projection_parameters_per_layer_after=2*d*4*dh,interaction_flops_ratio=F(1),
    csa=[dict(context=S,saved_entries=S//4,index_scanned_entries=S//4,selected_cap=min(512,S//4)) for S in [8192,16384]])
result['2-5']=[]
for name,fixed,per in [('Qwen3.6',int(F('61.875')*2**20),20*1024),('Kimi K3',414*2**20+20348928,27*1024)]:
    result['2-5'].append(dict(model=name,fixed_bytes=fixed,per_token_bytes=per,crossing_tokens=F(fixed,per),
        context_totals={str(S):fixed+S*per for S in [32768,131072]},
        capacity_256MiB_feasible=fixed<=256*2**20,
        max_tokens_256MiB=(256*2**20-fixed)//per if fixed<=256*2**20 else None))
result['2-6']=[]
for E,width,k in [(256,512,8),(128,1024,4)]:
    for routing in ['uniform','concentrated']:
        loads=[64*k//E]*E if routing=='uniform' else [64]*k+[0]*(E-k)
        count=sum(t>0 for t in loads)
        result['2-6'].append(dict(experts=E,expert_width=width,selected=k,routing=routing,t_e=loads,
            routed_parameters=3*2048*width*E,flops=6*2048*width*sum(loads),
            accessed_experts=count,bf16_expert_read_bytes=count*3*2048*width*2))
assert len(set(r['flops'] for r in result['2-6']))==len(set(r['routed_parameters'] for r in result['2-6']))==1
result['2-6-shared']=dict(parameters=3*2048*512,flops_for_B64=6*64*2048*512,bf16_bytes=2*3*2048*512)
qweight=next(m['uniform_bf16_bytes'] for m in models if m['model_id']=='qwen3-8b')
result['2-7']=[]
for S,workspace in [(4096,2),(8192,2),(16384,2),(8192,3)]:
    free=24*10**9-qweight-workspace*2**30
    result['2-7'].append(dict(model='Qwen3-8B',weight_bytes=qweight,context=S,workspace_gib=workspace,
        remaining_bytes=free,kv_per_request_bytes=S*kv,requests=free//(S*kv)))
for S in [8192,32768]:
    free=48*10**9-39500*10**6-2*2**30
    result['2-7'].append(dict(model='70B 4bit',weight_bytes=39500*10**6,context=S,workspace_gib=2,
        remaining_bytes=free,kv_per_request_bytes=S*320*1024,requests=free//(S*320*1024)))
S,P,G=1392,51,128;n=G-1
full_prefill=matrix(1,0,1443);cached_prefill=matrix(1,S,P)
decode_pairs=sum(1443+j+1 for j in range(n))
result['2-8']=dict(S=S,P=P,G=G,decode_calls=n,final_context=S+P+n,new_kv_bytes=(P+n)*kv,
    full_prefill=full_prefill,cached_prefill=cached_prefill,
    projection_rows_saved=1392,prefill_projection_saving_fraction=F(1392,1443),
    whole_request_projection_saving_fraction=F(1392,1443+n),
    causal_pairs_saved=full_prefill['causal_pairs']-cached_prefill['causal_pairs'],
    prefill_pairs_saving_fraction=F(full_prefill['causal_pairs']-cached_prefill['causal_pairs'],full_prefill['causal_pairs']),
    whole_request_pairs_saving_fraction=F(full_prefill['causal_pairs']-cached_prefill['causal_pairs'],full_prefill['causal_pairs']+decode_pairs),
    after_edit=dict(longest_prefix_tokens=500,new_input_tokens=943))
result['2-9']=[dict(**m,total_bytes_with_workspace=m['uniform_bf16_bytes']+m['state_8192_bytes']+2*2**30,
    fits_80GB=m['uniform_bf16_bytes']+m['state_8192_bytes']+2*2**30<=80*10**9) for m in models]
result['sources']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,comparison,Path(__file__)]}
def encode(x):
    if isinstance(x,F):return dict(exact=str(x),value=float(x))
    raise TypeError(type(x).__name__)
(R/'results.json').write_text(json.dumps(result,default=encode,ensure_ascii=False,indent=2)+'\n')
print('Nine current exercise calculations and dependency graphs generated; full-prefill result agrees exactly with registered model calculation.')
