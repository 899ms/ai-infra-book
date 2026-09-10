#!/usr/bin/env python3
"""Generate chapter-ten vector figures, data, and an offline reading edition."""
from pathlib import Path
from fractions import Fraction
import argparse, base64, hashlib, html, json, re, subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np
import markdown
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--font');args=parser.parse_args()
font=next((Path(p) for p in [args.font,'/System/Library/Fonts/Supplemental/Arial Unicode.ttf','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'] if p and Path(p).exists()),None)
if font is None:raise SystemExit('Install a CJK font or pass --font')
font_manager.fontManager.addfont(str(font));family=font_manager.FontProperties(fname=str(font)).get_name()
plt.rcParams.update({'font.family':family,'font.size':11,'axes.unicode_minus':False,'svg.fonttype':'none','svg.hashsalt':'ch10-training-v1','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white','savefig.facecolor':'white','text.color':'#203c48','axes.labelcolor':'#203c48','pdf.fonttype':42})
C={'ink':'#203c48','blue':'#286b98','teal':'#16857b','orange':'#bc722b','red':'#a94c52','pale':'#eef4f7','light':'#eaf5f1','sand':'#fbf0e5','line':'#c3d0d7','muted':'#546e7a'}
for x in json.loads((HERE/'sources.json').read_text())['sources']:
 if hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()!=x['sha256']:raise SystemExit('Review changed source: '+x['path'])
def read(p):return json.loads((ROOT/p).read_text())
def calc(name):return read('calculations/results/'+name+'.json')
outputs=[];data={};layout=[]
def save(f,name):
 f.canvas.draw();renderer=f.canvas.get_renderer()
 for t in f.findobj(matplotlib.text.Text):
  if not t.get_visible() or not t.get_text():continue
  # Tick labels outside active limits are not painted by Matplotlib.
  if getattr(t,'axes',None) and not t.axes.get_visible():continue
  b=t.get_window_extent(renderer)
  if b.x0<0 or b.y0<0 or b.x1>f.bbox.width or b.y1>f.bbox.height:
   layout.append({'figure':name,'text':t.get_text(),'bbox':[round(v,2) for v in b.bounds]})
 for ext in ['svg','png','pdf']:
  p=HERE/(name+'.'+ext);f.savefig(p,dpi=180,bbox_inches='tight',pad_inches=.15);outputs.append(p)
 plt.close(f)
def canvas(height=8):
 f,a=plt.subplots(figsize=(13,height));f.subplots_adjust(left=.025,right=.975,top=.98,bottom=.035);a.set(xlim=(0,1),ylim=(0,1));a.axis('off');return f,a
def box(a,x,y,w,h,title,body='',col='pale',size=12):
 a.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.004,rounding_size=0.009',ec=C['line'],fc=C[col],lw=1.1))
 a.text(x+w/2,y+h*(.69 if body else .5),title,ha='center',va='center',fontsize=size,weight='bold')
 if body:a.text(x+w/2,y+h*.27,body,ha='center',va='center',fontsize=10,linespacing=1.4,color=C['muted'])
def arrow(a,p,q,col='teal',rad=0,lw=1.5):a.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=13,lw=lw,color=C[col],connectionstyle=f'arc3,rad={rad}'))
def panel(a,x,y,t):a.text(x,y,t,fontsize=14,weight='bold',va='top')
# All figures have their captions in the manuscript, not on the drawing canvas.
state=calc('training-state-book');deadline=calc('training-deadline-book')
N=state['summary']['parameters'];data['source_scope']={'state_parameters':N,'deadline_matrix_flops':deadline['summary']['task_training_matrix_flops']}
# 1. Persistent allocations and two explicit conversion paths.
f,a=canvas(8.5);panel(a,.02,.98,'持久状态：同一模型，不同任务')
ax=f.add_axes([.14,.58,.81,.29]);vals=np.array([[2*N,0,0,0,0],[2*N,2*N,4*N,4*N,4*N]])/1e9;left=np.zeros(2)
for j,(label,col) in enumerate([('BF16 权重','blue'),('BF16 梯度','teal'),('FP32 主权重','orange'),('Adam 一阶矩','red'),('Adam 二阶矩','muted')]):
 ax.barh([1,0],vals[:,j],left=left,height=.45,label=label,color=C[col]);left+=vals[:,j]
