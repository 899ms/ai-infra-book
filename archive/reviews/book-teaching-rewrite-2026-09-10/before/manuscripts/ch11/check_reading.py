#!/usr/bin/env python3
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[2];HERE=ROOT/'manuscripts/ch11';records=[]
with sync_playwright() as p:
 chrome=Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 browser=p.chromium.launch(**({'executable_path':str(chrome)} if chrome.exists() else {}),headless=True)
 for width in [1440,390]:
  page=browser.new_page(viewport={'width':width,'height':1050},device_scale_factor=1)
  page.goto((ROOT/'manuscripts/11-资源调度与运行环境.html').as_uri());page.wait_for_load_state('load')
  result=page.evaluate('''() => ({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,images:[...document.images].map(i=>({loaded:i.complete&&i.naturalWidth>0})),mathErrors:document.querySelectorAll('.katex-error').length,mathCount:document.querySelectorAll('.katex').length,captions:document.querySelectorAll('figcaption').length,nav:[...document.querySelectorAll('nav a')].map(a=>({target:a.hash,valid:!!document.getElementById(a.hash.slice(1))})),externalAssets:[...document.querySelectorAll('script[src],link[href],img[src]')].map(e=>e.src||e.href).filter(s=>/^https?:/.test(s))})''')
  page.screenshot(path=str(HERE/f'preview-{width}.png'))
  page.get_by_role('heading',name='11.4.3 排队、限流与模型路由').scroll_into_view_if_needed();page.screenshot(path=str(HERE/f'preview-routing-{width}.png'))
  if width==1440:
   page.locator('figure').nth(13).scroll_into_view_if_needed();page.screenshot(path=str(HERE/'preview-cost-figure.png'))
  records.append(result);page.close()
 browser.close()
passed=all(r['scrollWidth']<=r['width'] and r['mathErrors']==0 and r['mathCount']>0 and r['captions']==19 and len(r['images'])==19 and all(i['loaded'] for i in r['images']) and len(r['nav'])==5 and all(n['valid'] for n in r['nav']) and not r['externalAssets'] for r in records)
(HERE/'browser-validation.json').write_text(json.dumps({'passed':passed,'viewports':records},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'passed':passed,'viewports':records},ensure_ascii=False,indent=2));raise SystemExit(0 if passed else 1)
