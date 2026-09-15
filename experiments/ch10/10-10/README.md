## V4 resource floor and coverage gap

[MoE-only V4 bounds](v4-lower-bounds/README.md) count278,152,609,792 parameters in the43 main-layer MoE subset and4,450,441,756,672bytes of declared16B/parameter optimizer state. This alone requires at least56×80GB or25×180GB devices in aggregate; it excludes all other state/workspace and is not a sufficient deployment.36 conditional compute/state cases are checked. Full attention/compressor backward and complete training coverage remain missing.

## Conditional cost comparison added

[72 hardware cases and72 exact rental-price boundaries](cost-boundaries/README.md) distinguish modeled compute-only release from full-deadline reservation, using existing Qwen/Dense calculations. Prices, quality acceptance and full layout feasibility remain unknown where not supported. This does not substitute a Dense/V3 proxy for the missing V4 training-task comparison.

# 实验 10-10：训练完成期限的公开记录校准

已完成 [SmolLM3 作者公开训练记录的离线核验](public-training/README.md)，含原始配置、逐步抽样、最终 run 完整控制台日志和图。公开记录显示阶段间配置变化及恢复计数口径，不能把项目简介中的设备数套到每一个 run。

当前仍为部分完成。具体 Qwen／V4、1T／5T／10T Dense 的跨硬件期限、质量目标和成本不能由这个 3B 模型的记录直接外推。数量级计算由另一个任务负责，本目录不重复其计算；匹配目标任务的实际分配、供数、保存与故障时间线仍缺。
