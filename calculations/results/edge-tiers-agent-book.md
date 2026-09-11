# edge-deployment-tiers — 

输入：`{"bf16_block_bytes": 64, "cases": [{"deadline_seconds": 45, "id": "twenty-rounds", "rounds": 20}, {"deadline_seconds": 23, "id": "ten-rounds", "rounds": 10}, {"deadline_seconds": 15, "id": "ten-rounds-tight", "rounds": 10}, {"deadline_seconds": 45, "id": "twenty-retain-nine", "reconnect_seconds": 1, "redo_rounds": 1, "rounds": 20}, {"deadline_seconds": 45, "id": "twenty-lose-ten", "reconnect_seconds": 1, "redo_rounds": 10, "rounds": 20}, {"deadline_seconds": 23, "id": "ten-retain-seven", "reconnect_seconds": 2, "redo_rounds": 1, "rounds": 10}, {"deadline_seconds": 23, "id": "ten-lose-eight", "reconnect_seconds": 2, "redo_rounds": 8, "rounds": 10}], "constant_uplink_bits_per_second": 8000000, "context_tokens": 8192, "decode_result": "results/qwen3-8b-decode-b1-s8192.json", "efficiency_record": "experiments/ch08/08-01/efficiency.json", "encoder_devices": ["rtx4090", "h100-sxm"], "encoder_uplink_bits_per_second": 6400000, "energy_ledger_result": "results/energy-ledger-book.json", "fast_link_bits_per_second": 400000000000, "image_bytes": 800000, "model": "qwen3-8b", "phone_joules_per_token": ["0.576", "0.756"], "q4_block_bytes": 18, "screenshot_bytes": 800000, "terminal_seconds": "0.3", "tiers": [{"device": null, "label": "phone, four LPDDR5X x16 channels", "name": "end", "rtt_seconds": "0", "uplink_bits_per_second": null}, {"device": "rtx-pro6000-blackwell-ws", "label": "nearby workstation", "name": "near", "rtt_seconds": "0.02", "uplink_bits_per_second": 80000000}, {"device": "h100-sxm", "label": "cloud region", "name": "cloud", "rtt_seconds": "0.2", "uplink_bits_per_second": 6400000}], "tokens_per_round": 45, "uplink_scan_bits_per_second": [2000000, 20000000, 181], "variable_uplink": [[10, 6000000], [10, 10000000]], "vision_result": "results/vision-encoding-single.json"}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| step_bytes | 5,465,189,952 |
| q4_weight_bytes | 4,257,230,400 |
| kv_bytes | 1,207,959,552 |
| prefill_flops | 133,594,323,353,600 |
| end_model_seconds_per_round | 2.8730554654205607 |
| near_model_seconds_per_round | 0.13723970303571428 |
| cloud_model_seconds_per_round | 0.07341299935522388 |
| near_prepare_seconds | 0.2651733294037316 |
| cloud_prepare_seconds | 0.13502559465696382 |
| totals_twenty_rounds_seconds | `[63.46110930841122, 11.009967390118018, 31.60328558176144]` |
| energy_twenty_rounds_joules | `[[518.4, 680.4], [1805.9804340708104, 1805.9804340708104], [1122.299907233009, 1122.299907233009]]` |
| lowest_energy_feasible_twenty_rounds | `"cloud"` |
| cloud_deadline_uplink_mbit_per_second | 3.832712355982445 |
| cloud_faster_than_near_uplink_mbit_per_second | `null` |
| measured_cloud_faster_uplink_mbit_per_second | 73.32745090401862 |
| local_encode_seconds | 0.007931601510895885 |
| remote_encode_seconds | 0.0013243385583181727 |
| fast_link_transfer_difference_ms | 0.14784 |

计量条件：

- All tiers run one Qwen3-8B q4_0 checkpoint at 8K context and generate the same tokens per round; quality is fixed by construction.
- Model time per round is tokens x (q4_0 weights + 8K KV) / memory bandwidth, the decode read lower bound used in 12.1.5.
- Preparation is one 8K-context prefill at the dense BF16 peak; the phone has no archived matrix peak and is given zero, which only favours it.
- GPU energy is TDP/TGP x busy seconds (an upper bound); phone energy is the MELTing Point measured 0.16-0.21 mWh per token.
- Measured-efficiency rows scale both GPU model times by the RTX PRO 6000 batch-1 8K decode measurement of experiment 8-1.
- Uplink, round-trip times, terminal time and reconnect times are declared network and task conditions.
- A disconnection affects only remote tiers; redone rounds are executed again and counted again in energy.

固定来源：

