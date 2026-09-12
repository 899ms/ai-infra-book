# split-reduction-order — qwen3-8b

输入：`{"row": "bf16(sin(i+1)) for i in range(width)", "splits": 8, "width_multiplier": 1}`

数值为精确浮点复算；ULP 为 FP32 间距，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| width | 4,096 |
| epsilon | 1e-06 |
| exact_sum | 2038.1288089819586 |
| ulp | 0.0001220703125 |
| fused_total | 2038.107421875 |
| split_total | 2038.127685546875 |
| total_ulp_gap | 166 |
| relative_gap | 9.942396390646576e-06 |
| scale_ulp_gap | -59 |
| first_output_ulp_gap | -50 |
| merge_orders | 40,320 |
| distinct_merge_results | 3 |
| merge_spread_ulp | 2 |

| 切分段数 | 每段宽度 | 平方和 | 与精确值相距 / ULP | 缩放因子 | 首个输出 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 4096 | 2038.107421875 | -175.2 | 1.4176400899887085 | 1.1905962228775024 |
| 2 | 2048 | 2038.115478515625 | -109.2 | 1.4176373481750488 | 1.1905938386917114 |
| 4 | 1024 | 2038.1220703125 | -55.2 | 1.4176350831985474 | 1.1905919313430786 |
| 8 | 512 | 2038.127685546875 | -9.2 | 1.417633056640625 | 1.190590262413025 |
| 16 | 256 | 2038.1280517578125 | -6.2 | 1.4176329374313354 | 1.1905901432037354 |
| 32 | 128 | 2038.1287841796875 | -0.2 | 1.4176326990127563 | 1.1905899047851562 |

8 个局部和的 40,320 种合并次序共给出 3 个不同的 FP32 结果，彼此相距 2 ULP：`2038.1275634765625, 2038.127685546875, 2038.1278076171875`。

结合律反例：`(1 + 2⁻²⁴) + 2⁻²⁴ = 1.0`，`1 + (2⁻²⁴ + 2⁻²⁴) = 1.0000001192092896`。

计量条件：

- 教学行由给定公式生成并舍入到 BF16，不是采集到的激活。平方在 FP32 中精确，因此各路径的差异只来自加法次序。
- 每段内部按顺序累加，段间再合并；exact_sum 用有理数求得，只作比较基准，不是任何 kernel 的输出。
- ULP 取 FP32 在该和所在区间上的间距；offset_ulp 是与精确值的距离，不是误差上界，拆得更细也不保证更准。
- 枚举全部合并次序覆盖原子加可能出现的次序，不代表某个后端的实际分布；并发调度还可能改变段内划分。
- 缩放因子与输出按官方 rms_norm_eps 计算，只取一行，不乘层数，也不换算为端到端的质量差异。

固定来源：

- [configs/models/qwen3-8b/config.json](https://huggingface.co/Qwen/Qwen3-8B/resolve/b968826d9c46dd6066d109eabc6255188de91218/config.json)，SHA256 `f7c4eadfbbf522470667b797a3c89be2524832d2d599797248dc304fff447c30`。
- [sources/qwen3-8b/model.safetensors.index.json](https://huggingface.co/Qwen/Qwen3-8B/resolve/b968826d9c46dd6066d109eabc6255188de91218/model.safetensors.index.json)，SHA256 `f9fdbcb91c23971c13ec5d5f2573d2349e8f61f2f049371ec699281748fdb1bc`。
- [sources/qwen3/modeling_qwen3.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3/modeling_qwen3.py)，SHA256 `704c914530530a1acb0b443add1f520404e3ac2c28c0ab7e16f80f86cfe8ccb2`。
- [sources/qwen3/modeling_qwen3_moe.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3_moe/modeling_qwen3_moe.py)，SHA256 `3af43d01f9f902c8009b6dd7d7b8b563561b53dd0aa54175f585ae90d049fdb8`。
