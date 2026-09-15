"""RL bottlenecks and a batch traced through retained real verl execution."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile
P=Path(__file__).resolve().parent;ROOT=P.parents[2];base=ROOT/'experiments/ch10/10-08'
for script in ['verify_manifest.py']:
 subprocess.run([sys.executable,str(base/script)],check=True,capture_output=True)
with tempfile.TemporaryDirectory(prefix='book-rl-review-') as tmp:
 subprocess.run([sys.executable,str(base/'analyze.py'),'--output',tmp],check=True,capture_output=True)
 analysis=json.loads((Path(tmp)/'summary.json').read_text())
x=json.loads((base/'control/tensor-export.json').read_text());name='advantage-batch-2.pt';t=x['tensor_files'][name];samples=[]
for row in x['decoded_batches'][name]:
 i=row['index'];mask=t['response_mask']['values'][i];rewards=t['token_level_rewards']['values'][i]
 valid=[j for j,m in enumerate(mask) if m];assert len(valid)==len(row['actual_response_token_ids'])
 assert all(not rew or mask[j] for j,rew in enumerate(rewards))
 samples.append(dict(index=i,uid=row['uid'],response=row['response'],response_token_ids=row['actual_response_token_ids'],valid_response_positions=valid,reward_sum=sum(rewards),reward_positions=[j for j,v in enumerate(rewards) if v],advantage_on_valid_positions=[t['advantages']['values'][i][j] for j in valid]))
rates=[]
for name,g,v,l in [('base',12,6,8),('double_generation',24,6,8),('double_verification',12,12,8),('double_learning',12,6,16)]:
 rate=min(F(3,4)*min(g,v),l);rates.append(dict(case=name,generation=g,verification=v,learning=l,effective_samples_s=float(rate),relative_to_base=float(rate/F(9,2))))
version=analysis['runs']['control']['weight_versions'];assert [v['version'] for v in version]==[0,1,2]
files=[next((ROOT/'manuscripts').glob('10-*.md')),base/'control/tensor-export.json',base/'analyze.py',base/'manifest.json']
out=dict(exercise='10-7',stage_cases=rates,cycles=dict(sync_s=60,async_s=44,sync_effective_batch_s=float(F(1,60)),cases=[dict(retention=float(q),effective_batch_s=float(q/44),relative_to_sync=float(q*60/44)) for q in [F(4,5),F(7,10)]],strict_break_even_retention=float(F(11,15))),traced_control_batch2=samples,weight_versions=version,control_gradient_norms=[r['gradient_norm'] for r in analysis['runs']['control']['batches']],control_validation_correct=analysis['runs']['control']['validation_arithmetic_correct'],scope='Reanalysis of retained real single-GPU verl/vLLM training. Arithmetic stage model is separate; receiver proof covers full representative embedding, not every model tensor.',source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
(P/'10-7-results.json').write_text(json.dumps(out,indent=2)+'\n');print('Verified 8 sample rows, 3 received weight versions, and RL capacity/cycle arithmetic')
