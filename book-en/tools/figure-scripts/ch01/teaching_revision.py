"""Chapter 1: one question per book-size figure. Inputs come from build.py's locked evidence."""
import numpy as np
import matplotlib.pyplot as plt
from figure_style import COL, STYLE, canvas, plot, text, box, arrow, Exporter

def draw(here,data):
    out=Exporter(here)
    with plt.rc_context(STYLE):
        f,a=canvas(5.2)
        layers=[("applications and tasks","What to complete, when",'orange'),
                ("model and workload","What compute and data needed",'blue'),
                ("training and inference system","Schedule requests, batches, accelerators",'green'),
                ("operator and compiler runtime","Turn computation into executable program",'purple'),
                ("processors and storage","Compute and store data",'blue'),
                ("interconnect and datacenter","Connect devices, provide power and cooling",'gray')]
        for i,(title,body,c) in enumerate(layers):
            y=.825-i*.153
            box(a,.06,y,.88,.125,title+'\n'+body,c)
            if i<5:arrow(a,(.5,y),(.5,y-.028))
        out.save(f,'figure-1-1-panorama')

        f,a=canvas(4.4)
        for x,label,c in [(.02,"Application\norganize input",'orange'),(.36,"Service entry\nreceive requests",'gray'),(.70,"Router\nselect instance",'purple')]:
            box(a,x,.76,.28,.18,label,c)
        arrow(a,(.30,.85),(.36,.85));arrow(a,(.64,.85),(.70,.85))
        box(a,.02,.06,.96,.52,'','gray');text(a,.05,.53,"selected inference instance",14)
        box(a,.06,.17,.24,.22,"instance scheduler\nforms batch",'green')
        box(a,.38,.17,.24,.22,"CPU\nsubmits program",'blue')
        box(a,.70,.17,.24,.22,"GPU\nexecutes computation",'orange')
        arrow(a,(.30,.28),(.38,.28));arrow(a,(.62,.28),(.70,.28))
        arrow(a,(.84,.76),(.84,.61));text(a,.49,.65,"request enters instance",11,ha='center')
        out.save(f,'figure-1-2-request')

        f,a=canvas(3.7)
        box(a,.04,.82,.29,.13,"model file",'gray');box(a,.04,.63,.92,.13,"GPU memory: stores one copy of weights",'blue')
        arrow(a,(.18,.82),(.18,.76));text(a,.46,.875,"loaded at startup",11)
        for x,s in [(.05,"step 1"),(.37,"step 2"),(.69,"step 3")]:
            box(a,x,.20,.26,.23,s+"\nCompute unit",'green')
            arrow(a,(x+.13,.63),(x+.13,.44))
        text(a,.50,.55,"each step reads required weights from GPU memory",12,ha='center')
        arrow(a,(.31,.31),(.37,.31));arrow(a,(.63,.31),(.69,.31))
        text(a,.5,.08,"previous step's output becomes next step's input",12,ha='center')
        out.save(f,'figure-1-weight-lifetime')

        f,a=canvas(4.8)
        box(a,.04,.77,.40,.17,"ingress and shared storage",'gray');box(a,.57,.77,.39,.17,"other supernodes",'purple')
        box(a,.20,.56,.60,.12,"datacenter network",'green')
        arrow(a,(.24,.77),(.38,.68));arrow(a,(.76,.77),(.62,.68))
        box(a,.02,.025,.96,.44,'','gray');text(a,.05,.425,"zoom into one supernode",14)
        box(a,.08,.27,.36,.11,"CPU and main memory",'blue');box(a,.61,.27,.31,.11,"NIC",'green')
        arrow(a,(.5,.56),(.76,.39));arrow(a,(.44,.325),(.61,.325))
        for x in [.08,.61]:box(a,x,.07,.31,.13,"GPU and memory",'orange')
        arrow(a,(.235,.27),(.235,.20));arrow(a,(.765,.27),(.765,.20))
        arrow(a,(.39,.135),(.61,.135));text(a,.50,.235,"internal interconnect",11,ha='center')
        out.save(f,'figure-1-3-datacenter')

        f,a=plot(3.4,left=.29)
        names=["main memory access","in-datacenter round trip","disk seek"]; vals=[100,500000,10000000]
        a.barh(names,vals,color=[COL['blue'],COL['green'],COL['orange']],edgecolor=COL['line'],height=.5)
        a.set_xscale('log');a.set_xlim(10,1e8);a.set_xlabel("Time (ns, log scale)");a.invert_yaxis()
        for i,(v,label) in enumerate(zip(vals,['0.1 μs','0.5 ms','10 ms'])):a.text(v*1.35,i,label,va='center',fontsize=12)
        out.save(f,'figure-1-4-numbers')

        capacity=data['capacity_example']
        bf16=capacity['bf16_weight_bytes']/1e9
        int8=capacity['int8_weight_and_metadata_bytes']/1e9
        f,a=plot(3.5,left=.25)
        for y,v,c in [(3,bf16,'orange'),(2,bf16/2,'blue'),(1,bf16/2,'blue'),(0,int8,'green')]:
            a.barh(y,v,height=.55,color=COL[c],edgecolor=COL['line'])
            a.text(6,y,f'{v:.2f} GB',va='center',fontsize=12)
        a.axvline(80,color='#80542e',ls='--',lw=1);a.text(82,3.65,"Single-card capacity 80 GB",fontsize=11)
        a.axhline(.5,color='#999999',lw=.7)
        a.set(yticks=[3,2,1,0],yticklabels=["BF16 single card","BF16 card 0","BF16 card 1","8-bit single card"],
              xlim=(0,190),ylim=(-.55,4.05),xlabel="Weights and quantization overhead (GB)",xticks=[0,40,80,120,160])
        out.save(f,'figure-1-capacity-path')

        f,a=canvas(3.0)
        box(a,.04,.58,.37,.24,"Memory\n70 GB weights",'blue');box(a,.61,.58,.35,.24,"Compute unit\nmultiply-add",'green')
        arrow(a,(.41,.70),(.61,.70));text(a,.5,.45,"Read path: 3350 GB/s",12,ha='center')
        text(a,.5,.25,'70 GB ÷ 3350 GB/s ≈ 20.90 ms',14,ha='center')
        text(a,.5,.09,"1 byte/param, full read per step",11,ha='center')
        out.save(f,'figure-1-read-path')

        f,a=plot(3.7,left=.25)
        comp=data['teaching']['compute_ms'];mem=data['teaching']['weight_read_ms']
        labels=["original accelerator","compute doubled","bandwidth doubled"];y=np.arange(3)
        a.barh(y+.16,[mem,mem,mem/2],height=.29,color=COL['blue'],edgecolor=COL['line'],label="Read weights")
        a.barh(y-.16,[comp,comp/2,comp],height=.29,color=COL['orange'],edgecolor=COL['line'],label="matrix computation")
        for i,v in enumerate([mem,mem,mem/2]):a.text(v+.4,i+.16,f'{v:.2f}',fontsize=12,va='center')
        a.set(yticks=y,yticklabels=labels,xlim=(0,25),xlabel="Resource time lower bound (ms)");a.invert_yaxis();a.legend(loc='lower right',frameon=False)
        out.save(f,'figure-1-5-budget')

        f,a=canvas(3.5)
        text(a,.04,.91,"Same weights serving eight requests",14)
        box(a,.04,.64,.92,.15,"One read: 70 GB weights",'blue')
        for i in range(8):
            x=.04+i*.117;box(a,x,.24,.105,.18,str(i+1),'green');arrow(a,(x+.052,.63),(x+.052,.43))
        text(a,.5,.52,"Eight inputs each complete computation",12,ha='center')
        text(a,.5,.10,"Batch ~20.90 ms; ~2.61 ms per output token",12,ha='center')
        out.save(f,'figure-1-batch-reuse')

        d=data['teaching_diagrams']['batch_transition'];b=np.array(d['batch'])
        f,a=plot(3.8)
        a.plot(b,comp*b,color='#a96c28',label="matrix computation");a.axhline(mem,color='#267398',label="weight read")
        a.plot(b,np.maximum(comp*b,mem),color='#333333',ls='--',label="Max of both")
        a.axvline(d['crossing_batch'],color='#777777',ls=':',lw=1)
        a.text(156,mem+4,"~148",fontsize=12);a.set(xlim=(0,512),ylim=(0,80),xlabel="Requests per batch B",ylabel="Time lower bound (ms)")
        a.legend(loc='upper left',frameon=False);out.save(f,'figure-1-batch-transition')
        f,a=plot(3.4)
        a.plot(b,d['throughput'],color='#267398',lw=1.8);a.axvline(d['crossing_batch'],ls=':',color='#777777')
        a.set(xlim=(0,512),ylim=(0,8000),xlabel="Requests per batch B",ylabel="Output throughput (token/s)")
        a.text(180,6200,"Compute term starts to dominate",fontsize=12);out.save(f,'figure-1-batch-throughput')

        rows=data['measured_short_group']
        for key,ylabel,name in [('throughput',"Batch output throughput (token/s)",'figure-1-measured-throughput'),('tpot_ms',"Per-request output interval (ms)",'figure-1-measured-tpot')]:
            f,a=plot(3.3)
            vals=[r[key] for r in rows];a.plot(range(4),vals,'o-',color='#267398',lw=1.5)
            for i,v in enumerate(vals):a.annotate(f'{v:.2f}',(i,v),xytext=(0,10),textcoords='offset points',ha='center',fontsize=11)
            a.set(xlim=(-.45,3.45),ylim=(0,max(vals)*1.23),xticks=range(4),xticklabels=[r['batch'] for r in rows],xlabel="Concurrent requests (evenly spaced tiers)",ylabel=ylabel)
            out.save(f,name)

        for slug,title,items in [
            ('tpu',"Add dedicated compute and data-movement resources",[("input buffer",'blue'),("Matrix compute array",'orange'),("Output buffer",'green')]),
            ('smartnic',"Move packet processing to data path",[("Network data",'blue'),("Programmable NIC\npacket processing",'orange'),("Host CPU\nrun application",'green')]),
            ('ub',"Let devices exchange data directly",[("Device 0\ncompute and storage",'blue'),("Unified interconnect\ndata transfer",'green'),("Device 1\ncompute and storage",'orange')])]:
            f,a=canvas(2.5);text(a,.04,.89,title,14)
            for i,(label,c) in enumerate(items):
                x=.03+.335*i;box(a,x,.30,.27,.34,label,c)
                if i<2:arrow(a,(x+.27,.47),(x+.335,.47))
            out.save(f,'figure-1-design-'+slug)
    from core_principles_figures import draw as draw_principles
    draw_principles(1, out)
    return out.finish()
