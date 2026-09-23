#!/usr/bin/env python3
"""Build original chapter-nine diagrams and a self-contained reading edition."""
from pathlib import Path
from fractions import Fraction
import argparse,base64,hashlib,html,json,re,subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch,Rectangle
import numpy as np
import markdown
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--font');args=parser.parse_args()
import sys
sys.path.insert(0,str(HERE.parent))
from figure_style.typography import configure_font
font,family=configure_font(args.font)
plt.rcParams.update({'font.family':[family,'DejaVu Sans'],'font.size':11,'axes.unicode_minus':False,'svg.fonttype':'path','svg.hashsalt':'ch09-v1','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white','savefig.facecolor':'white','text.color':'#243c48','axes.labelcolor':'#243c48','pdf.fonttype':42})
C={'ink':'#243c48','blue':'#286b98','teal':'#16857b','orange':'#b87530','red':'#a95159','pale':'#edf4f7','green':'#eaf5f0','sand':'#fcf1e5','line':'#bcced4','muted':'#536b78'}
outputs=[];data={};layout=[]
for source in json.loads((HERE/'sources.json').read_text())['sources']:
 p=ROOT/source['path']
 if hashlib.sha256(p.read_bytes()).hexdigest()!=source['sha256']:raise SystemExit('Source changed; review before rebuilding: '+str(p))
def calc(name):return json.loads((ROOT/'calculations/results'/f'{name}.json').read_text())
def num(v):return float(Fraction(str(v)))
def canvas(h=7):
 f,a=plt.subplots(figsize=(12,h));f.subplots_adjust(left=.035,right=.965,bottom=.05,top=.96);a.set(xlim=(0,1),ylim=(0,1));a.axis('off');return f,a
def box(a,x,y,w,h,title,body='',col='pale',fs=12):
 a.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.004,rounding_size=.01',ec=C['line'],fc=C[col]))
 a.text(x+w/2,y+h*(.68 if body else .5),title,ha='center',va='center',fontsize=fs,weight='bold')
 if body:a.text(x+w/2,y+h*.25,body,ha='center',va='center',fontsize=10,color=C['muted'],linespacing=1.5)
def arrow(a,p,q,col='teal',rad=0,style='-'):
 a.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=13,lw=1.5,color=C[col],connectionstyle=f'arc3,rad={rad}',linestyle=style))
def label(a,x,y,t,fs=13):a.text(x,y,t,fontsize=fs,weight='bold',va='top')
def save(f,name):
 f.canvas.draw();renderer=f.canvas.get_renderer()
 for t in f.findobj(matplotlib.text.Text):
  if not t.get_visible() or not t.get_text():continue
  b=t.get_window_extent(renderer)
  if b.x0<0 or b.y0<0 or b.x1>f.bbox.width or b.y1>f.bbox.height:layout.append({'figure':name,'text':t.get_text()})
 for ext in ['svg','png','pdf']:
  p=HERE/f'{name}.{ext}';f.savefig(p,dpi=180,bbox_inches='tight',pad_inches=.17);outputs.append(p)
 plt.close(f)
