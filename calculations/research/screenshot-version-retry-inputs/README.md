# C69 单次版本重试：静态输入与手算合同

本包只设计新应用策略及独立手算，不改公共实现、旧五个完整负载、章节或任何运行源码。`build.py` 实际读取四份旧完整摘要，输出 `old-four-case-causes.json`、`contract.json`、`hand-oracles.json` 与来源锁；没有运行事件引擎，contract 也不冒充当前可直接执行的 application schema。

## 先区分旧负载真实失败原因

四格旧 `computer-use` 观察器均 `complete=false`、`complete_at=null`、缺少 `screen-action`、`usable=false`，预期版本和结果检查版本均为 v1。可成立的解释是动作消息未交付，不能将其描述成已观察到旧版本动作、服务端明确拒绝或已发生重试。保存的四份摘要及SHA支持这个范围；当前版本策略设计是新的有限反例，不重写这些历史结果。

## 有界流程与真实跨端通知

新轨迹最多 initial attempt0 + retry attempt1。客户端初始版本v0，t=0发送 screen0。t=1客户端版本变v1，同时向服务器发送真实32B version-notice，服务器只有收到此消息后才拥有v1知识。

服务器 screen0 完整到达后运行2秒非抢占任务。version-notice在运行期间到达不会撤销已开始的计算；任务完成才比较其截图版本v0与已收到的v1，并生成真实32B failure-notice。客户端只有收到该拒绝消息才允许消耗一次retry预算、开始0.5秒截图采集；采集开始读取本端当前版本，不在服务器伪造客户端截图。

retry截图实际上传、服务器再次计算，产生带attempt1/versionv1的动作。动作到达客户端时，还需比较客户端当时的版本；匹配才commit。晚到旧动作/重复拒绝不能覆盖有效attempt或启动第三次工作。

## 当前 schema 与新增接口

现有 schema 已支持本端 `message_delivered`、`task_completed` 依赖、固定 ready、compute resource、非抢占任务、cancel tag，以及截图观察器的版本判定。但观察器目前报告结果，不动态创建新消息/任务，也不把“usable=false”自动变成策略事件。

建议新增最小应用策略接口，复用原 network/sender：

- `policy.max_retries=1`、active attempt、notice去重集合和终态；策略状态归拥有该策略的端点。
- 实际任务完成后，本端 `task_result` 分支选择成功动作或失败通知；读的远端版本只能来自已交付消息。本端版本变化可生成真实版本通知，不能直接更新另一端状态。
- 实际 failure-notice 交付客户端后产生本端 `retry_authorized`，激活事先声明的 dormant attempt1 task/message模板。模板占用业务身份但未激活前不能发送、消耗credit或被计为已开始工作。
- `action_commit` 在客户端实际接收动作后执行版本/attempt检查，区分 received、valid、committed。错误动作不可只因网络交付就算成功。
- 每次截图使用独立 STREAM flow 或显式规定 offset 预分配；本合同使用screen-0/screen-1独立流，避免取消旧未发范围留下永久HOL。不是为旧流返还额度。
- 保留已开始非抢占task和in-flight范围。对未开始任务可明确取消，但不得从累计FLOPs中抹掉已完成的失败工作。本合同不实现任务中途抢占。

候选实现须严格验证模板可达性、最多一次重试、重复notice幂等、端点依赖及retry耗尽后的终态。不能用给定未来通知到达时间直接激活策略；下面手算时间是简化链路输入推导的独立期望，接实际网络时由真实packet/ACK/cwnd/流控决定抵达。

## 手算计时范围

采用两个非抢占FIFO **应用字节服务器**，上行3443B/s、下行32B/s，传播0。它是刻意便于手算的应用层 oracle，排除了包头、ACK、cwnd、无线PHY和恢复，不声称是共享空口实际结果。3443B截图沿用既有PNG负载字节数；版本通知、拒绝和动作各32B是新教学布局（不是旧64B动作的无声替换）。server2秒、capture0.5秒均教学耗时，不是模型或设备测量。

| 时刻 s | 实际事件与可用知识 |
|---:|---|
| 0 | screen0上传开始 |
| 1 | server完整收到3443B，work0开始；client变v1、开始发送32B通知 |
| `1+32/3443` | server收到版本通知，旧任务继续运行 |
| 3 | work0完成，server才发送拒绝 |
| 4 | client收到拒绝，retry capture开始 |
| 4.5 | capture完成、screen1上传 |
| 5.5 | server收到screen1、work1开始 |
| 7.5 | work1完成、action1发送 |
| 8.5 | client收到action1，本地v1匹配，动作有效提交 |

## 字节与逐任务矩阵账

完整分支上行 `3443+32+3443=6918 B`，下行 `32+32=64 B`，总 **6982 B**。对照“版本不变、一次截图+动作”的静态负载3475B，增加3507B。这个比较只说明声明字节增量，不推出端到端时间差。

真实VL模型的视觉编码/文本prefill/动作decode工作不能由3443B PNG推算。当前任务为可审计的**微型矩阵工作fixture**，明确不冒充某个VL模型：

| 每次server task的操作 | 矩阵 | FLOPs（FMA=2） |
|---|---|---:|
| feature_projection | `[8,16] × [16,8] → [8,8]` | 2048 |
| action_projection | `[1,8] × [8,4] → [1,4]` | 64 |

每次2112FLOPs，失败的work0仍完整消耗2112，work1再耗2112，总4224；server时间总4秒，capture另外0.5秒。capture矩阵成本为null而不是0，PNG解码、真实视觉encoder/attention/MLP/其他非矩阵工作均未计入。后续真实模型算例必须通过task.work_ref接既有已验VL算子账，不能把该小fixture标成实际模型计算量，亦不能用这4秒反推硬件吞吐。

## 预写负例

1. failure-notice丢失/迟到：客户端在通知实际交付前不得启动retry；手算4秒不再是可硬编码的触发。
2. 同一个拒绝重复交付：最多一次capture1，不能再次扣预算/生成新截图。
3. action1抵达前client变v2：本地拒绝、预算已耗尽、终态失败，不隐式生成attempt2。
4. version-notice晚于work0完成：server不能提前读v1并拒绝；它可能发v0动作，由client实际接收后本地判断。该分支需另外明确策略，不能复用本例“server在3秒已知v1”的期望。

本包完成输入合同与手算，不声称当前引擎已有动态重试、C69版本重试已实现或真实动作闭环已验收。
