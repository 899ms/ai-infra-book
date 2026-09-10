#!/usr/bin/env python3
"""Check offline rendering in desktop/mobile Chromium and save representative views."""
from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--executable',default='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');args=parser.parse_args()
catalog=json.loads((HERE/'figure-catalog.json').read_text());figure_count=len(catalog)
expected=json.loads((HERE/'math-validation.json').read_text())['expressions'];results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=args.executable,headless=True)
 for label,width,height in [('desktop',1440,1000),('mobile',390,844)]:
  page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
  page.goto((HERE.parent/'12-端边云协同.html').as_uri(),wait_until='load');page.evaluate('document.fonts.ready')
  result=page.evaluate('''() => ({images:document.images.length,loadedImages:[...document.images].filter(x=>x.complete&&x.naturalWidth>0).length,captions:document.querySelectorAll('figcaption').length,formulas:document.querySelectorAll('.katex').length,mathErrors:document.querySelectorAll('.katex-error').length,viewport:innerWidth,documentWidth:document.documentElement.scrollWidth,brokenAnchors:[...document.querySelectorAll('a[href^="#"]')].map(a=>a.getAttribute('href').slice(1)).filter(id=>!document.getElementById(decodeURIComponent(id)))})''')
  page.locator('figure img').nth(4).click();page.wait_for_selector('#figure-viewer[open]')
  result['zoomWorks']=page.locator('#figure-viewer img').evaluate('(img)=>img.complete && img.naturalWidth>0 && img.getBoundingClientRect().width>=900')
  page.locator('.viewer-close').click();page.wait_for_selector('#figure-viewer[open]',state='hidden')
  result['device']=label;result['passed']=result['images']==result['loadedImages']==result['captions']==figure_count and result['formulas']==expected and result['mathErrors']==0 and result['documentWidth']<=width and not result['brokenAnchors'] and result['zoomWorks']
  page.evaluate('window.scrollTo(0,0)');page.screenshot(path=str(HERE/f'preview-{label}.png'));page.locator('figure').nth(0).scroll_into_view_if_needed();page.screenshot(path=str(HERE/f'preview-{label}-raw.png'))
  page.locator('figure').nth(next(e['number']-1 for e in catalog if e['source_id']==6)).scroll_into_view_if_needed();page.screenshot(path=str(HERE/f'preview-{label}-queqiao.png'))
  for number,name in [(5,'agent'),(9,'window'),(14,'budgets'),(16,'recovery')]:
   page.locator('figure').nth(number-1).scroll_into_view_if_needed();page.screenshot(path=str(HERE/f'preview-{label}-{name}.png'))
  results.append(result);page.close()
 browser.close()
out={'passed':all(x['passed'] for x in results),'viewports':results};(HERE/'browser-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False,indent=2));raise SystemExit(not out['passed'])
