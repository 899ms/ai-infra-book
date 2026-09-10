"""Refresh the added section in the existing offline chapter HTML, without rerendering figures."""
import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
md=ROOT/'manuscripts/02-模型架构.md'
html=md.with_suffix('.html')
section=md.read_text().split('### 2.3.6 ',1)[1].split('## 2.4 ',1)[0]
section='### 2.3.6 '+section
maths=[]
def protect(match):
    text=match.group(); display=text.startswith('$$')
    token=f'V41MATHPLACEHOLDER{len(maths)}END'
    maths.append(dict(latex=text[2:-2].strip() if display else text[1:-1],display=display,token=token))
    return '\n\n'+token+'\n\n' if display else token
protected=re.sub(r'\$\$[\s\S]*?\$\$|\$[^$\n]+\$',protect,section)
body=subprocess.run(['pandoc','--from=markdown','--to=html'],input=protected,text=True,capture_output=True,check=True).stdout
js="const fs=require('fs'),k=require(process.argv[1]);let a=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(a.map(x=>k.renderToString(x.latex,{displayMode:x.display,throwOnError:true,output:'htmlAndMathml'}))))"
rendered=json.loads(subprocess.run(['node','-e',js,str(ROOT/'manuscripts/ch02/vendor/katex/katex.js')],input=json.dumps(maths),text=True,capture_output=True,check=True).stdout)
for item,value in zip(maths,rendered):
    body=body.replace('<p>'+item['token']+'</p>',value) if item['display'] else body.replace(item['token'],value)
body=re.sub(r'<table>(.*?)</table>',r'<div class="table-scroll"><table>\1</table></div>',body,flags=re.S)
start='<!-- v41-cache-comparison:start -->';end='<!-- v41-cache-comparison:end -->'
page=html.read_text()
block=start+'\n'+body+'\n'+end+'\n'
if start in page:
    page=re.sub(re.escape(start)+r'[\s\S]*?'+re.escape(end)+r'\n?',lambda _:block,page,count=1)
else:
    anchor=re.search(r'<h2[^>]*>2\.4 条件计算与专家权重复用</h2>',page)
    if not anchor:raise ValueError('Chapter 2.4 anchor missing')
    page=page[:anchor.start()]+block+page[anchor.start():]
if 'V41MATHPLACEHOLDER' in page:raise ValueError('Unrendered math')
html.write_text(page)
print(json.dumps(dict(section='2.3.6',math_expressions=len(maths),html=str(html.relative_to(ROOT)))))
