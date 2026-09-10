# 第九章正文与插图

[阅读版 HTML](../09-分布式推理.html) · [正文 Markdown](../09-分布式推理.md) · [写作前阅读记录](reading-notes.md)

正文按七节 outline 展开，包含24个小节、7个定量例题及1份解题示范、17幅原创插图、10道练习及来源注释。采用提出问题、定义计量口径、推导、代入例题、改变条件的教材体例；已有实测与条件计算分别呈现。正文及注释约1.84万汉字（不含数字和英文），为可继续编辑的完整初稿。

## 插图

全章共 17 幅原创图，按正文顺序编号。新增图重点展示任务分配、数据复用和时间依赖。

| 文件 | 内容 |
| --- | --- |
| figure-9-1-organization | 多卡协作完整副本和计算分工 |
| figure-9-2-state | 请求阶段、实例分工与状态寿命 |
| figure-9-3-pd | 阶段配比与请求率 |
| figure-9-4-allocation | 不同请求下八个执行单元的分工 |
| figure-9-5-local | 专家权重搬运与CPU就地计算 |
| figure-9-6-reuse | 专家复用与执行位置边界 |
| figure-9-7-footprint | 同样分派次数下的专家数与输入行数 |
| figure-9-8-handoff | 消息数量与启动开销 |
| figure-9-9-balance | 八张卡的任务分布与结果合并时刻 |
| figure-9-10-experts | 专家副本的准备与回本 |
| figure-9-11-overlap | 专家分派计算与结果合并的流水时间线 |
| figure-9-12-cache | 读取页与可复用连续前缀 |
| figure-9-13-route | 缓存路由中排队取回与计算的时间关系 |
| figure-9-14-migration | 状态生成与后台复制的进度 |
| figure-9-15-recovery | 输出记录与KV检查点的恢复位置 |
| figure-9-16-composition | 直接交接与共享池中转 |
| figure-9-17-service | 服务能力与启动积压消退 |

每幅图均提供 SVG、PNG、PDF。图号只在外部图注中出现。build.py 与 extra-figures.py 共同生成插图，figure-data.json 保存数值。阅读版内嵌全部图片和公式字体，可离线阅读。

## 复现

在仓库根目录，使用独立Python环境安装本目录requirements.txt。构建另外需要Node.js与CJK字体；默认尝试macOS Arial Unicode或Linux Noto Sans CJK，也可传入`--font /path/to/font`。数学排版复用仓库已有的`manuscripts/ch06/vendor/katex`，不联网加载CDN。

```sh
python3 -m venv /tmp/ai-infra-ch09-build
/tmp/ai-infra-ch09-build/bin/pip install -r manuscripts/ch09/requirements.txt
/tmp/ai-infra-ch09-build/bin/python manuscripts/ch09/build.py
python3 manuscripts/ch09/verify.py
```

build.py在绘图前核对sources.json。来源文件变化时应先复核它是否影响本章，再更新锁定记录，不跳过哈希检查。构建不启动模型，不运行新的GPU实验。

浏览器验证为可选项，需Playwright与本地Chrome／Chromium：

```sh
python manuscripts/ch09/browser-check.py --executable /path/to/chrome
```

## 已完成检查

- [validation.json](validation.json)：章节与outline一致，实验和图注顺序、引用、来源、图片内部无图号、关键数值独立复算、导出哈希等302项检查。
- [browser-validation.json](browser-validation.json)：1440px和390px视口，17张图片、109个公式正常，目录锚点有效，无页面级横向溢出。
- [figure-layout-check.json](figure-layout-check.json)：图中文字均在画布范围内。
- [math-validation.json](math-validation.json)：KaTeX构建时严格解析全部公式。
- [manifest.json](manifest.json)：正文、阅读版、图数据和51份图片导出的SHA256。

已目视检查九图缩略总览、桌面正文与手机组合图页面；配套浏览器截图保存在本目录。验证证明本次书稿与证据的一致性，不把既有计算子账提升为尚未完成的跨机性能实验。

## 数字论证修订

本轮按[修订说明](revision-numeric/README.md)改写各节数字推导，统一精度并重组主图。原图4／5依正文出现顺序交换：新图4讲专家复用，新图5讲消息频次；实验9-4／9-5编号保持原义。正文、outline配图计划、生成器和导出文件均同步，历史计算与实验记录中的图号按原记录解释。

## 连贯性与教材体例修订

