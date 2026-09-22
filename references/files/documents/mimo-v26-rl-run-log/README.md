# MiMo-V2.6 RL 运行日志快照

小米在 <https://mimo.xiaomi.com/rl/> 直播了 MiMo-V2.6-Pro 与 MiMo-V2.6-Flash 两次强化学习运行的训练指标。本目录保存该站点 JSON 接口的原始响应，用于第 10 章故障恢复相关的推算。

## 抓取时间与内容

| 文件 | 接口 | 抓取时间（UTC） | 内容 |
| --- | --- | --- | --- |
| `runs.json` | `api/runs` | 2026-09-22T03:02 | 站点配置、两次运行的标识与指标说明 |
| `notices.json` | `api/notices` | 2026-09-22T03:02 | 运营方公告六条，含四条重启原因 |
| `benchmarks.json` | `api/benchmarks` | 2026-09-22T03:02 | 三个离线基准逐步得分 |
| `status_pro.json` / `status_flash.json` | `api/status?run=` | 2026-09-22T03:02 | 收尾状态、累计用量、成本口径、事件日志（末 30 条） |
| `series_pro.json` / `series_flash.json` | `api/series?run=` | 2026-09-22T03:02 | 逐步 `dynsam/avg@n`、`timing_s/*`、`ctx_total_length/mean`、`perf/total_num_tokens` |
| `status_pro_2026-09-18.json` / `status_flash_2026-09-18.json` | `api/status?run=` | 2026-09-18T04:31 | 运行中途快照，保留早期事件 |
| `events_pro.json` / `events_flash.json` | 由上两组合并 | 2026-09-22 | 完整事件日志，见下 |

## 日志完整性与成本口径

**接口只返回最近 30 条事件。** 收尾时抓取的 `status_*.json` 中，Pro 的事件日志从第 11 步开始，前 9 次重启已经不在响应里；Flash 从第 8 步开始。完整日志只能靠 9 月 18 日的中途快照补齐。`events_*.json` 由两次抓取按 `(t, kind, step, redo)` 去重合并而成，合并后的重启计数与接口自报的 `totals.restarts`（Pro 14、Flash 5）一致。这两份已保存的收尾响应不含早期事件，复算应使用本目录的合并日志；重启计数一致并不证明其他类型的事件没有遗漏。

**成本是站点自己的口径，不是账单。** `cost.so_far` 由 `cost.rate_per_s` 乘墙钟时间得到，按构造恒等，Pro 每秒 5.71 美元、Flash 每秒 2.855 美元。两者分别为 262 万与 85 万美元，与技术报告 §4.1 自报的 260 万与 90 万美元同量级。引用时应以小时为主，金额只作一次换算并注明口径。

## 与技术报告的对应

技术报告 §5.5 与图 12 给出同两次运行的故障分类与根因，总时长记为 Pro 123.1 h、Flash 81.8 h；本日志按 `run.start` 到 `run.end` 计为 127.5 h 与 83.1 h，Flash 从开始到第 30 步完成为 81.8003 h，与图 12 的标注一致，之后还有 1.2942 h 才到日志结束时刻；Pro 从开始到最后一步为 127.2414 h，仍与图 12 不同，现有材料不足以解释其起止范围。引用时需注明采用哪套口径。报告归档于 `../../papers/mimo-v26-tech-report.pdf`。

## 复算与解释范围

`recalculate.py` 为本次核对新增的计算脚本，`recalculated.json` 为脚本输出；二者不是站点原始响应。在仓库根目录运行：

```bash
python3 references/files/documents/mimo-v26-rl-run-log/recalculate.py
```

脚本核对事件合并结果、重启计数及最终步骤时间戳，计算最终 30 步的 `timing_s/step` 之和、重启前事件区间、被回滚步骤和重跑步骤的事件区间。Pro／Flash 最终逐步计时之和为 95.11／67.65 h，平均每步为 3.17／2.26 h。总时长与逐步计时之差为 32.38／15.44 h，但这个差额包含多种尚未分开的时间，不能全部称为恢复开销；事件区间也不等于纯丢弃计算。所有时长均为墙钟小时，未按设备数加权。

详细定义、与第 10 章模型的分母差异和技术报告的证据范围见[案例笔记](../../../../case-studies/mimo-v26-rl-interruptions.md)。

## 中断费用估算与配图

复算记录的 `costs` 字段使用官方看板的固定费率，计算各次重启前事件区间的费用；Flash 另计第一次执行后被回滚的第 16、17 步。Pro 合计约 61.91 万美元，Flash 合计约 14.09 万美元。它们是按事件区间换算的资源占用成本，包含失败尝试及重启前等待，不是官方单列的故障账单，也未扣除可能复用的采样结果。Pro 中断时间减半可节省约 31 万美元，是训练工作、费率与其他耗时不变时的情景估算。

第 10 章配图由 `manuscripts/ch10/mimo-interruptions.py` 读取这些字段绘制；时间线采用完整运行日志，参考作者提供的 2026-09-18 Claude Artifact 截图布局。
