# PDF 图文流动与公式修订

沿用 ElegantBook 的字体与系列样式，修复图形尺寸设置影响公式、强制图片位置阻断正文、短表横排导致空白等问题。

- 全书从 540 页变为 384 页；第二章从 65 页变为 51 页。393 幅图均保留。
- 封面标题实际下移约 58.8 pt（20.7 mm），页底日期留白为 3.95 cm。
- 图片宽度上限为正文的 68%，高度上限为正文区的 38%，等比缩放。恢复 `!htbp` 浮动，浮动页不再用伸缩空白分隔图。
- 短比较表用竖向浮动排版，长矩阵表保留跨页横排。进入长表前清理待排图表，避免输出例程冲突。
- 公式恢复原生 LaTeX 数学环境；第二章数学字号最高约 10 pt，全书最高约 12 pt（含小节标题中的公式）。旧版曾因缩放产生异常大字。

[新封面](cover.png) · [图文同页](inline-figures.png) · [正常字号公式](native-formula.png) · [200K 图与正文](long-context-figure.png) · [矩阵表](matrix-table.png)

[实际 PDF 字号与页数对比](layout-comparison.json) · [字体、边界和内容校验](../../../book/pdf-validation.json)

旧 PDF 与旧排版源码保存在 `before/`，用于版式对照。复算命令：

```bash
bash book/build_pdf.sh
bash book/build_pdf.sh --chapter 2
python3 book/verify_pdf.py
# 需要 PyMuPDF
python3 book/check_layout.py
```
