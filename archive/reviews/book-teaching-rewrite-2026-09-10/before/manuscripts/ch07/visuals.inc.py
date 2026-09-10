"""Mechanism figures for the chapter's existing worked examples.
Executed by build.py with its plotting helpers and source loader.
"""
from models import compute
teaching=compute(ROOT)
# 4: Follow one microbatch diagonally; read utilization horizontally.
f,ax=plt.subplots(figsize=(11,4.8));f.subplots_adjust(left=.12,right=.97,top=.84,bottom=.17)
shade=plt.get_cmap('Blues')
for stage in range(4):
 ax.broken_barh([(0,11)],(stage-.36,.72),facecolors='#f0f2f3')
 for mb in range(8):
  t=stage+mb;ax.add_patch(Rectangle((t,stage-.36),1,.72,fc=shade(.28+mb*.065),ec='white'))
  ax.text(t+.5,stage,str(mb+1),ha='center',va='center',fontsize=12,color=C['ink'] if mb<5 else 'white')
ax.set(xlim=(0,11),ylim=(3.7,-.7),xticks=range(12),yticks=range(4),yticklabels=[f'阶段 {i+1}' for i in range(4)],xlabel='时间 / ms')
ax.set_title('同一微批依次通过四个阶段；不同微批可以同时计算',pad=18,fontsize=14)
ax.text(1,3,'启动时空闲',ha='center',va='center',fontsize=10,color=C['muted']);ax.text(9.5,0,'结束时空闲',ha='center',va='center',fontsize=10,color=C['muted'])
save(f,'figure-7-4-pipeline');data['7-4']={'kind':'derived teaching','stages':4,'microbatches':8,'stage_ms':1,'start_ms':[[i+j for j in range(8)] for i in range(4)],'finish_ms':11}
# 5: The same bytes meet independent or shared ingress resources.
f,a=canvas(8)
for row,(title,mode,result) in enumerate([('集中到一个接收端','single','约 1.34 ms'),('均分到四个独立接收端','independent','约 0.34 ms'),('四张网卡共用入口','shared','约 0.84 ms')]):
 y=.75-row*.32;panel(a,.015,y+.22,title);box(a,.02,y,.17,.13,'分派数据','合计 32 MiB',size=11)
 if mode=='single':
  box(a,.41,y,.23,.13,'NIC：25 GB/s','接收 32 MiB',size=11);arrow(a,(.20,y+.065),(.40,y+.065))
 else:
  if mode=='shared':
   box(a,.25,y,.17,.13,'共享入口','40 GB/s',col='sand',size=11);arrow(a,(.20,y+.065),(.24,y+.065));origin=(.43,y+.065)
  else:origin=(.20,y+.065)
  for j in range(4):
   yy=y-.015+j*.048
   a.add_patch(Rectangle((.54,yy),.20,.037,fc=C['light'],ec=C['line']))
   a.text(.64,yy+.0185,f'NIC {j}：8 MiB',ha='center',va='center',fontsize=9)
   arrow(a,origin,(.535,yy+.0185),lw=1)
  a.text(.64,y-.05,'每张 25 GB/s',ha='center',fontsize=10)
 box(a,.80,y,.17,.13,result,'接收阶段下界',col='sand',size=13)
save(f,'figure-7-5-expert');data['7-5']={'kind':'derived teaching','payload_bytes':32*2**20,'receiver_count':[1,4,4],'effective_Bps':[25e9,100e9,40e9],'lower_ms':[32*2**20/b*1000 for b in [25e9,100e9,40e9]]}
# 6: Trace forks and merges before applying min and sum.
f,a=canvas(5.2);panel(a,.02,.98,'并行路径可以相加；串联路径由较慢的一段限制')
box(a,.02,.40,.15,.17,'源 GPU',size=13)
box(a,.30,.70,.22,.14,'直接连接的 NIC','40 GB/s',col='light',size=11)
box(a,.25,.13,.24,.17,'本地 GPU 互联','剩余 60 GB/s',col='sand',size=11)
box(a,.57,.13,.19,.17,'相邻 NIC × 2','合计 80 GB/s',size=11)
box(a,.81,.42,.17,.18,'下游路径','网络与接收端',size=12)
arrow(a,(.175,.53),(.30,.74));arrow(a,(.175,.44),(.25,.24));arrow(a,(.50,.215),(.56,.215));arrow(a,(.53,.76),(.81,.55));arrow(a,(.765,.24),(.83,.415))
a.text(.64,.82,'最多 40 GB/s',ha='center',color=C['teal'],fontsize=11)
a.text(.60,.05,'中继路径最多 60 GB/s',ha='center',color=C['orange'],fontsize=11)
a.text(.50,.48,'汇合前合计最多 100 GB/s',ha='center',fontsize=12)
save(f,'figure-7-6-relay');data['7-6']={'kind':'derived teaching','direct_GBs':40,'local_remaining_GBs':60,'relay_nics_GBs':80,'pre_downstream_GBs':100}
# 8: Network crossing once per read versus once per snapshot, then cumulative cost.
f=plt.figure(figsize=(12,8));a=f.add_axes([.035,.66,.93,.31]);a.set(xlim=(0,1),ylim=(0,1));a.axis('off')
for i,title in enumerate(['每次直接远读','搬回一次，本地复用']):
 y=.59-i*.48;a.text(.01,y+.28,title,fontsize=12,weight='bold');box(a,.02,y,.21,.20,'远端快照',size=11);box(a,.51,y,.20,.20,'本地副本' if i else '本地计算',size=11)
 arrow(a,(.24,y+.10),(.50,y+.10),'orange');a.text(.37,y+.21,'只跨网络一次' if i else '每次都跨网络',ha='center',fontsize=10,color=C['orange'])
 box(a,.79,y,.19,.20,'重复读取' if i else '下一次再请求',size=10);arrow(a,(.72,y+.10),(.78,y+.10))
