"""Concept figures; executed by build.py with its drawing helpers and source data."""
# Serial versus overlapping image work: all segments use the same time scale.
f,a=plot_canvas();f.set_size_inches(12,6)
for y,start,duration,color in [(3,0,12,'blue'),(3,12,.05,'muted'),(3,12.05,.3,'teal'),(3,12.35,.4,'orange'),(3,12.75,.05,'muted')]:
 a.broken_barh([(start,duration)],(y-.19,.38),facecolors=C[color])
for j,(name,col) in enumerate([('上传','blue'),('处理','teal'),('回传','orange'),('传播','muted')]):a.plot([],[],lw=8,color=C[col],label=name)
for i in range(3):
 start=i*4;a.broken_barh([(start,4)],(2-.19,.38),facecolors=C['blue'],edgecolors='white');a.text(start+2,2,f'块 {i+1}',ha='center',va='center',color='white')
 a.broken_barh([((i+1)*4+.05,.1)],(1-.19,.38),facecolors=C['teal'])
 a.broken_barh([((i+1)*4+.15,[.08,.16,.16][i])],(0-.19,.38),facecolors=C['orange'])
 a.plot([(i+1)*4,(i+1)*4+.05],[1.8,1.2],color=C['line'],lw=1)
end=12+.05+.1+.16+.05
a.axvline(12,color=C['line'],ls=':');a.text(12.9,3,'12.8 s',va='center');a.annotate('最后一块决定结束时刻\n约 12.4 s',(end,0),(9,.65),arrowprops={'arrowstyle':'->','color':C['muted']},fontsize=11)
a.text(6,1.2,'前两块的处理与回传发生在后续上传期间',ha='center',fontsize=11)
a.set(xlim=(0,14.5),ylim=(-.5,3.6),yticks=[3,2,1,0],yticklabels=['整图串行','分块上传','分块处理','分块回传'],xlabel='从开始上传起的时间 / s');a.set_xticks([0,4,8,12,14]);a.legend(frameon=False,ncol=4,loc='lower left',bbox_to_anchor=(0,1));a.grid(axis='x',alpha=.15)
save(f,'figure-12-8-overlap');data['12-8']={'kind':'teaching_timeline','serial_s':12.8,'chunk_upload_s':4,'chunk_compute_s':.1,'chunk_return_s':[.08,.16,.16],'one_way_s':.05,'chunked_s':end,'relationship':'依赖改变重叠时间'}
# Buffer conservation.
f,a=plot_canvas();t=np.linspace(0,.245,120);rate=(256000-130000)/1000
for initial,col in [(15.36,'teal'),(30.72,'blue')]:
 until=initial/rate;ts=t[t<=until];ts=np.append(ts,until);a.plot(ts,initial-rate*ts,lw=2.5,color=C[col],label=f'初始 {initial/256*1000:.0f} ms 音频');a.scatter([until],[0],color=C[col]);a.text(until,.9,f'{until:.2f} s',ha='center')
a.text(.13,26,'每秒收到 130 kbit\n每秒播放 256 kbit\n缓冲每秒减少 126 kbit',fontsize=12,linespacing=1.7)
a.set(xlim=(0,.27),ylim=(-1,34),xlabel='开始播放后的时间 / s',ylabel='缓冲中尚未播放的数据 / kbit');a.set_xticks([0,.06,.12,.18,.24]);a.set_yticks([0,10,20,30]);a.grid(alpha=.15);a.legend(frameon=False,loc='upper right')
save(f,'figure-12-9-buffer');data['12-9']={'kind':'teaching_conservation','input_bps':130000,'output_bps':256000,'initial_bits':[15360,30720],'empty_s':[15360/126000,30720/126000],'relationship':'缓冲量由接收与播放之差决定'}
# Closed-loop task dependence; positions represent logical steps, not durations.
f,a=canvas(4.8)
steps=[('截图 v','当前界面'),('上传','0.8 MB'),('模型判断','决定操作'),('执行与更新','生成新界面')]
for i,(title,body) in enumerate(steps):
 x=.035+i*.245;box(a,x,.48,.20,.25,title,body,size=14)
 if i<3:arrow(a,(x+.203,.605),(x+.24,.605))
