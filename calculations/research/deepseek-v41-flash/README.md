# DeepSeek V4.1 Flash：2026-09-10 发布核对与版本选择

建议保留 V4 Flash 作为已经完成前向、算子、训练和实验核对的历史模型，新增 V4.1 Flash 作为 CED、跨层 KV 共享、原生视觉与 Agent 服务的新例子。两者不是相同结构的权重更新，不能只替换模型名称并保留原来的数字。书中当前 API 选型应与历史架构复算分开：用户提供的官方公告说明 `deepseek-flash` 已切换到 V4.1，旧 `deepseek-v4-flash` 名称也会路由到新版；因此 API 别名无法用来复现旧权重实验。公告还给出 V4 Pro 于北京时间 2026-09-14 12:00 起切换路由的计划；这不影响固定 revision 的旧开源模型计算。

## 第二章计算扩展

第二章五模型修订已新增完整文本矩阵适配器 `v41-forward`，覆盖注意力、压缩／索引、路由与共享专家、Engram、Single-Pass mHC 和词表头，并按 CED 与参考全层路径分别累计。新增结果与测试见[五模型修订记录](../../../research/ch02-five-models-2026-09-10/README.md)。下文关于“只完成专家子账”的表述记录此次扩展前的调研状态；原 `v41-flash` 命令继续保留其较窄的权重、缓存与专家工作口径。

## 官方证据与下载范围

- [官方模型卡](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/df42c109f1defefcbfcedbe7d905718a12266e40/README.md)：发布说明、基准、参数标签与许可。
- [官方 config](../../configs/models/deepseek-v4.1-flash/config.json)、[inference config](../../configs/models/deepseek-v4.1-flash/inference/config.json)：HF 根配置为 text/vision 嵌套结构；43 项 compress_ratios 包括 40 层主干和 3 层 DSpark，主干计算不能用 43 层。
- [技术报告原件](../../sources/deepseek-v4.1-flash/DeepSeek_V41_Tech_Report.pdf)：§2.2 CED、§2.3 CSA2、§2.4 KV 格式、§3.2 服务与持久缓存。
- [参考 model.py](../../sources/deepseek-v4.1-flash/inference/model.py) 与同目录 kernel、Engram、视觉、转换、生成代码：作为静态证据保存，未执行远程模型代码。
- [官方 FlashMLA 格式说明](../../sources/deepseek-v4.1-flash/FlashMLA-README.md)，固定 `07a1089857b63e74e3133630c02b083b75e8d4b2`：V4 主 KV 584 B，V4.1 SWA 528 B，V4.1 全局主 KV 288 B。
- [权重索引](../../sources/deepseek-v4.1-flash/model.safetensors.index.json) 与 `sources/deepseek-v4.1-flash/headers/`：通过 HTTP Range 下载全部 **48 个分片的二进制 safetensors 文件头**，核对 **96,085 张量**、每张量 shape/dtype/offset、连续性、分片归属与索引总字节。没有下载约 510 GB 的张量值，也没有执行模型推理。

模型 revision 固定为 `df42c109f1defefcbfcedbe7d905718a12266e40`。全部官方输入及 Range 在 `configs/sources.lock.json` 记录 URL、revision、大小、SHA-256；`verify-sources` 校验本地内容。`download.py` 可重取固定模型输入；公共 `fetch-sources --model deepseek-v4.1-flash` 还会重取已锁定的 FlashMLA 文件。

## 实质差别

| 项目 | V4 Flash | V4.1 Flash |
| --- | --- | --- |
| 官方主干参数标签 | 284B | 552B，另有约 196B Engram |
| 层与宽度 | 43 层、4096 | 40 层、5120；20 encoder + 20 decoder |
| 路由专家 / 每 token top-k | 256 / 6 | 384 / 6 |
| 共享专家 / 专家中间维 | 1 / 2048 | 1 / 2304 |
| 官方激活参数标签 | 13B | prefill 8B / decode 16B |
| 全局注意力 | 21 CSA（4:1）+ 20 HCA（128:1） | 38 CSA2；4 个 KV owner、8 个 indexer |
| 原生视觉 | 此固定发布不含视觉主干 | 32 层 ViT + projector |
| 残差与辅助模块 | mHC、1 层 MTP | Single-Pass mHC、Engram、3 层 DSpark |
| 全局 KV 渐近增长 | 3,514.25 B/token | 890 B/token |

Checkpoint 的精确主干逻辑参数为 551,566,180,464，Engram（含投影）196,928,504,320，视觉与 projector 485,268,480，DSpark 14,225,362,530。逻辑参数不含量化 scale；I8 容器中的 routed expert FP4 参数按每字节两个值展开。Engram 表本身有 196,613,849,600 个参数。

全部 checkpoint 张量载荷为 **510,286,023,000 B**；加 safetensors 文件头为 **510,296,708,312 B**。这些是文件存储，不是全部常驻 HBM 的要求，也不是每 token 读取权重的字节数。组件拆分见[计算结果](../../results/v41-flash-n8192-b1.md)。

## 复算官方 3,514 → 890

V4 主 KV entry：448 B FP8 NoPE + 128 B BF16 RoPE + 8 B scales/padding = 584 B。Indexer 的 MXFP4 entry：128/2 + 128/32 = 68 B。因此全局增长为：

