# 公共来源映射

本次只新增一份官方 RFC Editor Verified Errata7539 HTML 与公共总锁的一条记录。RFC9000、RFC9002 和 sender 兼容 DATAGRAM 分支所需 RFC9221 均复用已有公共原件，未重复下载或复制它们。

| 用途 | 公共路径 | provenance group |
|---|---|---|
| 绝对 flow control、ACK、PN/STREAM 重传 | sources/protocol-rfc/rfc9000.txt | protocol-rfc |
| RTT、loss、PTO、参考 NewReno | sources/protocol-rfc/rfc9002.txt | protocol-rfc |
| §5.3 方差先使用旧 SRTT，再更新 SRTT | sources/protocol-rfc/rfc9002-errata7539.html | transport-feedback-errata |
| sender 已有 DATAGRAM 兼容分支 | sources/shared-media-rfc/rfc9221.txt | shared-media-rfc |

新增勘误 revision 为 `RFC9002 Verified Errata7539`，原 URL 为 https://www.rfc-editor.org/errata/eid7539，8446 字节，SHA256 `685a6ef4fabde4fe163d1e86d6fb7aea7ded40ceab07a8a70e8027a4a9d0e23a`。独立 group 保持旧 protocol-rfc 恰好七条的合同，文件置于已有源目录使现有 reproduce 输入文件枚举自动涵盖它。全部四份已用公共 `read_source` 实际核字节及哈希。

RFC9000 §13.2.5 是 ACK Delay 边界的来源：端点有意控制的等待与不控制的 host 延迟应区分。本参考立即生成 ACK，随后串行队列明确作为外部网络服务，ACK Delay 为零；不能把这个声明推广成所有发送缓冲/pacer 延迟都应排除。具体适用段落和限制保留在研究候选 `../transport-closed-loop/SOURCE-SCOPE.md`。

公共 source 校验必须按用途筛选精确 revision 集合，逐份调用 read_source；不得把共享 group 全部条目误当成本模型依赖。官方勘误是 §5.3 的有效修正，不能让旧正文错误次序成为可选模式。
