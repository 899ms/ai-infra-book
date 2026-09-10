# C68 下一步：指定控制器与发送方反馈接入完整业务

本次只写范围审查，不实现、不修改公共模块或 PLAN。对照原 C68、`research/plan-c68-c69-audit.md`、正文 12.3、现有 `connection_window`/`connection_sequence`/`shared_media_transport` 及本轮公共接入范围。旧教学计算保持有效，下一步必须补发送方真正收到的反馈如何改变发送，而非给固定信用换一个 CUBIC/BBR 名字。

## 建议版本与本轮实际读取的来源

**CUBIC 固定为 RFC 9438（2023-08），BBR 固定为 Linux v6.6 的 tcp_bbr.c 源码行为**；后者常称 BBRv1，以固定源码为最终版本标识，不称最新 BBR 或 BBRv2/v3。两者先做独立控制器状态转换与来源对照，再接公共网络事件层。CUBIC 的规范语义与 Linux BBR 的具体实现不是同一类证据，结果必须标注这种差异。

本轮在仓库找到并读取 RFC9000/9002/5681；未找到 RFC9438 官方原文。读取了 RFC Editor 的固定 RFC9438，并从 Linux 官方仓库解析 v6.6 tag 到 commit，以 GitHub 官方仓库 contents API 读取该 commit 的两个文件、解码后计算 SHA。未写下载文件，因为本任务仅授权本报告；下面是实现前可用的精确固定记录，后续来源封存步骤仍需落原件并重读校验。