for y,v in zip([1,0],left):ax.text(v+1.5,y,f'{v:.3f}',va='center',fontsize=11)
ax.set(yticks=[1,0],yticklabels=['推理权重','训练状态'],xlabel='逻辑容量 / GB',xlim=(0,148),xticks=[0,20,40,60,80,100,120,140],ylim=(-.65,1.65));ax.legend(ncol=3,fontsize=9,frameon=False,loc='upper left')
panel(a,.02,.48,'同一 96 MiB 梯度：转换位置改变传输和暂存')
for y,label,b1,b2,col in [(.285,'CPU 转换','GPU：BF16 梯度','主机：96 MiB → 192 MiB','blue'),(.075,'GPU 转换','GPU：96 MiB → 192 MiB','主机：FP32 梯度','orange')]:
 a.text(.025,y+.055,label,fontsize=11,va='center');box(a,.20,y,.30,.13,b1,'GPU 额外转换缓冲：192 MiB' if col=='orange' else '先传输 BF16',size=11);box(a,.66,y,.31,.13,b2,'转换后供 CPU 优化器消费',size=11)
 arrow(a,(.505,y+.065),(.655,y+.065),col);a.text(.58,y+.105,'96 MiB' if col=='blue' else '192 MiB',ha='center',fontsize=10)
save(f,'figure-10-1-state');data['10-1']={'allocations_bytes':(vals*1e9).astype(int).tolist(),'gradient':calc('gradient-cast-book')['summary']}
# 2. Integer resource lower bounds, all from existing calculation rows.
f,ax=plt.subplots(figsize=(12,6));f.subplots_adjust(bottom=.17,top=.89,left=.09,right=.96)
devs=['rtx4090','a100-80gb-sxm','h100-sxm','b200-sxm'];labels=['RTX 4090','A100 80GB SXM','H100 SXM','B200'];x=np.arange(4);rows=deadline['training_deadline_rows'];series={}
for j,(ef,label,col) in enumerate([('3/10','计算：30%','blue'),('2/5','计算：40%','teal'),('1/2','计算：50%','orange')]):
 ys=[next(r['compute_count_bound'] for r in rows if r['device']==d and r['matrix_work_efficiency_exact']==ef) for d in devs];series[ef]=ys;ax.bar(x+(j-1)*.21,ys,.20,label=label,color=C[col]);
 for xx,yy in zip(x+(j-1)*.21,ys):ax.text(xx,yy+.65,str(yy),ha='center',fontsize=10)
caps=[next(r['persistent_capacity_count_bound'] for r in rows if r['device']==d) for d in devs];ax.scatter(x,caps,marker='D',s=55,facecolors='white',edgecolors=C['red'],linewidths=1.7,label='仅持久状态容量下界',zorder=5)
ax.set(xticks=x,xticklabels=labels,ylabel='必要设备数（向上取整）',ylim=(0,49));ax.legend(ncol=2,frameon=False,loc='upper right',fontsize=11);ax.grid(axis='y',alpha=.18)
f.text(.09,.045,'100B 有效 token · 30 天 · 矩阵工作口径；不保证通信、激活或实际部署可行',fontsize=11)
save(f,'figure-10-2-budget');data['10-2']={'devices':devs,'compute':series,'capacity':caps}
# 3. Capacity feasibility is necessary, not sufficient.
f=plt.figure(figsize=(12,7));ax=f.add_axes([.085,.17,.47,.72]);persist=np.array([r['persistent_bytes_per_rank'] for r in state['training_state_stages']])/2**30
ax.bar(np.arange(4),persist,color=C['blue'],label='持久状态');ax.bar(np.arange(4),[10]*4,bottom=persist,color=C['orange'],label='假定同时存活附加量');ax.axhline(24,color=C['red'],ls='--',label='24 GiB 教学净预算')
for i,v in enumerate(persist+10):ax.text(i,v+2,f'{v:.2f}',ha='center',fontsize=10)
ax.set(xticks=range(4),xticklabels=['普通 DP','ZeRO-1','ZeRO-2','ZeRO-3'],ylabel='每卡存活量 / GiB',ylim=(0,157));ax.legend(frameon=False,fontsize=10,loc='upper right')
a=f.add_axes([.61,.10,.36,.81]);a.set(xlim=(0,1),ylim=(0,1));a.axis('off')
for i,(t,b) in enumerate([('逐卡容量','任一卡超限 → 排除'),('必要通信与物理路径','检查最窄接口及启动次数'),('训练步时间','前向、反向、更新与重叠'),('日历期限','供数、保存、故障与恢复')]):
 y=.78-i*.235;box(a,.05,y,.90,.17,t,b,size=12)
 if i<3:arrow(a,(.5,y-.01),(.5,y-.057))
