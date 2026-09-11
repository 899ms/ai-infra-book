# clos-cut — 

输入：`{"gradient_dtype": "FP32", "link_bytes_per_second": 50000000000, "mode": "clos", "model": "qwen3-8b", "nic_bytes_per_second": 50000000000, "oversubscription": "3", "pairing": "aligned", "partition_endpoints": 1024, "radix": 64, "rails": 8, "results_glob": "gradient-*.json", "server_counts": [2, 4, 8, 16, 32], "servers": 2, "startup_ns": 2000, "supernode_scenario": "scenarios/supernode-scaling-example.json", "tiers": [2, 3]}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| radix | 64 |
| oversubscription | `"3"` |
| leaf_downlinks | 48 |
| leaf_uplinks | 16 |
| tier2_endpoints | 3,072 |
| tier2_total_switches | 80 |
| tier2_bisection_bytes_per_second | 25,600,000,000,000.0 |
| tier2_bisection_fraction_of_nonblocking | `"1/3"` |
| tier3_endpoints | 98,304 |
| tier3_total_switches | 3,584 |
| tier3_bisection_bytes_per_second | 819,200,000,000,000.0 |
| tier3_bisection_fraction_of_nonblocking | `"1/3"` |
| partition_endpoints | 1,024 |
| partition_cut_bytes_per_second | 17,600,000,000,000.0 |
| partition_cut_bytes_per_second_per_endpoint | 17,187,500,000.0 |
| supernode8_egress_bytes_per_second | 133,333,333,333.33333 |
| supernode64_egress_bytes_per_second | 1,066,666,666,666.6666 |
| supernode128_egress_bytes_per_second | 2,133,333,333,333.3333 |
| supernode256_egress_bytes_per_second | 4,266,666,666,666.6665 |

计量条件：

- k 端口交换机的折叠 Clos：叶层每台 d 下行、u 上行，d/u 为声明的超额订阅比；上层保持对叶上行不阻塞。二层为叶—脊，三层沿用 fat-tree 论文的 pod 结构（每 pod k/2 台边缘交换机）。
- 半分带宽按顶层链路计：所有叶上行数的一半乘每链路速率；不模拟具体流的路由、ECMP 冲突或队列。
- 分区割集只对占用整数个叶（或 pod）的分区成立；不足一叶时按向上取整计入整叶上行。每端点份额 = 割集/端点数。
- 超节点出口取 supernode-scaling 场景的每卡 NIC 速率乘卡数，再除以超额订阅比；跨域字节读取已有结果文件，本模块不重算梯度同步。

固定来源：

