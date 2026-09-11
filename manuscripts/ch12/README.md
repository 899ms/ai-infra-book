# 第十二章正文与配图

[阅读版 HTML](../12-端边云协同.md) · [正文 Markdown](../12-端边云协同.md) · [写作大纲](../../archive/outlines/12-端边云协同.md)

正文按五节、21 个小节展开。图片用于分析各步骤的耗时与依赖，音频用于解释连续播放，30 轮截图任务贯穿分工与部署；最后从已完成十轮的状态比较剩余二十轮。12.3.5 的 Queqiao 案例先介绍集中部署的动机、系统结构和设计目标，再通过预测、对照实验和执行记录解释性能差异，十项练习按计算、改变条件和解释机制分步展开。

十六幅插图提供 SVG、PNG 和 PDF。图号、完整图题与说明均位于图片外；图内仅含面板说明、对象、图例与单位。HTML 内嵌图片、数学公式和公式字体，可离线阅读，外部来源链接仍指向仓库。点击插图可打开大图并横向查看，手机也可缩放页面；独立 SVG／PDF 适合放大或出版使用。

| 图 | 说明 | SVG | PNG | PDF |
|---|---|---|---|---|
| 12-1 | 上行速率改变三种精修方案的完成时间 | [SVG](figure-12-1-raw.svg) | [PNG](figure-12-1-raw.png) | [PDF](figure-12-1-raw.pdf) |
| 12-2 | 分块计算怎样与后续上传重叠 | [SVG](figure-12-2-overlap.svg) | [PNG](figure-12-2-overlap.png) | [PDF](figure-12-2-overlap.pdf) |
| 12-3 | 一个音频块晚到如何推迟后续播放 | [SVG](figure-12-3-paths.svg) | [PNG](figure-12-3-paths.png) | [PDF](figure-12-3-paths.pdf) |
| 12-4 | 接收比播放慢时缓冲逐渐耗尽 | [SVG](figure-12-4-buffer.svg) | [PNG](figure-12-4-buffer.png) | [PDF](figure-12-4-buffer.pdf) |
| 12-5 | 下一轮截图依赖本轮操作完成 | [SVG](figure-12-5-agent.svg) | [PNG](figure-12-5-agent.png) | [PDF](figure-12-5-agent.pdf) |
| 12-6 | 相同上行下原图与完整视觉特征的传输时间 | [SVG](figure-12-6-placement.svg) | [PNG](figure-12-6-placement.png) | [PDF](figure-12-6-placement.pdf) |
| 12-7 | 逐轮节省如何抵消迁移开销 | [SVG](figure-12-7-migration.svg) | [PNG](figure-12-7-migration.png) | [PDF](figure-12-7-migration.pdf) |
| 12-8 | 两台设备每层都要汇总结果才能继续计算 | [SVG](figure-12-8-sync.svg) | [PNG](figure-12-8-sync.png) | [PDF](figure-12-8-sync.pdf) |
| 12-9 | 窗口用完后链路空闲等待确认 | [SVG](figure-12-9-window.svg) | [PNG](figure-12-9-window.png) | [PDF](figure-12-9-window.pdf) |
| 12-10 | 相同发送轨迹下交付顺序改变音频完成时间 | [SVG](figure-12-10-transport.svg) | [PNG](figure-12-10-transport.png) | [PDF](figure-12-10-transport.pdf) |
| 12-11 | 短数据帧也需要相同的无线交换固定开销 | [SVG](figure-12-11-wireless.svg) | [PNG](figure-12-11-wireless.png) | [PDF](figure-12-11-wireless.pdf) |
| 12-12 | 两条接入路径汇入共同出口 | [SVG](figure-12-12-multipath.svg) | [PNG](figure-12-12-multipath.png) | [PDF](figure-12-12-multipath.pdf) |
| 12-13 | 调优基线使同一语音请求的时间差缩小 | [SVG](figure-12-13-queqiao.svg) | [PNG](figure-12-13-queqiao.png) | [PDF](figure-12-13-queqiao.pdf) |
| 12-14 | 不同执行设备的时间组成 | [SVG](figure-12-14-budgets.svg) | [PNG](figure-12-14-budgets.png) | [PDF](figure-12-14-budgets.pdf) |
| 12-15 | 云路径上行决定部署方案何时满足期限和何时更快 | [SVG](figure-12-15-deployment.svg) | [PNG](figure-12-15-deployment.png) | [PDF](figure-12-15-deployment.pdf) |
| 12-16 | 保留提交记录可以少做哪些工作 | [SVG](figure-12-16-recovery.svg) | [PNG](figure-12-16-recovery.png) | [PDF](figure-12-16-recovery.pdf) |

