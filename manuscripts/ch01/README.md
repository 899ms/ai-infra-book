# 第1章正文与配图

[Markdown 正文](../01-初识 AI Infra.md) · [HTML 阅读版](../01-初识%20AI%20Infra.md)

本章按逐节设计组织概念、推导、例题与练习。当前共 8 幅配图，均提供 SVG 和 PNG；正文、图表中的数学表达采用 LaTeX，HTML 使用本地 KaTeX 渲染并嵌入图片与字体。

[前三章逐节设计](../../research/ch01-03-model-led-rewrite-2026-09-10/section-design.md) · [练习参考解答](../../research/ch01-03-model-led-rewrite-2026-09-10/exercise-answers.md) · [本轮修订记录](../../research/ch01-03-model-led-rewrite-2026-09-10/README.md)

## 配图

图号按阅读顺序排列，文件名保持稳定。

| 图示 | SVG | PNG |
| --- | --- | --- |
| AI Infra 六层全景：从应用需求到设备与互联，右侧为跨层平台能力，底部为共同物理条件。 | [SVG](figure-1-1-panorama.svg) | [PNG](figure-1-1-panorama.png) |
| 请求经过应用、入口、路由、实例调度、GPU 执行与输出返回；另标模型加载、KV 状态与多设备协作。 | [SVG](figure-1-2-request.svg) | [PNG](figure-1-2-request.png) |
| 数据中心通过网络连接多个超节点，放大一个超节点展示计算托盘、CPU 与主存、GPU 与 HBM、内部互联和网卡。 | [SVG](figure-1-3-datacenter.svg) | [PNG](figure-1-3-datacenter.png) |
| 关键数字分为历史访问延迟与 H100 SXM 资源卡。延迟采用对数刻度；容量、带宽与计算吞吐分别列示。 | [SVG](figure-1-4-numbers.svg) | [PNG](figure-1-4-numbers.png) |
| 图 1-5 每卡容量与执行时的权重读取 | [SVG](figure-1-capacity-path.svg) | [PNG](figure-1-capacity-path.png) |
| 教学模型的算力、带宽和批复用变化，以及独立 Qwen3-8B 实测中的吞吐和每请求时间。 | [SVG](figure-1-5-budget.svg) | [PNG](figure-1-5-budget.png) |
| 图 1-7 batch 增长时的计算、读取与吞吐转折 | [SVG](figure-1-batch-transition.svg) | [PNG](figure-1-batch-transition.png) |
| TPU、SmartNIC 与 Unified Bus 分别改变专用资源配置、处理位置和协作范围。 | [SVG](figure-1-6-designs.svg) | [PNG](figure-1-6-designs.png) |

## 构建与数据

在仓库根目录安装本目录 requirements.txt 中的依赖，并准备 Node.js，运行：

```sh
python manuscripts/ch01/build.py
```

生成器查找 macOS 或 Noto 中文字体，也可使用 `--font /path/to/font.ttf`。共享机制图由 [teaching_figures.py](../teaching_figures.py) 生成。

[sources.json](sources.json) 保存输入文件及哈希；[figure-data.json](figure-data.json) 保存绘图数据；[manifest.json](manifest.json) 保存生成产物校验值；[math-validation.json](math-validation.json) 记录公式解析。输入变化时须先审查再更新来源锁。本轮使用已有 calculations、survey 与实验记录以及明确给出的教学条件，没有执行新的 GPU 实验。

## 当前阅读版配图（2026-09-10）

正文现引用 17 幅图，以下清单按当前阅读顺序列出；上文旧图号用于追溯构建记录。