save(f,'figure-10-3-candidates');data['10-3']={'persistent_gib':persist.tolist(),'extra_live_gib':10,'net_budget_gib':24,'participants':8}
# 4. Real generated event schedules, not invented pipeline rectangles.
f=plt.figure(figsize=(13,11));policies=[('training-pipeline-gpipe-m8','填满排空'),('training-pipeline-1f1b-m8','1F1B')];pipedata={}
for idx,(name,label) in enumerate(policies):
 d=calc(name);ax=f.add_axes([.09,.68-idx*.285,.86,.225]);events=[e for e in d['events'] if e['kind'] in ['F','B','update']]
 for ev in events:
  if ev['stage'] is None:continue
  col={'F':'blue','B':'orange','update':'teal'}[ev['kind']];start=ev['start']*1000;dur=ev['duration']*1000;y=3-ev['stage'];ax.broken_barh([(start,dur)],(y-.30,.6),facecolors=C[col],edgecolors='white',linewidth=.35)
  if dur>=9:ax.text(start+dur/2,y,str(ev['microbatch']+1),ha='center',va='center',fontsize=7,color='white')
 ax.set(yticks=[0,1,2,3],yticklabels=['阶段 3','阶段 2','阶段 1','阶段 0'],xlim=(0,355),xticks=[0,50,100,150,200,250,300,350],ylim=(-.65,3.65),xlabel='时间 / ms');ax.set_title(label+f"：{d['summary']['step_makespan_seconds']*1000:.0f} ms",loc='left',fontsize=13);ax.grid(axis='x',alpha=.15)
 pipedata[label]={'events':events,'summary':d['summary'],'scenario':d['scenario']}
ax=f.add_axes([.09,.09,.57,.205]);x=np.arange(4)
for idx,(_,label) in enumerate(policies):ax.bar(x+(idx-.5)*.34,np.array(pipedata[label]['summary']['reserved_activation_scope_peak_bytes'])/1e9,.32,color=C[['blue','orange'][idx]],label=label)
ax.set(xticks=x,xticklabels=['阶段 0','阶段 1','阶段 2','阶段 3'],ylabel='保存范围峰值 / GB',ylim=(0,3.1));ax.legend(frameon=False,fontsize=10)
f.text(.71,.23,'蓝：前向；橙：反向\n绿：更新（1 ms）\n块内数字：微批编号\n\n8 微批 × 128 token\n每边界传输 1 ms\n前向 10 ms，反向 20 ms',fontsize=11,va='top',linespacing=1.65)
save(f,'figure-10-4-pipeline');data['10-4']=pipedata
# 5. Capture versus durable, followed by the declared first-order loss curve.
f=plt.figure(figsize=(13,10));ax=f.add_axes([.10,.59,.85,.33]);checkpointdata={}
for j,(name,label,col) in enumerate([('checkpoint-async-rounded','8 GB/s','blue'),('checkpoint-async-fast','16 GB/s','teal')]):
 d=calc(name);checkpointdata[label]=d['checkpoint_save_rows']
 for row in d['checkpoint_save_rows']:
  t=row['seconds'];y=3-(j*2+row['snapshot']);ax.broken_barh([(t['capture'],t['staging_end']-t['capture'])],(y-.24,.48),facecolors=C['orange']);ax.broken_barh([(t['upload_start'],t['durable']-t['upload_start'])],(y-.24,.48),facecolors=C[col]);ax.plot(t['durable'],y,'o',color=C['red']);ax.text(t['durable']+.45,y,f"{t['durable']:g}",va='center',fontsize=10)
