"""A physical path before its budget; an event clock before its recurrence."""
import numpy as np
import matplotlib.pyplot as plt
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw_encoder_paths(out):
    """Show the same vision stages with the network boundary in two places."""
    with plt.rc_context(STYLE):
        for local, name in [(False, 'encoder-remote'), (True, 'encoder-local')]:
            f, a = canvas(6.5)
            # Two device lanes; vertical order follows the execution order.
            for x, title in [(.02, "Edge device"), (.59, "Remote server")]:
                box(a, x, .32, .39, .63, '', 'gray')
                text(a, x + .195, .918, title, 13, ha='center', weight='medium')
            a.plot([.5, .5], [.34, .95], color=COL['line'], lw=.8, ls=':')
            text(a, .5, .983, "Deployment boundary: uplink 6.4 Mbit/s", 12, ha='center')
            box(a, .045, .80, .34, .072, "Compressed screenshot 0.8 MB", 'blue', 11)
            x = .045 if local else .615
            cx = x + .17
            if not local:
                box(a, .615, .80, .34, .072, "Receive compressed image", 'blue', 11)
                arrow(a, (.385, .836), (.615, .836))
                text(a, .50, .875, "image", 11, ha='center')
                text(a, .215, .68, "Upload image", 12, ha='center')
                text(a, .215, .61, '0.8 MB ÷ 0.8 MB/s\n= 1.00 s', 11, ha='center')
                text(a, .215, .45, "Visual computation done remotely\nFeatures stay on server", 11, ha='center')
            box(a, x, .684, .34, .076, "Decode and preprocess\nResize to 640 × 640", 'blue', 11)
            arrow(a, (cx, .80), (cx, .76))
            box(a, x, .562, .34, .080, "Visual encoding and patch merging\nForm 400 visual tokens", 'green', 11)
            arrow(a, (cx, .684), (cx, .642))
            box(a, x, .430, .34, .090, "Final projection + 3 DeepStack groups\nFull BF16 features 8.192 MB", 'green', 11)
            arrow(a, (cx, .562), (cx, .520))
            if local:
                box(a, .615, .430, .34, .090, "Receive and restore four feature groups\nShape and precision match model", 'green', 11)
                arrow(a, (.385, .475), (.615, .475))
                text(a, .5, .536, "Full features", 11, ha='center')
                text(a, .785, .77, "Upload full numeric features", 12, ha='center')
                text(a, .785, .68, '8.192 MB ÷ 0.8 MB/s\n= 10.24 s', 11, ha='center')
                text(a, .215, .363, "Encode locally then serialize and send", 11, ha='center')
            arrow(a, (.785, .430), (.785, .397))
            arrow(a, (.785, .343), (.785, .307))
            text(a, .785, .367, "Feed into remote language model", 11, ha='center')
            # Both placements use identical downstream feature interfaces.
            box(a, .02, .025, .96, .277, '', 'white')
            text(a, .50, .272, "How four feature groups enter language model", 12, ha='center', weight='medium')
            box(a, .045, .162, .39, .060, "Final projection [400, 2560]", 'green', 11)
            box(a, .565, .162, .39, .060, "Combine with text embeddings as input", 'purple', 11)
            arrow(a, (.435, .192), (.565, .192))
            box(a, .045, .072, .39, .060, 'DeepStack  3 × [400, 2560]', 'green', 11)
            box(a, .565, .072, .39, .060, "Inject into corresponding intermediate layers", 'purple', 11)
            arrow(a, (.435, .102), (.565, .102))
            out.save(f, 'figure-12-' + name)

