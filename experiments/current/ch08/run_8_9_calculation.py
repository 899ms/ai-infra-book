"""Exercise 8-9 rounded-input design comparison; live replay separately pending."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('08-*.md'));rows=[]
for budget,outputs in ((12288,256),(6144,256),(12288,16)):
 private=((2048+outputs-1+15)//16)*16*144/1024
 shared=864+16*private
 for name,extra,prefill,rounds,step in [('B',0,F('2.04'),outputs-1,F('.02735')),('D',3188,F('2.23'),(outputs-1+2)//3,F('.02735')),('E',0,F('2.04'),(outputs-1+1)//2,F('.02745'))]:
  memory=shared+extra;t=prefill+rounds*step;fit=memory<=budget;good=16 if fit and t<=7 else 0
  rows.append(dict(KV_and_aux_budget_MiB=budget,output_tokens=outputs,configuration=name,KV_and_aux_MiB=memory,KV_and_aux_GiB=memory/1024,rounds=rounds,total_seconds=float(t),fits=fit,qualified_results_assuming_all_correct=good,GPU_seconds_per_qualified_result=float(t/16) if good else None,effective_requests_per_s=float(16/t) if good else 0))
assert next(r for r in rows if r['configuration']=='E')['total_seconds']==5.5536
out=dict(exercise='8-9',status='calculation_complete_open_replay_completed_see_service_comparison',rows=rows,scope='Rounded book inputs 2.04/2.23s, 27.35ms, lookup 0.1ms; all-correct conditional assumption; separate memory reduction and output reduction; no extra GPU index memory',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'8-9-calculation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
