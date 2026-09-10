"""Check full chapter and teaching excerpt in an independent headless browser."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
r=Path(__file__).resolve().parents[2];d=r/'manuscripts/ch05';records=[]
review=r/'reviews/ch05-52-53-teaching-2026-09-10';review.mkdir(exist_ok=True)
with sync_playwright() as p:
 chrome=Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
 browser=p.chromium.launch(**({'executable_path':str(chrome)} if chrome.exists() else {}),headless=True)
 for name,count in [('05-算子与运行时.html',23),('05-算子与运行时-5.2-5.3.html',13)]:
  for width in [1440,390]:
   page=browser.new_page(viewport={'width':width,'height':1050},device_scale_factor=1)
   page.goto((r/'manuscripts'/name).as_uri());page.wait_for_load_state('load')
   result=page.evaluate('''() => ({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,images:[...document.images].map(i=>({loaded:i.complete&&i.naturalWidth>0})),mathErrors:document.querySelectorAll('.katex-error').length,mathCount:document.querySelectorAll('.katex').length,teachingFigures:[...document.querySelectorAll('.teaching-figure')].map(f=>({asset:f.dataset.asset,width:f.querySelector('img').getBoundingClientRect().width,scrollable:f.querySelector('.diagram-scroll').scrollWidth>f.querySelector('.diagram-scroll').clientWidth})),brokenAnchors:[...document.querySelectorAll('a[href^="#"]')].map(a=>a.getAttribute('href').slice(1)).filter(id=>!document.getElementById(decodeURIComponent(id)))})''')
   result.update(page=name,expectedImages=count);records.append(result)
   assert result['scrollWidth']<=width and result['mathErrors']==0 and len(result['images'])==count and all(i['loaded'] for i in result['images'])
   assert not result['brokenAnchors'], result['brokenAnchors']
   assert len(result['teachingFigures'])==13
   if width==390:assert all(z['width']>=560 and z['scrollable'] for z in result['teachingFigures'])
   if count==13:
    page.screenshot(path=str(review/f'reading-{width}.png'))
    for asset in ['figure-5-reuse-steps.svg','figure-5-tile-working-set.svg','figure-5-buffer-slots.svg','figure-5-7-online-softmax.svg']:
     fig=page.locator(f'figure[data-asset="{asset}"]');fig.scroll_into_view_if_needed();page.screenshot(path=str(review/f'{Path(asset).stem}-{width}.png'))
    if width==1440:
     page.pdf(path=str(review/'sections-5.2-5.3.pdf'),format='A4',print_background=True,margin={'top':'18mm','bottom':'18mm','left':'18mm','right':'18mm'})
   else:
    page.screenshot(path=str(d/f'preview-{width}.png'))
    if width==1440:
     page.get_by_role('heading',name='5.4.2 用循环变换表达分块与融合').scroll_into_view_if_needed();page.screenshot(path=str(d/'preview-polyhedral.png'))
     for asset,out in [('figure-5-9-polyhedral.svg','preview-loop-figure.png'),('figure-5-16-critical-path.svg','preview-critical-path.png')]:
      page.locator(f'figure[data-asset="{asset}"]').scroll_into_view_if_needed();page.screenshot(path=str(d/out))
   page.close()
 browser.close()
(d/'browser-validation.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
print(json.dumps([{'page':z['page'],'width':z['width'],'images':len(z['images']),'mathCount':z['mathCount'],'brokenAnchors':z['brokenAnchors'],'status':'passed'} for z in records],ensure_ascii=False,indent=2))
