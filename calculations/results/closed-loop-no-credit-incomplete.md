# 上传、模型工作与响应：有限网络闭环

这是已确认单路径上的参考 NewReno 与显式报文预算计算。包含实际双向发送、ACK、绝对流控、接收消费与可选有限路由队列。尚未覆盖媒体播放/取消/截图版本、控制器适配、自适应 pacing、ACK 聚合及完整 persistent congestion；不能据此宣称完整 TCP/QUIC。

上传有效输入 **3,504 B**；响应有效输出 **0 B**；声明模型工作 **0 s**。

| 业务事件 | 实际时刻（秒，有理数） |
|---|---|
| 服务端完整收到上传 | 未完成 |
| 服务端模型开始 | 未完成 |
| 模型结束 | 未完成 |
| 客户端完整收到响应 | 未完成 |

| 方向 | 端点出口 bit/s | 出口后传播 s | 开始发送包数 | QUIC B | UDP/IP B | 声明完整线上 B |
|---|---:|---:|---:|---:|---:|---:|
| up | 9824 | 1 | 0 | 0 | 0 | 0 |
| down | 736 | 1 | 0 | 0 | 0 | 0 |

截至 horizon 实际串行线上字节：**0 B**；已开始包的完整声明字节可能包含截止后尚未发完部分。接收唯一字节：**0 B**。

ACK 策略为每个 ack-eliciting 包立即生成独立单范围 ACK；ACK 出口排队和传播进入 RTT。MAX 控制也需 ACK，不能把额度到达时刻当作下一数据包实际发送时刻。纯 ACK/MAX、恢复/探测、普通数据依次优先，各类 FIFO；已经开始的串行发送不抢占。

数值量化 quantum：`未启用，精确有理数`。量化采用 ties-to-even，保留正数和最小窗口；下面记录局部差值，不构成全轨迹误差界。

## 完整线上包时间轴

| 方向/PN | 类型 | STREAM 区间 | 开始 s | 结束 s | 计划到达 s | 实际接收 s | 线上 B | 丢弃 | 恢复/探测旧 PN | router 开始/结束 s |
|---|---|---|---|---|---|---|---:|---|---|---|

## 接收、消费与网络丢弃事件

| 时刻 s | 事件 | 方向 | 本地事实 |
|---|---|---|---|

## 发送方实际反馈与等待

| 方向 | 时刻 s | 事件 | 已知反馈 |
|---|---|---|---|
| up | 0 | 等待 | MAX_DATA, MAX_STREAM_DATA:business |

## 定时器、判失与终态

### timers

```json
{
  "up": [],
  "down": []
}
```

### losses

```json
{
  "up": [],
  "down": []
}
```

### final_states

```json
{
  "up": {
    "bytes_in_flight": 0,
    "cwnd": "2400",
    "ssthresh": null,
    "recovery_start": null,
    "latest_rtt": "4",
    "smoothed_rtt": "4",
    "rttvar": "2",
    "min_rtt": "4",
    "pto_count": 0,
    "probe_allowance": 0,
    "largest_acked": null,
    "next_timer": null,
    "max_data": 0,
    "max_stream_data": {
      "business": 0
    },
    "stream_highest_sent_offsets": {},
    "max_data_consumed": 0
  },
  "down": {
    "bytes_in_flight": 0,
    "cwnd": "2400",
    "ssthresh": null,
    "recovery_start": null,
    "latest_rtt": "4",
    "smoothed_rtt": "4",
    "rttvar": "2",
    "min_rtt": "4",
    "pto_count": 0,
    "probe_allowance": 0,
    "largest_acked": null,
    "next_timer": null,
    "max_data": 0,
    "max_stream_data": {
      "business": 0
    },
    "stream_highest_sent_offsets": {},
    "max_data_consumed": 0
  }
}
```

### summary

```json
{
  "wire_bytes": 0,
  "serialized_wire_bytes_by_horizon": "0",
  "unique_received_bytes": 0,
  "pending_packets": {
    "up": 3,
    "down": 0
  },
  "complete": false
}
```

## 局部数值量化记录

| 方向 | 时刻 s | 字段 | 原值 | 舍入值 | 局部差 |
|---|---|---|---|---|---|

## 已校验官方来源

- [RFC9000](https://www.rfc-editor.org/rfc/rfc9000.txt) — `f88aae47f8b18e102024916e975e919201d8dde689cba79b01079eaedd402e22`
- [RFC9002](https://www.rfc-editor.org/rfc/rfc9002.txt) — `3a8a54eea1ad5d1c134a548bf15edfa0e21bfb4106dbd7db3c09cace842099af`
- [RFC9002 Verified Errata7539](https://www.rfc-editor.org/errata/eid7539) — `9b5338a8ac92a5968da09b63ee28616fb923b89ed4389f1cacd75b66693a7be7`