`21 × (584 + 68) / 4 + 20 × 584 / 128 = 3514.25 B/token`。

V4.1 主 KV entry：512/2 + 512/16 = 288 B；index entry 仍为 68 B。KV owner 位于从零编号的 2、8、14、20 层，前三处 2:1 压缩，最后一处 1:1。因此：

`(3/2 + 1) × (288 + 68) = 890 B/token`。

此式不乘 40 层，也不再乘 K/V 的 2。偶数长度正好为 `890×N`；奇数长度应分别取每个 owner 的 `floor(N/r)`。从偶数 N 到 N+1 的全局增量是 356 B，从奇数到下一偶数是 1,424 B；890 是平均增长。SWA 另占 `40×min(N,128)×528 B`，其中 528=512 FP8 值+16 scales。压缩器、分配器、candidate/top-k 缓冲等不包含在这两项中。

在 B=1、N=8192 下，V4 Flash 的生产格式全局 KV 为 28,788,736 B；V4.1 为 7,290,880 B，相差约 3.9486 倍。但逐层主注意力与索引读一次的逻辑载荷分别为 13,165,568 B 和 11,927,552 B，差异远小于存储差异。跨层缓存可复用存储，不代表每层免读；实际 HBM 还取决于 L2、融合、tile 与驻留。

V4.1 后半段的后续 indexer 在生产路径只扫描第一轮生成的候选集合，最多 2048×8=16,384 个 entry。本次结果按该 selective-read 路径计逻辑索引载荷；公开参考代码先对完整 index cache 执行 einsum 再 mask，其读取不能冒充生产优化路径。参考 BF16 cache 与论文生产 FP4 cache 同样分开。

“SSD 降到 1/8”包含 SWA bounded replay 和持久缓存策略的变化，受工作负载影响，不能把任意旧缓存容量机械除以 8。官方图的 V1 389,120 与 V3.2 48,068 B/token 可作为发布图中的历史值引用；本次没有为这两个版本新增独立权重/config 复算，不能把它们标成已验证计算。

## 能力与性能判断

官方 instruct 表在 `reasoning_effort=100`、temperature=1.0、top_p=0.95 下报告：Terminal-Bench 2.1 从 82.7 到 90.6；DeepSWE v1.1 从 54.4 到 74.2；AutomationBench 从 37.7 到 54.8；GPQA Diamond 从 89.9 到 90.9。这支持将新版用于当前 Agent 选型的优先评估，但不是我们的独立实测，也不是所有任务单调改善：base MGSM 从 85.7 到 80.2，AGIEval 从 83.9 到 83.4。不同 HLE 全集/文本子集不能混比。Agent 成绩还依赖 harness、工具、推理预算和上下文设置。

“更快”需要区分输入和输出。新 MoE 的单 token 单层专家矩阵工作更大，但长输入 CED 可跳过多数 decoder token。`v41-flash` 给出三矩阵专家子账：参考全层 prefill、论文 CED+bounded replay prefill、单步 decode。没有将它们标成完整 FLOPs、GPU 时延或服务吞吐；路由、注意力、Engram、mHC、视觉和 DSpark 执行仍待独立接入。

## 书中采用方式

1. 第二章新增跨模型缓存小节，给增长、容量、decode 读取与固定状态的统一口径；V4.1 作为共享 KV/CED 的新例子，保留 V4 Flash 的原始 BF16 计算。
2. 第三章后续有关输入/输出成本的模型扩展应采用 CED 分阶段子账，不能用旧 Flash 的对称全层假设。
3. 第五章 V4 kernel、mHC、量化与 tile 的例子保留原 revision；V4.1 Single-Pass mHC、32×32 FP8 scales 和新 attention layout 需要单独验证。
4. 第六至九章权重容量、前缀恢复、P/D 分离等例子保留已有旧版结果；新版 Engram 放置、EPD 与 bounded replay 用新增案例解释，不沿用旧 GPU 数或读写预算。
5. 第十章训练例子不全局改名：V4.1 新增 Engram/embedding/head 的 Sinkhorn-balanced 更新及 head-wise Muon，优化器状态需要重新建账。

## 可复现命令

```bash
python3 calculations/calc.py v41-flash --length 8192 --batch 1 --format md
python3 calculations/calc.py kv-comparison --length 8192 --batch 1 --format md
python3 calculations/calc.py kv-comparison --length 131072 --format md
python3 calculations/calc.py verify-sources
python3 -m unittest discover -s calculations/tests -p test_v41_kv_comparison.py -v
python3 calculations/research/deepseek-v41-flash/reproduce.py
```

9 个新场景已登记到公共 `scenarios/book.json`，统一 `calc.py reproduce` 会生成它们。上面的专题脚本只刷新本次 18 份 JSON/Markdown 结果并写出 `reproduction.json`，不冒称重跑全书其他实验或刷新旧全局结果 manifest。

当前跨模型表覆盖 12 个独立模型、15 条缓存路径；包括四个 Qwen3、Qwen3.5/3.6、DeepSeek V3/V4 Flash/V4 Pro/V4.1、Kimi K3 和 R1-Distill-Llama-70B。长上下文超出模型原始 config 上限时明确跳过，不默默启用 RoPE 扩展。
