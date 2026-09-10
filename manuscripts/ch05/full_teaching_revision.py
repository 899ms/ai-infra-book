"""Extend the approved 5.2–5.3 style to execution, compilation and runtime."""
import numpy as np
import matplotlib.pyplot as plt
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,name):out.save(f,'figure-5-'+name)
    with plt.rc_context(STYLE):
        d=data['5-1'];f,a=plot(3.6,left=.20)
        cells=[]
        for y,kernel in enumerate(d['kernel_us']):
            start=0
            for dur,label,c in [(3,'提\n交','orange'),(8,'H2D','blue'),(kernel,'内核','green'),(4,'D2H','purple')]:
                cell=a.barh(y,dur,left=start,height=.64,color=COL[c],edgecolor=COL['line'])[0]
                label_artist=a.text(start+dur/2,y,label,fontsize=12,ha='center',va='center',linespacing=1.15)
                cells.append((cell,label_artist))
                start+=dur
        a.set(yticks=[0,1],yticklabels=['原内核','内核加快'],xlim=(0,37),ylim=(-.6,1.6),xlabel='从 CPU 提交起计时（μs）')
        a.invert_yaxis()
        # Preserve proportional durations and require padding inside every cell.
        f.canvas.draw();renderer=f.canvas.get_renderer();padding=2*f.dpi/72
        for cell,label_artist in cells:
            outer=cell.get_window_extent(renderer);inner=label_artist.get_window_extent(renderer)
            if not (outer.x0+padding <= inner.x0 and inner.x1 <= outer.x1-padding
                    and outer.y0+padding <= inner.y0 and inner.y1 <= outer.y1-padding):
                raise ValueError(f'figure-5-1: label must fit inside its cell: {label_artist.get_text()}')
        save(f,'1-execution')
        f,a=canvas(4.6);text(a,.04,.94,'缩进层级决定保存到何时',14)
        box(a,.04,.08,.92,.76,'','gray');text(a,.07,.79,'遍历输出块 io、jo',14)
        box(a,.12,.62,.76,.10,'创建 FP32 累加器：16 KiB','green')
        box(a,.15,.29,.70,.26,'','blue');text(a,.18,.49,'循环 ko：共 128 次',12)
        text(a,.20,.38,'读取 A、W 块 → 更新累加器',11)
        box(a,.12,.12,.76,.10,'归约结束 → BF16 舍入 → SiLU','orange',11)
        arrow(a,(.5,.62),(.5,.55));arrow(a,(.5,.29),(.5,.22));save(f,'9-polyhedral')
        f,a=canvas(3.8)
        for y,title,expr,c in [(.57,'先相加，再激活','1 + (−1) = 0 → SiLU(0) = 0','green'),(.12,'先分别激活，再相加','SiLU(1) + SiLU(−1) ≈ 0.4621','orange')]:
            text(a,.04,y+.25,title,14);box(a,.04,y,.92,.17,expr,c)
        save(f,'activation-order')
        f,a=canvas(3.8);text(a,.04,.94,'先读完整行，才能确定整行量化尺度',14)
        box(a,.04,.60,.40,.18,'块 0：最大值 1','blue');box(a,.56,.60,.40,.18,'块 1：最大值 10','orange')
        arrow(a,(.24,.60),(.42,.43));arrow(a,(.76,.60),(.58,.43));box(a,.20,.28,.60,.14,'整行最大值为 10','green')
        text(a,.5,.11,'第一项：1 → 44.8 → 舍入 44 → 55/56',12,ha='center');save(f,'quantization-scale')
        f,a=canvas(4.3)
        for y,title,label,c in [(.59,'保存低位宽中间结果','读原输入 32 + 写量化 16 + 重读 192','green'),(.13,'每个列块重新量化','读原输入求尺度 32 + 重读原输入 384','orange')]:
            text(a,.04,y+.26,title,14);box(a,.04,y,.92,.17,label,c,11)
            text(a,.50,y-.065,'输入相关：240 MiB' if c=='green' else '输入相关：416 MiB',12,ha='center')
        save(f,'10-quantization')
        d=data['5-11'];f,a=plot(3.4);p=np.linspace(0,1,101);a.axhline(10,color='#267398',label='原实现');a.plot(p,20-15*p,color='#a56c28',label='新实现');a.axvline(2/3,ls=':',color='#777777');a.set(xlim=(0,1),ylim=(0,23),xlabel='形状 A 的调用比例',ylabel='平均执行时间（μs）');a.legend(frameon=False);save(f,'11-feedback')
        # One trace panel per capture; exact event times remain tied to source records.
        ranges=data['5-12']['ranges']
        for i,r in enumerate(ranges):
            f,a=plot(2.9,left=.20)
            for event in r['kernels']:a.barh(1,(event['end_ns']-event['start_ns'])/1000,left=(event['start_ns']-r['start_ns'])/1000,height=.38,color=COL['green'],edgecolor=COL['line'],lw=.5)
            # Host API collection is emitted by the fixed trace-analysis source.
            events=r.get('launches',r.get('apis',[]))
            for event in [e for e in events if 'Launch' in e['name']]:a.barh(0,(event['end_ns']-event['start_ns'])/1000,left=(event['start_ns']-r['start_ns'])/1000,height=.38,color=COL['blue'],edgecolor=COL['line'],lw=.5)
            a.set(yticks=[0,1],yticklabels=['主机启动','设备内核'],xlim=(0,(r['end_ns']-r['start_ns'])/1000),ylim=(-.6,1.6),xlabel='从本段采集起点计时（μs）');a.invert_yaxis();save(f,'12-runtime' if i==0 else f'runtime-{i}')
        f,a=canvas(3.7);text(a,.04,.94,'图重放按已记录的地址读取输入',14)
        box(a,.04,.62,.34,.18,'本次新输入\n地址 X','blue');box(a,.62,.62,.34,.18,'固定图缓冲\n地址 G','orange');arrow(a,(.38,.71),(.62,.71))
        text(a,.5,.51,'X 与 G 不同时，复制到 G',11,ha='center')
        box(a,.24,.13,.52,.16,'重放设备图，读取 G','green');arrow(a,(.79,.62),(.5,.29));save(f,'graph-address')
        d=data['5-13'];f,a=plot(3.5,left=.25)
        for y,(prep,copy) in enumerate(zip(d['prepare_us'],d['copy_us'])):
            for start,dur,c in [(0,prep,'orange'),(prep,copy,'blue'),(prep+copy,20,'green')]:a.barh(y,dur,left=start,height=.5,color=COL[c],edgecolor=COL['line'])
        a.set(yticks=range(3),yticklabels=['普通提交','图：2 MiB 输入','图：16 MiB 输入'],xlim=(0,46),xlabel='准备、复制与计算总时间（μs）');a.invert_yaxis()
        for c,label in [('orange','准备'),('blue','复制'),('green','计算')]:a.barh([],[],color=COL[c],label=label)
        a.legend(ncol=3,loc='upper center',bbox_to_anchor=(.5,1.02),frameon=False);save(f,'13-graph-copy')
        d=data['5-14'];f,a=plot(3.5);r=np.arange(1,141)
        for row,col,label in zip(d['policies'],['#267398','#388768','#a56c28'],['通用','分桶','特化']):a.plot(r,(row['prepare_ns']+r*row['cohort_execution_ns'])/1e6,color=col,label=label)
        a.set(xlabel='重复执行的组数',ylabel='准备加执行（ms）',xlim=(0,140));a.legend(frameon=False);save(f,'14-specialization')
        d=data['5-15']
        for fine,name in [(False,'15-persistent'),(True,'persistent-blocks')]:
            f,a=plot(3.5,left=.19)
            proj=d['projection_us']+(.7 if fine else 0);act=d['activation_us']+(.7 if fine else 0)
            first=5+proj if fine else 10+8*proj
            for i in range(8):
                a.barh(0,proj,left=5+i*proj,height=.45,color=COL['blue'],edgecolor=COL['line']);a.barh(1,act,left=first+i*act,height=.45,color=COL['green'],edgecolor=COL['line'])
            a.set(yticks=[0,1],yticklabels=['投影','激活'],xlim=(0,610),ylim=(-.6,1.6),xlabel='时间（μs）');a.invert_yaxis();a.axvline(first,ls='--',color='#a56c28');save(f,name)
        f,a=canvas(4.9)
        for i,A in enumerate([60,15]):
            y=.58-i*.45;text(a,.04,y+.32,f'A 为 {A} μs：请求 {10+max(A,40)+10} μs',14)
            box(a,.04,y+.06,.20,.15,'准备 10','gray',11);box(a,.38,y+.16,.24,.13,f'A：{A}','orange');box(a,.38,y-.03,.24,.13,'B：40','blue');box(a,.76,y+.06,.20,.15,'收尾 10','green',11)
            for yy in [y+.225,y+.035]:arrow(a,(.24,y+.135),(.38,yy));arrow(a,(.62,yy),(.76,y+.135))
        save(f,'16-critical-path')
        d=data['5-17'];v=[r['latency_saving_ms'] for r in d['pairs']];f,a=plot(3.8)
        a.axhline(0,color='#555555',lw=.8);a.vlines(range(1,12),0,v,color='#267398');a.scatter(range(1,12),v,color='#267398');a.axhline(np.median(v),color='#a56c28',ls='--',label=f'中位数 {np.median(v):.1f} ms')
        a.set(xlim=(.5,11.5),ylim=(-3.2,5.4),xticks=range(1,12),xlabel='配对轮次',ylabel='原请求减新请求耗时（ms）');a.legend(frameon=False);save(f,'17-request')
    from v41_case_figures import draw as draw_v41
    draw_v41(5, out)
    out.finish();return out.outputs,out.checks
