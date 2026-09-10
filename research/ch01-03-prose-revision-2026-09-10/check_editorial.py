from pathlib import Path
import json,re,math
H=Path(__file__).resolve().parent;R=H.parents[1];checks=[]
def check(name,value):checks.append(dict(name=name,passed=bool(value)))
for n in (1,2,3):
 p=next((R/'manuscripts').glob(f'{n:02d}-*.md'));s=p.read_text();b=(H/('before-'+p.name)).read_text()
 check(f'chapter {n} headings retained',re.findall(r'^#{2,3} .*',s,re.M)==re.findall(r'^#{2,3} .*',b,re.M))
 check(f'chapter {n} figures retained',re.findall(r'!\[[^\]]*\]\(([^)]+)\)',s)==re.findall(r'!\[[^\]]*\]\(([^)]+)\)',b))
 refs=set(re.findall(r'\[\^([^\]]+)\](?!:)',s));defs=re.findall(r'^\[\^([^\]]+)\]:',s,re.M)
 check(f'chapter {n} footnotes complete',refs==set(defs) and len(defs)==len(set(defs)))
 check(f'chapter {n} no control characters',not any(ord(x)<32 and x!='\n' for x in s))
 if n==2:check('all chapter 2 table rows unchanged',[x for x in s.splitlines() if x.startswith('|')]==[x for x in b.splitlines() if x.startswith('|')])
check('ideal batch throughput',round(8/(70/3350))==383)
check('MoE parameter shares',round(32.212/34.661*100)==93 and 97<277.025/284.332*100<98 and 97<2722.741/2779.484*100<98)
check('RL incremental work',math.isclose(3410.701-2181.559,1229.142))
check('training parameter-state ratio',18/2==9)
result=dict(passed=all(x['passed'] for x in checks),checks=checks)
(H/'editorial-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False));raise SystemExit(not result['passed'])
