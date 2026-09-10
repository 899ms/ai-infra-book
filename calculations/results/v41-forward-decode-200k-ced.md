# DeepSeek V4.1 Flash：完整文本矩阵计算

{'batch': 1, 'tokens': 1, 'history': 204800, 'execution': 'ced', 'index_algorithm': 'candidate', 'output_head': 'last'}

| 项目 | 结果 |
| --- | ---: |
| 文本逻辑参数（含 Engram） | 748,494,684,784 |
| 完整矩阵 FLOPs | 40,211,980,288 |
| 上下文交互 FLOPs | 7,952,408,576 |
| 调用前 BF16 逻辑状态（B） | 662,265,856 |
| 调用后 BF16 逻辑状态（B） | 662,267,144 |

| 组件 | 矩阵 FLOPs |
| --- | ---: |
| hyper_connections | 78,643,200 |
| attention_projection | 10,129,244,160 |
| attention_interaction | 3,221,225,472 |
| router | 157,286,400 |
| shared_expert | 2,831,155,200 |
| routed_expert | 16,986,931,200 |
| engram | 629,145,600 |
| compressor | 36,700,160 |
| index_projection | 86,638,592 |
| index_interaction | 4,731,183,104 |
| vocabulary_head | 1,323,827,200 |

## 逐层执行

| 层（从零编号） | 查询位置数 | 全局投影位置数 | 新全局条目 |
| --- | ---: | ---: | ---: |
| 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 0 |
| 2 | 1 | 1 | 0 |
| 3 | 1 | 0 | 0 |
| 4 | 1 | 0 | 0 |
| 5 | 1 | 0 | 0 |
| 6 | 1 | 0 | 0 |
| 7 | 1 | 0 | 0 |
| 8 | 1 | 1 | 0 |
| 9 | 1 | 0 | 0 |
| 10 | 1 | 0 | 0 |
| 11 | 1 | 0 | 0 |
| 12 | 1 | 0 | 0 |
| 13 | 1 | 0 | 0 |
| 14 | 1 | 1 | 0 |
| 15 | 1 | 0 | 0 |
| 16 | 1 | 0 | 0 |
| 17 | 1 | 0 | 0 |
| 18 | 1 | 0 | 0 |
| 19 | 1 | 0 | 0 |
| 20 | 1 | 1 | 1 |
| 21 | 1 | 0 | 0 |
| 22 | 1 | 0 | 0 |
| 23 | 1 | 0 | 0 |
| 24 | 1 | 0 | 0 |
| 25 | 1 | 0 | 0 |
| 26 | 1 | 0 | 0 |
| 27 | 1 | 0 | 0 |
| 28 | 1 | 0 | 0 |
| 29 | 1 | 0 | 0 |
| 30 | 1 | 0 | 0 |
| 31 | 1 | 0 | 0 |
| 32 | 1 | 0 | 0 |
| 33 | 1 | 0 | 0 |
| 34 | 1 | 0 | 0 |
| 35 | 1 | 0 | 0 |
| 36 | 1 | 0 | 0 |
| 37 | 1 | 0 | 0 |
| 38 | 1 | 0 | 0 |
| 39 | 1 | 0 | 0 |

## 口径

- All text parameters include Engram tables and projections; exclude vision, DSpark and quantization scales. Shapes validated against all 48 pinned checkpoint headers.
- Reference: all 40 layers over fresh prompt, rectangular index einsum before causal/candidate masking. CED: 20 encoder layers over all prompt positions, decoder KV/index-key projection over all positions, 20 decoder layers over last min(P,128) positions.
- CED decoder SWA replay truncates local attention to the replay segment; it reconstructs approximate states, not mathematically identical full-prefix states (paper 3.2.2). Global attention remains causal with original absolute positions.
- Candidate index mode counts causally reachable entries; later decoder indexers scan at most 16384 entries. Selection/pooling comparisons are not matrix FLOPs.
- One call with history>0 requires one token, matching the released source. Chunked prefix continuation and encoder cache-miss replay are not modeled by this entry point.
- Matrix FLOPs use FMA=2 and effective sparse pairs; scalar/special work is reported separately. These are resource demands, not measured time or throughput.

完整运算记录、各矩阵形状与来源哈希见同名 JSON。非矩阵算术仅为已列明分项，不作为完整标量或 GPU 指令总量。
