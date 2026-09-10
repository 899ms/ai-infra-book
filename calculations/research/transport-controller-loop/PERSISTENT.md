# 持续拥塞证据：独立组件与接入边界

`persistent_congestion.py`依据固定RFC9002§7.6，从发送方已知的完整包历史给出证据；它不自行发现网络丢包，不改变控制器窗口。每次调用校验已封存RFC原件SHA。

持续时间为`3 × (smoothed_rtt + max(4*rttvar, granularity) + max_ack_delay)`，不乘PTO退避次数。两个端点须为已声明丢失的ack-eliciting包，发送时已有RTT样本；端点间任何ACKed包均打断区间，包括迟到ACK与非ack-eliciting包。间隔必须严格大于门槛。PTO或loss timer可留下待审证据，但只有ACK处理阶段返回`established=True`和最低窗口`2×max_datagram_size`的要求。

本参考限定已确认单路径、单Application PN空间；输入PN在保留区间内连续，不能漏掉纯ACK的身份来隐藏屏障。真实QUIC允许跳号，支持该行为须另给完整历史保证，不能直接删掉这里的校验。`rtt_known_at_send`由实际发送时的本地状态记录，避免凭同刻时间戳猜测首个RTT与发送的先后。RFC示例的1–8秒损失区间以发送前已有RTT估计为条件，不把1.2秒的ACK擅自解释成首个样本。

本轮实际运行17项主审检查及13项独立检查。独立例使用0.615秒门槛，恰等不建立、0.616秒建立。预写的RFC示例核7秒区间超过6秒门槛，未把PTO到期当作丢包证据。

## 控制器接入必须继续验证

`evidence_key`描述区间，不是完整的去重机制。独立检查证明，同一批旧丢包在收到迟到ACK后，key可能从`0:4`变成`2:4`；这不代表发生了新的丢失。调用方须维护未处理的loss声明及持续拥塞episode，使最低窗口动作只由相应新证据触发。新的短损失区间也不能借另一段已经处理的旧长区间再次触发动作。

ACK处理要按实际反馈层顺序更新确认与丢失状态，再审证据；loss timer阶段的证据应留待ACK阶段，而不是丢弃或立即减窗。CUBIC、HyStart退出和BBR适配对持续拥塞如何响应需要分别核验，不能在这里先减一次、控制器回调再减一次。该组件的通过不关闭原sender拒绝的persistent分支，只有集成的动作与恢复周期也验证后才可移除该拒绝。

这里是O(N)完整历史审查参考，不应在每个无新loss的ACK上反复扫描大文件全部历史。后续增量索引须与这个纯函数交叉核验，不能为性能省掉ACK屏障或历史身份。

复现：

```bash
python3 calculations/research/transport-controller-loop/check-persistent.py
python3 calculations/research/transport-controller-loop/check-persistent-independent.py
```
