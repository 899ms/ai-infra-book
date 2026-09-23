"""UB layer separation and EP skew, using the book's common figure style."""
from pathlib import Path
import json
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from figure_style import COL, STYLE, Exporter, canvas, plot, box, text, arrow
from figure_style.typography import configure_font

ROOT=Path(__file__).resolve().parents[1]


EP_LINE={'blue':'#267398','orange':'#a56c28','green':'#28856a','purple':'#7a5c99'}


def draw_ep_mechanisms(out):
    """Chapter 9: one layer's dispatch/combine, CPU bottleneck switch, AF ping-pong, and skew growth with EP size."""
    from matplotlib.patches import Rectangle, Patch
    # One MoE layer on the two HGX servers of section 9.4.1: attention cards A0-A3, expert cards B0-B3.
    # Time runs downward; chip colour names the expert card an input row is sent to.
    dest=['blue','green','orange','purple']
    f,a=canvas(6.0)
    X=[.235+i*.19 for i in range(4)];W=.165;H=.13
    Y={'attn':.80,'exp':.47,'merge':.14}
    def chips(x,y,cols):
        for j,c in enumerate(cols):
            a.add_patch(Rectangle((x+.018+j*.035,y+.018),.027,.036,facecolor=COL[c],edgecolor=COL['line'],linewidth=.7))
    for i,x in enumerate(X):
        box(a,x,Y['attn'],W,H,'','gray');text(a,x+W/2,Y['attn']+.093,f'A{i}',12,ha='center');chips(x,Y['attn'],dest)
        box(a,x,Y['exp'],W,H,'',dest[i]);text(a,x+W/2,Y['exp']+.093,f'B{i}',12,ha='center');chips(x,Y['exp'],[dest[i]]*4)
        box(a,x,Y['merge'],W,H,'','gray');text(a,x+W/2,Y['merge']+.093,f'A{i}',12,ha='center');chips(x,Y['merge'],dest)
    # All-to-All: chip j of source i travels to slot i of card j, and back along the same pair.
    for i in range(4):
        for j in range(4):
            sx=X[i]+.0315+j*.035;dx=X[j]+.0315+i*.035
            a.annotate('',xy=(dx,Y['exp']+H+.004),xytext=(sx,Y['attn']-.004),arrowprops=dict(arrowstyle='-|>',color=EP_LINE[dest[j]],lw=.9,shrinkA=0,shrinkB=0,mutation_scale=7))
            a.annotate('',xy=(sx,Y['merge']+H+.004),xytext=(dx,Y['exp']-.004),arrowprops=dict(arrowstyle='-|>',color=EP_LINE[dest[j]],lw=.9,shrinkA=0,shrinkB=0,mutation_scale=7))
    for y,label in [(Y['attn']+H/2,"注意力、路由\n伺服器 A"),(.705,'dispatch'),(Y['exp']+H/2,"專家計算\n伺服器 B"),(.375,'combine'),(Y['merge']+H/2,"加權求和\n伺服器 A")]:
        text(a,.005,y,label,12)
    arrow(a,(.60,.98),(.60,Y['attn']+H));arrow(a,(.60,Y['merge']),(.60,.05))
    text(a,.63,.975,"上一層輸出",11);text(a,.63,.055,"下一層注意力",11)
    out.save(f,'figure-9-ep-layer')

    s=json.loads((ROOT/'calculations/results/ep-scale-skew-book.json').read_text())
    res={r['ep']:r for r in s['results']};hot=s['scenario']['hot_expert_rows']
    # Same hot expert, three EP sizes: bars are cards, stacked segments are the experts on that card.
    f,axes=plt.subplots(1,3,figsize=(420/72,3.9),sharey=True)
    f.subplots_adjust(left=.14,right=.985,bottom=.17,top=.83,wspace=.12)
    pos=[0,1,2,3.4]
    for k,(ax,ep) in enumerate(zip(axes,[8,32,256])):
        r=res[ep];m=r['experts_per_card'];mean=r['mean_rows'];other=r['hot_other_expert_rows']/mean
        for c,xc in enumerate(pos):
            y=0
            segs=[(hot/mean,'orange')]+[(other,'blue')]*(m-1) if c==0 else [(other,'blue')]*m
            for h,col in segs:
                ax.add_patch(Rectangle((xc-.34,y),.68,h,facecolor=COL[col],edgecolor='white',linewidth=.35 if m>8 else .8));y+=h
            ax.add_patch(Rectangle((xc-.34,0),.68,y,fill=False,edgecolor=COL['line'],linewidth=.9))
        ax.text(2.7,.45,'…',ha='center',fontsize=12)
        ax.axhline(1,color=COL['line'],ls=(0,(2,2)),lw=.9)
        ax.text(0,r['hot_ratio']+.1,f"{r['hot_ratio']:.2f}×" if ep<256 else '4×',ha='center',va='bottom',fontsize=11)
        ax.set(xlim=(-.75,3.85),ylim=(0,4.5),xticks=pos)
        ax.set_xticklabels(['0','1','2',str(ep-1)],fontsize=11)
        ax.set_title(f'EP{ep}\n每卡 {m} 個專家',fontsize=12,loc='center')
        ax.spines[['top','right']].set_visible(False)
        if k:ax.tick_params(axis='y',length=0)
    axes[0].set_ylabel("卡負載 ÷ 每卡平均")
    axes[2].text(2.2,1.15,"虛線：平均",ha='center',va='bottom',fontsize=11)
    f.text(.56,.035,"卡號",ha='center',fontsize=12)
    out.save(f,'figure-9-ep-scale-cards')

    # Busiest/mean against EP size: one hot expert (exact) and uniform random routing (seeded simulation).
    f,a=plot(3.5,left=.15,bottom=.18)
    eps=[r['ep'] for r in s['results']]
    a.plot(eps,[r['hot_ratio'] for r in s['results']],marker='o',color=EP_LINE['orange'],label="一個 4 倍熱點專家")
    a.plot(eps,[r['random_mean_ratio'] for r in s['results']],marker='o',color=EP_LINE['blue'],label="均勻隨機路由，1000 批均值")
    for r in s['results'][-1:]:
        a.text(r['ep']/1.12,r['hot_ratio'],f"{r['hot_ratio']:.1f}",ha='right',va='center',fontsize=11)
        a.text(r['ep']/1.12,r['random_mean_ratio']+.2,f"{r['random_mean_ratio']:.2f}",ha='right',va='center',fontsize=11)
    a.set_xscale('log',base=2);a.minorticks_off()
    a.set(xticks=eps,xticklabels=[str(e) for e in eps],xlim=(6.5,300),ylim=(.9,4.3),yticks=[1,2,3,4],
          xlabel="EP 組的卡數（每卡專家數 = 256 ÷ 卡數）",ylabel="最忙卡 ÷ 每卡平均")
    a.axhline(1,color=COL['line'],ls=(0,(2,2)),lw=.9)
    a.legend(frameon=False,loc='upper left');a.grid(axis='y',alpha=.15)
    out.save(f,'figure-9-ep-scale-sweep')

    # Section 9.3.2: eight 36 MiB experts, 128 tokens each, on one Xeon 8452Y socket; the longer bar sets the time.
    P=3*4096*1536;W=2*P;flop=8*128*2*P
    f,axes=plt.subplots(1,2,figsize=(420/72,3.3))
    f.subplots_adjust(left=.17,right=.97,bottom=.30,top=.86,wspace=.35)
    for ax,(kernel,C,xmax) in zip(axes,[('AVX-512 kernel：1.8 TFLOP/s',1.8e12,26),('AMX kernel：21.3 TFLOP/s',21.3e12,3.2)]):
        for row,(bw,label) in enumerate([(220e9,"同插槽"),(125e9,"跨插槽")]):
            read=8*W/bw*1e3;comp=flop/C*1e3
            for off,(v,col) in zip((-.17,.17),[(read,'blue'),(comp,'green')]):
                ax.barh(row+off,v,height=.3,color=COL[col],edgecolor=COL['line'],linewidth=1.6 if v==max(read,comp) else .8)
                ax.text(v+xmax*.02,row+off,f'{v:.2f}',va='center',fontsize=11)
        ax.set(yticks=[0,1],yticklabels=["同插槽\n220 GB/s","跨插槽\n125 GB/s"] if ax is axes[0] else ['',''],xlim=(0,xmax),ylim=(1.5,-.5))
        ax.set_title(kernel,fontsize=12);ax.spines[['top','right']].set_visible(False)
        if ax is not axes[0]:ax.tick_params(axis='y',length=0)
    f.text(.57,.14,"時間（ms）",ha='center',fontsize=12)
    f.legend(handles=[Patch(facecolor=COL['blue'],edgecolor=COL['line'],label="讀取八份權重"),Patch(facecolor=COL['green'],edgecolor=COL['line'],label="八個專家的矩陣計算")],
             frameon=False,ncol=2,loc='lower center',bbox_to_anchor=(.57,-.01))
    out.save(f,'figure-9-cpu-bottleneck')

    # Section 9.3.4: attention 2 ms and experts 3 ms per microbatch, four microbatches, serial versus ping-pong.
    tA,tF,q=2,3,4
    serial=[(0,i*(tA+tF),tA,i+1) for i in range(q)]+[(1,i*(tA+tF)+tA,tF,i+1) for i in range(q)]
    pipe=[(0,i*tA,tA,i+1) for i in range(q)]
    ready=0
    for i in range(q):
        start=max(i*tA+tA,ready);pipe.append((1,start,tF,i+1));ready=start+tF
    f,axes=plt.subplots(2,1,figsize=(420/72,3.6),sharex=True)
    f.subplots_adjust(left=.20,right=.97,bottom=.15,top=.91,hspace=.75)
    for ax,(title,items) in zip(axes,[(f'依次執行：{q*(tA+tF)} ms',serial),(f'交錯流水：{ready} ms',pipe)]):
        for row,start,dur,k in items:
            ax.barh(row,dur,left=start,height=.55,color=COL['blue' if row==0 else 'green'],edgecolor=COL['line'])
            ax.text(start+dur/2,row,str(k),ha='center',va='center',fontsize=11)
        ax.set(yticks=[0,1],yticklabels=["注意力節點","專家節點"],xlim=(0,21),ylim=(1.6,-.6),xticks=[0,5,10,14,20])
        ax.set_title(title,loc='left',fontsize=12);ax.spines[['top','right']].set_visible(False);ax.grid(axis='x',alpha=.15)
    axes[1].axvline(ready,color=EP_LINE['orange'],ls='--',lw=1)
    axes[1].set_xlabel("時間（ms）；方塊中的數字為 micro-batch 編號")
    out.save(f,'figure-9-af-pingpong')



