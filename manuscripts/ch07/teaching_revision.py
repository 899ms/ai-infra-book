"""Follow a shard across servers, request slots and consumer dependencies."""
import json
import numpy as np
from fractions import Fraction
import matplotlib.pyplot as plt
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,n):out.save(f,'figure-7-'+n)
    with plt.rc_context(STYLE):
        f,a=canvas(4.9)
        for row in range(2):
            y=.58-row*.46;box(a,.03,y,.94,.31,'','gray');text(a,.08,y+.26,f'服务器 {"AB"[row]}',13)
            for i in range(4):box(a,.08+i*.13,y+.07,.10,.10,str(row*4+i),'blue',11)
            box(a,.66,y+.055,.26,.14,'两张网卡\n共享 40 GB/s','orange',11);arrow(a,(.58,y+.12),(.66,y+.12))
        arrow(a,(.79,.635),(.79,.315));text(a,.44,.48,'交换网络：双向传输',12,ha='center');save(f,'1-boundaries')
        d=data['7-2'];f,a=plot(3.6);n=np.array(d['device_multipliers']);c=np.array(d['compute_ms']);t=d['cut_ms'];a.plot(n,c+t,label='串行',color='#267398');a.plot(n,np.maximum(c,t),label='完全重叠',color='#388768');a.plot(n,c,ls=':',label='计算',color='#a56c28');a.set(xlabel='设备数相对倍数',ylabel='每步时间（ms）',xticks=n,ylim=(0,32));a.legend(frameon=False);save(f,'2-cut')
        for idx,order in enumerate(data['7-3']['ring_orders']):
            f,a=canvas(4.1);text(a,.04,.93,'连续环：两条边跨服务器' if idx==0 else '交错环：八条边都跨服务器',14)
            for i,rank in enumerate(order):
                x=.025+i*.12;box(a,x,.50,.09,.16,str(rank),'blue' if rank<4 else 'orange',12)
                if i<7:arrow(a,(x+.09,.58),(x+.12,.58))
            a.plot([.91,.91,.07,.07],[.50,.34,.34,.50],color=COL['line']);arrow(a,(.07,.34),(.07,.50));text(a,.5,.18,'蓝：服务器 A；橙：服务器 B',12,ha='center');save(f,'3-hierarchy' if idx==0 else 'ring-interleaved')
        f,a=canvas(5.2)
        for col in range(2):
            x=.04+.51*col;text(a,x+.20,.93,f'服务器 {"AB"[col]}',14,ha='center');box(a,x,.64,.41,.17,'本地 ReduceScatter\n得到四个 48 MiB 分片','blue',11);box(a,x,.35,.41,.16,'对应分片跨服务器\n执行两卡 AllReduce','orange',11);box(a,x,.06,.41,.16,'本地 AllGather\n得到完整归约结果','green',11);arrow(a,(x+.20,.64),(x+.20,.51));arrow(a,(x+.20,.35),(x+.20,.22))
        arrow(a,(.45,.46),(.55,.46));arrow(a,(.55,.39),(.45,.39));save(f,'hierarchy-stages')
        f,a=plot(3.6,left=.22);left=np.zeros(3)
        for k,l,c in [('local_MiB','本地','blue'),('remote_MiB','跨服务器','orange')]:v=data['7-3'][k];a.barh(range(3),v,left=left,color=COL[c],edgecolor=COL['line'],label=l);left+=v
        a.set(yticks=range(3),yticklabels=['连续环','交错环','分层归约'],xlabel='逻辑发送量，两方向合计（MiB）');a.invert_yaxis();a.legend(frameon=False);save(f,'hierarchy-bytes')
        f,a=plot(3.6,left=.18)
        for stage in range(4):
            for batch in range(8):a.barh(stage,1,left=stage+batch,height=.7,color=COL[['blue','green','orange','purple'][batch%4]],edgecolor=COL['line']);a.text(stage+batch+.5,stage,str(batch),ha='center',va='center',fontsize=11)
        a.set(yticks=range(4),yticklabels=[f'阶段 {i}' for i in range(4)],xlim=(0,11),xticks=[0,2,4,6,8,10,11],xlabel='时间（ms）；格内为微批编号');a.invert_yaxis();save(f,'4-pipeline')
        for i in range(3):
            f,a=canvas(3.7);text(a,.04,.94,['集中到一张网卡','均分到四张独立网卡','四张网卡共用一个入口'][i],14);box(a,.04,.42,.24,.24,'32 MiB','blue')
            if i==0:box(a,.64,.42,.30,.24,'网卡\n25 GB/s','orange');arrow(a,(.28,.54),(.64,.54))
            else:
                if i==2:box(a,.36,.32,.24,.42,'共享入口\n40 GB/s','gray',11);arrow(a,(.28,.54),(.36,.54))
                for j in range(4):
                    y=.21+j*.16;box(a,.72,y,.25,.12,'8 MiB','orange',11);arrow(a,(.60 if i==2 else .28,.54),(.72,y+.06))
            text(a,.5,.09,f'接收阶段至少 {data["7-5"]["lower_ms"][i]:.2f} ms',13,ha='center');save(f,'5-expert' if i==0 else f'expert-path-{i}')
        f,a=canvas(4.8);box(a,.03,.44,.21,.18,'源 GPU','blue');box(a,.39,.72,.27,.15,'直连 40','green');box(a,.36,.17,.31,.19,'本地互联 60\n中继网卡 80','orange',11);box(a,.78,.40,.20,.25,'下游\n带宽 BD','gray');arrow(a,(.24,.53),(.39,.79));arrow(a,(.24,.53),(.36,.26));arrow(a,(.66,.79),(.78,.52));arrow(a,(.67,.26),(.78,.52));text(a,.5,.05,'单位 GB/s；中继先受 60 限制',12,ha='center');save(f,'6-relay')
        paths=[('主机 RPC',['CPU A','网卡 A','网卡 B','CPU B']),('CPU 提交 GPUDirect RDMA',['GPU A','网卡 A','网卡 B','GPU B']),('GPU 经 NVLink 访问',['GPU A','NVLink','GPU B']),('设备发起 URMA 异步访问',['设备 A','UB 互联','设备 B'])]
        for i,(title,nodes) in enumerate(paths):
            f,a=canvas(3.8);text(a,.04,.94,title,14);step=.94/len(nodes)
            for j,node in enumerate(nodes):
                x=.03+j*step;box(a,x,.36,step-.045,.18,node,'blue' if j in [0,len(nodes)-1] else 'gray',11)
                if j<len(nodes)-1:arrow(a,(x+step-.045,.45),(x+step,.45))
            if i==1:box(a,.20,.69,.28,.12,'CPU 提交请求','orange',11);arrow(a,(.34,.69),(.38,.54),'control')
            else:text(a,.5,.73,'发起者提交操作，接收方按完成条件使用结果',11,ha='center')
            text(a,.5,.13,'实线：数据；虚线：控制提交',11,ha='center');save(f,'7-access' if i==0 else f'access-{i}')
        f,a=canvas(4.1)
        for i in range(2):
            y=.61-i*.43;box(a,.04,y,.31,.19,'远端快照','blue');box(a,.65,y,.31,.19,'消费者' if i==0 else '本地副本','green');arrow(a,(.35,y+.095),(.65,y+.095));text(a,.5,y+.25,'每次使用都跨网络读取' if i==0 else '搬回一次，再读取本地副本',13,ha='center')
        save(f,'snapshot-paths')
        for i,(label,c) in enumerate(data['7-8']['cases'].items()):
            f,a=plot(3.5);r=np.arange(1,6 if i==0 else 26);a.plot(r,c['remote_per_read_ms']*r,label='每次远读',color='#267398');a.plot(r,c['setup_ms']+c['local_per_read_ms']*r,label='先搬回本地',color='#388768');a.set(xlabel='复用次数',ylabel='累计时间（ms）');a.legend(frameon=False);save(f,'8-snapshot' if i==0 else 'snapshot-partial')
        f,a=canvas(4.0);text(a,.04,.94,'槽位保存一项尚未完成的请求',14)
        for x,label,c in [(.03,'分配槽位','blue'),(.37,'传输与等待','orange'),(.71,'处理完成\n释放槽位','green')]:box(a,x,.39,.26,.23,label,c,12)
        arrow(a,(.29,.5),(.37,.5));arrow(a,(.63,.5),(.71,.5));text(a,.5,.18,'占用时间：从分配到释放，共 2 μs',12,ha='center');save(f,'slot-lifetime')
        f,a=plot(3.5,left=.24)
        for y,(key,p) in enumerate(data['7-9']['periods'].items()):
            a.barh(y,4,height=.5,color=COL['gray'])
            for start,dur in p['segments_us']:a.barh(y,dur,left=start,height=.5,color=COL['blue'],edgecolor=COL['line'])
        a.set(yticks=[0,1],yticklabels=['128 个槽位','313 个槽位'],xlim=(0,4),xlabel='时间（μs）；蓝色为载荷发送');a.invert_yaxis();save(f,'9-window')
        f,a=plot(3.5);n=np.arange(1,501);a.plot(n,np.minimum(40,n*256/2000),label='路径与槽位限制',color='#267398');a.plot(n,np.minimum(2.56,n*256/2000),label='再加 100 ns 启动间隔',color='#a56c28');a.set(xlabel='活跃请求槽位数',ylabel='吞吐上限（GB/s）');a.legend(frameon=False);save(f,'window-rate')
        f,a=plot(3.8,left=.23);a.barh(0,5,color=COL['blue'],height=.48);a.barh(1,12,color=COL['orange'],height=.48);a.barh(1,4,left=8,color=COL['green'],height=.48);a.axvline(6,ls=':',color='#a54b43');a.text(6.2,-.45,'6 μs 提前覆盖',fontsize=11);a.set(yticks=[0,1],yticklabels=['源缓冲占用','目的缓冲占用'],xlim=(0,14),ylim=(-.7,1.6),xlabel='时间（μs）；绿色为消费者读取');a.invert_yaxis();save(f,'10-lifetime')
        f,a=canvas(4.5)
        for i in range(2):
            y=.63-i*.39;box(a,.04,y,.23,.18,f'端点 {i}','blue');box(a,.38,y,.24,.18,'关系绑定','orange');arrow(a,(.27,y+.09),(.38,y+.09));arrow(a,(.62,y+.09),(.77,.52))
        box(a,.77,.35,.20,.34,'目标\n传输状态','green',11);text(a,.5,.08,'端点身份分别保存，目标传输状态共享',12,ha='center');save(f,'11-state')
        f,a=plot(3.7,left=.26);left=np.zeros(3)
        for j,label,col in [(0,'端点','blue'),(1,'绑定','orange'),(2,'传输','green')]:v=np.array(data['7-11']['state_MiB'])[:,j];a.barh(range(3),v,left=left,height=.5,color=COL[col],edgecolor=COL['line'],label=label);left+=v
        a.axvline(1,ls='--',color='#777777');a.set(yticks=range(3),yticklabels=['逐关系独占','按目标共享','八类隔离'],xlabel='状态占用（MiB）',xlim=(0,10));a.invert_yaxis();a.legend(frameon=False);save(f,'state-capacity')
        for i,(label,schedule) in enumerate(data['7-12']['schedules'].items()):
            f,a=plot(3.6,left=.21)
            for t in schedule['tasks']:
                lane=1 if t['id']=='independent_transfer' else 0;color={'write_data':'blue','recover_and_make_visible':'orange','publish_notification':'green','independent_transfer':'purple'}[t['id']];a.barh(lane,t['duration_ns']/1000,left=t['start_ns']/1000,height=.45,color=COL[color],edgecolor=COL['line'])
            a.set(yticks=[0,1],yticklabels=['写入与发布','独立传输'],xlim=(0,115),xlabel='时间（μs）');a.invert_yaxis();save(f,'12-ordering' if i==0 else 'ordering-independent')
        f,a=canvas(5.0)
        for row,(time,label,c) in enumerate([(1,'提前读取：得到旧值','orange'),(2,'生产者写入新值','blue'),(3,'就绪标志可见','green'),(4,'消费者读到就绪标志','green'),(5,'交付先前读到的旧值','orange'),(6,'若在 4 μs 重读，此时得到新值','blue')]):
            y=.78-row*.14;text(a,.03,y+.04,f'{time} μs',11);box(a,.19,y,.76,.10,label,c,11)
        save(f,'13-stale')
        for i,(name,ops) in enumerate(data['7-14']['operations'].items()):
            f,a=plot(5,left=.17)
            for op in ops:
                y=op['operation'];start=op['submit_ns']/1000;end=op['transfer_complete_ns']/1000;done=op['completion_consumed_ns']/1000;a.barh(y,end-start,left=start,height=.65,color=COL['blue']);a.barh(y,done-end,left=end,height=.65,color=COL['orange'])
            a.set(xlim=(0,82),yticks=[0,4,8,12,15],ylabel='请求编号',xlabel='时间（μs）；蓝为传输，橙为等待回收');a.invert_yaxis();save(f,'14-reclaim' if i==0 else 'reclaim-more')
        for kind,n in [('arrival','15-congestion'),('queue','congestion-queue')]:
            f,a=plot(3.8)
            for (name,segs),label,c in zip(data['7-15']['periodic_segments'].items(),['重叠 20 ms','重叠 5 ms','不重叠'],['#267398','#a56c28','#388768']):
                xs=[];ys=[]
                for seg in segs:
                    xs.extend([seg['start_ns']/1e6,seg['end_ns']/1e6]);ys.extend([seg['arrival_bytes_per_second']/1e9]*2 if kind=='arrival' else [seg['queue_start_bytes']/1e6,seg['queue_end_bytes']/1e6])
                a.plot(xs,ys,label=label,color=c)
            a.set(xlabel='时间（ms）',ylabel='到达速率（GB/s）' if kind=='arrival' else '积压（MB）',xlim=(0,100));a.legend(frameon=False);save(f,n)
        f,a=canvas(3.8);box(a,.04,.42,.24,.20,'发送者\n80 GB/s','blue');box(a,.43,.42,.24,.20,'缓冲队列','orange');box(a,.78,.42,.19,.20,'出口\n50 GB/s','green',11);arrow(a,(.28,.52),(.43,.52));arrow(a,(.67,.52),(.78,.52));arrow(a,(.55,.42),(.17,.18),'control');text(a,.46,.12,'反馈生效后，发送降至 40 GB/s',12,ha='center');save(f,'feedback-loop')
        f,a=plot(3.8)
        for seg in data['7-16']['queue_segments']:a.plot([seg['start_ns']/1000,seg['end_ns']/1000],[seg['queue_start_bytes']/1024,seg['queue_end_bytes']/1024],color='#267398')
        a.axvline(20,ls='--',color='#a56c28');a.set(xlabel='时间（μs）',ylabel='队列占用（KiB）',xlim=(0,120),ylim=(0,580));save(f,'16-feedback')
        packet_cases=dict(data['7-17']['cases'])
        loss=json.loads((here.parents[1]/'calculations/results/packet-reorder-loss.json').read_text())
        packet_cases['packet-reorder-loss']={k:loss[k] for k in ['transmissions','delivery']}
        for i,(name,c) in enumerate(packet_cases.items()):
            f,a=plot(3.7);delivery={x['sequence']:float(Fraction(x['delivery_exact_ns']))/1000 for x in c['delivery']}
            for t in c['transmissions']:
                if t['lost']:continue
                arrival=float(Fraction(t['arrival_exact_ns']))/1000;seq=t['sequence'];a.plot([arrival,delivery[seq]],[seq,seq],color='#a56c28');a.scatter(arrival,seq,color='#267398',s=22)
            a.set(xlim=(0,25),yticks=range(8),ylabel='报文序号',xlabel='到达与可交付时刻（μs）');a.invert_yaxis();save(f,'17-packets' if i==0 else f'packets-{i}')
        f,a=canvas(3.6);box(a,.04,.40,.34,.25,'请求 0 持有 A\n等待 B','blue');box(a,.62,.40,.34,.25,'请求 1 持有 B\n等待 A','orange');arrow(a,(.38,.58),(.62,.58));arrow(a,(.62,.46),(.38,.46));text(a,.5,.16,'双方都需要对方先释放',13,ha='center');save(f,'18-deadlock')
        f,a=canvas(3.7)
        for x,label,col in [(.03,'请求资源','blue'),(.37,'执行资源','orange'),(.71,'独立响应\n资源','green')]:box(a,x,.42,.26,.24,label,col,12)
        arrow(a,(.29,.54),(.37,.54));arrow(a,(.63,.54),(.71,.54));text(a,.5,.18,'响应有预留通路，可返回并释放原请求',12,ha='center');save(f,'response-reserve')
        for i,(ready,ex) in enumerate([([0,0,0,2],.4),([0,0,0,2],.2),([0]*4,.4)]):
            f,a=plot(3.5,left=.18)
            for lane,t in enumerate(ready):
                a.barh(lane,t,height=.5,color=COL['gray']);a.barh(lane,max(ready)-t,left=t,height=.5,color=COL['orange']);a.barh(lane,ex,left=max(ready),height=.5,color=COL['blue']);a.scatter(t,lane,color='#252525',s=16)
            a.set(yticks=range(4),yticklabels=[f'参与者 {j}' for j in range(4)],xlim=(0,2.6),xlabel='时间（ms）；圆点为就绪');a.invert_yaxis();save(f,'19-progress' if i==0 else f'progress-{i}')
        for i,c in enumerate(data['7-20']['cases']):
            f,a=plot(2.9,left=.17);a.barh(0,20,height=.45,color=COL['gray']);a.barh(1,c['comm_ms'],left=c['ready_ms'],height=.45,color=COL['blue']);a.barh(0,2,left=c['update_start_ms'],height=.45,color=COL['green']);a.scatter(c['ready_ms'],1,color='#252525',s=16);a.set(yticks=[0,1],yticklabels=['计算／更新','通信'],xlim=(0,37),xlabel='时间（ms）');a.invert_yaxis();save(f,'20-step' if i==0 else f'step-{i}')
        f,a=plot(3.7);m=np.logspace(3,8,200)
        for alpha,b,label,col in [(5e-6,25e9,'原配置','#267398'),(5e-6,75e9,'带宽三倍','#388768'),(2e-6,25e9,'启动缩短','#a56c28')]:a.loglog(m,(14*alpha+1.75*m/b)*1e6,label=label,color=col)
        a.set(xlabel='每参与者输入（bytes）',ylabel='归约时间（μs）');a.legend(frameon=False);save(f,'21-message')
    out.finish();return out.outputs,out.checks
