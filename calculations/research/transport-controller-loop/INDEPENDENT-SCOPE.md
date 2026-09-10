# 控制器接入前独立审查边界

本文件先于网络适配实现验收。复用已有固定官方 RFC9000/9002 及 Verified Errata7539、RFC9438、RFC9406，并使用 Linux v6.6 commit `ffc253263a1375a65fa6c9f62a893e9767fbebfa` 的 tcp_bbr.c/tcp_rate.c/tcp.h/win_minmax 原件。依赖具体字节锁保留在相邻来源目录；本次不复制或修改公共来源。RFC9002 勘误决定旧 SRTT 用于方差更新；RFC9406 样本与 round 来源不能从任意ACKdelta推造。

## 同负载和单位

BBR 作者提出全部 in-flight/ack-eliciting PN（含 STREAM 尾包、MAX、探测）padding为1200B QUIC/UDP有效载荷，每PN为一个BBR packet。纯ACK仍独立64B且不计flight/delivery-rate packet。该政策须同时用于CUBIC、HyStart和参考NewReno对照；否则不同padding成本可被误归因于控制器。链路另计28B UDP/IPv4；业务STREAM仅按真实offset有效字节消耗流控/交付，padding不消耗MAX_DATA。

CUBIC段单位必须显式定义为1200B拥塞字节的参考单位，并保留有理数窗口增量；这不是声称TCP SMSS等于QUIC的STREAM payload。HyStart增长的N若采用QUIC确认拥塞字节，也必须作为适配政策写出；SND.NXT round界限应来自发送时累计的唯一传输单位/字节索引，不能直接用可能重传/多流的业务offset作为全连接TCP序号。

BBR的MSS=1200用于packet-rate到QUIC字节率换算，外层出口按1228B线上服务。所有控制器必须遵守相同实际非抢占串行资源，控制器pacing输出不能当作物理线上速率而省略头部。

## 反馈和恢复

packet PN只分配于实际发送开始；发送时保存delivery快照、first-send/last-delivery时间、是否app-limited等。ACK处理必须先确定新确认的传输PN及选择对应发送快照，再计算delivery sample。不能仅用相邻ACK间隔估带宽，不能把当下发送队列为空回填为旧包的app-limited样本标志。

QUIC新PN重发旧STREAM区间是新的传输包。原PN与重发PN先后首次收到ACK时，若均计transport-delivered，则BBR包交付计数可为2而业务区间只为1；这份定义与Linux TCP skb/字节重传去重并不等价。先前已判lost PN首次lateACK如何更新delivery统计、是否调用BBR、是否提供RTT必须单独定义。冻结feedback的lateACK不再RTT/CC政策不能未经说明便被叫作完整tcp_rate_gen。

重复ACK不能重复释放flight或重复delivered；loss只减少当次尚在flight的包，不作为delivery。PTO只授权实际probe，不能自己触发loss、CUBIC乘beta或BBR Loss回调。loss恢复epoch、BBR ca_state变化与其回调顺序要来自显式QUIC恢复适配，不能冒称正在执行TCP恢复。

应用受限与流控受限分列：已有业务等待MAX时不等于没有应用可发。样本标志来源于发送时的限制水位/快照；RTT样本来自明确有效的新确认包且扣除声明合法ACK delay。HyStart需要独立有效RTT样本，不得每ACK重复SRTT凑8样本。

## pacing调度待合同定案

必须明确rate更新时如何处理已预约下一发送时刻、是否积累credit以及idle重启。无论采取何种参考政策，已开始的包不被新rate或反馈抢占；过期旧唤醒不能再额外送包，纯ACK/控制包是否受pacer约束应一致声明。当前仅固定这些不变量，未在政策确定前编造某个rate变化后的唯一下一发送时刻。

这是一组固定控制器接入QUIC参考网络的适配。即使纯BBR与固定C源码逐回调一致，也不能把新闭环称Linux TCP执行；真实TCP ACK/SACK、skb选择、GSO及恢复路径仍未实现。原C68多流/媒体/取消及公平对照仍需明确保留，不能由单个30MB成功路径关闭。

作者已确认 lateACK 政策：首次看到的每个 PN ACK（含已lost）均计一次 transport delivered；两副本PN计2，重复同PN ACK不再计，不重复释放flight/产生RTT。这是明确的QUIC适配语义，并非TCP skb重复字节去重的等价声明。

HyStart累计marker风险的限定：若首次loss通知立即handoff，可以采用累计PN前缀并在loss时结束HyStart；无需为了不再运行的round强行实现副本补洞。尚未判loss的乱序期，largest ACKed PN与累计前缀仍须明确区分。

## Persistent congestion 证据独立执行

`check-persistent-independent.py` 实际13例通过（函数hash见 `persistent-independent.json`）。RTT0.1s、variance0.02s、maxACKdelay0.025s给出阈值0.615s，恰等不建立、0.616s建立。端点必须为lost且ack-eliciting且发送前已有RTT；任何已ACK包（含lateACK和非eliciting）打断其间证据，尚未ACK的中间包不是ACK屏障。该函数仅在ACK触发建立，不将PTO/时间loss检测当作自身的建立事件。

已实际构造同一旧lossepisode的lateACK把证据key从0:4变为2:4；新key不表示新丢失，不能据此再减窗。集成需未消费的loss声明和episode状态。函数要求完整连续PN历史属于本参考有限合同，真实QUIC可跳PN；纯ACK不占flight/rate但仍须在证据ledger保留身份，不能因为省略纯ACK形成假历史。纯谓词通过不代表控制器动作已正确实现。
