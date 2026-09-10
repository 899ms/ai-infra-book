#!/usr/bin/env python3
"""Verify chapter artifacts and retained outline structure, without running models."""
from pathlib import Path
import hashlib,json,re,urllib.parse,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
md=HERE.parent/'03-推理与训练负载.md';s=md.read_text();outline=(ROOT/'outlines/03-推理与训练负载.md').read_text();errors=[]
def check(ok,msg):
 if not ok:errors.append(msg)
def heads(s):return [x.replace('$','') for x in re.findall(r'^#{2,3} (3\.\d+[^\n]*)',s,re.M)]
check(heads(s)==heads(outline),'outline headings differ')
labs=sorted(set(map(int,re.findall(r'\*\*练习 3-(\d+)',s))))
check(labs==list(range(1,11)),'ten exercises missing')
figs=re.findall(r'!\[[^\]]*\]\((ch03/[^)]+\.svg)\)',s)
check(len(figs)==12,'twelve figures missing')
check(len(re.findall(r'^\*图 3-\d+：',s,re.M))==12,'external captions missing')
check(not re.search(r'<(?:sub|sup)\b',s),'manual formula sub/sup')
for link in re.findall(r'\]\(([^)]+)\)',s):
 u=urllib.parse.urlsplit(link)
 if not u.scheme and u.path:check((md.parent/urllib.parse.unquote(u.path)).exists(),'missing link '+link)
for filename in ['sources.json','manifest.json']:
 data=json.loads((HERE/filename).read_text())
 for z in data.get('sources',data.get('outputs',[])):
  p=ROOT/z['path'];check(p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==z['sha256'],'hash differs '+z['path'])
for p in HERE.glob('figure-*.svg'):
 root=ET.parse(p).getroot();texts=' '.join(''.join(e.itertext()) for e in root.iter() if e.tag.endswith('}text'))
 check(not re.search(r'图\s*3[-−]\d',texts),'embedded figure number '+p.name)
check(not json.loads((HERE/'figure-layout-check.json').read_text())['outside_canvas_text'],'figure extent warnings')
math=json.loads((HERE/'math-validation.json').read_text());check(not math['errors'],'math errors')
for z in json.loads((HERE/'browser-validation.json').read_text()):
 check(z['width']==z['documentWidth'] and z['imagesLoaded'] and z['images']==12 and z['mathErrors']==0 and not z['unresolvedMath'],'browser check')
report={'chapter':3,'headings':len(heads(s)),'exercises':labs,'figures':len(figs),'math_expressions':math['expressions'],'chinese_characters':len(re.findall(r'[\u4e00-\u9fff]',s)),'errors':errors}
(HERE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False));raise SystemExit(bool(errors))
