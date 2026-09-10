"""Placement first, state handoff second, resource rates last."""
from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,n):out.save(f,'figure-9-'+n)
    with plt.rc_context(STYLE):
        for i,title in enumerate(['多卡共同执行一个完整模型','完整副本分别接收请求','PD：按输入处理与生成阶段分工','AF：按每层的算子分工']):
            f,a=canvas(3.7);text(a,.04,.94,title,14)
            if i==0:
                box(a,.04,.22,.92,.48,'','gray');text(a,.5,.61,'一个调度器，一组模型权重与状态',12,ha='center')
                for j in range(8):box(a,.06+j*.112,.32,.09,.12,str(j),'blue',11)
            elif i==1:
                for x in [.04,.56]:box(a,x,.25,.40,.26,'完整模型副本','blue');text(a,x+.2,.72,'独立请求',12,ha='center');arrow(a,(x+.2,.65),(x+.2,.51))
            else:
                for x,label,c in [(.04,'P：处理输入' if i==2 else '注意力','blue'),(.61,'D：逐步生成' if i==2 else 'FFN／专家','green')]:box(a,x,.28,.35,.27,label,c)
                arrow(a,(.39,.46),(.61,.46));text(a,.5,.68,'传输上下文 KV' if i==2 else '逐层传递激活',12,ha='center')
                if i==3:arrow(a,(.61,.35),(.39,.35))
            save(f,'1-organization' if i==0 else f'organization-{i}')
        f,a=canvas(4.3)
        for j,l in enumerate(['P','D','工具等待','下一轮 P']):box(a,.20+j*.19,.73,.18,.15,l,'gray',11)
        for row,(l,start,c) in enumerate([('权重',.20,'blue'),('KV',.20,'green'),('可复用 EC',.20,'purple')]):
            y=.48-row*.17;text(a,.02,y+.05,l,11);box(a,start,y,.75,.10,'',c)
        text(a,.5,.04,'阶段宽度示意顺序；等待期间状态仍保留',11,ha='center');save(f,'2-state')
        for stage,name in [(0,'kv-residency'),(1,'kv-publish'),(2,'kv-release')]:
            f,a=canvas(3.9);text(a,.04,.94,['传输开始：两端都占用完整空间','传输完成：通知目的端可以使用 KV','源端释放缓冲区，D 继续生成'][stage],13)
            box(a,.04,.35,.35,.29,'源 P\n1.125 GiB' if stage<2 else '源 P\n已释放','blue' if stage<2 else 'gray');box(a,.61,.35,.35,.29,'目的 D\n1.125 GiB','orange' if stage==0 else 'green');arrow(a,(.39,.5),(.61,.5),'data' if stage==0 else 'control');text(a,.5,.15,'数据复制中' if stage==0 else '完成标记建立使用顺序' if stage==1 else '下一请求可使用源端空间',12,ha='center');save(f,name)
        f,a=canvas(4.4)
        for row,(title,count,c) in enumerate([('P 池：四个 A',4,'blue'),('D 池：四个 B',4,'green')]):
            y=.61-row*.40;text(a,.04,y+.23,title,14)
            for i in range(count):box(a,.04+i*.235,y,.21,.16,'2 请求/s',c,11)
            text(a,.5,y-.09,'池能力：8 请求/s',12,ha='center')
        save(f,'pd-layout')
        f,a=plot(4.5,left=.17);matrix=np.zeros((5,5))
        for row in data['9-3']['assignments']:
            x=row['prefill_workers']['prefill-oriented'];y=row['prefill_workers']['decode-oriented'];matrix[y,x]=float(Fraction(row['bound_requests_per_second_exact']))
        a.imshow(matrix,origin='lower',cmap='Blues',vmin=0,vmax=12,aspect='equal')
        for y in range(5):
            for x in range(5):a.text(x,y,f'{matrix[y,x]:g}',fontsize=12,ha='center',va='center')
        a.set(xticks=range(5),yticks=range(5),xlabel='分给 P 的 A 数量',ylabel='分给 P 的 B 数量');save(f,'3-pd')
        f,a=canvas(4.9)
        for row,count in enumerate(data['new-allocation']['prefill_A']):
            y=.69-row*.28;text(a,.04,y+.18,['原始请求','前缀命中','长输出'][row],13)
            for i in range(8):box(a,.035+i*.117,y,.10,.12,('A' if i<4 else 'B')+'\n'+('P' if i<count else 'D'),'blue' if i<count else 'green',11)
            text(a,.5,y-.06,f'请求率上限 {data["new-allocation"]["rates"][row]:g}/s',11,ha='center')
        save(f,'4-allocation')
        for local,name in [(False,'5-local'),(True,'local-cpu')]:
            f,a=canvas(4.4);box(a,.04,.67,.35,.18,'CPU 主存：专家权重','blue',11);box(a,.61,.67,.35,.18,'GPU：输入激活','green',11)
            if local:
                arrow(a,(.61,.76),(.39,.76));box(a,.04,.31,.35,.18,'CPU 专家计算','blue');arrow(a,(.215,.67),(.215,.49));arrow(a,(.39,.40),(.61,.40));box(a,.61,.31,.35,.18,'GPU 汇合结果','orange',11)
            else:
                arrow(a,(.39,.76),(.61,.76));box(a,.61,.31,.35,.18,'GPU 专家计算','green');arrow(a,(.785,.67),(.785,.49))
            text(a,.5,.13,'激活往返：每行共 16 KiB' if local else '搬运一份专家权重：36 MiB',12,ha='center');save(f,name)
        d=data['9-6'];f,a=plot(3.7)
        for key,label,c in [('cpu_ms','CPU 就地计算','#267398'),('weight_copy_gpu_ms','搬权重到 GPU','#388768')]:a.plot(d['tokens_per_expert'],d[key],label=label,color=c)
        a.set(xlabel='每个专家收到的输入行数',ylabel='八个专家的路径时间（ms）');a.legend(frameon=False);save(f,'6-reuse')
        for i,(experts,rows) in enumerate(zip(data['new-footprint']['active_experts'],data['new-footprint']['rows_per_expert'])):
            f,a=plot(3.5);a.bar(0,rows,width=experts,align='edge',color=COL['blue'],edgecolor=COL['line']);a.set(xlim=(0,136),ylim=(0,70),xlabel='不同专家数',ylabel='每专家输入行数');a.text(.5,.9,f'{experts} × {rows} = 512 次分派',transform=a.transAxes,ha='center',fontsize=12);save(f,'7-footprint' if i==0 else 'footprint-reuse')
        d=data['9-8'];f,a=plot(3.6)
        for k,l,c in [('one_message_ms','一次发送','#267398'),('many_messages_ms','72 次发送','#a56c28')]:
            # Stable source uses an explicit descriptive field for the second curve.
            vals=d.get(k,d.get('seventy_two_messages_ms'))
            if vals is None:vals=np.array(d['one_message_ms'])+71*np.array(d['startup_us'])/1000
            a.plot(d['startup_us'],vals,label=l,color=c)
        a.set(xlabel='每次启动开销（μs）',ylabel='同样 1.125 GiB 的总时间（ms）');a.legend(frameon=False);save(f,'8-handoff')
        for i,tasks in enumerate(data['new-balance']['assignments_per_card']):
            f,a=plot(4,left=.17);times=np.array(tasks)*2*18874368/1e14*1e6;a.barh(range(8),times,color=COL['blue'],edgecolor=COL['line']);a.axvline(max(times),ls='--',color='#a56c28');a.set(yticks=range(8),yticklabels=[f'卡 {j}' for j in range(8)],xlim=(0,205),xlabel='专家矩阵计算（μs）');a.invert_yaxis();save(f,'9-balance' if i==0 else 'balance-hotspot')
        d=data['9-10'];f,a=plot(3.6);a.plot(d['batches'],d['net_saving_ms'],color='#388768');a.axhline(0,color='#777777');a.set(xlabel='热点持续的批数',ylabel='累计净节省（ms）');save(f,'10-experts')
        for i,items in enumerate([[(0,0,.2),(1,.2,.6),(2,.8,.2)],[(0,0,.1),(0,.1,.1),(1,.1,.3),(1,.4,.3),(2,.4,.1),(2,.7,.1)]]):
            f,a=plot(3.5,left=.23)
            for row,start,dur in items:a.barh(row,dur,left=start,height=.5,color=COL[['blue','green','orange'][row]],edgecolor=COL['line'])
            a.set(yticks=[0,1,2],yticklabels=['分派','专家计算','结果合并'],xlim=(0,1.05),xlabel='时间（ms）');a.invert_yaxis();save(f,'11-overlap' if i==0 else 'overlap-pipeline')
        f,a=canvas(3.8);box(a,.04,.50,.34,.24,'目录记录\n标识 → 存储位置','orange',11);box(a,.62,.50,.34,.24,'KV 数据对象\n实际上下文状态','blue',11);arrow(a,(.38,.62),(.62,.62),'control');text(a,.5,.22,'先按目录定位，再确认对象可用并取回',12,ha='center');save(f,'cache-directory')
        f,a=canvas(4.5)
        for i in range(64):
            x=.04+i%16*.059;y=.72-i//16*.14;box(a,x,y,.05,.10,str(i+1),'orange' if i==63 else 'green',11)
        text(a,.5,.94,'读入 64 页，前 63 页可连续复用',14,ha='center');text(a,.5,.10,'绿色：1008 位置；橙色：16 位置仍需处理',11,ha='center');save(f,'12-cache')
        V=1207959552
        for i,(queue,band,compute) in enumerate([(250,None,10),(20,None,180),(20,5,10),(20,20,10)]):
            f,a=plot(3.0,left=.17);a.barh(0,queue,height=.45,color=COL['gray']);ready=0
            if band:
                for dur,c in [(10,'gray'),(V/(band*1e9)*1000,'orange'),(V/25e9*1000,'blue')]:a.barh(1,dur,left=ready,height=.45,color=COL[c],edgecolor=COL['line']);ready+=dur
            a.barh(0,compute,left=max(queue,ready),height=.45,color=COL['green']);a.set(yticks=[0,1],yticklabels=['GPU','取回'],xlim=(0,340),xlabel='从请求到达起计时（ms）');a.invert_yaxis();save(f,'13-route' if i==0 else f'route-{i}')
        f,a=plot(3.7);t=np.linspace(0,1,121);a.plot(t,1+.5*t,color='#a56c28',label='源端状态');a.plot(t,np.minimum(2*t,1+.5*t),color='#388768',label='已复制状态');a.set(xlabel='后台复制时间（s）',ylabel='累计状态（GiB）');a.legend(frameon=False);save(f,'14-migration')
        f,a=canvas(4.8)
        for row,title in enumerate(['已可靠记录的序列','故障前保存的 KV','恢复后继续生成']):
            y=.68-row*.27;text(a,.04,y+.20,title,13);box(a,.04,y,.36,.13,'输入 8192 位置','blue',11)
            if row!=1:box(a,.43,y,.32,.13,'输出 1—128','green',11);box(a,.78,y,.19,.13,'输出 129','orange',11)
            else:text(a,.68,y+.065,'生成部分尚未保存',11,ha='center')
        text(a,.5,.03,'补算 128 位置 → KV 到 8320 → 处理输出 129',11,ha='center');save(f,'15-recovery')
        for pooled,name in [(False,'16-composition'),(True,'composition-pool')]:
            f,a=canvas(3.6);nodes=['P','共享池','D'] if pooled else ['P','D'];xs=[.04,.40,.76] if pooled else [.04,.76]
            for x,n in zip(xs,nodes):box(a,x,.39,.20,.22,n,'orange' if n=='共享池' else 'blue')
            for x1,x2 in zip(xs,xs[1:]):arrow(a,(x1+.20,.5),(x2,.5));text(a,(x1+.20+x2)/2,.71,'1.125 GiB',11,ha='center')
            text(a,.5,.18,'完整写入并通知 D 后，D 再读取' if pooled else 'P 直接将完整状态交给 D',12,ha='center');save(f,name)
        d=data['9-17'];f,a=plot(3.7)
        for key,c in [('8','#388768'),('5','#a56c28')]:a.plot(d['time_s'],d['queues'][key],color=c,label=f'服务 {key} 请求/s')
        a.axvline(10,ls='--',color='#777777');a.set(xlabel='从启动开始计时（s）',ylabel='积压请求数',xlim=(0,55));a.legend(frameon=False);save(f,'17-service')
    out.finish();return out.outputs,out.checks
