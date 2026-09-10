# 第二章：五模型比较与 1M 上下文复核

## 修改目标

将 DeepSeek V4.1 Flash 纳入第二章的第五个典型模型，并在横向比较中列为第一项。Qwen3-8B 继续承担基础矩阵推导；原有 V4-Flash 案例与实验保持其模型身份。总体架构、参数分解、计算与状态、长上下文、完整请求、模型矩阵查阅表及相关配图一并更新。

所有新数值均由 `calculations` 的架构适配器生成，正文与配图程序只读取、分组和格式化结果。执行：

```bash
python3 calculations/reproduce_ch02.py
python3 manuscripts/ch02/render_v41_case.py
python3 manuscripts/ch02/compare_models.py
python3 manuscripts/ch02/compare_long_context.py
python3 -m unittest discover -s calculations/tests -p 'test_v41*.py' -v
python3 manuscripts/ch02/build.py
```

## 固定证据与参数

官方 revision：`df42c109f1defefcbfcedbe7d905718a12266e40`。来源锁文件、模型配置、技术报告、参考源码和 48 个 checkpoint 分片头见 [原调研](../../calculations/research/deepseek-v41-flash/README.md)。没有下载模型完整权重或运行 GPU 推理。

[V4.1 前向适配器](../../calculations/src/infra_calc/topics/v41_forward.py)逐一核对文本二维矩阵形状；所有专家的 FP4 打包形状都还原为逻辑形状。文本参数包括主干与 Engram，排除视觉、DSpark 和量化 scales。分组参数与完整分片头枚举守恒，避免把 Engram 的查表参数误当成每 token 全量执行的矩阵。

## 计算边界

- 表格比较完整的文本**矩阵 FLOPs**，FMA=2，稀疏注意力使用有效位置对，专家使用有效分派行数。归一化、门控、Softmax、排序、量化与采样不能混入 Tensor 矩阵 FLOPs；实现分别报告非矩阵分项及尚未累计的标量／后端指令工作。
- 参考路径按公开 `Transformer.forward` 执行全 40 层；参考索引器先矩形 einsum，再屏蔽不可见位置。CED 是论文 §2.2、§3.2.2 描述的服务执行模型，不是公开参考函数的直接运行结果。
- CED prefill：20 层编码器处理全部输入；第 20 层的全局 KV 和索引键为全部输入生成；20 层解码器只处理最后 `min(P,128)` 个位置，其局部 SWA 截断到重放片段。该重放构造的是**近似**局部状态，不与完整前向数学等价。后续单步生成仍执行全 40 层。
- 生产式候选索引只扫描因果可见条目，后续 Reindex 最多扫描 16,384 个候选。参考矩形扫描和候选扫描作为独立选项；完整前向与 CED 的差异同时涉及查询位置数及索引算法，不能全部归因于跳过层。
- 当前接口接受首次 prefill 或单 token continuation；带已有前缀的多 token chunk 和 encoder SWA 缺失恢复没有冒充已实现路径。
- 状态比较用 BF16 全局 KV／索引／局部窗口、FP32 压缩器槽，加参考 Engram int64 词元历史。按已填充长度统计，max_seq_len 预分配单独报告。V4.1 的生产 FP4／FP8 状态另列。权重、运行时 workspace、静态 RoPE／token map、并行复制及分配器对齐不在状态列。
- 状态访问曲线列 KV、索引读取与已有模型的递推矩阵读写，不含所有状态写入、Engram 查表及真实 HBM 流量。数值不表示速度、吞吐或任务质量。

## 为什么由 200K 改为 1M

[统一结果](../../calculations/results/chapter2-model-comparison.json)同时保留 8K、200K、1M。1M 下 V4.1 Flash 的单步矩阵工作约 57.49 GFLOPs，V4-Flash 约 140.34 GFLOPs；200K 下分别约 40.21、50.48 GFLOPs。1M 更清楚地展示剩余完整索引扫描、分层索引上限与压缩表示的不同增长规律。

8K／200K 表示调用前有 8192／204800 个位置；1M 表示调用前有 1048575 个位置，加当前输入后正好 1048576。两者没有把已到达模型上限的 1048576 个历史位置再加一。1M 最后一步恰好完成压缩块，因此非交互投影会出现块边界差异，不能继续断言它与 8K 的非交互项严格相等。

V4.1 Flash、V4-Flash、Kimi K3 的固定配置上下文上限均为 1048576。Qwen3-8B 上限 40960；Qwen3.6 上限 262144。因此 Qwen3-8B 的 200K／1M、Qwen3.6 的 1M 是**显式结构公式外推**，不表示可运行配置、RoPE 扩展已验证或该长度下的任务质量。计算结果每行保留 `extrapolated` 和 `pinned_context_limit`。正文按作者要求集中解释结构与数学关系，外推和验证边界集中记录在此。

## 完整请求口径

五个模型统一 P=128、G=4、B=1、S=0；一次 prefill 产生首输出，随后三次 decode，最终保留 131 个已处理位置。Kimi K3 统一使用紧凑 MLA，与前面的资源表一致，因此从旧表展开 MLA 的 27.13 TFLOPs 变为约 27.16 TFLOPs。V4-Pro 的历史结果与原始四模型请求记录保留在原计算目录，不改写其身份。

## 验证

新测试用独立 checkpoint 矩阵权重求和、显式小规模因果位置集合、CED 窗口边界、压缩块奇偶相位、batch 线性关系、参数分组守恒与旧专家分项交叉核对。构建及视觉检查结果另附于本目录或本地 `build/ch02-v41/`。

验证结果：21 项 V4.1 单元测试通过；98 个矩阵形状检查通过；五模型的参数守恒、15 行上下文结果、完整请求逐调用求和与 1M 端点检查通过。第二章的 36 幅图、83 项来源哈希、102 个本地链接、桌面／手机页面图片与公式检查通过。网站 17 个页面的内部链接、图片与搜索检查通过。第二章 PDF 共 52 页，已查看架构表、参数表、资源表、CED 阶段表、长上下文表及矩阵表的实际页面。编译保留模板既有的字体／microtype 提示；没有新增表格越界。
