# CUBIC / BBR 纯状态候选：独立来源合同

本文件审查算法合同、依赖和实现前可复核期望，不修改作者代码或冻结的transport-feedback。独立期望见 `independent-oracles.json`（9组CUBIC、10组BBR），其数值从规范/固定源码手算，未调用候选函数生成。BBR接口已经落盘后才完成本文件，因此不声称所有期望都早于代码文件创建；期望早于本审查调用候选执行，CUBIC状态实现也尚未由本审查运行。最终候选正确性仍须实际执行这些边界验证。

## 固定来源与实际阅读

CUBIC使用本目录 `sources.lock.json` 的RFC9438和RFC5681官方原件，逐份复制后重新读bytes/SHA。BBR使用 `../congestion-controller-inputs/sources.lock.json` 中Linux v6.6 commit `ffc253263a1375a65fa6c9f62a893e9767fbebfa` 的 `tcp_bbr.c`、`tcp_rate.c`、`include/net/tcp.h`；本文件不改另一目录来源锁。具体源码版本不得写成可移动的master或“最新BBR”。

本次实际阅读全文相关段落：RFC9438§4.1–4.10、§5.8；RFC5681§3.1、§4.1；BBR的rate换算、BDP/quantization、update_bw、full_bw/Drain、ProbeRTT退出及idle回调；tcp_rate_gen的发送/ACK区间和无效样本条件。代码注释及类型定义是单位证据的一部分，不把变量名中的bytes/packets含义猜出来。

