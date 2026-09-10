#!/usr/bin/env python3
"""Build chapter 11 figures and offline HTML; read-only access to locked evidence."""
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
font=next((Path(x) for x in [args.font,'/System/Library/Fonts/Supplemental/Arial Unicode.ttf','/System/Library/Fonts/STHeiti Medium.ttc','/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'] if x and Path(x).exists()),None)
if not font:raise SystemExit('Use --font to provide a CJK font')
font_manager.fontManager.addfont(str(font));family=font_manager.FontProperties(fname=str(font)).get_name()
plt.rcParams.update({'font.family':family,'font.size':12,'axes.unicode_minus':False,'svg.fonttype':'none','svg.hashsalt':'chapter11-v1','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white','savefig.facecolor':'white','text.color':'#233c48','axes.labelcolor':'#233c48','axes.edgecolor':'#9bacb4'})
C={'ink':'#233c48','blue':'#286b94','teal':'#20867e','orange':'#bb682d','red':'#aa4949','pale':'#edf3f7','green':'#e4f2ed','sand':'#fbf0df','muted':'#506975','line':'#bccdd5','gray':'#e1e6ea'}
for row in json.loads((HERE/'sources.json').read_text())['sources']:
 if hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()!=row['sha256']:raise SystemExit('Locked source changed: '+row['path'])
def load(name):return json.loads((ROOT/'calculations/results'/f'{name}.json').read_text())
lifecycle=load('environment-lifecycle-default');route=load('routing-cost-book');retry=load('retry-paths-book')
outputs=[];data={};warnings=[]
def save(f,name):
 f.canvas.draw();renderer=f.canvas.get_renderer()
 for t in f.findobj(matplotlib.text.Text):
  if not t.get_visible() or not t.get_text():continue
  bb=t.get_window_extent(renderer)
  if bb.x0<0 or bb.y0<0 or bb.x1>f.bbox.width or bb.y1>f.bbox.height:warnings.append({'figure':name,'text':t.get_text()})
 for ext in ['svg','png','pdf']:
  path=HERE/f'{name}.{ext}';f.savefig(path,dpi=180,bbox_inches='tight',pad_inches=.15);outputs.append(path)
 plt.close(f)
def canvas(h=6.5):
 f,a=plt.subplots(figsize=(12,h));f.subplots_adjust(left=.025,right=.975,top=.97,bottom=.04);a.set(xlim=(0,1),ylim=(0,1));a.axis('off');return f,a
def box(a,x,y,w,h,title,body='',color='pale',size=13):
 a.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.005,rounding_size=0.008',edgecolor=C['line'],facecolor=C[color]))
 a.text(x+w/2,y+h*(.67 if body else .5),title,ha='center',va='center',fontsize=size,weight='bold')
 if body:a.text(x+w/2,y+h*.27,body,ha='center',va='center',fontsize=11,color=C['muted'],linespacing=1.5)
def arrow(a,p,q,color='teal',rad=0):a.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=15,lw=1.7,color=C[color],connectionstyle=f'arc3,rad={rad}'))
# Diagrams contain labels only. Figure numbering and explanatory captions live in Markdown.
f,a=plt.subplots(figsize=(12,4.8));f.subplots_adjust(left=.19,right=.96,bottom=.21,top=.89)
for k in range(3):
 a.broken_barh([(10*k,9)],(2.7,.5),facecolors=C['blue']);a.text(10*k+4.5,2.95,f'模型调用 {k+1}',color='white',ha='center',va='center',fontsize=12)
 a.broken_barh([(10*k+9,1)],(1.6,.5),facecolors=C['orange']);a.text(10*k+9.5,2.26,'1 s',ha='center',fontsize=10)
