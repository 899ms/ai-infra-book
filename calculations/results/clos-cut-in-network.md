# clos-cut — 

输入：`{"gradient_dtype": "FP32", "link_bytes_per_second": 50000000000, "mode": "in_network", "model": "qwen3-8b", "nic_bytes_per_second": 50000000000, "oversubscription": "1", "pairing": "aligned", "partition_endpoints": 1024, "radix": 64, "rails": 8, "results_glob": "gradient-*.json", "server_counts": [2, 4, 8, 16, 32], "servers": 2, "startup_ns": 833, "supernode_scenario": "scenarios/supernode-scaling-example.json", "tiers": [2, 3]}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| results_found | 4 |
| bf16_nic8_switch_cross_server_bytes | 201,326,592 |
| bf16_nic8_switch_per_nic_seconds | 0.00025249124 |
| bf16_nic8_hierarchical_cross_server_bytes | 201,326,592 |
| bf16_nic8_hierarchical_cross_server_seconds | 0.00025332424 |
| bf16_nic8_hierarchical_cross_server_rounds | 2 |
| bf16_nic8_switch_over_ring_at_32_servers | 0.4682407172368856 |
| fp32_nic1_switch_cross_server_bytes | 402,653,184 |
| fp32_nic1_switch_per_nic_seconds | 0.00050414948 |
| fp32_nic1_hierarchical_cross_server_bytes | 402,653,184 |
| fp32_nic1_hierarchical_cross_server_seconds | 0.00402819784 |
| fp32_nic1_hierarchical_cross_server_rounds | 2 |
| fp32_nic1_switch_over_ring_at_32_servers | 0.49098055662400897 |
| fp32_nic8_switch_cross_server_bytes | 402,653,184 |
| fp32_nic8_switch_per_nic_seconds | 0.00050414948 |
| fp32_nic8_hierarchical_cross_server_bytes | 402,653,184 |
| fp32_nic8_hierarchical_cross_server_seconds | 0.00050498248 |
| fp32_nic8_hierarchical_cross_server_rounds | 2 |
| fp32_nic8_switch_over_ring_at_32_servers | 0.49098055662400897 |
| fp32_nic2_switch_cross_server_bytes | 402,653,184 |
| fp32_nic2_switch_per_nic_seconds | 0.00201409892 |
| fp32_nic2_hierarchical_cross_server_bytes | 402,653,184 |
| fp32_nic2_hierarchical_cross_server_seconds | 0.006293122 |
| fp32_nic2_hierarchical_cross_server_rounds | 2 |
| fp32_nic2_switch_over_ring_at_32_servers | 0.5095954488550292 |

计量条件：

- 交换机侧归约（SHARP 类）：本地 ReduceScatter 后每 rank 把自己的分片发给交换机一次、收回归约结果一次，跨服务器阶段只有一轮；本地 RS/AG 阶段与分层方案相同，不重复计。
- 对照数据直接读取 results/ 中的 hierarchical-gradient 结果（跨服务器阶段的轮数、字节与屏障下界），本模块不重算环。网卡速率取该结果声明的 nic0.tx 速率。
- 不声称交换机归约引擎的吞吐、精度或可用性；时间只是每网卡分片串行发送加一次启动的下界。
- servers_sweep 把跨服务器阶段推广到 S 台服务器：同一分片的 S 个持有者做环形 AllReduce，每网卡 2(S-1)/S×分片、2(S-1) 轮；交换机归约保持 1 个分片、1 轮。两台服务器时字节相同，只省一轮启动；服务器越多差距越大。

固定来源：

