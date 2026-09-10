# 同一反馈网络上的 NewReno、CUBIC + HyStart++ 与 BBR 参考

这是研究候选：已确认单路径、1-RTT application packet-number space、有限上传→服务器计算→完整响应。控制器接收真正经过反向 serializer 和传播的 ACK；接收/消费后生成的绝对 MAX 更新同样占用链路，并等待更新实际到达发送方。它没有实现握手、迁移、完整 QUIC 编解码、ACK frequency 协商、多媒体调度或全部 TCP 行为。BBR 是固定 Linux v6.6 函数的明确 QUIC packet-count 适配，不能称 Linux TCP 的实际端到端测量。

`INTERFACE-CONTRACT.md` 是实现前合同；`bbr-adapter-contract.md` 解释 BBR delivery sample、初始化、恢复及 EDT 映射；`PERSISTENT.md` 说明持续拥塞证据。源码都在本目录；所依赖的旧 CUBIC、HyStart++、BBR 参考保持冻结。

## 可编辑输入与复算

```bash
# 原有十个场景，未启用新控制器，保留旧数学与全部轨迹
python calculations/research/transport-controller-loop/calculate.py --output /tmp/legacy-network.json

# 任意单个可编辑 JSON
python calculations/research/transport-controller-loop/calculate.py --inputs /tmp/network-input.json --output /tmp/network-result.json

# 六个固定控制器输入，以及单个/全部完整结果
python calculations/research/transport-controller-loop/run-scenarios.py --write-inputs
python calculations/research/transport-controller-loop/run-scenarios.py --scenario book-bbr
python calculations/research/transport-controller-loop/run-scenarios.py
```

`controller-scenarios.json` 保存六个新增输入。每个 `NAME-result.json` 保存完整结果，`NAME-manifest.json` 保存生成前后相同的六源码 hash、结果 hash、业务摘要和计算用时。`calculate.py` 的默认十场景仍为冻结基线，不能将新增六场景误计入该默认入口。`development-*.json` 是历史开发摘要，不是完整轨迹验收。生成器不会删除它们。

`run-scenarios.py` 每次验证网络、CUBIC、HyStart++、BBR 官方来源锁，并在计算前后核对。`source-audit.json` 是首批正式结果生成后补做的全部原件审计，明确没有伪称事前检查。首批网络/CUBIC/HyStart 原件在各内核内已核验；BBR 固定函数代码当时已校验，补审其官方原件。后续 runner 将全部原件在前后核验。结果内 `reference_sources` 保留网络原件，控制器来源可沿上述审计文件和相邻冻结目录锁追溯。

## 六个对照的实际范围

| 输入 | 上行 | 下行 | 业务 |
| --- | --- | --- | --- |
| book-* | 20 Mbps 出口，50 ms 传播 | 100 Mbps 出口，50 ms 传播 | 30,000,000 B 上传，声明 0.3 s 计算，5,000,000 B 响应 |
| router-* | 1 Gbps 出口→20 Mbps 中间队列，50 ms 传播；10,000,000 B 等待容量 | 100 Mbps 出口，50 ms 传播 | 3,000,000 B 上传，声明 0.3 s 计算，500,000 B 响应 |

每组只有 controller 名称变化。全部在途数据报填充至 1,200 B QUIC UDP payload，另加 28 B IPv4/UDP；纯 ACK 为 64 + 28 B。尾包、MAX、probe 也需要真实 padding 和时间。每个满 STREAM 包承载 1,168 B 业务；不能用 1,200 B 当有效业务字节。双向 serializer 非抢占，ACK 可以绕过 pacer 债务但不能绕过正在服务的包。

首批正式结果：

| 原书场景控制器 | 上传完整 / s | 响应完整 / s | modeled wire / B | 唯一业务 / B |
| --- | ---: | ---: | ---: | ---: |
| NewReno + pacing | 13.087839089 | 14.521037240 | 39,555,120 | 35,000,000 |
| CUBIC + HyStart++ + pacing | 13.087839089 | 14.521037240 | 39,555,120 | 35,000,000 |
| BBR 适配 | 13.344766867 | 14.974125992 | 39,555,120 | 35,000,000 |

三者各有 59,932 个实际发送包，业务均完整。上述数值是声明模型的计算结果；不包含真实实现的 CPU、无线链路、加密、握手等开销。不可据此排列真实互联网控制器性能。BBR 无已测 RTT 种子时使用固定参考的未知 RTT 启动政策；NewReno/CUBIC 的配置 RTT 是猜测，不是免费测量。控制器的启动政策也会影响该有限业务。

原书的瓶颈设在出口，RTT 从实际开始发送计时，不包含发送前排队；该案例的 HyStart 一直处在 slow start，不能用它声称立方增长或 CSS 的吞吐效果。额外 router 场景出现真实中间排队，CUBIC 实际进入 CSS，结束时累计 3 个 CSS round，尚未完成 5 轮 CA 交接。完整 HyStart→CUBIC 交接另由独立预写手算/回调检查覆盖。

## 状态与字节账

`transmissions` 按 PN、方向、发送/接收时刻保留 wire、padding、STREAM offset 和业务范围；`sender_events` 保存真实送达反馈；`losses`/`timers` 区分判失和 PTO，PTO 本身不宣告丢失或减窗。恢复使用新 PN、旧 STREAM 范围，业务有效量不重复计数。BBR 对每个首次确认 PN 计 transport delivered，包含丢失后的迟 ACK；它不等于唯一业务交付。

`controller_events` 和 `final_states` 展示每个控制器可复核的状态；`persistent_events` 仅在真实 ACK 上消费新的丢失证据，迟 ACK 拆分旧 span 不能再触发一次。普通 BBR packet-conservation 忠实保留可能的 1 MDS 窗口；RFC9002 普通 2 MDS 是推荐值，未被静默夹窗。持续拥塞适配的最小窗口另为 2 MDS。CUBIC/参考 NewReno 的最小窗口仍遵循各自合同。

`numeric_errors`、`controller_numeric_errors`、`pacer_errors` 分开记录局部量化。默认显式控制器采用 1 ns 发送时刻上取整及 10^-12 B pacer 债务上取整；状态量化也显式记录。ready-time projection 可能反复查询，不能把每次投影误差相加当实际总等待，更不能声称全部理想实数轨迹误差上界。原无控制器基线保留其精确事件策略。

## 验证边界

`baseline-root-check.json` 记录十个旧场景完整数学 payload 相等（包括原书大例）；根代理的 pacer/network/persistent 检查记录独立手算；reviewer 的 adapter/network 检查分别核同 ACK 前后 flight、同恢复 epoch 多次 loss 身份、迟 ACK/PTO、HyStart 交接和 flow/MAX。正式大例独立审查另读取完整结果与生成 manifest，不能用上述局部检查代替。

这仍是有限单业务、声明立即 ACK 策略的研究网络。多流/媒体业务、真实协议互操作、完整 ECN 信号路径、实际 TCP 协议栈及广泛性能实验没有由本候选完成。应用接收状态和窗口反馈有真实传播，但控制器公式正确也不意味着模拟器覆盖了所有网络机制。
