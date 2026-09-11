#!/usr/bin/env python3
"""Generate chapter-seven vector figures, data, and an offline reading edition."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from preview_output import preview_path
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
import sys
sys.path.insert(0,str(HERE.parent))
from figure_style.typography import configure_font
font,family=configure_font(args.font)
plt.rcParams.update({'font.family':[family,'DejaVu Sans'],'font.size':11,'axes.unicode_minus':False,'svg.fonttype':'path','svg.hashsalt':'ch07-network-v1','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white','savefig.facecolor':'white','text.color':'#203c48','axes.labelcolor':'#203c48','pdf.fonttype':42})
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
# Figures 7-1 to 7-3 are drawn at book size in teaching_revision.py; this block records their data.
data['7-1']={'kind':'conceptual','ranks':16,'servers':2,'ranks_per_server':8,'nics_per_server':8,'nic_Bps_per_direction':50e9,'nvlink_Bps_per_direction':450e9}
# 2: One relationship: compute scaling against a fixed cut (one NIC carries the ring's cross-server bytes).
n=np.arange(1,9);cut=360*2**20/50e9*1000;compute=20/n
data['7-2']={'kind':'teaching','volume_per_direction_bytes':360*2**20,'cut_bandwidth_Bps':50e9,'compute_base_ms':20,'cut_ms':cut,'device_multipliers':n.tolist(),'compute_ms':compute.tolist()}
# 3: Same total communication, different cross-boundary fraction and NIC usage.
names=['gradient-fp32-flat-contiguous-nic8','gradient-fp32-flat-interleaved-nic8','gradient-fp32-hierarchical-nic8'];g=[calc(x) for x in names];labels=['连续环','交错环','分层归约']
local=[z['summary']['local_send_bytes']/2**20 for z in g];remote=[z['summary']['remote_send_bytes']/2**20 for z in g];ts=[float(Fraction(z['summary']['serial_barrier_lower_seconds_exact']))*1000 for z in g];nics=[z['summary']['remote_nics_used_per_server'] for z in g]
ring_orders=[list(range(16)),[r for pair in zip(range(8),range(8,16)) for r in pair]]
data['7-3']={'kind':'saved_calculation','sources':names,'local_MiB':local,'remote_MiB':remote,'lower_ms':ts,'nics_used_per_server':nics,'ring_orders':ring_orders,'hierarchy_pairs':[[i,i+8] for i in range(8)],'plotted':'logical paths and local/remote bytes; lower_ms supports prose'}

# 4: Concrete responsibilities, no timing inferred from arrow length.
f,a=canvas(9)
rows=[('主机处理的 RPC',['应用 / CPU','NIC / 网络','对端 CPU'],['请求序列化','载荷传送','执行并响应']),('CPU 提交的 GPUDirect RDMA',['CPU 提交','NIC ↔ GPU 内存','远端 NIC ↔ GPU'],['提交 / 读取完成状态','数据直达','目标内存写入']),('GPU 经 NVLink 访问',['发起 GPU','NVLink / 交换','对端 GPU 内存'],['设备指令','访问路径','等待访问完成']),('设备发起的 URMA 异步读写',['发起设备 / 队列','UB / 交换','目标设备内存'],['提交 / 处理完成通知','数据路径','写入 / 通知'])]
for i,(title,boxes,notes) in enumerate(rows):
 y=.79-i*.235;panel(a,.015,y+.18,title)
 for j,(t,b) in enumerate(zip(boxes,notes)):box(a,.025+j*.335,y,.285,.12,t,b,size=11)
 for j in range(2):
  ar=FancyArrowPatch((.315+j*.335,y+.075),(.35+j*.335,y+.075),arrowstyle='-|>',mutation_scale=12,color=C['blue'],lw=1.7,linestyle='--' if (i==1 and j==0) else '-');a.add_patch(ar)
 a.annotate('',xy=(.17,y-.04),xytext=(.83,y-.04),arrowprops={'arrowstyle':'->','ls':'--','color':C['muted'],'lw':1});a.text(.50,y-.075,'响应 / 完成与同步关系',fontsize=9,ha='center',color=C['muted'])
save(f,'figure-7-7-access');data['7-7']={'kind':'conceptual','timing':None,'paths':[x[0] for x in rows]}
# 5: Shared states, retaining relation memory.
f=plt.figure(figsize=(13,8));a=f.add_axes([.04,.58,.92,.37]);a.set(xlim=(0,1),ylim=(0,1));a.axis('off');panel(a,.01,.98,'应用端点与传输状态分离')
for i in range(3):
 y=.63-i*.24;box(a,.015,y,.23,.17,f'应用端点 {i}','独立提交 / 完成',size=11);box(a,.36,y,.23,.17,'关系绑定','目标、权限与身份',size=11);arrow(a,(.25,y+.085),(.35,y+.085));arrow(a,(.60,y+.085),(.735,.42))
box(a,.745,.30,.23,.26,'同目标传输状态','可靠交付 / 拥塞',col='light',size=11)
ss=[calc('connection-states-full')['summary'],calc('connection-states-isolated')['summary']];z=ss[0];vals=np.array([[z['endpoint_bytes'],z['relation_bytes'],z['coupled_transport_bytes']],[z['endpoint_bytes'],z['relation_bytes'],z['shared_transport_bytes']],[ss[1]['endpoint_bytes'],ss[1]['relation_bytes'],ss[1]['shared_transport_bytes']]])/2**20
ax=f.add_axes([.15,.12,.77,.33]);left=np.zeros(3)
for j,(title,col) in enumerate([('端点','blue'),('关系绑定','orange'),('传输状态','teal')]):ax.barh(range(3),vals[:,j],left=left,color=C[col],label=title);left+=vals[:,j]
ax.set(yticks=range(3),yticklabels=['逐关系独占','按目标共享','八类隔离'],xlabel='状态容量 / MiB',xlim=(0,10.4),xticks=[0,2,4,6,8,10]);ax.invert_yaxis();ax.axvline(1,ls='--',color=C['red']);ax.legend(frameon=False,ncol=3,loc='lower right')
for i,v in enumerate(left):ax.text(v+.1,i,f'{v:.2f}',va='center',fontsize=10)
save(f,'figure-7-11-state');data['7-11']={'kind':'saved_calculation','state_MiB':vals.tolist(),'budget_MiB':1}
# 6: Only the effect of an unnecessary ordering dependency.
from matplotlib.patches import Patch
order=calc('operation-ordering-book')
f=plt.figure(figsize=(12,8.5));graph=f.add_axes([.05,.71,.90,.27]);graph.set(xlim=(0,1),ylim=(0,1));graph.axis('off')
for x,t,c in [(.015,'写入 A','pale'),(.26,'恢复 / 可见','sand'),(.505,'通知 B','pale'),(.75,'独立传输 C','light')]:box(graph,x,.32,.20,.34,t,col=c,size=11)
arrow(graph,(.22,.49),(.252,.49));arrow(graph,(.465,.49),(.497,.49))
graph.add_patch(FancyArrowPatch((.71,.49),(.744,.49),arrowstyle='-|>',mutation_scale=12,color=C['red'],lw=1.5,ls='--'))
graph.text(.365,.83,'写入后才能通知',ha='center',fontsize=12,color=C['teal']);graph.text(.82,.12,'额外的等待关系',ha='center',fontsize=11,color=C['red'])
ax=f.add_axes([.18,.11,.77,.50])
colors={'write_data':'blue','recover_and_make_visible':'orange','publish_notification':'red','independent_transfer':'teal'};task_names={'write_data':'写入','recover_and_make_visible':'恢复','publish_notification':'通知','independent_transfer':'独立传输'}
for i,key in enumerate(['strict','necessary_dependencies']):
 for task in order['request_schedules'][key]['tasks']:
  row=3-i*2-(.55 if task['id']=='independent_transfer' else 0)
  ax.broken_barh([(task['start_ns']/1000,task['duration_ns']/1000)],(row-.15,.3),facecolors=C[colors[task['id']]])
 ax.text(-3,2.75-i*2,['全部依次执行','仅保留必要依赖'][i],ha='right',va='center',fontsize=11)
 ax.text([112,10][i]+1,2.45-i*2,f'{[112,10][i]} μs',va='center',color=C['teal'])
ax.set(xlim=(0,126),ylim=(0,3.6),yticks=[],xlabel='时间 / μs',xticks=[0,20,60,100,112]);ax.legend(handles=[Patch(color=C[v],label=task_names[k]) for k,v in colors.items()],frameon=False,ncol=4,loc='upper center',bbox_to_anchor=(.5,1.12))
save(f,'figure-7-12-ordering');data['7-12']={'kind':'saved_calculation','schedules':{k:order['request_schedules'][k] for k in ['strict','necessary_dependencies']},'stale_read_example':order['stale_read_example'],'necessary_edges':[['write_data','recover_and_make_visible'],['recover_and_make_visible','publish_notification']],'extra_edge':['publish_notification','independent_transfer'],'plotted':'dependency graph and schedules; stale_read_example supports prose'}

# 7: One cause/effect pair with the same time axis and inputs.
f,axs=plt.subplots(2,1,sharex=True,figsize=(10,7));f.subplots_adjust(left=.13,right=.95,top=.9,bottom=.1,hspace=.18)
queue_data={}
for name,label,col,ls in [('periodic-queue-aligned','重叠 20 ms','blue','-'),('periodic-queue-drift','重叠 5 ms','orange',':'),('periodic-queue-staggered','不重叠','teal','--')]:
 z=calc(name);queue_data[name]=z['queue_segments'];tt=[];qq=[];rr=[]
 for seg in z['queue_segments']:
  tt.extend([seg['start_ns']/1e6,seg['end_ns']/1e6]);qq.extend([seg['queue_start_bytes']/1e6,seg['queue_end_bytes']/1e6]);rr.extend([seg['arrival_bytes_per_second']/1e9]*2)
 axs[0].plot(tt,rr,c=C[col],ls=ls,label=label,lw=2);axs[1].plot(tt,qq,c=C[col],ls=ls,lw=2)
axs[0].axhline(50,c=C['red'],ls='--',lw=1);axs[0].text(44,53,'出口 50 GB/s',color=C['red'],fontsize=10)
axs[0].set(ylim=(-3,96),ylabel='到达速率 / GB/s');axs[0].legend(frameon=False,ncol=3,loc='upper center',bbox_to_anchor=(.5,1.23))
axs[1].set(xlim=(0,60),ylim=(-20,1120),xlabel='时间 / ms',ylabel='积压 / MB');axs[1].text(21,1010,'1000 MB',color=C['blue']);axs[1].text(21,260,'250 MB',color=C['orange'])
packet_data={name:calc(name)['receive_events'] for name in ['packet-reorder-balanced','packet-reorder-skewed','packet-reorder-loss']}
save(f,'figure-7-15-congestion');data['7-15']={'kind':'saved_calculation','periodic_segments':queue_data,'feedback':calc('feedback-queue-overflow'),'packets':packet_data,'plotted':'periodic_segments only; feedback and packets support prose'}

# 8: Resource dependency cycles, not physical topology cycles.
f,a=canvas(6);panel(a,.015,.98,'导致循环等待的资源依赖');panel(a,.53,.98,'预留响应资源，规定申请次序')
xy=[(.04,.63),(.30,.63),(.30,.19),(.04,.19)]
for i,(x,y) in enumerate(xy):box(a,x,y,.15,.18,f'资源 {chr(65+i)}',size=12)
arrow(a,(.195,.72),(.29,.72),'red');arrow(a,(.375,.625),(.375,.385),'red');arrow(a,(.295,.28),(.20,.28),'red');arrow(a,(.115,.385),(.115,.625),'red')
a.text(.245,.495,'持有前一项\n等待后一项',ha='center',va='center',fontsize=11,color=C['red'])
for i,(t,b) in enumerate([('请求资源','按次序申请'),('执行资源','处理数据'),('响应资源','预留缓冲 / 优先发送')]):
 y=.66-i*.25;box(a,.60,y,.31,.17,t,b,col='light',size=12)
 if i<2:arrow(a,(.755,y-.005),(.755,y-.07))
a.text(.755,.03,'响应到达后释放原请求资源',ha='center',fontsize=10,color=C['muted'])
save(f,'figure-7-18-deadlock');data['7-18']={'kind':'conceptual_resource_graph','cycle':['A','B','C','D','A'],'acyclic':['request','execution','response']}
# 9: Only readiness versus exchange on one shared clock.
f,ax=plt.subplots(figsize=(11,6.5));f.subplots_adjust(left=.21,right=.96,top=.86,bottom=.13);ready=[0,0,0,2]
for group,(label,rd,ex) in enumerate([('原始',ready,.4),('交换减半',ready,.2),('消除就绪偏差',[0]*4,.4)]):
 base=10-group*4
 for r,t in enumerate(rd):
  y=base-r*.55;ax.broken_barh([(0,t)],(y-.17,.32),facecolors='#dbe2e6');ax.broken_barh([(t,max(rd)-t)],(y-.17,.32),facecolors='#f6e3c9');ax.broken_barh([(max(rd),ex)],(y-.17,.32),facecolors=C['blue']);ax.scatter([t],[y],s=12,color=C['ink'],zorder=3)
 ax.text(-.08,base-.75,label,ha='right',va='center',fontsize=11)
 ax.text(max(rd)+ex+.04,base-.75,f'{max(rd)+ex:.1f} ms',va='center',color=C['blue'])
ax.set(xlim=(0,2.85),xticks=[0,.5,1,1.5,2,2.5],ylim=(-.4,11),yticks=[],xlabel='时间 / ms');ax.legend(handles=[Patch(color='#dbe2e6',label='尚未就绪'),Patch(color='#f6e3c9',label='等待其他参与者'),Patch(color=C['blue'],label='交换')],ncol=3,frameon=False,loc='upper center',bbox_to_anchor=(.5,1.15))
sizes=np.array([8192,8*2**20]);ring=np.array([14*5e-6+1.75*sizes/b for b in [50e9,150e9]])*1e6
meas=read('experiments/ch07/07-10/rank-readiness/results/summary.json');m=[z for z in meas if z['bytes']==4096]
save(f,'figure-7-19-progress');data['7-19']={'kind':'teaching','ready_ms':ready,'exchange_ms':.4,'ring_us':ring.tolist(),'measured':m,'plotted':'ready_ms and exchange_ms only; ring and CPU observations support prose'}

exec(compile((HERE/'visuals.inc.py').read_text(),str(HERE/'visuals.inc.py'),'exec'))

from models import compute
(HERE/'teaching-data.json').write_text(json.dumps(compute(ROOT),ensure_ascii=False,indent=2)+'\n')
(HERE/'figure-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(HERE/'figure-layout-check.json').write_text(json.dumps({'text_extent_warnings':layout},ensure_ascii=False,indent=2)+'\n')
import sys
sys.path.insert(0,str(HERE.parent))
from ub_ep_figures import draw as draw_ub_ep
outputs += draw_ub_ep(7, HERE)
from teaching_revision import draw as draw_teaching
teaching_outputs,teaching_checks=draw_teaching(HERE,data)
outputs=list(dict.fromkeys(outputs+teaching_outputs))
exec(compile((HERE/'render.inc.py').read_text(),str(HERE/'render.inc.py'),'exec'))