r=teaching['snapshot'];record={}
for idx,(fraction,limit,title) in enumerate([(1,4,'每次读取全部快照'),(.1,22,'每次只读取 10%')]):
 ax=f.add_axes([.09+idx*.49,.12,.38,.42]);xs=np.linspace(0,limit,200);remote=xs*r['remote_per_read_s']*fraction*1000;stage=(r['setup_s']+xs*r['local_per_read_s']*fraction)*1000
 ax.plot(xs,remote,c=C['orange'],label='每次远读',lw=2);ax.plot(xs,stage,c=C['teal'],label='先搬回',lw=2)
 cross=r['setup_s']/(fraction*(r['remote_per_read_s']-r['local_per_read_s']));cy=cross*r['remote_per_read_s']*fraction*1000
 ax.scatter([cross],[cy],c=C['ink'],s=24,zorder=4);ax.annotate(f'约 {cross:.1f} 次',xy=(cross,cy),xytext=(cross*.48,cy+2.2),arrowprops={'arrowstyle':'->','color':C['muted']},fontsize=11)
 ax.set(xlim=(0,limit),ylim=(0,16 if idx==0 else 10),xlabel='读取次数',ylabel='累计耗时 / ms',title=title);ax.legend(frameon=False,loc='upper left')
 record[title]={'fraction':fraction,'crossover':cross,'remote_per_read_ms':r['remote_per_read_s']*fraction*1000,'local_per_read_ms':r['local_per_read_s']*fraction*1000,'setup_ms':r['setup_s']*1000}
save(f,'figure-7-8-snapshot');data['7-8']={'kind':'derived from saved snapshot costs','cases':record}
# 9: Show idle space in time, then distinguish the submission cap.
f=plt.figure(figsize=(11,8));ax=f.add_axes([.17,.65,.77,.25]);periods={}
for y,n in [(1,128),(0,313)]:
 duration=n*256/40e9*1e6;period=max(2,duration);segments=[]
 t=0
 while t<4:
  segments.append((t,min(duration,4-t)));t+=period
 ax.broken_barh([(0,4)],(y-.17,.34),facecolors='#eef0f2');ax.broken_barh(segments,(y-.17,.34),facecolors=C['blue']);periods[str(n)]={'send_batch_us':duration,'cycle_us':period,'segments_us':segments}
