"""Additional explanatory figures, executed in build.py's drawing namespace."""
# Stored bytes and unpartitioned workspaces share the same per-device capacity.
f,ax=plt.subplots(figsize=(11,4.2));f.subplots_adjust(left=.17,right=.97,bottom=.18,top=.9)
segments=np.array([[w1,k1,2**31],[w8,k8,2**31]])/1e9
for j,(label,color) in enumerate(zip(['模型权重','KV 状态','每卡工作区'],['blue','teal','orange'])):
 ax.barh([1,0],segments[:,j],left=segments[:,:j].sum(axis=1),height=.48,color=C[color],label=label)
for y,total in zip([1,0],segments.sum(axis=1)):ax.text(total+.3,y,f'{total:.2f} GB',va='center')
ax.axvline(24,color=C['red'],ls='--');ax.text(23.8,1.48,'每卡容量 24 GB',ha='right',color=C['red'])
ax.set(yticks=[1,0],yticklabels=['单卡部署','八卡 TP 中的每卡'],xlim=(0,26),xticks=[0,5,10,15,20,24],ylim=(-.65,1.7),xlabel='每卡内存占用 / GB');ax.legend(loc='lower left',frameon=False,ncol=3,fontsize=10)
save(f,'capacity');data['capacity_plot']={'segments_GB':segments.tolist(),'capacity_GB':24}
# Rows and columns show which results are combined, and which KV is repeated.
f,a=canvas(7.6)
a.text(.04,.965,'每行：一个专家组，两卡 TP',fontsize=14,va='top')
a.text(.59,.965,'每列：四个专家组之间归约',fontsize=14,va='top',color=C['orange'])
for ep in range(4):
 y=.74-ep*.205
 a.text(.018,y+.06,f'EP {ep}\n专家 {ep*32}—{ep*32+31}',va='center',fontsize=11)
 for tp in range(2):
  x=.21+tp*.43
  box(a,x,y,.28,.15,f'卡 {2*ep+tp}：专家矩阵'+('左半' if tp==0 else '右半'),f'同一请求 KV 头 '+('0、1' if tp==0 else '2、3'),col='light' if tp==0 else 'pale',size=11)
 a.annotate('',xy=(.635,y+.075),xytext=(.495,y+.075),arrowprops={'arrowstyle':'<->','color':C['teal'],'lw':1.5})
 if ep==0:a.text(.565,y+.12,'① TP 求和',ha='center',fontsize=10,color=C['teal'])
for x in [.35,.78]:
 for ep in range(3):a.annotate('',xy=(x,.74-(ep+1)*.205+.155),xytext=(x,.74-ep*.205-.005),arrowprops={'arrowstyle':'<->','color':C['orange'],'lw':1.5})
a.text(.975,.40,'② EP\n求和',ha='right',fontsize=11,color=C['orange'])
a.text(.5,.025,'每行重复执行同一请求的 attention；专家计算则由四行分担',ha='center',fontsize=12)
save(f,'ep-layout')
# Same selected experts, distinct placement: preserves total work and reuse.
f,axs=plt.subplots(1,3,figsize=(13,4.3),sharey=True);f.subplots_adjust(left=.08,right=.98,bottom=.23,top=.8,wspace=.16)
loads=[[128]*4,[512,0,0,0],[128]*4]
for ax,vals,title,detail in zip(axs,loads,['均匀选择 128 个专家','八个专家集中在一组','同八个专家分散到四组'],['读取 4.5 GiB 权重','读取 288 MiB 权重','读取 288 MiB 权重']):
 ax.bar(range(4),vals,color=[C['blue'],C['teal'],C['orange'],C['muted']])
 for i,v in enumerate(vals):ax.text(i,v+12,str(v),ha='center',fontsize=11)
 ax.set(xticks=range(4),xticklabels=['EP 0','EP 1','EP 2','EP 3'],ylim=(0,600),xlabel=detail);ax.set_title(title,fontsize=12)
