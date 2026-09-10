import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=Path(__file__).absolute().parent;s=json.loads((r/'results/q-control-summary.json').read_text())
fig,ax=plt.subplots(figsize=(8,4),layout='constrained')
for i,name in enumerate(['bf16','fp8','fp8_qbf16']):
 if name=='fp8_qbf16':values=[x['correct'] for x in s['summary']]
 else:
  p=r/'reference'/name;tasks={x['id']:x['expected'] for x in json.loads((p/'inputs.json').read_text())['tasks']};rows=[json.loads(x) for x in (p/'requests.jsonl').read_text().splitlines()];values=[]
  for n in [128,512]:
   for b in [1,4]:
    group=[x for x in rows if x['id'].startswith(('0-n%d-b%d-natural-'%(n,b),'1-n%d-b%d-natural-'%(n,b)))];assert len(group)==8
    def correct(x):
     try:return json.loads(x['text'])==tasks[x['task_id']]
     except ValueError:return False
    values.append(sum(correct(x) for x in group))
 ax.bar([j+(i-1)*.25 for j in range(4)],values,.25,label={'bf16':'BF16 KV','fp8':'FP8 KV + Q','fp8_qbf16':'FP8 KV, BF16 Q'}[name])
ax.set_xticks(range(4),['128 / 1','128 / 4','512 / 1','512 / 4']);ax.set_xlabel('Document rows / concurrency');ax.set_ylabel('Exact answers / 8');ax.set_ylim(0,10);ax.legend(ncol=3,fontsize=8);ax.set_title('Identical online FP8 weights and calibrated FP8 KV')
for ext in ['png','svg','pdf']:fig.savefig(r/f'q-control.{ext}',dpi=160)