| 来源 | revision 与 bytes | SHA256 |
|---|---|---|
| [RFC9438 原文](https://www.rfc-editor.org/rfc/rfc9438.txt) | RFC9438，73704 bytes | `baa4dd77295e27b9fa5c79993e962e70f728409bd1a48b9029bae4b551b0348a` |
| [Linux tcp_bbr.c](https://github.com/torvalds/linux/blob/ffc253263a1375a65fa6c9f62a893e9767fbebfa/net/ipv4/tcp_bbr.c) | v6.6 commit `ffc253263a1375a65fa6c9f62a893e9767fbebfa`，42724 bytes | `ba7d0706259dfef5bf455f26ac4bab65f43b9209b9cfd4f761c64c89816bdfe4` |
| [Linux tcp_rate.c](https://github.com/torvalds/linux/blob/ffc253263a1375a65fa6c9f62a893e9767fbebfa/net/ipv4/tcp_rate.c) | 同 commit，8436 bytes | `52d682c760573819a36bfef45a094ea8615a39d56c0248569d96f9e6e47b2b23` |
| [RFC9002](https://www.rfc-editor.org/rfc/rfc9002.txt) | 本地 `calculations/sources/protocol-rfc/rfc9002.txt`，89071 bytes | `3a8a54eea1ad5d1c134a548bf15edfa0e21bfb4106dbd7db3c09cace842099af` |
| [RFC9000](https://www.rfc-editor.org/rfc/rfc9000.txt) | 同目录，403442 bytes | `f88aae47f8b18e102024916e975e919201d8dde689cba79b01079eaedd402e22` |
| [RFC5681](https://www.rfc-editor.org/rfc/rfc5681.txt) | 同目录，44339 bytes | `a2d99a2421d5c57b248394f26ba44fc364aa546680fbf10ff0aa7034dad8b87d` |

v6.6 annotated tag object 为 `5260836abb7056beed3f3f0d0e4262c11f36f0d0`，解析后的 commit 如表；不是把可移动分支当不可变 revision。核查日期为 2026-09-09。一次 raw URL 读取不完整后改用同官方仓库 contents API 取得完整 bytes，不以截断数据计算固定记录。没有进行一般性最新版本/全部 errata 调研。

实际读段及适用边界：

- RFC9438 §4.2/4.3/4.6/4.10：按新 ACK 推进的 CUBIC 曲线、Reno-friendly 分支、拥塞响应、启动选择；HyStart++ 有另外规范依赖。仅采样一条立方曲线不足以实现完整控制器，不能把 W_cubic(t) 直接赋给每时刻的 cwnd。[规范正文](https://www.rfc-editor.org/rfc/rfc9438.html#section-4.2)
- RFC9002 §5.1–5.3、§6.1–6.2.1、§7：RTT 与 ACK delay、包/时间阈值、PTO、bytes-in-flight。PTO 到期并不自动宣布旧包丢失；规范默认拥塞控制类似 NewReno，不是 CUBIC/BBR。RFC9000 §4.1 的 MAX_DATA/MAX_STREAM_DATA 是发送方收到的绝对限额，普通 ACK 本身不提高该限额。
- 固定 tcp_bbr.c 的带宽/RTT滤波参数、`bbr_update_bw`、`bbr_check_full_bw_reached`、`bbr_check_drain`，及 tcp_rate.c 的 `tcp_rate_gen`：采样必须保留发送与 ACK 两个区间，不能用相邻 ACK 的间隔直接估带宽；BBR 状态按其固定源码条件转换。核心默认增益与计数也来自源码，不能混用不同版本的简图。[固定 BBR 源码](https://github.com/torvalds/linux/blob/ffc253263a1375a65fa6c9f62a893e9767fbebfa/net/ipv4/tcp_bbr.c)、[固定采样器](https://github.com/torvalds/linux/blob/ffc253263a1375a65fa6c9f62a893e9767fbebfa/net/ipv4/tcp_rate.c)
- 仓库 `experiments/ch12/12-07/transport-pool/source/internal/congestion/bbr.go` 自述是独立实验性 BBRv1-shaped 实现，不可替代上述 Linux 原件。它及 TUIC 变体可作为既有记录/交叉核验对象，不能根据文件名推定为官方固定版本或抹去这些已有工作。

## 下一项应先实现什么

建议先做 `research/transport-feedback/`：**已确认连接、单路径、1-RTT application packet space 的 ACK/丢失/绝对流控基座**，先用 RFC9002 参考 NewReno 检查反馈正确，再通过显式适配层接 CUBIC 与 BBR。这个基座不等于已完成全部拥塞比较，但比继续扩教学固定窗口更接近原 C68。算法实现随后单独验收，不能提前用名称填充结果。

采用有限可靠 STREAM、有限不可靠媒体及双方向资源；每方向发送历史/RTT/拥塞状态独立。传输 PN、逻辑 STREAM offset、网络发送次数是三种身份，恢复必须新 PN、原业务区间，应用唯一收到一次。DATAGRAM 无 MAX_DATA 信用占用，但使用同路径拥塞预算；ACK/流控更新/恢复与响应共同消耗相应实际出口。限定已确认连接是阶段边界，保留已有握手图，不把其初始/握手丢失处理假装一并实现。

### 分阶段接口与验收门槛

| 阶段 | 输入与输出合同 | 通过后才可做 |
|---|---|---|
| 0 来源/单位 | 封存上述精确原件；补所选 CUBIC 启动及恢复依赖（例如 HyStart++）；固定 MSS/UDP payload/封装、发送时间戳定义、时钟粒度、舍入、ECN/ACK政策和随机种子 | 命名明确版本的控制器，不称完整协议栈 |
| 1 网络/接收/反馈 | `packet_sent`、接收 ACK ranges/ack_delay、消费驱动 MAX_DATA/MAX_STREAM_DATA、可观察丢失阈值与 PTO 事件；输出每个 PN 的 sent/acked/lost、bytes_in_flight、RTT 估计、next_timer、限额。队列容量/丢失在网络层发生，发送方只能在收到反馈后获知 | 在固定输入下与独立参考 ACK/恢复 trace 对照 |
| 2 控制器纯状态 | `on_packet_sent`、`on_ack(newly_acked, RTT, delivery_sample, app_limited)`、`on_loss(newly_lost,recovery_epoch)`、`on_idle` → cwnd/pacing_rate/状态/可发时间；所有输入字段定义 provenance，保留原始采样 | CUBIC 与 BBR 各自源码/规范手算、边界和状态覆盖通过 |
| 3 闭环调度 | `can_send` 同时检查 cwnd/inflight、pacer、发送方已知连接/流限额及 ready/dependency。输出阻塞原因集合和起止时刻，不把重叠等待简单相加 | 30 MB 上传+模型+5 MB 回传，响应无需等待上传最后 ACK，但保留共同方向队列 |
| 4 同业务消融 | 原 shared-media 的图像/ASR/TTS/截图/预览/取消，保持 offered workload/位置/网络不变；网络/CPU调度分离、单独改变算法/流控/ACK/恢复 | 公共 CLI/输入/固定结果/独立检查，更新图12-4关联的拥塞与业务面板 |

TCP 与 QUIC 要有明确分开的 transport_profile。RFC9002 恢复层配 CUBIC 可以命名为固定 QUIC 恢复+CUBIC 适配模型；Linux BBR 的 TCP 回调与 tcp_rate 样本映射到该层必须列出差异，完成适配验收前只能叫“固定 BBR 控制器移植/实验”。若要声称 Linux v6.6 TCP 行为，必须额外固定 TCP ACK/SACK、恢复、接收窗口以及相关核心代码，不能拿 QUIC ACK/PTO 充当 TCP 回调。为了比较控制器，优先使用相同反馈 transport_profile；为了比较 TCP/H3，则另列完整栈差异。

最初可禁用 ECN、限制单路径及一次指定网络丢失，但“固定丢失”只指定丢在哪个发送尝试，不再指定发送方什么时候应重传。尾包丢失、ACK 丢失、乱序和同刻 ACK/定时器必须有可审查的反馈行为。未知/未覆盖分支应拒绝或输出未完成原因，不能偷偷回退为固定延迟恢复。

## 实现前手算验收

以下期望在写实现前固定；时间使用精确单位。算法内部若必须用整数定点或立方根近似，另列误差界/舍入，不能宣称 Fraction 自动给出一般立方根的精确值。

1. **BDP 与不受限序列化下界。** 20 Mbit/s、100 ms 上行 BDP=250000 bytes；100 Mbit/s 下行=1250000 bytes。30 MB/20 Mbit/s=12 s，5 MB/100 Mbit/s=0.4 s。若每向传播0.05 s、模型0.3 s，已建立连接、无限制无封装理想完整响应为12.8 s。加入真实头/ACK/窗口后不得低于这个明确条件下的串行全图依赖下界；预览不替代最终成片。
2. **RTT 更新/重复 ACK。** 已确认连接，首次样本100 ms且报告延迟0：min_rtt=100、smoothed_rtt=100、rttvar=50 ms。第二样本120 ms、ack_delay=20且max_ack_delay=25：调整后100、smoothed仍100、rttvar=37.5 ms。重复 ACK 没有新确认时不重复取样或释放字节。必须从发送记录定位最大新确认 PN，而非从物理接收方直接输入 RTT。
3. **包阈值不是任意时间丢失。** PN0/1/2/3 分别在0/1/2/3 ms发送，ACK在103 ms仅新确认PN3，已有smoothed/latest RTT=100 ms。包阈值3使PN0此时丢失；PN1/2尚未达到112.5 ms时间阈值，不得一并判丢。后续对应时间阈值时刻113.5/114.5 ms可触发未确认包检查；同刻到达的有效ACK先处理，已ACK字节不能再次释放。
4. **PTO 与 loss 分离。** 沿第2例，granularity=1 ms、max_ack_delay=25 ms：PTO周期=100+150+25=275 ms。最后一个ack-eliciting包发送于1 s，满足已确认application-space及无更早loss_timer条件，则初次PTO为1.275 s。到期产生允许的probe机会，不把所有未ACK包判丢、不直接将cwnd减半；后续指数退避及有效ACK后的计数重置单列测试。定时器失效不延长协议忙时刻。
5. **普通 ACK 不解除绝对流控。** 初始MAX_DATA=6 bytes，stream A限额4、B限额2；已发A[0,4)、B[0,2)。全部ACK只影响flight/cwnd，不能允许新STREAM数据。新的MAX_DATA=8在发送端5 s收到、MAX_STREAM_DATA(A)=6在6 s收到，则A[4,6)最早在6 s才具备流控许可，仍须过cwnd/pacer。重复或较小限额不回退；恢复旧offset不再次消耗绝对数据额度，但新发送包仍占拥塞/网络字节。
6. **CUBIC 函数与ACK更新分开。** 单独种子W_max=100 segments、cwnd_epoch=96.8、C=0.4，K=2 s；W_cubic(0/2/3)=96.8/100/100.4。这是曲线单元测试，不是从0.7减窗推来的epoch，也不是完整cwnd轨迹。另测满负载flight_size=100 segments、β=0.7时的减窗目标70（排除其它恢复例外）；完整ACK更新还须检查Reno-friendly、target/cwnd限制、恢复epoch只降一次、闲置/受限应用不凭空增长。启动选择和HyStart++未接入时不得称该算法全过程完成。
7. **BBR 采样不能被ACK压缩放大。** 以固定tcp_rate合同的样本字段为输入：本样本delivered=10 segments，send interval=100 ms、ACK interval=20 ms，minRTT≤100 ms且无其它无效条件。分母取100 ms，原始rate=100 segments/s，不能算500。具体定点值按固定源码舍入。发送记录必须携带prior_delivered/prior timestamp/app_limited，不能仅用当前ACK确认数除相邻ACK间隔。
8. **BBR 状态边界。** 既有full_bw=10（统一采样单位），其后3个非app-limited的新packet-timed round最大带宽各为12，均未达到1.25×10，计数1/2/3，第三次置full_bw_reached；同样样本若app_limited不得推进该判据。DRAIN退出还受inflight目标约束，不能直接因次数到3就无条件PROBE_BW。固定源码high_gain为739/256，不能把2.885文字近似当位精确常数；完整pacing还存在固定实现的margin/整数转换。另须覆盖PROBE_RTT条件、最小窗口、ACK aggregation及恢复行为后才升级完整版本声明。

每个闭环场景额外输出：数据/封装/ACK/流控更新/重发逐方向bytes、唯一应用区间、最终完整接收/最后ACK/有效业务、队列与pacing/cwnd/flow-control阻塞。至少有接收窗口受限、发送应用受限、ACK反向拥塞、首部/中部/尾部丢失和晚到恢复的负例。不得用一条lossless长流就声称覆盖原文的恢复与短请求差异。

## 当前成果保留与原完整缺口

`connection_window` 的 ACK-ID/累计前缀与固定RTO、`connection_sequence` 的连续请求共同队列，以及 shared-media 的信用/非抢占/HOL/播放/取消手算已经提供有用教学证据，保持其命名和结果。此次应增加明确版本的反馈算法，不能把既有25KB教学块/ACK增长参数翻译成真实MSS或cwnd。

C68继续保留：TCP侧剩余HRR/PSK与票据/完整编码、运行时Retry组合边界；实际协议的多轮恢复/复用业务累计；指定CUBIC/BBR与真正拥塞/流控/一般恢复；相同图片/ASR/TTS/CU轨迹的默认/调优TCP/H3匹配对照；握手、媒体、拥塞及真实记录恰当连接的完整图12-4。已有loopback、H3多流、shared-media的局部计算和图不归零，也不据此提前勾选。

C69的TCP ACK与MAC ACK空口区别、双向无线竞争、多路径RAW汇合、备份/蜂窝计费能耗、完整截图版本/重试和图12-5仍独立待办。不能用全双工链路ACK账替代空口。原实验条件允许声明计算/网络记录；本计划不新增“必须生产WAN实测才能完成”的门槛，但凡声称实测或特定实现性能，就必须具备对应匹配记录。

建议执行顺序明确为：来源封存与反馈基座 → 各指定控制器的独立状态审查 → 30MB完整请求与媒体业务闭环 → 公共结果和图12-4收口。控制器之外的原C68范围不因本阶段选择而删除。
