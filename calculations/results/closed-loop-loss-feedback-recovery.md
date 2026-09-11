# 上传、模型工作与响应：有限网络闭环

这是已确认单路径上的参考 NewReno 与显式报文预算计算。包含实际双向发送、ACK、绝对流控、接收消费与可选有限路由队列。尚未覆盖媒体播放/取消/截图版本、控制器适配、自适应 pacing、ACK 聚合及完整 persistent congestion；不能据此宣称完整 TCP/QUIC。

上传有效输入 **2,336 B**；响应有效输出 **0 B**；声明模型工作 **0 s**。

| 业务事件 | 实际时刻（秒，有理数） |
|---|---|
| 服务端完整收到上传 | 7 |
| 服务端模型开始 | 7 |
| 模型结束 | 7 |
| 客户端完整收到响应 | 7 |

| 方向 | 端点出口 bit/s | 出口后传播 s | 开始发送包数 | QUIC B | UDP/IP B | 声明完整线上 B |
|---|---:|---:|---:|---:|---:|---:|
| up | 9824 | 1 | 3 | 3600 | 84 | 3684 |
| down | 736 | 1 | 2 | 128 | 56 | 184 |

截至 horizon 实际串行线上字节：**3868 B**；已开始包的完整声明字节可能包含截止后尚未发完部分。接收唯一字节：**2336 B**。

ACK 策略为每个 ack-eliciting 包立即生成独立单范围 ACK；ACK 出口排队和传播进入 RTT。MAX 控制也需 ACK，不能把额度到达时刻当作下一数据包实际发送时刻。纯 ACK/MAX、恢复/探测、普通数据依次优先，各类 FIFO；已经开始的串行发送不抢占。

数值量化 quantum：`未启用，精确有理数`。量化采用 ties-to-even，保留正数和最小窗口；下面记录局部差值，不构成全轨迹误差界。

## 完整线上包时间轴

| 方向/PN | 类型 | STREAM 区间 | 开始 s | 结束 s | 计划到达 s | 实际接收 s | 线上 B | 丢弃 | 恢复/探测旧 PN | router 开始/结束 s |
|---|---|---|---|---|---|---|---:|---|---|---|
| up/0 | data | business:[0,1168) | 0 | 1 | 2 | None | 1228 | True | None | —/— |
| up/1 | data | business:[1168,2336) | 1 | 2 | 3 | 3 | 1228 | False | None | —/— |
| down/0 | ack | 控制 | 3 | 4 | 5 | 5 | 92 | False | None | —/— |
| up/2 | data | business:[0,1168) | 5 | 6 | 7 | 7 | 1228 | False | 0 | —/— |
| down/1 | ack | 控制 | 7 | 8 | 9 | 9 | 92 | False | None | —/— |

## 接收、消费与网络丢弃事件

| 时刻 s | 事件 | 方向 | 本地事实 |
|---|---|---|---|
| 3 | application_prefix | up | `{"prefix": 0}` |
| 7 | application_prefix | up | `{"prefix": 2336}` |

## 发送方实际反馈与等待

| 方向 | 时刻 s | 事件 | 已知反馈 |
|---|---|---|---|
| up | 5 | ack | `{"ranges": [[1, 1]], "ack_delay": "0", "app_limited": true, "flow_limited": false}` |
| up | 9 | ack | `{"ranges": [[2, 2]], "ack_delay": "0", "app_limited": true, "flow_limited": false}` |

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
  "up": [
    {
      "at": "5",
      "pn": 0,
      "packet_threshold": false,
      "time_threshold": true
    }
  ],
  "down": []
}
```

### final_states

```json
{
  "up": {
    "bytes_in_flight": 0,
    "cwnd": "2400",
    "ssthresh": "1200",
    "recovery_start": "5",
    "latest_rtt": "4",
    "smoothed_rtt": "4",
    "rttvar": "9/8",
    "min_rtt": "4",
    "pto_count": 0,
    "probe_allowance": 0,
    "largest_acked": 2,
    "next_timer": null,
    "max_data": 2336,
    "max_stream_data": {
      "business": 2336
    },
    "stream_highest_sent_offsets": {
      "business": 2336
    },
    "max_data_consumed": 2336
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
    "max_data": 2336,
    "max_stream_data": {
      "business": 2336
    },
    "stream_highest_sent_offsets": {},
    "max_data_consumed": 0
  }
}
```

### summary

```json
{
  "wire_bytes": 3868,
  "serialized_wire_bytes_by_horizon": "3868",
  "unique_received_bytes": 2336,
  "pending_packets": {
    "up": 0,
    "down": 0
  },
  "complete": true
}
```

## 局部数值量化记录

| 方向 | 时刻 s | 字段 | 原值 | 舍入值 | 局部差 |
|---|---|---|---|---|---|

## 已校验官方来源

- [RFC9000](https://www.rfc-editor.org/rfc/rfc9000.txt) — `f88aae47f8b18e102024916e975e919201d8dde689cba79b01079eaedd402e22`
- [RFC9002](https://www.rfc-editor.org/rfc/rfc9002.txt) — `3a8a54eea1ad5d1c134a548bf15edfa0e21bfb4106dbd7db3c09cace842099af`
- [RFC9002 Verified Errata7539](https://www.rfc-editor.org/errata/eid7539) — `9b5338a8ac92a5968da09b63ee28616fb923b89ed4389f1cacd75b66693a7be7`
