# 第九章正文与插图

[阅读版 HTML](../09-分布式推理.md) · [正文 Markdown](../09-分布式推理.md) · [写作前阅读记录](reading-notes.md)

正文沿现有章节组织计算与状态的分工，当前共 36 幅插图。专家部分补充大 EP、专家分离、两阶段通信与计算偏斜，并引用论文测量。采用提出问题、推导、代入例题、改变条件的教材体例，实测与条件计算分别呈现。

## 插图

以下为早期版本的 17 幅图清单；当前图号与配图见文末。

| 文件 | 内容 |
| --- | --- |
| figure-9-1-organization | 多卡协作完整副本和计算分工 |
| figure-9-2-state | 请求阶段、实例分工与状态保存时间 |
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

## 旧版已完成检查

- [validation.json](validation.json)：章节与outline一致，实验和图注顺序、引用、来源、图片内部无图号、关键数值独立复算、导出哈希等302项检查。
- [browser-validation.json](browser-validation.json)：1440px和390px视口，17张图片、109个公式正常，目录锚点有效，无页面级横向溢出。
- [figure-layout-check.json](figure-layout-check.json)：图中文字均在画布范围内。
- [math-validation.json](math-validation.json)：KaTeX构建时严格解析全部公式。
- [manifest.json](manifest.json)：正文、阅读版、图数据和51份图片导出的SHA256。

已目视检查九图缩略总览、桌面正文与手机组合图页面；配套浏览器截图保存在本目录。验证证明本次书稿与证据的一致性，不把既有计算子账提升为尚未完成的跨机性能实验。

## 数字论证修订

本轮按[修订说明](revision-numeric/README.md)改写各节数字推导，统一精度并重组主图。原图4／5依正文出现顺序交换：新图4讲专家复用，新图5讲消息频次；实验9-4／9-5编号保持原义。正文、outline配图计划、生成器和导出文件均同步，历史计算与实验记录中的图号按原记录解释。

## 连贯性与教材体例修订

本轮以八 worker 服务设计贯穿开篇、阶段配比、缓存和生命周期，例 9.8 在相同资源与负载下选择直接 PD，并推导 25 秒排空目标所需的最低能力。MoE 的第二条推导从批内复用连接到执行位置、最忙设备和副本回本。正文删去段末泛化提醒与自我辩护，必要条件放入例题，版本与证据说明放在注释。

CPU 专家先用低复用、高复用数值解释选择翻转，再给出路径公式；缓存与迁移新增依赖关系的具体解释。练习加入完整设计题和一份已解示范，区分 CPU 自身的资源交点与 CPU/GPU 路径交点。详见[修订记录](revision-coherence/README.md)。

## 中文表达修订

正文、表格、图注和练习已按语境统一术语，并逐句调整主语、语序及修饰关系。两处小节标题与 outline 同步，插图文字同步重绘。[修订记录](revision-language/README.md)。

## 段落衔接与图示修订

新增七幅机制图，重写各节之间和数字段落之间的衔接。图前说明观察对象，图后解释因果关系；专家复用、最忙卡、流水执行、缓存路由、状态迁移与输出恢复均可沿图推导。[修订记录](revision-visual/README.md)。

## 与第八章的范围划分

第八章现名“推理优化”，本章现名“分布式推理”。本章以计算和状态的执行位置为主线，适用于单实例内的多卡协作，也适用于多个副本和阶段服务池。新图 9-1 说明硬件组织与服务组织；原有 16 图顺延一号。详细修改见 [两章范围修订](../../research/ch08-ch09-scope-revision/README.md)。正文文件路径保留，链接标题使用新章名。

## 本次修订验证

当前正文、来源快照、算例、图形与浏览器验证见[统一视角修订记录](../../research/ub-ep-integration-2026-09-10/README.md)。旧版 manifest、浏览器记录与图号反映当时版本，不作为本次验证结果。

## 当前阅读版配图（2026-09-12）

以下图号以当前正文顺序为准；前面的旧版图表记录仅用于历史对照。新增内容使用 `../ub_ep_figures.py` 和统一 `figure_style` 生成。

