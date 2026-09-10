"""Audit the authorized cross-chapter revision against its source snapshots."""
from pathlib import Path
from urllib.parse import unquote,urlsplit
import json,re,hashlib
R=Path(__file__).resolve().parent;ROOT=R.parents[1];M=ROOT/'manuscripts';errors=[];rows=[]
def check(ok,msg):
 if not ok:errors.append(msg)
for n in range(1,13):
 p=next(M.glob(f'{n:02}-*.md'));s=p.read_text();before=(R/'before'/p.relative_to(ROOT)).read_text();page=(ROOT/'build/legacy'/p.relative_to(ROOT).with_suffix('.html')).read_text()
 heads=re.findall(r'^## (.+)$',s,re.M);check(heads[-1]=='本章小结' and heads.count('本章小结')==1,f'{n}: final conclusion')
 check(not any('资料' in h or '证据范围' in h for h in heads),f'{n}: no evidence section')
 check('V4.1' in s and '[^v41-case]' in s,f'{n}: case and source')
 defined=set(re.findall(r'^\[\^([^\]]+)\]:',s,re.M));used=set(re.findall(r'\[\^([^\]]+)\](?!:)',s));check(used<=defined,f'{n}: undefined footnotes {used-defined}')
 for url in re.findall(r'\]\(([^)]+)\)',s):
  u=urlsplit(url.strip('<>'))
  if not u.scheme and u.path:check((p.parent/unquote(u.path)).exists(),f'{n}: missing {url}')
 exercises=lambda t:re.findall(r'^> \*\*(?:练习|实验) (\d+-\d+)',t,re.M)
 check(exercises(s)==exercises(before),f'{n}: exercise identifiers preserved')
 old_assets=re.findall(r'!\[[^\n]*\]\(([^)]+)\)',before);assets=re.findall(r'!\[[^\n]*\]\(([^)]+)\)',s)
 check([a for a in assets if a in old_assets]==old_assets,f'{n}: original figures preserved')
 index=json.loads((M/f'ch{n:02}/figure-index.json').read_text());got=[r.get('asset') or f'ch{n:02}/'+(r.get('file') or r['name']+'.svg') for r in index];check(assets==got,f'{n}: active figure index')
 check(re.findall(r'<h2\b[^>]*>(.*?)</h2>',page,re.S)[-1]=='本章小结',f'{n}: HTML last section')
 rows.append(dict(chapter=n,figures=len(assets),added_figures=len(assets)-len(old_assets)))
data=json.loads((ROOT/'calculations/results/v41-throughline.json').read_text())
for source in data['sources']:check(hashlib.sha256((ROOT/source['path']).read_bytes()).hexdigest()==source['sha256'],f'source hash {source["path"]}')
check(data['ced']['ced_token_layers']==166400,'CED arithmetic');check(abs(data['transfer']['global_only_ms']['deepseek-v4.1-flash']-4.6661632)<1e-9,'transfer arithmetic')
check(sum(r['added_figures'] for r in rows)==1,'one new figure')
report=dict(passed=not errors,chapters=rows,total_figures=sum(r['figures'] for r in rows),errors=errors);(R/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
