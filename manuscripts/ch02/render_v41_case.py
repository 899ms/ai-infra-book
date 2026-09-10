#!/usr/bin/env python3
"""Render source-backed V4.1 stage and matrix tables; numeric inputs are calculations results."""
from pathlib import Path
import json,re
H=Path(__file__).resolve().parent;R=H.parents[1]
load=lambda name:json.loads((R/'calculations/results'/f'{name}.json').read_text())
ced=load('v41-forward-prefill-8192-ced');ref=load('v41-forward-prefill-8192-reference');dc=load('v41-forward-decode-8192-ced')

def stages(result):
    rows=[0,0,0,0]
    for op in result['operations']:
        layer=op['layer']
        if layer is None:i=3
        elif layer<20:i=0
        elif layer==20 and (op['component']=='compressor' or op['name'].endswith('indexer.wk.weight')):i=1
        else:i=2
        rows[i]+=op['matrix_flops']
    assert sum(rows)==result['summary']['matrix_flops']
    return rows

# This is only grouping and formatting already-counted operations, not a new formula.
a,b=stages(ref),stages(ced)
stage=['**表 2-E　V4.1 Flash 的 8K 输入如何分配到执行阶段（TFLOPs）**','','| 阶段 | 参考全层前向 | CED＋末尾窗口重放 |','| --- | ---: | ---: |']
for title,x,y in zip(['20 层编码器','解码器共享全局 KV 与索引键投影','20 层解码器的查询与前馈等计算','末位置词表头'],a,b):stage.append(f'| {title} | {x/1e12:.3f} | {y/1e12:.3f} |')
stage.append(f"| 合计 | {sum(a)/1e12:.3f} | {sum(b)/1e12:.3f} |")
stage+=['','参考路径执行全部 8192 个位置的 40 层，并按公开实现先计算矩形索引分数再屏蔽；CED 路径的编码器处理全部输入，解码器全局 KV 与索引键仍为全部输入生成，解码器主体只处理末尾 128 个位置，后续索引限制在候选集合内。表中分别包含各路径的全部文本矩阵工作，差异同时来自执行位置数与索引算法。','',
'两条路径均包含注意力、路由评分、路由及共享专家、Engram 投影、Single-Pass mHC 投影和词表头。把解码器的全局投影与查询计算分开，就能看出 CED 如何缩短长提示经过的计算链。[^v41-forward]']
md=H.parent/'02-模型架构.md';s=md.read_text()
s=re.sub(r'\n\n\*\*表 2-E.*?\[\^v41-forward\]\n', '\n', s, flags=re.S)
s=re.sub(r'\n\n\*\*表 2-6.*?(?=\n\[\^)', '\n', s, flags=re.S)
s=re.sub(r'^\[\^v41-forward\]:.*\n?', '', s, flags=re.M)
start=s.index('**上下文从');end=s.index('### 2.6.2',start)
d=load('chapter2-model-comparison');rows={(x['model_id'],x['context_label']):x for x in d['long_context']}
v=rows['deepseek-v4.1-flash','1M'];v4=rows['deepseek-v4-flash','1M'];k=rows['kimi-k3','1M']
long='''**上下文从 8K 增至 1M 时的运算量与状态增长。** 长文档问答和多轮任务会放大上下文访问的成本。下面保持单请求、一次新增一个 token 和末位置词表头不变。8K 场景有 8192 个历史位置；1M 场景有 1,048,575 个历史位置，加上当前查询正好为 1,048,576 个可见位置。\n\n![五模型在 8K 与 1M 上下文下的单步矩阵运算量。](ch02/figure-2-long-context-compute.svg)\n\n*图 2-31　8K／1M 上下文下再处理一个 token 的矩阵运算量。沿用表 2-C 的执行路径，横轴为对数刻度；1M 包含当前查询。*\n\n表 2-D 单独累计当前查询的注意力评分与值汇总；V4-Flash 与 V4.1 Flash 再加入索引点积。状态列列出调用前的上下文和固定状态，精度与表 2-C 一致。[^long-context-data]\n\n**表 2-D　长上下文下的交互运算与状态容量**\n\n| 模型 | 待生成 |\n| --- | --- |\n\n'''
long+=f'''V4.1 Flash 的全局 KV 只有四份独立来源，增加上下文时不会为所有 40 层各增一份。主注意力每层最多使用 128 个局部位置和 512 个全局条目；解码器首个 Full 层生成候选集合，后续四个 Reindex 层各扫描至多 16384 个候选位置。编码器的三个索引器和解码器首个索引器仍需扫描增长的全局历史，因此计算量继续上升；跨层共享和分层索引改变了增长幅度。1M 下，其上下文交互为 {v['history_interaction_flops']/1e9:.2f} GFLOPs，完整单步矩阵工作为 {v['matrix_flops']/1e9:.2f} GFLOPs。\n\nV4-Flash 则沿用 CSA 与 HCA 的两种压缩粒度：CSA 的主注意力选择上限保持不变，但索引扫描随历史增长；HCA 会读取全部已完成的粗粒度条目。1M 下，其上下文交互为 {v4['history_interaction_flops']/1e9:.2f} GFLOPs，完整单步矩阵工作为 {v4['matrix_flops']/1e9:.2f} GFLOPs。较短上下文时，V4.1 Flash 更大的主干会增加投影和专家计算；历史足够长时，较少的索引器与分层候选选择才会抵消这部分新增工作。\n\nKimi K3 的 69 个 KDA 层保持固定递推状态，24 个 MLA 层继续访问随上下文增长的历史。紧凑 MLA 减少了缓存容量，却没有取消查询与历史位置之间的计算；1M 下，这部分交互达到 {k['history_interaction_flops']/1e9:.2f} GFLOPs，整模型达到 {k['matrix_flops']/1e9:.2f} GFLOPs。评估长上下文设计，应分别检查保存了多少状态、访问哪些位置，以及为索引和更新状态增加了多少工作。\n\n统一计算还保留了 200K 场景：V4.1 Flash 的完整单步矩阵工作为 {rows['deepseek-v4.1-flash','200K']['matrix_flops']/1e9:.2f} GFLOPs，V4-Flash 为 {rows['deepseek-v4-flash','200K']['matrix_flops']/1e9:.2f} GFLOPs。到 1M 时，两者的计算量差异进一步扩大，所以正文选用 1M 展示长上下文下的设计价值。\n\n'''
s=s[:start]+long+s[end:]
# Stage comparison follows the parameter/resource block without new figure numbers.
marker='<!-- MODEL-COMPARISON:END -->'
s=s.replace(marker,marker+'\n\n'+'\n'.join(stage),1)
# Matrix table gathers all 2-D operations from the independently checked decoder ledger.
labels={
'hc_attn_fn':'注意力 Single-Pass mHC 投影','hc_ffn_fn':'FFN Single-Pass mHC 投影',
'attn.wq_a.weight':'查询下投影','attn.wq_b.weight':'查询上投影','attn.wkv.weight':'局部 SWA KV 投影',
'attn.wo_a.weight':'分组输出投影','attn.wo_b.weight':'输出拼接投影',
'attn.compressor.wkv.weight':'全局 KV 投影','attn.compressor.wgate.weight':'2:1 压缩门控',
'attn.indexer.wk.weight':'全局索引键投影','attn.indexer.wq_b.weight':'索引查询投影',
'attn.indexer.weights_proj.weight':'索引头权重投影','ffn.gate.weight':'路由评分',
'ffn.shared_experts.w1.weight':'共享专家 gate','ffn.shared_experts.w3.weight':'共享专家 up','ffn.shared_experts.w2.weight':'共享专家 down',
'ffn.experts.0.w1.weight':'路由专家 gate','ffn.experts.0.w3.weight':'路由专家 up','ffn.experts.0.w2.weight':'路由专家 down',
'engram.wkv.weight':'Engram 查询结果的 KV 投影','head.weight':'末位置词表头'}
buckets={}
for op in dc['operations']:
 if 'weight_math' not in op:continue
 key=re.sub(r'^layers\.\d+\.','',op['name']);buckets.setdefault(key,[]).append(op)
