# 架构演进的定量比较

本计算支撑第四章 4.6：先固定模型工作，再替换资源或执行路径。运行：

```sh
python3 calculations/research/architecture-evolution-quantitative/calculate.py
python3 calculations/research/architecture-evolution-quantitative/check.py
```

[结果](result.json)中的时间均为所列工作的资源服务下界，计时测量使用本章已有实验 4-6。新增图由 `manuscripts/ch04/architecture_evolution.py` 读取本结果生成。没有执行新的 GPU／NPU 性能实验。

## 输入与计量

- 硬件：`calculations/configs/hardware.json`，原样读取名义容量、带宽和匹配精度的峰值。BF16 矩阵比较只选 BF16 输入、FP32 累加、稠密 tensor 行。Apple 与昇腾未满足此组合的值保留为空；不从 Neural Engine 或不同累加口径补数。
- RTX 3090：本轮补取 [NVIDIA GA102 白皮书](sources/nvidia-ampere-ga102.pdf)，表 9，24 GB、936 GB/s、BF16／FP32 稠密 71 TFLOP/s。71／142 是稠密／结构化稀疏，不使用 142 替代本书的稠密执行。
- V100：原有 Volta 白皮书，SXM2，FP32 普通 FMA 15.7 TFLOP/s、FP16／FP32 Tensor Core 125 TFLOP/s、900 GB/s。同一 FP16 输入、FP32 累加任务；普通路径提升到 FP32 寄存器，转换成本未加入乘加资源下界。输出均保存 FP16。
- 模型：固定 Qwen3-8B 配置。每层矩阵从 Q、K、V、O 与三次前馈投影逐项计数；4K prefill 采用因果三角形的有效乘加工作，只为最后一个位置算输出头。内核实际 tile 的补齐与三角对角块多余工作进入后续实际执行分析。
- 存储：直接复用 `storage-generation-qwen8-235.json` 的张量清单、权重常驻、实际选中专家、scale、KV 与 2 GiB 工作区。decode 的 8K 表示 8191 历史位置加本步一个位置。
- 容量：厂商容量用十进制 GB 作预算阈值。Apple 示例另外预留 8 GB 整机空间，明确区别于已有 2 GiB 工作区；未把这项预留加入接口读取量。
- M5 Ultra：使用已归档官方公布规格和 availability 字段。512 GB 产品在 2026-09-10 尚为公布规格；不将计算结果标为已交付设备实测。M3 Ultra 512 GB 为官方历史配置记录，不是推测路线图。

## 昇腾的三项分析

1. **img2col。** FP16、56×56×64、3×3、步长 1、同尺寸 padding、64 输出通道。比较显式 HBM 展开矩阵与片上搬运中展开。计算被移除的中间矩阵写读，不宣称原始输入或片上展开数据消失。按早期论文 1.2 TB/s 得 6.02 μs 的 HBM 工作量。
2. **向量需求。** 论文配置 Cube 8192 FLOPs/cycle，Vector width 256 bytes。宽度只用于计算每组 FP32 值的数量，不能推断指数指令周期。128×128×128 注意力要求 256 组指数数据；要匹配 1024 周期矩阵服务，至少平均四周期一组。归约、归一化和依赖另计。
3. **交接。** 比较 FP32 分数与概率各 64 KiB 的两次交接：外层接口写读共 256 KiB；直接通路承担两次各 64 KiB。早期论文的每核 LLC 94 GB/s 用来说明外层接口的量级，不能当作 910B、910C 或 950 的测量带宽；CV 目标 128 GB/s 是由 128 KiB／1.024 μs 反推的设计要求，不是厂商披露值。950 的实际通路、向量增强、NDDMA、BufferID 和格式能力按官方白皮书分别引用。

作者关于早期 ResNet 背景的回顾与论文微架构记录分别保存；没有用作者谈到的 30%／3 倍作为通用性能参数。论文 §3.4 的 BERT 结果说明多数层仍由 Cube 时间主导，因此正文以具体算子与工作比例判断瓶颈，不采用“910A 所有 Transformer 都因为 Vector 少而低效”的泛化。

## 验证

[独立检查](check.py)从已有张量清单重算各层线性参数和矩阵工作，枚举因果 token 对，检查 img2col 展开与交接字节、FP16／BF16 表示、带宽比例、专家路由和容量转折。输入文件 SHA-256 随结果保存。

官方 GA102 原始地址：<https://www.nvidia.com/content/PDF/nvidia-ampere-ga-102-gpu-architecture-whitepaper-v2.pdf>，本轮下载日期 2026-09-10。