a.broken_barh([(0,30)],(.5,.5),facecolors=C['teal']);a.text(15,.75,'2 GiB × 30 s = 60 GiB·s',color='white',ha='center',va='center',fontsize=14)
a.set(yticks=[.75,1.85,2.95],yticklabels=['环境内存','工具 CPU','模型服务'],xlim=(0,30),ylim=(0,3.6),xticks=[0,9,10,19,20,29,30],xlabel='时间 / s')
a.spines['left'].set_visible(False);a.tick_params(axis='y',length=0);a.grid(axis='x',alpha=.16)
a.text(.0,1.04,'三轮串行任务：完成 30 s；工具工作 3 核秒',transform=a.transAxes,fontsize=15,weight='bold')
save(f,'figure-11-1-timeline');data['11-1']={'kind':'teaching','rounds':3,'model_seconds_per_round':9,'tool_core_seconds_per_round':1,'resident_gib':2,'resident_gib_seconds':60}
# Agent/control path plus container / microVM boundaries.
f,a=canvas(6.8)
box(a,.02,.72,.18,.15,'Agent 控制器','任务、历史与验收')
box(a,.32,.72,.21,.15,'模型服务','返回工具参数')
arrow(a,(.20,.82),(.32,.82));arrow(a,(.32,.76),(.20,.76))
box(a,.02,.38,.18,.17,'环境平台','准入与节点分配');arrow(a,(.11,.72),(.11,.55))
a.text(.14,.64,'明确调用',fontsize=11)
a.add_patch(Rectangle((.30,.20),.26,.40,fill=False,ls='--',lw=1.4,edgecolor=C['teal']))
a.text(.43,.565,'执行节点',ha='center',fontsize=13,weight='bold')
box(a,.33,.28,.20,.19,'工具环境','文件、进程、工具','green');arrow(a,(.20,.46),(.33,.40));arrow(a,(.33,.32),(.20,.39))
a.text(.02,.13,'工具结果回到控制器，成为下一轮输入',fontsize=12,color=C['muted'])
a.plot([.61,.61],[.12,.91],color=C['line'],lw=1)
for x,title in [(.65,'容器'),(.83,'microVM')]:
 a.text(x+.065,.86,title,ha='center',fontsize=14,weight='bold');box(a,x,.63,.14,.13,'工具代码',size=11)
box(a,.65,.43,.14,.13,'宿主内核','共享边界',size=11)
box(a,.83,.43,.14,.13,'客体内核',size=11)
box(a,.83,.23,.14,.13,'VMM／宿主',size=11)
arrow(a,(.72,.63),(.72,.56));arrow(a,(.90,.63),(.90,.56));arrow(a,(.90,.43),(.90,.36))
a.text(.81,.12,'机制比较；具体配置决定隔离与设备能力',ha='center',fontsize=10,color=C['muted'])
save(f,'figure-11-2-boundary');data['11-2']={'kind':'mechanism','source':'case-studies/platform-routing.md'}
# State graph and synchronized preparation timelines.
f,a=canvas(7.4)
for x,t,c in [(.03,'模板','pale'),(.28,'运行','green'),(.53,'暂停快照','sand'),(.79,'恢复运行','green')]:box(a,x,.72,.17,.14,t,color=c)
arrow(a,(.20,.79),(.28,.79));arrow(a,(.45,.79),(.53,.79));arrow(a,(.70,.79),(.79,.79))
a.text(.24,.87,'创建',ha='center',fontsize=11);a.text(.49,.87,'保存',ha='center',fontsize=11);a.text(.75,.87,'恢复',ha='center',fontsize=11)
box(a,.53,.49,.17,.12,'分支环境',color='pale');arrow(a,(.615,.72),(.615,.61));a.text(.67,.66,'派生',fontsize=10)
box(a,.28,.49,.17,.12,'终止',color='gray');arrow(a,(.365,.72),(.365,.61))
a.text(.025,.38,'准备耗时 2 s；明确调用在第 4 秒到达',fontsize=13,weight='bold')
x0=.29;scale=.105
for y,label,start,end in [(.28,'按需创建',4,6),(.18,'提前 1 s',3,5),(.08,'提前 3 s',1,3)]:
 a.text(.025,y,label,va='center',fontsize=12)
 a.plot([x0,x0+6*scale],[y,y],color=C['line'],lw=1)
 a.plot([x0+start*scale,x0+end*scale],[y,y],color=C['blue'],lw=11,solid_capstyle='butt')
 if end<4:a.plot([x0+end*scale,x0+4*scale],[y,y],color=C['orange'],lw=11,solid_capstyle='butt')
 a.text(x0+6*scale+.025,y,['等待 2 s','等待 1 s','就绪空闲 1 s'][[.28,.18,.08].index(y)],va='center',fontsize=10)
