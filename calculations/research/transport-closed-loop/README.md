# 双向网络与发送方反馈候选（开发中）

本目录把冻结 `../transport-feedback/calculate.py` 的发送方算法提取为可推进对象，加入实际双向串行发送、传播、接收端有序 STREAM 区间、逐包立即 ACK、消费驱动绝对 MAX 更新及完整上传→模型→响应依赖。不是完整 TCP/QUIC 实现；本候选尚在独立审查，未公共接入。

`sender.py:create_sender(inputs)` 返回 `enqueue(event)`、`advance(until, inclusive=True)`、`state()`、`result()` 和审计索引。构造函数不自动入队 inputs.events；调用者显式逐事件 enqueue。advance 水位不倒退；同刻已处理更低优先级事件后不能补入更高优先级事件。可先 advance(t,False)，再入队同刻 ACK，最后 advance(t,True)。默认精确配置与冻结重放 14 个场景的完整结果相同。`check-sender-root.py` 属于独立验收方。

网络调用 `calculate.py:calculate(inputs)`，CLI 接受 `--inputs JSON --output JSON`。`example()` 是2336 B上传、1s模型、32 B响应的手算。每向独立发送方 PN 空间，包含纯 ACK 的 PN；纯 ACK 不进入拥塞在途活跃索引。每个新发送/恢复/探测都用新 PN；旧 STREAM offset 保留。只按实际到达发送方的 ACK 更新确认区间，已经确认的范围不因旧 PN 被判失再次恢复。

输入 `links.up/down` 的 rate_bps/propagation 声明各向端点串行出口速率和服务后传播；UDP/IPv4头固定28 B，STREAM包有效字节之外的QUIC预算32 B，纯ACK和合并MAX_DATA/MAX_STREAM_DATA控制包默认64 B。这里声明布局预算，没有实现完整报文codec。ACK政策明确选用 immediate_each_packet，每个ACK只含收到的单PN范围，ACK delay=0；串行队列等待和传播属于RTT，不能计入ACK delay。控制帧也受实际链路限制；MAX是ack-eliciting，接收MAX后的纯ACK优先于同刻待发数据。因此第三流控手算的6s是获得发送许可，实际数据要等ACK占用的23/307s。

待发优先级为纯ACK/MAX控制、恢复/探测、普通业务，各类FIFO；只在实际发送开始时选包和分配PN。已经开始的串行发送不抢占。`pacer_interval` 是显式固定最小发送间隔，默认0；尚未提供控制器推导的自适应pacer，不能称默认具有完整QUIC pacing。

可选 `routers.up/down` 在相应端点出口之后增加真实有限FIFO瓶颈，字段rate_bps、queue_bytes和可选propagation。queue_bytes只计等待区的线上字节，在服务中的包不占等待容量。包到达空闲router时立即服务；忙时若等待容量不足则丢弃，发送方仍保留已发送和在途记录，直到实际ACK/loss timer/PTO提供反馈。同刻router服务完成先于新入队，以释放实际容量。没有router的场景只有端点串行出口，不能称其已经经历队列溢出。

接收缓冲窗口 `receive_window` 同时初始化连接与business流绝对额度。接收端维护唯一已收区间与连续前缀；乱序可ACK，应用只交付连续前缀。`consume_delay` 可声明在新前缀交付后多久消费；或用 `explicit_consumption` 的direction/at/upto明确消费事件。消费不能超过实际前缀，重叠消费不重复计算；消费后发送MAX的绝对额度=初始窗口+累计已消费字节。发送方等这个控制包实际到达才解锁新offset。每向未消费的唯一接收字节不得超过初始窗口。

窗口/RTT默认Fraction精确，小整数例与冻结轨迹相同。长轨迹必须明确选择 `sender.numeric_quantum`，例如 `"0.000000000001"`。每个事件更新后、下一定时器计算前，对RTT状态/cwnd/ssthresh按最近网格值舍入，正中间采用ties-to-even；正数不舍入为零，cwnd保留2*MDS下界。quantum不能粗于timer granularity。输出每次原值、舍入值与精确局部差，不声称整个实数轨迹误差有界；后续同刻比较使用实际舍入状态。默认精确状态超过位数预算明确拒绝，不能无限增大整数输出限制。

结果逐包记录端点串行开始/结束、计划arrival与实际received_at、PN/offset、QUIC/UDP-IP/线上字节、丢弃及router排队。有限horizon下已开始包可能还没串行结束，summary的wire_bytes是已开始包的完整声明字节；serialized_wire_bytes_by_horizon才是截止时间已实际串行的线上字节。business.complete语义由完整响应实际交付决定，不能用pending空替代。sender_events是实际发送方事件，便于小例回放交叉核；不在每包上重放全部历史。发送方active索引和三类待发deque避免扫描全部历史/待发业务；大结果只保留每包与局部事件。

尚未完成：自动延迟/范围合并ACK、所有拥塞控制器接入、完整persistent congestion（当前明确拒绝触发该区间）、媒体DATAGRAM/播放/取消/截图版本业务、真实TCP对照。当前完整业务是上传→模型→响应；不能据此宣称 shared-media 的所有业务、完整协议或全部C68已经完成。

固定复算入口：`python calculations/research/transport-closed-loop/calculate.py --output /tmp/closed-all.json` 执行10场景；`--inputs calculations/research/transport-closed-loop/example.json`执行单场景。`result.json`是完整固定场景输出；`book-input.json`与`large-input.json`分别保留原书条件及100/100Mbps、10ms附加输入，开发期间的重复大结果已移除。当前原书固定场景使用20/100Mbps、每向50ms、声明模型0.3秒；其完整包和局部误差在result.json的book-30mb-5mb项。
