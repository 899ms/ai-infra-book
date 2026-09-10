# 多媒体闭环：共享 sender 接口合同

本研究直接复用冻结公共 `infra_calc.topics.transport_sender`。实读后确认其已经实现多 STREAM 绝对额度和 DATAGRAM 发送/ACK 身份；不为任务名称复制或改写拥塞、RTT、loss、PTO 算法。研究 `sender.py` 仅提供源码锁校验、原 API 转出及恢复帧筛选助手。所有相关公共 Python 与官方 source lock 身份见 `sender-dependencies.lock.json`；实际官方原件仍由公共 `read_source` 校验。

每方向只有一个 `create_sender(inputs)` 对象，所有流和不可靠媒体共用其 cwnd、flight、PN、ACK/loss/PTO、控制器和 pacing 回调。反向独立对象，两个方向物理链路归网络引擎所有。

- 初始额度：`initial_max_data` 和 `initial_max_stream_data={stream_name: absolute_limit}`。每个流名为已登记非空字符串。
- STREAM 帧：`{type:'stream',stream:'audio',offset:0,length:100}`。长度为正整数；offset+length 不超过 2^62-1。
- DATAGRAM 帧：`{type:'datagram',id:'audio:chunk0',length:100}`。id 为每方向从未发送过的非空字符串；flow/message/业务截止时间保留于网络元数据，不混入 STREAM 序号。
- 发送事件沿旧接口：`{type:'sent',at,pn,sent_bytes,frames,ack_eliciting,in_flight,probe}`。每个新的传输使用新 PN；有限核心要求从0连续增长。发送时真实调用 enqueue/advance，不用未来 ACK 提前推进。
- 更新额度：`{type:'max_data',at,value}` 或 `{type:'max_stream_data',at,stream,value}`。由真实控制包到达触发；绝对值仅增不减。
- ACK：`{type:'ack',at,ranges:[[low,high]],ack_delay,...}`。恢复/PTO 与 ACK 的同刻顺序保持原核心规则。

连接已消费额度是各 STREAM **已实际发送最高 end 的和**，不是 payload 之和，也不是已 ACK 但尚未消费字节。多个流各自受 MAX_STREAM_DATA 限制。新 PN 重发旧 offset 不重复消耗可靠额度；发送高 offset 会连前方空洞一起计入连接额度。未发送的取消块不改变核心最高 end；取消不返还已发送额度，不重置流 offset，不捏造接收消费。

DATAGRAM 共享拥塞与真实 ACK/loss，但不占 MAX_DATA/MAX_STREAM_DATA。首次 ACK 只确认该 DATAGRAM 传输身份；这是发送方证据，不证明应用在截止时间前使用。重复 DATAGRAM id 的发送由原核心拒绝，即使原传输已被声明丢失也不重发相同身份。

## 网络恢复责任

`retransmittable_frames(record)` 对已发送 packet/history record 返回仅 STREAM 帧的深拷贝；混合 STREAM+DATAGRAM 包恢复时不能顺手复制 DATAGRAM。仅 DATAGRAM 帧返回空列表。助手不分配 PN、不扣额度、不调度发送、不把 loss 当真正丢包事实。

网络 loss 路径使用返回的 STREAM 帧按未确认业务范围/取消政策选择必要内容。MAX 等无 payload 控制信息必须由网络保留的 control metadata 独立判断是否仍需发送；不能因为 frames=[] 就统一丢弃可靠控制更新。

PTO 不是 DATAGRAM 重发许可。若只有不可靠 payload 在途，网络可使用 `{frames:[],ack_eliciting:true,in_flight:true,probe:true}` 的声明 PING 探测包，并通过原 sender 的 probe_allowance 检查；不可重新发送 DATAGRAM id。PING 的实际 QUIC 头/帧预算和统一 padding 由网络指定。应用重新产生不同 id 的新媒体数据不是旧 DATAGRAM 重发，仍须真实排程和拥塞许可。

原字典 API 的 state/result/history/active/losses/timers/validate_packet 保留。`inputs.events` 不会由 create_sender 自动执行；调用者必须按实际反馈执行 enqueue，再 advance，避免漏回放或重复回放。`state` 给出每流最高 end 与额度，`result.sender_confirmed_business` 分别给 STREAM 唯一区间/字节、DATAGRAM 已 ACK ids/字节；它们不能替代网络真实接收与播放统计。

有限合同不实现 STREAM ID 的 QUIC 位语义、RESET_STREAM/STOP_SENDING、final_size、MAX_STREAMS、HTTP 优先级或真实浏览器媒体行为。取消造成的流洞与应用不可用状态必须在网络/应用层如实呈现。旧单流默认数学保持直接委托，回放检查另存执行证据。
