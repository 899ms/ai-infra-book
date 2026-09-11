# 跨地域放置：同一任务、同一质量

All three placements replay one pinned trace: same model revision, same token sequence, same rounds. Quality is fixed by construction, and no placement here is claimed to have been evaluated on its own.

会话状态按官方配置的 K/V 几何计为每 token 147456 字节；请求与回复字节取自轨迹自身的消息体。价格、功率上限与交付期是声明输入。

## 硬约束先于价格

| 地域 | 需求 kW | 功率上限 kW | 交付期 周 | 期限 周 | 可用 | 原因 |
|---|---:|---:|---:|---:|---|---|
| far | 250 | 400 | 30 | 36 | 是 | within the declared power cap and lead time |
| near | 250 | 400 | 4 | 36 | 是 | within the declared power cap and lead time |

| 交付期限 周 | 仍是候选的地域 |
|---:|---|
| 4 | near |
| 12 | near |
| 26 | near |
| 30 | far、near |
| 36 | far、near |
| 52 | far、near |

## 三种放置的字节与费用

| 放置 | 地域 | 入向 B | 出向 B | 矩阵 FLOPs | 计算费 | 出网费 | 驻留费 | 合计 | 可用 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| remote_stateless | far | 66207 | 2527 | 296505803538432 | 0.299682 | 0.000000 | 0.000000 | 0.299682 | 是 |
| remote_warm | far | 10193 | 2527 | 60380764176384 | 0.061028 | 0.000000 | 0.080293 | 0.141320 | 是 |
| local | near | 0 | 0 | 60380764176384 | 0.061028 | 0.000000 | 0.000000 | 0.061028 | 是 |

可用放置按费用排序：near/local < far/remote_warm < far/remote_stateless。

## 每会话等待（往返区间两端）

等待中的计算项是矩阵工作量除以声明速率，是服务时间下界而非时延。同一轨迹的实测模型时间为 13.156 s、实测总耗时 13.803 s，两者不可互相替代。

| 放置 | 往返 ms | 会话等待 s |
|---|---:|---:|
| remote_stateless | 199.0 | 2.689 |
| remote_stateless | 207.0 | 2.785 |
| remote_warm | 199.0 | 2.449 |
| remote_warm | 207.0 | 2.545 |
| local | 199.0 | 0.061 |
| local | 207.0 | 0.061 |

## 盈亏平衡

- 保温时长：可保温 41.0 s（0.01140 h）；Below this hold the warm placement is cheaper; above it the prefill it avoids no longer pays for the memory it occupies。
- 出网价格：不适用；The remote region is not cheaper even before any egress is charged。

## 复用比例扫描

实测缓存命中比例 0.8337。

| 命中比例 | 保温合计 | 无状态合计 | 保温更便宜 |
|---:|---:|---:|---|
| 0.0 | 0.379975 | 0.299682 | 否 |
| 0.1 | 0.352455 | 0.299682 | 否 |
| 0.2 | 0.324609 | 0.299682 | 否 |
| 0.3 | 0.296536 | 0.299682 | 是 |
| 0.4 | 0.268165 | 0.299682 | 是 |
| 0.5 | 0.239524 | 0.299682 | 是 |
| 0.6 | 0.210701 | 0.299682 | 是 |
| 0.7 | 0.181564 | 0.299682 | 是 |
| 0.8 | 0.152216 | 0.299682 | 是 |
| 0.9 | 0.122584 | 0.299682 | 是 |
| 1.0 | 0.092815 | 0.299682 | 是 |

## 口径与限制

- Request and reply bytes are the trace's own message bodies and output text, not token counts times a guess.
- Session state is the official config's K/V geometry times the tokens actually held.
- Prices, power caps and lead times are declared teaching inputs; no operator tariff is claimed.
- Compute time is work divided by a declared rate, a lower bound on service rather than a latency.
- Round-trip delay and link capacity come from the pinned Queqiao path, which is one measured path.
- The power and lead-time gate runs before any price ranking, so a cheap site that cannot carry the demand never ranks.
- Quality is fixed by replaying one identical trace, not by evaluating each placement separately.

## 完整输入、来源与结果