| 图号 | 内容 | SVG | PNG | PDF |
| --- | --- | --- | --- | --- |
| 1-1 | 从应用到设备的六层分工。沿箭头向下，任务逐步落实为运算、程序和物理资源；调度、观测等跨层能力由正文说明。 | [SVG](figure-1-1-panorama.svg) | [PNG](figure-1-1-panorama.png) | [PDF](figure-1-1-panorama.pdf) |
| 1-2 | 应用编排的入口从程序接口扩展到模型与上下文。两列实线由上向下表示调用关系，虚线表示工具调用转入操作系统。固定权重不等于固定应用。 | [SVG](figure-1-programmability.svg) | [PNG](figure-1-programmability.png) | [PDF](figure-1-programmability.pdf) |
| 1-3 | 一次请求先由路由器选择模型实例，再由实例内部的调度器安排执行。灰色外框圈出同一个实例，实线表示请求和工作提交的方向。 | [SVG](figure-1-2-request.svg) | [PNG](figure-1-2-request.png) | [PDF](figure-1-2-request.pdf) |
| 1-4 | 权重加载一次，生成时逐步读取。蓝框表示显存中持续保存的同一份权重，三个绿框表示先后发生的计算；箭头表示读取或结果依赖，步骤间距不代表耗时。 | [SVG](figure-1-weight-lifetime.svg) | [PNG](figure-1-weight-lifetime.png) | [PDF](figure-1-weight-lifetime.pdf) |
| 1-5 | 物理连接的两层视图。上方用数据中心网络连接服务与超节点，下方放大一个超节点，显示主机、网卡、GPU 与显存；线条展示数据路径，设备数量用于示意。 | [SVG](figure-1-3-datacenter.svg) | [PNG](figure-1-3-datacenter.png) | [PDF](figure-1-3-datacenter.pdf) |
| 1-6 | Jeff Dean 2009 年演讲中的三种操作延迟。横轴为对数刻度，每相邻数量级相差十倍；先识别操作，再比较它们在串行等待中的代价。 | [SVG](figure-1-4-numbers.svg) | [PNG](figure-1-4-numbers.png) | [PDF](figure-1-4-numbers.pdf) |
| 1-7 | DeepSeek-R1-Distill-Llama-70B：BF16 权重共 141.11 GB，两卡均分后每卡约 70.55 GB；分组 8 比特量化后共 73.73 GB。各条使用相同尺度，虚线表示一张 H100 SXM 的名义 80 GB 容量。柱长只计权重及相应量化附加数据。 | [SVG](figure-1-capacity-path.svg) | [PNG](figure-1-capacity-path.png) | [PDF](figure-1-capacity-path.pdf) |
| 1-8 | 本例按每参数一字节，将主要权重读取量近似取为 70 GB。权重驻留显存，计算单元每步沿同一接口读取一遍；用读取量除以接口带宽，得到 20.90 ms 的读取下界。 | [SVG](figure-1-read-path.svg) | [PNG](figure-1-read-path.png) | [PDF](figure-1-read-path.pdf) |
| 1-9 | 保持运算量与读取量不变，分别把算力或带宽翻倍。蓝条是权重读取下界，橙条是矩阵计算下界；较长的读取项决定这组条件下的优化方向。 | [SVG](figure-1-5-budget.svg) | [PNG](figure-1-5-budget.png) | [PDF](figure-1-5-budget.pdf) |
| 1-10 | 一批八个请求共享一次权重读取，各产生一个输出。整批读取仍需约 20.90 ms，除以八得到每输出分摊的服务时间；每个请求经历整批执行。 | [SVG](figure-1-batch-reuse.svg) | [PNG](figure-1-batch-reuse.png) | [PDF](figure-1-batch-reuse.pdf) |
| 1-11 | 批内请求增加时，矩阵运算量按 $2BN$ 增长，权重读取保持每批 70 GB。约 148 个请求处两项下界相等，随后计算项主导。 | [SVG](figure-1-batch-transition.svg) | [PNG](figure-1-batch-transition.png) | [PDF](figure-1-batch-transition.pdf) |
| 1-12 | 上述批处理模型的理想输出吞吐率。每批输出数除以时间下界得到曲线；竖虚线与前图对应同一个约 148 请求的转折点。 | [SVG](figure-1-batch-throughput.svg) | [PNG](figure-1-batch-throughput.png) | [PDF](figure-1-batch-throughput.pdf) |
| 1-13 | Qwen3-8B 实测的整批输出吞吐。四档请求数等距排列，纵轴从零开始；模型、精度、输入输出长度和计时范围保持一致。 | [SVG](figure-1-measured-throughput.svg) | [PNG](figure-1-measured-throughput.png) | [PDF](figure-1-measured-throughput.pdf) |
| 1-14 | 同一组实测中的每请求输出间隔。吞吐增加的同时，单个请求的平均间隔也在增大；两张图分别说明设备的输出速度和用户的等待时间。 | [SVG](figure-1-measured-tpot.svg) | [PNG](figure-1-measured-tpot.png) | [PDF](figure-1-measured-tpot.pdf) |
| 1-15 | 专用处理器围绕反复出现的矩阵运算组织计算阵列和输入输出缓冲。缓冲是临时保存待计算或已算完数据的存储区域；三个方框及其箭头展示数据搬运方向。 | [SVG](figure-1-design-tpu.svg) | [PNG](figure-1-design-tpu.png) | [PDF](figure-1-design-tpu.pdf) |
| 1-16 | 可编程网卡在数据进入主机前完成指定的包处理。图中实线跟踪数据；网卡承担的处理减少主机 CPU 的辅助工作。 | [SVG](figure-1-design-smartnic.svg) | [PNG](figure-1-design-smartnic.png) | [PDF](figure-1-design-smartnic.pdf) |
| 1-17 | 统一互联连接不同设备的计算与存储资源。模型分工确定要交换什么，互联负责把数据送到后续使用它的设备。 | [SVG](figure-1-design-ub.svg) | [PNG](figure-1-design-ub.png) | [PDF](figure-1-design-ub.pdf) |
