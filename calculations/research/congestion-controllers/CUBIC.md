# CUBIC 控制器事件参考计算

`cubic.py` 实现 RFC9438 的窗口状态推进：ACK、Reno-friendly 估计、立方 target 限幅、loss/fast convergence、恢复期、受限时间排除，以及明确选择的 Reno 慢启动与 timeout 回调。它没有发包、ACK 检测器或链路队列，不能由这里的窗口曲线推断 30 MB 请求完成时间。`CUBIC-CONTRACT.md` 是实现前合同；原件在本目录 `sources/`，每次调用验证 `sources.lock.json` 的长度及 SHA256。

```sh
python calculations/research/congestion-controllers/cubic.py --output /tmp/cubic-all.json
python calculations/research/congestion-controllers/cubic.py --inputs calculations/research/congestion-controllers/cubic-example.json --output /tmp/cubic-one.json
```

无输入时执行 `scenarios()` 的全部固定场景。`calculate(inputs=None)` 返回单场景，`example()` 提供默认可编辑对象。`cubic-scenarios.json` 是场景名到输入映射，`cubic-result.json` 是相同键到结果映射。

所有时间单位秒、窗口/flight/已确认数据量单位 segment；有理数可以用 `"9/17"` 字符串。此处 segment 是统一 SMSS 单位，可以表达部分 segment；没有假定一个 ACK 对应一个 segment。输入最大 1000 事件。字段未知、非法负数、超预算有理数均拒绝。

| 输入 | 含义 |
|---|---|
| `C`, `beta` | 默认 2/5、7/10；alpha 初始为 3(1-beta)/(1+beta) |
| `fast_convergence` | 默认 false；单独场景显式启用 |
| `startup_policy` | 唯一支持 `reno_reference`；这是明确选用的参考启动，不实现通常 SHOULD 使用的 HyStart++ |
| `initial_window` | 空闲重启的 IW；默认初始 cwnd |
| `initial` | `phase` 为 slow_start 或 avoidance；cwnd、ssthresh、cwnd_prior、w_max、cwnd_epoch、w_est、epoch_elapsed 可编辑 |
| `events` | 按 at 非递减排列；同刻按输入顺序，纯状态调用不擅自重排网络事件 |

初始 avoidance 可以声明历史状态 seed，例如 cwnd=100、cwnd_epoch=96.8、Wmax=100，对应 K=2。它不是从 beta=0.7 的 100-segment loss 推导出的窗口。若不一致 seed 导致 Reno-friendly 新 ACK 降低 cwnd，拒绝该轨迹，不能悄悄夹值改变 RFC 更新。

| 事件 type | 额外字段/行为 |
|---|---|
| ack | segments_acked、smoothed_rtt。调用者保证仅含新确认量；0 表示重复 ACK，不增长。恢复/受限期也不增长 |
| congestion | event_id、flight_size，可选 signal=loss。保存旧 cwnd 为 cwnd_prior；按 flight×beta 减少，最少2；重复 ID/当前恢复期不重复减窗 |
| recovery_exit | 显式退出恢复。此处不实现 PRR/SACK；窗口等于阈值时按 RFC9438§4.10 进入慢启动，一次 ACK 超过阈值后进入新 CA epoch |
| timeout | event_id、flight_size。显式 TCP 式超时回调，cwnd=1，阈值按 beta×flight 且最少2；下次 CA 的 K=0。QUIC PTO 不能映射为这个回调 |
| limited_start/end | start 必须 reason=application 或 receiver_window；区间不能嵌套。区间内不积累 CA 立方时间 |
| idle_restart | idle_duration、rto；须在已观察受限区间内且持续时长不超该区间。idle>rto 时按 RFC5681 重启窗 min(IW,cwnd)；本参考采用重新建立 epoch 的显式政策，保留 Wmax，避免旧 epoch 与新 cwnd 错配 |
| observe | 仅观察，不把 Wcubic 值直接写入 cwnd |

每个 ACK 先 `W_est += alpha * segments_acked / cwnd`，达到 cwnd_prior 后 alpha 切1用于后续更新。如果 W_est 大于 Wcubic(t)，选择 RFC SHOULD 的 Reno-friendly W_est；否则 target=Wcubic(t+RTT) 夹在 `[cwnd,1.5*cwnd]`，单个 ACK 的增量为 `(target-cwnd)/cwnd`，此分支不再乘 segments_acked。输出 detail 留下 target/increment，state 留下窗口、阈值、epoch、K区间及受限状态。

有理数算术保持简单手算精确。一般 K 的立方根使用整数算术给出宽度不超过 10^-30 秒的包围区间，实际更新用其中点；curve/target 同时输出上下界。若 Reno 选择边界无法由区间确定，报错。状态位数超过4096时量化至10^-30 segment，并逐次记录精确局部误差；这不是整个理想实数轨迹的误差界。完全立方 K 和短手算没有此误差。

尚未实现 HyStart++、ECE/ECN、spurious undo、PRR/SACK、自动应用受限判断和反馈/业务闭环。RFC9438 的 errata7806 被官方拒绝，不将其 cwnd_prior→flight_size 建议应用到本计算。Reno 启动是本参考的明确选择，不能用本候选宣称所有生产 CUBIC 启动策略已经覆盖。