axs[0].set_ylabel('每组 token—专家计算次数')
save(f,'expert-load');data['expert_load']={'tasks':loads,'reads_bytes':[4.5*2**30,288*2**20,288*2**20]}
# A bar is a whole dependent decode step, not three unrelated metrics.
f,ax=plt.subplots(figsize=(11,4.7));f.subplots_adjust(left=.10,right=.98,bottom=.16,top=.86)
steps=continuous['first_steps'];ys=np.arange(4)[::-1];left=np.zeros(4)
for key,label,color in [('local_s','本地内存访问','blue'),('communication_s','72 次归约','orange'),('serial_s','其他串行处理','muted')]:
 vals=np.array([x[key]*1000 for x in steps]);ax.barh(ys,vals,left=left,height=.55,color=C[color],label=label);left+=vals
for y,t in zip(ys,left):ax.text(t+.15,y,f'{t:.2f} ms',va='center')
ax.set(yticks=ys,yticklabels=['TP 1','TP 2','TP 4','TP 8'],xlim=(0,18.4),xticks=[0,2.5,5,7.5,10,12.5,15,17.5],xlabel='一次 decode 的执行时间 / ms');ax.legend(loc='upper center',bbox_to_anchor=(.5,1.18),ncol=3,frameon=False)
save(f,'tp-time')
# Ports are discrete resources; the same 32 slots must be split between directions.
f,a=canvas(5.8)
for y,down,up in [(.62,16,16),(.18,24,8)]:
 box(a,.015,y,.21,.23,f'{down} 个设备端口',f'总输入 {down*50} GB/s',col='light')
 box(a,.77,y,.215,.23,f'{up} 个上联端口',f'总带宽 {up*50} GB/s',col='sand')
 arrow(a,(.23,y+.12),(.30,y+.12));arrow(a,(.70,y+.12),(.76,y+.12),'orange')
 a.text(.5,y+.27,f'32 个端口：{down} 下联 / {up} 上联',ha='center',fontsize=13)
 for i in range(32):
  row=i//16;col=i%16
  a.add_patch(Rectangle((.305+col*.024,y+.145-row*.09),.019,.06,fc=C['teal' if i<down else 'orange']))
a.text(.5,.045,'端口总数固定：多接设备，就会减少上联带宽',ha='center',fontsize=13)
save(f,'ports');data['port_split']={'total_ports':32,'splits':[[16,16],[24,8]],'port_GBs':50}
# Show the two cut surfaces of a torus using k x k planes, then compare growth.
f=plt.figure(figsize=(13,5.3));a=f.add_axes([.025,.13,.53,.77]);a.set(xlim=(0,1),ylim=(0,1));a.axis('off')
for x,label in [(.05,'左半部'),(.57,'右半部')]:
 box(a,x,.28,.36,.42,'',col='light' if x<.5 else 'pale',size=13)
 a.text(x+.18,.64,label,ha='center',fontsize=12)
 for i in range(3):
  for j in range(3):a.plot(x+.09+i*.09,.37+j*.08,'o',color=C['blue'],ms=5)
arrow(a,(.415,.50),(.56,.50),'orange');a.text(.49,.59,'中间切面\nk² 条链路',ha='center',fontsize=11,color=C['orange'])
# Wrap-around connections meet the other cut surface.
a.plot([.09,.09,.88,.88],[.28,.13,.13,.28],color=C['teal'],lw=2)
a.text(.49,.04,'首尾连接：另有 k² 条链路',ha='center',fontsize=12,color=C['teal'])
a.text(.49,.89,'沿一个维度分成两半',ha='center',fontsize=14)
ax=f.add_axes([.67,.23,.30,.56]);xx=np.arange(2)
ax.bar(xx-.17,[1,8],.32,color=C['blue'],label='设备数')
ax.bar(xx+.17,[1,4],.32,color=C['orange'],label='二分链路数')
for x,y,t in [(-.17,1,'64'),(.17,1,'32'),(.83,8,'512'),(1.17,4,'128')]:ax.text(x,y+.18,t,ha='center',fontsize=11)
ax.set(xticks=xx,xticklabels=['k = 4','k = 8'],ylim=(0,10),ylabel='相对 k = 4 的倍数');ax.legend(frameon=False,loc='upper left',fontsize=10)
save(f,'torus');data['torus_cut']={'k':[4,8],'devices':[64,512],'cut_links':[32,128]}
# Physical placement: never draw an 80 GiB resident bar in a 64 GiB node.
f,axs=plt.subplots(1,2,figsize=(12,5),sharey=True);f.subplots_adjust(left=.09,right=.97,bottom=.16,top=.82,wspace=.2)
for ax,title in zip(axs,['借用前：任务 0 还缺 16 GiB','借用后：16 GiB 保存在节点 1']):
 ax.bar(range(4),[64]*4,color='white',edgecolor=C['line'],width=.65)
 ax.set(xticks=range(4),xticklabels=['节点 0','节点 1','节点 2','节点 3'],ylim=(0,89),yticks=[0,16,32,48,64,80]);ax.set_title(title,fontsize=13)
 ax.axhline(64,ls=':',color=C['muted']);ax.text(3.4,65,'容量 64 GiB',ha='right',fontsize=10)
 for i,v in enumerate([64,48,32,32]):ax.bar(i,v,color=C[['blue','teal','orange','muted'][i]],width=.65)