## 来源与重建

[阅读记录](reading-notes.md)说明 calculations、survey、协议、案例和已有实验的实际采用范围。[sources.json](sources.json)锁定来源，[figure-data.json](figure-data.json)保存图数据及条件，[manifest.json](manifest.json)保存输出校验值。正文明确区分固定形状计算、教学参数与已有实测，没有新执行模型、网络或设备性能实验。

在仓库根目录运行：

```sh
python3 -m venv /tmp/ch12-book-venv
/tmp/ch12-book-venv/bin/pip install -r manuscripts/ch12/requirements.txt
/tmp/ch12-book-venv/bin/python manuscripts/ch12/build.py
/tmp/ch12-book-venv/bin/python manuscripts/ch12/verify.py
```

生成需要 Node.js 与中文字体，默认使用 macOS Arial Unicode 或 Linux Noto CJK，也可传 `--font /path/to/font`。KaTeX 0.16.11 复用仓库的 `manuscripts/ch06/vendor/katex` 及原有许可证；其生成结果和字体均已嵌入 HTML。来源变化时构建停止，先审阅变化再更新来源锁。

## 校验与预览

[内容与数据校验](validation.json)检查小节、练习、外部图注、来源与输出 SHA-256、本地链接、图片文本与主要算式。[公式检查](math-validation.json)记录 KaTeX 的严格解析结果。[练习算术核对](exercise-check.json)提供关键数值，不替代开放式解释题的讨论。

[浏览器检查](browser-validation.json)覆盖 1440 px 桌面与 390 px 手机，检查图片加载、公式、目录锚点和横向溢出。[插图总览](preview-figures.png)、[桌面图文](preview-desktop-raw.png)、[手机正文](preview-mobile.png)。十六幅插图已逐图目视检查，图例和标签无裁切，所有图片内部均无图号。

可选浏览器复验需要 Playwright 和本地 Chromium／Chrome：

```sh
/tmp/ch12-book-venv/bin/pip install playwright
/tmp/ch12-book-venv/bin/python manuscripts/ch12/browser-check.py --executable '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
```

## 数字论证与配图修订

本次按条件、推导、结论与下一项问题重写全章。配置形状与整数边界保留精确值，性能和成本采用能解释选择的精度。上一轮七幅主图各用一组坐标突出一个关系；播放设备记录、双连接故障及精确统计移入[配套证据说明](evidence-notes.md)和脚注。[修订记录](../../research/ch12-prose-revision-2026-09-10/README.md)保存图文调整及旧稿归档位置。

## 教材体例重写

[本轮修订记录](../../research/ch12-textbook-revision-2026-09-10/README.md)说明统一主例、模型递进和案例重组。正文减少重复小算例，深入解释依赖、摊销与反馈；新增带宽波动、期限余量及恢复进度推导。定义和例题开头交代模型条件，段落以因果解释和推导结果推进。

## 中文表达修订

正文、图注、习题和脚注已逐段润色：按上下文明确设备、部署方案、计算、传输和播放等具体对象，调整生硬搭配与主语不清的句子。计算结果、公式含义和章节结构保持一致。[修订说明](../../research/ch12-language-revision-2026-09-10/README.md)记录本轮修改范围。

