# ub-fabric — 

输入：`{"apps_per_host": 8, "channel_bytes": 56, "clock_hz": 322000000, "context_cache_bytes": 262144, "cqe_poll_host_ns": 70, "cqe_poll_onchip_ns": 5, "directory_lines": 1048576, "directory_tag_bytes": 8, "dram_row_ns": 30, "endpoint_counts": [1, 8, 64, 256, 1024], "fpga_luts": 871680, "gating_max_cycles": 50, "host_counts": [2, 8, 64, 192, 384, 1024], "ioctl_ns": 5000, "isolation_release_cycles": 78, "jetty_bytes": 20, "ldst_pipeline_cycles": 8, "link_ns": 100, "link_sweep_ns": [50, 100, 200, 500], "local_dram_ns": 70, "membus_ns": 30, "oob_rtt_ns": 500000, "pcie_dma_read_ns": 500, "pcie_dma_write_ns": 250, "pcie_mmio_ns": 150, "psn_serialize_ns": 50, "qp_bytes": 512, "roce_bram": 67, "roce_cadence_cycles": 8, "roce_cold_cycles": 9, "roce_cycles_per_request": 6, "roce_flipflops": 91900, "roce_luts": 46636, "roce_pipeline_cycles": 9, "segment_bytes": 32, "setup_cores": 32, "ub_bram": 328, "ub_cold_cycles": 24, "ub_flipflops": 194266, "ub_initiation_interval_cycles": 2, "ub_luts": 122710, "urma_pipeline_cycles": 25, "verb_poll_ns": 30, "verb_post_ns": 50, "wqe_construct_ns": 30}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| endpoints_max | 1,024 |
| ub_state_bytes_max | 110,592 |
| roce_state_bytes_max | 536,903,680 |
| state_ratio_max | 4,854.8 |
| roce_spill_endpoints | 23 |
| ub_spill_endpoints | 2,428 |
| roce_refetch_ns | 1,000 |
| ub_refetch_ns | 200 |
| ub_loadstore_round_trip_ns | 419.4 |
| ub_urma_round_trip_ns | 745.6 |
| roce_dma_round_trip_ns | 2,221.8 |
| roce_pcie_ns | 1,650.0 |
| round_trip_ratio | 5.3 |
| apps_per_host | 8 |
| roce_max_hosts_in_cache | 8 |
| ub_max_hosts_in_cache | 4,674 |
| roce_setup_parallel_s_max | 17.03936 |
| ub_setup_parallel_s_max | 0.01632 |
| setup_ratio_max | 1,044.1 |
| ub_requests_per_us | 161.0 |
| roce_requests_per_us | 53.67 |
| ub_lut_share | 0.1408 |
| extra_cold_ns | 46.6 |

计量条件：

- 每条记录的字节数取自 OpenURMA 实现的状态结构（Jetty 20 B、内存段 32 B、TP 通道 56 B）与其 RoCE RC 对照的 QP 上下文 512 B；同类字段的正式规范可能更大，比例的量级不变。
- 端点状态按 N 个本地端点访问 M=N 个远端端点的全连接计算：UB 为 N(Jetty+段)+M×通道，RoCE 为 N×M×QP+N×段。这是可共享的核心硬件状态，不含页表、未完成请求和软件映射。
- 上下文缓存按字节容量判断是否溢出；论文仿真器按条目数（RoCE 512 条 QP、UB 2048 条通道）判断，因此 UB 的溢出点在论文中为 1024 端点，这里为字节口径的结果。溢出后每次操作在两端各多一次上下文重取。
- 一次 64 B 远程读取的各阶段延迟为声明值：片上总线 30 ns、PCIe MMIO 150 ns、PCIe DMA 读 500 ns、写 250 ns、线路单程 100 ns，NIC 流水线按周期数乘 322 MHz 时钟。各阶段全部串行在关键路径上；论文仿真值作为对照记录，不参与推导。
- 主机数算例假设每台主机 A 个应用端点、主机之间全连接，每台主机的 NIC 只保存自己发起方向的状态；目录式一致互联按每缓存行为每个对端保留 1 bit 加固定标签计算。
- 连接建立按每个对象的控制操作计数：RoCE 每条 QP 需 4 次系统调用与 1 次带外往返，UB 每个 Jetty 1 次系统调用、每条通道 1 次系统调用与 1 次往返；并行核数只把串行总时间等分，不建模内核锁竞争。
- 请求速率由流水线最慢级的启动间隔决定，UB 取 II=2 周期；RoCE 取每请求 6 周期的序号分配依赖。面积与周期数为论文报告的综合结果，不是推导值，用来与推导出的每操作节省作比较。

固定来源：

- [../references/files/papers/openurma.pdf](https://arxiv.org/abs/2605.28717)，SHA256 `793c1c62eeeb6fc7dcf4fa52d4ca44e78255d52a9d50a9bb453dc2e5c9ed7964`。
