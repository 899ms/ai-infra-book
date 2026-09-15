import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;P=R.parent;s=json.loads((R/'results.json').read_text())
fig,ax=plt.subplots(2,1,figsize=(11,7.6),gridspec_kw={'height_ratios':[1.4,1]})
chosen=[next(x for x in s['arrangements'] if x['arrangement']==p and (x['rep']==1 if p!='preserve' else x['cut']==32)) for p in ['fixed','additional','preserve']]
for i,x in enumerate(chosen):
 prep=json.loads((P/('training-consumption' if x['arrangement']=='preserve' else 'canonical-training')/'summary.json').read_text())['preparation_s']
 ax[0].barh(i,x['generation_s'],color='#3579a8',label='Generation / receipt' if i==0 else None)
 ax[0].barh(i,prep,left=x['generation_s'],color='#d79d42',label='Consumer weight/model preparation' if i==0 else None)
 step=x['composed_training_s']-prep;ax[0].barh(i,step,left=x['generation_s']+prep,color='#38845d',label='Optimizer + durable checkpoints' if i==0 else None)
 ax[0].text(x['composed_total_s']+1,i,f'{x["composed_total_s"]:.2f}s',va='center',fontsize=9)
ax[0].set_yticks(range(3),['Fixed Mac (rep1)','Mac + RTX (rep1)','Preserve on Mac (K32)']);ax[0].invert_yaxis();ax[0].set_xlim(0,132);ax[0].set_xlabel('Composed stage seconds — not a live end-to-end clock');ax[0].legend(loc='lower right',fontsize=8);ax[0].set_title('Same two canonical samples: 500 trained output positions',loc='left')
d=P/'formal/sequence-k32-preserve';ex=json.loads((d/'execution.json').read_text());origin=ex[0]['start']
colors={'prompt_prefill':'#8560a6','prefix_rebuild':'#cf6d44','decode':'#3579a8'};used=set()
for i,row in enumerate(ex):
 ax[1].barh(i,row['end']-row['start'],left=row['start']-origin,color='#dedede')
 env=json.loads((d/f'attempt-{i}/environment.json').read_text());ax[1].barh(i,env['load_end']-env['load_start'],left=env['load_start']-origin,color='#d79d42',label='Weight/model load' if i==0 else None)
 for line in (d/f'attempt-{i}/calls.jsonl').read_text().splitlines():
  c=json.loads(line);k=c['kind'];ax[1].barh(i,c['end']-c['start'],left=c['start']-origin,color=colors[k],label=k if k not in used else None);used.add(k)
 if row['killed']:
  x=row['killed']-origin;ax[1].axvline(x,color='#b22b32',linestyle='--');ax[1].text(x+.1,.48,'SIGKILL after commit32, before ACK',fontsize=8,color='#b22b32')
ax[1].set_yticks([0,1],['Original worker','Recovery worker']);ax[1].invert_yaxis();ax[1].set_xlabel('Actual Mac monotonic seconds from first worker start');ax[1].set_title('Recorded prefix-preservation path: sequence / K32',loc='left');ax[1].legend(loc='upper center',bbox_to_anchor=(.5,-.25),fontsize=8,ncol=4)
for a in ax:a.spines[['top','right']].set_visible(False);a.grid(axis='x',alpha=.18);a.set_axisbelow(True)
fig.tight_layout();fig.savefig(R/'timeline.svg');fig.savefig(R/'timeline.png',dpi=150);plt.close(fig)
