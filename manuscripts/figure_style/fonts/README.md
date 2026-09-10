# 思源黑体（Source Han Sans CN）

本项目固定使用 Adobe Source Han Sans 2.005 简体中文子集，SIL Open Font License 1.1，许可见 LICENSE.txt。

- 图表：Regular 标签、Medium 标题、Bold 强调；PDF 嵌入字体，SVG 文字转矢量轮廓，PNG 直接渲染。
- 书籍 PDF：中文粗体与章节标题使用 Bold；无衬线文字及图注使用 Regular；普通正文继续使用原来的宋体。
- 可编辑的图中文字保存在各章 Python 源码中。

下载来源：https://github.com/adobe-fonts/source-han-sans/tree/release/SubsetOTF/CN

SHA-256：

- `SourceHanSansCN-Bold.otf`: `62383707c086a32f3afd5e293f34c7eff64c7fea31f579fdc6cbe34d920519a6`
- `SourceHanSansCN-Medium.otf`: `a94e558a2fe972bee4f46bce0843abff37063fd68c33f1e7d9058f6f09432b01`
- `SourceHanSansCN-Regular.otf`: `e2bc8a2e7f37474b774fff8db758681ece40bb6947a90d571bce9dd60671a8e4`

## TrueType 导出版本

Matplotlib 的 PDF Type 42 导出使用 TrueType 轮廓，避免 CFF OTF 嵌入时的字体类型不匹配。`.ttf` 文件由上游同版本的 `Variable/TTF/Subset/SourceHanSansCN-VF.ttf` 通过 fontTools `instantiateVariableFont` 固定 `wght=400/500/700` 生成，并设置对应家族、字重与 PostScript 名称。LaTeX 使用上游 OTF。两者均为思源黑体 2.005。

上游变量字体 SHA-256：`25a01e41b5cc99893eb35a6cd2cc7611841dc19eb03cbaf7f0c1de8210f2ba0b`。

- `SourceHanSansCN-Bold.ttf`: `0578bcab9c04a0b7f3c0445f27e0063027e02c63fd7025177d94b385aded4c8c`
- `SourceHanSansCN-Medium.ttf`: `bdb6e98fe194707b16e0f6589906f539df18b76cf188f283e6dda69f3cdd058d`
- `SourceHanSansCN-Regular.ttf`: `bdfd5bece19538f35b89acf8e95270c80853e9892abd21c958f504cbbf1156ab`
