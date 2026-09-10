"""Five chapter-2 models under common call shapes, using architecture adapters."""
from pathlib import Path
import hashlib
from ..models import forward
from ..schema import Scenario
from ..sources import model_config
from . import qwen36_forward, v4_forward, k3_forward, state, v41_forward

MODELS=('deepseek-v4.1-flash','qwen3-8b','qwen3.6-35b-a3b','deepseek-v4-flash','kimi-k3')
LABELS=('V4.1 Flash','Qwen3-8B','Qwen3.6','V4-Flash','Kimi K3（紧凑 MLA）')


def call(model,tokens,history=0):
    if model==MODELS[0]:return v41_forward.calculate(tokens=tokens,history=history)
    if model=='qwen3-8b':return forward(model,Scenario(tokens=tokens,history=history))
    if model=='qwen3.6-35b-a3b':return qwen36_forward.calculate(tokens=tokens,history=history,output_head='last')
    if model=='deepseek-v4-flash':return v4_forward.calculate(model,tokens=tokens,history=history)
    return k3_forward.calculate(tokens=tokens,history=history,mla_path='compact',output_head='last')


def matrix(r):
    return r['summary'].get('matrix_flops',r['summary'].get('matrix_flops_effective_attention'))


def groups(model,r):
    if model==MODELS[0]:return r['parameter_groups']
    if model=='qwen3-8b':
        total=r['summary']['parameters'];p=[2*151936*4096,36*(2*4096**2+2*4096*1024),36*3*4096*12288,0]
    elif model=='qwen3.6-35b-a3b':
        total=r['summary']['base_text_parameters']
        p=[2*248320*2048,sum(w['parameters'] for w in r['weights'] if ('.self_attn.' in w['name'] or '.linear_attn.' in w['name']) and len(w['shape'])==2),40*3*2048*512,40*256*3*2048*512]
    elif model=='deepseek-v4-flash':
        total=r['summary']['logical_parameters_excluding_mtp_and_quant_scales'];a=r['parameter_components']
        p=[a['embedding']+a['vocabulary_head'],a['attention_matrices'],43*3*4096*2048,43*256*3*4096*2048]
    else:
        total=r['summary']['logical_text_parameters'];a=r['parameter_components']
        p=[a['embedding']+a['vocabulary_head'],a['mla_matrices']+a['kda_projections'],3*7168*33792+92*3*7168*6144,92*896*3*3584*3072]
    result=dict(zip(('embedding_head','attention_projection','dense_shared_ffn','routed_experts'),p))
    result.update(engram=0,other=total-sum(p))
    assert result['other']>=0
    return result


def state_bytes(model,length):
    if model==MODELS[0]:return v41_forward.state(length)['resident_bytes']
    if model=='qwen3.6-35b-a3b':
        if length>model_config(model)['text_config']['max_position_embeddings']:
            anchor=state_bytes(model,8192)
            return anchor+20*1024*(length-8192)
        r=qwen36_forward.calculate(tokens=1,history=length-1,output_head='last')
        return sum(r['state'][k] for k in ('full_kv_after_bytes','linear_recurrent_fp32_bytes','linear_conv_slot_bytes'))
    if model=='qwen3-8b' and length>32768:
        # Explicit architecture extrapolation, preserving the previous chapter contract.
        return state.calculate(model,8192)['summary']['kv_bytes_per_token_per_request']*length
    return state.calculate(model,length,mla_path='compact')['summary']['resident_bytes']


def interaction(model,r,history):
    if model==MODELS[0]:return r['summary']['context_interaction_flops']
    if model=='qwen3-8b':return 36*4*32*128*(history+1)
    if model=='qwen3.6-35b-a3b':return 10*4*16*256*(history+1)
    if model=='deepseek-v4-flash':
        a=r['components']['attention']['summary']
        return a['effective_qk_pv_matrix_flops']+a['reference_index_matrix_flops']
    return 24*2*96*(576+512)*(history+1)


