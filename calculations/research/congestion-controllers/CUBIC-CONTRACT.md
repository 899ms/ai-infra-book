# RFC9438 CUBIC纯状态候选：实现前合同

2026-09-09，先于本目录CUBIC代码编写。已读固定RFC9438§4.1–4.10/5.8、`../shared-media-integration/next-congestion-scope.md`及`../congestion-controller-inputs/controller-oracles.json`。此交付是控制器状态计算，不是仅采样W_cubic曲线，也不假称与实际发送方恢复/媒体业务闭环已经连接。

## 状态、接口与ACK推进

窗口单位segment，时间秒，C默认2/5、beta默认7/10、初始Reno-friendly alpha=3(1-beta)/(1+beta)。状态保存cwnd、ssthresh、cwnd_prior、W_max、cwnd_epoch、W_est、K区间、epoch有效时间、alpha、启动/恢复阶段及应用受限状态。

计划API `calculate(inputs)`，输入初始状态和显式时间序列事件：`ack`（segments_acked、smoothed_rtt）、`congestion`（唯一event_id、flight_size）、`recovery_exit`、`limited_start/end`、`idle_restart`、`timeout`及不更新窗口的`observe`。不生成网络PN或ACK；ACK新字节数及恢复事件由调用方提供，经适配层接入时必须来自已验收反馈。重复ACK用segments_acked=0表达，重复拥塞event_id不再次减窗。

每个新ACK先按Figure4推进W_est（只有此式乘segments_acked），达到cwnd_prior后将alpha切1。若W_est大于W_cubic(t)，按RFC的SHOULD选择Reno-friendly W_est；否则计算W_cubic(t+RTT)，夹在[cwnd,1.5cwnd]，按每新ACK `(target-cwnd)/cwnd`增窗，不额外乘segments_acked。相同时属于非Reno分支。observe只报告曲线，不把曲线值赋给cwnd。

## 拥塞、epoch及应用受限

新拥塞恢复事件先应用可选fast convergence，再以flight_size×beta减窗，loss窗口及ssthresh最少2segment。fast convergence可显式关闭；同一恢复期重复loss不再次减窗，退出必须显式事件，未实现PRR/SACK或协议恢复检测。ECE继续减到1及更低速率策略不在首版，明确拒绝ECE事件，不把普通loss代替它。

新epoch按当前窗口设置cwnd_epoch/W_est/alpha和K。有效elapsed只累加非受限的拥塞避免时间；应用或接收窗口受限用明确limited_start/end区间，不由两个ACK间隔猜测。受限ACK不增窗，不让idle积累立方时间。idle_restart另接收已观察的idle持续时长及RTO，在满足重启条件时采用明确Reno重启窗口政策。

## 启动选择

本候选明确支持一种可审政策：RFC5681 Reno慢启动，作为固定算术/状态对照；不能推荐它替代RFC9438§4.10通常SHOULD使用的HyStart++。每个新ACK增加min(segments_acked,1) segment，启动阶段窗口不大于ssthresh时继续慢启动，超过阈值进入拥塞避免。首个无W_max或timeout后的CA使用K=0、W_max=cwnd_epoch。也支持明确从已有CA状态开始的seed，用于既有独立96.8/100/2秒oracle，不能把该seed说成beta0.7损失后的状态。

timeout为显式TCP式控制器回调：按RFC9438+5681将cwnd降至1，ssthresh按beta×flight且最少2；后续慢启动到新CA时K=0。不从QUIC PTO构造这个事件。未实现HyStart++的RTT轮次与退出、完整spurious undo、TCP恢复、ECE、ECN反馈和拥塞多算法适配，这些缺口保留。

## 数值合同

尽量使用Fraction保持有限有理数案例完全精确。一般K包含立方根：用整数有理数算术构造宽度不超过10^-30秒的区间；完全立方数则输出精确K。曲线给基于该K区间的上下界，选择区间中点作为声明实现值，不能称一般立方根为精确Fraction。

为防连续ACK有理数分母指数增长，若状态分子/分母超过声明位数预算，量化到10^-30 segment并记录原值、量化值及精确局部误差；这不是全轨迹相对理想实数控制器误差界。分支若落在K数值区间的不确定边界须报告或拒绝，不隐瞒不确定性。固定简单oracle必须无需量化即可精确匹配。

验收至少包括三曲线点、100.004单ACK、target夹限、Reno-friendly及alpha切换、concave/convex、fractional/delayed ACK、fast convergence、减窗与重复恢复事件、idle时钟排除、慢启动与timeout、新epoch、未知输入/错误状态拒绝；不以这些通过推定闭环或HyStart++完成。