a.plot([.87,.87,.135,.135],[.47,.25,.25,.47],color=C['teal'],lw=2);arrow(a,(.135,.35),(.135,.48));a.text(.5,.12,'下一轮截图必须等待本轮操作生效',ha='center',fontsize=15);a.text(.5,.90,'一轮完成后，下一轮输入才出现',ha='center',fontsize=17,weight='bold')
save(f,'figure-12-10-agent');data['12-10']={'kind':'dependency_diagram','steps':[x[0] for x in steps],'round_s':3.5,'compressed_round_s':2.78,'rounds':30,'relationship':'操作结果决定下一轮输入'}
# Migration payoff.
f,a=plot_canvas();n=np.arange(0,41);m=64*2**20*8/80e6+1
for extra,col,label in [(0,'teal','恢复 1 s'),(1,'orange','恢复 2 s')]:a.plot(n,n*.4-m-extra,color=C[col],lw=2,label=label)
a.axhline(0,color=C['muted'],lw=1);a.scatter([20,22],[20*.4-m,22*.4-m-1],color=[C['teal'],C['orange']],zorder=4)
a.annotate('第 20 轮开始获益',(20,20*.4-m),(3,5),arrowprops={'arrowstyle':'->','color':C['muted']},fontsize=11);a.annotate('多恢复 1 s → 第 22 轮回本',(22,22*.4-m-1),(22,-5),arrowprops={'arrowstyle':'->','color':C['muted']},fontsize=11)
a.set(xlim=(0,40),ylim=(-10,10),xlabel='迁移后继续执行的轮数',ylabel='相比留在原设备省下的时间 / s');a.set_xticks([0,10,20,30,40]);a.set_yticks([-10,-5,0,5,10]);a.grid(alpha=.15);a.legend(frameon=False,loc='lower right')
save(f,'figure-12-11-migration');data['12-11']={'kind':'teaching_payoff','preparation_s':m,'saving_per_round_s':.4,'minimum_rounds':[20,22],'relationship':'后续节省逐轮抵消迁移准备'}
# TP repeats synchronization inside each layer.
f,a=canvas(5.2)
for row,dev in [(.70,'设备 A'),(.36,'设备 B')]:
 a.text(.025,row+.07,dev,fontsize=13)
 for i,lab in enumerate(['注意力计算','FFN 计算','下一层计算']):box(a,.15+i*.285,row,.20,.15,lab,size=13)
 for x in [.355,.64]:arrow(a,(x,row+.075),(x+.075,row+.075),col='muted')
for x,lab in [(.39,'输出归约'),(.675,'输出归约')]:
 arrow(a,(x,.70),(x,.51));arrow(a,(x,.51),(x,.70));a.text(x+.025,.59,lab,fontsize=11,va='center')
a.plot([.16,.63],[.24,.24],color=C['muted']);a.text(.40,.16,'每层两次归约，逐层重复 36 次',ha='center',fontsize=14);a.text(.50,.94,'后续计算等待两台设备汇总结果',ha='center',fontsize=17,weight='bold')
save(f,'figure-12-12-sync');data['12-12']={'kind':'dependency_diagram','layers':36,'reductions_per_layer':2,'startup_stages_per_reduction':2,'startup_multiplier':144,'relationship':'逐层依赖累积同步等待'}
# Window send/wait cycle using a fixed window with batch feedback.
f,a=plot_canvas();f.set_size_inches(12,5.2);send=64000*8/20e6;cycle=.1+send
for i in range(3):
 start=i*cycle;a.broken_barh([(start*1000,send*1000)],(.55,.30),facecolors=C['blue']);a.text((start+send/2)*1000,.70,'64 KB',ha='center',va='center',fontsize=10,color='white')
 a.broken_barh([((start+send)*1000,100)],(.55,.30),facecolors=C['pale'],edgecolors=C['line']);a.text((start+send+.05)*1000,.70,'等待确认',ha='center',va='center',fontsize=11)
 a.annotate('ACK',((start+cycle)*1000,.53),((start+cycle)*1000-18,.23),fontsize=10,arrowprops={'arrowstyle':'->','color':C['orange']},color=C['orange'])
