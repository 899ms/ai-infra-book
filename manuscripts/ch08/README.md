# 第八章正文与配图

[阅读版 HTML](../08-推理优化.md) · [正文 Markdown](../08-推理优化.md) · [写作大纲](../../archive/outlines/08-单实例推理.md)

正文按执行基线、批处理、KV 生命周期、压缩与卸载、推测解码、服务选择六节展开，共 22 个小节、九项分层练习。贯穿设计采用 RTX PRO 6000 Blackwell 工作站版上分给实例的 32 GiB、12 GiB 状态预算、2K／8K 输入、256 输出和 7 秒期限；时间由实验 8-1 的效率表（[efficiency.json](../../experiments/ch08/08-01/efficiency.json)）与实验 8-5 的实测推出。章末综合例题完成容量、时间和 GPU 占用的比较，并通过内存预算和输出长度变化解释最优方案变化。

十五幅插图提供 SVG、PNG 和 PDF。图号与完整 caption 放在图片外；HTML 内嵌图片、公式和字体，可离线阅读并点击放大。

| 图 | 内容 | SVG | PNG | PDF |
|---|---|---|---|---|
| 8-1 | 请求时间线 | [SVG](figure-8-1-lifecycle.svg) | [PNG](figure-8-1-lifecycle.png) | [PDF](figure-8-1-lifecycle.pdf) |
| 8-2 | 批量与读取量 | [SVG](figure-8-2-batch.svg) | [PNG](figure-8-2-batch.png) | [PDF](figure-8-2-batch.pdf) |
| 8-3 | 调度与输出间隔 | [SVG](figure-8-3-scheduling.svg) | [PNG](figure-8-3-scheduling.png) | [PDF](figure-8-3-scheduling.pdf) |
| 8-4 | 分块注意力访问范围 | [SVG](figure-8-4-attention.svg) | [PNG](figure-8-4-attention.png) | [PDF](figure-8-4-attention.pdf) |
| 8-5 | 分页与共享 | [SVG](figure-8-5-pages.svg) | [PNG](figure-8-5-pages.png) | [PDF](figure-8-5-pages.pdf) |
| 8-6 | 多轮前缀结构 | [SVG](figure-8-6-prefix.svg) | [PNG](figure-8-6-prefix.png) | [PDF](figure-8-6-prefix.pdf) |
| 8-7 | 同一缓存空间的两种用法 | [SVG](figure-8-7-cache-choice.svg) | [PNG](figure-8-7-cache-choice.png) | [PDF](figure-8-7-cache-choice.pdf) |
| 8-8 | KV 分组格式 | [SVG](figure-8-8-kv-format.svg) | [PNG](figure-8-8-kv-format.png) | [PDF](figure-8-8-kv-format.pdf) |
| 8-9 | 预取缓冲与容量 | [SVG](figure-8-9-offload.svg) | [PNG](figure-8-9-offload.png) | [PDF](figure-8-9-offload.pdf) |
| 8-10 | KV／Q 精度与质量 | [SVG](figure-8-10-kv-quality.svg) | [PNG](figure-8-10-kv-quality.png) | [PDF](figure-8-10-kv-quality.pdf) |
| 8-11 | 草稿验证与修正 | [SVG](figure-8-11-verification.svg) | [PNG](figure-8-11-verification.png) | [PDF](figure-8-11-verification.pdf) |
| 8-12 | 查询开销与推测收益 | [SVG](figure-8-12-speculation.svg) | [PNG](figure-8-12-speculation.png) | [PDF](figure-8-12-speculation.pdf) |
| 8-13 | 到达率与有效吞吐 | [SVG](figure-8-13-service.svg) | [PNG](figure-8-13-service.png) | [PDF](figure-8-13-service.pdf) |
| 8-14 | 配置的容量与时间 | [SVG](figure-8-14-design.svg) | [PNG](figure-8-14-design.png) | [PDF](figure-8-14-design.pdf) |
| 8-15 | 局部加速与完整任务 | [SVG](figure-8-15-task.svg) | [PNG](figure-8-15-task.png) | [PDF](figure-8-15-task.pdf) |

## 来源与构建

