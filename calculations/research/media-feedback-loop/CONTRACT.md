# 共享媒体真实反馈候选：实现前合同

仅研究，不改公共模块或十二章。读取 `transport-controller-loop/NEXT-SCOPE.md` 与 `media-feedback-inputs/README.md` 后确定此接口。网络每direction只有一个共享sender/controller/pacer；规范化DAG负责何时产生数据及何时业务可用，不读取未来网络状态。

## 文件职责与输入

`calculate.py` 负责物理事件、队列/ACK/恢复与业务依赖；`application.py` 负责DAG验证/本地就绪/计算资源/业务观测；`sender.py`由另一代理负责，薄封装锁定公共sender，提供原create_sender API及retransmittable_frames，只返回STREAM恢复帧。ACK receiver/pacer/controller复用现有公共实现，不复制修改算法。

输入 `{"application": <normalize输出>, "network": {...}}`。network显式提供 `links:{up/down:{rate_bps,propagation}}`、until、initial_cwnd、initial_max_data（每direction）、initial_max_stream_data（direction→flow→绝对额度）、receive_memory_bytes（每direction）。controller/ack_policy遵循已验公共schema；可选routers/drop_packets/consume_delay/pad_in_flight。初始声明不从legacy教学credit映射。consume_delay省略或null表示不消费、不发MAX，初始额度及内存必须足够；非负delay使按序可消费前缀实际到达后触发消费，随后MAX消息仍须实际传输。预先高额度不是免费动态窗口。

布局为声明QUIC packet：STREAM有效片≤1168、32B布局预算；DATAGRAM同预算且原子单片≤1168；可统一填充1200，再加28B IPv4/UDP。pureACK64B，MAX/PING64B（若统一pad则1200）。DATAGRAM的id用于应用消息身份，flow保留在packet metadata，不假装QUIC STREAM ID。

## 依赖与选择

DAG依赖为同端message_delivered/task_completed。可靠完整消息要求所有切片且同流从0开始的连续已收prefix达到message end；最后一片到达不等于完整有序交付。task只有ready时刻和全部本端依赖满足后进入(endpoint,resource)独立FIFO，非抢占。跨端依赖必须是真实通知消息；版本改变是各observer端本地事件，不向远端瞬移。

应用消息激活后分片入方向内各flow待发队列；只在实际发送开始选FIFO或priority。共享连接窗口/物理串行器不因flow数增长。flow受绝对额度阻塞时其他flow可继续；cwnd/pacer是方向共享约束。compute调度不随send priority改变。

取消消息须完整可靠按序交付才在其receiver生效。只抑制该端未开始task、尚未发送的目标消息片；已开始任务到期才结束，已开始包非抢占，已发送可靠片保留真实恢复。初版不实现RESET_STREAM，取消未发尾部可能留下可靠流洞，后续同流消息不得跳洞交付。DATAGRAM已过期未发可丢弃，接收过期不影响ACK/flight记账；不能丢可靠图像片却宣称完整。

## 网络与反馈

沿已验事件顺序：router结束-1、arrival0、service/consume/ACKdeadline1、sender反馈与timer2、尚未开始发送pump3。同刻sender收到ACK先推进其状态再处理timer；actual arrival才生成ACK，actual ACK start才冻结聚合快照。pureACK不触发ACK循环，不pace但共享物理serializer。

可靠STREAM每流offset、连接sum(highwater)流控；重发旧offset新PN不增绝对用量。消费只释放真实收到且有序前缀后的内存，MAX_DATA=max_initial+sum(consumed)，MAX_STREAM_DATA=stream_initial+consumed_prefix。DATAGRAM不占这两种额度；实际收到后可因应用期限丢弃且仍合法ACK。其丢失只由真实sender反馈判定，不重发。只有DATAGRAM outstanding的PTO发送无业务payload PING，不能复制媒体。MAX控制可真实重发，保留stream字段。

两端FIFO物理发送可有有限router等待队列；拥塞损失/ACK丢失均沿已有sender判据与定时器，不接入旧recovery_ready。输出保留PN、message/slice身份、实际send/arrival/ACK、flight/flow等待、loss/PTO/recovery、唯一业务区间与wire，另列业务完整/播放/版本/取消。

## 阶段与可扩展性

先小型共享窗口、多流额度、DATAGRAM loss、取消洞/非抢占、截图可用/过时及真实ACK竞争手算。网络数学无业务时需退化核既有闭环行为。接线采用ready依赖邻接表与逐flow待发队列，不逐包重放sender历史；完整30MB混合四格（FIFO/priority×立即/聚合ACK）是后续明确交付目标，不由小例替代。根代理主审小例前不运行大例。共享媒体接入不宣称真实TCP/H3匹配实验、握手或无线MAC实现。
