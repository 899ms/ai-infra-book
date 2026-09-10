# 固定来源与适用范围

已从仓库既有官方 RFC 原件复制六份全文到 `sources/`，逐份重新读取目标文件并核对 bytes/SHA256。`sources.lock.json` 记录原始 RFC Editor URL、RFC 版本、复制路径、校验时刻；这是本地封存原件的再次固定，没有声称本轮重新联网下载或核查全部后续 errata。以下列出实际阅读的正文段落；RFC 语义依据与本候选教学假设必须分开。

| 固定来源与已读段落 | 本题适用内容 | 不能据此声称 |
|---|---|---|
| [RFC 9221](https://www.rfc-editor.org/rfc/rfc9221.txt) §5–5.4 | DATAGRAM 尽早交付、不随丢失重发，但 ack-eliciting；与可靠流共享连接拥塞控制。拥塞受限时等待或丢弃，可声明发送过期时间 | DATAGRAM 免拥塞限制；transport ACK 证明媒体已播放；没有 ACK/PTO 开销 |
| [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.txt) §2.2–2.3、§4–4.1、§13.3 | STREAM 按 offset 有序重组、重复数据不增加业务贡献；优先级来自应用；逐流与连接接收限额；丢失信息由新帧/包再次携带 | 简单 packet 信用就是 QUIC MAX_DATA；QUIC 规定本候选 FIFO/EDF；同包号重传是 QUIC 恢复 |
| [RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.txt) §7–7.2（并核对§6/7目录边界） | QUIC 恢复与拥塞有具体算法，文中控制器类似 NewReno；cwnd/bytes-in-flight 以 bytes 计，纯 ACK 不占拥塞 bytes-in-flight，仍需真实链路发送 | 固定窗口/单次声明重传等于 NewReno/CUBIC/BBR 或 PTO 实现；ACK 不占串行出口 |
| [RFC 9114](https://www.rfc-editor.org/rfc/rfc9114.txt) §2、§4.1.1 | 请求/响应使用 QUIC 流；一个流的丢失不直接阻止其他流进展；HTTP 帧与 QPACK 独立存在。取消与未处理的拒绝区分，部分处理后不能冒称未执行 | 所有跨流阻塞完全消失；应用取消控制包等于已实现 HTTP/3 RESET_STREAM/STOP_SENDING；收到取消自动撤销已产生副作用 |
| [RFC 8836](https://www.rfc-editor.org/rfc/rfc8836.txt) §2 要求1–5 | 实时媒体需要在有用带宽、低延迟、竞争流、公平性、突发/启动响应间权衡；网络到达与应用可用须分开 | RFC 指定通用播放 deadline、固定丢帧阈值或本例调度算法；本候选已经实现符合其全部要求的实时拥塞控制 |
| [RFC 3550](https://www.rfc-editor.org/rfc/rfc3550.txt) §1、§5.1、§6.4.1 | RTP 的序号/采样时间戳可区分生成、到达、顺序；RTP 本身不保证及时可靠交付。RFC jitter 是具体平滑统计量 | 普通到达时刻差、播放缓冲时长或停顿总量可以直接命名为 RFC RTP jitter；本例教学音频包是完整 RTP/RTCP 实现 |

## 审查必须维持的语义边界

1. RFC 9221 §5.3 明确 DATAGRAM 不贡献逐流或连接数据限额；§5.4 的共享拥塞预算是另一概念。若有限模型让不可靠媒体也占固定发送信用，须命名为教学发送窗口；不得让 DATAGRAM 的永久丢失卡住可靠流的累计接收前缀。若可靠流接收窗口未实现，应直接列缺口。
2. DATAGRAM 在 QUIC 层没有 stream ID（§5.1）；音频 flow ID 是应用字段，不冒称 QUIC STREAM ID。帧本身不能分片；模型应用层媒体分块与实际路径 MTU/帧编码约束分开。
3. 每次重发仍消耗出口与发送字节；应用区间只有首次有效收到才增加唯一贡献。固定单次丢失/恢复的时间是输入，不能由来源引用伪装为已经实现 ACK 推断或 PTO。
4. 全连接整体有序与逐流有序的固定 trace 对照，只隔离交付依赖，不是完整 TCP 与 QUIC 栈性能。QUIC 仍有共享拥塞/流控、HTTP/QPACK 和应用依赖。
5. 丢弃过期单元、播放槽、缺音隐藏、ASR 必要输入、模型时长、截图版本和取消生效规则均为应用合同。可靠 RAW/成片不能因媒体 deadline 被截断后仍称完整；缺音不能当同质量加速。
6. 双向全双工串行资源不等于 Wi-Fi 共享空口；ACK 与 MAC ACK、争用/切换、蜂窝 bytes/电量仍属 C69。具体 CUBIC/固定 BBR、一般恢复、完整编码、真实业务/WAN 记录仍未由此候选实现。

独立数学与事件审核另见后续 `check-independent.py`、其 JSON 和 `REVIEW.md`；本文件仅完成来源固定和已读适用范围，不提前报告候选通过。
