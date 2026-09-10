#!/usr/bin/env python3
"""Generate chapter-seven vector figures, data, and an offline reading edition."""
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
plt.rcParams.update({'font.family':family,'font.size':11,'axes.unicode_minus':False,'svg.fonttype':'none','svg.hashsalt':'ch07-network-v1','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white','savefig.facecolor':'white','text.color':'#203c48','axes.labelcolor':'#203c48','pdf.fonttype':42})
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
# Figures contain panel labels and units only; their numbers and full captions live outside.
f,a=canvas(7)
panel(a,.02,.98,'同一紧密互联范围')
box(a,.29,.72,.42,.12,'内部交换互联',col='light')
for i in range(8):
 x=.035+i*.119;box(a,x,.47,.097,.12,f'卡 {i}',size=11);arrow(a,(x+.048,.60),(.31+i*.052,.71),lw=1)
a.plot([.02,.98],[.40,.40],color=C['line'],ls='--')
panel(a,.02,.39,'两台服务器，经数据中心网络协作')
for j in range(2):
 x=.025+j*.56;box(a,x,.025,.39,.21,f'服务器 {j}','四个参与者；本地互联',size=13);box(a,x+.12,.265,.15,.075,'NIC',col='sand',size=10);arrow(a,(x+.195,.24),(x+.195,.26))
box(a,.437,.04,.115,.14,'交换网络',size=10);arrow(a,(.30,.30),(.465,.185),'blue');arrow(a,(.535,.185),(.70,.30),'blue')
save(f,'figure-7-1-boundaries');data['7-1']={'kind':'conceptual','ranks':8,'servers':2}
# 2: Explicit path constraints and scaling bound.
f=plt.figure(figsize=(13,6));a=f.add_axes([.025,.12,.47,.79]);a.set(xlim=(0,1),ylim=(0,1));a.axis('off');panel(a,.01,.99,'一条路径的串联资源〔教学〕')
for i,(t,b) in enumerate([('源端 GPU → PCIe','80 GB/s'),('网卡与共享出口','50 GB/s'),('交换割集','50 GB/s'),('接收端路径','40 GB/s')]):
 y=.73-i*.22;box(a,.16,y,.68,.15,t,b,size=12)
 if i<3:arrow(a,(.50,y-.005),(.50,y-.065))
a=f.add_axes([.61,.19,.35,.66]);n=np.arange(1,9);cut=8*2**30/50e9*1000;compute=100/n
a.plot(n,np.maximum(cut,compute),'o-',c=C['teal'],label='完全重叠：资源下界');a.plot(n,cut+compute,'s--',c=C['blue'],label='完全串行模型');a.plot(n,compute,':',c=C['orange'],label='仅计算段');a.set(xlabel='设备数相对倍数',ylabel='每步时间 / ms',xticks=n,ylim=(0,315));a.legend(frameon=False,fontsize=10,loc='upper right')
save(f,'figure-7-2-cut');data['7-2']={'kind':'teaching','cut_ms':cut,'device_multipliers':n.tolist(),'compute_ms':compute.tolist()}
# 3: Hierarchy ownership and saved resource ledgers.
f=plt.figure(figsize=(13,9));a=f.add_axes([.035,.58,.93,.38]);a.set(xlim=(0,1),ylim=(0,1));a.axis('off');panel(a,.01,.99,'本地分散归约 → 对应分片跨机归约 → 本地收集')
for row,y in enumerate([.62,.13]):
 a.text(.01,y+.07,f'服务器 {row}',fontsize=11,va='center')
 for k in range(4):box(a,.18+k*.20,y,.16,.18,f'卡 {row*4+k}',f'分片 {k}：48 MiB',size=10)
for k in range(4):
 x=.26+k*.20;arrow(a,(x-.018,.61),(x-.018,.325));arrow(a,(x+.018,.325),(x+.018,.61));a.text(x,.465,'归约',ha='center',fontsize=9,bbox={'fc':'white','ec':'none','pad':1})
