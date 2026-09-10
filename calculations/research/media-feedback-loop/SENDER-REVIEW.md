# sender 复用执行报告

本轮没有更改或复制公共 sender 算法。`sender.py` 是受来源锁约束的直接委托，另有 STREAM 恢复帧筛选助手。网络引擎的真正 DATAGRAM 不重发、控制包重传、取消与播放语义仍由网络作者接线，不能把本报告当整条媒体网络验收。

实际运行 `python calculations/research/media-feedback-loop/check-sender.py` 通过：18 项小整数/非法输入检查和 14 个历史完整数学回放。详细源码/依赖 SHA 与检查名称见 `sender-check.json`。

独立小例：A 实发 offset2,length3 占5连接额度；B 实发 offset0,length5再占5，总10。DATAGRAM length2不增加此值；新PN重发A原区间也仍为10。全部ACK后 STREAM 唯一字节是8，但 STREAM 总传输payload为11；DATAGRAM ACK字节为2。只增加 MAX_DATA 到20仍受B流额度5限制；真实 MAX_STREAM_DATA 到6后才解除。

DATAGRAM-only PTO 例以初始RTT0.1、max_ack_delay0，在0.3s产生机会；0.301s真实发送新PN的无payload PING probe，0.4s收到该ACK后旧DATAGRAM被声明lost但未重发。0.41s旧DATAGRAM晚ACK只增加一次确认字节，不重复释放flight。此例只证明sender与显式PING接口可用，不宣称网络已经自动正确选取该行为。

混合STREAM/DATAGRAM恢复助手返回STREAM深拷贝；修改返回值不会篡改原发送记录。非法重复DATAGRAM身份、未知流、布尔或负offset、零length、同包重复DATAGRAM和重叠STREAM均拒绝，validate_packet失败不改变state。

历史14场景从既有 `transport-feedback/scenarios.json` 逐事件enqueue后advance，逐完整events、packets、loss_events、timer_events、rtt_samples、final_state、sender_confirmed_business与summary和冻结result比较一致。来源路径等包装元数据不作为数学字段；没有用新输出覆盖旧期望。