ax.set(xlim=(0,4),ylim=(-.6,1.6),yticks=[1,0],yticklabels=['128 个槽位','313 个槽位'],xlabel='时间 / μs',xticks=[0,.82,2,2.82,4]);ax.set_title('槽位还未释放时，链路已经无数据可发',pad=16,fontsize=13)
ax.text(1.42,1,'等待槽位',ha='center',va='center',fontsize=10);ax.text(3.4,1,'等待槽位',ha='center',va='center',fontsize=10)
ax=f.add_axes([.12,.12,.82,.36]);ns=np.arange(1,401);bound=np.minimum(40,ns*256/2e-6/1e9)
ax.plot(ns,bound,c=C['blue'],lw=2,label='只考虑在途数量与链路限制');ax.plot(ns,np.minimum(bound,2.56),c=C['orange'],lw=2,label='再加上每 100 ns 启动一项的限制');ax.axhline(40,c=C['muted'],ls=':',lw=1)
for n,val in [(128,16.384),(313,40)]:ax.scatter([n],[val],c=C['blue'],s=22);ax.text(n+7,val-3,f'{n} 项：约 {val:.1f} GB/s',fontsize=10)
ax.set(xlim=(0,400),ylim=(0,48),xlabel='同时使用的请求槽位数',ylabel='吞吐上界 / GB/s');ax.legend(frameon=False,loc='upper left',fontsize=10)
save(f,'figure-7-9-window');data['7-9']={'kind':'derived teaching','transaction_bytes':256,'lifetime_us':2,'bandwidth_GBs':40,'submission_cap_GBs':2.56,'periods':periods}
# 10: Different owners release different buffers at different times.
f,ax=plt.subplots(figsize=(11,4.8));f.subplots_adjust(left=.18,right=.95,top=.82,bottom=.18)
ax.broken_barh([(0,5)],(1.7,.5),facecolors=C['blue']);ax.broken_barh([(5,9)],(1.7,.5),facecolors=C['light'])
ax.broken_barh([(0,8)],(.7,.5),facecolors='#f6e3c9');ax.broken_barh([(8,4)],(.7,.5),facecolors=C['orange']);ax.broken_barh([(12,2)],(.7,.5),facecolors=C['light'])
for x,y,t in [(2.5,1.95,'发送中'),(9.5,1.95,'源缓冲可复用'),(4,.95,'目的缓冲保留'),(10,.95,'接收方使用')]:ax.text(x,y,t,ha='center',va='center',fontsize=11)
ax.plot([6,6],[.2,1.35],color=C['red'],lw=1.5);ax.scatter([6],[.95],marker='x',s=75,c=C['red']);ax.text(6,.04,'6 μs 覆盖：新数据会替换旧数据',ha='center',fontsize=10,color=C['red'])
ax.set(xlim=(0,14),ylim=(-.2,2.6),yticks=[1.95,.95],yticklabels=['源缓冲区','目的缓冲区'],xticks=[0,5,8,12,14],xlabel='时间 / μs',title='发送完成后，接收方可能还没有开始使用数据')
save(f,'figure-7-10-lifetime');data['7-10']={'kind':'teaching ownership timeline','source_reusable_us':5,'consumer_start_us':8,'destination_reusable_us':12,'incorrect_overwrite_us':6}
# 13: Sampling and delivery are two different events.
f,ax=plt.subplots(figsize=(11,5.5));f.subplots_adjust(left=.22,right=.94,top=.86,bottom=.15)
ax.broken_barh([(0,2)],(2.8,.4),facecolors='#e2e8eb');ax.broken_barh([(2,4.5)],(2.8,.4),facecolors=C['light']);ax.text(1,3,'D = 0',ha='center',va='center');ax.text(4.2,3,'D = 1',ha='center',va='center')
ax.scatter([3],[2.2],c=C['teal'],s=45);ax.text(3.12,2.2,'就绪标志可见',va='center',fontsize=11)
ax.plot([1,5],[1.3,1.3],c=C['red'],lw=2);ax.scatter([1],[1.3],c=C['red'],s=50,zorder=3);ax.scatter([5],[1.3],facecolors='white',edgecolors=C['red'],s=65,zorder=3);ax.text(1,1.58,'取到 0',ha='center',fontsize=10);ax.text(5,1.58,'仍交付 0',ha='center',fontsize=10)
ax.scatter([4],[.45],c=C['ink'],s=35);ax.plot([4,6],[.45,.45],c=C['teal'],lw=2);ax.scatter([6],[.45],facecolors='white',edgecolors=C['teal'],s=65,zorder=3);ax.text(4,.13,'检查后重读',ha='center',fontsize=10);ax.text(6,.13,'得到 1',ha='center',fontsize=10)
ax.set(xlim=(0,6.7),ylim=(-.1,3.6),xticks=range(7),yticks=[3,2.2,1.3,.45],yticklabels=['远端数据','发布通知','只调整交付顺序','检查并重读'],xlabel='时间 / μs',title='晚交付不会把已取到的旧值变成新值')
save(f,'figure-7-13-stale');data['7-13']={'kind':'saved example events','sample_us':1,'update_us':2,'flag_visible_us':3,'flag_read_us':4,'stale_delivery_us':5,'repaired_delivery_us':6}
# 14: Every row is a request, orange remains occupied after transfer finishes.
f,axs=plt.subplots(2,1,sharex=True,figsize=(11,9));f.subplots_adjust(left=.12,right=.94,top=.91,bottom=.09,hspace=.38);rec={}
for ax,name,title in zip(axs,['completion-reclaim-book','completion-reclaim-more-slots'],['8 个槽位：后续提交等待回收','16 个槽位：提前传完，仍需等待回收']):
 z=calc(name);ops=z['completion_operations'];rec[name]=ops
 for op in ops:
  i=op['operation'];start=op['submit_ns']/1000;done=op['transfer_complete_ns']/1000;free=op['completion_consumed_ns']/1000
  ax.broken_barh([(start,done-start)],(i-.35,.7),facecolors=C['blue']);ax.broken_barh([(done,free-done)],(i-.35,.7),facecolors='#eac799')
 for t in [20,40,60,80]:ax.axvline(t,c=C['line'],ls=':',lw=1)
 ax.set(ylim=(15.8,-.8),yticks=[0,3,7,11,15],yticklabels=[1,4,8,12,16],ylabel='请求编号',title=title,xlim=(0,82),xticks=[0,20,40,48,60,80])
