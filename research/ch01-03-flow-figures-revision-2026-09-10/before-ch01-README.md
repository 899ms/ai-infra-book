# 第一章图片与生成记录

六幅图均由本书自行绘制。数据图直接读取固定计算结果与原始实验的分析记录，结构图采用教学示意；均提供可编辑 SVG 和 160 dpi PNG。SVG 保留文字，需要中文字体；HTML 阅读版嵌入 PNG，避免缺少字体导致显示变化。

| 图 | SVG | PNG | 内容 |
| --- | --- | --- | --- |
| 1-1 | [六层全景](figure-1-1-panorama.svg) | [预览](figure-1-1-panorama.png) | 六层塔、跨层平台、共同物理条件 |
| 1-2 | [请求路由与执行](figure-1-2-request.svg) | [预览](figure-1-2-request.png) | 入口、路由、实例调度、生成循环与输出 |
| 1-3 | [数据中心与超节点](figure-1-3-datacenter.svg) | [预览](figure-1-3-datacenter.png) | CPU／GPU 连接、内部互联、跨超节点网络 |
| 1-4 | [关键数字](figure-1-4-numbers.svg) | [预览](figure-1-4-numbers.png) | Jeff Dean 历史延迟与独立的 H100 SXM 资源卡 |
| 1-5 | [生成估算](figure-1-5-budget.svg) | [预览](figure-1-5-budget.png) | 70B 教学下界、理想批复用、独立 Qwen 实测 |
| 1-6 | [架构选择](figure-1-6-designs.svg) | [预览](figure-1-6-designs.png) | TPU、SmartNIC、UB 的动机、变化与限制 |

来源与原件 SHA-256 见 [sources.json](sources.json)，绘图数据见 [figure-data.json](figure-data.json)，输出清单见 [manifest.json](manifest.json)。构建前会核对来源，来源改变时停止并要求重新审阅，不静默更新既有数据。

在仓库根目录准备 Python 环境，安装本目录 requirements.txt，然后运行：

```sh
python manuscripts/ch01/build.py
```

脚本依次寻找 macOS 的 Arial Unicode／STHeiti 和 Linux 的 Noto Sans CJK。其他环境可指定字体：

```sh
python manuscripts/ch01/build.py --font /path/to/chinese-font.ttf
```

该命令重建六幅 SVG／PNG、图数据、输出清单和第一章 HTML；不修改 Markdown，不运行模型，不覆盖既有实验。计算／测量分面，单位和计时口径在正文、图注与来源清单中分别标明。

[图文验证](validation.json)记录结构、图像、链接与人工图片检查结果。本轮已用独立无头 Chrome 检查桌面与 390px 窄屏，见[当前浏览器记录](../../research/ch01-03-textbook-revision-2026-09-10/browser-review.json)。

图片内部不重复图号或总标题，编号与说明由正文 caption 承担。导出时按可见内容边界裁切，仅留约 0.015 英寸防裁切余量；图内布局间距保留。

正文算式已改为 LaTeX，HTML 使用随目录保存的 KaTeX 0.16.11 渲染；重建还需要 Node.js。公式解析记录见 [math-validation.json](math-validation.json)，桌面／手机复查见 [latex-browser-validation.json](latex-browser-validation.json)，排版截图见 [preview-latex.png](preview-latex.png)。

教材修订新增 Amdahl 定律、带解预算和章末谬误／小结，核心练习为 1-2、1-3、1-4；修改说明与练习数值参考见[修订记录](../../research/ch01-03-textbook-revision-2026-09-10/README.md)。