axs[0].add_patch(Rectangle((-.325,64),.65,16,fc='none',ec=C['blue'],ls='--',lw=2));axs[0].text(0,72,'16',ha='center',va='center')
axs[1].bar(1,16,bottom=48,color=C['blue'],width=.65);axs[1].text(1,56,'16',ha='center',va='center',color='white')
axs[1].annotate('任务 0 的远端数据',xy=(1,64),xytext=(1.6,79),arrowprops={'arrowstyle':'->','color':C['blue']},fontsize=11,color=C['blue'])
axs[0].set_ylabel('内存需求与占用 / GiB')
save(f,'pool-placement');data['pool_placement']={'capacity_GiB':64,'before_assigned_GiB':[64,48,32,32],'unassigned_GiB':16,'after_assigned_GiB':[64,64,32,32]}
# Time and space: the empty interval is latency, overlapping arrows are in-flight work.
f,a=canvas(6.5)
a.text(.11,.94,'发出读取请求',ha='center',fontsize=13);a.text(.68,.94,'收到返回数据',ha='center',fontsize=13)
for i in range(4):
 y=.76-i*.155
 box(a,.025,y,.16,.09,f'请求 {i}',size=11)
 arrow(a,(.19,y+.045),(.61,y+.045),'blue')
 box(a,.62,y,.14,.09,'q 字节',col='light',size=11)
 a.text(.38,y+.068,'等待远端返回',ha='center',fontsize=10,color=C['muted'])
a.annotate('',xy=(.18,.16),xytext=(.77,.16),arrowprops={'arrowstyle':'<->','color':C['ink']});a.text(.475,.09,'往返时间 L',ha='center',fontsize=12)
box(a,.81,.36,.17,.28,'在途窗口','u 个请求\n共 uq 字节',col='sand',size=12)
a.text(.48,.015,'窗口带宽上限 = uq / L',ha='center',fontsize=13)
save(f,'read-window');data['read_window']={'illustrated_requests':4,'example_requests':128,'bytes_per_request':256,'latency_s':2e-6}
# Same sessions, different concurrency. Width is service time; rows are instances.
f,axs=plt.subplots(2,2,figsize=(13,7.8),sharex=True);f.subplots_adjust(left=.1,right=.98,bottom=.12,top=.93,hspace=.52,wspace=.24)
for ax,c in zip(axs.flat,continuous['candidates']):
 p=c['tp'];instances=8//p;service=c['service_ms'];shown=min(instances,4)
 for request in range(4):
  instance=request%instances;start=(request//instances)*service
  ax.barh(shown-1-instance,service,left=start,height=.58,color=C[['blue','teal','orange','red'][request]])
  ax.text(start+service/2,shown-1-instance,f'会话 {request}',ha='center',va='center',color='white',fontsize=10)
 ax.axvline(90,color=C['muted'],ls='--',lw=1)
 ax.set(yticks=range(shown),yticklabels=[f'实例 {i}' for i in range(shown-1,-1,-1)],xlim=(0,150),ylim=(-.6,max(shown-.4,1)),xticks=[0,30,60,90,120,150])
 ax.set_title(f'{instances} 个'+('单卡' if p==1 else f'{p} 卡')+'实例'+('（另有四个空闲实例）' if p==1 else ''),fontsize=12,loc='left')
 ax.text(max(c['healthy_completion_ms']),-.42,f"{max(c['healthy_completion_ms']):.1f} ms",ha='right',va='top',fontsize=10)
for ax in axs[1]:ax.set_xlabel('从四个会话同时到达起的时间 / ms')
save(f,'session-schedule')
