"""Validate revised chapters at desktop/mobile widths and save review PDFs."""
from pathlib import Path
import argparse,json,re
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('chapters',nargs='+',type=int);args=parser.parse_args()
review=ROOT.parent/'reviews/book-teaching-rewrite-2026-09-10';records=[]
with sync_playwright() as p:
    chrome=Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    browser=p.chromium.launch(**({'executable_path':str(chrome)} if chrome.exists() else {}),headless=True)
    for n in args.chapters:
        md=next(ROOT.glob(f'{n:02}-*.md'));expected=len(re.findall(r'!\[',md.read_text()))
        target=review/f'ch{n:02}';target.mkdir(exist_ok=True)
        for width in [1440,390]:
            page=browser.new_page(viewport={'width':width,'height':1050})
            page.goto(md.with_suffix('.html').as_uri());page.wait_for_load_state('load')
            result=page.evaluate('''() => ({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,images:[...document.images].map(i=>({loaded:i.complete&&i.naturalWidth>0,width:i.getBoundingClientRect().width})),mathErrors:document.querySelectorAll('.katex-error').length,mathCount:document.querySelectorAll('.katex').length,brokenAnchors:[...document.querySelectorAll('a[href^="#"]')].map(a=>a.hash.slice(1)).filter(id=>id&&!document.getElementById(decodeURIComponent(id)))})''')
            result.update(chapter=n,expectedImages=expected);records.append(result)
            assert result['scrollWidth']<=width,result
            assert len(result['images'])==expected and all(i['loaded'] for i in result['images']),result
            assert not result['mathErrors'] and not result['brokenAnchors'],result
            if width==390:assert all(i['width']>=559 for i in result['images']), 'Mobile diagram labels must stay at book scale'
            page.screenshot(path=str(target/f'reading-{width}.png'))
            if width==1440:page.pdf(path=str(target/'chapter.pdf'),format='A4',print_background=True,margin={'top':'18mm','bottom':'18mm','left':'18mm','right':'18mm'})
            page.close()
        # Contact sheet uses only active figure references, in reading order.
        from PIL import Image,ImageOps,ImageDraw
        paths=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',md.read_text())
        sheet=Image.new('RGB',(1200,((len(paths)+2)//3)*410),'#dddddd');d=ImageDraw.Draw(sheet)
        for i,path in enumerate(paths):
            im=Image.open((ROOT/path).with_suffix('.png'));im.thumbnail((390,380))
            x=(i%3)*400+(400-im.width)//2;y=(i//3)*410+22
            sheet.paste(im,(x,y));d.text(((i%3)*400+8,(i//3)*410+5),f'{n}-{i+1}',fill='black')
        sheet.save(target/'contact-sheet.png')
        (ROOT/f'ch{n:02}'/'teaching-browser-validation.json').write_text(json.dumps([r for r in records if r['chapter']==n],ensure_ascii=False,indent=2)+'\n')
    browser.close()
(review/'browser-validation.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print(json.dumps([dict(chapter=r['chapter'],width=r['width'],figures=len(r['images']),math=r['mathCount'],status='passed') for r in records]))
