# 48次新增真实CLI验收：已准备，等待正式reproduce

`check-cli.py`已落盘并仅做语法编译检查；尚未执行CLI、readiness或reproduce。主代理确认正式reproduce完成、源码冻结后运行：

```sh
python calculations/research/shared-airtime-public-integration/check-cli.py --ready
python calculations/research/shared-airtime-public-integration/check-cli.py --run
```

默认或`--ready`只检查，不运行48次计算。脚本先调用公共`reproduce.input_hashes()`读取当前完整输入清单，与正式`results/manifest.json.inputs`严格比较；清单不一致立即拒绝stale。核24个注册ID与provenance映射、canonical输入hash，48个正式JSON/MD文件必须存在且与manifest逐文件SHA相同。

每一调用写入临时精确场景JSON，实际启动`calc.py transport-closed-loop --inputs ... --format json/md --output ...`子进程重新计算。完整输出按1MB块与正式产物逐字节比较，记录双方SHA/长度，不读取正式结果生成输出。每次前后核公共全部Python、运行配置/场景、相关官方原件和正式manifest；最后重新验证整个正式输入清单与48产物。临时文件随后释放，保留输入hash、注册ID、运行命令、输出hash、耗时与逐调用证据。

`cli-runs/<UTC时间>/progress.json`每次调用后原子更新；成功写`check.json`及本目录`cli-check.json`，失败保留`failure.json`和已完成记录。进度不宣称全48完成，旧运行目录不删除。当前没有这些新执行证据，不能把脚本准备好等同于验收通过。

只读报告源码审查：`airtime_report.ledger`要求每交换已收到、反馈已知、成功、结束不晚于horizon、真实PHY字段不为null，并要求全部reservation结束且reserved=observed，才提供完整PHY账；否则`complete_success_phy_ledger=None`。教学确认段、失败和截止未完成不被算成已知RF。WAN使用`wan_serialized_ip_bytes_by_horizon`，原媒体报告将旧null序列化字节显示“未提供”，`wire_bytes`明确称“已安排发送”。完整成功账里DATA PSDU和MAC ACK独立计，RF/空等/SIFS传播分列。未发现将未来字节或未知PHY字段无条件报为实际观察值的分支；这是源码阅读结论，48实际Markdown验收仍待正式运行。
