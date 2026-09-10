# 专用化的固定费用能否被节省付清

回本 token 数 = 固定费用 ÷ 每 token 节省 = 4e+13 token。下列金额全部是教学假设，不是供应商价格或项目预测。

## 四种情形

| 情形 | 服务期 s | 机器 | 有效速率 tok/s | 需要 token | 交付 token | 覆盖率 | 回本 | 需要机器数 |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| planned | 31536000 | 100 | 10000 | 4e+13 | 1.577e+13 | 0.394 | 否 | 254 |
| life_halves | 15768000 | 100 | 10000 | 4e+13 | 7.884e+12 | 0.197 | 否 | 508 |
| delivery_slips | 15811200 | 100 | 10000 | 4e+13 | 7.906e+12 | 0.198 | 否 | 506 |
| output_rate_falls | 31536000 | 100 | 6000 | 4e+13 | 9.461e+12 | 0.237 | 否 | 423 |

## 整站费用与净节省

电费按设施计量，散热系数只乘电费，不乘网络与备份。

| 情形 | 设施功率 kW | 电费 | 网络 | 备份 | 站点合计 | 站点每百万 token | 净节省每百万 token | 扣除后回本 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| planned | 1300.0 | 911,040 | 250,000 | 150,000 | 1,311,040 | 0.0831 | 0.4169 | 否 |
| life_halves | 1300.0 | 455,520 | 125,000 | 75,000 | 655,520 | 0.0831 | 0.4169 | 否 |
| delivery_slips | 1300.0 | 456,768 | 125,342 | 75,205 | 657,316 | 0.0831 | 0.4169 | 否 |
| output_rate_falls | 1300.0 | 911,040 | 250,000 | 150,000 | 1,311,040 | 0.1386 | 0.3614 | 否 |

能够回本的情形：无。
机器数只是产出折算，还需要真实需求把它消化掉。

## 口径与限制

- Every amount is a declared teaching input, not a vendor price or a project estimate.
- The fixed cost is incremental, so the per-token saving must not already amortise it.
- Machine count is an output conversion; the demand to fill those machines is a separate condition.
- Delivery time is taken out of the economic life rather than added to it.
- The cooling overhead multiplies metered electricity only, not the network or backup lines.
- Site cost is charged against delivered tokens, so a saving quoted before it is not the saving that repays anything.
- Maintenance, spare capacity, downtime and model-quality change are outside this account.
- Changing the machine count may change unit price or utilisation, which would require repricing.

## 完整输入与结果

