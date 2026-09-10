#!/usr/bin/env python3
"""Verify chapter artifacts and retained outline structure, without running models."""
from pathlib import Path
import hashlib,json,re,urllib.parse,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
md=HERE.parent/'03-推理与训练负载.md';s=md.read_text();outline=(ROOT/'outlines/03-推理与训练负载.md').read_text();errors=[]
def check(ok,msg):
 if not ok:errors.append(msg)
def heads(s):return re.findall(r'^#{2,3} (3\.\d+(?:\.\d+)?) ',s,re.M)
check(heads(s)==heads(outline),'outline section numbering/order differs')
labs=sorted(set(map(int,re.findall(r'\*\*练习 3-(\d+)',s))))
check(labs==list(range(1,11)),'ten exercises missing')
figs=re.findall(r'!\[[^\]]*\]\((ch03/[^)]+\.svg)\)',s)
index=json.loads((HERE/'figure-index.json').read_text());check(figs==[z['asset'] for z in index],'Figure index matches reading order')
check(re.findall(r'^\*图 (3-\d+)',s,re.M)==[z['figure'] for z in index],'External caption sequence')
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
for z in json.loads((HERE/'teaching-browser-validation.json').read_text()):
 check(z['width']==z['scrollWidth'] and all(i['loaded'] for i in z['images']) and len(z['images'])==len(figs) and z['mathErrors']==0 and not z['brokenAnchors'],'browser check')
layout=json.loads((HERE/'teaching-layout-validation.json').read_text())
check(len(layout)==len(figs) and all(z['width_pt']==420 and z['min_label_pt']>=11 and not z['text_extent_warnings'] for z in layout),'book-size figure typography')
report={'chapter':3,'headings':len(heads(s)),'exercises':labs,'figures':len(figs),'math_expressions':math['expressions'],'chinese_characters':len(re.findall(r'[\u4e00-\u9fff]',s)),'errors':errors}
(HERE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False));raise SystemExit(bool(errors))
