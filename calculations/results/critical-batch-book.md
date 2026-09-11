# critical-batch — 

输入：`{"card_counts": [32, 48, 96, 192, 384, 768, 1536], "compute_seconds_at_reference": "10284614378256728064/196933746337890625", "declared_noise_scale_tokens": 2000000, "microbatches_per_card": 8, "overhead_seconds_per_step": "6751999/11718750", "reference_cards": 48, "reference_sequences_per_step": 384, "sequence_tokens": 8192, "step_seconds_at_reference": "62388490856210290259/1181602478027343750", "total_tokens": 100000000000}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| weak_scaling_speedup_ceiling_exact | `"40201/24576"` |
| weak_scaling_speedup_ceiling | 1.6357828776041667 |
| weak_scaling_step_floor | 19,434.119549264942 |
| cards_where_weak_batch_equals_noise_scale | 30.517578125 |
| half_efficiency_batch_tokens | 2,000,000 |

计量条件：

- 关系式取自归档 scaling-laws 文本对 McCandlish 等人结果的转述：(S/S_min-1)(E/E_min-1)=1；B_noise 为声明输入，未对本章模型实测。
- 参考运行（每步 384×8192 token、共 100B token）视为恰好达到目标：由 S_ref 与 B_ref 反推 S_min 与 E_min，其他批量的步数与样本数按关系式换算。
- 弱扩展：每卡固定微批数，批量随卡数增长，每步时间不变（取本章 48 卡的 56.7 s）；强扩展：批量固定，计算时间按卡数反比缩放，通信与输入等待 4.5 s 不变。两者都不含并行效率变化。
- 弱扩展加速上限 = S_ref/S_min，是数据并行扩大批量的天花板；不代表学习率调度、warmup 或质量变化。

固定来源：