table=['**表 2-6　DeepSeek V4.1 Flash：CED、共享上下文与 Engram**','',
'本表覆盖普通文本生成的全部矩阵投影。输入行数 $m_l$ 表示第 $l$ 层本次处理的查询位置数；$u_l$ 表示需要生成全局 KV 的位置数，$c_l$ 表示本次新完成的压缩条目数。参考全层 prefill 中 $m_l=P$；CED 中编码器 $m_l=P$、解码器 $m_l=\\min(P,128)$，但解码器全局 KV 来源层仍有 $u_{20}=P$。所有行数还需乘请求数 $B$。','',
'| 模块及作用 | 权重矩阵（输入宽 × 输出宽） | 执行行数 | 层／调用数 |','| --- | --- | --- | ---: |']
for key,ops in buckets.items():
 iw,ow=ops[0]['weight_math'];rows='$m_l$'
 if key.startswith('attn.compressor.'):rows='$u_l$'
 if key=='attn.indexer.wk.weight':rows='$c_l$'
 if key.startswith('ffn.experts.'):rows='$\\sum_e t_e=6m_l$'
 if key=='head.weight':rows='末位置一次'
 shape=f'${iw}\\times{ow}$'
 if key=='attn.wo_a.weight':
  # Stored output is 8 groups. Display each block to avoid implying a dense group cross-product.
  shape=f'${iw}\\times{ow//8}$，共 8 组'
 table.append(f'| {labels[key]} | {shape} | {rows} | {len(ops)} |')
table+=['',
'每个二维投影的矩阵运算量为输入行数乘输入宽、输出宽，再乘 2；分组输出投影只在各组内部运算，不能把组间不存在的连接计入。路由专家的三行按各专家接收的行数相加，共享专家处理全部查询位置。','',
'注意力交互没有新增权重：每个查询有 64 个头、每头 512 维，QK 与 PV 共同按实际访问位置累计。索引器有 32 个头、每头 128 维，Full、Reindex、Reuse 的扫描范围和是否执行索引各不相同。压缩器仅在相应块完成后产生索引键，不能把键投影的行数写成每次输入的位置数。','',
'Engram 首先从 n-gram 对应的 24 个桶各取一个 256 维向量，拼成 6144 维输入，再经表中的投影形成四路键和一个共享值；归一化点积与门控将其写入四路残差。查表不计作矩阵乘法，读取载荷、门控和加权归约分别列在计算记录中。最后的 mHC 加权汇合与 RMSNorm 不引入另一份词表权重。[^v41-forward]','']
foot=s.index('\n[^',s.index('**表 2-5'))
s=s[:foot]+'\n\n'+'\n'.join(table)+s[foot:]
s+='\n[^v41-forward]: [V4.1 Flash 完整文本矩阵计算实现](../calculations/src/infra_calc/topics/v41_forward.py)；[CED 8K 输入](../calculations/results/v41-forward-prefill-8192-ced.md)、[参考全层输入](../calculations/results/v41-forward-prefill-8192-reference.md)、[8K decode](../calculations/results/v41-forward-decode-8192-ced.md)、[1M decode](../calculations/results/v41-forward-decode-1m-ced.md)。[计算与复核记录](../research/ch02-five-models-2026-09-10/README.md)。\n'
md.write_text(s)
print('Rendered V4.1 stage breakdown, module matrix table and 1M discussion.')
