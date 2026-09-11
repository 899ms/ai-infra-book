# moe-capacity — 

输入：`{"capacity_factors": ["1", "1.25", "1.5", "2"], "chapter_histogram": [96, 32], "declared_hot_fraction": "1/2", "declared_hot_multiplier": "3/2", "model": "qwen3-235b-a22b", "tokens": 8192}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| chapter_assignments | 128 |
| model_experts | 128 |
| model_top_k | 8 |
| model_assignments | 65,536 |
| chapter_c1_capacity | 64 |
| chapter_c1_dropped | 32 |
| chapter_c1_padded | 32 |
| chapter_c5/4_capacity | 80 |
| chapter_c5/4_dropped | 16 |
| chapter_c5/4_padded | 48 |
| chapter_c3/2_capacity | 96 |
| chapter_c3/2_dropped | 0 |
| chapter_c3/2_padded | 64 |
| chapter_c2_capacity | 128 |
| chapter_c2_dropped | 0 |
| chapter_c2_padded | 128 |
| model_c1_capacity | 512 |
| model_c1_dropped_fraction | 0.25 |
| model_c1_padded_fraction_of_executed | 0.25 |
| model_c5/4_capacity | 640 |
| model_c5/4_dropped_fraction | 0.125 |
| model_c5/4_padded_fraction_of_executed | 0.3 |
| model_c3/2_capacity | 768 |
| model_c3/2_dropped_fraction | 0.0 |
| model_c3/2_padded_fraction_of_executed | 0.3333333333333333 |
| model_c2_capacity | 1,024 |
| model_c2_dropped_fraction | 0.0 |
| model_c2_padded_fraction_of_executed | 0.5 |

计量条件：

- 容量因子规则取自归档 Switch Transformer 文本：每专家容量 = (token 数×k/E)×c，向下取整；超出容量的分派被丢弃（该层不处理），不足的槽位填充，仍占用计算与通信。
- 第 10 章示例：两张卡上的专家分别收到 96、32 次分派，按 E=2、k=1 处理。锁定配置示例：Qwen3-235B 的 E 与 k 来自官方 config；不均衡形状（一半专家收到 1.5 倍均值）为声明输入，与 96/32 的 3:1 比例一致。
- 只统计行数：丢弃 token 对质量的影响、辅助损失、专家并行的通信量与实际内核分组方式都不在本账内。

固定来源：

- [configs/models/qwen3-235b-a22b/config.json](https://huggingface.co/Qwen/Qwen3-235B-A22B/resolve/8efa61729e24bd65b1d152b5ab5409052aa80e65/config.json)，SHA256 `0ecd5d6fe6f2db6739e4e36ab06b88ebe7bd013ef31b9583f43796059a2b23a4`。
- [sources/qwen3-235b-a22b/model.safetensors.index.json](https://huggingface.co/Qwen/Qwen3-235B-A22B/resolve/8efa61729e24bd65b1d152b5ab5409052aa80e65/model.safetensors.index.json)，SHA256 `53dd34fac4a29fc7ee58fa9d92c7892ea6884431c3bd3d0dc93def7bbd0b8b78`。
- [sources/qwen3/modeling_qwen3.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3/modeling_qwen3.py)，SHA256 `704c914530530a1acb0b443add1f520404e3ac2c28c0ab7e16f80f86cfe8ccb2`。
- [sources/qwen3/modeling_qwen3_moe.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3_moe/modeling_qwen3_moe.py)，SHA256 `3af43d01f9f902c8009b6dd7d7b8b563561b53dd0aa54175f585ae90d049fdb8`。
