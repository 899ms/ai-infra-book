# incast-feedback — 

输入：`{"declared_end_to_end_rtt_ns": 20000, "declared_one_hop_cable_m": 30, "declared_propagation_ns_per_m": 5, "egress_bytes_per_second": 50000000000, "free_buffer_bytes": 4194304, "mtu_bytes": 1500, "sender_bytes_per_second": 50000000000, "senders": [8, 16, 64]}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| free_buffer_bytes | 4,194,304 |
| one_hop_feedback_ns | 330.0 |
| end_to_end_feedback_ns | 20,000 |
| allowed_feedback_ns | `{"8": 13981.013333333334, "16": 5991.862857142857, "64": 1353.0012903225806}` |
| end_to_end_fits | `{"8": false, "16": false, "64": false}` |
| one_hop_fits | `{"8": true, "16": true, "64": true}` |

计量条件：

- N-1 个发送方同时以速率 B 向一个出口发送，出口速率 B_out；反馈到达前积压以 (N-1)B - B_out 线性增长，允许的反馈时延 = 空闲缓冲/超额速率。流体模型，无报文粒度、无 ECN 概率标记。
- 一跳暂停的反馈距离 = 暂停帧上行传播 + 已在线数据下行传播 + 一个 MTU 的串行化；线缆长度与每米传播时延是声明输入。端到端反馈距离取声明 RTT。均不含交换机处理与排队时延。
- fluid_check 用本模块的单次反馈流体队列复算：反馈时延取允许值向下取整 ns，反馈后发送降为 0，确认不丢包；这是自洽检查，不是协议模拟。
- 需要的缓冲 = 反馈距离 × 超额速率，是单个出口端口、单优先级的下界；实际交换机按端口/优先级预留 headroom（DCQCN 论文给出每端口每优先级 22.4 KB 的一例，随 MTU 与链路而变）。

固定来源：

