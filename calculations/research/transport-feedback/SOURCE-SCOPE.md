# Stage 1 发送方反馈重放：来源范围

本阶段固定 RFC9000 与 RFC9002 两份仓库既有官方原件，以及新读取的 RFC9002 Verified Errata7539 官方 HTML。`sources.lock.json` 记录原始 RFC Editor URL、revision、原路径、字节数、SHA256 和本轮重新核验时间；两份RFC复制后重新读取目标文件核对；Errata7539则从官方地址联网读取并重读核对。未全面核查其它后续errata。本任务不固定尚未使用的 CUBIC/BBR 文本，不用其名字描述 stage1。

## 实际阅读的条款

- [RFC9002](https://www.rfc-editor.org/rfc/rfc9002.txt) §5.1–5.3 与 A.7：最大新确认包的 RTT、首次样本初始化、min_rtt 不扣 ACK delay、后续延迟修正和估计更新。必须应用 [Verified Errata7539](https://www.rfc-editor.org/errata/eid7539)：先以旧 smoothed_rtt 计算 rttvar_sample 并更新 rttvar，再更新 smoothed_rtt，与 A.7 一致。原§5.3正文顺序是已确认技术错误，不是可任择的不同合同。
- RFC9002 §6.1–6.2.1 与 A.8–A.10：包阈值 3、时间阈值 9/8、推荐 granularity 1ms；丢失依据发送方收到的 ACK 和定时器，不能读网络真实 drop 状态。PTO 是探测机会，不自动宣布未确认包丢失；PTO 与 loss_time 的选择、有效 ACK 后重置和同刻事件次序应分列。
- RFC9002 §7.2–7.3 与 B.2–B.8：默认初始/最小窗口、slow start、NewReno 立即减窗参考分支、恢复周期和拥塞避免。B.5 的 app/flow-control-limited 条件抑制增长；一次 ACK 中先处理新丢失、再处理确认。同恢复 epoch 的旧包丢失不能再次减窗。
- [RFC9000](https://www.rfc-editor.org/rfc/rfc9000.txt) §4.1：MAX_DATA 与 MAX_STREAM_DATA 为接收方公布的绝对限额，普通 ACK 不会恢复一个可重复使用的流控额度。发送方只有实际收到更新后才可使用新限额，较小/重复更新无效。旧 offset 恢复不重复消耗新业务限额。
- RFC9000 §2.2、§13.3 与 RFC9002 §4.2：逻辑流区间和传输包身份不同；相同数据 offset 可由新 PN 携带。重复业务区间不能增加有效应用字节，每个新发送包仍产生自己的拥塞/网络占用。

## 时间、单位与参数合同

1. `sent` 时刻必须明确定义为本重放交给恢复算法的发送时间戳。输入已经给出发送记录时，stage1不推导串行器起止，也不隐含添加header/传播/RTT；ACK arrival是发送端可处理该ACK的时刻。传输发送机未来接入时必须明确把哪个序列化时刻映射至该时间戳。
2. `sent_bytes`/bytes_in_flight按QUIC包字节，包括QUIC头和AEAD开销，排除UDP/IP；max_datagram_size是QUIC适用的UDP payload上限，规范最小1200。STREAM offset/payload与该计量独立。只含ACK的包不占flight；含PADDING的非ack-eliciting包仍可能占flight，不能只用ack_eliciting推断全部拥塞占用。
3. 已确认、地址已验证、单路径、单application PN空间是输入合同，不由stage1执行握手或密码验证。双方向若调用两份状态机，应独立RTT/cwnd；输入反馈不是自动生成的反向ACK网络。
4. 新ACK、重复ACK、已判lost包的晚ACK必须区别记账，不能重复释放flight/增加cwnd或唯一业务量。loss/PTO事件必须记录原因；重放截止时间是可观察范围，不能假定所有有限输入后网络自然完成。
5. 伪码的0哨兵不能直接用于真实数值为0的教学时间：time_sent=0的包应正确增长/减窗；没有恢复epoch或没有RTT样本应用显式空状态。首次ACK/PTO/恢复发生在时钟0也应无歧义。
6. 接收消费、ACK生成/延迟、流控更新和网络瓶颈尚未闭环时，IsAppOrFlowControlLimited等字段只能是明确的外部观测输入；不能宣称算法已经从应用/接收状态完整推导它们。参考伪码所选浮点/有理数与整数舍入策略须明确。

## 有限范围与后续缺口

本阶段可以审查发送方在给定sent/ACK-arrival/limit-arrival记录上的RFC参考行为，并检查发送时是否满足已知cwnd与流控。它不证明这些记录来自合法真实网络栈，也不计算原图上传/模型/回传端到端闭环；30MB的带宽下界仅是独立单位/依赖手算。

完整 persistent congestion、ECN、拥塞避免整数实现、PTO实际probe发送与新包时序、spurious loss处理等，只能按作者明确实现并审查的范围声明。未实现分支须保留或拒绝，不能引用整份RFC就称全部覆盖。TCP的ACK/SACK/RTO、CUBIC、BBR、三PN空间握手、无线空口与实际业务/WAN测量均不由stage1完成。

独立审查结果后续写 `check-independent.py`、`check-independent.json` 和 `REVIEW.md`；本文件只固定来源与已读适用范围，不预先报告实现通过。

## 已确认勘误的审查修正

初稿只核未勘误正文，错误地向作者建议使用先更新SRTT次序；根审查指出Verified Errata7539后，本轮实际下载并阅读了完整官方HTML，已纠正本文并通知作者。勘误2023-06-13确认为Verified。本地8446 bytes，SHA256 `685a6ef4fabde4fe163d1e86d6fb7aea7ded40ceab07a8a70e8027a4a9d0e23a`。独立分歧样例：旧SRTT100ms、var50ms、latest180ms、ack_delay20ms（限额允许且minRTT100ms），adjusted160ms，var更新为52.5ms、SRTT107.5ms。旧错误顺序产生50.625ms，必须拒绝该期望。

## DATAGRAM 输入分支补源

候选明确支持DATAGRAM输入，因此另固定并重读RFC9221官方本地原件。实际适用§5.2–5.4：DATAGRAM是ack-eliciting、不做相同传输身份的可靠重发，不贡献MAX_DATA/MAX_STREAM_DATA，仍受共享拥塞控制。此分支仅确认运输ACK，不证明应用媒体成功交付。实现最终来源锁为四份（9000、9002、Verified7539、9221）。