```json
{
  "calculation": "specialisation-payback",
  "inputs": {
    "fixed_cost": "20000000",
    "saving_per_million_tokens": "0.50",
    "machines": 100,
    "tokens_per_second": 10000,
    "utilisation": "0.5",
    "economic_life_months": 12,
    "delivery_weeks": 0,
    "shortened_life_months": 6,
    "delayed_delivery_weeks": 26,
    "degraded_output_tokens_per_second": 6000,
    "machine_power_kw": "10",
    "cooling_overhead": "1.3",
    "electricity_price_per_kwh": "0.08",
    "network_cost_per_year": "250000",
    "backup_cost_per_year": "150000",
    "include_site": true
  },
  "payback_volume_tokens": {
    "numerator": 40000000000000,
    "denominator": 1
  },
  "scenarios": [
    {
      "scenario": "planned",
      "life_seconds": {
        "numerator": 31536000,
        "denominator": 1
      },
      "delivery_seconds": {
        "numerator": 0,
        "denominator": 1
      },
      "serving_seconds": {
        "numerator": 31536000,
        "denominator": 1
      },
      "machines": 100,
      "tokens_per_second": 10000,
      "utilisation": {
        "numerator": 1,
        "denominator": 2
      },
      "required_tokens": {
        "numerator": 40000000000000,
        "denominator": 1
      },
      "delivered_tokens": {
        "numerator": 15768000000000,
        "denominator": 1
      },
      "coverage": {
        "numerator": 1971,
        "denominator": 5000
      },
      "pays_back": false,
      "machines_required": 254,
      "machine_shortfall": 154,
      "reason": "This life needs 254 machines of the same output, and the demand to fill them",
      "site": {
        "machines": 100,
        "machine_power_kw": {
          "numerator": 10,
          "denominator": 1
        },
        "cooling_overhead": {
          "numerator": 13,
          "denominator": 10
        },
        "facility_power_kw": {
          "numerator": 1300,
          "denominator": 1
        },
        "energy_kwh": {
          "numerator": 11388000,
          "denominator": 1
        },
        "electricity_cost": {
          "numerator": 911040,
          "denominator": 1
        },
        "network_cost": {
          "numerator": 250000,
          "denominator": 1
        },
        "backup_cost": {
          "numerator": 150000,
          "denominator": 1
        },
        "total_site_cost": {
          "numerator": 1311040,
          "denominator": 1
        },
        "note": "Electricity is metered at the facility, so the cooling overhead applies to it and not to the network or backup lines."
      },
      "site_cost_per_million_tokens": {
        "numerator": 4097,
        "denominator": 49275
      },
      "net_saving_per_million_tokens": {
        "numerator": 41081,
        "denominator": 98550
      },
      "saving_survives_site_cost": true,
      "required_tokens_net_of_site": {
        "numerator": 1971000000000000000,
        "denominator": 41081
      },
      "pays_back_net_of_site": false
    },
    {
      "scenario": "life_halves",
      "life_seconds": {
        "numerator": 15768000,
        "denominator": 1
      },
      "delivery_seconds": {
        "numerator": 0,
        "denominator": 1
      },
      "serving_seconds": {
        "numerator": 15768000,
        "denominator": 1
      },
      "machines": 100,
      "tokens_per_second": 10000,
      "utilisation": {
        "numerator": 1,
        "denominator": 2
      },
      "required_tokens": {
        "numerator": 40000000000000,
        "denominator": 1
      },
      "delivered_tokens": {
        "numerator": 7884000000000,
        "denominator": 1
      },
      "coverage": {
        "numerator": 1971,
        "denominator": 10000
      },
      "pays_back": false,
      "machines_required": 508,
      "machine_shortfall": 408,
      "reason": "This life needs 508 machines of the same output, and the demand to fill them",
      "site": {
        "machines": 100,
        "machine_power_kw": {
          "numerator": 10,
          "denominator": 1
        },
        "cooling_overhead": {
          "numerator": 13,
          "denominator": 10
        },
        "facility_power_kw": {
          "numerator": 1300,
          "denominator": 1
        },
        "energy_kwh": {
          "numerator": 5694000,
          "denominator": 1
        },
        "electricity_cost": {
          "numerator": 455520,
          "denominator": 1
        },
        "network_cost": {
          "numerator": 125000,
          "denominator": 1
        },
        "backup_cost": {
          "numerator": 75000,
          "denominator": 1
        },
        "total_site_cost": {
          "numerator": 655520,
          "denominator": 1
        },
        "note": "Electricity is metered at the facility, so the cooling overhead applies to it and not to the network or backup lines."
      },
      "site_cost_per_million_tokens": {
        "numerator": 4097,
        "denominator": 49275
      },
      "net_saving_per_million_tokens": {
        "numerator": 41081,
        "denominator": 98550
      },
      "saving_survives_site_cost": true,
      "required_tokens_net_of_site": {
        "numerator": 1971000000000000000,
        "denominator": 41081
      },
      "pays_back_net_of_site": false
    },
    {
      "scenario": "delivery_slips",
      "life_seconds": {
        "numerator": 31536000,
        "denominator": 1
      },
      "delivery_seconds": {
        "numerator": 15724800,
        "denominator": 1
      },
      "serving_seconds": {
        "numerator": 15811200,
        "denominator": 1
      },
      "machines": 100,
      "tokens_per_second": 10000,
      "utilisation": {
        "numerator": 1,
        "denominator": 2
      },
      "required_tokens": {
        "numerator": 40000000000000,
        "denominator": 1
      },
      "delivered_tokens": {
        "numerator": 7905600000000,
        "denominator": 1
      },
      "coverage": {
        "numerator": 4941,
        "denominator": 25000
      },
      "pays_back": false,
      "machines_required": 506,
      "machine_shortfall": 406,
      "reason": "This life needs 506 machines of the same output, and the demand to fill them",
      "site": {
        "machines": 100,
        "machine_power_kw": {
          "numerator": 10,
          "denominator": 1
        },
        "cooling_overhead": {
          "numerator": 13,
          "denominator": 10
        },
        "facility_power_kw": {
          "numerator": 1300,
          "denominator": 1
        },
        "energy_kwh": {
          "numerator": 5709600,
          "denominator": 1
        },
        "electricity_cost": {
          "numerator": 456768,
          "denominator": 1
        },
        "network_cost": {
          "numerator": 9150000,
          "denominator": 73
        },
        "backup_cost": {
          "numerator": 5490000,
          "denominator": 73
        },
        "total_site_cost": {
          "numerator": 47984064,
          "denominator": 73
        },
        "note": "Electricity is metered at the facility, so the cooling overhead applies to it and not to the network or backup lines."
      },
      "site_cost_per_million_tokens": {
        "numerator": 4097,
        "denominator": 49275
      },
      "net_saving_per_million_tokens": {
        "numerator": 41081,
        "denominator": 98550
      },
      "saving_survives_site_cost": true,
      "required_tokens_net_of_site": {
        "numerator": 1971000000000000000,
        "denominator": 41081
      },
      "pays_back_net_of_site": false
    },
    {
      "scenario": "output_rate_falls",
      "life_seconds": {
        "numerator": 31536000,
        "denominator": 1
      },
      "delivery_seconds": {
        "numerator": 0,
        "denominator": 1
      },
      "serving_seconds": {
        "numerator": 31536000,
        "denominator": 1
      },
      "machines": 100,
      "tokens_per_second": 6000,
      "utilisation": {
        "numerator": 1,
        "denominator": 2
      },
      "required_tokens": {
        "numerator": 40000000000000,
        "denominator": 1
      },
      "delivered_tokens": {
        "numerator": 9460800000000,
        "denominator": 1
      },
      "coverage": {
        "numerator": 5913,
        "denominator": 25000
      },
      "pays_back": false,
      "machines_required": 423,
      "machine_shortfall": 323,
      "reason": "This life needs 423 machines of the same output, and the demand to fill them",
      "site": {
        "machines": 100,
        "machine_power_kw": {
          "numerator": 10,
          "denominator": 1
        },
        "cooling_overhead": {
          "numerator": 13,
          "denominator": 10
        },
        "facility_power_kw": {
          "numerator": 1300,
          "denominator": 1
        },
        "energy_kwh": {
          "numerator": 11388000,
          "denominator": 1
        },
        "electricity_cost": {
          "numerator": 911040,
          "denominator": 1
        },
        "network_cost": {
          "numerator": 250000,
          "denominator": 1
        },
        "backup_cost": {
          "numerator": 150000,
          "denominator": 1
        },
        "total_site_cost": {
          "numerator": 1311040,
          "denominator": 1
        },
        "note": "Electricity is metered at the facility, so the cooling overhead applies to it and not to the network or backup lines."
      },
      "site_cost_per_million_tokens": {
        "numerator": 4097,
        "denominator": 29565
      },
      "net_saving_per_million_tokens": {
        "numerator": 21371,
        "denominator": 59130
      },
      "saving_survives_site_cost": true,
      "required_tokens_net_of_site": {
        "numerator": 1182600000000000000,
        "denominator": 21371
      },
      "pays_back_net_of_site": false
    }
  ],
  "pays_back_anywhere": [],
  "fails_everywhere": true,
  "planned_case": "planned",
  "assumptions": [
    "Every amount is a declared teaching input, not a vendor price or a project estimate.",
    "The fixed cost is incremental, so the per-token saving must not already amortise it.",
    "Machine count is an output conversion; the demand to fill those machines is a separate condition.",
    "Delivery time is taken out of the economic life rather than added to it.",
    "The cooling overhead multiplies metered electricity only, not the network or backup lines.",
    "Site cost is charged against delivered tokens, so a saving quoted before it is not the saving that repays anything.",
    "Maintenance, spare capacity, downtime and model-quality change are outside this account.",
    "Changing the machine count may change unit price or utilisation, which would require repricing."
  ]
}
```
