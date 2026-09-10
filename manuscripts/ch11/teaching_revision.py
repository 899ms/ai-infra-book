"""Keep the task, its environment and its resource occupancy visually distinct."""
import numpy as np
import matplotlib.pyplot as plt
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,n):out.save(f,'figure-11-'+n)
    def timeline(name,model=9,env=False,rebuild=False):
        f,a=plot(3.7,left=.21);period=model+1
        for k in range(3):
            if env:a.barh(0,3 if rebuild else period,left=k*period+model-2 if rebuild else k*period,height=.55,color=COL['green'],edgecolor=COL['line'])
            else:
                a.barh(1,model,left=k*period,height=.5,color=COL['blue'],edgecolor=COL['line']);a.barh(0,1,left=k*period+model,height=.5,color=COL['orange'],edgecolor=COL['line'])
        a.set(yticks=[0] if env else [1,0],yticklabels=['2 GiB 内存'] if env else ['模型调用','工具 CPU'],xlabel='从任务到达计时（s）',xlim=(0,31),ylim=(-.7,1.6 if not env else .7));save(f,name)
    with plt.rc_context(STYLE):
        timeline('1-timeline');timeline('memory-area',env=True)
        for i,key in enumerate(['demand_9','demand_12']):
            f,a=plot(3.6,left=.24);v=data['capacity'][key];cap=data['capacity']['capacity'];a.barh(range(3),np.array(v)/cap*100,color=[COL[c] for c in ['orange','blue','green']],edgecolor=COL['line']);a.axvline(100,ls='--',color='#666')
            for j,(x,c) in enumerate(zip(v,cap)):a.text(x/c*100+2,j,f'{x}/{c}',fontsize=11,va='center')
            a.set(yticks=range(3),yticklabels=['CPU 核','模型并发','内存 GiB'],xlim=(0,170),xlabel='需求／容量（%）');a.invert_yaxis();save(f,'capacity' if i==0 else 'capacity-slow')
        f,a=canvas(4.5)
        for x,y,w,l,c in [(.04,.66,.32,'任务控制器','orange'),(.64,.66,.32,'模型服务','blue'),(.04,.19,.32,'环境平台','gray'),(.64,.19,.32,'工具环境','green')]:box(a,x,y,w,.22,l,c)
        for p,q in [((.36,.82),(.64,.82)),((.64,.71),(.36,.71)),((.2,.66),(.2,.41)),((.36,.35),(.64,.35)),((.64,.24),(.36,.24))]:arrow(a,p,q)
        text(a,.5,.94,'模型请求／完整工具参数',11,ha='center');text(a,.5,.09,'工具执行／保存结果／交回控制器',11,ha='center');save(f,'2-boundary')
        for i,l in enumerate(['进程','容器','microVM']):
            f,a=canvas(4.0);text(a,.04,.94,l+'的隔离边界',14);box(a,.04,.11,.92,.17,'宿主操作系统内核','gray')
            for j in range(2):
                x=.04+j*.48;box(a,x,.39,.44,.40,'','blue' if i<2 else 'green');text(a,x+.22,.67,'任务 '+str(j),12,ha='center');text(a,x+.22,.50,['私有地址空间','私有视图与配额','独立虚拟机内核'][i],11,ha='center');arrow(a,(x+.22,.39),(x+.22,.28))
            save(f,'isolation-'+str(i))
        f,a=canvas(4.2);box(a,.04,.62,.35,.24,'共享模板\n文件与依赖','blue');box(a,.61,.62,.35,.24,'环境私有内容\n修改页与管理数据','orange');box(a,.24,.13,.52,.24,'活跃环境内存\n进程、工作页与缓冲区','green')
        arrow(a,(.215,.62),(.40,.37));arrow(a,(.785,.62),(.60,.37));text(a,.5,.48,'加载执行所需内容',11,ha='center');save(f,'template-runtime')
        f,a=plot(4.0,left=.25);v=data['pages']['local_mib'];a.barh(range(4),v,color=COL['blue'],edgecolor=COL['line'])
        for i,x in enumerate(v):a.text(x+30,i,str(x),fontsize=11,va='center')
        a.set(yticks=range(4),yticklabels=['完整复制','按需加载','仅私有页','保留热点页'],xlim=(0,2500),xlabel='每环境本地内容（MiB）');a.invert_yaxis();save(f,'pages')
        for pause,name in [(False,'pause'),(True,'pause-release')]:
            f,a=plot(3.0,left=.21)
            for start,dur in ([(10,1),(18,1)] if pause else [(10,9)]):a.barh(0,dur,left=start,height=.5,color=COL['green'],edgecolor=COL['line'])
            a.set(yticks=[0],yticklabels=['2 GiB 内存'],xlim=(10,19),xticks=[10,11,14,18,19],xlabel='时间（s）');save(f,name)
        timeline('residency',env=True);timeline('residency-rebuild',env=True,rebuild=True)
        for lead,name in [(0,'3-lifecycle'),(1,'prewarm-1'),(2,'prewarm-2'),(3,'prewarm-3')]:
            f,a=plot(2.8,left=.22);start=4-lead;a.barh(0,2,left=start,height=.5,color=COL['blue'],edgecolor=COL['line'])
            if lead>2:a.barh(0,lead-2,left=start+2,height=.5,color=COL['orange'],edgecolor=COL['line'])
            a.axvline(4,ls='--',color='#666');a.set(yticks=[0],yticklabels=['准备环境'],xlim=(0,6.2),xlabel='时间（s）');save(f,name)
        f,a=plot(3.6,left=.25);a.barh(1,2,left=2,height=.5,color=COL['gray'],edgecolor=COL['line']);a.barh(0,2,left=4,height=.5,color=COL['blue'],edgecolor=COL['line']);a.axvline(4,ls='--',color='#666');a.set(yticks=[1,0],yticklabels=['误选环境','实际所需环境'],xlim=(0,6.2),xlabel='时间（s）');save(f,'prewarm-wrong')
        for after,name in [(False,'4-placement'),(True,'placement-after')]:
            f,a=canvas(4.1);text(a,.5,.93,'新作业需要：同节点四张 A 卡＋16 核',13,ha='center')
            for i,(gpu,cpu) in enumerate([('A',16 if after else 8),('B',24 if after else 32)]):
                x=.04+i*.49;box(a,x,.23,.43,.48,'','gray');text(a,x+.215,.62,f'节点 {i+1}',13,ha='center');text(a,x+.215,.47,f'4 张 {gpu} 型空闲卡',12,ha='center');text(a,x+.215,.33,f'{cpu} 个空闲 CPU 核',11,ha='center')
            save(f,name)
        for burst,name in [(False,'queue'),(True,'queue-burst')]:
            f,a=plot(5.0,left=.16)
            for i in range(10):
                arrive=0 if burst else i
                if burst:a.barh(i,i,left=0,height=.52,color=COL['gray'])
                a.barh(i,1,left=i,height=.52,color=COL['blue'],edgecolor=COL['line']);a.plot(arrive,i,'o',ms=4,color='#454545')
            a.set(yticks=range(10),yticklabels=[str(i+1) for i in range(10)],ylabel='工具调用',xlabel='时间（s）',xlim=(-.3,10.3));a.invert_yaxis();save(f,name)
        f,a=plot(3.8,left=.18)
        for i,row in enumerate(data['rl-stages']['stage_seconds']):
            start=0
            for j,(v,c,l) in enumerate(zip(row,['blue','orange','green','purple'],['生成','验证','更新','发布'])):a.barh(i,v,left=start,height=.5,color=COL[c],edgecolor=COL['line'],label=l if i==0 else None);start+=v
        a.set(yticks=[0,1],yticklabels=['原配置','生成加速'],xlim=(0,90),ylim=(-.5,2.1),xlabel='迭代时间（s）');a.legend(ncol=4,frameon=False,loc='upper left');save(f,'rl-stages')
        f,a=canvas(5.0);box(a,.27,.74,.46,.16,'发送端：200 Gbit/s','orange',12)
        for i in range(6):
            x=.04+(i%3)*.32;y=.43-(i//3)*.26;box(a,x,y,.28,.18,f'实例 {i+1}\n30 GB／50 Gbit/s','blue',11)
        arrow(a,(.5,.74),(.5,.66));text(a,.5,.64,'同一出口共传 180 GB',11,ha='center')
        for i in range(3):
            x=.18+i*.32;arrow(a,(x,.59),(x,.61));arrow(a,(x,.43),(x,.35))
        a.plot([.18,.82],[.59,.59],color=COL['line'],lw=1);text(a,.5,.05,'单份至少 4.8 s；全部至少 7.2 s',12,ha='center');save(f,'weights')
        for batch,name in [(False,'5-stages'),(True,'stages-batch')]:
            f,a=plot(3.1,left=.20)
            for i in range(3):a.barh(0,10,left=i*10+(20 if batch else 0),height=.5,color=COL[['blue','green','orange'][i]],edgecolor=COL['line']);a.plot(i*10,1,'o',color='#454545')
            a.set(yticks=[1,0],yticklabels=['样本到达','验证进程'],xlim=(-1,51),xlabel='时间（s）');save(f,name)
        f,a=plot(4.0,left=.20);a.barh(range(10),[1]*9+[100],height=.6,color=[COL['blue']]*9+[COL['orange']],edgecolor=COL['line']);a.axvline(10,ls='--',color='#666');a.set(yticks=[0,8,9],yticklabels=['样本 1','样本 9','样本 10'],xlim=(0,105),xlabel='验证时间（s）');a.invert_yaxis();save(f,'remaining-time')
        f,a=plot(3.9,left=.18)
        for i,row in enumerate(data['thinking']['cost_parts']):
            start=0
            for v,c,l in zip(row,['blue','orange','green'],['输入','思考','可见输出']):a.barh(i,v,left=start,height=.5,color=COL[c],edgecolor=COL['line'],label=l if i==0 else None);start+=v
        a.set(yticks=[0,1],yticklabels=['1000 思考','100 思考'],xlabel='单次调用成本',ylim=(-.5,2.0));a.legend(ncol=3,frameon=False,loc='upper left');save(f,'thinking')
        f,a=canvas(4.1);box(a,.04,.40,.23,.23,'任务控制器','orange',11);box(a,.38,.40,.23,.23,'服务入口','gray');box(a,.74,.68,.22,.19,'外部 API','blue',11);box(a,.74,.15,.22,.19,'自建副本','green',11);arrow(a,(.27,.515),(.38,.515));arrow(a,(.61,.56),(.74,.775));arrow(a,(.61,.46),(.74,.245));text(a,.50,.86,'按调用用量计费',11,ha='center');text(a,.5,.13,'按设备与运行支出计费',11,ha='center');save(f,'6-service')
        for quality,name in [(False,'7-routing'),(True,'routing-deadline')]:
            d=data['11-7'];h=np.array(d['h']);f,a=plot(4.0)
            if quality:a.plot(h*100,.98*h*100,color='#267398');a.axhline(90,ls='--',color='#a56c28');a.axvline(d['joint_target_hit']*100,ls='--',color='#666');a.set(ylabel='按时成功的提交比例（%）',ylim=(0,105))
            else:a.plot(h*100,d['cost_B'],label='服务 B',color='#267398');a.axhline(d['cost_A'],label='服务 A',color='#a56c28');a.axvline(d['cost_crossover']*100,ls='--',color='#666');a.set(ylabel='每个成功任务的成本');a.legend(frameon=False)
            a.set(xlabel='B 请求命中率（%）',xlim=(0,100));save(f,name)
        f,a=plot(3.8);n=np.linspace(0,200000,100);d=data['purchase'];a.plot(n/1e4,d['fixed']+n*d['self_per_task'],label='自建',color='#267398');a.plot(n/1e4,n*d['api_per_task'],label='按量 API',color='#388768');a.set(xlabel='提交任务数（万项）',ylabel='总成本');a.legend(frameon=False);save(f,'purchase')
        f,a=canvas(4.6)
        for x,l,c in [(.04,'控制器','orange'),(.64,'外部系统','blue')]:box(a,x,.69,.32,.17,l,c)
        arrow(a,(.36,.77),(.64,.77));text(a,.5,.95,'操作 ID：K',12,ha='center');box(a,.64,.39,.32,.17,'操作已提交','green',11);arrow(a,(.80,.69),(.80,.56));arrow(a,(.64,.46),(.36,.46),'control');text(a,.17,.46,'确认丢失',12,ha='center');arrow(a,(.36,.18),(.64,.18),'control');text(a,.5,.08,'恢复后先按 K 查询结果',12,ha='center');save(f,'commit-ack')
        # Split the probability tree at the local-repair node to keep edge labels readable.
        f,a=canvas(5.3);box(a,.30,.75,.40,.17,'首次尝试：10 s','blue')
        for x,l,c in [(.02,'首次成功\n80%','green'),(.355,'局部修复\n12%','orange'),(.69,'直接升级\n8%','purple')]:box(a,x,.37,.29,.22,l,c);arrow(a,(.5,.75),(x+.145,.59))
        text(a,.5,.18,'下方比例均以全部提交为分母',11,ha='center');save(f,'retry-tree')
        f,a=canvas(5.4);box(a,.29,.74,.42,.18,'进入修复：全部的 12%','orange',11)
        box(a,.04,.37,.37,.22,'修复成功：7.2%\n累计 14 s','green',11);box(a,.59,.37,.37,.22,'修复后升级：4.8%\n累计 22 s','purple',11)
        arrow(a,(.40,.74),(.225,.59));arrow(a,(.60,.74),(.775,.59));text(a,.18,.68,'条件 60%',11,ha='center');text(a,.82,.68,'条件 40%',11,ha='center');text(a,.5,.19,'12% × 60% = 7.2%\n12% × 40% = 4.8%',12,ha='center');save(f,'retry-conditional')
        f,a=plot(4.0,bottom=.28);v=data['11-8']['policy_costs'];a.bar(range(3),v,color=[COL[c] for c in ['blue','green','orange']],edgecolor=COL['line'])
        for i,y in enumerate(v):a.text(i,y+.00035,f'{y:.4f}',ha='center',fontsize=12)
        a.set(xticks=range(3),xticklabels=['仅首次\n成功任务','有限恢复\n成功任务','有限恢复\n按时成功'],ylabel='全部支出／符合条件的任务数',ylim=(0,.018));save(f,'8-retry')
        f,a=plot(3.6,left=.20)
        for i,model in enumerate([9,6]):
            for k in range(3):a.barh(i,model,left=k*(model+1),height=.5,color=COL['blue'],edgecolor=COL['line']);a.barh(i,1,left=k*(model+1)+model,height=.5,color=COL['orange'],edgecolor=COL['line'])
        a.axvline(24,ls='--',color='#a56c28');a.set(yticks=[0,1],yticklabels=['普通模型','快速模型'],xlim=(0,31),xlabel='完成时间（s）');save(f,'decision')
    from core_principles_figures import draw as draw_principles
    draw_principles(11, out)
    out.finish();return out.outputs,out.checks
