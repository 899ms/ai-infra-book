# DeepSeek V4.1 Flash：完整文本矩阵计算

{'batch': 1, 'tokens': 8192, 'history': 0, 'execution': 'reference', 'index_algorithm': 'reference', 'output_head': 'last'}

| 项目 | 结果 |
| --- | ---: |
| 文本逻辑参数（含 Engram） | 748,494,684,784 |
| 完整矩阵 FLOPs | 282,386,229,624,832 |
| 上下文交互 FLOPs | 28,957,676,142,592 |
| 调用前 BF16 逻辑状态（B） | 24,576 |
| 调用后 BF16 逻辑状态（B） | 31,547,392 |

| 组件 | 矩阵 FLOPs |
| --- | ---: |
| hyper_connections | 644,245,094,400 |
| attention_projection | 82,978,768,158,720 |
| attention_interaction | 25,384,263,352,320 |
| router | 1,288,490,188,800 |
| shared_expert | 23,192,823,398,400 |
| routed_expert | 139,156,940,390,400 |
| engram | 5,153,960,755,200 |
| compressor | 300,647,710,720 |
| index_projection | 711,353,958,400 |
| index_interaction | 3,573,412,790,272 |
| vocabulary_head | 1,323,827,200 |

## 逐层执行

| 层（从零编号） | 查询位置数 | 全局投影位置数 | 新全局条目 |
| --- | ---: | ---: | ---: |
| 0 | 8192 | 0 | 0 |
| 1 | 8192 | 0 | 0 |
| 2 | 8192 | 8192 | 4096 |
| 3 | 8192 | 0 | 0 |
| 4 | 8192 | 0 | 0 |
| 5 | 8192 | 0 | 0 |
| 6 | 8192 | 0 | 0 |
| 7 | 8192 | 0 | 0 |
| 8 | 8192 | 8192 | 4096 |
| 9 | 8192 | 0 | 0 |
| 10 | 8192 | 0 | 0 |
| 11 | 8192 | 0 | 0 |
| 12 | 8192 | 0 | 0 |
| 13 | 8192 | 0 | 0 |
| 14 | 8192 | 8192 | 4096 |
| 15 | 8192 | 0 | 0 |
| 16 | 8192 | 0 | 0 |
| 17 | 8192 | 0 | 0 |
| 18 | 8192 | 0 | 0 |
| 19 | 8192 | 0 | 0 |
| 20 | 8192 | 8192 | 8192 |
| 21 | 8192 | 0 | 0 |
| 22 | 8192 | 0 | 0 |
| 23 | 8192 | 0 | 0 |
| 24 | 8192 | 0 | 0 |
| 25 | 8192 | 0 | 0 |
| 26 | 8192 | 0 | 0 |
| 27 | 8192 | 0 | 0 |
| 28 | 8192 | 0 | 0 |
| 29 | 8192 | 0 | 0 |
| 30 | 8192 | 0 | 0 |
| 31 | 8192 | 0 | 0 |
| 32 | 8192 | 0 | 0 |
| 33 | 8192 | 0 | 0 |
| 34 | 8192 | 0 | 0 |
| 35 | 8192 | 0 | 0 |
| 36 | 8192 | 0 | 0 |
| 37 | 8192 | 0 | 0 |
| 38 | 8192 | 0 | 0 |
| 39 | 8192 | 0 | 0 |

## 口径

- All text parameters include Engram tables and projections; exclude vision, DSpark and quantization scales. Shapes validated against all 48 pinned checkpoint headers.
- Reference: all 40 layers over fresh prompt, rectangular index einsum before causal/candidate masking. CED: 20 encoder layers over all prompt positions, decoder KV/index-key projection over all positions, 20 decoder layers over last min(P,128) positions.
- CED decoder SWA replay truncates local attention to the replay segment; it reconstructs approximate states, not mathematically identical full-prefix states (paper 3.2.2). Global attention remains causal with original absolute positions.
- Candidate index mode counts causally reachable entries; later decoder indexers scan at most 16384 entries. Selection/pooling comparisons are not matrix FLOPs.
- One call with history>0 requires one token, matching the released source. Chunked prefix continuation and encoder cache-miss replay are not modeled by this entry point.
- Matrix FLOPs use FMA=2 and effective sparse pairs; scalar/special work is reported separately. These are resource demands, not measured time or throughput.

完整运算记录、各矩阵形状与来源哈希见同名 JSON。非矩阵算术仅为已列明分项，不作为完整标量或 GPU 指令总量。