本轮以八 worker 服务设计贯穿开篇、阶段配比、缓存和生命周期，例 9.7 在相同资源与负载下选择直接 PD，并推导 25 秒排空目标所需的最低能力。MoE 的第二条推导从批内复用连接到执行位置、最忙设备和副本回本。正文删去段末泛化提醒与自我辩护，必要条件放入例题，版本与证据说明放在注释。

CPU 专家先用低复用、高复用数值解释选择翻转，再给出路径公式；缓存与迁移新增依赖关系的具体解释。练习加入完整设计题和一份已解示范，区分 CPU 自身的资源交点与 CPU/GPU 路径交点。详见[修订记录](revision-coherence/README.md)。

## 中文表达修订

正文、表格、图注和练习已按语境统一术语，并逐句调整主语、语序及修饰关系。两处小节标题与 outline 同步，插图文字同步重绘。[修订记录](revision-language/README.md)。

## 段落衔接与图示修订

新增七幅机制图，重写各节之间和数字段落之间的衔接。图前说明观察对象，图后解释因果关系；专家复用、最忙卡、流水执行、缓存路由、状态迁移与输出恢复均可沿图推导。[修订记录](revision-visual/README.md)。

## 与第八章的范围划分

第八章现名“推理优化”，本章现名“分布式推理”。本章以计算和状态的执行位置为主线，适用于单实例内的多卡协作，也适用于多个副本和阶段服务池。新图 9-1 说明硬件组织与服务组织；原有 16 图顺延一号。详细修改见 [两章范围修订](../../research/ch08-ch09-scope-revision/README.md)。正文文件路径保留，链接标题使用新章名。

## 当前阅读版配图（2026-09-10）

正文现引用 33 幅图，以下清单按当前阅读顺序列出；上文旧图号用于追溯构建记录。

