"""Verify the rebuilt chapter on desktop/mobile and capture changed tables."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[1]
preview=R/'build/legacy/manuscripts/02-模型架构.html'
output=R/'build/ch02-v41/browser';output.mkdir(parents=True,exist_ok=True)
reports=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
    page=browser.new_page()
    for width,height in [(1440,1050),(390,844)]:
        page.set_viewport_size({'width':width,'height':height})
        page.goto(preview.as_uri());page.wait_for_function('document.fonts.status === "loaded"')
        report=page.evaluate('''()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
          images:[...document.images].map(i=>({loaded:i.complete&&i.naturalWidth>0,width:i.getBoundingClientRect().width})),
          mathErrors:document.querySelectorAll('.katex-error').length,mathCount:document.querySelectorAll('.katex').length,
          brokenAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(decodeURIComponent(a.hash.slice(1)))).map(a=>a.hash)})''')
        for tag in ('A','B','C','D','E','6'):
            locator=page.locator('strong').filter(has_text=f'表 2-{tag}').first
            locator.scroll_into_view_if_needed()
            page.screenshot(path=str(output/f'table-{tag}-{width}.png'))
        assert report['scrollWidth']<=width and not report['mathErrors'] and not report['brokenAnchors'],report
        assert len(report['images'])==36 and all(x['loaded'] for x in report['images'])
        reports.append(report)
    browser.close()
(H/'teaching-browser-validation.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
print('PASS: rebuilt chapter, desktop/mobile, 36 images, formulas and anchors; six changed tables captured.')