本轮另访问[官方RFC9438勘误查询](https://www.rfc-editor.org/errata/rfc9438)，实际重定向到官方errata站全文列表，仅返回技术勘误7806、状态**Rejected**（2024-02-26）。其建议把cwnd_prior改成flight_size未被采纳，不能按提案修改规范；本候选应保留§4.6的旧cwnd与flight_size各自用途。这不是全面确认未来永远没有勘误。原HTTP网页读取工具遇429，官方URL通过普通只读请求获得全文，未把失败页面当证据。

## CUBIC：从ACK状态到窗口，不只是画曲线

依据[RFC9438](https://www.rfc-editor.org/rfc/rfc9438.txt)，单位固定segments/seconds，或明确SMSS映射到bytes。需要区分cwnd、cwnd_prior、cwnd_epoch、W_max、W_est、K与epoch时钟。

- W_cubic是目标函数，不是没有ACK也可自动生效的窗口。新ACK触发更新；Reno-friendly的W_est使用新确认segments_acked，非Reno分支依§4.4/4.5每个新ACK增量为 `(target-cwnd)/cwnd`，不额外乘segments_acked。target须夹在当前cwnd与1.5cwnd之间。
- W_est达到cwnd_prior后的alpha切换，以及loss时保存旧cwnd、用flight_size乘beta、fast convergence对W_max的调整，各有独立状态。不能用同一变量替代这几个量。
- 受应用或接收窗口限制的时间必须排除在有效立方时钟外；只略过该时刻ACK增长但让数十秒idle继续累计t仍不正确。恢复epoch、重复拥塞事件与新ACK数量由外部给出，纯控制器不自行确认网络PN或推断实际loss。

当前作者 `CUBIC-CONTRACT.md` 选择明确的 **RFC5681 Reno启动参考**，包含每ACK `min(segments_acked,1)`，没有实现通常推荐的HyStart++。这个可审分支不等于证明HyStart++不适用，也不能推荐为RFC9438的默认完整启动。若下一阶段要符合常规推荐，应另外固定RFC9406及其RTT轮次/退出条件并接实测样本；本轮不靠任意ssthresh常数伪装实现HyStart++。[RFC9438启动条款](https://www.rfc-editor.org/rfc/rfc9438.html#section-4.10)

RFC5681还决定TCP超时后的窗口和idle重启政策。timeout回调与QUIC PTO必须区别：stage1 PTO不会宣布loss，更不能把每个PTO都传给CUBIC的TCP timeout。这里smoothed_rtt、idle时长/RTO和恢复退出是已知外部输入，不由纯状态函数执行RFC6298估计器或SACK/PRR。因此6298、6582/6675、9406等是后续完整集成可能需要的依赖，不能因9438引用它们就声称本目录已实现。

一般K不是有理数。完全立方小例可精确核对；其它值应明确立方根区间、近似点、分支不确定性和状态量化记录。局部舍入误差不是整条轨迹相对实数解的累计误差上界。外部输入也必须限制预算、时间单调、重复事件及不合法状态，而非接受任意不可达seed后默默制造负窗口。

## BBR：固定Linux回调契约，不能把QUIC事件改名

[固定tcp_bbr.c](https://github.com/torvalds/linux/blob/ffc253263a1375a65fa6c9f62a893e9767fbebfa/net/ipv4/tcp_bbr.c)及[固定tcp_rate.c](https://github.com/torvalds/linux/blob/ffc253263a1375a65fa6c9f62a893e9767fbebfa/net/ipv4/tcp_rate.c)需要保留整数运算的单位、顺序和上下游边界。窗口/交付计数通常是TCP segments；带宽样本为packets/µs乘2^24，gain乘256。MSS换算、移位、99% pacing margin和溢出域不可换成浮点近似后仍叫位精确。

`rate_sample`只对应上游 `tcp_rate_skb_delivered` 已选定skb后的算术。它接收保存于发送时的prior_delivered、prior时间戳与当前累计delivered，不是本次ACK确认bytes除相邻ACK时间。分母取发送阶段和ACK阶段较大者；零prior时间戳、SACK reneging、短于minRTT等会使样本无效。Linux中零prior时间戳是该函数明确的无效哨兵，不应照搬上一RFC模型“所有零时间都改None”的处理。

当前 `bbr_reference.py` 的覆盖是有限函数与STARTUP→DRAIN→PROBE_BW入口，已知外部量包括：

| 外部输入 | 尚未由当前有限函数产生的真实上游工作 |
|---|---|
| 选定skb的rate_sample字段 | TCP ACK/SACK处理、发送快照、skb选择、计数单位及retrans标记 |
| filtered_max_bw | 固定Linux minmax窗口及有效/app-limited样本准入、过期与round更新 |
| packets_in_net_at_edt / drain_target | TCP in-flight/EDT、TSO/GSO、BBR inflight/quantization相关输入 |
| TCP CA状态与prior_cwnd | TCP核心恢复/退出、loss识别以及最终target/cwnd clamp |
| ProbeRTT done stamp / round_done | 完整minRTT窗口、模式进入、低flight条件、计时启动与一轮完成 |

app_limited并非一概“无效样本”。源码中更高的app-limited样本仍可能更新带宽filter；但full_bw启动判据跳过app-limited轮次。当前函数把filtered_max_bw作为外部输入时，只能声称后者门控及round标记已覆盖，不能宣称内部已经算出完整maxfilter。

idle也不是把BBR重设成初始状态。固定源码 `bbr_cwnd_event` 在满足TX_START/app_limited条件时更新idle_restart/ACK聚合epoch，PROBE_BW恢复时使用相应pacing策略；minRTT与PROBE_RTT逻辑还受idle_restart影响。这些回调、完整PROBE_BW随机相位/进展、ACK aggregation、长期policer和socket pacing cap尚未全部在纯函数组合里实现，应明确列缺口。到PROBE_BW入口给出“需要相位初始化”，不应凭null gain继续假演完整状态机。

若未来把RFC9002 ACK记录传入BBR适配器，必须先说明TCP segments/ACK-SACK计数、delivered round、发送快照和QUIC PN/STREAM新确认之间的映射。没有这种来源明确的适配，不得声称Linux v6.6 TCP行为或把现有实验性BBRv1-shaped Go控制器替代官方代码。固定版本选择也不代表最新BBR。

## 独立oracle与先前近似纠正

`independent-oracles.json`保留：CUBIC曲线96.8/100/100.4、一次ACK真正窗口、Reno-friendly/alpha阈值、delayed ACK非Reno增量、cwnd_prior与flight_size分歧、100秒idle排除、Reno启动/timeout；BBR的压缩ACK样本整数1677、pacing98957/285662B/s、BDP10及量化14/16、三轮full_bw、app-limited、DRAIN等号、恢复前后、ProbeRTT严格after及无效sample。

**纠正上一next-congestion-scope中的10/12近似例：** Linux阈值 `(10*320)>>8` 为12，sample12恰达到阈值，会更新full_bw并清零计数，不会连续计为未增长。三轮不增长的独立例改用full_bw1000、sample1200、阈值1250；另保留10/12等号用例，防止把理想1.25浮点阈值混入整数版本。旧范围文件未修改，修正在本轮明确记录。

这些19组是源码/规范派生的预期，不是候选运行PASS报告。最终审查应逐个映射到两位作者实际接口执行、记录代码hash与每项范围；不符合的地方反馈作者修正，不修改他们实现。两者纯状态通过之后，仍需真实发送方反馈适配、双向网络/pacer、30MB与媒体业务闭环和图12-4，保持原C68/C69完整范围。

## 后续实际边界审查记录（不扩大为全控制器结论）

本文件及独立期望落盘后，新增 `check-minmax-boundaries.py`，从同commit的win_minmax.c/h原样编译算法（仅替换kernel include/macro），4834次更新逐一对照三样本的全部时间/数值状态，通过严格窗口/四分之一/二分之一边界、重复时间、相等max及u32回绕；14个类型/边界拒绝通过。结果见minmax-boundary-check.json，源依赖另锁在bbr-sources.lock.json。此前表中“未有maxfilter”的边界现应细分为：**三样本RunningMax内核已独立验证**，有效/app-limited样本准入、上游回调及全状态接线仍待其对应审查，不能仅凭内核通过就称闭环BBR完成。

同时 `check-cubic-independent.py` 已将预先9组CUBIC期望映射实际接口，并检查10个非法输入，当前10组报告全部通过（执行hash见cubic-independent-check.json）。它不调用候选curve/root辅助函数计算期望；源码后续若变化须重新核。BBR作者继续开发bbr_state时，旧有限函数声明与新状态机声明应分列，逐份记录来源及覆盖，避免本范围说明变成未经验证的“全部完成”背书。
