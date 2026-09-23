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
        region(a,.30,.10,.40,.80,L("沙箱",'Sandbox'))
        box(a,.34,.58,.32,.15,L("agent 程式",'Agent processes'),'blue')
        box(a,.34,.26,.32,.15,L("平台代理程式",'Platform proxy'),'gray')
        arrow(a,(.50,.58),(.50,.41),'control');text(a,.52,.495,'AppArmor',11)
        text(a,.50,.17,L("輸出與寫盤設上限",'Output/disk caps'),11,ha='center')
        box(a,.01,.42,.16,.16,L("其他沙箱",'Other\nsandboxes'),'gray',11)
        text(a,.235,.50,L("虛擬化\n與配額",'VM and\nquotas'),11,ha='center')
        box(a,.78,.58,.20,.15,L("外部網路",'Network'),'green',11)
        arrow(a,(.66,.655),(.78,.655),'control');text(a,.88,.80,L("eBPF 白名單",'eBPF allowlist'),11,ha='center')
        save(f,'sandbox-boundaries')
        # Guest page caches duplicate the image; DAX maps one host copy.
        for shared,name in [(False,'page-cache-copies'),(True,'page-cache-shared')]:
            f,a=canvas(3.9)
            for i in range(3):
                x=.03+i*.33;box(a,x,.52,.28,.36,'','blue')
                text(a,x+.14,.80,f'microVM {i+1}',12,ha='center')
                if shared:text(a,x+.14,.63,L("對映宿主機頁",'maps host pages'),11,ha='center')
                else:box(a,x+.03,.57,.22,.14,L("映象頁副本",'image copy'),'orange',11)
                arrow(a,(x+.14,.36),(x+.14,.52 if shared else .57),'control' if shared else 'data')
            box(a,.03,.14,.94,.22,'','gray')
            text(a,.50,.29,L("宿主機 page cache",'Host page cache'),12,ha='center')
            box(a,.35,.16,.30,.09,L("映象頁（唯一一份）" if shared else "映象頁",'single copy' if shared else 'image pages'),'orange',11)
            text(a,.50,.06,L("DAX 直接對映，不再複製",'DAX maps pages, no copy') if shared else L("經虛擬塊裝置複製到每臺虛擬機器",'copied into every VM via virtual block device'),11,ha='center')
            save(f,name)
        # Pause during a long GPU preemption; the axis is schematic.
        f,a=plot(3.2,left=.22)
        for start,dur,c,label in [(0,3,'blue',L("訓練",'train')),(3,8,'gray',L("被搶佔",'preempted')),(11,3,'blue',L("訓練",'train'))]:
            a.barh(1,dur,left=start,height=.5,color=COL[c],edgecolor=COL['line']);text(a,start+dur/2,1,label,11,ha='center')
        for start,dur,c,label in [(0,3,'green',L("駐留",'resident')),(3,1.4,'orange',L("儲存",'save')),(4.4,5.2,'white',L("記憶體已釋放",'released')),(9.6,1.4,'blue',L("恢復",'load')),(11,3,'green',L("駐留",'resident'))]:
            a.barh(0,dur,left=start,height=.5,color=COL[c],edgecolor=COL['line'],ls='--' if c=='white' else '-');text(a,start+dur/2,0,label,11,ha='center')
        a.set(yticks=[1,0],yticklabels=[L("GPU 作業",'GPU job'),L("沙箱記憶體",'Sandbox\nmemory')],xticks=[],xlim=(0,14),ylim=(-.6,1.6),xlabel=L("時間（未按比例）",'Time (not to scale)'))
        save(f,'preempt-pause')
        # Sampled placement over a stale view, with node-side admission.
        f,a=canvas(4.6)
        box(a,.02,.40,.32,.26,L("排程器\n彙總檢視＋本地疊加",'Scheduler\nstale view + own recent'),'orange',11)
        nodes=[(L("節點 A",'Node A'),'70%','gray'),(L("節點 B",'Node B'),'35%','green'),(L("節點 C",'Node C'),'55%','gray'),(L("節點 D",'Node D'),'60%','blue'),(L("節點 E",'Node E'),'80%','gray')]
        for i,(n,load,c) in enumerate(nodes):
            y=.80-i*.155;box(a,.60,y,.37,.12,f'{n}　{load}'+(L("（選中）",' (picked)') if c=='green' else ''),c,11)
        arrow(a,(.34,.60),(.60,.705),'control');arrow(a,(.34,.48),(.60,.395),'control')
        text(a,.47,.72,L("隨機抽取 2 個",'sample 2'),11,ha='center')
        text(a,.785,.95,L("節點負載",'Node load'),11,ha='center')
        text(a,.50,.05,L("節點檢查本地容量：不足則拒絕，排程器改選",'Node checks local capacity; on reject, re-pick'),11,ha='center')
        save(f,'placement-sampling')
        # One physical core, two hardware threads.
        for core,name in [(False,'smt-sibling'),(True,'smt-core-scheduling')]:
            f,a=canvas(3.7)
            region(a,.04,.06,.92,.86,L("一個物理核",'One physical core'))
            box(a,.09,.50,.38,.20,L("硬體執行緒 0：LS 任務",'HW thread 0: LS task'),'orange',11)
            box(a,.53,.50,.38,.20,L("硬體執行緒 1：空閒",'HW thread 1: idle') if core else L("硬體執行緒 1：BE 任務",'HW thread 1: BE task'),'white' if core else 'blue',11)
            box(a,.20,.12,.60,.18,L("共享執行單元與一級快取",'Shared execution units and L1'),'purple',11)
            arrow(a,(.28,.50),(.40,.30))
            if not core:arrow(a,(.72,.50),(.60,.30))
            save(f,name)
        # Who holds rollout state when the GPU job is preempted.
        for moved,name in [(False,'rollout-owner-before'),(True,'rollout-owner-after')]:
            f,a=canvas(4.4)
            region(a,.02,.18,.44,.74,L("可搶佔 GPU 資源",'Preemptible GPU pool'))
            region(a,.54,.18,.44,.74,L("CPU 沙箱平台",'CPU sandbox platform'))
            box(a,.06,.62,.36,.14,L("模型服務",'Model serving'),'blue',11)
            box(a,.06,.43,.36,.14,L("RL 框架",'RL framework'),'blue',11)
            box(a,.58 if moved else .06,.24,.36,.14,L("agent 迴圈",'Agent loop'),'orange',11)
            box(a,.58,.52,.36,.22,L("沙箱\n檔案與程式",'Sandbox\nfiles, processes'),'green',11)
            if moved:arrow(a,(.58,.31),(.42,.66));arrow(a,(.76,.38),(.76,.52))
            else:arrow(a,(.42,.31),(.58,.58))
            text(a,.50,.07,L("搶佔後 GPU 側重新連線即可繼續",'After preemption the GPU side reconnects') if moved else L("搶佔時 agent 迴圈丟失，按命令日誌重放",'Preemption loses the loop; replay command log'),11,ha='center')
            save(f,name)
