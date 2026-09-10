# C68 发送方反馈阶段验收

验收对象为 `calculate.py` SHA256 `1f3890671c60d9841d3dd89e289483940872c2823d7ba767b3a6b845dcbea567`，限定已确认单路径、Application PN 空间的发送方观察记录。此次没有改公共计算模块、正文或公共图，也没有重跑全项目测试。

## 已验证

- 四份固定官方原件逐调用校验：RFC9000、RFC9002、RFC9221、Verified Errata7539。RTT 方差按旧 SRTT 更新；180ms 原始样本扣20ms后，方差52.5ms、平滑RTT107.5ms。
- 独立审查27组通过，含14固定场景；12非法输入及超出 persistent congestion 范围的拒绝已验证。详见 `REVIEW.md`、`check-independent.json`。
- 主审在候选运行前记录的 `root-hand-oracles.json` 已落实到 `check-root-oracles.py`，33项检查通过。包括独立包/时间阈值、时间0恢复期、PTO与loss区别、绝对流控和offset空洞。
- 实际运行默认CLI一次，全部14场景与 `result.json` 完整相等；再运行14次可编辑输入CLI，完整输出逐场景匹配。没有仅比较摘要或仅调用Python函数冒充CLI。
- 同刻ACK1在113.5ms到达时，不仅取消PN1的loss，还产生112.5ms原始RTT；PN2期限因此从114.5ms推迟到128.5625ms。这是新增样本的影响，不是把旧手算固定期限套到修改后的轨迹。

复现：

```bash
python3 calculations/research/transport-feedback/check-independent.py
python3 calculations/research/transport-feedback/check-root-oracles.py
python3 calculations/research/transport-feedback/calculate.py --output /tmp/transport-feedback.json
```

## 保留的完整工作

这不是网络／接收方／自动发送闭环。`sent`、ACK与限额抵达时间来自声明输入；PTO只产生探测许可，实际发送必须有输入事件。ACK确认区间不等于应用交付、播放或完整业务完成。persistent congestion未实现而明确拒绝，不能据此称完整NewReno。

接下来先完成指定CUBIC和固定Linux BBR的纯状态及采样审查，再连接实际网络队列、接收端、恢复发送、双向控制字节与30MB／5MB业务。各控制器的版本、单位和回调映射需要分别验收；不能把QUIC恢复直接称Linux TCP行为。控制器原件与整数手算见 `../congestion-controller-inputs/README.md`，其BBR 10/12整数阈值说明修正了上一范围报告中的歧义。

本阶段通过不关闭C68，也不替代 `../shared-media-integration/acceptance.json` 的公共基线。统一公共CLI和图12-4的下一次扩展仍须在闭环接入时完成。