# The same service can be organized across hardware in different ways.
f,a=canvas(8)
label(a,.025,.96,"多卡協作：一個實例共同處理一批請求")
label(a,.53,.96,"完整副本：分別接收獨立請求")
box(a,.025,.59,.44,.27,"統一排程與完整模型","八張卡協作執行",col='pale')
for i in range(8):
 x=.045+(i%4)*.10;y=.61+(i//4)*.06
 a.add_patch(Rectangle((x,y),.075,.035,fc=C['blue']))
for x in [.54,.78]:
 box(a,x,.62,.19,.19,"完整副本","權重、KV、排程",col='green',fs=12)
 a.text(x+.095,.88,"請求",ha='center',fontsize=11);arrow(a,(x+.095,.85),(x+.095,.815))
label(a,.025,.49,"PD：按生成階段分工")
box(a,.025,.16,.18,.18,"P 服務池","處理輸入",col='pale')
box(a,.29,.16,.18,.18,"D 服務池","逐步生成",col='green')
arrow(a,(.21,.25),(.285,.25));a.text(.245,.36,"上下文 KV",ha='center',fontsize=11)
label(a,.53,.49,"AF：按層內運算子分工")
box(a,.54,.16,.19,.18,'Attention',"注意力計算",col='pale')
box(a,.79,.16,.19,.18,"FFN／專家","前饋計算",col='green')
arrow(a,(.735,.29),(.785,.29));arrow(a,(.785,.20),(.735,.20))
a.text(.76,.37,"活化值往返",ha='center',fontsize=11)
a.text(.035,.06,"不同階段可分別排隊、組成批次",fontsize=11)
a.text(.54,.06,"同一請求每層都經過兩側計算",fontsize=11)
save(f,'figure-9-1-organization')
data['9-1']={'type':'organization_schematic','organizations':['cooperative_instance','complete_replicas','PD','AF']}
# State lifetime follows one request; stage widths are schematic.
f,a=canvas(6)
stages=['P','D',"工具等待","下一輪 P"];edges=[.19,.37,.56,.78,.96]
for j,title in enumerate(stages):
 a.text((edges[j]+edges[j+1])/2,.92,title,ha='center',fontsize=13,weight='bold')
 a.axvline(edges[j],ymin=.12,ymax=.84,color=C['line'],lw=.8)
rows=[("權重",.72,.19,.96,'blue'),("輸入 KV",.54,.23,.96,'orange'),("生成 KV",.36,.40,.96,'orange'),("EC（可選）",.18,.19,.96,'teal')]
for title,y,x0,x1,col in rows:
 a.text(.025,y,title,va='center',fontsize=12)
 a.add_patch(Rectangle((x0,y-.035),x1-x0,.07,color=C[col],alpha=.82))
a.add_patch(Rectangle((.56,.11),.22,.72,fc=C['pale'],alpha=.5,zorder=0))
a.text(.67,.045,"計算可暫停，狀態仍駐留",ha='center',fontsize=12)
save(f,'figure-9-2-state');data['9-2']={'type':'schematic_state_lifetime','stages':stages,'retention':'all shown states retained through tool wait; optional EC reuse'}

# PD pool: exact frozen enumeration over four A100 and four H20 with stage rates derived from datasheet peaks.
z=calc('pd-pool-book');f,ax=plt.subplots(figsize=(9,7));f.subplots_adjust(left=.15,right=.80,bottom=.14,top=.93);grid=np.zeros((5,5))
rows=z['pool_assignments'];data['9-3']={'type':'frozen_calculation','source':'pd-pool-book','assignments':rows}
rates={d['device']:d for d in z['derived_stage_rates']}
pA=1/num(rates['a100-80gb-sxm']['prefill']['seconds_exact']);dA=1/num(rates['a100-80gb-sxm']['decode']['seconds_per_request_exact'])
pH=1/num(rates['h20-sxm5-96gb']['prefill']['seconds_exact']);dH=1/num(rates['h20-sxm5-96gb']['decode']['seconds_per_request_exact'])
data['9-3']['per_card_rates']={'A100':{'prefill':pA,'decode':dA},'H20':{'prefill':pH,'decode':dH}}
for row in rows:
 pa=row['prefill_workers']['A100'];ph=row['prefill_workers']['H20']
 grid[ph,pa]=num(row['bound_requests_per_second_exact'])
 assert abs(grid[ph,pa]-min(pa*pA+ph*pH,(4-pa)*dA+(4-ph)*dH,25e9/1207959552))<1e-9
im=ax.imshow(grid,origin='lower',cmap='YlGnBu',vmin=0,vmax=7)
for j in range(5):
 for i in range(5):ax.text(i,j,f'{grid[j,i]:.2f}',ha='center',va='center',color='white' if grid[j,i]>3.5 else C['ink'],fontsize=12)
ax.add_patch(plt.Rectangle((3.52,-.48),.96,.96,fill=False,edgecolor=C['orange'],lw=3))
ax.set(xticks=range(5),yticks=range(5),xlabel="分給 P 的 A100 數",ylabel="分給 P 的 H20 數")
cax=f.add_axes([.84,.15,.025,.73]);f.colorbar(im,cax=cax).set_label("請求率上界 / 請求·s⁻¹")
save(f,'figure-9-3-pd')
# Local CPU/GPU execution.
f,a=canvas(8)
label(a,.025,.96,"權重交接：GPU 執行專家")
box(a,.03,.70,.25,.14,'CPU DRAM',"專家權重",col='sand');box(a,.39,.70,.24,.14,"GPU 權重緩衝","等待載荷就緒");box(a,.75,.70,.22,.14,"GPU 專家計算","輸出活化值",col='green');arrow(a,(.285,.77),(.38,.77),'orange');arrow(a,(.635,.77),(.74,.77));a.text(.335,.86,'W',ha='center',color=C['orange'])
label(a,.025,.56,"活化值交接：CPU 就地計算專家")
box(a,.03,.30,.25,.15,'GPU attention',"輸入活化值 X");box(a,.39,.30,.24,.15,"CPU 專家計算","本地讀取權重",col='sand');box(a,.75,.30,.22,.15,"同步合併","繼續下一層",col='green');arrow(a,(.285,.375),(.38,.375));arrow(a,(.635,.375),(.74,.375));a.text(.335,.465,'X',ha='center',color=C['teal']);a.text(.69,.465,'Y',ha='center',color=C['teal'])
box(a,.39,.04,.24,.14,"GPU 常駐專家","可執行獨立分支");arrow(a,(.17,.295),(.385,.11),rad=.15);arrow(a,(.635,.11),(.86,.295),rad=.15)
save(f,'figure-9-5-local');data['9-5']={'type':'conceptual','weight_payload_MiB_per_expert':36,'activation_roundtrip_bytes_per_assignment':16384}
# The same payload isolates the amplification of startup latency.
z=calc('pd-af-handoff-qwen8');f,ax=plt.subplots(figsize=(11,6));f.subplots_adjust(left=.11,right=.96,bottom=.16,top=.92)
alpha=np.linspace(0,20,101);base=1207959552/25e9*1000
for messages,col in [(1,'blue'),(72,'orange')]:ax.plot(alpha,base+messages*alpha/1000,color=C[col],lw=2.3,label=f'{messages} 次訊息')
ax.set(xlabel="每次啟動與同步 / μs",ylabel="依序交接時間 / ms",xlim=(0,20),ylim=(48.2,50),xticks=[0,5,10,15,20])
ax.annotate("差值約 0.36 ms",xy=(5,base+.360),xytext=(7,49.0),arrowprops={'arrowstyle':'->','color':C['muted']},fontsize=12)
ax.legend(frameon=False);ax.grid(alpha=.15)
save(f,'figure-9-8-handoff');data['9-8']={'type':'same_payload_startup_sensitivity','summary':z['summary'],'startup_us':alpha.tolist(),'one_message_ms':(base+alpha/1000).tolist(),'many_messages_ms':(base+72*alpha/1000).tolist(),'same_payload_ms':[base+.005,base+.360]}
# One PD snapshot versus one AF decode step: GQA and compact MLA states, frozen results at 25 and 50 GB/s.
mla={k:calc(n) for k,n in [('gqa25','pd-af-handoff-qwen8'),('mla25','pd-af-handoff-qwen8-mla'),('gqa50','pd-af-handoff-qwen8-50gbps'),('mla50','pd-af-handoff-qwen8-mla-50gbps')]}
assert mla['mla25']['summary']['kv_bytes_per_token']==70272 and mla['mla25']['summary']['pd_snapshot_bytes']==575668224 and mla['mla25']['mla_compact_path']['extra_flops_per_step']==2046820352
for k,bw in [('gqa25',25e9),('mla25',25e9),('gqa50',50e9),('mla50',50e9)]:
 sm=mla[k]['summary'];assert sm['af_total_bytes']==589824;assert abs(num(sm['equal_time_startup_ns_exact'])-(sm['pd_snapshot_bytes']-589824)/(71*bw)*1e9)<1e-3
alpha=np.linspace(0,800,161)
data['9-mla-handoff']={'type':'frozen_calculation','sources':['pd-af-handoff-qwen8','pd-af-handoff-qwen8-mla','pd-af-handoff-qwen8-50gbps','pd-af-handoff-qwen8-mla-50gbps'],'network_bytes_per_second':25e9,'startup_us':alpha.tolist(),'pd_gqa_ms':(1207959552/25e9*1e3+alpha/1e3).tolist(),'pd_mla_ms':(575668224/25e9*1e3+alpha/1e3).tolist(),'af_step_ms':(589824/25e9*1e3+72*alpha/1e3).tolist(),'equal_time_startup_us':{k:num(v['summary']['equal_time_startup_ns_exact'])/1e3 for k,v in mla.items()},'kv_bytes_per_token':{'gqa':147456,'mla':70272},'mla_extra_flops_per_step':2046820352}

# Expert reuse on the KTransformers paper machine: one Xeon 8452Y socket (AVX-512 1.8, AMX 21.3 TFLOP/s, 220 GB/s), A100 40GB PCIe at 50% of peak.
m=np.arange(1,1025);W=37748736;tasks=8*m
def cpu_path(C):return (16*5e-6+tasks*16384/25e9+np.maximum(tasks*37748736/C,8*W/220e9))*1e3
cpu=cpu_path(1.8e12);amx=cpu_path(21.3e12);gpu=(8*5e-6+8*W/25e9+np.maximum(tasks*37748736/156e12,8*W/777.5e9))*1e3
for name,arr,k in [('expert-locality-avx512',cpu,1),('expert-locality-avx512-128',cpu,128),('expert-locality-amx',amx,1),('expert-locality-amx-128',amx,128)]:
 z=calc(name)['summary'];assert abs(arr[k-1]-num(z['cpu_service_ns_exact'])/1e6)<1e-9;assert abs(gpu[k-1]-num(z['weight_copy_service_ns_exact'])/1e6)<1e-9
assert cpu[70]<gpu[70] and cpu[71]>gpu[71] and amx[687]<gpu[687] and amx[688]>gpu[688]
f,ax=plt.subplots(figsize=(12,6));f.subplots_adjust(left=.10,right=.96,bottom=.17,top=.88)
ax.plot(m,cpu,color=C['teal'],lw=2.3,label="CPU 就地計算，AVX-512");ax.plot(m,amx,color=C['blue'],lw=2.3,label="CPU 就地計算，AMX");ax.plot(m,gpu,color=C['orange'],lw=2.3,label="搬一次權重＋GPU 計算")
ax.set_xscale('log',base=2);ax.set(xlabel="每個熱點專家的 token 數",ylabel="八個專家依次執行的時間 / ms",xlim=(1,1024),ylim=(0,30),xticks=[1,4,16,64,256,1024],xticklabels=['1','4','16','64','256','1024']);ax.minorticks_off();ax.legend(frameon=False);ax.grid(alpha=.15)
save(f,'figure-9-6-reuse');data['9-6']={'type':'declared_model','tokens_per_expert':m.tolist(),'cpu_avx512_ms':cpu.tolist(),'cpu_amx_ms':amx.tolist(),'weight_copy_gpu_ms':gpu.tolist(),'crossover_tokens':{'avx512':72,'amx':689},'scenario':calc('expert-locality-avx512')['scenario']}
# Replica preparation is paid once; batch savings accumulate. Same HGX H100 batch, two copy paths.
zr={'nvlink':calc('replica-payback-hgx-h100-nvlink')['summary'],'cx7':calc('replica-payback-hgx-h100-cx7')['summary']};f,ax=plt.subplots(figsize=(10,6));f.subplots_adjust(left=.12,right=.96,bottom=.16,top=.92)
n=np.arange(0,65);delta=num(zr['nvlink']['per_batch_saving_ns_exact'])/1e6;assert zr['cx7']['per_batch_saving_ns_exact']==zr['nvlink']['per_batch_saving_ns_exact']
net={}
for key,col,title,dy in [('nvlink','teal',"同一臺 HGX 內經 NVLink",4),('cx7','orange',"跨伺服器經 ConnectX-7",-4)]:
 setup=num(zr[key]['serialized_copy_setup_ns_exact'])/1e6;k=zr[key]['algebraic_strict_payback_batches'];assert k==int(setup//delta)+1
 net[key]=(n*delta-setup).tolist();ax.plot(n,n*delta-setup,color=C[col],lw=2.3,label=f'{title}：準備 {setup:.2f} ms')
 ax.scatter([k],[k*delta-setup],color=C[col],zorder=3);ax.annotate(f'第 {k} 批迴本',(k,k*delta-setup),xytext=(k+4,k*delta-setup+dy),fontsize=12,arrowprops={'arrowstyle':'->'})
ax.axhline(0,color=C['line']);ax.set(xlabel="熱點持續的批數",ylabel="累計淨節省 / ms",xlim=(0,64),ylim=(-7,17),yticks=[-5,0,5,10,15],xticks=[0,16,32,48,64]);ax.legend(frameon=False,loc='upper left');ax.grid(alpha=.15)
save(f,'figure-9-10-experts');data['9-10']={'type':'replica_payback','sources':['replica-payback-hgx-h100-nvlink','replica-payback-hgx-h100-cx7'],'replica_summary':zr,'batches':n.tolist(),'net_saving_ms':net}

# Page availability, not bytes read, determines usable prefix length.
f,a=canvas(5);z=calc('cache-restart-book')['summary']
for i in range(64):
 row=i//16;col=i%16;x=.08+col*.055;y=.77-row*.17
 a.add_patch(Rectangle((x,y),.047,.095,fc=C['orange'] if i==63 else C['teal'],ec='white'))
 a.text(x+.0235,y+.047,str(i+1),ha='center',va='center',fontsize=10,color='white')
a.text(.50,.965,"讀入 64 頁",ha='center',fontsize=15,weight='bold')
a.text(.10,.11,"前 63 頁：1008 位置可複用",color=C['teal'],fontsize=13)
a.text(.62,.11,"末頁：16 位置仍需處理",color=C['orange'],fontsize=13)
save(f,'figure-9-12-cache');data['9-12']={'type':'observed_usable_prefix_pages','restart_summary':z,'pages_read':64,'pages_reused':63,'page_tokens':16}

# Direct and pooled transfers compare exactly the same state object.
f,a=canvas(7)
box(a,.025,.71,.21,.16,'P',"生成上下文 KV");box(a,.755,.71,.21,.16,'D',"讀取上下文 KV",col='green');arrow(a,(.245,.79),(.745,.79),'orange');a.text(.50,.86,'1.125 GiB',ha='center',color=C['orange'],fontsize=12)
a.text(.025,.96,"直接交接",fontsize=14,weight='bold')
box(a,.025,.36,.21,.16,'P',"生成上下文 KV");box(a,.39,.36,.21,.16,"共享池","儲存後釋出",col='sand');box(a,.755,.36,.21,.16,'D',"讀取上下文 KV",col='green')
for x in [.245,.61]:arrow(a,(x,.44),(x+.135,.44),'orange');a.text(x+.065,.55,'1.125 GiB',ha='center',color=C['orange'],fontsize=11)
a.text(.025,.62,"經池中轉",fontsize=14,weight='bold')
box(a,.755,.055,.21,.14,"後續實例","取回，替代重算",col='green');arrow(a,(.50,.35),(.75,.125),'teal',rad=.12);a.text(.43,.15,"再次複用同一物件",fontsize=12,color=C['teal'])
save(f,'figure-9-16-composition');data['9-16']={'type':'direct_vs_pool_reuse','state_GiB':1.125,'direct_payload_GiB':1.125,'pool_initial_payload_GiB':2.25,'additional_read_GiB':1.125}

# Same startup backlog, different spare service capacities: direct PD, ideal chunked colocation, colocation without chunking.
zb=calc('pd-pool-book');mu_pd=num(zb['summary']['best_pd_bound_requests_per_second_exact']);mu_co=num(zb['summary']['colocated_bound_requests_per_second_exact'])
def overlap_seconds(d):
 comp=num(d['prefill']['compute_seconds_exact'])+1024*num(d['decode']['step_compute_seconds_exact'])/32
 mem=num(d['prefill']['memory_seconds_exact'])+1024*num(d['decode']['step_memory_seconds_exact'])/32
 return max(comp,mem)
mu_ch=sum(4/overlap_seconds(d) for d in zb['derived_stage_rates'])
lam=3.5;f,ax=plt.subplots(figsize=(10,6));f.subplots_adjust(left=.11,right=.96,bottom=.16,top=.92);tt=np.linspace(0,80,801);series={};drain=[]
for mu,col,label in [(mu_pd,'teal',"直接 PD"),(mu_ch,'blue',"理想分塊共置"),(mu_co,'orange',"不分塊共置")]:
 q=np.where(tt<=10,lam*tt,np.maximum(0,lam*10-(mu-lam)*(tt-10)));series[f'{mu:.2f}']=q.tolist();ax.plot(tt,q,label=f'{label}：{mu:.2f} 請求/s',color=C[col],lw=2.3)
 if mu>lam:drain.append(10+lam*10/(mu-lam))
ax.axvline(10,color=C['line'],ls='--');ax.axvline(60,color=C['red'],ls=':');ax.text(11,50,"就緒：積壓 35 請求",fontsize=12);ax.text(61,50,"期限 60 s",fontsize=12,color=C['red'])
ax.set(xlabel="從啟動開始的時間 / s",ylabel="積壓請求數",ylim=(-2,70),xlim=(0,80),xticks=[0,10,20,30,40,50,60,70,80]);ax.legend(frameon=False,fontsize=11);ax.grid(alpha=.15)
save(f,'figure-9-17-service');data['9-17']={'type':'startup_backlog_drain','startup_s':10,'arrival_rps':lam,'time_s':tt.tolist(),'queues':series,'drain_time_from_start_s':drain}

exec(compile((HERE/'extra-figures.py').read_text(), str(HERE/'extra-figures.py'), 'exec'))

(HERE/'figure-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');(HERE/'figure-layout-check.json').write_text(json.dumps({'text_extent_warnings':layout},ensure_ascii=False,indent=2)+'\n')

import sys
sys.path.insert(0,str(HERE.parent))
from teaching_revision import draw as draw_teaching
teaching_outputs,teaching_checks=draw_teaching(HERE,data)
outputs=list(dict.fromkeys(outputs+teaching_outputs))
# UB-EP figures are drawn before the reading edition is assembled so the HTML embeds every active figure.
from ub_ep_figures import draw as draw_ub_ep
outputs += draw_ub_ep(9, HERE)
# Section 9.5.2 multi-tier KV figures read calculations/results/kv-tiers-book.json.
from kv_tier_figures import draw as draw_kv_tiers
outputs += draw_kv_tiers(HERE)
# Render formulas on the build machine; bundle all image/font bytes into HTML.
md=HERE.parent/'09-分布式推理.md';raw=md.read_text();maths=[]
def protect(match):
 text=match[0];display=text.startswith('$$');latex=text[2:-2] if display else text[1:-1];token=f'MATHPLACEHOLDER{len(maths)}END';maths.append({'latex':latex.strip(),'display':display,'token':token});return '\n\n'+token+'\n\n' if display else token
protected=re.sub(r'\$\$[\s\S]*?\$\$|\$[^$\n]+\$',protect,raw)
body=markdown.markdown(protected,extensions=['tables','footnotes','fenced_code','toc'],output_format='html')
node="const fs=require('fs'),k=require(process.argv[1]);const a=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(a.map(x=>k.renderToString(x.latex,{displayMode:x.display,throwOnError:true,output:'htmlAndMathml'}))))"
res=subprocess.run(['node','-e',node,str(HERE.parent/'ch06/vendor/katex/katex.js')],input=json.dumps(maths),text=True,capture_output=True)
if res.returncode:raise SystemExit(res.stderr)
for entry,rendered in zip(maths,json.loads(res.stdout)):
 body=body.replace('<p>'+entry['token']+'</p>',rendered) if entry['display'] else body.replace(entry['token'],rendered)
math_css=(HERE.parent/'ch06/vendor/katex/katex.min.css').read_text()
def font_url(m):
 p=HERE.parent/'ch06/vendor/katex'/m[1];return 'url(data:font/'+p.suffix[1:]+';base64,'+base64.b64encode(p.read_bytes()).decode()+')'
math_css=re.sub(r'url\((fonts/[^)]+)\)',font_url,math_css)
body=re.sub(r'<table>(.*?)</table>',r'<div class="table-scroll"><table>\1</table></div>',body,flags=re.S)
for p in outputs:
 if p.suffix=='.svg':body=body.replace('src="ch09/'+p.name+'"','src="data:image/png;base64,'+base64.b64encode(p.with_suffix('.png').read_bytes()).decode()+'"')
css='''*{box-sizing:border-box}body{margin:0;background:#f7f7f4;color:#243640;font:18px/1.95 Georgia,"Songti SC",serif}main{max-width:1020px;margin:auto;padding:48px 46px 85px;background:#fff}h1,h2,h3{font-family:Arial,"PingFang SC",sans-serif;line-height:1.45;color:#183949}h1{font-size:36px}h2{font-size:28px;border-top:1px solid #d5e1e4;margin-top:65px;padding-top:26px}h3{font-size:23px;margin-top:38px}a{color:#286b98;text-underline-offset:3px;overflow-wrap:anywhere}img{display:block;width:100%;height:auto;margin:28px auto 10px}em{font-size:15px;color:#546e7a}table{border-collapse:collapse;width:100%;font-size:15px;line-height:1.7;margin:22px 0}td,th{padding:10px 12px;border-bottom:1px solid #d5e1e4;text-align:left}th{background:#edf4f6}blockquote{margin:27px 0;padding:14px 24px;border-left:4px solid #16857b;background:#f0f7f4;font-size:16px}code{font:0.85em/1.6 Menlo,monospace;background:#f0f4f6;overflow-wrap:anywhere}pre{overflow-x:auto;padding:16px;max-width:100%}nav{font:16px/1.9 Arial,"PingFang SC",sans-serif;background:#eff5f7;padding:18px 24px}nav a{display:block}.footnote{font-size:14px;line-height:1.8}.footnote li{margin-bottom:13px}.table-scroll{overflow-x:auto;max-width:100%}.katex{font-size:1.04em}.katex-display{overflow-x:auto;overflow-y:hidden;padding:12px 0}@media(max-width:650px){main{padding:24px 18px}body{font-size:17px}h1{font-size:29px}h2{font-size:25px}h3{font-size:21px}}@media print{main{max-width:none;padding:0}h2,h3{break-after:avoid}img,blockquote{break-inside:avoid}body{font-size:11pt}}'''
css+='main{max-width:760px;padding-left:24px;padding-right:24px}img{max-width:720px}@media print{img{width:420pt;max-width:100%}}'
nav=''.join('<a href="#'+ident+'">'+title+'</a>' for ident,title in re.findall(r'<h2 id="([^"]+)">(9\.\d+ [^<]+)</h2>',body))
page="<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>第 9 章 分散式推理</title><style>"+css+math_css+"</style></head><body><main><nav aria-label=\"本章目录\">"+nav+'</nav>'+body+'</main></body></html>'
import sys
sys.path.insert(0,str(HERE.parent))
from teaching_reading import readable_diagrams
from preview_output import preview_path
page=readable_diagrams(page)
hp=preview_path(md);hp.write_text(page)
(HERE/'math-validation.json').write_text(json.dumps({'renderer':'KaTeX 0.16.11','expressions':len(maths),'display_expressions':sum(x['display'] for x in maths),'errors':[]},indent=2)+'\n')
from book_assets import sync_figure_index
active_assets=sync_figure_index(HERE)
artifacts=outputs+[HERE.parent/'ub_ep_figures.py',HERE/'ub-ep-layout-validation.json',ROOT/'calculations/results/ep-skew-book.json',HERE/'teaching_revision.py',HERE/'figure-index.json',HERE/'teaching-layout-validation.json',HERE/'figure-data.json',hp,md]+active_assets
(HERE/'manifest.json').write_text(json.dumps({'chapter':9,'generator':'manuscripts/ch09/build.py','figures':len(teaching_checks),'font_family':family,'outputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in artifacts if not (p.parent==ROOT/'manuscripts' and p.suffix=='.md' and p.name[:2].isdigit())]},ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(outputs)} image files, {len(maths)} formulas, offline HTML; {len(layout)} extent warnings.')
