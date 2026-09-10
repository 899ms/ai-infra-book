# 五个完整旧 workload 的显式关闭无线回归

检查入口：

```sh
/Users/boj/miniconda3/bin/python calculations/research/shared-airtime-review/check-disabled-book.py
```

脚本读取旧 `media-feedback-loop/runs/book-*-result.json` 的完整 inputs，仅增加 `network.wireless_access={"enabled":false}`，实际调用新版共享空口 `calculate()`。五例为 image-baseline、mixed-fifo-immediate、mixed-fifo-aggregate、mixed-priority-immediate、mixed-priority-aggregate。

比较整个 JSON 对象，不排除任何字段，也不只比较 summary。随后分别计算实际新结果及旧结果的规范化 SHA-256；旧文件原始字节哈希另行记录，避免把规范化哈希误称为文件原始哈希。每例记录实际 calculate 耗时和包括解析/完整比较/哈希在内的耗时。大结果不重复落盘，因为实际结果已逐字段对照完整保留的基线；可执行脚本保留重算能力。

`disabled-book-result.json` 的 `status` 只有在五例全部完成、源码与基线始末不变时才为 `PASS`。运行中该文件可能只包含已完成案例、状态为 `running`，不得视为全五例通过。`disabled-book-progress.json` 仅表示当前执行位置，亦不是完成证据。

源码锁包括实际导入的公共 infra_calc Python 模块、候选 calculate/airtime、检查脚本及公共 sources.lock。此任务只验关闭无线的兼容性，不提供启用无线的大 workload 证据。

实际执行已完成：PTY 58347 正常 exit 0，五例全部 PASS，总耗时 138.77 秒。

| 完整 workload | calculate 秒 | 传输记录数 | 完整 JSON |
|---|---:|---:|---|
| book-image-baseline | 18.221 | 61600 | 相等 |
| book-mixed-fifo-immediate | 19.149 | 61626 | 相等 |
| book-mixed-fifo-aggregate | 29.258 | 46226 | 相等 |
| book-mixed-priority-immediate | 19.201 | 61642 | 相等 |
| book-mixed-priority-aggregate | 29.718 | 46237 | 相等 |

本轮覆盖源码 `37c442824b5b127407658a75b21638882ee5a75ff08156cfc716b141d1b75f6b`；包括先前14小例后，旧19个场景的关闭无线完整回归已全部实际执行。
