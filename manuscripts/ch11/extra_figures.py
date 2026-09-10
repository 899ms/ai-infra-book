"""Teaching figures: stage order, resource occupancy, and cost composition."""
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction

def draw(save, C, data, canvas, box, arrow, design, lifecycle):
    def chart(height=4.8,left=.19):
        f,a=plt.subplots(figsize=(11,height));f.subplots_adjust(left=left,right=.93,bottom=.19,top=.87)
        a.grid(axis='x',alpha=.15);a.set_axisbelow(True)
        return f,a
    def done(f,key,values):
        save(f,'figure-11-'+key);data[key]=values
    # Same workload, different limiting resource.
    f,a=chart();labels=['CPU 核数','并发模型调用数','内存 / GiB'];before=[30/40,270/300,600/640];after=[30/40,360/300,780/640]
    y=np.arange(3)
    a.barh(y+.18,np.array(before)*100,.30,color=C['blue'],label='每次模型调用 9 s')
    a.barh(y-.18,np.array(after)*100,.30,color=C['orange'],label='每次模型调用 12 s')
    for i,(v,w) in enumerate(zip(before,after)):
        a.text(v*100+1,i+.18,['30 / 40','270 / 300','600 / 640'][i],va='center',fontsize=11)
        a.text(w*100+1,i-.18,['30 / 40','360 / 300','780 / 640'][i],va='center',fontsize=11)
    a.axvline(100,color=C['red'],ls='--');a.set(yticks=y,yticklabels=labels,xlim=(0,150),xlabel='需求 / 容量（%）');a.invert_yaxis();a.legend(loc='lower center',bbox_to_anchor=(.5,1.02),ncol=2,frameon=False)
    done(f,'capacity',{'demand_9':[30,270,600],'demand_12':[30,360,780],'capacity':[40,300,640]})
    # Page footprint: common horizontal scale reveals replicated bytes.
    f,a=chart();parts=[[2048,0,4],[512,0,4],[0,128,4],[256,128,4]];colors=[C['blue'],C['orange'],C['teal']]
    for i,row in enumerate(parts):
        start=0
        for v,c in zip(row,colors):a.barh(i,v,left=start,color=c,height=.52);start+=v
        a.text(start+25,i,f'{sum(row):,} MiB',va='center')
    a.set(yticks=range(4),yticklabels=['完整复制','仅加载访问内容','共享只读内容','共享＋保留常用页'],xlim=(0,2440),xlabel='每个环境在本地保存的数据 / MiB');a.invert_yaxis()
    for c,l in zip(colors,['本地内容','私有修改页','管理开销']):a.plot([],[],color=c,lw=8,label=l)
    a.legend(frameon=False,loc='lower right');done(f,'pages',{'local_mib':[sum(x) for x in parts],'shared_template_mib':2048})
    # Pause one gap; memory area is the central relationship.
    f,a=chart();a.broken_barh([(10,9)],(1.1,.5),facecolors=C['blue']);a.text(14.5,1.35,'2 GiB × 9 s = 18 GiB·s',ha='center',va='center',color='white')
    a.broken_barh([(10,1),(18,1)],(.1,.5),facecolors=C['teal']);a.text(10.5,.8,'保存',ha='center');a.text(18.5,.8,'恢复',ha='center');a.text(14.5,.35,'中间 7 s 释放内存',ha='center')
    a.set(yticks=[1.35,.35],yticklabels=['持续保留','暂停后恢复'],xlim=(10,19),ylim=(-.25,2),xticks=range(10,20),xlabel='任务开始后的时间 / s')
    a.text(14.5,1.8,'第二轮工具在第 19 秒开始，两种方案相同',ha='center');done(f,'pause',{'gap':[10,19],'resident_gib_seconds':18,'paused_gib_seconds':4})
    # Entire task memory occupied only in prep/tool phases.
    f,a=chart();a.broken_barh([(0,30)],(1.25,.5),facecolors=C['blue']);a.text(15,1.5,'60 GiB·s',ha='center',va='center',color='white')
    for start in [7,17,27]:
        a.broken_barh([(start,2)],(.25,.5),facecolors=C['teal']);a.broken_barh([(start+2,1)],(.25,.5),facecolors=C['orange'])
    a.set(yticks=[1.5,.5],yticklabels=['全程保留环境','每轮重建环境'],xlim=(0,30),ylim=(-.2,2.2),xticks=[0,7,9,10,17,19,20,27,29,30],xlabel='任务开始后的时间 / s')
    a.text(15,1,'三段各占 2 GiB × 3 s，合计 18 GiB·s',ha='center',fontsize=12)
    for c,l in [(C['teal'],'准备环境'),(C['orange'],'运行工具')]:a.plot([],[],color=c,lw=8,label=l)
    a.legend(loc='upper left',bbox_to_anchor=(0,1.15),ncol=2,frameon=False);done(f,'residency',{'preparation_starts':[7,17,27],'gib_seconds':[60,18]})
    # Bursts queue despite identical service work.
    f,axes=plt.subplots(1,2,figsize=(11,5),sharey=True);f.subplots_adjust(left=.09,right=.97,top=.84,bottom=.16,wspace=.15)
    for a,burst in zip(axes,[False,True]):
        for i in range(10):
            if burst and i:a.barh(i,i,left=0,color=C['gray'],height=.65)
            a.barh(i,1,left=i,color=C['blue'],height=.65);a.plot(0 if burst else i,i,'o',color=C['red'],ms=4)
        a.set(xlim=(-.3,10),ylim=(9.7,-.8),yticks=range(10),yticklabels=range(1,11),xlabel='时间 / s');a.grid(axis='x',alpha=.15);a.set_title('同时到达：平均等待 4.5 s' if burst else '每秒到达一项：无需等待')
    axes[0].set_ylabel('任务编号');axes[1].plot([],[],'o',color=C['red'],label='到达');axes[1].plot([],[],color=C['gray'],lw=8,label='排队');axes[1].plot([],[],color=C['blue'],lw=8,label='执行');axes[1].legend(ncol=3,frameon=False,loc='lower center',bbox_to_anchor=(.5,1.08))
    done(f,'queue',{'service_seconds':[1]*10,'arrival_even':list(range(10)),'arrival_burst':[0]*10,'start':list(range(10))})
    # Amdahl visible as unchanged blocks.
    f,a=chart();rows=[[40,10,30,5],[20,10,30,5]];colors=[C['blue'],C['orange'],C['teal'],C['muted']]
    for i,row in enumerate(rows):
        left=0
        for j,(v,c) in enumerate(zip(row,colors)):
            a.barh(i,v,left=left,color=c,height=.5);a.text(left+v/2,i,str(v),ha='center',va='center',color='white');left+=v
        a.text(left+1,i,f'合计 {left} s',va='center')
    for c,l in zip(colors,['生成','验证','更新','发布']):a.plot([],[],color=c,lw=8,label=l)
    a.set(yticks=[0,1],yticklabels=['原配置','生成速度加倍'],xlim=(0,100),xlabel='每轮时间 / s');a.invert_yaxis();a.legend(ncol=4,frameon=False,loc='lower center',bbox_to_anchor=(.5,1.03))
    done(f,'rl-stages',{'stage_seconds':rows})
    # Shared network link is a physical constriction.
    f,a=canvas(5.7);box(a,.02,.38,.22,.24,'训练实例','完整权重 30 GB');box(a,.32,.38,.23,.24,'共享发送出口','200 Gbit/s','sand');arrow(a,(.24,.5),(.32,.5))
    for i,y in enumerate([.80,.47,.14]):
        box(a,.74,y-.08,.23,.19,f'接收实例 {i*2+1}、{i*2+2}','各接收 30 GB',size=12);arrow(a,(.55,.5),(.73,y+.015))
    a.text(.62,.93,'6 个实例，各 50 Gbit/s',ha='center',fontsize=13)
    a.text(.40,.22,'出口累计发送 6 × 30 = 180 GB',ha='center',fontsize=13)
    a.text(.40,.12,'全部传完至少 7.2 s',ha='center',fontsize=15,weight='bold')
    done(f,'weights',{'weight_gb':30,'receivers':6,'sender_gbps':200,'receiver_gbps':50,'lower_seconds':7.2})
    # Cost composition preserves the fixed portion.
    f,a=chart();rows=[[.020,.010,.002],[.020,.001,.002]];colors=[C['blue'],C['orange'],C['teal']]
    for i,row in enumerate(rows):
        left=0
        for v,c in zip(row,colors):a.barh(i,v,left=left,color=c,height=.5);left+=v
        a.text(left+.0005,i,f'{left:.3f}',va='center')
    for c,l in zip(colors,['输入 0.020','思考 0.010 → 0.001','可见输出 0.002']):a.plot([],[],color=c,lw=8,label=l)
    a.set(yticks=[0,1],yticklabels=['思考 1,000 token','思考 100 token'],xlim=(0,.038),xlabel='每次调用成本');a.invert_yaxis();a.legend(frameon=False,loc='lower center',bbox_to_anchor=(.5,1.02),ncol=3,fontsize=10)
    done(f,'thinking',{'cost_parts':rows})
    # Fixed intercept and marginal slope.
    f,a=chart(left=.12);n=np.linspace(0,200000,201);a.plot(n/1000,1000+.002*n,label='自建：1,000 + 0.002N',color=C['blue']);a.plot(n/1000,.012*n,label='API：0.012N',color=C['orange'])
    a.scatter([100],[1200],color=C['teal']);a.axvline(100,color=C['muted'],ls='--',lw=1);a.annotate('100,000 项时成本相等',(100,1200),(65,2050),arrowprops={'arrowstyle':'->','color':C['muted']});a.set(xlabel='提交任务数 / 千项',ylabel='总成本',xlim=(0,200),ylim=(0,2600));a.legend(frameon=False,loc='upper left')
    done(f,'purchase',{'fixed':1000,'self_per_task':.002,'api_per_task':.012,'crossover':100000})
    # Six terminal paths with time and deadline, linked to probability tree.
    f,a=canvas(7);box(a,.01,.40,.18,.19,'首次尝试','10 s；成本 0.010',size=12)
    box(a,.33,.64,.20,.17,'局部修复','再用 4 s；0.006',size=12)
    box(a,.33,.20,.20,.17,'直接升级','再用 8 s；0.030',size=12)
    box(a,.66,.89,.31,.09,'首次成功：80% · 10 s',color='green',size=12)
    box(a,.66,.72,.31,.09,'修复成功：7.2% · 14 s',color='green',size=12)
    box(a,.66,.49,.31,.14,'修复后升级：22 s','成功 4.704%；失败 0.096%','sand',12)
    box(a,.66,.17,.31,.14,'直接升级：18 s','成功 7.84%；失败 0.16%','green',12)
    for p,q in [((.19,.5),(.33,.72)),((.19,.46),(.33,.28)),((.53,.76),(.66,.76)),((.53,.69),(.66,.56)),((.53,.28),(.66,.24))]:arrow(a,p,q)
    a.plot([.10,.10,.63],[.59,.935,.935],color=C['teal'],lw=1.7);arrow(a,(.63,.935),(.66,.935));a.text(.20,.95,'80%',fontsize=11)
    a.text(.24,.66,'12%',fontsize=11);a.text(.24,.31,'8%',fontsize=11);a.text(.56,.80,'60%',fontsize=11);a.text(.55,.62,'40%',fontsize=11)
    a.text(.81,.42,'超过 20 s 期限',ha='center',color=C['red'],fontsize=12)
    a.text(.5,.055,'先修复再升级多绕一步，成功结果也会迟到',ha='center',fontsize=14)
    done(f,'retry-tree',{'terminal_probabilities':['.8','.072','.04704','.00096','.0784','.0016'],'terminal_seconds':[10,14,22,22,18,18]})
    # Final decision ties back to initial trace.
    f,a=chart();rows=[('普通模型',9),('快速模型',6)]
    for i,(label,m) in enumerate(rows):
        for r in range(3):
            st=r*(m+1);a.barh(i,m,left=st,color=C['blue'],height=.5);a.barh(i,1,left=st+m,color=C['orange'],height=.5)
        a.text(3*(m+1)+.4,i,f'{3*(m+1)} s',va='center')
    a.axvline(24,color=C['red'],ls='--');a.text(24,-.52,'24 s 期限',ha='center',color=C['red']);a.set(yticks=[0,1],yticklabels=[x[0] for x in rows],xlim=(0,33),ylim=(1.6,-.8),xlabel='任务开始后的时间 / s')
    for c,l in [(C['blue'],'模型调用'),(C['orange'],'工具执行')]:a.plot([],[],color=c,lw=8,label=l)
    a.legend(frameon=False,loc='lower right');done(f,'decision',{'model_seconds':[9,6],'task_seconds':[30,21],'deadline':24})
