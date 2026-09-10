# BBR接同一QUIC参考反馈：发送侧输入映射合同

研究适配草案，2026-09-09。只使用已独立检查的 `../congestion-controllers/bbr_state.py`，不改冻结BBR或旧网络。本阶段不是Linux TCP复现：QUIC Application PN、MAX额度和RFC9002恢复由共同网络/反馈层负责，BBR控制器接收明确的发送侧移植回调。

## 共同主对照的包单位

已与网络作者确认：新controller-loop主对照 `pad_in_flight=True`，NewReno/CUBIC/BBR三者所有in-flight包都填充到MDS1200B **QUIC UDP payload**。满STREAM有效数据1168B+声明预算32B；尾STREAM、DATAGRAM、MAX_DATA/MAX_STREAM_DATA、PTO probe均填至1200B。IPv4/UDP28B另计物理wire，pureACK保持声明64B UDPpayload、92B wire且不占flight。旧网络默认非padding行为不改。

因此每个in-flight ack-eliciting PN对应BBR一个packet，MSS取1200B；cwnd_packets×1200输出cwnd_quic_bytes，pacing字节率对应QUIC UDPpayload。网络实际发送间隔=sent_bytes/pacing_rate；方向串行器同时按(sent_bytes+28)/link_rate计真实wire。两个门槛都要满足，不能漏掉physical serializer或把28B再加入BBR delivered。窗口和MAX_DATA仍是不同预算，padding不消耗STREAM应用额度。

非padding模式只可单列诊断：每PN=1及名义MSS1200会使短尾/MAX采样与实际字节不同，必须同时输出actualUDPbytes/interval与nominal_packets×1200/interval，不能作为同条件主性能结论。BBR主入口默认拒绝未填满的in-flight包；若开放诊断必须显式旗标。

## Hook最低字段和位置

| Hook | 发送端可见输入 | 更新 |
| --- | --- | --- |
| on_sent(packet, now, flight_before, limited_flags) | 实际开始方向序列化时刻；PN、sent_bytes、in_flight、ack_eliciting、frames、probe；发包前sender已知flight；当前ready/app/flow/cwnd/pacer原因 | 给该PN保存delivery快照；推进本方向pacing下一eligible时刻 |
| on_ack(newly_seen, newly_lost, rtt_sample, now, flight_after, rttstate) | 当前ACK ranges首次确认的全部PN，包括先前lost的lateACK；was_lost、sent_time、frames、实际释放flight；同反馈新判失；发送方RTT估计 | 每PN首次确认计transport delivered一次，选采样快照，生成BBR Ack，再输出窗口/pacing |
| on_loss(records, now, flight_after) | 同一发送方包/时间阈值新宣布丢失PN；已lost不重复 | 记录总loss和待反馈loss，进入明确的移植恢复epoch；不指定神奇重传时间 |
| on_pto | 发送方PTO probe额度 | 不把PTO视为TCP CA_Loss，不清空flight、不直接缩窗；后续probe实际发送才on_sent |

ACK事件中的newly_seen必须包含lost PN的首次lateACK。冻结反馈旧策略对lateACK不再次释放flight/更新RTT可以保留，但不能因此完全丢掉BBR transport-delivered通知。重复ACK范围不产生任何新delivered，也不重取样。

packet.sent_time表示actual serialization start，不能是业务ready或预约尚未开始时间。两方向BBR/计数/采样独立，但ACK和MAX等仍占共享物理反向链路，不创建独立“免费控制链路”。

## 发送delivery快照与采样

每个被BBR计数的PN在发送时保存：`prior_delivered`（u32）、`prior_delivered_udp_bytes`（独立精确整数）、`delivered_mstamp_us`、`first_tx_mstamp_us`、`sent_us`、`is_app_limited`、`flow_limited`。时间映射声明为 `1 + floor(absolute_seconds×1e6)`，加1用于避免Linux0时间戳“缺快照”哨兵；原Fraction秒也保存。亚微秒的不同时间可能映射同一μs，零采样间隔必须无效，不用epsilon造速率。

ACK先找未确认过的可计数PN并更新total_delivered及实际UDPbytes；选择其中**实际发送时间最新**的PN，时间相同用PN顺序打破平局。这是把TCP“最新发送skb、序号辅助”映射到QUIC PN，不是按接收方到达时间选。由该发送快照计算：

