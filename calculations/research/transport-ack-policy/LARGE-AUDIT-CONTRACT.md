# 原书 ACK 聚合大例：独立验收预案

在三份新完整 trace 落盘前写定。输入为 30,000,000B 上传、5,000,000B 完整响应、模型耗时 0.3s，上行 20Mbps、下行 100Mbps、每向传播 0.05s；三种 controller 为 NewReno、CUBIC+HyStart++、固定 BBR 参考适配。ACK 字典策略 every=2、max_delay=0.01s，其余参数和统一 1200B in-flight padding 必须逐字段比较，不能把不同负载当控制器对照。没有在此预定完成时刻或性能排名。

## 数据与线上字节代数

每个数据包最多携带 1168B STREAM 业务内容，另有声明 32B QUIC 头/帧预算。因此原始上传至少 25,685 个数据包，原始响应至少 4,281 个，共 29,966 个。上传尾有效内容 1088B、padding 80B；响应尾有效内容 960B、padding 208B。若没有重发、额外控制或探测，原始数据 QUIC 字节 35,959,200，外层字节 839,048，原始数据线上总额 **36,798,248B**。

ACK 数量记为实际 A_up、A_down，不预写成 ceil(数据包数/2)。双向数据和 pure ACK 共享本方向 PN 空间；缺口、即时触发、尾计时器、发送前范围刷新和反向 serializer 阻塞均可能改变数量。一份 ACK 可包含旧范围，覆盖的 PN 数也不等于新确认的 in-flight 包数。

若 ACK 固定 64B QUIC + 28B 外层，线上总额 = 36,798,248 + 92 × (A_up+A_down) + 额外传输的实际线上字节。额外项按重发数据、PTO probe、MAX/control 分列；不能隐藏进业务字节或只用 union 掩盖重复传输。无额外传输时，上行基准数据线上 31,541,180B，下行 5,257,068B，再分别加本方向 ACK 线上额。

逐方向 STREAM offset 必须覆盖 [0,目标大小)，无漏字节；额外发送用区间多重性计数，报告传输有效 payload 总和与业务唯一 payload 两种口径。PN 必须唯一、递增；重发旧 offset 必须用新 PN。ACK 本身不贡献业务、不占 congestion in-flight、不形成 ACK 循环，但占物理序列化时间。

## 从真实到达重建 ACK

按接收端实际事件时间重放本方向已到达 PN，而不是用发送端全部 PN 或 ACK 声称的范围作事实。掉包/尚在途 PN 不可被确认；同刻按声明 arrival-before-pump 顺序纳入。最近 retain_packets 范围加未首次报告集合必须独立重建；保留完整历史防重，避免用发送范围遗忘状态伪造第二次接收。

每份 ACK 的最大 PN、该 PN 首次接收时间、ranges 与实际开始发送时快照一致。开送后到达不得追溯进入已有 ACK；等待中的占位 ACK 应在开送时刷新。varint 字节用独立宽度公式核算 type/largest/delay/count/first-range/gap/range 加声明头预算，确认没有超过 ACK QUIC packet 大小。

raw_delay = ACK send_start − 首次接收 largest PN 的时间。encoded=floor(raw_delay/tick)，tick=2^exponent µs；decoded=encoded×tick，故 0≤raw−decoded<tick。raw_delay 可以因实际排队超过 10ms；必须逐份核 exceeds 标记并计次数、最大超额，不把 max_delay 当真实观察的硬上界。自身 serialization 和反向传播不在接收 ACK delay 内。

## 发送方采样与控制器反馈

每个真正到达的 ACK 才产生一次发送方 ACK 输入，ranges/decoded_delay 必须对应其已发快照。重复覆盖旧 PN 不得重复释放 flight、增长 delivered 或贡献新业务。ACK 丢失不产生虚假确认。采 RTT 的资格按 RFC9002：最大被确认 PN 新确认，且至少有一个新确认 eliciting 包；最大 PN 自身可为 pure ACK。已确认最大 PN 加新低 PN不产生新样本。由真实 sent/ACK arrival 计算 raw RTT，不能只验证日志自洽。

根另独立审查 delay 扣减/minRTT/Errata7539 的小例和接线；大例仍应逐实际采样检查 decoded delay 来源、peer cap 与 raw→adjusted 的关联。若 BBR callback 使用 adjusted RTT，应核对这一实际输入，不能沿用旧逐包 delay=0 场景的 raw RTT 等式。

BBR transport delivered 按每 PN 首次 ACK 计包，包含旧 lost PN 的晚 ACK，但不包含 pure ACK；业务仍按 STREAM offset 去重。采样发送快照、最大选中发送时间、send/ACK interval、单位转换和 app/flowlimited 状态应与真实轨迹关联。HyStart round/frontier 不可由 ACK 数乘2推定；CUBIC 的阶段和减窗必须报告实际出现的状态，不预设此大例必然进入 avoidance。若出现 loss/PTO/persistent，必须单独解释与核状态，不因无注入丢包就删去相关轨迹。

## 物理、业务与数值

逐方向 serializer 区间互不重叠，服务时间=wire_bytes×8/rate；无 router 时 arrival=send_end+0.05s，两个方向可以并行。模型启动依赖完整上传实际到达，model_end−model_start=0.3s；响应首发不得早于 model_end，完整响应时刻取所有必要唯一字节实际到达之后，不等同最后 ACK。

每条数值日志单独检查 rounded−original=local_error、所声明网格及局部舍入界。pacer 向上取整误差、sender 的有限网格与 CUBIC segment 转换使用各自单位；BBR µs/u32/整数带宽为另一个明确边界。局部误差不能直接称整条轨迹的累计误差上界。统计实际舍入条数、最大绝对局部误差及超期 ACK，不能只核汇总字段。

完整 JSON 按顶层数组流式处理，三场景逐份释放；记录正式输入、结果及源码始末 SHA。保存结果与 manifest 的校验仅证明冻结身份；数学检查必须另从包身份与物理事实重建。不修改公共模块、不重启 reproduce，不以旧小例或作者摘要替代新大结果审查。
