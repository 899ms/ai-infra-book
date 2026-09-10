"""Chapter-nine mechanism diagrams. Executed by build.py with its drawing helpers."""

# Three workloads redistribute the same eight workers.
f,a=canvas(5.8)
for y,title,pa,pb,rate in [(.76,'原始请求：8192 输入，129 输出',4,0,'8 请求/s'),(.47,'命中 6144 个前缀位置',2,0,'9 请求/s'),(.18,'输出增至 1025 个 token',1,0,'约 1.19 请求/s')]:
 a.text(.025,y+.14,title,fontsize=12,weight='bold')
 for i in range(8):
  isp=i<pa if i<4 else i-4<pb
  x=.05+i*.10
  a.add_patch(Rectangle((x,y),.082,.10,fc=C['blue'] if isp else C['teal'],ec='white'))
  a.text(x+.041,y+.05,('A' if i<4 else 'B')+(' → P' if isp else ' → D'),ha='center',va='center',fontsize=10,color='white')
 a.text(.88,y+.05,rate,va='center',fontsize=11)
a.text(.05,.02,'蓝色：prefill     绿色：decode',fontsize=11)
save(f,'figure-9-4-allocation')
data['new-allocation']={'prefill_A':[4,2,1],'prefill_B':[0,0,0],'rates':[8,9,19/16]}

# Same task count: each rectangle's area equals rows times active experts.
f,axes=plt.subplots(2,1,figsize=(11,7),sharex=True);f.subplots_adjust(left=.12,right=.97,bottom=.12,top=.92,hspace=.58)
for ax,experts,rows,col,title in [(axes[0],128,4,'blue','均匀覆盖：128 个专家，每个处理 4 行'),(axes[1],8,64,'teal','集中复用：8 个专家，每个处理 64 行')]:
 ax.add_patch(Rectangle((0,0),experts,rows,fc=C[col],alpha=.75))
 ax.set(xlim=(0,128),ylim=(0,70),ylabel='每专家输入行数',yticks=[0,4,32,64])
 ax.set_title(title,loc='left',fontsize=13)
 ax.text(45,43,'矩形面积均为 512 次分派\n矩阵计算均约 19.3 GFLOPs',fontsize=12)
 ax.grid(axis='y',alpha=.15)
axes[0].text(64,12,'读取权重 4.5 GiB',ha='center',fontsize=12,color=C['blue'])
axes[1].text(12,14,'读取权重 288 MiB',fontsize=12,color=C['teal'])
axes[1].set(xlabel='本批访问的专家数',xticks=[0,8,32,64,96,128])
save(f,'figure-9-7-footprint')
data['new-footprint']={'active_experts':[128,8],'rows_per_expert':[4,64],'weight_MiB':[4608,288],'assignments':512}

# Synchronization waits for the busiest card, with identical total work.
f,axes=plt.subplots(2,1,figsize=(11,7),sharex=True);f.subplots_adjust(left=.12,right=.96,bottom=.12,top=.91,hspace=.50)
for ax,counts,title in [(axes[0],[64]*8,'均匀放置：八张卡同时完成'),(axes[1],[512]+[0]*7,'八个热点专家在同一卡：其余卡等待')]:
 times=np.array(counts)*2*18874368/100e12*1e6
 ax.barh(range(8),times,color=C['teal'],height=.65);ax.invert_yaxis()
 ax.set(yticks=range(8),yticklabels=[f'卡 {i}' for i in range(8)],xlim=(0,225),xticks=[0,50,100,150,200])
 ax.set_title(title,loc='left',fontsize=13);ax.axvline(max(times),color=C['orange'],ls='--')
 ax.text(max(times)+3,3,f'{max(times):.0f} μs\n后可合并',fontsize=11)
 ax.grid(axis='x',alpha=.15)
axes[1].set_xlabel('完成本卡专家计算所需时间 / μs')
save(f,'figure-9-9-balance')
data['new-balance']={'assignments_per_card':[[64]*8,[512]+[0]*7],'effective_TFLOPs':100}

# A schedule rather than a summed bar explains what overlap actually hides.
f,axes=plt.subplots(2,1,figsize=(11,6.6),sharex=True);f.subplots_adjust(left=.15,right=.97,bottom=.12,top=.91,hspace=.65)
schedules=[
 ('串行：1.0 ms',[(0,0,.2,'分派'),(1,.2,.6,'计算'),(2,.8,.2,'合并')]),
 ('两个微批流水：0.8 ms',[(0,0,.1,'1'),(0,.1,.1,'2'),(1,.1,.3,'1'),(1,.4,.3,'2'),(2,.4,.1,'1'),(2,.7,.1,'2')])]
