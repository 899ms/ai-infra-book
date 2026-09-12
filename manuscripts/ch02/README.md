# 第二章：模型架构

[正文](../02-模型架构.md)以 Qwen3-8B 建立矩阵与状态的基础推导，再比较 DeepSeek V4.1 Flash、Qwen3-8B、Qwen3.6、DeepSeek V4-Flash 和 Kimi K3。V4.1 Flash 在横向比较中列为第一项，补充 CED、共享 KV、分层索引、Engram 和阶段计算分解。

## 计算与图表

表 2-A 至 2-C 与表 2-E、完整请求表和相关配图统一覆盖五个典型模型。长上下文主图比较 8K 与 1M，200K 数据保留在计算结果中。表 2-D 分解 V4.1 Flash 的参考全层与 CED 输入计算；表 2-6 列出其矩阵组成。表 2-3 的 DeepSeek-V3 是 MLA 的历史参照。

- [统一计算结果](../../calculations/results/chapter2-model-comparison.json)
- [V4.1 CED 8K 前向记录](../../calculations/results/v41-forward-prefill-8192-ced.md)
- [五模型参数与资源表](model-comparison.md)
- [8K／200K／1M 数据](long-context-comparison.json)
- [来源与适用条件、写作复核记录](../../research/ch02-five-models-2026-09-10/README.md)

在仓库根目录运行：

```bash
python3 calculations/reproduce_ch02.py
python3 manuscripts/ch02/render_v41_case.py
python3 manuscripts/ch02/compare_models.py
python3 manuscripts/ch02/compare_long_context.py
python3 -m unittest discover -s calculations/tests -p 'test_v41*.py' -v
```

前三个图表生成脚本读取 `calculations/results/`，只做分组与格式化。资源计算全部位于 `calculations/src/infra_calc/`。生成完成后，`sources.json` 记录所采用计算文件的哈希；若计算输入变化，需核对结果后更新来源锁定，再生成图片。

## 配图与排版

安装 [requirements.txt](requirements.txt)，然后运行：

```bash
python3 manuscripts/ch02/build.py
python3 manuscripts/ch02/verify_tables.py
bash book/build_pdf.sh --chapter 2
```

`build.py` 输出 SVG、PNG、PDF 配图，并将本地阅读预览写入 `build/legacy/manuscripts/02-模型架构.html`。数学表达式由固定版本 KaTeX 渲染；PDF 编译另需 Pandoc 和 XeLaTeX。配图编号与顺序来自正文，记录在 [figure-index.json](figure-index.json)。

完整矩阵计算的实现、复算入口和边界测试分别见 [v41_forward.py](../../calculations/src/infra_calc/topics/v41_forward.py)、[reproduce_ch02.py](../../calculations/reproduce_ch02.py) 和 [test_v41_forward.py](../../calculations/tests/test_v41_forward.py)。
