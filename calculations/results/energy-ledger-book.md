# energy-ledger — 

输入：`{"area_after_over_before": "0.60", "chapter1_context_tokens": 2048, "declared_air_cooling_kw_per_rack": "40", "declared_phone_channels_x16": 4, "decode_result": "results/qwen3-8b-decode-b1-s8192.json", "power_after_over_before": "0.75", "rack_budget_kw": "120", "rack_card_counts": [64, 72, 96], "rack_fixed_kw": "12", "rack_per_card_kw": "1.2", "sources_extract": "research/gap-plan-2026-09-11/sources-extract.json", "voltage_after": "0.55", "voltage_before": "0.85"}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| weight_read_bytes | 15,136,819,200 |
| kv_read_bytes | 1,207,959,552 |
| kv_read_bytes_at_chapter1_context | 301,989,888 |
| matrix_flops | 19,968,622,592 |
| extract_present | `true` |
| hbm_pj_per_byte | 31.76 |
| joules_per_token_weights | 0.480745377792 |
| joules_per_token_kv | 0.03836479537152 |
| joules_per_token_compute | 0.014976466944 |
| joules_per_token_total | 0.53408664010752 |
| dynamic_power_ratio | 0.4186851211072664 |
| power_density_ratio | 1.25 |
| rack_max_cards | 90 |
| phone_bus_gb_per_second | 85.6 |

计量条件：

- 一步 decode 的权重、KV 读取字节与矩阵 FLOPs 直接读取已有结果文件，本模块不重算前向；第 1 章的 2048 token KV 行按同一文件的每 token 字节乘 2048。
- 各层次每字节能耗、每 FLOP 能耗、手机总线与 MELTing point 参考行只在 sources-extract.json 存在且给出该行时出现，附带其 node/date/source；缺失时对应字段为空，不用占位数。
- 按层次的 J/token 阶梯是"若全部字节都来自该层次"的对照，不是真实数据路径；权重/KV/计算三分账按 HBM 每字节能耗与每 FLOP 能耗相加，不含控制、时钟或静态功耗。
- 电压项只解释 V^2 的影响，不能单独复现论文的 66%；功率密度用投影面积，不与各层硅面积之和混用。
- 机柜线性功率模型与第 6.5.2 节一致；风冷上限为声明输入（来自归档冷却指南时在场景中注明来源），缺省时不做判断。

固定来源：

