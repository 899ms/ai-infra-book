# BBR 状态接线候选：来源函数组合，不是TCP网络仿真

`bbr_state.py` 新增固定Linux v6.6状态回调组合；保留 `bbr_reference.py` 作为此前有限函数参考，不把旧报告覆写成新状态已验收。`bbr_minmax.py` 直接对应同commit `lib/win_minmax.c` 三样本近似，原件及 `include/linux/win_minmax.h` 保存于 `bbr-sources/`，另有 `bbr-sources.lock.json`。该max filter不是exact deque，独立C oracle已审查其全部三样本状态。

## 对外合同

`BBR(...)`构造已存在TCP socket的控制器状态，`Ack(...)`是TCP核心ACK/SACK处理之后的回调输入。`on_ack`按源顺序执行带宽与packet-round、ACK aggregation、PROBE_BW phase、full_bw、drain、minRTT/PROBE_RTT、gain、pacing、cwnd。给定独立快照的`on_ssthresh`、`on_ca_loss`、`on_undo_cwnd`、`on_tx_start`模拟相应TCP回调，不发现丢包、不执行重传、不生成ACK。

`delivered/interval_us/prior_delivered/app_limited`仍必须由skb采样流程提供，可使用此前rate_sample函数的有限算术输出，但未实现skb选择。`acked_sacked`是本次新确认数，与取样期间delivered不同；`total_delivered/total_lost`为发送端TCP累计u32计数。`inflight/prior_inflight`为TCP当前与此ACK前的包数；`edt_ns`为发送端下一包Earliest Departure Time。所有数量是TCP packet计数，不是媒体块数、字节或QUIC PN。

单调`now_us`提供微秒时间；jiffies由floor(now_us×HZ/1e6)再u32截断生成，HZ显式限制100/250/300/1000。该受控时钟映射不是任意Linux主机实时钟测量。`srtt_us_x8`使用Linux左移3位单位。`min_rtt_us=0xffffffff`表示尚无有效RTT，不替换成0。PROBE_RTT的200ms按msecs_to_jiffies向上舍入，出口严格after，deadline相等不退出。

`random_draws`是显式`get_random_u32_below(7)`返回值序列（每个0…6），用于可审查初相位，耗尽拒绝；不是声称复现内核随机数生成器。源初相位先7−draw再advance，结果(8−draw)&7。不能把“seed0”理解为Python random或内核PRNG相同流。

TSO计算依赖构建ABI宏。`max_tcp_header_bytes=256`与`gso_legacy_max_size=65536`是显式声明配置，前者不能从仅有tcp.h中`L1_CACHE_ALIGN(128+MAX_HEADER)`推出通用常数；构造参数及快照保留它们。MSS默认1500B、pacing_shift10、cwnd_clamp1000000和最大pacing1e12B/s也为场景声明。真实主机对照必须给匹配构建值。

## 已接入的状态路径

- 10个packet round的固定三样本max filter；低app-limited采样不更新，较高者可更新。
- STARTUP满带宽计数与DRAIN含EDT/TSO目标；八相位PROBE_BW的gain/时间/丢包/inflight门槛及显式初相位。
- PROBE_RTT的minRTT更新、10秒失效、idle_restart抑制、save/restore、4包、200ms与至少一round，回写给TCP核心的app_limited_until标记。
- ACK aggregation两窗口5-round轮换、20-bit epoch计数和16-bit excess存储、100ms带宽补偿限额。
- loss扣除、packet conservation、恢复退出、目标cwnd和clamp/min4/PROBE_RTT cap；零acked跳过recover helper、仍应用最终cap。
- pacing整数换算与socket cap、首次观察RTT重新初始化、STARTUP只增pacing；EDT预计交付与TSO budget。
- 长期policer两区间检测、app-limited重置、4…16round区间、20%近似整数loss阈值、48round退出、带宽一致性；undo和CA_Loss回调。

`bbr_state_scenarios.py`生成9份自检轨迹：启动/排空/8相位、PROBE_RTT、恢复、app-limited max、idle抑制、aggregation、HZ250、policer两个区间与48round过期、policer app-limited重置。每次运行先核验已有四个来源及两个新minmax原件。自身断言通过不替代独立源C回调对照。

## 审查与尚未宣称的交付