ax.axvline(50,ls='--',color=C['red']);ax.text(50.5,3.7,'故障：50 s',color=C['red'],fontsize=11)
ax.set(xlim=(18,60),ylim=(-.6,4),yticks=[3,2,1,0],yticklabels=['8 GB/s · 快照 1','8 GB/s · 快照 2','16 GB/s · 快照 1','16 GB/s · 快照 2'],xlabel='时间 / s');ax.grid(axis='x',alpha=.15)
ax=f.add_axes([.10,.11,.52,.34]);d=calc('checkpoint-interval-book')['summary'];c=float(Fraction(d['blocking_save_cost_exact_seconds']));lam=float(Fraction(d['job_failure_rate_exact_per_second']));r=120;tau=np.linspace(100,2400,250);ys=c/tau+lam*tau/2+lam*r
ax.plot(tau,ys*100,color=C['blue'],lw=2,label='总一阶损失');ax.plot(tau,c/tau*100,color=C['orange'],label='保存');ax.plot(tau,lam*tau/2*100,color=C['teal'],label='重做');opt=d['first_order_optimal_useful_interval_seconds'];ax.axvline(opt,ls='--',color=C['muted']);ax.set(xlabel='两次保存间的有用计算 / s',ylabel='每单位有用计算的损失 / %',ylim=(0,17),xlim=(100,2400));ax.legend(frameon=False,fontsize=10)
f.text(.68,.405,'112 GB 教学时间线\n橙色短段：staging 0.5 s\n圆点：完整持久化\n恢复位置取快照捕获时刻',fontsize=11,va='top',linespacing=1.7)
f.text(.68,.215,f'周期模型使用官方载荷\nc = {c:.3f} s，r = 120 s\n作业 MTBF = 30796.875 s\n一阶最优间隔 ≈ {opt:.1f} s',fontsize=11,va='top',linespacing=1.7)
save(f,'figure-10-5-recovery');data['10-5']={'timelines':checkpointdata,'loss':{'c':c,'lambda':lam,'r':r,'tau':tau.tolist(),'loss':ys.tolist(),'optimum':opt}}
# 6. RL stage ownership and co-location peak.
f,a=canvas(8.5);panel(a,.02,.98,'同一批样本从生成进入更新，再交接新权重')
for i,(title,body) in enumerate([('生成','prompt → token\n行为策略版本 v'),('验证与样本组织','奖励、优势、mask\n样本与分组身份'),('学习','微批累积\n一次更新：v → v+1'),('权重交接','装载、版本就绪\n下一轮使用 v+1')]):
 x=.015+i*.25;box(a,x,.67,.22,.20,title,body,size=12)
 if i<3:arrow(a,(x+.225,.77),(x+.245,.77))
