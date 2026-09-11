# 第六章正文与配图

[阅读版 HTML](../06-超节点.md) · [正文 Markdown](../06-超节点.md) · [写作大纲](../../archive/outlines/06-超节点.md)

正文沿“算子分块—跨卡所有权—通信路径—方案选择”组织：6.1 给出贯穿算例和六种并行方式的切分维度一览，6.2 用六个小节逐一介绍 DP、TP、SP、CP、PP、EP，6.3 讨论组合、MoE 负载与模型规模，6.4 起为集合通信、物理组织、内存池与规模选择。当前正文共 51 幅图，提供 SVG、PNG、PDF；图号、完整图题与说明位于图片外。当前索引见文末；网站由正文 Markdown 构建。

以下为早期版本的配图清单，当前编号以文末为准。

| 图 | 内容 | SVG | PNG | PDF |
|---|---|---|---|---|
| 6-1 | 八张卡上的实例分组 | [SVG](figure-6-1-placement.svg) | [PNG](figure-6-1-placement.png) | [PDF](figure-6-1-placement.pdf) |
| 6-2 | 模型分片与每卡内存占用 | [SVG](figure-6-2-capacity.svg) | [PNG](figure-6-2-capacity.png) | [PDF](figure-6-2-capacity.pdf) |
| 6-3 | TP 的切分方向与输出部分和 | [SVG](figure-6-3-tp.svg) | [PNG](figure-6-3-tp.png) | [PDF](figure-6-3-tp.pdf) |
| 6-4 | 四阶段流水的填充与排空 | [SVG](figure-6-4-pipeline.svg) | [PNG](figure-6-4-pipeline.png) | [PDF](figure-6-4-pipeline.pdf) |
| 6-5 | token 派发和专家结果合并 | [SVG](figure-6-5-dispatch.svg) | [PNG](figure-6-5-dispatch.png) | [PDF](figure-6-5-dispatch.pdf) |
| 6-6 | TP 与 EP 的分组及归约方向 | [SVG](figure-6-6-ep-layout.svg) | [PNG](figure-6-6-ep-layout.png) | [PDF](figure-6-6-ep-layout.pdf) |
| 6-7 | 批内专家复用与权重读取 | [SVG](figure-6-7-reuse.svg) | [PNG](figure-6-7-reuse.png) | [PDF](figure-6-7-reuse.pdf) |
| 6-8 | 专家复用与设备负载分布 | [SVG](figure-6-8-expert-load.svg) | [PNG](figure-6-8-expert-load.png) | [PDF](figure-6-8-expert-load.pdf) |
| 6-9 | 环形归约的逐轮状态 | [SVG](figure-6-9-ring-rounds.svg) | [PNG](figure-6-9-ring-rounds.png) | [PDF](figure-6-9-ring-rounds.pdf) |
| 6-10 | 增加 TP 卡数时各项时间的变化 | [SVG](figure-6-10-tp-time.svg) | [PNG](figure-6-10-tp-time.png) | [PDF](figure-6-10-tp-time.pdf) |
| 6-11 | 消息大小与环树选择 | [SVG](figure-6-11-collectives.svg) | [PNG](figure-6-11-collectives.png) | [PDF](figure-6-11-collectives.pdf) |
| 6-12 | 并发时的资源竞争与完成时间 | [SVG](figure-6-12-resources.svg) | [PNG](figure-6-12-resources.png) | [PDF](figure-6-12-resources.pdf) |
| 6-13 | 下联与上联端口分配 | [SVG](figure-6-13-ports.svg) | [PNG](figure-6-13-ports.png) | [PDF](figure-6-13-ports.pdf) |
| 6-14 | 相同发送量与不同物理路径 | [SVG](figure-6-14-topology.svg) | [PNG](figure-6-14-topology.png) | [PDF](figure-6-14-topology.pdf) |
| 6-15 | 三维环面网络的二分链路 | [SVG](figure-6-15-torus.svg) | [PNG](figure-6-15-torus.png) | [PDF](figure-6-15-torus.pdf) |
| 6-16 | 三种系统的连接组织 | [SVG](figure-6-16-systems.svg) | [PNG](figure-6-16-systems.png) | [PDF](figure-6-16-systems.pdf) |
| 6-17 | 借用前后的物理内存位置 | [SVG](figure-6-17-pool-placement.svg) | [PNG](figure-6-17-pool-placement.png) | [PDF](figure-6-17-pool-placement.pdf) |
| 6-18 | 远端读取中的在途事务 | [SVG](figure-6-18-read-window.svg) | [PNG](figure-6-18-read-window.png) | [PDF](figure-6-18-read-window.pdf) |
| 6-19 | 访问频率与带宽需求 | [SVG](figure-6-19-memory-pool.svg) | [PNG](figure-6-19-memory-pool.png) | [PDF](figure-6-19-memory-pool.pdf) |
| 6-20 | 实例数量与四会话的完成顺序 | [SVG](figure-6-20-session-schedule.svg) | [PNG](figure-6-20-session-schedule.png) | [PDF](figure-6-20-session-schedule.pdf) |
| 6-21 | 期限、故障与按时完成会话的平均成本 | [SVG](figure-6-21-scale-cost.svg) | [PNG](figure-6-21-scale-cost.png) | [PDF](figure-6-21-scale-cost.pdf) |

