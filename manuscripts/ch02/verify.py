#!/usr/bin/env python3
"""Verify chapter 2 coverage, locked evidence, numeric anchors and reading artifacts."""
from pathlib import Path
from urllib.parse import unquote,urlsplit
import hashlib,html,json,re,xml.etree.ElementTree as ET
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[1];M=H.parent/'02-模型架构.md'
s=M.read_text();outline=(R/'outlines/02-模型架构.md').read_text();errors=[]
def check(ok,msg):
 if not ok:errors.append(msg)
def load(n):return json.loads((R/'calculations/results'/f'{n}.json').read_text())
head=lambda t:re.findall(r'^#{2,3} (2\.\d+(?:\.\d+)? [^\n]+)',t,re.M)
check(head(s)==head(outline),'Outline headings/order differ')
check(re.findall(r'^> \*\*练习 (2-\d+)',s,re.M)==[f'2-{i}' for i in range(1,10)],'Exercise sequence')
check(re.findall(r'^> \*\*练习 (2-\d+)[^\n]*〔核心〕',s,re.M)==['2-2','2-5','2-7'],'Core exercise selection')
check(len(re.findall(r'!\[图 2-',s))==15,'Fifteen manuscript figures')
check(not re.search('配图计划|待扩写|此处补充',s),'Unexpanded placeholder')
lock=json.loads((H/'sources.json').read_text())
for row in lock['sources']:check(hashlib.sha256((R/row['path']).read_bytes()).hexdigest()==row['sha256'],'Source changed: '+row['path'])
links=0
for source in [M,H/'README.md']:
 for u in re.findall(r'\]\(([^)]+)\)',source.read_text()):
  q=urlsplit(unquote(u))
  if q.scheme or not q.path:continue
  p=(source.parent/q.path).resolve();check(p.exists(),'Broken link '+u);links+=1
page=(H.parent/'02-模型架构.html').read_text();ids=set(re.findall(r'\bid="([^"]+)"',page))
for target in re.findall(r'href="#([^"]+)"',page):check(unquote(target) in ids,'Missing navigation target '+target)
check(page.count('src="data:image/png;base64,')==15,'Fifteen embedded images')
for p in H.glob('figure-*.svg'):
 ET.parse(p);check(not re.search(r'图\s*2[-－]\d',p.read_text()),'Internal figure caption '+p.name)
for p in H.glob('figure-*.png'):
 with Image.open(p) as im:check(im.width>=1800 and im.height>=1000,'Figure too small '+p.name);im.verify()
manifest=json.loads((H/'manifest.json').read_text())
for row in manifest['outputs']:check(hashlib.sha256((R/row['path']).read_bytes()).hexdigest()==row['sha256'],'Artifact changed: '+row['path'])
q=load('qwen3-8b-prefill-8192')['summary'];d=load('qwen3-8b-decode-b1-s8192')['summary']
check(q['parameters']==8190735360,'Qwen parameter anchor');check(2*36*8*128*2==q['kv_bytes_per_token_per_request'],'Qwen KV formula')
check(f"{q['matrix_flops']/1e12:.1f}" in s,'Prefill number in text');check(f"{d['matrix_flops']/1e9:.1f}" in s,'Decode number in text')
kv=147456;H0=8192;D=1024
check(kv*(D*H0+D*(D-1)//2)/2**30==1223.9296875,'Accumulated history')
request=load('request-four-models-book')
check(request['contract']['decode_forward_calls']==3 and request['contract']['final_retained_positions']==131,'Request call contract')
for row in request['comparisons']:check(f"{row['summary']['matrix_flops']/1e12:.2f}" in s,'Request FLOPs '+row['model'])
fdata=json.loads((H/'figure-data.json').read_text());v=load('state-deepseek-v4-flash-n8192-b1-native')['summary'];k=load('state-kimi-k3-n8192-b1-compact')['summary']
check(fdata['figure_2_7']['resident_bytes']['v4'][0]==v['resident_bytes'],'V4 curve anchor');check(fdata['figure_2_7']['resident_bytes']['k3'][0]==k['resident_bytes'],'K3 curve anchor')
check(fdata['figure_2_7']['accounted_access_bytes']['v4'][0]==v['selected_history_payload_bytes'],'V4 access curve anchor')
browser=json.loads((H/'browser-validation.json').read_text());check(browser['loaded_images']==15 and browser['all_nav_targets_exist'],'Browser image/navigation');check(not browser['desktop_overflow'] and not browser['mobile_overflow'],'Reading layout overflow')
check('<sub>' not in s and '<sup>' not in s,'HTML math in manuscript')
check(len(re.findall(r'^\*\*表 2-[1-5]',s,re.M))==5,'Five model module tables')
math_report=json.loads((H/'math-validation.json').read_text());check(math_report['expressions']>250 and not math_report['errors'],'LaTeX rendering')
table_report=json.loads((H/'table-validation.json').read_text());check(all(x['matched'] for x in table_report),'Matrix dimensions match evidence')
check(browser['math_errors']==0,'Browser math errors')
report={'status':'passed' if not errors else 'failed','chinese_characters':len(re.findall('[\u4e00-\u9fff]',s)),'sections':6,'subsections':21,'exercises':9,'figures':15,'source_hashes_checked':len(lock['sources']),'local_links_checked':links,'numeric_checks':'Qwen parameter/KV/prefill/decode, accumulated history, four-model requests, V4/K3 curve anchors','browser':browser,'errors':errors}
(H/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
