# 有限 ACK 聚合：实现前合同

仅已确认单路径 1RTT application space。新 receiver.py 管理接收 ACK 状态，calculate.py 管理真实网络接线；复用冻结 transport-controller-loop sender/pacer/controller，不改旧源码。本轮不重写共享媒体。

旧 `ack_policy` 缺省或字符串 `immediate_each_packet` 保留原逐包快照行为与输出字段，完整回归旧10+controller6场景。新增字典策略启用聚合：`{"mode":"count_or_timer","every":2,"max_delay":"0.01","delay_exponent":3,"retain_packets":256,"reorder_immediate":true}`。每向独立计数/定时器，参数暂共同；every为正整数，max_delay为非负秒，delay_exponent为0..20，retain_packets为正整数。max_delay须能容纳至少一个编码tick或为0；输入中的sender.max_ack_delay若另给必须与该策略相同，不能声明接收延迟却让发送方以0计算PTO。

新到ack-eliciting包纳入未报告集合。已接收纯ACK可纳入范围但不启动计数/定时器；本轮不模拟网络复制（新PN恢复不是duplicatePN），receiver纯状态可核重复PN。重复ack-eliciting接收可触发反馈但不重复计入新PN阈值，首次接收时间不被更新。乱序策略按最高已收到ack-eliciting PN判断：较低PN，或较高PN且两者之间有实际尚未收到的包；纯ACK也用于判定中间是否真的缺包，若选择立即则产生待ACK信号。无ACK_FREQUENCY协商，不称客户端默认。

第一个尚未报告ack-eliciting包安装固定deadline；随后接收不能滑动延长。计数达到阈值、deadline、明确乱序/重复触发只创建一个待发送ACK占位。物理发送开始前它可以覆盖更多实际到达PN。开送时刷新范围与最大PN接收时间、编码delay并清空本次覆盖的未报告触发状态；旧timer以generation失效。同刻先接收/serializer完成，再ACKdeadline，再网络pump（既有真实到发送方ACK优先于sender timer保持）。已开始ACK不能追溯覆盖后来到达。

范围保留是有限声明：最近retain_packets个接收PN加所有未首次报告的ack-eliciting PN；至少每个新触发PN被报告一次，可重复报告但不需要每ACK展开整条历史。纯ACK被遗忘不影响flight。遗漏更早已报告PN不冒称它们未到达；若先前ACK丢失且不再保留，发送方须真实loss/PTO恢复。输出明确retention，不以无界累积范围造成O(N²)。ACK ranges必须由实际接收集合压缩而来，不跨洞。若未报告集合超显式规模上限，拒绝受限合同而非丢弃未报告PN。

ACK delay = 开始发送时间 - 本ACK最大PN第一次接收时间，量化为 floor(delay秒*1e6 / 2^exponent) 的QUIC varint；解码值供sender处理。输出raw、encoded、decoded、量化差。应用生成后反向serializer排队属于ACK延迟，若超过max_delay明确记录实际超限，不伪造更短wire delay；sender按现有RFC算法使用它。传播与ACK自己串行时间不属于接收端ACK delay。ACK只含已知PN，收到ACK的发送方继续自行判样本资格/扣减，不从receiver直接修改RTT。

ACK包预算在actual snapshot时验证QUIC varint ACK frame字段（type,largest,delay,range_count,first_range,每后续gap/range）加明确声明header+AEAD预算；ack_bytes是整个QUIC packet声明，另加28B IPv4/UDP。若范围装不下不伪造64B包；初版受限输入直接报错（保存可诊断原因），不引入隐式分包策略。反向纯ACK不进flight、不pace但占真实serializer；MAX/probe仍ack-eliciting。ACK无网络到达不能解除flight。snapshot必须保存于已发packet身份，后续接收不能改写。

结果增加ack_events（receive/trigger/start及编码/范围/超限），ack_state final（pending/timer/retention）仅在新策略开启时出现。旧默认数学输出保持原样。协议来源由独立reviewer固定并核官方条款；合同若与原件冲突必须先修正，不能按预写数值强行实现。

保留范围有界不等于全内存恒定：history保留全部首次接收PN与时刻用于去重/验证，总量随实际包数线性增长；只有每ACK报告范围受retain_packets及未报告上限约束。
