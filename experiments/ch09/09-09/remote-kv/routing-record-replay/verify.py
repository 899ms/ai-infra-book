"""Independently check replay decisions, coverage and source identity."""
import hashlib,json,itertools,math,statistics
from pathlib import Path
R=Path(__file__).resolve().parent;B=R.parent.parent
s=json.loads((R/'results.json').read_text())
for p,h in s['source_sha256'].items():assert hashlib.sha256((B/p).read_bytes()).hexdigest()==h
expected=set(itertools.product([('chat',i) for i in range(4)]+[('agent',i) for i in range(12)],range(6),['cache','cold'],[1,2],['queue_first','cache_first','predicted_completion']))
seen=set()
for d in s['decisions']:
 key=((d['kind'],d['turn']),d['queue_source_row'],d['busy'],d['cold_pass'],d['policy']);assert key not in seen;seen.add(key)
 choices=['cold','cache'];q=d['queue_s'];e=d['estimated_service_s'];h=d['available_cache_tokens']
 if d['policy']=='queue_first':score={k:(q[k],choices.index(k)) for k in choices}
 elif d['policy']=='cache_first':score={k:(-h[k],q[k],choices.index(k)) for k in choices}
 else:score={k:(q[k]+e[k],choices.index(k)) for k in choices}
 winner=sorted(choices,key=lambda k:score[k])[0];assert winner==d['selected']
 assert d['completion_s']==d['alternative_completion_s'][winner]
 assert math.isclose(d['regret_s'],d['completion_s']-min(d['alternative_completion_s'].values()),abs_tol=1e-12)
 assert q[d['busy']]>0 and q['cold' if d['busy']=='cache' else 'cache']==0
for a in s['summary']:
 rows=[r for r in s['decisions'] if all(r[k]==a[k] for k in ['kind','busy','policy'])]
 assert len(rows)==a['decisions']
 assert math.isclose(statistics.mean(r['completion_s'] for r in rows),a['mean_completion_s'])
 assert math.isclose(sum(r['cached_tokens'] for r in rows)/sum(r['input_tokens'] for r in rows),a['token_hit_rate'])
assert seen==expected
print('Verified source hashes, all 1152 unique decisions, policy ties, queue orientation, regret and summary means/hits.')
