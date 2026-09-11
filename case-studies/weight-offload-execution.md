# 权重卸载的容量、流量与执行位置

核对于 2026-09-08，用于第 8.4→9.3 的既有实验。[原始资料与读取范围](../references/framework-history/2026-09-08/offload-execution/README.md)包括 2024／2025 的 vLLM 实现、2026 的预取与选择性卸载、SGLang 两条执行路径及 Ollama runner。源码只静态读取；以下数字是固定模型配置与明确假设的推算，没有运行框架或测量硬件性能。

## 从权重放在哪里到计算发生在哪里

vLLM v0.6.0（2024）的所读 helper 将部分参数放到主存，每次前向再构造 GPU 参数并执行；`non_blocking` 本身不保证下一层已被提前搬好。v0.9.2（2025）的 V1 路径要求 UVA 支持，让 GPU 通过映射访问主存参数，旧路径仍保留按需搬入。UVA 减少显式管理，不消除 CPU—GPU 链路上的数据流；也不表示矩阵乘法已经转给 CPU。离散 PCIe、Grace 的一致性互联与 Apple 统一内存需要各自的带宽和拓扑预算。

2026 年的变化是把“选哪些参数”和“何时准备权重”进一步分开：选择性卸载 PR 于 2 月 14 日合入，预取 PR 于 2 月 26 日合入，3 月 7 日的 [vLLM v0.17.0 发布说明](https://github.com/vllm-project/vllm/releases/tag/v0.17.0)同时列出这两项能力。固定当前实现按层分组、参数名称选择卸载对象，用独立复制流和静态 GPU 缓冲准备未来层，再通过依赖事件让计算等待对应权重。计算图还必须表达缓冲何时可复用，不能为了重叠覆盖仍在读取的权重。

这条预取路径明确借鉴 SGLang 的实现；[2025 年 GB200 公告](../references/framework-history/2026-09-08/overlap-placement/sglang-gb200-2025-sept.md)已用较快主存互联换取更小的 EP 规模。当前 SGLang 通用 offloader 与 KT wrapper 则解决不同问题：前者搬权重供 GPU 计算，后者提交 CPU 专家工作，同时运行 GPU 专家，最后合并结果。不能因为两者都使用主存，就按同一种 PCIe 载荷计算。

Ollama 的 GPU layer offload 又是另一种用法：runner 选择哪些层交给 GPU。2024 的所读入口把层数传给 llama.cpp server；2025 新引擎加入分配反馈；2026 v0.30 的 GGUF 路径与 MLX 并存，当前默认让 llama-server 自动选 GPU 层。v0.30.0 GitHub 发布记录为 5 月 13 日，[对应公告](https://ollama.com/blog/improved-performance-and-model-support-with-gguf)为 6 月 5 日，两个日期分别保存。

实际诊断要看层放置与阶段耗时。当前 Ollama 的内存报告在文本模型层全部放到 GPU 时可显示 100% GPU；这不是 GPU 利用率，也不保证每个辅助阶段都在 GPU。所读启动路径会在部分文本卸载或容量不足等条件下把多模态 projector 留在 CPU。对于每轮新截图的 Computer Use，应单独计图像处理与语言模型 TTFT，不能仅凭驻留比例判断速度。mmap 的文件映射跨度、实际驻留页、CPU 重打包副本与设备分配也不能全部相加。

## Qwen3-8B：省下的显存能换来多少 KV

沿[固定配置](../references/outline-checks/2026-09-07/scaling-history/qwen3-8b-config.json)，一层 FFN 的 gate、up、down 矩阵共 `3 × 4096 × 12288 = 150994944` 个参数，BF16 为 **288 MiB**。融合 gate／up 改变实现的张量组织，不改变这组三矩阵的总参数。

36 层按每四层卸载最后一层的 FFN，共卸载九份、**2.53125 GiB**。假定参数形状、布局一致，当前 vLLM 静态池可在不同层之间复用同一组缓冲：

| 预取缓冲组数 | 预取缓冲占用 | 扣除缓冲后的权重净节省 | 相当于多少条独立 8K BF16 KV |
| --- | ---: | ---: | ---: |
| 1 | 0.28125 GiB | 2.25 GiB | 2 条 |
| 2 | 0.5625 GiB | 1.96875 GiB | 1 条，另余 0.84375 GiB |

Qwen3-8B 的每条 8192-token KV 为 `2 × 36 × 8 × 128 × 2 × 8192 = 1.125 GiB`。这里仅比较 FFN 权重与逻辑 KV，未计页碎片、图池、其他权重及工作区；剩余容量不是完整服务已可行的证明。更多预取缓冲可以给复制更长的提前量，也会挤占能服务的上下文。真实参数如果有不同 shape、stride、dtype 或量化后的临时张量，要按实际池分组求和。

再算每步流量。若这九份 FFN 权重每次模型前向都需重新搬入，每步要经 CPU—GPU 链路复制 2,717,908,992 字节（2.72 GB）。经 PCIe Gen5 x16（每方向 64 GB/s），纯复制服务时间至少为 `2.72 GB / 64 GB/s ≈ 42.47 ms`；增加预取距离不会改变这些字节，也不会把这个共享链路的稳态工作量消掉。换成 GH200 的 NVLink-C2C，同一项约为 6.04 ms：它的 900 GB/s 是收发两个方向的合计，单向复制按每方向 450 GB/s 计算。两档链路与第 8.4 节的[PCIe Gen5 算例](../calculations/results/weight-offload-pcie5.md)、[NVLink-C2C 算例](../calculations/results/weight-offload-gh200-c2c.md)一致，C2C 带宽见 [GH200 架构说明](../references/files/documents/nvidia-grace-hopper-blog.md)。

经 PCIe Gen5 x16，单份 FFN 复制约 4.72 ms。只有未来层需要权重之前有足够独立计算，且各轮复制能跟上消费，才可能隐藏等待；还要画出首次准备、环回预取和最后汇合。GPU 计算、KV 读写、其他传输占用同一路径时应重新 profile，不能只对独占时间取 `max` 就宣布流水可行。

同一步若给四条请求各生成一个 token，复制字节可由四个输出分摊，PCIe Gen5 链路单项给出的总吞吐上限约为 **94.19 token/s**，但每条请求的步间隔下界仍约 42.47 ms。一次 2048-token prefill 同样能复用这份权重，摊到输入 token 的复制服务时间约 0.0207 ms；完整 TTFT 仍要加计算和准备。扩大批量前先检查 KV 是否放得下，不能用摊销后的总吞吐代替交互延迟。

这里假设每步完整搬入所选 FFN，是预取路径的教学模型。MoE 的 UVA 访问可以只触及被路由到的部分，但实际 kernel tile、量化布局和缓存会造成重读；显式预取整块专家张量则可能搬入未被当前 token 选中的专家。按真实访问方式核字节，不能一律用激活参数或总参数代替。

同一份 288 MiB 权重还可以接到第 6 章的内存借用：源端更快是否真的缩短 GPU 等待，取决于下游链路与预取提前量。[分层内存算例](memory-criticality-and-tiering.md)继续计算迁移成本与未来复用的交点，并区分 CPU 页放置和实际引擎缓冲的管理条件。

## Qwen3-235B：把权重搬过来，还是把计算留在主存

接回[独立活跃专家算例](moe-and-startup.md)：一层有 128 个专家，每 token 选 8 个；单专家 BF16 三矩阵为 36 MiB。教学固定 32 个专家驻留 GPU，其余 96 个留在 CPU；各 token 独立均匀选 8 个不同专家，仅为可复算的路由假设。若本步处理 m 个 token，则 CPU 侧不同专家期望为 `96 × [1 − (15/16)^m]`，CPU 专家任务数期望为 `6m`。不同专家数决定可复用的权重载荷，任务数决定计算量，两者分别计算。

用第 9.3 节例 9.3 的同一台实验机（KTransformers 论文平台）：单颗 Xeon Platinum 8452Y，同插槽 DDR5 带宽按论文的 Intel MLC 实测取 220 GB/s，PyTorch AVX-512 内核与 AMX 内核分别按论文实测的 1.8 与 21.3 TFLOP/s 计；GPU 为 A100 40GB PCIe，按峰值的 50% 计 156 TFLOP/s；H2D 经 PCIe 4.0 x16 按 25 GB/s 计。对留在主存的部分，CPU 用 `max(权重字节／DRAM带宽, FLOPs／CPU效率)` 求资源下界；搬到 GPU 的对照先整批搬权重、再计算，作为明确的串行估算：

| 本步 token 数 | CPU 侧不同专家期望 | CPU 资源下界 | 先搬权重再 GPU 计算的估算 |
| --- | ---: | ---: | ---: |
| 1，单请求 decode | 6 | 约 1.03 ms，DRAM 主导（两种内核相同） | 约 9.06 ms，H2D 主导 |
| 2048，一次 prefill chunk | 接近 96 | AVX-512 约 257.7 ms；AMX 约 21.8 ms，均为计算主导 | 约 147.9 ms，H2D＋计算 |

这还没有计 CPU 的激活交接、路由、NUMA 远端访问、GPU 常驻专家与同步。只按一份输入 hidden state 和一份合并输出估算，BF16 往返载荷为 `2 × m × 4096 × 2` 字节：m=1 为 16 KiB，m=2048 为 32 MiB，另加路由元数据。小载荷仍可能被逐层启动延迟主导；与第 9.3.4 的交接频次相接。

结果说明 CPU 就地计算可以省掉低批量时的专家权重搬移；prefill 增大后，AVX-512 内核先碰到 CPU 算力，就地计算反比搬运路径更慢，而 AMX 内核仍快于搬运——同一台机器上，CPU 用哪套指令就改变执行位置的选择，与例 9.3 的交点分析一致。两边并行时，应比较整层关键路径，而非把 CPU 与 GPU 工作简单串行相加。表格未计量化与缓存的影响；实际 SGLang／KT 常使用 CPU AMXINT4 与 GPU FP8 等不同格式，必须重算载荷并保留质量条件，不能将 BF16 算例当成混合精度配置的预测值。

## 公开成绩怎样进入实验

[SGLang 2025 年 KT 公告](https://www.lmsys.org/blog/2025-10-22-KTransformers/)既讲单 GPU 的原项目实验，也给多 GPU 集成预览，需分开引用。其 ShareGPT 示例的 CPU 参数为 AMXINT4，GPU 服务名中的 FP8 不说明全部权重均为 FP8；227.85 是输入加输出总 token/s，输出为 87.58 token/s，median／p99 ITL 约 299／1935 ms。它不能支持“每请求 220 token/s”的说法，也不能把 R1／V3 改名为本书的 V4／K3。

同层的 submit→GPU compute→CPU sync/merge 可以保持原依赖。Expert Deferral 则把部分贡献延后到其他层，公告明确承认模型行为变化；不能仅以存在残差连接解释为天然等价。固定当前 KT wrapper 将 deferral 参数传给后端，并在末层禁止继续延后。实验先关闭 deferral，再单独比较时间和任务质量；本轮没有审查 kt-kernel 内部调度或证明任意模型的误差界。

vLLM 预取 PR 的两卡／四卡原始结果为总请求率 18.04／33.82 request/s，即每卡约 9.02／8.455。原结果小标题不能代替归一化；两者均只输出一个 token，适合看 prefill 与资源效率，不能据此预测长 decode 的 TPOT。选择性卸载 PR 的示例则使用 `--load-format dummy` 和极少请求，只证明所述形状下的性能测试，不能当作真实 Kimi 权重的质量验证。

## 回到大纲

8.4 用 Qwen3-8B 的缓冲与 KV 算例解释容量、预取和摊销；实验 8-5 保留本地大模型主例，增加小模型卸载变体。9.3 用真实 SGLang／KT submit-compute-sync 路径解释 CPU 专家、混合格式、批量与质量；实验 9-3／9-5 先做同一矩阵的纸笔估算，再用受支持的实际引擎记录检验。图 8-4／9-3 增加权重／激活方向和缓冲标注，维持原实验与图号。
