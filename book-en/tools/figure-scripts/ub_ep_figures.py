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
    for y,label in [(Y['attn']+H/2,"attention, routing\nserver A"),(.705,'dispatch'),(Y['exp']+H/2,"expert computation\nserver B"),(.375,'combine'),(Y['merge']+H/2,"weighted sum\nserver A")]:
        text(a,.005,y,label,12)
    arrow(a,(.60,.98),(.60,Y['attn']+H));arrow(a,(.60,Y['merge']),(.60,.05))
    text(a,.63,.975,"previous layer output",11);text(a,.63,.055,"next layer attention",11)
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
        ax.set_title(f'EP{ep}\ncard {m} experts',fontsize=12,loc='center')
        ax.spines[['top','right']].set_visible(False)
        if k:ax.tick_params(axis='y',length=0)
    axes[0].set_ylabel("card load ÷ per-card average")
    axes[2].text(2.2,1.15,"dashed line: average",ha='center',va='bottom',fontsize=11)
    f.text(.56,.035,"card ID",ha='center',fontsize=12)
    out.save(f,'figure-9-ep-scale-cards')

    # Busiest/mean against EP size: one hot expert (exact) and uniform random routing (seeded simulation).
    f,a=plot(3.5,left=.15,bottom=.18)
    eps=[r['ep'] for r in s['results']]
    a.plot(eps,[r['hot_ratio'] for r in s['results']],marker='o',color=EP_LINE['orange'],label="one 4× hot expert")
    a.plot(eps,[r['random_mean_ratio'] for r in s['results']],marker='o',color=EP_LINE['blue'],label="uniform random routing, mean over 1000 batches")
    for r in s['results'][-1:]:
        a.text(r['ep']/1.12,r['hot_ratio'],f"{r['hot_ratio']:.1f}",ha='right',va='center',fontsize=11)
        a.text(r['ep']/1.12,r['random_mean_ratio']+.2,f"{r['random_mean_ratio']:.2f}",ha='right',va='center',fontsize=11)
    a.set_xscale('log',base=2);a.minorticks_off()
    a.set(xticks=eps,xticklabels=[str(e) for e in eps],xlim=(6.5,300),ylim=(.9,4.3),yticks=[1,2,3,4],
          xlabel="cards in EP group (experts per card = 256 ÷ cards)",ylabel="busiest card ÷ per-card average")
    a.axhline(1,color=COL['line'],ls=(0,(2,2)),lw=.9)
    a.legend(frameon=False,loc='upper left');a.grid(axis='y',alpha=.15)
    out.save(f,'figure-9-ep-scale-sweep')

    # Section 9.3.2: eight 36 MiB experts, 128 tokens each, on one Xeon 8452Y socket; the longer bar sets the time.
    P=3*4096*1536;W=2*P;flop=8*128*2*P
    f,axes=plt.subplots(1,2,figsize=(420/72,3.3))
    f.subplots_adjust(left=.17,right=.97,bottom=.30,top=.86,wspace=.35)
    for ax,(kernel,C,xmax) in zip(axes,[('AVX-512 kernel：1.8 TFLOP/s',1.8e12,26),('AMX kernel：21.3 TFLOP/s',21.3e12,3.2)]):
        for row,(bw,label) in enumerate([(220e9,"same socket"),(125e9,"cross socket")]):
            read=8*W/bw*1e3;comp=flop/C*1e3
            for off,(v,col) in zip((-.17,.17),[(read,'blue'),(comp,'green')]):
                ax.barh(row+off,v,height=.3,color=COL[col],edgecolor=COL['line'],linewidth=1.6 if v==max(read,comp) else .8)
                ax.text(v+xmax*.02,row+off,f'{v:.2f}',va='center',fontsize=11)
        ax.set(yticks=[0,1],yticklabels=["same socket\n220 GB/s","cross socket\n125 GB/s"] if ax is axes[0] else ['',''],xlim=(0,xmax),ylim=(1.5,-.5))
        ax.set_title(kernel,fontsize=12);ax.spines[['top','right']].set_visible(False)
        if ax is not axes[0]:ax.tick_params(axis='y',length=0)
    f.text(.57,.14,"time (ms)",ha='center',fontsize=12)
    f.legend(handles=[Patch(facecolor=COL['blue'],edgecolor=COL['line'],label="read eight weight copies"),Patch(facecolor=COL['green'],edgecolor=COL['line'],label="matrix computation for eight experts")],
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
    for ax,(title,items) in zip(axes,[(f'sequential execution:{q*(tA+tF)} ms',serial),(f'interleaved pipeline:{ready} ms',pipe)]):
        for row,start,dur,k in items:
            ax.barh(row,dur,left=start,height=.55,color=COL['blue' if row==0 else 'green'],edgecolor=COL['line'])
            ax.text(start+dur/2,row,str(k),ha='center',va='center',fontsize=11)
        ax.set(yticks=[0,1],yticklabels=["attention node","expert node"],xlim=(0,21),ylim=(1.6,-.6),xticks=[0,5,10,14,20])
        ax.set_title(title,loc='left',fontsize=12);ax.spines[['top','right']].set_visible(False);ax.grid(axis='x',alpha=.15)
    axes[1].axvline(ready,color=EP_LINE['orange'],ls='--',lw=1)
    axes[1].set_xlabel("time (ms); numbers in boxes are micro-batch IDs")
    out.save(f,'figure-9-af-pingpong')



def draw(ch, here):
    out=Exporter(here)
    with plt.rc_context(STYLE):
        if ch == 6:
            f,a=canvas(4.3)
            text(a,.04,.95,"app endpoints kept separate, reliable transport shared on demand",13)
            for x,label in ((.06,"app A\nJetty A"),(.59,"app B\nJetty B")):
                box(a,x,.69,.35,.18,label,'blue')
                arrow(a,(x+.175,.69),(.5,.56))
            box(a,.17,.37,.66,.19,"shared transport channel\nsequencing, ACK, retransmission, congestion control",'orange')
            arrow(a,(.5,.37),(.5,.24))
            box(a,.17,.06,.66,.18,"remote transaction layer\ndispatch and permission check by target endpoint",'green')
            text(a,.50,.63,"transaction → packet",11,ha='center')
            text(a,.73,.30,"network delivery",11,ha='center')
            out.save(f,'figure-6-ub-layers')
            fab=json.loads((ROOT/'calculations/results/ub-fabric-book.json').read_text())
            LINE={'blue':'#267398','orange':'#a56c28','green':'#28856a','purple':'#7a5c99'}
            # Controller placement: behind PCIe versus on the on-chip bus.
            f,a=canvas(4.0)
            text(a,.04,.95,"issue path for one remote read",13)
            for x0,title,chain in ((.02,"PCIe peripheral NIC",[("processor",'blue'),("on-chip\nbus",'green'),('PCIe','gray'),("NIC",'orange')]),
                                   (.52,"controller on on-chip bus",[("processor",'blue'),("on-chip\nbus",'green'),("UB\ncontroller",'orange')])):
                text(a,x0+.23,.84,title,12,ha='center')
                n=len(chain);gap=.025;w=(.46-(n-1)*gap)/n
                for i,(label,c) in enumerate(chain):
                    x=x0+i*(w+gap)
                    box(a,x,.47,w,.26,label,c,11)
                    if i<n-1:arrow(a,(x+w,.60),(x+w+gap,.60))
                arrow(a,(x0+.23,.47),(x0+.23,.33))
                text(a,x0+.23,.27,"network",11,ha='center')
            text(a,.25,.11,"doorbell and DMA each cross PCIe once",11,ha='center')
            text(a,.75,.11,"instruction reaches controller via on-chip bus",11,ha='center')
            out.save(f,'figure-6-ub-controller')
            # Per-NIC state against hosts in one fabric, three organisations.
            hosts=[r['hosts'] for r in fab['hosts']]
            f,a=plot(3.8,left=.19)
            f.subplots_adjust(top=.80)
            for key,label,c in (('roce_bytes',"pairwise connection (RoCE)",'orange'),('directory_bytes',"directory-based coherent interconnect",'purple'),('ub_bytes',"endpoint plus channel (UB)",'green')):
                a.plot(hosts,[r[key]/1024 for r in fab['hosts']],marker='o',color=LINE[c],label=label)
            a.axhline(fab['cache']['context_cache_bytes']/1024,color=COL['line'],ls='--')
            a.text(hosts[0],fab['cache']['context_cache_bytes']/1024*1.4,"on-chip context cache 256 KiB",fontsize=11)
            a.set(xscale='log',yscale='log',xlabel="hosts in interconnect (8 endpoints each)",ylabel="state per NIC (KiB)")
            a.set_xticks(hosts);a.set_xticklabels([str(h) for h in hosts])
            a.legend(frameon=False,ncol=3,loc='upper center',bbox_to_anchor=(.45,1.27),columnspacing=.8,handlelength=1.4)
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-6-ub-hosts')
            # Connection setup time, N local × N remote endpoints, 32 cores in parallel.
            f,a=plot(3.7,left=.19)
            f.subplots_adjust(top=.82)
            ns=[r['endpoints'] for r in fab['setup']]
            for key,label,c in (('roce_parallel_s',"one connection per pair (RoCE)",'orange'),('ub_parallel_s',"one Jetty per endpoint, one channel per remote (UB)",'green')):
                a.plot(ns,[max(r[key],1e-9) for r in fab['setup']],marker='o',color=LINE[c],label=label)
            top=fab['setup'][-1]
            a.annotate(f"{top['roce_parallel_s']:.1f} s",(ns[-1],top['roce_parallel_s']),xytext=(-52,-4),textcoords='offset points',fontsize=11)
            a.annotate(f"{top['ub_parallel_s']*1000:.0f} ms",(ns[-1],top['ub_parallel_s']),xytext=(-46,-14),textcoords='offset points',fontsize=11)
            a.set(xscale='log',yscale='log',xlabel="local endpoints N (remote endpoints M = N)",ylabel="time to establish all relations (s)")
            a.set_xticks(ns);a.set_xticklabels([str(n) for n in ns])
            a.legend(frameon=False,ncol=1,loc='upper center',bbox_to_anchor=(.45,1.3),handlelength=1.4)
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-6-ub-setup')
        if ch == 6:
            # Who issues a network request: CPU proxy, GPU SMs, or the NIC's own processor.
            f, a = canvas(4.0)
            for i, (title, ctrl, note) in enumerate([("CPU proxy thread", 0, "PCIe crossings: 3"), ("GPU SM", 1, "PCIe crossings: 2"), ("NIC processor", 2, "PCIe crossings: 0")]):
                x0 = .02 + .33 * i
                text(a, x0 + .15, .95, title, 12, ha='center')
                box(a, x0 + .01, .70, .12, .12, 'CPU', 'orange' if ctrl == 0 else 'gray', 11)
                box(a, x0 + .17, .70, .12, .12, 'GPU', 'orange' if ctrl == 1 else 'blue', 11)
                a.plot([x0, x0 + .30], [.52, .52], color=COL['line'], lw=.9, ls=(0, (3, 3)))
                text(a, x0 + .30, .56, 'PCIe', 11, ha='right')
                box(a, x0 + .09, .20, .12, .12, "NIC", 'orange' if ctrl == 2 else 'green', 11)
                if ctrl == 0:
                    arrow(a, (x0 + .17, .76), (x0 + .13, .76)); text(a, x0 + .15, .86, "ready", 11, ha='center')
                    arrow(a, (x0 + .06, .70), (x0 + .12, .32)); text(a, x0 + .01, .45, "doorbell\nrequest descriptor", 11)
                elif ctrl == 1:
                    arrow(a, (x0 + .19, .70), (x0 + .13, .32)); text(a, x0 + .01, .45, "doorbell\nrequest descriptor", 11)
                else:
                    arrow(a, (x0 + .06, .70), (x0 + .12, .32)); text(a, x0 + .01, .45, "one trigger per batch", 11)
                arrow(a, (x0 + .18, .32), (x0 + .24, .70)); text(a, x0 + .21, .40, "payload, completion", 11)
                text(a, x0 + .15, .08, note, 11, ha='center')
            out.save(f, 'figure-6-initiator')
        if ch == 7:
            # PCIe transaction types: posted writes finish on send; reads wait for tagged completions.
            f, a = canvas(3.2)
            text(a, .02, .90, "write (posted): complete on send", 12)
            box(a, .10, .58, .16, .16, "initiator", 'blue', 11); box(a, .74, .58, .16, .16, "receiver", 'green', 11)
            arrow(a, (.26, .66), (.74, .66)); text(a, .50, .74, "write transaction packet: address + data", 11, ha='center')
            text(a, .02, .44, "read (non-posted): in-flight count limited by tags and credits", 12)
            box(a, .10, .10, .16, .16, "initiator", 'blue', 11); box(a, .74, .10, .16, .16, "receiver", 'green', 11)
            arrow(a, (.26, .22), (.74, .22)); text(a, .50, .31, "read request packet: address + tag", 11, ha='center')
            arrow(a, (.74, .14), (.26, .14)); text(a, .50, .04, "completion packet: data + same tag", 11, ha='center')
            out.save(f, 'figure-7-pcie-transactions')
            # Which ceiling binds a 64 B random DMA read on the KV-Direct platform.
            f, a = plot(2.8, left=.34, bottom=.26)
            labels = ["link bandwidth conversion", "packet header overhead cap", "in-flight tag limit", "measured"]
            vals = [123, 87, 61, 60]; cols = [COL['blue'], COL['blue'], COL['orange'], COL['green']]
            a.barh(range(4), vals, color=cols, edgecolor=COL['line'], height=.55)
            for i, v in enumerate(vals): a.text(v + 2, i, f'{v}', va='center', fontsize=11)
            a.set(yticks=range(4), yticklabels=labels, xlim=(0, 140), xlabel="64 B random DMA reads, million ops/s"); a.invert_yaxis()
            out.save(f, 'figure-7-pcie-limits')
            # Two traffic classes sharing a GPU's PCIe link, per direction.
            f, a = canvas(3.8)
            box(a, .03, .62, .18, .14, "host memory", 'gray', 11); box(a, .03, .24, .18, .14, "NIC", 'gray', 11)
            a.plot([.56, .56], [.10, .92], color=COL['line'], lw=.9, ls=(0, (3, 3))); text(a, .56, .96, "PCIe link", 11, ha='center')
            box(a, .62, .14, .34, .70, '', 'blue'); text(a, .79, .78, 'GPU', 12, ha='center')
            box(a, .68, .40, .22, .14, 'HBM', 'white', 11)
            arrow(a, (.21, .72), (.62, .72)); text(a, .41, .79, "completion packet (H2D copy)", 11, ha='center')
            arrow(a, (.62, .62), (.21, .62)); text(a, .41, .55, "posted write (D2H copy)", 11, ha='center')
            arrow(a, (.21, .34), (.62, .34)); text(a, .41, .41, "posted write (remote write)", 11, ha='center')
            arrow(a, (.62, .24), (.21, .24)); text(a, .41, .17, "completion packet (remote read)", 11, ha='center')
            text(a, .79, .30, "two outbound paths\nboth fetch from HBM first", 11, ha='center')
            text(a, .79, .64, "two inbound paths\ncontend on link", 11, ha='center')
            out.save(f, 'figure-7-pcie-asymmetry')
            f,a=canvas(4.6)
            text(a,.04,.96,"64-card supernode: 8 TP8 groups",13)
            for row in range(8):
                y=.79-row*.075
                text(a,.02,y+.023,str(row),11)
                for col in range(8):box(a,.10+col*.103,y,.079,.047,'','orange' if col==0 else 'blue')
            text(a,.51,.88,"same row: TP sharding, jointly compute one input",11,ha='center')
            text(a,.5,.12,"same column: corresponding gradients reduced locally first",12,ha='center')
            arrow(a,(.5,.09),(.5,.02))
            text(a,.73,.04,"then exchanged across nodes",11,ha='center')
            out.save(f,'figure-7-supernode-groups')
            records=json.loads((ROOT/'calculations/results/supernode-scaling-book.json').read_text())['results']
            f,a=plot(3.7,left=.19)
            labels=["egress expansion","egress cap","egress expansion + local doubling"]
            colors=['#267398','#a56c28','#28856a']
            for i in range(3):
                rs=records[i*4:(i+1)*4]
                a.plot(range(4),[r['tokens_per_s']/1e4 for r in rs],marker='o',color=colors[i],label=labels[i])
            a.set(xticks=range(4),xticklabels=['8','64','128','256'],xlabel="cards per supernode",ylabel="throughput (10k tokens/s)",ylim=(100,205))
            a.legend(frameon=False,fontsize=11,loc='upper left')
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-7-supernode-scaling')
            fab=json.loads((ROOT/'calculations/results/ub-fabric-book.json').read_text())
            LINE={'blue':'#267398','orange':'#a56c28','green':'#28856a','purple':'#7a5c99'}
            # Endpoint state, N = M sweep.
            f,a=plot(3.7,left=.19)
            f.subplots_adjust(top=.82)
            ns=[r['endpoints'] for r in fab['state']]
            a.plot(ns,[r['roce_bytes']/1024 for r in fab['state']],marker='o',color=LINE['orange'],label="N×M connection states (RoCE)")
            a.plot(ns,[r['ub_bytes']/1024 for r in fab['state']],marker='o',color=LINE['green'],label="N Jetties plus M channels (UB)")
            a.axhline(fab['cache']['context_cache_bytes']/1024,color=COL['line'],ls='--')
            a.text(ns[0],fab['cache']['context_cache_bytes']/1024*1.5,"on-chip cache 256 KiB",fontsize=11)
            top=fab['state'][-1]
            a.annotate(f"{top['ratio']:,.0f} ×",(ns[-1],top['ub_bytes']/1024),xytext=(-40,12),textcoords='offset points',fontsize=11)
            a.set(xscale='log',yscale='log',xlabel="local endpoints N (remote endpoints M = N)",ylabel="state per NIC (KiB)")
            a.set_xticks(ns);a.set_xticklabels([str(n) for n in ns])
            a.legend(frameon=False,ncol=2,loc='upper center',bbox_to_anchor=(.45,1.25),columnspacing=1,handlelength=1.4)
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-7-ub-state-growth')
            # Latency against active endpoints: the cache cliff.
            f,a=plot(3.6,left=.17)
            f.subplots_adjust(top=.82)
            sw=fab['cache']['sweep'];xs=[r['endpoints'] for r in sw]
            a.step(xs,[r['roce_dma_ns']/1000 for r in sw],where='post',color=LINE['orange'],label="RoCE read")
            a.step(xs,[r['ub_loadstore_ns']/1000 for r in sw],where='post',color=LINE['green'],label='UB Load')
            a.annotate(f"N = {fab['cache']['roce_spill_endpoints']} overflow, each extra {fab['cache']['roce_refetch_ns']} ns",(fab['cache']['roce_spill_endpoints'],sw[-1]['roce_dma_ns']/1000),xytext=(6,6),textcoords='offset points',fontsize=11)
            a.annotate(f"N = {fab['cache']['ub_spill_endpoints']} overflow, extra {fab['cache']['ub_refetch_ns']} ns",(fab['cache']['ub_spill_endpoints'],sw[-1]['ub_loadstore_ns']/1000),xytext=(-4,8),textcoords='offset points',fontsize=11,ha='right')
            a.set(xscale='log',xlabel="active endpoints N (M = N)",ylabel="one 64 B read (μs)",ylim=(0,3.9))
            a.set_xticks([1,8,64,512,4096]);a.set_xticklabels(['1','8','64','512','4096'])
            a.legend(frameon=False,ncol=2,loc='upper center',bbox_to_anchor=(.45,1.22),columnspacing=1.5,handlelength=1.4)
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-7-ub-cache-cliff')
            # Round trip budget by phase group, three stacks.
            f,a=plot(3.9,left=.24,bottom=.18)
            f.subplots_adjust(top=.80)
            stacks=[('roce_dma',"peripheral-style RoCE read"),('ub_urma',"UB asynchronous read"),('ub_loadstore','UB Load')]
            groups=fab['groups'];fills=['blue','gray','green','orange','purple','white']
            from matplotlib.patches import Patch
            for row,(key,label) in enumerate(stacks):
                start=0
                for g,c in zip(groups,fills):
                    v=fab['round_trip'][key]['group_ns'][g]
                    if v:a.barh(row,v,left=start,height=.55,color=COL[c],edgecolor=COL['line']);start+=v
                a.text(start+40,row,f"derivation {fab['round_trip'][key]['total_ns']:.0f}, simulation {fab['round_trip'][key]['paper_measured_ns']}",va='center',fontsize=11)
            a.set(yticks=range(3),yticklabels=[l for _,l in stacks],xlabel="critical path of one 64 B remote read (ns)",xlim=(0,3300))
            a.invert_yaxis()
            a.legend(handles=[Patch(facecolor=COL[c],edgecolor=COL['line'],label=g) for g,c in zip(groups,fills)],frameon=False,ncol=3,loc='upper center',bbox_to_anchor=(.4,1.3),columnspacing=.8,handlelength=1.2)
            out.save(f,'figure-7-ub-round-trip')
            # Total against one-way link delay: same slope, different intercepts.
            f,a=plot(3.6,left=.17)
            f.subplots_adjust(top=.82)
            for key,label,c in (('roce_dma',"peripheral-style RoCE read",'orange'),('ub_urma',"UB asynchronous read",'blue'),('ub_loadstore','UB Load','green')):
                pts=fab['round_trip'][key]['link_sweep']
                a.plot([p['link_ns'] for p in pts],[p['total_ns']/1000 for p in pts],marker='o',color=LINE[c],label=label)
            a.set(xlabel="one-way wire latency (ns)",ylabel="one 64 B read (μs)",xlim=(0,540),ylim=(0,3.4))
            a.legend(frameon=False,ncol=3,loc='upper center',bbox_to_anchor=(.45,1.22),columnspacing=1.2,handlelength=1.4)
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-7-ub-link-delay')
        if ch == 9:
            data=json.loads((ROOT/'calculations/results/ep-skew-book.json').read_text())['results']
            f,a=plot(3.7,left=.16)
            for i,(r,label,col) in enumerate(zip(data[:2],["balanced","hotspot"],['blue','orange'])):
                v=np.array(r['expert_assignments'])*8192/2**20
                a.bar(np.arange(4)+(i-.5)*.32,v,width=.30,label=label,color=COL[col],edgecolor=COL['line'])
                for j,y in enumerate(v):a.text(j+(i-.5)*.32,y+.8,f'{y:g}',ha='center',fontsize=11)
            a.set(xticks=range(4),xticklabels=["group 0","group 1","group 2","group 3"],ylim=(0,49),ylabel="payload per group per direction (MiB)")
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
            handles=[Patch(facecolor=COL[c],edgecolor=COL['line'],label=label) for c,label in [('blue',"dispatch"),('green',"compute"),('orange',"return"),('gray',"wait")]]
            a.axvline(1.4,color=COL['line'],ls='--');a.set(yticks=[0,1],yticklabels=["fast expert","slow expert"],xlabel="timing from layer dispatch (ms)",xlim=(0,1.52),ylim=(1.6,-.65))
            a.legend(handles=handles,frameon=False,ncol=4,loc='upper center',bbox_to_anchor=(.48,1.28),columnspacing=.65,handlelength=1)
            out.save(f,'figure-9-ep-tail')
            draw_ep_mechanisms(out)
    (Path(here)/'ub-ep-layout-validation.json').write_text(json.dumps(out.checks,ensure_ascii=False,indent=2)+'\n')
    return out.outputs


if __name__=='__main__':
    _,family=configure_font()
    plt.rcParams.update({'font.family':[family,'DejaVu Sans'],'axes.unicode_minus':False,'svg.hashsalt':'ub-ep-book'})
    for ch in (6,7,9):draw(ch,ROOT/f'manuscripts/ch{ch:02}')
