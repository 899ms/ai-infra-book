# 在线阅读与自动发布

正文维护在 `manuscripts/`，包含前言和十二章 Markdown；网站目录直接从正文生成。MkDocs Material 从这些源文件构建中文阅读网站，提供章节导航、全文搜索、数学公式、脚注、深色模式和手机阅读布局。

## 本地构建

在仓库根目录运行（Python 3.10+）：

```bash
python3 -m venv .venv-site
source .venv-site/bin/activate
pip install -r website/requirements.txt
python scripts/build_site.py
python scripts/check_site.py
```

输出全部位于被 Git 忽略的 `build/site/`。预览运行 `python scripts/build_site.py --serve`，打开 `http://127.0.0.1:8000`；修改正文后重新运行命令以重新整理源文件。临时 Markdown 位于 `build/docs/`，由构建器覆盖，不应手动维护。公式使用固定版本的 MathJax CDN，首次阅读需要网络。

构建只复制正文与引用的图片；实验、计算记录和原始资料链接指向构建提交对应的 GitHub 文件，避免网站携带庞大的研究归档。缺失的本地引用或未下载的图片 LFS 指针会使构建失败。

## 推送即发布

每次 push 到 `main`，GitHub Actions 自动执行：

1. 从同一提交的 Markdown 构建网站与十二章全书 PDF。
2. 检查网站链接、图片、PDF 章节、文字及字体；保存 PDF 日志和代表页面预览。
3. 创建 `build-<完整提交 SHA>` 对应的 GitHub Release，上传全书 PDF、封面 PDF/PNG、网站压缩包、来源记录、校验结果和 `SHA256SUMS`。重复运行同一提交会覆盖该 Release 的附件。
4. 将网站部署到 GitHub Pages。只有 PDF 和网站都构建成功后才发布；Release 与 Pages 分别执行，Pages 设置问题不会阻止 Release 附件发布。

不需要手工打标签或创建 Release。也可在默认分支手动运行 `Build and publish book` 工作流。Pull Request 只构建、检查和上传 Actions 产物，不发布 Release 或 Pages。GitHub Actions 同一分支的发布串行执行；快速连续推送时，GitHub 可能替换尚未启动的待运行任务，以最新提交为准。

PDF 在 Ubuntu 24.04 使用 Pandoc、XeLaTeX、Noto CJK 与 DejaVu 字体构建。Apple 字体可用时本地编译仍沿用 Apple 字体；项目提供的思源黑体用于中文粗体与图注。发布版中的资料链接指向该提交的 GitHub 文件，下载 PDF 后仍可访问来源（私有仓库需要登录）。

## GitHub Pages 首次启用

仓库设置 **Settings → Pages → Build and deployment → Source** 需选择 **GitHub Actions**。目标地址：

<https://bojieli.github.io/ai-infra-book/>

首次发布前启用上述设置，再推送到 `main` 或手动运行工作流；部署成功后即可在线阅读。

## 下载和本地复现

从仓库 [Releases](https://github.com/bojieli/ai-infra-book/releases) 下载 PDF，或解压 `ai-infra-book-site.tar.gz` 后运行 `python -m http.server` 阅读网站。

已有 PDF 编译依赖时，在仓库根目录运行：

```bash
bash book/build_pdf.sh --output-dir ../build/pdf --source-ref "$(git rev-parse HEAD)"
python3 -m pip install -r book/requirements-ci.txt
python3 book/check_ci_pdf.py build/pdf
```

`--output-dir` 相对于 `book/`；CI 的 PDF 产物放在忽略目录 `build/pdf/`，不覆盖仓库内已有 PDF。省略 `--source-ref` 时保留本地资料链接；发布构建传入提交 SHA 生成可独立下载的版本。

## HTML 迁移

重复的章节 HTML 已删除。仅有 HTML 的资料快照转为 Markdown；迁移清单 `website/html-migration.json` 记录旧路径、新路径及原始 HTML 的 SHA-256。转换保留可读资料，但不保留网页脚本和原始布局；精确原始字节仍可从 Git 历史恢复。当前来源清单中的文件路径及对应 SHA-256 已更新；原始 HTML 哈希保存在迁移清单及 `original_html_sha256` 字段中。压缩包内的历史文件清单保持原样。

`.gitignore` 忽略 HTML，CI 额外拒绝任何被强行加入版本控制的 HTML 文件。旧章节绘图脚本的阅读预览仅写入 `build/legacy/`；正式网站始终由 Markdown 重新构建。