axs[0].legend(handles=[Patch(color=C['blue'],label='传输中'),Patch(color='#eac799',label='传完，等待处理完成通知')],ncol=2,frameon=False,loc='upper center',bbox_to_anchor=(.5,1.30),fontsize=11)
axs[1].set_xlabel('时间 / μs');save(f,'figure-7-14-reclaim');data['7-14']={'kind':'saved events','operations':rec}
# 16: Finite buffer plateau and the delayed control action.
f=plt.figure(figsize=(11,7));a=f.add_axes([.04,.71,.92,.24]);a.set(xlim=(0,1),ylim=(0,1));a.axis('off')
box(a,.01,.30,.21,.38,'发送端','80 → 40 GB/s',size=12);box(a,.39,.30,.25,.38,'512 KiB 缓冲','初始已有 256 KiB',col='sand',size=12);box(a,.80,.30,.19,.38,'出口','50 GB/s',size=12);arrow(a,(.23,.49),(.38,.49));arrow(a,(.65,.49),(.79,.49));a.annotate('',xy=(.12,.22),xytext=(.51,.22),arrowprops={'arrowstyle':'->','ls':'--','color':C['red']});a.text(.32,.01,'反馈到 20 μs 才生效',ha='center',fontsize=10,color=C['red'])
ax=f.add_axes([.12,.12,.82,.48]);fb=calc('feedback-queue-overflow');tt=[];qq=[]
for seg in fb['queue_segments']:tt.extend([seg['start_ns']/1000,seg['end_ns']/1000]);qq.extend([seg['queue_start_bytes']/1024,seg['queue_end_bytes']/1024])
ax.plot(tt,qq,c=C['orange'],lw=2.5);ax.fill_between(tt,qq,color=C['sand']);ax.axvspan(256*1024/30e9*1e6,20,color=C['red'],alpha=.14);ax.axvline(20,c=C['red'],ls='--',lw=1);ax.text(22,535,'降速至 40 GB/s',fontsize=10,color=C['red']);ax.text(14.4,580,'满缓冲，超额数据丢弃',ha='center',fontsize=10,color=C['red']);ax.annotate('约 72 μs 排空',xy=(72.4288,0),xytext=(49,130),arrowprops={'arrowstyle':'->','color':C['muted']},fontsize=11)
ax.set(xlim=(0,82),ylim=(0,640),xticks=[0,8.7,20,40,60,72.4,80],yticks=[0,256,512],xlabel='时间 / μs',ylabel='队列占用 / KiB')
save(f,'figure-7-16-feedback');data['7-16']={'kind':'saved segments','queue_segments':fb['queue_segments'],'feedback_us':20}
# 17: Arrival is a dot; ordered delivery is the end of the horizontal wait.
f,axs=plt.subplots(2,1,sharex=True,figsize=(11,8));f.subplots_adjust(left=.12,right=.94,top=.92,bottom=.10,hspace=.38);pack={}
for ax,name,title in zip(axs,['packet-reorder-balanced','packet-reorder-skewed'],['两条路径均为 1 μs：约 5.1 μs 全部交付','传播时延为 1 / 9 μs：约 13.1 μs 全部交付']):
 z=calc(name);delivery={v['sequence']:float(Fraction(v['delivery_exact_ns']))/1000 for v in z['delivery']}
 for tr in z['transmissions']:
  seq=tr['sequence'];arr=float(Fraction(tr['arrival_exact_ns']))/1000;end=delivery[seq];col=C['teal'] if tr['path']==0 else C['orange']
  ax.plot([arr,end],[seq,seq],color=col,lw=4,alpha=.6);ax.scatter([end],[seq],marker='|',s=110,c=col);ax.scatter([arr],[seq],s=40,c=col,zorder=4)
 ax.set(ylim=(7.8,-.8),yticks=range(8),ylabel='报文序号',title=title,xlim=(0,14),xticks=[0,2,4,6,8,10,12,14]);pack[name]={'transmissions':z['transmissions'],'delivery':z['delivery']}
