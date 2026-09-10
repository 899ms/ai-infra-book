# 接收端 ACK 聚合研究候选

本候选在冻结的已确认单路径网络上增加接收 ACK 状态，不实现握手或媒体引擎。实现前合同为 `CONTRACT.md`，预写五个数值／因果边界在 `hand-oracles.json`。`receiver.py` 负责纯接收状态；`calculate.py` 只增加网络接线，按 `dependencies.lock.json` 验证并复用旧 sender、controller、pacer。

```sh
python calculations/research/transport-ack-policy/calculate.py --output /tmp/ack-results.json
python calculations/research/transport-ack-policy/calculate.py --inputs /tmp/ack-input.json --output /tmp/ack-one.json
```

默认运行 `scenarios.json` 的七个聚合网络输入（五个基础场景，两个反向串行器忙碌诊断）。`calculate(inputs)` 接受单个输入，`legacy_scenarios()` 保留旧十场景输入供回归。旧缺省或 `ack_policy="immediate_each_packet"` 沿原路径保持完整数学输出；新字典模式才添加 `ack_events`、`ack_state` 和每个实际 ACK 包的 `ack_snapshot`。

字典示例：`{"mode":"count_or_timer","every":2,"max_delay":"0.01","delay_exponent":3,"retain_packets":256,"reorder_immediate":true,"header_tag_bytes":24}`。max_delay 单位秒但须能表示合法整数毫秒，delay_exponent 指数单位为微秒。它是明确的接收策略，未模拟 ACK_FREQUENCY 协商。ACK header/tag 与 packet 长度是声明布局，不冒称某固定 QUIC 库编码。

ACK 达到包数或期限时进入待发队列，实际开送才冻结 ranges 和编码 delay；反向忙碌期间到达的新包可覆盖进尚未开送的 ACK。纯 ACK 不触发 ACK，但其 PN 可以顺带被确认，所以新策略保留发送方纯 ACK 历史。范围采用声明有限保留，旧报告丢失且超出保留范围时仍需真实后续反馈／PTO，不能免费清除在途量。

`ack_snapshot` 保存最大 PN 首到时间、原始延迟、wire 编码整数、解码值、量化差和是否超过配置最大延迟。发送方独立遵循既有 RTT 样本资格与 ACK delay 上限，不把第一样本随意减掉 delay。ACK 内范围字段的 varint 容量在开送时核验；初版范围装不下即报告输入超出有限布局合同，没有隐式分包或静默丢弃未报告范围。

本目录正在候选验证，不能以首版小例或旧 sender 的通过记录宣称本策略最终验收。源码冻结、独立审查与完整默认回归完成后应保存相应证据。无线 MAC ACK、空口竞争、TCP 默认策略、共享媒体和完整协议编码均不由此候选完成。

当反向不可抢占包使实际ACK delay超过声明max_ack_delay，结果保留真实等待并标exceeds_max_delay。这是输入负载下未满足期限的诊断，不声称该次发送满足RFC及时反馈要求；不能夹短delay隐藏拥塞。queued-snapshot-refresh与queued-deadline-overrun分别展示开送前刷新和真实超限。

默认路径完整回归已实际完成：default-small-regression.json 为旧9小例+3controller router，default-large-regression.json 为旧book+3controller book；合计16。每项比较完整数学payload，仅排除两顶层来源元数据。新聚合接线与receiver的独立审查另存对应checker结果，不从默认回归推定新策略正确。

## 原书 30 MB／5 MB 聚合对照

`book-comparison-inputs.json` 从已验立即 ACK 三控制器输入复制，只增加 `ack_policy`：每2个新 ack-eliciting 包或10ms触发，指数3、ACK packet64B、有限保留256PN。三者继续统一1200B在途填充、20/100Mbps、各50ms传播和0.3秒模型。接收政策使发送方 max_ack_delay 更新为0.01秒，并保留纯ACK PN历史以允许顺带确认；这些派生设置在manifest中明列。

```sh
python calculations/research/transport-ack-policy/run-book-comparison.py --pilot
python calculations/research/transport-ack-policy/run-book-comparison.py --controller newreno
python calculations/research/transport-ack-policy/run-book-comparison.py --controller cubic_hystart
python calculations/research/transport-ack-policy/run-book-comparison.py --controller bbr
```

300KB/50KB探查先核运行开销和范围容量，随后三组真正30MB/5MB均完整执行。`book-aggregate-*-result.json` 保留完整轨迹，旁附manifest记录生成前后相同源码hash、全部官方原件核验、实际输入和结果SHA；pilot不替代大例。

| 控制器 | 立即 ACK 完整响应/s | 聚合 ACK 完整响应/s | 聚合 ACK 数 | 聚合 modeled wire/B |
| --- | ---: | ---: | ---: | ---: |
| NewReno | 14.521037240 | 14.564459796 | 14990 | 38177328 |
| CUBIC + HyStart++ | 14.521037240 | 14.564459796 | 14990 | 38177328 |
| BBR适配 | 14.974125992 | 14.996386157 | 14984 | 38176776 |

三者都交付35,000,000 B唯一业务，无物理丢包、数据恢复或PTO探测，ACK最大frame10B、单范围、没有delay超限。ACK数不能直接套ceil(data/2)：期限与控制器发送节奏共同决定触发。这里反向流量减少约1.38MB，但完整响应稍晚；不能由减少ACK推断任务必然更快。

`losses`数组仍保留12,591/12,589个下行纯ACK PN的发送方判失记录：它们不占flight，长期不在有限ACK保留范围中，后来被sender记为lost。所有这些PN在物理网络中都实际到达；没有应用数据丢失或重发。`book-comparison-summary.json` 将纯ACK身份状态与物理drop／应用恢复严格分列，不能拿losses数组长度当数据丢包率。该summary是完整结果的派生说明，独立大例审查另留证据。

RTT 审计输出升级：旧七小例与三大例的完整结果、manifest、比较summary及旧calculate源码保留在 `pre-rtt-output/`。上述数值最初来自该版本；当前仅在新ACK字典输出分支新增每方向一次直接读取sender实际 `rtt_samples`，已重新执行相同输入，新增值来自当次运行而非派生replay。新三大例与七小例manifest现已齐全，根目录的新结果为最终审计对象；旧16默认回归报告仍明确绑定其原源码hash。

最终当前hash58718e22默认兼容性已重新实际验证：12小＋4大共16场景全部通过，default-small-regression.json与default-large-regression.json已更新。旧hash报告另保存在pre-rtt-output。研究验收范围见ACCEPTANCE-CHECKLIST.md，公共接入未由本包宣称完成。
