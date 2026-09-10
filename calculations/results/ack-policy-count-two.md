# 上传、模型工作与响应：有限网络闭环

这是已确认单路径的有限 ACK 聚合与真实反馈计算。接收端按声明包数或期限触发，ACK 真正开始发送时才冻结范围和编码延迟；沿用同一发送方、流控、恢复与可选控制器。不是浏览器默认策略、ACK_FREQUENCY 协商或完整 TCP/QUIC 实测；媒体业务接入仍另行核算。

上传有效输入 **2,336 B**；响应有效输出 **0 B**；声明模型工作 **0 s**。

| 业务事件 | 实际时刻（秒，有理数） |
|---|---|
| 服务端完整收到上传 | 3 |
| 服务端模型开始 | 3 |
| 模型结束 | 3 |
| 客户端完整收到响应 | 3 |

| 方向 | 端点出口 bit/s | 出口后传播 s | 开始发送包数 | QUIC B | UDP/IP B | 声明完整线上 B |
|---|---:|---:|---:|---:|---:|---:|
| up | 9824 | 1 | 2 | 2400 | 56 | 2456 |
| down | 736 | 1 | 1 | 64 | 28 | 92 |

截至 horizon 实际串行线上字节：**2548 B**；已开始包的完整声明字节可能包含截止后尚未发完部分。接收唯一字节：**2336 B**。

ACK 策略按配置的包数或期限触发；实际开送前刷新范围，反向串行等待进入真实延迟。MAX 纳入 ack-eliciting 计数，纯 ACK 不触发 ACK；已开始发送的包不能抢占。

数值量化 quantum：`未启用，精确有理数`。量化采用 ties-to-even，保留正数和最小窗口；下面记录局部差值，不构成全轨迹误差界。

## 完整线上包时间轴

| 方向/PN | 类型 | STREAM 区间 | 开始 s | 结束 s | 计划到达 s | 实际接收 s | 线上 B | 丢弃 | 恢复/探测旧 PN | router 开始/结束 s |
|---|---|---|---|---|---|---|---:|---|---|---|
| up/0 | data | business:[0,1168) | 0 | 1 | 2 | 2 | 1228 | False | None | —/— |
| up/1 | data | business:[1168,2336) | 1 | 2 | 3 | 3 | 1228 | False | None | —/— |
| down/0 | ack | 控制 | 3 | 4 | 5 | 5 | 92 | False | None | —/— |

## 接收、消费与网络丢弃事件

| 时刻 s | 事件 | 方向 | 本地事实 |
|---|---|---|---|
| 2 | application_prefix | up | `{"prefix": 1168}` |
| 3 | application_prefix | up | `{"prefix": 2336}` |

## 发送方实际反馈与等待

| 方向 | 时刻 s | 事件 | 已知反馈 |
|---|---|---|---|
| up | 5 | ack | `{"ranges": [[0, 1]], "ack_delay": "0", "app_limited": true, "flow_limited": false}` |

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
    "rttvar": "3/2",
    "min_rtt": "4",
    "pto_count": 0,
    "probe_allowance": 0,
    "largest_acked": 1,
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
  "wire_bytes": 2548,
  "serialized_wire_bytes_by_horizon": "2548",
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

## ACK 聚合、范围与延迟

声明策略：`{"mode": "count_or_timer", "every": 2, "max_delay": 10}`。

范围保留数只限制报告范围，不等于接收端全部历史的内存上限。ACK frame 按实际 QUIC varint 宽度核算；声明报文空间不足时明确拒绝。若反向排队超过 max_delay，保留真实值并标记超期，不能夹短延迟掩盖期限未满足。

发送方首个 RTT 样本不扣 ACK delay；已有样本时按 minRTT 与声明上限决定扣除。纯 ACK PN 的 lost 身份不等于物理丢包或业务重传；应与数据 PN、实际 drop 和恢复记录分别计数。

| 方向/PN | 实际开送 s | ACK ranges | raw delay s | decoded delay s | frame B | 超期 |
|---|---|---|---|---|---:|---|
| down/0 | 3 | [[0, 1]] | 0 | 0 | 5 | False |

逐次 raw/adjusted RTT、SRTT 和 variance 记录见同名 JSON 的 rtt_samples。


## 已校验官方来源

- [RFC9000](https://www.rfc-editor.org/rfc/rfc9000.txt) — `f88aae47f8b18e102024916e975e919201d8dde689cba79b01079eaedd402e22`
- [RFC9002](https://www.rfc-editor.org/rfc/rfc9002.txt) — `3a8a54eea1ad5d1c134a548bf15edfa0e21bfb4106dbd7db3c09cace842099af`
- [RFC9002 Verified Errata7539](https://www.rfc-editor.org/errata/eid7539) — `685a6ef4fabde4fe163d1e86d6fb7aea7ded40ceab07a8a70e8027a4a9d0e23a`