for ax,(title,items) in zip(axes,schedules):
 for row,start,dur,txt in items:
  ax.barh(row,dur,left=start,height=.65,color=C[['blue','teal','orange'][row]],edgecolor='white')
  ax.text(start+dur/2,row,txt,ha='center',va='center',color='white',fontsize=11)
 ax.set(yticks=[0,1,2],yticklabels=['分派','专家计算','结果合并'],xlim=(0,1.05),ylim=(2.6,-.6))
 ax.set_title(title,loc='left',fontsize=13);ax.grid(axis='x',alpha=.15)
axes[1].set(xlabel='时间 / ms',xticks=[0,.2,.4,.6,.8,1.0])
save(f,'figure-9-11-overlap')
data['new-overlap']={'serial_ms':1.0,'pipeline_ms':.8,'slowed_pipeline_ms':1.0}

# Each row is a dependency timeline. Queue and retrieval start together.
f,axes=plt.subplots(4,1,figsize=(11,8.2),sharex=True);f.subplots_adjust(left=.13,right=.97,bottom=.11,top=.94,hspace=.85)
V=1207959552;host=V/25e9*1000
routes=[('A：本地命中',250,None,10),('B：本地重算',20,None,180),('B：远端 5 GB/s',20,5,10),('B：远端 20 GB/s',20,20,10)]
for ax,(title,q,band,c) in zip(axes,routes):
 ax.barh(0,q,color=C['line'],height=.6)
 ready=0
 if band:
  for duration,col in [(10,'muted'),(V/(band*1e9)*1000,'orange'),(host,'blue')]:
   ax.barh(1,duration,left=ready,color=C[col],height=.6,edgecolor='white');ready+=duration
 start=max(q,ready)
 ax.barh(0,c,left=start,color=C['teal'],height=.6)
 ax.axvline(start+c,color=C['teal'],ls=':',alpha=.7)
 ax.text(start+c+3,.2,f'{start+c:.0f} ms',fontsize=11)
 ax.set(yticks=[0,1],yticklabels=['GPU','取回'],ylim=(1.6,-.6),xlim=(0,340),xticks=[0,50,100,150,200,250,300])
 ax.set_title(title,loc='left',fontsize=12);ax.grid(axis='x',alpha=.12)
axes[-1].set_xlabel('从请求到达开始的时间 / ms')
f.text(.14,.025,'灰：排队／查找    橙：远端读取    蓝：主存 → GPU    绿：计算',fontsize=11)
save(f,'figure-9-13-route')
data['new-route']={'first_token_ms':[260,200,10+V/5e9*1000+host+10,10+V/20e9*1000+host+10],'host_ms':host}

# Background copying catches a moving frontier.
f,ax=plt.subplots(figsize=(10,5.5));f.subplots_adjust(left=.12,right=.96,bottom=.17,top=.91)
t=np.linspace(0,1,121);ax.plot(t,1+.5*t,label='源端：原有 1 GiB ＋ 每秒新增 0.5 GiB',color=C['orange'],lw=2.5)
ax.plot(t,np.minimum(2*t,1+.5*t),label='目标：每秒复制 2 GiB',color=C['teal'],lw=2.5)
ax.fill_between(t,2*t,1+.5*t,where=t<=2/3,color=C['pale'])
ax.scatter([2/3],[4/3],color=C['ink']);ax.annotate('约 0.67 s：复制赶上生成',xy=(2/3,4/3),xytext=(.35,.5),fontsize=12,arrowprops={'arrowstyle':'->'})
ax.set(xlabel='后台复制开始后的时间 / s',ylabel='累计状态大小 / GiB',xlim=(0,1),ylim=(0,1.7));ax.legend(frameon=False,loc='upper left',fontsize=10);ax.grid(alpha=.15)
save(f,'figure-9-14-migration')
data['new-migration']={'initial_GiB':1,'copy_GiBs':2,'growth_GiBs':.5,'catchup_s':2/3}

# Token log and KV checkpoint have different ends.
f,a=canvas(6)
for y,title in [(.72,'已返回并记录的序列'),(.43,'故障前保存的 KV'),(.14,'重建后继续生成')]:
 a.text(.025,y+.15,title,fontsize=12,weight='bold')
 box(a,.04,y,.39,.10,'输入：8192 个位置',col='pale',fs=11)
 if y!=.43:
  box(a,.45,y,.32,.10,'已返回输出 1—128',col='green',fs=11)
  box(a,.80,y,.16,.10,'输出 129',col='sand',fs=11)
 else:
  a.text(.47,y+.05,'缺少生成部分的 KV',va='center',fontsize=12,color=C['orange'])
a.text(.46,.32,'将已记录的输出 1—128 重新送入模型',fontsize=11,color=C['teal'])
a.text(.05,.015,'KV 先恢复到 8320 个位置，再处理输出 129，生成下一个 token。',fontsize=12)
save(f,'figure-9-15-recovery')
data['new-recovery']={'input_positions':8192,'delivered_outputs':129,'replayed_outputs':128,'restored_KV_positions':8320}
