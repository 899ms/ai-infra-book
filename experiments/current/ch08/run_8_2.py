"""Hand-derived scheduling rounds plus verified six-request replay analysis."""
from pathlib import Path
import json,hashlib,statistics as st,math
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('08-*.md'));raw=ROOT/'experiments/ch08/08-02'
def duration(tokens,pairs):return 26220000+30400*tokens+3*pairs
rounds=[]
for name,tokens,pairs in [('r0_r1_initial_prefill',4096,2*2048*2049//2),('r0_r1_next_decode',2,2*2049),('r0_decode_and_r2_prefill',8193,8192*8193//2+2050)]:rounds.append(dict(name=name,new_tokens=tokens,causal_pairs=pairs,duration_ns=duration(tokens,pairs),duration_ms=duration(tokens,pairs)/1e6))
records=[];sources=[source,raw/'run.py',raw/'analyze.py',raw/'verify.py']
for name in ['measured-chunk512','measured-chunk8192','measured-nochunk8192','measured-graph512']:
 d=raw/'results'/name;s=json.loads((d/'summary.json').read_text());env=json.loads((d/'environment.json').read_text());assert env['requests_sha256']==hashlib.sha256((d/'requests.json').read_bytes()).hexdigest();assert env['run_sha256']==hashlib.sha256((raw/'run.py').read_bytes()).hexdigest()
 itl=sorted(v*1000 for v in s['engine']['inter_token_intervals_s']);assert len(itl)==1998
 records.append(dict(configuration=name,budget=env['config']['max_num_batched_tokens'],max_ITL_ms=max(itl),median_ITL_ms=st.median(itl),p95_ITL_ms=itl[math.ceil(.95*len(itl))-1],passes_observed_strict_50ms=max(itl)<50,per_request=[dict(id=f'r{i}',median_engine_queue_ms=st.median(r['engine_queue_ms'] for r in s['requests'] if r['id']==f'r{i}'),median_TTFT_ms=st.median(r['delivered_ttft_ms'] for r in s['requests'] if r['id']==f'r{i}')) for i in range(6)]))
 sources.extend(d/f for f in ('environment.json','requests.json','summary.json','engine-stats.jsonl','events.jsonl'))
pairs=[dict(new_tokens=512,history=h,causal_pairs=512*h+512*513//2) for h in (0,7680)]
out=dict(exercise='8-2',hand_rounds=rounds,attention_pairs=pairs,replay=records,scope='Four-request analytical model distinct from archived six-request real GPU replay; observed interval maximum is not a prospective SLO guarantee; no new replay',source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sources})
(P/'8-2-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(rounds=rounds,replay=[dict(config=r['configuration'],max_ms=r['max_ITL_ms'],r4=r['per_request'][4]) for r in records]),indent=2))
