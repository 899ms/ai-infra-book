# 共享媒体有限教学传输

声明的串行块、信用与单次恢复模型，不是 TCP／QUIC 协议栈或实测推理／播放性能。

## 独立调度与信用输入

| 参数 | 声明值 |
| --- | --- |
| scheduler | `fifo` |
| compute_scheduler | `fifo` |
| delivery_mode | `per_stream` |
| shared_credit_bytes | `1` |
| reliable_receive_credit_bytes | `100` |
| stream_credit_bytes | `100` |
| header_bytes | `0` |
| ack_bytes | `1` |

网络调度与计算调度分开。所有数据共享发送信用；不可靠媒体不占可靠接收／流信用。实际 ACK 只说明运输收到，不代表应用播放。

## 业务可用性与播放质量

本场景只检查运输条件，没有声明完整业务。

## 字节与未完成原因

| 数量 | 值 |
| --- | --- |
| evaluated_business_count | `0` |
| all_businesses_usable | `null` |
| all_reliable_packets_delivered | `true` |
| data_wire_bytes | `1` |
| ack_wire_bytes | `0` |
| unique_received_payload_bytes | `0` |
| unique_delivered_payload_bytes | `0` |
| shared_outstanding_bytes | `{"c2s": 1, "s2c": 0}` |
| last_event | `"2"` |

事件队列结束或 unfinished 为空不能代替业务完成；旧截图、缺音、取消输出分别保留状态。

- `lost-unit`：selected_loss_without_remaining_recovery_or_feedback
- `next-unit`：sender_visible_shared_or_reliable_credit_insufficient

## 非抢占工作与应用取消

| 工作 | 执行端／资源 | 开始（s） | 结束（s） | 运行中获知取消 |
| --- | --- | ---: | ---: | --- |

取消信号经过实际网络与可靠顺序交付后只影响接收端。已开始计算和发送保留。


## 适用范围与固定来源

