# 三控制器 ACK 聚合原书大例：完整 trace 独立审查

三份正式结果均已实际按数组流式审查，PASS。`check-large-independent.py` 为可重运行脚本，逐控制器结果为 `large-independent-{newreno,cubic_hystart,bbr}.json`，输入比较见 `large-comparison-independent.json`。本审查读取完整结果而非作者摘要；所有正式结果 SHA、依赖源码 SHA 均在运行开始和结束校验。

受审新 calculate SHA 为 `58718e22f3e29cba582f7ce2fdaf5f701b9bbb45acf8e71cd22a0253c64e6ae2`，receiver 为 `a8a44b09c95d76501821a20a4737fdc352d564de706f98082b2c5f7f55949378`。新版本增加实际 sender `rtt_samples` 输出。旧未导出样本的大结果已由作者保存在 `pre-rtt-output/`；这里的最终通过证据针对新版本。

三输入仅 controller.name 不同：30MB 上传、5MB 响应、0.3s 模型，上/下行 20/100Mbps、各向 50ms，统一 in-flight padding 和 every=2/max_delay=10ms。没有将 ACK 数设为 ceil(data/2)。

| 控制器 | ACK 上行/下行 | ACK 合计 | 全部线上字节 | 完整响应时间 |
|---|---:|---:|---:|---:|
| NewReno | 2,144 / 12,846 | 14,990 | 38,177,328 | 14.564459796s |
| CUBIC+HyStart++ | 2,144 / 12,846 | 14,990 | 38,177,328 | 14.564459796s |
| BBR 参考适配 | 2,141 / 12,843 | 14,984 | 38,176,776 | 14.996386157s |

每例数据包均为上行 25,685、下行 4,281；原始有效字节恰好 35,000,000，逐 offset 检查为连续不重叠分区，而不是只检查 union。padding 上行 80B、下行 208B。逐包核物理服务时长与每向 serializer 互斥、传播 50ms、PN 递增、无实际 drop/probe/recovery。原始数据线上 36,798,248B 加每个 ACK 92B，精确得到上表。

所有 ACK 均由真实接收时间独立重建最近 256 PN 与未首次报告数据集合；范围不确认未来包，最大 PN 的第一次到达决定 raw delay。逐字段核 varint 字节、floor 编码和量化余数，并核实际到达 ACK 对应发送方 ranges/decoded_delay 输入。最大 ACK frame 为 10B，raw delay 最大 10ms，超期次数为零。这是这三条实际轨迹的结论，不是接收策略保证永不排队超期；独立小网络已有明确超期反例。

真正导出的 sender RTT 样本逐份验证：NewReno 和 CUBIC 各 14,990，BBR 14,984。资格由 ACK 范围、首次确认身份、实际发送时间与被宣告丢失时间重建；raw RTT 从物理 ACK 到达减发送时刻得出。逐样本核 peer cap、minRTT 下界、首次样本不扣 delay、adjusted 值、使用旧 SRTT 的 variance 更新，以及事件间声明的 1e-12 网格舍入。最终 minRTT 也与独立递推相符。本大例没有最大 PN 为 pure ACK 的合格样本，因此该特殊边界仍由专项小例覆盖，不能虚增本大例覆盖范围。

BBR 另核实际发送快照、首次 ACK 的 transport packet delivered、选中最新发送 PN、send/ACK interval、整数带宽、发送时 app/flowlimited 标记和 ACK 前后 flight。selected snapshot 内 acked 状态随 ACK 改变是合法状态更新；对照保持不变的发送字段，不将 acked=False 的原发送状态误当永久不变。BBR 回调实际取 **raw RTT** 微秒，而发送方 RTT 估计器另外使用 adjusted RTT；两条数值路径已分别核对，未混同。

loss 数组不为空：NewReno/CUBIC 各 12,591、BBR 12,589 条，全部是下行 **pure ACK 身份**，没有 data 身份 loss。这些旧纯 ACK PN 因有限保留范围不再得到后续覆盖，被发送方记录为丢失；不能表述成应用数据丢包率。真实数据均一次发送，业务唯一贡献没有重复。业务时刻逐包验证：完整上传到达触发模型，恰好 0.3s 后允许响应，完整响应取最后必要数据到达而非最后 ACK。

每条 sender/pacer 数值日志均检查差值、网格和局部舍入界；具体条数和最大误差在三个 JSON 中。sender 最大绝对局部误差为 0.5×10^-12；pacer 使用其独立单位与上取整界，未宣称这些局部界就是完整轨迹累计误差界。

CUBIC 上行实际仅 slow_start，下行 initial_waiting_for_ack/slow_start，没有观察到 CSS 或 avoidance，不能据此比较 CUBIC avoidance 性能。BBR 上行实际观察 STARTUP/PROBE_BW/PROBE_RTT，下行 STARTUP/PROBE_RTT。此审查核有限 QUIC 网络与固定控制器适配的轨迹一致性，不将其称为真实 Linux TCP、浏览器默认 ACK 策略或完整拥塞算法网络实现的通用证明。