## 段落衔接与直观图解

本轮新增九幅图，将分块重叠、缓冲耗尽、Agent 的逐轮依赖、迁移回本、层内同步、窗口停等、共享出口、部署时间组成与恢复进度画出来。每幅图旁说明应看哪一段、哪个箭头或交点，前后段落据此继续推导。所有图按阅读顺序重新编号，[figure-catalog.json](figure-catalog.json)记录编号与文件，[修订记录](../../research/ch12-visual-revision-2026-09-10/README.md)说明衔接调整和数据核对。新增图由 `draw-concepts.py` 绘制，`build.py` 统一生成阅读版和配图。

## 当前阅读版配图（2026-09-10）

正文现引用 34 幅图，以下清单按当前阅读顺序列出；上文旧图号用于追溯构建记录。

| 图号 | 内容 | SVG | PNG | PDF |
| --- | --- | --- | --- | --- |
| 12-1 | 原图经上行到服务器，服务器收齐后处理，再经下行返回完整成片。实线箭头表示数据与处理顺序；连接已建立，双向传播合计 0.1 s。 | [SVG](figure-12-image-path.svg) | [PNG](figure-12-image-path.png) | [PDF](figure-12-image-path.pdf) |
| 12-2 | 压缩和计算加速对任务完成时间的影响随上行速率而变化。本例采用原图 30 MB、成片 5 MB、下行 100 Mbit/s、RTT 0.1 秒，原处理时间 0.3 秒；压缩方案将输入减半并增加 0.15 秒编解码。三种方案的成片质量相同，连接已建立且各阶段串行。 | [SVG](figure-12-1-raw.svg) | [PNG](figure-12-1-raw.png) | [PDF](figure-12-1-raw.pdf) |
| 12-3 | 整图串行：30 MB 全部上传并传播到服务器后才处理，随后回传 5 MB。上行 20 Mbit/s、下行 100 Mbit/s、单向传播 0.05 s，任务于 12.8 s 完成。 | [SVG](figure-12-2-overlap.svg) | [PNG](figure-12-2-overlap.png) | [PDF](figure-12-2-overlap.pdf) |
| 12-4 | 三块各上传 4 s，每块到达后独立处理 0.1 s，随后回传 1、2、2 MB。前两块的处理和回传与后续上传重叠，完整成片于 12.36 s 返回。 | [SVG](figure-12-overlap-chunks.svg) | [PNG](figure-12-overlap-chunks.png) | [PDF](figure-12-overlap-chunks.pdf) |
| 12-5 | 第一块音频从采集开始计时：20 ms 就绪，32 ms 处理完，33 ms 发完，38 ms 到达；初始缓冲 40 ms 后于 78 ms 播放。圆点标出到达，最后一行是播放设备的时钟。 | [SVG](figure-12-audio-clocks.svg) | [PNG](figure-12-audio-clocks.png) | [PDF](figure-12-audio-clocks.pdf) |
| 12-6 | 第三块晚到使后续各块的播放时间都推迟 5 ms。每块长 20 ms，模型处理 12 ms、发送 1 ms；通常传播 5 ms，第三块传播 50 ms，初始缓冲 40 ms。实线段表示实际播放，浅色轮廓表示原定播放区间，圆点表示到达；所有时间均从开始采集第一块起算。图为上述教学流水的计算结果，播放器等待缺块而不丢弃。 | [SVG](figure-12-3-paths.svg) | [PNG](figure-12-3-paths.png) | [PDF](figure-12-3-paths.pdf) |
| 12-7 | 缓冲量等于初始数据量加累计接收量，再减累计播放量。PCM 播放需要 256 kbit/s，接收只有 130 kbit/s，两条直线的下降速率均为 126 kbit/s。初始缓冲分别包含 60 ms 和 120 ms 音频，约在 0.12 秒和 0.24 秒耗尽；图画到各自第一次耗尽为止。 | [SVG](figure-12-4-buffer.svg) | [PNG](figure-12-4-buffer.png) | [PDF](figure-12-4-buffer.pdf) |
| 12-8 | 截图 Agent 的一轮执行。箭头表示先后依赖，方框宽度不表示耗时。底部返回箭头要经过操作执行与界面更新，才能取得下一轮截图。 | [SVG](figure-12-5-agent.svg) | [PNG](figure-12-5-agent.png) | [PDF](figure-12-5-agent.pdf) |
| 12-9 | 三档本地设备读一遍 Qwen3-8B 单请求 8K decode 主要载荷（16.345 GB）的时间下界。手机按四条 x16 LPDDR5X 通道合计 85.6 GB/s 计算（通道数为声明输入），BF16 与 q4_0 权重分别成行；M3 Ultra 与 RTX PRO 6000 取自第 4.8.2 节的设备表。柱端标注对应的 token/s 上限。 | [SVG](figure-12-local-tiers.svg) | [PNG](figure-12-local-tiers.png) | [PDF](figure-12-local-tiers.pdf) |
| 12-10 | 远端编码：先发送压缩图片，在服务器执行视觉编码，再执行语言模型。 | [SVG](figure-12-encoder-remote.svg) | [PNG](figure-12-encoder-remote.png) | [PDF](figure-12-encoder-remote.pdf) |
| 12-11 | 端侧编码：先执行视觉编码，再发送完整数值特征到语言模型。发送对象随计算的放置位置改变。 | [SVG](figure-12-encoder-local.svg) | [PNG](figure-12-encoder-local.png) | [PDF](figure-12-encoder-local.pdf) |
| 12-12 | 同一图片的完整视觉特征比压缩图片需要更多传输时间。压缩图片为 0.8 MB；Qwen3-VL-4B 在预处理后 640×640 输入上产生 400 个视觉位置，最终投影及三组 DeepStack 合计 [400,10240] BF16，共 8,192,000 bytes。上行速率为 6.4 Mbit/s，柱长表示发送时间；编码、排队和转换时间另计。两种方案处理同一张图片，完成相同的视觉理解任务。 | [SVG](figure-12-6-placement.svg) | [PNG](figure-12-6-placement.png) | [PDF](figure-12-6-placement.pdf) |
| 12-13 | 三种保存对象对应三个重算起点。EC 省去视觉编码；匹配模型权重、前缀与位置的 KV 进一步省去已处理前缀的语言模型计算。容量对应正文固定视觉配置。 | [SVG](figure-12-cache-restart.svg) | [PNG](figure-12-cache-restart.png) | [PDF](figure-12-cache-restart.pdf) |
| 12-14 | 迁移 64 MiB 状态，链路 80 Mbit/s，迁移后每轮节省 0.4 秒。两条曲线分别取恢复时间 1 秒和 2 秒，净节省为 N×0.4 减去传输和恢复时间。圆点标出首次获益的整数轮数；零线以上表示迁移更快，首次获益分别在第 20、22 轮。 | [SVG](figure-12-7-migration.svg) | [PNG](figure-12-7-migration.png) | [PDF](figure-12-7-migration.pdf) |
| 12-15 | 张量并行的一次注意力输出归约：两卡先分别计算，再交换并求和，取得完整输出后进入前馈。横向箭头表示执行顺序，中间纵向箭头表示两卡通信。 | [SVG](figure-12-8-sync.svg) | [PNG](figure-12-8-sync.png) | [PDF](figure-12-8-sync.pdf) |
| 12-16 | 前馈网络也分别计算局部输出，再做两卡归约。完整前馈结果就绪后才能进入下一层，这一结构在 36 层中重复。 | [SVG](figure-12-sync-ffn.svg) | [PNG](figure-12-sync-ffn.png) | [PDF](figure-12-sync-ffn.pdf) |
| 12-17 | 固定窗口 64 KB，链路 20 Mbit/s，一批数据发送需 25.6 ms。为单独显示停等，图设接收端收齐一批后统一确认，从这批数据全部发出到收到整批确认再需 100 ms；每批完整周期为 125.6 ms。正文 W/R 是吞吐上界，图中的整批确认还增加了发送时间，因此实际周期更长。 | [SVG](figure-12-9-window.svg) | [PNG](figure-12-9-window.png) | [PDF](figure-12-9-window.pdf) |
| 12-18 | 同一路径（RTT 0.2 s、容量膝点 333 Mbit/s、丢包率 14%）传送 354,640 bytes 的完成时间，横轴为对数坐标。串行预算是 RTT、模型 30 ms 与发送 8.5 ms 之和；FEC 多发 63 个修复符号（冗余 25.7%）后 99.9% 不需重传；逐轮重传两行是不计窗口收缩与超时的下界；Mathis 上界对应把丢包当作拥塞的 TCP，仅发送就需约 18.3 s。 | [SVG](figure-12-loss-repair.svg) | [PNG](figure-12-loss-repair.png) | [PDF](figure-12-loss-repair.pdf) |
| 12-19 | 整体有序交付：音频第 3 s 已收齐，却因图片缺口继续等到第 7 s。灰色段表示数据已齐后的等待，圆点表示数据交给应用的时刻。 | [SVG](figure-12-10-transport.svg) | [PNG](figure-12-10-transport.png) | [PDF](figure-12-10-transport.pdf) |
| 12-20 | 逐流有序交付：音频在第 3 s 收齐后立即交付，图片仍于第 7 s 交付。两图具有相同的发送、到达与恢复时刻；改变的是跨流等待依赖。 | [SVG](figure-12-transport-per-stream.svg) | [PNG](figure-12-transport-per-stream.png) | [PDF](figure-12-transport-per-stream.pdf) |
| 12-21 | 新建连接时，354640-byte 固定音频的直接路径与 Queqiao 请求中位数分别为 1185.3、301.6 ms。计时从发起请求到收齐结果，输入文件相同，两条路径交替运行。 | [SVG](figure-12-13-queqiao.svg) | [PNG](figure-12-13-queqiao.png) | [PDF](figure-12-13-queqiao.pdf) |
| 12-22 | 保持连接并调优后，同一固定音频的直接路径与 Queqiao 中位数分别为 240.9、236.5 ms。与前图采用相同纵轴，两条路径均接近数据发送、必要往返和处理的总预算。 | [SVG](figure-12-queqiao-tuned.svg) | [PNG](figure-12-queqiao-tuned.png) | [PDF](figure-12-queqiao-tuned.pdf) |
| 12-23 | 后续单因素实验的设计：保持相同文件、路径和其他设置，每次只改变一个因素，配对记录中间事件与总完成时间。此图列出实验步骤。 | [SVG](figure-12-experiment-design.svg) | [PNG](figure-12-experiment-design.png) | [PDF](figure-12-experiment-design.pdf) |
| 12-24 | 报文变短后，固定交换开销仍然存在，因此空口占用时间不会同比缩短。两种成功交换采用相同的 34 μs 接入等待、16 μs SIFS、44 μs MAC ACK，区别只在数据 PPDU：208 μs 或 40 μs。条件为 OFDM54／6、无聚合、无重传的教学参考模型。 | [SVG](figure-12-11-wireless.svg) | [PNG](figure-12-11-wireless.png) | [PDF](figure-12-11-wireless.pdf) |
| 12-25 | 一次取消同时触发两条路径：本地清空待播音频，远端在控制消息到达后停止生成和发送。虚线表示控制流；本地停止播放与远端资源释放有各自的完成时刻。 | [SVG](figure-12-cancel-paths.svg) | [PNG](figure-12-cancel-paths.png) | [PDF](figure-12-cancel-paths.pdf) |
| 12-26 | 两条独立路径按带宽比例分配输入，分别发送 20 MB 和 10 MB，均需 8 s。任务等两部分都齐备后完成。 | [SVG](figure-12-multipath-independent.svg) | [PNG](figure-12-multipath-independent.png) | [PDF](figure-12-multipath-independent.pdf) |
| 12-27 | 30 MB 图片按 20／10 MB 分到 20／10 Mbit/s 两条独立接入，各需 8 秒。两路再经过同一 24 Mbit/s 出口，全部数据通过该出口至少需 10 秒。箭头表示数据路径，不表示传播距离；容量取恒定值。 | [SVG](figure-12-12-multipath.svg) | [PNG](figure-12-12-multipath.png) | [PDF](figure-12-12-multipath.pdf) |
| 12-28 | 端侧：终端工作 6 s，模型计算 57.5 s，共 63.5 s。三图共用 45 s 期限线和同一横轴，颜色分别汇总二十轮同类工作的耗时。 | [SVG](figure-12-14-budgets.svg) | [PNG](figure-12-14-budgets.png) | [PDF](figure-12-14-budgets.pdf) |
| 12-29 | 附近工作站（RTX PRO 6000）：准备 0.27 s，二十轮终端 6 s、模型 2.7 s、传播 0.4 s、上传 1.6 s，共 11.0 s，满足 45 s 期限。虚线表示 45 s 完成期限。 | [SVG](figure-12-budgets-1.svg) | [PNG](figure-12-budgets-1.png) | [PDF](figure-12-budgets-1.pdf) |
| 12-30 | 云端（H100 SXM）：准备 0.14 s，二十轮终端 6 s、模型 1.5 s、传播 4 s、上传 20 s，共 31.6 s。计算更快而传输更久，比附近工作站慢约 20.6 s，仍在期限之内。虚线表示 45 s 完成期限。 | [SVG](figure-12-budgets-2.svg) | [PNG](figure-12-budgets-2.png) | [PDF](figure-12-budgets-2.pdf) |
| 12-31 | 云路径上行改变完整任务的部署选择。剩余 20 轮每轮上传 0.8 MB，云端准备 0.14 秒，每轮其余工作合计约 0.57 秒，因此总时间为 11.6+128/b 秒；附近工作站为 11.0 秒，期限为 45 秒。本例保持模型、处理时间和其他网络参数不变，忽略排队与故障。约 3.8 Mbit/s 起云方案可满足期限；上行再高，云端也不低于 11.6 秒，始终慢于附近工作站。 | [SVG](figure-12-15-deployment.svg) | [PNG](figure-12-15-deployment.png) | [PDF](figure-12-15-deployment.pdf) |
| 12-32 | 保留前九轮提交记录（绿色），只重做未确认的第十轮（橙色）。云端每轮 1.57 s，恢复连接 1 s，增加 2.57 s，总时间为 34.2 s。此例采用可安全重放的操作；已提交的外部操作则先查询其结果。 | [SVG](figure-12-16-recovery.svg) | [PNG](figure-12-16-recovery.png) | [PDF](figure-12-16-recovery.pdf) |
| 12-33 | 丢失十轮进度时，恢复连接后重做十轮，额外 1＋10×1.57≈16.7 s，总任务从 31.6 s 延至 48.3 s，超过 45 s 期限。 | [SVG](figure-12-recovery-all.svg) | [PNG](figure-12-recovery-all.png) | [PDF](figure-12-recovery-all.pdf) |
| 12-34 | 固定任务轨迹中的加速上限。模型从 8 秒缩短至 0.8 秒，其他串行阶段保持 2 秒；第三行表示模型时间趋近于零的理想下界。 | [SVG](figure-12-task-counterfactual.svg) | [PNG](figure-12-task-counterfactual.png) | [PDF](figure-12-task-counterfactual.pdf) |
