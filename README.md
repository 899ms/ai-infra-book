# 深入理解 AI Infra：量化分析与系统设计

[![Build](https://github.com/bojieli/ai-infra-book/actions/workflows/book-site.yml/badge.svg)](https://github.com/bojieli/ai-infra-book/actions/workflows/book-site.yml)
[![PDF](https://img.shields.io/badge/PDF-下载-blue)](https://github.com/bojieli/ai-infra-book/releases/latest)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/bojieli/ai-infra-book?style=social)](https://github.com/bojieli/ai-infra-book)

**从一次模型执行出发，理解芯片、网络、推理与训练系统的设计取舍。**

模型为什么能放进显存，却跑不快？增加 GPU 为什么不一定缩短完成时间？算子融合、KV Cache、并行通信和资源调度，怎样共同影响一次任务的质量、延迟与成本？

本书沿着模型执行中的计算、数据搬移与等待，用十二章连接模型架构、加速器、运行时、互联和服务系统。通过公式推导、机制图、具体模型和配套实验，学习估算资源需求、识别瓶颈，并用测量检验设计判断。

**[阅读前言](manuscripts/00-前言.md) · [章节正文](manuscripts/README.md) · [下载 PDF](https://github.com/bojieli/ai-infra-book/releases/latest) · [配套实验](experiments/README.md)**

## 阅读本书

- **PDF**：[Releases](https://github.com/bojieli/ai-infra-book/releases) 提供按提交构建的全书 PDF、封面和校验文件；也可查看[仓库内 PDF](book/AI-Infra-Book.pdf)。
- **Markdown**：下方目录直接进入章节正文，无需安装环境。
- **在线网站**：发布地址为 <https://bojieli.github.io/ai-infra-book/>，首次 Pages 部署成功后可用，支持全文搜索、数学公式与深色模式。

正文持续修订。引用具体结论或复现实验时，请记录所用提交或 Release，以及模型版本、硬件条件和输入参数。

## 适合谁读

本书面向希望理解 AI 系统工作原理的工程师、研究人员和计算机专业学生。具备 Python、线性代数和计算机系统基础会更容易跟上推导；前言介绍了阅读前置条件。

- **建立全景**：从第 1–3 章理解系统层次、模型结构和负载。
- **深入底层执行**：第 4–7 章讨论加速器、算子与运行时、超节点和网络。
- **设计完整系统**：第 8–12 章讨论推理、训练、资源调度与端边云协同。

建议先做资源估算，再阅读实现与实验结果，最后改变一个条件，观察原来的选择是否仍然成立。

## 内容目录

| 章 | 主题 | 主要问题 |
| :--: | --- | --- |
| 1 | [初识 AI Infra](<manuscripts/01-初识 AI Infra.md>) | 如何估算一次生成的容量、计算量与数据读取？ |
| 2 | [模型架构](manuscripts/02-模型架构.md) | 注意力、历史状态与专家结构如何改变系统需求？ |
| 3 | [推理与训练负载](manuscripts/03-推理与训练负载.md) | 任务阶段、到达模式和状态寿命如何影响资源需求？ |
| 4 | [加速器架构](manuscripts/04-加速器架构.md) | 如何在计算、存储、带宽、功耗与成本之间取舍？ |
| 5 | [算子与运行时](manuscripts/05-算子与运行时.md) | 融合、复用、并发和调度如何减少执行开销？ |
| 6 | [超节点](manuscripts/06-超节点.md) | 多设备协作如何平衡容量、吞吐和同步代价？ |
| 7 | [数据中心网络](manuscripts/07-数据中心网络.md) | 通信语义与网络设计如何影响任务关键路径？ |
| 8 | [推理优化](manuscripts/08-单实例推理.md) | 批处理、KV 管理、卸载与推测解码何时有效？ |
| 9 | [分布式推理](manuscripts/09-分布式推理.md) | 如何放置计算和状态，并处理扩缩容与恢复？ |
| 10 | [训练系统](manuscripts/10-训练系统.md) | 如何在容量、通信和重算之间提高有效训练进展？ |
| 11 | [资源调度与运行环境](manuscripts/11-资源调度与运行环境.md) | 如何计入状态驻留、环境准备和恢复的完整成本？ |
| 12 | [端边云协同](manuscripts/12-端边云协同.md) | 如何按完整交互的质量、时限与传输代价选择执行位置？ |

## 配套计算与实验

[量化计算项目](calculations/README.md)提供模型配置、资源推导、统一 CLI 和[结果索引](calculations/results/README.md)。静态计算只需 Python 3.10+ 标准库，无需 GPU 或模型权重。

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

[配套实验](experiments/README.md)按 `experiments/chXX/XX-YY/` 组织，各目录提供运行方法、输入、结果和适用条件。计算推导、硬件实测与公开资料分别注明来源；尚未覆盖的条件见各实验说明及 [inventory.json](experiments/inventory.json)。GPU 实验的硬件和依赖要求以各自 README 为准。

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

本书与[《深入理解 AI Agent：设计原理与工程实践》](https://github.com/bojieli/ai-agent-book)属于同一系列，PDF 沿用其 ElegantBook / XeLaTeX 模板。感谢相关论文、开源项目与技术文档的作者，以及参与勘误和实验复现的读者。具体来源见正文脚注和[参考资料库](references/README.md)。

## 许可

本书原创正文、配图及配套代码采用 [Apache License 2.0](LICENSE) 许可。Copyright © 2026 Bojie Li（李博杰）。

仓库中的第三方代码、字体、模板与参考资料保留各自的版权和许可声明，不因收录于本仓库而改用 Apache-2.0；具体来源和使用条件见相应目录。