| 图号 | 内容 | SVG | PNG | PDF |
| --- | --- | --- | --- | --- |
| 9-1 | 八张卡共同执行一个完整模型实例，接收同一批请求。卡号表示协作组成员。 | [SVG](figure-9-1-organization.svg) | [PNG](figure-9-1-organization.png) | [PDF](figure-9-1-organization.pdf) |
| 9-2 | 每个副本都能完成整次推理，可以分别接收独立请求。副本自身也可以由多张卡组成。 | [SVG](figure-9-organization-1.svg) | [PNG](figure-9-organization-1.png) | [PDF](figure-9-organization-1.pdf) |
| 9-3 | P 处理输入，D 继续生成。两个服务池分别调度，上下文 KV 从 P 交给 D。 | [SVG](figure-9-organization-2.svg) | [PNG](figure-9-organization-2.png) | [PDF](figure-9-organization-2.pdf) |
| 9-4 | 注意力与 FFN／专家分别执行，隐状态作为激活在两侧往返。每层都需要这次交接。 | [SVG](figure-9-organization-3.svg) | [PNG](figure-9-organization-3.png) | [PDF](figure-9-organization-3.pdf) |
| 9-5 | 计算暂停期间，状态仍需保留。示意同一请求从 prefill、decode 到工具等待和下一轮的状态寿命；横轴按阶段排列，不表示相等时长，EC 仅在有视觉输入时出现。 | [SVG](figure-9-2-state.svg) | [PNG](figure-9-2-state.png) | [PDF](figure-9-2-state.pdf) |
| 9-6 | 源 P 保留完整 1.125 GiB 状态，目的 D 同时分配 1.125 GiB 接收空间。传输过程共占 2.25 GiB。 | [SVG](figure-9-kv-residency.svg) | [PNG](figure-9-kv-residency.png) | [PDF](figure-9-kv-residency.pdf) |
| 9-7 | 数据到齐并满足可见性条件后，完成标记允许 D 读取状态。标记指示使用顺序，完整载荷已经写到目的端。 | [SVG](figure-9-kv-publish.svg) | [PNG](figure-9-kv-publish.png) | [PDF](figure-9-kv-publish.pdf) |
| 9-8 | 本算例将执行权交给 D 后释放 P 的源缓冲，D 保留上下文并继续生成。源端空间用于后续请求。 | [SVG](figure-9-kv-release.svg) | [PNG](figure-9-kv-release.png) | [PDF](figure-9-kv-release.pdf) |
| 9-9 | 每个 A 在 P 阶段提供 2 请求/s，每个 B 在 D 阶段也提供 2 请求/s。两池均为 8 请求/s，低于给定链路约 20.7 请求/s 的交接能力。 | [SVG](figure-9-pd-layout.svg) | [PNG](figure-9-pd-layout.png) | [PDF](figure-9-pd-layout.pdf) |
| 9-10 | 阶段配比如何限制请求率。两类 worker 各四个，能力见例 9.2；横纵轴为分给 P 的数量，其余分给 D。每格取两池能力与 25 GB/s 链路容量的最小值，单位为请求/s，不含排队。 | [SVG](figure-9-3-pd.svg) | [PNG](figure-9-3-pd.png) | [PDF](figure-9-3-pd.pdf) |
| 9-11 | 请求组成改变资源分配。两类 worker 各四个，处理速度沿用例 9.2；第二行只减少 P 的新输入，第三行恢复完整输入并将输出增至 1025 个 token。方块表示设备数量，每行下方为对应的吞吐率上限。 | [SVG](figure-9-4-allocation.svg) | [PNG](figure-9-4-allocation.png) | [PDF](figure-9-4-allocation.pdf) |
| 9-12 | 把一份 36 MiB 专家权重从主存送到 GPU，再由 GPU 读取本地输入完成计算。 | [SVG](figure-9-5-local.svg) | [PNG](figure-9-5-local.png) | [PDF](figure-9-5-local.pdf) |
| 9-13 | 输入从 GPU 交给 CPU，CPU 使用主存权重执行专家，结果回到 GPU。每行输入和输出合计 16 KiB；并行的 GPU 常驻专家分支完成后再汇合。 | [SVG](figure-9-local-cpu.svg) | [PNG](figure-9-local-cpu.png) | [PDF](figure-9-local-cpu.pdf) |
| 9-14 | 专家复用改变执行位置的选择。八个专家各有 36 MiB BF16 权重，有效 CPU／GPU 算力为 2／100 TFLOP/s，DRAM／HBM 带宽为 200／1000 GB/s，交接为 25 GB/s、每次启动 5 μs。曲线按例 9.3 计算单层专家路径，未含 NUMA 和格式转换。 | [SVG](figure-9-6-reuse.svg) | [PNG](figure-9-6-reuse.png) | [PDF](figure-9-6-reuse.pdf) |
| 9-15 | 512 次分派覆盖 128 个专家，每专家四行。矩形宽为专家数，高为每专家行数，面积为分派次数。 | [SVG](figure-9-7-footprint.svg) | [PNG](figure-9-7-footprint.png) | [PDF](figure-9-7-footprint.pdf) |
| 9-16 | 八个专家各处理 64 行，总面积仍为 512。两图横纵轴相同，权重读取却从 4608 MiB 降至 288 MiB。 | [SVG](figure-9-footprint-reuse.svg) | [PNG](figure-9-footprint-reuse.png) | [PDF](figure-9-footprint-reuse.pdf) |
| 9-17 | 相同总载荷下，消息数放大启动开销。两条曲线总载荷均为 1.125 GiB、有效带宽均为 25 GB/s，分别串行发送 1 次和 72 次；差值为 $71\alpha$，纵轴从48.2 ms起以显示差异。这样保持总字节数不变，只比较消息数量的影响，实际一步 AF 仅传 576 KiB。 | [SVG](figure-9-8-handoff.svg) | [PNG](figure-9-8-handoff.png) | [PDF](figure-9-8-handoff.pdf) |
| 9-18 | 总计 512 次专家分派均分到八张卡，每卡 64 次；虚线表示全部计算结束、可以汇合的时刻。 | [SVG](figure-9-9-balance.svg) | [PNG](figure-9-9-balance.png) | [PDF](figure-9-9-balance.pdf) |
| 9-19 | 512 次全部落在卡 0，其他卡空闲。相同总计算量，需要等待卡 0 完成；两图使用相同时间尺度。 | [SVG](figure-9-balance-hotspot.svg) | [PNG](figure-9-balance-hotspot.png) | [PDF](figure-9-balance-hotspot.pdf) |
| 9-20 | 热点持续多久，专家复制才值得。一次准备约 10.6 ms，每批节省约 0.40 ms；曲线使用例 9.5 未舍入时间计算，第 27 批开始净获益。七张接收卡各需额外 36 MiB，假设容量足够且热点不变。 | [SVG](figure-9-10-experts.svg) | [PNG](figure-9-10-experts.png) | [PDF](figure-9-10-experts.pdf) |
| 9-21 | 整批依次分派 0.2 ms、计算 0.6 ms、合并 0.2 ms，总时间 1 ms。 | [SVG](figure-9-11-overlap.svg) | [PNG](figure-9-11-overlap.png) | [PDF](figure-9-11-overlap.pdf) |
| 9-22 | 每微批次各阶段时间减半，三条轨道使用独立资源。第一微批次计算时可以分派第二微批次，总时间降到 0.8 ms。 | [SVG](figure-9-overlap-pipeline.svg) | [PNG](figure-9-overlap-pipeline.png) | [PDF](figure-9-overlap-pipeline.pdf) |
| 9-23 | 虚线表示按标识查找对象位置。目录用于定位，实际 KV 对象用于恢复计算；路由前还需确认对象版本与可用性。 | [SVG](figure-9-cache-directory.svg) | [PNG](figure-9-cache-directory.png) | [PDF](figure-9-cache-directory.pdf) |
| 9-24 | 读入的页不一定全部成为可复用前缀。正常重启后的这一请求读入 64 个 16-token 页，只复用前 63 页；末页仍需处理。每页 2.25 MiB，该请求的匹配边界为 1008 个位置。 | [SVG](figure-9-12-cache.svg) | [PNG](figure-9-12-cache.png) | [PDF](figure-9-12-cache.pdf) |
| 9-25 | A 本地缓存已命中，GPU 排队 250 ms 后再计算 10 ms，首 token 在 260 ms 返回。灰为排队，绿为计算。 | [SVG](figure-9-13-route.svg) | [PNG](figure-9-13-route.png) | [PDF](figure-9-13-route.pdf) |
| 9-26 | B 在 20 ms 空闲，随后重算 180 ms，首 token 在 200 ms 返回。 | [SVG](figure-9-route-1.svg) | [PNG](figure-9-route-1.png) | [PDF](figure-9-route-1.pdf) |
| 9-27 | 取回先查找 10 ms，再按 5 GB/s 读取 1.125 GiB 至主存，最后按 25 GB/s 搬到 GPU。计算等待数据和 GPU 都就绪，首 token 约 310 ms 返回。 | [SVG](figure-9-route-2.svg) | [PNG](figure-9-route-2.png) | [PDF](figure-9-route-2.pdf) |
| 9-28 | 远端带宽提高到 20 GB/s 后，首 token 约 129 ms 返回。橙为远端读取，蓝为主存到 GPU；四图均从请求到达起计时，横轴相同。 | [SVG](figure-9-route-3.svg) | [PNG](figure-9-route-3.png) | [PDF](figure-9-route-3.pdf) |
| 9-29 | 服务余量决定启动积压的消退速度。连续流量模型，每秒到达四请求，启动 10 秒后积压 40 个。就绪后服务率为八或五请求/s，净排空率分别为四或一请求/s，从开始启动算起在第 20 或 50 秒排空。例 9.7 的排空期限为第 25 秒。 | [SVG](figure-9-17-service.svg) | [PNG](figure-9-17-service.png) | [PDF](figure-9-17-service.pdf) |
| 9-30 | 后台复制需要赶上仍在增长的状态。开始时待复制状态为 1 GiB，源端以 0.5 GiB/s 生成新状态，目标以 2 GiB/s 复制；两条曲线相交前，垂直距离就是尚未复制的数据量。相交后，目标只需跟随源端的新增状态。 | [SVG](figure-9-14-migration.svg) | [PNG](figure-9-14-migration.png) | [PDF](figure-9-14-migration.pdf) |
| 9-31 | 输出记录决定继续哪条序列，KV 检查点决定从哪里补算。假定 129 个输出均已可靠记录，但 KV 只保存了原输入。下方按输入、前 128 个输出和第 129 个输出分段示意，宽度不按 token 数量比例绘制。 | [SVG](figure-9-15-recovery.svg) | [PNG](figure-9-15-recovery.png) | [PDF](figure-9-15-recovery.pdf) |
| 9-32 | P 直接向 D 交接 1.125 GiB 上下文 KV 缓存，只经过一条数据边。 | [SVG](figure-9-16-composition.svg) | [PNG](figure-9-16-composition.png) | [PDF](figure-9-16-composition.pdf) |
| 9-33 | P 先向池写入完整 1.125 GiB 并发布，D 再取回同一对象，共经过两条边。后续实例还可以复用池中对象。 | [SVG](figure-9-composition-pool.svg) | [PNG](figure-9-composition-pool.png) | [PDF](figure-9-composition-pool.pdf) |


