# 第四章：从演进综述改为量化比较

按用户要求将 4.6 整体改写，顺序为 NVIDIA → 昇腾 → Apple → 同模型横向比较。保留专门一节，前置计算／存储／搬运／封装知识，后接第 4.8 节的实际执行测量与成本分析。

## 主要变化

- V100 在相同操作数与累加精度下比较普通 FMA 和 Tensor Core，分别算一行与 4096 行的计算／搬运下界。
- BF16 计算数值范围和舍入间距；MXFP8／MXFP4 计算含 scale 的容量，并分离带宽和位宽带来的收益。
- NVIDIA 消费级、工作站、数据中心分线比较，列出 3090／4090／5090、RTX PRO 6000、A100／H100／H200 的同口径矩阵参数、带宽与容量。新增 GA102 官方白皮书核对 3090。
- 昇腾 910A/CNN 背景引用作者回顾，img2col 机制、Cube／Vector 配比与带宽引用架构论文。计算卷积窗口展开的九倍存储和 6.891 MiB 写读；注意力独立计算向量吞吐要求与交接字节。避免把向量宽度当成指数吞吐或把 94 GB/s 当成后代芯片实测。
- Apple 区分容量与带宽。M3 Ultra 512GB 为已有官方历史配置，M5 Ultra 的 512GB／1200GB/s 为公布规格。用 Qwen3-8B 稠密和 Qwen3-235B-A22B MoE 分别计算每步载荷、常驻容量、额外整机预算和路由变化。
- 横向比较固定 Qwen3-8B 的 8K decode 与 4K causal prefill，明确输出头计算位置；不同阶段的改进幅度单独计算。最后用有效速率与已有实际 Q 投影实验接回总耗时。

[计算程序、原件与结果](../../calculations/research/architecture-evolution-quantitative/README.md)为数字的唯一来源。[独立检查](../../calculations/research/architecture-evolution-quantitative/verification.json)从已有张量清单、因果 token 对和数据字节重算，不新增设备性能实验。计算的边界与版本记录放在配套，正文采用直接陈述与明确题设，不添加无证据的历史归因或整模型加速倍数。

## 图表

本节 8 幅图对应全章 4-22 至 4-29。相比上一轮净增 3 幅，全章 34 幅：新增 Tensor Core 预算、img2col、CV 交接；精度图改为实际字节／带宽计算；共同方向图改为同一模型的 decode 与 prefill 时间对照。保留必要的数据通路图。全部使用全书 figure_style，思源黑体、420 pt 画布与 11–14 pt 字号。图注与正文图号统一顺延。

正文局部修订前版本在 [before/ch04.md](before/ch04.md)。最终图表、引用、PDF 与网页校验结果见 [validation.json](validation.json)。
