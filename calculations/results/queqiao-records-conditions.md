# Queqiao 原始记录的同条件统计

全部数字取自两份固定文档，本节不重跑实验。只有代次、负载、连接状态与内核设置全部相同的行才允许比较。

## 同条件比较

| 条件 | 分子 | 分母 | 分子 ms | 分母 ms | 中位数之比 | 文档配对比 |
|---|---|---|---:|---:|---:|---:|
| rotating-eight-files/asr_upload/held_open/0 | asr-rot-held-tuned-direct | asr-rot-held-tuned-queqiao | 225.80 | 295.00 | 0.765 | — |
| rotating-eight-files/asr_upload/held_open/1 | asr-rot-held-stock-direct | asr-rot-held-stock-queqiao | 789.90 | 292.70 | 2.699 | — |
| rotating-eight-files/asr_upload/new/1 | asr-rot-new-direct | asr-rot-new-queqiao | 1133.50 | 290.20 | 3.906 | 3.63 |
| rotating-eight-files/tts_download/held_open/0 | tts-rot-held-tuned-direct | tts-rot-held-tuned-queqiao | 629.40 | 71.40 | 8.815 | — |
| rotating-eight-files/tts_download/new/1 | tts-rot-new-direct | tts-rot-new-queqiao | 5661.30 | 4550.40 | 1.244 | — |
| single-fixed-file/asr_upload/held_open/0 | asr-fixed-held-tuned-direct | asr-fixed-held-tuned-queqiao | 240.90 | 236.50 | 1.019 | 1.03 |
| single-fixed-file/asr_upload/new/1 | asr-fixed-new-direct | asr-fixed-new-queqiao | 1185.30 | 301.60 | 3.930 | 3.96 |
| single-fixed-file/tts_download/new/1 | tts-fixed-new-direct | tts-fixed-new-queqiao | 827.70 | 53.40 | 15.500 | — |

配对比是逐轮比值的中位数，与两个中位数之比是不同的统计量；逐轮原值不在记录中，无法在此重算。

## 算术下界与可行载荷

下界＝一个往返＋拐点速率下的串行时间＋模型服务；两端都是区间，所以下界也是区间。
低于下界的中位数不是更快，而是不可能。

| 记录 | 观测 p50 ms | 最小载荷下界 ms | 最大可行载荷 B | 判定 |
|---|---:|---:|---:|---|
| asr-rot-new-direct | 1133.50 | 232.51 | ≥405000 | Consistent with the recorded payload range |
| asr-rot-new-queqiao | 290.20 | 232.51 | ≥405000 | Consistent with the recorded payload range |
| asr-rot-held-stock-direct | 789.90 | 232.51 | ≥405000 | Consistent with the recorded payload range |
| asr-rot-held-stock-queqiao | 292.70 | 232.51 | ≥405000 | Consistent with the recorded payload range |
| asr-rot-held-tuned-direct | 225.80 | 232.51 | 不可行 | Below the floor across the recorded round-trip band; only the recorded minimum round trip admits it |
| asr-rot-held-tuned-queqiao | 295.00 | 232.51 | ≥405000 | Consistent with the recorded payload range |
| asr-fixed-new-direct | 1185.30 | 235.52 | ≥354640 | Consistent with the recorded payload range |
| asr-fixed-new-queqiao | 301.60 | 235.52 | ≥354640 | Consistent with the recorded payload range |
| asr-fixed-held-tuned-direct | 240.90 | 235.52 | ≥354640 | Consistent with the recorded payload range |
| asr-fixed-held-tuned-queqiao | 236.50 | 235.52 | ≥354640 | Consistent with the recorded payload range |
| tts-rot-new-direct | 5661.30 | 232.51 | ≥405000 | Consistent with the recorded payload range |
| tts-rot-new-queqiao | 4550.40 | 232.51 | ≥405000 | Consistent with the recorded payload range |

## 分段与时间戳误差

各段是各自轮次的中位数，中位数不可相加；残差用来证明这一点，不代表未测量的阶段。

| 记录 | 各段和 ms | 总计 ms | 残差 ms | 分辨率界 ms | 结论 |
|---|---:|---:|---:|---:|---|
| asr-rot-new-direct | 1135.30 | 1133.50 | -1.80 | 0.15 | Residual exceeds rounding, so these are per-leg medians of different rounds and do not add |
| asr-rot-new-queqiao | 290.30 | 290.20 | -0.10 | 0.15 | Residual fits the reported resolution |
| tts-rot-new-direct | 5588.10 | 5661.30 | 73.20 | 0.20 | Residual exceeds rounding, so these are per-leg medians of different rounds and do not add |
| tts-rot-new-queqiao | 4533.40 | 4550.40 | 17.00 | 0.20 | Residual exceeds rounding, so these are per-leg medians of different rounds and do not add |

## 帧分位数的样本支撑

缺失的分位数保持缺失。已给出的分位数标注其背后实际有多少个样本。

| 记录 | 提供 | 丢失 | 丢失率 | p50 | p99 | p99 之外样本 | 支撑 |
|---|---:|---:|---:|---:|---:|---:|---|
| frames-live-udp-direct | 3200 | 163 | 0.0509 | 193.60 | 213.70 | 32 | 是 |
| frames-live-udp-queqiao | 3200 | 34 | 0.0106 | 208.20 | 217.60 | 32 | 是 |
| frames-live-tcp-queqiao | 3200 | 0 | 0.0000 | 208.40 | 728.40 | 32 | 是 |
| frames-dc-udp-direct | 1200 | 40 | 0.0333 | — | 210.10 | 12 | 是 |
| frames-dc-udp-queqiao | 1200 | 2 | 0.0017 | — | 213.50 | 12 | 是 |
| frames-dc-tcp-queqiao | 1200 | 0 | 0.0000 | — | — | — | — |
| frames-access-udp-direct | 1200 | 156 | 0.1300 | — | 212.10 | 12 | 是 |
| frames-access-udp-queqiao | 1200 | 45 | 0.0375 | — | 215.00 | 12 | 是 |
| frames-access-tcp-queqiao | 1200 | 0 | 0.0000 | — | 599.90 | 12 | 是 |
| frames-revalidated-udp-direct | 1200 | 52 | 0.0433 | — | 212.40 | 12 | 是 |
| frames-revalidated-udp-queqiao | 1200 | 15 | 0.0125 | — | 209.80 | 12 | 是 |
| frames-revalidated-tcp-queqiao | 1200 | 0 | 0.0000 | — | 737.10 | 12 | 是 |
| frames-emulated-24-session | — | — | — | 203.30 | 766.60 | — | — |

## 持续供给与播放消费

按声明的 16000 Hz／1 声道／2 字节采样，播放消费为 256000 bit/s。文档只记录了字节数，格式是本计算的声明假设。

| 测量 | 供给 bit/s | 相对消费 | 足够 | 首次卡顿 ms |
|---|---:|---:|---|---:|
| download_direct_cubic_high | 470000 | 1.836 | 是 | — |
| download_direct_cubic_low | 130000 | 0.508 | 否 | 121.90 |
| download_direct_high | 84000000 | 328.125 | 是 | — |
| download_direct_low | 68000000 | 265.625 | 是 | — |
| download_queqiao_high | 268000000 | 1046.875 | 是 | — |
| download_queqiao_low | 224000000 | 875.000 | 是 | — |
| upload_direct_high | 105800000 | 413.281 | 是 | — |
| upload_direct_low | 3600000 | 14.062 | 是 | — |
| upload_queqiao_high | 310400000 | 1212.500 | 是 | — |
| upload_queqiao_low | 400000 | 1.562 | 是 | — |

