# DeepSeek V4.1 Flash：完整文本矩阵计算

{'batch': 1, 'tokens': 8192, 'history': 0, 'execution': 'ced', 'index_algorithm': 'candidate', 'output_head': 'last'}

| 项目 | 结果 |
| --- | ---: |
| 文本逻辑参数（含 Engram） | 748,494,684,784 |
| 完整矩阵 FLOPs | 143,946,626,891,776 |
| 上下文交互 FLOPs | 12,652,976,275,456 |
| 调用前 BF16 逻辑状态（B） | 24,576 |
| 调用后 BF16 逻辑状态（B） | 31,547,392 |

| 组件 | 矩阵 FLOPs |
| --- | ---: |
| hyper_connections | 327,155,712,000 |
| attention_projection | 42,137,655,705,600 |
| attention_interaction | 12,198,042,664,960 |
| router | 654,311,424,000 |
| shared_expert | 11,777,605,632,000 |
| routed_expert | 70,665,633,792,000 |
| engram | 5,153,960,755,200 |
| compressor | 300,647,710,720 |
| index_projection | 275,356,057,600 |
| index_interaction | 454,933,610,496 |
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
| 20 | 128 | 8192 | 8192 |
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