- send_interval = tcp_stamp_us_delta(selected.sent_us, selected.first_tx_mstamp_us)
- ack_interval = tcp_stamp_us_delta(ack.now_us, selected.delivered_mstamp_us)
- delivered = u32(total_delivered − selected.prior_delivered)
- interval = max(send_interval, ack_interval)，不是相邻ACK间隔
- BW_scaled = floor(delivered×2²⁴/interval_us)，样本低于发送方已知minRTT或缺快照时无效

ACK处理后first_tx_mstamp推进到所选最近发送时刻；delivered_mstamp仅在新确认可计数PN时推进。app_limited取所选PN发送时的标记，绝不拿ACK到达时应用队列已空替代。仅flow-limited但仍有应用数据的情况单独标记，不等同app-limited。cwnd/pacer/serializer受限也不能假称应用没有需求。

packet-round必须消费这套prior_delivered与post-total，BBR内部实际执行10round滤波、mode和gain；适配层不传外部已算maxBW或直接指定STARTUP退出。

### Lost tombstone与空管线的重置边界

独立审查复现旧逻辑错误：原lost PN永不ACK会使重传成功、发送端active已空后仍继承旧epoch，空闲后的新样本被错误摊入整段idle。当前适配以发送方active传输PN（既未ACK也未判lost）为空作为新实际发送的epoch重置条件；两个时间戳都重置为该次send时刻。lost记录仍保留给lateACK身份，但不占采样epoch的active集合。

这是明确的QUIC每传输PN适配，不能称与TCP skb的packets_out完全相同。TCP重传ACK可退休同逻辑数据的旧skb；本适配重传使用新PN，因此不能机械地让旧PN墓碑永久阻止reset。发送方判lost是可见恢复状态，不等于物理接收方已证明该包消失；迟到原PN仍可首次计入transport delivery一次并使用原发送快照。

手算：原PN0在0s发送后判失，PN1在0.08s重发、0.1s确认。PN1发送时active已空，样本区间0.02s，BW整数838。若PN0永不ACK，之后10s新发PN2、10.1s确认，其发送快照两个stamp均10000001μs，样本区间100000μs、BW整数167，不能包含9.9s idle。原PN0若0.12s迟到ACK仍按它自己的快照产生279定点样本，且不重复释放flight。

## 重传、lateACK、控制包与业务计数

新PN携带旧STREAM offset是另一次传输packet；若两PN最终均获首次ACK，BBR delivered计2，而业务唯一数据计1份，源TCP去重不等价。MAX包填充后每个首次ACK也计1，pureACK不计；这些包含控制流的transport交付率不是应用goodput。两种字节量必须同时输出。

loss已释放flight的原PN后来ACK，不再释放flight；BBR可以计一次新transport delivery，但不能由此替共同RFC9002层重采不合格RTT。BBR的loss计数按新宣布lost PN数；重复loss通知不再计。

## 恢复、RTT与pacing待代码严格执行的规则

同ACK先处理newly_lost，再产生一个合成BBR Ack，避免同一次loss在on_loss和on_ack重复扣。时间阈值独立loss先save_cwnd并保存pending_losses；没有新ACK时不伪造acked_sacked>0。PTO只发probe，不能调用TCP CA_Loss。移植的Recovery退出应以发送方实际确认了恢复epoch之后发送的包为准，需和网络作者共同固定：不能把一串同epoch丢包重复当新恢复。

传入BBR rtt_us使用发送方真正可取样的原始RTT（不从接收端免费推算）；srtt_us_x8来自同QUIC层已修正的smoothed RTT，保留其ACK-delay处理差异。无合法RTT给−1；lateACK不另造RTT。采样rate使用原始时间间隔，不扣对端声明ACK delay。pacing以BBR实际输出为准；下次eligible依据实际发送时刻+QUIC包字节/当前pacing_rate，保留精确Fraction，不将计算耗时/网络传播重复计为pacing。

代码实现与手算验收前不宣称该适配已闭环。当前文件是已与网络作者协调的输入合同，原模型、固定来源和公共CLI均保持不变。

## 首版接口落地说明

`bbr_adapter.py`按共同facade提供 `BbrAdapter(mds,initial_cwnd,initial_rtt,config)`；`on_sent(record,context)`、`on_ack(records,context)`、`on_loss(records,context)`、`on_pto(context)`、`on_limited(context)`及`snapshot()`。context的now为Fraction秒，flight_before/after为真实QUIC bytes，rtt_sample字典的raw字段仅在原反馈允许RTT样本时提供，smoothed_rtt单列。内部保存精确发送快照，不接外部maxBW。