- Teaching packet-ID credit and declared one-shot recovery; not TCP/QUIC cwnd/MAX_DATA/PTO.
- ACK means transport receipt, not playback; receive staging consumes into a separately unbounded reassembly store.
- Unreliable packets share send credit but not reliable receive/stream credit; lost packets without feedback retain send credit.
- Running work and in-flight packets cannot be cancelled; cancellation affects only local future starts after signal arrival.
- [RFC9221](https://www.rfc-editor.org/rfc/rfc9221.txt)：`ee8c04c5228fd120030ba7a8f6725c2ca609da107ad2ba8c44fdd44f73edb3b4`。
- [RFC8836](https://www.rfc-editor.org/rfc/rfc8836.txt)：`b124b69c5f067cabac4beac23c55dc1cae15be94b802a66f1649db64b01056a6`。
- [RFC3550](https://www.rfc-editor.org/rfc/rfc3550.txt)：`4c210e9434b5b4c029e8536ad8991f3709bc3cbfa0999e951bcb4c2143c539e8`。
- [RFC9000](https://www.rfc-editor.org/rfc/rfc9000.txt)：`f88aae47f8b18e102024916e975e919201d8dde689cba79b01079eaedd402e22`。
- [RFC9002](https://www.rfc-editor.org/rfc/rfc9002.txt)：`3a8a54eea1ad5d1c134a548bf15edfa0e21bfb4106dbd7db3c09cace842099af`。
- [RFC9114](https://www.rfc-editor.org/rfc/rfc9114.txt)：`6b84555c88eeebcf5d2b2e1d9d7b58630abc97ab877b2cf62dee4cd635db34e4`。

## 完整输入、逐包轨迹与固定轨迹交付重放

```json
{
  "calculation": "shared-media-finite-teaching-transport",
  "inputs": {
    "scheduler": "fifo",
    "delivery_mode": "per_stream",
    "c2s_bits_per_second": 8,
    "s2c_bits_per_second": 8,
    "c2s_propagation_seconds": 1,
    "s2c_propagation_seconds": 1,
    "header_bytes": 0,
    "ack_bytes": 1,
    "shared_credit_bytes": 1,
    "reliable_receive_credit_bytes": 100,
    "stream_credit_bytes": 100,
    "packets": [
      {
        "id": "lost-unit",
        "stream": "unit",
        "direction": "c2s",
        "offset": 0,
        "payload_bytes": 1,
        "reliable": false,
        "drop_first": true,
        "dependencies": [],
        "ready": 0,
        "priority": 0,
        "allow_expire": false,
        "deadline": null,
        "recovery_ready": null,
        "cancel_targets": []
      },
      {
        "id": "next-unit",
        "stream": "next",
        "direction": "c2s",
        "offset": 0,
        "payload_bytes": 1,
        "reliable": false,
        "dependencies": [],
        "ready": 0,
        "priority": 0,
        "allow_expire": false,
        "deadline": null,
        "drop_first": false,
        "recovery_ready": null,
        "cancel_targets": []
      }
    ],
    "businesses": [],
    "compute_scheduler": "fifo"
  },
  "reference_sources": [
    {
      "file": "sources/shared-media-rfc/rfc9221.txt",
      "url": "https://www.rfc-editor.org/rfc/rfc9221.txt",
      "revision": "RFC9221",
      "sha256": "ee8c04c5228fd120030ba7a8f6725c2ca609da107ad2ba8c44fdd44f73edb3b4"
    },
    {
      "file": "sources/shared-media-rfc/rfc8836.txt",
      "url": "https://www.rfc-editor.org/rfc/rfc8836.txt",
      "revision": "RFC8836",
      "sha256": "b124b69c5f067cabac4beac23c55dc1cae15be94b802a66f1649db64b01056a6"
    },
    {
      "file": "sources/shared-media-rfc/rfc3550.txt",
      "url": "https://www.rfc-editor.org/rfc/rfc3550.txt",
      "revision": "RFC3550",
      "sha256": "4c210e9434b5b4c029e8536ad8991f3709bc3cbfa0999e951bcb4c2143c539e8"
    },
    {
      "file": "sources/protocol-rfc/rfc9000.txt",
      "url": "https://www.rfc-editor.org/rfc/rfc9000.txt",
      "revision": "RFC9000",
      "sha256": "f88aae47f8b18e102024916e975e919201d8dde689cba79b01079eaedd402e22"
    },
    {
      "file": "sources/protocol-rfc/rfc9002.txt",
      "url": "https://www.rfc-editor.org/rfc/rfc9002.txt",
      "revision": "RFC9002",
      "sha256": "3a8a54eea1ad5d1c134a548bf15edfa0e21bfb4106dbd7db3c09cace842099af"
    },
    {
      "file": "sources/protocol-rfc/rfc9114.txt",
      "url": "https://www.rfc-editor.org/rfc/rfc9114.txt",
      "revision": "RFC9114",
      "sha256": "6b84555c88eeebcf5d2b2e1d9d7b58630abc97ab877b2cf62dee4cd635db34e4"
    }
  ],
  "transmissions": [
    {
      "kind": "data",
      "packet": "lost-unit",
      "stream": "unit",
      "direction": "c2s",
      "offset": 0,
      "end_offset": 1,
      "payload_bytes": 1,
      "wire_bytes": 1,
      "attempt": 1,
      "start": "0",
      "end": "1",
      "arrival": "2",
      "lost": true
    }
  ],
  "packets": [
    {
      "id": "lost-unit",
      "attempts": 1,
      "received": null,
      "delivered": null,
      "expired": false,
      "ready_order": 1,
      "acked": false,
      "recovery_due": false,
      "expiry_stage": null,
      "deadline_met": false,
      "cancelled_before_send": false
    },
    {
      "id": "next-unit",
      "attempts": 0,
      "received": null,
      "delivered": null,
      "expired": false,
      "ready_order": 2,
      "acked": false,
      "recovery_due": false,
      "expiry_stage": null,
      "deadline_met": false,
      "cancelled_before_send": false
    }
  ],
  "credit_events": [
    {
      "at": "0",
      "event": "send",
      "packet": "lost-unit",
      "direction": "c2s",
      "reserved_bytes": 1,
      "shared_outstanding": 1,
      "reliable_receive_outstanding": 0
    }
  ],
  "work": [],
  "cancellations": [],
  "businesses": [],
  "task_status": {},
  "delivery_only_replay": {
    "connection": {},
    "per_stream": {}
  },
  "summary": {
    "evaluated_business_count": 0,
    "all_businesses_usable": null,
    "all_reliable_packets_delivered": true,
    "data_wire_bytes": 1,
    "ack_wire_bytes": 0,
    "unique_received_payload_bytes": 0,
    "unique_delivered_payload_bytes": 0,
    "shared_outstanding_bytes": {
      "c2s": 1,
      "s2c": 0
    },
    "last_event": "2"
  },
  "unfinished_details": [
    {
      "packet": "lost-unit",
      "reason": "selected_loss_without_remaining_recovery_or_feedback"
    },
    {
      "packet": "next-unit",
      "reason": "sender_visible_shared_or_reliable_credit_insufficient"
    }
  ],
  "unfinished": [
    "lost-unit",
    "next-unit"
  ],
  "limitations": [
    "Teaching packet-ID credit and declared one-shot recovery; not TCP/QUIC cwnd/MAX_DATA/PTO.",
    "ACK means transport receipt, not playback; receive staging consumes into a separately unbounded reassembly store.",
    "Unreliable packets share send credit but not reliable receive/stream credit; lost packets without feedback retain send credit.",
    "Running work and in-flight packets cannot be cancelled; cancellation affects only local future starts after signal arrival."
  ]
}
```