arrow(a,(.875,.655),(.125,.655),rad=-.18);a.text(.50,.48,'新权重发布后，检查旧 KV 与在途样本的版本',ha='center',fontsize=11,color=C['teal'])
ax=f.add_axes([.22,.12,.69,.28]);d=calc('weight-handoff-qwen8')['summary'];names=['training','rollout','restore_all_before_release','sync_weights_before_release'];vals=[d['phase_live_bytes'][x]/2**30 for x in names];ax.barh([3,2,1,0],vals,color=[C['blue'],C['teal'],C['red'],C['orange']],height=.53)
for y,v in zip([3,2,1,0],vals):ax.text(v+.7,y,f'{v:.3f}',va='center',fontsize=10)
ax.axvline(64,ls='--',color=C['muted']);ax.text(64.8,3.6,'64 GiB 净预算',fontsize=10);ax.set(yticks=[3,2,1,0],yticklabels=['训练阶段','生成阶段','全部恢复后释放','先交接再释放'],xlabel='声明的驻留峰值 / GiB',xlim=(0,96),ylim=(-.65,4.1))
save(f,'figure-10-6-rl');data['10-6']={'phase_live_bytes':d['phase_live_bytes'],'net_budget_gib':64}
# 7. Distinguish logical discrete routing from current continuous recomputation.
f,a=canvas(9);panel(a,.02,.98,'固定 token 与逻辑专家身份，检查两端执行的一致性')
box(a,.025,.72,.24,.15,'生成端：版本 v','路由分数 → top-k',size=12);box(a,.385,.72,.25,.15,'路由记录','token、层、专家 ID、版本',col='sand',size=12);box(a,.75,.72,.22,.15,'训练端：当前权重','重新计算路由分数',size=12)
arrow(a,(.27,.795),(.38,.795));a.plot([.637,.86],[.79,.55],ls='--',color=C['orange'],lw=2);a.text(.71,.665,'重放离散选择',ha='center',fontsize=11,color=C['orange'])
box(a,.735,.35,.25,.17,'专家前向与反向','当前输出及梯度',col='light',size=12);arrow(a,(.86,.71),(.86,.535));a.text(.60,.37,'专家 ID ≠ 物理副本位置\n不回放旧输出\n不消除策略滞后',fontsize=11,ha='right',linespacing=1.8)
ax=f.add_axes([.16,.085,.41,.23]);ax.barh([1,0],[6,12],height=.45,color=[C['blue'],C['orange']]);ax.set(yticks=[1,0],yticklabels=['uint16','int32'],xlabel='仅专家 ID 的载荷 / MiB',xlim=(0,14),ylim=(-.55,1.65));ax.text(6.25,1,'6',va='center');ax.text(12.25,0,'12',va='center')
f.text(.63,.19,'8192 token × 48 层 × top-8\n另计 mask、位置与版本元数据\n不包含 KV 或旧输出',fontsize=11,va='center',linespacing=1.8)
save(f,'figure-10-7-replay');data['10-7']={'route_summary':calc('routing-metadata-book')['summary'],'id_bytes':[6*2**20,12*2**20]}
# 8. Hypothetical sensitivity, no unsupported cross-hardware performance bars.
f,ax=plt.subplots(figsize=(11,6.5));f.subplots_adjust(left=.10,right=.95,bottom=.17,top=.91);rat=np.linspace(.25,1.5,200);curves={}
for frac,col in [(.05,'teal'),(.2,'blue'),(.5,'orange')]:
 y=1-frac+frac/rat;curves[str(frac)]=y.tolist();ax.plot(rat,y,color=C[col],lw=2.4,label=f'基线暴露通信占比 {frac:.0%}');ax.scatter([.5],[1-frac+frac/.5],color=C[col])
ax.axvline(1,ls='--',color=C['line']);ax.axhline(1,ls='--',color=C['line']);ax.set(xlabel='候选有效通信能力 / 基线能力',ylabel='候选完成时间 / 基线完成时间',xlim=(.25,1.5),xticks=[.25,.5,.75,1,1.25,1.5],ylim=(.8,2.65));ax.legend(frameon=False,fontsize=12);ax.grid(alpha=.15)
f.text(.10,.055,'教学敏感性：其余工作不变；真实硬件需重新检查重叠、精度、容量和软件支持',fontsize=10.5)
save(f,'figure-10-8-hardware');data['10-8']={'kind':'declared_sensitivity','formula':'1-f+f/r','relative_bandwidth':rat.tolist(),'curves':curves}
# 9. Nominal Dense model, fixed data and hardware count.
f,ax=plt.subplots(figsize=(11.5,6.5));f.subplots_adjust(left=.11,right=.96,bottom=.18,top=.92);rows=calc('dense-training-scale-book')['dense_scale_rows'];scaledata={}
for dev,label,col in [('a100-80gb-sxm','A100 80GB SXM','blue'),('h100-sxm','H100 SXM','teal'),('b200-sxm','B200','orange')]:
 rr=sorted([r for r in rows if r['device']==dev and r['efficiency_exact']=='1/2'],key=lambda r:r['parameters']);xx=[r['parameters']/1e12 for r in rr];yy=[r['training_days'] for r in rr];scaledata[dev]=rr;ax.plot(xx,yy,'o-',color=C[col],lw=2,label=label)
 for x,y in zip(xx,yy):ax.annotate(f'{y:.0f}',(x,y),xytext=(5,6),textcoords='offset points',fontsize=10,color=C[col])
