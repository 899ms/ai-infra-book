from pathlib import Path
from playwright.sync_api import sync_playwright
import json
r=Path(__file__).resolve().parents[2];d=r/'manuscripts/ch05';records=[]
with sync_playwright() as p:
 chrome=Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 browser=p.chromium.launch(**({'executable_path':str(chrome)} if chrome.exists() else {}),headless=True)
 for width in [1440,390]:
  page=browser.new_page(viewport={'width':width,'height':1050},device_scale_factor=1)
  page.goto((r/'manuscripts/05-算子与运行时.html').as_uri());page.wait_for_load_state('load')
  result=page.evaluate('''() => ({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,images:[...document.images].map(i=>({loaded:i.complete&&i.naturalWidth>0})),mathErrors:document.querySelectorAll('.katex-error').length,mathCount:document.querySelectorAll('.katex').length})''')
  page.screenshot(path=str(d/f'preview-{width}.png'))
  if width==1440:
   page.get_by_role('heading',name='5.4.2 用循环变换表达分块与融合').scroll_into_view_if_needed();page.screenshot(path=str(d/'preview-polyhedral.png'))
   page.locator('img').nth(8).scroll_into_view_if_needed();page.screenshot(path=str(d/'preview-loop-figure.png'))
   page.locator('img').nth(15).scroll_into_view_if_needed();page.screenshot(path=str(d/'preview-critical-path.png'))
  records.append(result);page.close()
 browser.close()
(d/'browser-validation.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(records,indent=2))
assert all(z['scrollWidth']<=z['width'] and z['mathErrors']==0 and len(z['images'])==17 and all(i['loaded'] for i in z['images']) for z in records)