names=['gradient-fp32-flat-contiguous-nic2','gradient-fp32-flat-interleaved-nic2','gradient-fp32-hierarchical-nic2'];g=[calc(x) for x in names];labels=['连续平坦环','交错平坦环','分层']
ax=f.add_axes([.095,.14,.36,.31]);local=[z['summary']['local_send_bytes']/2**20 for z in g];remote=[z['summary']['remote_send_bytes']/2**20 for z in g];ax.bar(labels,local,color=C['teal'],label='本地');ax.bar(labels,remote,bottom=local,color=C['orange'],label='跨服务器');ax.set(ylabel='逻辑发送 / MiB',ylim=(0,3300));ax.legend(frameon=False,ncol=2);ax.set_title('总发送相同，跨边界比例不同',loc='left',fontsize=12)
ax=f.add_axes([.60,.14,.35,.31]);ts=[float(Fraction(z['summary']['serial_barrier_lower_seconds_exact']))*1000 for z in g];ax.bar(labels,ts,color=[C['blue'],C['orange'],C['teal']]);ax.set(ylabel='逐轮资源下界 / ms',ylim=(0,43));ax.set_title('计入共享出口与每轮启动',loc='left',fontsize=12)
for i,v in enumerate(ts):ax.text(i,v+.8,f'{v:.3f}',ha='center',fontsize=11)
save(f,'figure-7-3-hierarchy');data['7-3']={'kind':'saved_calculation','sources':names,'local_MiB':local,'remote_MiB':remote,'lower_ms':ts}
# 4: Concrete responsibilities, no timing inferred from arrow length.
f,a=canvas(9)
rows=[('主机处理的 RPC',['应用 / CPU','NIC / 网络','对端 CPU'],['请求序列化','载荷传送','执行并响应']),('CPU 提交的 GPUDirect RDMA',['CPU 提交','NIC ↔ GPU 内存','远端 NIC ↔ GPU'],['提交 / 观察完成','数据直达','目标内存写入']),('GPU 经 NVLink 访问',['发起 GPU','NVLink / 交换','对端 GPU 内存'],['设备指令','访问路径','按机制同步']),('设备发起的 URMA 异步读写',['发起设备 / 队列','UB / 交换','目标设备内存'],['提交与完成消费','数据路径','按契约发布'])]
for i,(title,boxes,notes) in enumerate(rows):
 y=.79-i*.235;panel(a,.015,y+.18,title)
 for j,(t,b) in enumerate(zip(boxes,notes)):box(a,.025+j*.335,y,.285,.12,t,b,size=11)
 for j in range(2):
  ar=FancyArrowPatch((.315+j*.335,y+.075),(.35+j*.335,y+.075),arrowstyle='-|>',mutation_scale=12,color=C['blue'],lw=1.7,linestyle='--' if (i==1 and j==0) else '-');a.add_patch(ar)
 a.annotate('',xy=(.17,y-.04),xytext=(.83,y-.04),arrowprops={'arrowstyle':'->','ls':'--','color':C['muted'],'lw':1});a.text(.50,y-.075,'响应 / 完成与同步关系',fontsize=9,ha='center',color=C['muted'])
save(f,'figure-7-4-access');data['7-4']={'kind':'conceptual','timing':None,'paths':[x[0] for x in rows]}
# 5: Shared states, retaining relation memory.
f=plt.figure(figsize=(13,8));a=f.add_axes([.04,.58,.92,.37]);a.set(xlim=(0,1),ylim=(0,1));a.axis('off');panel(a,.01,.98,'应用关系与传输状态分别组织')
for i in range(3):
 y=.63-i*.24;box(a,.015,y,.23,.17,f'应用端点 {i}','独立提交 / 完成',size=11);box(a,.36,y,.23,.17,'关系绑定','目标、权限与身份',size=11);arrow(a,(.25,y+.085),(.35,y+.085));arrow(a,(.60,y+.085),(.735,.42))
