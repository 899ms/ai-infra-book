"""Check the generated site at desktop and mobile widths for changed chapters."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
import re
ROOT=Path(__file__).resolve().parents[2]
rows=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
    for ch in (1,4,5,6,7,9,10):
        source=next((ROOT/'manuscripts').glob(f'{ch:02}-*.md'))
        expected=len(re.findall(r'!\[',source.read_text()))
        target=next((ROOT/'build/site/manuscripts').glob(f'{ch:02}-*.html'))
        for width in (1440,390):
            page=browser.new_page(viewport={'width':width,'height':1000})
            page.goto(target.as_uri(),wait_until='load')
            page.wait_for_function('window.MathJax && MathJax.startup && MathJax.startup.promise',timeout=30000)
            page.evaluate('MathJax.startup.promise')
            result=page.evaluate('''() => ({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,images:[...document.images].filter(i=>i.src.includes('/ch')).map(i=>({loaded:i.complete&&i.naturalWidth>0,src:i.getAttribute('src')})),mathErrors:document.querySelectorAll('mjx-merror').length,mathCount:document.querySelectorAll('mjx-container').length})''')
            result.update(chapter=ch,expected_images=expected)
            assert result['scrollWidth']<=width,(ch,width,'overflow')
            assert len(result['images'])==expected and all(i['loaded'] for i in result['images']),(ch,'images')
            assert result['mathCount']>0 and not result['mathErrors'],(ch,'math')
            rows.append(result);page.close()
    browser.close()
(Path(__file__).parent/'browser-validation.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(f'PASS: {len(rows)} chapter/viewport combinations, images and rendered math')
