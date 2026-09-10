# 共享媒体与真实反馈：研究候选

本目录连接规范化应用 DAG 与已有公共 sender/ACK/controller/pacer，保持两向各一个共享拥塞窗口和物理发送器。`CONTRACT.md` 在实现前确定范围。当前是小例审查阶段，不能将规范化输入、构造器预检或小例通过当作完整30MB混合业务验收。

文件职责：`calculate.py` 是网络事件引擎；`application.py` 是本地依赖/非抢占FIFO计算/业务观察；主代理负责 `application_validation.py`；另一代理负责 `sender.py` 和依赖锁，直接委托冻结公共算法。`network_validation.py` 检查有限布局、链路、共享额度和内存；`run-small.py` 保存小场景完整结果。公共实现、已有研究候选及十二章正文未由本目录修改。

```sh
python calculations/research/media-feedback-loop/calculate.py --inputs calculations/research/media-feedback-loop/example.json --output /tmp/media-result.json
python calculations/research/media-feedback-loop/run-small.py
```

单输入由 `application`（media-feedback-inputs 的规范化DAG）和 `network` 组成。`example.json` 是真实PNG字节规模的截图→声明50ms服务→64B动作结果小例；固定14个小场景位于 `scenarios.json`。它们不沿用旧教学单包大小/共享credit/预定recovery_ready：消息保留，底层重新按声明1168B payload切片，并用实际PN选择丢包和sender反馈恢复。

网络必须显式声明两向links、until、initial_cwnd、initial_max_data、initial_max_stream_data和receive_memory_bytes。consume_delay为null时不消费、不发送MAX；非负值使真实按序前缀到达后才消费，并经真实反向消息更新MAX。有限STREAM额度使某流受阻时，其他流仍可被选择；它们共享同一方向cwnd。DATAGRAM不消耗STREAM额度，原子片过大拒绝，损失不重发；只有DATAGRAM尾部在途时PTO使用零业务PING。上层过期或内存不足不免费释放发送方flight。

统一1200B QUIC packet填充与28B外层头是声明profile；ACK64B仍通过真实反向serializer。每个message边界都保留，不跨块合并：完整30MB/5MB原始1400个业务块将对应30800个基础数据包，不能套旧合并字节流的29966包。归一化DAG的服务时间、音频生成间隔与版本事件是业务假设，不是模型实测速率。

计算资源按(endpoint,resource) FIFO、容量1、非抢占。发送priority只影响尚未开始的候选，不能抢占大包或改变compute顺序。可靠取消完整按序交付后只作用接收端本地tag，已经开始计算与发送保留；初版没有RESET_STREAM，取消未发尾部可能留下同流缺口，不能让后续可靠消息跳洞成功。

结果保存逐包transmissions、真实sender_events/rtt_samples、ACK开送快照、loss/timer/recovery、按流received/consumed、计算work和application_events。`delivered`同时列消息交付与task完成；`message_status`现为整DAG节点状态。业务观察分完整成片、识别结果、首次与完整播放、固定槽缺音、截图结果版本可用性。TTS `scheduled_play_end`是已开始播放的计划结束，`play_end`只在观测截止前实际结束时填写；未开始的未来播放不能报first_play。网络无待发包不等于业务完成。

`book-inputs.json`四格（FIFO/priority×立即/聚合ACK）和`image-baseline-inputs.json`由独立输入作者准备。它们仅通过构造器预检；完整运行需等待主审小例批准。后续验收必须保留真实完整轨迹、前后来源/代码hash、字节/flow/ACK守恒，以及各业务完成或失败原因。书中的TCP/H3匹配实测、握手整合与无线MAC仍是不同范围。