def draw_local_tiers(out,data):
    """Three local device tiers reading the same 16.345 GB decode step."""
    rows=[('RTX PRO 6000',9.12,'109.6 token/s','green'),
          ('M3 Ultra',19.96,'50.1 token/s','green'),
          ("phone, q4_0 weights",64.4,'15.5 token/s','blue'),
          ("phone, BF16 weights",192.7,'5.2 token/s','blue')]
    with plt.rc_context(STYLE):
        f,a=plot(3.4,left=.28)
        for y,(label,ms,rate,c) in enumerate(rows):
            a.barh(y,ms,height=.55,color=COL[c],edgecolor=COL['line'])
            text(a,ms+6,y,f'{ms:g} ms，{rate}',11)
        a.set(yticks=range(4),yticklabels=[r[0] for r in rows],xlabel="Per-step read time lower bound (ms)",xlim=(0,330))
        out.save(f,'figure-12-local-tiers')
    data['12-local-tiers']={'kind':'teaching_bound','step_bytes':16344778752,'phone_channels_x16_declared':4,
        'phone_bus_GBps':84.8,'q4_weight_bytes':4257230400,'rows_ms':[r[1] for r in rows],
        'token_per_s':[109.6,50.1,15.5,5.2],'relationship':"bandwidth sets per-step read lower bound"}

def draw_loss_repair(out,data):
    """Completion time on the 14 percent loss path under three repair schemes."""
    rows=[("send only, under Mathis bound",18.33,'gray'),
          ("per-round retransmit p99 (6 rounds)",1.239,'orange'),
          ("per-round retransmit expectation",0.756,'orange'),
          ("FEC 308 symbols, 99.9% retransmit-free",0.2407,'blue'),
          ("serial budget: RTT + model + send",0.2385,'green')]
    with plt.rc_context(STYLE):
        f,a=plot(3.6,left=.42)
        for y,(label,t,c) in enumerate(rows):
            a.barh(y,t,height=.55,color=COL[c],edgecolor=COL['line'])
            text(a,t*1.12,y,f'{t:g} s',11)
        a.set(xscale='log',xlim=(0.1,60),yticks=range(5),yticklabels=[r[0] for r in rows],
              xlabel="Completion time (s, log scale)",xticks=[.1,1,10],xticklabels=['0.1','1','10'])
        out.save(f,'figure-12-loss-repair')
    data['12-loss-repair']={'kind':'teaching_bound','path':{'rtt_s':.2,'knee_Mbps':333,'loss':.14,'mss_bytes':1448,
        'request_bytes':354640},'packets':245,'serial_budget_s':.2385,'mathis_Mbps':.1548,'mathis_send_s':18.33,
        'retransmit_expected_s':.756,'retransmit_p99_s':1.239,'fec_repair':63,'fec_overhead':.257,'fec_s':.2407,
        'relationship':"repair method determines completion time"}

