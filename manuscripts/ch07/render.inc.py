# Render formulas on the build machine; bundle all image/font bytes into HTML.
md=HERE.parent/'07-数据中心网络.md';raw=md.read_text();maths=[]
def protect(match):
 text=match[0];display=text.startswith('$$');latex=text[2:-2] if display else text[1:-1];token=f'MATHPLACEHOLDER{len(maths)}END';maths.append({'latex':latex.strip(),'display':display,'token':token});return '\n\n'+token+'\n\n' if display else token
protected=re.sub(r'\$\$[\s\S]*?\$\$|\$[^$\n]+\$',protect,raw)
body=markdown.markdown(protected,extensions=['tables','footnotes','fenced_code','toc'],output_format='html')
node="const fs=require('fs'),k=require(process.argv[1]);const a=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(a.map(x=>k.renderToString(x.latex,{displayMode:x.display,throwOnError:true,output:'htmlAndMathml'}))))"
res=subprocess.run(['node','-e',node,str(HERE/'vendor/katex/katex.js')],input=json.dumps(maths),text=True,capture_output=True)
if res.returncode:raise SystemExit(res.stderr)
for entry,rendered in zip(maths,json.loads(res.stdout)):
 body=body.replace('<p>'+entry['token']+'</p>',rendered) if entry['display'] else body.replace(entry['token'],rendered)
math_css=(HERE/'vendor/katex/katex.min.css').read_text()
def font_url(m):
 p=HERE/'vendor/katex'/m[1];return 'url(data:font/'+p.suffix[1:]+';base64,'+base64.b64encode(p.read_bytes()).decode()+')'
math_css=re.sub(r'url\((fonts/[^)]+)\)',font_url,math_css)
body=re.sub(r'<table>(.*?)</table>',r'<div class="table-scroll"><table>\1</table></div>',body,flags=re.S)
for p in outputs:
 if p.suffix=='.svg':body=body.replace('src="ch07/'+p.name+'"','src="data:image/png;base64,'+base64.b64encode(p.with_suffix('.png').read_bytes()).decode()+'"')
css='''*{box-sizing:border-box}body{margin:0;background:#f7f7f4;color:#243640;font:18px/1.95 Georgia,"Songti SC",serif}main{max-width:1020px;margin:auto;padding:48px 46px 85px;background:#fff}h1,h2,h3{font-family:Arial,"PingFang SC",sans-serif;line-height:1.45;color:#183949}h1{font-size:36px}h2{font-size:28px;border-top:1px solid #d5e1e4;margin-top:65px;padding-top:26px}h3{font-size:23px;margin-top:38px}a{color:#286b98;text-underline-offset:3px;overflow-wrap:anywhere}img{display:block;width:100%;height:auto;margin:28px auto 10px}em{font-size:15px;color:#546e7a}table{border-collapse:collapse;width:100%;font-size:15px;line-height:1.7;margin:22px 0}td,th{padding:10px 12px;border-bottom:1px solid #d5e1e4;text-align:left}th{background:#edf4f6}blockquote{margin:27px 0;padding:14px 24px;border-left:4px solid #16857b;background:#f0f7f4;font-size:16px}code{font:0.85em/1.6 Menlo,monospace;background:#f0f4f6;overflow-wrap:anywhere}pre{overflow-x:auto;padding:16px;max-width:100%}nav{font:16px/1.9 Arial,"PingFang SC",sans-serif;background:#eff5f7;padding:18px 24px}nav a{display:block}.footnote{font-size:14px;line-height:1.8}.footnote li{margin-bottom:13px}.table-scroll{overflow-x:auto;max-width:100%}.katex{font-size:1.04em}.katex-display{overflow-x:auto;overflow-y:hidden;padding:12px 0}@media(max-width:650px){main{padding:24px 18px}body{font-size:17px}h1{font-size:29px}h2{font-size:25px}h3{font-size:21px}}@media print{main{max-width:none;padding:0}h2,h3{break-after:avoid}img,blockquote{break-inside:avoid}body{font-size:11pt}}'''
css+='main{max-width:760px;padding-left:24px;padding-right:24px}img{max-width:720px}@media print{img{width:420pt;max-width:100%}}'
nav=''.join('<a href="#'+ident+'">'+title+'</a>' for ident,title in re.findall(r'<h2 id="([^"]+)">(7\.\d+ [^<]+)</h2>',body))
page='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>第 7 章 数据中心网络</title><style>'+css+math_css+'</style></head><body><main><nav aria-label="本章目录">'+nav+'</nav>'+body+'</main></body></html>'
import sys
sys.path.insert(0,str(HERE.parent))
from teaching_reading import readable_diagrams
page=readable_diagrams(page)
hp=md.with_suffix('.html');hp.write_text(page)
(HERE/'math-validation.json').write_text(json.dumps({'renderer':'KaTeX 0.16.11','expressions':len(maths),'display_expressions':sum(x['display'] for x in maths),'errors':[]},indent=2)+'\n')
from book_assets import sync_figure_index
active_assets=sync_figure_index(HERE)
artifacts=outputs+[HERE/'teaching_revision.py',HERE/'figure-index.json',HERE/'teaching-layout-validation.json',HERE/'figure-data.json',HERE/'teaching-data.json',hp,md]+active_assets
(HERE/'manifest.json').write_text(json.dumps({'chapter':7,'generator':'manuscripts/ch07/build.py','figures':len(outputs)//3,'font_family':family,'outputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in artifacts]},ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(outputs)} image files, {len(maths)} formulas, offline HTML; {len(layout)} extent warnings.')
