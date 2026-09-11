# clos-cut — 

输入：`{"gradient_dtype": "FP32", "link_bytes_per_second": 50000000000, "mode": "rail", "model": "qwen3-8b", "nic_bytes_per_second": 50000000000, "oversubscription": "1", "pairing": "aligned", "partition_endpoints": 1024, "radix": 64, "rails": 8, "results_glob": "gradient-*.json", "server_counts": [2, 4, 8, 16, 32], "servers": 2, "startup_ns": 833, "supernode_scenario": "scenarios/supernode-scaling-example.json", "tiers": [2, 3]}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| rails | 8 |
| servers | 2 |
| pairing | `"aligned"` |
| cross_server_rounds | 2 |
| bytes_per_rail_each_direction | 25,165,824 |
| bytes_all_rails_each_direction | 201,326,592 |
| spine_crossing_bytes | 0 |
| per_rail_seconds_exact | `"6312281/12500000000"` |
| single_nic_counterfactual_seconds_exact | `"50352473/12500000000"` |
| rail_parallel_speedup_exact | `"50352473/6312281"` |

计量条件：

- 两台服务器各 8 卡，每卡一张网卡接到对应轨道（rail）的叶交换机；分层 AllReduce 的跨服务器阶段是两 rank 的 ReduceScatter + AllGather，各发送半个分片。
- 梯度取 Qwen3-8B 第一层 gate_proj 一份参数梯度（与 hierarchical-gradient 相同的张量），FP32 时 192 MiB；分片 = 梯度/本地 rank 数。
- aligned 配对时每对只经过自己的轨道叶交换机；shifted 配对时每对跨两个轨道，全部字节须经脊层。时间只计网卡串行发送与每轮启动，不含本地 NVLink 阶段、传播或交换机排队。

固定来源：

- [configs/models/qwen3-8b/config.json](https://huggingface.co/Qwen/Qwen3-8B/resolve/b968826d9c46dd6066d109eabc6255188de91218/config.json)，SHA256 `f7c4eadfbbf522470667b797a3c89be2524832d2d599797248dc304fff447c30`。
- [sources/qwen3-8b/model.safetensors.index.json](https://huggingface.co/Qwen/Qwen3-8B/resolve/b968826d9c46dd6066d109eabc6255188de91218/model.safetensors.index.json)，SHA256 `f9fdbcb91c23971c13ec5d5f2573d2349e8f61f2f049371ec699281748fdb1bc`。
- [sources/qwen3/modeling_qwen3.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3/modeling_qwen3.py)，SHA256 `704c914530530a1acb0b443add1f520404e3ac2c28c0ab7e16f80f86cfe8ccb2`。
- [sources/qwen3/modeling_qwen3_moe.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3_moe/modeling_qwen3_moe.py)，SHA256 `3af43d01f9f902c8009b6dd7d7b8b563561b53dd0aa54175f585ae90d049fdb8`。
