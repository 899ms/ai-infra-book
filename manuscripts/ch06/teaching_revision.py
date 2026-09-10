"""Chapter six: follow ownership, then messages, then elapsed time."""
import numpy as np
import matplotlib.pyplot as plt
from figure_style import COL, STYLE, canvas, plot, text, box, arrow, Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,n): out.save(f,'figure-6-'+n)
    with plt.rc_context(STYLE):
        f,a=canvas(4.4)
        for row,group in enumerate([1,4,8]):
            y=.73-row*.29;text(a,.02,y+.19,f'每实例 {group} 张卡',12)
            for start in range(0,8,group):
                box(a,.03+start*.118,y,.118*group-.012,.13,'','gray')
                for i in range(start,start+group):box(a,.04+i*.118,y+.025,.09,.08,str(i),'blue',11)
        save(f,'1-placement')
        f,a=plot(3.6,left=.24);left=np.zeros(2)
        for i,label,col in [(0,'权重','blue'),(1,'KV','green'),(2,'工作区','orange')]:
            v=np.array(data['capacity_plot']['segments_GB'])[:,i];a.barh([0,1],v,left=left,height=.45,label=label,color=COL[col],edgecolor=COL['line']);left+=v
        a.axvline(24,ls='--',color='#777777');a.set(yticks=[0,1],yticklabels=['单卡实例','八卡中的每卡'],xlim=(0,25),xlabel='每卡内存占用（GB）');a.invert_yaxis();a.legend(frameon=False,ncol=3,loc='upper center',bbox_to_anchor=(.5,1.02));save(f,'2-capacity')
        for rows,name in [(False,'tp-columns'),(True,'tp-rows')]:
            f,a=canvas(4.4);text(a,.04,.94,'同一乘法：[2, 3] × [[1, 4], [2, 5]]',12)
            for i in range(2):
                x=.04+i*.50;box(a,x,.37,.42,.43,'','green' if i else 'blue');text(a,x+.21,.72,f'卡 {i}',14,ha='center')
                expr=([ '2 × [1, 4]','3 × [2, 5]'] if rows else ['[2, 3] × [1, 2] T','[2, 3] × [4, 5] T'])[i]
                text(a,x+.21,.59,expr,12,ha='center');text(a,x+.21,.45,(['[2, 8]','[6, 15]'] if rows else ['8','23'])[i],14,ha='center');arrow(a,(x+.21,.37),(.50,.24))
            box(a,.16,.06,.68,.17,'逐元素求和 → [8, 23]' if rows else '并排拼接 → [8, 23]','orange');save(f,name)
        f,a=canvas(5.1);box(a,.29,.82,.42,.12,'完整输入 X：m × h','gray')
        for i in range(2):
            x=.04+.50*i;arrow(a,(.5,.82),(x+.21,.70));box(a,x,.52,.42,.18,f'上投影 → SiLU 与乘法\nZ{i}：m × (f/2)','blue' if i==0 else 'green',11);arrow(a,(x+.21,.52),(x+.21,.41));box(a,x,.26,.42,.15,f'下投影部分和\nm × h','blue' if i==0 else 'green',11);arrow(a,(x+.21,.26),(.5,.15))
        box(a,.23,.02,.54,.13,'相加 → 完整输出 m × h','orange');save(f,'3-tp')
        f,a=plot(3.8,left=.18)
        for stage in range(4):
            for batch in range(4):
                a.barh(stage,1,left=stage+batch,height=.72,color=COL[['blue','green','orange','purple'][batch]],edgecolor=COL['line']);a.text(stage+batch+.5,stage,str(batch),ha='center',va='center',fontsize=12)
        a.set(yticks=range(4),yticklabels=[f'阶段 {i}' for i in range(4)],xticks=range(8),xlim=(0,7),xlabel='时间（ms）；格内为微批次编号');a.invert_yaxis();save(f,'4-pipeline')
        f,a=canvas(4.7);box(a,.04,.72,.30,.18,'卡 0：输入 A','blue');box(a,.65,.72,.31,.18,'卡 3：输入 A','blue');arrow(a,(.34,.81),(.65,.81));text(a,.5,.94,'派发输入',12,ha='center')
        for x,label in [(.04,'专家 1 → y1'),(.65,'专家 6 → y6')]:
            arrow(a,(x+.15,.72),(x+.15,.56));box(a,x,.39,.31,.17,label,'green');arrow(a,(x+.15,.39),(.5,.20))
        box(a,.12,.04,.76,.16,'卡 0：按路由权重合并 a1 y1 + a6 y6','orange',11);save(f,'5-dispatch')
        for reduction,name in [(False,'6-ep-layout'),(True,'ep-reduction')]:
            f,a=canvas(5.6);text(a,.5,.95,'专家贡献：先行内，再列内求和' if reduction else '每行分一组专家，同列重复保存 KV',14,ha='center')
            for row in range(4):
                y=.68-row*.18;text(a,.02,y+.055,f'组 {row}',11)
                for col in range(2):
                    x=.18+col*.43;label=f'卡 {2*row+col}\n'+(f'组贡献 {row+1}' if reduction else f'KV 头 {"0、1" if col==0 else "2、3"}')
                    box(a,x,y,.30,.13,label,'blue' if col==0 else 'green',11)
                    if reduction and row<3:arrow(a,(x+.15,y),(x+.15,y-.05))
                if reduction:arrow(a,(.48,y+.065),(.61,y+.065))
            text(a,.5,.06,'两列各得到完整输出：1 + 2 + 3 + 4 = 10' if reduction else '每行的专家中间维：左 768，右 768',11,ha='center');save(f,name)
        f,a=plot(3.4,left=.28);vals=data['expert_reuse']['balanced_vs_concentrated']['weight_read_bytes'];a.barh([0,1],np.array(vals)/2**20,height=.45,color=[COL['blue'],COL['orange']],edgecolor=COL['line']);a.set(yticks=[0,1],yticklabels=['选择 128 个专家','选择 8 个专家'],xlim=(0,5000),xlabel='一批读取的专家权重（MiB）');a.invert_yaxis();save(f,'7-reuse')
        for i,vals in enumerate(data['expert_load']['tasks']):
            f,a=plot(3.4);a.bar(range(4),vals,color=COL['blue'],edgecolor=COL['line']);a.set(xticks=range(4),xticklabels=[f'组 {j}' for j in range(4)],ylim=(0,580),ylabel='token—专家计算次数')
            for j,v in enumerate(vals):a.text(j,v+12,str(v),ha='center',fontsize=12)
            save(f,'8-expert-load' if i==0 else f'expert-load-{i}')
        f,a=canvas(4.3);text(a,.04,.94,'沿 0 → 1 → 2 → 3，累计块 0 的贡献',13)
        for i,v in enumerate([1,11,111,1111]):
            x=.025+i*.25;box(a,x,.47,.20,.23,f'卡 {i}\n{v}','green' if i==3 else 'blue');text(a,x+.10,.34,'起点' if i==0 else f'加 {10**i}',12,ha='center')
            if i<3:arrow(a,(x+.20,.585),(x+.25,.585))
        text(a,.5,.13,'三轮后，卡 3 持有块 0 的完整和',13,ha='center');save(f,'9-ring-rounds')
        f,a=canvas(5.0);text(a,.04,.94,'AllGather：每轮向下一卡转发一块',14)
        for r in range(4):
            y=.72-r*.20;text(a,.02,y+.06,'起点' if r==0 else f'{r} 轮',11)
            for card in range(4):
                owned=[(card+1-j)%4 for j in range(r+1)];box(a,.16+card*.21,y,.19,.13,','.join(map(str,owned)),'green' if r==3 else 'blue',11)
                if r==0:text(a,.255+card*.21,y+.20,f'卡 {card}',12,ha='center')
        text(a,.5,.03,'格内为已归约的数据块编号',11,ha='center');save(f,'ring-gather')
        f,a=plot(3.9,left=.19);left=np.zeros(4)
        for key,label,col in [('local_s','本地','blue'),('communication_s','归约','orange'),('serial_s','串行','gray')]:
            v=np.array([x[key]*1000 for x in data['continuous_execution']['first_steps']]);a.barh(range(4),v,left=left,height=.5,color=COL[col],edgecolor=COL['line'],label=label);left+=v
        a.set(yticks=range(4),yticklabels=['TP 1','TP 2','TP 4','TP 8'],xlim=(0,18),xlabel='一次 decode 的时间（ms）');a.invert_yaxis();a.legend(ncol=3,frameon=False);save(f,'10-tp-time')
        d=data['collectives'];f,a=plot(3.7)
        for key,label,c in [('ring_seconds','环','#267398'),('tree_seconds','二项树','#a56c28')]:a.loglog(d['message_bytes'],np.array(d[key])*1e6,label=label,color=c)
        a.set(xlabel='每卡输入大小（bytes）',ylabel='通信时间（μs）');a.legend(frameon=False);save(f,'11-collectives')
        d=data['concurrency']['teaching_ms']
        for concurrent,name in [(False,'12-resources'),(True,'resources-concurrent')]:
            f,a=plot(3.5,left=.24)
            if concurrent:
                for i in range(2):
                    a.barh(i-.16,d['shared_comm'][i],height=.28,color=COL['orange'],edgecolor=COL['line']);a.barh(i+.16,d['shared_compute'][i],height=.28,color=COL['blue'],edgecolor=COL['line'])
                for c,l in [('orange','通信'),('blue','计算')]:a.barh([],[],color=COL[c],label=l)
                a.legend(frameon=False)
            else:a.barh([0,1],d['independent_comm'],height=.45,color=COL['orange'],edgecolor=COL['line'])
            a.set(yticks=[0,1],yticklabels=['配置 A','配置 B'],xlim=(0,.7),xlabel='从同时就绪起计时（ms）' if concurrent else '独立通信时间（ms）');a.invert_yaxis();save(f,name)
        f,a=canvas(4.6)
        for row,(down,up) in enumerate([(16,16),(24,8)]):
            y=.62-row*.43;text(a,.04,y+.26,f'{down} 下联 + {up} 上联 = 32 个端口',13)
            for i in range(32):box(a,.045+(i%16)*.058,y+(1-i//16)*.075,.045,.055,'','blue' if i<down else 'orange')
            text(a,.5,y-.075,f'下联 {down*50} GB/s → 上联 {up*50} GB/s',12,ha='center')
        save(f,'13-ports')
        patterns=data['physical_paths']['collective_patterns']
        for i,p in enumerate(patterns):
            f,a=canvas(4.8);angles=np.linspace(np.pi/2,np.pi/2-2*np.pi,16,endpoint=False);coords=np.array([[.5+.34*np.cos(t),.49+.35*np.sin(t)] for t in angles]);a.plot(*np.vstack([coords,coords[:1]]).T,color='#999999')
            for j,(x,y) in enumerate(coords):a.plot(x,y,'o',color='#267398',ms=4);text(a,.5+(x-.5)*1.17,.49+(y-.49)*1.17,str(j),11,ha='center')
            route=p['rounds'][2]['routes'][0]
            for u,v in route['path']:arrow(a,coords[u],coords[v])
            text(a,.5,.96,('递归' if i==0 else 'Swing')+f'：第三轮 0 → {route["receiver"]}',14,ha='center');save(f,'14-topology' if i==0 else 'topology-swing')
        f,a=plot(3.5)
        for i,p in enumerate(patterns):a.bar(np.arange(3)+(i-.5)*.32,[r['peak_link_bytes']/2**20 for r in p['rounds'][:3]],width=.32,color=COL['blue' if i==0 else 'orange'],edgecolor=COL['line'],label='递归' if i==0 else 'Swing')
        a.set(xticks=range(3),xticklabels=['第 1 轮','第 2 轮','第 3 轮'],ylim=(0,5),ylabel='最忙单向链路传输量（MiB）');a.legend(frameon=False);save(f,'topology-load')
        f,a=canvas(4.2);box(a,.04,.36,.32,.33,'左半部','blue');box(a,.64,.36,.32,.33,'右半部','green');arrow(a,(.36,.52),(.64,.52));text(a,.5,.76,'中间切面：k² 条链路',12,ha='center');a.plot([.20,.20,.80,.80],[.36,.18,.18,.36],color='#454545');text(a,.5,.07,'首尾连接再切一次：另有 k² 条',12,ha='center');save(f,'15-torus')
        f,a=plot(3.4)
        for shift,vals,label,col in [(-.17,[1,8],'设备数','blue'),(.17,[1,4],'二分链路数','orange')]:a.bar(np.arange(2)+shift,vals,width=.32,label=label,color=COL[col],edgecolor=COL['line'])
        a.set(xticks=[0,1],xticklabels=['k = 4','k = 8'],ylim=(0,10),ylabel='相对 k = 4 的倍数');a.legend(frameon=False);save(f,'torus-growth')
        f,a=canvas(5.4)
        for row,(title,left,middle,right) in enumerate([('GB200 NVL72','计算托盘','NVLink\n交换','计算托盘'),('TPU v4','64 芯片\n电互联单元','光电路\n交换机','64 芯片\n电互联单元'),('Unified Bus','主机与\n计算资源','UB\n互联','主机与\n内存资源')]):
            y=.65-row*.29;text(a,.03,y+.23,title,14)
            for x,label,col in [(.03,left,'blue'),(.38,middle,'gray'),(.73,right,'green')]:box(a,x,y,.24,.17,label,col,11)
            arrow(a,(.27,y+.085),(.38,y+.085));arrow(a,(.62,y+.085),(.73,y+.085))
        save(f,'16-systems')
        for after,name in [(False,'17-pool-placement'),(True,'pool-after')]:
            f,a=plot(3.8)
            for i,v in enumerate([64,48,32,32]):a.bar(i,v,color=COL[['blue','green','orange','purple'][i]],edgecolor=COL['line'],width=.6)
            if after:a.bar(1,16,bottom=48,color=COL['blue'],edgecolor=COL['line'],width=.6);a.text(1,56,'16',ha='center',va='center',fontsize=12)
            else:a.text(.05,76,'任务 0 另需 16 GiB，尚未分配',fontsize=12)
            a.axhline(64,ls='--',color='#777777');a.set(xticks=range(4),xticklabels=[f'节点 {i}' for i in range(4)],ylim=(0,84),ylabel='已占用物理内存（GiB）');save(f,name)
        f,a=canvas(4.6);text(a,.04,.94,'在途请求：已经发出，尚未收到结果',13)
        for i in range(4):
            y=.70-i*.15;box(a,.04,y,.21,.10,f'请求 {i}','blue',11);arrow(a,(.25,y+.05),(.72,y+.05));box(a,.73,y,.23,.10,'256 字节','green',11)
        text(a,.5,.09,'往返 2 μs；允许 128 个请求同时在途',12,ha='center');save(f,'18-read-window')
        d=data['remote_memory'];f,a=plot(3.7);a.loglog(d['frequency_per_second'],d['mean_payload_GBs'],color='#267398',label='16 GiB × 读取频率');a.axhline(40,color='#a56c28',label='路径：40 GB/s');a.axhline(d['window_bound_GBs'],ls='--',color='#388768',label='窗口：16.4 GB/s');a.set(xlabel='每秒完整读取次数',ylabel='平均带宽需求（GB/s）');a.legend(frameon=False,loc='upper left');save(f,'19-memory-pool')
        for i,c in enumerate(data['continuous_execution']['candidates']):
            f,a=plot(3.6,left=.20);instances=c['instances'];service=c['service_ms'];shown=min(instances,4)
            for req in range(4):
                lane=req%instances;start=req//instances*service;a.barh(lane,service,left=start,height=.52,color=COL[['blue','green','orange','purple'][req]],edgecolor=COL['line']);a.text(start+service/2,lane,f'会话 {req}',fontsize=11,ha='center',va='center')
            a.axvline(90,ls='--',color='#777777');a.set(yticks=range(shown),yticklabels=[f'实例 {j}' for j in range(shown)],xlim=(0,150),ylim=(-.6,shown-.4),xlabel='从四会话到达起计时（ms）');a.invert_yaxis();save(f,'20-session-schedule' if i==0 else f'session-tp{c["tp"]}')
        for phase,name in [('healthy','21-scale-cost'),('fault','scale-cost-fault')]:
            f,a=plot(3.8)
            for c,col in zip(data['deadline_curves'][phase],['#267398','#388768','#a56c28','#86649b']):a.step(c['deadlines_ms'],[np.nan if v is None else v for v in c['cost_per_valid']],where='post',label=f'TP {c["tp"]}',color=col)
            a.axvline(90,ls='--',color='#777777');a.set(xlim=(20,220),ylim=(0,.95),xlabel='完成期限（ms）',ylabel='每个按时完成会话的成本');a.legend(ncol=2,frameon=False);save(f,name)
    out.finish();return out.outputs,out.checks
