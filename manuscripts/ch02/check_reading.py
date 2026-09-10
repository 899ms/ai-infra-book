from pathlib import Path
import json,re
from PIL import Image,ImageOps,ImageDraw
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[1]
paths=[H/x for x in re.findall(r'\]\(ch02/(figure-[^)]+)\)',(H.parent/'02-模型架构.md').read_text())]
thumbs=[]
for p in paths:
 im=Image.open(p.with_suffix('.png')).convert('RGB');im.thumbnail((680,450));tile=Image.new('RGB',(700,480),'white');tile.paste(im,((700-im.width)//2,20));ImageDraw.Draw(tile).text((10,455),p.name,fill='black');thumbs.append(tile)
contact=Image.new('RGB',(1400,480*5),'#eee')
for i,t in enumerate(thumbs):contact.paste(t,((i%2)*700,(i//2)*480))
contact.save(H/'contact-sheet.png')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 page=browser.new_page(viewport={'width':1400,'height':1050});page.goto((H.parent/'02-模型架构.html').as_uri());page.wait_for_function('document.fonts.status === "loaded"');page.screenshot(path=str(H/'reading-desktop.png'))
 def metrics():return page.evaluate('''()=>({loaded_images:[...document.images].filter(x=>x.complete&&x.naturalWidth).length,all_nav_targets_exist:[...document.querySelectorAll('nav a')].every(x=>document.getElementById(decodeURIComponent(x.hash.slice(1)))),overflow:document.documentElement.scrollWidth>innerWidth,math_errors:document.querySelectorAll('.katex-error').length,math_count:document.querySelectorAll('.katex').length,tables:document.querySelectorAll('table').length})''')
 d=metrics();page.get_by_text('表 2-5　Kimi K3：KDA、紧凑 MLA 与潜空间专家',exact=True).evaluate('(e)=>e.scrollIntoView({block:"start"})');page.screenshot(path=str(H/'reading-k3-table.png'))
 page.set_viewport_size({'width':390,'height':844});page.get_by_text('表 2-5　Kimi K3：KDA、紧凑 MLA 与潜空间专家',exact=True).evaluate('(e)=>e.scrollIntoView({block:"start"})');page.screenshot(path=str(H/'reading-mobile.png'));m=metrics()
 report={**d,'desktop_overflow':d['overflow'],'mobile_overflow':m['overflow'],'viewport_mobile':390};(H/'browser-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report);browser.close()