def draw(here,data):
    out=Exporter(here)
    def save(f,n):out.save(f,'figure-12-'+n)
    with plt.rc_context(STYLE):
        f,a=canvas(4.8);box(a,.04,.67,.32,.20,"device: 30 MB original image",'blue',11);box(a,.64,.67,.32,.20,"server: process 0.3 s",'green',11);arrow(a,(.36,.77),(.64,.77));text(a,.5,.95,"uplink: 20 Mbit/s, send 12 s",12,ha='center')
        box(a,.64,.22,.32,.20,"generate 5 MB final clip",'green',11);box(a,.04,.22,.32,.20,"device: all received, task done",'orange',11);arrow(a,(.8,.67),(.8,.42));arrow(a,(.64,.32),(.36,.32));text(a,.5,.09,"Downlink: 100 Mbit/s, send 0.4 s",12,ha='center');text(a,.27,.52,"Round-trip propagation 0.1 s",11,ha='center');save(f,'image-path')
        d=data['12-1'];f,a=plot(4.0);b=np.array(d['uplink_Mbps'])
        for y,l,c in [(240/b+.8,"Original scheme",'#267398'),(240/b+.53,"10× faster processing",'#388768'),(120/b+.95,"Input halved",'#a56c28')]:a.plot(b,y,label=l,color=c)
        a.set(xscale='log',xlabel="Uplink rate (Mbit/s)",ylabel="Full clip return time (s)");a.legend(frameon=False);save(f,'1-raw')
        for chunked,name in [(False,'2-overlap'),(True,'overlap-chunks')]:
            f,a=plot(4.0,left=.20)
            if chunked:
                for i,ret in enumerate([.08,.16,.16]):
                    u=4*(i+1);a.barh(2,4,left=4*i,height=.5,color=COL['blue'],edgecolor=COL['line']);a.barh(1,.1,left=u+.05,height=.5,color=COL['green'],edgecolor=COL['line']);a.barh(0,ret,left=u+.15,height=.5,color=COL['orange'],edgecolor=COL['line'])
            else:
                for row,start,dur,c in [(2,0,12,'blue'),(1,12.05,.3,'green'),(0,12.35,.4,'orange')]:a.barh(row,dur,left=start,height=.5,color=COL[c],edgecolor=COL['line'])
            a.set(yticks=[2,1,0],yticklabels=["upload","processing","return transfer"],xlim=(0,13),xlabel="Time (s)");save(f,name)
        f,a=plot(4.1,left=.23)
        for row,start,dur,c in [(3,0,20,'blue'),(2,20,12,'green'),(1,32,1,'orange'),(0,78,20,'purple')]:a.barh(row,dur,left=start,height=.5,color=COL[c],edgecolor=COL['line'])
        a.plot(38,1,'o',color='#454545');a.annotate("Arrival 38 ms",(38,1),(45,1.55),fontsize=11,arrowprops={'arrowstyle':'->'});a.set(yticks=[3,2,1,0],yticklabels=["Capture","Model processing","Send/arrival","Playback"],xlim=(0,105),xlabel="time (ms)");save(f,'audio-clocks')
        f,a=plot(4.3,left=.20);chunks=data['12-3']['audio_chunks'][:5]
        for i,r in enumerate(chunks):
            a.barh(i,20,left=r['deadline_ns']/1e6,height=.6,color='white',edgecolor=COL['line']);a.barh(i,20,left=r['playback_start_ns']/1e6,height=.36,color=COL['blue'],edgecolor=COL['line']);a.plot(r['arrival_ns']/1e6,i,'o',color='#a56c28')
        a.set(yticks=range(5),yticklabels=[f'block {i+1}' for i in range(5)],xlabel="time (ms)",xlim=(25,190));a.invert_yaxis();save(f,'3-paths')
        d=data['12-4'];f,a=plot(3.8)
        for bits,c in zip(d['initial_bits'],['#267398','#a56c28']):t=np.linspace(0,bits/(256000-130000),100);a.plot(t*1000,(bits-t*126000)/1000,color=c,label=f'initial {bits/256000*1000:g} ms audio')
        a.set(xlabel="Time since playback start (ms)",ylabel="Unplayed data (kbit)",ylim=(0,34));a.legend(frameon=False);save(f,'4-buffer')
        f,a=canvas(4.1)
        for x,y,l,c in [(.04,.63,"screenshot v",'blue'),(.62,.63,"Upload and model inference",'green'),(.62,.18,"Execute action",'orange'),(.04,.18,"Update UI v+1",'blue')]:box(a,x,y,.34,.21,l,c)
        for p,q in [((.38,.735),(.62,.735)),((.79,.63),(.79,.39)),((.62,.285),(.38,.285)),((.21,.39),(.21,.63))]:arrow(a,p,q)
        save(f,'5-agent')
        draw_encoder_paths(out)
        f,a=plot(3.3,left=.23);a.barh([1,0],[1,10.24],height=.5,color=[COL['blue'],COL['green']],edgecolor=COL['line']);a.set(yticks=[1,0],yticklabels=["compressed image","Full features"],xlabel="6.4 Mbit/s uplink send time (s)",xlim=(0,11.5));save(f,'6-placement')
        f,a=canvas(5.4)
        for row,(l,c) in enumerate([("Image: 0.8 MB",'blue'),("Encoder cache EC: 7.8 MiB",'green'),("Visual token KV: 56.3 MiB",'purple')]):
            y=.73-row*.28;box(a,.04,y,.49,.17,l,c,11);text(a,.57,y+.085,["redo vision encoding\nthen process language prefix","start from language prefix processing","continue after matched prefix"][row],11)
        save(f,'cache-restart')
        f,a=plot(3.9);n=np.arange(0,41)
        for extra,c in [(0,'#267398'),(1,'#a56c28')]:a.plot(n,n*.4-data['12-7']['preparation_s']-extra,label=f'recover {1+extra} s',color=c)
        a.axhline(0,color='#666');a.set(xlabel="Rounds completed after migration",ylabel="Cumulative net savings (s)");a.legend(frameon=False);save(f,'7-migration')
        # A layer's reductions are separate handoffs with two matching participants.
        for ffn,name in [(False,'8-sync'),(True,'sync-ffn')]:
            f,a=canvas(4.1);text(a,.5,.94,"After feedforward output aggregation, proceed to next layer" if ffn else "After attention output aggregation, proceed to feedforward",13,ha='center')
            for row in range(2):
                y=.62-row*.36;box(a,.04,y,.29,.20,('FFN' if ffn else "Attention")+f'shard {row}','blue',11);box(a,.68,y,.28,.20,"next layer" if ffn else "feedforward computation",'green',11);arrow(a,(.33,y+.10),(.68,y+.10))
            arrow(a,(.50,.72),(.50,.36));arrow(a,(.54,.36),(.54,.72));text(a,.54,.11,"Two-card reduction output",11,ha='center');save(f,name)
        f,a=plot(3.8,left=.18);cycle=data['12-9']['cycle_s']*1000
        for i in range(3):
            a.barh(0,25.6,left=i*cycle,height=.5,color=COL['blue'],edgecolor=COL['line']);a.barh(0,100,left=i*cycle+25.6,height=.5,color=COL['gray'],edgecolor=COL['line'])
        a.set(yticks=[0],yticklabels=["sender"],xlabel="time (ms)",xlim=(0,380));text(a,20,.6,"Send 25.6 ms",11);text(a,60,-.6,"Wait for batch ack 100 ms",11);a.set_ylim(-1,1);save(f,'9-window')
        for order,name in [(False,'10-transport'),(True,'transport-per-stream')]:
            f,a=plot(3.2,left=.20)
            for row,ready,done,c in [(1,3,3 if order else 7,'blue'),(0,7,7,'green')]:
                a.barh(row,ready,height=.5,color=COL[c],edgecolor=COL['line'])
                if done>ready:a.barh(row,done-ready,left=ready,height=.5,color=COL['gray'],edgecolor=COL['line'])
                a.plot(done,row,'o',color='#454545')
            a.set(yticks=[1,0],yticklabels=["audio","image"],xlim=(0,8),xlabel="Time data handed to app (s)");save(f,name)
        f,a=plot(4.0,left=.20)
        for row,parts in enumerate(data['12-11']['exchange_components_us']):
            start=0
            for v,c,l in zip(parts,['gray','blue','orange','green'],["access wait","Data frame",'SIFS','MAC ACK']):a.barh(row,v,left=start,height=.5,color=COL[c],edgecolor=COL['line'],label=l if row==0 else None);start+=v
        a.set(yticks=[0,1],yticklabels=["data exchange","feedback exchange"],xlabel="Airtime usage (μs)",ylim=(-.5,2.4));a.legend(ncol=2,frameon=False,loc='upper left');save(f,'11-wireless')
        f,a=canvas(4.4);box(a,.30,.73,.40,.18,"User sends cancel",'orange')
        for x,l,c in [(.04,"Local: flush playback buffer",'blue'),(.57,"Remote: stop generation and sending",'green')]:box(a,x,.30,.39,.23,l,c,11);arrow(a,(.5,.73),(x+.195,.53),'control')
        text(a,.235,.15,"Stop playback immediately",11,ha='center');text(a,.765,.15,"Execute after control message arrives",11,ha='center');save(f,'cancel-paths')
        for shared,name in [(False,'multipath-independent'),(True,'12-multipath')]:
            f,a=canvas(4.6);box(a,.04,.39,.23,.21,"30 MB image",'blue',11)
            for y,l in [(.72,'20 MB／20 Mbit/s'),(.15,'10 MB／10 Mbit/s')]:box(a,.38,y,.40,.17,l,'green',11);arrow(a,(.27,.5),(.38,y+.085))
            if shared:box(a,.82,.37,.15,.25,"shared\negress",'orange',11);arrow(a,(.78,.805),(.89,.62));arrow(a,(.78,.235),(.89,.37));text(a,.5,.05,"shared egress 24 Mbit/s → at least 10 s",11,ha='center')
            else:text(a,.5,.05,"two independent paths: each finishes its part in 8 s",11,ha='center')
            save(f,name)
        for i,row in enumerate(data['12-13']['matched_ASR_ms']):
            f,a=plot(3.8);a.bar([0,1],np.array(row)/1000,color=[COL['blue'],COL['green']],edgecolor=COL['line'])
            for j,v in enumerate(row):a.text(j,v/1000+.03,f'{v:.1f} ms',fontsize=12,ha='center')
            a.set(xticks=[0,1],xticklabels=["direct path",'Queqiao'],ylabel="median request time (s)",ylim=(0,1.4));save(f,'13-queqiao' if i==0 else 'queqiao-tuned')
        f,a=canvas(4.7);text(a,.04,.94,"Single-factor design: change one setting per step",13)
        for row,(l,c) in enumerate([("connection reuse → handshake and first-byte time",'blue'),("window setting → in-flight amount and ack time",'green'),("send pacing → egress idle and completion time",'orange')]):box(a,.04,.68-row*.26,.92,.18,l,c,12)
        save(f,'experiment-design')
        for i,row in enumerate(data['12-14']['seconds']):
            f,a=plot(3.6,left=.18);start=0
            for v,c,l in zip(row,['gray','orange','green','purple','blue'],["Prep","terminal","model","propagation","upload"]):
                if v:a.barh(0,v,left=start,height=.5,color=COL[c],edgecolor=COL['line'],label=l)
                start+=v
            a.axvline(45,ls='--',color='#a56c28');a.set(yticks=[0],yticklabels=[["device side","nearby","cloud"][i]],xlabel="remaining 20 rounds completion time (s)",xlim=(0,68),ylim=(-.6,1.6));a.legend(ncol=3,frameon=False,loc='upper left');save(f,'14-budgets' if i==0 else 'budgets-'+str(i))
        d=data['12-15'];f,a=plot(4.0);b=np.array(d['scan_Mbps']);a.plot(b,d['cloud_seconds'],color='#267398',label="Cloud H100");a.axhline(d['near_s'],color='#388768',label=f"nearby RTX PRO 6000:{d['near_s']:.1f} s");a.axhline(d['deadline_s'],ls='--',color='#a56c28',label=f"deadline:{d['deadline_s']:g} s");a.set(xlabel="Cloud uplink (Mbit/s)",ylabel="Time to complete 20 rounds (s)",ylim=(0,80));a.legend(frameon=False);save(f,'15-deployment')
        for retained,name in [(True,'16-recovery'),(False,'recovery-all')]:
            rc=data['12-16']['round_s'];f,a=canvas(4.2);text(a,.04,.94,f'cloud has executed 10 rounds, each round {rc:.2f} s; reconnecting requires 1 s',14)
            for i in range(10):box(a,.04+i%5*.187,.66-(i//5)*.22,.17,.15,str(i+1),'green' if retained and i<9 else 'orange',12)
            text(a,.5,.22,"keep first 9 rounds, redo only round 10" if retained else "progress lost, redo 10 rounds",12,ha='center');text(a,.5,.08,f'extra 1 + {rc:.2f} = {1+rc:.2f} s' if retained else f'extra 1 + 10 × {rc:.2f} ≈ {1+10*rc:.1f} s',12,ha='center');save(f,name)
    from core_principles_figures import draw as draw_principles
    draw_principles(12, out)
    draw_local_tiers(out,data);draw_loss_repair(out,data)
    out.finish();return out.outputs,out.checks