box(a,.745,.30,.23,.26,'同目标传输状态','可靠交付 / 拥塞',col='light',size=11)
ss=[calc('connection-states-full')['summary'],calc('connection-states-isolated')['summary']];z=ss[0];vals=np.array([[z['endpoint_bytes'],z['relation_bytes'],z['coupled_transport_bytes']],[z['endpoint_bytes'],z['relation_bytes'],z['shared_transport_bytes']],[ss[1]['endpoint_bytes'],ss[1]['relation_bytes'],ss[1]['shared_transport_bytes']]])/2**20
ax=f.add_axes([.15,.12,.77,.33]);left=np.zeros(3)
for j,(title,col) in enumerate([('端点','blue'),('关系绑定','orange'),('传输状态','teal')]):ax.barh(range(3),vals[:,j],left=left,color=C[col],label=title);left+=vals[:,j]
ax.set(yticks=range(3),yticklabels=['逐关系独占','按目标共享','八类隔离'],xlabel='声明状态容量 / MiB',xlim=(0,10.4),xticks=[0,2,4,6,8,10]);ax.invert_yaxis();ax.axvline(1,ls='--',color=C['red']);ax.legend(frameon=False,ncol=3,loc='lower right')
for i,v in enumerate(left):ax.text(v+.1,i,f'{v:.3f}',va='center',fontsize=10)
save(f,'figure-7-5-state');data['7-5']={'kind':'saved_calculation','state_MiB':vals.tolist(),'budget_MiB':1}
# 6: Lifetime, actual schedules, stale value witness.
f=plt.figure(figsize=(13,10));a=f.add_axes([.03,.78,.94,.18]);a.set(xlim=(0,1),ylim=(0,1));a.axis('off')
for i,t in enumerate(['写入','数据可见','通知','消费结束','可回收']):
 x=.012+i*.20;box(a,x,.30,.16,.43,t,size=12)
 if i<4:arrow(a,(x+.165,.51),(x+.19,.51))
order=calc('operation-ordering-book');ax=f.add_axes([.14,.39,.80,.32]);colors={'write_data':'blue','recover_and_make_visible':'orange','publish_notification':'red','independent_transfer':'teal'};task_names={'write_data':'写入','recover_and_make_visible':'附加恢复','publish_notification':'通知','independent_transfer':'独立传输'}
for i,(key,label) in enumerate([('strict','全完成串行'),('necessary_dependencies','保留必要依赖')]):
 for task in order['request_schedules'][key]['tasks']:
  row=2-i*1.5-(.38 if task['id']=='independent_transfer' and i==1 else 0);start=task['start_ns']/1000;dur=task['duration_ns']/1000
  ax.broken_barh([(start,dur)],(row-.12,.24),facecolors=C[colors[task['id']]])
 ax.text(-3,2-i*1.5,label,ha='right',va='center',fontsize=10)
ax.set(xlim=(0,118),ylim=(-.3,2.6),yticks=[],xlabel='时间 / μs',xticks=[0,20,60,100,112]);ax.set_title('相同发布依赖；独立传输具有独立资源',loc='left',fontsize=12)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=C[v],label=task_names[k]) for k,v in colors.items()],frameon=False,ncol=4,fontsize=9,loc='upper center')
a=f.add_axes([.045,.06,.91,.23]);a.set(xlim=(0,1),ylim=(0,1));a.axis('off');panel(a,.01,.99,'取值时刻与交付时刻不同〔独立教学反例〕')
for i,(t,b) in enumerate([('1 μs','提前读取 D=0'),('2 μs','D=1 可见'),('3–4 μs','标志可见并读到'),('5 μs','按序交付仍带旧 D'),('6 μs','重读后交付 D=1')]):
 x=.01+i*.20;box(a,x,.22,.18,.40,t,b,size=11)
 if i<4:arrow(a,(x+.182,.42),(x+.197,.42),lw=1)
