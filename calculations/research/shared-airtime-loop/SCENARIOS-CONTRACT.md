# 共享空口：独立小输入及网络兼容合同

本文件与 `scenarios.json`、`network-hand-oracles.json` 在读取候选运行输出前写定。只检查规范化应用schema，没有运行网络或用候选输出修期望。来源profile当前仍待独立审查，`scenarios-metadata.json`明确 `source_configuration_final=false`。

## 三种证据层级

1. `local-service-oracles.json` 原样保留上一输入包的五类期望及SHA：它们有纯空口服务、初始接收状态和静态包账，不全是可直接塞入完整网络的输入。
2. `scenarios.json` 是十个可供 `calculate({application,network})` 使用的小型规范化DAG。`scenario_helpers.py`只构造消息、依赖、额度和声明输入，不预测网络结果；`build-scenarios.py`可重新生成。
3. `network-hand-oracles.json` 是明确加上有限WAN后的新手算。没有将极高有限速率当零时间，也不强求其数值等于旧无WAN局部服务例。后续计算若不一致必须先审因果，不可从结果倒填期望。

## 输入接口

沿现有媒体 `{application,network}`。新增 `network.wireless_access={enabled,profile,max_attempts,retry_wait,failures}`，profile直接传原 `profiles.json.abstract_teaching_profile`。不另传未约定mode字段；原profile由字段区分参考/教学分支。failure按direction、QUIC PN、从1起的MAC attempt和data_lost/mac_ack_lost指定。普通小例max_attempts2、retry_wait0.5s。

所有正常网络小例保留每方向9824bps WAN、零WAN传播；1200B QUIC数据+28B外层的WAN服务恰为1s，64B QUIC ACK+28B外层为 **α=23/307s**。空口数据PPDU1s、其后MAC确认0.25s；QUIC ACK承载PPDU0.25s、其后MAC确认0.25s。二者源接收时刻与MAC发送方成功已知时刻分开。

每方向初始cwnd2400B（忙ACK例4800B）；可靠连接/内存额度明确给足，每流额度为声明最高end；不消费、不隐式发MAX。无控制器pacer配置，使用原reference sender以隔离空口时序。除PTO专例外显式先验RTT100s/variance50s，避免小整数空口时长意外引发恢复；该seed是教学假设，不是实测。PTO专例不种RTT样本，初始RTT4/3s、立即ACK策略max_ack_delay0，首PTO为4s。时间范围14s。

应用ready均为真实本端ready，不提前使用远端状态。消息只有1B有效payload但仍pad1200B，因此此处检验机制，不是30MB图片或媒体码率实验。尾部播放例3B可靠流，第三字节为一个0.25s音频块、固定6s槽；两策略只改ACK阈值/策略，DAG和WAN相同。

## 上下行路径与ACK冻结

上行client→空口→AP→WAN→server；下行server→WAN→AP→空口→client。AP不是QUIC端点。**上行客户端ACK在无线实际源发送时冻结；下行服务器ACK在WAN实际源发送时冻结**，AP后来发往空口不得读取服务器未来ranges或重新计算delay。已有下行WAN排队和空口排队不是同一个本端ACK生成延迟。

忙ACK两例专门选择上行客户端ACK，故可合法在真实空口开送时刷新。第一下行DATA在客户端2s收到；其0.25s定时器在2.25s到期，但第二下行服务占2.25–3.5s，第二DATA在3.25s收到。上行ACK3.5s冻结PN0..1，largest接收3.25s，raw=0.25s。把max_delay改为0.1s时原到期变2.1s，实际开送仍3.5s，raw仍0.25s并超期。冻结后转发不得追溯改写。

## 十场景与五类原问题映射

| 场景 | 独立预期重点 |
|---|---|
| bidirectional-shared / disabled | 共享时上行空口0–1.25s、下行WAN0–1s后空口1.25–2.5s；应用到达上行2s、下行2.25s。关闭时原双向WAN可同时0–1s，应用均1s。原纯资源1秒例另留local文件 |
| two-data-immediate / every2 | 两DATA各有MAC确认；端到端ACK各自也含MAC确认。总成功空口服务3.5s vs3s，非业务时刻 |
| busy-client-ACK-refresh / overrun | 合法客户端实际源发送快照、最大PN接收时间、0.25s编码31250，以及0.1s声明的超期 |
| same-PN-MAC-ACK-lost | 同PN0空口DATA0–1、2–3；失败1.5已知，成功3.25已知。第一次AP接收1s、只转发一次WAN，server2s唯一交付；MAC重试不调用第二次sender.sent |
| MAC-data-loss-exhaustion-then-PTO | 原PN0两次DATA都丢失，没有接收或端到端ACK提前解除flight；失败1.5/3.5已知，4s真实PTO后新PN1，server6s才收业务。不能把MAC失败直接当QUIC loss/PTO |
| tail-immediate / every4 | 计入WAN后完整尾部5s vs8.5+αs；空口服务5.25 vs4.75s。6s播放槽前者可用，后者缺0.25s音频。旧无WAN4.5/6.5s仍保留在local文件，不混为同一拓扑 |

尾例聚合首次server接收2s，4秒timer在6s到期；ACK到AP为6+α，client在6.25+α接收QUIC反馈，MAC确认至6.5+α才释放空口。第三DATA不能抢占它，从6.5+α发送，AP7.5+α收到，WAN后server8.5+α收到。少一次ACK的服务节省不抵消等待反馈造成的尾部延迟。

## 后续实际检查边界

先验证source/profile合同，再执行上述小例并逐PN、同PN MAC尝试、WAN单次转发、每向sender.sent、radio占用互斥、实际ACK到达和业务输出。纯ACK自身MAC确认不能产生端到端ACK循环。重试耗尽也不立即释放cwnd。失败/重试期间接收到真实端到端ACK时，应依据实际先后决定取消尚未开始的重试，而非预知结果。

本批没有完成随机DCF、碰撞/隐藏节点、PHY速率适配、聚合、TACK/TCP、真实WAN测量或完整媒体验收。无线disabled还需与公共旧完整输出比较；本文件的两个disabled手算只覆盖所列小输入，不替代19场景回归。不得据此移动业务截止时间或在完整媒体未运行时宣称质量收益。
