#!/usr/bin/env python3
"""Inspect actual PDF fonts and portable SVG text, including all active figures."""
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET
import fitz

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / 'archive/reviews/figure-font-revision-2026-09-10'
REVIEW.mkdir(parents=True, exist_ok=True)
errors, figures, books = [], [], []
for md in sorted((ROOT / 'manuscripts').glob('[0-9][0-9]-*.md')):
    for ref in re.findall(r'!\[[^\n]*\]\(([^)]+)\)', md.read_text()):
        svg = md.parent / ref
        pdf = svg.with_suffix('.pdf')
        with fitz.open(pdf) as doc:
            fonts = sorted({font[3] for page in doc for font in page.get_fonts()})
        if not any('SourceHanSansCN' in font for font in fonts):
            errors.append(f'{pdf.name}: missing Source Han Sans')
        if any('ArialUnicode' in font for font in fonts):
            errors.append(f'{pdf.name}: old Arial Unicode font')
        if list(ET.parse(svg).getroot().iter('{http://www.w3.org/2000/svg}text')):
            errors.append(f'{svg.name}: SVG depends on installed fonts')
        figures.append(dict(path=str(pdf.relative_to(ROOT)), fonts=fonts))
for name in ['AI-Infra-Book', 'AI-Infra-Book-Chapter-02']:
    with fitz.open(ROOT / 'book' / f'{name}.pdf') as doc:
        samples = {}
        preview_page = None
        for n, page in enumerate(doc):
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    for span in line['spans']:
                        if not re.search(r'[\u4e00-\u9fff]', span['text']):
                            continue
                        font = span['font']
                        if n >= 2:
                            samples.setdefault(font, dict(page=n+1, text=span['text'], size=span['size']))
                        if 'SourceHanSansCN-Bold' in font and span['size'] > 14 and n >= 2:
                            preview_page = preview_page if preview_page is not None else n
        if not any('Songti' in f and 'Regular' in f for f in samples):
            errors.append(f'{name}: regular Songti body missing')
        if not any('SourceHanSansCN-Bold' in f for f in samples):
            errors.append(f'{name}: Source Han Sans bold missing')
        if name.endswith('02') and preview_page is not None:
            doc[preview_page].get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(str(REVIEW / 'chapter-02-typography.png'))
        books.append(dict(pdf=name+'.pdf', pages=len(doc), chinese_font_samples=samples))
report = dict(passed=not errors, figure_count=len(figures), books=books, errors=errors, figures=figures)
(REVIEW / 'typography-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='figures'}, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
