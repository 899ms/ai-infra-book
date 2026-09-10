# 同网络、实际反馈控制器适配：实现前合同

本合同先于sender/network适配代码。冻结基线为 `../transport-closed-loop/calculate.py` SHA3326f326…、`sender.py` SHA f81ca5ff…；CUBIC为 `../congestion-controllers/cubic.py` SHA91be0851…；HyStart++为 `../hystart-plus-plus/calculate.py` SHA4eb38d1b…。不修改这些文件或公共代码。

## 保持基线、显式对照

原10场景没有controller选项时走原参考NewReno，完整数学字段/轨迹应保持一致，来源根允许不同。新增controller选择 cubic_hystart、bbr或带同一pacer的newreno。主要公平对照另显式设 pad_in_flight=true：所有在途PN，包括尾包/MAX/PTO探测，填至MDS=1200 B；纯ACK仍为64 B。三控制器使用同一业务分包、链路、ACK和消费策略。未padding原场景保留；BBR的变长packet-count适配另标为诊断，不能将名义packet×MDS交付率当实际有效goodput。

MDS和cwnd采用QUIC UDP payload字节，不含额外28 B IPv4/UDP头。CUBIC segment=一个MDS，确认量可为sent_bytes/MDS的有理数；反向MAX是实际拥塞字节，纯ACK不是在途字节。网络serializer始终按sent_bytes+28计服务时间。新PN恢复相同STREAM offset增加线上/拥塞传输字节，不增加业务有效区间或绝对MAX额度。

## 共用回调

适配器构造 `Adapter(mds, initial_cwnd, initial_rtt, config)`，暴露 `cwnd_bytes`、`pacing_rate_quic_bytes_per_second` 与小型 `snapshot()`。共同回调为：

- `on_sent(record, context)`：出口实际开始时，新的PN/时间/在途已知字段；不是应用入队或未来接收。
- `on_ack(records, context)`：本次首次确认的所有PN，包括先lost后lateACK，标记was_lost/inflight_released，迟ACK不能再释放flight。控制器自行按合同决定增长/采样。
- `on_loss(records, context)`：实际发送方判失后调用；给判失前、剔除同ACK新确认量后的flight，包含此次将判失的包。
- `on_pto(context)`：仅通知合法probe机会，不映射为TCP timeout/loss/减窗。
- `on_limited(context)`：发送方实际ready、应用或绝对流控受限状态变化，不从接收端未来状态推断。

context含now（Fraction秒）、flight_before/after、smoothed_rtt/latest_rtt、独立rtt_sample或null、app_limited/flow_limited、recovery_start。record含pn/time（另at别名）、sent_bytes、in_flight、ack_eliciting、frames，ACK另带上述迟ACK标记。BBR作者负责其delivery快照与packet-round实现，不能直接用两ACK间隔代替采样。

## HyStart++：明确的QUIC适配

这里的round不是TCP字节序号。为每个实际开始发送的in-flight新PN按其QUIC长度分配一个单调、不重叠的transmission-byte区间；纯ACK不取得该区间。所有已确认区间合并后的连续前缀作为HyStart ack_seq。不能以largest_acked越过尚未确认的洞，也不能以本次ACK delta伪造完整round。恢复副本取得新PN和新transmission区间；它不会自动确认旧PN。

首次实际ACK时，使用此刻发送方已经实际发送的frontier初始化HyStart第一window_end；后续每次sent更新SND.NXT。这个初始化只读当前本地发送历史，绝不预定未来flight。一次ACK只提供发送方RFC9002算法认可的一次独立RTT样本（已核资格和ACK-delay处理）；不用smoothed RTT冒充新样本。RTT sample ID由本次首次确认PN和实际ACK到达身份组成，缺样本传null。

实际loss通知先终止初始HyStart并handoff，之后不再等待其旧round洞。PTO本身不终止；probe副本被ACK后若使原PN达到实际loss条件，则此时退出HyStart。需要专门验收：丢原包之前没有未来反馈、PTO不退出、确认副本不能冒充原PN累计确认、loss退出后迟原ACK不再次增长窗口。此选择是有限QUIC packet-round适配，不能称为TCP累计ACK实现。

初始HyStart从packet字节转换为segment后handoff给CUBIC。CSS正常退出且Wmax尚未定义时设置cwnd_prior=cwnd、Wmax=cwnd_epoch、K=0；仅传递数值，不重做该ACK增长。loss/ECN退出本身不执行beta减窗；真正恢复回调执行一次。后续slow start使用冻结CUBIC的Reno参考分支，不重开HyStart。

## CUBIC恢复、受限与数值

普通ACK的Reno-friendly N为本次可增长的新确认QUIC字节/MDS；立方分支仍每ACK推进一次，不因一个ACK涵盖多PN而多次执行。已lost的迟ACK不再次增长CUBIC窗口。恢复期按发送方真实recovery_start分界：发送时间不晚于该边界的ACK不增窗；新的拥塞epoch才允许再次beta减窗。减窗flight取实际未确认在途，包括此次lost字节，剔除本次已经确认的包。两个恢复epoch之间不虚构网络ACK。

应用无ready数据或绝对流控阻塞时，停止CUBIC有效epoch时间和窗口增长；正常cwnd/pacer等待不是应用受限。状态切换必须在实际本地队列/反馈变化时发生，不仅在下一ACK到达时才追认整段idle。受限期间仍处理合法RTT与传输确认；HyStart窗口增量可由外部受限gate抑制，并明确记录，不能破坏确认/round记账。

CUBIC采用冻结有理数/有界立方根参考；长闭环可显式量化cwnd、W_est与RTT并记录局部误差。不声称整体理想实数轨迹误差界。所有新数值策略均需显式输入，原NewReno10场景默认保持不变。

## 真实pacer与同刻事件

窗口型pacer采用RFC9002§7.7示例形式 rate=N*cwnd/smoothed_rtt，默认N=5/4，必须明确选择启用；因此HyStart paced=true有实际发送器支撑。BBR由其适配器给名义QUIC bytes/s。纯ACK按RFC建议不pace，但仍走物理串行出口；MAX和probe需要正常记账。

pacer用无积累突发信用的字节债务：实际发送一个包才增加其QUIC字节；时间推进按当时有效rate扣债。rate更新先按旧rate结算已过去时间，再用新rate计算未来等待，不能把新rate追溯到过去。已开始serializer不抢占；ACK优先于同刻timer与尚未开始的新发送。长轨迹若使用债务量化/发送时间向上网格取整，须分别记录局部误差和新增等待，不能提前满足依赖。

## Persistent congestion

根代理负责 `persistent_congestion.py` 纯证据函数，本适配保留hook。提供完整连续PN历史（包括不进入flight的纯ACK）；在实际ACK处理时审查证据。不能仅靠evidence_key去重：迟ACK拆分旧span不产生新的loss episode，必须跟踪尚未消费的loss声明/episode边界。PTO及loss timer不能凭自身伪造新ACK证据或永久拥塞。判定与CUBIC/BBR具体最小窗口动作分开审计。

## 验收与范围

先回归旧10完整场景，再验证ACK聚合、恢复、PTO、迟ACK、app/flow限制造成的epoch冻结、真实pacer更新及HyStart初始化/交接。最终用原书20Mbps上行/100Mbps下行、每向50ms、30MB上传、声明0.3s模型、5MB响应做同业务对照。保持wire/QUIC/有效字节与完整业务时刻分列。本阶段不据此宣称完整TCP或所有媒体业务已实现。
