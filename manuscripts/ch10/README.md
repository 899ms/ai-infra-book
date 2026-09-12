# 第十章正文与配图

[阅读版 HTML](../10-训练系统.md) · [正文 Markdown](../10-训练系统.md) · [写作大纲](../../archive/outlines/10-训练系统.md)

六节、24 个小节，约 2.9 万汉字，包含定量例题、261 个公式和十道分层习题。正文先解释数据如何保存、传输和参与计算，再用算例推导显存、耗时与完成期限。32／48 卡设计案例贯穿各节，RL 部分进一步解释阶段协作和策略版本。

全部插图分别提供 SVG、PNG、PDF。图中用张量分片、时间轴、数据路径、注意力面积和曲线解释机制，完整条件和图号位于图片外。HTML 内嵌图片与公式字体，可以离线阅读。

| 图 | 内容 | SVG | PNG | PDF |
|---|---|---|---|---|
| 10-1 | 训练状态与推理权重的容量比较 | [SVG](figure-10-1-state.svg) | [PNG](figure-10-1-state.png) | [PDF](figure-10-1-state.pdf) |
| 10-2 | 容量下界与不同效率下的计算设备数 | [SVG](figure-10-2-budget.svg) | [PNG](figure-10-2-budget.png) | [PDF](figure-10-2-budget.pdf) |
| 10-3 | 参数分片与执行时的完整参数缓冲区 | [SVG](figure-10-3-sharding.svg) | [PNG](figure-10-3-sharding.png) | [PDF](figure-10-3-sharding.pdf) |
| 10-4 | 保存乘积与反向前重建乘积的时间对比 | [SVG](figure-10-4-recompute.svg) | [PNG](figure-10-4-recompute.png) | [PDF](figure-10-4-recompute.pdf) |
| 10-5 | CPU 与 GPU 转换梯度时的传输路径 | [SVG](figure-10-5-casting.svg) | [PNG](figure-10-5-casting.png) | [PDF](figure-10-5-casting.pdf) |
| 10-6 | 分片参与者数与每卡容量 | [SVG](figure-10-6-candidates.svg) | [PNG](figure-10-6-candidates.png) | [PDF](figure-10-6-candidates.pdf) |
| 10-7 | 两种流水的依赖等待与激活保存 | [SVG](figure-10-7-pipeline.svg) | [PNG](figure-10-7-pipeline.png) | [PDF](figure-10-7-pipeline.pdf) |
| 10-8 | 链路占用怎样使归约延迟到计算结束之后 | [SVG](figure-10-8-overlap.svg) | [PNG](figure-10-8-overlap.png) | [PDF](figure-10-8-overlap.pdf) |
| 10-9 | 等长与不等长序列的因果注意力面积 | [SVG](figure-10-9-attention-area.svg) | [PNG](figure-10-9-attention-area.png) | [PDF](figure-10-9-attention-area.pdf) |
| 10-10 | 预取进度与已经完成的训练进度 | [SVG](figure-10-10-input-queue.svg) | [PNG](figure-10-10-input-queue.png) | [PDF](figure-10-10-input-queue.pdf) |
| 10-11 | 从四份权重分片恢复为八份分片 | [SVG](figure-10-11-resharding.svg) | [PNG](figure-10-11-resharding.png) | [PDF](figure-10-11-resharding.pdf) |
| 10-12 | 写带宽与故障时可用恢复点 | [SVG](figure-10-12-recovery.svg) | [PNG](figure-10-12-recovery.png) | [PDF](figure-10-12-recovery.pdf) |
| 10-13 | 保存间隔对保存成本与故障重做成本的相反影响 | [SVG](figure-10-13-save-interval.svg) | [PNG](figure-10-13-save-interval.png) | [PDF](figure-10-13-save-interval.pdf) |
| 10-14 | 生成验证学习的处理瓶颈与权重反馈 | [SVG](figure-10-14-rl-flow.svg) | [PNG](figure-10-14-rl-flow.png) | [PDF](figure-10-14-rl-flow.pdf) |
| 10-15 | 权重同步次序与显存峰值 | [SVG](figure-10-15-rl.svg) | [PNG](figure-10-15-rl.png) | [PDF](figure-10-15-rl.pdf) |
| 10-16 | 同步等待与跨批次异步执行的时间对比 | [SVG](figure-10-16-async-cycle.svg) | [PNG](figure-10-16-async-cycle.png) | [PDF](figure-10-16-async-cycle.pdf) |
| 10-17 | 重放离散选择与重算当前数值 | [SVG](figure-10-17-replay.svg) | [PNG](figure-10-17-replay.png) | [PDF](figure-10-17-replay.pdf) |
| 10-18 | 32卡与48卡方案的完成时间分解 | [SVG](figure-10-18-deadline.svg) | [PNG](figure-10-18-deadline.png) | [PDF](figure-10-18-deadline.pdf) |
| 10-19 | 通信带宽变化对每步耗时的影响 | [SVG](figure-10-19-hardware.svg) | [PNG](figure-10-19-hardware.png) | [PDF](figure-10-19-hardware.pdf) |
| 10-20 | 给定期限下模型规模与设备数边界 | [SVG](figure-10-20-scale.svg) | [PNG](figure-10-20-scale.png) | [PDF](figure-10-20-scale.pdf) |

