# hash-collision — 

输入：`{"flows": 8, "spray_model": "qwen3-8b", "spray_packet_bytes": 4096, "spray_path_bytes_per_second": 50000000000, "spray_path_delays_ns": [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000], "spray_paths": 8, "spray_tokens": 1024, "uplinks": 32}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| flows | 8 |
| uplinks | 32 |
| ideal_load_per_uplink_exact | `"1/4"` |
| expected_max_load_exact | `"7149497699/4294967296"` |
| expected_max_load | 1.6646221510600299 |
| expected_max_over_ideal | 6.6584886042401195 |
| p99_max_load | 3 |
| probability_no_collision_exact | `"828316125/2147483648"` |
| probability_no_collision | 0.38571475306525826 |
| expected_empty_uplinks_exact | `"852891037441/34359738368"` |
| expected_empty_uplinks | 24.82239615175058 |
| effective_uplinks_exact | `"34359738368/7149497699"` |
| effective_uplinks | 4.805895436934807 |
| effective_fraction_of_nominal_cut_exact | `"1073741824/7149497699"` |
| effective_fraction_of_nominal_cut | 0.15018423240421272 |

计量条件：

- 每条流独立、均匀地哈希到 m 条等速上行；流大小相同。这是 ECMP 的教学模型，不是具体交换机哈希函数或实际流量分布。
- n 条流是同一台叶交换机（多轨拓扑中的同一条 rail）上必须穿过脊层的流，m 是该叶的上行数（clos-cut 结果：k=64 无阻塞叶 32 条，3:1 超额订阅叶 16 条）。错位配对的八条流从八台不同的叶交换机出发，彼此不会在同一叶的上行上冲突，因此不构成一个 n=8、m=8 的场景。
- 最大负载分布用截断指数多项式精确计算（有理数），期望与 99 分位均为精确值；不做模拟。
- 有效割集 = 理想每链路流数 / E[最大负载]：假定各流受最忙链路限速到同一速率（公平共享），其余链路的空闲容量不能被已经分配的流使用。
- 逐包喷洒复用 packet-reorder 模型：按序号轮转路径、各路径独立串行、无丢包，接收端按连续前缀交付。路径延迟为声明输入；乱序等待 = 完成时刻减去理想并行传输加最长路径延迟。

固定来源：

