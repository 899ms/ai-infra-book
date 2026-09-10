# ACK 聚合独立来源与适用范围

本目录固定并重读三份已有官方原件：RFC 9000、RFC 9002、Verified Errata 7539。URL、字节数、SHA256、复制来源与本次校验时间见 `sources.lock.json`。没有重新抓取在线版本，也不将该快照描述成当前浏览器实现。

本轮限于连接已确认、单路径 Application packet number space 的声明接收策略。握手空间、ACK_FREQUENCY、ECN、迁移、内核时间戳、真实浏览器默认值均不由这些实验覆盖。旧逐包候选保留原证据身份。

## 实际读取的规范映射

| 来源 | 适用规则 | 对候选的约束 |
|---|---|---|
| RFC 9000 §12.3 | 接收端不得重复处理同 PN；可以维护递增最小 PN | 重复包不得重复贡献、刷新首次接收时间；若不使用接收下界，必须保留足够历史去重 |
| §13.2、§13.2.1 | ack-eliciting 包在 max_ack_delay 内确认；非 eliciting 可顺带确认但不能独自触发非 eliciting 应答 | 纯 ACK 不创建 ACK 循环；队列超期必须如实记录，不能冒称满足最大延迟 |
| §13.2.1–13.2.2 | 乱序、前向缺口 SHOULD 立即 ACK；最高比较对象是已收到的 ack-eliciting PN；通常每至少两个包 ACK 一次，但允许其他策略 | every、timer、重复包重 ACK 是显式模型政策，不是浏览器默认；纯 ACK 插入不应悄悄改变所宣称的规范比较对象 |
| §13.2.3 | 帧过大可省略较旧范围；丢弃范围后须确保不再接受其中 PN；保留最大 PN | 最近 256 PN 仅限制 ACK 发送历史，不自动限制完整 duplicate history；丢 ACK 后仍可依靠后续 ACK 或真实恢复 |
| §13.2.5 | 报告最大被确认 PN 的接收至发送延迟；不是最新到达包的接收时间 | actual-send 策略应在物理发送开始刷新 ranges、最大 PN 和其原接收时间；ACK 自身序列化及传播不计入 delay |
| §18.2 | ack_delay_exponent 默认 3，范围 0..20；max_ack_delay 整数毫秒且小于 2^14 | 接收策略秒值须映射合法毫秒传输参数；严格类型和边界检查 |
| §19.3–19.3.1、§16 | ACK Delay 解码为 field × 2^exponent 微秒；每个字段是 QUIC varint；range/gap 相对编码 | floor 是本实验声明的编码舍入政策；逐字段计字节，不能把任意多个离散范围塞入固定 64B |
| RFC 9002 §5.1–5.3 | 仅在最大被 ACK PN 新确认且存在新确认 eliciting 包时采 RTT；首次样本不用 delay；minRTT 取原始观测 | 最大 PN 本身可为纯 ACK，只要该帧含其他新确认 eliciting PN；重复最大 PN 不因新低 PN 再采样 |
| RFC 9002 §5.3 与 Errata 7539 | 确认连接后 delay 受 peer max_ack_delay 限制；不得扣至 minRTT 以下；先用旧 SRTT 更新 variance | 保留 raw、encoded、decoded、实际扣减和 sample eligibility 的证据；不可使用已被勘误纠正的旧更新顺序 |

## 范围与容量的明确边界

完整 PN history 保留去重与首次接收时刻；最近 retain_packets 个 PN 加未首次报告集合用于输出 ACK 范围。因此这是有限输入包预算下的模型，不是常数内存接收器。若将来删除完整 history，必须另实现明确拒绝下界或同等防重机制。

对于 256 个偶数 PN 0..510，共 256 个 singleton ranges，raw delay 为零：type 1B、largest 2B、delay 1B、range count 2B、first range 1B、255 对 gap/range 各 2B，总 ACK frame **517B**。加声明 header/tag 24B 为 **541B** QUIC packet；64B 必须拒绝。该 24B 是布局假设，不是所有 QUIC 连接的通用头长；外层 IPv4/UDP 28B 另记。

接收端当 ACK 开始发送时才冻结快照。发送开始后到达的包只能由后续 ACK 覆盖。排队阶段刷新不是规范命令的唯一实现方式，而是本候选明确选择的事件模型；它避免对已发送字节进行追溯修改。不得把输入许可的 serializer 超期行为描述成满足 max_ack_delay 的合规保证。

独立预写数值见 `independent-oracles.json`。这些期望不来自候选运行结果；实现运行与最终 hash 将另记，不能把本文件当执行通过证据。