def calculate():
    models=[];long=[];requests=[];sources={}
    routes=(40*6*3*5120*2304,0,40*8*3*2048*512,43*6*3*4096*2048,92*16*3*3584*3072)
    for model,label,route in zip(MODELS,LABELS,routes):
        pf=call(model,8192);dc=call(model,1,8192);pg=groups(model,pf)
        models.append(dict(model=label,model_id=model,total_parameters=sum(pg.values()),
                           parameter_groups=pg,uniform_bf16_bytes=2*sum(pg.values()),
                           prefill_matrix_flops=matrix(pf),decode_matrix_flops=matrix(dc),
                           state_8192_bytes=state_bytes(model,8192),selected_routed_expert_bf16_bytes=2*route))
        sources[model]=pf['sources']
        for history in (8192,204800,1048575):
            config=model_config(model);limit=config.get('text_config',config)['max_position_embeddings']
            extrapolate=history+1>limit
            r=dc if history==8192 or extrapolate else call(model,1,history)
            total=matrix(r)
            if extrapolate:
                slope=36*4*32*128 if model=='qwen3-8b' else 10*4*16*256
                total+=slope*(history-8192)
            cross=interaction(model,r,history)
            long.append(dict(model=label,model_id=model,history=history,visible_positions=history+1,
                             context_label={8192:'8K',204800:'200K',1048575:'1M'}[history],
                             extrapolated=extrapolate,pinned_context_limit=limit,matrix_flops=total,
                             history_interaction_flops=cross,other_matrix_flops=total-cross,
                             state_bytes=state_bytes(model,history)))
        calls=[dict(tokens=128,history=0,matrix_flops=matrix(call(model,128)))]
        calls += [dict(tokens=1,history=h,matrix_flops=matrix(call(model,1,h))) for h in (128,129,130)]
        requests.append(dict(model=label,model_id=model,calls=calls,matrix_flops=sum(x['matrix_flops'] for x in calls),
                             final_retained_positions=131))
    long.sort(key=lambda r:(r['history'],MODELS.index(r['model_id'])))
    for short,large,row in zip(long[:5],long[5:10],models):
        assert short['matrix_flops']==row['decode_matrix_flops']
        assert short['state_bytes']==row['state_8192_bytes']
        # Both lengths end on the same compressor phase for the next token.
        assert short['other_matrix_flops']==large['other_matrix_flops']
    lengths=[8192,16384,32768,65536,131072,262144,524288,1048576]
    curves={'lengths':lengths,'resident_bytes':{},'accounted_access_bytes':{}}
    for model in MODELS:
        curves['resident_bytes'][model]=[state_bytes(model,n) for n in lengths]
        access=[]
        for n in lengths:
            if model==MODELS[0]:value=v41_forward.state(n)['selected_history_payload_bytes']
            elif model=='qwen3-8b':value=147456*n
            elif model=='qwen3.6-35b-a3b':value=20*1024*n+120*2**20
            else:
                cache=state.calculate(model,n,mla_path='compact')['summary']
                value=cache['selected_history_payload_bytes']+cache.get('recurrent_read_once_write_once_bytes',0)
            access.append(value)
        curves['accounted_access_bytes'][model]=access
    context_rows={(r['model_id'],r['context_label']):r for r in long}
    insights={}
    for model in (MODELS[0],'deepseek-v4-flash','kimi-k3'):
        medium=context_rows[model,'200K'];large=context_rows[model,'1M']
        insights[model]={'matrix_growth_200k_to_1m':large['matrix_flops']/medium['matrix_flops']}
    insights['v4_to_v41_matrix_ratio_1m']=context_rows['deepseek-v4-flash','1M']['matrix_flops']/context_rows[MODELS[0],'1M']['matrix_flops']
    insights['v4_full_attention_hypothetical_1m_flops']=43*4*64*512*1048576
    insights['v4_interaction_reduction_1m']=insights['v4_full_attention_hypothetical_1m_flops']/context_rows['deepseek-v4-flash','1M']['history_interaction_flops']
    root=Path(__file__).resolve().parents[1]
    return dict(calculation='chapter2-models',context_insights=insights,state_curves=curves,models=models,long_context=long,requests=requests,sources=sources,
                parameter_group_order=['embedding_head','attention_projection','dense_shared_ffn','routed_experts','engram','other'],
                calculator_sha256={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*.py'))},
                scope='Text only; full effective matrix graph, last-position vocabulary head; V4.1 CED/candidate, Qwen causal, Qwen3.6 eager/chunk, V4 effective sparse/reference index, K3 compact MLA/chunk prefill/recurrent decode; not latency.',
                long_context_scope='8K/200K mean 8192/204800 prior positions; 1M means 1048575 prior positions plus the current query, exactly the 1048576 supported limit. Qwen3-8B beyond 40960 and Qwen3.6 beyond 262144 are explicit formula extrapolations, never runnable or quality claims.',
                request_scope='All five use P128,G4,B1,S0 and the SAME paths as the 8K comparison; prefill produces first output, three decode calls retain 131 positions.')
