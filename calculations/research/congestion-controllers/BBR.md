# 固定 Linux v6.6 BBR：选定函数的纯状态参考

`bbr_reference.py` 是固定 `ffc253263a1375a65fa6c9f62a893e9767fbebfa` 的 `tcp_rate.c`／`tcp_bbr.c` 函数级参考。运行 `python3 calculations/research/congestion-controllers/bbr_scenarios.py` 生成 `bbr-results.json`。脚本按 `../congestion-controller-inputs/sources.lock.json` 重读核验4份原件。没有下载/改写新原件，没有把这个参考接入QUIC反馈或公共计算。

## 事件、整数单位与回调映射

rate_sample的起点是TCP核心已经运行`tcp_rate_skb_sent`记录快照、`tcp_rate_skb_delivered`选择采样skb之后；该参考没有实现skb选择或SACK scoreboard。输入`prior_delivered`和`prior_mstamp_us`来自该skb发送时快照，`send_interval_us`来自该skb发送阶段，`total_delivered`和`now_us`来自ACK/SACK处理后的发送端TCP状态。不能由接收端完成时刻免费给出，不可拿当前ACK的新包数或相邻ACK间隔替代。

`rate_sample()`实现这段纯算术：u32 delivered差、max(send_interval,ACK_interval)、缺快照/SACK reneging/小于minRTT的无效样本、整数BW。BW单位为packets/μs×2²⁴；对照100segments/s原始值对应整数1677。负值为内核无效约定，本接口用`valid=False`保留明确reason；零区间在BBR入口也无效。时间输入是非回绕微秒单调时钟；u32 delivered差超过有符号半域则拒绝，避免把任意回退当回绕。

`StartupDrain.update()`按固定源顺序处理packet-round、full_bw和drain门槛。这里`filtered_max_bw`必须是**上游Linux minmax滤波输出**，不是无声明地拿当前sample代替；`packets_in_net_at_edt`必须是上游EDT估计，`drain_target`必须来自上游bbr_inflight，而非原始flight或任意“BDP”。这些字段本轮场景是明确状态种子，因此只证明指定函数的状态转换。packet round用u32 `!before(prior_delivered,next_rtt_delivered)`，不是墙钟每RTT自动递增。

CWR/Recovery/Loss由TCP核心选择。`recovery_cwnd()`只对应`bbr_set_cwnd_to_recover_or_restore`，进入Recovery开启packet conservation并设置cwnd=inflight+acked；退出恢复到max(current,prior_cwnd)。调用者还须把函数返回的“reset round”映射到当前tp->delivered；本函数不自动维护StartupDrain对象。其返回值是**target/cap应用前的cwnd**。完整`bbr_set_cwnd`在acked=0时跳过该helper，调用者不得把本helper单独作用于所有零ACK回调后称完整内核行为。

没有`on_packet_sent`网络回调实现；也没有QUIC PN、ACK ranges、PTO与TCP SACK之间的隐含映射。因此不能称“Linux TCP仿真”或“QUIC内核BBR性能”。

## 本轮具体函数与已验证结果

| 函数/分支 | 已覆盖边界 |
| --- | --- |
| rate_sample | ACK压缩send100ms/ACK20ms取100ms；10包BW整数1677；缺时间戳、interval<minRTT无效 |
| before | equality、新round阈值、u32回绕；要求serial距离小于2³¹ |
| pacing_bytes_per_second | 按源码乘MSS/gain、右移8、乘990000、右移24，含1%margin；1677、MSS1500、gain739得到428493B/s；u64溢出范围拒绝 |
| bdp_packets | 固定乘法/右移/向上整包舍入；无RTT的0xffffffff返回TCP_INIT_CWND10；不是将未知RTT置零 |
| quantization_budget | 外部给定TSO目标，增加3×TSO，向上偶数；PROBE_BW phase0另+2 |
| STARTUP full_bw | 1000→1200阈值1250，三个合格新round计数1/2/3；app-limited或非新round不计数 |
| 整数阈值纠正 | 内部10→12阈值是12，会更新full_bw并归零，不遵循抽象12<12.5的未舍入推论 |
| DRAIN | 达到full_bw进入DRAIN，flight20>target14保持；下一回调等于14可进入PROBE_BW边界 |
| recovery helper | loss扣除、进入Recovery、packet conservation、退出时restore；未应用后续target/global cap |
| PROBE_RTT出口门槛 | 必须至少一个round完成且now严格after(done_stamp)，相等时不退出；只实现出口布尔门槛 |

同样的高app-limited带宽可能进入上游max滤波，但不推进full_bw检测；两者是不同分支。此参考尚未实现max滤波，所以不能把本例的app-limited不计数概括为“所有app-limited样本丢弃”。

## 明确未完成的完整BBR行为

`StartupDrain`到PROBE_BW即停止，之后再次update明确抛ValueError；输出`pacing_gain=None`与`needs_probe_bw_phase_initialization=True`，不免费选相位、不偷偷保持STARTUP增益。以下工作仍须实现并验收：

- 固定Linux三样本minmax滤波及10-round窗口，长期policer分支、app-limited样本接纳；当前只消费外部值。
- PROBE_BW随机初相位和八相位转换（持续时间、gain、loss、inflight门槛），随机种子/取样映射。
- PROBE_RTT完整minRTT维护、10秒失效、idle_restart、进入/4包/200ms+round、prior_cwnd恢复；必须固定HZ和jiffies换算。已有布尔出口门槛不是完整模式。
- `bbr_update_ack_aggregation`及相应cwnd补偿；完整cwnd目标、min4、clamp、PROBE_RTT cap及acked=0路径。
- `bbr_packets_in_net_at_edt`、TSO目标、socket pacing cap及startup只增pacing条件；整数溢出和TSO/MTU单位边界。
- idle/TX_START、loss通知、save_cwnd/undo、TCP CA回调的完整组合。当前helper不检测网络拥塞、不决定重传、不实现ACK/SACK恢复。
- 与同反馈transport_profile的明确适配；若移植到QUIC恢复，记录原始样本来源与所有差异，而非改个名字。

当前文件和场景推进固定算法输入与关键分支验证，但不是控制器全过程交付；公共CLI、网络闭环与媒体拥塞对照均尚未接入。
