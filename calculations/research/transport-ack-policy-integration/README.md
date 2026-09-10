# ACK 策略公共 CLI 交付复核

`check-cli.py --ready` 只检查 book 中恰好 10 个 `ack-policy-` 场景及正式 manifest 的 20 个 JSON/Markdown 条目，不生成或重启 reproduce。收到根代理现有复算完成确认后，才执行不带参数的脚本。

完整检查实际调用统一 `calc.py transport-closed-loop` 共 20 次，包括三个原书大例每格式独立计算；每次输出与正式文件逐字节比较并核 manifest SHA，随后释放临时输入与输出。记录输入内容与 SHA、预期/实际字节数与 SHA、每调用耗时、公共代码和官方输入来源前后指纹，以及整体 manifest 稳定性。

指纹包含公共 ACK 接收器、网络与 sender、全部共享 transport 控制器、CLI/入口、book 输入、source lock 和 reference_sources 指向的实际官方原件。此检查不修改公共实现、正式结果或 manifest。

完成证据为 `cli-check.json`；执行中 `cli-check-progress.json` 仅表示部分完成，不代表 20 次通过。

实际完成：20 次统一 CLI 调用全部通过，含三个大例每格式真实重算。总耗时 159.926s；32 个公共代码、配置和官方来源文件指纹在每次调用前后及整体始末一致，正式 results manifest 始末一致。所有输出均逐字节等于正式产物，临时文件已逐份释放。详细输入、预期/实际 SHA、字节数和耗时见 `cli-check.json`。
