# 权重驻留之后还剩什么要搬

模型几何与字节量由固定官方配置重建；片上容量、跳延迟、每 stack 带宽、存储密度与 lane 速率是声明输入。本设计没有流片，下面没有任何一项是实测速率。

## 驻留拆分

- 完整 checkpoint：16381470720 B；一步活跃权重读取：15136811008 B。
- 每历史 token 的 KV：147456 B；上下文 32768 时每序列每步读取 4831838208 B。
- 权重／KV 交叉点 batch：3.1327，即从 batch 4 起 KV 读取超过权重读取。
- 权重移出该接口后，仅此内存服务的理想加速比：4.133（batch=1）。
- The speedup covers this memory service only. Arithmetic, immutable-store service, communication and scheduling still have to be timed.

## 供给倒推

- 维持 10000 tok/s 仅 KV 读就需 48318382080000 B/s，按每 stack 1200000000000 B/s 至少 41 个 stack。
- 按密度 3009000 B/mm²，仅该状态需约 1605.8 mm²。
- 15134641792 次运算在理想条件下需 75674 条 lane；只留 0.40 预算、利用率 0.60 时需 315306 条。
- Every figure here is a lower bound on supply for one term. They do not add up to a feasible design, and none of them is a measurement.

## 激活扇出／扇入与跳数

| 切分 | 每层 tile 数 | 网格边长 | 直径跳 | 每层扇出 B | 每层扇入 B | 归约轮 | 每 token 总跳 | 每 token 关键路径跳 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| column | 6 | 3 | 4 | 49152 | 8192 | 0 | 360 | 288 |
| row | 6 | 3 | 4 | 8192 | 49152 | 3 | 360 | 288 |

选定切分 column；Hop counts are a topology lower bound: a spanning tree cannot use fewer edges and a diameter cannot be crossed in fewer hops. Serialisation, reduction arithmetic, contention and tail delay are not included.

## 同步跨度

- 36 层 × 每层 2 次集合通信 = 72 次；token 预算 0.000100 s 的 0.30 分给通信，每次可用 0.000000417 s。
- 直径传播每次 0.000000400 s，每 token 合计 0.000029 s。
- 单次预算内：是；token 预算内：是，超出倍数 0.29。
- Propagation alone. A design that already fails here cannot be rescued by scheduling; the fabric, the number of events, the partition or the target has to change.

预算允许的最大直径：单次预算 4 跳，整 token 预算 13 跳。超过后仅传播就不成立。

| 直径跳 | 每 token 传播 s | 单次预算内 | token 预算内 | 超出倍数 |
|---:|---:|---|---|---:|
| 4 | 0.00002880 | 是 | 是 | 0.288 |
| 13 | 0.00009360 | 否 | 是 | 0.936 |
| 14 | 0.00010080 | 否 | 否 | 1.008 |
| 15 | 0.00010800 | 否 | 否 | 1.080 |

## 明确未计入的约束

- KV writes, re-reads and allocator overhead are outside the read-side account.
- Immutable-store service time is not modelled; only its absence from the memory interface is.
- Hop counts carry no serialisation, reduction arithmetic, contention or tail delay.
- Lane counts leave out operand supply, accumulation, clocking, routing and timing closure.
- Area covers the named term only, with nothing reserved for weights, arithmetic or interconnect.
- Sparse attention needs resident state, per-step access and index scan counted separately.
- No figure here is measured: this design has no silicon, and its rates are not achieved rates.

## 口径与限制

- Weight, state and activation bytes are rebuilt from the pinned official config.
- Tile capacity, hop latency, per-stack bandwidth, storage density and lane rate are declared teaching inputs.
- Hop and lane figures are topology and arithmetic lower bounds, not schedules.
- The memory-service speedup covers one interface, never a whole machine.
- This design has no silicon; no rate here is presented as achieved.

## 完整输入、来源与结果

