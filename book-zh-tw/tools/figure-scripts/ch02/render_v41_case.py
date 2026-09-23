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
stage=["**表 2-D　V4.1 Flash 的 8K 輸入如何分配到執行階段（TFLOPs）**",'',"| 階段 | 參考全層前向 | CED＋末尾視窗重放 |",'| --- | ---: | ---: |']
for title,x,y in zip(["20 層編碼器","解碼器共享全域 KV 與索引鍵投影","20 層解碼器的查詢與前饋等計算","末尾 token詞表頭"],a,b):stage.append(f'| {title} | {x/1e12:.3f} | {y/1e12:.3f} |')
stage.append(f"| 合計 | {sum(a)/1e12:.3f} | {sum(b)/1e12:.3f} |")
stage+=['',"參考路徑執行全部 8192 個 token的 40 層，並按公開實作先計算矩形索引分數再遮蔽；CED 路徑的編碼器處理全部輸入，解碼器全域 KV 與索引鍵仍為全部輸入生成，解碼器主體只處理末尾 128 個 token，後續索引限制在候選集合內。表中分別包含各路徑的全部文字矩陣工作，差異同時來自執行位置數與索引演算法。",'',
"兩條路徑均包含注意力、路由評分、路由及共享專家、Engram 投影、Single-Pass mHC 投影和詞表頭。把解碼器的全域投影與查詢計算分開，就能看出 CED 如何縮短長提示經過的計算鏈。[^v41-forward]"]
md=H.parent/'02-模型架构.md';s=md.read_text()
s=re.sub("\\n\\n\\*\\*表 2-D.*?\\[\\^v41-forward\\]\\n", '\n', s, flags=re.S)
s=re.sub("\\n\\n\\*\\*表 2-6.*?(?=\\n\\[\\^)", '\n', s, flags=re.S)
s=re.sub(r'^\[\^v41-forward\]:.*\n?', '', s, flags=re.M)
start=s.index("**上下文從");end=s.index('### 2.6.2',start)
d=load('chapter2-model-comparison');rows={(x['model_id'],x['context_label']):x for x in d['long_context']}
v=rows['deepseek-v4.1-flash','1M'];v4=rows['deepseek-v4-flash','1M'];k=rows['kimi-k3','1M']
long="**上下文從 8K 增至 1M 時的運算量與狀態增長。** 長文件問答和多輪任務會放大上下文存取的成本。下面保持單請求、一次新增一個 token 和末尾 token詞表頭不變。8K 場景有 8192 個歷史 token；1M 場景有 1,048,575 個歷史 token，加上當前查詢正好為 1,048,576 個可見位置。\n\n![五模型在 8K 與 1M 上下文下的單步矩陣運算量。](ch02/figure-2-long-context-compute.svg)\n\n*圖 2-31　8K／1M 上下文下再處理一個 token 的矩陣運算量。沿用表 2-C 的執行路徑，橫軸為對數刻度；1M 包含當前查詢。*\n\n表 2-E 單獨累計當前查詢的注意力評分與值彙總；V4-Flash 與 V4.1 Flash 再加入索引點積。狀態列列出呼叫前的上下文和固定狀態，精度與表 2-C 一致。[^long-context-data]\n\n**表 2-E　長上下文下的互動運算與狀態容量**\n\n| 模型 | 待生成 |\n| --- | --- |\n\n"
long+=f'''V4.1 Flash 的全域 KV 只有四份獨立來源，增加上下文時不會為所有 40 層各增一份。主注意力每層最多使用 128 個區域性 token和 512 個全域條目；解碼器首個 Full 層生成候選集合，後續四個 Reindex 層各掃描至多 16384 個候選條目。編碼器的三個索引器和解碼器首個索引器仍需掃描增長的全域歷史，因此計算量繼續上升；跨層共享和分層索引改變了增長幅度。1M 下，其上下文互動為 {v['history_interaction_flops']/1e9:.2f} GFLOPs，完整單步矩陣工作為 {v['matrix_flops']/1e9:.2f} GFLOPs。\n\nV4-Flash 則沿用 CSA 與 HCA 的兩種壓縮粒度：CSA 的主注意力選擇上限保持不變，但索引掃描隨歷史增長；HCA 會讀取全部已完成的粗粒度條目。1M 下，其上下文互動為 {v4['history_interaction_flops']/1e9:.2f} GFLOPs，完整單步矩陣工作為 {v4['matrix_flops']/1e9:.2f} GFLOPs。較短上下文時，V4.1 Flash 更大的主幹會增加投影和專家計算；歷史足夠長時，較少的索引器與分層候選選擇才會抵消這部分新增工作。\n\nKimi K3 的 69 個 KDA 層保持固定遞推狀態，24 個 MLA 層繼續存取隨上下文增長的歷史。緊湊 MLA 減少了快取容量，卻沒有取消查詢與歷史 token之間的計算；1M 下，這部分互動達到 {k['history_interaction_flops']/1e9:.2f} GFLOPs，整模型達到 {k['matrix_flops']/1e9:.2f} GFLOPs。評估長上下文設計，應分別檢查儲存了多少狀態、存取哪些位置，以及為索引和更新狀態增加了多少工作。\n\n統一計算還保留了 200K 場景：V4.1 Flash 的完整單步矩陣工作為 {rows['deepseek-v4.1-flash','200K']['matrix_flops']/1e9:.2f} GFLOPs，V4-Flash 為 {rows['deepseek-v4-flash','200K']['matrix_flops']/1e9:.2f} GFLOPs。到 1M 時，兩者的計算量差異進一步擴大，所以正文選用 1M 展示長上下文下的設計價值。\n\n'''
s=s[:start]+long+s[end:]
# Stage comparison follows the parameter/resource block without new figure numbers.
marker='<!-- MODEL-COMPARISON:END -->'
s=s.replace(marker,marker+'\n\n'+'\n'.join(stage),1)
# Matrix table gathers all 2-D operations from the independently checked decoder ledger.
labels={
'hc_attn_fn':"注意力 Single-Pass mHC 投影",'hc_ffn_fn':"FFN Single-Pass mHC 投影",
'attn.wq_a.weight':"查詢下投影",'attn.wq_b.weight':"查詢上投影",'attn.wkv.weight':"區域性 SWA KV 投影",
'attn.wo_a.weight':"分組輸出投影",'attn.wo_b.weight':"輸出拼接投影",
'attn.compressor.wkv.weight':"全域 KV 投影",'attn.compressor.wgate.weight':"2:1 壓縮門控",
'attn.indexer.wk.weight':"全域索引鍵投影",'attn.indexer.wq_b.weight':"索引查詢投影",
'attn.indexer.weights_proj.weight':"索引頭權重投影",'ffn.gate.weight':"路由評分",
'ffn.shared_experts.w1.weight':"共享專家 gate",'ffn.shared_experts.w3.weight':"共享專家 up",'ffn.shared_experts.w2.weight':"共享專家 down",
'ffn.experts.0.w1.weight':"路由專家 gate",'ffn.experts.0.w3.weight':"路由專家 up",'ffn.experts.0.w2.weight':"路由專家 down",
'engram.wkv.weight':"Engram 查詢結果的 KV 投影",'head.weight':"末尾 token詞表頭"}
buckets={}
for op in dc['operations']:
 if 'weight_math' not in op:continue
 key=re.sub(r'^layers\.\d+\.','',op['name']);buckets.setdefault(key,[]).append(op)