## 来源与复现

[阅读记录](reading-notes.md)注明 calculations、survey、案例与已有实验的阅读范围和采用方式。[sources.json](sources.json)锁定来源文件，[figure-data.json](figure-data.json)保存作图数值及事件，[manifest.json](manifest.json)保存输出校验值。没有执行新的 GPU 训练或增加未测得的跨硬件性能结果。

在仓库根目录执行：

```sh
python3 -m venv /tmp/ch10-book-venv
/tmp/ch10-book-venv/bin/pip install -r manuscripts/ch10/requirements.txt
/tmp/ch10-book-venv/bin/python manuscripts/ch10/build.py
python3 manuscripts/ch10/verify.py
```

构建需要 Node.js 和中文字体；默认寻找 macOS Arial Unicode 或 Linux Noto CJK，可用 `--font /path/to/font` 指定。公式复用仓库已有的 `manuscripts/ch06/vendor/katex`（0.16.11，许可证同目录），无需构建时下载。来源哈希不匹配会停止生成，须审阅变化再更新锁文件。

浏览器校验为可选步骤，需要 Playwright 和 Chrome：

```sh
/tmp/ch10-book-venv/bin/pip install playwright
/tmp/ch10-book-venv/bin/python manuscripts/ch10/browser-check.py --executable /path/to/chrome
```

## 校验

[内容与数据校验](validation.json)覆盖 outline 对齐、全部题号与外部图注、原始数据、图内无图号、插入公式、关键算术和本地链接。[公式校验](math-validation.json)记录公式渲染结果，[布局检查](figure-layout-check.json)记录图片文字边界。[浏览器检查](browser-validation.json)检查 1440 px 与 390 px 阅读视口中的图片、公式、锚点和页面宽度。

[桌面预览](preview-desktop.png) · [手机预览](preview-mobile.png) · [流水图文预览](preview-desktop-pipeline.png)。复杂时序图可通过上表中的 SVG／PDF 放大阅读。

本轮[定量叙述修订记录](revisions/quantitative-prose/README.md)说明算例展开、数字精度与插图重组。

最新[教学结构修订记录](revisions/teaching-structure/README.md)说明全章连贯重写。[贯穿设计题](design-case.md)给出输入与推导，运行 `python3 manuscripts/ch10/design-case.py` 可独立复算。

已完成全章术语和中文句式修订，详见[修订说明](revisions/chinese-terminology/README.md)。

本轮[图示与段落衔接修订](revisions/visual-explanation/README.md)新增十一幅机制图，并按阅读顺序统一编号。旧版图号对应关系见 [figure-number-map.json](figure-number-map.json)。新图由 [mechanism-figures.py](mechanism-figures.py) 生成，统一通过 build.py 构建。

## 当前阅读版配图（2026-09-10）

正文现引用 46 幅图，以下清单按当前阅读顺序列出；上文旧图号用于追溯构建记录。