| 图号 | 内容 | SVG | PNG | PDF |
|---|---|---|---|---|
| 9-1 | 八张卡共同执行一个完整模型实例，接收同一批请求。卡号表示协作组成员。 | [SVG](figure-9-1-organization.svg) | [PNG](figure-9-1-organization.png) | [PDF](figure-9-1-organization.pdf) |
| 9-2 | 每个副本都能完成整次推理，可以分别接收独立请求。副本自身也可以由多张卡组成。 | [SVG](figure-9-organization-1.svg) | [PNG](figure-9-organization-1.png) | [PDF](figure-9-organization-1.pdf) |
| 9-3 | P 处理输入，D 继续生成。两个服务池分别调度，上下文 KV 从 P 交给 D。 | [SVG](figure-9-organization-2.svg) | [PNG](figure-9-organization-2.png) | [PDF](figure-9-organization-2.pdf) |
| 9-4 | 注意力与 FFN／专家分别执行，隐状态作为激活在两侧往返。每层都需要这次交接。 | [SVG](figure-9-organization-3.svg) | [PNG](figure-9-organization-3.png) | [PDF](figure-9-organization-3.pdf) |
| 9-5 | 计算暂停期间，状态仍需保留。示意同一请求从 prefill、decode 到工具等待和下一轮的状态驻留时间；横轴按阶段排列，不表示相等时长，EC 仅在有视觉输入时出现。E 为视觉编码，EC 为保存的视觉编码结果，P 为 prefill，D 为 decode。 | [SVG](figure-9-2-state.svg) | [PNG](figure-9-2-state.png) | [PDF](figure-9-2-state.pdf) |
| 9-6 | 源 P 保留完整状态，目的 D 同时分配同样大小的接收空间。GQA 状态两端各 1.125 GiB，传输过程共占 2.25 GiB；紧凑 MLA 状态两端各 549 MiB，共占 1.07 GiB。方框宽度按字节数比例绘制。 | [SVG](figure-9-kv-residency.svg) | [PNG](figure-9-kv-residency.png) | [PDF](figure-9-kv-residency.pdf) |
| 9-7 | 完整的 1.125 GiB 载荷已经写入目的端，P 随后发出完成标记。标记本身不再搬移数据，只规定先写完、后使用的顺序：D 看到标记才读取状态。 | [SVG](figure-9-kv-publish.svg) | [PNG](figure-9-kv-publish.png) | [PDF](figure-9-kv-publish.pdf) |
| 9-8 | 本算例将执行权交给 D 后释放 P 的源缓冲，D 保留上下文并继续生成。源端空间用于后续请求。 | [SVG](figure-9-kv-release.svg) | [PNG](figure-9-kv-release.png) | [PDF](figure-9-kv-release.pdf) |
| 9-9 | 每张 A100 在 P 阶段提供约 1.17 请求/s，每张 H20 在 D 阶段提供约 1.14 请求/s。P 池 4.67 请求/s，D 池 4.55 请求/s，均低于网卡约 20.7 请求/s 的交接能力。 | [SVG](figure-9-pd-layout.svg) | [PNG](figure-9-pd-layout.png) | [PDF](figure-9-pd-layout.pdf) |
| 9-10 | 阶段配比如何限制请求率。四张 A100 与四张 H20，阶段能力见例 9.2；横轴为分给 P 的 A100 数，纵轴为分给 P 的 H20 数，其余分给 D。每格取两池能力与 25 GB/s 网卡交接能力的最小值，不含排队；颜色深浅表示可持续的请求率，单位为请求/s，框出的格子为最优配比。 | [SVG](figure-9-3-pd.svg) | [PNG](figure-9-3-pd.png) | [PDF](figure-9-3-pd.pdf) |
| 9-11 | 请求组成改变资源分配。四张 A100 与四张 H20，阶段能力按例 9.2 的方法推出；第一行为 8192 输入、1025 输出的推理请求，第二行只减少 P 的新输入，第三行恢复完整输入并将输出减至 129 个 token。方块表示卡，每行下方为对应的吞吐率上限。P 为 prefill 池，D 为 decode 池。 | [SVG](figure-9-4-allocation.svg) | [PNG](figure-9-4-allocation.png) | [PDF](figure-9-4-allocation.pdf) |
| 9-12 | 把一份 36 MiB 专家权重从主存送到 GPU，再由 GPU 读取本地输入完成计算。 | [SVG](figure-9-5-local.svg) | [PNG](figure-9-5-local.png) | [PDF](figure-9-5-local.pdf) |
| 9-13 | 输入从 GPU 交给 CPU，CPU 使用主存权重执行专家，结果回到 GPU。每次 token 到专家的分派，传入和传出的特征向量合计 16 KiB；并行的 GPU 常驻专家分支完成后再汇合。 | [SVG](figure-9-local-cpu.svg) | [PNG](figure-9-local-cpu.png) | [PDF](figure-9-local-cpu.pdf) |
| 9-14 | 专家复用改变执行位置的选择。八个专家各有 36 MiB BF16 权重。CPU 为单颗 Xeon Platinum 8452Y，AVX-512 与 AMX kernel 分别按论文实测的 1.8 与 21.3 TFLOP/s、同插槽内存 220 GB/s 计；GPU 为 A100 40GB PCIe，按峰值的 50% 计为 156 TFLOP/s、778 GB/s；PCIe 交接 25 GB/s，每次启动 5 μs。横轴为对数刻度，曲线按例 9.3 计算单层专家路径，未含格式转换。 | [SVG](figure-9-6-reuse.svg) | [PNG](figure-9-6-reuse.png) | [PDF](figure-9-6-reuse.pdf) |
| 9-15 | 八个 Qwen3-235B-A22B 专家各处理 128 个 token 时，单颗 Xeon Platinum 8452Y 上的两项时间：读取八份 BF16 权重共 288 MiB，矩阵计算共 38.7 GFLOPs。粗框标出较长的一项，即这条路径的耗时下界。左右两图横轴刻度不同；AVX-512 与 AMX kernel 的算力、同插槽与跨插槽带宽均为论文实测值。 | [SVG](figure-9-cpu-bottleneck.svg) | [PNG](figure-9-cpu-bottleneck.png) | [PDF](figure-9-cpu-bottleneck.pdf) |
| 9-16 | 512 次分派覆盖 128 个专家，每专家四行。矩形宽为专家数，高为每专家行数，面积为分派次数。 | [SVG](figure-9-7-footprint.svg) | [PNG](figure-9-7-footprint.png) | [PDF](figure-9-7-footprint.pdf) |
| 9-17 | 八个专家各处理 64 行，总面积仍为 512。两图横纵轴相同，权重读取却从 4608 MiB 降至 288 MiB。 | [SVG](figure-9-footprint-reuse.svg) | [PNG](figure-9-footprint-reuse.png) | [PDF](figure-9-footprint-reuse.pdf) |
| 9-18 | 一层 MoE 在两台服务器间的执行顺序，时间从上到下。A0–A3 执行注意力与路由，B0–B3 执行专家。小方块表示一张 A 卡发往一张 B 卡的一组输入，颜色标出它去往哪张 B 卡；dispatch 把各色方块送到同色的 B 卡，combine 再把结果送回原来的 A 卡。两次交换都是 4×4 的 All-to-All。 | [SVG](figure-9-ep-layer.svg) | [PNG](figure-9-ep-layer.png) | [PDF](figure-9-ep-layer.pdf) |
| 9-19 | 四个 micro-batch 在注意力节点与专家节点间执行，每个 micro-batch 注意力 2 ms、专家 3 ms，忽略交接。上图依次执行，两个节点轮流空闲；下图交错执行，micro-batch 1 做专家计算时 micro-batch 2 做注意力。流水稳定后，专家节点连续工作，每 3 ms 完成一个 micro-batch。 | [SVG](figure-9-af-pingpong.svg) | [PNG](figure-9-af-pingpong.png) | [PDF](figure-9-af-pingpong.pdf) |
| 9-20 | 一次 PD 交接与一步 AF 交接的串行时间随每次启动开销的变化，25 GB/s 链路。PD 只启动一次，斜率为 1；AF 一步 72 次启动，斜率为 72。两条 PD 线分别对应 GQA 状态 1.125 GiB 与紧凑 MLA 状态 549 MiB，与 AF 线的交点即临界启动时间 680 与 324 μs；50 GB/s 链路下交点移到 340 与 162 μs。 | [SVG](figure-9-mla-handoff.svg) | [PNG](figure-9-mla-handoff.png) | [PDF](figure-9-mla-handoff.pdf) |
| 9-21 | 总计 512 次专家分派均分到八张卡，每卡 64 次；虚线表示全部计算结束、可以汇合的时刻。 | [SVG](figure-9-9-balance.svg) | [PNG](figure-9-9-balance.png) | [PDF](figure-9-9-balance.pdf) |
| 9-22 | 512 次全部落在卡 0，其他卡空闲。相同总计算量，需要等待卡 0 完成；两图使用相同时间尺度。 | [SVG](figure-9-balance-hotspot.svg) | [PNG](figure-9-balance-hotspot.png) | [PDF](figure-9-balance-hotspot.pdf) |
| 9-23 | 同一个热点专家在三种 EP 规模下造成的卡间 skew。256 个专家，1024 个 token 各选 8 个，专家 0 收到平均值 4 倍的 128 行。每根柱是一张卡，柱内每一段是这张卡上的一个专家，橙色为热点专家；纵轴为该卡行数除以每卡平均行数。每幅图只画卡 0、1、2 和最后一张卡，其余各卡与卡 1 相同。 | [SVG](figure-9-ep-scale-cards.svg) | [PNG](figure-9-ep-scale-cards.png) | [PDF](figure-9-ep-scale-cards.pdf) |
| 9-24 | 最忙卡行数与每卡平均行数之比随 EP 组卡数的变化。橙线为一个 4 倍热点专家，不含随机波动，可以直接手算；蓝线为均匀随机路由，是固定种子模拟 1000 批的平均值。256 个专家按编号均分，不设副本；横轴为对数刻度。 | [SVG](figure-9-ep-scale-sweep.svg) | [PNG](figure-9-ep-scale-sweep.png) | [PDF](figure-9-ep-scale-sweep.pdf) |
| 9-25 | 四个专家组在 dispatch 阶段接收、combine 阶段发送的载荷。均衡与热点分布总计均为每方向 64 MiB；热点组在两个阶段都承担 40 MiB。柱高表示字节需求，不表示测得的瞬时带宽。 | [SVG](figure-9-ep-skew.svg) | [PNG](figure-9-ep-skew.png) | [PDF](figure-9-ep-skew.pdf) |
| 9-26 | 热点持续多久，专家复制才值得。每批节省约 0.240 ms；同一台 HGX H100 内经 NVLink 复制一次约 0.622 ms，第 3 批开始净获益；跨服务器经 ConnectX-7 网卡复制约 5.32 ms，第 23 批开始净获益。曲线使用例 9.6 中未经四舍五入的时间计算；七张接收卡各需额外 36 MiB，假设热点不变。 | [SVG](figure-9-10-experts.svg) | [PNG](figure-9-10-experts.png) | [PDF](figure-9-10-experts.pdf) |
| 9-27 | 整批依次分派 0.336 ms、计算 0.156 ms、合并 0.336 ms，总时间 0.827 ms；数值取自第 9.4.1 节表中跨服务器的均衡分布。 | [SVG](figure-9-11-overlap.svg) | [PNG](figure-9-11-overlap.png) | [PDF](figure-9-11-overlap.pdf) |
| 9-28 | 每个 micro-batch 的各阶段时间减半，三条轨道使用独立资源。第一个 micro-batch 计算时可以 dispatch 第二个 micro-batch，总时间降到 0.581 ms。 | [SVG](figure-9-overlap-pipeline.svg) | [PNG](figure-9-overlap-pipeline.png) | [PDF](figure-9-overlap-pipeline.pdf) |
| 9-29 | 一个 token 选中的两条专家分支，教学时长分别为 0.5 ms 与 1.4 ms。每条都依次经过 dispatch、计算与 combine；同一个 token 要等两份结果，图中忽略本地加权合并的时间。灰色表示快分支的结果到达之后等待的时间。 | [SVG](figure-9-ep-tail.svg) | [PNG](figure-9-ep-tail.png) | [PDF](figure-9-ep-tail.pdf) |
| 9-30 | 虚线表示按标识查找对象位置。目录用于定位，实际 KV 对象用于恢复计算；路由前还需确认对象版本与可用性。 | [SVG](figure-9-cache-directory.svg) | [PNG](figure-9-cache-directory.png) | [PDF](figure-9-cache-directory.pdf) |
| 9-31 | DGX A100 中每张 A100 分到的四级存储。方框宽度只表示容量次序；右侧是这一级到 GPU 的路径，以及取回 1.125 GiB 前缀所需的时间。远端取回先经网卡到主机内存，再经 PCIe 到 GPU，两段串行。 | [SVG](figure-9-kv-tiers.svg) | [PNG](figure-9-kv-tiers.png) | [PDF](figure-9-kv-tiers.pdf) |
| 9-32 | 所需容量随复用间隔线性增长。斜线为 $C=rT$，其中 $r\approx1.41$ GB/s 是一张 A100 连续执行无命中 8K prefill 时产生 KV 的速率；三条虚线是每张 GPU 在三级存储中的容量；两条竖线标出两类负载 80% 复用所在的时间范围。两轴均为对数刻度。 | [SVG](figure-9-kv-capacity.svg) | [PNG](figure-9-kv-capacity.png) | [PDF](figure-9-kv-capacity.pdf) |
| 9-33 | 命中率随容量增加而趋于饱和。数据为 Mooncake 一小时采样 trace 在 LRU 淘汰下的命中率，每块 512 个 token；横轴按 Qwen3-8B 每 token 144 KiB 换算为字节。这只是采样得到的一段流量，真实服务所需的容量按流量同比例放大。 | [SVG](figure-9-kv-hit.svg) | [PNG](figure-9-kv-hit.png) | [PDF](figure-9-kv-hit.pdf) |
| 9-34 | 先把 1.125 GiB 历史 KV 整份从主机内存读入，再计算 256 个新 token，共 79.2 ms。橙色为 PCIe 读取，绿色为 GPU 计算，每一小段对应一层。 | [SVG](figure-9-kv-load-serial.svg) | [PNG](figure-9-kv-load-serial.png) | [PDF](figure-9-kv-load-serial.pdf) |
| 9-35 | 逐层预加载。GPU 计算某一层时，PCIe 读取后面的层；每层读取 1.34 ms、计算 0.857 ms，计算每层都要等待读取，总时间 49.2 ms 由读取决定。 | [SVG](figure-9-kv-load-layerwise.svg) | [PNG](figure-9-kv-load-layerwise.png) | [PDF](figure-9-kv-load-layerwise.pdf) |
| 9-36 | 轮到这个请求之前，趁上一个 batch 执行时先读入前 14 层（448 MiB）；其余 22 层的读取被计算完全掩盖，总时间等于计算本身的 30.9 ms。三幅图的横轴相同。 | [SVG](figure-9-kv-load-preload.svg) | [PNG](figure-9-kv-load-preload.png) | [PDF](figure-9-kv-load-preload.pdf) |
| 9-37 | 主机内存有四个位置，其中一个空出来接收读入的数据，其余三个留给队列中接下来的 J2—J4。J3 的状态还在 SSD 上，趁它排队时读入空位；J6 排在这三个请求之后，下次使用最晚，先换出到 SSD。 | [SVG](figure-9-kv-prefetch.svg) | [PNG](figure-9-kv-prefetch.png) | [PDF](figure-9-kv-prefetch.pdf) |
| 9-38 | 读入的页不一定全部成为可复用前缀。正常重启后的这一请求读入 64 个各含 16 个 token 的页，只复用前 63 页；末页仍需处理。每页 2.25 MiB，该请求的匹配边界为 1008 个 token。 | [SVG](figure-9-12-cache.svg) | [PNG](figure-9-12-cache.png) | [PDF](figure-9-12-cache.pdf) |
| 9-39 | A 本地缓存已命中，GPU 排队 250 ms 后再计算 30.9 ms，首 token 在 281 ms 返回。灰为排队，绿为计算。 | [SVG](figure-9-13-route.svg) | [PNG](figure-9-13-route.png) | [PDF](figure-9-13-route.pdf) |
| 9-40 | B 在 20 ms 空闲，随后在 A100 上重算 887 ms，首 token 在 907 ms 返回。 | [SVG](figure-9-route-1.svg) | [PNG](figure-9-route-1.png) | [PDF](figure-9-route-1.pdf) |
| 9-41 | 取回先查找 10 ms，再经 50 GbE 以 6.25 GB/s 读取 1.125 GiB 至主存，最后经 PCIe 以 25 GB/s 搬到 GPU。计算要等数据和 GPU 都就绪，首 token 约 282 ms 返回，比 A 慢约 1.6 ms。 | [SVG](figure-9-route-2.svg) | [PNG](figure-9-route-2.png) | [PDF](figure-9-route-2.pdf) |
| 9-42 | 远端链路换成 200 GbE（25 GB/s）后，首 token 约 137 ms 返回。橙为远端读取，蓝为主存到 GPU；四图均从请求到达起计时，横轴相同。 | [SVG](figure-9-route-3.svg) | [PNG](figure-9-route-3.png) | [PDF](figure-9-route-3.pdf) |
| 9-43 | 缓存亲和性与空闲执行位置的比较。A 保留全局 KV 与编码器 SWA；B 需要 4.666 ms 全局传输和假设的 8 ms 编码器恢复。两端共同的解码器重放等后续工作略去，只比较不同的串行准备时间；A 的排队时间从 10 ms 增到 20 ms 时，更快的方案由 A 变为 B。灰色为等待队列，其他色块分别为全局状态传输与编码器局部状态恢复。 | [SVG](figure-9-v41-routing.svg) | [PNG](figure-9-v41-routing.png) | [PDF](figure-9-v41-routing.pdf) |
| 9-44 | 服务余量决定启动积压的消退速度。连续流量模型，每秒到达 3.5 个请求，启动 10 秒后积压 35 个。就绪后服务率分别为直接 PD 的 4.55、理想分块共置的 4.17 和不分块共置的 3.02 请求/s；前两者从开始启动算起在第 43 与第 63 秒排空，后者持续积压。例 9.8 的排空期限为第 60 秒。 | [SVG](figure-9-17-service.svg) | [PNG](figure-9-17-service.png) | [PDF](figure-9-17-service.pdf) |
| 9-45 | 后台复制需要赶上仍在增长的状态。开始时待复制状态为 41.1 GB，源端每秒增长约 0.172 GB；目标经 25 GB/s 的网卡约 1.65 秒赶上，经 6.25 GB/s 的 50 GbE 约 6.76 秒赶上。曲线相交前，垂直距离就是尚未复制的数据量；相交后，目标只需跟随源端的新增状态。 | [SVG](figure-9-14-migration.svg) | [PNG](figure-9-14-migration.png) | [PDF](figure-9-14-migration.pdf) |
| 9-46 | 输出记录决定继续哪条序列，KV checkpoint 决定从哪里补算。假定 1025 个输出均已可靠记录，但 KV 只保存了原输入。下方按输入、前 1024 个输出和第 1025 个输出分段示意，宽度不按 token 数量比例绘制。 | [SVG](figure-9-15-recovery.svg) | [PNG](figure-9-15-recovery.png) | [PDF](figure-9-15-recovery.pdf) |
| 9-47 | P 直接向 D 交接 1.125 GiB 上下文 KV 缓存，只经过一次直接传输。P 为 prefill，D 为后续逐 token 的 decode。 | [SVG](figure-9-16-composition.svg) | [PNG](figure-9-16-composition.png) | [PDF](figure-9-16-composition.pdf) |
| 9-48 | P 先向池写入完整 1.125 GiB 并发布，D 再取回同一对象，共经过写入和取回两次传输。后续实例还可以复用池中对象。P 为 prefill，D 为后续逐 token 的 decode。 | [SVG](figure-9-composition-pool.svg) | [PNG](figure-9-composition-pool.png) | [PDF](figure-9-composition-pool.pdf) |
