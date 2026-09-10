"""Check section/exercise coverage and recompute teaching answers without a model run."""
from pathlib import Path
import json,re,math
H=Path(__file__).resolve().parent;R=H.parents[1];results=[]
def check(ok,msg):
 results.append({'check':msg,'passed':bool(ok)})
 if not ok:raise AssertionError(msg)
def dump(name,x):(H/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
design=json.loads((H/'section-design.json').read_text());ex=json.loads((H/'exercises.json').read_text())
for ch,count in [(1,8),(2,15),(3,12)]:
 p=next((R/'manuscripts').glob(f'{ch:02d}-*.md'));s=p.read_text()
 heads=re.findall(r'^### (\d+\.\d+\.\d+)',s,re.M)
 check(heads==[d['section'] for d in design if d['section'].startswith(str(ch)+'.')],f'chapter {ch}: section design coverage')
 check(re.findall(r'\*\*练习 '+str(ch)+r'-(\d+)',s)==[str(n) for n in range(1,len(ex[str(ch)])+1)],f'chapter {ch}: exercise order')
 check(re.findall(r'^\*图 '+str(ch)+r'-(\d+)',s,re.M)==[str(n) for n in range(1,count+1)],f'chapter {ch}: figure sequence')
 check(not re.search('[\x00-\x08\x0b-\x1f\t]',s),f'chapter {ch}: no damaged escapes')
 defs=set(re.findall(r'^\[\^([^\]]+)\]:',s,re.M));body=re.sub(r'^\[\^[^\]]+\]:.*$','',s,flags=re.M)
 check(set(re.findall(r'\[\^([^\]]+)\]',body))==defs,f'chapter {ch}: footnotes resolve and are used')
N=8190735360;c=147456;GiB=2**30;MiB=2**20
values={}
values['1-3']=[{'B':b,'batch_ms':1000*max(140e9*b/(.5*989.4e12),70e9/(.7*3.35e12)),'amortized_ms':1000*max(140e9*b/(.5*989.4e12),70e9/(.7*3.35e12))/b,'tokens_per_s':b/max(140e9*b/(.5*989.4e12),70e9/(.7*3.35e12)),'half_read_batch_ms':1000*max(140e9*b/(.5*989.4e12),35e9/(.7*3.35e12))} for b in [1,16,64]]
values['1-3-crossing']=[.5*989.4e12/(2*.7*3.35e12),.5*.5*989.4e12/(2*.7*3.35e12)]
values['1-4']=[{'B':b,'speedup':t/37.31,'TPOT_increase_percent':(p/26.53-1)*100} for b,t,p in [(1,37.31,26.53),(4,141.73,26.97),(16,479.33,29.30),(64,1164.94,40.48)]]
def flops(b,s,p):return [36*385875968*b*p,36*16384*b*(p*s+p*(p+1)//2),2*b*4096*151936]
values['2-2']={'first':flops(4,4096,1024),'second':flops(1,4096,4096),'prefix_saving':1-sum(flops(1,6144,2048))/sum(flops(1,0,8192))}
values['2-3']=[{'G':g,'decode_steps':g-1,'final_GiB':c*(8192+g-1)/GiB,'old_read_GiB':c*((g-1)*8192+(g-1)*(g-2)//2)/GiB} for g in [513,1025]]
values['2-5']=[{'model':name,'crossing':fixed/slope,'32K_MiB':(fixed+32768*slope)/MiB,'128K_MiB':(fixed+131072*slope)/MiB,'256MiB_max_history':max(0,math.floor((256*MiB-fixed)/slope)),'fixed_fits_256MiB':fixed<=256*MiB} for name,fixed,slope in [('Qwen3.6',61.875*MiB,20*1024),('K3',414*MiB+20348928,27*1024)]]
values['2-7']={'qwen_requests':[math.floor((24e9-2*N-2*GiB)/(c*h)) for h in [4096,8192,16384]],'qwen_3GiB_workspace':math.floor((24e9-2*N-3*GiB)/(c*8192)),'70B_requests':[math.floor((48e9-39.5e9-2*GiB)/(x*GiB)) for x in [2.5,10]]}
values['2-8']={'new_KV_MiB':(51+127)*c/MiB,'pairs_full':1443*1444//2,'pairs_cached':51*1392+51*52//2}
values['3-6']={'state_bytes':18*N,'saved_bytes':2*N,'input_tokens':2*4096*8,'supervised_tokens':2*1024*8}
base=2181558727344128;low=3410701494255616;slope=(low-base)//32
values['3-7']={'per_answer_FLOPs':slope,'fixed_update_FLOPs':base-32*slope,'48_answers_FLOPs':base+16*slope,'teacher_FLOPs':634943973621760*3//2,'four_replica_bytes':4*2*N}
values['3-10']={'calendar_days':[1022362/n/24 for n in [2048,1024]],'break_even_tasks':1e6/.002,'small_minus_large_cost':[1e6-q*.002 for q in [2e8,1e9]]}
check(values['2-7']['qwen_requests']==[9,4,2],'capacity integer boundaries')
check(values['3-7']['fixed_update_FLOPs']==952415960432640,'RL linear model recovers fixed update')
check(abs(values['2-5'][0]['crossing']-3168)<1e-9,'hybrid state crossing')
check(sum(flops(1,0,8192))>sum(flops(1,6144,2048)),'prefix reuse reduces matrix work')
dump('exercise-values.json',values);dump('rewrite-validation.json',results)
print(f'{len(results)} structural/numerical checks passed')
