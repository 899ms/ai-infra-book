#!/usr/bin/env python3
"""Optional browser layout check (requires Playwright and Chromium/Chrome)."""
from pathlib import Path
import argparse, json
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--executable', default='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
args=parser.parse_args()
results=[]
expected_formulas=json.loads((HERE/'math-validation.json').read_text())['expressions']
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=args.executable,headless=True)
    for label,width,height in [('desktop',1440,1000),('mobile',390,844)]:
        page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
        page.goto((HERE.parent/'08-推理优化.html').as_uri(),wait_until='load')
        page.evaluate('document.fonts.ready')
        result=page.evaluate('''() => ({images:document.images.length,loadedImages:[...document.images].filter(x=>x.complete&&x.naturalWidth>0).length,formulas:document.querySelectorAll('.katex').length,mathErrors:document.querySelectorAll('.katex-error').length,viewport:innerWidth,documentWidth:document.documentElement.scrollWidth,brokenAnchors:[...document.querySelectorAll('a[href^="#"]')].map(a=>a.getAttribute('href').slice(1)).filter(id=>!document.getElementById(decodeURIComponent(id)))})''')
        result['device']=label
        result['passed']=result['images']==result['loadedImages']==15 and result['formulas']==expected_formulas and result['mathErrors']==0 and result['documentWidth']<=width and not result['brokenAnchors']
        page.screenshot(path=str(HERE/f'preview-{label}.png'))
        page.locator('img').nth(5).scroll_into_view_if_needed()
        page.screenshot(path=str(HERE/f'preview-{label}-prefix.png'))
        page.locator('main img').nth(5).click()
        result['image_zoom_opened']=page.locator('#figure-view').evaluate('(x)=>x.open')
        page.locator('#close-figure').click()
        result['image_zoom_closed']=not page.locator('#figure-view').evaluate('(x)=>x.open')
        result['passed']=result['passed'] and result['image_zoom_opened'] and result['image_zoom_closed']
        results.append(result)
        page.close()
    browser.close()
out={'passed':all(x['passed'] for x in results),'viewports':results}
(HERE/'browser-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
raise SystemExit(0 if out['passed'] else 1)
