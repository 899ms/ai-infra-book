from pathlib import Path
import re,json,hashlib
H=Path(__file__).resolve().parent;R=H.parents[1];checks=[]
def check(ok,label):
 assert ok,label
 checks.append(label)
for n,count in [(1,7),(2,15),(3,11)]:
 p=next((R/'manuscripts').glob(f'{n:02d}-*.md'));s=p.read_text();before=(H/p.name).read_text()
 head=lambda x:re.findall(r'^#{2,3} .+',x,re.M)
 check(head(s)==head(before),f'ch{n}: section headings and order preserved')
 tables=lambda x:re.findall(r'^\|[^\n]+\n\|[ :|\-]+\n(?:\|[^\n]+\n)+',x,re.M)
 check(tables(s)==tables(before),f'ch{n}: all table cells preserved')
 nums=re.findall(r'^\*图 '+str(n)+r'-(\d+)[：　]',s,re.M)
 check(nums==list(map(str,range(1,count+1))),f'ch{n}: captions follow reading order')
 defs=set(re.findall(r'^\[\^([^\]]+)\]:',s,re.M));refs=set(re.findall(r'\[\^([^\]]+)\](?!:)',s))
 check(refs==defs,f'ch{n}: footnotes defined and referenced')
 for u in re.findall(r'\]\(([^)]+)\)',s):
  if '://' not in u and not u.startswith('#'):check((p.parent/u.split('#')[0]).exists(),f'ch{n}: link {u}')
 check(not any(ord(c)<32 and c not in '\t\n' for c in s),f'ch{n}: no control characters')
 check(not re.search(r'候选|子账|未闭合|token 几何|矩阵工作',s),f'ch{n}: obsolete wording absent')
 figs=re.findall(r'!\[[^\]]+\]\((ch\d+/[^)]+)\)',s)
 check(len(figs)==count,f'ch{n}: figure count')
check((R/'manuscripts/ch02/model-comparison.md').read_text().strip() in (R/'manuscripts/02-模型架构.md').read_text(),'generated comparison text matches manuscript')
d=json.loads((R/'manuscripts/ch02/figure-data.json').read_text())['teaching_diagrams']
check(d['history']['batch_crossings']==[13,51],'history crossings')
check(d['history']['read_counts']==[4,5,6,7] and sum(d['history']['read_counts'])==22,'staircase reads and retained positions')
e=d['expert_reuse'];check(e['total_assignments']==e['batch']*e['top_k']==512,'expert assignment conservation')
check(all(a*b==512 for a,b in zip(e['unique_experts'],e['rows_per_expert'])),'same expert rows in both layouts')
check(e['read_MiB'][0]/e['read_MiB'][1]==32,'expert byte ratio')
check(d['resource_comparison']['models']==json.loads((R/'manuscripts/ch02/model-comparison.json').read_text())['models'],'resource figure uses exact comparison data')
d=json.loads((R/'manuscripts/ch03/figure-data.json').read_text())['teaching_diagrams'];v=d['vision_shapes']
check(v['positions']*v['feature_groups']*v['feature_width']*2==v['ec_bytes']==8192000,'vision tensor bytes')
check(v['kv_bytes']/2**20==56.25,'vision KV bytes')
c=d['success_cost'];check([x/y for x,y in zip(c['relative_total_cost'],c['successes'])]==c['cost_per_success'],'successful task denominator')
(H/'flow-validation.json').write_text(json.dumps({'status':'passed','checks':checks},ensure_ascii=False,indent=2)+'\n');print('Passed',len(checks),'flow/figure checks')