a.plot([x0+4*scale]*2,[.035,.325],ls='--',color=C['red'])
for n in [0,1,2,3,4,5,6]:a.text(x0+n*scale,.005,str(n),ha='center',fontsize=10)
a.text(x0+.11,.335,'蓝：准备　橙：就绪未使用',fontsize=10,color=C['muted'])
save(f,'figure-11-3-lifecycle');data['11-3']={'kind':'mechanism_and_teaching','preparation_seconds':2,'call_time':4,'lead_seconds':[0,1,3],'existing_budget':lifecycle['prewarm_budget']}
# Resource before/after diagram.
f,a=canvas(6)
a.text(.5,.92,'新作业：4 张 A 型 GPU + 16 核 CPU，同一节点',ha='center',fontsize=16,weight='bold')
for x,title in [(.04,'整理前'),(.55,'整理后')]:
 a.text(x+.19,.79,title,ha='center',fontsize=14,weight='bold')
 if x<.5:
  box(a,x,.48,.37,.22,'节点 1：4 张 A 型 GPU','仅 8 核可用 → 无法启动','sand')
  box(a,x,.15,.37,.22,'节点 2：4 张 B 型 GPU','32 核可用 → 卡型不符','pale')
 else:
  box(a,x,.48,.37,.22,'节点 1：4 张 A 型 GPU','16 核可用 → 整组启动','green')
  box(a,x,.15,.37,.22,'节点 2：4 张 B 型 GPU','24 核可用 + 接收迁移任务','pale')
arrow(a,(.43,.57),(.53,.57));a.text(.48,.39,'迁移\n8 核任务',ha='center',fontsize=11)
a.text(.5,.055,'迁移需要状态可恢复；新作业收益须连同被迁移任务的延迟评价',ha='center',fontsize=12,color=C['muted'])
save(f,'figure-11-4-placement');data['11-4']={'kind':'teaching','required_gpu_type':'A','required_gpus':4,'required_cpu':16,'before_free_cpu':[8,32],'after_free_cpu':[16,24]}
# Lifecycle stages unscaled; verification below has explicit clock.
f=plt.figure(figsize=(12,7));gs=f.add_gridspec(2,1,height_ratios=[1,2],hspace=.55);f.subplots_adjust(left=.17,right=.96,top=.92,bottom=.12)
a=f.add_subplot(gs[0]);a.set(xlim=(0,1),ylim=(0,1));a.axis('off')
a.text(0,1.05,'临时 rollout 实例：资源分配之后仍有准备路径',fontsize=14,weight='bold')
for x,w,t,c in [(0,.18,'实例出现','pale'),(.24,.20,'权重传输','pale'),(.50,.20,'加载／恢复','sand'),(.76,.22,'有效生成','green')]:
 box(a,x,.26,w,.46,t,color=c,size=12)
 if x<.76:arrow(a,(x+w,.49),(x+w+.055,.49))
a.text(.5,.035,'阶段条宽不表示时长；六实例全部权重传完下界为 7.2 s',ha='center',fontsize=11,color=C['muted'])
a=f.add_subplot(gs[1]);cols=[C['blue'],C['teal'],C['orange']]
for y,starts in [(1.3,[0,10,20]),(.3,[20,30,40])]:
 for k,start in enumerate(starts):a.broken_barh([(start,10)],(y,.5),facecolors=cols[k]);a.text(start+5,y+.25,f'样本 {k+1}',ha='center',va='center',color='white',fontsize=11)
