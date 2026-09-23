#!/usr/bin/env python3
"""Create and verify the Traditional Chinese manuscript copy.

The source is already Chinese, so this pass is deliberately conservative: it
converts characters and Taiwan terminology while protecting syntax that carries
meaning for the build or for repository navigation. It does not paraphrase,
delete, or add prose.

    python3 convert_book.py translate
    python3 convert_book.py verify
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from opencc import OpenCC
except ImportError as exc:  # pragma: no cover - exercised by the CLI guard
    raise SystemExit(
        'Missing OpenCC. Install with: python3 -m pip install '
        '-r book-zh-tw/tools/requirements.txt'
    ) from exc

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / 'manuscripts'
TARGET = HERE / 'manuscripts-zh-tw'
CONVERTER = OpenCC('s2twp')

# OpenCC handles character and phrase conversion. These are Taiwan-localized
# technical terms that s2twp intentionally leaves unchanged or handles by a
# different regional convention.
TAIWAN_REPLACEMENTS = tuple(sorted({
    '擴充套件': '擴充',
    '片記憶體儲': '片上儲存',
    '全域性': '全域',
    '許可權': '權限',
    '器件': '元件',
    '引數': '參數',
    '例項': '實例',
    '程序': '程式',
    '響應': '回應',
    '訪問': '存取',
    '配置': '設定',
    '示例': '範例',
    '平臺': '平台',
    '用戶端': '使用者端',
    '服務器': '伺服器',
    '移動端': '行動裝置',
    '數據庫': '資料庫',
    '軟件': '軟體',
    '硬件': '硬體',
    '視頻': '影片',
    '屏幕': '螢幕',
    '質量': '品質',
    '信息': '資訊',
    '網絡': '網路',
    '數據': '資料',
    '用戶': '使用者',
    '智能': '智慧',
    '默認': '預設',
    '支持': '支援',
    '兼容': '相容',
    '反饋': '回饋',
    '實現': '實作',
    '通過': '透過',
    '水平': '水準',
    '托盤': '託盤',
    '“': '「',
    '”': '」',
    '‘': '『',
    '’': '』',
}.items(), key=lambda pair: len(pair[0]), reverse=True))

PROTECTED_TOKEN = '\u0000ZH_TW_PROTECTED_{}\u0000'
# Keep this book's computing terms when OpenCC chooses a different sense.
TECHNICAL_TERMS = tuple(sorted({
    '实现原子性、一致性、隔离性和持久性': '實現原子性、一致性、隔離性與持久性',
    '实现的行为': '實現的行為',
    '實現原子性、一致性、隔離性與持久性': '實現原子性、一致性、隔離性與持久性',
    '實現的行為': '實現的行為',
    '未通过测试': '未通過測試',
    '未通過測試': '未通過測試',
    '通过测试': '通過測試',
    '通過測試': '通過測試',
    '通过验证': '通過驗證',
    '通過驗證': '通過驗證',
    '通过检查': '通過檢查',
    '通過檢查': '通過檢查',
    '通过验收': '通過驗收',
    '通過驗收': '通過驗收',
    '通过评分': '通過評分',
    '通過評分': '通過評分',
    '通过筛选': '通過篩選',
    '通過篩選': '通過篩選',
    '通过数值': '通過數值',
    '通过下界': '通過下界',
    '通过 FP64': '通過 FP64',
    '通过率': '通過率',
    '通過率': '通過率',
    '通过比例': '通過比例',
    '通過比例': '通過比例',
    '水平点线': '水平點線',
    '水平點線': '水平點線',
    '接近水平': '接近水平',
    '水平线': '水平線',
    '水平線': '水平線',
    '每个 token 实际激活的参数': '每個 token 實際選用的參數',
    '一个 token 激活多少参数': '一個 token 選用多少參數',
    '激活 FLOPs': '選用路徑的 FLOPs',
    '被激活路径': '被選用路徑',
    '稀疏激活': '稀疏路由',
    '行激活': '行啟用',
    '工具程序仍由操作系统执行': '工具行程仍由作業系統執行',
    '中间向量称为激活': '中間向量稱為活化值',
    '激活的生命周期': '活化值的生命週期',
    '激活函数': '活化函數',
    '激活张量': '活化張量',
    '激活梯度': '活化梯度',
    '激活值': '活化值',
    '激活参数相同': '每個 token 選用的參數數量相同',
    '激活参数量': '每 token 選用參數量',
    '每 token 激活约': '每 token 選用約',
    'MoE 激活量': 'MoE 每 token 選用參數量',
    '激活参数': '每 token 選用參數',
    '激活规模': '每 token 選用參數規模',
    '激活': '活化',
    '程序代码': '程式碼',
    '提交程序': '提交行程',
    '进程': '行程',
    '進程': '行程',
    '算子': '運算子',
    '运算子': '運算子',
    '運算子': '運算子',
    '演算子': '演算子',
    '卸载': '卸載',
    '卸載': '卸載',
}.items(), key=lambda pair: len(pair[0]), reverse=True))


def protect_syntax(text: str) -> tuple[str, list[str]]:
    """Replace build-sensitive syntax with opaque placeholders."""
    values: list[str] = []

    def hold(match: re.Match[str] | str) -> str:
        value = match.group(0) if isinstance(match, re.Match) else match
        token = PROTECTED_TOKEN.format(len(values))
        values.append(value)
        return token

    # Do the broadest regions first so nested Markdown is not processed again.
    patterns = (
        re.compile(r'^```[^\n]*\n.*?^```\s*$', re.M | re.S),
        re.compile(r'`[^`\n]*`'),
        re.compile(r'(?<=\]\()([^()\n]+)(?=\))'),
        re.compile(r'https?://[^\s)>\]]+'),
        re.compile(r'<[^>\n]+>'),
    )
    for pattern in patterns:
        text = pattern.sub(hold, text)
    return text, values


def restore_syntax(text: str, values: list[str]) -> str:
    for index, value in enumerate(values):
        text = text.replace(PROTECTED_TOKEN.format(index), value)
    return text


def convert_text(text: str) -> str:
    protected, values = protect_syntax(text)
    for old, new in TECHNICAL_TERMS:
        if old in protected:
            token = PROTECTED_TOKEN.format(len(values))
            protected = protected.replace(old, token)
            values.append(new)
    converted = CONVERTER.convert(protected)
    for old, new in TAIWAN_REPLACEMENTS:
        converted = converted.replace(old, new)
    return restore_syntax(converted, values)


INLINE_MATH = re.compile(r'(?<!\$)\$[^$\n]+\$(?!\$)')
IMAGE = re.compile(r'!\[[^\n]*\]\(([^)]+)\)')
LINK = re.compile(r'(?<!!)\[[^\]]*\]\(([^)]+)\)')


def fingerprint(text: str) -> dict:
    return {
        'display_math': text.count('$$') // 2,
        'inline_math': len(INLINE_MATH.findall(text)),
        'fences': text.count('```') // 2,
        'table_rows': sum(1 for line in text.splitlines()
                          if line.strip().startswith('|')),
        'headings': re.findall(r'^(#+)\s', text, re.M),
        'image_targets': IMAGE.findall(text),
        'link_targets': LINK.findall(text),
        'numbers': re.findall(r'(?<![A-Za-z])\d+(?:[.,]\d+)*(?:%|[A-Za-zµμ]+)?', text),
    }


def source_files(only: str | None = None) -> list[Path]:
    files = sorted(SOURCE.glob('[0-9][0-9]-*.md'))
    return [path for path in files if only is None or only in path.name]


def translate(args: argparse.Namespace) -> None:
    files = source_files(args.only)
    TARGET.mkdir(parents=True, exist_ok=True)
    total_chars = changed_chars = 0
    for source in files:
        target = TARGET / source.name
        original = source.read_text(encoding='utf-8')
        converted = convert_text(original)
        target.write_text(converted, encoding='utf-8')
        total_chars += len(original)
        changed_chars += sum(a != b for a, b in zip(original, converted))
        print(f'{source.name:32s} {len(original):8,d} chars  '
              f'{sum(a != b for a, b in zip(original, converted)):8,d} changed')
    print(f'\n{len(files)} file(s), {total_chars:,} source characters, '
          f'{changed_chars:,} changed positions')


def verify(args: argparse.Namespace) -> int:
    failures = 0
    for source in source_files(args.only):
        target = TARGET / source.name
        if not target.exists():
            print(f'MISSING {target}')
            failures += 1
            continue
        original = source.read_text(encoding='utf-8')
        actual = target.read_text(encoding='utf-8')
        expected = convert_text(original)
        problems = []
        if actual != expected:
            problems.append('not equal to deterministic conversion')
        if fingerprint(original) != fingerprint(actual):
            problems.append('Markdown/math/link structure changed')
        if problems:
            failures += 1
            print(f'FAIL   {source.name}: {"; ".join(problems)}')
        else:
            print(f'OK     {source.name}')
    if failures:
        print(f'\n{failures} manuscript(s) failed verification')
        return 1
    print(f'\nPASS: {len(source_files(args.only))} manuscript(s), '
          'protected syntax and quantitative tokens unchanged')
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name, fn in [('translate', translate), ('verify', verify)]:
        command = sub.add_parser(name)
        command.add_argument('--only', help='Only process files containing this text')
        command.set_defaults(fn=fn)
    args = parser.parse_args()
    result = args.fn(args)
    return result if isinstance(result, int) else 0


if __name__ == '__main__':
    sys.exit(main())
