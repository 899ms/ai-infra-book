# 4-2：在模型内替换一个真实专家的矩阵输出

对固定 Qwen3-VL-30B-A3B-Instruct-FP8 快照，替换第 0 层专家 0 的 gate_up 输出。激活按 K 维每 128 元素量化，权重沿用同一逐列 INT8 表示：一条做 16 次 INT8 部分矩阵乘并用 FP32 合并，一条将相同量化值展开为 BF16 后矩阵乘。其余专家、SwiGLU、第二处矩阵乘和后续模型执行保持原生实现。

两条路径各执行四条冻结检索任务，均 **4/4 严格 JSON 答案正确**，每条 46 个输出 token，与此前原生参考逐 token 相同。下游路由发生变化，因此输出相同不代表中间计算相同。只有四个不同任务；不能把八次执行当成八个独立任务，也不代表全模型 INT8 或开放任务质量通过。

## 实际执行和检查

- 单次模型装载，先 direct 四题，再 dequant 四题，温度 0、seed 906；请求间通过 collective RPC 切换模式。固定顺序用于质量检查，不做时间比较。
- 总计 392 次目标层调用，保存 6,514 行被选输入及其原生、替换输出。每次在原生第一处 GEMM 后，仅按 `token * top_k + slot` 写回专家 0 的槽位，并断言所有未选槽位逐元素不变。
- 检查运行时 FP8 权重字节和 scale 与封存专家矩阵转置完全一致。保存的 top-k 与模型返回的第 0 层路由按调用顺序逐项核对。实际替换输出确实改变，非空操作。
- 独立 CPU FP64 审计根据保存的 BF16 输入重建量化值和矩阵输出。审计容差预设 0.4%（用于核对实现和输出 BF16 舍入，不是模型质量门槛）；实际最大相对 L2 差异约 0.217%。此前原始矩阵局部误差的 2% 门槛保持原义。
- 原生 GEMM **仍然执行**，随后覆盖选中输出，并有保存数据与检查的开销。因此本目录墙钟不用于比较速度、节省显存或生产部署收益。性能结果见独立的 [block-scales](../block-scales/README.md)。

## 证据与复现

`results/requests.jsonl` 保存全部答案、输出 token、停止原因和事件；每题 routes.npy 保存完整模型路由。`results/interventions.jsonl` 和对应 `.pt` 保存每次介入的数据；`analysis.json` 给出逐题质量、路由差异和逐文件 CPU 审计。`run/supervisor.json` 记录实际正常退出、无资源终止原因、无残留子进程。没有重跑模型来挑选答案。

`reference/` 来自此前 [只读采集实验](../routed-activations/README.md) 的原生运行，原生基线没有重复计算；`reference-expert.pt` 是相同已封存训练专家。`source/` 保存本次实际 vLLM 的专家和 kernel 源码，便于复核输出寻址与单 token 分支。

环境：RTX PRO 6000 Blackwell；vLLM 0.23、Torch 2.11.0+cu130；模型完整快照路径见 `results/environment.json`。KV 为 2 GiB、eager、chunked prefill 2048、max_num_seqs=1，APC 与异步调度关闭，文本请求，无图像输入。使用现有剩余显存，没有终止其他服务。

在安装相同 vLLM 环境、准备同一模型快照的独立目录中运行。先移走本目录的封存 `run/`、`results/`、`analysis.json`，避免覆盖证据：

```sh
python reproduce.py --model /path/to/frozen/model/snapshot
```

`reproduce.py` 拒绝已存在的输出目录。新运行的时间戳、文件校验值会不同；`verify.py` 用于检查交付包的既有封存，重现实验应运行 `analyze.py` 检查新结果，不能要求新结果文件匹配原 manifest。扩展至更多专家、更多任务与完整部署的内存工作区验证仍待完成。
