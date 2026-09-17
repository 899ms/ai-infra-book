"""Follow a shard across servers, request slots and consumer dependencies."""
import json, math
import numpy as np
from fractions import Fraction
import matplotlib.pyplot as plt
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,n):out.save(f,'figure-7-'+n)
    with plt.rc_context(STYLE):
        # 1: two eight-GPU servers, NVSwitch inside, one NIC per GPU, rail switches between.
        f,a=canvas(5.6)
        for row in range(2):
            top=row==0
            base=.615 if top else .03
            box(a,.02,base,.96,.355,'','gray')
            text(a,.05,.945 if top else .055,f'server {"AB"[row]}',13)
            sw_y=base+.24 if top else base+.055
            gpu_y=base+.14 if top else base+.155
            nic_y=base+.04 if top else base+.255
            box(a,.05,sw_y,.90,.06,"NVSwitch: 450 GB/s per direction per card NVLink",'green',11)
            for i in range(8):
                x=.05+i*.1125
                box(a,x,gpu_y,.095,.08,str(row*8+i),'blue',11)
                box(a,x,nic_y,.095,.06,'NIC','orange',11)
                if top:arrow(a,(x+.0475,nic_y),(x+.0475,.545))
                else:arrow(a,(x+.0475,.455),(x+.0475,nic_y+.06))
        box(a,.02,.455,.96,.09,"switch network: one switch per rail, 50 GB/s per direction per NIC",'gray',11)
        save(f,'1-boundaries')
        d=data['7-2'];f,a=plot(3.6);n=np.array(d['device_multipliers']);c=np.array(d['compute_ms']);t=d['cut_ms'];a.plot(n,c+t,label="serial",color='#267398');a.plot(n,np.maximum(c,t),label="fully overlapped",color='#388768');a.plot(n,c,ls=':',label="compute",color='#a56c28');a.set(xlabel="accelerator count / baseline count",ylabel="time per step (ms)",xticks=n,ylim=(0,32));a.legend(frameon=False);save(f,'2-cut')
        for idx,order in enumerate(data['7-3']['ring_orders']):
            f,a=canvas(4.4);text(a,.04,.93,"contiguous ring: 2 of 16 edges cross servers" if idx==0 else "interleaved ring: all 16 edges cross servers",14)
            xs=[.03+i*.118 for i in range(8)];pos={}
            for i,rank in enumerate(order):
                col=i if i<8 else 15-i;y=.60 if i<8 else .28;pos[i]=(xs[col],y)
                box(a,xs[col],y,.082,.14,str(rank),'blue' if rank<8 else 'orange',12)
            for i in range(16):
                (x1,y1),(x2,y2)=pos[i],pos[(i+1)%16]
                if i<7:arrow(a,(x1+.082,y1+.07),(x2,y2+.07))
                elif i==7:arrow(a,(x1+.041,y1),(x2+.041,y2+.14))
                elif i<15:arrow(a,(x1,y1+.07),(x2+.082,y2+.07))
                else:arrow(a,(x1+.041,y1+.14),(x2+.041,y2))
            if idx==0:text(a,xs[7]+.026,.51,"cross-server",11,ha='right');text(a,xs[0]+.056,.51,"cross-server",11)
            text(a,.5,.12,"blue: server A; orange: server B",12,ha='center');save(f,'3-hierarchy' if idx==0 else 'ring-interleaved')
        f,a=canvas(5.2)
        for col in range(2):
            x=.04+.51*col;text(a,x+.20,.93,f'server {"AB"[col]}',14,ha='center');box(a,x,.64,.41,.17,"local ReduceScatter\nyields eight 24 MiB shards",'blue',11);box(a,x,.35,.41,.16,"corresponding shard cross-server\ntwo-card AllReduce, each on one rail",'orange',11);box(a,x,.06,.41,.16,"local AllGather\nyields full reduction result",'green',11);arrow(a,(x+.20,.64),(x+.20,.51));arrow(a,(x+.20,.35),(x+.20,.22))
        arrow(a,(.45,.46),(.55,.46));arrow(a,(.55,.39),(.45,.39));save(f,'hierarchy-stages')
        f,a=plot(3.6,left=.22);left=np.zeros(3)
        for k,l,c in [('local_MiB',"local",'blue'),('remote_MiB',"cross-server",'orange')]:v=data['7-3'][k];a.barh(range(3),v,left=left,color=COL[c],edgecolor=COL['line'],label=l);left+=v
        a.set(yticks=range(3),yticklabels=["contiguous ring","interleaved ring","hierarchical reduction"],xlabel="logical send volume, both directions combined (MiB)");a.invert_yaxis();f.subplots_adjust(top=.84);a.legend(frameon=False,ncol=2,loc='upper center',bbox_to_anchor=(.45,1.17),columnspacing=1.5,handlelength=1.4);save(f,'hierarchy-bytes')
        f,a=plot(3.6,left=.18)
        for stage in range(4):
            for batch in range(8):a.barh(stage,1,left=stage+batch,height=.7,color=COL[['blue','green','orange','purple'][batch%4]],edgecolor=COL['line']);a.text(stage+batch+.5,stage,str(batch),ha='center',va='center',fontsize=11)
        a.set(yticks=range(4),yticklabels=[f'Stage {i}' for i in range(4)],xlim=(0,11),xticks=[0,2,4,6,8,10,11],xlabel="time (ms); cell shows micro-batch index");a.invert_yaxis();save(f,'4-pipeline')
        for i in range(3):
            f,a=canvas(3.9);text(a,.04,.94,["concentrated on one NIC","split evenly across eight NICs","control setup: dual-port NIC sharing one PCIe slot"][i],14);box(a,.04,.42,.24,.24,'32 MiB','blue')
            if i==0:box(a,.64,.42,.30,.24,"NIC\n50 GB/s",'orange');arrow(a,(.28,.54),(.64,.54))
            elif i==1:
                for j in range(8):
                    y=.10+j*.10;box(a,.70,y,.25,.08,'4 MiB','orange',11);arrow(a,(.28,.54),(.70,y+.04))
            else:
                box(a,.36,.32,.24,.42,"PCIe Gen4\nx16 slot\n32 GB/s",'gray',11);arrow(a,(.28,.54),(.36,.54))
                for j in range(2):
                    y=.29+j*.28;box(a,.72,y,.25,.16,'16 MiB','orange',11);arrow(a,(.60,.54),(.72,y+.08))
            text(a,.5,.04,f'receive phase at least {data["7-5"]["lower_ms"][i]:.2f} ms',13,ha='center');save(f,'5-expert' if i==0 else f'expert-path-{i}')
        f,a=canvas(4.8);box(a,.03,.44,.21,.18,"source GPU",'blue');box(a,.39,.72,.27,.15,"direct 50",'green');box(a,.36,.17,.31,.19,"NVLink 450\nrelay NIC 100",'orange',11);box(a,.78,.40,.20,.25,"downstream\navailable bandwidth",'gray');arrow(a,(.24,.53),(.39,.79));arrow(a,(.24,.53),(.36,.26));arrow(a,(.66,.79),(.78,.52));arrow(a,(.67,.26),(.78,.52));text(a,.5,.05,"unit GB/s; relay limited to 100 total via borrowed NIC",12,ha='center');save(f,'6-relay')
        paths=[("host RPC",['CPU A',"NIC A","NIC B",'CPU B']),("CPU submits GPUDirect RDMA",['GPU A',"NIC A","NIC B",'GPU B']),("GPU access via NVLink",['GPU A','NVLink','GPU B']),("device-initiated URMA async access",["device A","UB interconnect","device B"])]
        for i,(title,nodes) in enumerate(paths):
            f,a=canvas(3.8);text(a,.04,.94,title,14);step=.94/len(nodes)
            for j,node in enumerate(nodes):
                x=.03+j*step;box(a,x,.36,step-.045,.18,node,'blue' if j in [0,len(nodes)-1] else 'gray',11)
                if j<len(nodes)-1:arrow(a,(x+step-.045,.45),(x+step,.45))
            if i==1:box(a,.20,.69,.28,.12,"CPU submits request",'orange',11);arrow(a,(.34,.69),(.38,.54),'control')
            else:text(a,.5,.73,"initiator submits op, receiver uses result per completion condition",11,ha='center')
            text(a,.5,.13,"solid: data; dashed: control submission",11,ha='center');save(f,'7-access' if i==0 else f'access-{i}')
        f,a=canvas(4.1)
        for i in range(2):
            y=.61-i*.43;box(a,.04,y,.31,.19,"remote snapshot",'blue');box(a,.65,y,.31,.19,"consumer" if i==0 else "local copy",'green');arrow(a,(.35,y+.095),(.65,y+.095));text(a,.5,y+.25,"read across network every use" if i==0 else "move back once, then read local copy",13,ha='center')
        save(f,'snapshot-paths')
        for i,(label,c) in enumerate(data['7-8']['cases'].items()):
            f,a=plot(3.5);r=np.arange(1,6 if i==0 else 26);a.plot(r,c['remote_per_read_ms']*r,label="remote read each time",color='#267398');a.plot(r,c['setup_ms']+c['local_per_read_ms']*r,label="move back locally first",color='#388768');a.set(xlabel="reuse count",ylabel="cumulative time (ms)");a.legend(frameon=False);save(f,'8-snapshot' if i==0 else 'snapshot-partial')
        f,a=canvas(4.0);text(a,.04,.94,"slot holds one pending request",14)
        for x,label,c in [(.03,"allocate slot",'blue'),(.37,"transfer and wait",'orange'),(.71,"process notification\nrelease slot",'green')]:box(a,x,.39,.26,.23,label,c,12)
        arrow(a,(.29,.5),(.37,.5));arrow(a,(.63,.5),(.71,.5));text(a,.5,.18,"occupancy time: allocation to release, 2 μs total",12,ha='center');save(f,'slot-lifetime')
        f,a=plot(3.5,left=.24)
        for y,(key,p) in enumerate(data['7-9']['periods'].items()):
            a.barh(y,4,height=.5,color=COL['gray'])
            for start,dur in p['segments_us']:a.barh(y,dur,left=start,height=.5,color=COL['blue'],edgecolor=COL['line'])
        a.set(yticks=[0,1],yticklabels=["128 slots","391 slots"],xlim=(0,4),xlabel="time (μs); blue is payload send");a.invert_yaxis();save(f,'9-window')
        f,a=plot(3.5);n=np.arange(1,501);a.plot(n,np.minimum(50,n*256/2000),label="path and slot limit",color='#267398');a.plot(n,np.minimum(data['7-9']['submission_cap_GBs'],n*256/2000),label="plus 18.6 ns launch interval",color='#a56c28');a.set(xlabel="active request slot count",ylabel="throughput limit (GB/s)");a.legend(frameon=False);save(f,'window-rate')
        f,a=plot(3.8,left=.23);a.barh(0,5,color=COL['blue'],height=.48);a.barh(1,12,color=COL['orange'],height=.48);a.barh(1,4,left=8,color=COL['green'],height=.48);a.axvline(6,ls=':',color='#a54b43');a.text(6.2,-.45,"6 μs advance coverage",fontsize=11);a.set(yticks=[0,1],yticklabels=["source buffer usage","destination buffer usage"],xlim=(0,14),ylim=(-.7,1.6),xlabel="time (μs); green is consumer read");a.invert_yaxis();save(f,'10-lifetime')
        f,a=canvas(4.5)
        for i in range(2):
            y=.63-i*.39;box(a,.04,y,.23,.18,f'endpoint {i}','blue');box(a,.38,y,.24,.18,"relationship binding",'orange');arrow(a,(.27,y+.09),(.38,y+.09));arrow(a,(.62,y+.09),(.77,.52))
        box(a,.77,.35,.20,.34,"target\ntransfer state",'green',11);text(a,.5,.08,"endpoint identity stored separately, target transfer state shared",12,ha='center');save(f,'11-state')
        f,a=plot(3.7,left=.26);left=np.zeros(3)
        for j,label,col in [(0,"endpoint",'blue'),(1,"binding",'orange'),(2,"transmission",'green')]:v=np.array(data['7-11']['state_MiB'])[:,j];a.barh(range(3),v,left=left,height=.5,color=COL[col],edgecolor=COL['line'],label=label);left+=v
        a.axvline(1,ls='--',color='#777777');a.set(yticks=range(3),yticklabels=["per-relationship exclusive","shared by target","eight-way isolation"],xlabel="state footprint (MiB)",xlim=(0,10));a.invert_yaxis();a.legend(frameon=False);save(f,'state-capacity')
        for i,(label,schedule) in enumerate(data['7-12']['schedules'].items()):
            f,a=plot(3.6,left=.21)
            for t in schedule['tasks']:
                lane=1 if t['id']=='independent_transfer' else 0;color={'write_data':'blue','recover_and_make_visible':'orange','publish_notification':'green','independent_transfer':'purple'}[t['id']];a.barh(lane,t['duration_ns']/1000,left=t['start_ns']/1000,height=.45,color=COL[color],edgecolor=COL['line'])
            a.set(yticks=[0,1],yticklabels=["write and publish","independent transfer"],xlim=(0,115),xlabel="Time (μs)");a.invert_yaxis();save(f,'12-ordering' if i==0 else 'ordering-independent')
        f,a=canvas(5.0)
        for row,(time,label,c) in enumerate([(1,"early read: gets old value",'orange'),(2,"producer writes new value",'blue'),(3,"ready flag visible",'green'),(4,"consumer reads ready flag",'green'),(5,"returns previously read old value",'orange'),(6,"if re-read at 4 μs, gets new value",'blue')]):
            y=.78-row*.14;text(a,.03,y+.04,f'{time} μs',11);box(a,.19,y,.76,.10,label,c,11)
        save(f,'13-stale')
        for i,(name,ops) in enumerate(data['7-14']['operations'].items()):
            f,a=plot(5,left=.17)
            for op in ops:
                y=op['operation'];start=op['submit_ns']/1000;end=op['transfer_complete_ns']/1000;done=op['completion_consumed_ns']/1000;a.barh(y,end-start,left=start,height=.65,color=COL['blue']);a.barh(y,done-end,left=end,height=.65,color=COL['orange'])
            a.set(xlim=(0,82),yticks=[0,4,8,12,15],ylabel="request ID",xlabel="time (μs)\nblue: transfer; orange: waiting for slot release");a.invert_yaxis();save(f,'14-reclaim' if i==0 else 'reclaim-more')
        for kind,n in [('arrival','15-congestion'),('queue','congestion-queue')]:
            f,a=plot(3.8)
            for (name,segs),label,c in zip(data['7-15']['periodic_segments'].items(),["overlap 20 ms","overlap 5 ms","no overlap"],['#267398','#a56c28','#388768']):
                xs=[];ys=[]
                for seg in segs:
                    xs.extend([seg['start_ns']/1e6,seg['end_ns']/1e6]);ys.extend([seg['arrival_bytes_per_second']/1e9]*2 if kind=='arrival' else [seg['queue_start_bytes']/1e6,seg['queue_end_bytes']/1e6])
                a.plot(xs,ys,label=label,color=c)
            a.set(xlabel="time (ms)",ylabel="arrival rate (GB/s)" if kind=='arrival' else "backlog (MB)",xlim=(0,100));a.legend(frameon=False);save(f,n)
        f,a=canvas(3.8);box(a,.04,.42,.24,.20,"sender\n100 GB/s",'blue');box(a,.43,.42,.24,.20,"buffer queue",'orange');box(a,.78,.42,.19,.20,"egress\n50 GB/s",'green',11);arrow(a,(.28,.52),(.43,.52));arrow(a,(.67,.52),(.78,.52));arrow(a,(.55,.42),(.17,.18),'control');text(a,.46,.12,"after feedback takes effect, send drops to 40 GB/s",12,ha='center');save(f,'feedback-loop')
        f,a=plot(3.8)
        for seg in data['7-16']['queue_segments']:a.plot([seg['start_ns']/1000,seg['end_ns']/1000],[seg['queue_start_bytes']/1024,seg['queue_end_bytes']/1024],color='#267398')
        a.axvline(20,ls='--',color='#a56c28');a.set(xlabel="Time (μs)",ylabel="queue footprint (KiB)",xlim=(0,120),ylim=(0,580));save(f,'16-feedback')
        packet_cases=dict(data['7-17']['cases'])
        loss=json.loads((here.parents[1]/'calculations/results/packet-reorder-loss.json').read_text())
        packet_cases['packet-reorder-loss']={k:loss[k] for k in ['transmissions','delivery']}
        for i,(name,c) in enumerate(packet_cases.items()):
            f,a=plot(3.7);delivery={x['sequence']:float(Fraction(x['delivery_exact_ns']))/1000 for x in c['delivery']}
            for t in c['transmissions']:
                if t['lost']:continue
                arrival=float(Fraction(t['arrival_exact_ns']))/1000;seq=t['sequence'];a.plot([arrival,delivery[seq]],[seq,seq],color='#a56c28');a.scatter(arrival,seq,color='#267398',s=22)
            a.set(xlim=(0,[1.6,10,22][i]),yticks=range(8),ylabel="packet sequence number",xlabel="arrival and delivery-to-app time (μs)");a.invert_yaxis();save(f,'17-packets' if i==0 else f'packets-{i}')
        f,a=canvas(3.6);box(a,.04,.40,.34,.25,"request 0 holds A\nwaits for B",'blue');box(a,.62,.40,.34,.25,"request 1 holds B\nwaits for A",'orange');arrow(a,(.38,.58),(.62,.58));arrow(a,(.62,.46),(.38,.46));text(a,.5,.16,"both sides need the other to release first",13,ha='center');save(f,'18-deadlock')
        f,a=canvas(3.7)
        for x,label,col in [(.03,"request resource",'blue'),(.37,"execution resource",'orange'),(.71,"independent response\nresources",'green')]:box(a,x,.42,.26,.24,label,col,12)
        arrow(a,(.29,.54),(.37,.54));arrow(a,(.63,.54),(.71,.54));text(a,.5,.18,"response has reserved path, can return and release original request",12,ha='center');save(f,'response-reserve')
        for i,(ready,ex) in enumerate([([0,0,0,2],.4),([0,0,0,2],.2),([0]*4,.4)]):
            f,a=plot(3.5,left=.18)
            for lane,t in enumerate(ready):
                a.barh(lane,t,height=.5,color=COL['gray']);a.barh(lane,max(ready)-t,left=t,height=.5,color=COL['orange']);a.barh(lane,ex,left=max(ready),height=.5,color=COL['blue']);a.scatter(t,lane,color='#252525',s=16)
            a.set(yticks=range(4),yticklabels=[f'participant {j}' for j in range(4)],xlim=(0,2.6),xlabel="time (ms); dot indicates ready");a.invert_yaxis();save(f,'19-progress' if i==0 else f'progress-{i}')
        for i,c in enumerate(data['7-20']['cases']):
            f,a=plot(2.9,left=.17);a.barh(0,20,height=.45,color=COL['gray']);a.barh(1,c['comm_ms'],left=c['ready_ms'],height=.45,color=COL['blue']);a.barh(0,2,left=c['update_start_ms'],height=.45,color=COL['green']);a.scatter(c['ready_ms'],1,color='#252525',s=16);a.set(yticks=[0,1],yticklabels=["compute/update","communication"],xlim=(0,37),xlabel="time (ms)");a.invert_yaxis();save(f,'20-step' if i==0 else f'step-{i}')
        f,a=plot(3.7);m=np.logspace(3,8,200)
        for alpha,b,label,col in [(5e-6,50e9,"original config",'#267398'),(5e-6,150e9,"3x bandwidth",'#388768'),(2e-6,50e9,"startup shortened",'#a56c28')]:a.loglog(m,(14*alpha+1.75*m/b)*1e6,label=label,color=col)
        a.set(xlabel="input per participant (bytes)",ylabel="reduction time (μs)");a.legend(frameon=False);save(f,'21-message')
        # Switch network (2026-09-11): Clos cut, rail pairing, in-network sweep, ECMP collision, incast feedback.
        f,a=canvas(4.3);text(a,.04,.95,"two-tier Clos: leaf switches connect endpoints, spine switches connect all leaf switches",13)
        spx=[.24,.56];lx=[.03+i*.245 for i in range(4)]
        for j,x in enumerate(spx):box(a,x,.70,.20,.11,f'spine switch {j}','green',11)
        for i,x in enumerate(lx):
            box(a,x,.40,.20,.11,f'leaf switch {i}','blue',11);box(a,x,.10,.20,.11,"32 endpoints",'gray',11)
            a.plot([x+.10,x+.10],[.21,.40],color=COL['line'],lw=1)
            for sx in spx:a.plot([x+.10,sx+.10],[.51,.70],color=COL['line'],lw=1)
        a.plot([.5,.5],[.06,.67],ls='--',color='#a54b43',lw=1.2);text(a,.505,.30,"bisection set",11,color='#a54b43')
        text(a,.5,.03,"64 ports: 32 downlink, 32 uplink per leaf; 64 leaves, 32 spines, 2048 endpoints total",11,ha='center');save(f,'clos-cut')
        f,a=canvas(6.2)
        from matplotlib.path import Path as MPath
        from matplotlib.patches import FancyArrowPatch
        for panel,(title,shifted) in enumerate([("aligned pairing rank i ↔ i+8: each pair stays within its own rail",False),("misaligned pairing rank i ↔ i+9: each pair switches rail via spine",True)]):
            y0=.52-panel*.50;text(a,.03,y0+.45,title,12);xs=[.03+i*.1175 for i in range(8)]
            box(a,.03,y0+.35,.94,.07,"spine switch" if not shifted else '','green',11)
            if shifted:text(a,.5,y0+.405,"spine switch",11,ha='center')
            for i,x in enumerate(xs):
                box(a,x,y0+.22,.105,.08,f'rail {i}','blue',11);box(a,x,y0+.05,.048,.07,str(i),'orange',11);box(a,x+.057,y0+.05,.048,.07,str(i+8),'purple',11)
                arrow(a,(x+.024,y0+.12),(x+.03,y0+.22))
                if shifted:
                    x2=xs[(i+1)%8];arrow(a,(x+.03,y0+.30),(x+.03,y0+.35));arrow(a,(x2+.075,y0+.35),(x2+.075,y0+.30));arrow(a,(x2+.075,y0+.22),(x2+.081,y0+.12))
                else:arrow(a,(x+.075,y0+.22),(x+.081,y0+.12))
            if shifted:
                # Two representative cross-rail paths drawn end to end: NIC i -> leaf i -> spine -> leaf i+1 -> NIC i+9.
                for i,col,label in [(0,'#a54b43',"0 → spine → 9"),(5,'#267398',"5 → spine → 14")]:
                    x=xs[i];x2=xs[(i+1)%8];xa=x+.012;xb=x2+.093
                    verts=[(xa,y0+.12),(xa,y0+.365),(xb,y0+.365),(xb,y0+.12)]
                    a.add_patch(FancyArrowPatch(path=MPath(verts),arrowstyle='-|>',mutation_scale=11,linewidth=1.6,color=col,shrinkA=0,shrinkB=0,zorder=5))
                    text(a,(xa+xb)/2,y0+.397,label,11,ha='center',color=col)
            text(a,.5,y0+.015,"orange: server A NICs 0–7; purple: server B NICs 8–15; one leaf switch per rail",11,ha='center')
        save(f,'rail-pairing')
        sw=data['7-in-network']['sweep'];f,a=plot(3.4,left=.15);xs=[r['servers'] for r in sw]
        a.plot(xs,[r['ring_seconds']*1000 for r in sw],marker='o',label="ring AllReduce",color='#a56c28');a.plot(xs,[r['switch_seconds']*1000 for r in sw],marker='s',label="in-network reduction",color='#267398')
        a.set_xscale('log',base=2);a.set_xticks(xs,[str(x) for x in xs]);a.set(xlabel="number of servers holding same shard",ylabel="cross-server phase (ms)",ylim=(0,1.35));a.legend(frameon=False,loc='upper left')
        a.text(32,sw[-1]['ring_seconds']*1000+.06,f"{sw[-1]['ring_seconds']*1000:.2f} ms",ha='right',fontsize=11);a.text(32,sw[-1]['switch_seconds']*1000-.12,f"{sw[-1]['switch_seconds']*1000:.2f} ms",ha='right',fontsize=11);save(f,'in-network-sweep')
        ec=data['7-ecmp']['cases'];f,a=plot(3.5,left=.14,bottom=.26);ns=[8,32,128];x=np.arange(3);w=.36
        for j,(m,label,c) in enumerate([(32,"32 uplinks (non-blocking leaf)",COL['blue']),(16,"16 uplinks (3:1 oversubscribed leaf)",COL['orange'])]):
            ks=[f'{n}-on-{m}' for n in ns];vals=[ec[k]['expected_max_load']/math.ceil(ec[k]['flows']/ec[k]['uplinks']) if k in ec else None for k in ks]
            pos=[i+(j-.5)*w for i,v in enumerate(vals) if v is not None];a.bar(pos,[v for v in vals if v is not None],color=c,edgecolor=COL['line'],width=w*.92,label=label)
            for p,v in zip(pos,vals):
                if v is not None:a.text(p,v+.12,f'{v:.2f}',ha='center',fontsize=11)
        a.axhline(1,ls=':',color='#777777');a.set(xticks=x,xticklabels=[f'{n} flows' for n in ns],ylabel="busiest uplink flow count / no contention",ylim=(0,4.3));a.legend(frameon=False,loc='upper right');save(f,'ecmp-collision')
        ic=data['7-incast'];f,a=plot(3.6,left=.16);t=np.linspace(0,4,401);free=ic['free_buffer_bytes']
        for row,c in zip(ic['rows'],['#267398','#388768','#a56c28']):
            ex=float(Fraction(row['excess_bytes_per_second_exact']));a.plot(t,np.minimum(ex*t*1e-6,free)/1024,color=c,label=f"N = {row['N']}");ta=row['allowed_feedback_ns']/1000;a.scatter([ta],[free/1024],color=c,s=28,zorder=4);a.text(ta+.06,free/1024-140,f'{ta:.2f} μs',fontsize=11,color=c)
        a.axhline(free/1024,ls='--',color='#777777');a.text(2.6,free/1024+40,"1 MiB remaining buffer",fontsize=11);a.axvline(.33,ls=':',color='#a54b43');a.text(.40,1150,"PFC one hop 0.33 μs",fontsize=11,color='#a54b43')
        a.set(xlabel="time (μs); end-to-end feedback 20 μs off-chart",ylabel="queue footprint (KiB)",xlim=(0,4),ylim=(0,1260));a.legend(frameon=False,loc='lower right');save(f,'incast-feedback')
    out.finish();return out.outputs,out.checks
