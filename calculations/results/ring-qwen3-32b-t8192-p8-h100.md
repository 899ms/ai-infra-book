# qwen-ring-collective — qwen3-32b

输入：`{"bandwidth_bytes_per_second": 450000000000, "batch": 1, "message_dtype": "BF16", "message_scope": "full activation per rank for all-reduce", "participants": 8, "startup_ns": 822, "tokens": 8192}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| activation_shape | `[8192, 5120]` |
| message_bytes_per_rank | 83,886,080 |
| chunk_bytes | 10,485,760 |
| all_reduce_rounds | 14 |
| all_reduce_send_bytes_per_rank | 146,800,640 |
| all_reduce_receive_bytes_per_rank | 146,800,640 |
| all_reduce_network_send_bytes | 1,174,405,120 |
| all_reduce_global_reduction_adds | 293,601,280 |
| all_reduce_startup_seconds | 1.1508e-05 |
| all_reduce_bandwidth_seconds | 0.0003262236444444444 |
| all_reduce_modeled_seconds | 0.00033773164444444445 |
| dense_tp_all_reduce_calls | 128 |
| dense_tp_serial_collective_seconds | 0.04322965048888889 |
| measured_collective_seconds | `null` |

| 阶段 | 轮次 | sender → receiver : chunk (bytes) |
| --- | ---: | --- |
| reduce_scatter | 0 | 0 → 1 : 0 (10485760); 1 → 2 : 1 (10485760); 2 → 3 : 2 (10485760); 3 → 4 : 3 (10485760); 4 → 5 : 4 (10485760); 5 → 6 : 5 (10485760); 6 → 7 : 6 (10485760); 7 → 0 : 7 (10485760) |
| reduce_scatter | 1 | 0 → 1 : 7 (10485760); 1 → 2 : 0 (10485760); 2 → 3 : 1 (10485760); 3 → 4 : 2 (10485760); 4 → 5 : 3 (10485760); 5 → 6 : 4 (10485760); 6 → 7 : 5 (10485760); 7 → 0 : 6 (10485760) |
| reduce_scatter | 2 | 0 → 1 : 6 (10485760); 1 → 2 : 7 (10485760); 2 → 3 : 0 (10485760); 3 → 4 : 1 (10485760); 4 → 5 : 2 (10485760); 5 → 6 : 3 (10485760); 6 → 7 : 4 (10485760); 7 → 0 : 5 (10485760) |
| reduce_scatter | 3 | 0 → 1 : 5 (10485760); 1 → 2 : 6 (10485760); 2 → 3 : 7 (10485760); 3 → 4 : 0 (10485760); 4 → 5 : 1 (10485760); 5 → 6 : 2 (10485760); 6 → 7 : 3 (10485760); 7 → 0 : 4 (10485760) |
| reduce_scatter | 4 | 0 → 1 : 4 (10485760); 1 → 2 : 5 (10485760); 2 → 3 : 6 (10485760); 3 → 4 : 7 (10485760); 4 → 5 : 0 (10485760); 5 → 6 : 1 (10485760); 6 → 7 : 2 (10485760); 7 → 0 : 3 (10485760) |
| reduce_scatter | 5 | 0 → 1 : 3 (10485760); 1 → 2 : 4 (10485760); 2 → 3 : 5 (10485760); 3 → 4 : 6 (10485760); 4 → 5 : 7 (10485760); 5 → 6 : 0 (10485760); 6 → 7 : 1 (10485760); 7 → 0 : 2 (10485760) |
| reduce_scatter | 6 | 0 → 1 : 2 (10485760); 1 → 2 : 3 (10485760); 2 → 3 : 4 (10485760); 3 → 4 : 5 (10485760); 4 → 5 : 6 (10485760); 5 → 6 : 7 (10485760); 6 → 7 : 0 (10485760); 7 → 0 : 1 (10485760) |
| all_gather | 0 | 0 → 1 : 1 (10485760); 1 → 2 : 2 (10485760); 2 → 3 : 3 (10485760); 3 → 4 : 4 (10485760); 4 → 5 : 5 (10485760); 5 → 6 : 6 (10485760); 6 → 7 : 7 (10485760); 7 → 0 : 0 (10485760) |
| all_gather | 1 | 0 → 1 : 0 (10485760); 1 → 2 : 1 (10485760); 2 → 3 : 2 (10485760); 3 → 4 : 3 (10485760); 4 → 5 : 4 (10485760); 5 → 6 : 5 (10485760); 6 → 7 : 6 (10485760); 7 → 0 : 7 (10485760) |
| all_gather | 2 | 0 → 1 : 7 (10485760); 1 → 2 : 0 (10485760); 2 → 3 : 1 (10485760); 3 → 4 : 2 (10485760); 4 → 5 : 3 (10485760); 5 → 6 : 4 (10485760); 6 → 7 : 5 (10485760); 7 → 0 : 6 (10485760) |
| all_gather | 3 | 0 → 1 : 6 (10485760); 1 → 2 : 7 (10485760); 2 → 3 : 0 (10485760); 3 → 4 : 1 (10485760); 4 → 5 : 2 (10485760); 5 → 6 : 3 (10485760); 6 → 7 : 4 (10485760); 7 → 0 : 5 (10485760) |
| all_gather | 4 | 0 → 1 : 5 (10485760); 1 → 2 : 6 (10485760); 2 → 3 : 7 (10485760); 3 → 4 : 0 (10485760); 4 → 5 : 1 (10485760); 5 → 6 : 2 (10485760); 6 → 7 : 3 (10485760); 7 → 0 : 4 (10485760) |
| all_gather | 5 | 0 → 1 : 4 (10485760); 1 → 2 : 5 (10485760); 2 → 3 : 6 (10485760); 3 → 4 : 7 (10485760); 4 → 5 : 0 (10485760); 5 → 6 : 1 (10485760); 6 → 7 : 2 (10485760); 7 → 0 : 3 (10485760) |
| all_gather | 6 | 0 → 1 : 3 (10485760); 1 → 2 : 4 (10485760); 2 → 3 : 5 (10485760); 3 → 4 : 6 (10485760); 4 → 5 : 7 (10485760); 5 → 6 : 0 (10485760); 6 → 7 : 1 (10485760); 7 → 0 : 2 (10485760) |

计量条件：

- Qwen3 Dense BF16 [B*T,H] partial output per rank; two row-parallel output all-reduces per layer is an explicit basic TP execution assumption, not every backend implementation.
- Reduce-scatter starts with the full M-byte partial tensor on each rank and ends with M/p reduced bytes; all-gather starts with those M/p bytes and ends with M bytes. Do not interpret M as per-rank input for both phases.
- Every round sends one chunk to the next rank. After reduce-scatter rank r owns reduced chunk (r+1) mod p; all-gather follows that ownership. p=1 is an identity with zero communication.
- Per-rank sent and received bytes are separate endpoint counters. Network payload sums sends once, not sends plus receives. Physical hops, shared links, multiport paths and staging require a topology model.
- Time assumes a balanced ring with simultaneous independent directed edges, one startup per round and one-direction effective link bandwidth. Reduction compute, launch, contention, overlap and channels are not measured here.
- Reduction scalar additions are logical counts; accumulator precision and floating-point reassociation require a backend-specific analysis. They are not Tensor FLOPs.
- Serial 2L-call total deliberately excludes overlap and fusion. Only communication for the stated TP path is counted; weights, KV placement, compute and device feasibility are separate.

固定来源：

- [configs/models/qwen3-32b/config.json](https://huggingface.co/Qwen/Qwen3-32B/resolve/9216db5781bf21249d130ec9da846c4624c16137/config.json)，SHA256 `97e295b63283935788fac5e4f8860862a56d4089538cafc93f0431f2ebe483bb`。
- [sources/qwen3-32b/model.safetensors.index.json](https://huggingface.co/Qwen/Qwen3-32B/resolve/9216db5781bf21249d130ec9da846c4624c16137/model.safetensors.index.json)，SHA256 `bed42c6c55274bc08a1f616bceb3bcb84b3f02cb6584c573bd18c6519291ecd0`。
- [sources/qwen3/modeling_qwen3.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3/modeling_qwen3.py)，SHA256 `704c914530530a1acb0b443add1f520404e3ac2c28c0ab7e16f80f86cfe8ccb2`。
- [sources/qwen3/modeling_qwen3_moe.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3_moe/modeling_qwen3_moe.py)，SHA256 `3af43d01f9f902c8009b6dd7d7b8b563561b53dd0aa54175f585ae90d049fdb8`。