```json
{
  "calculation": "weight-resident-remaining-traffic",
  "inputs": {
    "model": "qwen3-8b",
    "context": 32768,
    "batch": 1,
    "tokens_per_second": 10000,
    "stack_bytes_per_second": 1200000000000,
    "density_bytes_per_mm2": 3009000,
    "tensor_operations": 15134641792,
    "token_budget_seconds": "0.0001",
    "arithmetic_budget_share": "0.4",
    "lane_utilisation": "0.6",
    "lane_operations_per_second": 2000000000,
    "tile_bytes": 67108864,
    "sharding": "column",
    "hop_latency_seconds": "1e-7",
    "collectives_per_layer": 2,
    "communication_share": "0.3",
    "diameter_hops": null
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
    }
  ],
  "geometry": {
    "hidden_size": 4096,
    "intermediate_size": 12288,
    "num_hidden_layers": 36,
    "num_attention_heads": 32,
    "num_key_value_heads": 8,
    "head_dim": 128,
    "vocab_size": 151936,
    "params_per_layer": 192946432,
    "params_embedding": 622329856,
    "params_checkpoint": 8190735360,
    "params_active_decode": 7568405504,
    "checkpoint_bytes": 16381470720,
    "active_decode_read_bytes": 15136811008,
    "layer_bytes": 385892864,
    "kv_bytes_per_token": 147456,
    "activation_bytes": 8192
  },
  "residency_split": {
    "context": 32768,
    "batch": 1,
    "kv_bytes_per_token": 147456,
    "kv_read_bytes_per_sequence_step": 4831838208,
    "active_weight_read_bytes": 15136811008,
    "step_bytes_with_resident_weights": 19968649216,
    "step_bytes_without_weight_reads": 4831838208,
    "crossover_batch_exact": {
      "numerator": 7391021,
      "denominator": 2359296
    },
    "crossover_batch_first_integer": 4,
    "memory_service_speedup": {
      "numerator": 9750317,
      "denominator": 2359296
    },
    "note": "The speedup covers this memory service only. Arithmetic, immutable-store service, communication and scheduling still have to be timed."
  },
  "supply_backsolve": {
    "tokens_per_second": 10000,
    "kv_read_bandwidth_bytes_per_second": 48318382080000,
    "stack_bytes_per_second": 1200000000000,
    "stacks_required": 41,
    "session_state_area_mm2": {
      "numerator": 201326592,
      "denominator": 125375
    },
    "density_bytes_per_mm2": 3009000,
    "tensor_operations": 15134641792,
    "ideal_lanes": 75674,
    "derated_lanes": 315306,
    "derating": {
      "arithmetic_budget_share": {
        "numerator": 2,
        "denominator": 5
      },
      "lane_utilisation": {
        "numerator": 3,
        "denominator": 5
      }
    },
    "note": "Every figure here is a lower bound on supply for one term. They do not add up to a feasible design, and none of them is a measurement."
  },
  "fan_traffic": {
    "column": {
      "sharding": "column",
      "tile_bytes": 67108864,
      "layer_bytes": 385892864,
      "tiles_per_layer": 6,
      "mesh_side": 3,
      "mesh_diameter_hops": 4,
      "activation_bytes": 8192,
      "fan_out_bytes_per_layer": 49152,
      "fan_in_bytes_per_layer": 8192,
      "reduction_rounds_per_layer": 0,
      "spanning_tree_hops_per_collective": 5,
      "total_hops_per_token": 360,
      "critical_path_hops_per_token": 288,
      "propagation_lower_bound_seconds": {
        "numerator": 9,
        "denominator": 312500
      },
      "note": "Hop counts are a topology lower bound: a spanning tree cannot use fewer edges and a diameter cannot be crossed in fewer hops. Serialisation, reduction arithmetic, contention and tail delay are not included."
    },
    "row": {
      "sharding": "row",
      "tile_bytes": 67108864,
      "layer_bytes": 385892864,
      "tiles_per_layer": 6,
      "mesh_side": 3,
      "mesh_diameter_hops": 4,
      "activation_bytes": 8192,
      "fan_out_bytes_per_layer": 8192,
      "fan_in_bytes_per_layer": 49152,
      "reduction_rounds_per_layer": 3,
      "spanning_tree_hops_per_collective": 5,
      "total_hops_per_token": 360,
      "critical_path_hops_per_token": 288,
      "propagation_lower_bound_seconds": {
        "numerator": 9,
        "denominator": 312500
      },
      "note": "Hop counts are a topology lower bound: a spanning tree cannot use fewer edges and a diameter cannot be crossed in fewer hops. Serialisation, reduction arithmetic, contention and tail delay are not included."
    }
  },
  "selected_sharding": "column",
  "diameter_hops_used": 4,
  "diameter_hops_derived_from_mesh": 4,
  "synchronisation_span": {
    "layers": 36,
    "collectives_per_layer": 2,
    "collective_events_per_token": 72,
    "largest_diameter_within_per_collective_budget": 4,
    "largest_diameter_within_token_budget": 13,
    "token_budget_seconds": {
      "numerator": 1,
      "denominator": 10000
    },
    "communication_share": {
      "numerator": 3,
      "denominator": 10
    },
    "budget_per_collective_seconds": {
      "numerator": 1,
      "denominator": 2400000
    },
    "propagation_per_collective_seconds": {
      "numerator": 1,
      "denominator": 2500000
    },
    "propagation_per_token_seconds": {
      "numerator": 9,
      "denominator": 312500
    },
    "fits_per_collective_budget": true,
    "fits_token_budget": true,
    "overrun_factor_against_token_budget": {
      "numerator": 36,
      "denominator": 125
    },
    "note": "Propagation alone. A design that already fails here cannot be rescued by scheduling; the fabric, the number of events, the partition or the target has to change."
  },
  "diameter_scan": [
    {
      "diameter_hops": 4,
      "propagation_per_token_seconds": {
        "numerator": 9,
        "denominator": 312500
      },
      "fits_per_collective_budget": true,
      "fits_token_budget": true,
      "overrun_factor_against_token_budget": {
        "numerator": 36,
        "denominator": 125
      }
    },
    {
      "diameter_hops": 13,
      "propagation_per_token_seconds": {
        "numerator": 117,
        "denominator": 1250000
      },
      "fits_per_collective_budget": false,
      "fits_token_budget": true,
      "overrun_factor_against_token_budget": {
        "numerator": 117,
        "denominator": 125
      }
    },
    {
      "diameter_hops": 14,
      "propagation_per_token_seconds": {
        "numerator": 63,
        "denominator": 625000
      },
      "fits_per_collective_budget": false,
      "fits_token_budget": false,
      "overrun_factor_against_token_budget": {
        "numerator": 126,
        "denominator": 125
      }
    },
    {
      "diameter_hops": 15,
      "propagation_per_token_seconds": {
        "numerator": 27,
        "denominator": 250000
      },
      "fits_per_collective_budget": false,
      "fits_token_budget": false,
      "overrun_factor_against_token_budget": {
        "numerator": 27,
        "denominator": 25
      }
    }
  ],
  "omitted_constraints": [
    "KV writes, re-reads and allocator overhead are outside the read-side account.",
    "Immutable-store service time is not modelled; only its absence from the memory interface is.",
    "Hop counts carry no serialisation, reduction arithmetic, contention or tail delay.",
    "Lane counts leave out operand supply, accumulation, clocking, routing and timing closure.",
    "Area covers the named term only, with nothing reserved for weights, arithmetic or interconnect.",
    "Sparse attention needs resident state, per-step access and index scan counted separately.",
    "No figure here is measured: this design has no silicon, and its rates are not achieved rates."
  ],
  "assumptions": [
    "Weight, state and activation bytes are rebuilt from the pinned official config.",
    "Tile capacity, hop latency, per-stack bandwidth, storage density and lane rate are declared teaching inputs.",
    "Hop and lane figures are topology and arithmetic lower bounds, not schedules.",
    "The memory-service speedup covers one interface, never a whole machine.",
    "This design has no silicon; no rate here is presented as achieved."
  ]
}
```
