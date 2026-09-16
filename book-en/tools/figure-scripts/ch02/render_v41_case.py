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
stage=["**Table 2-D  How V4.1 Flash's 8K Input Is Allocated to Execution Stages (TFLOPs)**",'',"| Stage | Reference Full-Layer Forward | CED + Tail-Window Replay |",'| --- | ---: | ---: |']
for title,x,y in zip(["20-layer encoder","decoder shares global KV and index key projection","20-layer decoder query and feedforward computation","tail-token vocab head"],a,b):stage.append(f'| {title} | {x/1e12:.3f} | {y/1e12:.3f} |')
stage.append(f"| Total |{sum(a)/1e12:.3f} | {sum(b)/1e12:.3f} |")
stage+=['',"The reference path executes all 40 layers over all 8192 tokens, computing rectangular index scores before masking per the public implementation; the CED path's encoder processes all input, decoder global KV and index keys are still generated from all input, while the decoder body processes only the tail 128 tokens, with subsequent indexing restricted to the candidate set. The table includes the full text-matrix work for each path; differences stem from both the number of execution positions and the indexing algorithm.",'',
"Both paths include attention, routing scores, routed and shared experts, Engram projection, single-pass mHC projection, and vocab head. Separating the decoder's global projection from query computation shows how CED shortens the compute chain for long prompts. [^v41-forward]"]
md=H.parent/'02-模型架构.md';s=md.read_text()
s=re.sub("\\n\\n\\*\\*Table 2-D.*?\\[\\^v41-forward\\]\\n", '\n', s, flags=re.S)
s=re.sub("\\n\\n\\*\\*Table 2-6.*?(?=\\n\\[\\^)", '\n', s, flags=re.S)
s=re.sub(r'^\[\^v41-forward\]:.*\n?', '', s, flags=re.M)
start=s.index("**Context from");end=s.index('### 2.6.2',start)
d=load('chapter2-model-comparison');rows={(x['model_id'],x['context_label']):x for x in d['long_context']}
v=rows['deepseek-v4.1-flash','1M'];v4=rows['deepseek-v4-flash','1M'];k=rows['kimi-k3','1M']
long="**Compute and state growth as context grows from 8K to 1M.** Long-document QA and multi-turn tasks amplify the cost of context access. Below we keep single-request, one new token per step, and the final-token vocab head unchanged. The 8K scenario has 8192 history tokens; the 1M scenario has 1,048,575 history tokens, plus the current query for exactly 1,048,576 visible positions.\n\n![Single-step matrix compute for five models at 8K and 1M context.](ch02/figure-2-long-context-compute.svg)\n\n*Figure 2-31 Matrix compute for processing one more token at 8K/1M context. Follows the execution path from Table 2-C; x-axis is log scale; 1M includes the current query.*\n\nTable 2-E separately accumulates the current query's attention scores and value aggregation; V4-Flash and V4.1 Flash also add index dot products. The state column lists context and fixed state before the call, with precision consistent with Table 2-C.[^long-context-data]\n\n**Table 2-E Interaction Compute and State Capacity under Long Context**\n\n| Model | To Generate |\n| --- | --- |\n\n"
long+=f'''V4.1 Flash 的全局 KV 只有四份独立来源，增加上下文时不会为所有 40 层各增一份。主注意力每层最多使用 128 个局部 token和 512 个全局条目；解码器首个 Full 层生成候选集合，后续四个 Reindex 层各扫描至多 16384 个候选条目。编码器的三个索引器和解码器首个索引器仍需扫描增长的全局历史，因此计算量继续上升；跨层共享和分层索引改变了增长幅度。1M 下，其上下文交互为 {v['history_interaction_flops']/1e9:.2f} GFLOPs, and full single-step FLOPs are {v['matrix_flops']/1e9:.2f} GFLOPs。\n\nV4-Flash 则沿用 CSA 与 HCA 的两种压缩粒度：CSA 的主注意力选择上限保持不变，但索引扫描随历史增长；HCA 会读取全部已完成的粗粒度条目。1M 下，其上下文交互为 {v4['history_interaction_flops']/1e9:.2f} GFLOPs, and full single-step FLOPs are {v4['matrix_flops']/1e9:.2f} GFLOPs。较短上下文时，V4.1 Flash 更大的主干会增加投影和专家计算；历史足够长时，较少的索引器与分层候选选择才会抵消这部分新增工作。\n\nKimi K3 的 69 个 KDA 层保持固定递推状态，24 个 MLA 层继续访问随上下文增长的历史。紧凑 MLA 减少了缓存容量，却没有取消查询与历史 token之间的计算；1M 下，这部分交互达到 {k['history_interaction_flops']/1e9:.2f} GFLOPs, and the full model reaches {k['matrix_flops']/1e9:.2f} GFLOPs。评估长上下文设计，应分别检查保存了多少状态、访问哪些位置，以及为索引和更新状态增加了多少工作。\n\n统一计算还保留了 200K 场景：V4.1 Flash 的完整单步矩阵工作为 {rows['deepseek-v4.1-flash','200K']['matrix_flops']/1e9:.2f} GFLOPs，V4-Flash 为 {rows['deepseek-v4-flash','200K']['matrix_flops']/1e9:.2f} GFLOPs. By 1M, the gap between the two widens further, so the main text uses 1M to show the design value under long context.\n\n'''
s=s[:start]+long+s[end:]
# Stage comparison follows the parameter/resource block without new figure numbers.
marker='<!-- MODEL-COMPARISON:END -->'
s=s.replace(marker,marker+'\n\n'+'\n'.join(stage),1)
# Matrix table gathers all 2-D operations from the independently checked decoder ledger.
labels={
'hc_attn_fn':"attention single-pass mHC projection",'hc_ffn_fn':"FFN single-pass mHC projection",
'attn.wq_a.weight':"query down-projection",'attn.wq_b.weight':"query up-projection",'attn.wkv.weight':"local SWA KV projection",
'attn.wo_a.weight':"grouped output projection",'attn.wo_b.weight':"output concat projection",
'attn.compressor.wkv.weight':"global KV projection",'attn.compressor.wgate.weight':"2:1 compression gate",
'attn.indexer.wk.weight':"global index key projection",'attn.indexer.wq_b.weight':"index query projection",
'attn.indexer.weights_proj.weight':"index head weight projection",'ffn.gate.weight':"routing score",
'ffn.shared_experts.w1.weight':"shared expert gate",'ffn.shared_experts.w3.weight':"shared expert up",'ffn.shared_experts.w2.weight':"shared expert down",
'ffn.experts.0.w1.weight':"routed expert gate",'ffn.experts.0.w3.weight':"routed expert up",'ffn.experts.0.w2.weight':"routed expert down",
'engram.wkv.weight':"KV projection of Engram query result",'head.weight':"tail-token vocab head"}
buckets={}
for op in dc['operations']:
 if 'weight_math' not in op:continue
 key=re.sub(r'^layers\.\d+\.','',op['name']);buckets.setdefault(key,[]).append(op)
