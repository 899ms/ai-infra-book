#!/usr/bin/env python3
"""Build chapter comparison tables from pinned results; no runtime performance inference."""
from pathlib import Path
import json, hashlib
H=Path(__file__).resolve().parent; R=H.parents[1]; inputs=[]
def load(name,local=False):
 p=(H if local else R/'calculations/results')/(name+'.json');inputs.append({'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()});return json.loads(p.read_text())
q=load('qwen3-8b-prefill-8192');q36=load('qwen36-prefill-last-head');v=load('forward-deepseek-v4-flash-b1-t8192-s0');k=load('forward-kimi-k3-b1-t8192-s0-compact')
qd=load('qwen3-8b-decode-b1-s8192');q36d=load('qwen36-decode-b1');vd=load('comparison-v4-decode',True);kd=load('forward-kimi-k3-b1-t1-s8192-compact')
vs=load('state-deepseek-v4-flash-n8192-b1-native');ks=load('state-kimi-k3-n8192-b1-compact')
# Disjoint buckets conserve total logical parameters. Tiny norms remain in Other.
qtotal=q['summary']['parameters'];qt=q36['summary']['base_text_parameters'];vt=v['summary']['logical_parameters_excluding_mtp_and_quant_scales'];kt=k['summary']['logical_text_parameters']
qparts=[2*151936*4096,36*(2*4096**2+2*4096*1024),36*3*4096*12288,0]
q36parts=[2*248320*2048,sum(w['parameters'] for w in q36['weights'] if ('.self_attn.' in w['name'] or '.linear_attn.' in w['name']) and len(w['shape'])==2),40*3*2048*512,40*256*3*2048*512]
vp=v['parameter_components'];vparts=[vp['embedding']+vp['vocabulary_head'],vp['attention_matrices'],43*3*4096*2048,43*256*3*4096*2048]
kp=k['parameter_components'];kparts=[kp['embedding']+kp['vocabulary_head'],kp['mla_matrices']+kp['kda_projections'],3*7168*33792+92*3*7168*6144,92*896*3*3584*3072]
rows=[]
for name,total,parts,pf,dc,state,route in zip(['Qwen3-8B','Qwen3.6','V4-Flash','K3（紧凑 MLA）'],[qtotal,qt,vt,kt],[qparts,q36parts,vparts,kparts],[q['summary']['matrix_flops'],q36['summary']['matrix_flops'],v['summary']['matrix_flops_effective_attention'],k['summary']['matrix_flops']],[qd['summary']['matrix_flops'],q36d['summary']['matrix_flops'],vd['summary']['matrix_flops_effective_attention'],kd['summary']['matrix_flops']],[qd['summary']['kv_resident_before_bytes'],sum(q36['state'][z] for z in ['full_kv_after_bytes','linear_recurrent_fp32_bytes','linear_conv_slot_bytes']),vs['summary']['resident_bytes'],ks['summary']['resident_bytes']],[0,40*8*3*2048*512,43*6*3*4096*2048,92*16*3*3584*3072]):
 other=total-sum(parts);assert other>=0
 rows.append(dict(model=name,total_parameters=total,parameter_groups=parts+[other],uniform_bf16_bytes=2*total,prefill_matrix_flops=pf,decode_matrix_flops=dc,state_8192_bytes=state,selected_routed_expert_bf16_bytes=2*route))
assert all(sum(x['parameter_groups'])==x['total_parameters'] for x in rows)
lines=['**表 2-B　参数由哪些部分构成（单位：十亿个逻辑参数）**','','| 模型 | 嵌入与输出头 | 注意力投影 | 稠密／共享 FFN | 路由专家 | 其他 | 合计 |','| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
for x in rows:lines.append('| '+x['model']+' | '+' | '.join(('<0.001' if 0<z<500000 else f'{z/1e9:.3f}') for z in x['parameter_groups']+[x['total_parameters']])+' |')
lines+=['','其他包含 router、潜空间进出投影、归一化、卷积和连接等未进入前四栏的参数；注意力投影包含 V4 压缩与索引投影。分项按整数守恒累计，显示取整可能使末位和不同。路由专家构成三个 MoE 模型的大部分参数，而单 token 只使用其中一部分。','','**表 2-C　相同输入条件下的计算与状态**','','| 模型 | 统一 BF16 权重（GB） | 8K prefill（TFLOPs） | 8K 历史单步 decode（GFLOPs） | 8K 状态（MiB） | 单 token 选中路由专家 BF16 载荷（GiB） |','| --- | ---: | ---: | ---: | ---: | ---: |']
for x in rows:lines.append(f"| {x['model']} | {x['uniform_bf16_bytes']/1e9:.2f} | {x['prefill_matrix_flops']/1e12:.2f} | {x['decode_matrix_flops']/1e9:.2f} | {x['state_8192_bytes']/2**20:.2f} | "+(f"{x['selected_routed_expert_bf16_bytes']/2**30:.3f}" if x['selected_routed_expert_bf16_bytes'] else '—')+' |')
lines+=['', '两种调用均取 $B=1$，prefill 为 $S=0,P=8192$，decode 为 $S=8192,P=1$，都只执行末位置词表头。状态取调用前已有 8192 位置；GQA／MLA 与历史表示采用 BF16，递推和压缩缓冲采用所列 FP32。工作区、并行复制与实际 HBM 流量另计。最后一列只含选中的路由专家，在理想每专家读取一次的统一 BF16 格式下计量，不是完整模型每步权重读取。', '', '计算口径仍需逐模型阅读：Qwen3-8B 使用有效因果注意力，Qwen3.6 使用 eager 矩形注意力与块式线性分支，V4 使用有效主注意力及参考索引，K3 使用紧凑 MLA 与块式 KDA。对齐调用与输出头并未使这些算法工作完全等价；矩阵 FLOPs、普通算术和特殊函数继续分开，不由此推断速度排名。', '', '**状态访问另算。** 同一份 8K 历史，Qwen3-8B 的旧 KV 唯一载荷为 1152 MiB；V4 选中主历史与索引合计 27.625 MiB，另有压缩器更新；K3 紧凑 MLA 为 216 MiB，递推矩阵另需理想读写 828 MiB，卷积等继续另计。Qwen3.6 的全局历史为 160 MiB，递推矩阵理想读写为 120 MiB。这里列出不同状态机制的分项，不能将其与算子接口读写直接相加作为 HBM 总量。', '', '**格式再比较。** 统一 BF16 让读者看到结构规模，发布文件则有自己的格式。V4 基础主干 checkpoint 约 156.02 GB，K3 文本 checkpoint 约 1559.97 GB，包含各自存储格式；K3 还保留已知配置／checkpoint 形状差异。文件载荷不等于运行时分配，不能和上一表混成显存或性能排名。', '', '表 2-B、2-C 的逐项整数、来源与复算见[四模型比较数据](ch02/model-comparison.json)和[生成程序](ch02/compare_models.py)。Qwen3.6 使用[末位置输出头结果](../calculations/results/qwen36-prefill-last-head.md)，V4 单步由相同公共计算入口生成；完整算子与 checkpoint 范围仍以对应模型表的结果链接为准。']
(H/'model-comparison.md').write_text('\n'.join(lines)+'\n')
(H/'model-comparison.json').write_text(json.dumps({'scope':'B1, prefill P8192 S0 / decode P1 S8192; head last; per-model algorithm as documented','parameter_group_order':['embedding_head','attention_projection','dense_shared_ffn','routed_experts','other'],'sources':inputs,'models':rows},ensure_ascii=False,indent=2)+'\n')
p=H.parent/'02-模型架构.md';s=p.read_text();a='<!-- MODEL-COMPARISON:START -->';b='<!-- MODEL-COMPARISON:END -->';block=a+'\n\n'+'\n'.join(lines)+'\n\n'+b+'\n\n'
if a in s:s=s[:s.index(a)]+block+s[s.index(b)+len(b):].lstrip('\n')
else:s=s.replace('### 2.6.2',block+'### 2.6.2',1)
p.write_text(s)
print([(x['model'],round(x['prefill_matrix_flops']/1e12,2),round(x['decode_matrix_flops']/1e9,2)) for x in rows])
