# ACK 策略阶段独立审查

后续验收：加入实际 RTT 输出后的 calculate `58718e22…` 已重跑 8 个小网络场景；三条原书 30MB/5MB 聚合轨迹也已完整独立通过，见 `LARGE-INDEPENDENT-REVIEW.md`。下文保留最初阶段的执行范围与当时缺口，不将后续覆盖倒填为早期已验证。

已固定并读取三份官方来源，见 `SOURCE-SCOPE.md`、`sources.lock.json`。仅新 research 目录发生写入；没有修改作者实现、旧候选或公共内容。

当前实际核验版本：calculate.py `5e921efa58d85f7f77dd9ba945f20facbb91cf2f6033f25145092e9750dd5c38`，receiver.py `a8a44b09c95d76501821a20a4737fdc352d564de706f98082b2c5f7f55949378`。两份执行结果均记录源码 SHA；网络运行始末一致。

`check-receiver-independent.py` 实际通过 19 项：计数与尾包计时、排队期间刷新、最大 PN 而非最新到达时刻、重复 PN 原时间、3µs 编码余数、256 离散范围精确容量和拒绝原子性、纯 ACK 不触发、同刻到达/计时器仅一个 ACK、已发送快照不再变化、旧范围省略后仍然去重，以及 8 项非法参数。

`check-network-independent.py` 实际运行七个作者固定场景，完整结果与保存结果相同；独立从实际到达包重建其 14 个 ACK 的范围与最大 PN 接收时刻、编码、发送方反馈时刻，并检查逐方向物理序列化互斥与线速。前四个场景还核预写整数时间，不只比较作者保存的输出。第五个 MAX 场景确认纯 ACK 可顺带进入范围但没有 ACK 循环。

作者另加两个反向忙场景也已实际核验：ACK 2–4s 的快照仅 PN0；第二 ACK 4–6s 在首例包含同刻到达的 PN2，delay=0；次例没有 PN2，delay=1s，明确超过 0.5s 声明。这两例在核心实现后新增，与最初预写 oracle 分开。

另实际构造一个反向 serializer 忙场景：1168B 上传及响应，下行 736bps、每向传播 1s，响应数据从 2s 发送，1228B 线长的服务时间为 307/23s。尾 ACK 在 2.5s 到期却无法抢占响应包，实际开始为 **353/23s**，raw ACK delay 为 **307/23s**，显式超过 max_delay=0.5s；结束为 376/23s。该例通过，确认不会把定时器触发时刻误作真实发送时刻，也不隐瞒超期。

来源审查指出的 highest-PN 比较对象已由作者改为 largest_eliciting；完整接收 history 的线性内存与仅限制输出范围的区别也已说明。没有以固定 64B 容量接受任意 256 离散范围：本合同选择明确拒绝无法装入的快照，尚不是通用 ACK 帧截断/分包实现。

本阶段仍未独立重跑旧默认大例兼容性或新聚合 30MB 三控制器场景；这些不能由上述小例代替。`independent-oracles.json` 中发送方 variance、delay cap、minRTT guard、纯 ACK 最大 PN 样本资格等仍是预写期望，并未在本轮两份 checker 中全部重新执行；旧发送方的已有验证不自动冒充此次端到端验证。此模型的 count/timer/reorder/duplicate 与 floor 编码均为声明政策，不代表浏览器默认策略或完整 QUIC 实现。
