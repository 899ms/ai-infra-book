"""Current chapter 3 exercise arithmetic and pinned six/two C4 refit."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys
R=Path(__file__).resolve().parent
ROOT=R.parents[2]
sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.topics import scaling_law
from infra_calc.topics.real_scaling_fit import GRID
P=8190735360
out={}
out['3-1']=[dict(requests=n,output_each=g,prefill_calls=n,decode_calls=n*(g-1),final_context=1024+g,prefill_weight_rounds=1,decode_weight_rounds=g-1,total_weight_rounds=g) for n,g in [(1,1024),(8,128)]]
q=[]
for cards in [2,3]:
    rate=2796*cards;growth=max(F('7471.2')-rate,0);backlog=growth*30
    q.append(dict(cards=cards,service_rate=rate,backlog_growth=growth,backlog_30=backlog,drain_s=backlog/rate))
out['3-2']=dict(queue=q,tool_wait=[dict(wait_s=w,tasks=2*w,state_GiB=2*w) for w in [10,30]])
out['3-3']=dict(old_cost=F(1)/F('.5'),new_cost=F(2)/F('.8'),minimum_success=F('1.5')/(F(1)/F('.5')))
total=F('76.510');model=F('36.375');tool=F('.078')
out['3-4']=dict(sequential_s=2+6+10+3,parallel_s=2+max(6,10)+3,sequential_GiB_s=16,parallel_GiB_s=10,
    first_model_speedup=dict(saved_s=model*(1-F(1,4)),total_s=total-model+model/4),tool_speedup=dict(saved_s=tool/2,total_s=total-tool/2))
audio=[]
arrivals=[20*(i+1)+12+1+(50 if i==2 else 5) for i in range(8)]
for delay in [40,60]:
    clock=arrivals[0]+delay;rows=[]
    for i,arrived in enumerate(arrivals):
        start=max(clock,arrived);rows.append(dict(block=i+1,arrival_ms=arrived,start_ms=start,stall_ms=start-clock));clock=start+20
    audio.append(dict(buffer_ms=delay,first_play_ms=rows[0]['start_ms'],stall_ms=sum(r['stall_ms'] for r in rows),blocks=rows))
out['3-5']=dict(vision_tokens=1280**2//16**2//2**2,EC_bytes=1600*10240*2,KV_bytes=1600*144*1024,
    audio=audio,continuous_buffer_empty_s=F('.3')/(1-F('.9')))
out['3-6']=dict(parameters=P,state_18_bytes=18*P,state_16_bytes=16*P,saved_bytes=2*P,input_tokens=2*4096*8,supervised_tokens=2*1024*8,
    full_vocab_rows=2*4096*8,selected_vocab_rows=2*1024*8)
a,b=F('2181.559'),F('3410.701');slope=(b-a)/32;fixed=a-32*slope
out['3-7']=dict(precision='uses rounded manuscript TFLOP inputs; inferred intercept differs by 0.001 TFLOP from rounded stage table',extra_per_answer_TF=slope,fixed_update_TF=fixed,
    total_48_TF=fixed+48*slope,teacher_48_TF=F('634.944')*48/32,weight_four_bytes=2*P*4)
fit_path=ROOT/'calculations/results/datablations-real-c4-eight-point-fit.json'
old=json.loads(fit_path.read_text());fit=scaling_law.fit(old['records'],GRID,1e9,1e10)
assert fit['law']==old['primary']['result']['law']
# Deliberately change held-out losses: fitting must remain unchanged.
perturbed=[dict(r,loss=r['loss']+10) if r['split']=='holdout' else r for r in old['records']]
assert scaling_law.fit(perturbed,GRID,1e9,1e10)['law']==fit['law']
out['3-8']=dict(law=fit['law'],grid=GRID,fit_sse=fit['fit_sse'],holdout_rmse=fit['holdout_rmse'],
    predictions=[{k:r[k] for k in ['id','N','D','split','loss','predicted_loss','residual']} for r in fit['predictions']],
    holdout_excluded_from_fit_verified=True,equal_exponents=[dict(budget_factor=c,N_factor=n,D_factor=n) for c,n in [(4,2),(9,3)]])
history=[('Llama 1',6700000000,10**12),('Llama 2',7*10**9,2*10**12),('Llama 3.1',8*10**9,15*10**12),('Qwen2.5',7*10**9,18*10**12),('Qwen3',8*10**9,36*10**12)]
out['3-9']=[dict(model=m,N=n,D=d,D_per_N=F(d,n),flops=6*n*d,four_D_flops=24*n*d,weight_capacity_factor=1) for m,n,d in history]
out['3-10']=dict(training_days=[dict(cards=n,days=F(1022362,n*24)) for n in [2048,1024]],
    break_even_successes=F(100000*3600)/F('.72'),cost_differences=[dict(successes=n,small_minus_large_H100_hours=100000-F(n)*F('.72')/3600) for n in [200000000,1000000000]])
def encode(x):
    if isinstance(x,F):return dict(exact=str(x),value=float(x))
    raise TypeError(type(x))
inputs=['manuscripts/03-推理与训练负载.md',str(fit_path.relative_to(ROOT)),
    'calculations/src/infra_calc/topics/scaling_law.py','calculations/src/infra_calc/topics/real_scaling_fit.py']
result=dict(exercises=out,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs})
(R/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=encode)+'\n')
print(json.dumps(out,ensure_ascii=False,default=encode,indent=2))