a.text(170,1.07,'链路空闲，但窗口已满',ha='center',fontsize=14);a.set(xlim=(0,390),ylim=(0,1.25),yticks=[],xlabel='时间 / ms');a.set_xticks([0,100,200,300]);a.spines['left'].set_visible(False)
save(f,'figure-12-13-window');data['12-13']={'kind':'teaching_batch_feedback','window_bytes':64000,'rate_bps':20000000,'rtt_s':.1,'batch_send_s':send,'cycle_s':cycle,'relationship':'窗口耗尽使发送等待确认'}
# Independent access routes converge on one bottleneck.
f,a=canvas(5.6);box(a,.02,.40,.16,.22,'终端','30 MB 图片',size=14);box(a,.35,.68,.22,.18,'快路：20 Mbit/s','分配 20 MB → 8 s',col='light',size=13);box(a,.35,.18,.22,.18,'慢路：10 Mbit/s','分配 10 MB → 8 s',col='light',size=13);box(a,.76,.40,.21,.22,'共同出口','24 Mbit/s → 至少 10 s',col='sand',size=13)
arrow(a,(.185,.56),(.345,.76));arrow(a,(.185,.46),(.345,.27));arrow(a,(.575,.76),(.755,.56));arrow(a,(.575,.27),(.755,.46));a.text(.5,.96,'两路同时发送，所有字节仍须经过同一出口',ha='center',fontsize=16,weight='bold');a.text(.5,.04,'共同出口的容量限制速度；共同端点故障会中断两路',ha='center',fontsize=13)
save(f,'figure-12-14-multipath');data['12-14']={'kind':'teaching_topology','split_MB':[20,10],'access_Mbps':[20,10],'shared_Mbps':24,'access_s':[8,8],'shared_min_s':10,'relationship':'两条接入仍共享下游资源'}
# Show how the fastest compute loses its lead to communication.
f,a=plot_canvas();f.set_size_inches(12,5.5);R=base['rounds'];components=np.array([[tiers[k]['prepare_seconds'],R*tiers[k]['terminal_seconds'],R*tiers[k]['model_seconds_per_round'],R*tiers[k]['rtt_seconds'],R*tiers[k]['upload_seconds_per_round']] for k in ('end','near','cloud')]);left=np.zeros(3)
for j,(label,col) in enumerate([('准备','muted'),('终端工作','line'),('模型计算','teal'),('往返传播','orange'),('上传','blue')]):
 a.barh(np.arange(3),components[:,j],left=left,height=.48,color=C[col],label=label)
 for y,w,l in zip(range(3),components[:,j],left):
  if w>=3:a.text(l+w/2,y,f'{w:.1f}',ha='center',va='center',color='white' if col!='line' else C['ink'],fontsize=11)
 left+=components[:,j]
for y,v in enumerate(left):a.text(v+1,y,f'{v:.1f} s',va='center')
a.axvline(45,color=C['red'],ls='--');a.text(45,-.55,'期限 45 s',ha='center',color=C['red']);a.set(yticks=range(3),yticklabels=['端侧','附近工作站','云地域'],xlim=(0,71),ylim=(-.8,2.6),xlabel='剩余 20 轮累计时间 / s');a.invert_yaxis();a.legend(frameon=False,ncol=5,fontsize=10,loc='lower left',bbox_to_anchor=(-.12,1.02));a.set_xticks([0,10,20,30,40,50,60,70])
save(f,'figure-12-15-budgets');data['12-15']={'kind':'teaching_stacked_time','components':['prepare','terminal','model','rtt','upload'],'seconds':components.tolist(),'totals_s':left.tolist(),'relationship':'较快模型被较长通信抵消'}
# Progress retention determines how many rounds repeat.
rc=tiers['cloud']['round_seconds'];keep=next(c for c in edge['cases'] if c['id']=='twenty-retain-nine');lost=next(c for c in edge['cases'] if c['id']=='twenty-lose-ten')
f,a=canvas(6)
a.text(.02,.93,'断连前已执行',fontsize=13)
for i in range(10):box(a,.20+i*.071,.85,.060,.10,str(i+1),col='light' if i<9 else 'sand',size=11)
a.text(.83,.78,'第 10 轮确认丢失',fontsize=11,ha='center',color=C['orange'])
a.text(.02,.59,'保留进度',fontsize=13);box(a,.20,.49,.30,.14,'第 1–9 轮已提交','从第 10 轮继续',col='light',size=13);arrow(a,(.51,.56),(.58,.56));box(a,.59,.49,.13,.14,'重做 1 轮',f'{rc:.2f} s',col='sand',size=12);a.text(.76,.56,f'恢复 1 s + {rc:.2f} s\n额外 {1+rc:.2f} s',va='center',fontsize=13)
a.text(.02,.27,'丢失进度',fontsize=13);box(a,.20,.17,.30,.14,'重做第 1–10 轮',f'10 × {rc:.2f} s',col='sand',size=13);arrow(a,(.51,.24),(.58,.24));a.text(.60,.24,f'恢复 1 s + {10*rc:.1f} s\n额外 {1+10*rc:.1f} s',va='center',fontsize=13)
save(f,'figure-12-16-recovery');data['12-16']={'kind':'teaching_progress','executed':10,'committed_retained':9,'round_s':rc,'restore_s':1,'redo_rounds':[1,10],'extra_s':[1+rc,1+10*rc],'totals_s':[next(r for r in keep['rows'] if r['tier']=='cloud')['total_seconds'],next(r for r in lost['rows'] if r['tier']=='cloud')['total_seconds']],'relationship':'提交记录决定恢复后的重复工作'}