## 慢启动轮次核对

初始窗口 10 段、每轮翻倍，清空该载荷需 5 轮，预测 995.00 ms；实测 request-to-first-byte 为 948.20 ms，差 -46.80 ms。

## 口径与限制

- Every figure is transcribed from the two pinned documents; no run was repeated for this calculation.
- Rows are compared only when generation, workload, connection state and kernel setting all match.
- The rotating-eight-file generation carries a payload interval, not a size, so no per-size claim rests on it.
- Per-leg medians come from different rounds and are not additive; the residual measures that, not a missing stage.
- Audio sample rate, channel count and sample width are declared assumptions; the documents state only the byte count.
- Capture and playback are outside every recorded leg, so no recorded total is a user-perceived time.
- A quantile the documents do not print stays unavailable; none is interpolated from the ones they do print.
- Ratios here are ratios of medians; the documents' paired per-round ratios are carried for comparison and cannot be recomputed from these records.

## 完整输入、来源与结果

```json
{
  "calculation": "queqiao-recorded-conditions",
  "inputs": {
    "prebuffer_ms": 60.0,
    "comparison_leg": "total"
  },
  "sources": [
    {
      "file": "sources/queqiao-records/PATH-CHARACTER-DC-20260826.md",
      "bytes": 43272,
      "sha256": "26b2b1086d63579276ac304d456c9cfd69ca8c23b242b71ba27f10c87eef3675",
      "origin": "references/author-context/queqiao-168ff4b/PATH-CHARACTER-DC-20260826.md"
    },
    {
      "file": "sources/queqiao-records/DESIGN-DC-PROFILE.md",
      "bytes": 28995,
      "sha256": "0c1e1a6f47b14a7ab60e671bc2163ed3c0d4f2a99ad413e6fa0d5afd4d335491",
      "origin": "references/author-context/queqiao-168ff4b/DESIGN-DC-PROFILE.md"
    },
    {
      "file": "sources/queqiao-records/records.json",
      "bytes": 19413,
      "sha256": "02d83d3479fc8433df0525db364ddef8ed21269219456a2723c17384b2d1f0c4",
      "origin": "transcribed from the two pinned documents above"
    }
  ],
  "reported_resolution_ms": 0.1,
  "half_ulp_ms": {
    "numerator": 1,
    "denominator": 20
  },
  "generations": {
    "rotating-eight-files": {
      "superseded": true,
      "payload_low_bytes": 146000,
      "payload_high_bytes": 405000,
      "claimed_label_bytes": 355000,
      "label_supported": false,
      "reason": "The benchmark rotated eight files and reported only the last request's size, so every figure labelled 355KB is a median across the whole range.",
      "section": "PATH#the-workload-this-was-built-for"
    },
    "single-fixed-file": {
      "superseded": false,
      "payload_low_bytes": 354640,
      "payload_high_bytes": 354640,
      "claimed_label_bytes": 354640,
      "label_supported": true,
      "reason": "One fixed file, arms alternating within the run, after the pacing fix.",
      "section": "PATH#re-measured-with-one-fixed-file"
    }
  },
  "same_condition_comparisons": [
    {
      "leg": "total",
      "condition": [
        "rotating-eight-files",
        "asr_upload",
        "held_open",
        0
      ],
      "numerator_id": "asr-rot-held-tuned-direct",
      "denominator_id": "asr-rot-held-tuned-queqiao",
      "numerator_ms": {
        "numerator": 1129,
        "denominator": 5
      },
      "denominator_ms": {
        "numerator": 295,
        "denominator": 1
      },
      "ratio": {
        "numerator": 1129,
        "denominator": 1475
      },
      "difference_ms": {
        "numerator": -346,
        "denominator": 5
      },
      "documented_paired_ratio": null,
      "paired_vs_ratio_of_medians": null,
      "paired_note": "The documents give only a spread for this condition, not a paired median",
      "documented_paired_spread": [
        0.66,
        2.93
      ]
    },
    {
      "leg": "total",
      "condition": [
        "rotating-eight-files",
        "asr_upload",
        "held_open",
        1
      ],
      "numerator_id": "asr-rot-held-stock-direct",
      "denominator_id": "asr-rot-held-stock-queqiao",
      "numerator_ms": {
        "numerator": 7899,
        "denominator": 10
      },
      "denominator_ms": {
        "numerator": 2927,
        "denominator": 10
      },
      "ratio": {
        "numerator": 7899,
        "denominator": 2927
      },
      "difference_ms": {
        "numerator": 2486,
        "denominator": 5
      },
      "documented_paired_ratio": null,
      "paired_vs_ratio_of_medians": null,
      "paired_note": "The documents give no median of per-round ratios for this condition",
      "documented_paired_spread": null
    },
    {
      "leg": "total",
      "condition": [
        "rotating-eight-files",
        "asr_upload",
        "new",
        1
      ],
      "numerator_id": "asr-rot-new-direct",
      "denominator_id": "asr-rot-new-queqiao",
      "numerator_ms": {
        "numerator": 2267,
        "denominator": 2
      },
      "denominator_ms": {
        "numerator": 1451,
        "denominator": 5
      },
      "ratio": {
        "numerator": 11335,
        "denominator": 2902
      },
      "difference_ms": {
        "numerator": 8433,
        "denominator": 10
      },
      "documented_paired_ratio": {
        "numerator": 363,
        "denominator": 100
      },
      "paired_vs_ratio_of_medians": {
        "numerator": -40037,
        "denominator": 145100
      },
      "paired_note": "A median of per-round ratios is not the ratio of the two medians; the per-round values are not in the records, so only the difference is shown",
      "documented_paired_spread": [
        3.47,
        4.21
      ]
    },
    {
      "leg": "download",
      "condition": [
        "rotating-eight-files",
        "tts_download",
        "held_open",
        0
      ],
      "numerator_id": "tts-rot-held-tuned-direct",
      "denominator_id": "tts-rot-held-tuned-queqiao",
      "numerator_ms": {
        "numerator": 3147,
        "denominator": 5
      },
      "denominator_ms": {
        "numerator": 357,
        "denominator": 5
      },
      "ratio": {
        "numerator": 1049,
        "denominator": 119
      },
      "difference_ms": {
        "numerator": 558,
        "denominator": 1
      },
      "documented_paired_ratio": null,
      "paired_vs_ratio_of_medians": null,
      "paired_note": "The documents give no median of per-round ratios for this condition",
      "documented_paired_spread": null
    },
    {
      "leg": "total",
      "condition": [
        "rotating-eight-files",
        "tts_download",
        "new",
        1
      ],
      "numerator_id": "tts-rot-new-direct",
      "denominator_id": "tts-rot-new-queqiao",
      "numerator_ms": {
        "numerator": 56613,
        "denominator": 10
      },
      "denominator_ms": {
        "numerator": 22752,
        "denominator": 5
      },
      "ratio": {
        "numerator": 18871,
        "denominator": 15168
      },
      "difference_ms": {
        "numerator": 11109,
        "denominator": 10
      },
      "documented_paired_ratio": null,
      "paired_vs_ratio_of_medians": null,
      "paired_note": "The documents give only a spread for this condition, not a paired median",
      "documented_paired_spread": [
        0.9,
        1.42
      ]
    },
    {
      "leg": "total",
      "condition": [
        "single-fixed-file",
        "asr_upload",
        "held_open",
        0
      ],
      "numerator_id": "asr-fixed-held-tuned-direct",
      "denominator_id": "asr-fixed-held-tuned-queqiao",
      "numerator_ms": {
        "numerator": 2409,
        "denominator": 10
      },
      "denominator_ms": {
        "numerator": 473,
        "denominator": 2
      },
      "ratio": {
        "numerator": 219,
        "denominator": 215
      },
      "difference_ms": {
        "numerator": 22,
        "denominator": 5
      },
      "documented_paired_ratio": {
        "numerator": 103,
        "denominator": 100
      },
      "paired_vs_ratio_of_medians": {
        "numerator": 49,
        "denominator": 4300
      },
      "paired_note": "A median of per-round ratios is not the ratio of the two medians; the per-round values are not in the records, so only the difference is shown",
      "documented_paired_spread": [
        null,
        null
      ]
    },
    {
      "leg": "total",
      "condition": [
        "single-fixed-file",
        "asr_upload",
        "new",
        1
      ],
      "numerator_id": "asr-fixed-new-direct",
      "denominator_id": "asr-fixed-new-queqiao",
      "numerator_ms": {
        "numerator": 11853,
        "denominator": 10
      },
      "denominator_ms": {
        "numerator": 1508,
        "denominator": 5
      },
      "ratio": {
        "numerator": 11853,
        "denominator": 3016
      },
      "difference_ms": {
        "numerator": 8837,
        "denominator": 10
      },
      "documented_paired_ratio": {
        "numerator": 99,
        "denominator": 25
      },
      "paired_vs_ratio_of_medians": {
        "numerator": 2259,
        "denominator": 75400
      },
      "paired_note": "A median of per-round ratios is not the ratio of the two medians; the per-round values are not in the records, so only the difference is shown",
      "documented_paired_spread": [
        null,
        null
      ]
    },
    {
      "leg": "download",
      "condition": [
        "single-fixed-file",
        "tts_download",
        "new",
        1
      ],
      "numerator_id": "tts-fixed-new-direct",
      "denominator_id": "tts-fixed-new-queqiao",
      "numerator_ms": {
        "numerator": 8277,
        "denominator": 10
      },
      "denominator_ms": {
        "numerator": 267,
        "denominator": 5
      },
      "ratio": {
        "numerator": 31,
        "denominator": 2
      },
      "difference_ms": {
        "numerator": 7743,
        "denominator": 10
      },
      "documented_paired_ratio": null,
      "paired_vs_ratio_of_medians": null,
      "paired_note": "The documents give no median of per-round ratios for this condition",
      "documented_paired_spread": null
    }
  ],
  "conditions_without_a_pair": [
    {
      "condition": [
        "single-fixed-file",
        "tts_download",
        "held_open",
        0
      ],
      "ids": [
        "tts-fixed-held-tuned-direct"
      ],
      "reason": "This condition does not hold both arms with a shared leg median"
    }
  ],
  "floor_feasibility": [
    {
      "id": "asr-rot-new-direct",
      "generation": "rotating-eight-files",
      "observed_p50_ms": {
        "numerator": 2267,
        "denominator": 2
      },
      "payload_interval_bytes": [
        146000,
        405000
      ],
      "label_supported": false,
      "round_trip_band_ms": [
        199.0,
        207.0
      ],
      "floor_at_smallest_payload": {
        "payload_bytes": 146000,
        "wire_ms": {
          "numerator": 1168,
          "denominator": 333
        },
        "low_ms": {
          "numerator": 77425,
          "denominator": 333
        },
        "high_ms": {
          "numerator": 82753,
          "denominator": 333
        }
      },
      "floor_at_largest_payload": {
        "payload_bytes": 405000,
        "wire_ms": {
          "numerator": 360,
          "denominator": 37
        },
        "low_ms": {
          "numerator": 8833,
          "denominator": 37
        },
        "high_ms": {
          "numerator": 9425,
          "denominator": 37
        }
      },
      "below_floor_at_smallest_payload": false,
      "largest_feasible_payload_bytes": 37649812,
      "largest_feasible_payload_bytes_at_minimum_rtt": 38195100,
      "exceeds_recorded_payload_range": true,
      "verdict": "Consistent with the recorded payload range"
    },
    {
      "id": "asr-rot-new-queqiao",
      "generation": "rotating-eight-files",
      "observed_p50_ms": {
        "numerator": 1451,
        "denominator": 5
      },
      "payload_interval_bytes": [
        146000,
        405000
      ],
      "label_supported": false,
      "round_trip_band_ms": [
        199.0,
        207.0
      ],
      "floor_at_smallest_payload": {
        "payload_bytes": 146000,
        "wire_ms": {
          "numerator": 1168,
          "denominator": 333
        },
        "low_ms": {
          "numerator": 77425,
          "denominator": 333
        },
        "high_ms": {
          "numerator": 82753,
          "denominator": 333
        }
      },
      "floor_at_largest_payload": {
        "payload_bytes": 405000,
        "wire_ms": {
          "numerator": 360,
          "denominator": 37
        },
        "low_ms": {
          "numerator": 8833,
          "denominator": 37
        },
        "high_ms": {
          "numerator": 9425,
          "denominator": 37
        }
      },
      "below_floor_at_smallest_payload": false,
      "largest_feasible_payload_bytes": 2547450,
      "largest_feasible_payload_bytes_at_minimum_rtt": 3092737,
      "exceeds_recorded_payload_range": true,
      "verdict": "Consistent with the recorded payload range"
    },
    {
      "id": "asr-rot-held-stock-direct",
      "generation": "rotating-eight-files",
      "observed_p50_ms": {
        "numerator": 7899,
        "denominator": 10
      },
      "payload_interval_bytes": [
        146000,
        405000
      ],
      "label_supported": false,
      "round_trip_band_ms": [
        199.0,
        207.0
      ],
      "floor_at_smallest_payload": {
        "payload_bytes": 146000,
        "wire_ms": {
          "numerator": 1168,
          "denominator": 333
        },
        "low_ms": {
          "numerator": 77425,
          "denominator": 333
        },
        "high_ms": {
          "numerator": 82753,
          "denominator": 333
        }
      },
      "floor_at_largest_payload": {
        "payload_bytes": 405000,
        "wire_ms": {
          "numerator": 360,
          "denominator": 37
        },
        "low_ms": {
          "numerator": 8833,
          "denominator": 37
        },
        "high_ms": {
          "numerator": 9425,
          "denominator": 37
        }
      },
      "below_floor_at_smallest_payload": false,
      "largest_feasible_payload_bytes": 23347462,
      "largest_feasible_payload_bytes_at_minimum_rtt": 23892750,
      "exceeds_recorded_payload_range": true,
      "verdict": "Consistent with the recorded payload range"
    },
    {
      "id": "asr-rot-held-stock-queqiao",
      "generation": "rotating-eight-files",
      "observed_p50_ms": {
        "numerator": 2927,
        "denominator": 10
      },
      "payload_interval_bytes": [
        146000,
        405000
      ],
      "label_supported": false,
      "round_trip_band_ms": [
        199.0,
        207.0
      ],
      "floor_at_smallest_payload": {
        "payload_bytes": 146000,
        "wire_ms": {
          "numerator": 1168,
          "denominator": 333
        },
        "low_ms": {
          "numerator": 77425,
          "denominator": 333
        },
        "high_ms": {
          "numerator": 82753,
          "denominator": 333
        }
      },
      "floor_at_largest_payload": {
        "payload_bytes": 405000,
        "wire_ms": {
          "numerator": 360,
          "denominator": 37
        },
        "low_ms": {
          "numerator": 8833,
          "denominator": 37
        },
        "high_ms": {
          "numerator": 9425,
          "denominator": 37
        }
      },
      "below_floor_at_smallest_payload": false,
      "largest_feasible_payload_bytes": 2651512,
      "largest_feasible_payload_bytes_at_minimum_rtt": 3196800,
      "exceeds_recorded_payload_range": true,
      "verdict": "Consistent with the recorded payload range"
    },
    {
      "id": "asr-rot-held-tuned-direct",
      "generation": "rotating-eight-files",
      "observed_p50_ms": {
        "numerator": 1129,
        "denominator": 5
      },
      "payload_interval_bytes": [
        146000,
        405000
      ],
      "label_supported": false,
      "round_trip_band_ms": [
        199.0,
        207.0
      ],
      "floor_at_smallest_payload": {
        "payload_bytes": 146000,
        "wire_ms": {
          "numerator": 1168,
          "denominator": 333
        },
        "low_ms": {
          "numerator": 77425,
          "denominator": 333
        },
        "high_ms": {
          "numerator": 82753,
          "denominator": 333
        }
      },
      "floor_at_largest_payload": {
        "payload_bytes": 405000,
        "wire_ms": {
          "numerator": 360,
          "denominator": 37
        },
        "low_ms": {
          "numerator": 8833,
          "denominator": 37
        },
        "high_ms": {
          "numerator": 9425,
          "denominator": 37
        }
      },
      "below_floor_at_smallest_payload": true,
      "largest_feasible_payload_bytes": null,
      "largest_feasible_payload_bytes_at_minimum_rtt": 412087,
      "exceeds_recorded_payload_range": false,
      "verdict": "Below the floor across the recorded round-trip band; only the recorded minimum round trip admits it"
    },
    {
      "id": "asr-rot-held-tuned-queqiao",
      "generation": "rotating-eight-files",
      "observed_p50_ms": {
        "numerator": 295,
        "denominator": 1
      },
      "payload_interval_bytes": [
        146000,
        405000
      ],
      "label_supported": false,
      "round_trip_band_ms": [
        199.0,
        207.0
      ],
      "floor_at_smallest_payload": {
        "payload_bytes": 146000,
        "wire_ms": {
          "numerator": 1168,
          "denominator": 333
        },
        "low_ms": {
          "numerator": 77425,
          "denominator": 333
        },
        "high_ms": {
          "numerator": 82753,
          "denominator": 333
        }
      },
      "floor_at_largest_payload": {
        "payload_bytes": 405000,
        "wire_ms": {
          "numerator": 360,
          "denominator": 37
        },
        "low_ms": {
          "numerator": 8833,
          "denominator": 37
        },
        "high_ms": {
          "numerator": 9425,
          "denominator": 37
        }
      },
      "below_floor_at_smallest_payload": false,
      "largest_feasible_payload_bytes": 2747250,
      "largest_feasible_payload_bytes_at_minimum_rtt": 3292537,
      "exceeds_recorded_payload_range": true,
      "verdict": "Consistent with the recorded payload range"
    },
    {
      "id": "asr-fixed-new-direct",
      "generation": "single-fixed-file",
      "observed_p50_ms": {
        "numerator": 11853,
        "denominator": 10
      },
      "payload_interval_bytes": [
        354640,
        354640
      ],
      "label_supported": true,
      "round_trip_band_ms": [
        197.0,
        205.0
      ],
      "floor_at_smallest_payload": {
        "payload_bytes": 354640,
        "wire_ms": {
          "numerator": 70928,
          "denominator": 8325
        },
        "low_ms": {
          "numerator": 1960703,
          "denominator": 8325
        },
        "high_ms": {
          "numerator": 2093903,
          "denominator": 8325
        }
      },
      "floor_at_largest_payload": {
        "payload_bytes": 354640,
        "wire_ms": {
          "numerator": 70928,
          "denominator": 8325
        },
        "low_ms": {
          "numerator": 1960703,
          "denominator": 8325
        },
        "high_ms": {
          "numerator": 2093903,
          "denominator": 8325
        }
      },
      "below_floor_at_smallest_payload": false,
      "largest_feasible_payload_bytes": 39889237,
      "largest_feasible_payload_bytes_at_minimum_rtt": null,
      "exceeds_recorded_payload_range": true,
      "verdict": "Consistent with the recorded payload range"
    },
    {
      "id": "asr-fixed-new-queqiao",
      "generation": "single-fixed-file",
      "observed_p50_ms": {
        "numerator": 1508,
        "denominator": 5
      },
      "payload_interval_bytes": [
        354640,
        354640
      ],
      "label_supported": true,
      "round_trip_band_ms": [
        197.0,
        205.0
      ],
      "floor_at_smallest_payload": {
        "payload_bytes": 354640,
        "wire_ms": {
          "numerator": 70928,
          "denominator": 8325
        },
        "low_ms": {
          "numerator": 1960703,
          "denominator": 8325
        },
        "high_ms": {
          "numerator": 2093903,
          "denominator": 8325
        }
      },
      "floor_at_largest_payload": {
        "payload_bytes": 354640,
        "wire_ms": {
          "numerator": 70928,
          "denominator": 8325
        },
        "low_ms": {
          "numerator": 1960703,
          "denominator": 8325
        },
        "high_ms": {
          "numerator": 2093903,
          "denominator": 8325
        }
      },
      "below_floor_at_smallest_payload": false,
      "largest_feasible_payload_bytes": 3105225,
      "largest_feasible_payload_bytes_at_minimum_rtt": null,
      "exceeds_recorded_payload_range": true,
      "verdict": "Consistent with the recorded payload range"
    },
    {
      "id": "asr-fixed-held-tuned-direct",
      "generation": "single-fixed-file",
      "observed_p50_ms": {
        "numerator": 2409,
        "denominator": 10
      },
      "payload_interval_bytes": [
        354640,
        354640
      ],
      "label_supported": true,
      "round_trip_band_ms": [
        197.0,
        205.0
      ],
      "floor_at_smallest_payload": {
        "payload_bytes": 354640,
        "wire_ms": {
          "numerator": 70928,
          "denominator": 8325
        },
        "low_ms": {
          "numerator": 1960703,
          "denominator": 8325
        },
        "high_ms": {
          "numerator": 2093903,
          "denominator": 8325
        }
      },
      "floor_at_largest_payload": {
        "payload_bytes": 354640,
        "wire_ms": {
          "numerator": 70928,
          "denominator": 8325
        },
        "low_ms": {
          "numerator": 1960703,
          "denominator": 8325
        },
        "high_ms": {
          "numerator": 2093903,
          "denominator": 8325
        }
      },
      "below_floor_at_smallest_payload": false,
      "largest_feasible_payload_bytes": 578587,
      "largest_feasible_payload_bytes_at_minimum_rtt": null,
      "exceeds_recorded_payload_range": true,
      "verdict": "Consistent with the recorded payload range"
    },
    {
      "id": "asr-fixed-held-tuned-queqiao",
      "generation": "single-fixed-file",
      "observed_p50_ms": {
        "numerator": 473,
        "denominator": 2
      },
      "payload_interval_bytes": [
        354640,
        354640
      ],
      "label_supported": true,
      "round_trip_band_ms": [
        197.0,
        205.0
      ],
      "floor_at_smallest_payload": {
        "payload_bytes": 354640,
        "wire_ms": {
          "numerator": 70928,
          "denominator": 8325
        },
        "low_ms": {
          "numerator": 1960703,
          "denominator": 8325
        },
        "high_ms": {
          "numerator": 2093903,
          "denominator": 8325
        }
      },
      "floor_at_largest_payload": {
        "payload_bytes": 354640,
        "wire_ms": {
          "numerator": 70928,
          "denominator": 8325
        },
        "low_ms": {
          "numerator": 1960703,
          "denominator": 8325
        },
        "high_ms": {
          "numerator": 2093903,
          "denominator": 8325
        }
      },
      "below_floor_at_smallest_payload": false,
      "largest_feasible_payload_bytes": 395437,
      "largest_feasible_payload_bytes_at_minimum_rtt": null,
      "exceeds_recorded_payload_range": true,
      "verdict": "Consistent with the recorded payload range"
    },
    {
      "id": "tts-rot-new-direct",
      "generation": "rotating-eight-files",
      "observed_p50_ms": {
        "numerator": 56613,
        "denominator": 10
      },
      "payload_interval_bytes": [
        146000,
        405000
      ],
      "label_supported": false,
      "round_trip_band_ms": [
        199.0,
        207.0
      ],
      "floor_at_smallest_payload": {
        "payload_bytes": 146000,
        "wire_ms": {
          "numerator": 1168,
          "denominator": 333
        },
        "low_ms": {
          "numerator": 77425,
          "denominator": 333
        },
        "high_ms": {
          "numerator": 82753,
          "denominator": 333
        }
      },
      "floor_at_largest_payload": {
        "payload_bytes": 405000,
        "wire_ms": {
          "numerator": 360,
          "denominator": 37
        },
        "low_ms": {
          "numerator": 8833,
          "denominator": 37
        },
        "high_ms": {
          "numerator": 9425,
          "denominator": 37
        }
      },
      "below_floor_at_smallest_payload": false,
      "largest_feasible_payload_bytes": 226119487,
      "largest_feasible_payload_bytes_at_minimum_rtt": 226664775,
      "exceeds_recorded_payload_range": true,
      "verdict": "Consistent with the recorded payload range"
    },
    {
      "id": "tts-rot-new-queqiao",
      "generation": "rotating-eight-files",
      "observed_p50_ms": {
        "numerator": 22752,
        "denominator": 5
      },
      "payload_interval_bytes": [
        146000,
        405000
      ],
      "label_supported": false,
      "round_trip_band_ms": [
        199.0,
        207.0
      ],
      "floor_at_smallest_payload": {
        "payload_bytes": 146000,
        "wire_ms": {
          "numerator": 1168,
          "denominator": 333
        },
        "low_ms": {
          "numerator": 77425,
          "denominator": 333
        },
        "high_ms": {
          "numerator": 82753,
          "denominator": 333
        }
      },
      "floor_at_largest_payload": {
        "payload_bytes": 405000,
        "wire_ms": {
          "numerator": 360,
          "denominator": 37
        },
        "low_ms": {
          "numerator": 8833,
          "denominator": 37
        },
        "high_ms": {
          "numerator": 9425,
          "denominator": 37
        }
      },
      "below_floor_at_smallest_payload": false,
      "largest_feasible_payload_bytes": 179878275,
      "largest_feasible_payload_bytes_at_minimum_rtt": 180423562,
      "exceeds_recorded_payload_range": true,
      "verdict": "Consistent with the recorded payload range"
    }
  ],
  "leg_accounts": [
    {
      "id": "asr-rot-new-direct",
      "decomposable": true,
      "legs_ms": {
        "connect": {
          "numerator": 1871,
          "denominator": 10
        },
        "request_to_first_byte": {
          "numerator": 4741,
          "denominator": 5
        }
      },
      "total_ms": {
        "numerator": 2267,
        "denominator": 2
      },
      "summed_legs_ms": {
        "numerator": 11353,
        "denominator": 10
      },
      "residual_ms": {
        "numerator": -9,
        "denominator": 5
      },
      "resolution_bound_ms": {
        "numerator": 3,
        "denominator": 20
      },
      "within_resolution": false,
      "explanation": "Residual exceeds rounding, so these are per-leg medians of different rounds and do not add",
      "stages_covered": [
        "asr_model",
        "llm",
        "tts_model",
        "upload"
      ],
      "stages_uncovered": [
        "capture",
        "encode",
        "download",
        "playback_buffer",
        "playback"
      ]
    },
    {
      "id": "asr-rot-new-queqiao",
      "decomposable": true,
      "legs_ms": {
        "connect": {
          "numerator": 1,
          "denominator": 1
        },
        "request_to_first_byte": {
          "numerator": 2893,
          "denominator": 10
        }
      },
      "total_ms": {
        "numerator": 1451,
        "denominator": 5
      },
      "summed_legs_ms": {
        "numerator": 2903,
        "denominator": 10
      },
      "residual_ms": {
        "numerator": -1,
        "denominator": 10
      },
      "resolution_bound_ms": {
        "numerator": 3,
        "denominator": 20
      },
      "within_resolution": true,
      "explanation": "Residual fits the reported resolution",
      "stages_covered": [
        "asr_model",
        "llm",
        "tts_model",
        "upload"
      ],
      "stages_uncovered": [
        "capture",
        "encode",
        "download",
        "playback_buffer",
        "playback"
      ]
    },
    {
      "id": "asr-rot-held-stock-direct",
      "decomposable": false,
      "reason": "The document reports no total, or no separate legs, for this row"
    },
    {
      "id": "asr-rot-held-stock-queqiao",
      "decomposable": false,
      "reason": "The document reports no total, or no separate legs, for this row"
    },
    {
      "id": "asr-rot-held-tuned-direct",
      "decomposable": false,
      "reason": "The document reports no total, or no separate legs, for this row"
    },
    {
      "id": "asr-rot-held-tuned-queqiao",
      "decomposable": false,
      "reason": "The document reports no total, or no separate legs, for this row"
    },
    {
      "id": "asr-fixed-new-direct",
      "decomposable": false,
      "reason": "The document reports no total, or no separate legs, for this row"
    },
    {
      "id": "asr-fixed-new-queqiao",
      "decomposable": false,
      "reason": "The document reports no total, or no separate legs, for this row"
    },
    {
      "id": "asr-fixed-held-tuned-direct",
      "decomposable": false,
      "reason": "The document reports no total, or no separate legs, for this row"
    },
    {
      "id": "asr-fixed-held-tuned-queqiao",
      "decomposable": false,
      "reason": "The document reports no total, or no separate legs, for this row"
    },
    {
      "id": "tts-rot-new-direct",
      "decomposable": true,
      "legs_ms": {
        "connect": {
          "numerator": 963,
          "denominator": 5
        },
        "request_to_first_byte": {
          "numerator": 44793,
          "denominator": 10
        },
        "download": {
          "numerator": 4581,
          "denominator": 5
        }
      },
      "total_ms": {
        "numerator": 56613,
        "denominator": 10
      },
      "summed_legs_ms": {
        "numerator": 55881,
        "denominator": 10
      },
      "residual_ms": {
        "numerator": 366,
        "denominator": 5
      },
      "resolution_bound_ms": {
        "numerator": 1,
        "denominator": 5
      },
      "within_resolution": false,
      "explanation": "Residual exceeds rounding, so these are per-leg medians of different rounds and do not add",
      "stages_covered": [
        "asr_model",
        "download",
        "llm",
        "tts_model",
        "upload"
      ],
      "stages_uncovered": [
        "capture",
        "encode",
        "playback_buffer",
        "playback"
      ]
    },
    {
      "id": "tts-rot-new-queqiao",
      "decomposable": true,
      "legs_ms": {
        "connect": {
          "numerator": 4,
          "denominator": 5
        },
        "request_to_first_byte": {
          "numerator": 44577,
          "denominator": 10
        },
        "download": {
          "numerator": 749,
          "denominator": 10
        }
      },
      "total_ms": {
        "numerator": 22752,
        "denominator": 5
      },
      "summed_legs_ms": {
        "numerator": 22667,
        "denominator": 5
      },
      "residual_ms": {
        "numerator": 17,
        "denominator": 1
      },
      "resolution_bound_ms": {
        "numerator": 1,
        "denominator": 5
      },
      "within_resolution": false,
      "explanation": "Residual exceeds rounding, so these are per-leg medians of different rounds and do not add",
      "stages_covered": [
        "asr_model",
        "download",
        "llm",
        "tts_model",
        "upload"
      ],
      "stages_uncovered": [
        "capture",
        "encode",
        "playback_buffer",
        "playback"
      ]
    },
    {
      "id": "tts-rot-held-tuned-direct",
      "decomposable": false,
      "reason": "The document reports no total, or no separate legs, for this row"
    },
    {
      "id": "tts-rot-held-tuned-queqiao",
      "decomposable": false,
      "reason": "The document reports no total, or no separate legs, for this row"
    },
    {
      "id": "tts-fixed-new-direct",
      "decomposable": false,
      "reason": "The document reports no total, or no separate legs, for this row"
    },
    {
      "id": "tts-fixed-new-queqiao",
      "decomposable": false,
      "reason": "The document reports no total, or no separate legs, for this row"
    },
    {
      "id": "tts-fixed-held-tuned-direct",
      "decomposable": false,
      "reason": "The document reports no total, or no separate legs, for this row"
    }
  ],
  "frame_runs": [
    {
      "id": "frames-live-udp-direct",
      "carrier": "udp",
      "arm": "direct",
      "sessions": 16,
      "offered": 3200,
      "lost": 163,
      "delivered_recorded": 3037,
      "delivered_derived": 3037,
      "loss_fraction": {
        "numerator": 163,
        "denominator": 3200
      },
      "quantiles": {
        "p50": {
          "value_ms": {
            "numerator": 968,
            "denominator": 5
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 1,
              "denominator": 2
            },
            "sample_count": 3200,
            "order_statistic_rank": 1600,
            "samples_beyond": 1600,
            "supported": true,
            "reason": null
          }
        },
        "p90": {
          "value_ms": {
            "numerator": 1028,
            "denominator": 5
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 9,
              "denominator": 10
            },
            "sample_count": 3200,
            "order_statistic_rank": 2880,
            "samples_beyond": 320,
            "supported": true,
            "reason": null
          }
        },
        "p99": {
          "value_ms": {
            "numerator": 2137,
            "denominator": 10
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 99,
              "denominator": 100
            },
            "sample_count": 3200,
            "order_statistic_rank": 3168,
            "samples_beyond": 32,
            "supported": true,
            "reason": null
          }
        }
      },
      "tail_over_median": {
        "numerator": 2137,
        "denominator": 1936
      },
      "tail_over_median_reason": null,
      "section": "PATH#what-fixes-the-frame-tail-using-the-carrier-voice-actually-uses"
    },
    {
      "id": "frames-live-udp-queqiao",
      "carrier": "udp",
      "arm": "queqiao",
      "sessions": 16,
      "offered": 3200,
      "lost": 34,
      "delivered_recorded": 3166,
      "delivered_derived": 3166,
      "loss_fraction": {
        "numerator": 17,
        "denominator": 1600
      },
      "quantiles": {
        "p50": {
          "value_ms": {
            "numerator": 1041,
            "denominator": 5
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 1,
              "denominator": 2
            },
            "sample_count": 3200,
            "order_statistic_rank": 1600,
            "samples_beyond": 1600,
            "supported": true,
            "reason": null
          }
        },
        "p90": {
          "value_ms": {
            "numerator": 2139,
            "denominator": 10
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 9,
              "denominator": 10
            },
            "sample_count": 3200,
            "order_statistic_rank": 2880,
            "samples_beyond": 320,
            "supported": true,
            "reason": null
          }
        },
        "p99": {
          "value_ms": {
            "numerator": 1088,
            "denominator": 5
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 99,
              "denominator": 100
            },
            "sample_count": 3200,
            "order_statistic_rank": 3168,
            "samples_beyond": 32,
            "supported": true,
            "reason": null
          }
        }
      },
      "tail_over_median": {
        "numerator": 1088,
        "denominator": 1041
      },
      "tail_over_median_reason": null,
      "section": "PATH#what-fixes-the-frame-tail-using-the-carrier-voice-actually-uses"
    },
    {
      "id": "frames-live-tcp-queqiao",
      "carrier": "tcp",
      "arm": "queqiao",
      "sessions": 16,
      "offered": 3200,
      "lost": 0,
      "delivered_recorded": 3200,
      "delivered_derived": 3200,
      "loss_fraction": {
        "numerator": 0,
        "denominator": 1
      },
      "quantiles": {
        "p50": {
          "value_ms": {
            "numerator": 1042,
            "denominator": 5
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 1,
              "denominator": 2
            },
            "sample_count": 3200,
            "order_statistic_rank": 1600,
            "samples_beyond": 1600,
            "supported": true,
            "reason": null
          }
        },
        "p90": {
          "value_ms": {
            "numerator": 214,
            "denominator": 1
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 9,
              "denominator": 10
            },
            "sample_count": 3200,
            "order_statistic_rank": 2880,
            "samples_beyond": 320,
            "supported": true,
            "reason": null
          }
        },
        "p99": {
          "value_ms": {
            "numerator": 3642,
            "denominator": 5
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 99,
              "denominator": 100
            },
            "sample_count": 3200,
            "order_statistic_rank": 3168,
            "samples_beyond": 32,
            "supported": true,
            "reason": null
          }
        }
      },
      "tail_over_median": {
        "numerator": 1821,
        "denominator": 521
      },
      "tail_over_median_reason": null,
      "section": "PATH#what-fixes-the-frame-tail-using-the-carrier-voice-actually-uses"
    },
    {
      "id": "frames-dc-udp-direct",
      "carrier": "udp",
      "arm": "direct",
      "sessions": 8,
      "offered": 1200,
      "lost": 40,
      "delivered_recorded": null,
      "delivered_derived": 1160,
      "loss_fraction": {
        "numerator": 1,
        "denominator": 30
      },
      "quantiles": {
        "p50": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p90": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p99": {
          "value_ms": {
            "numerator": 2101,
            "denominator": 10
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 99,
              "denominator": 100
            },
            "sample_count": 1200,
            "order_statistic_rank": 1188,
            "samples_beyond": 12,
            "supported": true,
            "reason": null
          }
        }
      },
      "tail_over_median": null,
      "tail_over_median_reason": "Needs both p99 and p50; this run reports only one of them",
      "section": "PATH#end-to-end-validation-both-profiles-all-three-carriers"
    },
    {
      "id": "frames-dc-udp-queqiao",
      "carrier": "udp",
      "arm": "queqiao",
      "sessions": 8,
      "offered": 1200,
      "lost": 2,
      "delivered_recorded": null,
      "delivered_derived": 1198,
      "loss_fraction": {
        "numerator": 1,
        "denominator": 600
      },
      "quantiles": {
        "p50": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p90": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p99": {
          "value_ms": {
            "numerator": 427,
            "denominator": 2
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 99,
              "denominator": 100
            },
            "sample_count": 1200,
            "order_statistic_rank": 1188,
            "samples_beyond": 12,
            "supported": true,
            "reason": null
          }
        }
      },
      "tail_over_median": null,
      "tail_over_median_reason": "Needs both p99 and p50; this run reports only one of them",
      "section": "PATH#end-to-end-validation-both-profiles-all-three-carriers"
    },
    {
      "id": "frames-dc-tcp-queqiao",
      "carrier": "tcp",
      "arm": "queqiao",
      "sessions": 8,
      "offered": 1200,
      "lost": 0,
      "delivered_recorded": null,
      "delivered_derived": 1200,
      "loss_fraction": {
        "numerator": 0,
        "denominator": 1
      },
      "quantiles": {
        "p50": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p90": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p99": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p999": {
          "value_ms": {
            "numerator": 7317,
            "denominator": 10
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 999,
              "denominator": 1000
            },
            "sample_count": 1200,
            "order_statistic_rank": 1199,
            "samples_beyond": 1,
            "supported": false,
            "reason": "Only 1 sample(s) lie beyond this quantile; it is decided by that many points"
          }
        }
      },
      "tail_over_median": null,
      "tail_over_median_reason": "Needs both p99 and p50; this run reports only one of them",
      "section": "PATH#end-to-end-validation-both-profiles-all-three-carriers"
    },
    {
      "id": "frames-access-udp-direct",
      "carrier": "udp",
      "arm": "direct",
      "sessions": 8,
      "offered": 1200,
      "lost": 156,
      "delivered_recorded": null,
      "delivered_derived": 1044,
      "loss_fraction": {
        "numerator": 13,
        "denominator": 100
      },
      "quantiles": {
        "p50": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p90": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p99": {
          "value_ms": {
            "numerator": 2121,
            "denominator": 10
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 99,
              "denominator": 100
            },
            "sample_count": 1200,
            "order_statistic_rank": 1188,
            "samples_beyond": 12,
            "supported": true,
            "reason": null
          }
        }
      },
      "tail_over_median": null,
      "tail_over_median_reason": "Needs both p99 and p50; this run reports only one of them",
      "section": "PATH#end-to-end-validation-both-profiles-all-three-carriers"
    },
    {
      "id": "frames-access-udp-queqiao",
      "carrier": "udp",
      "arm": "queqiao",
      "sessions": 8,
      "offered": 1200,
      "lost": 45,
      "delivered_recorded": null,
      "delivered_derived": 1155,
      "loss_fraction": {
        "numerator": 3,
        "denominator": 80
      },
      "quantiles": {
        "p50": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p90": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p99": {
          "value_ms": {
            "numerator": 215,
            "denominator": 1
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 99,
              "denominator": 100
            },
            "sample_count": 1200,
            "order_statistic_rank": 1188,
            "samples_beyond": 12,
            "supported": true,
            "reason": null
          }
        }
      },
      "tail_over_median": null,
      "tail_over_median_reason": "Needs both p99 and p50; this run reports only one of them",
      "section": "PATH#end-to-end-validation-both-profiles-all-three-carriers"
    },
    {
      "id": "frames-access-tcp-queqiao",
      "carrier": "tcp",
      "arm": "queqiao",
      "sessions": 8,
      "offered": 1200,
      "lost": 0,
      "delivered_recorded": null,
      "delivered_derived": 1200,
      "loss_fraction": {
        "numerator": 0,
        "denominator": 1
      },
      "quantiles": {
        "p50": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p90": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p99": {
          "value_ms": {
            "numerator": 5999,
            "denominator": 10
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 99,
              "denominator": 100
            },
            "sample_count": 1200,
            "order_statistic_rank": 1188,
            "samples_beyond": 12,
            "supported": true,
            "reason": null
          }
        }
      },
      "tail_over_median": null,
      "tail_over_median_reason": "Needs both p99 and p50; this run reports only one of them",
      "section": "PATH#end-to-end-validation-both-profiles-all-three-carriers"
    },
    {
      "id": "frames-revalidated-udp-direct",
      "carrier": "udp",
      "arm": "direct",
      "sessions": 8,
      "offered": 1200,
      "lost": 52,
      "delivered_recorded": null,
      "delivered_derived": 1148,
      "loss_fraction": {
        "numerator": 13,
        "denominator": 300
      },
      "quantiles": {
        "p50": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p90": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p99": {
          "value_ms": {
            "numerator": 1062,
            "denominator": 5
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 99,
              "denominator": 100
            },
            "sample_count": 1200,
            "order_statistic_rank": 1188,
            "samples_beyond": 12,
            "supported": true,
            "reason": null
          }
        }
      },
      "tail_over_median": null,
      "tail_over_median_reason": "Needs both p99 and p50; this run reports only one of them",
      "section": "PATH#re-validated-after-the-classification-and-carrier-changes"
    },
    {
      "id": "frames-revalidated-udp-queqiao",
      "carrier": "udp",
      "arm": "queqiao",
      "sessions": 8,
      "offered": 1200,
      "lost": 15,
      "delivered_recorded": null,
      "delivered_derived": 1185,
      "loss_fraction": {
        "numerator": 1,
        "denominator": 80
      },
      "quantiles": {
        "p50": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p90": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p99": {
          "value_ms": {
            "numerator": 1049,
            "denominator": 5
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 99,
              "denominator": 100
            },
            "sample_count": 1200,
            "order_statistic_rank": 1188,
            "samples_beyond": 12,
            "supported": true,
            "reason": null
          }
        }
      },
      "tail_over_median": null,
      "tail_over_median_reason": "Needs both p99 and p50; this run reports only one of them",
      "section": "PATH#re-validated-after-the-classification-and-carrier-changes"
    },
    {
      "id": "frames-revalidated-tcp-queqiao",
      "carrier": "tcp",
      "arm": "queqiao",
      "sessions": 8,
      "offered": 1200,
      "lost": 0,
      "delivered_recorded": null,
      "delivered_derived": 1200,
      "loss_fraction": {
        "numerator": 0,
        "denominator": 1
      },
      "quantiles": {
        "p50": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p90": {
          "value_ms": null,
          "available": false,
          "reason": "The document does not report this quantile for this run"
        },
        "p99": {
          "value_ms": {
            "numerator": 7371,
            "denominator": 10
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 99,
              "denominator": 100
            },
            "sample_count": 1200,
            "order_statistic_rank": 1188,
            "samples_beyond": 12,
            "supported": true,
            "reason": null
          }
        }
      },
      "tail_over_median": null,
      "tail_over_median_reason": "Needs both p99 and p50; this run reports only one of them",
      "section": "PATH#re-validated-after-the-classification-and-carrier-changes"
    },
    {
      "id": "frames-emulated-24-session",
      "carrier": "tcp",
      "arm": "queqiao",
      "sessions": 24,
      "offered": null,
      "lost": null,
      "delivered_recorded": null,
      "delivered_derived": null,
      "loss_fraction": null,
      "quantiles": {
        "p50": {
          "value_ms": {
            "numerator": 2033,
            "denominator": 10
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 1,
              "denominator": 2
            },
            "sample_count": null,
            "supported": null,
            "reason": "The document does not state how many samples this run produced"
          }
        },
        "p90": {
          "value_ms": {
            "numerator": 1041,
            "denominator": 5
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 9,
              "denominator": 10
            },
            "sample_count": null,
            "supported": null,
            "reason": "The document does not state how many samples this run produced"
          }
        },
        "p99": {
          "value_ms": {
            "numerator": 3833,
            "denominator": 5
          },
          "available": true,
          "support": {
            "quantile": {
              "numerator": 99,
              "denominator": 100
            },
            "sample_count": null,
            "supported": null,
            "reason": "The document does not state how many samples this run produced"
          }
        }
      },
      "tail_over_median": {
        "numerator": 7666,
        "denominator": 2033
      },
      "tail_over_median_reason": null,
      "section": "PATH#concurrency-the-two-workload-shapes-disagree"
    }
  ],
  "slow_start_check": {
    "rounds": 5,
    "schedule": [
      {
        "round": 1,
        "window_segments": 10,
        "cumulative_segments": 10
      },
      {
        "round": 2,
        "window_segments": 20,
        "cumulative_segments": 30
      },
      {
        "round": 3,
        "window_segments": 40,
        "cumulative_segments": 70
      },
      {
        "round": 4,
        "window_segments": 80,
        "cumulative_segments": 150
      },
      {
        "round": 5,
        "window_segments": 160,
        "cumulative_segments": 245
      }
    ],
    "predicted_ramp_ms": {
      "numerator": 995,
      "denominator": 1
    },
    "measured_request_to_first_byte_ms": {
      "numerator": 4741,
      "denominator": 5
    },
    "measured_minus_predicted_ms": {
      "numerator": -234,
      "denominator": 5
    },
    "note": "The ramp accounts for the request-to-first-byte leg to within one model service time; it is an arithmetic bound on a doubling window, not a simulation of cubic"
  },
  "playback_supply": {
    "assumed_format": {
      "sample_rate_hz": 16000,
      "channels": 1,
      "sample_bytes": 2,
      "declared_by_document": false
    },
    "consumption_bytes_per_s": 32000,
    "consumption_bits_per_s": 256000,
    "file_bytes": 354640,
    "pcm_bytes": 354596,
    "implied_duration_s": {
      "numerator": 88649,
      "denominator": 8000
    },
    "prebuffer_ms": {
      "numerator": 60,
      "denominator": 1
    },
    "rows": [
      {
        "measurement": "download_direct_cubic_high",
        "supply_bits_per_s": 470000,
        "headroom": {
          "numerator": 235,
          "denominator": 128
        },
        "sufficient_for_playback": true,
        "stall_onset_ms": null,
        "note": null
      },
      {
        "measurement": "download_direct_cubic_low",
        "supply_bits_per_s": 130000,
        "headroom": {
          "numerator": 65,
          "denominator": 128
        },
        "sufficient_for_playback": false,
        "stall_onset_ms": {
          "numerator": 2560,
          "denominator": 21
        },
        "note": "Average supply is under consumption, so the prebuffer only postpones the stall"
      },
      {
        "measurement": "download_direct_high",
        "supply_bits_per_s": 84000000,
        "headroom": {
          "numerator": 2625,
          "denominator": 8
        },
        "sufficient_for_playback": true,
        "stall_onset_ms": null,
        "note": null
      },
      {
        "measurement": "download_direct_low",
        "supply_bits_per_s": 68000000,
        "headroom": {
          "numerator": 2125,
          "denominator": 8
        },
        "sufficient_for_playback": true,
        "stall_onset_ms": null,
        "note": null
      },
      {
        "measurement": "download_queqiao_high",
        "supply_bits_per_s": 268000000,
        "headroom": {
          "numerator": 8375,
          "denominator": 8
        },
        "sufficient_for_playback": true,
        "stall_onset_ms": null,
        "note": null
      },
      {
        "measurement": "download_queqiao_low",
        "supply_bits_per_s": 224000000,
        "headroom": {
          "numerator": 875,
          "denominator": 1
        },
        "sufficient_for_playback": true,
        "stall_onset_ms": null,
        "note": null
      },
      {
        "measurement": "upload_direct_high",
        "supply_bits_per_s": 105800000,
        "headroom": {
          "numerator": 13225,
          "denominator": 32
        },
        "sufficient_for_playback": true,
        "stall_onset_ms": null,
        "note": null
      },
      {
        "measurement": "upload_direct_low",
        "supply_bits_per_s": 3600000,
        "headroom": {
          "numerator": 225,
          "denominator": 16
        },
        "sufficient_for_playback": true,
        "stall_onset_ms": null,
        "note": null
      },
      {
        "measurement": "upload_queqiao_high",
        "supply_bits_per_s": 310400000,
        "headroom": {
          "numerator": 2425,
          "denominator": 2
        },
        "sufficient_for_playback": true,
        "stall_onset_ms": null,
        "note": null
      },
      {
        "measurement": "upload_queqiao_low",
        "supply_bits_per_s": 400000,
        "headroom": {
          "numerator": 25,
          "denominator": 16
        },
        "sufficient_for_playback": true,
        "stall_onset_ms": null,
        "note": null
      }
    ]
  },
  "stages": [
    "capture",
    "encode",
    "upload",
    "asr_model",
    "llm",
    "tts_model",
    "download",
    "playback_buffer",
    "playback"
  ],
  "assumptions": [
    "Every figure is transcribed from the two pinned documents; no run was repeated for this calculation.",
    "Rows are compared only when generation, workload, connection state and kernel setting all match.",
    "The rotating-eight-file generation carries a payload interval, not a size, so no per-size claim rests on it.",
    "Per-leg medians come from different rounds and are not additive; the residual measures that, not a missing stage.",
    "Audio sample rate, channel count and sample width are declared assumptions; the documents state only the byte count.",
    "Capture and playback are outside every recorded leg, so no recorded total is a user-perceived time.",
    "A quantile the documents do not print stays unavailable; none is interpolated from the ones they do print.",
    "Ratios here are ratios of medians; the documents' paired per-round ratios are carried for comparison and cannot be recomputed from these records."
  ]
}
```