默认initial_rtt只是QUIC配置估计，BBR不把它当作已测minRTT：初始化min_rtt_us=0xffffffff、srtt_us_x8=0，沿固定BBR nominal1ms的初始pacing规则。只有显式config.bbr_rtt_seed_known=True才将initial_rtt作为已有观测seed。之后从发送方ACK计算出的raw/SRTT更新。该差异会影响startup pacing，场景必须保留旗标。

共同网络最终采用piecewise-debt pacer：ACK改rate前先按旧rate偿还过去债务，剩余债务按新rate重新决定未来eligible。闭环必须设置config.external_pacer=True，BBR适配关闭自有发送gate，返回有效next_eligible=None，仅保留内部旧deadline诊断字段。网络在on_ack context传pacer_next_eligible，表示本次改rate之前、已按旧rate结算到now的下一eligible；适配用它构造真实sender EDT，不使用陈旧内部deadline。实际gate由共同网络唯一执行。

局部独立hook自测的external_pacer=False保留按原发送rate收取固定间隔的简单策略；它不是闭环主pacer，也不能用于三控制器性能对照。方向physical serializer在两种模式中都由外部网络单独执行。

sender on_limited维护app-limited marker，后续PN发送快照继承标记直到新交付跨过marker；flow-limited不单独触发app标记。恢复cutoff为进入loss epoch时已实际发出的最大PN；只有该cutoff之后发送的包首次确认才退出该移植Recovery，重复loss不创建同epoch新cutoff。时间loss保留pending_losses，下一有效ACK调用核心；没有ACK不虚构delivery。

`check-bbr-adapter.py`目前只验证局部发送hook：原PN失、重传PN新确认、原PNlateACK、重复ACK、MAX与pureACK计数、send-time limited标记、PTO不直接减窗、短flight包及错误flight输入拒绝。`bbr-adapter-check.json`保存逐事件数据。这不是网络闭环验收；网络作者仍需接相同facade，独立审查仍需核hook时序与flags。


### Persistent congestion与接线审查

新增on_persistent(context)：由共同RFC9002发送方证据组件在真实ACK确认persistent后调用，要求稳定evidence_key，立即令cwnd=2*MDS；不调用TCP_CA_Loss、不改BBR mode，之后实际ACK可按BBR重新增窗。相同key重复通知不重置已恢复窗口。key检查只是额外防护，不能替代共同sender对未消费新loss/episode的完整去重（lateACK分裂span也不能当新事件）。

接线检查发现on_ack的flight_before必须是本ACK处理之前的真实sender flight，而非context默认的处理后flight；BBR prior_inflight用于phase门槛，不能错误传零。每个新判lost PN都须通知适配（同Recovery epoch也通知），以便删除active并累加loss；是否新epoch减窗由各控制器自己按合同决定。EDT已确认从共同pacer在旧rate下结算到now后的nexteligibility传入，随后才更新新rate。网络作者负责这些sender接线修正，适配保留flight_after一致性检查。

### Active flight implementation checkpoint

The adapter maintains an insertion-ordered active-PN dictionary and actual UDP-byte counter. Actual counted sends insert once; the first ACK or first loss removes once. Late ACKs and duplicate loss notifications cannot subtract twice. Historical records remain available for delivery snapshots and late-ACK identity, but no longer participate in the per-event flight scan. Empty-epoch detection, packet counts and supplied-byte checks use the active index; the highest sent PN is maintained separately for recovery cutoff. This changes bookkeeping cost, not callback math or event order.

`check-bbr-active-index.py` compares membership, insertion order and bytes against a historical scan after 2,000 callbacks (800 PNs), including nonmonotonic unique PN order, pure ACKs, repeated loss, late ACKs and duplicate ACKs. Its optional `--baseline` mode executes a supplied pre-edit adapter without changing its code; the recorded run compared every returned event and snapshot against SHA256 `c4101a79a516d66f6ea002593b1f3e67e2e84d8dd5fe6372ef97d39a7049dc56`. The pre-edit file is sealed at `baselines/bbr_adapter_c410_before_active_index.py` solely for replay, and is never imported by the network or the current adapter. The checker uses this baseline by default and records both checker and baseline SHA256.