save(f,'figure-7-6-ordering');data['7-6']={'kind':'saved_calculation','schedules':order['request_schedules'],'stale_read_example':order['stale_read_example']}
# 7: Queues use saved event segments; distinct panels explicitly mark distinct inputs.
f,axs=plt.subplots(2,2,figsize=(13,10));f.subplots_adjust(left=.085,right=.97,top=.94,bottom=.09,wspace=.32,hspace=.44)
queue_data={}
for name,label,col,ls in [('periodic-queue-aligned','同时开始','blue','-'),('periodic-queue-staggered','错开 20 ms','teal','--'),('periodic-queue-drift','重叠 5 ms','orange',':')]:
 z=calc(name);queue_data[name]=z['queue_segments'];tt=[];qq=[];rr=[]
 for seg in z['queue_segments']:
  tt.extend([seg['start_ns']/1e6,seg['end_ns']/1e6]);qq.extend([seg['queue_start_bytes']/1e6,seg['queue_end_bytes']/1e6]);rr.extend([seg['arrival_bytes_per_second']/1e9]*2)
 axs[0,0].plot(tt,rr,c=C[col],ls=ls,label=label,lw=2);axs[1,0].plot(tt,qq,c=C[col],ls=ls,label=label,lw=2)
axs[0,0].axhline(50,c=C['red'],lw=1,ls='--');axs[0,0].set(xlim=(0,65),ylim=(-3,90),xlabel='时间 / ms',ylabel='外生到达 / GB/s',title='周期高峰与 50 GB/s 出口');axs[0,0].legend(frameon=False,fontsize=9)
axs[1,0].set(xlim=(0,65),ylim=(-15,680),xlabel='时间 / ms',ylabel='分析队列 / MB',title='无限缓冲、无反馈的队列');axs[1,0].legend(frameon=False,fontsize=9)
z=calc('feedback-queue-overflow');tt=[];qq=[]
for seg in z['queue_segments']:tt.extend([seg['start_ns']/1000,seg['end_ns']/1000]);qq.extend([seg['queue_start_bytes']/1024,seg['queue_end_bytes']/1024])
ax=axs[0,1];ax.plot(tt,qq,c=C['blue'],lw=2);ax.axvline(20,c=C['red'],ls='--');ax.text(23,560,'反馈后降至 40 GB/s',fontsize=10);ax.set(xlim=(0,100),ylim=(0,630),xlabel='时间 / μs',ylabel='分析队列 / KiB',title='有限缓冲：512 KiB');ax.axhline(512,c=C['line'],ls=':')
packet_data={};ax=axs[1,1]
for name,label,col in [('packet-reorder-balanced','等延迟','teal'),('packet-reorder-skewed','延迟 1 / 9 μs','blue'),('packet-reorder-loss','偏斜且首包丢失','orange')]:
 z=calc(name);packet_data[name]=z['receive_events'];tt=[0];v=[0]
 for row in z['receive_events']:tt.append(float(Fraction(row['time_exact_ns']))/1000);v.append(row['retained_bytes']/1024)
 ax.step(tt,v,where='post',color=C[col],label=label,lw=2)
ax.set(xlim=(0,26),xticks=[0,5,10,15,20,25],ylim=(-.2,8.2),xlabel='时间 / μs',ylabel='保留的乱序载荷 / KiB',title='八个报文的接收与按序释放');ax.legend(frameon=False,fontsize=9,loc='upper left')
save(f,'figure-7-7-congestion');data['7-7']={'kind':'saved_calculation_distinct_panels','periodic_segments':queue_data,'feedback':calc('feedback-queue-overflow'),'packets':packet_data}
# 8: Resource dependency cycles, not physical topology cycles.
f,a=canvas(6);panel(a,.015,.98,'可能循环等待的资源依赖');panel(a,.53,.98,'拆分响应资源并约束申请次序')
xy=[(.04,.63),(.30,.63),(.30,.19),(.04,.19)]
for i,(x,y) in enumerate(xy):box(a,x,y,.15,.18,f'资源 {chr(65+i)}',size=12)
arrow(a,(.195,.72),(.29,.72),'red');arrow(a,(.375,.625),(.375,.385),'red');arrow(a,(.295,.28),(.20,.28),'red');arrow(a,(.115,.385),(.115,.625),'red')
a.text(.245,.495,'持有前一项\n等待后一项',ha='center',va='center',fontsize=11,color=C['red'])
for i,(t,b) in enumerate([('请求资源','按次序申请'),('执行资源','消费数据'),('响应资源','独立预留 / 获得服务')]):
 y=.66-i*.25;box(a,.60,y,.31,.17,t,b,col='light',size=12)
 if i<2:arrow(a,(.755,y-.005),(.755,y-.07))