## 来源与重建

[阅读记录](reading-notes.md)说明 calculations、survey、案例与已有实验的采用范围。[sources.json](sources.json)锁定来源，[figure-data.json](figure-data.json)保存画图数据，[manifest.json](manifest.json)保存输出校验值。所有性能教学输入与实测分别标注，没有新执行 GPU 实验。

[贯穿算例说明](continuous-example.md)列出教学设备、访问模型、续写输入、调度与故障条件；[计算脚本](continuity_model.py)生成[完整精度结果](continuity-model.json)。正文先从矩阵与 KV 访问推导单步时间，再累加八步并安排四个会话，图 6-21 使用同一执行模型。原先独立指定 62／100／160 ms 服务时间的调度情景保留在 `figure-data.json` 的 `legacy_schedule` 及原计算材料中。修订前正文与图数据保存在 [archive-before-continuity](archive-before-continuity/manuscript.md)。

在仓库根目录运行：

```sh
python3 -m venv /tmp/ch06-book-venv
/tmp/ch06-book-venv/bin/pip install -r manuscripts/ch06/requirements.txt
/tmp/ch06-book-venv/bin/python manuscripts/ch06/build.py
/tmp/ch06-book-venv/bin/python manuscripts/ch06/verify.py
```

[新增图示脚本](visual_examples.py)绘制容量分摊、TP／EP 分组、专家负载、单步时间分解、端口分配、环面网络二分、内存借用、在途事务和会话时序。[图号与文件清单](figure-catalog.json)统一管理正文图号与生成文件名。

生成器需要 Node.js 和中文字体，默认寻找 macOS Arial Unicode 或 Linux Noto CJK；可用 `--font /path/to/font` 指定。来源校验值变化会停止生成，需审阅来源后更新锁文件。KaTeX 0.16.11 与许可证在 vendor/katex 中。

## 旧版校验与预览

[内容与数据校验](validation.json)覆盖七节与 25 个小节、十项递进练习、十三个公式编号、二十一幅图及外部图注、来源与输出校验值、链接，并独立复算单步执行、会话调度、成本和主要算式；[公式校验](math-validation.json)记录正文全部表达式。[浏览器检查](browser-validation.json)在 1440 px 与 390 px 宽度验证图片加载、公式、目录锚点与页面宽度。

[桌面预览](preview-desktop.png) · [手机预览](preview-mobile.png) · [桌面 MoE 图文](preview-desktop-moe.png)。复杂插图可使用上表中的独立 SVG／PDF 放大阅读。可选浏览器检查使用 Playwright：`python browser-check.py --executable /path/to/chrome`，不属于基本构建依赖。

## 路由观测配套图

[V4-Flash 路由热图 PNG](route-observation.png) · [SVG](route-observation.svg) · [PDF](route-observation.pdf)。采用 `retrieval-2048-A-early` 的 prefill 原始计数，43 层、2036 个有效 token，每层共选择六个路由专家。颜色表示各专家被选择的次数除以 token 数；每层各专家频率之和为 6。这是单个固定输入的观测，不是长期请求分布或跨卡性能测量。

路由热图单独作为配套，主图 6-7 集中比较同样 512 次分派下的专家权重复用。实际路由的正文讨论与来源链接保留。新增图 6-4 解释 PP 的时序，图 6-5 解释专家派发与返回，图 6-9 解释归约各轮数据的变化；容量、所有权、CPU 实测、端口与 NUMA 算例仍由相邻正文和表格展开。