先读已有 calculations 与 survey，再据此写作；采用范围见[阅读记录](reading-notes.md)。[来源锁](sources.json)保存实际采用文件的 SHA-256，[图数据](figure-data.json)保存绘图输入，[产物清单](manifest.json)记录正文、HTML 和图文件的校验值。模型性能来自已有记录，本轮没有重新执行 GPU 实验。

在仓库根目录运行：

```sh
python3 -m venv /tmp/ch08-book-venv
/tmp/ch08-book-venv/bin/pip install -r manuscripts/ch08/requirements.txt
/tmp/ch08-book-venv/bin/python manuscripts/ch08/build.py
/tmp/ch08-book-venv/bin/python manuscripts/ch08/verify.py
```

需要 Node.js 和中文字体；默认查找 macOS Arial Unicode 或 Linux Noto CJK，也可通过 `--font /path/to/font` 指定。KaTeX 0.16.11 与许可证放在 vendor/katex 中。来源改变时构建会停止，应先阅读变化，再更新来源锁。

可选浏览器检查另需 Playwright 与 Chrome／Chromium：

```sh
/tmp/ch08-book-venv/bin/pip install playwright
/tmp/ch08-book-venv/bin/python manuscripts/ch08/browser-check.py --executable '/path/to/chrome'
```

[内容与证据核验](validation.json)覆盖六节标题、实验与外部图注、引用、图片内无图号、源数据、算式与离线 HTML。[公式核验](math-validation.json)保存渲染数量；[浏览器检查](browser-validation.json)记录桌面与手机宽度、图片加载、公式和目录锚点。[桌面预览](preview-desktop.png)与[手机预览](preview-mobile.png)供快速查看。

## 教学组织与核对

正文由同一设计条件逐步推导：完整请求页容量、批量读取交点、共享前缀、缓存保留概率、格式容量、搬移成本、推测解码输出数与边际预算，最后比较 A—D 配置。模型与框架历史集中在延伸阅读，运行条件通过脚注进入原资料。

练习分为计算、分析、数据解释、概率推导和综合设计，核心编号仍为 8-2、8-4、8-9。配套实验目录沿用原 ID，映射见[重组记录](../../research/ch08-reorganization-2026-09-10/README.md)。[计算题参考结果](exercise-notes.md)给出主要中间结果；[算例检查](teaching-check.py)由实测效率与有理数独立计算容量边界、时间、GPU 占用与最优方案变化，结果保存在 [teaching-validation.json](teaching-validation.json)，由 verify.py 一并执行。

批量曲线使用已有精确权重与 KV 输入；调度图的到达和最长输出间隔直接来自保存的事件；质量图逐任务对齐并发及两次重复。完整样本、版本与来源摘要保留在配套数据中。

## 与第九章的范围划分

本章现名“推理优化”，研究给定设备组合下的运行配置；第九章研究计算与状态的分布和服务规模。单卡算例的容量条件已明确，多卡实例需逐卡计算容量。正文文件路径保留，章名、目录和阅读版均已更新。[修改说明](../../research/ch08-ch09-scope-revision/README.md)。

## 当前阅读版配图（2026-09-10）

正文现引用 35 幅图，以下清单按当前阅读顺序列出；上文旧图号用于追溯构建记录。

