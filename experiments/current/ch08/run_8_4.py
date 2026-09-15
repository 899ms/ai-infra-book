"""Prefix retention value and measured token overlap versus cache hits."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2];sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.models import forward
from infra_calc.schema import Scenario
source=next((ROOT/'manuscripts').glob('08-*.md'));raw=ROOT/'experiments/ch08/08-04'
work={n:forward('qwen3-8b',Scenario(history=0,tokens=n,output_head='none')) for n in (2048,6144)}
rows=[]
for bandwidth in (64,32):
 vals=[]
 for n in (6144,2048):
  flops=work[n]['summary']['matrix_flops'];tr=F(flops,1)/F(5038*10**11)*F(100,62);tf=F(n*147456,bandwidth*10**9);v=(tr-tf)/2-tf
  vals.append((tr,tf,v));rows.append(dict(link_GBps=bandwidth,tokens=n,matrix_flops=flops,recompute_ms=float(tr*1000),fetch_and_separate_maintenance_each_ms=float(tf*1000),expected_net_saved_ms=float(v*1000)))
 a,b=vals;threshold=(3*b[2]+a[1])/(a[0]-a[1]);assert threshold*(a[0]-a[1])-a[1]==3*b[2]
 rows.append(dict(link_GBps=bandwidth,one_A_saved_ms=float(a[2]*1000),three_B_saved_ms=float(3*b[2]*1000),A_hit_probability_tie=float(threshold),winner_at_half='A' if a[2]>3*b[2] else 'three_B'))
inputs=json.loads((raw/'inputs/agent-prompts.json').read_text());seq=[r['prompt_token_ids'] for r in inputs['requests']]
def lcp(a,b):
 for i,(x,y) in enumerate(zip(a,b)):
  if x!=y:return i
 return min(len(a),len(b))
rounds=[]
for i,s in enumerate(seq):
 prev=lcp(s,seq[i-1]) if i else 0;best=max((lcp(s,t) for t in seq[:i]),default=0)
 rounds.append(dict(round=i,input_tokens=len(s),common_with_previous=prev,longest_common_with_any_prior=best,common_fraction=prev/len(s)))
summary=json.loads((raw/'results/summary.json').read_text());total=sum(map(len,seq));assert total==19556
hits=[]
for r in summary['configurations']:
 assert len(r['cached_by_round'])==12
 hits.append(dict(configuration=r['name'],cached_by_round=r['cached_by_round'],cached_tokens=r['cached_tokens'],token_hit_fraction=r['cached_tokens']/total,request_hit_fraction=sum(v>0 for v in r['cached_by_round'])/12))
sources=[source,raw/'inputs/agent-prompts.json',raw/'run.py',raw/'analyze.py',raw/'results/summary.json',raw/'results/raw-manifest.json']
for name in ('cache6','gap6','pressure1','pressure6','nocache6'):sources.extend(raw/'results'/name/f for f in ('environment.json','requests.jsonl'))
out=dict(exercise='8-4',retention=rows,overlap_by_round=rounds,aggregate_common_fraction=sum(r['common_with_previous'] for r in rounds)/total,aggregate_best_prior_fraction=sum(r['longest_common_with_any_prior'] for r in rounds)/total,measured_hits=hits,flop_evidence=work,scope='Exactly 62% efficiency per exercise; all 12 prompt tokens in denominator including cold first request; original failed Agent trajectory replayed for cache behavior only',source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sources})
(P/'8-4-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('flop_evidence','source_sha256')},indent=2))
