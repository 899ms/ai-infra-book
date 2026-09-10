# C68 阶段1：发送方实际反馈、RFC9002恢复与绝对STREAM限额

研究候选，尚未公共接入。限定已经完成握手和地址验证、单一路径、Application packet-number space、单发送方向。输入是发送方实际可见的发送／ACK／限额事件，不是自动网络调度器，也不把接收方未来状态直接交给发送方。两方向完整业务闭环、CUBIC、BBR保持下一阶段。

```bash
python3 calculations/research/transport-feedback/calculate.py \
  --output calculations/research/transport-feedback/result.json
# 单个输入：--inputs path/to/input.json --output path/to/result.json
```

`calculate(inputs)`、`example()`、`scenarios()`，默认14个固定场景。每次读取并校验 `sources.lock.json` 中四份官方来源：RFC9000、RFC9002、RFC9221及**Verified Errata7539**。后者修正RFC9002§5.3的更新次序：先用旧smoothed_rtt计算rttvar，然后更新smoothed_rtt，与附录A.7一致。没有继续采用未更正正文的先SRTT后方差顺序。来源适用边界见 `SOURCE-SCOPE.md`。

## 明确的输入合同

所有`at`、RTT、ACK delay、`until`均为秒，可输入小数或分数字符串。`sent`时间戳表示输入记录里的发送时间点，本阶段不从它推导串行起止，也不检查出口重叠。包长`sent_bytes`是UDP payload，包括QUIC头、帧、tag与padding，不含UDP/IP头。正负方向网络、ACK和MAX消息的封装/排队开销将在闭环阶段加入，不在此伪填零字节结果。

- `sent`：`pn`、`sent_bytes`、`ack_eliciting`、`in_flight`、`probe`、`frames`。PN在这个有限完整历史中从0连续递增，不支持发送方主动PN间隙；不得重复原PN恢复。STREAM帧给stream/offset/length，DATAGRAM给应用id/length。包内STREAM区间不能相互重叠，跨包相同区间允许恢复或PTO探测。DATAGRAM应用id在本合同不能重发；如应用生成新媒体必须使用新id。
- `ack`：解码后的inclusive `ranges=[[low,high],…]`、`ack_delay`、`app_limited`和`flow_limited`。范围不重叠、不确认尚未发送PN。两种limited是发送方明确观察的策略输入，不从“恰好用完MAX_DATA”自动猜测应用需求。
- `max_data`／`max_stream_data`：该绝对限额实际到达发送方的时刻与value；重复或较小值不回退。它们不是普通ACK带来的隐式窗口增长。
- `can_send`：使用与sent相同的包信息但不真正发送，报告当前`cwnd`、`MAX_DATA`、`MAX_STREAM_DATA`、probe许可阻塞；用于复算两项限额先后到达的区别。实际`sent`若违反任一发送方已知门槛则拒绝输入。

`max_datagram_size`最少1200B。声明负载至少留下32B包头/帧/tag预算，这只是有限输入的下限防错，不是完整QUIC字节编码器。`initial_cwnd`默认RFC9002的`min(10*MDS,max(2*MDS,14720))`；最低2*MDS。可给`rtt_seed`代表本记录开始前已有的已知RTT状态；没有seed时使用声明初始RTT（默认333ms），首个实际ACK样本重置估计。

绝对STREAM额度按每流**最高发送offset**计算，包含空洞。例如先发A[5,6)即消耗连接6B额度；再补A[0,5)不增加额度。普通ACK和重发旧区间都不退还/再次增加MAX额度。DATAGRAM不占STREAM/连接MAX_DATA，但其发送包仍占bytes_in_flight与cwnd。

## RTT、loss、PTO与NewReno参考

ACK最大PN必须是新确认，且本次新确认至少有ack-eliciting包，才定位发送记录取RTT。首样本不扣ack_delay；min_rtt始终使用原始RTT。已确认连接的后续样本只在合理时扣除不超过max_ack_delay的延迟。全部使用Fraction，NewReno的加性增长采用附录B的有理数式，未声称某内核整数舍入轨迹。

