# 9-9 补充：容量淘汰与进程重启后的真实 KV 命中

2026-09-14 在 `rtx-pro` 完成三轮、30 次 Qwen3-8B 生成；其中 18 次目标请求、12 次容量压力请求。目标沿用封存的 Agent 提示，3136 个输入 token，每次生成 16 个 token。18 次目标输出文字完全一致。该提示来自原有失败任务，16 个生成 token 不是完整任务或质量改进的证明。

| 生命周期阶段 | 三轮原生 cached_tokens | 客户端耗时中位数 |
| --- | --- | --- |
| 新进程首次目标 | 0 / 0 / 0 | 349.8 ms |
| 同进程重复目标 | 3135 / 3135 / 3135 | 200.3 ms |
| 四条无关输入造成容量压力后 | 0 / 0 / 0 | 357.6 ms |
| 再次重复目标 | 3135 / 3135 / 3135 | 200.8 ms |
| 终止原 worker、新进程加载同权重后 | 0 / 0 / 0 | 349.6 ms |
| 新进程再次重复目标 | 3135 / 3135 / 3135 | 200.5 ms |

原生 KV 池限制为 4096 token，四条不同开头的压力输入各 1800 token，依次运行，累计工作超过容量。本实验未调用 flush_cache；观察到目标缓存复用全部丢失，随后可重新建立。重启创建新 PID，不使用持久化 KV 存储。缓存命中来源为 `/generate` 的原生 `meta_info.cached_tokens`，没有以客户端维护的标签替代实际命中。

这是单 worker 的容量压力与生命周期实验。**没有运行双实例 router 或远端 KV 取回，历史实验 9-9 整体仍部分完成。** 此处的零命中证明被测目标不再复用旧缓存；没有逐节点跟踪内部 LRU 树，不将其扩写为生产淘汰分布。计时含客户端与框架开销，顺序固定、共享 GPU、仅三轮，不能推导稳定 p95/p99、整机吞吐或独占性能收益。

## 执行环境与复现

使用既有 `/home/ubuntu/ai-infra-book-experiments/tools/sglang0513-venv`，固定 Qwen3-8B revision `b968826d9c46dd6066d109eabc6255188de91218`，BF16、Triton attention、temperature=0、seed=909、忽略 EOS、每请求 16 输出。关闭完整与分段 CUDA Graph；最多允许 8 个运行请求，但本脚本按顺序一次只提交一个。`results/protocol.json` 保存准确命令和输入/脚本 SHA；六份 `server-*.json` 保存实际解析后的配置和 PID，服务器日志保存权重加载、KV 池、prefill/decode 事件。

当前默认 `nvidia-smi` 的 NVML 与内核驱动不匹配；脚本只为自建进程指定已存在的匹配 NVML 路径，不重装驱动或重启机器。SGLang 全局 JIT 缓存中有链接 CUDA 11 的对象，而当前 PyTorch 使用 CUDA 13；复用既有实验的 CUDA 13 缓存并显式设置 CUDA 13 动态库路径后启动成功。未修改共享 Python 包，也未通过删除全局缓存来修复问题。KV 池由 `max-total-tokens=4096` 限制，日志显示 K、V 各约 0.28 GiB；`mem-fraction-static=0.90` 是框架的剩余内存计算参数，不代表本实验实际占用整卡 90%。原服务保留。

在服务器的新目录复制 `run.py`、`agent-prompts.json`，确认 31491 端口空闲、至少 26 GiB 空闲显存，然后执行：

```sh
/home/ubuntu/ai-infra-book-experiments/tools/sglang0513-venv/bin/python run.py
```

脚本拒绝覆盖 `results/`，只终止自身创建的进程组。`results/cleanup.json` 记录六个已回收进程，GPU 前后状态各自留档。在 Mac 上运行 `python3 experiments/ch09/09-09/eviction-restart/analyze.py`，独立检查 30 份响应的输入/输出 token 数、全部生命周期顺序、缓存字段、不同 PID 和脚本散列，生成 [summary.json](summary.json) 与 [manifest.json](manifest.json)。成功前的启动配置调试没有作为正式测量交付。
