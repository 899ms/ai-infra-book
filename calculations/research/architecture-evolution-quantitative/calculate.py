"""Chapter 4: fixed work, documented resources, component service times.

Run from any directory. No generated throughput is a device measurement.
"""
from pathlib import Path
import json, hashlib, math
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent

def read(p): return json.loads((ROOT/p).read_text())

def calculate():
    hw=read('calculations/configs/hardware.json')
    devices={d['id']:d for d in hw['devices']}
    # Official GA102 whitepaper Table 9: first of dense/sparse pairs.
    devices['rtx3090']={'id':'rtx3090','name':'RTX 3090 FE','memory':{'nominal_capacity':24,'bandwidth_bytes_per_second':936e9},'peak_rates':[{'input_precision':'BF16','accumulator_precision':'FP32','execution_unit':'tensor','sparsity':'dense','tera_ops_per_second':71}], 'source':'sources/nvidia-ampere-ga102.pdf, Table 9'}
    selected=['rtx3090','rtx4090','rtx5090','rtx-pro6000-blackwell-ws','a100-80gb-sxm','h100-sxm','h200-sxm','ascend-950pr-max-spec','ascend-950dt-max-spec','m1-ultra-64gpu-128gb','m2-ultra-76gpu-192gb','m3-ultra-80gpu-256gb','m3-ultra-80gpu-512gb','m4-max-40gpu-128gb','m5-ultra-80gpu-512gb']
    profiles=[]
    for id in selected:
        d=devices[id];rates=[r['tera_ops_per_second'] for r in d['peak_rates'] if r['input_precision']=='BF16' and r['accumulator_precision']=='FP32' and r['sparsity']=='dense' and r['execution_unit']=='tensor']
        profiles.append({'id':id,'name':d['name'],'capacity_gb':d['memory']['nominal_capacity'],'bandwidth_gbs':d['memory']['bandwidth_bytes_per_second']/1e9,'bf16_fp32_dense_tflops':rates[0] if rates else None})
    cfg=read('calculations/configs/models/qwen3-8b/config.json')
    H,I,L,Nh,Nkv,D=(cfg[k] for k in ['hidden_size','intermediate_size','num_hidden_layers','num_attention_heads','num_key_value_heads','head_dim'])
    linear_per_token=2*L*(2*H*(Nh*D)+2*H*(Nkv*D)+3*H*I)
    lm_head=2*H*cfg['vocab_size']
    decode_flops=linear_per_token+4*L*Nh*8192*D+lm_head
    S=4096
    prefill_flops=linear_per_token*S+2*L*Nh*D*S*(S+1)+lm_head
    projection=[]
    for p in profiles:
        if p['bf16_fp32_dense_tflops'] is None:continue
        for m in [1,256,4096]:
            f=2*m*H**2;v=2*(H**2+2*m*H)
            tc=f/(p['bf16_fp32_dense_tflops']*1e12);tm=v/(p['bandwidth_gbs']*1e9)
            projection.append({'device':p['id'],'rows':m,'flops':f,'bytes':v,'compute_us':tc*1e6,'memory_us':tm*1e6,'resource_floor_us':max(tc,tm)*1e6})
    storage=read('calculations/results/storage-generation-qwen8-235.json')
    ids=['qwen3-8b-b1-h8191-w16-balanced','qwen3-8b-b8-h8191-w16-balanced','qwen3-8b-b1-h32767-w4-balanced','qwen3-235b-a22b-b1-h8191-w4-balanced','qwen3-235b-a22b-b8-h8191-w4-balanced','qwen3-235b-a22b-b8-h8191-w4-concentrated']
    works=[{k:v for k,v in w.items() if k not in ['tensors','sources','expert_counts']} for w in storage['workloads'] if w['id'] in ids]
    decode=[]
    for w in works:
        for p in profiles:
            t=w['accounted_payload_bytes']/(p['bandwidth_gbs']*1e9)
            decode.append({'workload':w['id'],'device':p['id'],'resident_gb':w['resident_budget_bytes']/1e9,'payload_gb':w['accounted_payload_bytes']/1e9,'fits_nominal':w['resident_budget_bytes']<=p['capacity_gb']*1e9,'read_ms':t*1e3,'io_token_ceiling':w['batch']/t,'headroom_gb':p['capacity_gb']-w['resident_budget_bytes']/1e9})
    qwen=[]
    for p in profiles:
        rate=p['bf16_fp32_dense_tflops']
        qwen.append({'device':p['id'],'decode_matrix_ms':decode_flops/(rate*1e12)*1e3 if rate else None,'prefill_matrix_ms':prefill_flops/(rate*1e12)*1e3 if rate else None})
    # V100 SXM2, same FP16 operands and FP32 accumulator; traditional path
    # promotes operands into FP32 registers and uses ordinary FP32 FMA.
    volta=[]
    for m in [1,4096]:
        f=2*m*H**2;v=2*(H**2+2*m*H)
        for kind,rate in [('FP32 FMA',15.7),('Tensor Core',125)]:
            volta.append({'rows':m,'path':kind,'compute_ms':f/(rate*1e12)*1e3,'memory_ms':v/900e9*1e3,'resource_floor_ms':max(f/(rate*1e12),v/900e9)*1e3})
    # Spatial 3x3 stride-1, same padding, 56x56, Cin=Cout=64, batch=1.
    pixels=56*56;elems=pixels*64;expanded=elems*9*2
    conv={'input_bytes':elems*2,'expanded_bytes':expanded,'explicit_expansion_roundtrip_bytes':expanded*2,'flops':2*pixels*64*64*9,'cube_cycles_at_8192':2*pixels*64*64*9/8192,'relu_elements':elems,'fp16_vector_issues_at_128_lanes':math.ceil(elems/128),'saved_hbm_service_us_at_1_2TBs':expanded*2/1.2e12*1e6}
    # 128x128 score tile, d=128. Lane width gives instruction groups,
    # NOT exponential instruction latency or throughput.
    n=128;attention={'score_elements':n*n,'matrix_flops':4*n**3,'cube_cycles_at_8192':4*n**3/8192,'fp32_vector_lanes':256//4,'exp_vector_groups':n*n//(256//4),'fp32_one_tensor_bytes':n*n*4,'two_handoffs_external_roundtrip_bytes':4*n*n*4,'external_service_us_at_94GBs':4*n*n*4/94e9*1e6,'fp16_one_handoff_bytes':n*n*2,'required_cv_GBs_for_two_handoffs_in_1_024us':2*n*n*4/(1.024e-6)/1e9,'required_external_GBs_in_1_024us':4*n*n*4/(1.024e-6)/1e9,'required_exp_values_per_cycle':n*n/(4*n**3/8192),'required_exp_vector_issues_per_cycle':(n*n//64)/(4*n**3/8192)}
    # One-variable sensitivity from the chapter's resource-balance model.
    matrix_vector=[{'label':label,'matrix_cycles':mc,'exp_cycles':ex,'memory_cycles':sm,'interval_cycles':max(mc,ex,sm)} for label,mc,ex,sm in [('基线',1024,1024,768),('仅矩阵 ×2',512,1024,768),('再增加指数 ×2',512,512,768),('三项 ×2',512,512,384)]]
    # Same BF16 matrix storage vs MXFP8/MXFP4 blocks of 32, one scale byte.
    formats=[]
    for name,bits,scale in [('BF16',16,0),('MXFP8',8,1),('MXFP4',4,1)]:
        size=H*H*bits//8+H*H//32*scale
        formats.append({'format':name,'bytes':size,'MiB':size/2**20,'read_us_4090':size/1008e9*1e6,'read_us_5090':size/1792e9*1e6})
    sources=['calculations/configs/hardware.json','calculations/configs/models/qwen3-8b/config.json','calculations/results/storage-generation-qwen8-235.json','references/text/ascend-davinci.txt','references/text/ascend-950-official.txt','references/text/nvidia-v100.txt','references/author-materials/2026-09-09/network-intelligence.md',str((HERE/'sources/nvidia-ampere-ga102.pdf').relative_to(ROOT))]
    return {'schema_version':1,'profiles':profiles,'projection':projection,'volta':volta,'qwen_work':{'linear_flops_per_token':linear_per_token,'decode_8k_matrix_flops':decode_flops,'prefill_4k_causal_matrix_flops':prefill_flops,'lm_head_policy':'last position only for prefill; one output token for decode'},'qwen_compute':qwen,'workloads':works,'decode':decode,'conv':conv,'ascend_attention':attention,'resource_sensitivity':matrix_vector,'formats':formats,'numerics':{'FP16':{'min_normal':2**-14,'min_subnormal':2**-24,'spacing_at_one':2**-10},'BF16':{'min_normal':2**-126,'min_subnormal':2**-133,'spacing_at_one':2**-7}},'interconnect':{'payload_bytes':64*2**20,'a100_one_way_GBs':300,'h100_one_way_GBs':450,'a100_us':64*2**20/300e9*1e6,'h100_us':64*2**20/450e9*1e6},'sources':[{'path':p,'sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} for p in sources],'contracts':['BF16 input FP32 accumulator dense matrix rates only; unknown Apple/Ascend comparable rates remain null.','All expert weights reside; active-expert reads depend on routing. Existing storage-generation model supplies exact payload and workspace.','Time=bytes/bandwidth and FLOPs/peak are service floors, not measured end-to-end latency. Capacity uses nominal decimal GB; headroom is separately visible.','Ascend vector width is not an instruction throughput. Compute issue requirements, never infer exp cycles from width.','94GB/s is the early paper per-core LLC allocation. CV calculation is an interface substitution exercise, not a measured 910A-to-950 speedup.','M5 Ultra profiles are announced specifications as of 2026-09-10, not measured retail devices.']}

if __name__=='__main__':
    result=calculate()
    (HERE/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['qwen_work','conv','ascend_attention','volta','formats']},ensure_ascii=False,indent=2))
    print('device / decode read ms / prefill matrix ms')
    for p in result['profiles']:
        d=next(r for r in result['decode'] if r['device']==p['id'] and r['workload']=='qwen3-8b-b1-h8191-w16-balanced');c=next(r for r in result['qwen_compute'] if r['device']==p['id'])
        print(p['id'],round(d['read_ms'],3),round(c['prefill_matrix_ms'],2) if c['prefill_matrix_ms'] else None)
