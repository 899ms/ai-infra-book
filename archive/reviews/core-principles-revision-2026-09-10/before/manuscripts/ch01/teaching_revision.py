"""Chapter 1: one question per book-size figure. Inputs come from build.py's locked evidence."""
import numpy as np
import matplotlib.pyplot as plt
from figure_style import COL, STYLE, canvas, plot, text, box, arrow, Exporter

def draw(here,data):
    out=Exporter(here)
    with plt.rc_context(STYLE):
        f,a=canvas(5.2)
        layers=[('应用与任务','要完成什么，何时完成','orange'),
                ('模型与负载','需要哪些计算和数据','blue'),
                ('训练与推理系统','安排请求、批次和设备','green'),
                ('算子与编译运行时','把运算变成可执行程序','purple'),
                ('处理器与存储','计算并保存数据','blue'),
                ('互联与数据中心','连接设备，提供电力与散热','gray')]
        for i,(title,body,c) in enumerate(layers):
            y=.825-i*.153
            box(a,.06,y,.88,.125,title+'\n'+body,c)
            if i<5:arrow(a,(.5,y),(.5,y-.028))
        out.save(f,'figure-1-1-panorama')

        f,a=canvas(4.4)
        for x,label,c in [(.02,'应用\n组织输入','orange'),(.36,'服务入口\n接收请求','gray'),(.70,'路由器\n选择实例','purple')]:
            box(a,x,.76,.28,.18,label,c)
        arrow(a,(.30,.85),(.36,.85));arrow(a,(.64,.85),(.70,.85))
        box(a,.02,.06,.96,.52,'','gray');text(a,.05,.53,'被选中的模型实例',14)
        box(a,.06,.17,.24,.22,'实例调度器\n组成批次','green')
        box(a,.38,.17,.24,.22,'CPU\n提交程序','blue')
        box(a,.70,.17,.24,.22,'GPU\n执行运算','orange')
        arrow(a,(.30,.28),(.38,.28));arrow(a,(.62,.28),(.70,.28))
        arrow(a,(.84,.76),(.84,.61));text(a,.49,.65,'请求进入实例',11,ha='center')
        out.save(f,'figure-1-2-request')

        f,a=canvas(3.7)
        box(a,.04,.82,.29,.13,'模型文件','gray');box(a,.04,.63,.92,.13,'显存：保存一份权重','blue')
        arrow(a,(.18,.82),(.18,.76));text(a,.46,.875,'启动时加载',11)
        for x,s in [(.05,'第 1 步'),(.37,'第 2 步'),(.69,'第 3 步')]:
            box(a,x,.20,.26,.23,s+'\n计算单元','green')
            arrow(a,(x+.13,.63),(x+.13,.44))
        text(a,.50,.55,'每步从显存读取所需权重',12,ha='center')
        arrow(a,(.31,.31),(.37,.31));arrow(a,(.63,.31),(.69,.31))
        text(a,.5,.08,'前一步输出成为下一步输入',12,ha='center')
        out.save(f,'figure-1-weight-lifetime')

        f,a=canvas(4.8)
        box(a,.04,.77,.40,.17,'入口与共享存储','gray');box(a,.57,.77,.39,.17,'其他超节点','purple')
        box(a,.20,.56,.60,.12,'数据中心网络','green')
        arrow(a,(.24,.77),(.38,.68));arrow(a,(.76,.77),(.62,.68))
        box(a,.02,.025,.96,.44,'','gray');text(a,.05,.425,'放大一个超节点',14)
        box(a,.08,.27,.36,.11,'CPU 与主存','blue');box(a,.61,.27,.31,.11,'网卡','green')
        arrow(a,(.5,.56),(.76,.39));arrow(a,(.44,.325),(.61,.325))
        for x in [.08,.61]:box(a,x,.07,.31,.13,'GPU 与显存','orange')
        arrow(a,(.235,.27),(.235,.20));arrow(a,(.765,.27),(.765,.20))
        arrow(a,(.39,.135),(.61,.135));text(a,.50,.235,'内部互联',11,ha='center')
        out.save(f,'figure-1-3-datacenter')

        f,a=plot(3.4,left=.29)
        names=['主存访问','机房内往返','磁盘寻道']; vals=[100,500000,10000000]
        a.barh(names,vals,color=[COL['blue'],COL['green'],COL['orange']],edgecolor=COL['line'],height=.5)
        a.set_xscale('log');a.set_xlim(10,1e8);a.set_xlabel('时间（ns，对数刻度）');a.invert_yaxis()
        for i,(v,label) in enumerate(zip(vals,['0.1 μs','0.5 ms','10 ms'])):a.text(v*1.35,i,label,va='center',fontsize=12)
        out.save(f,'figure-1-4-numbers')

        capacity=data['capacity_example']
        bf16=capacity['bf16_weight_bytes']/1e9
        int8=capacity['int8_weight_and_metadata_bytes']/1e9
        f,a=plot(3.5,left=.25)
        for y,v,c in [(3,bf16,'orange'),(2,bf16/2,'blue'),(1,bf16/2,'blue'),(0,int8,'green')]:
            a.barh(y,v,height=.55,color=COL[c],edgecolor=COL['line'])
            a.text(6,y,f'{v:.2f} GB',va='center',fontsize=12)
        a.axvline(80,color='#80542e',ls='--',lw=1);a.text(82,3.65,'单卡容量 80 GB',fontsize=11)
        a.axhline(.5,color='#999999',lw=.7)
        a.set(yticks=[3,2,1,0],yticklabels=['BF16 单卡','BF16 卡 0','BF16 卡 1','8 比特单卡'],
              xlim=(0,190),ylim=(-.55,4.05),xlabel='权重及量化附加数据（GB）',xticks=[0,40,80,120,160])
        out.save(f,'figure-1-capacity-path')

        f,a=canvas(3.0)
        box(a,.04,.58,.37,.24,'显存\n70 GB 权重','blue');box(a,.61,.58,.35,.24,'计算单元\n完成乘加','green')
        arrow(a,(.41,.70),(.61,.70));text(a,.5,.45,'读取路径：3350 GB/s',12,ha='center')
        text(a,.5,.25,'70 GB ÷ 3350 GB/s ≈ 20.90 ms',14,ha='center')
        text(a,.5,.09,'每参数一字节，每步完整读取一遍',11,ha='center')
        out.save(f,'figure-1-read-path')

        f,a=plot(3.7,left=.25)
        comp=data['teaching']['compute_ms'];mem=data['teaching']['weight_read_ms']
        labels=['原设备','算力翻倍','带宽翻倍'];y=np.arange(3)
        a.barh(y+.16,[mem,mem,mem/2],height=.29,color=COL['blue'],edgecolor=COL['line'],label='读取权重')
        a.barh(y-.16,[comp,comp/2,comp],height=.29,color=COL['orange'],edgecolor=COL['line'],label='矩阵计算')
        for i,v in enumerate([mem,mem,mem/2]):a.text(v+.4,i+.16,f'{v:.2f}',fontsize=12,va='center')
        a.set(yticks=y,yticklabels=labels,xlim=(0,25),xlabel='资源时间下界（ms）');a.invert_yaxis();a.legend(loc='lower right',frameon=False)
        out.save(f,'figure-1-5-budget')

        f,a=canvas(3.5)
        text(a,.04,.91,'同一份权重，为八个请求服务',14)
        box(a,.04,.64,.92,.15,'一次读取：70 GB 权重','blue')
        for i in range(8):
            x=.04+i*.117;box(a,x,.24,.105,.18,str(i+1),'green');arrow(a,(x+.052,.63),(x+.052,.43))
        text(a,.5,.52,'八条输入各自完成运算',12,ha='center')
        text(a,.5,.10,'整批约 20.90 ms；每输出分摊约 2.61 ms',12,ha='center')
        out.save(f,'figure-1-batch-reuse')

        d=data['teaching_diagrams']['batch_transition'];b=np.array(d['batch'])
        f,a=plot(3.8)
        a.plot(b,comp*b,color='#a96c28',label='矩阵计算');a.axhline(mem,color='#267398',label='权重读取')
        a.plot(b,np.maximum(comp*b,mem),color='#333333',ls='--',label='两者最大值')
        a.axvline(d['crossing_batch'],color='#777777',ls=':',lw=1)
        a.text(156,mem+4,'约 148',fontsize=12);a.set(xlim=(0,512),ylim=(0,80),xlabel='批内请求数 B',ylabel='时间下界（ms）')
        a.legend(loc='upper left',frameon=False);out.save(f,'figure-1-batch-transition')
        f,a=plot(3.4)
        a.plot(b,d['throughput'],color='#267398',lw=1.8);a.axvline(d['crossing_batch'],ls=':',color='#777777')
        a.set(xlim=(0,512),ylim=(0,8000),xlabel='批内请求数 B',ylabel='输出吞吐（token/s）')
        a.text(180,6200,'计算项开始主导',fontsize=12);out.save(f,'figure-1-batch-throughput')

        rows=data['measured_short_group']
        for key,ylabel,name in [('throughput','整批输出吞吐（token/s）','figure-1-measured-throughput'),('tpot_ms','每请求输出间隔（ms）','figure-1-measured-tpot')]:
            f,a=plot(3.3)
            vals=[r[key] for r in rows];a.plot(range(4),vals,'o-',color='#267398',lw=1.5)
            for i,v in enumerate(vals):a.annotate(f'{v:.2f}',(i,v),xytext=(0,10),textcoords='offset points',ha='center',fontsize=11)
            a.set(xlim=(-.45,3.45),ylim=(0,max(vals)*1.23),xticks=range(4),xticklabels=[r['batch'] for r in rows],xlabel='同时请求数（各档等距排列）',ylabel=ylabel)
            out.save(f,name)

        for slug,title,items in [
            ('tpu','增加专用计算与数据搬运资源',[('输入缓冲','blue'),('矩阵计算阵列','orange'),('输出缓冲','green')]),
            ('smartnic','把包处理放到数据经过的位置',[('网络数据','blue'),('可编程网卡\n完成包处理','orange'),('主机 CPU\n运行应用','green')]),
            ('ub','让多台设备直接交换所需数据',[('设备 0\n计算与存储','blue'),('统一互联\n传递数据','green'),('设备 1\n计算与存储','orange')])]:
            f,a=canvas(2.5);text(a,.04,.89,title,14)
            for i,(label,c) in enumerate(items):
                x=.03+.335*i;box(a,x,.30,.27,.34,label,c)
                if i<2:arrow(a,(x+.27,.47),(x+.335,.47))
            out.save(f,'figure-1-design-'+slug)
    return out.finish()
