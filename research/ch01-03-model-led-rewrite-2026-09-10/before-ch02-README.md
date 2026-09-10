# 第二章正文与配图

第二章按新版大纲的六节、21 个小节扩写，包含九项练习、十五幅配图、LaTeX 公式、四模型总体比较、五张分组模块表（含 V3 历史参照）、参数组成与同条件资源表。

- [HTML 阅读版](../02-模型架构.html)：本地图片内嵌，可离线阅读，含目录跳转与移动端样式。
- [Markdown 编辑源](../02-模型架构.md)：正文及图片引用。
- [图数据](figure-data.json)、[固定来源](sources.json)、[产物校验](manifest.json)。
- [内容与数值验证](validation.json)、[浏览器验证](browser-validation.json)。

数学源使用 `$...$`／`$$...$$`，HTML 由本地 KaTeX 0.16.11 预渲染，并内嵌字体，无 CDN 依赖。图片不包含图号或整图 caption，相关说明保留在正文图下。修订前完整正文及细节存于[修订档案](../../research/ch02-teaching-revision-2026-09-09/before-manuscript.md)。

## 当前配图顺序

图号按正文阅读顺序排列；图片文件名保持稳定，便于核对历史记录。新增机制图由 [teaching_figures.py](../teaching_figures.py) 生成，随各章构建脚本一同运行。

| 图号 | SVG | PNG |
| --- | --- | --- |
| 2-1 | [序列模型的计算依赖](figure-2-1-dependencies.svg) | [PNG](figure-2-1-dependencies.png) |
| 2-2 | [四个模型的层数、隐藏维度与专家数](figure-2-architecture.svg) | [PNG](figure-2-architecture.png) |
| 2-3 | [Qwen3-8B 单层的尺寸与数据流](figure-2-2-layer.svg) | [PNG](figure-2-2-layer.png) |
| 2-4 | [历史读取的阶梯与批内权重复用](figure-2-history.svg) | [PNG](figure-2-history.png) |
| 2-5 | [查询头与共享历史的对应关系](figure-2-3-sharing.svg) | [PNG](figure-2-3-sharing.png) |
| 2-6 | [KV 共享与潜变量压缩](figure-2-4-cache.svg) | [PNG](figure-2-4-cache.png) |
| 2-7 | [V4 的窗口、压缩与索引](figure-2-5-sparse.svg) | [PNG](figure-2-5-sparse.png) |
| 2-8 | [逐位置历史与固定状态矩阵](figure-2-recurrence.svg) | [PNG](figure-2-recurrence.png) |
| 2-9 | [混合注意力与专家计算的组合](figure-2-6-hybrid.svg) | [PNG](figure-2-6-hybrid.png) |
| 2-10 | [状态容量、访问与输入工作](figure-2-7-state-growth.svg) | [PNG](figure-2-7-state-growth.png) |
| 2-11 | [同样的专家运算量与不同的权重读取量](figure-2-expert-reuse.svg) | [PNG](figure-2-expert-reuse.png) |
| 2-12 | [稠密层与 V4 层的数据流](figure-2-8-residual.svg) | [PNG](figure-2-8-residual.png) |
| 2-13 | [模型权重、单步计算与历史状态的对照](figure-2-resources.svg) | [PNG](figure-2-resources.png) |
| 2-14 | [权重、历史与显存可容纳的并发请求数](figure-2-9-capacity.svg) | [PNG](figure-2-9-capacity.png) |
| 2-15 | [请求输入与计算状态映射](figure-2-10-request.svg) | [PNG](figure-2-10-request.png) |

机制图为本书自绘，SVG 保留文本和矢量元素；PNG 避免阅读设备缺少中文字体。公式与数据图只使用已锁定的本地结果或图数据中明确的结构推导。

图 2-10 的 A、B 为长度变化的结构推算；C 仅展示现有 8192-token 完整 prefill 结果，不用未经验证的插值伪造完整内核工作曲线。K3 曲线与 C 使用 compact MLA，正文四模型请求表使用原记录的 expanded MLA，两处均注明执行路径。B 是已计状态访问，而非所有状态读写或物理 HBM 流量。

## 复现

需要 Node.js（用于本地 KaTeX）和 Python 3，安装可选绘图与 Markdown 依赖：

```sh
python -m pip install -r manuscripts/ch02/requirements.txt
python manuscripts/ch02/compare_models.py
python manuscripts/ch02/build.py
python manuscripts/ch02/verify_tables.py
python manuscripts/ch02/verify.py
```

脚本默认查找 macOS 或 Noto 中文字体，也可以使用 `--font /path/to/font.ttf`。本次生成使用 Arial Unicode MS。来源哈希不一致时脚本停止，需先审查变动；不自动接受新数据。运行脚本只重建本章图片、图数据、HTML 和产物清单，不运行模型，不修改 calculations／experiments 原件。

本章保留 V4 专家数值门槛未通过、V4/K3 未完成匹配质量比较、K3 A_log 配置冲突，以及物理 HBM／完整时延未知等证据边界。现有实验被引用和解释，并未因写作而获得更广泛的完成或质量结论。

## 阅读检查

十五幅 PNG 已逐幅检查，修正字体缺字和残差箭头。阅读版用独立的无头 Chrome 检查桌面与 390px 窄屏，确认十五幅内嵌图片、六个目录目标和 LaTeX 渲染结果；截图保存在本目录 `reading-*.png`。图中文字适合放大阅读，窄屏表格在容器内横向滚动。

矩阵表中的权重尺寸由 [verify_tables.py](verify_tables.py) 与固定计算结果核对；[公式渲染校验](math-validation.json)记录 LaTeX 表达式数量。桌面与窄屏截图可用 [check_reading.py](check_reading.py) 在装有 Playwright 和 Chrome 的环境重建。

本轮教材修订保留四个主模型完整表，增加层／调用数与组装规则。`model-comparison.json` 保存整数分项与输入哈希，`compare_models.py` 再生比较表。V4 B1/8K decode 使用公共 `v4-forward` 入口，命令与审读记录见[本轮修订](../../research/ch01-03-textbook-revision-2026-09-10/README.md)。

本次段落衔接与配图修订的检查记录见[修订档案](../../research/ch01-03-flow-figures-revision-2026-09-10/README.md)。
