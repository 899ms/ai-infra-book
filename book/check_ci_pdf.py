#!/usr/bin/env python3
"""Check the newly built full PDF and render pages for CI visual diagnostics."""
from pathlib import Path
import argparse
import json
import fitz


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    directory = args.directory
    report = json.loads((directory / 'AI-Infra-Book-build.json').read_text())
    if report['chapters'] != list(range(1, 13)):
        raise SystemExit('Expected all 12 chapters')
    doc = fitz.open(directory / 'AI-Infra-Book.pdf')
    if len(doc) < 12:
        raise SystemExit('PDF is unexpectedly short')
    chapter_entries = [r for r in doc.get_toc() if r[0] == 1]
    if len(chapter_entries) < 12:
        raise SystemExit('PDF is missing chapter bookmarks')
    text = ''.join(page.get_text() for page in doc)
    if 'AI Infra' not in text or '端边云' not in text or '\ufffd' in text:
        raise SystemExit('PDF text/title/last chapter check failed')
    fatal = [w for w in report['warnings'] if 'Missing character:' in w or 'undefined references' in w]
    if fatal:
        raise SystemExit('Font/reference errors:\n' + '\n'.join(fatal))
    pages = sorted({0, min(8, len(doc)-1), len(doc)//2, len(doc)-1})
    for number in pages:
        doc[number].get_pixmap(matrix=fitz.Matrix(1, 1)).save(directory / f'preview-{number+1:03}.png')
    result = dict(passed=True, pages=len(doc), chapters=report['chapters'],
                  figures=report['figure_count'], source_ref=report['source_ref'],
                  layout_warnings=report['warnings'], preview_pages=[p+1 for p in pages])
    (directory / 'pdf-validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(f'PASS: {len(doc)} pages, 12 chapters, readable text, fonts and references')


if __name__ == '__main__':
    main()
