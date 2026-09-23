"""DSec mechanism figures for chapter 11: isolation, page cache, pause, placement, SMT, rollout state."""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from figure_style import COL,STYLE,canvas,plot,text,box,arrow


def draw(out,english=False):
    L=lambda zh,en:en if english else zh
    def save(f,n):out.save(f,'figure-11-'+n)
    def region(a,x,y,w,h,label):
        a.add_patch(Rectangle((x,y),w,h,fill=False,ls='--',lw=1,edgecolor=COL['line']))
        text(a,x+w/2,y+h-.05,label,12,ha='center')
    with plt.rc_context(STYLE):
        # Three isolation directions around one sandbox.
        f,a=canvas(4.4)
        region(a,.30,.10,.40,.80,L('沙箱','Sandbox'))
        box(a,.34,.58,.32,.15,L('agent 进程','Agent processes'),'blue')
        box(a,.34,.26,.32,.15,L('平台代理进程','Platform proxy'),'gray')
        arrow(a,(.50,.58),(.50,.41),'control');text(a,.52,.495,'AppArmor',11)
        text(a,.50,.17,L('输出与写盘设上限','Output/disk caps'),11,ha='center')
        box(a,.01,.42,.16,.16,L('其他沙箱','Other\nsandboxes'),'gray',11)
        text(a,.235,.50,L('虚拟化\n与配额','VM and\nquotas'),11,ha='center')
        box(a,.78,.58,.20,.15,L('外部网络','Network'),'green',11)
        arrow(a,(.66,.655),(.78,.655),'control');text(a,.88,.80,L('eBPF 白名单','eBPF allowlist'),11,ha='center')
        save(f,'sandbox-boundaries')
        # Guest page caches duplicate the image; DAX maps one host copy.
        for shared,name in [(False,'page-cache-copies'),(True,'page-cache-shared')]:
            f,a=canvas(3.9)
            for i in range(3):
                x=.03+i*.33;box(a,x,.52,.28,.36,'','blue')
                text(a,x+.14,.80,f'microVM {i+1}',12,ha='center')
                if shared:text(a,x+.14,.63,L('映射宿主机页','maps host pages'),11,ha='center')
                else:box(a,x+.03,.57,.22,.14,L('镜像页副本','image copy'),'orange',11)
                arrow(a,(x+.14,.36),(x+.14,.52 if shared else .57),'control' if shared else 'data')
            box(a,.03,.14,.94,.22,'','gray')
            text(a,.50,.29,L('宿主机 page cache','Host page cache'),12,ha='center')
            box(a,.35,.16,.30,.09,L('镜像页（唯一一份）' if shared else '镜像页','single copy' if shared else 'image pages'),'orange',11)
            text(a,.50,.06,L('DAX 直接映射，不复制','DAX maps pages, no copy') if shared else L('经虚拟块设备复制到每台虚拟机','copied into every VM via virtual block device'),11,ha='center')
            save(f,name)
        # Pause during a long GPU preemption; the axis is schematic.
        f,a=plot(3.2,left=.22)
        for start,dur,c,label in [(0,3,'blue',L('训练','train')),(3,8,'gray',L('被抢占','preempted')),(11,3,'blue',L('训练','train'))]:
            a.barh(1,dur,left=start,height=.5,color=COL[c],edgecolor=COL['line']);text(a,start+dur/2,1,label,11,ha='center')
        for start,dur,c,label in [(0,3,'green',L('驻留','resident')),(3,1.4,'orange',L('保存','save')),(4.4,5.2,'white',L('内存已释放','released')),(9.6,1.4,'blue',L('恢复','load')),(11,3,'green',L('驻留','resident'))]:
            a.barh(0,dur,left=start,height=.5,color=COL[c],edgecolor=COL['line'],ls='--' if c=='white' else '-');text(a,start+dur/2,0,label,11,ha='center')
        a.set(yticks=[1,0],yticklabels=[L('GPU 作业','GPU job'),L('沙箱内存','Sandbox\nmemory')],xticks=[],xlim=(0,14),ylim=(-.6,1.6),xlabel=L('时间（未按比例）','Time (not to scale)'))
        save(f,'preempt-pause')
        # Sampled placement over a stale view, with node-side admission.
        f,a=canvas(4.6)
        box(a,.02,.40,.32,.26,L('调度器\n汇总视图＋本地叠加','Scheduler\nstale view + own recent'),'orange',11)
        nodes=[(L('节点 A','Node A'),'70%','gray'),(L('节点 B','Node B'),'35%','green'),(L('节点 C','Node C'),'55%','gray'),(L('节点 D','Node D'),'60%','blue'),(L('节点 E','Node E'),'80%','gray')]
        for i,(n,load,c) in enumerate(nodes):
            y=.80-i*.155;box(a,.60,y,.37,.12,f'{n}　{load}'+(L('（选中）',' (picked)') if c=='green' else ''),c,11)
        arrow(a,(.34,.60),(.60,.705),'control');arrow(a,(.34,.48),(.60,.395),'control')
        text(a,.47,.72,L('随机抽取 2 个','sample 2'),11,ha='center')
        text(a,.785,.95,L('节点负载','Node load'),11,ha='center')
        text(a,.50,.05,L('节点检查本地容量：不足则拒绝，调度器改选','Node checks local capacity; on reject, re-pick'),11,ha='center')
        save(f,'placement-sampling')
        # One physical core, two hardware threads.
        for core,name in [(False,'smt-sibling'),(True,'smt-core-scheduling')]:
            f,a=canvas(3.7)
            region(a,.04,.06,.92,.86,L('一个物理核','One physical core'))
            box(a,.09,.50,.38,.20,L('硬件线程 0：LS 任务','HW thread 0: LS task'),'orange',11)
            box(a,.53,.50,.38,.20,L('硬件线程 1：空闲','HW thread 1: idle') if core else L('硬件线程 1：BE 任务','HW thread 1: BE task'),'white' if core else 'blue',11)
            box(a,.20,.12,.60,.18,L('共享执行单元与一级缓存','Shared execution units and L1'),'purple',11)
            arrow(a,(.28,.50),(.40,.30))
            if not core:arrow(a,(.72,.50),(.60,.30))
            save(f,name)
        # Who holds rollout state when the GPU job is preempted.
        for moved,name in [(False,'rollout-owner-before'),(True,'rollout-owner-after')]:
            f,a=canvas(4.4)
            region(a,.02,.18,.44,.74,L('可抢占 GPU 资源','Preemptible GPU pool'))
            region(a,.54,.18,.44,.74,L('CPU 沙箱平台','CPU sandbox platform'))
            box(a,.06,.62,.36,.14,L('模型服务','Model serving'),'blue',11)
            box(a,.06,.43,.36,.14,L('RL 框架','RL framework'),'blue',11)
            box(a,.58 if moved else .06,.24,.36,.14,L('agent 循环','Agent loop'),'orange',11)
            box(a,.58,.52,.36,.22,L('沙箱\n文件与进程','Sandbox\nfiles, processes'),'green',11)
            if moved:arrow(a,(.58,.31),(.42,.66));arrow(a,(.76,.38),(.76,.52))
            else:arrow(a,(.42,.31),(.58,.58))
            text(a,.50,.07,L('抢占后 GPU 侧重新连接即可继续','After preemption the GPU side reconnects') if moved else L('抢占时 agent 循环丢失，按命令日志重放','Preemption loses the loop; replay command log'),11,ha='center')
            save(f,name)
