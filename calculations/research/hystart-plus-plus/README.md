# HyStart++ 启动状态计算

本候选实现固定 RFC9406 的初始启动状态，供后续与 CUBIC、发送方反馈适配。它不修改冻结的 `../congestion-controllers/cubic.py`，也不接入公共模块。实现前范围与事件次序见 `CONTRACT.md`；手算见 `hand-oracles.json` 和独立审查方的 `independent-oracles.json`。

```sh
python calculations/research/hystart-plus-plus/calculate.py --output /tmp/hystart-all.json
python calculations/research/hystart-plus-plus/calculate.py --inputs calculations/research/hystart-plus-plus/example.json --output /tmp/hystart-one.json
```

默认运行 `scenarios()` 的全部13个固定场景。`calculate(inputs=None)` 返回单场景，`Startup(inputs).step(event)` 可增量推进，`state()` 导出当前状态。每次 calculate 校验官方 RFC9406 与官方勘误查询快照的长度/SHA256；当前固定查询结果为未找到匹配勘误。

窗口与序号单位 byte，时间与 RTT 单位秒。所有计算采用 Fraction，无近似立方根或小数窗口舍入。逻辑序号不回绕；参数使用有理数字符串也可。事件最大10000个，单个数值位数与字节序号有有限上限。

| 初始字段 | 含义 |
|---|---|
| smss | 最大数据segment大小，默认1000 B，不含TCP/IP头 |
| initial_cwnd | 初始窗口，默认10000 B |
| initial_snd_nxt | 已发送第一flight的排他端点，默认8000 |
| initial_acked_seq | 已累计确认的排他端点，默认0 |
| paced | 是否由外部真实pacer提供平滑发送；false限制单ACK标准增长至8×SMSS，true不设此上限 |
| initial_slow_start | 默认true；false直接交给后续标准慢启动，不能再次开启HyStart |
| constants | 可调min/max_rtt_thresh、min_rtt_divisor、n_rtt_sample、css_growth_divisor、css_rounds；默认9406推荐值 |

| 事件 | 字段与作用 |
|---|---|
| sent | at、snd_nxt；只更新发送方实际已见的最高发送序号，不能从ACK数据量猜测 |
| ack | at、ack_seq、newly_acked_bytes；可选rtt和唯一rtt_sample_id。新确认量与累计ACK共同满足已发字节约束；SACK范围细节由上游反馈适配器核验 |
| congestion | at、signal=loss或ecn；退出启动并设置ssthresh=cwnd。没有执行实际拥塞乘法减窗 |
| restart | at；仅初始HyStart已经退出后合法，交给标准慢启动，不在本模块重做Reno |
| observe | at；仅观察 |

ACK属于到达前的阶段，因此进入CSS的ACK仍按标准慢启动增窗，恢复标准慢启动的ACK仍只按CSS增窗一次。先统计该ACK，再判断阶段切换，最后结束其所确认的window_end轮次；边界触发CSS时，此partial round计入CSS的5轮上限。这是明确的callback次序，不宣称RFC提供了完整网络事件调度器。

CSS期间必须至少有8个有效RTT样本才检查抖动回退，严格小于baseline才回退。即便CSS轮样本不足，该实际轮次仍计入CSS时长上限。缺少RTT的ACK可以增窗但不加样本数；重复样本ID拒绝。累计确认完所有已发数据后，window_end暂为null，直到新的实际sent重新确定，重复ACK不会空转轮次。

默认完整例的窗口是第一轮结束18000 B、第二轮触发CSS时26000 B，完成首个partial round及之后4个CSS round后34000 B，ssthresh=34000 B并交付CA。paced/unpaced的单ACK确认20000 B对照，标准增长分别20000/8000 B，CSS增长分别5000/2000 B。

handoff 中的 `congestion_reduction_applied=false` 说明尚需外部CUBIC/NewReno处理真实loss/ECN减窗；不得将启动退出与恢复减窗重复执行。CA之后的ACK不能继续由本模块增长窗口。后续适配还需要明确TCP cumulative ACK到QUIC确认轮次的映射、RTT样本资格、恢复状态与真实pacer；本文件不提供完整TCP、QUIC或30MB网络性能结果。
