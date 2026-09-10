# DeepSeek V4.1 Flash：完整文本矩阵计算

{'batch': 1, 'tokens': 128, 'history': 0, 'execution': 'ced', 'index_algorithm': 'candidate', 'output_head': 'last'}

| 项目 | 结果 |
| --- | ---: |
| 文本逻辑参数（含 Engram） | 748,494,684,784 |
| 完整矩阵 FLOPs | 4,036,154,621,952 |
| 上下文交互 FLOPs | 75,030,331,392 |
| 调用前 BF16 逻辑状态（B） | 24,576 |
| 调用后 BF16 逻辑状态（B） | 5,678,080 |

| 组件 | 矩阵 FLOPs |
| --- | ---: |
| hyper_connections | 10,066,329,600 |
| attention_projection | 1,296,543,252,480 |
| attention_interaction | 74,591,502,336 |
| router | 20,132,659,200 |
| shared_expert | 362,387,865,600 |
| routed_expert | 2,174,327,193,600 |
| engram | 80,530,636,800 |
| compressor | 4,697,620,480 |
| index_projection | 11,114,905,600 |
| index_interaction | 438,829,056 |
| vocabulary_head | 1,323,827,200 |

## 逐层执行

| 层（从零编号） | 查询位置数 | 全局投影位置数 | 新全局条目 |
| --- | ---: | ---: | ---: |
| 0 | 128 | 0 | 0 |
| 1 | 128 | 0 | 0 |
| 2 | 128 | 128 | 64 |
| 3 | 128 | 0 | 0 |
| 4 | 128 | 0 | 0 |
| 5 | 128 | 0 | 0 |
| 6 | 128 | 0 | 0 |
| 7 | 128 | 0 | 0 |
| 8 | 128 | 128 | 64 |
| 9 | 128 | 0 | 0 |
| 10 | 128 | 0 | 0 |
| 11 | 128 | 0 | 0 |
| 12 | 128 | 0 | 0 |
| 13 | 128 | 0 | 0 |
| 14 | 128 | 128 | 64 |
| 15 | 128 | 0 | 0 |
| 16 | 128 | 0 | 0 |
| 17 | 128 | 0 | 0 |
| 18 | 128 | 0 | 0 |
| 19 | 128 | 0 | 0 |
| 20 | 128 | 128 | 128 |
| 21 | 128 | 0 | 0 |
| 22 | 128 | 0 | 0 |
| 23 | 128 | 0 | 0 |
| 24 | 128 | 0 | 0 |
| 25 | 128 | 0 | 0 |
| 26 | 128 | 0 | 0 |
| 27 | 128 | 0 | 0 |
| 28 | 128 | 0 | 0 |
| 29 | 128 | 0 | 0 |
| 30 | 128 | 0 | 0 |
| 31 | 128 | 0 | 0 |
| 32 | 128 | 0 | 0 |
| 33 | 128 | 0 | 0 |
| 34 | 128 | 0 | 0 |
| 35 | 128 | 0 | 0 |
| 36 | 128 | 0 | 0 |
| 37 | 128 | 0 | 0 |
| 38 | 128 | 0 | 0 |
| 39 | 128 | 0 | 0 |

## 口径

- All text parameters include Engram tables and projections; exclude vision, DSpark and quantization scales. Shapes validated against all 48 pinned checkpoint headers.
- Reference: all 40 layers over fresh prompt, rectangular index einsum before causal/candidate masking. CED: 20 encoder layers over all prompt positions, decoder KV/index-key projection over all positions, 20 decoder layers over last min(P,128) positions.
- CED decoder SWA replay truncates local attention to the replay segment; it reconstructs approximate states, not mathematically identical full-prefix states (paper 3.2.2). Global attention remains causal with original absolute positions.
- Candidate index mode counts causally reachable entries; later decoder indexers scan at most 16384 entries. Selection/pooling comparisons are not matrix FLOPs.
- One call with history>0 requires one token, matching the released source. Chunked prefix continuation and encoder cache-miss replay are not modeled by this entry point.
- Matrix FLOPs use FMA=2 and effective sparse pairs; scalar/special work is reported separately. These are resource demands, not measured time or throughput.

完整运算记录、各矩阵形状与来源哈希见同名 JSON。非矩阵算术仅为已列明分项，不作为完整标量或 GPU 指令总量。
