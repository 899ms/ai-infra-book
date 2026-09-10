# 第三章正文与配图

[阅读版 HTML](../03-推理与训练负载.html) · [正文 Markdown](../03-推理与训练负载.md) · [写作大纲](../../outlines/03-推理与训练负载.md)

正文按六节、十九小节展开，以积压、关键路径、训练状态、有效样本与拟合例题串联，保留十项实验。十一幅图均提供 SVG 与 PNG；编号、图题和说明放在正文图片之外。正文公式以 LaTeX 编写，阅读版使用本地 KaTeX 渲染，图片与字体嵌入 HTML，可离线阅读。

| 图 | 内容 | 文件 |
|---|---|---|
| 3-1 | Prefill、Decode 与逻辑状态增长 | [SVG](figure-3-1-stages.svg) · [PNG](figure-3-1-stages.png) |
| 3-2 | 请求组成、阶段需求与积压 | [SVG](figure-3-2-workload-budget.svg) · [PNG](figure-3-2-workload-budget.png) |
| 3-3 | Agent 逐轮时间、前缀命中与状态 | [SVG](figure-3-3-agent.svg) · [PNG](figure-3-3-agent.png) |
| 3-4 | 多模态阶段与实时语音时序 | [SVG](figure-3-4-realtime.svg) · [PNG](figure-3-4-realtime.png) |
| 3-5 | 训练依赖、矩阵工作与参数状态 | [SVG](figure-3-5-training.svg) · [PNG](figure-3-5-training.png) |
| 3-6 | RL／OPD 循环及有效样本预算 | [SVG](figure-3-6-rl.svg) · [PNG](figure-3-6-rl.png) |
| 3-7 | Scaling Law 拟合、留出与生命周期代理 | [SVG](figure-3-7-scaling.svg) · [PNG](figure-3-7-scaling.png) |
| 3-8 | 训练数据投入及两类 MoE 参数口径 | [SVG](figure-3-8-history.svg) · [PNG](figure-3-8-history.png) |
| 3-9 | 分硬件、分阶段的公开 GPU 小时 | [SVG](figure-3-9-gpu-hours.svg) · [PNG](figure-3-9-gpu-hours.png) |

## 取材与边界

写作读取既有调研、案例笔记、计算结果和实验分析，未执行新的 GPU 实验。[阅读与取舍记录](reading-notes.md)说明正文如何采用这些材料；逐条引用见正文脚注。[sources.json](sources.json)锁定输入文件，[figure-data.json](figure-data.json)保存画图数据，[manifest.json](manifest.json)记录输出校验值。

教学输入、公式计算、历史公开披露与本仓库实测分别标注。尤其注意：reasoning 的三组主评分均无合格任务；Agent 轨迹不能证明通用质量提升；工具等待时 KV 保留只是条件预算；历史音频只有接收记录；相同拟合损失不能证明任务质量相同。V4 专项计算存在范围交叠，不将它们相加当成完整训练步。

## 重建

在仓库根目录运行（Python 3、Node.js）：

```sh
python3 -m venv /tmp/ch03-book-venv
/tmp/ch03-book-venv/bin/pip install -r manuscripts/ch03/requirements.txt
/tmp/ch03-book-venv/bin/python manuscripts/ch03/build.py
/tmp/ch03-book-venv/bin/python manuscripts/ch03/verify.py
```

生成器优先选择 macOS 中文字体，Linux 可安装 Noto CJK，或使用 `--font /path/to/font`。输入校验值变化时生成器会停止，应先审阅差异再更新来源锁。KaTeX 0.16.11 与许可证保存在 `vendor/katex/`。

## 检查

[validation.json](validation.json)检查大纲标题、十项实验、十一幅图、外置图题、本地链接与输入输出校验值；[math-validation.json](math-validation.json)记录公式解析结果；[figure-layout-check.json](figure-layout-check.json)记录图中文字边界。

[browser-validation.json](browser-validation.json)记录独立无头 Chrome 在 1440 px 和 390 px 下的检查：图像加载、公式错误和页面横向溢出。可查看[桌面](preview-1440.png)、[手机](preview-390.png)、[公式和矩阵表](preview-math-table.png)截图。接入式浏览器当时未连接，检查使用独立浏览器进程，没有使用个人浏览器会话。

## 当前配图顺序

图号按正文阅读顺序排列；图片文件名保持稳定，便于核对历史记录。新增机制图由 [teaching_figures.py](../teaching_figures.py) 生成，随各章构建脚本一同运行。

| 图号 | SVG | PNG |
| --- | --- | --- |
| 3-1 | [同一模型的 Prefill 与 Decode](figure-3-1-stages.svg) | [PNG](figure-3-1-stages.png) |
| 3-2 | [请求组成与阶段积压](figure-3-2-workload-budget.svg) | [PNG](figure-3-2-workload-budget.png) |
| 3-3 | [每次尝试的费用与每个成功任务的费用](figure-3-success-cost.svg) | [PNG](figure-3-success-cost.png) |
| 3-4 | [Agent 轨迹与 KV 生命周期](figure-3-3-agent.svg) | [PNG](figure-3-3-agent.png) |
| 3-5 | [图像位置合并与特征宽度的变化](figure-3-vision-shapes.svg) | [PNG](figure-3-vision-shapes.png) |
| 3-6 | [实时交互的端到端时序](figure-3-4-realtime.svg) | [PNG](figure-3-4-realtime.png) |
| 3-7 | [推理与各训练阶段的计算和状态](figure-3-5-training.svg) | [PNG](figure-3-5-training.png) |
| 3-8 | [RL／OPD 的工作与数据流](figure-3-6-rl.svg) | [PNG](figure-3-6-rl.png) |
| 3-9 | [训练预算与生命周期成本](figure-3-7-scaling.svg) | [PNG](figure-3-7-scaling.png) |
| 3-10 | [Llama 与 Qwen 的模型—数据选择](figure-3-8-history.svg) | [PNG](figure-3-8-history.png) |
| 3-11 | [公开 GPU 小时与训练阶段](figure-3-9-gpu-hours.svg) | [PNG](figure-3-9-gpu-hours.png) |


本次段落衔接与配图修订的检查记录见[修订档案](../../research/ch01-03-flow-figures-revision-2026-09-10/README.md)。
