# 三控制器原书大结果独立审查：PASS

实际读取并审查三份正式完整结果，未以development摘要或小例替代：NewReno约74MB、CUBIC/HyStart约108MB、BBR约322MB。`check-large-independent.py` 用标准库分块解析，每次处理一条数组事件，仅保留紧凑PN/发送快照索引，不同时载入三个完整对象。每份结果SHA与生成manifest一致，审查前后六份生成源码SHA与manifest一致。

统一输入逐字段比较后，唯一差别是 `controller.name`。上传30MB、响应5MB、模型0.3s，上行20Mb/s、下行100Mb/s、两向各50ms传播、初始窗口12000B及padding政策全部相同。实际业务完成时间为：

| 控制器profile | 上传完整（s） | 模型完成（s） | 响应完整（s） |
|---|---:|---:|---:|
| NewReno | 13.087839089 | 13.387839089 | 14.52103724 |
| CUBIC + HyStart++适配 | 13.087839089 | 13.387839089 | 14.52103724 |
| BBR固定状态适配 | 13.344766867 | 13.644766867 | 14.974125992 |

三份均无loss/PTO/persistent事件。每份25,685个上传数据包、4,281个响应数据包及逐包反向ACK，共59,932次发送；上行31,935,032B、下行7,620,088B，共39,555,120B线上字节。数据头预算958,912B，短尾padding共288B；STREAM唯一有效量35,000,000B。独立逐数据帧核offset连续、不重叠且完整，不能靠接收区间并集掩盖重复贡献。

每一包逐方向核serializer不重叠、服务时长=wire×8/rate、到达=结束+50ms；ACK所指PN实际已经到达。上传最后实际到达即模型开始，模型严格0.3s，响应所有发送均不早于模型结束，最后响应实际到达即完整成片。最终pending、flight与timer清空，独立区间和完整业务条件另行通过。

每份29,900条sender量化记录逐项核new−old及1e-12局部界；pacer误差记录分别39,802、107,622、175,501条，逐项核向上舍入、对应网格和非负小于一个quantum。大例CUBIC未产生CA分支的窗口量化误差记录，不能把空记录当作大例检验了立方数值分支。BBR发送/ACK整数时钟另逐项核1+floor(seconds×1e6)，不把该1us映射称为1e-12精度。

BBR完整trace逐实际发送快照核先验delivered、首ACK身份累计、选择最新实际发送PN、max(send interval,ACK interval)和scaled bandwidth；实际/名义QUIC采样字节一致。每ACK还从真实发送和此前确认独立重建pre/post flight并核callback输入、raw RTT及未事后改写的app/flow-limited样本标志。其上行记录中实际观察到STARTUP、PROBE_BW、PROBE_RTT，下行观察到STARTUP、PROBE_RTT；这里按记录的状态报告，不凭源码存在某分支便说它已执行。

CUBIC/HyStart本例全程只观察到初始等待和slow_start，没有进入CSS或立方拥塞避免。因此它与NewReno得到同一时间，不能解释为立方CA提供了性能优势。三个数字只属于所声明网络、统一padding/pacer及适配政策，不能泛化为控制器普遍优劣或真实Linux TCP实验。

证据：三份 `large-independent-*.json`、`large-comparison-independent.json`、正式manifest及本检查脚本。此审查没有重新运行网络，没有修改公共/主纲/冻结控制器；pacer算法本身仍由根独立检查。丢失/lateACK等语义另有小例，主大例无损不能替代有损大负载、媒体/多流或完整C68验证。
