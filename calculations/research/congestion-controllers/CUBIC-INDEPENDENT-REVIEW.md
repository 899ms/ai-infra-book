# CUBIC 独立合同与手算审核

有限纯状态候选的独立手算审查PASS。实际运行 `check-cubic-independent.py`，10组通过（9组预先数学/状态期望及14个非法输入组成的拒绝组），代码首尾SHA均为 `91be0851fb7a2e947e42578e8703bd098df98ba7432672440a2f81e677282836`。结果见cubic-independent-check.json；没有修改作者实现或冻结的transport-feedback。

期望先写于independent-oracles.json，随后映射calculate接口；未调用候选curve/root辅助函数生成期望。包括96.8/100/100.4曲线点、真正单ACK窗口117173/1210、Reno-friendly窗口3982577/41140、8segments单ACK的cubic增量仍0.5、alpha阈值、prior80与flight50的区别、100秒受限时间排除、所选Reno启动及TCP timeout。未知字段/事件、错误状态/参数、超出可观察区间的idle时长均有拒绝检查。

来源为本目录固定RFC9438/RFC5681；本轮实际读取官方9438勘误列表，仅有7806 Rejected，不将其中cwnd_prior=flight_size提案当规范。SOURCE-SCOPE记录完整来源合同与必要后续依赖。

本审核不声称验证全部可达状态或数值分支。一般立方根/量化及长期累计误差、所有恢复/重复事件边界应由作者和根的其余检查补足；本独立脚本没有第二套完整CUBIC状态机。作者16场景覆盖范围也不能用本10组数字替代。

明确选择的Reno启动不是通常推荐HyStart++的完整实现；新ACK数量、恢复退出、idle和RTO由外部提供，没有自行检测网络反馈。TCP timeout不等于QUIC PTO。该纯控制器尚未与stage1、双向网络/pacer、30MB请求或媒体业务闭环连接，C68/C69与完整图12-4缺口保持。
