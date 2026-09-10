"""Follow state ownership, then execution dependencies, then recoverable progress."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,n):out.save(f,'figure-10-'+n)
    with plt.rc_context(STYLE):
        f,a=canvas(5.0)
        for x,y,w,l,c in [(.04,.70,.25,'输入样本','blue'),(.38,.70,.25,'前向计算','blue'),(.72,.70,.24,'损失','orange'),(.38,.39,.25,'反向计算','green'),(.04,.08,.25,'参数梯度','green'),(.38,.08,.25,'Adam 更新','purple'),(.72,.08,.24,'新权重','blue')]:box(a,x,y,w,.17,l,c)
        for p,q in [((.29,.785),(.38,.785)),((.63,.785),(.72,.785)),((.84,.70),(.63,.475)),((.38,.475),(.165,.25)),((.29,.165),(.38,.165)),((.63,.165),(.72,.165))]:arrow(a,p,q)
        text(a,.04,.95,'一次迭代：由预测误差得到下一份权重',13);text(a,.50,.63,'保存激活',11,ha='center');text(a,.75,.39,'更新时读取\n主权重与两份矩状态',11);save(f,'update-cycle')
        f,a=plot(4.7,left=.20,bottom=.16);vals=np.array(data['10-1']['allocations_bytes'])/1e9;left=np.zeros(2)
        for j,(l,c) in enumerate([('BF16 权重','blue'),('BF16 梯度','green'),('FP32 主权重','orange'),('一阶矩','purple'),('二阶矩','gray')]):a.barh([1,0],vals[:,j],left=left,height=.45,color=COL[c],edgecolor=COL['line'],label=l);left+=vals[:,j]
        a.set(yticks=[1,0],yticklabels=['推理权重','训练状态'],xlabel='容量（GB）',xlim=(0,145),ylim=(-.5,2.8));a.legend(frameon=False,ncol=2,loc='upper left');save(f,'1-state')
        for j,key in enumerate(['3/10','2/5','1/2']):
            f,a=plot(3.7);v=data['10-2']['compute'][key];a.bar(range(4),v,color=COL['blue'],edgecolor=COL['line']);a.scatter(range(4),data['10-2']['capacity'],marker='D',facecolors=COL['orange'],edgecolors=COL['line'],label='状态容量下限',zorder=3)
            for x,y in enumerate(v):a.text(x,y+.8,str(y),fontsize=12,ha='center')
            a.set(xticks=range(4),xticklabels=['4090','A100','H100','B200'],ylabel='必要设备数',ylim=(0,50));a.legend(frameon=False);save(f,'2-budget' if j==0 else f'budget-{j}')
        for stage in range(4):
            f,a=canvas(4.6);text(a,.04,.94,['普通数据并行','ZeRO-1：优化器相关状态分片','ZeRO-2：再将梯度分片','ZeRO-3：再将模型权重分片'][stage],13)
            for row,(l,c,split) in enumerate([('权重','blue',stage>=3),('梯度','green',stage>=2),('主权重＋矩','purple',stage>=1)]):
                y=.64-row*.22;text(a,.02,y+.07,l,11)
                for i in range(4):box(a,.29+i*.17,y,.15,.15,('片 '+str(i)) if split else '完整',c,11)
            for i in range(4):text(a,.365+i*.17,.84,'卡 '+str(i),11,ha='center')
            save(f,f'zero-{stage}')
        f,a=canvas(4.7)
        for i in range(4):
            x=.04+i*.235;box(a,x,.70,.21,.15,f'卡 {i}：片 {i}',['blue','green','orange','purple'][i],11);arrow(a,(x+.105,.70),(x+.105,.45))
        box(a,.04,.18,.92,.27,'','gray');text(a,.5,.12,'GPU 0 的执行缓冲区',12,ha='center')
        for i in range(4):box(a,.06+i*.225,.23,.205,.15,f'片 {i}',['blue','green','orange','purple'][i],11)
        text(a,.5,.03,'用完释放完整缓冲，原始分片继续保留',11,ha='center');save(f,'3-sharding')
        f,a=canvas(4.1);box(a,.04,.59,.29,.20,'上游梯度 dY','green');box(a,.63,.59,.33,.20,'本层：Y = XW','blue');arrow(a,(.33,.69),(.63,.69))
        box(a,.04,.18,.39,.20,'dX：传给前一层','green');box(a,.57,.18,.39,.20,'dW：更新本层参数','purple')
        arrow(a,(.70,.59),(.235,.38));arrow(a,(.83,.59),(.765,.38));save(f,'gradient-branches')
        for rebuild,name in [(False,'4-recompute'),(True,'recompute-rebuild')]:
            f,a=canvas(3.8);text(a,.04,.92,'反向前重建乘积' if rebuild else '从前向保存乘积',14)
            for i,l in enumerate(['前向相乘','等待反向','下投影反向']):text(a,.17+i*.33,.71,l,11,ha='center')
            box(a,.04,.41,.92,.14,'一直保留 a、u','blue')
            box(a,.71 if rebuild else .04,.18,.25 if rebuild else .92,.14,'h：6 MiB','orange',11)
            if rebuild:arrow(a,(.83,.41),(.83,.32))
            save(f,name)
        for gpu,name in [(False,'5-casting'),(True,'casting-gpu')]:
            f,a=canvas(4.5);box(a,.04,.65,.35,.20,'GPU：BF16\n96 MiB','blue');box(a,.61,.23,.35,.20,'CPU：FP32\n192 MiB','green')
            if gpu:box(a,.04,.23,.35,.20,'GPU：FP32\n192 MiB','orange');arrow(a,(.215,.65),(.215,.43));arrow(a,(.39,.33),(.61,.33));text(a,.5,.52,'链路传 192 MiB',11,ha='center')
            else:box(a,.61,.65,.35,.20,'CPU：BF16\n96 MiB','blue');arrow(a,(.39,.75),(.61,.75));arrow(a,(.785,.65),(.785,.43));text(a,.5,.52,'链路传 96 MiB',11,ha='center')
            text(a,.5,.08,'GPU 转换时同时占用 288 MiB' if gpu else '格式转换在 CPU 完成',12,ha='center');save(f,name)
        d=data['10-6'];f,a=plot(4.2)
        for k,l,c in [('total_gib','分片＋10 GiB 临时缓冲','#267398'),('persistent_gib','训练状态分片','#388768')]:a.plot(d['participants'],d[k],label=l,color=c)
        a.axhline(24,ls='--',color='#a56c28',label='可用 24 GiB');a.set(xlabel='分片参与者数',ylabel='每卡容量（GiB）',ylim=(0,47));a.legend(frameon=False);save(f,'6-candidates')
        for i,(label,d) in enumerate(data['10-7'].items()):
            f,a=plot(4.1,left=.18)
            for e in d['events']:
                if e['stage'] is None:continue
                a.barh(e['stage'],e['duration']*1000,left=e['start']*1000,height=.58,color=COL[{'F':'blue','B':'orange','update':'green'}[e['kind']]],edgecolor=COL['line'],linewidth=.5)
            a.set(yticks=range(4),yticklabels=[f'阶段 {j}' for j in range(4)],xlim=(0,355),xlabel='时间（ms）');a.invert_yaxis();a.set_title(f'{label}：{d["summary"]["step_makespan_seconds"]*1000:.0f} ms',loc='left');save(f,'7-pipeline' if i==0 else 'pipeline-1f1b')
        f,a=plot(3.4,left=.22)
        for e in data['10-7']['1F1B']['events']:
            if e['stage']==3 and e['end']*1000>65 and e['start']*1000<110:a.barh(0,min(e['end']*1000,110)-max(e['start']*1000,65),left=max(e['start']*1000,65),height=.5,color=COL[{'F':'blue','B':'orange','update':'green'}[e['kind']]],edgecolor=COL['line'])
        a.axvspan(93,95,color=COL['gray']);a.annotate('等输入：2 ms',(94,0),xytext=(82,.7),fontsize=12,arrowprops={'arrowstyle':'->'});a.set(xlim=(65,110),ylim=(-.6,1.2),yticks=[0],yticklabels=['阶段 3'],xlabel='时间（ms）',xticks=[65,75,85,95,105]);save(f,'pipeline-gap')
        f,a=plot(3.7)
        for i,(l,d) in enumerate(data['10-7'].items()):a.bar(np.arange(4)+(i-.5)*.34,np.array(d['summary']['reserved_activation_scope_peak_bytes'])/1e9,.32,color=COL[['blue','orange'][i]],edgecolor=COL['line'],label=l)
        a.set(xticks=range(4),xticklabels=[f'阶段 {i}' for i in range(4)],ylabel='激活与收发缓冲峰值（GB）',ylim=(0,3.4));a.legend(frameon=False);save(f,'pipeline-memory')
        for busy,name in [(False,'8-overlap'),(True,'overlap-busy')]:
            f,a=plot(3.2,left=.20);a.barh(1,5,color=COL['blue'],height=.5,edgecolor=COL['line'])
            if busy:a.barh(0,4,color=COL['gray'],height=.5,edgecolor=COL['line'])
            a.barh(0,3,left=4 if busy else 0,color=COL['orange'],height=.5,edgecolor=COL['line']);a.axvline(5,ls='--',color='#666');a.set(xlim=(0,7.5),yticks=[1,0],yticklabels=['独立计算','链路'],xlabel='时间（ms）');save(f,name)
        for i,lengths in enumerate(data['10-9']['lengths']):
            f,a=plot(4.8,left=.20);offset=0
            for n,c in zip(lengths,['blue','green']):a.add_patch(Polygon([(offset,offset),(offset,offset+n),(offset+n,offset+n)],facecolor=COL[c],edgecolor=COL['line']));offset+=n
            a.set(xlim=(0,8192),ylim=(8192,0),xticks=[0,lengths[0],8192],yticks=[0,lengths[0],8192],xlabel='被读取的位置',ylabel='查询位置');a.set_aspect('equal');save(f,'9-attention-area' if i==0 else 'attention-unequal')
        f,a=canvas(4.1);box(a,.04,.65,.92,.17,'已训练：到批次 100','green')
        for i in range(8):box(a,.04+(i%4)*.235,.37-(i//4)*.20,.21,.14,str(101+i),'blue' if i<4 else 'gray',12)
        text(a,.5,.05,'101—108：已安排准备，仍等待训练',12,ha='center');save(f,'10-input-queue')
        f,a=canvas(4.0)
        for i in range(4):
            x=.04+i*.235;box(a,x,.66,.215,.18,f'旧 {i}',['blue','green','orange','purple'][i])
            for j in range(2):box(a,x+j*.1175,.22,.10,.18,str(i*2+j),['blue','green','orange','purple'][i]);arrow(a,(x+.1075,.66),(x+j*.1175+.05,.40))
        text(a,.5,.07,'新分片：每片 1536 行；旧分片：3072 行',11,ha='center');save(f,'11-resharding')
        f,a=canvas(4.4)
        for i,(l,c) in enumerate([('捕获一致状态','blue'),('复制到独立缓冲','orange'),('后台写入数据','blue'),('提交完整快照','green')]):
            y=.75-i*.21;box(a,.23,y,.54,.15,l,c)
            if i<3:arrow(a,(.5,y),(.5,y-.06))
        text(a,.80,.60,'训练\n可继续',11);save(f,'checkpoint-commit')
        for i,(l,rows) in enumerate(data['10-12']['timelines'].items()):
            f,a=plot(3.9,left=.19)
            for j,r in enumerate(rows):
                t=r['seconds'];a.barh(j,.5,left=t['capture'],color=COL['orange'],height=.5,edgecolor=COL['line']);a.barh(j,min(t['durable'],50)-t['upload_start'],left=t['upload_start'],color=COL['blue'],height=.5,edgecolor=COL['line'])
                if t['durable']>50:a.barh(j,t['durable']-50,left=50,color='white',hatch='///',height=.5,edgecolor=COL['line'])
                a.plot(t['durable'],j,'o',mfc=COL['green'] if t['durable']<=50 else 'white',mec=COL['line']);a.text(t['durable'],j+.4,str(t['durable'])+' s',fontsize=11,ha='center')
            a.axvline(50,ls='--',color='#a56c28');a.set(xlim=(18,59),ylim=(-.5,1.8),yticks=[0,1],yticklabels=['快照 1','快照 2'],xlabel='时间（s）');a.invert_yaxis();a.set_title(l+'：故障发生在 50 s',loc='left');save(f,'12-recovery' if i==0 else 'recovery-fast')
        d=data['10-13'];t=np.array(d['interval_seconds']);c=d['checkpoint_seconds'];lam=d['job_failure_rate_per_second'];r=d['restore_seconds'];f,a=plot(4.1)
        for y,l,color in [(c/t,'保存','#267398'),(lam*t/2,'重做','#a56c28'),(c/t+lam*t/2+lam*r,'总附加成本','#388768')]:a.plot(t/60,y*100,label=l,color=color)
        a.set(xlabel='保存间隔（分钟）',ylabel='每单位有用训练的附加时间（%）');a.legend(frameon=False);save(f,'13-save-interval')
        f,a=canvas(4.2)
        for i,(l,c) in enumerate([('生成\n12 条/s','blue'),('验证\n6 条/s','orange'),('学习\n8 条/s','green')]):box(a,.04+i*.34,.48,.24,.24,l,c)
        for x in [.28,.62]:arrow(a,(x,.60),(x+.10,.60))
        text(a,.70,.34,'保留 75% → 4.5 条/s',11,ha='center');arrow(a,(.84,.48),(.84,.16),'control');arrow(a,(.84,.16),(.16,.16),'control');arrow(a,(.16,.16),(.16,.48),'control');text(a,.5,.08,'新权重用于后续生成',12,ha='center');save(f,'14-rl-flow')
        for i,key in enumerate(['restore_bytes','staged_bytes']):
            f,a=plot(4.1,bottom=.26);v=np.array(data['10-15'][key])/2**30;a.step(range(4),v,where='post',color='#267398');a.plot(range(4),v,'o',color='#267398');a.axhline(64,ls='--',color='#a56c28');a.set(xticks=range(4),xticklabels=['训练\n结束','加载权重\n分配 KV' if i==0 else '只加载\n权重','释放\n训练状态','开始\n生成'],ylabel='显存占用（GiB）',ylim=(0,100));a.text(1,v[1]+4,f'峰值 {v[1]:.1f} GiB',fontsize=12,ha='center');save(f,'15-rl' if i==0 else 'rl-staged')
        f,a=canvas(4.5)
        for row,(l,c) in enumerate([('μ：实际生成样本的策略','blue'),('πold：本轮优化开始时的策略','orange'),('πθ：本轮更新中的当前策略','green')]):
            y=.70-row*.28;box(a,.04,y,.92,.18,l,c)
            if row<2:arrow(a,(.5,y),(.5,y-.10),'control')
        text(a,.5,.04,'对同一前缀与 token 分别记录概率',12,ha='center');save(f,'policy-versions')
        for async_,name in [(False,'16-async-cycle'),(True,'async-overlap')]:
            f,a=plot(3.5,left=.20);items=[(2,0,40,'blue'),(1,0 if async_ else 40,16,'green'),(0,40 if async_ else 56,4,'orange')]
            for row,s,d,c in items:a.barh(row,d,left=s,height=.5,color=COL[c],edgecolor=COL['line'])
            a.set(yticks=[2,1,0],yticklabels=['生成','学习','权重同步'],xlim=(0,62),xlabel='稳态周期内时间（s）');save(f,name)
        f,a=canvas(4.9);box(a,.04,.69,.40,.20,'生成时记录\n样本 A／位置 17／层 3','blue',11);box(a,.60,.69,.36,.20,'专家 ID：[2, 7]','orange',11);arrow(a,(.44,.79),(.60,.79))
        box(a,.60,.28,.36,.20,'训练时仍选 2、7','orange',11);arrow(a,(.78,.69),(.78,.48),'control');box(a,.04,.28,.40,.20,'用当前权重计算\n分数、输出与梯度','green',11);arrow(a,(.60,.38),(.44,.38));text(a,.5,.08,'记录固定离散选择；当前权重参与数值计算',11,ha='center');save(f,'17-replay')
        f,a=plot(3.8,left=.18);rows=data['10-18']['rows']
        for i,r in enumerate(rows):
            left=0
            for j,(v,c) in enumerate(zip(r['days'],['blue','orange','gray'])):a.barh(i,v,left=left,height=.45,color=COL[c],edgecolor=COL['line'],label=['基础训练','保存恢复','计划停顿'][j] if i==0 else None);left+=v
            a.text(left+.4,i,f'{left:.1f}',fontsize=12,va='center')
        a.axvline(30,ls='--',color='#a56c28');a.set(yticks=[0,1],yticklabels=['32 卡','48 卡'],xlabel='完成时间（天）',xlim=(0,41),ylim=(-.5,2.0));a.legend(frameon=False,ncol=2,loc='upper left');save(f,'18-deadline')
        d=data['10-19'];f,a=plot(3.9)
        for k,c in zip(d['curves'],['#388768','#267398','#a56c28']):a.plot(d['relative_bandwidth'],d['curves'][k],color=c,label=f'原通信占比 {float(k):.0%}')
        a.set(xlabel='新带宽／原带宽',ylabel='新耗时／原耗时');a.legend(frameon=False);save(f,'19-hardware')
        f,a=plot(4.2)
        for (key,d),l,c in zip(data['10-20'].items(),['A100','H100','B200'],['#267398','#388768','#a56c28']):a.plot(np.array(d['parameters'])/1e12,np.array(d['continuous_required_devices'])/1e4,color=c,label=l)
        a.axhline(1.6384,ls='--',color='#666');a.set(yscale='log',xlabel='稠密模型参数量（万亿）',ylabel='90 天所需设备（万张）');a.legend(frameon=False);save(f,'20-scale')
    from core_principles_figures import draw as draw_principles
    draw_principles(10, out)
    out.finish();return out.outputs,out.checks
