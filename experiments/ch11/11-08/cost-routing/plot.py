import json,statistics,hashlib
from fractions import Fraction
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;root=R.parents[3];s=json.loads((R/'results.json').read_text());book=root/'calculations/results/routing-cost-book.json';b=json.loads(book.read_text());f=lambda x:float(Fraction(x))
fig,axes=plt.subplots(2,2,figsize=(12,8.8));a=axes[0,0]
recipes=[('8B',False,1000,'8B no-think'),('8B',True,100,'8B cap100'),('8B',True,1000,'8B cap1000'),('8B',True,4096,'8B cap4096'),('MoE',False,1000,'MoE one-shot'),('MoE_feedback',False,1000,'MoE feedback')]
for model,thinking,cap,label in recipes:
 rows=[r for r in s['records'] if r['model']==model and r['thinking']==thinking and r['budget']==cap and not r['warm'] and not r['busy']]
 a.scatter(statistics.median(r['total_s'] for r in rows),statistics.median(r['attempt_cost'] for r in rows)*1e3,label=label,marker='x',s=55)
a.set(title='Measured candidates: all fail the same quality gate',xlabel='Target + validation seconds (median)',ylabel='Teaching attempt cost (milli-units)');a.legend(fontsize=8,ncol=2);a.text(.03,.95,'Success cost: undefined',transform=a.transAxes,va='top',fontsize=9)
a=axes[0,1];rows=[]
for cap in [100,1000,4096]:
 r=[r for r in s['records'] if r['model']=='8B' and r['thinking'] and r['budget']==cap and not r['warm'] and not r['busy']];x=statistics.median(z['reasoning_tokens'] for z in r);y=statistics.median(z['total_s'] for z in r);a.scatter(x,y,color='#3579a8');a.annotate(f'total cap {cap}',(x,y),xytext=(5,-15 if cap==4096 else 7),textcoords='offset points',fontsize=8)
a.set(title='Actual reasoning count and observed completion',xlabel='Tokens before thinking close / truncation',ylabel='Target + validation seconds');a.text(.03,.95,'Two repeats per setting; no passing result',transform=a.transAxes,va='top',fontsize=8)
a=axes[1,0];labels=[];idle=[];warm=[];queue=[]
for model in ['8B','MoE','MoE_feedback']:
 r=[x for x in s['records'] if x['model']==model and not x['thinking']];idle.append(statistics.median(x['total_s'] for x in r if not x['warm'] and not x['busy']));w=[x for x in r if x['warm'] and x['busy']];warm.append(statistics.median(x['total_s'] for x in w));queue.append(statistics.median(x['queue_s'] for x in w));labels.append(model.replace('_','\n'))
x=np.arange(3);a.bar(x-.2,idle,.4,label='Cold idle total',color='#3579a8');a.bar(x+.2,warm,.4,label='Warm busy total',color='#d39b45');a.scatter(x+.2,queue,color='#222',marker='_',s=120,label='Native initial queue');a.set_xticks(x,labels);a.set(title='Cache hits do not remove queueing',ylabel='Seconds (median)');a.legend(fontsize=8)
a=axes[1,1];a.set_facecolor('#f5f2e9');A,B=b['routing_cost_rows'];h=np.linspace(0,1,201);ca=f(A['cost_per_quality_success_exact']);cb=(h*f(B['hit_attempt_cost_exact'])+(1-h)*f(B['miss_attempt_cost_exact']))/(f(B['expected_quality_successes_exact'])/b['scenario']['tasks']);cross=f(b['summary']['cost_crossover_b_hit_fraction_exact']);deadline=f(b['summary']['minimum_b_hit_for_joint_target_exact']);a.plot(h*100,[ca]*len(h),label='Assumed A');a.plot(h*100,cb,label='Assumed B');a.axvline(cross*100,color='#666',linestyle='--');a.axvspan(deadline*100,100,color='#83b78a',alpha=.35,label='B meets joint deadline target');a.annotate(f'Cost crossing {cross:.2%}',(cross*100,ca),xytext=(10,.032),arrowprops=dict(arrowstyle='->'),fontsize=8);a.set(title='Separate book assumptions: cost and deadline',xlabel='B request cache-hit percentage',ylabel='Assumed cost per successful task');a.legend(fontsize=7,loc='upper right');a.text(.03,.05,f'6s deadline + 90% joint target: hit ≥ {deadline:.2%}',transform=a.transAxes,fontsize=8)
for a in axes.flat:a.grid(alpha=.16);a.set_axisbelow(True);a.spines[['top','right']].set_visible(False)
fig.tight_layout();fig.savefig(R/'comparison.svg');fig.savefig(R/'comparison.pdf');fig.savefig(R/'comparison.png',dpi=150);plt.close(fig)
(R/'plot-sources.json').write_text(json.dumps({str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [book,R/'results.json',R/'plot.py']},indent=2)+'\n')