| 图号 | 内容 | SVG | PNG | PDF |
| --- | --- | --- | --- | --- |
| 8-1 | A 跨越两个迭代继续执行。B 在第一轮结束，下一轮由 C 接替其执行位置（每轮为一条活跃请求预留的一行计算）；请求状态仍按各自身份保存。 | [SVG](figure-8-request-iterations.svg) | [PNG](figure-8-request-iterations.png) | [PDF](figure-8-request-iterations.pdf) |
| 8-2 | 一条输出 256 个 token 的请求。排队 0.1 秒、prefill 0.096 秒，后续 255 个输出间隔各为 26.5 ms（实验 8-1 的 batch 1 实测）。横条按实际时间比例绘制，点标出首、末 token；7 秒虚线是完成时限。 | [SVG](figure-8-1-lifecycle.svg) | [PNG](figure-8-1-lifecycle.png) | [PDF](figure-8-1-lifecycle.pdf) |
| 8-3 | 批处理怎样减少每生成一个 token 所需的读取量。横轴为同时生成的请求数，纵轴为整批读取字节数除以本轮输出 token 数。蓝、绿实线分别对应每条请求已有 2048、8192 个 token 的上下文，包含权重与 KV 读取；同色水平点线仅表示该长度下的 KV 读取量。灰色虚线表示批内共用的权重读取量除以请求数。模型为 Qwen3-8B，使用 BF16；每份矩阵权重每轮读取一次，各请求的 KV 独立。两轴均为对数刻度。 | [SVG](figure-8-2-batch.svg) | [PNG](figure-8-2-batch.png) | [PDF](figure-8-2-batch.pdf) |
| 8-4 | 每输出 token 分摊的 HBM 读取量。固定 8K 上下文，传统路径为 W/B+K，独立快速 ROM 路径为 K；纵轴按上述公式计算读取量。W 是整批读取的权重字节数，B 是批内请求数，K 是单请求本步读取的 KV 字节数；W/B+K 为每个输出 token 分摊的读取量。 | [SVG](figure-8-batch-counterfactual.svg) | [PNG](figure-8-batch-counterfactual.png) | [PDF](figure-8-batch-counterfactual.pdf) |
| 8-5 | 固定 batch 等待整组结束，再接纳 r2、r3。蓝色为 prefill，绿色为 decode，三角为到达时刻。各色带宽度为整次调度迭代耗时，时间按 RTX PRO 6000 上的实测拟合计算。 | [SVG](figure-8-3-scheduling.svg) | [PNG](figure-8-3-scheduling.png) | [PDF](figure-8-3-scheduling.pdf) |
| 8-6 | 连续批处理在 r1 结束后接纳 r2。每行是一条请求；蓝色为处理输入（prefill），绿色为生成输出（decode），三角形为请求到达时刻，色带宽度为所在调度迭代的耗时。r0 等待 r2 的 8K 输入处理，最长输出间隔增至约 376 ms；全部请求约 766 ms 完成。 | [SVG](figure-8-scheduling-continuous.svg) | [PNG](figure-8-scheduling-continuous.png) | [PDF](figure-8-scheduling-continuous.pdf) |
| 8-7 | 将长输入分块处理，每轮先安排已有请求生成，再处理一块新输入。每行是一条请求；蓝色为输入处理，绿色为输出生成，三角形为到达时刻。分块使最长输出间隔降至约 133 ms，全部请求约 844 ms 完成。横轴与图 8-5、8-6 使用相同时间尺度。 | [SVG](figure-8-scheduling-chunked.svg) | [PNG](figure-8-scheduling-chunked.png) | [PDF](figure-8-scheduling-chunked.pdf) |
| 8-8 | 首次处理 4 个 token 时，没有旧上下文，只有新 token 之间的因果注意力配对，形成 1 + 2 + 3 + 4 = 10 个绿色格。白格表示未来 token，不参与当前查询。 | [SVG](figure-8-4-attention.svg) | [PNG](figure-8-4-attention.png) | [PDF](figure-8-4-attention.pdf) |
| 8-9 | 已有 8 个 token 的上下文时，4 个新 token 与旧上下文形成 4 × 8 = 32 个蓝色格，块内仍为 10 个绿色格。块长相同，总配对从 10 增至 42。 | [SVG](figure-8-attention-history.svg) | [PNG](figure-8-attention-history.png) | [PDF](figure-8-attention-history.pdf) |
| 8-10 | 逻辑块 0、1、2 按顺序组成序列，块表分别指向物理块 2、0、3。物理块 1 为空闲，注意力按块表恢复逻辑顺序。 | [SVG](figure-8-page-map.svg) | [PNG](figure-8-page-map.png) | [PDF](figure-8-page-map.pdf) |
| 8-11 | 四条请求分别含 9、13、5、15 个 token，每条预留可保存 16 个 token 的 KV 空间，共分配可保存 64 个 token 的 KV 空间。蓝色已用，灰色预留未用。 | [SVG](figure-8-5-pages.svg) | [PNG](figure-8-5-pages.png) | [PDF](figure-8-5-pages.pdf) |
| 8-12 | 按每块保存 4 个 token 的 KV 分配空间，四条请求分别获得 12、16、8、16 个 token 的容量，合计 52 个。灰色表示块尾未用容量，由 22 个 token 减到 10 个 token。 | [SVG](figure-8-pages-paged.svg) | [PNG](figure-8-pages-paged.png) | [PDF](figure-8-pages-paged.pdf) |
| 8-13 | A、B 的两个共同前缀块只保存一次，各自块表都指向它们。A、B 保留各自的私有尾块；四条请求实际分配的 KV 容量进一步降至 44 个 token。 | [SVG](figure-8-pages-shared.svg) | [PNG](figure-8-pages-shared.png) | [PDF](figure-8-pages-shared.pdf) |
| 8-14 | A 结束后引用数从 2 降到 1，B 仍可使用；最后一个引用释放且加速器已用完，块才能回到空闲池。 | [SVG](figure-8-reference-release.svg) | [PNG](figure-8-reference-release.png) | [PDF](figure-8-reference-release.pdf) |
| 8-15 | 每块 4 个 token 的尾块已有共同的 a、b、c。分支分别追加 x、y，需要不同物理尾块；此前已填满的块继续共享。 | [SVG](figure-8-copy-on-write.svg) | [PNG](figure-8-copy-on-write.png) | [PDF](figure-8-copy-on-write.pdf) |
| 8-16 | 取消接口返回表示已接收取消请求。已提交的加速器操作完成后，再释放私有块和相关引用；观测中的 1.6 ms 与 31 ms 对应不同事件。 | [SVG](figure-8-cancel-lifetime.svg) | [PNG](figure-8-cancel-lifetime.png) | [PDF](figure-8-cancel-lifetime.pdf) |
| 8-17 | 前四轮代码 Agent 输入的压缩前缀树。根部已有 206 个共同 token，边上是新增数量，叶子是输入轮次。分叉表示后续内容不同。 | [SVG](figure-8-6-prefix.svg) | [PNG](figure-8-6-prefix.png) | [PDF](figure-8-6-prefix.pdf) |
| 8-18 | 蓝色为与上一轮逐 token 相同的前缀，橙色为其余输入。此图描述输入内容的可复用程度，实际缓存命中还取决于状态是否保留。 | [SVG](figure-8-prefix-lengths.svg) | [PNG](figure-8-prefix-lengths.png) | [PDF](figure-8-prefix-lengths.pdf) |
| 8-19 | 文本匹配到 10752，最近状态快照在 8192。恢复后仍需重算 2560 个 token，才能得到匹配末端的递推状态。图中 10752 和 8192 是从序列起点累计的 token 数。 | [SVG](figure-8-prefix-restore.svg) | [PNG](figure-8-prefix-restore.png) | [PDF](figure-8-prefix-restore.pdf) |
| 8-20 | 同一历史的三种更新方式。蓝色表示可复用前缀，橙色表示需要重新处理的输入；总结方案先生成摘要，再重建缓存。长度以 K token 示意。 | [SVG](figure-8-context-edits.svg) | [PNG](figure-8-context-edits.png) | [PDF](figure-8-context-edits.pdf) |
| 8-21 | 缓存容量均为 864 MiB。A 占 864 MiB，期望净节省 132.7 ms；三个 B 类前缀各占 288 MiB、各节省 40.3 ms，合计 120.9 ms。图中宽度表示容量；时间按 RTX PRO 6000 上的重算时间和 PCIe Gen5 取回时间计算，命中概率均为 50%。 | [SVG](figure-8-7-cache-choice.svg) | [PNG](figure-8-7-cache-choice.png) | [PDF](figure-8-7-cache-choice.pdf) |
| 8-22 | BF16、q8_0、q4_0 保存同一组 32 个数值所需的空间。横条按字节数成比例绘制；橙色为每组 2 bytes 的缩放系数。把每组总长度乘以组数，就得到整条上下文的 KV 容量。 | [SVG](figure-8-8-kv-format.svg) | [PNG](figure-8-8-kv-format.png) | [PDF](figure-8-8-kv-format.pdf) |
| 8-23 | 卸载九份 FFN 共腾出 2592 MiB。橙色为留在设备上的预取缓冲，绿色为可重新分配的净空间；一组缓冲净省 2304 MiB，两组净省 2016 MiB。 | [SVG](figure-8-9-offload.svg) | [PNG](figure-8-9-offload.png) | [PDF](figure-8-9-offload.pdf) |
| 8-24 | 每轮复制量保持为 2592 MiB（2.72 GB）。经 PCIe Gen5 x16（每方向 64 GB/s）至少需要约 42.5 ms，经 GH200 的 NVLink-C2C（每方向 450 GB/s）至少需要约 6.0 ms。 | [SVG](figure-8-offload-copy.svg) | [PNG](figure-8-offload-copy.png) | [PDF](figure-8-offload-copy.pdf) |
| 8-25 | BF16 KV 基线。每行是一道固定任务，四列为并发 1、4 下各两次自然生成。绿色圆圈正确，橙色叉号错误，共 28/32 正确。 | [SVG](figure-8-10-kv-quality.svg) | [PNG](figure-8-10-kv-quality.png) | [PDF](figure-8-10-kv-quality.pdf) |
| 8-26 | 同一任务与运行顺序，原 FP8 实现共 26/32 正确。这里 FP8 为每元素 8 bit 浮点格式，比较包含实现选择对 Q 精度的影响。 | [SVG](figure-8-kv-quality-1.svg) | [PNG](figure-8-kv-quality-1.png) | [PDF](figure-8-kv-quality-1.pdf) |
| 8-27 | 将查询 Q 保持为 BF16，KV 仍用 FP8，共 28/32 正确；失败位置与 BF16 基线不同。三图使用相同任务和列顺序，模型权重均为 BF16。 | [SVG](figure-8-kv-quality-2.svg) | [PNG](figure-8-kv-quality-2.png) | [PDF](figure-8-kv-quality-2.pdf) |
| 8-28 | 贪心验证的教学示意。a、b、c、d、x 表示 token；目标模型在第三个位置选出 x，与草稿 c 不同。第四个位置及其后的验证结果被丢弃，下一轮从 a、b、x 继续生成。方框表示序列位置，不表示执行耗时。 | [SVG](figure-8-11-verification.svg) | [PNG](figure-8-11-verification.png) | [PDF](figure-8-11-verification.pdf) |
| 8-29 | 接受 A 的概率为 1/4，拒绝后输出 B 的概率为 3/4。两条路径合起来给出目标分布。 | [SVG](figure-8-sample-A.svg) | [PNG](figure-8-sample-A.png) | [PDF](figure-8-sample-A.pdf) |
| 8-30 | 接受 B 的概率为 3/4，拒绝后输出 A 的概率为 1/4。目标分布相同，草稿被接受的概率更高。 | [SVG](figure-8-sample-B.svg) | [PNG](figure-8-sample-B.png) | [PDF](figure-8-sample-B.pdf) |
| 8-31 | 两符号目标分布，每轮生成四个草稿 token。每轮验证 26.3 ms，查询时间沿横轴变化；每个输出 token 的耗时用一轮耗时除以平均输出数。普通 decode 为 26.3 ms/token（RTX PRO 6000，batch 1，2K 上下文）。没有提前停止，额外 token 计入输出数。图中的点标出查询耗时为 0.1 ms 的算例；AAAA、BBBB 分别在查询约 8.7、53.9 ms 处与普通执行相交。 | [SVG](figure-8-12-speculation.svg) | [PNG](figure-8-12-speculation.png) | [PDF](figure-8-12-speculation.pdf) |
| 8-32 | 每种接纳与到达条件使用三个 16 请求窗口。柱为全部完成请求的吞吐中位数，圆点为各窗口结果。时间从计划到达起计算。 | [SVG](figure-8-13-service.svg) | [PNG](figure-8-13-service.png) | [PDF](figure-8-13-service.pdf) |
| 8-33 | 分子仅计正确且在 3 秒内完成的请求。两图采用相同横轴顺序和纵轴范围，差额来自错误或迟到的回答。 | [SVG](figure-8-service-goodput.svg) | [PNG](figure-8-service-goodput.png) | [PDF](figure-8-service-goodput.pdf) |
| 8-34 | 16 条长请求在 RTX PRO 6000 上的配置比较。横轴为 KV 和辅助缓冲区占用，已扣除共同的权重与基本工作区；纵轴为整批请求总耗时，由实验 8-1、8-5 的实测推出。A 内存不足，不能在本实例上执行，图中是它所需的时间。阴影区域同时满足 12 GiB 和 7 秒限制。A 为 BF16 独立上下文，B 为 BF16 共享前缀，C 为 q8_0 独立上下文，D 为 BF16 共享前缀加推测解码。 | [SVG](figure-8-14-design.svg) | [PNG](figure-8-14-design.png) | [PDF](figure-8-14-design.pdf) |
| 8-35 | 其他阶段时间固定、没有新增准备工作的 Amdahl 教学曲线。三条曲线分别取 decode 占基线时间 20%、50%、80%。局部加速的收益随着该阶段原有占比增加。 | [SVG](figure-8-15-task.svg) | [PNG](figure-8-15-task.png) | [PDF](figure-8-15-task.pdf) |


