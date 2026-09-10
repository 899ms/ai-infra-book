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
for x in rows:lines.append('| '+x['model']+' | '+' | '.join(('$<0.001$' if 0<z<500000 else f'{z/1e9:.3f}') for z in x['parameter_groups']+[x['total_parameters']])+' |')
lines+=['','其他包含 router、潜空间进出投影、归一化、卷积和连接等参数；注意力投影包括 V4 的压缩与索引投影。Qwen3-8B 的主要参数集中在每个 token 都执行的稠密 FFN，三个 MoE 模型则将大部分参数放进路由专家。Qwen3.6 的路由专家占约 93%，V4 与 K3 约为 97%—98%。因此，它们的总容量主要由专家集合决定，单 token 的专家运算量则取决于每层选中的专家。','','**表 2-C　相同输入条件下的计算与状态**','','| 模型 | 统一 BF16 权重（GB） | 8K prefill（TFLOPs） | 8K 历史单步 decode（GFLOPs） | 8K 状态（MiB） | 单 token 选中路由专家的 BF16 权重（GiB） |','| --- | ---: | ---: | ---: | ---: | ---: |']
for x in rows:lines.append(f"| {x['model']} | {x['uniform_bf16_bytes']/1e9:.2f} | {x['prefill_matrix_flops']/1e12:.2f} | {x['decode_matrix_flops']/1e9:.2f} | {x['state_8192_bytes']/2**20:.2f} | "+(f"{x['selected_routed_expert_bf16_bytes']/2**30:.3f}" if x['selected_routed_expert_bf16_bytes'] else '—')+' |')
lines+=['', '两种调用均取 $B=1$，prefill 为 $S=0,P=8192$，decode 为 $S=8192,P=1$，词表头均只处理末位置。状态列列出保存 8192 个历史位置所需的空间：历史表示采用 BF16，递推状态和压缩缓冲按相应实现采用 FP32。最后一列将一个 token 在各层选中的路由专家权重相加，再按 BF16 换算为字节数。由此可以分别比较完整模型占用的空间、一次调用的运算量，以及请求历史占用的空间。', '', '各模型按自己的执行路径累计：Qwen3-8B 为有效因果注意力，Qwen3.6 为 eager 矩形注意力与块式线性分支，V4 为有效主注意力及参考索引，K3 为紧凑 MLA 与块式 KDA。Qwen3.6 保存的权重约为 Qwen3-8B 的四倍，单步矩阵运算量却更少；V4 权重继续扩大，8K 状态反而因压缩与选择缩小；K3 拥有更多专家，隐藏维度更大、层数也更多，因此需要保存更多权重，完成更多运算。这些差异说明，总参数量、单次运算量和历史状态大小需要根据各自对应的结构分别计算。', '', '**从保存量继续推到访问量。** Qwen3-8B 每步使用 1152 MiB 旧 KV；V4 的主历史选择与索引扫描合计 27.625 MiB，并更新压缩器。K3 紧凑 MLA 使用 216 MiB 历史，414 MiB 递推矩阵还要一读一写，读写量合计 828 MiB；Qwen3.6 对应 160 MiB 全局历史和 120 MiB 递推矩阵读写。递推状态每步都要读出并更新，历史表示则要供当前查询使用。因此，即使状态大小固定，每步也仍有相应的读写开销。', '', '**从参数转到存储格式。** 统一按 BF16 计算时，每个参数占 2 字节，权重大小可以直接反映参数量的差异。实际发布的 checkpoint 使用各自的存储格式，V4 主干约为 156.02 GB，K3 文本约为 1559.97 GB。文件大小由低位宽矩阵、保留较高精度的参数以及格式元数据共同决定。模型加载后，还需要为格式转换和计算分配空间。第五章将分析存储格式与运行时实现如何影响显存占用。', '', '表 2-B 的参数组成解释了权重容量，表 2-C 则展示这些参数怎样参与一次调用。二者结合起来，可以区分“模型能容纳多少参数”与“处理一个 token 要使用多少资源”。[^comparison-data]']
import sys
sys.path.insert(0,str(H.parent))
from math_style import normalize
lines=normalize('\n'.join(lines),2).splitlines()
(H/'model-comparison.md').write_text('\n'.join(lines)+'\n')
(H/'model-comparison.json').write_text(json.dumps({'scope':'B1, prefill P8192 S0 / decode P1 S8192; head last; per-model algorithm as documented','parameter_group_order':['embedding_head','attention_projection','dense_shared_ffn','routed_experts','other'],'sources':inputs,'models':rows},ensure_ascii=False,indent=2)+'\n')
p=H.parent/'02-模型架构.md';s=p.read_text();a='<!-- MODEL-COMPARISON:START -->';b='<!-- MODEL-COMPARISON:END -->';block=a+'\n\n'+'\n'.join(lines)+'\n\n'+b+'\n\n'
if a in s:s=s[:s.index(a)]+block+s[s.index(b)+len(b):].lstrip('\n')
else:s=s.replace('### 2.6.2',block+'### 2.6.2',1)
p.write_text(s)
print([(x['model'],round(x['prefill_matrix_flops']/1e12,2),round(x['decode_matrix_flops']/1e9,2)) for x in rows])