for t in [0,10,20]:a.annotate('到达',(t,2.05),(t,2.48),arrowprops={'arrowstyle':'-|>','color':C['muted']},ha='center',fontsize=10)
a.set(yticks=[.55,1.55],yticklabels=['整批后提交','逐条提交'],xlim=(-1,51),ylim=(0,2.7),xticks=[0,10,20,30,40,50],xlabel='时间 / s');a.spines['left'].set_visible(False);a.tick_params(axis='y',length=0);a.grid(axis='x',alpha=.18)
save(f,'figure-11-5-stages');data['11-5']={'kind':'mechanism_and_teaching','weight_bytes':30_000_000_000,'receivers':6,'sender_bits_per_second':200_000_000_000,'receiver_bits_per_second':50_000_000_000,'all_transfer_lower_seconds':7.2,'verification_arrivals':[0,10,20],'worker_service_seconds':10,'stream_completion_seconds':30,'batch_completion_seconds':50}
# Model service pathways.
f,a=canvas(6)
box(a,.02,.51,.17,.22,'任务控制器','质量与期限')
box(a,.30,.51,.21,.22,'服务入口','鉴权、路由、限流')
box(a,.69,.69,.27,.21,'外部模型 API','队列、缓存、生成','pale')
box(a,.69,.26,.27,.21,'自建模型副本','加载、队列、执行','green')
arrow(a,(.19,.62),(.30,.62));arrow(a,(.51,.67),(.69,.79));arrow(a,(.51,.55),(.69,.37))
a.text(.56,.83,'调用账单',ha='center',fontsize=11);a.text(.57,.35,'设备预留费用',ha='center',fontsize=11)
box(a,.15,.045,.48,.21,'统一任务与尝试账本','普通输入 / 创建 / 读取 / 生成 / 其他费用','sand',12)
arrow(a,(.40,.51),(.40,.255));arrow(a,(.81,.26),(.63,.16))
a.text(.07,.86,'请求与结果沿各自路径往返',fontsize=12,color=C['muted'])
save(f,'figure-11-6-service');data['11-6']={'kind':'mechanism','usage_categories':['uncached_input','cache_creation','cache_read','billed_generation','storage','tools']}
# Quantitative curves derived from locked routing results.
A,B=route['routing_cost_rows'];h=np.linspace(0,1,201);qB=float(Fraction(B['expected_quality_successes_exact'])/route['scenario']['tasks']);hit=float(Fraction(B['hit_attempt_cost_exact']));miss=float(Fraction(B['miss_attempt_cost_exact']));ca=float(Fraction(A['cost_per_quality_success_exact']));cb=(h*hit+(1-h)*miss)/qB
cross=float(Fraction(route['summary']['cost_crossover_b_hit_fraction_exact']));target=float(Fraction(route['summary']['minimum_b_hit_for_joint_target_exact']))
f,axs=plt.subplots(1,2,figsize=(12,5));f.subplots_adjust(left=.09,right=.97,bottom=.18,top=.87,wspace=.32)
a=axs[0];a.plot(h*100,cb,color=C['blue'],label='B：命中率变化',lw=2.3);a.axhline(ca,color=C['orange'],label='A：前缀全命中',lw=2);a.axvline(cross*100,color=C['muted'],ls='--',lw=1);a.scatter([cross*100],[ca],color=C['red'],zorder=5);a.annotate('费用交点 84.93%',(cross*100,ca),(29,.030),arrowprops={'arrowstyle':'->','color':C['muted']},fontsize=11);a.set(xlabel='B 请求命中率 / %',ylabel='费用单位 / 质量成功任务',xlim=(0,100),ylim=(0,.046));a.legend(frameon=False,fontsize=10,loc='upper right');a.set_title('费用：保留所有失败尝试',loc='left',fontsize=13)
a=axs[1];a.plot(h*100,.98*h*100,color=C['blue'],lw=2.3,label='B：质量且按时');a.axhline(0,color=C['orange'],lw=2,label='A：10 s，超过期限');a.axhline(90,color=C['red'],ls='--',lw=1.5,label='目标 90%');a.axvline(target*100,color=C['muted'],ls='--',lw=1);a.annotate('至少命中 91.84%',(target*100,90),(17,68),arrowprops={'arrowstyle':'->','color':C['muted']},fontsize=11);a.set(xlabel='B 请求命中率 / %',ylabel='质量且 6 s 内完成 / %',xlim=(0,100),ylim=(-3,104));a.set_title('期限：与质量联合判定',loc='left',fontsize=13);a.legend(frameon=False,fontsize=10,loc='upper left')
for a in axs:a.grid(alpha=.15)
save(f,'figure-11-7-routing');data['11-7']={'kind':'teaching_from_locked_calculation','source':'calculations/results/routing-cost-book.json','h':h.tolist(),'cost_A':ca,'cost_B':cb.tolist(),'cost_crossover':cross,'joint_target_hit':target}
# Finite retry branches and contributions to total expected cost.
f=plt.figure(figsize=(12,6));gs=f.add_gridspec(1,2,width_ratios=[1.2,1]);f.subplots_adjust(left=.03,right=.96,bottom=.19,top=.95,wspace=.27)
a=f.add_subplot(gs[0]);a.set(xlim=(0,1),ylim=(0,1));a.axis('off')
box(a,.02,.69,.23,.20,'首次尝试','0.010 / 10 s',size=12)
box(a,.42,.69,.22,.20,'局部修复','+0.006 / 4 s',size=12)
box(a,.42,.22,.22,.20,'升级模型','+0.030 / 8 s',size=12)
box(a,.79,.69,.17,.20,'成功',color='green',size=12)
box(a,.79,.07,.17,.15,'失败',color='sand',size=12)
arrow(a,(.25,.82),(.42,.82));a.text(.33,.87,'0.12',ha='center',fontsize=11)
arrow(a,(.12,.69),(.42,.32));a.text(.19,.45,'0.08',fontsize=11)
arrow(a,(.17,.89),(.79,.89),rad=-.24);a.text(.50,.99,'0.80',ha='center',fontsize=11)
arrow(a,(.64,.82),(.79,.82));a.text(.715,.87,'0.60',ha='center',fontsize=11)
arrow(a,(.53,.69),(.53,.42));a.text(.56,.55,'0.40',fontsize=11)
arrow(a,(.64,.36),(.83,.69));a.text(.76,.50,'0.98',fontsize=11)
arrow(a,(.64,.25),(.79,.15));a.text(.70,.15,'0.02',fontsize=11)
a.text(.03,.02,'每条分支均保留此前发生的消耗',fontsize=11,color=C['muted'])
a=f.add_subplot(gs[1]);parts=[.8*.01+.072*.016+.0784*.04,.04704*.046,.00096*.046+.0016*.04];labels=['按时成功路径','超时成功路径','失败路径'];colors=[C['teal'],C['orange'],C['red']]
y=np.arange(3);a.barh(y,parts,color=colors,height=.52)
for i,v in enumerate(parts):a.text(v+.0002,i,f'{v:.6f}',va='center',fontsize=11)
a.set(yticks=y,yticklabels=labels,xlim=(0,.0157),xlabel='每项提交的期望费用贡献');a.invert_yaxis();a.tick_params(axis='y',length=0);a.spines['left'].set_visible(False);a.grid(axis='x',alpha=.15)
a.set_title('三类贡献合计 0.01456',loc='left',fontsize=14)
save(f,'figure-11-8-retry');data['11-8']={'kind':'teaching_from_locked_calculation','source':'calculations/results/retry-paths-book.json','contributions':dict(zip(labels,parts)),'summary':retry['summary']}
(HERE/'figure-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(HERE/'figure-layout-check.json').write_text(json.dumps({'text_extent_warnings':warnings},ensure_ascii=False,indent=2)+'\n')

# Offline HTML; KaTeX and its fonts are vendored with the chapter.
md=HERE.parent/'11-资源调度与运行环境.md';raw=md.read_text();maths=[]
def protect_math(match):
 text=match.group(0);display=text.startswith('$$');latex=text[2:-2] if display else text[1:-1];token=f'MATHPLACEHOLDER{len(maths)}END';maths.append({'latex':latex.strip(),'display':display,'token':token});return ('\n\n'+token+'\n\n') if display else token
protected=re.sub(r'\$\$[\s\S]*?\$\$|\$[^$\n]+\$',protect_math,raw)
body=markdown.markdown(protected,extensions=['tables','footnotes','fenced_code','toc'],output_format='html')
node_code="const fs=require('fs'),k=require(process.argv[1]);let a=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(a.map(x=>k.renderToString(x.latex,{displayMode:x.display,throwOnError:true,output:'htmlAndMathml'}))))"
result=subprocess.run(['node','-e',node_code,str(HERE/'vendor/katex/katex.js')],input=json.dumps(maths),text=True,capture_output=True)
if result.returncode:raise SystemExit(result.stderr)
for entry,rendered in zip(maths,json.loads(result.stdout)):body=body.replace('<p>'+entry['token']+'</p>',rendered) if entry['display'] else body.replace(entry['token'],rendered)
math_css=(HERE/'vendor/katex/katex.min.css').read_text()
def font_data(match):
 p=HERE/'vendor/katex'/match[1];return 'url(data:font/'+p.suffix[1:]+';base64,'+base64.b64encode(p.read_bytes()).decode()+')'
math_css=re.sub(r'url\((fonts/[^)]+)\)',font_data,math_css)
body=re.sub(r'<table>(.*?)</table>',r'<div class="table-scroll"><table>\1</table></div>',body,flags=re.S)
for p in outputs:
 if p.suffix=='.svg':body=body.replace('src="ch11/'+p.name+'"','src="data:image/png;base64,'+base64.b64encode(p.with_suffix('.png').read_bytes()).decode()+'"')
body=re.sub(r'<p>(<img [^>]+>)</p>\s*<p><em>(图 11-[\s\S]*?)</em></p>',r'<figure>\1<figcaption>\2</figcaption></figure>',body)
css='''figure{margin:32px 0}figcaption{font:15px/1.8 Arial,"PingFang SC",sans-serif;color:#506975;padding:8px 0}body{margin:0;background:#fafaf8;color:#243640;font:18px/1.95 Georgia,"Songti SC",serif}main{max-width:960px;margin:auto;padding:50px 38px 90px;background:white}h1,h2,h3{font-family:Arial,"PingFang SC",sans-serif;line-height:1.45;color:#163747}h1{font-size:36px}h2{font-size:28px;border-top:1px solid #d5e1e4;margin-top:65px;padding-top:28px}h3{font-size:23px;margin-top:40px}p{margin:1em 0}a{color:#246f91;text-underline-offset:3px}img{display:block;width:100%;height:auto;margin:26px auto 10px}em{font-size:15px;color:#55707d}table{border-collapse:collapse;width:100%;font-size:15px;line-height:1.7;margin:24px 0}td,th{padding:10px 12px;border-bottom:1px solid #d5e1e4;text-align:left}th{background:#edf4f6}blockquote{margin:28px 0;padding:16px 24px;border-left:4px solid #138b83;background:#f1f8f6;font-size:16px}code{font:0.85em/1.65 Menlo,monospace;background:#f0f4f6;overflow-wrap:anywhere}pre{white-space:pre;overflow-x:auto;padding:16px;border:1px solid #d5e1e4;max-width:100%;box-sizing:border-box}nav{font:16px/1.9 Arial,"PingFang SC",sans-serif;background:#f0f6f8;padding:18px 24px}nav a{display:block}.footnote{font-size:14px;line-height:1.8}.footnote li{margin-bottom:12px}.table-scroll{overflow-x:auto;max-width:100%}.katex{font-size:1.04em}.katex-display{overflow-x:auto;overflow-y:hidden;padding:12px 0}@media(max-width:650px){main{padding:25px 18px}body{font-size:17px}h1{font-size:29px}h2{font-size:25px}}@media print{main{max-width:none;padding:0}h2,h3{break-after:avoid}img,blockquote{break-inside:avoid}body{font-size:11pt}}'''
nav=''.join('<a href="#'+ident+'">'+title+'</a>' for ident,title in re.findall(r'<h2 id="([^"]+)">(11\.\d+ [^<]+)</h2>',body))
page='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>第 11 章 资源调度与运行环境</title><style>'+css+math_css+'</style><main><nav>'+nav+'</nav>'+body+'</main></html>'
html_path=HERE.parent/'11-资源调度与运行环境.html';html_path.write_text(page)
(HERE/'math-validation.json').write_text(json.dumps({'renderer':'KaTeX 0.16.11','expressions':len(maths),'display_expressions':sum(x['display'] for x in maths),'errors':[]},indent=2)+'\n')
artifacts=outputs+[HERE/'figure-data.json',html_path,md]
(HERE/'manifest.json').write_text(json.dumps({'chapter':11,'generator':'manuscripts/ch11/build.py','figures':8,'font_family':family,'outputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in artifacts]},ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(outputs)} figure files, {len(maths)} equations and offline HTML; {len(warnings)} layout warnings.')