table=["**Table 2-6  DeepSeek V4.1 Flash: CED, Shared Context, and Engram**",'',
"This table covers all matrix projections for plain text generation. Input row count $m_l$ denotes the number of query positions processed by layer $l$ in this step; $u_l$ denotes the number of positions needing global KV generation, and $n_{\\mathrm{cmp},l}$ denotes newly completed compression entries this step. In reference full-layer prefill, $m_l=P$; in CED, encoder $m_l=P$, decoder $m_l=\\min(P,128)$, but the decoder's global-KV source layer still has $u_{20}=P$. All row counts must also be multiplied by request count $B$.",'',
"| Module & Role | Weight Matrix (Input Width × Output Width) | Execution Rows | Layers/Calls |",'| --- | --- | --- | ---: |']
for key,ops in buckets.items():
 iw,ow=ops[0]['weight_math'];rows='$m_l$'
 if key.startswith('attn.compressor.'):rows='$u_l$'
 if key=='attn.indexer.wk.weight':rows='$n_{\\mathrm{cmp},l}$'
 if key.startswith('ffn.experts.'):rows='$\\sum_e t_e=6m_l$'
 if key=='head.weight':rows="last token once"
 shape=f'${iw}\\times{ow}$'
 if key=='attn.wo_a.weight':
  # Stored output is 8 groups. Display each block to avoid implying a dense group cross-product.
  shape=f'${iw}\\times{ow//8}$, 8 groups total'
 table.append(f'| {labels[key]} | {shape} | {rows} | {len(ops)} |')
table+=['',
"The FLOPs for each 2D projection are input rows times input width times output width, times 2; grouped output projection only computes within each group, and connections that don't exist between groups must not be counted. The three routed-expert rows sum the rows received by each expert; shared experts process all query positions.",'',
"Attention interaction adds no new weights: each query has 64 heads at 512 dims each, with QK and PV jointly accumulated over actually accessed positions. The indexer has 32 heads at 128 dims each; Full, Reindex, and Reuse differ in scan range and whether indexing is executed. The compressor produces index keys only after the corresponding chunk completes; key-projection row count must not be written as positions per input step.",'',
"Engram first takes one 256-dim vector from each of 24 n-gram buckets, concatenates them into a 6144-dim input, then applies the table's projections to form four keys and one shared value; normalized dot product and gating write these into four residuals. The table lookup is not counted as matrix multiply; read payload, gating, and weighted reduction are each listed in the calculation record. The final mHC weighted merge and RMSNorm introduce no additional vocab weights. [^v41-forward]",'']
foot=s.index('\n[^',s.index("**Table 2-5"))
s=s[:foot]+'\n\n'+'\n'.join(table)+s[foot:]
s+="\n[^v41-forward]: [V4.1 Flash full-text matrix compute implementation](../calculations/src/infra_calc/topics/v41_forward.py); [CED 8K input](../calculations/results/v41-forward-prefill-8192-ced.md), [reference full-layer input](../calculations/results/v41-forward-prefill-8192-reference.md), [8K decode](../calculations/results/v41-forward-decode-8192-ced.md), [1M decode](../calculations/results/v41-forward-decode-1m-ced.md). [Calculation and review log](../research/ch02-five-models-2026-09-10/README.md).\n"
md.write_text(s)
print('Rendered V4.1 stage breakdown, module matrix table and 1M discussion.')
