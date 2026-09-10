from pathlib import Path
import hashlib,json
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[1];reports=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 for i in [1,2,3]:
  src=next((R/'manuscripts').glob(f'{i:02d}-*.html'));page=b.new_page();chapter=[]
  for width in [1440,390]:
   page.set_viewport_size({'width':width,'height':1000});page.goto(src.as_uri());page.wait_for_function('document.fonts.status === "loaded"')
   result=page.evaluate('''()=>({width:innerWidth,documentWidth:document.documentElement.scrollWidth,images:document.images.length,imagesLoaded:[...document.images].every(x=>x.complete&&x.naturalWidth>0),mathErrors:document.querySelectorAll('.katex-error').length,mathCount:document.querySelectorAll('.katex').length,unresolvedMath:document.body.innerText.includes('MATHPLACEHOLDER'),all_nav_targets_exist:[...document.querySelectorAll('nav a')].every(x=>document.getElementById(decodeURIComponent(x.hash.slice(1)))),tables:document.querySelectorAll('table').length})''')
   assert result['width']==result['documentWidth'] and result['imagesLoaded'] and result['mathErrors']==0 and not result['unresolvedMath'] and result['all_nav_targets_exist'],result
   chapter.append(result);page.screenshot(path=str(H/f'ch{i:02d}-{width}.png'))
   if i==2:
    for text,name in [('表 2-A　四个模型的总体架构（固定文本主干配置）','overview'),('表 2-5　Kimi K3：KDA、紧凑 MLA 与潜空间专家','k3'),('表 2-C　相同输入条件下的计算与状态','resources')]:
     page.get_by_text(text,exact=True).evaluate('(e)=>e.scrollIntoView({block:"start"})');page.screenshot(path=str(H/f'ch02-{name}-{width}.png'))
  if i==2:
   d,m=chapter;report={'loaded_images':d['images'],'all_nav_targets_exist':d['all_nav_targets_exist'],'desktop_overflow':d['documentWidth']>d['width'],'mobile_overflow':m['documentWidth']>m['width'],'math_errors':d['mathErrors'],'html_sha256':hashlib.sha256(src.read_bytes()).hexdigest()};(R/'manuscripts/ch02/browser-validation.json').write_text(json.dumps(report,indent=2)+'\n')
  if i==3:(R/'manuscripts/ch03/browser-validation.json').write_text(json.dumps(chapter,indent=2)+'\n')
  reports.append({'chapter':i,'html_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'viewports':chapter});page.close()
 b.close()
(H/'browser-review.json').write_text(json.dumps(reports,indent=2)+'\n');print(json.dumps(reports,indent=2))