新确认后先检测包阈值3及时间阈值`max(9/8*max(latest,smoothed),granularity)`的损失，再执行NewReno ACK增长。只有不晚于最大已确认PN的待确认包可被这些阈值判失。loss timer跟踪下一个阈值，不用固定“发送后RTO”代替。首次拥塞事件减半并受最小窗口约束；恢复期旧包的后续loss不再次减窗，同一ACK中的恢复期包也不增长。时间0用None区分尚无恢复／尚无RTT样本，避免直接照抄伪码0哨兵的错误。

PTO周期为`smoothed+max(4*rttvar,granularity)+max_ack_delay`并按pto_count退避，基准是最后ack-eliciting发送时间。PTO只给最多两个probe机会，不宣布旧包丢失、不直接减窗；真正发送probe必须由后续sent事件提供。probe可越过cwnd但继续计入flight，仍不能越过绝对流控。新有效ACK重置pto_count与剩余probe机会。

同刻先处理ACK/限额，再timer，随后sent，最后can_send。有效ACK恰在定时器时刻先使旧timer失效，不会再释放一次flight。自动timer仅执行到`until`；超过范围的next_timer仍作为未决状态输出。失效timer不更新`last_processed_event`，这个时刻不是协议或业务完成时间。

纯ACK不进入flight且不启动PTO；PADDING-only可进入flight但不是ack-eliciting，不能凭它单独启动PTO。尚未确认、丢失、ACKed分别保存。丢失记录保留以标记late ACK和已确认业务区间；late ACK不会重复释放flight、重新增长cwnd或独立重采RTT。该保留策略明确区别于附录A直接删除lost记录；它不增加接收应用交付证明。

本阶段没有实现完整persistent congestion过程。若已知历史达到“两个已失ack-eliciting包、已有RTT、区间内无ACK、跨越三倍PTO基准”的候选范围，明确拒绝并要求进入后续persistent实现，**不静默当作完整NewReno结果**。ECN、迁移、其他PN空间、网络pacing、实际接收与一般业务调度未覆盖。

## 固定场景与手算

- `rtt-duplicate-ack`：首100ms，次120ms减20ms后仍100ms，rttvar37.5ms；重复确认不再次释放或增长。
- `rtt-verified-errata`：第二原始180ms减20ms后160ms；smoothed107.5ms、rttvar52.5ms，区分错误次序的50.625ms。
- `packet-and-time-threshold`／`ack-at-loss-deadline`：PN0/1/2/3在0/1/2/3ms，103ms ACK3；PN0首先判失，PN1/2时间阈值113.5/114.5ms。恰时ACK优先。
- `tail-no-feedback-pto`／`probe-then-ack-reset`／`ack-at-pto-deadline`：275ms周期，最后发送1s，首PTO1.275s；无反馈不伪造loss，probe实际发送与有效ACK重置另计。
- `absolute-flow-feedback`：A4+B2用完MAX_DATA6；ACK不解除；5s到MAX_DATA8仍受A4限制，6s到A6才通过两项绝对流控。
- `stream-offset-high-water`：先A[5,6)、后补[0,5)，额度始终6，ACK确认有效区间最终为6B。
- `datagram-without-stream-credit`：MAX_DATA和流限额均0仍可发送受cwnd约束的DATAGRAM。
- `ack-only`／`padding-only`：区分flight与PTO条件。
- `new-pn-old-offset-recovery`：新PN4恢复旧offset0，旧PN0晚ACK不重复计量；后续新恢复期包ACK使6000B cwnd增长到6240B。
- `pto-probe-over-cwnd`：2400B窗口已有2400B in-flight，授权probe增加到3600B，不自动判失腾出空间。

输出 `events` 给每次反馈后的完整状态和next_timer；`loss_events`、`timer_events`、`rtt_samples`可独立核。`sender_confirmed_business`只证明ACK覆盖的唯一STREAM区间或DATAGRAM，不等于完整识别、图片、播放。`summary`分UDP payload、重复STREAM发送、DATAGRAM发送及声明QUIC头/padding/control字节；不冒充全链路线速字节。

最多10000外部事件、100000处理事件和32次PTO退避。下一阶段仍需接入固定CUBIC/BBR及采样适配、双方共享资源、30MB完整请求和媒体业务闭环，再公共注册及更新图12-4；本候选不关闭C68。
