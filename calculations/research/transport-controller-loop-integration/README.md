# 六场景公共 CLI 交付独立审查：PASS

实际运行统一 `calc.py transport-closed-loop`，六个book/router场景各JSON与Markdown，共12次CLI调用；包括三种控制器的30MB/5MB实际重算。每个输入来自公共book.json，逐次创建并释放临时输入与输出；输出按块逐字节和正式results比对，另核正式文件与已完成results manifest的SHA一致。

共耗时 167.36 秒。每次输入原文/哈希、预期与实际文件哈希/大小、调用耗时、代码前后指纹见 `cli-check.json`。始末公共transport包、两个topic、CLI、source校验器、来源锁和book场景文件哈希完全相同，results manifest也未变化。

可运行脚本为 `check-cli.py`；`--ready`只检查六个场景的12份产物均已存在且登记，不触发reproduce。验收前确实等待根的已有reproduce完成，没有重复启动全流水线。该证据核公共交付一致性，不把字节相同替代此前独立算法/物理审查。未改公共代码、正文或主纲。

## 最终公共接入验收（2026-09-10）

[acceptance.json](acceptance.json) 固定52项文件证据。最终909 tests（887通过/22可选跳过）、2256产物28图及12章5096链接通过。6场景完整研究/公共数学一致，12实际CLI输出与最终产物一致；控制器数字限定于声明的业务、包布局与QUIC适配，不能当通用性能排名。

复算收尾实际发现并修复两项问题：正文同步不再合并作者空行；stage resource模块的set遍历改为稳定排序。后者25场景跨进程raw JSON/MD字节一致，数值与保留旧JSON完全一致；[最终核对](final-stability-check.json)保留2206其他产物不变及CLI证据继续有效。最后一次同步12章主文均未改变。

C68的完整媒体接真实反馈、公共ACK聚合和匹配TCP/H3实测仍待；全书目标未完成。历史日志保留发现问题和重算过程，不能用早期通过覆盖最终结果，也不能把研究候选检查当公共验收。
