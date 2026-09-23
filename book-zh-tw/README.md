# 深入理解 AI Infra・繁體中文版

這是《深入理解 AI Infra：量化分析與系統設計》的繁體中文版，與原始中文稿和英文版並列保存。原始 `manuscripts/` 與 `book/` 不會因為這個版本而改寫；本目錄保留繁中字稿、繁中配圖、封面與獨立的 PDF 建置腳本。

## 內容

| 路徑 | 內容 |
| --- | --- |
| `introduction.md`、`chapter01.md` … `chapter12.md` | 前言與十二章繁中字稿 |
| `images/` | 以繁中標籤重繪的配圖（Git LFS） |
| `preamble.tex` | 繁中字型設定與共用書籍版型 |
| `cover.tex` | 繁中封面 |
| `build_pdf.py`、`build_pdf.sh` | Pandoc + XeLaTeX 建置腳本 |
| `assemble.py` | 從繁中字稿整理章節並收集配圖 |
| `tools/` | 簡繁轉換、台灣用語校正與配圖腳本 |

## 建置 PDF

```bash
git lfs pull --include="book-zh-tw/images/**" --exclude=""
bash book-zh-tw/build_pdf.sh
```

需要 Python 3.9+、Pandoc 3.x、XeLaTeX 與 Poppler。建置結果會寫入
`book-zh-tw/AI-Infra-Book-ZH-TW.pdf`；中間檔案放在 `book-zh-tw/build/`，不納入版本控制。

推送到 GitHub 後，`Build and publish book` workflow 會另外建置繁中版本；在該次 run
的 artifacts 下載 `book-pdf-zh-tw-download` 即可取得 PDF 與版面驗證結果。

## 更新翻譯

繁中字稿由目前的 `manuscripts/` 產生。要重建稿件，先安裝可選的轉換工具：

```bash
python3 -m pip install -r book-zh-tw/tools/requirements.txt
python3 book-zh-tw/tools/convert_book.py translate
python3 book-zh-tw/tools/translate_figures.py apply
python3 book-zh-tw/tools/translate_figures.py check
python3 book-zh-tw/tools/translate_figures.py render
python3 book-zh-tw/assemble.py
```

`convert_book.py verify` 會確認標題、表格、公式、程式碼區塊、圖片目標、連結目標與數字沒有漂移。配圖腳本只替換可繪製的字串常數；檔名、路徑、資料比對值與檢查腳本中的簡體字會保留。

`translate_figures.py render` 需要各章 `requirements.txt` 中的繪圖依賴，並會在暫存的 `manuscripts/` 副本中執行，不會改寫原始稿件。`assemble.py` 會檢查 LFS 指標檔與配圖中的簡體字；第 6 章的 `figure-6-context-dependency` 沒有生成腳本，第 7 章的 `figure-7-ub-round-trip` 從資料檔讀取文字，因此保留為已知例外。其餘結果與 fallback 會記錄在被忽略的 `tools/figure-check.json`。

## 版本範圍

這份版本是依照英文版 PR #4 的組織方式製作：翻譯版獨立放在 `book-zh-tw/`，不取代原始稿件；數字、公式、連結、程式碼與計算條件以原稿為準。