def draw(ch, here):
    out=Exporter(here)
    with plt.rc_context(STYLE):
        if ch == 6:
            f,a=canvas(4.3)
            text(a,.04,.95,"應用端點分別保留，可靠傳輸按需共享",13)
            for x,label in ((.06,"應用 A\nJetty A"),(.59,"應用 B\nJetty B")):
                box(a,x,.69,.35,.18,label,'blue')
                arrow(a,(x+.175,.69),(.5,.56))
            box(a,.17,.37,.66,.19,"共享傳輸通道\n序號、確認、重傳、擁塞控制",'orange')
            arrow(a,(.5,.37),(.5,.24))
            box(a,.17,.06,.66,.18,"遠端事務層\n按目標端點分派與檢查權限",'green')
            text(a,.50,.63,"事務 → 報文",11,ha='center')
            text(a,.73,.30,"網路交付",11,ha='center')
            out.save(f,'figure-6-ub-layers')
            fab=json.loads((ROOT/'calculations/results/ub-fabric-book.json').read_text())
            LINE={'blue':'#267398','orange':'#a56c28','green':'#28856a','purple':'#7a5c99'}
            # Controller placement: behind PCIe versus on the on-chip bus.
            f,a=canvas(4.0)
            text(a,.04,.95,"一次遠端讀取的發起路徑",13)
            for x0,title,chain in ((.02,"PCIe 外設網路卡",[("處理器",'blue'),("片上\n匯流排",'green'),('PCIe','gray'),("網路卡",'orange')]),
                                   (.52,"片上匯流排上的控制器",[("處理器",'blue'),("片上\n匯流排",'green'),("UB\n控制器",'orange')])):
                text(a,x0+.23,.84,title,12,ha='center')
                n=len(chain);gap=.025;w=(.46-(n-1)*gap)/n
                for i,(label,c) in enumerate(chain):
                    x=x0+i*(w+gap)
                    box(a,x,.47,w,.26,label,c,11)
                    if i<n-1:arrow(a,(x+w,.60),(x+w+gap,.60))
                arrow(a,(x0+.23,.47),(x0+.23,.33))
                text(a,x0+.23,.27,"網路",11,ha='center')
            text(a,.25,.11,"門鈴與 DMA 各穿越 PCIe 一次",11,ha='center')
            text(a,.75,.11,"指令經片上匯流排直達控制器",11,ha='center')
            out.save(f,'figure-6-ub-controller')
            # Per-NIC state against hosts in one fabric, three organisations.
            hosts=[r['hosts'] for r in fab['hosts']]
            f,a=plot(3.8,left=.19)
            f.subplots_adjust(top=.80)
            for key,label,c in (('roce_bytes',"逐對連線（RoCE）",'orange'),('directory_bytes',"目錄式一致互聯",'purple'),('ub_bytes',"端點加通道（UB）",'green')):
                a.plot(hosts,[r[key]/1024 for r in fab['hosts']],marker='o',color=LINE[c],label=label)
            a.axhline(fab['cache']['context_cache_bytes']/1024,color=COL['line'],ls='--')
            a.text(hosts[0],fab['cache']['context_cache_bytes']/1024*1.4,"片上上下文快取 256 KiB",fontsize=11)
            a.set(xscale='log',yscale='log',xlabel="互聯內的主機數（每臺 8 個端點）",ylabel="每個 NIC 的狀態（KiB）")
            a.set_xticks(hosts);a.set_xticklabels([str(h) for h in hosts])
            a.legend(frameon=False,ncol=3,loc='upper center',bbox_to_anchor=(.45,1.27),columnspacing=.8,handlelength=1.4)
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-6-ub-hosts')
            # Connection setup time, N local × N remote endpoints, 32 cores in parallel.
            f,a=plot(3.7,left=.19)
            f.subplots_adjust(top=.82)
            ns=[r['endpoints'] for r in fab['setup']]
            for key,label,c in (('roce_parallel_s',"每對關係一條連線（RoCE）",'orange'),('ub_parallel_s',"每端點一個 Jetty、每遠端一條通道（UB）",'green')):
                a.plot(ns,[max(r[key],1e-9) for r in fab['setup']],marker='o',color=LINE[c],label=label)
            top=fab['setup'][-1]
            a.annotate(f"{top['roce_parallel_s']:.1f} s",(ns[-1],top['roce_parallel_s']),xytext=(-52,-4),textcoords='offset points',fontsize=11)
            a.annotate(f"{top['ub_parallel_s']*1000:.0f} ms",(ns[-1],top['ub_parallel_s']),xytext=(-46,-14),textcoords='offset points',fontsize=11)
            a.set(xscale='log',yscale='log',xlabel="本地端點數 N（遠端端點數 M = N）",ylabel="建立全部關係的時間（s）")
            a.set_xticks(ns);a.set_xticklabels([str(n) for n in ns])
            a.legend(frameon=False,ncol=1,loc='upper center',bbox_to_anchor=(.45,1.3),handlelength=1.4)
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-6-ub-setup')
        if ch == 6:
            # Who issues a network request: CPU proxy, GPU SMs, or the NIC's own processor.
            f, a = canvas(4.0)
            for i, (title, ctrl, note) in enumerate([("CPU 代理執行緒", 0, "穿越 PCIe：3 次"), ("GPU 的 SM", 1, "穿越 PCIe：2 次"), ("網路卡上的處理器", 2, "穿越 PCIe：0 次")]):
                x0 = .02 + .33 * i
                text(a, x0 + .15, .95, title, 12, ha='center')
                box(a, x0 + .01, .70, .12, .12, 'CPU', 'orange' if ctrl == 0 else 'gray', 11)
                box(a, x0 + .17, .70, .12, .12, 'GPU', 'orange' if ctrl == 1 else 'blue', 11)
                a.plot([x0, x0 + .30], [.52, .52], color=COL['line'], lw=.9, ls=(0, (3, 3)))
                text(a, x0 + .30, .56, 'PCIe', 11, ha='right')
                box(a, x0 + .09, .20, .12, .12, "網路卡", 'orange' if ctrl == 2 else 'green', 11)
                if ctrl == 0:
                    arrow(a, (x0 + .17, .76), (x0 + .13, .76)); text(a, x0 + .15, .86, "就緒", 11, ha='center')
                    arrow(a, (x0 + .06, .70), (x0 + .12, .32)); text(a, x0 + .01, .45, "門鈴\n請求描述符", 11)
                elif ctrl == 1:
                    arrow(a, (x0 + .19, .70), (x0 + .13, .32)); text(a, x0 + .01, .45, "門鈴\n請求描述符", 11)
                else:
                    arrow(a, (x0 + .06, .70), (x0 + .12, .32)); text(a, x0 + .01, .45, "每批一次觸發", 11)
                arrow(a, (x0 + .18, .32), (x0 + .24, .70)); text(a, x0 + .21, .40, "載荷、完成", 11)
                text(a, x0 + .15, .08, note, 11, ha='center')
            out.save(f, 'figure-6-initiator')
        if ch == 7:
            # PCIe transaction types: posted writes finish on send; reads wait for tagged completions.
            f, a = canvas(3.2)
            text(a, .02, .90, "寫（posted）：發出即完成", 12)
            box(a, .10, .58, .16, .16, "發起方", 'blue', 11); box(a, .74, .58, .16, .16, "接收方", 'green', 11)
            arrow(a, (.26, .66), (.74, .66)); text(a, .50, .74, "寫事務報文：地址＋資料", 11, ha='center')
            text(a, .02, .44, "讀（non-posted）：在途數受標籤與信用限制", 12)
            box(a, .10, .10, .16, .16, "發起方", 'blue', 11); box(a, .74, .10, .16, .16, "接收方", 'green', 11)
            arrow(a, (.26, .22), (.74, .22)); text(a, .50, .31, "讀請求報文：地址＋標籤", 11, ha='center')
            arrow(a, (.74, .14), (.26, .14)); text(a, .50, .04, "完成報文：資料＋同一標籤", 11, ha='center')
            out.save(f, 'figure-7-pcie-transactions')
            # Which ceiling binds a 64 B random DMA read on the KV-Direct platform.
            f, a = plot(2.8, left=.34, bottom=.26)
            labels = ["鏈路頻寬換算", "報文頭開銷上限", "在途標籤上限", "實測"]
            vals = [123, 87, 61, 60]; cols = [COL['blue'], COL['blue'], COL['orange'], COL['green']]
            a.barh(range(4), vals, color=cols, edgecolor=COL['line'], height=.55)
            for i, v in enumerate(vals): a.text(v + 2, i, f'{v}', va='center', fontsize=11)
            a.set(yticks=range(4), yticklabels=labels, xlim=(0, 140), xlabel="64 B 隨機 DMA 讀，每秒百萬次操作"); a.invert_yaxis()
            out.save(f, 'figure-7-pcie-limits')
            # Two traffic classes sharing a GPU's PCIe link, per direction.
            f, a = canvas(3.8)
            box(a, .03, .62, .18, .14, "主機記憶體", 'gray', 11); box(a, .03, .24, .18, .14, "網路卡", 'gray', 11)
            a.plot([.56, .56], [.10, .92], color=COL['line'], lw=.9, ls=(0, (3, 3))); text(a, .56, .96, "PCIe 鏈路", 11, ha='center')
            box(a, .62, .14, .34, .70, '', 'blue'); text(a, .79, .78, 'GPU', 12, ha='center')
            box(a, .68, .40, .22, .14, 'HBM', 'white', 11)
            arrow(a, (.21, .72), (.62, .72)); text(a, .41, .79, "完成報文（H2D 複製）", 11, ha='center')
            arrow(a, (.62, .62), (.21, .62)); text(a, .41, .55, "posted 寫（D2H 複製）", 11, ha='center')
            arrow(a, (.21, .34), (.62, .34)); text(a, .41, .41, "posted 寫（遠端寫入）", 11, ha='center')
            arrow(a, (.62, .24), (.21, .24)); text(a, .41, .17, "完成報文（遠端讀取）", 11, ha='center')
            text(a, .79, .30, "離開 GPU 的兩路\n都先從 HBM 取數", 11, ha='center')
            text(a, .79, .64, "進入 GPU 的兩路\n在鏈路上爭用", 11, ha='center')
            out.save(f, 'figure-7-pcie-asymmetry')
            f,a=canvas(4.6)
            text(a,.04,.96,"64 卡超節點：8 個 TP8 組",13)
            for row in range(8):
                y=.79-row*.075
                text(a,.02,y+.023,str(row),11)
                for col in range(8):box(a,.10+col*.103,y,.079,.047,'','orange' if col==0 else 'blue')
            text(a,.51,.88,"同一行：TP 分片，共同計算一份輸入",11,ha='center')
            text(a,.5,.12,"同一列：對應梯度先在本地歸約",12,ha='center')
            arrow(a,(.5,.09),(.5,.02))
            text(a,.73,.04,"再跨節點交換",11,ha='center')
            out.save(f,'figure-7-supernode-groups')
            records=json.loads((ROOT/'calculations/results/supernode-scaling-book.json').read_text())['results']
            f,a=plot(3.7,left=.19)
            labels=["出口擴充","出口封頂","出口擴充＋本地加倍"]
            colors=['#267398','#a56c28','#28856a']
            for i in range(3):
                rs=records[i*4:(i+1)*4]
                a.plot(range(4),[r['tokens_per_s']/1e4 for r in rs],marker='o',color=colors[i],label=labels[i])
            a.set(xticks=range(4),xticklabels=['8','64','128','256'],xlabel="每超節點卡數",ylabel="吞吐（萬 token/s）",ylim=(100,205))
            a.legend(frameon=False,fontsize=11,loc='upper left')
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-7-supernode-scaling')
            fab=json.loads((ROOT/'calculations/results/ub-fabric-book.json').read_text())
            LINE={'blue':'#267398','orange':'#a56c28','green':'#28856a','purple':'#7a5c99'}
            # Endpoint state, N = M sweep.
            f,a=plot(3.7,left=.19)
            f.subplots_adjust(top=.82)
            ns=[r['endpoints'] for r in fab['state']]
            a.plot(ns,[r['roce_bytes']/1024 for r in fab['state']],marker='o',color=LINE['orange'],label="N×M 份連線狀態（RoCE）")
            a.plot(ns,[r['ub_bytes']/1024 for r in fab['state']],marker='o',color=LINE['green'],label="N 個 Jetty 加 M 條通道（UB）")
            a.axhline(fab['cache']['context_cache_bytes']/1024,color=COL['line'],ls='--')
            a.text(ns[0],fab['cache']['context_cache_bytes']/1024*1.5,"片上快取 256 KiB",fontsize=11)
            top=fab['state'][-1]
            a.annotate(f"{top['ratio']:,.0f} 倍",(ns[-1],top['ub_bytes']/1024),xytext=(-40,12),textcoords='offset points',fontsize=11)
            a.set(xscale='log',yscale='log',xlabel="本地端點數 N（遠端端點數 M = N）",ylabel="每個 NIC 的狀態（KiB）")
            a.set_xticks(ns);a.set_xticklabels([str(n) for n in ns])
            a.legend(frameon=False,ncol=2,loc='upper center',bbox_to_anchor=(.45,1.25),columnspacing=1,handlelength=1.4)
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-7-ub-state-growth')
            # Latency against active endpoints: the cache cliff.
            f,a=plot(3.6,left=.17)
            f.subplots_adjust(top=.82)
            sw=fab['cache']['sweep'];xs=[r['endpoints'] for r in sw]
            a.step(xs,[r['roce_dma_ns']/1000 for r in sw],where='post',color=LINE['orange'],label="RoCE 讀取")
            a.step(xs,[r['ub_loadstore_ns']/1000 for r in sw],where='post',color=LINE['green'],label='UB Load')
            a.annotate(f"N = {fab['cache']['roce_spill_endpoints']} 溢位，每次多 {fab['cache']['roce_refetch_ns']} ns",(fab['cache']['roce_spill_endpoints'],sw[-1]['roce_dma_ns']/1000),xytext=(6,6),textcoords='offset points',fontsize=11)
            a.annotate(f"N = {fab['cache']['ub_spill_endpoints']} 溢位，多 {fab['cache']['ub_refetch_ns']} ns",(fab['cache']['ub_spill_endpoints'],sw[-1]['ub_loadstore_ns']/1000),xytext=(-4,8),textcoords='offset points',fontsize=11,ha='right')
            a.set(xscale='log',xlabel="活躍端點數 N（M = N）",ylabel="一次 64 B 讀取（μs）",ylim=(0,3.9))
            a.set_xticks([1,8,64,512,4096]);a.set_xticklabels(['1','8','64','512','4096'])
            a.legend(frameon=False,ncol=2,loc='upper center',bbox_to_anchor=(.45,1.22),columnspacing=1.5,handlelength=1.4)
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-7-ub-cache-cliff')
            # Round trip budget by phase group, three stacks.
            f,a=plot(3.9,left=.24,bottom=.18)
            f.subplots_adjust(top=.80)
            stacks=[('roce_dma',"外設式 RoCE 讀取"),('ub_urma',"UB 非同步讀取"),('ub_loadstore','UB Load')]
            groups=fab['groups'];fills=['blue','gray','green','orange','purple','white']
            from matplotlib.patches import Patch
            for row,(key,label) in enumerate(stacks):
                start=0
                for g,c in zip(groups,fills):
                    v=fab['round_trip'][key]['group_ns'][g]
                    if v:a.barh(row,v,left=start,height=.55,color=COL[c],edgecolor=COL['line']);start+=v
                a.text(start+40,row,f"推導 {fab['round_trip'][key]['total_ns']:.0f}，模擬 {fab['round_trip'][key]['paper_measured_ns']}",va='center',fontsize=11)
            a.set(yticks=range(3),yticklabels=[l for _,l in stacks],xlabel="一次 64 B 遠端讀取的關鍵路徑（ns）",xlim=(0,3300))
            a.invert_yaxis()
            a.legend(handles=[Patch(facecolor=COL[c],edgecolor=COL['line'],label=g) for g,c in zip(groups,fills)],frameon=False,ncol=3,loc='upper center',bbox_to_anchor=(.4,1.3),columnspacing=.8,handlelength=1.2)
            out.save(f,'figure-7-ub-round-trip')
            # Total against one-way link delay: same slope, different intercepts.
            f,a=plot(3.6,left=.17)
            f.subplots_adjust(top=.82)
            for key,label,c in (('roce_dma',"外設式 RoCE 讀取",'orange'),('ub_urma',"UB 非同步讀取",'blue'),('ub_loadstore','UB Load','green')):
                pts=fab['round_trip'][key]['link_sweep']
                a.plot([p['link_ns'] for p in pts],[p['total_ns']/1000 for p in pts],marker='o',color=LINE[c],label=label)
            a.set(xlabel="線路單程時延（ns）",ylabel="一次 64 B 讀取（μs）",xlim=(0,540),ylim=(0,3.4))
            a.legend(frameon=False,ncol=3,loc='upper center',bbox_to_anchor=(.45,1.22),columnspacing=1.2,handlelength=1.4)
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-7-ub-link-delay')
        if ch == 9:
            data=json.loads((ROOT/'calculations/results/ep-skew-book.json').read_text())['results']
            f,a=plot(3.7,left=.16)
            for i,(r,label,col) in enumerate(zip(data[:2],["均衡","熱點"],['blue','orange'])):
                v=np.array(r['expert_assignments'])*8192/2**20
                a.bar(np.arange(4)+(i-.5)*.32,v,width=.30,label=label,color=COL[col],edgecolor=COL['line'])
                for j,y in enumerate(v):a.text(j+(i-.5)*.32,y+.8,f'{y:g}',ha='center',fontsize=11)
            a.set(xticks=range(4),xticklabels=["組 0","組 1","組 2","組 3"],ylim=(0,49),ylabel="每組每方向載荷（MiB）")
            a.legend(frameon=False,ncol=2,loc='upper right')
            out.save(f,'figure-9-ep-skew')
            f,a=plot(3.3,left=.21,bottom=.23)
            f.subplots_adjust(top=.81)
            for row,times in enumerate(((.1,.3,.1),(.2,.8,.4))):
                start=0
                for duration,c in zip(times,('blue','green','orange')):
                    a.barh(row,duration,left=start,height=.42,color=COL[c],edgecolor=COL['line']);start+=duration
                if start<1.4:a.barh(row,1.4-start,left=start,height=.42,color=COL['gray'],edgecolor=COL['line'])
                a.text(start,row-.34,f'{start:.1f} ms',ha='center',fontsize=11)
            from matplotlib.patches import Patch
            handles=[Patch(facecolor=COL[c],edgecolor=COL['line'],label=label) for c,label in [('blue',"分派"),('green',"計算"),('orange',"回傳"),('gray',"等待")]]
            a.axvline(1.4,color=COL['line'],ls='--');a.set(yticks=[0,1],yticklabels=["快專家","慢專家"],xlabel="從該層分派開始計時（ms）",xlim=(0,1.52),ylim=(1.6,-.65))
            a.legend(handles=handles,frameon=False,ncol=4,loc='upper center',bbox_to_anchor=(.48,1.28),columnspacing=.65,handlelength=1)
            out.save(f,'figure-9-ep-tail')
            draw_ep_mechanisms(out)
    (Path(here)/'ub-ep-layout-validation.json').write_text(json.dumps(out.checks,ensure_ascii=False,indent=2)+'\n')
    return out.outputs


if __name__=='__main__':
    _,family=configure_font()
    plt.rcParams.update({'font.family':[family,'DejaVu Sans'],'axes.unicode_minus':False,'svg.hashsalt':'ub-ep-book'})
    for ch in (6,7,9):draw(ch,ROOT/f'manuscripts/ch{ch:02}')
