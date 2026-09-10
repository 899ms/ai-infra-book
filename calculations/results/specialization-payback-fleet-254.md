# 专用化的固定费用能否被节省付清

回本 token 数 = 固定费用 ÷ 每 token 节省 = 4e+13 token。下列金额全部是教学假设，不是供应商价格或项目预测。

## 四种情形

| 情形 | 服务期 s | 机器 | 有效速率 tok/s | 需要 token | 交付 token | 覆盖率 | 回本 | 需要机器数 |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| planned | 31536000 | 254 | 10000 | 4e+13 | 4.005e+13 | 1.001 | 是 | 254 |
| life_halves | 15768000 | 254 | 10000 | 4e+13 | 2.003e+13 | 0.501 | 否 | 508 |
| delivery_slips | 15811200 | 254 | 10000 | 4e+13 | 2.008e+13 | 0.502 | 否 | 506 |
| output_rate_falls | 31536000 | 254 | 6000 | 4e+13 | 2.403e+13 | 0.601 | 否 | 423 |

## 整站费用与净节省

电费按设施计量，散热系数只乘电费，不乘网络与备份。

| 情形 | 设施功率 kW | 电费 | 网络 | 备份 | 站点合计 | 站点每百万 token | 净节省每百万 token | 扣除后回本 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| planned | 3302.0 | 2,314,042 | 250,000 | 150,000 | 2,714,042 | 0.0678 | 0.4322 | 否 |
| life_halves | 3302.0 | 1,157,021 | 125,000 | 75,000 | 1,357,021 | 0.0678 | 0.4322 | 否 |
| delivery_slips | 3302.0 | 1,160,191 | 125,342 | 75,205 | 1,360,739 | 0.0678 | 0.4322 | 否 |
| output_rate_falls | 3302.0 | 2,314,042 | 250,000 | 150,000 | 2,714,042 | 0.1129 | 0.3871 | 否 |

能够回本的情形：planned。
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
    "machines": 254,
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
      "machines": 254,
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
        "numerator": 40050720000000,
        "denominator": 1
      },
      "coverage": {
        "numerator": 250317,
        "denominator": 250000
      },
      "pays_back": true,
      "machines_required": 254,
      "machine_shortfall": 0,
      "reason": "The declared fleet delivers enough over this life",
      "site": {
        "machines": 254,
        "machine_power_kw": {
          "numerator": 10,
          "denominator": 1
        },
        "cooling_overhead": {
          "numerator": 13,
          "denominator": 10
        },
        "facility_power_kw": {
          "numerator": 3302,
          "denominator": 1
        },
        "energy_kwh": {
          "numerator": 28925520,
          "denominator": 1
        },
        "electricity_cost": {
          "numerator": 11570208,
          "denominator": 5
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
          "numerator": 13570208,
          "denominator": 5
        },
        "note": "Electricity is metered at the facility, so the cooling overhead applies to it and not to the network or backup lines."
      },
      "site_cost_per_million_tokens": {
        "numerator": 424069,
        "denominator": 6257925
      },
      "net_saving_per_million_tokens": {
        "numerator": 5409787,
        "denominator": 12515850
      },
      "saving_survives_site_cost": true,
      "required_tokens_net_of_site": {
        "numerator": 250317000000000000000,
        "denominator": 5409787
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
      "machines": 254,
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
        "numerator": 20025360000000,
        "denominator": 1
      },
      "coverage": {
        "numerator": 250317,
        "denominator": 500000
      },
      "pays_back": false,
      "machines_required": 508,
      "machine_shortfall": 254,
      "reason": "This life needs 508 machines of the same output, and the demand to fill them",
      "site": {
        "machines": 254,
        "machine_power_kw": {
          "numerator": 10,
          "denominator": 1
        },
        "cooling_overhead": {
          "numerator": 13,
          "denominator": 10
        },
        "facility_power_kw": {
          "numerator": 3302,
          "denominator": 1
        },
        "energy_kwh": {
          "numerator": 14462760,
          "denominator": 1
        },
        "electricity_cost": {
          "numerator": 5785104,
          "denominator": 5
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
          "numerator": 6785104,
          "denominator": 5
        },
        "note": "Electricity is metered at the facility, so the cooling overhead applies to it and not to the network or backup lines."
      },
      "site_cost_per_million_tokens": {
        "numerator": 424069,
        "denominator": 6257925
      },
      "net_saving_per_million_tokens": {
        "numerator": 5409787,
        "denominator": 12515850
      },
      "saving_survives_site_cost": true,
      "required_tokens_net_of_site": {
        "numerator": 250317000000000000000,
        "denominator": 5409787
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
      "machines": 254,
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
        "numerator": 20080224000000,
        "denominator": 1
      },
      "coverage": {
        "numerator": 627507,
        "denominator": 1250000
      },
      "pays_back": false,
      "machines_required": 506,
      "machine_shortfall": 252,
      "reason": "This life needs 506 machines of the same output, and the demand to fill them",
      "site": {
        "machines": 254,
        "machine_power_kw": {
          "numerator": 10,
          "denominator": 1
        },
        "cooling_overhead": {
          "numerator": 13,
          "denominator": 10
        },
        "facility_power_kw": {
          "numerator": 3302,
          "denominator": 1
        },
        "energy_kwh": {
          "numerator": 14502384,
          "denominator": 1
        },
        "electricity_cost": {
          "numerator": 29004768,
          "denominator": 25
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
          "numerator": 2483348064,
          "denominator": 1825
        },
        "note": "Electricity is metered at the facility, so the cooling overhead applies to it and not to the network or backup lines."
      },
      "site_cost_per_million_tokens": {
        "numerator": 424069,
        "denominator": 6257925
      },
      "net_saving_per_million_tokens": {
        "numerator": 5409787,
        "denominator": 12515850
      },
      "saving_survives_site_cost": true,
      "required_tokens_net_of_site": {
        "numerator": 250317000000000000000,
        "denominator": 5409787
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
      "machines": 254,
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
        "numerator": 24030432000000,
        "denominator": 1
      },
      "coverage": {
        "numerator": 750951,
        "denominator": 1250000
      },
      "pays_back": false,
      "machines_required": 423,
      "machine_shortfall": 169,
      "reason": "This life needs 423 machines of the same output, and the demand to fill them",
      "site": {
        "machines": 254,
        "machine_power_kw": {
          "numerator": 10,
          "denominator": 1
        },
        "cooling_overhead": {
          "numerator": 13,
          "denominator": 10
        },
        "facility_power_kw": {
          "numerator": 3302,
          "denominator": 1
        },
        "energy_kwh": {
          "numerator": 28925520,
          "denominator": 1
        },
        "electricity_cost": {
          "numerator": 11570208,
          "denominator": 5
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
          "numerator": 13570208,
          "denominator": 5
        },
        "note": "Electricity is metered at the facility, so the cooling overhead applies to it and not to the network or backup lines."
      },
      "site_cost_per_million_tokens": {
        "numerator": 424069,
        "denominator": 3754755
      },
      "net_saving_per_million_tokens": {
        "numerator": 2906617,
        "denominator": 7509510
      },
      "saving_survives_site_cost": true,
      "required_tokens_net_of_site": {
        "numerator": 150190200000000000000,
        "denominator": 2906617
      },
      "pays_back_net_of_site": false
    }
  ],
  "pays_back_anywhere": [
    "planned"
  ],
  "fails_everywhere": false,
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
