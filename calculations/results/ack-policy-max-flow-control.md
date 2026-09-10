# 上传、模型工作与响应：有限网络闭环

这是已确认单路径的有限 ACK 聚合与真实反馈计算。接收端按声明包数或期限触发，ACK 真正开始发送时才冻结范围和编码延迟；沿用同一发送方、流控、恢复与可选控制器。不是浏览器默认策略、ACK_FREQUENCY 协商或完整 TCP/QUIC 实测；媒体业务接入仍另行核算。

上传有效输入 **3,504 B**；响应有效输出 **0 B**；声明模型工作 **0 s**。

| 业务事件 | 实际时刻（秒，有理数） |
|---|---|
| 服务端完整收到上传 | 7 |
| 服务端模型开始 | 7 |
| 模型结束 | 7 |
| 客户端完整收到响应 | 7 |

| 方向 | 端点出口 bit/s | 出口后传播 s | 开始发送包数 | QUIC B | UDP/IP B | 声明完整线上 B |
|---|---:|---:|---:|---:|---:|---:|
| up | 9824 | 1 | 6 | 3792 | 168 | 3960 |
| down | 736 | 1 | 5 | 320 | 140 | 460 |

截至 horizon 实际串行线上字节：**4420 B**；已开始包的完整声明字节可能包含截止后尚未发完部分。接收唯一字节：**3504 B**。

ACK 策略按配置的包数或期限触发；实际开送前刷新范围，反向串行等待进入真实延迟。MAX 纳入 ack-eliciting 计数，纯 ACK 不触发 ACK；已开始发送的包不能抢占。

数值量化 quantum：`未启用，精确有理数`。量化采用 ties-to-even，保留正数和最小窗口；下面记录局部差值，不构成全轨迹误差界。

## 完整线上包时间轴

| 方向/PN | 类型 | STREAM 区间 | 开始 s | 结束 s | 计划到达 s | 实际接收 s | 线上 B | 丢弃 | 恢复/探测旧 PN | router 开始/结束 s |
|---|---|---|---|---|---|---|---:|---|---|---|
| up/0 | data | business:[0,1168) | 0 | 1 | 2 | 2 | 1228 | False | None | —/— |
| up/1 | data | business:[1168,2336) | 1 | 2 | 3 | 3 | 1228 | False | None | —/— |
| down/0 | max | 控制 | 2 | 3 | 4 | 4 | 92 | False | None | —/— |
| down/1 | ack | 控制 | 3 | 4 | 5 | 5 | 92 | False | None | —/— |
| down/2 | max | 控制 | 4 | 5 | 6 | 6 | 92 | False | None | —/— |
| up/2 | ack | 控制 | 9/2 | 2809/614 | 3423/614 | 3423/614 | 92 | False | None | —/— |
| up/3 | data | business:[2336,3504) | 5 | 6 | 7 | 7 | 1228 | False | None | —/— |
| up/4 | ack | 控制 | 13/2 | 4037/614 | 4651/614 | 4651/614 | 92 | False | None | —/— |
| down/3 | max | 控制 | 7 | 8 | 9 | 9 | 92 | False | None | —/— |
| down/4 | ack | 控制 | 8 | 9 | 10 | 10 | 92 | False | None | —/— |
| up/5 | ack | 控制 | 19/2 | 5879/614 | 6493/614 | 6493/614 | 92 | False | None | —/— |

## 接收、消费与网络丢弃事件

| 时刻 s | 事件 | 方向 | 本地事实 |
|---|---|---|---|
| 2 | application_prefix | up | `{"prefix": 1168}` |
| 2 | consume | up | `{"consumed": 1168, "advertised_limit": 3504}` |
| 3 | application_prefix | up | `{"prefix": 2336}` |
| 3 | consume | up | `{"consumed": 2336, "advertised_limit": 4672}` |
| 7 | application_prefix | up | `{"prefix": 3504}` |
| 7 | consume | up | `{"consumed": 3504, "advertised_limit": 5840}` |

## 发送方实际反馈与等待

