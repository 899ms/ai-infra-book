"""Chapter six: follow ownership, then messages, then elapsed time."""
import numpy as np
import matplotlib.pyplot as plt
from figure_style import COL, STYLE, canvas, plot, text, box, arrow, Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,n): out.save(f,'figure-6-'+n)
    with plt.rc_context(STYLE):
        f,a=canvas(4.4)
        for row,group in enumerate([1,4,8]):
            y=.73-row*.29;text(a,.02,y+.19,f'per instance {group} cards',12)
            for start in range(0,8,group):
                box(a,.03+start*.118,y,.118*group-.012,.13,'','gray')
                for i in range(start,start+group):box(a,.04+i*.118,y+.025,.09,.08,str(i),'blue',11)
        save(f,'1-placement')
        f,a=plot(3.6,left=.24);left=np.zeros(2)
        for i,label,col in [(0,"weights",'blue'),(1,'KV','green'),(2,"workspace",'orange')]:
            v=np.array(data['capacity_plot']['segments_GB'])[:,i];a.barh([0,1],v,left=left,height=.45,label=label,color=COL[col],edgecolor=COL['line']);left+=v
        a.axvline(80,ls='--',color='#777777');a.text(84,.5,'H100：80 GB',fontsize=11,va='center');[a.text(max(t+6,86),j,f'{t:.1f} GB' if t>100 else f'{t:.2f} GB',va='center',fontsize=11) for j,t in enumerate(left)];a.set(yticks=[0,1],yticklabels=["single-card instance","each card of eight"],xlim=(0,560),xlabel="memory footprint per GPU (GB)");a.invert_yaxis();f.subplots_adjust(top=.84);a.legend(frameon=False,ncol=3,loc='lower center',bbox_to_anchor=(.5,1.0));save(f,'2-capacity')
        dm=data['continuous_execution']['dense_moe']['models'];names=['Qwen3-32B','Qwen3-30B-A3B','Qwen3.6-35B-A3B']
        f,axs=plt.subplots(1,2,figsize=(420/72,3.6));f.subplots_adjust(left=.12,right=.98,bottom=.12,top=.80,wspace=.45)
        a=axs[0];ctx=['32768','131072','262144'];x=np.arange(3)
        for i,(m,col) in enumerate(zip(dm,['blue','orange','green'])):
            vals=[m['state_per_request'][c]/1e9 if (c!='262144' or m['model']=='qwen3.6-35b-a3b') else np.nan for c in ctx]
            a.bar(x+(i-1)*.27,vals,width=.27,color=COL[col],edgecolor=COL['line'],label=names[i])
        a.set(xticks=x,xticklabels=['32K','128K','256K'],ylabel="state per request (GB)",ylim=(0,40));a.set_title("context and state",fontsize=11)
        f.legend(*a.get_legend_handles_labels(),frameon=False,ncol=3,loc='upper center',bbox_to_anchor=(.5,1.0),fontsize=11,handlelength=1,columnspacing=.8)
        a=axs[1];w=np.array([m['b64_weight_read_s']*1e3 for m in dm]);st=np.array([m['b64_state_read_s']*1e3 for m in dm])
        a.bar(range(3),w,color=COL['gray'],edgecolor=COL['line'],label="weights");a.bar(range(3),st,bottom=w,color=COL['purple'],edgecolor=COL['line'],label="state")
        for j in range(3):a.text(j,w[j]+st[j]+4,f'{w[j]+st[j]:.0f}',ha='center',fontsize=11)
        a.legend(frameon=False,loc='upper right',fontsize=11,handlelength=1)
        a.set(xticks=range(3),xticklabels=['32B','30B-A3B','3.6-35B'],ylabel="read time (ms)",ylim=(0,210));a.set_title('batch 64、32K',fontsize=11)
        save(f,'dense-moe')
        for rows,name in [(False,'tp-columns'),(True,'tp-rows')]:
            f,a=canvas(4.4);text(a,.04,.94,"same multiplication: [2, 3] × [[1, 4], [2, 5]]",12)
            for i in range(2):
                x=.04+i*.50;box(a,x,.37,.42,.43,'','green' if i else 'blue');text(a,x+.21,.72,f'card {i}',14,ha='center')
                expr=([ '2 × [1, 4]','3 × [2, 5]'] if rows else ['[2, 3] × [1, 2] T','[2, 3] × [4, 5] T'])[i]
                text(a,x+.21,.59,expr,12,ha='center');text(a,x+.21,.45,(['[2, 8]','[6, 15]'] if rows else ['8','23'])[i],14,ha='center');arrow(a,(x+.21,.37),(.50,.24))
            box(a,.16,.06,.68,.17,"elementwise sum → [8, 23]" if rows else "side-by-side concat → [8, 23]",'orange');save(f,name)
        f,a=canvas(5.1);box(a,.29,.82,.42,.12,"full input X: m × h",'gray')
        for i in range(2):
            x=.04+.50*i;arrow(a,(.5,.82),(x+.21,.70));box(a,x,.52,.42,.18,f'up-projection → SiLU and multiply\nZ{i}：m × (f/2)','blue' if i==0 else 'green',11);arrow(a,(x+.21,.52),(x+.21,.41));box(a,x,.26,.42,.15,f'down-projection partial sum\nm × h','blue' if i==0 else 'green',11);arrow(a,(x+.21,.26),(.5,.15))
        box(a,.23,.02,.54,.13,"sum → full output m × h",'orange');save(f,'3-tp')
        f,a=plot(3.8,left=.18)
        for stage in range(4):
            for batch in range(4):
                a.barh(stage,1,left=stage+batch,height=.72,color=COL[['blue','green','orange','purple'][batch]],edgecolor=COL['line']);a.text(stage+batch+.5,stage,str(batch),ha='center',va='center',fontsize=12)
        a.set(yticks=range(4),yticklabels=[f'Stage {i}' for i in range(4)],xticks=range(8),xlim=(0,7),xlabel="time (ms); cell shows micro-batch index");a.invert_yaxis();save(f,'4-pipeline')
        f,a=canvas(4.7);box(a,.04,.72,.30,.18,"card 0: input A",'blue');box(a,.65,.72,.31,.18,"card 3: input A",'blue');arrow(a,(.34,.81),(.65,.81));text(a,.5,.94,"dispatch input",12,ha='center')
        for x,label in [(.04,"expert 1 → y1"),(.65,"expert 6 → y6")]:
            arrow(a,(x+.15,.72),(x+.15,.56));box(a,x,.39,.31,.17,label,'green');arrow(a,(x+.15,.39),(.5,.20))
        box(a,.12,.04,.76,.16,"card 0: merge by routing weight a1 y1 + a6 y6",'orange',11);save(f,'5-dispatch')
        for reduction,name in [(False,'6-ep-layout'),(True,'ep-reduction')]:
            f,a=canvas(5.6);text(a,.5,.95,"expert contribution: sum within row, then within column" if reduction else "each row assigned an expert group, KV duplicated within column",14,ha='center')
            for row in range(4):
                y=.68-row*.18;text(a,.02,y+.055,f'Group {row}',11)
                for col in range(2):
                    x=.18+col*.43;label=f'card {2*row+col}\n'+(f'group contribution {row+1}' if reduction else f'KV head {"0、1" if col==0 else "2、3"}')
                    box(a,x,y,.30,.13,label,'blue' if col==0 else 'green',11)
                    if reduction and row<3:arrow(a,(x+.15,y),(x+.15,y-.05))
                if reduction:arrow(a,(.48,y+.065),(.61,y+.065))
            text(a,.5,.06,"each column gets complete output: 1 + 2 + 3 + 4 = 10" if reduction else "expert intermediate dim per row: left 768, right 768",11,ha='center');save(f,name)
        f,a=plot(3.4,left=.28);vals=data['expert_reuse']['balanced_vs_concentrated']['weight_read_bytes'];a.barh([0,1],np.array(vals)/2**20,height=.45,color=[COL['blue'],COL['orange']],edgecolor=COL['line']);a.set(yticks=[0,1],yticklabels=["select 128 experts","select 8 experts"],xlim=(0,5000),xlabel="expert weights read per batch (MiB)");a.invert_yaxis();save(f,'7-reuse')
        for i,vals in enumerate(data['expert_load']['tasks']):
            f,a=plot(3.4);a.bar(range(4),vals,color=COL['blue'],edgecolor=COL['line']);a.set(xticks=range(4),xticklabels=[f'Group {j}' for j in range(4)],ylim=(0,580),ylabel="token-expert computation count")
            for j,v in enumerate(vals):a.text(j,v+12,str(v),ha='center',fontsize=12)
            save(f,'8-expert-load' if i==0 else f'expert-load-{i}')
        f,a=canvas(4.3);text(a,.04,.94,"along 0 → 1 → 2 → 3, accumulate block 0 contribution",13)
        for i,v in enumerate([1,11,111,1111]):
            x=.025+i*.25;box(a,x,.47,.20,.23,f'card {i}\n{v}','green' if i==3 else 'blue');text(a,x+.10,.34,"start" if i==0 else f'plus {10**i}',12,ha='center')
            if i<3:arrow(a,(x+.20,.585),(x+.25,.585))
        text(a,.5,.13,"after 3 rounds, card 3 holds full sum of block 0",13,ha='center');save(f,'9-ring-rounds')
        f,a=canvas(5.0);text(a,.04,.94,"AllGather: forward one block to next card per round",14)
        for r in range(4):
            y=.72-r*.20;text(a,.02,y+.06,"start" if r==0 else f'{r} rounds',11)
            for card in range(4):
                owned=[(card+1-j)%4 for j in range(r+1)];box(a,.16+card*.21,y,.19,.13,','.join(map(str,owned)),'green' if r==3 else 'blue',11)
                if r==0:text(a,.255+card*.21,y+.20,f'card {card}',12,ha='center')
        text(a,.5,.03,"cell shows reduced block index",11,ha='center');save(f,'ring-gather')
        f,a=plot(3.9,left=.19);left=np.zeros(4)
        for key,label,col in [('local_s',"local",'blue'),('communication_s',"reduction",'orange')]:
            v=np.array([x[key]*1000 for x in data['continuous_execution']['first_steps']]);a.barh(range(4),v,left=left,height=.5,color=COL[col],edgecolor=COL['line'],label=label);left+=v
        a.set(yticks=range(4),yticklabels=['TP 1','TP 2','TP 4','TP 8'],xlim=(0,32),xlabel="time per decode (ms)");a.invert_yaxis();a.legend(ncol=2,frameon=False);save(f,'10-tp-time')
        d=data['collectives'];f,a=plot(3.7)
        for key,label,c in [('ring_seconds',"ring",'#267398'),('tree_seconds',"binomial tree",'#a56c28')]:a.loglog(d['message_bytes'],np.array(d[key])*1e6,label=label,color=c)
        a.set(xlabel="input size per GPU (bytes)",ylabel="communication time (μs)");a.legend(frameon=False);save(f,'11-collectives')
        d=data['concurrency']['measured_ms']
        for concurrent,name in [(False,'12-resources'),(True,'resources-concurrent')]:
            f,a=plot(3.5,left=.24)
            comm=d['shared_comm' if concurrent else 'independent_comm'];comp=d['shared_compute' if concurrent else 'independent_compute']
            for i in range(2):
                a.barh(i-.16,comm[i],height=.28,color=COL['orange'],edgecolor=COL['line']);a.barh(i+.16,comp[i],height=.28,color=COL['blue'],edgecolor=COL['line'])
                a.text(comm[i]+.6,i-.16,f'{comm[i]+1e-9:.2f}',va='center',fontsize=11);a.text(comp[i]+.6,i+.16,f'{comp[i]+1e-9:.2f}',va='center',fontsize=11)
            from matplotlib.patches import Patch
            a.legend(handles=[Patch(facecolor=COL[c],edgecolor=COL['line'],label=l) for c,l in [('orange',"communication"),('blue',"matrix multiply")]],frameon=False,loc='lower right')
            a.set(yticks=[0,1],yticklabels=['4 MiB','64 MiB'],xlim=(0,56),xlabel="time after simultaneous start (ms)" if concurrent else "time running alone (ms)");a.invert_yaxis();save(f,name)
        f,a=canvas(4.6)
        for row,(down,up) in enumerate([(32,32),(48,16)]):
            y=.62-row*.43;text(a,.04,y+.26,f'{down} downlink + {up} uplink = 64 ports',13)
            for i in range(64):box(a,.045+(i%32)*.0292,y+(1-i//32)*.075,.022,.055,'','blue' if i<down else 'orange')
            text(a,.5,y-.075,f'downlink {down*25} GB/s → uplink {up*25} GB/s',12,ha='center')
        save(f,'13-ports')
        patterns=data['physical_paths']['collective_patterns']
        for i,p in enumerate(patterns):
            f,a=canvas(4.8);angles=np.linspace(np.pi/2,np.pi/2-2*np.pi,16,endpoint=False);coords=np.array([[.5+.34*np.cos(t),.49+.35*np.sin(t)] for t in angles]);a.plot(*np.vstack([coords,coords[:1]]).T,color='#999999')
            for j,(x,y) in enumerate(coords):a.plot(x,y,'o',color='#267398',ms=4);text(a,.5+(x-.5)*1.17,.49+(y-.49)*1.17,str(j),11,ha='center')
            route=p['rounds'][2]['routes'][0]
            for u,v in route['path']:arrow(a,coords[u],coords[v])
            text(a,.5,.96,("recursion" if i==0 else 'Swing')+f': round 3, 0 → {route["receiver"]}',14,ha='center');save(f,'14-topology' if i==0 else 'topology-swing')
        f,a=plot(3.5)
        for i,p in enumerate(patterns):a.bar(np.arange(3)+(i-.5)*.32,[r['peak_link_bytes']/2**20 for r in p['rounds'][:3]],width=.32,color=COL['blue' if i==0 else 'orange'],edgecolor=COL['line'],label="recursion" if i==0 else 'Swing')
        a.set(xticks=range(3),xticklabels=["Round 1","Round 2","Round 3"],ylim=(0,5),ylabel="busiest unidirectional link traffic (MiB)");f.subplots_adjust(top=.84);a.legend(frameon=False,ncol=2,loc='upper center',bbox_to_anchor=(.45,1.17),columnspacing=1.5,handlelength=1.4);save(f,'topology-load')
        f,a=canvas(4.2);box(a,.04,.36,.32,.33,"left half",'blue');box(a,.64,.36,.32,.33,"right half",'green');arrow(a,(.36,.52),(.64,.52));text(a,.5,.76,"middle cut: k² links",12,ha='center');a.plot([.20,.20,.80,.80],[.36,.18,.18,.36],color='#454545');text(a,.5,.07,"head-tail link, cut again: k² more",12,ha='center');save(f,'15-torus')
        f,a=plot(3.4)
        for shift,vals,label,col in [(-.17,[1,8],"accelerator count",'blue'),(.17,[1,4],"bisection link count",'orange')]:a.bar(np.arange(2)+shift,vals,width=.32,label=label,color=COL[col],edgecolor=COL['line'])
        a.set(xticks=[0,1],xticklabels=['k = 4','k = 8'],ylim=(0,10),ylabel="multiple relative to k = 4");a.legend(frameon=False);save(f,'torus-growth')
        f,a=canvas(5.4)
        for row,(title,left,middle,right) in enumerate([('GB200 NVL72',"compute tray","NVLink\nswitch","compute tray"),('TPU v4',"64-chip\nelectrical interconnect unit","optical circuit\nswitch","64-chip\nelectrical interconnect unit"),('Unified Bus',"host and\ncompute resources","UB\ninterconnect","host and\nmemory resources")]):
            y=.65-row*.29;text(a,.03,y+.23,title,14)
            for x,label,col in [(.03,left,'blue'),(.38,middle,'gray'),(.73,right,'green')]:box(a,x,y,.24,.17,label,col,11)
            arrow(a,(.27,y+.085),(.38,y+.085));arrow(a,(.62,y+.085),(.73,y+.085))
        save(f,'16-systems')
        for after,name in [(False,'17-pool-placement'),(True,'pool-after')]:
            f,a=plot(3.8)
            for i,v in enumerate([80,60,40,40]):a.bar(i,v,color=COL[['blue','green','orange','purple'][i]],edgecolor=COL['line'],width=.6)
            if after:a.bar(1,20,bottom=60,color=COL['blue'],edgecolor=COL['line'],width=.6);a.text(1,70,'20',ha='center',va='center',fontsize=12)
            else:a.text(.05,95,"Task 0 needs 20 GB more, unallocated",fontsize=12)
            a.axhline(80,ls='--',color='#777777');a.set(xticks=range(4),xticklabels=[f'node {i}' for i in range(4)],ylim=(0,105),ylabel="physical memory used (GB)");save(f,name)
        f,a=canvas(4.6);text(a,.04,.94,"in-flight request: sent, result pending",13)
        for i in range(4):
            y=.70-i*.15;box(a,.04,y,.21,.10,f'request {i}','blue',11);arrow(a,(.25,y+.05),(.72,y+.05));box(a,.73,y,.23,.10,"256 bytes",'green',11)
        text(a,.5,.09,"round trip 7.52 μs; up to 128 concurrent in-flight requests",12,ha='center');save(f,'18-read-window')
        d=data['remote_memory'];f,a=plot(3.7);a.loglog(d['frequency_per_second'],d['mean_payload_GBs'],color='#267398',label="20 GB × read frequency");a.axhline(d['path_GBs'],color='#a56c28',label="Path: 50 GB/s");a.axhline(d['window_bound_GBs'],ls='--',color='#388768',label="In-flight window: 4.36 GB/s");a.set(xlabel="full reads per second",ylabel="Average bandwidth requirement (GB/s)");a.legend(frameon=False,loc='upper left');save(f,'19-memory-pool')
        cands=data['continuous_execution']['candidates'];cap=data['continuous_execution']['capacity']
        f,a=plot(3.6,left=.20);left=np.zeros(4)
        for key,label,col in [('weights',"weights",'blue'),('kv','KV','green'),('workspace',"workspace",'orange')]:
            v=np.array([cap[str(c['tp'])][key]*(c['sessions_per_instance'] if key=='kv' else 1)/1e9 for c in cands]);a.barh(range(4),v,left=left,height=.5,color=COL[col],edgecolor=COL['line'],label=label);left+=v
        for j,t in enumerate(left):a.text(t+1.5,j,f'{t:.2f}',va='center',fontsize=11)
        a.axvline(80,ls='--',color='#777777');a.set(yticks=range(4),yticklabels=['TP 1 × 8','TP 2 × 4','TP 4 × 2','TP 8 × 1'],xlim=(0,118),xlabel="memory requirement per GPU (GB)");a.invert_yaxis();f.subplots_adjust(top=.84);a.legend(ncol=3,frameon=False,loc='lower center',bbox_to_anchor=(.5,1.0));save(f,'session-capacity')
        for i,c in enumerate(cands):
            if not c['capacity_fits']:continue
            f,a=plot(3.6,left=.20);instances=c['instances'];service=c['service_ms'];shown=min(instances,4)
            for req in range(4):
                lane=req%instances;start=req//instances*service;a.barh(lane,service,left=start,height=.52,color=COL[['blue','green','orange','purple'][req]],edgecolor=COL['line']);a.text(start+service/2,lane,f'Session {req}',fontsize=11,ha='center',va='center')
            a.axvline(130,ls='--',color='#777777');a.set(yticks=range(shown),yticklabels=[f'Instance {j}' for j in range(shown)],xlim=(0,180),ylim=(-.6,shown-.4),xlabel="time since 4 sessions arrived (ms)");a.invert_yaxis();save(f,f'session-tp{c["tp"]}')
        for phase,name in [('healthy','21-scale-cost'),('fault','scale-cost-fault')]:
            f,a=plot(3.8)
            for c,col in zip(data['deadline_curves'][phase],['#267398','#388768','#a56c28','#86649b']):
                if c['capacity_fits']:a.step(c['deadlines_ms'],[np.nan if v is None else v for v in c['cost_per_valid']],where='post',label=f'TP{c["tp"]}',color=col)
            a.axvline(130,ls='--',color='#777777');a.set(xlim=(80,240),ylim=(0,.8),xlabel="deadline (ms)",ylabel="GPU·s per on-time session");a.legend(ncol=3,frameon=False);save(f,name)
        # 6.7.4: V4.1 Flash decode throughput per card against supernode size, and the token time once weights leave HBM.
        import json
        from pathlib import Path
        si=json.loads((Path(here).parents[1]/'calculations/results/supernode-inference-book.json').read_text())
        rows=si['results'];rdma=si['rdma']
        f,a=plot(3.7,left=.17);f.subplots_adjust(top=.84)
        a.plot(range(4),[r['tokens_per_s_per_gpu']/1e3 for r in rows],marker='o',color='#267398',label="instance within one supernode")
        a.plot([1],[rdma['tokens_per_s_per_gpu']/1e3],marker='s',linestyle='none',color='#a56c28',label="64-card instance across eight servers")
        for i,r in enumerate(rows[:2]):a.annotate(f"per card {r['sessions']} sessions",(i,r['tokens_per_s_per_gpu']/1e3),xytext=(8,-14 if i==0 else 6),textcoords='offset points',fontsize=11)
        a.set(xticks=range(4),xticklabels=['8','64','128','256'],xlabel="cards per supernode",ylabel="Decode throughput per card (thousand token/s)",ylim=(0,24))
        a.legend(frameon=False,ncol=2,loc='lower center',bbox_to_anchor=(.5,1.0));a.grid(axis='y',alpha=.15);save(f,'supernode-inference')
        # Three placements of weights and KV: shared HBM, ROM + HBM, ROM + on-chip SRAM.
        f,a=canvas(3.9)
        cols=[("GPU supernode",.03,.22,[("HBM\nweights + KV",'blue',.34)]),("ROM wafer + HBM",.29,.33,[("ROM\nweights",'gray',.34),('HBM\nKV','green',.34)]),("ROM wafer + SRAM",.66,.33,[("ROM\nweights",'gray',.34),("on-chip SRAM\nKV",'green',.18)])]
        for title,x,w,stores in cols:
            text(a,x+w/2,.95,title,13,ha='center')
            box(a,x+w/2-.08,.64,.16,.15,"compute",'orange')
            n=len(stores);sw=(w-.03*(n-1))/n
            for j,(label,col,h) in enumerate(stores):
                sx=x+j*(sw+.03);box(a,sx,.48-h,sw,h,label,col,11);arrow(a,(sx+sw/2,.48),(x+w/2,.64))
        text(a,.5,.03,"arrow: data read each step; box height shows capacity",11,ha='center')
        save(f,'weight-placement')
        # Where the Engram tables live: host memory, sharded HBM, or mask ROM; the lookup address is known before layer 0.
        f,a=canvas(4.2)
        box(a,.05,.86,.90,.11,"token sequence → hash → 48-row address per token, fixed before layer 0",'gray',11)
        cols=[("host memory",.05,"DDR\ntwo tables 203 GB",'gray',.26,"PCIe/RDMA round trip"),("HBM per card in supernode",.375,"HBM shard\n203 GB/s per card",'green',.18,"NVLink switch round"),("mask ROM",.70,"ROM\n~half wafer",'gray',.34,"on-chip read")]
        for title,x,label,col,h,path in cols:
            w=.25
            text(a,x+w/2,.78,title,12,ha='center')
            box(a,x+.03,.55,w-.06,.12,"layer 1 Engram",'orange',11)
            box(a,x,.46-h,w,h,label,col,11)
            arrow(a,(x+.05,.46),(x+.05,.55));text(a,x+.085,.505,path,11)
        save(f,'engram-placement')
        bars=[si['gpu_row'],si['rom']['rows'][2],si['rom']['rows'][0]];labels=["8× H100\nweights in HBM","58× B200\nweights in HBM","2 ROM wafers\nweights in ROM"]
        f,a=plot(3.5,left=.26);f.subplots_adjust(top=.84)
        for j,(seg,col,name) in enumerate([('storage_compute_s','blue',"storage and compute"),('link_s','orange',"collective communication"),('fixed_s','gray',"fixed latency")]):
            left=np.array([sum(b[k] for k in ['storage_compute_s','link_s','fixed_s'][:j]) for b in bars])*1e6
            a.barh(range(3),[b[seg]*1e6 for b in bars],left=left,height=.55,color=COL[col],edgecolor=COL['line'],label=name)
        for i,b in enumerate(bars):a.text(b['token_s']*1e6+60,i,f"{b['per_user_tokens_s']:,.0f} token/s",va='center',fontsize=11)
        a.set(yticks=range(3),yticklabels=labels,xlim=(0,3900),xlabel="time per token per user (μs)");a.invert_yaxis()
        a.legend(frameon=False,ncol=3,loc='lower center',bbox_to_anchor=(.5,1.0));save(f,'rom-token-time')
    out.finish();return out.outputs,out.checks