本候选新增完整状态接线后仍需逐回调独立C对照、各种字段类型与整数范围审查，不能把此前函数级检查数套作整个状态模块通过。极大bw乘法、u32/位域截断、恢复与PROBE_RTT交叠、持续应用受限、无有效RTT和时间回绕必须覆盖或明确拒绝。当前入口限制单次关键包计数不超过100万；部分函数对u64溢出主动拒绝，这是参考计算的受支持域，不是Linux运行时全域。

未实现TCP core，包括skb/TSO实际拆分、ACK/SACK选择、packet-in-flight计算、重传定时器/恢复检测、socket队列与拥塞网络。未接入transport-feedback，更没有把QUIC ACK/PTO当Linux回调。后续应通过显式适配层提供同一发送方反馈、网络与媒体业务，在完成相应校准和公共CLI前继续保留原C68缺口。

## 2026-09-09 后续输入修复与原样C逐回调对照

已修复有效sample的delivered与u32(total_delivered−prior_delivered)一致性，srtt_us_x8按u32、edt_ns按u64、interval_us/rtt_us按声明LP64 long范围校验；rtt_us写回u32 min_rtt_us时保持源码截断。构造的pacing_shift限定0…63，时钟转换限制u64纳秒范围。app-limited及aggregation场景的累计计数已修正，不再把不可能的采样值当合法TCP快照。

初始pacing_gain/cwnd_gain现在保持Linux零初始化，直到首个update_gains；初始socket pacing仍由bbr_init_pacing_rate_from_rtt计算。snapshot对可变列表做deep copy，防止后续ACK重写既往事件中的extra_acked记录。

`check-bbr-state-c.py`从固定tcp_bbr.c原样截取BW定义至get_info之前的全部算法代码，另原样提取bbr_set_state，合入已固定minmax原件。生成 `bbr-c-state-build/oracle.c` 并实际clang编译。C算法函数体没有重写成第二套Python算式；socket/TCP字段、时钟、随机返回、ABI宏和通用算术操作为显式测试桩，LP64通过static_assert约束。MAX_TCP_HEADER256等仍是声明构建配置。

当前C对照包含167个init/ACK/其他回调，逐次核验38个顶层字段（bw_filter另含全部3个t/v样本）：STARTUP/DRAIN/8相位、7个初相位返回值、PROBE_RTT/HZ250、恢复、aggregation、app-limited、policer/48round、idle、CA_Loss/undo，以及long interval和long RTT写回u32边界。`bbr-state-c-check.json`记录同次候选/harness/生成C哈希、范围和零差异；`bbr-state-c-trace.json`保存命令及逐次C/Python状态。运行后删除临时可执行文件，保留C源码供审核。

TX_START可额外给app_limited_until精确TCP marker，省略时声明布尔true对应marker1；这不推算真实管线marker。on_ack在模型更新前执行tcp_rate_gen的应用受限marker清理条件，然后控制器PROBE_RTT可能再次设置marker；该少量TCP字段适配是显式合同。C测试桩执行相同核心前置操作，不包含skb采样或网络事件。

这些是实现者编写、调用原样C的跨语言对照，尚不可称另一个审查者完成全部harness二审。独立review已复现并确认此前4个非法输入现在拒绝；该检查与全状态C覆盖明确分列。仍未接入媒体网络闭环，不声称全Linux TCP执行或任意参数全域覆盖。

### 独立审查后的时间差共同盲点修复

审查者发现最初C桩把tcp_stamp_us_delta写成u64正差，Python的cycle条件也用无限精度正差，导致共同漏掉u32回绕。现harness直接从固定tcp.h抽取原始helper函数，使用声明s64/u64类型；Python `stamp_us_delta`按u64差→解释s64→max(0)→u32返回实现。cycle、ACK aggregation及参考rate sample的ACK interval改用该helper。

新C对照覆盖cycle时间跨度2³²+1μs（返回1μs，不能仅因该差使phase前进），另有6个helper直接对照，含负差、u64回绕和s64半域。追加单条连续8phase转换轨迹，区别于此前7个不同初相位只观察到8个phase取值。当前报告为197个回调×38字段，以及6个helper检查，零差异。旧167回调结果不能作为该新增边界的证据。

复核其它桩：LP64有静态断言；TCP/BBR结构字段类型和原BBR位域保留；before为s32(u32差)，minmax为原C；pacing单位、MSS和ABI宏显式；HZ使用已声明有限值；随机桩返回本场景固定draw，对比同值序列。socket核心的flight/SACK/采样选择仍为外部输入，未扩大成真实Linux网络证明。
