from pathlib import Path
import re,json,html,sys
from urllib.parse import unquote,urlsplit
D=Path(__file__).resolve().parent;R=D.parents[1];O=R/'outlines';p=O/'08-单实例推理.md';e=O/'extensions'/p.name
s=p.read_text();x=e.read_text();old=(D/'outline-before.txt').read_text();ox=(D/'extension-before.txt').read_text();errors=[]
def check(ok,msg):
 if not ok:errors.append(msg)
heads=re.findall(r'^#{2,3} (8\.[^\n]+)',s,re.M)
check(heads==re.findall(r'^#{2,3} (8\.[^\n]+)',x,re.M),'main/extension headings')
for h in heads:check(f'id="detail-{h.split()[0]}"' in x,'anchor '+h)
check(len(re.findall(r'^## 8\.',s,re.M))==6,'six sections');check(len(re.findall(r'^### 8\.',s,re.M))==22,'22 subsections')
for word,n in [('实验',9),('图',8)]:
 for label,t in [('main',s),('extension',x)]:
  ids=re.findall(r'^> \*\*'+word+r' 8-(\d+)',t,re.M);check(len(ids)==n and set(ids)==set(map(str,range(1,n+1))),f'{label} {word} identities')
check(re.findall(r'^> \*\*实验 (8-\d+)[^\n]*〔核心〕',s,re.M)==['8-2','8-4','8-9'],'core exercises')
def targets(t,parent):
 return {(parent/unquote(urlsplit(u).path)).resolve() for u in re.findall(r'\]\(([^)]+)\)',t) if not re.match(r'\w+:|#',u)}
before=targets(old,O)|targets(ox,O/'extensions');after=targets(s,O)|targets(x,O/'extensions')
# Self-links changed to current anchors; all external evidence targets must survive.
missing=before-after-{p.resolve(),e.resolve()};check(not missing,'missing preserved evidence: '+str(sorted(str(t.relative_to(R)) for t in missing)))
markers=set(re.findall(r'已复算（([^）]+)）',ox));check(markers<=set(re.findall(r'已复算（([^）]+)）',x)),'calculation markers preserved')
for q in [p,e,D/'README.md']:
 for u in re.findall(r'\]\(([^)]+)\)',q.read_text()):
  if re.match(r'\w+:',u):continue
  parts=urlsplit(u);t=(q.parent/unquote(parts.path)).resolve() if parts.path else q
  if t.name in ['validation.json','full-outline-validation.json']:continue
  check(t.exists(),f'missing link {q.name}: {u}')
page=(R/'skeleton.html').read_text();article=re.search(r'<article class="card" id="ch-8">(.*?)</article>',page,re.S)[1]
sys.path.insert(0,str(R/'scripts'));from outline_text import rendered_inline
visible=html.unescape(re.sub(r'<[^>]+>','',article))
for para in s.split('## 写作资料',1)[0].split('\n\n')[2:]:
 if not para.startswith(('#','>')):check(rendered_inline(para.replace('\n',' ')) in visible,'stale HTML '+para[:50])
for h in heads:check('id="sec-'+h.split()[0].replace('.','-')+'"' in article,'HTML heading '+h)
inv=[r for r in json.loads((R/'experiments/inventory.json').read_text()) if r.get('chapter')==8]
check({r['outline_id'] for r in inv}=={f'8-{i}' for i in range(1,10)},'inventory outline identity')
for row in inv:check((R/row['directory']).is_dir(),'stable directory '+row['id'])
report=dict(status='passed' if not errors else 'failed',sections=6,subsections=22,experiments=9,figures=8,core_experiments=['8-2','8-4','8-9'],preserved_evidence_targets=len(before),preserved_calculation_markers=len(markers),errors=errors)
(D/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(errors))
