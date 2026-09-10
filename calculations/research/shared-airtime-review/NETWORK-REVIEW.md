# 共享空口小型闭环独立验收

实际执行 `python3 calculations/research/shared-airtime-review/check-network-independent.py`，16 个小型输入、14 份已有完整结果各两种 disabled 入口，共 386 项检查通过。报告为 `network-review-result.json`。没有执行大例，没有修改作者引擎或公共代码。

被审候选 `calculate.py` SHA-256 为 `37c442824b5b127407658a75b21638882ee5a75ff08156cfc716b141d1b75f6b`；`airtime.py` 为 `131ce04a522e641ece9a851f9e6ab3b1771b7fc83a5417be3b2a52c53a717658`。报告锁定候选、输入、预写 oracle 和导入的公共 Python 文件，检查运行前后不变。

## 实际执行的范围

预写 `network-hand-oracles.json` 十例全部通过。它们与本地五组 oracle 的区别是明确追加有限 WAN：DATA 1228 B 在 9824 bps 上占 1 秒，ACK 92 B 占 `23/307` 秒，而本地 oracle 的 1/0.25/0.5 秒为空口教学服务。检查没有把本地尾帧 6.5 秒当成端到端 WAN 结果。

- 双方向共享：up 空口 `[0,1.25]`、down WAN `[0,1]`、down 空口 `[1.25,2.5]`；server 接收 up 为 2 秒，client 接收 down 为 2.25 秒。disabled 双方向都是 1 秒接收。
- 两帧 immediate/every2：transport ACK 数为 2/1，总成功空口服务 3.5/3 秒。
- 忙时 client ACK：发送在 3.5 秒，范围 `[0,1]`，最大 PN 在 3.25 秒接收，raw delay 0.25 秒。max_delay=0.25 和 0.1 分别产生未超过/超过标记；没有把初始 deadline 当实际发送或最大 PN 接收时间。
- up MAC ACK 丢失：原 PN 0 的两次 DATA 空口 `[0,1]`、`[2,3]`，失败 1.5 秒才知道，重试 MAC 成功 3.25 秒才知道；WAN 转发和原 sender sent 各只有一次，server 在 2 秒唯一交付。
- 两次 DATA MAC 丢失：1.5/3.5 秒获知失败；端到端 PTO 在独立输入所决定的 4 秒触发，新 PN 1 空口 `[4,5]`，server 6 秒唯一交付。没有借 MAC failure 直接声称端到端 loss。
- 三帧尾部 immediate：server 尾帧 5 秒，6 秒固定槽播放至 6.25 秒，总空口 5.25 秒。
- every4：server 前两帧 2/3.25 秒，ACK deadline 6 秒，先走 WAN `23/307` 秒再进空口，client ACK 接收 `7767/1228` 秒。第三帧在 ACK 自身 MAC 确认后开送，server 尾帧为 `5265/614` 秒，错过 6 秒槽、缺音 0.25 秒；总服务 4.75 秒。

通用轨迹断言逐条核对全局 reservation 不重叠、每方向 PN 唯一传输记录、传输发送先于 radio、重试不早于实际反馈加等待、WAN 在 AP 接收后才开始、上行 WAN 字节与串行时长一致、下行空口不早于 AP ready、端到端 ACK 事件只能在反向 ACK 包实际抵达时出现。所有 started attempts 的 received/feedback_known 与 horizon 对照，不能因预先知道损失选择就提前暴露发送方知识。

## 新增反例与修复复验

### 下行同 PN 重试不能再次进入 QUIC

Root 已发现并通知作者的缺陷是下行 MAC duplicate 再次调用 transport `acknowledge_received`。本审查开始执行时作者代码已有 `air_receive` 的双方向重复过滤；没有保存或声称实际复现旧版失败。

独立将一帧 up MAC ACK loss 场景改成 server→client：第一次 client 接收在 2 秒，随后 MAC ACK 丢失、原 PN 0 重试。对 legacy immediate 与 count_or_timer(every=1) 各实际执行一次：

- 仍只有原 PN 0 两次 MAC attempt；
- 应用只在 2 秒唯一交付；
- 上行 transport ACK 总数只有 1；
- count receiver 只记录一次 receive，不额外触发重复 ACK。

这直接覆盖修复的行为边界，不能用“应用字节仍为 1”替代，因为旧缺陷可以不重复应用字节却重复生成 transport ACK。

### 失败尚未到时不暴露未来反馈

把 up MAC ACK loss 场景 horizon 截到 1.1 秒：DATA 已到 AP、WAN 尚未到 server；第一次失败要等 1.5 秒。实际结果只有一个 attempt，feedback_known=false，无 mac_feedback 事件、无重试、无应用交付。

### OFDM source ACK 在真正发射时才冻结

一帧 down，WAN 在 1 秒到 AP；source profile 下 DATA 在 `1s+242µs` 被 client 接收、MAC 交换至 `1s+302µs`。ACK 自身还需前置 34 µs，因此实际空口 DATA TXSTART 为 `1s+336µs`。

实际 count receiver snapshot 正在该时刻生成，raw delay=94 µs，8 µs 单位 floor 编码为 11，decoded=88 µs。该反例能够区分错误地在 reservation 开始冻结（会得到 60 µs）或在首次 ACK 触发时冻结（会得到 0）。DATA 与 ACK 承载 PSDU 也独立确认 1264/128 B，未重复添加 IP/UDP。

## disabled 精确回归与保留边界

使用既有 `media-feedback-loop/result.json` 的 14 份完整小例：不传 wireless_access 和显式 `{'enabled': false}` 两种入口，返回的完整结构都与旧结果逐字段相同，非仅比较 summary 或完成时间。

当前没有发现上述小例范围内新的阻断性缺陷。通过不表示完整混合大例、任意路由队列/丢包组合、任意可编辑 PHY、竞争碰撞或真实 802.11 实现均已验收；也不将 source profile 标为 IEEE 原文逐条核验。本次没有执行大例。


## 新版覆盖与旧版归档

本报告现对应实际重新执行的 `37c4428` 版本，不能将此前 `9c5f` 的结果自动外推。本次重跑全部既有小例，并新增下面两项。旧报告、旧完整结果证据和当时的检查脚本原样保存于 `archive-9c5f/`，附 `archive-manifest.json` 文件哈希；当前报告没有抹除旧版覆盖边界。

### PHY 前导阶段 44 µs 截止

source profile 的前置空等为 34 µs，前导从 34 µs 延续到 50 µs。horizon=44 µs 时 DATA PPDU 刚开始 10 µs，AP 尚未接收；不能按整个 DATA 持续时间等比例捏造 IP 字节。

实际断言：一个已开始但未收到的无线 attempt、TXSTART=34 µs、observed reservation=44 µs；`serialized_wire_bytes_by_horizon=null`，明确未提供物理层逐字节量；`wan_serialized_ip_bytes_by_horizon=0`，无应用交付。这核验的是拒绝错误 byte/time 混算，并非已实现 PHY bitstream 输出。

### 下行尚在 WAN 途中

DATA 1228 B 在 9824 bps WAN 上需要 1 秒，horizon=0.5 秒时只串行了 614 IP 字节。实际结果尚无无线 attempt；发送记录 `arrival` 和 `received_at` 都为 null，预定 AP 抵达时间单列 `wan_arrival=1`，应用未交付。该字段表示计划到 AP 的时间，不能冒充实际 client 抵达。

最终执行共 16 个实际小输入、14 个完整旧结果各隐式/显式 disabled 两入口、386 项检查。源码前后哈希一致，无大例执行，无正文及公共文件修改。
