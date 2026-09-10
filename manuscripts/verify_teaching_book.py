#!/usr/bin/env python3
"""Audit active book assets, hashes, numbering, rendering, and sample preservation."""
from pathlib import Path
import hashlib,json,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];M=ROOT/'manuscripts';REVIEW=ROOT/'reviews/book-teaching-rewrite-2026-09-10'
errors=[];chapters=[]
def check(ok,message):
    if not ok:errors.append(message)
for n in range(1,13):
    md=next(M.glob(f'{n:02}-*.md'));s=md.read_text();d=M/f'ch{n:02}';refs=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',s);captions=re.findall(rf'^\*图 {n}-(\d+)[：\s]',s,re.M)
    check(captions==[str(i) for i in range(1,len(refs)+1)],f'{n}: caption sequence')
    check(len(set(refs))==len(refs),f'{n}: unique active illustrations')
    for chapter,number in re.findall(r'图\s+(\d+)-(\d+)',s):
        target=next(M.glob(f'{int(chapter):02}-*.md'),None)
        check(target is not None and 1<=int(number)<=len(re.findall(r'!\[',target.read_text())),f'{n}: figure reference {chapter}-{number}')
    for ref in refs:
        p=M/ref
        check(all(p.with_suffix(ext).exists() for ext in ['.svg','.png','.pdf']),f'{n}: formats {ref}')
        svg=ET.parse(p).getroot();check(abs(float(svg.attrib['width'].replace('pt',''))-420)<.1,f'{n}: book width {ref}')
    manifest=json.loads((d/'manifest.json').read_text())
    for row in manifest['outputs']:
        p=ROOT/row['path'];check(p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],f'{n}: artifact {row["path"]}')
    for row in json.loads((d/'sources.json').read_text())['sources']:
        p=ROOT/row['path'];check(p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],f'{n}: source {row["path"]}')
    layout_path=d/('teaching-layout-check.json' if n==5 else 'teaching-layout-validation.json');layout=json.loads(layout_path.read_text())
    if isinstance(layout,dict):layout=layout.get('figures',layout.get('checks',[]))
    check(len(layout)==len(refs),f'{n}: layout inventory')
    check(all(r['width_pt']==420 and r['min_label_pt']>=11 and not r['text_extent_warnings'] for r in layout),f'{n}: figure typography')
    maths=json.loads((d/'math-validation.json').read_text());check(not maths.get('errors',[]),f'{n}: math rendering')
    browsers=json.loads((d/'teaching-browser-validation.json').read_text())
    check({r['width'] for r in browsers}=={390,1440},f'{n}: viewports')
    for r in browsers:
        check(len(r['images'])==len(refs) and all(i['loaded'] for i in r['images']) and not r['mathErrors'] and not r['brokenAnchors'] and r['scrollWidth']<=r['width'],f'{n}: browser')
        if r['width']==390:check(all(i['width']>=559 for i in r['images']),f'{n}: readable mobile labels')
    chapters.append(dict(chapter=n,figures=len(refs),formulas=maths.get('expressions',browsers[0]['mathCount']),source_files=len(json.loads((d/'sources.json').read_text())['sources']),minimum_label_pt=min(r['min_label_pt'] for r in layout)))
prototype=M/'ch05/teaching_revision.py';check(prototype.read_bytes()==(REVIEW/'before/manuscripts/ch05/teaching_revision.py').read_bytes(),'approved prototype drawing source unchanged')
report=dict(passed=not errors,chapters=chapters,figures=sum(r['figures'] for r in chapters),formulas=sum(r['formulas'] for r in chapters),errors=errors)
(REVIEW/'final-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
# Replace the old chapter-one report with a report for its current reading edition.
(M/'ch01/validation.json').write_text(json.dumps(dict(status='passed' if not any(e.startswith('1:') for e in errors) else 'failed',**chapters[0],validation='manuscripts/verify_teaching_book.py',errors=[e for e in errors if e.startswith('1:')]),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