axs[0].text(8.2,2,'圆点：到达\n横线：等待前方缺口\n竖线：按序交付',fontsize=11,linespacing=1.6)
axs[1].set_xlabel('时间 / μs');save(f,'figure-7-17-packets');data['7-17']={'kind':'saved packet events','cases':pack}
# 20: Preserve a common time scale and show the dependency of update on both rows.
f,ax=plt.subplots(figsize=(12,9));f.subplots_adjust(left=.22,right=.94,top=.91,bottom=.10);p=teaching['primary'];st=teaching['step']
cases=[('连续环，串行',20,p['flat_s']*1000),('分层归约，串行',20,p['hier_s']*1000),('分层，只有 128 项在途',20,st['hier_window_limited_comm_s']*1000),('分层，17 ms 就绪',17,p['hier_s']*1000),('分层，12 ms 就绪',12,p['hier_s']*1000),('分层，出口降至 20 GB/s',17,st['hier_slow_comm_s']*1000)];steps=[]
for i,(label,ready,comm) in enumerate(cases):
 y=10-i*1.8;update=max(20,ready+comm);end=update+2
 ax.broken_barh([(0,20)],(y,.40),facecolors='#dbe2e6');ax.broken_barh([(ready,comm)],(y-.48,.34),facecolors=C['blue']);ax.broken_barh([(update,2)],(y,.40),facecolors=C['teal']);ax.scatter([ready],[y-.31],c=C['ink'],s=20,zorder=4)
 ax.plot([ready+comm,update],[y-.31,y+.2],c=C['line'],lw=1);ax.text(-.8,y-.03,label,ha='right',va='center',fontsize=10);ax.text(end+.3,y+.2,f'{end:.1f} ms',va='center',fontsize=11)
 steps.append({'label':label,'ready_ms':ready,'comm_ms':comm,'update_start_ms':update,'finish_ms':end})
ax.axvline(20,c=C['muted'],ls=':',lw=1);ax.set(xlim=(0,39),ylim=(.1,11),yticks=[],xticks=[0,5,10,15,20,25,30,35],xlabel='时间 / ms');ax.legend(handles=[Patch(color='#dbe2e6',label='计算'),Patch(color=C['blue'],label='通信'),Patch(color=C['teal'],label='更新')],ncol=3,frameon=False,loc='upper center',bbox_to_anchor=(.5,1.09))
save(f,'figure-7-20-step');data['7-20']={'kind':'derived teaching schedules','compute_ms':20,'update_ms':2,'cases':steps}
# 21: Log axes show both the startup floor and payload slope without hiding the small case.
f,ax=plt.subplots(figsize=(11,6.5));f.subplots_adjust(left=.12,right=.94,top=.90,bottom=.15);size=np.geomspace(1024,16*2**20,240);startup=np.full_like(size,70.);payload=1.75*size/25e9*1e6
ax.loglog(size,startup,c=C['orange'],ls=':',lw=1.7,label='启动：14 × 5 μs');ax.loglog(size,payload,c=C['muted'],ls='--',lw=1.7,label='仅载荷：25 GB/s')
ax.loglog(size,startup+payload,c=C['blue'],lw=2.4,label='总时间：25 GB/s，5 μs');ax.loglog(size,startup+payload/3,c=C['teal'],lw=2,label='带宽增至 75 GB/s');ax.loglog(size,28+payload,c=C['red'],lw=2,label='每轮启动缩短至 2 μs')
ax.axvline(1e6,c=C['line'],lw=1);ax.text(1.18e6,1.8,'两项相等：1 MB',fontsize=10);ax.text(2500,190,'小消息：启动占主导',fontsize=11);ax.text(1.3e6,1800,'大消息：传输占主导',fontsize=11)
ax.set(xlim=(1024,16*2**20),ylim=(.05,4000),xlabel='每个参与者的输入大小',ylabel='一次环形归约耗时 / μs');ax.set_xticks([1024,8192,65536,2**20,8*2**20],['1 KiB','8 KiB','64 KiB','1 MiB','8 MiB']);ax.legend(frameon=False,loc='lower right',fontsize=10)
save(f,'figure-7-21-message');data['7-21']={'kind':'derived teaching','input_bytes':size.tolist(),'baseline_us':(startup+payload).tolist(),'bandwidth_upgrade_us':(startup+payload/3).tolist(),'startup_upgrade_us':(28+payload).tolist(),'crossover_bytes':1e6}