## V4／V4.1 会话修订后的当前图表

当前正文共 34 幅图；下表是当前图号，前文旧图号保留作历史记录。

| 图号 | 内容 | 文件 |
| --- | --- | --- |
| 9-1 | 八张卡共同执行一个完整模型实例，接收同一批请求。卡号表示协作组成员。 | [SVG](figure-9-1-organization.svg) |
| 9-2 | 每个副本都能完成整次推理，可以分别接收独立请求。副本自身也可以由多张卡组成。 | [SVG](figure-9-organization-1.svg) |
| 9-3 | P 处理输入，D 继续生成。两个服务池分别调度，上下文 KV 从 P 交给 D。 | [SVG](figure-9-organization-2.svg) |
| 9-4 | 注意力与 FFN／专家分别执行，隐状态作为激活在两侧往返。每层都需要这次交接。 | [SVG](figure-9-organization-3.svg) |
| 9-5 | 计算暂停期间，状态仍需保留。示意同一请求从 prefill、decode 到工具等待和下一轮的状态寿命；横轴按阶段排列，不表示相等时长，EC 仅在有视觉输入时出现。 | [SVG](figure-9-2-state.svg) |
| 9-6 | 源 P 保留完整 1.125 GiB 状态，目的 D 同时分配 1.125 GiB 接收空间。传输过程共占 2.25 GiB。 | [SVG](figure-9-kv-residency.svg) |
| 9-7 | 数据到齐并满足可见性条件后，完成标记允许 D 读取状态。标记指示使用顺序，完整载荷已经写到目的端。 | [SVG](figure-9-kv-publish.svg) |
| 9-8 | 本算例将执行权交给 D 后释放 P 的源缓冲，D 保留上下文并继续生成。源端空间用于后续请求。 | [SVG](figure-9-kv-release.svg) |
| 9-9 | 每个 A 在 P 阶段提供 2 请求/s，每个 B 在 D 阶段也提供 2 请求/s。两池均为 8 请求/s，低于给定链路约 20.7 请求/s 的交接能力。 | [SVG](figure-9-pd-layout.svg) |
| 9-10 | 阶段配比如何限制请求率。两类 worker 各四个，能力见例 9.2；横纵轴为分给 P 的数量，其余分给 D。每格取两池能力与 25 GB/s 链路容量的最小值，单位为请求/s，不含排队。 | [SVG](figure-9-3-pd.svg) |
| 9-11 | 请求组成改变资源分配。两类 worker 各四个，处理速度沿用例 9.2；第二行只减少 P 的新输入，第三行恢复完整输入并将输出增至 1025 个 token。方块表示设备数量，每行下方为对应的吞吐率上限。 | [SVG](figure-9-4-allocation.svg) |
| 9-12 | 把一份 36 MiB 专家权重从主存送到 GPU，再由 GPU 读取本地输入完成计算。 | [SVG](figure-9-5-local.svg) |
| 9-13 | 输入从 GPU 交给 CPU，CPU 使用主存权重执行专家，结果回到 GPU。每次 token 到专家的分派，传入和传出的特征向量合计 16 KiB；并行的 GPU 常驻专家分支完成后再汇合。 | [SVG](figure-9-local-cpu.svg) |
| 9-14 | 专家复用改变执行位置的选择。八个专家各有 36 MiB BF16 权重，有效 CPU／GPU 算力为 2／100 TFLOP/s，DRAM／HBM 带宽为 200／1000 GB/s，交接为 25 GB/s、每次启动 5 μs。曲线按例 9.3 计算单层专家路径，未含 NUMA 和格式转换。 | [SVG](figure-9-6-reuse.svg) |
| 9-15 | 512 次分派覆盖 128 个专家，每专家四行。矩形宽为专家数，高为每专家行数，面积为分派次数。 | [SVG](figure-9-7-footprint.svg) |
| 9-16 | 八个专家各处理 64 行，总面积仍为 512。两图横纵轴相同，权重读取却从 4608 MiB 降至 288 MiB。 | [SVG](figure-9-footprint-reuse.svg) |
| 9-17 | 相同总载荷下，消息数放大启动开销。两条曲线总载荷均为 1.125 GiB、有效带宽均为 25 GB/s，分别串行发送 1 次和 72 次；差值为 $71\alpha$，纵轴从48.2 ms起以显示差异。这样保持总字节数不变，只比较消息数量的影响，实际一步 AF 仅传 576 KiB。 | [SVG](figure-9-8-handoff.svg) |
| 9-18 | 总计 512 次专家分派均分到八张卡，每卡 64 次；虚线表示全部计算结束、可以汇合的时刻。 | [SVG](figure-9-9-balance.svg) |
| 9-19 | 512 次全部落在卡 0，其他卡空闲。相同总计算量，需要等待卡 0 完成；两图使用相同时间尺度。 | [SVG](figure-9-balance-hotspot.svg) |
| 9-20 | 热点持续多久，专家复制才值得。一次准备约 10.6 ms，每批节省约 0.40 ms；曲线使用例 9.5 未舍入时间计算，第 27 批开始净获益。七张接收卡各需额外 36 MiB，假设容量足够且热点不变。 | [SVG](figure-9-10-experts.svg) |
| 9-21 | 整批依次分派 0.2 ms、计算 0.6 ms、合并 0.2 ms，总时间 1 ms。 | [SVG](figure-9-11-overlap.svg) |
| 9-22 | 每微批次各阶段时间减半，三条轨道使用独立资源。第一微批次计算时可以分派第二微批次，总时间降到 0.8 ms。 | [SVG](figure-9-overlap-pipeline.svg) |
| 9-23 | 虚线表示按标识查找对象位置。目录用于定位，实际 KV 对象用于恢复计算；路由前还需确认对象版本与可用性。 | [SVG](figure-9-cache-directory.svg) |
| 9-24 | 读入的页不一定全部成为可复用前缀。正常重启后的这一请求读入 64 个 16-token 页，只复用前 63 页；末页仍需处理。每页 2.25 MiB，该请求的匹配边界为 1008 个位置。 | [SVG](figure-9-12-cache.svg) |
| 9-25 | A 本地缓存已命中，GPU 排队 250 ms 后再计算 10 ms，首 token 在 260 ms 返回。灰为排队，绿为计算。 | [SVG](figure-9-13-route.svg) |
| 9-26 | B 在 20 ms 空闲，随后重算 180 ms，首 token 在 200 ms 返回。 | [SVG](figure-9-route-1.svg) |
| 9-27 | 取回先查找 10 ms，再按 5 GB/s 读取 1.125 GiB 至主存，最后按 25 GB/s 搬到 GPU。计算等待数据和 GPU 都就绪，首 token 约 310 ms 返回。 | [SVG](figure-9-route-2.svg) |
| 9-28 | 远端带宽提高到 20 GB/s 后，首 token 约 129 ms 返回。橙为远端读取，蓝为主存到 GPU；四图均从请求到达起计时，横轴相同。 | [SVG](figure-9-route-3.svg) |
| 9-29 | 缓存亲和性与空闲执行位置的比较。A 保留完整状态；B 需要 4.666 ms 全局传输和假设的 8 ms 局部恢复。只比较后续处理前的串行等待；A 的队列从 10 ms 增到 20 ms 时，选择翻转。 | [SVG](figure-9-v41-routing.svg) |
| 9-30 | 服务余量决定启动积压的消退速度。连续流量模型，每秒到达四请求，启动 10 秒后积压 40 个。就绪后服务率为八或五请求/s，净排空率分别为四或一请求/s，从开始启动算起在第 20 或 50 秒排空。例 9.7 的排空期限为第 25 秒。 | [SVG](figure-9-17-service.svg) |
| 9-31 | 后台复制需要赶上仍在增长的状态。开始时待复制状态为 1 GiB，源端以 0.5 GiB/s 生成新状态，目标以 2 GiB/s 复制；两条曲线相交前，垂直距离就是尚未复制的数据量。相交后，目标只需跟随源端的新增状态。 | [SVG](figure-9-14-migration.svg) |
| 9-32 | 输出记录决定继续哪条序列，KV 检查点决定从哪里补算。假定 129 个输出均已可靠记录，但 KV 只保存了原输入。下方按输入、前 128 个输出和第 129 个输出分段示意，宽度不按 token 数量比例绘制。 | [SVG](figure-9-15-recovery.svg) |
| 9-33 | P 直接向 D 交接 1.125 GiB 上下文 KV 缓存，只经过一条数据边。 | [SVG](figure-9-16-composition.svg) |
| 9-34 | P 先向池写入完整 1.125 GiB 并发布，D 再取回同一对象，共经过两条边。后续实例还可以复用池中对象。 | [SVG](figure-9-composition-pool.svg) |