## 本次修订验证

当前正文、来源快照、算例、图形与浏览器验证见[统一视角修订记录](../../research/ub-ep-integration-2026-09-10/README.md)。旧版 manifest、浏览器记录与图号反映当时版本，不作为本次验证结果。

## 当前阅读版配图（2026-09-11）

以下图号以当前正文顺序为准；前面的旧版图表记录仅用于历史对照。

| 图号 | 内容 | SVG | PNG | PDF |
|---|---|---|---|---|
| 6-1 | 相同八张卡上的三种实例分组。每个外框表示一个独立推理实例，内部连线表示完成请求所需的协作。各实例一次处理一个请求时，三种 | [SVG](figure-6-1-placement.svg) | [PNG](figure-6-1-placement.png) | [PDF](figure-6-1-placement.pdf) |
| 6-2 | 单卡实例与分到八张卡后的每卡内存需求。权重和 KV 各分成八份，2 GiB 工作区则在每张卡分别预留。虚线表示 24 G | [SVG](figure-6-2-capacity.svg) | [PNG](figure-6-2-capacity.png) | [PDF](figure-6-2-capacity.pdf) |
| 6-3 | 左侧是一层的输入激活，三个维度分别对应数据并行、序列并行与上下文并行、张量并行的切分位置；右侧是模型结构，流水线并行切在 | [SVG](figure-6-parallel-map.svg) | [PNG](figure-6-parallel-map.png) | [PDF](figure-6-parallel-map.pdf) |
| 6-4 | 两张卡各保存一份完整模型，分别处理不同样本。推理时两张卡互不等待；训练时两张卡的梯度要先汇合，再各自更新参数副本。 | [SVG](figure-6-dp.svg) | [PNG](figure-6-dp.png) | [PDF](figure-6-dp.pdf) |
| 6-5 | 注意力按头分给两张卡，前馈网络按中间维分给两张卡；两处的最后一个投影都只得到部分和，各需要一次 AllReduce 把两 | [SVG](figure-6-tp-layer.svg) | [PNG](figure-6-tp-layer.png) | [PDF](figure-6-tp-layer.pdf) |
| 6-6 | 按权重矩阵的列切分时，每张卡使用完整输入，计算不同的输出元素。格内的转置符号 T 表示将方括号中横排的数解释为列向量。 | [SVG](figure-6-tp-columns.svg) | [PNG](figure-6-tp-columns.png) | [PDF](figure-6-tp-columns.pdf) |
| 6-7 | 按权重矩阵的行切分时，两卡产生形状相同的输出部分和。对应位置相加，恢复完整乘法的结果。 | [SVG](figure-6-tp-rows.svg) | [PNG](figure-6-tp-rows.png) | [PDF](figure-6-tp-rows.pdf) |
| 6-8 | SwiGLU 的两卡切分。上投影按权重矩阵的列划分输出特征，逐元素运算留在本地；下投影按权重矩阵的行划分输入特征。两步均 | [SVG](figure-6-3-tp.svg) | [PNG](figure-6-3-tp.png) | [PDF](figure-6-3-tp.pdf) |
| 6-9 | LayerNorm 和残差只用到本 token 的数据，两张卡各处理一半位置；进入列并行线性层前用 AllGather  | [SVG](figure-6-sp.svg) | [PNG](figure-6-sp.png) | [PDF](figure-6-sp.pdf) |
| 6-10 | 每张卡保存自己那段位置的 Q、K、V。因果注意力下，卡 1 的查询还要用到卡 0 的 K、V，所以 K、V 必须跨卡传递 | [SVG](figure-6-cp.svg) | [PNG](figure-6-cp.png) | [PDF](figure-6-cp.pdf) |
| 6-11 | 八个 token 的因果注意力，横轴为键的位置、纵轴为查询的位置。实色格是必须计算的查询—键配对；前四行归卡 0，后四行 | [SVG](figure-6-context-dependency.svg) | [PNG](figure-6-context-dependency.png) | [PDF](figure-6-context-dependency.pdf) |
| 6-12 | 两个阶段各保存自己那些层的权重。相邻阶段之间只交接激活；训练时梯度沿同一边界反向传递。 | [SVG](figure-6-pp.svg) | [PNG](figure-6-pp.png) | [PDF](figure-6-pp.pdf) |
| 6-13 | 四个等时阶段处理四个独立微批次。每格为 1 ms，同色表示同一微批次。第一项结果在 4 ms 产生，最后一项在 7 ms | [SVG](figure-6-4-pipeline.svg) | [PNG](figure-6-4-pipeline.png) | [PDF](figure-6-4-pipeline.pdf) |
| 6-14 | 注意力和路由器在 token 所在的卡完成；输入按所选专家的所在卡发送，专家算完后结果送回原卡，按路由权重合并。两次交换 | [SVG](figure-6-ep.svg) | [PNG](figure-6-ep.png) | [PDF](figure-6-ep.pdf) |
| 6-15 | 卡 0 持有 token A，选择本地专家 1 与卡 3 上的专家 6。输入沿上方路径派发，专家输出沿下方返回并加权合并 | [SVG](figure-6-5-dispatch.svg) | [PNG](figure-6-5-dispatch.png) | [PDF](figure-6-5-dispatch.pdf) |
| 6-16 | 八张卡排成四个专家分组，每组两卡沿专家中间维分工。同一列的注意力头与 KV 重复四份；每组因此都能在本地得到相同的专家输 | [SVG](figure-6-6-ep-layout.svg) | [PNG](figure-6-6-ep-layout.png) | [PDF](figure-6-6-ep-layout.pdf) |
| 6-17 | 横向箭头表示组内两卡求和，纵向箭头表示四个组求和。格内数字是某个输出元素经组内求和后的值，两列各自都得到相同的完整结果  | [SVG](figure-6-ep-reduction.svg) | [PNG](figure-6-ep-reduction.png) | [PDF](figure-6-ep-reduction.pdf) |
| 6-18 | 64 个 token、每 token 八个专家，共 512 次分派。均匀覆盖与集中选择的有效计算量相同，被选中专家的权重 | [SVG](figure-6-7-reuse.svg) | [PNG](figure-6-7-reuse.png) | [PDF](figure-6-7-reuse.pdf) |
| 6-19 | 均匀使用 128 个专家时，四个 EP 组各处理 128 次 token—专家计算，合计读取 4.5 GiB 权重。 | [SVG](figure-6-8-expert-load.svg) | [PNG](figure-6-8-expert-load.png) | [PDF](figure-6-8-expert-load.pdf) |
| 6-20 | 所选八个专家都在组 0：权重读取降到 288 MiB，512 次计算却全部压在同一组。 | [SVG](figure-6-expert-load-1.svg) | [PNG](figure-6-expert-load-1.png) | [PDF](figure-6-expert-load-1.pdf) |
| 6-21 | 把同样的八个专家分散到四组，将读取量维持在 288 MiB，同时让四组各承担 128 次计算。三图纵轴范围相同。 | [SVG](figure-6-expert-load-2.svg) | [PNG](figure-6-expert-load-2.png) | [PDF](figure-6-expert-load-2.pdf) |
| 6-22 | 仅跟踪块 0 的一个元素：每经过一张卡，就加入该卡的贡献。三轮后得到 1111，保存在卡 3。其他三个块同时沿环推进。 | [SVG](figure-6-9-ring-rounds.svg) | [PNG](figure-6-9-ring-rounds.png) | [PDF](figure-6-9-ring-rounds.pdf) |
| 6-23 | ReduceScatter 结束时，卡 0、1、2、3 分别持有块 1、2、3、0。接下来每轮转发一块，三轮后每卡都拥有 | [SVG](figure-6-ring-gather.svg) | [PNG](figure-6-ring-gather.png) | [PDF](figure-6-ring-gather.pdf) |
| 6-24 | 根据式（6-5）和环形归约模型绘制单步时间。本地内存访问随卡数增加而减少，归约时间则增加；0.20 ms 的其他串行处理 | [SVG](figure-6-10-tp-time.svg) | [PNG](figure-6-10-tp-time.png) | [PDF](figure-6-10-tp-time.pdf) |
| 6-25 | 八卡环形算法与未分段二项树的时间模型，固定每轮 2 μs、有效单向 50 GB/s。交点约为 184 KiB；8 KiB | [SVG](figure-6-11-collectives.svg) | [PNG](figure-6-11-collectives.png) | [PDF](figure-6-11-collectives.pdf) |
| 6-26 | 通信独立运行时，配置 B 用 0.18 ms 完成，快于 A 的 0.24 ms。 | [SVG](figure-6-12-resources.svg) | [PNG](figure-6-12-resources.png) | [PDF](figure-6-12-resources.pdf) |
| 6-27 | 同一配置的两条色带从同一时刻开始。橙色为通信，蓝色为计算；后续工作等待两者完成。A 在 0.44 ms 完成，B 在 0 | [SVG](figure-6-resources-concurrent.svg) | [PNG](figure-6-resources-concurrent.png) | [PDF](figure-6-resources-concurrent.pdf) |
| 6-28 | 三种发起位置。橙色是构造请求项的部件；虚线是 PCIe 边界。CPU 代理线程的控制路径穿越 PCIe 三次，GPU 发 | [SVG](figure-6-initiator.svg) | [PNG](figure-6-initiator.png) | [PDF](figure-6-initiator.pdf) |
| 6-29 | 同一台 32 端口交换机的两种分配，每个端口单向带宽为 50 GB/s。上联链路是所有跨交换机流量的共同出口；16／16 | [SVG](figure-6-13-ports.svg) | [PNG](figure-6-13-ports.png) | [PDF](figure-6-13-ports.pdf) |
| 6-30 | 递归算法第三轮，卡 0 发往卡 4。细线为 16 张卡组成的物理环，箭头标出经过的四条链路。 | [SVG](figure-6-14-topology.svg) | [PNG](figure-6-14-topology.png) | [PDF](figure-6-14-topology.pdf) |
| 6-31 | 同一物理环上，Swing 第三轮卡 0 发往卡 3，经过三条链路。每张卡这一轮的发送量仍为 1 MiB。 | [SVG](figure-6-topology-swing.svg) | [PNG](figure-6-topology-swing.png) | [PDF](figure-6-topology-swing.pdf) |
| 6-32 | 把所有发送方的数据累加到各条有向链路上，取每轮的最大值。递归前三轮均为 4 MiB，Swing 为 4、2、2 MiB。 | [SVG](figure-6-topology-load.svg) | [PNG](figure-6-topology-load.png) | [PDF](figure-6-topology-load.pdf) |
| 6-33 | 左侧是三维环面的一层，每张卡与四个邻居直连，虚线表示每一维首尾相连；从角上的卡到中心的卡要经过四跳，加上第三个维度最多六 | [SVG](figure-6-topology-hops.svg) | [PNG](figure-6-topology-hops.png) | [PDF](figure-6-topology-hops.pdf) |
| 6-34 | 每张卡六个 50 GB/s 端口、每卡发送 32 MiB。沿维度归约时两种拓扑都用满端口带宽；均匀 All-to-All | [SVG](figure-6-topology-patterns.svg) | [PNG](figure-6-topology-patterns.png) | [PDF](figure-6-topology-patterns.pdf) |
| 6-35 | 沿一个维度把三维环面网络分成两半，需要切断中间连接和首尾连接。每处包含 k² 条链路，合计 2k² 条。 | [SVG](figure-6-15-torus.svg) | [PNG](figure-6-15-torus.png) | [PDF](figure-6-15-torus.pdf) |
| 6-36 | k 从 4 增到 8 时，加速器数从 64 增到 512，二分链路从 32 增到 128。两种增长均以 k = 4 时为 | [SVG](figure-6-torus-growth.svg) | [PNG](figure-6-torus-growth.png) | [PDF](figure-6-torus-growth.pdf) |
| 6-37 | 两个本地应用保留各自的 Jetty，经共享传输通道访问远端端点。事务层区分操作及其完成归属，传输层处理报文的可靠交付；共 | [SVG](figure-6-ub-layers.svg) | [PNG](figure-6-ub-layers.png) | [PDF](figure-6-ub-layers.pdf) |
| 6-38 | 左侧网卡位于 PCIe 之后，请求项、门铃、数据和完成项在处理器与网卡之间各穿越 PCIe 一次；右侧控制器位于片上总线 | [SVG](figure-6-ub-controller.svg) | [PNG](figure-6-ub-controller.png) | [PDF](figure-6-ub-controller.pdf) |
| 6-39 | 每台主机 8 个端点时，三种组织的每网卡状态随互联内主机数的变化。虚线为 256 KiB 片上缓存。逐对连接在 8 台主 | [SVG](figure-6-ub-hosts.svg) | [PNG](figure-6-ub-hosts.png) | [PDF](figure-6-ub-hosts.pdf) |
| 6-40 | N 个本地端点与 N 个远端端点之间建立全部通信关系所需的时间，32 个核并行。逐对连接随 N² 增长，端点加通道随 N | [SVG](figure-6-ub-setup.svg) | [PNG](figure-6-ub-setup.png) | [PDF](figure-6-ub-setup.pdf) |
| 6-41 | 三个公开系统的连接层次。NVLink 是 NVIDIA 的设备互联，TPU v4 的光电路交换机连接电互联单元，Unif | [SVG](figure-6-16-systems.svg) | [PNG](figure-6-16-systems.png) | [PDF](figure-6-16-systems.pdf) |
| 6-42 | 借用前的物理占用。每节点容量为 64 GiB，任务 0 的需求为 80 GiB，其中 16 GiB 尚未找到存储位置。颜 | [SVG](figure-6-17-pool-placement.svg) | [PNG](figure-6-17-pool-placement.png) | [PDF](figure-6-17-pool-placement.pdf) |
| 6-43 | 把任务 0 的额外 16 GiB 放在节点 1。节点 1 的绿色 48 GiB 属于任务 1，蓝色 16 GiB 属于任 | [SVG](figure-6-pool-after.svg) | [PNG](figure-6-pool-after.png) | [PDF](figure-6-pool-after.pdf) |
| 6-44 | 一批读取请求发出后，要经过往返时间 L 才能收到结果。最多有 u 个请求在途、每个返回 q 字节时，在一个往返时间内最多 | [SVG](figure-6-18-read-window.svg) | [PNG](figure-6-18-read-window.png) | [PDF](figure-6-18-read-window.pdf) |
| 6-45 | 完整读取 16 GiB 的频率与平均带宽需求。路径带宽为 40 GB/s；每事务返回 256 bytes、往返 2 μs | [SVG](figure-6-19-memory-pool.svg) | [PNG](figure-6-19-memory-pool.png) | [PDF](figure-6-19-memory-pool.pdf) |
| 6-46 | 八个单卡实例中的四个处理会话，另外四个空闲。每个会话执行八步，约 132.4 ms 完成；虚线表示 90 ms 期限。 | [SVG](figure-6-20-session-schedule.svg) | [PNG](figure-6-20-session-schedule.png) | [PDF](figure-6-20-session-schedule.pdf) |
| 6-47 | 四会话同时推进，每个约 69.4 ms 完成。颜色与相邻配置图中的会话一致。本图使用四个 TP=2 实例，每实例两张卡， | [SVG](figure-6-session-tp2.svg) | [PNG](figure-6-session-tp2.png) | [PDF](figure-6-session-tp2.pdf) |
| 6-48 | 每个实例顺序处理两个会话，分别在约 41.3 ms 和 82.7 ms 完成。本图使用两个 TP=4 实例，每实例四张卡 | [SVG](figure-6-session-tp4.svg) | [PNG](figure-6-session-tp4.png) | [PDF](figure-6-session-tp4.pdf) |
| 6-49 | 单会话缩短到约 34.2 ms，四会话依次执行，最后一个约 137.0 ms 完成。四图横轴使用同一尺度。本图使用一个  | [SVG](figure-6-session-tp8.svg) | [PNG](figure-6-session-tp8.png) | [PDF](figure-6-session-tp8.pdf) |
| 6-50 | 无故障时，按时完成会话的平均成本随期限变化。八卡计费至所有会话结束；曲线从至少三个会话按时完成处开始。TP 数值为每实例 | [SVG](figure-6-21-scale-cost.svg) | [PNG](figure-6-21-scale-cost.png) | [PDF](figure-6-21-scale-cost.pdf) |
| 6-51 | 20 ms 时卡 0 故障，受影响实例在 60 ms 从当前会话起点重新执行，增加恢复费 1。采用与无故障图相同的计费方 | [SVG](figure-6-scale-cost-fault.svg) | [PNG](figure-6-scale-cost-fault.png) | [PDF](figure-6-scale-cost-fault.pdf) |
