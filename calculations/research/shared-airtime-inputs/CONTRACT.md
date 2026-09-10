# C69 单共享空口输入合同

本包只固定来源、可编辑输入和实现前手算；没有空口模拟器、ns-3运行、完整媒体重算或TACK实现。下一阶段依据 `media-feedback-public-integration/NEXT-SCOPE.md`，保留十二章落点，不恢复旧第13章。

## 已固定的官方来源与事实边界

仓库定向检索 `references`、已有C69研究和实验目录，没有定位到可直接复用的TACK论文原件或完整802.11标准正文。模糊字符串stack及无关论文索引不作来源。另从作者Keith Winstein的Stanford主页下载[TACK原论文](https://cs.stanford.edu/~keithw/tack-sigcomm2020.pdf)，实际读摘要与引言：它不只是少发ACK，还涉及TCP反馈与恢复设计。本包只借其问题背景，不复现其算法或引用其性能数字作为模型输入。

无线字段固定自ns-3官方仓库[ns-3.44提交](https://gitlab.com/nsnam/ns-3-dev/-/tree/43dce6710b8df69685e3479c1d33a571dda714ea)。官方release API原件也已保存，提交为 `43dce6710b8df69685e3479c1d33a571dda714ea`，不是跟随master。还保存官方3.44 Wi-Fi设计文档快照及原LICENSE。所有14份原件的URL、revision、字节数、SHA和抓取时间见 `sources.lock.json`；逐文件重新读取校验。

这里区分**官方模拟器实现事实**与**IEEE标准原文核验**：源代码注释引用标准章节，但本次没有获取完整IEEE标准正文，不能写成逐条独立规范符合性证明。实际设备PHY、速率集、竞争、加密、重试上限、损失、电量和浏览器策略都未知，`profiles.json.deployment_observation` 保留null。

| 可核字段 | 固定源码位置 | 采用边界 |
|---|---|---|
| OFDM20MHz前导16µs、SIGNAL4µs | `ofdm-phy.cc:GetPreambleDuration/GetHeaderDuration` | 前导是时间，不是假造MAC字节；SERVICE另在DATA符号内 |
| 符号4µs、SERVICE16bit、tail6bit、向上取整符号 | `ofdm-phy.cc:GetPayloadDuration/GetNumberServiceBits` | 单MPDU/BCC参考公式，非任意HT/HE/EHT聚合 |
| 5GHz signal extension为0 | `ofdm-phy.cc:GetSignalExtension` | 不把2.4GHz额外6µs误套此profile |
| SIFS16µs、slot9µs | `wifi-phy.cc:Configure80211a` | 仅选定legacy参考；AIFSN2为声明政策，间隔34µs |
| 三地址non-QoS DATA头24B；ACK头10B | `wifi-mac-header.cc:GetSize` | 非四地址、无QoS control、无加密；不是所有Wi-Fi头长度 |
| FCS4B、LLC/SNAP8B | `wifi-mac-trailer.h`、`llc-snap-header.h`及序列化源码 | 普通MAC ACK合计14B，不含LLC/IP/UDP |
| 接收unicast DATA后SIFS再发NormalAck | `frame-exchange-manager.cc:ReceiveMpdu/SendNormalAck` | QUIC ACK也作为本跳DATA携带时，仍有独立MAC ACK |
| ACK速率选择依赖control answer mode | `wifi-remote-station-manager.cc:GetAckTxVector` | 不能将ACK速率无条件等同数据速率；本例显式basic set={6Mbps} |
| 接入和backoff按slot/IFS处理 | `channel-access-manager.cc:GetBackoffStartFor`等 | 本教学profile选择FIFO、零backoff，不声称实现随机DCF/EDCA |

重要超时边界：`frame-exchange-manager.cc` 在数据TXEND之后用SIFS+slot+ACK PHY header等待RXSTART；`RxStartIndication`收到正PSDU时长后重新安排超时。选定profile的45µs是**接收开始监视时限**，不能当完整MAC ACK到达时限：SIFS16µs+完整ACK44µs本来就是60µs。完整ACK超时字段保留null，未来实现须选择声明的完成超时模型，或完整实现接收开始/结束状态机，不能照抄45µs就将合法ACK判丢。

## 可编辑profile的两层分离

`source_backed_reference_selection`选择legacy OFDM20MHz/5GHz、DATA54Mbps、MAC ACK6Mbps、non-QoS三地址无加密、一次一个MPDU，无A-MSDU/A-MPDU/BlockACK/RTSCTS。这些是可核实现支持下的**实验选择**，不是实际终端配置。DIFS式前置间隔34µs、零backoff、全局FIFO仲裁也是声明抽象；不能称已实现ns-3或完整802.11竞争。

参考字节链为：已有QUIC packet + IPv4 20B + UDP8B + LLC8B + MAC24B + FCS4B。不要再添加Ethernet头，亦不要把既有28B外层重复加两次。1200B QUIC数据得到1264B PSDU，64B QUIC ACK得到128B PSDU；MAC ACK自身为14B PSDU。各PPDU分别包含前导/SIGNAL和符号填充。

独立参考算术：DATA PPDU208µs，MAC ACK PPDU44µs，QUIC ACK承载帧PPDU40µs；包括一次前置34µs、SIFS16µs与MAC ACK后，成功DATA完整交换302µs，承载QUIC ACK的完整交换134µs。数据接收发生在DATA PPDU末，MAC发送方知道成功发生在后续ACK末，不可合成一个时刻。

`abstract_teaching_profile`使用秒级整数/分数服务用于五个手算，与以上微秒PHY选择是互斥模式；不得把它的1秒再加源支持的PHY字段。其QUIC ACK完整交换0.5秒拆成0.25秒承载帧和0.25秒MAC确认，接收端在前半段末获得QUIC反馈，但空口仍不可被新释放cwnd抢占。

## 拓扑和后续事件接口

一个全局半双工非抢占无线资源连接client与AP；AP到server的WAN两方向出口另记。原20/100Mbps及各50ms保留为WAN基线，既不当PHY，也不在替代同一链路时重复串行。下一引擎须明确无线段是追加还是替代哪一段。

MAC ACK是本跳确认，不更新端到端cwnd/RTT/MAX，不生成QUIC ACK循环。MAC重试保持同QUIC PN和业务身份，接收去重；重试失败或耗尽的知识只能在实际等待后出现。端到端恢复另发新PN，PTO本身不是loss或减窗证据。

待发QUIC ACK必须在实际空口开送时冻结ranges与最大PN接收时间。媒体ready/计算/播放槽保持原DAG，不能事后给冻结旧trace加airtime就称业务重算。输出分列PPDU时间、MAC字节/确认、接入空等、MAC重试、端到端ACK与重传，不把间隔变成线上字节。接收、MAC成功已知、端到端反馈已知和应用可用分别输出。

## 五个实现前期望

`hand-oracles.json`给出共享非抢占、两层ACK静态账、忙时快照/超期、MAC ACK丢失与同PN重试、少ACK节省服务但尾部更晚五类。最后一例用3帧、窗口2、阈值1或4、相同4秒timer：总服务从5.25降到4.75秒，尾帧却从4.5推迟到6.5秒，错过5秒播放槽。这是明确教学反例，不是生产无线性能预测。

`check-inputs.py`只检查来源锁、profile算术和手算恒等式；不运行MAC状态机、竞争或媒体。仍未知/未覆盖：实际信道/频率和MCS选择、随机backoff及碰撞冻结、hidden/exposed terminals、capture、重试分布、聚合、节能、速率适配、802.11加密、完整TCP-TACK算法、真实蜂窝收费或电量。禁止把这些空缺用原WAN带宽或任意默认值补成事实。
