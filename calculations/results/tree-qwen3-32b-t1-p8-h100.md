# qwen-binomial-tree-collective — qwen3-32b

输入：`{"bandwidth_bytes_per_second": 450000000000, "batch": 1, "message_dtype": "BF16", "participants": 8, "root": 0, "segmentation": false, "startup_ns": 822, "tokens": 1}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| activation_shape | `[1, 5120]` |
| message_bytes_per_rank | 10,240 |
| rounds_per_phase | 3 |
| all_reduce_rounds | 6 |
| all_reduce_network_send_bytes | 143,360 |
| all_reduce_global_reduction_adds | 35,840 |
| maximum_rank_send_bytes | 30,720 |
| maximum_rank_receive_bytes | 30,720 |
| all_reduce_startup_seconds | 4.932e-06 |
| all_reduce_bandwidth_seconds | 1.3653333333333334e-07 |
| all_reduce_modeled_seconds | 5.068533333333334e-06 |
| dense_tp_all_reduce_calls | 128 |
| dense_tp_serial_collective_seconds | 0.0006487722666666668 |
| measured_collective_seconds | `null` |

| 阶段 | 轮次 | sender → receiver (bytes) |
| --- | ---: | --- |
| reduce | 0 | 1 → 0 (10240); 3 → 2 (10240); 5 → 4 (10240); 7 → 6 (10240) |
| reduce | 1 | 2 → 0 (10240); 6 → 4 (10240) |
| reduce | 2 | 4 → 0 (10240) |
| broadcast | 0 | 0 → 4 (10240) |
| broadcast | 1 | 0 → 2 (10240); 4 → 6 (10240) |
| broadcast | 2 | 0 → 1 (10240); 2 → 3 (10240); 4 → 5 (10240); 6 → 7 (10240) |

| Rank | 发送 bytes | 接收 bytes | 标量归约加法 |
| --- | ---: | ---: | ---: |
| 0 | 30720 | 30720 | 15360 |
| 1 | 10240 | 10240 | 0 |
| 2 | 20480 | 20480 | 5120 |
| 3 | 10240 | 10240 | 0 |
| 4 | 30720 | 30720 | 10240 |
| 5 | 10240 | 10240 | 0 |
| 6 | 20480 | 20480 | 5120 |
| 7 | 10240 | 10240 | 0 |

计量条件：

- Same Qwen3 Dense BF16 [B*T,H] partial activation on every rank. Basic TP calls two output all-reduces per layer; no device placement or backend dispatch claim.
- Binomial reduction rooted at zero followed by the reverse edge schedule for broadcast. Non-power-of-two groups skip absent partners; p=1 is identity. Integer replay validates this schedule, not floating-point bitwise equivalence.
- Each edge sends the full M-byte tensor. Each round completes before the next, with independent simultaneous directed edges and one startup per round. This unsegmented algorithm is not a double binary tree, recursive halving/doubling or a model of every library tree.
- Network volume is 2(p-1)M, equal to ring all-reduce volume, but rank traffic is nonuniform and critical-path transfers are full tensors. Message-size-dependent performance differs despite equal total volume.
- Per-rank reduction additions are separate scalar work; precision, reduction service time, topology hops, link sharing, launch, segmentation and overlap are excluded from the declared timing model.
- Bandwidth is one-direction effective link bandwidth; startup and bandwidth defaults are teaching assumptions. Serial 2L total is not complete TP iteration latency or measured NCCL performance.

固定来源：

- [configs/models/qwen3-32b/config.json](https://huggingface.co/Qwen/Qwen3-32B/resolve/9216db5781bf21249d130ec9da846c4624c16137/config.json)，SHA256 `97e295b63283935788fac5e4f8860862a56d4089538cafc93f0431f2ebe483bb`。
- [sources/qwen3-32b/model.safetensors.index.json](https://huggingface.co/Qwen/Qwen3-32B/resolve/9216db5781bf21249d130ec9da846c4624c16137/model.safetensors.index.json)，SHA256 `bed42c6c55274bc08a1f616bceb3bcb84b3f02cb6584c573bd18c6519291ecd0`。
- [sources/qwen3/modeling_qwen3.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3/modeling_qwen3.py)，SHA256 `704c914530530a1acb0b443add1f520404e3ac2c28c0ab7e16f80f86cfe8ccb2`。
- [sources/qwen3/modeling_qwen3_moe.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3_moe/modeling_qwen3_moe.py)，SHA256 `3af43d01f9f902c8009b6dd7d7b8b563561b53dd0aa54175f585ae90d049fdb8`。