for y in [90,180]:ax.axhline(y,color=C['muted'],ls='--',lw=1);ax.text(9.4,y*1.045,f'{y} 天',ha='right',fontsize=10)
ax.set(yscale='log',xlabel='Dense 参数量 / T',ylabel='训练完成时间 / 天（对数刻度）',xticks=[1,5,10],xlim=(.6,10.7),ylim=(50,8500));ax.set_yticks([100,1000]);ax.legend(frameon=False,fontsize=11,loc='upper left');ax.grid(axis='y',which='major',alpha=.15)
f.text(.11,.052,'16384 张卡 · 20T token · 50% MFU · 6ND；不含额外日历停顿与可行性修正',fontsize=11)
save(f,'figure-10-9-scale');data['10-9']=scaledata
(HERE/'figure-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(HERE/'figure-layout-check.json').write_text(json.dumps({'text_extent_warnings':layout},ensure_ascii=False,indent=2)+'\n')
# Render formulas on the build machine; bundle all image/font bytes into HTML.
md=HERE.parent/'10-训练系统.md';raw=md.read_text();maths=[]
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
 if p.suffix=='.svg':body=body.replace('src="ch10/'+p.name+'"','src="data:image/png;base64,'+base64.b64encode(p.with_suffix('.png').read_bytes()).decode()+'"')
css='''*{box-sizing:border-box}body{margin:0;background:#f7f7f4;color:#243640;font:18px/1.95 Georgia,"Songti SC",serif}main{max-width:1020px;margin:auto;padding:48px 46px 85px;background:#fff}h1,h2,h3{font-family:Arial,"PingFang SC",sans-serif;line-height:1.45;color:#183949}h1{font-size:36px}h2{font-size:28px;border-top:1px solid #d5e1e4;margin-top:65px;padding-top:26px}h3{font-size:23px;margin-top:38px}a{color:#286b98;text-underline-offset:3px;overflow-wrap:anywhere}img{display:block;width:100%;height:auto;margin:28px auto 10px}em{font-size:15px;color:#546e7a}table{border-collapse:collapse;width:100%;font-size:15px;line-height:1.7;margin:22px 0}td,th{padding:10px 12px;border-bottom:1px solid #d5e1e4;text-align:left}th{background:#edf4f6}blockquote{margin:27px 0;padding:14px 24px;border-left:4px solid #16857b;background:#f0f7f4;font-size:16px}code{font:0.85em/1.6 Menlo,monospace;background:#f0f4f6;overflow-wrap:anywhere}pre{overflow-x:auto;padding:16px;max-width:100%}nav{font:16px/1.9 Arial,"PingFang SC",sans-serif;background:#eff5f7;padding:18px 24px}nav a{display:block}.footnote{font-size:14px;line-height:1.8}.footnote li{margin-bottom:13px}.table-scroll{overflow-x:auto;max-width:100%}.katex{font-size:1.04em}.katex-display{overflow-x:auto;overflow-y:hidden;padding:12px 0}@media(max-width:650px){main{padding:24px 18px}body{font-size:17px}h1{font-size:29px}h2{font-size:25px}h3{font-size:21px}}@media print{main{max-width:none;padding:0}h2,h3{break-after:avoid}img,blockquote{break-inside:avoid}body{font-size:11pt}}'''
nav=''.join('<a href="#'+ident+'">'+title+'</a>' for ident,title in re.findall(r'<h2 id="([^"]+)">(10\.\d+ [^<]+)</h2>',body))
page='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>第 10 章 训练系统</title><style>'+css+math_css+'</style></head><body><main><nav aria-label="本章目录">'+nav+'</nav>'+body+'</main></body></html>'
hp=md.with_suffix('.html');hp.write_text(page)
(HERE/'math-validation.json').write_text(json.dumps({'renderer':'KaTeX 0.16.11','expressions':len(maths),'display_expressions':sum(x['display'] for x in maths),'errors':[]},indent=2)+'\n')
artifacts=outputs+[HERE/'figure-data.json',hp,md]
(HERE/'manifest.json').write_text(json.dumps({'chapter':10,'generator':'manuscripts/ch10/build.py','figures':9,'font_family':family,'outputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in artifacts]},ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(outputs)} image files, {len(maths)} formulas, offline HTML; {len(layout)} extent warnings.')
