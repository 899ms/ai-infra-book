"""Placement first, state handoff second, resource rates last."""
from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,n):out.save(f,'figure-9-'+n)
    with plt.rc_context(STYLE):
        for i,title in enumerate(["Multiple cards jointly run one full model","Full replicas receive requests independently","PD: split by input processing and generation stages","AF: split by per-layer operators"]):
            f,a=canvas(3.7);text(a,.04,.94,title,14)
            if i==0:
                box(a,.04,.22,.92,.48,'','gray');text(a,.5,.61,"One scheduler, one set of model weights and state",12,ha='center')
                for j in range(8):box(a,.06+j*.112,.32,.09,.12,str(j),'blue',11)
            elif i==1:
                for x in [.04,.56]:box(a,x,.25,.40,.26,"Full model replica",'blue');text(a,x+.2,.72,"Independent request",12,ha='center');arrow(a,(x+.2,.65),(x+.2,.51))
            else:
                for x,label,c in [(.04,"P: process input" if i==2 else "Attention",'blue'),(.61,"D: generate step by step" if i==2 else "FFN/expert",'green')]:box(a,x,.28,.35,.27,label,c)
                arrow(a,(.39,.46),(.61,.46));text(a,.5,.68,"Transfer context KV" if i==2 else "Pass activations layer by layer",12,ha='center')
                if i==3:arrow(a,(.61,.35),(.39,.35))
            save(f,'1-organization' if i==0 else f'organization-{i}')
        f,a=canvas(4.3)
        for j,l in enumerate(['P','D',"tool waiting","next round P"]):box(a,.20+j*.19,.73,.18,.15,l,'gray',11)
        for row,(l,start,c) in enumerate([("weights",.20,'blue'),('KV',.20,'green'),("Reusable EC",.20,'purple')]):
            y=.48-row*.17;text(a,.02,y+.05,l,11);box(a,start,y,.75,.10,'',c)
        text(a,.5,.04,"Stage width shows order; state retained while waiting",11,ha='center');save(f,'2-state')
        for stage,name in [(0,'kv-residency'),(1,'kv-publish'),(2,'kv-release')]:
            if stage==0:
                # Two states of the same 8K context; box widths follow the byte counts (1.125 GiB versus 549 MiB).
                f,a=canvas(4.6);text(a,.04,.95,"Transfer start: both ends occupy full space",13)
                for row,(model,size,w) in enumerate([('Qwen3-8B，GQA','1.125 GiB',.35),("DeepSeek-V3, compact MLA",'549 MiB',.17)]):
                    y=.52-row*.38;text(a,.04,y+.30,model,12)
                    box(a,.04,y,w,.22,"Source P\n"+size,'blue');box(a,.96-w,y,w,.22,"Destination D\n"+size,'orange');arrow(a,(.04+w,y+.11),(.96-w,y+.11),'data')
                text(a,.5,.05,"Copying data; box width proportional to bytes",12,ha='center');save(f,name);continue
            f,a=canvas(3.9);text(a,.04,.94,["Transfer start: both ends occupy full space","Transfer complete: notify destination KV ready","Source releases buffer, D continues generation"][stage],13)
            box(a,.04,.35,.35,.29,"Source P\n1.125 GiB" if stage<2 else "Source P\nreleased",'blue' if stage<2 else 'gray');box(a,.61,.35,.35,.29,"Destination D\n1.125GiB",'orange' if stage==0 else 'green');arrow(a,(.39,.5),(.61,.5),'data' if stage==0 else 'control');text(a,.5,.15,"Copying data" if stage==0 else "Completion marker establishes usage order" if stage==1 else "Next request can use source space",12,ha='center');save(f,name)
        f,a=canvas(4.4)
        r=data['9-3']['per_card_rates']
        for row,(title,per,c) in enumerate([("P pool: four A100s",r['A100']['prefill'],'blue'),("D pool: four H20s",r['H20']['decode'],'green')]):
            y=.61-row*.40;text(a,.04,y+.23,title,14)
            for i in range(4):box(a,.04+i*.235,y,.21,.16,f'{per:.2f} req/s',c,11)
            text(a,.5,y-.09,f'Pool capacity:{4*per:.2f} req/s',12,ha='center')
        save(f,'pd-layout')
        f,a=plot(4.5,left=.17);matrix=np.zeros((5,5))
        for row in data['9-3']['assignments']:
            x=row['prefill_workers']['A100'];y=row['prefill_workers']['H20'];matrix[y,x]=float(Fraction(row['bound_requests_per_second_exact']))
        a.imshow(matrix,origin='lower',cmap='Blues',vmin=0,vmax=10,aspect='equal')
        for y in range(5):
            for x in range(5):a.text(x,y,f'{matrix[y,x]:.2f}',fontsize=11,ha='center',va='center')
        a.add_patch(plt.Rectangle((3.5,-.5),1,1,fill=False,edgecolor='#a56c28',lw=2.2))
        a.set(xticks=range(5),yticks=range(5),xlabel="A100 count allocated to P",ylabel="H20 count allocated to P");save(f,'3-pd')
        f,a=canvas(4.9)
        for row,(na,nh) in enumerate(zip(data['new-allocation']['prefill_A100'],data['new-allocation']['prefill_H20'])):
            y=.70-row*.31;text(a,.04,y+.18,["Inference request: 1025 outputs","Prefix hit: 6144 tokens","output reduced to 129 tokens"][row],13)
            for i in range(8):
                isp=i<na if i<4 else i-4<nh
                box(a,.035+i*.117,y,.10,.12,('A100' if i<4 else 'H20')+'\n'+('P' if isp else 'D'),'blue' if isp else 'green',11)
            text(a,.5,y-.045,f'Request rate limit{data["new-allocation"]["rates"][row]:.2f}/s',11,ha='center')
        save(f,'4-allocation')
        for local,name in [(False,'5-local'),(True,'local-cpu')]:
            f,a=canvas(4.4);box(a,.04,.67,.35,.18,"CPU memory: expert weights",'blue',11);box(a,.61,.67,.35,.18,"GPU: input activations",'green',11)
            if local:
                arrow(a,(.61,.76),(.39,.76));box(a,.04,.31,.35,.18,"CPU expert computation",'blue');arrow(a,(.215,.67),(.215,.49));arrow(a,(.39,.40),(.61,.40));box(a,.61,.31,.35,.18,"GPU aggregated result",'orange',11)
            else:
                arrow(a,(.39,.76),(.61,.76));box(a,.61,.31,.35,.18,"GPU expert computation",'green');arrow(a,(.785,.67),(.785,.49))
            text(a,.5,.13,"Activation round trip: 16 KiB per row" if local else "Move one expert weight: 36 MiB",12,ha='center');save(f,name)
        d=data['9-6'];f,a=plot(3.9)
        for key,label,c,ls in [('cpu_avx512_ms','CPU，AVX-512','#267398','-'),('cpu_amx_ms','CPU，AMX','#267398','--'),('weight_copy_gpu_ms',"Move weights to GPU",'#a56c28','-')]:a.plot(d['tokens_per_expert'],d[key],label=label,color=c,ls=ls)
        a.set_xscale('log',base=2);a.set(xlabel="Tokens received per expert (log scale)",ylabel="Path time for eight experts (ms)",xlim=(1,1024),ylim=(0,30),xticks=[1,4,16,64,256,1024],xticklabels=['1','4','16','64','256','1024']);a.minorticks_off();a.legend(frameon=False);save(f,'6-reuse')
        # The two expert-footprint rectangles repeated figure 6-19, so section 9.3.3 keeps only the prose recall.
        d=data['9-mla-handoff'];f,a=plot(3.8)
        for k,l,c in [('pd_gqa_ms',"PD one handoff: GQA 1.125GiB",'#267398'),('pd_mla_ms',"PD one handoff: compact MLA 549MiB",'#388768'),('af_step_ms',"AF one-step handoff: 72 times",'#a56c28')]:a.plot(d['startup_us'],d[k],label=l,color=c)
        for key,c in [('gqa25','#267398'),('mla25','#388768')]:
            x=d['equal_time_startup_us'][key];y=589824/25e9*1e3+72*x/1e3
            a.scatter([x],[y],color=c,zorder=3);a.annotate(f'{x:.0f} μs',(x,y),xytext=(x+25,y-9),fontsize=11)
        a.set(xlabel="Startup overhead per launch (μs)",ylabel="Serial handoff time (ms)",xlim=(0,800),ylim=(0,80),yticks=[0,20,40,60,80]);a.legend(frameon=False,loc='upper left');save(f,'mla-handoff')
        for i,tasks in enumerate(data['new-balance']['assignments_per_card']):
            f,a=plot(4,left=.17);times=np.array(tasks)*2*18874368/(data['new-balance']['effective_TFLOPs']*1e12)*1e6;a.barh(range(8),times,color=COL['blue'],edgecolor=COL['line']);a.axvline(max(times),ls='--',color='#a56c28');a.set(yticks=range(8),yticklabels=[f'card {j}' for j in range(8)],xlim=(0,42),xlabel="Expert matrix computation on H100 (μs)");a.invert_yaxis();save(f,'9-balance' if i==0 else 'balance-hotspot')
        d=data['9-10'];f,a=plot(3.6)
        for key,label,c in [('nvlink',"within same HGX via NVLink",'#388768'),('cx7',"cross-server via ConnectX-7",'#a56c28')]:a.plot(d['batches'],d['net_saving_ms'][key],color=c,label=label)
        a.axhline(0,color='#777777');a.set(xlabel="batches hotspot persists",ylabel="Cumulative net savings (ms)");a.legend(frameon=False);save(f,'10-experts')
        for i,items in enumerate([data['new-overlap']['serial_items'],data['new-overlap']['pipeline_items']]):
            f,a=plot(3.5,left=.23)
            for row,start,dur,_ in items:a.barh(row,dur,left=start,height=.5,color=COL[['blue','green','orange'][row]],edgecolor=COL['line'])
            a.set(yticks=[0,1,2],yticklabels=["dispatch","Expert computation","Result merge"],xlim=(0,.88),xlabel="time (ms)");a.invert_yaxis();save(f,'11-overlap' if i==0 else 'overlap-pipeline')
        f,a=canvas(3.8);box(a,.04,.50,.34,.24,"Directory record\nID → storage location",'orange',11);box(a,.62,.50,.34,.24,"KV data object\nactual context state",'blue',11);arrow(a,(.38,.62),(.62,.62),'control');text(a,.5,.22,"Locate via directory first, then confirm availability and fetch",12,ha='center');save(f,'cache-directory')
        f,a=canvas(4.5)
        for i in range(64):
            x=.04+i%16*.059;y=.72-i//16*.14;box(a,x,y,.05,.10,str(i+1),'orange' if i==63 else 'green',11)
        text(a,.5,.94,"Load 64 pages, first 63 reusable consecutively",14,ha='center');text(a,.5,.10,"Green: 1008 tokens; orange: 16 tokens still pending",11,ha='center');save(f,'12-cache')
        d=data['new-route']
        for i,(queue,segs,compute) in enumerate(zip(d['queues_ms'],d['retrieval_segments_ms'],d['compute_ms'])):
            f,a=plot(3.0,left=.17);a.barh(0,queue,height=.45,color=COL['gray']);ready=0
            for dur,c in zip(segs,['gray','orange','blue']):a.barh(1,dur,left=ready,height=.45,color=COL[c],edgecolor=COL['line']);ready+=dur
            a.barh(0,compute,left=max(queue,ready),height=.45,color=COL['green']);a.set(yticks=[0,1],yticklabels=['GPU',"Fetch"],xlim=(0,950),xlabel="Time since request arrival (ms)");a.invert_yaxis();save(f,'13-route' if i==0 else f'route-{i}')
        d=data['new-migration'];f,a=plot(3.7);t=np.linspace(0,8,321);src=d['initial_GB']+d['growth_GBs']*t;a.plot(t,src,color='#a56c28',label="Source-side state")
        for B,c,label in zip(d['copy_GBs'],['#388768','#267398'],["copied: 25 GB/s NIC","Copied: 50 GbE"]):a.plot(t,np.minimum(B*t,src),color=c,label=label)
        a.set(xlabel="Background copy time (s)",ylabel="Cumulative state (GB)",xlim=(0,8),ylim=(0,48));a.legend(frameon=False,loc='lower right');save(f,'14-migration')
        f,a=canvas(4.8)
        for row,title in enumerate(["Reliably recorded sequence","KV saved before failure","Resume generation after recovery"]):
            y=.68-row*.27;text(a,.04,y+.20,title,13);box(a,.04,y,.36,.13,"Input 8192 tokens",'blue',11)
            if row!=1:box(a,.43,y,.32,.13,"Output 1–1024",'green',11);box(a,.78,y,.19,.13,"output 1025",'orange',11)
            else:text(a,.68,y+.065,"Generated portion not yet saved",11,ha='center')
        text(a,.5,.03,"Recompute 1024 tokens → KV to 9216 → process output 1025",11,ha='center');save(f,'15-recovery')
        for pooled,name in [(False,'16-composition'),(True,'composition-pool')]:
            f,a=canvas(3.6);nodes=['P',"shared pool",'D'] if pooled else ['P','D'];xs=[.04,.40,.76] if pooled else [.04,.76]
            for x,n in zip(xs,nodes):box(a,x,.39,.20,.22,n,'orange' if n=='共享池' else 'blue')
            for x1,x2 in zip(xs,xs[1:]):arrow(a,(x1+.20,.5),(x2,.5));text(a,(x1+.20+x2)/2,.71,'1.125 GiB',11,ha='center')
            text(a,.5,.18,"D reads only after full write and notify" if pooled else "P hands full state directly to D",12,ha='center');save(f,name)
        d=data['9-17'];f,a=plot(4.8,bottom=.36)
        for (key,q),c,label in zip(d['queues'].items(),['#388768','#267398','#a56c28'],["direct PD","ideal chunked co-location","unchunked co-location"]):a.plot(d['time_s'],q,color=c,label=f'{label} {key} req/s')
        a.axvline(10,ls='--',color='#777777');a.axvline(60,ls=':',color='#a95159');a.set(xlabel="Time since startup (s)",ylabel="backlog request count",xlim=(0,80),ylim=(0,70));a.legend(frameon=False,loc='upper center',bbox_to_anchor=(.42,-.2));save(f,'17-service')
    from v41_case_figures import draw as draw_v41
    draw_v41(9, out)
    out.finish();return out.outputs,out.checks
