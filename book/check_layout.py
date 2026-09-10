#!/usr/bin/env python3
"""Inspect actual PDF font sizes and save representative layout review pages.

Requires PyMuPDF. Run after build_pdf.py and verify_pdf.py.
"""
from pathlib import Path
import json
import statistics
import pymupdf

ROOT=Path(__file__).resolve().parent.parent
REVIEW=ROOT/'archive/reviews/pdf-flow-revision-2026-09-10'
REVIEW.mkdir(parents=True,exist_ok=True)


def measure(path):
    doc=pymupdf.open(path)
    math=[]
    large=[]
    title_top=None
    for i,page in enumerate(doc):
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    if i==0 and '深入理解' in span['text']:
                        title_top=span['bbox'][1]
                    if 'Math' in span['font']:
                        math.append(span['size'])
                        # Section headings can use a 12pt inline equation.
                        if span['size']>14.1:
                            large.append(dict(page=i+1,text=span['text'],size_pt=span['size']))
    return dict(pages=len(doc),math_max_pt=max(math),math_median_pt=statistics.median(math),
                enlarged_math=large,cover_title_top_pt=title_top)


def main():
    result={}
    for name in ['AI-Infra-Book','AI-Infra-Book-Chapter-02']:
        new=ROOT/'book'/f'{name}.pdf'
        old=REVIEW/'before'/f'{name}.pdf'
        result[name]=dict(before=measure(old),after=measure(new))
        assert not result[name]['after']['enlarged_math']
        assert result[name]['after']['cover_title_top_pt']>result[name]['before']['cover_title_top_pt']+30
    doc=pymupdf.open(ROOT/'book/AI-Infra-Book-Chapter-02.pdf')
    selections={'cover':0,'inline-figures':3}
    for i,page in enumerate(doc):
        text=page.get_text()
        if '整模型只需' in text: selections['native-formula']=i
        if '1,235.13' in text: selections['long-context-figure']=i
        if 'CSA：主历史压缩内容及门控' in text:selections['matrix-table']=i
    for name,i in selections.items():
        doc[i].get_pixmap(matrix=pymupdf.Matrix(1.6,1.6)).save(REVIEW/f'{name}.png')
    result['review_pages']={name:i+1 for name,i in selections.items()}
    (REVIEW/'layout-comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({name:{phase:{k:v for k,v in values.items() if k!='enlarged_math'} for phase,values in row.items()}
                      for name,row in result.items() if name!='review_pages'},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