## V4／V4.1 会话修订后的当前图表

当前正文共 36 幅图；下表是当前图号，前文旧图号保留作历史记录。

| 图号 | 内容 | 文件 |
| --- | --- | --- |
| 8-1 | A 跨越两个迭代继续执行。B 在第一轮结束，下一轮由 C 接替其执行位置（每轮为一条活跃请求预留的一行计算）；请求状态仍按各自身份保存。 | [SVG](figure-8-request-iterations.svg) |
| 8-2 | 一条输出 256 个 token 的请求。排队 0.1 秒、prefill 0.096 秒，后续 255 个输出间隔各为 26.5 ms（实验 8-1 的 batch 1 实测）。横条按实际时间比例绘制，点标出首、末 token；7 秒虚线是完成时限。 | [SVG](figure-8-1-lifecycle.svg) |
| 8-3 | 批处理怎样减少每生成一个 token 所需的读取量。横轴为同时生成的请求数，纵轴为整批读取字节数除以本轮输出 token 数。蓝、绿实线分别对应每条请求已有 2048、8192 个 token 的上下文，包含权重与 KV 读取；同色水平点线仅表示该长度下的 KV 读取量。灰色虚线表示批内共用的权重读取量除以请求数。模型为 Qwen3-8B，使用 BF16；每份矩阵权重每轮读取一次，各请求的 KV 独立。两轴均为对数刻度。 | [SVG](figure-8-2-batch.svg) |
| 8-4 | 每输出 token 分摊的 HBM 读取量。固定 8K 上下文，传统路径为 W/B+K，独立快速 ROM 路径为 K；纵轴按上述公式计算读取量。W 是整批读取的权重字节数，B 是批内请求数，K 是单请求本步读取的 KV 字节数；W/B+K 为每个输出 token 分摊的读取量。 | [SVG](figure-8-batch-counterfactual.svg) |
| 8-5 | 固定 batch 等待整组结束，再接纳 r2、r3。蓝色为 prefill，绿色为 decode，三角为到达时刻。各色带宽度为整次调度迭代耗时，时间按 RTX PRO 6000 上的实测拟合计算。 | [SVG](figure-8-3-scheduling.svg) |
| 8-6 | 连续批处理在 r1 结束后接纳 r2。每行是一条请求；蓝色为处理输入（prefill），绿色为生成输出（decode），三角形为请求到达时刻，色带宽度为所在调度迭代的耗时。r0 等待 r2 的 8K 输入处理，最长输出间隔增至约 376 ms；全部请求约 766 ms 完成。 | [SVG](figure-8-scheduling-continuous.svg) |
| 8-7 | 将长输入分块处理，每轮先安排已有请求生成，再处理一块新输入。每行是一条请求；蓝色为输入处理，绿色为输出生成，三角形为到达时刻。分块使最长输出间隔降至约 133 ms，全部请求约 844 ms 完成。横轴与图 8-5、8-6 使用相同时间尺度。 | [SVG](figure-8-scheduling-chunked.svg) |
| 8-8 | 首次处理 4 个 token 时，没有旧上下文，只有新 token 之间的因果注意力配对，形成 1 + 2 + 3 + 4 = 10 个绿色格。白格表示未来 token，不参与当前查询。 | [SVG](figure-8-4-attention.svg) |
| 8-9 | 已有 8 个 token 的上下文时，4 个新 token 与旧上下文形成 4 × 8 = 32 个蓝色格，块内仍为 10 个绿色格。块长相同，总配对从 10 增至 42。 | [SVG](figure-8-attention-history.svg) |
| 8-10 | 逻辑块 0、1、2 按顺序组成序列，块表分别指向物理块 2、0、3。物理块 1 为空闲，注意力按块表恢复逻辑顺序。 | [SVG](figure-8-page-map.svg) |
| 8-11 | 四条请求分别含 9、13、5、15 个 token，每条预留可保存 16 个 token 的 KV 空间，共分配可保存 64 个 token 的 KV 空间。蓝色已用，灰色预留未用。 | [SVG](figure-8-5-pages.svg) |
| 8-12 | 按每块保存 4 个 token 的 KV 分配空间，四条请求分别获得 12、16、8、16 个 token 的容量，合计 52 个。灰色表示块尾未用容量，由 22 个 token 减到 10 个 token。 | [SVG](figure-8-pages-paged.svg) |
| 8-13 | A、B 的两个共同前缀块只保存一次，各自块表都指向它们。A、B 保留各自的私有尾块；四条请求实际分配的 KV 容量进一步降至 44 个 token。 | [SVG](figure-8-pages-shared.svg) |
| 8-14 | A 结束后引用数从 2 降到 1，B 仍可使用；最后一个引用释放且加速器已用完，块才能回到空闲池。 | [SVG](figure-8-reference-release.svg) |
| 8-15 | 每块 4 个 token 的尾块已有共同的 a、b、c。分支分别追加 x、y，需要不同物理尾块；此前已填满的块继续共享。 | [SVG](figure-8-copy-on-write.svg) |
| 8-16 | 取消接口返回表示已接收取消请求。已提交的加速器操作完成后，再释放私有块和相关引用；观测中的 1.6 ms 与 31 ms 对应不同事件。 | [SVG](figure-8-cancel-lifetime.svg) |
| 8-17 | 前四轮代码 Agent 输入的压缩前缀树。根部已有 206 个共同 token，边上是新增数量，叶子是输入轮次。分叉表示后续内容不同。 | [SVG](figure-8-6-prefix.svg) |
| 8-18 | 蓝色为与上一轮逐 token 相同的前缀，橙色为其余输入。此图描述输入内容的可复用程度，实际缓存命中还取决于状态是否保留。 | [SVG](figure-8-prefix-lengths.svg) |
| 8-19 | 文本匹配到 10752，最近状态快照在 8192。恢复后仍需重算 2560 个 token，才能得到匹配末端的递推状态。图中 10752 和 8192 是从序列起点累计的 token 数。 | [SVG](figure-8-prefix-restore.svg) |
| 8-20 | 同一历史的三种更新方式。蓝色表示可复用前缀，橙色表示需要重新处理的输入；总结方案先生成摘要，再重建缓存。长度以 K token 示意。 | [SVG](figure-8-context-edits.svg) |
| 8-21 | 编码器的三条前缀恢复路径与共同的解码器重放。缓存命中状态中的 SWA 专指编码器；所有路径在 prefill 中仍构建解码器 SWA，再开始生成。箭头表示执行先后，框大小不代表耗时。 | [SVG](figure-8-v41-recovery.svg) |
| 8-22 | 缓存容量均为 864 MiB。A 占 864 MiB，期望净节省 132.7 ms；三个 B 类前缀各占 288 MiB、各节省 40.3 ms，合计 120.9 ms。图中宽度表示容量；时间按 RTX PRO 6000 上的重算时间和 PCIe Gen5 取回时间计算，命中概率均为 50%。 | [SVG](figure-8-7-cache-choice.svg) |
| 8-23 | BF16、q8_0、q4_0 保存同一组 32 个数值所需的空间。横条按字节数成比例绘制；橙色为每组 2 bytes 的 scale。把每组总长度乘以组数，就得到整条上下文的 KV 容量。 | [SVG](figure-8-8-kv-format.svg) |
| 8-24 | 卸载九份 FFN 共腾出 2592 MiB。橙色为留在加速器上的预取缓冲，绿色为可重新分配的净空间；一组缓冲净省 2304 MiB，两组净省 2016 MiB。 | [SVG](figure-8-9-offload.svg) |
| 8-25 | 每轮复制量保持为 2592 MiB（2.72 GB）。经 PCIe Gen5 x16（每方向 64 GB/s）至少需要约 42.5 ms，经 GH200 的 NVLink-C2C（每方向 450 GB/s）至少需要约 6.0 ms。 | [SVG](figure-8-offload-copy.svg) |
| 8-26 | BF16 KV 基线。每行是一道固定任务，四列为并发 1、4 下各两次自然生成。绿色圆圈正确，橙色叉号错误，共 28/32 正确。 | [SVG](figure-8-10-kv-quality.svg) |
| 8-27 | 同一任务与运行顺序，原 FP8 实现共 26/32 正确。这一比较包含实现选择对 Q 精度的影响。圆圈表示回答正确，叉号表示回答错误；每行对应同一道题，列表示并发数与重复运行序号。 | [SVG](figure-8-kv-quality-1.svg) |
| 8-28 | 将查询 Q 保持为 BF16，KV 仍用 FP8，共 28/32 正确；答错的题目与 BF16 基线不同。三幅图使用相同任务和列顺序，模型权重均为 BF16。圆圈表示回答正确，叉号表示回答错误；每行对应同一道题，列表示并发数与重复运行序号。 | [SVG](figure-8-kv-quality-2.svg) |
| 8-29 | 贪心验证的过程。a、b、c、d、x 表示 token；目标模型在第三个 token 选出 x，与草稿 c 不同。第四个 token 及其后的验证结果作废，下一轮从 a、b、x 继续生成。方框表示序列中的 token 位置，不表示执行耗时。 | [SVG](figure-8-11-verification.svg) |
| 8-30 | 接受 A 的概率为 1/4，拒绝后输出 B 的概率为 3/4。两条路径合起来给出目标分布。 | [SVG](figure-8-sample-A.svg) |
| 8-31 | 接受 B 的概率为 3/4，拒绝后输出 A 的概率为 1/4。目标分布相同，草稿的接受概率更高。 | [SVG](figure-8-sample-B.svg) |
| 8-32 | 两符号目标分布，每轮生成四个草稿 token。每轮验证 26.26 ms，查询时间沿横轴变化；每个输出 token 的耗时用一轮耗时除以平均输出数。普通 decode 为 26.26 ms/token（RTX PRO 6000，batch 1，2K 上下文）。没有提前停止，额外 token 计入输出数。图中的点标出查询耗时为 0.1 ms 的算例；AAAA、BBBB 分别在查询约 8.7、53.9 ms 处与普通执行相交。 | [SVG](figure-8-12-speculation.svg) |
| 8-33 | 每种接纳与到达条件使用三个 16 请求窗口。柱为全部完成请求的吞吐中位数，圆点为各窗口结果。时间从计划到达起计算。 | [SVG](figure-8-13-service.svg) |
| 8-34 | 分子仅计正确且在 3 秒内完成的请求。两图采用相同横轴顺序和纵轴范围，差额来自错误或迟到的回答。 | [SVG](figure-8-service-goodput.svg) |
| 8-35 | 16 条长请求在 RTX PRO 6000 上的配置比较。横轴为 KV 和辅助缓冲区占用，已扣除共同的权重与基本工作区；纵轴为整批请求总耗时，由实验 8-1、8-5 的实测推出。A 内存不足，不能在本实例上执行，图中是它所需的时间。阴影区域同时满足 12 GiB 和 7 秒限制。A 为 BF16 独立上下文，B 为 BF16 共享前缀，C 为 q8_0 独立上下文，D 为 BF16 共享前缀加推测解码。 | [SVG](figure-8-14-design.svg) |
| 8-36 | 其他阶段时间固定、没有新增准备工作的 Amdahl 加速比曲线。三条曲线分别取 decode 占基线时间 20%、50%、80%。该阶段原有的耗时占比越高，局部加速带来的收益就越大。 | [SVG](figure-8-15-task.svg) |