```json
{
  "calculation": "cross-region-placement",
  "inputs": {
    "trace": "thinking-off",
    "model": "qwen3-8b",
    "device_flops_per_second": 989400000000000,
    "link_bits_per_second": 333000000,
    "state_bits": 16,
    "state_hold_hours": null,
    "ingress_price_per_gb": 0.0,
    "required_kw": 250,
    "deadline_weeks": 36
  },
  "sources": [
    {
      "file": "configs/models/qwen3-8b/config.json",
      "url": "https://huggingface.co/Qwen/Qwen3-8B/resolve/b968826d9c46dd6066d109eabc6255188de91218/config.json",
      "revision": "b968826d9c46dd6066d109eabc6255188de91218",
      "sha256": "f7c4eadfbbf522470667b797a3c89be2524832d2d599797248dc304fff447c30"
    },
    {
      "file": "sources/qwen3-8b/model.safetensors.index.json",
      "url": "https://huggingface.co/Qwen/Qwen3-8B/resolve/b968826d9c46dd6066d109eabc6255188de91218/model.safetensors.index.json",
      "revision": "b968826d9c46dd6066d109eabc6255188de91218",
      "sha256": "f9fdbcb91c23971c13ec5d5f2573d2349e8f61f2f049371ec699281748fdb1bc"
    },
    {
      "file": "sources/qwen3/modeling_qwen3.py",
      "url": "https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3/modeling_qwen3.py",
      "revision": "0720e206c6ba28887e4d60ef60a6a089f6c1cc76",
      "sha256": "704c914530530a1acb0b443add1f520404e3ac2c28c0ab7e16f80f86cfe8ccb2"
    },
    {
      "file": "sources/qwen3/modeling_qwen3_moe.py",
      "url": "https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3_moe/modeling_qwen3_moe.py",
      "revision": "0720e206c6ba28887e4d60ef60a6a089f6c1cc76",
      "sha256": "3af43d01f9f902c8009b6dd7d7b8b563561b53dd0aa54175f585ae90d049fdb8"
    },
    {
      "file": "configs/models/qwen3-8b/config.json",
      "url": "https://huggingface.co/Qwen/Qwen3-8B/resolve/b968826d9c46dd6066d109eabc6255188de91218/config.json",
      "revision": "b968826d9c46dd6066d109eabc6255188de91218",
      "sha256": "f7c4eadfbbf522470667b797a3c89be2524832d2d599797248dc304fff447c30"
    },
    {
      "file": "sources/qwen3-8b/model.safetensors.index.json",
      "url": "https://huggingface.co/Qwen/Qwen3-8B/resolve/b968826d9c46dd6066d109eabc6255188de91218/model.safetensors.index.json",
      "revision": "b968826d9c46dd6066d109eabc6255188de91218",
      "sha256": "f9fdbcb91c23971c13ec5d5f2573d2349e8f61f2f049371ec699281748fdb1bc"
    },
    {
      "file": "sources/qwen3/modeling_qwen3.py",
      "url": "https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3/modeling_qwen3.py",
      "revision": "0720e206c6ba28887e4d60ef60a6a089f6c1cc76",
      "sha256": "704c914530530a1acb0b443add1f520404e3ac2c28c0ab7e16f80f86cfe8ccb2"
    },
    {
      "file": "sources/qwen3/modeling_qwen3_moe.py",
      "url": "https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3_moe/modeling_qwen3_moe.py",
      "revision": "0720e206c6ba28887e4d60ef60a6a089f6c1cc76",
      "sha256": "3af43d01f9f902c8009b6dd7d7b8b563561b53dd0aa54175f585ae90d049fdb8"
    },
    {
      "file": "sources/agent-traces/thinking-off/rounds.jsonl",
      "sha256": "2be17dc0b78f5c4e9b913906fd7d610d625801a41965d01a0bd50ddfc7c553dc",
      "origin": "experiments/ch03/03-04/results/rounds.jsonl",
      "url": "../sources/agent-traces/thinking-off/rounds.jsonl"
    },
    {
      "file": "sources/agent-traces/thinking-off/environment.json",
      "sha256": "2fc2dd9cdc95a418fcd9f69b4706dc000c5e5982f20b9d3676d3c6a6a9dc77fa",
      "origin": "experiments/ch03/03-04/results/environment.json",
      "url": "../sources/agent-traces/thinking-off/environment.json"
    },
    {
      "file": "sources/agent-traces/thinking-off/final.json",
      "sha256": "abf5dbfed5c9031a0f6825a2cce7a85b935bf05fb5b87f159c4e1762fa558987",
      "origin": "experiments/ch03/03-04/results/final.json",
      "url": "../sources/agent-traces/thinking-off/final.json"
    },
    {
      "file": "sources/agent-traces/thinking-off/independent-checks-v2.json",
      "sha256": "c647074034f3f434c8ee8f55190f1c7044b34033b9ce0d9d885d172cf5f5935a",
      "origin": "experiments/ch03/03-04/results/independent-checks-v2.json",
      "url": "../sources/agent-traces/thinking-off/independent-checks-v2.json"
    }
  ],
  "quality_contract": "All three placements replay one pinned trace: same model revision, same token sequence, same rounds. Quality is fixed by construction, and no placement here is claimed to have been evaluated on its own.",
  "path": {
    "round_trip_ms_band": [
      199.0,
      207.0
    ],
    "link_bits_per_second": 333000000,
    "provenance": "pinned Queqiao path records"
  },
  "kv_bytes_per_token": 147456,
  "state_hold_hours_used": {
    "numerator": 4600921509321779,
    "denominator": 1200000000000000000
  },
  "measured_summary": {
    "turns": 12,
    "input_tokens": 19556,
    "cached_input_tokens": 16304,
    "uncached_input_tokens": 3252,
    "output_tokens": 765,
    "cached_prefill_matrix_flops": 48184267112448,
    "cold_prefill_matrix_flops": 284309306474496,
    "decode_matrix_flops": 12196497063936,
    "measured_model_seconds": 13.156450202688575,
    "measured_tool_seconds": 0.4764101605396718,
    "measured_other_seconds": 0.16990416473709047,
    "measured_elapsed_seconds": 13.802764527965337,
    "counterfactual_elapsed_seconds": 13.802764527965337,
    "counterfactual_speedup": 1.0,
    "hypothetical_tool_wait_kv_byte_seconds": 120010844.97798157,
    "maximum_round_logical_kv_bytes": 465223680,
    "evaluation_cases": 1013,
    "value_and_input_passed": 315,
    "including_alias_check_passed": 1,
    "actual_cache_peak_bytes": null
  },
  "regions": {
    "near": {
      "compute_price_per_gpu_hour": {
        "numerator": 3600,
        "denominator": 1
      },
      "egress_price_per_gb": {
        "numerator": 0,
        "denominator": 1
      },
      "state_price_per_gb_hour": {
        "numerator": 45,
        "denominator": 1
      },
      "electricity_price_per_kwh": {
        "numerator": 0,
        "denominator": 1
      },
      "cooling_overhead": {
        "numerator": 1,
        "denominator": 1
      },
      "power_cap_kw": 400,
      "lead_time_weeks": 4,
      "role": "beside the user"
    },
    "far": {
      "compute_price_per_gpu_hour": {
        "numerator": 3600,
        "denominator": 1
      },
      "egress_price_per_gb": {
        "numerator": 0,
        "denominator": 1
      },
      "state_price_per_gb_hour": {
        "numerator": 45,
        "denominator": 1
      },
      "electricity_price_per_kwh": {
        "numerator": 0,
        "denominator": 1
      },
      "cooling_overhead": {
        "numerator": 1,
        "denominator": 1
      },
      "power_cap_kw": 400,
      "lead_time_weeks": 30,
      "role": "H100 SXM cloud region across the region boundary"
    }
  },
  "feasibility": [
    {
      "region": "far",
      "role": "H100 SXM cloud region across the region boundary",
      "required_kw": 250,
      "power_cap_kw": 400,
      "lead_time_weeks": 30,
      "deadline_weeks": 36,
      "feasible": true,
      "reasons": [
        "within the declared power cap and lead time"
      ]
    },
    {
      "region": "near",
      "role": "beside the user",
      "required_kw": 250,
      "power_cap_kw": 400,
      "lead_time_weeks": 4,
      "deadline_weeks": 36,
      "feasible": true,
      "reasons": [
        "within the declared power cap and lead time"
      ]
    }
  ],
  "deadline_scan": [
    {
      "deadline_weeks": 4,
      "feasible_regions": [
        "near"
      ]
    },
    {
      "deadline_weeks": 12,
      "feasible_regions": [
        "near"
      ]
    },
    {
      "deadline_weeks": 26,
      "feasible_regions": [
        "near"
      ]
    },
    {
      "deadline_weeks": 30,
      "feasible_regions": [
        "far",
        "near"
      ]
    },
    {
      "deadline_weeks": 36,
      "feasible_regions": [
        "far",
        "near"
      ]
    },
    {
      "deadline_weeks": 52,
      "feasible_regions": [
        "far",
        "near"
      ]
    }
  ],
  "round_ledger": [
    {
      "turn": 0,
      "prompt_tokens": 210,
      "cached_tokens": 0,
      "uncached_tokens": 210,
      "output_tokens": 20,
      "prefix_bytes": 1014,
      "delta_bytes": 1014,
      "reply_bytes": 51,
      "inbound_bytes": {
        "remote_stateless": 1014,
        "remote_warm": 1014,
        "local": 0
      },
      "outbound_bytes": {
        "remote_stateless": 51,
        "remote_warm": 51,
        "local": 0
      },
      "held_state_tokens": 230,
      "held_state_bytes": 33914880,
      "prefill_matrix_flops": {
        "remote_stateless": 2931534528512,
        "remote_warm": 2931534528512,
        "local": 2931534528512
      },
      "decode_matrix_flops": 290053160960,
      "measured_model_seconds": 0.331885325955227
    },
    {
      "turn": 1,
      "prompt_tokens": 316,
      "cached_tokens": 192,
      "uncached_tokens": 124,
      "output_tokens": 20,
      "prefix_bytes": 1448,
      "delta_bytes": 434,
      "reply_bytes": 56,
      "inbound_bytes": {
        "remote_stateless": 1448,
        "remote_warm": 434,
        "local": 0
      },
      "outbound_bytes": {
        "remote_stateless": 56,
        "remote_warm": 56,
        "local": 0
      },
      "held_state_tokens": 336,
      "held_state_bytes": 49545216,
      "prefill_matrix_flops": {
        "remote_stateless": 4420511596544,
        "remote_warm": 1742408646656,
        "local": 1742408646656
      },
      "decode_matrix_flops": 291241066496,
      "measured_model_seconds": 0.31017042184248567
    },
    {
      "turn": 2,
      "prompt_tokens": 670,
      "cached_tokens": 304,
      "uncached_tokens": 366,
      "output_tokens": 125,
      "prefix_bytes": 2556,
      "delta_bytes": 1108,
      "reply_bytes": 428,
      "inbound_bytes": {
        "remote_stateless": 2556,
        "remote_warm": 1108,
        "local": 0
      },
      "outbound_bytes": {
        "remote_stateless": 428,
        "remote_warm": 428,
        "local": 0
      },
      "held_state_tokens": 795,
      "held_state_bytes": 117227520,
      "prefill_matrix_flops": {
        "remote_stateless": 9441156595712,
        "remote_warm": 5190785761280,
        "local": 5190785761280
      },
      "decode_matrix_flops": 1930461839360,
      "measured_model_seconds": 1.9313506009057164
    },
    {
      "turn": 3,
      "prompt_tokens": 884,
      "cached_tokens": 656,
      "uncached_tokens": 228,
      "output_tokens": 20,
      "prefix_bytes": 3201,
      "delta_bytes": 645,
      "reply_bytes": 56,
      "inbound_bytes": {
        "remote_stateless": 3201,
        "remote_warm": 645,
        "local": 0
      },
      "outbound_bytes": {
        "remote_stateless": 56,
        "remote_warm": 56,
        "local": 0
      },
      "held_state_tokens": 904,
      "held_state_bytes": 133300224,
      "prefill_matrix_flops": {
        "remote_stateless": 12512082919424,
        "remote_warm": 3272131346432,
        "local": 3272131346432
      },
      "decode_matrix_flops": 297606447104,
      "measured_model_seconds": 0.3182772099971771
    },
    {
      "turn": 4,
      "prompt_tokens": 1233,
      "cached_tokens": 880,
      "uncached_tokens": 353,
      "output_tokens": 125,
      "prefix_bytes": 4304,
      "delta_bytes": 1103,
      "reply_bytes": 428,
      "inbound_bytes": {
        "remote_stateless": 4304,
        "remote_warm": 1103,
        "local": 0
      },
      "outbound_bytes": {
        "remote_stateless": 428,
        "remote_warm": 428,
        "local": 0
      },
      "held_state_tokens": 1358,
      "held_state_bytes": 200245248,
      "prefill_matrix_flops": {
        "remote_stateless": 17578222223360,
        "remote_warm": 5125032181760,
        "local": 5125032181760
      },
      "decode_matrix_flops": 1971638632448,
      "measured_model_seconds": 1.994325031992048
    },
    {
      "turn": 5,
      "prompt_tokens": 1447,
      "cached_tokens": 1216,
      "uncached_tokens": 231,
      "output_tokens": 20,
      "prefix_bytes": 4949,
      "delta_bytes": 645,
      "reply_bytes": 56,
      "inbound_bytes": {
        "remote_stateless": 4949,
        "remote_warm": 645,
        "local": 0
      },
      "outbound_bytes": {
        "remote_stateless": 56,
        "remote_warm": 56,
        "local": 0
      },
      "held_state_tokens": 1467,
      "held_state_bytes": 216317952,
      "prefill_matrix_flops": {
        "remote_stateless": 20720211722240,
        "remote_warm": 3391673335808,
        "local": 3391673335808
      },
      "decode_matrix_flops": 303915794432,
      "measured_model_seconds": 0.3237843329552561
    },
    {
      "turn": 6,
      "prompt_tokens": 1796,
      "cached_tokens": 1440,
      "uncached_tokens": 356,
      "output_tokens": 125,
      "prefix_bytes": 6052,
      "delta_bytes": 1103,
      "reply_bytes": 428,
      "inbound_bytes": {
        "remote_stateless": 6052,
        "remote_warm": 1103,
        "local": 0
      },
      "outbound_bytes": {
        "remote_stateless": 428,
        "remote_warm": 428,
        "local": 0
      },
      "held_state_tokens": 1921,
      "held_state_bytes": 283262976,
      "prefill_matrix_flops": {
        "remote_stateless": 25902243774464,
        "remote_warm": 5286479396864,
        "local": 5286479396864
      },
      "decode_matrix_flops": 2012815425536,
      "measured_model_seconds": 2.210751400096342
    },
    {
      "turn": 7,
      "prompt_tokens": 2010,
      "cached_tokens": 1792,
      "uncached_tokens": 218,
      "output_tokens": 20,
      "prefix_bytes": 6697,
      "delta_bytes": 645,
      "reply_bytes": 56,
      "inbound_bytes": {
        "remote_stateless": 6697,
        "remote_warm": 645,
        "local": 0
      },
      "outbound_bytes": {
        "remote_stateless": 56,
        "remote_warm": 56,
        "local": 0
      },
      "held_state_tokens": 2030,
      "held_state_bytes": 299335680,
      "prefill_matrix_flops": {
        "remote_stateless": 29115296448512,
        "remote_warm": 3274097229824,
        "local": 3274097229824
      },
      "decode_matrix_flops": 310225141760,
      "measured_model_seconds": 0.3742837270256132
    },
    {
      "turn": 8,
      "prompt_tokens": 2359,
      "cached_tokens": 2000,
      "uncached_tokens": 359,
      "output_tokens": 125,
      "prefix_bytes": 7800,
      "delta_bytes": 1103,
      "reply_bytes": 428,
      "inbound_bytes": {
        "remote_stateless": 7800,
        "remote_warm": 1103,
        "local": 0
      },
      "outbound_bytes": {
        "remote_stateless": 428,
        "remote_warm": 428,
        "local": 0
      },
      "held_state_tokens": 2484,
      "held_state_bytes": 366280704,
      "prefill_matrix_flops": {
        "remote_stateless": 34413221249024,
        "remote_warm": 5449913729024,
        "local": 5449913729024
      },
      "decode_matrix_flops": 2053992218624,
      "measured_model_seconds": 2.3132751691155136
    },
    {
      "turn": 9,
      "prompt_tokens": 2573,
      "cached_tokens": 2352,
      "uncached_tokens": 221,
      "output_tokens": 20,
      "prefix_bytes": 8445,
      "delta_bytes": 645,
      "reply_bytes": 56,
      "inbound_bytes": {
        "remote_stateless": 8445,
        "remote_warm": 645,
        "local": 0
      },
      "outbound_bytes": {
        "remote_stateless": 56,
        "remote_warm": 56,
        "local": 0
      },
      "held_state_tokens": 2593,
      "held_state_bytes": 382353408,
      "prefill_matrix_flops": {
        "remote_stateless": 37697337098240,
        "remote_warm": 3392328630272,
        "local": 3392328630272
      },
      "decode_matrix_flops": 316534489088,
      "measured_model_seconds": 0.38091888604685664
    },
    {
      "turn": 10,
      "prompt_tokens": 2922,
      "cached_tokens": 2560,
      "uncached_tokens": 362,
      "output_tokens": 125,
      "prefix_bytes": 9548,
      "delta_bytes": 1103,
      "reply_bytes": 428,
      "inbound_bytes": {
        "remote_stateless": 9548,
        "remote_warm": 1103,
        "local": 0
      },
      "outbound_bytes": {
        "remote_stateless": 428,
        "remote_warm": 428,
        "local": 0
      },
      "held_state_tokens": 3047,
      "held_state_bytes": 449298432,
      "prefill_matrix_flops": {
        "remote_stateless": 43111154647040,
        "remote_warm": 5615335178240,
        "local": 5615335178240
      },
      "decode_matrix_flops": 2095169011712,
      "measured_model_seconds": 2.33632974489592
    },
    {
      "turn": 11,
      "prompt_tokens": 3136,
      "cached_tokens": 2912,
      "uncached_tokens": 224,
      "output_tokens": 20,
      "prefix_bytes": 10193,
      "delta_bytes": 645,
      "reply_bytes": 56,
      "inbound_bytes": {
        "remote_stateless": 10193,
        "remote_warm": 645,
        "local": 0
      },
      "outbound_bytes": {
        "remote_stateless": 56,
        "remote_warm": 56,
        "local": 0
      },
      "held_state_tokens": 3156,
      "held_state_bytes": 465371136,
      "prefill_matrix_flops": {
        "remote_stateless": 46466333671424,
        "remote_warm": 3512547147776,
        "local": 3512547147776
      },
      "decode_matrix_flops": 322843836416,
      "measured_model_seconds": 0.3310983518604189
    }
  ],
  "session_costs": [
    {
      "placement": "remote_stateless",
      "inbound_bytes": 66207,
      "outbound_bytes": 2527,
      "matrix_flops": 296505803538432,
      "compute_seconds_lower_bound": {
        "numerator": 24129704064,
        "denominator": 80517578125
      },
      "compute_cost": {
        "numerator": 24129704064,
        "denominator": 80517578125
      },
      "egress_cost": {
        "numerator": 0,
        "denominator": 1
      },
      "ingress_cost": {
        "numerator": 0,
        "denominator": 1
      },
      "resident_state_bytes": 0,
      "state_hold_hours": {
        "numerator": 0,
        "denominator": 1
      },
      "state_cost": {
        "numerator": 0,
        "denominator": 1
      },
      "total_cost": {
        "numerator": 24129704064,
        "denominator": 80517578125
      },
      "region": "far",
      "feasible": true
    },
    {
      "placement": "remote_warm",
      "inbound_bytes": 10193,
      "outbound_bytes": 2527,
      "matrix_flops": 60380764176384,
      "compute_seconds_lower_bound": {
        "numerator": 4913799168,
        "denominator": 80517578125
      },
      "compute_cost": {
        "numerator": 4913799168,
        "denominator": 80517578125
      },
      "egress_cost": {
        "numerator": 0,
        "denominator": 1
      },
      "ingress_cost": {
        "numerator": 0,
        "denominator": 1
      },
      "resident_state_bytes": 465371136,
      "state_hold_hours": {
        "numerator": 4600921509321779,
        "denominator": 1200000000000000000
      },
      "state_cost": {
        "numerator": 98013430913081858037,
        "denominator": 1220703125000000000000
      },
      "total_cost": {
        "numerator": 284469126775671983903013,
        "denominator": 2012939453125000000000000
      },
      "region": "far",
      "feasible": true
    },
    {
      "placement": "local",
      "inbound_bytes": 0,
      "outbound_bytes": 0,
      "matrix_flops": 60380764176384,
      "compute_seconds_lower_bound": {
        "numerator": 4913799168,
        "denominator": 80517578125
      },
      "compute_cost": {
        "numerator": 4913799168,
        "denominator": 80517578125
      },
      "egress_cost": {
        "numerator": 0,
        "denominator": 1
      },
      "ingress_cost": {
        "numerator": 0,
        "denominator": 1
      },
      "resident_state_bytes": 0,
      "state_hold_hours": {
        "numerator": 0,
        "denominator": 1
      },
      "state_cost": {
        "numerator": 0,
        "denominator": 1
      },
      "total_cost": {
        "numerator": 4913799168,
        "denominator": 80517578125
      },
      "region": "near",
      "feasible": true
    }
  ],
  "session_waits": [
    {
      "region": "far",
      "placement": "remote_stateless",
      "round_trip_bound": "low",
      "round_trip_ms": 199.0,
      "session_wait_seconds": {
        "numerator": 288429464041373,
        "denominator": 107249414062500
      }
    },
    {
      "region": "far",
      "placement": "remote_stateless",
      "round_trip_bound": "high",
      "round_trip_ms": 207.0,
      "session_wait_seconds": {
        "numerator": 298725407791373,
        "denominator": 107249414062500
      }
    },
    {
      "region": "far",
      "placement": "remote_warm",
      "round_trip_bound": "low",
      "round_trip_ms": 199.0,
      "session_wait_seconds": {
        "numerator": 43781592524671,
        "denominator": 17874902343750
      }
    },
    {
      "region": "far",
      "placement": "remote_warm",
      "round_trip_bound": "high",
      "round_trip_ms": 207.0,
      "session_wait_seconds": {
        "numerator": 45497583149671,
        "denominator": 17874902343750
      }
    },
    {
      "region": "near",
      "placement": "local",
      "round_trip_bound": "low",
      "round_trip_ms": 199.0,
      "session_wait_seconds": {
        "numerator": 4913799168,
        "denominator": 80517578125
      }
    },
    {
      "region": "near",
      "placement": "local",
      "round_trip_bound": "high",
      "round_trip_ms": 207.0,
      "session_wait_seconds": {
        "numerator": 4913799168,
        "denominator": 80517578125
      }
    }
  ],
  "ranked_feasible": [
    "near/local",
    "far/remote_warm",
    "far/remote_stateless"
  ],
  "excluded_by_hard_constraints": [],
  "hold_boundary": {
    "hold_hours": {
      "numerator": 16680473,
      "denominator": 1463693625
    },
    "hold_seconds": {
      "numerator": 266887568,
      "denominator": 6505305
    },
    "saving_at_zero_hold": {
      "numerator": 19215904896,
      "denominator": 80517578125
    },
    "residency_cost_per_hour": {
      "numerator": 8180352,
      "denominator": 390625
    },
    "resident_state_bytes": 465371136,
    "reason": "Below this hold the warm placement is cheaper; above it the prefill it avoids no longer pays for the memory it occupies"
  },
  "egress_price_boundary": {
    "price_per_gb": null,
    "reason": "The remote region is not cheaper even before any egress is charged"
  },
  "reuse_scan": {
    "measured_cache_hit_fraction": {
      "numerator": 4076,
      "denominator": 4889
    },
    "scan": [
      {
        "cache_hit_fraction": {
          "numerator": 0,
          "denominator": 1
        },
        "warm_total_cost": {
          "numerator": 764866749175671983903013,
          "denominator": 2012939453125000000000000
        },
        "stateless_total_cost": {
          "numerator": 24129704064,
          "denominator": 80517578125
        },
        "warm_is_cheaper": false
      },
      {
        "cache_hit_fraction": {
          "numerator": 1,
          "denominator": 10
        },
        "warm_total_cost": {
          "numerator": 709469766775671983903013,
          "denominator": 2012939453125000000000000
        },
        "stateless_total_cost": {
          "numerator": 24129704064,
          "denominator": 80517578125
        },
        "warm_is_cheaper": false
      },
      {
        "cache_hit_fraction": {
          "numerator": 1,
          "denominator": 5
        },
        "warm_total_cost": {
          "numerator": 653417562775671983903013,
          "denominator": 2012939453125000000000000
        },
        "stateless_total_cost": {
          "numerator": 24129704064,
          "denominator": 80517578125
        },
        "warm_is_cheaper": false
      },
      {
        "cache_hit_fraction": {
          "numerator": 3,
          "denominator": 10
        },
        "warm_total_cost": {
          "numerator": 596909545975671983903013,
          "denominator": 2012939453125000000000000
        },
        "stateless_total_cost": {
          "numerator": 24129704064,
          "denominator": 80517578125
        },
        "warm_is_cheaper": true
      },
      {
        "cache_hit_fraction": {
          "numerator": 2,
          "denominator": 5
        },
        "warm_total_cost": {
          "numerator": 539800654375671983903013,
          "denominator": 2012939453125000000000000
        },
        "stateless_total_cost": {
          "numerator": 24129704064,
          "denominator": 80517578125
        },
        "warm_is_cheaper": true
      },
      {
        "cache_hit_fraction": {
          "numerator": 1,
          "denominator": 2
        },
        "warm_total_cost": {
          "numerator": 482148156775671983903013,
          "denominator": 2012939453125000000000000
        },
        "stateless_total_cost": {
          "numerator": 24129704064,
          "denominator": 80517578125
        },
        "warm_is_cheaper": true
      },
      {
        "cache_hit_fraction": {
          "numerator": 3,
          "denominator": 5
        },
        "warm_total_cost": {
          "numerator": 424128669175671983903013,
          "denominator": 2012939453125000000000000
        },
        "stateless_total_cost": {
          "numerator": 24129704064,
          "denominator": 80517578125
        },
        "warm_is_cheaper": true
      },
      {
        "cache_hit_fraction": {
          "numerator": 7,
          "denominator": 10
        },
        "warm_total_cost": {
          "numerator": 365477092375671983903013,
          "denominator": 2012939453125000000000000
        },
        "stateless_total_cost": {
          "numerator": 24129704064,
          "denominator": 80517578125
        },
        "warm_is_cheaper": true
      },
      {
        "cache_hit_fraction": {
          "numerator": 4,
          "denominator": 5
        },
        "warm_total_cost": {
          "numerator": 306402282775671983903013,
          "denominator": 2012939453125000000000000
        },
        "stateless_total_cost": {
          "numerator": 24129704064,
          "denominator": 80517578125
        },
        "warm_is_cheaper": true
      },
      {
        "cache_hit_fraction": {
          "numerator": 9,
          "denominator": 10
        },
        "warm_total_cost": {
          "numerator": 246753373975671983903013,
          "denominator": 2012939453125000000000000
        },
        "stateless_total_cost": {
          "numerator": 24129704064,
          "denominator": 80517578125
        },
        "warm_is_cheaper": true
      },
      {
        "cache_hit_fraction": {
          "numerator": 1,
          "denominator": 1
        },
        "warm_total_cost": {
          "numerator": 186830987575671983903013,
          "denominator": 2012939453125000000000000
        },
        "stateless_total_cost": {
          "numerator": 24129704064,
          "denominator": 80517578125
        },
        "warm_is_cheaper": true
      }
    ],
    "ordering_changes_between": [
      {
        "cache_hit_fraction": {
          "numerator": 3,
          "denominator": 10
        },
        "warm_total_cost": {
          "numerator": 596909545975671983903013,
          "denominator": 2012939453125000000000000
        },
        "stateless_total_cost": {
          "numerator": 24129704064,
          "denominator": 80517578125
        },
        "warm_is_cheaper": true
      }
    ],
    "note": "Only the prefill a warm cache avoids pays for holding the state, so the scan says how much reuse the hold needs; the prefix payload is scaled from the trace's real bytes, not re-measured"
  },
  "assumptions": [
    "Request and reply bytes are the trace's own message bodies and output text, not token counts times a guess.",
    "Session state is the official config's K/V geometry times the tokens actually held.",
    "Prices, power caps and lead times are declared teaching inputs; no operator tariff is claimed.",
    "Compute time is work divided by a declared rate, a lower bound on service rather than a latency.",
    "Round-trip delay and link capacity come from the pinned Queqiao path, which is one measured path.",
    "The power and lead-time gate runs before any price ranking, so a cheap site that cannot carry the demand never ranks.",
    "Quality is fixed by replaying one identical trace, not by evaluating each placement separately."
  ]
}
```
