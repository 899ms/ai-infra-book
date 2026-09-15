# 首完成请求：原始事件索引

PID/seq定位原始JSONL；seq从1开始。本表直接读取原始return字段，不能把缺少的其他字段默认为false。先前表的progress值误写false，保留在REQUEST-EVIDENCE-before-correction.md；原始trace、分析与图未改变。

## 0-native-1 / native-0

| 阶段 | PID / seq | monotonic_ns | 源码行 / 值 |
|---|---|---:|---|
| rate return | 2573055 / 103 | 1128569192416120 | prefetch_rate_limited:1032 / `false` |
| prefetch return | 2573055 / 131 | 1128569192902887 | prefetch_from_storage:1521 / `null` |
| progress final | 2573055 / 5377 | 1128569438696194 | check_prefetch_progress:1412 / `true` |
| pop return | 2573055 / 5384 | 1128569438921697 | pop_prefetch_loaded_tokens:1429 / `1024` |
| prefill call | 2573055 / 5564 | 1128569689016543 | prepare_for_extend:2152 / `null` |

API首完成cached_tokens=1008。

## 0-native-8 / native-4

| 阶段 | PID / seq | monotonic_ns | 源码行 / 值 |
|---|---|---:|---|
| rate return | 2583040 / 1000 | 1128602182200643 | prefetch_rate_limited:1030 / `true` |
| prefetch return | 2583040 / 1003 | 1128602182278316 | prefetch_from_storage:1485 / `null` |
| progress final | 2583040 / 2000 | 1128602226699649 | check_prefetch_progress:1361 / `true` |
| pop return | 2583040 / 2014 | 1128602227240048 | pop_prefetch_loaded_tokens:1429 / `0` |
| prefill call | 2583040 / 2763 | 1128602486334373 | prepare_for_extend:2152 / `null` |

API首完成cached_tokens=0。

## 1-native-8 / native-4

| 阶段 | PID / seq | monotonic_ns | 源码行 / 值 |
|---|---|---:|---|
| rate return | 2591726 / 1353 | 1128632828538126 | prefetch_rate_limited:1030 / `true` |
| prefetch return | 2591726 / 1356 | 1128632828627023 | prefetch_from_storage:1485 / `null` |
| progress final | 2591726 / 2179 | 1128632860749369 | check_prefetch_progress:1361 / `true` |
| pop return | 2591726 / 2186 | 1128632860846690 | pop_prefetch_loaded_tokens:1429 / `0` |
| prefill call | 2591726 / 2746 | 1128633101902357 | prepare_for_extend:2152 / `null` |

API首完成cached_tokens=0。

## 1-native-1 / native-0

| 阶段 | PID / seq | monotonic_ns | 源码行 / 值 |
|---|---|---:|---|
| rate return | 2593889 / 103 | 1128662336285127 | prefetch_rate_limited:1032 / `false` |
| prefetch return | 2593889 / 137 | 1128662337707731 | prefetch_from_storage:1521 / `null` |
| progress final | 2593889 / 5310 | 1128662565786785 | check_prefetch_progress:1412 / `true` |
| pop return | 2593889 / 5317 | 1128662565995296 | pop_prefetch_loaded_tokens:1429 / `1024` |
| prefill call | 2593889 / 5497 | 1128662829950928 | prepare_for_extend:2152 / `null` |

API首完成cached_tokens=1008。