a.text(.755,.03,'响应到达后释放原请求资源',ha='center',fontsize=10,color=C['muted'])
save(f,'figure-7-8-deadlock');data['7-8']={'kind':'conceptual_resource_graph','cycle':['A','B','C','D','A'],'acyclic':['request','execution','response']}
# 9: Readiness counterfactual, ring model, existing CPU observation.
f=plt.figure(figsize=(13,10));ax=f.add_axes([.17,.60,.77,.33]);ready=[0,0,0,2]
for group,(label,rd,ex) in enumerate([('原始',ready,.4),('交换减半',ready,.2),('全部在起点就绪',[0]*4,.4)]):
 base=10-group*4
 for r,t in enumerate(rd):
  y=base-r*.55;ax.broken_barh([(0,t)],(y-.17,.32),facecolors='#dbe2e6');ax.broken_barh([(t,max(rd)-t)],(y-.17,.32),facecolors='#f6e3c9');ax.broken_barh([(max(rd),ex)],(y-.17,.32),facecolors=C['blue']);ax.scatter([t],[y],s=12,color=C['ink'],zorder=3)
 ax.text(-.07,base-.75,label,ha='right',va='center',fontsize=10)
ax.set(xlim=(0,2.6),xticks=[0,.5,1,1.5,2,2.5],ylim=(-.4,11),yticks=[],xlabel='时间 / ms');ax.set_title('四个参与者：就绪、等待与交换〔教学〕',loc='left',fontsize=12);ax.legend(handles=[Patch(color='#dbe2e6',label='尚未就绪'),Patch(color='#f6e3c9',label='等待其他参与者'),Patch(color=C['blue'],label='交换')],ncol=3,frameon=False,fontsize=9,loc='upper right')
ax=f.add_axes([.085,.12,.36,.32]);sizes=np.array([8192,8*2**20]);ring=np.array([14*5e-6+1.75*sizes/b for b in [25e9,75e9]])*1e6
for i,col in enumerate(['blue','teal']):ax.bar(np.arange(2)+(i-.5)*.32,ring[i],.30,color=C[col],label=['25 GB/s','75 GB/s'][i])
ax.set(xticks=[0,1],xticklabels=['8 KiB','8 MiB'],ylabel='通信模型时间 / μs',ylim=(0,790));ax.set_title('同一环算法的消息大小效应',loc='left',fontsize=12);ax.legend(frameon=False,fontsize=10)
meas=read('experiments/ch07/07-10/rank-readiness/results/summary.json');m=[z for z in meas if z['bytes']==4096];ax=f.add_axes([.60,.12,.35,.32]);values=[z['completion_ms']['median'] for z in m];ax.bar(range(3),values,color=C['orange']);ax.set(xticks=[0,1,2],xticklabels=['0 ms','2 ms','20 ms'],xlabel='请求一个参与者等待',ylabel='全组完成中位数 / ms',ylim=(0,33));ax.set_title('4 KiB，四进程 CPU Gloo〔实测〕',loc='left',fontsize=12)
for i,v in enumerate(values):ax.text(i,v+.6,f'{v:.3f}',ha='center',fontsize=10)
save(f,'figure-7-9-progress');data['7-9']={'kind':'teaching_and_cpu_observation_separate','ready_ms':ready,'exchange_ms':.4,'ring_us':ring.tolist(),'measured':m}
(HERE/'figure-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(HERE/'figure-layout-check.json').write_text(json.dumps({'text_extent_warnings':layout},ensure_ascii=False,indent=2)+'\n')
exec(compile((HERE/'render.inc.py').read_text(),str(HERE/'render.inc.py'),'exec'))
