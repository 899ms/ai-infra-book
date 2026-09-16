"""Physical resources and finite buffers at final book dimensions."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data,teaching):
    out=Exporter(here)
    def save(f,n):out.save(f,'figure-4-'+n)
    with plt.rc_context(STYLE):
        f,a=canvas(4.7)
        for row,m in enumerate([1,256]):
            y=.58-row*.44;text(a,.04,y+.30,f'{m}rows share 32 MiB weights',14)
            box(a,.34,y+.04,.32,.20,"weight W",'orange')
            for j in range(1 if m==1 else 4):
                yy=y+.12+(j-1.5)*.06 if m>1 else y+.12
                box(a,.04,yy,.17,.045,'','blue');box(a,.80,yy,.16,.045,'','green');arrow(a,(.21,yy+.023),(.34,y+.14));arrow(a,(.66,y+.14),(.80,yy+.023))
            text(a,.50,y-.07,"Per-row amortized:"+('32 MiB' if m==1 else '128 KiB'),12,ha='center')
        save(f,'1-reuse')
        f,a=canvas(4.9);box(a,.04,.79,.36,.14,"host CPU",'gray');box(a,.60,.79,.36,.14,"off-chip memory",'blue')
        box(a,.03,.06,.94,.60,'','gray');text(a,.06,.62,"inside accelerator chip",14)
        box(a,.10,.41,.80,.12,"shared cache and data movement",'blue');arrow(a,(.78,.79),(.68,.53));arrow(a,(.22,.79),(.24,.53),'control')
        box(a,.10,.16,.24,.14,"local buffer",'green');box(a,.41,.16,.24,.14,"matrix unit",'orange');box(a,.72,.16,.19,.14,"accumulator storage",'purple',11)
        arrow(a,(.25,.41),(.22,.30));arrow(a,(.34,.23),(.41,.23));arrow(a,(.65,.23),(.72,.23));save(f,'2-components')
        f,a=canvas(3.9);text(a,.04,.94,"small array reuses inputs and weights repeatedly",14)
        for i in range(3):
            text(a,.12,.67-i*.18,f'A{i}',12,ha='center')
            for j in range(3):
                x=.30+j*.22;y=.59-i*.18;box(a,x,y,.16,.14,"multiply-add",'green',11)
                arrow(a,(.18 if j==0 else x-.06,y+.07),(x,y+.07))
                if i==0:text(a,x+.08,.84,f'W{j}',12,ha='center')
                arrow(a,(x+.08,.79 if i==0 else y+.18),(x+.08,y+.14))
        text(a,.5,.08,"each MAC unit retains partial sum, accumulates next input pair",11,ha='center');save(f,'matrix-array')
        f,a=canvas(4.0);text(a,.04,.94,"each block fixed at 16 rows, gray rows also execute",14)
        for x,count,label in [(.08,2,"2 rows per expert"),(.57,16,"64 rows per expert\ncomposed of 4 blocks")]:
            for i in range(16):a.add_patch(Rectangle((x,.74-i*.034),.30,.029,facecolor=COL['green'] if i<count else COL['gray'],edgecolor=COL['line'],lw=.3))
            text(a,x+.15,.10,label,12,ha='center')
        save(f,'3-expert-rows')
        f,a=plot(3.2,left=.28)
        a.barh([0,1],[512,512],color=COL['green'],label="valid rows");a.barh([0,1],[3584,0],left=[512,512],color=COL['gray'],edgecolor=COL['line'],label="zero-padded row")
        a.set(yticks=[0,1],yticklabels=["256 experts","8 experts"],xlim=(0,4500),ylim=(-.7,1.7),xlabel="matrix rows executed (incl. zero-padding)");a.invert_yaxis();a.legend(frameon=False);save(f,'expert-padding-total')
        vals=np.array(data['4-4']['service_cycles'])
        f,a=plot(4.0,left=.27)
        for i,(label,c) in enumerate([("matrix",'orange'),("shared memory",'blue'),("exponent",'green')]):a.barh(np.arange(4)+(i-1)*.22,vals[:,i],height=.20,color=COL[c],edgecolor=COL['line'],label=label)
        a.set(yticks=range(4),yticklabels=["original config","matrix ×2","matrix and exponent ×2","three terms ×2"],xlabel="single compute group time (cycles)",xlim=(0,1150),ylim=(-1.1,3.6));a.invert_yaxis();a.legend(ncol=3,loc='upper center',frameon=False,fontsize=11);save(f,'4-attention')
        f,a=canvas(4.3)
        for y,title,stages in [(.58,"upcast to high precision first",[("compressed 8.5 MiB",'blue'),("expanded 32 MiB",'orange'),("BF16 compute",'green')]),(.12,"compute in low-precision path",[("compressed 8.5 MiB",'blue'),("low-precision compute",'orange'),("scaling and merging",'green')])]:
            text(a,.04,y+.29,title,14)
            for i,(label,c) in enumerate(stages):
                x=.03+i*.335;box(a,x,y,.27,.20,label,c,11)
                if i<2:arrow(a,(x+.27,y+.10),(x+.335,y+.10))
        save(f,'5-precision')
        d=data['4-6'];f,a=plot(3.8,left=.28,bottom=.25)
        for y,row in enumerate(d['cases']):
            left=0
            for n,c,label in [(d['weight_bytes'],'blue',"weights"),(d['workspace_bytes'],'orange',"workspace"),(row['requests']*row['context_multiplier']*d['kv_bytes_per_request'],'green','KV')]:
                a.barh(y,n/1e9,left=left,height=.5,color=COL[c],edgecolor=COL['line'],label=label if y==0 else None);left+=n/1e9
        a.axvline(24,ls='--',color='#555555');a.set(yticks=range(3),yticklabels=["8K token × 4 requests","8K token × 5 requests","16K token × 2 requests"],xlim=(0,27),xlabel="RTX 4090 memory usage (GB)");a.invert_yaxis();a.legend(ncol=3,loc='upper center',bbox_to_anchor=(.5,-.22),frameon=False);save(f,'6-capacity')
        f,a=canvas(3.3);text(a,.04,.92,"in-flight accesses occupy request slots",14)
        for i in range(4):box(a,.05+i*.235,.49,.20,.18,f'request {i+1}','blue',11)
        text(a,.5,.31,"128 bytes per request, returns 500 ns after issue",12,ha='center')
        text(a,.5,.12,"sustained bandwidth also depends on concurrent requests",12,ha='center');save(f,'memory-inflight')
        d=data['4-7'];f,a=plot(3.7)
        for b,ys,c in zip(['RTX 4090：1008 GB/s','RTX 5090：1792 GB/s'],d['bandwidth_upper_bytes_per_second'],['#267398','#388768']):a.plot(d['requests'],np.array(ys)/1e12,label=b,color=c)
        a.set(xlim=(0,10000),ylim=(0,2.4),xlabel="concurrent outstanding requests",ylabel="Bandwidth upper bound (TB/s)");a.legend(frameon=False);save(f,'7-memory')
        f,a=plot(3.4,left=.21)
        for i in range(4):a.barh(i,8192,color=COL['gray'],edgecolor=COL['line'],height=.5);a.barh(i,256,color=COL['blue'],height=.5)
        a.set(yticks=range(4),yticklabels=["row 0","row 1","row 2","row 127"],xlim=(0,8500),xlabel="byte offset from row start",xticks=[0,4096,8192]);a.invert_yaxis();a.annotate("actual read 256 bytes",(128,0),xytext=(2000,.65),arrowprops={'arrowstyle':'->'},fontsize=12);save(f,'8-layout')
        f,a=plot(3.1,left=.16);a.barh(0,320,left=0,color=COL['gray'],height=.62,label="slot occupancy");a.barh(0,64,left=0,color=COL['blue'],height=.4);a.barh(0,128,left=192,color=COL['green'],height=.4);a.axvline(192,color='#a56c28',lw=1)
        a.set(xlim=(0,350),ylim=(-.7,.7),yticks=[],xticks=[0,64,192,320],xlabel="time (tick)")
        for x,label in [(32,"transmission"),(128,"waiting for return"),(256,"compute")]:a.text(x,.4,label,fontsize=11,ha='center')
        a.text(175,-.4,"after 320 ticks, input slot can be written again",fontsize=11,ha='center');save(f,'slot-lifetime')
        for slots,name in [(1,'9-pipeline'),(2,'pipeline-two'),(3,'pipeline-three')]:
            r=teaching['baseline'][slots-1];f,a=plot(3.5,left=.17)
            for t in r['chunks']:
                y=t['chunk'];a.barh(y,t['slot_released']-t['issue_start'],left=t['issue_start'],height=.62,color=COL['gray']);a.barh(y,t['transfer_end']-t['issue_start'],left=t['issue_start'],height=.40,color=COL['blue']);a.barh(y,t['compute_end']-t['compute_start'],left=t['compute_start'],height=.40,color=COL['green']);a.plot(t['data_ready'],y,'|',color='#a56c28',markersize=12)
            a.set(yticks=range(4),yticklabels=[f'block {i}' for i in range(4)],xlim=(0,1320),xticks=[0,320,640,960,1280],xlabel="time (tick)");a.invert_yaxis();save(f,name)
        f,a=canvas(4.0);text(a,.04,.93,"full row transfer, two groups alternate buffers",14)
        box(a,.04,.61,.26,.17,"matrix unit\ncomputes QK",'orange');box(a,.70,.61,.26,.17,"vector unit\ncomputes softmax",'green')
        box(a,.38,.66,.23,.11,"slot A",'blue');box(a,.38,.42,.23,.11,"slot B",'purple')
        arrow(a,(.30,.695),(.38,.715));arrow(a,(.61,.715),(.70,.695));arrow(a,(.17,.61),(.38,.475))
        box(a,.28,.09,.44,.16,"matrix unit computes PV\nreleases buffer when done",'orange');arrow(a,(.83,.61),(.72,.17));save(f,'matrix-vector-handoff')
        cases=teaching['die_locality']['cases']
        for move,name in [(False,'10-locality'),(True,'locality-compute')]:
            f,a=canvas(4.8);text(a,.03,.96,"compute all on die 0" if not move else "compute on die holding weights",14)
            for row,c in enumerate(cases):
                y=.56-row*.46;text(a,.03,y+.31,'HGX B200' if row==0 else "Ascend 910C",13)
                box(a,.03,y,.27,.25,"die 0\n32 GiB weights\ncompute",'blue',11)
                box(a,.70,y,.27,.25,"die 1\n32 GiB weights"+("\ncompute" if move else ''),'orange',11)
                if move:
                    arrow(a,(.30,y+.17),(.70,y+.17));arrow(a,(.70,y+.08),(.30,y+.08))
                    text(a,.50,y+.215,f"input and result 64 MiB:{c['activation_us']:.1f} μs" if c['activation_us']<100 else f"input and result 64 MiB:{c['activation_us']/1000:.2f} ms",11,ha='center')
                    text(a,.50,y-.045,f"each side reads local weights:{c['split_ms']:.1f} ms",12,ha='center')
                else:
                    arrow(a,(.70,y+.125),(.30,y+.125))
                    limit="limited by die 1 HBM" if c['link_to_hbm_ratio']>=1 else "limited by inter-die link"
                    text(a,.50,y+.20,f"cross-die read 32 GiB:{c['remote_ms']:.1f} ms",11,ha='center')
                    text(a,.50,y+.05,limit,11,ha='center')
                    text(a,.50,y-.045,f"stage read time:{c['overlapped_ms']:.1f} ms",12,ha='center')
            save(f,name)
        d=data['4-11']
        for i,name in enumerate(['11-interconnect','large-message']):
            f,a=plot(3.2);vals=np.array(d['total_us'][i]);alpha=d['alpha_seconds']*1e6;a.bar([0,1],[alpha,alpha],color=COL['orange'],edgecolor=COL['line'],label="startup");a.bar([0,1],vals-alpha,bottom=alpha,color=COL['blue'],edgecolor=COL['line'],label="transmission")
            a.set(xticks=[0,1],xticklabels=['A100 NVLink\n300 GB/s','H100 NVLink\n450 GB/s'],ylabel="transfer time (μs)",ylim=(0,max(vals)*1.45));a.legend(ncol=2,frameon=False)
            for j,v in enumerate(vals):a.text(j,v+max(vals)*.035,f'{v:.3f}',ha='center',fontsize=12)
            save(f,name)
        d=data['4-12'];f,a=plot(3.5)
        a.axhline(d['active_weight_bytes']/1e9,color='#267398',label="weights per batch");a.plot(d['batch'],np.array(d['kv_read_bytes'])/1e9,color='#388768',label="KV per request");a.axvline(13,ls=':',color='#777777')
        a.set(xlim=(1,32),ylim=(0,45),xlabel="Requests per batch",ylabel="read per step (GB)");a.legend(frameon=False);save(f,'12-specialization')
        d=data['4-13'];f,a=plot(3.6)
        for key,label,c in [('compute_us',"matrix computation",'#a56c28'),('memory_us',"off-chip read",'#267398')]:a.plot(d['rows'],d[key],label=label,color=c)
        a.axvline(179,ls=':',color='#777777');a.set(xlim=(1,256),ylim=(0,65),xlabel="token count this call M",ylabel="resource time (μs)");a.legend(frameon=False);save(f,'13-roofline')
        d=data['4-14']
        for key,name,label in [('wall_us','14-performance',"total time per call (μs)"),('dram_read_mib','performance-traffic',"DRAM read (MiB)")]:
            f,a=plot(3.5)
            vals=d[key];a.bar(range(4),vals,color=[COL['blue'],COL['green']]*2,edgecolor=COL['line']);a.set(xticks=range(4),xticklabels=["1 row\nreuse","1 row\nrotation","256 rows\nreuse","256 rows\nrotation"],ylabel=label,ylim=(0,max(vals)*1.3))
            for i,v in enumerate(vals):a.text(i,v+max(vals)*.025,'256 B' if v<.001 else f'{v:.1f}',ha='center',fontsize=11)
            save(f,name)
    from core_principles_figures import draw as draw_principles
    draw_principles(4, out)
    from energy_physics import draw as draw_energy
    data['4-energy']=draw_energy(out)
    return out.finish()
