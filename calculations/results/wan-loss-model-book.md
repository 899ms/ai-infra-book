# wan-loss-model — 

输入：`{"declared_model_seconds": "0.038", "fec_extra_losses": [0, 1], "fec_symbol_bytes": 1448, "fec_target": "0.999", "knee_bits_per_second": 333000000, "loss_probability": "0.14", "mss_bytes": 1448, "reference": null, "request_bytes": 354640, "rtt_seconds": "0.2"}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| mathis_mbit_per_second | 0.15479771131567618 |
| bbr_ideal_goodput_mbit_per_second | 286.38 |
| bdp_bytes | 8,325,000.0 |
| packets | 245 |
| expected_losses | 34.3 |
| serial_budget_seconds | 0.2465198798798799 |
| expected_completion_seconds | 0.7639545776801243 |
| p99_completion_seconds | 1.2465198798798798 |
| expected_rounds | 3.587173489001222 |
| p99_rounds | 6 |
| fec_repair_symbols | 63 |
| fec_overhead_ratio | 0.2571428571428571 |

计量条件：

- 路径参数（RTT、拐点、擦除率、MSS、请求大小、模型时间）取自鹊桥路径文档并在 docstring 逐行引用；文档中的测量值只作对照行，不参与推导。
- Mathis 公式给出独立随机丢包下 TCP 的稳态速率；BBR 理想行假定以拐点速率 pacing、cwnd=2×BDP、丢包只损失有效载荷 (1-p)。
- 可靠流模型：n=ceil(大小/MSS) 个报文独立丢失，每轮 RTT 一次理想选择性重传（重传也可能再丢），完成 = 串行预算 + 额外轮数×RTT。不含拥塞窗口收缩、慢启动或 RTO，因此是有利于 TCP 的下界。
- 串行预算 = RTT + 模型时间 + 请求按拐点速率串行化；文档用约 200 ms 往返和 30 ms 模型给出约 230 ms 的下限，本模块另加串行化项。
- FEC：k 个数据符号加 r 个修复符号，块内丢失不超过 r 即可恢复，用二项分布尾精确求最小 r；额外容忍行给出比最小 r 再多承受的丢失数。不模拟符号大小对时延的影响或分块策略。

固定来源：

