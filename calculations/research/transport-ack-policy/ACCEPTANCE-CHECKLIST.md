# 有限 ACK 聚合研究验收清单

本清单只针对 `transport-ack-policy` 研究包，不表示公共接入或整项 C68 完成。受审计算源码为 `58718e22f3e29cba582f7ce2fdaf5f701b9bbb45acf8e71cd22a0253c64e6ae2`，receiver 为 `a8a44b09c95d76501821a20a4737fdc352d564de706f98082b2c5f7f55949378`。

- [x] 实现前合同及五个手算边界已固定；两个忙队列例在核心实现后、对应场景执行前追加，来源时序没有混写。
- [x] 三份官方原件按长度/SHA校验；依赖 sender/controller/pacer 保持冻结，明确声明 count/timer、retention、header/tag 与编码策略，不称浏览器默认。
- [x] Receiver 独立19项通过：计数／期限、最大PN首次到达、乱序、重复、纯ACK、范围容量、编码余数和非法输入；仅ACK报告范围有界，总接收history线性增长。
- [x] 当前hash独立8个小网络通过：七固定＋一个独立忙响应，核实际arrival→开送快照→反向serializer→sender反馈；延期与同刻刷新保留实际时间，不伪造及时ACK。
- [x] root当前hash RTT专项30项通过，涵盖首次／先验样本、实际RTT导出、排队延迟上限、最大PN为纯ACK等边界，见 `rtt-root-check.json`。
- [x] 三控制器真正30MB/5MB聚合大例生成完整轨迹与manifest；300KB pilot只用于前置容量/成本探查，没有代替原书大例。
- [x] 三大例独立完整审查通过：逐PN/业务offset/wire/实际ACK范围与编码/业务依赖、44,964个实际RTT样本、局部量化、BBR快照与flight均核验，见 `LARGE-INDEPENDENT-REVIEW.md` 与三个 `large-independent-*.json`。
- [x] 旧纯ACK PN的loss记录与物理丢包/应用恢复分别统计；三大例无真实drop/data recovery/probe，不把loss数组长度当数据丢包率。
- [x] 新RTT导出每方向只调用一次sender.result；七小＋三大完整数学输出除新增rtt_samples外与归档版本一致，见 `rtt-output-parity.json`。
- [x] 当前hash默认16场景完整回归全部通过：旧9小＋3controller router，以及旧book＋3controller book均实际重算。状态与完整源码hash见 `default-small-regression.json`、`default-large-regression.json` 的hash和checks为准。
- [x] CLI支持可编辑输入和完整JSON；七固定输入及三原书聚合输入分别保存，生成manifest记录源码/来源/完整结果hash。
- [x] `pre-rtt-output/` 保留旧源码、轨迹、manifest、摘要及旧hash默认回归报告；旧数据没有删除或冒称新hash生成。

## 公共接入前的边界

本包只实现已确认单路径1RTT的有限ACK策略；ACK_FREQUENCY协商、完整编码分包和任意碎片范围截断仍未实现。固定ACK预算装不下时明确拒绝，忙链路可能导致max_delay超限并显式报告。没有公共receiver/static import迁移、公共场景注册或公共全量reproduce验收。

下一步由主代理接公共共享组件及现有CLI；迁移需要完整数学一致性、旧默认场景兼容性与来源锁验收。共享媒体仍应按 `transport-controller-loop/NEXT-SCOPE.md` 单独接入真实反馈，不能用本包关闭媒体、匹配TCP/H3实验、无线MAC ACK或完整C68/C69。