| 图号 | 内容 | SVG | PNG | PDF |
| --- | --- | --- | --- | --- |
| 10-1 | 从输入和当前权重出发，前向得到损失，反向得到参数梯度，Adam 生成新权重。前向阶段保留的激活用于反向；更新过程还读取高精度主权重和梯度历史。 | [SVG](figure-10-update-cycle.svg) | [PNG](figure-10-update-cycle.png) | [PDF](figure-10-update-cycle.pdf) |
| 10-2 | 五类训练状态合计相当于八份 BF16 权重的容量。模型为 Qwen3-8B，采用表中数据格式；横轴表示各类状态累计占用的容量。 | [SVG](figure-10-1-state.svg) | [PNG](figure-10-1-state.png) | [PDF](figure-10-1-state.pdf) |
| 10-3 | 矩阵计算效率为 30% 时所需的卡数。任务为 Qwen3-8B 处理 100B token，序列长 8192，全部 30 天用于执行；蓝柱为计算需求，橙色菱形为训练状态容量下限。A100 为 80 GB SXM，H100 为 SXM。 | [SVG](figure-10-2-budget.svg) | [PNG](figure-10-2-budget.png) | [PDF](figure-10-2-budget.pdf) |
| 10-4 | 矩阵计算效率提高到 40%，同一任务所需的卡数下降；橙色菱形仍表示状态容量下限。各下限均以卡数计量；容量项是显存约束要求的最少卡数。 | [SVG](figure-10-budget-1.svg) | [PNG](figure-10-budget-1.png) | [PDF](figure-10-budget-1.pdf) |
| 10-5 | 矩阵计算效率为 50% 时所需的卡数。三图使用相同的型号顺序、纵轴范围、任务与 30 天执行期限。各下限均以卡数计量；容量项是显存约束要求的最少卡数。 | [SVG](figure-10-budget-2.svg) | [PNG](figure-10-budget-2.png) | [PDF](figure-10-budget-2.pdf) |
| 10-6 | 普通 DP：每卡保存完整权重、梯度、主权重和两份矩状态。 | [SVG](figure-10-zero-0.svg) | [PNG](figure-10-zero-0.png) | [PDF](figure-10-zero-0.pdf) |
| 10-7 | ZeRO-1：主权重和两份矩状态按参数分片，权重与梯度仍完整复制。 | [SVG](figure-10-zero-1.svg) | [PNG](figure-10-zero-1.png) | [PDF](figure-10-zero-1.pdf) |
| 10-8 | ZeRO-2：进一步划分梯度，每卡只保留归属于自己的梯度分片。 | [SVG](figure-10-zero-2.svg) | [PNG](figure-10-zero-2.png) | [PDF](figure-10-zero-2.pdf) |
| 10-9 | ZeRO-3：权重也分片。执行模块时，各卡通过通信取得所需的完整权重。 | [SVG](figure-10-zero-3.svg) | [PNG](figure-10-zero-3.png) | [PDF](figure-10-zero-3.pdf) |
| 10-10 | 同一模块的权重平时分散在四张卡上；执行时，各卡收集完整权重。图中展开 GPU 0 的收集过程，四种颜色分别表示四份参数分片。完整权重缓冲区用完即可释放，各卡长期保存的原始分片仍然保留。 | [SVG](figure-10-3-sharding.svg) | [PNG](figure-10-3-sharding.png) | [PDF](figure-10-3-sharding.pdf) |
| 10-11 | 矩阵反向产生两路梯度：dX 交给前一层继续反向，dW 交给本层的归约和参数更新。两路计算都读取上游梯度 dY。 | [SVG](figure-10-gradient-branches.svg) | [PNG](figure-10-gradient-branches.png) | [PDF](figure-10-gradient-branches.pdf) |
| 10-12 | 保留乘积 h：蓝色条表示一直保留的 a、u，橙色条表示从前向持续到下投影反向的乘积 h。128 个 token 的 micro-batch 采用 FP32，h 的形状为 [128,12288]，占 6 MiB。 | [SVG](figure-10-4-recompute.svg) | [PNG](figure-10-4-recompute.png) | [PDF](figure-10-4-recompute.pdf) |
| 10-13 | 保留 a、u，反向使用前重新相乘得到 h。橙色的 6 MiB 缓冲只在使用前后短暂存在；横轴表示操作顺序。 | [SVG](figure-10-recompute-rebuild.svg) | [PNG](figure-10-recompute-rebuild.png) | [PDF](figure-10-recompute-rebuild.pdf) |
| 10-14 | 先将 96 MiB BF16 梯度传到 CPU，再在 CPU 转为 192 MiB FP32。箭头表示数据流；转换的输入与输出均位于 CPU 一侧。 | [SVG](figure-10-5-casting.svg) | [PNG](figure-10-5-casting.png) | [PDF](figure-10-5-casting.pdf) |
| 10-15 | 先在 GPU 将 96 MiB BF16 梯度转为 192 MiB FP32，再传到 CPU。转换时输入与输出共存，GPU 峰值为 288 MiB。 | [SVG](figure-10-casting-gpu.svg) | [PNG](figure-10-casting-gpu.png) | [PDF](figure-10-casting-gpu.pdf) |
| 10-16 | 给定附加存储需求时，分片数决定哪些方案满足容量要求。曲线为 $16N/d+10$ GiB，水平线为 RTX 4090 每卡 22 GiB 可用显存。曲线低于预算的区域可以容纳这些训练状态和缓冲区；纵向距离给出容量余量。 | [SVG](figure-10-6-candidates.svg) | [PNG](figure-10-6-candidates.png) | [PDF](figure-10-6-candidates.pdf) |
| 10-17 | 填满排空先完成八个 micro-batch 的前向，再执行反向，最后更新参数。蓝色为前向，橙色为反向，绿色为参数更新。四个阶段共用同一时间刻度，按正文的计算与传输条件共需 337 ms。 | [SVG](figure-10-7-pipeline.svg) | [PNG](figure-10-7-pipeline.png) | [PDF](figure-10-7-pipeline.pdf) |
| 10-18 | 1F1B 在预热后交错前向和反向，本例完成时间为 347 ms。蓝色为前向，橙色为反向，绿色为参数更新；与前图使用相同时间刻度。 | [SVG](figure-10-pipeline-1f1b.svg) | [PNG](figure-10-pipeline-1f1b.png) | [PDF](figure-10-pipeline-1f1b.pdf) |
| 10-19 | 放大 1F1B 的阶段 3：第二个 micro-batch 在 93 ms 结束反向，下一份前向输入于 95 ms 到达，形成 2 ms 等待。 | [SVG](figure-10-pipeline-gap.svg) | [PNG](figure-10-pipeline-gap.png) | [PDF](figure-10-pipeline-gap.pdf) |
| 10-20 | 两种调度中各阶段的激活与收发缓冲峰值。提前反向使激活更早释放，最大值由约 2.57 GB 降到 0.97 GB。 | [SVG](figure-10-pipeline-memory.svg) | [PNG](figure-10-pipeline-memory.png) | [PDF](figure-10-pipeline-memory.pdf) |
| 10-21 | 交错式 1F1B（$v=2$）的各阶段时间线，完成时间 298 ms。蓝色为前向，橙色为反向，绿色为参数更新，斜线块为每卡的第二个层块。每个块约为图 10-18 中的一半长，预热与排空阶段的空隙被另一个层块的计算填上，阶段 3 的第一个前向从 33 ms 提前到约 20 ms；每个 micro-batch 要多穿过四条边界。 | [SVG](figure-10-pipeline-interleaved.svg) | [PNG](figure-10-pipeline-interleaved.png) | [PDF](figure-10-pipeline-interleaved.pdf) |
| 10-22 | 零气泡（ZB-H1）的各阶段时间线，完成时间 283 ms。蓝色为前向，橙色为 $dX$，紫色为 $dW$，绿色为参数更新。稳态中每个阶段按前向、$dX$、$dW$ 轮转，图 10-18 里反向之间的依赖空隙和末尾的排空空隙都被延后的 $dW$ 填上，四个阶段几乎同时结束；阶段 3 的 $dW$ 比 $dX$ 晚三个 micro-batch，那里的激活保留得最久。 | [SVG](figure-10-pipeline-zero-bubble.svg) | [PNG](figure-10-pipeline-zero-bubble.png) | [PDF](figure-10-pipeline-zero-bubble.pdf) |
| 10-23 | DualPipe 的各阶段时间线，完成时间 306 ms。颜色同图 10-22，斜线块为从阶段 3 进入的另一半 micro-batch（反方向）的计算。每个阶段同时承载两个方向，一个方向的预热和排空空隙由另一个方向的块填上；代价是每卡保存两份参数。 | [SVG](figure-10-pipeline-dualpipe.svg) | [PNG](figure-10-pipeline-dualpipe.png) | [PDF](figure-10-pipeline-dualpipe.pdf) |
| 10-24 | 四种流水线调度在八个与十六个 micro-batch 下的完成时间，以及八个 micro-batch 时各调度最大的单阶段激活与收发缓冲峰值。四种调度使用相同的前向 10 ms、反向 20 ms、边界传输 1 ms、参数更新 1 ms 条件。 | [SVG](figure-10-pipeline-schedules.svg) | [PNG](figure-10-pipeline-schedules.png) | [PDF](figure-10-pipeline-schedules.pdf) |
| 10-25 | 链路空闲时，3 ms 归约（橙色）可以在 5 ms 独立计算（蓝色）结束前完成。虚线标出计算结束。 | [SVG](figure-10-8-overlap.svg) | [PNG](figure-10-8-overlap.png) | [PDF](figure-10-8-overlap.pdf) |
| 10-26 | 链路先被其他通信占用 4 ms（灰色），归约推迟到 4—7 ms。虚线后多出的 2 ms 延长训练步。 | [SVG](figure-10-overlap-busy.svg) | [PNG](figure-10-overlap-busy.png) | [PDF](figure-10-overlap-busy.pdf) |
| 10-27 | Qwen3-235B-A22B 的路由形状（E=128、k=8、8,192 个 token、一半专家 1.5 倍热）下，容量因子增大时丢弃的 dispatch 占比下降、补零行占比上升。 | [SVG](figure-10-moe-capacity.svg) | [PNG](figure-10-moe-capacity.png) | [PDF](figure-10-moe-capacity.pdf) |
| 10-28 | 两条 4096 个 token 的序列的因果注意力配对。每个查询 token 读取本序列中不晚于自己的位置，形成两个三角形；两条序列的注意力计算彼此独立，总配对数为 16781312。 | [SVG](figure-10-9-attention-area.svg) | [PNG](figure-10-9-attention-area.png) | [PDF](figure-10-9-attention-area.pdf) |
| 10-29 | 相同 8192 个 token 改分为 7168 与 1024，总因果配对数增至 26218496。较长序列对应三角形增加的面积，超过了较短序列对应三角形减少的面积。 | [SVG](figure-10-attention-unequal.svg) | [PNG](figure-10-attention-unequal.png) | [PDF](figure-10-attention-unequal.pdf) |
| 10-30 | 训练已完成 batch 100，预取任务已安排到 108。中间八个 batch 仍需训练，其中一部分已经准备好，另一部分还在处理。虚线框示意尚在处理的 batch。恢复时应保留这些数据或重新准备它们，从 batch 101 继续。 | [SVG](figure-10-10-input-queue.svg) | [PNG](figure-10-10-input-queue.png) | [PDF](figure-10-10-input-queue.pdf) |
| 10-31 | 横向位置对应原矩阵的行号，颜色表示旧分片。每份旧分片分成前后两半后，分别存入两个新分片。模型权重的内容和顺序保持相同，改变的是各卡负责的行范围；BF16 权重总量始终为 96 MiB。上方“旧”编号标识原分片，下方编号标识重新分配后的分片。 | [SVG](figure-10-11-resharding.svg) | [PNG](figure-10-11-resharding.png) | [PDF](figure-10-11-resharding.pdf) |
| 10-32 | 捕获一致的训练状态，复制到独立缓冲后允许训练继续；后台写完数据并提交完整快照后，恢复程序才使用这份 checkpoint。箭头表示先后依赖。 | [SVG](figure-10-checkpoint-commit.svg) | [PNG](figure-10-checkpoint-commit.png) | [PDF](figure-10-checkpoint-commit.pdf) |
| 10-33 | 两份 112 GB 快照以 7 GB/s 写入，各先花 0.5 s 复制到缓冲（橙色），随后上传（蓝色）。50 s 故障时第一份已提交，第二份尚未提交；斜线为无故障时剩余上传，空心点为原定提交时刻。 | [SVG](figure-10-12-recovery.svg) | [PNG](figure-10-12-recovery.png) | [PDF](figure-10-12-recovery.pdf) |
| 10-34 | 相同快照以 20 GB/s 写入，于 26.1、46.1 s 提交。50 s 故障时可以恢复到 40 s 的训练状态，只需重做 10 s。 | [SVG](figure-10-recovery-fast.svg) | [PNG](figure-10-recovery-fast.png) | [PDF](figure-10-recovery-fast.pdf) |
| 10-35 | 蓝线为保存耗时占比，橙线为故障重做耗时占比，绿线为两者加上恢复耗时后的合计。使用 1024 卡作业平均 7.9 小时中断一次、保存约 16.4 s 和恢复 120 s 的一阶模型。最低点出现在两项随间隔变化的代价相互平衡处。 | [SVG](figure-10-13-save-interval.svg) | [PNG](figure-10-13-save-interval.png) | [PDF](figure-10-13-save-interval.pdf) |
| 10-36 | 三阶段分别最多处理 12、6、8 条等长轨迹/s。验证后保留 75%，所以只有 4.5 条/s 进入学习。返回箭头表示学习产生的新权重影响后续生成；其同步耗时在后面的阶段切换与异步算例中展开。 | [SVG](figure-10-14-rl-flow.svg) | [PNG](figure-10-14-rl-flow.png) | [PDF](figure-10-14-rl-flow.pdf) |
| 10-37 | 先加载生成权重并分配 KV 池，再释放训练状态，峰值约为 83.3 GiB，超过 H100 SXM 的 74.5 GiB。横轴按操作顺序排列。 | [SVG](figure-10-15-rl.svg) | [PNG](figure-10-15-rl.png) | [PDF](figure-10-15-rl.pdf) |
| 10-38 | 先加载生成权重，再释放训练状态，最后分配 KV 池。峰值降为约 59.3 GiB；两图共用 74.5 GiB 容量线和同一纵轴。 | [SVG](figure-10-rl-staged.svg) | [PNG](figure-10-rl-staged.png) | [PDF](figure-10-rl-staged.pdf) |
| 10-39 | 固定版本服务与策略训练的权重生命周期。上方 ROM 重复提供同一版本；下方训练产生新版本并发布给生成端。KV 写入与权重更新使用不同的数据通路。 | [SVG](figure-10-weight-update.svg) | [PNG](figure-10-weight-update.png) | [PDF](figure-10-weight-update.pdf) |
| 10-40 | μ 产生训练样本，πold 标识本轮优化的起点，πθ 随本轮更新变化。虚线表示版本演进顺序。三个概率必须针对同一前缀与同一 token 计算。 | [SVG](figure-10-policy-versions.svg) | [PNG](figure-10-policy-versions.png) | [PDF](figure-10-policy-versions.pdf) |
| 10-41 | 同步循环依次生成本批样本、学习本批样本、同步权重，分别用时 40、16、4 s，共 60 s。 | [SVG](figure-10-16-async-cycle.svg) | [PNG](figure-10-16-async-cycle.png) | [PDF](figure-10-16-async-cycle.pdf) |
| 10-42 | 稳态中生成下一批与学习上一批在独立资源上重叠；两者完成后同步权重，周期为 44 s。橙色同步阶段阻塞两侧。 | [SVG](figure-10-async-overlap.svg) | [PNG](figure-10-async-overlap.png) | [PDF](figure-10-async-overlap.pdf) |
| 10-43 | 离散专家 ID 连接生成端与训练端，当前权重继续参与数值计算。示意记录为样本 A、token 17、层 3 的 top-2 选择；虚线表示 ID 重放，实线表示当前计算数据流。 | [SVG](figure-10-17-replay.svg) | [PNG](figure-10-17-replay.png) | [PDF](figure-10-17-replay.pdf) |
| 10-44 | 每条横条依次累计基础训练时间、保存与故障恢复的附加时间，以及预留的 5 天计划性停顿。基础训练时间已经包括通信和输入等待；橙色小段为 checkpoint 模型得到的额外耗时。两套方案使用相同任务和全局 batch，虚线标出 30 天期限。 | [SVG](figure-10-18-deadline.svg) | [PNG](figure-10-18-deadline.png) | [PDF](figure-10-18-deadline.pdf) |
| 10-45 | 资源能力变化的收益由原有等待时间占比决定。曲线按 $T'/T=1-f+f/r$ 计算，固定单卡计算与依赖，通信时间与有效能力成反比。 | [SVG](figure-10-19-hardware.svg) | [PNG](figure-10-19-hardware.png) | [PDF](figure-10-19-hardware.pdf) |
| 10-46 | 固定 90 天执行期限，稠密模型规模增大要求更多的卡。数据量为 20T token，算法工作为 $6ND$，实线的 MFU 为 40%，虚线为 50%，使用 BF16 稠密矩阵峰值。各线为向上取整前的连续计算边界；横线标出 16,384 张卡。 | [SVG](figure-10-20-scale.svg) | [PNG](figure-10-20-scale.png) | [PDF](figure-10-20-scale.pdf) |