| 方向 | 时刻 s | 事件 | 已知反馈 |
|---|---|---|---|
| up | 4 | max_data | `{"value": 3504}` |
| up | 4 | max_stream_data | `{"value": 3504, "stream": "business"}` |
| up | 5 | ack | `{"ranges": [[0, 1]], "ack_delay": "0", "app_limited": false, "flow_limited": false}` |
| up | 6 | max_data | `{"value": 4672}` |
| up | 6 | max_stream_data | `{"value": 4672, "stream": "business"}` |
| up | 9 | max_data | `{"value": 5840}` |
| up | 9 | max_stream_data | `{"value": 5840, "stream": "business"}` |
| up | 10 | ack | `{"ranges": [[0, 4]], "ack_delay": "10627/25000", "app_limited": true, "flow_limited": false}` |
| down | 3423/614 | ack | `{"ranges": [[0, 0]], "ack_delay": "1/2", "app_limited": true, "flow_limited": false}` |
| down | 4651/614 | ack | `{"ranges": [[0, 2]], "ack_delay": "1/2", "app_limited": true, "flow_limited": false}` |
| down | 6493/614 | ack | `{"ranges": [[0, 3]], "ack_delay": "1/2", "app_limited": true, "flow_limited": false}` |
| up | 2 | 等待 | MAX_DATA, MAX_STREAM_DATA:business, cwnd |
| up | 4 | 等待 | cwnd |
| up | 2809/614 | 等待 | cwnd |

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
    "cwnd": "4800",
    "ssthresh": null,
    "recovery_start": null,
    "latest_rtt": "7/2",
    "smoothed_rtt": "63/16",
    "rttvar": "5/4",
    "min_rtt": "7/2",
    "pto_count": 0,
    "probe_allowance": 0,
    "largest_acked": 4,
    "next_timer": null,
    "max_data": 5840,
    "max_stream_data": {
      "business": 5840
    },
    "stream_highest_sent_offsets": {
      "business": 3504
    },
    "max_data_consumed": 3504
  },
  "down": {
    "bytes_in_flight": 0,
    "cwnd": "2400",
    "ssthresh": null,
    "recovery_start": null,
    "latest_rtt": "2195/614",
    "smoothed_rtt": "1213363/314368",
    "rttvar": "165771/157184",
    "min_rtt": "2195/614",
    "pto_count": 0,
    "probe_allowance": 0,
    "largest_acked": 3,
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
  "wire_bytes": 4420,
  "serialized_wire_bytes_by_horizon": "4420",
  "unique_received_bytes": 3504,
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

声明策略：`{"mode": "count_or_timer", "every": 2, "max_delay": "1/2"}`。

范围保留数只限制报告范围，不等于接收端全部历史的内存上限。ACK frame 按实际 QUIC varint 宽度核算；声明报文空间不足时明确拒绝。若反向排队超过 max_delay，保留真实值并标记超期，不能夹短延迟掩盖期限未满足。

发送方首个 RTT 样本不扣 ACK delay；已有样本时按 minRTT 与声明上限决定扣除。纯 ACK PN 的 lost 身份不等于物理丢包或业务重传；应与数据 PN、实际 drop 和恢复记录分别计数。

| 方向/PN | 实际开送 s | ACK ranges | raw delay s | decoded delay s | frame B | 超期 |
|---|---|---|---|---|---:|---|
| down/1 | 3 | [[0, 1]] | 0 | 0 | 5 | False |
| up/2 | 9/2 | [[0, 0]] | 1/2 | 1/2 | 8 | False |
| up/4 | 13/2 | [[0, 2]] | 1/2 | 1/2 | 8 | False |
| down/4 | 8 | [[0, 4]] | 261/614 | 10627/25000 | 8 | False |
| up/5 | 19/2 | [[0, 3]] | 1/2 | 1/2 | 8 | False |

逐次 raw/adjusted RTT、SRTT 和 variance 记录见同名 JSON 的 rtt_samples。


## 已校验官方来源

- [RFC9000](https://www.rfc-editor.org/rfc/rfc9000.txt) — `f88aae47f8b18e102024916e975e919201d8dde689cba79b01079eaedd402e22`
- [RFC9002](https://www.rfc-editor.org/rfc/rfc9002.txt) — `3a8a54eea1ad5d1c134a548bf15edfa0e21bfb4106dbd7db3c09cace842099af`
- [RFC9002 Verified Errata7539](https://www.rfc-editor.org/errata/eid7539) — `685a6ef4fabde4fe163d1e86d6fb7aea7ded40ceab07a8a70e8027a4a9d0e23a`