table=["**表 2-6　DeepSeek V4.1 Flash：CED、共享上下文與 Engram**",'',
"本表覆蓋普通文字生成的全部矩陣投影。輸入行數 $m_l$ 表示第 $l$ 層本次處理的查詢位置數；$u_l$ 表示需要生成全域 KV 的位置數，$n_{\\mathrm{cmp},l}$ 表示本次新完成的壓縮條目數。參考全層 prefill 中 $m_l=P$；CED 中編碼器 $m_l=P$、解碼器 $m_l=\\min(P,128)$，但解碼器全域 KV 來源層仍有 $u_{20}=P$。所有行數還需乘請求數 $B$。",'',
"| 模組及作用 | 權重矩陣（輸入寬 × 輸出寬） | 執行行數 | 層／呼叫數 |",'| --- | --- | --- | ---: |']
for key,ops in buckets.items():
 iw,ow=ops[0]['weight_math'];rows='$m_l$'
 if key.startswith('attn.compressor.'):rows='$u_l$'
 if key=='attn.indexer.wk.weight':rows='$n_{\\mathrm{cmp},l}$'
 if key.startswith('ffn.experts.'):rows='$\\sum_e t_e=6m_l$'
 if key=='head.weight':rows="末尾 token一次"
 shape=f'${iw}\\times{ow}$'
 if key=='attn.wo_a.weight':
  # Stored output is 8 groups. Display each block to avoid implying a dense group cross-product.
  shape=f'${iw}\\times{ow//8}$，共 8 組'
 table.append(f'| {labels[key]} | {shape} | {rows} | {len(ops)} |')
table+=['',
"每個二維投影的矩陣運算量為輸入行數乘輸入寬、輸出寬，再乘 2；分組輸出投影只在各組內部運算，不能把組間不存在的連線計入。路由專家的三行按各專家接收的行數相加，共享專家處理全部查詢位置。",'',
"注意力互動沒有新增權重：每個查詢有 64 個頭、每頭 512 維，QK 與 PV 共同按實際存取位置累計。索引器有 32 個頭、每頭 128 維，Full、Reindex、Reuse 的掃描範圍和是否執行索引各不相同。壓縮器僅在相應塊完成後產生索引鍵，不能把鍵投影的行數寫成每次輸入的位置數。",'',
"Engram 首先從 n-gram 對應的 24 個桶各取一個 256 維向量，拼成 6144 維輸入，再經表中的投影形成四路鍵和一個共享值；歸一化點積與門控將其寫入四路殘差。查表不計作矩陣乘法，讀取載荷、門控和加權歸約分別列在計算記錄中。最後的 mHC 加權匯合與 RMSNorm 不引入另一份詞表權重。[^v41-forward]",'']
foot=s.index('\n[^',s.index("**表 2-5"))
s=s[:foot]+'\n\n'+'\n'.join(table)+s[foot:]
s+="\n[^v41-forward]: [V4.1 Flash 完整文字矩陣計算實作](../calculations/src/infra_calc/topics/v41_forward.py)；[CED 8K 輸入](../calculations/results/v41-forward-prefill-8192-ced.md)、[參考全層輸入](../calculations/results/v41-forward-prefill-8192-reference.md)、[8K decode](../calculations/results/v41-forward-decode-8192-ced.md)、[1M decode](../calculations/results/v41-forward-decode-1m-ced.md)。[計算與複核記錄](../research/ch02-five-models-2026-09-10/README.md)。\n"
md.write_text(s)
print('Rendered V4.1 stage breakdown, module matrix table and 1M discussion.')
