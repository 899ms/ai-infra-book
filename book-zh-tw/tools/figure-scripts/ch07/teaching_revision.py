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
            text(a,.05,.945 if top else .055,f'伺服器 {"AB"[row]}',13)
            sw_y=base+.24 if top else base+.055
            gpu_y=base+.14 if top else base+.155
            nic_y=base+.04 if top else base+.255
            box(a,.05,sw_y,.90,.06,"NVSwitch：每卡 NVLink 每方向 450 GB/s",'green',11)
            for i in range(8):
                x=.05+i*.1125
                box(a,x,gpu_y,.095,.08,str(row*8+i),'blue',11)
                box(a,x,nic_y,.095,.06,'NIC','orange',11)
                if top:arrow(a,(x+.0475,nic_y),(x+.0475,.545))
                else:arrow(a,(x+.0475,.455),(x+.0475,nic_y+.06))
        box(a,.02,.455,.96,.09,"交換網路：每條 rail 一臺交換機，每張網路卡每方向 50 GB/s",'gray',11)
        save(f,'1-boundaries')
        d=data['7-2'];f,a=plot(3.6);n=np.array(d['device_multipliers']);c=np.array(d['compute_ms']);t=d['cut_ms'];a.plot(n,c+t,label="依序執行",color='#267398');a.plot(n,np.maximum(c,t),label="完全重疊",color='#388768');a.plot(n,c,ls=':',label="計算",color='#a56c28');a.set(xlabel="加速器數量／基準數量",ylabel="每步時間（ms）",xticks=n,ylim=(0,32));a.legend(frameon=False);save(f,'2-cut')
        for idx,order in enumerate(data['7-3']['ring_orders']):
            f,a=canvas(4.4);text(a,.04,.93,"連續環：十六條邊只有兩條跨伺服器" if idx==0 else "交錯環：十六條邊都跨伺服器",14)
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
            if idx==0:text(a,xs[7]+.026,.51,"跨伺服器",11,ha='right');text(a,xs[0]+.056,.51,"跨伺服器",11)
            text(a,.5,.12,"藍：伺服器 A；橙：伺服器 B",12,ha='center');save(f,'3-hierarchy' if idx==0 else 'ring-interleaved')
        f,a=canvas(5.2)
        for col in range(2):
            x=.04+.51*col;text(a,x+.20,.93,f'伺服器 {"AB"[col]}',14,ha='center');box(a,x,.64,.41,.17,"本地 ReduceScatter\n得到八個 24 MiB 分片",'blue',11);box(a,x,.35,.41,.16,"對應分片跨伺服器\n兩卡 AllReduce，各走一條 rail",'orange',11);box(a,x,.06,.41,.16,"本地 AllGather\n得到完整歸約結果",'green',11);arrow(a,(x+.20,.64),(x+.20,.51));arrow(a,(x+.20,.35),(x+.20,.22))
        arrow(a,(.45,.46),(.55,.46));arrow(a,(.55,.39),(.45,.39));save(f,'hierarchy-stages')
        f,a=plot(3.6,left=.22);left=np.zeros(3)
        for k,l,c in [('local_MiB',"本地",'blue'),('remote_MiB',"跨伺服器",'orange')]:v=data['7-3'][k];a.barh(range(3),v,left=left,color=COL[c],edgecolor=COL['line'],label=l);left+=v
        a.set(yticks=range(3),yticklabels=["連續環","交錯環","分層歸約"],xlabel="邏輯傳送量，兩方向合計（MiB）");a.invert_yaxis();f.subplots_adjust(top=.84);a.legend(frameon=False,ncol=2,loc='upper center',bbox_to_anchor=(.45,1.17),columnspacing=1.5,handlelength=1.4);save(f,'hierarchy-bytes')
        f,a=plot(3.6,left=.18)
        for stage in range(4):
            for batch in range(8):a.barh(stage,1,left=stage+batch,height=.7,color=COL[['blue','green','orange','purple'][batch%4]],edgecolor=COL['line']);a.text(stage+batch+.5,stage,str(batch),ha='center',va='center',fontsize=11)
        a.set(yticks=range(4),yticklabels=[f'階段 {i}' for i in range(4)],xlim=(0,11),xticks=[0,2,4,6,8,10,11],xlabel="時間（ms）；格內為 micro-batch 編號");a.invert_yaxis();save(f,'4-pipeline')
        for i in range(3):
            f,a=canvas(3.9);text(a,.04,.94,["集中到一張網路卡","均分到八張獨立網路卡","對照設定：雙埠網路卡共用一個 PCIe 插槽"][i],14);box(a,.04,.42,.24,.24,'32 MiB','blue')
            if i==0:box(a,.64,.42,.30,.24,"網路卡\n50 GB/s",'orange');arrow(a,(.28,.54),(.64,.54))
            elif i==1:
                for j in range(8):
                    y=.10+j*.10;box(a,.70,y,.25,.08,'4 MiB','orange',11);arrow(a,(.28,.54),(.70,y+.04))
            else:
                box(a,.36,.32,.24,.42,"PCIe Gen4\nx16 插槽\n32 GB/s",'gray',11);arrow(a,(.28,.54),(.36,.54))
                for j in range(2):
                    y=.29+j*.28;box(a,.72,y,.25,.16,'16 MiB','orange',11);arrow(a,(.60,.54),(.72,y+.08))
            text(a,.5,.04,f'接收階段至少 {data["7-5"]["lower_ms"][i]:.2f} ms',13,ha='center');save(f,'5-expert' if i==0 else f'expert-path-{i}')
        f,a=canvas(4.8);box(a,.03,.44,.21,.18,"源 GPU",'blue');box(a,.39,.72,.27,.15,"直連 50",'green');box(a,.36,.17,.31,.19,"NVLink 450\n中繼網路卡 100",'orange',11);box(a,.78,.40,.20,.25,"下游\n可用頻寬",'gray');arrow(a,(.24,.53),(.39,.79));arrow(a,(.24,.53),(.36,.26));arrow(a,(.66,.79),(.78,.52));arrow(a,(.67,.26),(.78,.52));text(a,.5,.05,"單位 GB/s；中繼受借用網路卡合計 100 限制",12,ha='center');save(f,'6-relay')
        paths=[("主機 RPC",['CPU A',"網路卡 A","網路卡 B",'CPU B']),("CPU 提交 GPUDirect RDMA",['GPU A',"網路卡 A","網路卡 B",'GPU B']),("GPU 經 NVLink 存取",['GPU A','NVLink','GPU B']),("裝置發起 URMA 非同步存取",["裝置 A","UB 互聯","裝置 B"])]
        for i,(title,nodes) in enumerate(paths):
            f,a=canvas(3.8);text(a,.04,.94,title,14);step=.94/len(nodes)
            for j,node in enumerate(nodes):
                x=.03+j*step;box(a,x,.36,step-.045,.18,node,'blue' if j in [0,len(nodes)-1] else 'gray',11)
                if j<len(nodes)-1:arrow(a,(x+step-.045,.45),(x+step,.45))
            if i==1:box(a,.20,.69,.28,.12,"CPU 提交請求",'orange',11);arrow(a,(.34,.69),(.38,.54),'control')
            else:text(a,.5,.73,"發起者提交操作，接收方按完成條件使用結果",11,ha='center')
            text(a,.5,.13,"實線：資料；虛線：控制提交",11,ha='center');save(f,'7-access' if i==0 else f'access-{i}')
        f,a=canvas(4.1)
        for i in range(2):
            y=.61-i*.43;box(a,.04,y,.31,.19,"遠端快照",'blue');box(a,.65,y,.31,.19,"消費者" if i==0 else "本地副本",'green');arrow(a,(.35,y+.095),(.65,y+.095));text(a,.5,y+.25,"每次使用都跨網路讀取" if i==0 else "搬回一次，再讀取本地副本",13,ha='center')
        save(f,'snapshot-paths')
        for i,(label,c) in enumerate(data['7-8']['cases'].items()):
            f,a=plot(3.5);r=np.arange(1,6 if i==0 else 26);a.plot(r,c['remote_per_read_ms']*r,label="每次遠端讀取",color='#267398');a.plot(r,c['setup_ms']+c['local_per_read_ms']*r,label="先搬回本地",color='#388768');a.set(xlabel="複用次數",ylabel="累計時間（ms）");a.legend(frameon=False);save(f,'8-snapshot' if i==0 else 'snapshot-partial')
        f,a=canvas(4.0);text(a,.04,.94,"槽位儲存一項尚未完成的請求",14)
        for x,label,c in [(.03,"分配槽位",'blue'),(.37,"傳輸與等待",'orange'),(.71,"處理通知\n釋放槽位",'green')]:box(a,x,.39,.26,.23,label,c,12)
        arrow(a,(.29,.5),(.37,.5));arrow(a,(.63,.5),(.71,.5));text(a,.5,.18,"佔用時間：從分配到釋放，共 2 μs",12,ha='center');save(f,'slot-lifetime')
        f,a=plot(3.5,left=.24)
        for y,(key,p) in enumerate(data['7-9']['periods'].items()):
            a.barh(y,4,height=.5,color=COL['gray'])
            for start,dur in p['segments_us']:a.barh(y,dur,left=start,height=.5,color=COL['blue'],edgecolor=COL['line'])
        a.set(yticks=[0,1],yticklabels=["128 個槽位","391 個槽位"],xlim=(0,4),xlabel="時間（μs）；藍色為載荷傳送");a.invert_yaxis();save(f,'9-window')
        f,a=plot(3.5);n=np.arange(1,501);a.plot(n,np.minimum(50,n*256/2000),label="路徑與槽位限制",color='#267398');a.plot(n,np.minimum(data['7-9']['submission_cap_GBs'],n*256/2000),label="再加 18.6 ns 啟動間隔",color='#a56c28');a.set(xlabel="活躍請求槽位數",ylabel="吞吐上限（GB/s）");a.legend(frameon=False);save(f,'window-rate')
        f,a=plot(3.8,left=.23);a.barh(0,5,color=COL['blue'],height=.48);a.barh(1,12,color=COL['orange'],height=.48);a.barh(1,4,left=8,color=COL['green'],height=.48);a.axvline(6,ls=':',color='#a54b43');a.text(6.2,-.45,"6 μs 提前覆蓋",fontsize=11);a.set(yticks=[0,1],yticklabels=["源緩衝佔用","目的緩衝佔用"],xlim=(0,14),ylim=(-.7,1.6),xlabel="時間（μs）；綠色為消費者讀取");a.invert_yaxis();save(f,'10-lifetime')
        f,a=canvas(4.5)
        for i in range(2):
            y=.63-i*.39;box(a,.04,y,.23,.18,f'端點 {i}','blue');box(a,.38,y,.24,.18,"關係繫結",'orange');arrow(a,(.27,y+.09),(.38,y+.09));arrow(a,(.62,y+.09),(.77,.52))
        box(a,.77,.35,.20,.34,"目標\n傳輸狀態",'green',11);text(a,.5,.08,"端點身份分別儲存，目標傳輸狀態共享",12,ha='center');save(f,'11-state')
        f,a=plot(3.7,left=.26);left=np.zeros(3)
        for j,label,col in [(0,"端點",'blue'),(1,"繫結",'orange'),(2,"傳輸",'green')]:v=np.array(data['7-11']['state_MiB'])[:,j];a.barh(range(3),v,left=left,height=.5,color=COL[col],edgecolor=COL['line'],label=label);left+=v
        a.axvline(1,ls='--',color='#777777');a.set(yticks=range(3),yticklabels=["逐關係獨佔","按目標共享","八類隔離"],xlabel="狀態佔用（MiB）",xlim=(0,10));a.invert_yaxis();a.legend(frameon=False);save(f,'state-capacity')
        for i,(label,schedule) in enumerate(data['7-12']['schedules'].items()):
            f,a=plot(3.6,left=.21)
            for t in schedule['tasks']:
                lane=1 if t['id']=='independent_transfer' else 0;color={'write_data':'blue','recover_and_make_visible':'orange','publish_notification':'green','independent_transfer':'purple'}[t['id']];a.barh(lane,t['duration_ns']/1000,left=t['start_ns']/1000,height=.45,color=COL[color],edgecolor=COL['line'])
            a.set(yticks=[0,1],yticklabels=["寫入與釋出","獨立傳輸"],xlim=(0,115),xlabel="時間（μs）");a.invert_yaxis();save(f,'12-ordering' if i==0 else 'ordering-independent')
        f,a=canvas(5.0)
        for row,(time,label,c) in enumerate([(1,"提前讀取：得到舊值",'orange'),(2,"生產者寫入新值",'blue'),(3,"就緒標誌可見",'green'),(4,"消費者讀到就緒標誌",'green'),(5,"回傳先前讀到的舊值",'orange'),(6,"若在 4 μs 重讀，此時得到新值",'blue')]):
            y=.78-row*.14;text(a,.03,y+.04,f'{time} μs',11);box(a,.19,y,.76,.10,label,c,11)
        save(f,'13-stale')
        for i,(name,ops) in enumerate(data['7-14']['operations'].items()):
            f,a=plot(5,left=.17)
            for op in ops:
                y=op['operation'];start=op['submit_ns']/1000;end=op['transfer_complete_ns']/1000;done=op['completion_consumed_ns']/1000;a.barh(y,end-start,left=start,height=.65,color=COL['blue']);a.barh(y,done-end,left=end,height=.65,color=COL['orange'])
            a.set(xlim=(0,82),yticks=[0,4,8,12,15],ylabel="請求編號",xlabel="時間（μs）\n藍：傳輸；橙：等待槽位釋放");a.invert_yaxis();save(f,'14-reclaim' if i==0 else 'reclaim-more')
        for kind,n in [('arrival','15-congestion'),('queue','congestion-queue')]:
            f,a=plot(3.8)
            for (name,segs),label,c in zip(data['7-15']['periodic_segments'].items(),["重疊 20 ms","重疊 5 ms","不重疊"],['#267398','#a56c28','#388768']):
                xs=[];ys=[]
                for seg in segs:
                    xs.extend([seg['start_ns']/1e6,seg['end_ns']/1e6]);ys.extend([seg['arrival_bytes_per_second']/1e9]*2 if kind=='arrival' else [seg['queue_start_bytes']/1e6,seg['queue_end_bytes']/1e6])
                a.plot(xs,ys,label=label,color=c)
            a.set(xlabel="時間（ms）",ylabel="到達速率（GB/s）" if kind=='arrival' else "積壓（MB）",xlim=(0,100));a.legend(frameon=False);save(f,n)
        f,a=canvas(3.8);box(a,.04,.42,.24,.20,"傳送者\n100 GB/s",'blue');box(a,.43,.42,.24,.20,"緩衝佇列",'orange');box(a,.78,.42,.19,.20,"出口\n50 GB/s",'green',11);arrow(a,(.28,.52),(.43,.52));arrow(a,(.67,.52),(.78,.52));arrow(a,(.55,.42),(.17,.18),'control');text(a,.46,.12,"回饋生效後，傳送降至 40 GB/s",12,ha='center');save(f,'feedback-loop')
        f,a=plot(3.8)
        for seg in data['7-16']['queue_segments']:a.plot([seg['start_ns']/1000,seg['end_ns']/1000],[seg['queue_start_bytes']/1024,seg['queue_end_bytes']/1024],color='#267398')
        a.axvline(20,ls='--',color='#a56c28');a.set(xlabel="時間（μs）",ylabel="佇列佔用（KiB）",xlim=(0,120),ylim=(0,580));save(f,'16-feedback')
        packet_cases=dict(data['7-17']['cases'])
        loss=json.loads((here.parents[1]/'calculations/results/packet-reorder-loss.json').read_text())
        packet_cases['packet-reorder-loss']={k:loss[k] for k in ['transmissions','delivery']}
        for i,(name,c) in enumerate(packet_cases.items()):
            f,a=plot(3.7);delivery={x['sequence']:float(Fraction(x['delivery_exact_ns']))/1000 for x in c['delivery']}
            for t in c['transmissions']:
                if t['lost']:continue
                arrival=float(Fraction(t['arrival_exact_ns']))/1000;seq=t['sequence'];a.plot([arrival,delivery[seq]],[seq,seq],color='#a56c28');a.scatter(arrival,seq,color='#267398',s=22)
            a.set(xlim=(0,[1.6,10,22][i]),yticks=range(8),ylabel="報文序號",xlabel="到達與交給應用的時刻（μs）");a.invert_yaxis();save(f,'17-packets' if i==0 else f'packets-{i}')
        f,a=canvas(3.6);box(a,.04,.40,.34,.25,"請求 0 持有 A\n等待 B",'blue');box(a,.62,.40,.34,.25,"請求 1 持有 B\n等待 A",'orange');arrow(a,(.38,.58),(.62,.58));arrow(a,(.62,.46),(.38,.46));text(a,.5,.16,"雙方都需要對方先釋放",13,ha='center');save(f,'18-deadlock')
        f,a=canvas(3.7)
        for x,label,col in [(.03,"請求資源",'blue'),(.37,"執行資源",'orange'),(.71,"獨立回應\n資源",'green')]:box(a,x,.42,.26,.24,label,col,12)
        arrow(a,(.29,.54),(.37,.54));arrow(a,(.63,.54),(.71,.54));text(a,.5,.18,"回應有預留通路，可回傳並釋放原請求",12,ha='center');save(f,'response-reserve')
        for i,(ready,ex) in enumerate([([0,0,0,2],.4),([0,0,0,2],.2),([0]*4,.4)]):
            f,a=plot(3.5,left=.18)
            for lane,t in enumerate(ready):
                a.barh(lane,t,height=.5,color=COL['gray']);a.barh(lane,max(ready)-t,left=t,height=.5,color=COL['orange']);a.barh(lane,ex,left=max(ready),height=.5,color=COL['blue']);a.scatter(t,lane,color='#252525',s=16)
            a.set(yticks=range(4),yticklabels=[f'參與者 {j}' for j in range(4)],xlim=(0,2.6),xlabel="時間（ms）；圓點為就緒");a.invert_yaxis();save(f,'19-progress' if i==0 else f'progress-{i}')
        for i,c in enumerate(data['7-20']['cases']):
            f,a=plot(2.9,left=.17);a.barh(0,20,height=.45,color=COL['gray']);a.barh(1,c['comm_ms'],left=c['ready_ms'],height=.45,color=COL['blue']);a.barh(0,2,left=c['update_start_ms'],height=.45,color=COL['green']);a.scatter(c['ready_ms'],1,color='#252525',s=16);a.set(yticks=[0,1],yticklabels=["計算／更新","通訊"],xlim=(0,37),xlabel="時間（ms）");a.invert_yaxis();save(f,'20-step' if i==0 else f'step-{i}')
        f,a=plot(3.7);m=np.logspace(3,8,200)
        for alpha,b,label,col in [(5e-6,50e9,"原設定",'#267398'),(5e-6,150e9,"頻寬三倍",'#388768'),(2e-6,50e9,"啟動縮短",'#a56c28')]:a.loglog(m,(14*alpha+1.75*m/b)*1e6,label=label,color=col)
        a.set(xlabel="每參與者輸入（bytes）",ylabel="歸約時間（μs）");a.legend(frameon=False);save(f,'21-message')
        # Switch network (2026-09-11): Clos cut, rail pairing, in-network sweep, ECMP collision, incast feedback.
        f,a=canvas(4.3);text(a,.04,.95,"兩層 Clos：葉交換機接端點，脊交換機連線所有葉交換機",13)
        spx=[.24,.56];lx=[.03+i*.245 for i in range(4)]
        for j,x in enumerate(spx):box(a,x,.70,.20,.11,f'脊交換機 {j}','green',11)
        for i,x in enumerate(lx):
            box(a,x,.40,.20,.11,f'葉交換機 {i}','blue',11);box(a,x,.10,.20,.11,"32 個端點",'gray',11)
            a.plot([x+.10,x+.10],[.21,.40],color=COL['line'],lw=1)
            for sx in spx:a.plot([x+.10,sx+.10],[.51,.70],color=COL['line'],lw=1)
        a.plot([.5,.5],[.06,.67],ls='--',color='#a54b43',lw=1.2);text(a,.505,.30,"半分割集",11,color='#a54b43')
        text(a,.5,.03,"64 埠：每葉 32 下行、32 上聯；共 64 葉、32 脊、2048 個端點",11,ha='center');save(f,'clos-cut')
        f,a=canvas(6.2)
        from matplotlib.path import Path as MPath
        from matplotlib.patches import FancyArrowPatch
        for panel,(title,shifted) in enumerate([("對齊配對 rank i ↔ i+8：每一對留在自己的 rail 內",False),("錯位配對 rank i ↔ i+9：每一對經脊交換機換到下一條 rail",True)]):
            y0=.52-panel*.50;text(a,.03,y0+.45,title,12);xs=[.03+i*.1175 for i in range(8)]
            box(a,.03,y0+.35,.94,.07,"脊交換機" if not shifted else '','green',11)
            if shifted:text(a,.5,y0+.405,"脊交換機",11,ha='center')
            for i,x in enumerate(xs):
                box(a,x,y0+.22,.105,.08,f'rail {i}','blue',11);box(a,x,y0+.05,.048,.07,str(i),'orange',11);box(a,x+.057,y0+.05,.048,.07,str(i+8),'purple',11)
                arrow(a,(x+.024,y0+.12),(x+.03,y0+.22))
                if shifted:
                    x2=xs[(i+1)%8];arrow(a,(x+.03,y0+.30),(x+.03,y0+.35));arrow(a,(x2+.075,y0+.35),(x2+.075,y0+.30));arrow(a,(x2+.075,y0+.22),(x2+.081,y0+.12))
                else:arrow(a,(x+.075,y0+.22),(x+.081,y0+.12))
            if shifted:
                # Two representative cross-rail paths drawn end to end: NIC i -> leaf i -> spine -> leaf i+1 -> NIC i+9.
                for i,col,label in [(0,'#a54b43',"0 → 脊 → 9"),(5,'#267398',"5 → 脊 → 14")]:
                    x=xs[i];x2=xs[(i+1)%8];xa=x+.012;xb=x2+.093
                    verts=[(xa,y0+.12),(xa,y0+.365),(xb,y0+.365),(xb,y0+.12)]
                    a.add_patch(FancyArrowPatch(path=MPath(verts),arrowstyle='-|>',mutation_scale=11,linewidth=1.6,color=col,shrinkA=0,shrinkB=0,zorder=5))
                    text(a,(xa+xb)/2,y0+.397,label,11,ha='center',color=col)
            text(a,.5,y0+.015,"橙：伺服器 A 的網路卡 0–7；紫：伺服器 B 的網路卡 8–15；每條 rail 一臺葉交換機",11,ha='center')
        save(f,'rail-pairing')
        sw=data['7-in-network']['sweep'];f,a=plot(3.4,left=.15);xs=[r['servers'] for r in sw]
        a.plot(xs,[r['ring_seconds']*1000 for r in sw],marker='o',label="環形 AllReduce",color='#a56c28');a.plot(xs,[r['switch_seconds']*1000 for r in sw],marker='s',label="在網歸約",color='#267398')
        a.set_xscale('log',base=2);a.set_xticks(xs,[str(x) for x in xs]);a.set(xlabel="持有同一分片的伺服器數",ylabel="跨伺服器階段（ms）",ylim=(0,1.35));a.legend(frameon=False,loc='upper left')
        a.text(32,sw[-1]['ring_seconds']*1000+.06,f"{sw[-1]['ring_seconds']*1000:.2f} ms",ha='right',fontsize=11);a.text(32,sw[-1]['switch_seconds']*1000-.12,f"{sw[-1]['switch_seconds']*1000:.2f} ms",ha='right',fontsize=11);save(f,'in-network-sweep')
        ec=data['7-ecmp']['cases'];f,a=plot(3.5,left=.14,bottom=.26);ns=[8,32,128];x=np.arange(3);w=.36
        for j,(m,label,c) in enumerate([(32,"32 條上聯（無阻塞葉）",COL['blue']),(16,"16 條上聯（3:1 超售葉）",COL['orange'])]):
            ks=[f'{n}-on-{m}' for n in ns];vals=[ec[k]['expected_max_load']/math.ceil(ec[k]['flows']/ec[k]['uplinks']) if k in ec else None for k in ks]
            pos=[i+(j-.5)*w for i,v in enumerate(vals) if v is not None];a.bar(pos,[v for v in vals if v is not None],color=c,edgecolor=COL['line'],width=w*.92,label=label)
            for p,v in zip(pos,vals):
                if v is not None:a.text(p,v+.12,f'{v:.2f}',ha='center',fontsize=11)
        a.axhline(1,ls=':',color='#777777');a.set(xticks=x,xticklabels=[f'{n} 條流' for n in ns],ylabel="最忙上聯流數／無衝突時",ylim=(0,4.3));a.legend(frameon=False,loc='upper right');save(f,'ecmp-collision')
        ic=data['7-incast'];f,a=plot(3.6,left=.16);t=np.linspace(0,4,401);free=ic['free_buffer_bytes']
        for row,c in zip(ic['rows'],['#267398','#388768','#a56c28']):
            ex=float(Fraction(row['excess_bytes_per_second_exact']));a.plot(t,np.minimum(ex*t*1e-6,free)/1024,color=c,label=f"N = {row['N']}");ta=row['allowed_feedback_ns']/1000;a.scatter([ta],[free/1024],color=c,s=28,zorder=4);a.text(ta+.06,free/1024-140,f'{ta:.2f} μs',fontsize=11,color=c)
        a.axhline(free/1024,ls='--',color='#777777');a.text(2.6,free/1024+40,"1 MiB 剩餘緩衝",fontsize=11);a.axvline(.33,ls=':',color='#a54b43');a.text(.40,1150,"PFC 一跳 0.33 μs",fontsize=11,color='#a54b43')
        a.set(xlabel="時間（μs）；端到端回饋 20 μs 在圖外",ylabel="佇列佔用（KiB）",xlim=(0,4),ylim=(0,1260));a.legend(frameon=False,loc='lower right');save(f,'incast-feedback')
    out.finish();return out.outputs,out.checks
