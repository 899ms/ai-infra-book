# hash-collision — 

输入：`{"flows": 32, "spray_model": "qwen3-8b", "spray_packet_bytes": 4096, "spray_path_bytes_per_second": 50000000000, "spray_path_delays_ns": null, "spray_paths": 0, "spray_tokens": 1024, "uplinks": 16}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| flows | 32 |
| uplinks | 16 |
| ideal_load_per_uplink_exact | `"2"` |
| expected_max_load_exact | `"3210361610309472709419436342306270951/664613997892457936451903530140172288"` |
| expected_max_load | 4.830415279379875 |
| expected_max_over_ideal | 2.4152076396899376 |
| p99_max_load | 8 |
| probability_no_collision_exact | `"0"` |
| probability_no_collision | 0.0 |
| expected_empty_uplinks_exact | `"43143988327398919500410556793212890625/21267647932558653966460912964485513216"` |
| expected_empty_uplinks | 2.028620582032006 |
| effective_uplinks_exact | `"21267647932558653966460912964485513216/3210361610309472709419436342306270951"` |
| effective_uplinks | 6.624689213907119 |
| effective_fraction_of_nominal_cut_exact | `"1329227995784915872903807060280344576/3210361610309472709419436342306270951"` |
| effective_fraction_of_nominal_cut | 0.4140430758691949 |

计量条件：

- 每条流独立、均匀地哈希到 m 条等速上行；流大小相同。这是 ECMP 的教学模型，不是具体交换机哈希函数或实际流量分布。
- n 条流是同一台叶交换机（多轨拓扑中的同一条 rail）上必须穿过脊层的流，m 是该叶的上行数（clos-cut 结果：k=64 无阻塞叶 32 条，3:1 超额订阅叶 16 条）。错位配对的八条流从八台不同的叶交换机出发，彼此不会在同一叶的上行上冲突，因此不构成一个 n=8、m=8 的场景。
- 最大负载分布用截断指数多项式精确计算（有理数），期望与 99 分位均为精确值；不做模拟。
- 有效割集 = 理想每链路流数 / E[最大负载]：假定各流受最忙链路限速到同一速率（公平共享），其余链路的空闲容量不能被已经分配的流使用。
- 逐包喷洒复用 packet-reorder 模型：按序号轮转路径、各路径独立串行、无丢包，接收端按连续前缀交付。路径延迟为声明输入；乱序等待 = 完成时刻减去理想并行传输加最长路径延迟。

固定来源：

