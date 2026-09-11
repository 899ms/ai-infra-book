# 第四章架构演进补写

## 结构决定

原稿在 4.2.3、存储、搬运、封装等节零散介绍了架构差异，图 4-3 的跨代协同缺少集中展开。旧比较笔记中“不再另设一节”的安排已更新。新增 4.6“模型需求如何推动架构演进”，位于机制分析之后、专用架构之前；原 4.6、4.7 顺延为 4.7、4.8。正文开篇、图 4-3 的引导和章末小结相应补充。全章为八节、二十七小节，31 幅图。

读者先理解硬件部件，再沿 NVIDIA、Apple、昇腾三条线比较完整架构，最后横向归纳相同模型工作所推动的共同设计。集中对比与前面的机制推导互相引用。用户已澄清所指为 Tensor Core，重点为不同厂商的共同演进方向；正文不作先发或模仿判断。Triton 仅作为软件如何使用硬件的一段例子。

## 证据审查

既有资料足以支撑主线。本轮补充 Turing 官方白皮书和 M4 官方公告，使整数低比特与 Apple 中间代际连贯；另外保存固定提交的 Triton 官方实现用于软件映射例子。尝试获取华为 2018 年发布页面未成功，未将该页面作为正文依据，也未加入先后归属结论。

| 事实 | 原件与定位 | 正文用途 |
| --- | --- | --- |
| Volta FP16 输入、FP32 累加 | `references/files/specs/nvidia-v100.pdf`，Tensor Cores | 专用矩阵计算起点 |
| Turing INT8、INT4 | [白皮书](sources/nvidia-turing.pdf)，Turing Tensor Cores；[提取文本](sources/nvidia-turing.txt)中 INT8／INT4 段落 | 补上整数低比特推理路线 |
| A100 TF32、BF16、稀疏与异步拷贝 | `references/files/specs/nvidia-a100.pdf` | 精度与操作数准备同步演进 |
| Hopper FP8、TMA、异步矩阵 | H100 白皮书、Hopper Tuning Guide | Tensor 流水与线程分工 |
| SM100 TMEM／分块缩放；SM120 差异 | Blackwell Tuning Guide、CUTLASS 功能和 SM100 示例 | 明确数据中心与 RTX 的实际路径 |
| Rubin 指数吞吐与描述符更新 | `rubin-rechecked.md`，attention 与 MoE 小节 | 对应 Softmax 和专家准备成本 |
| M3 动态局部内存分配 | `apple-m3-evolution.md`，Dynamic Caching | 区分整机共享内存与 GPU 局部资源 |
| M4 Dynamic Caching、120 GB/s、Neural Engine | [官方公告](sources/apple-m4-2024.md)；既有 Mac mini 官方规格 | 补上 M3 与 M5 之间的演进 |
| M5 GPU 每核 Neural Accelerator、153 GB/s、第二代动态缓存 | `apple-m5-evolution.md`，GPU 与统一内存小节 | GPU 内专用单元与独立 Neural Engine 并列 |
| 早期 DaVinci 资源分工 | DaVinci 论文 §3.1–3.4 | Scalar／Vector／Cube／MTE |
| Atlas A2 矩阵、向量分离 | Ascend C 指南第 4 章 | AIC／AIV 独立控制和全局地址交换 |
| 910C 双裸片及 24 AIC／48 AIV | CloudMatrix384 **v2** §3.3.1；MLA／MTP 实现 §4.2.2 | 封装、计算配比和模型实现 |
| 950 CV、寄存器、NDDMA、BufferID、MX 格式 | 950 官方白皮书 §4.1–4.1.6 与低精度介绍 | 交接、布局、同步和分块缩放 |
| 软件使用张量描述与流水 | [融合注意力](sources/06-fused-attention.py)、[持久化矩阵乘法](sources/09-persistent-matmul.py) | 软件到硬件的映射 |

新下载的原始地址：

- Turing：<https://images.nvidia.com/aem-dam/en-zz/Solutions/design-visualization/technologies/turing-architecture/NVIDIA-Turing-Architecture-Whitepaper.pdf>
- M4：<https://www.apple.com/newsroom/2024/05/apple-introduces-m4-chip/>
- Triton：<https://github.com/triton-lang/triton>，提交与时间见 [triton-commit.json](sources/triton-commit.json)。

原件版本与哈希见 [sources.json](sources.json)。正文保留必要的数值、计算路径与出处，来源审查和版本记录放在此处。所有代际收益均沿实际增加、减少的工作解释；没有把峰值倍数直接写成整段模型的加速比，也没有用后来模型证明早期芯片的历史设计动机。

## 图表与验证

新增图 4-22 至 4-26：NVIDIA 数据通路、精度与缩放、Apple 计算组织、昇腾 CV 演进、模型工作与共同机制。由 `manuscripts/ch04/architecture_evolution.py` 生成 SVG／PNG／PDF，调用全书 `figure_style`：思源黑体，420 pt 画布，11–14 pt 标注，浅色功能块、深色轮廓、实线数据箭头。原图 4-22 至 4-26 顺延为 4-27 至 4-31。

新增三张代际表与一张横向比较表。延续 Q 投影、注意力服务周期和 64 KiB 中间张量三个已有算例，连接前面各机制小节。

结构、链接、脚注、图号、图形字号、构建和渲染结果记录在 [validation.json](validation.json)。最终成书以仓库 `book/` 中的第四章 PDF 和全书 PDF 为准。
