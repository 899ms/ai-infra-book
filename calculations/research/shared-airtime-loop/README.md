# 单共享空口与媒体反馈：研究候选

本目录在已验公共媒体 Network 上增加 client↔AP 的一个半双工非抢占资源，AP↔server 仍走原双向 WAN。Application、sender、ACK receiver、controller、pacer 和恢复算法直接复用公共模块。当前只完成小型候选与关闭无线的14个小例完整回归，尚未运行新增无线的完整30MB混合负载，也未接入公共CLI/章节。

`INTERFACE-CONTRACT.md` 先于实现明确拓扑与反馈。`airtime.py`由主代理维护独立精确交换账；`calculate.py`负责接线；`scenario_helpers.py`、`build-scenarios.py`及 `SCENARIOS-CONTRACT.md`由独立输入作者维护，预写WAN手算见 `network-hand-oracles.json`。`run-small.py`实际执行并固定 `result.json` 和源码hash manifest，不从期望文件生成模拟输出。

```sh
python calculations/research/shared-airtime-loop/run-small.py
python calculations/research/shared-airtime-loop/calculate.py --inputs your-input.json --output your-result.json
```

输入仍是 `{application,network}`。无线配置放 `network.wireless_access`，包含 `enabled:true`、`profile`、可选 `mode`（abstract/ofdm且与profile一致）、`max_attempts`、`retry_wait` 和 `failures`。profile采用 `shared-airtime-inputs/profiles.json` 中完整教学或OFDM参考对象。failure含 direction/up或down、pn、从1开始的attempt、outcome/data_lost或mac_ack_lost。未声明完整MAC失败等待的参考profile不能模拟失败：45µs RXSTART监视器不是完整ACK到达超时。每次无线计算核验来源目录14份原件的长度与SHA。

没有无线字段时直接调用原公共计算；显式 `enabled:false` 时仅去除无线选项再调用原公共计算，返回同一旧输入/旧完整结果，避免给默认模式加诊断字段。无线启用的结果保留完整原输入。

上下行都必须计入WAN串行与传播；上行先无线收到再进AP的WAN队列，下行先server发送WAN到AP才排无线。原20/100Mbps不是PHY速率。全局FIFO先比较候选ready时刻，同刻client先于AP；每端发送仍按原应用FIFO/priority和真实窗口/pacer条件选择。固定接入等待只预留方向，DATA真正开送再选当时可发送的包，期间取消或额度变化不会被未来预订绕过。

传输ACK在**源端首次实际发送**冻结：client ACK在无线DATA起点，server ACK在WAN起点。AP转发下行ACK时不能读取server后来收到的包刷新ranges。原“实际无线开送刷新ACK”的概括仅适用于client源ACK；拓扑扩展后不能免费跨端传递接收状态。快照、首次发送、AP就绪、无线收到和最终端到端收到均可沿记录核对。

无线DATA接收发生在MAC反馈之前：上行在AP首收到时就排WAN，不等客户端知道成功。MAC ACK丢失可使同一端到端包、同PN重复无线尝试；两端本跳去重均不重复上交IP/QUIC，仍发送该尝试的MAC ACK。网络不再次调用sender.sent、不重复扣cwnd/流控或交付业务。MAC失败只在声明等待结束时为本跳发送方所知；重试上限耗尽不通知远端、不释放端到端flight，后续PTO/loss/新PN恢复只能由已有真实反馈推进。这里用(direction,PN)作为声明本跳重复身份，不模拟完整MAC序号控制。

结果继承原完整业务与发送方记录，另有 `wireless_attempts`、`wireless_reservations`、`wireless_events` 与 `wireless_summary`。`transmissions`仍是一条端到端packet/PN一行；`wireless_attempts`每次MAC尝试一行，两者不能相加当唯一业务。上行 `send_start/end` 是首次无线DATA源发送，下行是源WAN发送；上行 `wan_start/end` 和两向 `wireless_received_at` 说明分段路径。attempt内分列reservation、DATA、实际收到、MAC反馈/释放以及精确service；`received`/`feedback_known`标明是否在观察期限内实际发生。

`wire_bytes`沿用原IP/UDP/QUIC包账；它不是MAC/PHY总字节，也不包含同PN无线副本。airtime组件另外给PSDU、MAC ACK、PHY符号/前导、接入间隔等，教学模式未知的物理字节或纯RF发射时间保持null。`reserved_service_seconds`是已开始DATA尝试的完整声明服务，`observed_reserved_seconds`按观察期限截断全部预约，包含预约后取消/到期前尚未开DATA的接入等待；不能把未来完成的整段当已观测空口。事件队列空、源队列空和业务成功仍分别输出，AP/WAN/重试等待另列。

有限范围：声明全局FIFO、单帧、无随机DCF/EDCA、隐藏节点、聚合、RTS/CTS、加密、速率适配、生产能量或TCP-TACK。OFDM参数来自固定ns-3官方实现及声明选择，不是完整IEEE符合性认证或真实设备测量。参考NewReno先隔离接线；后续完整混合四格与ACK/码率扫描须小例独立审查后执行。

截止字节语义修订：启用无线时，旧 `summary.serialized_wire_bytes_by_horizon` 明确为null，不能在PHY前导/符号填充期间按IP字节线性比例声称已经传输。新增 `wan_serialized_ip_bytes_by_horizon` 仅按实际WAN出口开始/结束逐包算IP序列化前缀。`check-prefix-output.json`实际验证44µs截止（34µs接入等待加10µs前导）：无线IP前缀未知、WAN零字节、观测预约44µs。此前 `development-result.json` 保留为修订前过程记录，不作最终物理字节证据。
