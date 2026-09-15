"""6ND capacity arithmetic plus throughput of a resumed public log segment."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,tempfile,subprocess,math
P=Path(__file__).resolve().parent;ROOT=P.parents[2];sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.topics.dense_training_scale import calculate
results={};checks=[];files=[next((ROOT/'manuscripts').glob('10-*.md')),ROOT/'calculations/src/infra_calc/topics/dense_training_scale.py']
for rule in ['fixed','proportional']:
 r=calculate(data_rule=rule,efficiencies=['2/5','1/2']);results[rule]=r
 for row in r['dense_scale_rows']:
  speed=F(str(row['peak_bf16_fp32_dense_tflops']))*10**12*F(row['efficiency_exact']);work=row['algorithm_flops']
  for q in row['deadline_requirements']:
   n=q['compute_card_count'];budget=q['deadline_days']*86400
   assert (n-1)*speed*budget<work<=n*speed*budget
   checks.append(dict(rule=rule,N=row['parameters'],device=row['device'],MFU=row['efficiency_exact'],deadline_days=q['deadline_days'],compute_cards=n,necessary_cards=q['necessary_card_count'],actual_compute_days=float(F(work)/(n*speed*86400)),GPU_hours_to_finish=float(F(work)/(speed*3600)),GPU_hours_reserved_full_deadline=n*q['deadline_days']*24))
 for src in r['sources']:
  f=ROOT/'calculations'/src['file']
  if f.exists():files.append(f)
base=ROOT/'experiments/ch10/10-10/public-training'
with tempfile.TemporaryDirectory(prefix='book-public-log-') as tmp:
 subprocess.run([sys.executable,str(base/'analyze.py'),tmp],check=True,capture_output=True)
 audit=json.loads((Path(tmp)/'analysis.json').read_text())
run=next(r for r in audit['runs'] if r['name']=='n4jn9hla');segment=audit['final_console'];start=segment['first_step']-1;end=segment['last_step'];tokens_per_step=run['tokens_per_step'];delta=(end-start)*tokens_per_step
assert delta==segment['tokens_in_this_segment'] and end*tokens_per_step==run['final_global_consumed_tokens']
files += [base/'analyze.py',base/'results/analysis.json',base/'final-run/output.log']
public=dict(run='n4jn9hla',restored_step=start,final_step=end,steps=end-start,tokens_per_step=tokens_per_step,start_tokens=start*tokens_per_step,final_tokens=end*tokens_per_step,new_tokens=delta,reported_runtime_s=run['reported_runtime_seconds'],observed_new_tokens_per_s=delta/run['reported_runtime_seconds'],configured_ranks=run['configured_ranks'],scope='Average over reported run runtime, includes its reported overheads; not steady-state kernel throughput or full-job hardware calibration.')
out=dict(exercise='10-10',models=results,deadline_rows=checks,public_segment=public,source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
(P/'10-10-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(public,indent=2));print('verified deadline cases',len(checks))
