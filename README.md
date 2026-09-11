# 深入理解 AI Infra：量化分析与系统设计

[![Build](https://github.com/bojieli/ai-infra-book/actions/workflows/book-site.yml/badge.svg)](https://github.com/bojieli/ai-infra-book/actions/workflows/book-site.yml)
[![PDF](https://img.shields.io/badge/PDF-下载-blue)](https://github.com/bojieli/ai-infra-book/releases/latest)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/bojieli/ai-infra-book?style=social)](https://github.com/bojieli/ai-infra-book)

《深入理解 AI Infra》由李博杰撰写，是 GitHub 上获得 **45k+ Star** 的[《深入理解 AI Agent：设计原理与工程实践》](https://github.com/bojieli/ai-agent-book)的姊妹篇。

写完《深入理解 AI Agent》后，在与读者交流和开发 Agent 产品的过程中，我越来越感到：要开发好基于模型的应用，还需要理解它赖以运行的基础设施。就像软件工程师需要学习操作系统、编译原理和计算机体系结构一样，模型应用开发者也需要理解模型背后的执行系统：参数和上下文状态存在哪里，计算怎样执行，多个加速器怎样协作，模型调用怎样与工具程序衔接。

我认为，**编程抽象正在从操作系统上移到模型上下文**：一部分过去需要逐条写进程序的行为，现在可以用模型与上下文表达，底层系统设计可以利用的应用信息也随之改变。本书讨论的正是这次变化中的基础设施——把模型训练和推理当作一个完整的应用、贯穿各层来分析，用上层提供的计算依赖和数据使用时机，重新组织芯片、网络与运行时的工作。

贯穿全书的方法是**从约束推导设计**：根据模型的架构与负载，列出计算、存储、通信和依赖关系，对照硬件的容量、算力和带宽参数，推算性能、找出瓶颈，再决定模型怎样分工、状态放在哪里、执行如何组织，最后用测量检验判断。沿着数据搬移这条线索，本书反复追问五个问题：**搬什么、搬多少、搬几次、经过哪里、谁必须等它。** 更多写作背景见[前言](manuscripts/00-前言.md)。

**[在线阅读](https://bojieli.github.io/ai-infra-book/) · [下载 PDF](https://github.com/bojieli/ai-infra-book/releases/latest) · [章节正文](manuscripts/README.md) · [配套实验](experiments/README.md)**

目前书稿仍是初稿，正在持续修订。可以直接从下方目录阅读 Markdown，也可以通过网站或 PDF 阅读全书。[Releases](https://github.com/bojieli/ai-infra-book/releases) 中保留了各次发布的 PDF，方便查阅和引用同一版本。

## 内容目录

| 章 | 主题 | 主要问题 |
| :--: | --- | --- |
| 1 | [初识 AI Infra](<manuscripts/01-初识 AI Infra.md>) | 一次生成需要多少显存、计算和数据读写？ |
| 2 | [模型架构](manuscripts/02-模型架构.md) | 注意力、历史状态与专家结构如何改变系统需求？ |
| 3 | [推理与训练负载](manuscripts/03-推理与训练负载.md) | 任务阶段、到达模式和状态寿命如何影响资源需求？ |
| 4 | [加速器架构](manuscripts/04-加速器架构.md) | 如何在计算、存储、带宽、功耗与成本之间取舍？ |
| 5 | [算子与运行时](manuscripts/05-算子与运行时.md) | 融合、复用、并发和调度如何减少执行开销？ |
| 6 | [超节点](manuscripts/06-超节点.md) | 多设备协作如何平衡容量、吞吐和同步代价？ |
| 7 | [数据中心网络](manuscripts/07-数据中心网络.md) | 网络带宽、通信方式和拥塞怎样影响计算效率？ |
| 8 | [推理优化](manuscripts/08-单实例推理.md) | 批处理、KV 管理、卸载与推测解码何时有效？ |
| 9 | [分布式推理](manuscripts/09-分布式推理.md) | 如何放置计算和状态，并处理扩缩容与恢复？ |
| 10 | [训练系统](manuscripts/10-训练系统.md) | 怎样安排显存、通信和重算，让训练更高效？ |
| 11 | [资源调度与运行环境](manuscripts/11-资源调度与运行环境.md) | 模型服务和工具环境如何共享资源，减少等待？ |
| 12 | [端边云协同](manuscripts/12-端边云协同.md) | 任务放在本地、边缘还是云端，怎样兼顾效果、延迟和成本？ |

## 适合谁读

如果你已经调用过模型 API，或在自己的机器上运行过模型，想进一步弄清它为什么慢、怎样降低成本，这本书可以作为起点。对于从事系统、网络和芯片工作的工程师，以及相关方向的研究人员和学生，书中也会把各层的设计与实际模型任务联系起来。

阅读时需要一些 Python、线性代数和计算机系统基础，具体要求见[前言](manuscripts/00-前言.md)。建议先读第 1—3 章，了解模型与负载，再根据自己的兴趣选择重点：

- 做模型应用和推理服务，可以重点读第 8、9 章，再看第 11、12 章的任务环境与部署；遇到容量、算子或通信问题时，回到第 4—7 章追踪原因。
- 做系统或网络，可以重点读第 5—7 章，再看第 9、10 章，检查这些机制怎样影响分布式推理与训练。
- 做芯片与体系结构，可以重点读第 4—7 章，并结合后续章节的任务算例，检查硬件指标怎样转化为实际的服务能力。
- 希望系统学习，可以按目录顺序阅读，配合计算工具和实验，逐步核对自己的理解。

遇到书中的算例，不妨先自己估一下，再看推导和实验结果。也可以换成你正在使用的模型和硬件，看看结论会怎样变化。

## 配套计算与实验

[配套计算工具](calculations/README.md)可以用来复算书中的数字，也可以换一组模型和输入，估算资源需求。工具附有模型配置和[结果索引](calculations/results/README.md)，静态计算只需 Python 3.10+ 标准库，无需 GPU 或模型权重。

```bash
git lfs install
git clone https://github.com/bojieli/ai-infra-book.git
cd ai-infra-book
git lfs pull

# 查看模型支持情况
python3 calculations/calc.py models

# 估算 Qwen3-8B 在 8192-token prefill 下的逐算子资源需求
python3 calculations/calc.py forward --model qwen3-8b --tokens 8192 --format md
```

仓库使用 [Git LFS](https://git-lfs.com/) 保存论文和部分较大的输入与测量记录。复现前请下载所需 LFS 文件；仅阅读 Markdown 不必克隆整个资料库。

[配套实验](experiments/README.md)按章节存放在 `experiments/chXX/XX-YY/` 中，每个实验都附有运行方法、输入条件和结果说明。需要 GPU 的实验会注明硬件与依赖要求；没有相应设备，也可以先阅读已有记录。复现或引用结果时，请留意所用的书稿版本、模型、硬件和输入参数。

## 本地构建

**阅读网站**（Python 3.10+）：

```bash
python3 -m venv .venv-site
source .venv-site/bin/activate
python -m pip install -r website/requirements.txt
python scripts/build_site.py
python scripts/check_site.py
python scripts/build_site.py --serve
```

预览地址为 <http://127.0.0.1:8000>。生成文件位于 `build/`，详细说明见[网站构建与发布](website/README.md)。

**全书 PDF**（另需 Pandoc、XeLaTeX 和字体）：

```bash
bash book/build_pdf.sh
```

依赖、字体及单章编译方法见 [PDF 编译说明](book/README.md)。GitHub Actions 会检查 Pull Request 的网站与 PDF 构建；推送到 `main` 后自动生成 Release 并部署 Pages。

## 仓库结构

| 目录 | 内容 |
| --- | --- |
| [manuscripts/](manuscripts/README.md) | 前言、十二章正文、配图与绘图脚本 |
| [experiments/](experiments/README.md) | 按章节组织的实验与运行记录 |
| [calculations/](calculations/README.md) | 资源计算工具、固定输入与复算结果 |
| [case-studies/](case-studies/) | 模型、硬件和系统案例分析 |
| [references/](references/README.md) | 引用资料、来源清单与版本快照 |
| [research/](research/) | 支撑正文的专题调研与证据分析 |
| [book/](book/README.md) | PDF 模板、构建与校验工具 |
| [website/](website/README.md)、[scripts/](scripts/) | 网站资源、构建与检查脚本 |
| [archive/](archive/README.md) | 历史大纲、审阅和写作协调记录 |

## 参与贡献

欢迎通过 [Issues](https://github.com/bojieli/ai-infra-book/issues) 反馈勘误、提出问题，或提交 Pull Request 改进正文、配图和实验。

- **文字与公式**：注明章节、原文位置、问题及建议修改。
- **数据与结论**：提供可查阅来源、版本、单位、假设与计算过程。
- **实验与代码**：给出运行命令、依赖、硬件条件及结果；说明结果适用范围。

请直接修改 `manuscripts/` 中的正文源文件。网站页面由构建生成；临时截图、日志、虚拟环境和本地凭据不应提交。涉及构建或代码的修改，请运行相应检查并在 PR 中说明验证结果。

## 作者与致谢

作者：[李博杰](https://01.me/)（[@bojieli](https://github.com/bojieli)）。

感谢这些年一起做研究和工程的合作者，也感谢相关论文、开源项目与技术文档的作者，以及参与勘误和实验复现的读者。详细致谢见[前言](manuscripts/00-前言.md)，引用来源见正文脚注和[参考资料库](references/README.md)。本书 PDF 沿用《深入理解 AI Agent》的 ElegantBook / XeLaTeX 模板。

## 许可

本书原创正文、配图及配套代码采用 [Apache License 2.0](LICENSE) 许可。Copyright © 2026 Bojie Li（李博杰）。

仓库中的第三方代码、字体、模板与参考资料保留各自的版权和许可声明，不因收录于本仓库而改用 Apache-2.0；具体来源和使用条件见相应目录。
