"""Exact preparation/execution accounting; two buckets cached means bucket P=0 only."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,math
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
P={'generic':100,'bucket':400,'specialized':900};rates={'generic':100,'bucket':200,'specialized':250};factor=6*4096*12288
cases={}
for small in (8,4):
 shapes=[256]*small+[1536,2048];groups={}
 for strategy in P:
  padded=[512 if n<=512 else 2048 for n in shapes] if strategy=='bucket' else shapes
  times=[F(n*factor,rates[strategy]*10**9) for n in padded] # ms
  groups[strategy]=dict(actual_rows=sum(shapes),executed_rows=sum(padded),call_ms=[float(t) for t in times],group_ms=float(sum(times)),group_exact=str(sum(times)))
 slopes={s:F(g['group_exact']) for s,g in groups.items()};cross={}
 for a,b in [('generic','bucket'),('generic','specialized'),('bucket','specialized')]:
  r=F(P[b]-P[a],1)/(slopes[a]-slopes[b]);assert F(P[a])+r*slopes[a]==F(P[b])+r*slopes[b]
  cross[a+'_'+b]=dict(exact=str(r),groups=float(r))
 winners={};timelines={}
 for cache in ('cold','bucket_cached'):
  prep=dict(P);prep['bucket']=0 if cache=='bucket_cached' else prep['bucket']
  scan=[]
  for r in range(1,1001):
   totals={s:F(prep[s])+r*slopes[s] for s in P};lowest=min(totals.values());scan.append(dict(groups=r,winners=[s for s,t in totals.items() if t==lowest],total_ms={s:float(t) for s,t in totals.items()}))
  winners[cache]=scan
  tl=[]
  for s in P:
   t=F(prep[s]);events=[dict(stage='prepare',start_ms=0,end_ms=float(t))]
   for i,n in enumerate(shapes):
    execrows=512 if s=='bucket' and n<=512 else (2048 if s=='bucket' else n)
    duration=F(execrows*factor,rates[s]*10**9)
    events.append(dict(stage='execute',call=i,actual_rows=n,executed_rows=execrows,start_ms=float(t),end_ms=float(t+duration)));t+=duration
   assert t==prep[s]+slopes[s];tl.append(dict(strategy=s,events=events))
  timelines[cache]=tl
 cases[str(small)]=dict(groups=groups,pairwise_cold_crossings=cross,winners=winners,one_group_timelines=timelines)
out=dict(exercise='5-7',scope='Teaching rates and preparation costs, not measured compiler performance',cases=cases,source_sha256={'manuscripts/05-算子与运行时.md':hashlib.sha256((ROOT/'manuscripts/05-算子与运行时.md').read_bytes()).hexdigest()})
(R/'5-7-results.json').write_text(json.dumps(out,indent=2)+'\n')
for n,c in cases.items():
 print('small calls',n,'group ms',{k:v['group_ms'] for k,v in c['groups'].items()},'crossings',c['pairwise_cold_crossings'])
 for cache,rows in c['winners'].items():print(cache,[(r['groups'],r['winners']) for i,r in enumerate(rows) if i==0 or r['winners']!=rows[i-1]['winners']])
