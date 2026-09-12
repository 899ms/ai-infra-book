# straggler-max — 

输入：`{"checkpoint_devices": 48, "declared_sigma_seconds": "1.044", "declared_spike_mtbf_seconds": 604800, "device_mtbf_seconds": 29122560, "intervals_seconds": [300, 600, 900, 1800, 3600], "mean_compute_seconds": "52.2", "model": "qwen3-8b", "overhead_seconds": "0.58", "ranks": [8, 48, 1024], "recovery_ns": 120000000000, "save_bandwidth_bytes_per_second": 7000000000, "straggler_k_sigma": "3"}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| expected_step_seconds | `{"8": 54.266238719511264, "48": 55.111378199602996, "1024": 56.17116214383592}` |
| expected_standard_max | `{"8": 1.4236003060452715, "48": 2.2331208808457803, "1024": 3.2482396013754027}` |
| mean_step_seconds | 52.78 |

计量条件：

- 每 rank 计算时间为独立同分布正态（均值取第 10.6 节 48 卡方案的 52.2 s 单卡计算，标准差为声明输入）；同步步时间 = 最大值 + 声明的通信与输入等待（本次为 0.58 s）。正态尾部允许负值，但在所用 σ 下概率可忽略。
- E[max] 用阶次统计积分的复合 Simpson 数值求积（标准库），不是精确有理数；未模拟相关性、周期性抖动或持续性慢卡。
- 检测信号是每 rank 在桶 AllReduce 上的等待：均值 rank 的期望等待 = E[max] - μ；一张卡慢到 μ+kσ 时，其余卡等待 ≈ 该卡时间减其余 N-1 卡的最大值。
- 三种响应：等待（步时间取慢卡时间）、重分配（去掉慢卡后均匀摊派，均值乘 N/(N-1)，不计迁移成本）、驱逐（从检查点重启，成本 = 期望丢失工作 τ/2 + 恢复时间，复用 checkpoint-interval 的保存成本）。
- loss spike 回滚率作为作业级共同冲击率加入 checkpoint-interval 的一阶损失与 Poisson 模型：L(τ)=c/τ+(λ_hw+λ_spike)(τ/2+r)。spike 的 MTBF 为声明值，未归档实测。

固定来源：

- [configs/models/qwen3-8b/config.json](https://huggingface.co/Qwen/Qwen3-8B/resolve/b968826d9c46dd6066d109eabc6255188de91218/config.json)，SHA256 `f7c4eadfbbf522470667b797a3c89be2524832d2d599797248dc304fff447c30`。
- [sources/qwen3-8b/model.safetensors.index.json](https://huggingface.co/Qwen/Qwen3-8B/resolve/b968826d9c46dd6066d109eabc6255188de91218/model.safetensors.index.json)，SHA256 `f9fdbcb91c23971c13ec5d5f2573d2349e8f61f2f049371ec699281748fdb1bc`。
- [sources/qwen3/modeling_qwen3.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3/modeling_qwen3.py)，SHA256 `704c914530530a1acb0b443add1f520404e3ac2c28c0ab7e16f80f86cfe8ccb2`。
- [sources/qwen3/modeling_qwen3_moe.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3_moe/modeling_qwen3_moe.py)，SHA256 `3af43d01f9f902c8009b6dd7d7b8b563561b53dd0aa54175f585ae90d049fdb8`。
