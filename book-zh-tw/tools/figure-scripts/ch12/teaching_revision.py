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
            for x, title in [(.02, "端側裝置"), (.59, "遠端伺服器")]:
                box(a, x, .32, .39, .63, '', 'gray')
                text(a, x + .195, .918, title, 13, ha='center', weight='medium')
            a.plot([.5, .5], [.34, .95], color=COL['line'], lw=.8, ls=':')
            text(a, .5, .983, "部署邊界：上行 6.4 Mbit/s", 12, ha='center')
            box(a, .045, .80, .34, .072, "壓縮截圖  0.8 MB", 'blue', 11)
            x = .045 if local else .615
            cx = x + .17
            if not local:
                box(a, .615, .80, .34, .072, "接收壓縮圖片", 'blue', 11)
                arrow(a, (.385, .836), (.615, .836))
                text(a, .50, .875, "圖片", 11, ha='center')
                text(a, .215, .68, "上傳圖片", 12, ha='center')
                text(a, .215, .61, '0.8 MB ÷ 0.8 MB/s\n= 1.00 s', 11, ha='center')
                text(a, .215, .45, "視覺計算在遠端完成\n特徵留在伺服器內", 11, ha='center')
            box(a, x, .684, .34, .076, "解碼與預處理\n縮放至 640 × 640", 'blue', 11)
            arrow(a, (cx, .80), (cx, .76))
            box(a, x, .562, .34, .080, "視覺編碼與影象塊合併\n形成 400 個視覺 token", 'green', 11)
            arrow(a, (cx, .684), (cx, .642))
            box(a, x, .430, .34, .090, "最終投影 + 3 組 DeepStack\n完整 BF16 特徵  8.192 MB", 'green', 11)
            arrow(a, (cx, .562), (cx, .520))
            if local:
                box(a, .615, .430, .34, .090, "接收並還原四組特徵\n形狀、精度與模型匹配", 'green', 11)
                arrow(a, (.385, .475), (.615, .475))
                text(a, .5, .536, "完整特徵", 11, ha='center')
                text(a, .785, .77, "上傳完整數值特徵", 12, ha='center')
                text(a, .785, .68, '8.192 MB ÷ 0.8 MB/s\n= 10.24 s', 11, ha='center')
                text(a, .215, .363, "本地編碼後序列化傳送", 11, ha='center')
            arrow(a, (.785, .430), (.785, .397))
            arrow(a, (.785, .343), (.785, .307))
            text(a, .785, .367, "送入遠端語言模型", 11, ha='center')
            # Both placements use identical downstream feature interfaces.
            box(a, .02, .025, .96, .277, '', 'white')
            text(a, .50, .272, "四組特徵如何進入語言模型", 12, ha='center', weight='medium')
            box(a, .045, .162, .39, .060, "最終投影  [400, 2560]", 'green', 11)
            box(a, .565, .162, .39, .060, "與文字嵌入組成輸入", 'purple', 11)
            arrow(a, (.435, .192), (.565, .192))
            box(a, .045, .072, .39, .060, 'DeepStack  3 × [400, 2560]', 'green', 11)
            box(a, .565, .072, .39, .060, "分別注入對應的中間層", 'purple', 11)
            arrow(a, (.435, .102), (.565, .102))
            out.save(f, 'figure-12-' + name)

def draw_local_tiers(out,data):
    """Three local device tiers reading the same 16.345 GB decode step."""
    rows=[('RTX PRO 6000',9.12,'109.6 token/s','green'),
          ('M3 Ultra',19.96,'50.1 token/s','green'),
          ("手機，q4_0 權重",64.4,'15.5 token/s','blue'),
          ("手機，BF16 權重",192.7,'5.2 token/s','blue')]
    with plt.rc_context(STYLE):
        f,a=plot(3.4,left=.28)
        for y,(label,ms,rate,c) in enumerate(rows):
            a.barh(y,ms,height=.55,color=COL[c],edgecolor=COL['line'])
            text(a,ms+6,y,f'{ms:g} ms，{rate}',11)
        a.set(yticks=range(4),yticklabels=[r[0] for r in rows],xlabel="每步讀取時間下界（ms）",xlim=(0,330))
        out.save(f,'figure-12-local-tiers')
    data['12-local-tiers']={'kind':'teaching_bound','step_bytes':16344778752,'phone_channels_x16_declared':4,
        'phone_bus_GBps':84.8,'q4_weight_bytes':4257230400,'rows_ms':[r[1] for r in rows],
        'token_per_s':[109.6,50.1,15.5,5.2],'relationship':"頻寬決定每步讀取下界"}

def draw_loss_repair(out,data):
    """Completion time on the 14 percent loss path under three repair schemes."""
    rows=[("Mathis 上界下僅傳送",18.33,'gray'),
          ("逐輪重傳 p99（6 輪）",1.239,'orange'),
          ("逐輪重傳期望",0.756,'orange'),
          ("FEC 308 符號，99.9% 免重傳",0.2407,'blue'),
          ("序列預算：RTT＋模型＋傳送",0.2385,'green')]
    with plt.rc_context(STYLE):
        f,a=plot(3.6,left=.42)
        for y,(label,t,c) in enumerate(rows):
            a.barh(y,t,height=.55,color=COL[c],edgecolor=COL['line'])
            text(a,t*1.12,y,f'{t:g} s',11)
        a.set(xscale='log',xlim=(0.1,60),yticks=range(5),yticklabels=[r[0] for r in rows],
              xlabel="完成時間（s，對數座標）",xticks=[.1,1,10],xticklabels=['0.1','1','10'])
        out.save(f,'figure-12-loss-repair')
    data['12-loss-repair']={'kind':'teaching_bound','path':{'rtt_s':.2,'knee_Mbps':333,'loss':.14,'mss_bytes':1448,
        'request_bytes':354640},'packets':245,'serial_budget_s':.2385,'mathis_Mbps':.1548,'mathis_send_s':18.33,
        'retransmit_expected_s':.756,'retransmit_p99_s':1.239,'fec_repair':63,'fec_overhead':.257,'fec_s':.2407,
        'relationship':"修復方式決定完成時間"}

def draw(here,data):
    out=Exporter(here)
    def save(f,n):out.save(f,'figure-12-'+n)
    with plt.rc_context(STYLE):
        f,a=canvas(4.8);box(a,.04,.67,.32,.20,"終端：30 MB 原圖",'blue',11);box(a,.64,.67,.32,.20,"伺服器：處理 0.3 s",'green',11);arrow(a,(.36,.77),(.64,.77));text(a,.5,.95,"上行：20 Mbit/s，傳送 12 s",12,ha='center')
        box(a,.64,.22,.32,.20,"生成 5 MB 成片",'green',11);box(a,.04,.22,.32,.20,"終端收齊：任務完成",'orange',11);arrow(a,(.8,.67),(.8,.42));arrow(a,(.64,.32),(.36,.32));text(a,.5,.09,"下行：100 Mbit/s，傳送 0.4 s",12,ha='center');text(a,.27,.52,"雙向傳播合計 0.1 s",11,ha='center');save(f,'image-path')
        d=data['12-1'];f,a=plot(4.0);b=np.array(d['uplink_Mbps'])
        for y,l,c in [(240/b+.8,"原方案",'#267398'),(240/b+.53,"處理快十倍",'#388768'),(120/b+.95,"輸入減半",'#a56c28')]:a.plot(b,y,label=l,color=c)
        a.set(xscale='log',xlabel="上行速率（Mbit/s）",ylabel="完整成片返回時間（s）");a.legend(frameon=False);save(f,'1-raw')
        for chunked,name in [(False,'2-overlap'),(True,'overlap-chunks')]:
            f,a=plot(4.0,left=.20)
            if chunked:
                for i,ret in enumerate([.08,.16,.16]):
                    u=4*(i+1);a.barh(2,4,left=4*i,height=.5,color=COL['blue'],edgecolor=COL['line']);a.barh(1,.1,left=u+.05,height=.5,color=COL['green'],edgecolor=COL['line']);a.barh(0,ret,left=u+.15,height=.5,color=COL['orange'],edgecolor=COL['line'])
            else:
                for row,start,dur,c in [(2,0,12,'blue'),(1,12.05,.3,'green'),(0,12.35,.4,'orange')]:a.barh(row,dur,left=start,height=.5,color=COL[c],edgecolor=COL['line'])
            a.set(yticks=[2,1,0],yticklabels=["上傳","處理","回傳"],xlim=(0,13),xlabel="時間（s）");save(f,name)
        f,a=plot(4.1,left=.23)
        for row,start,dur,c in [(3,0,20,'blue'),(2,20,12,'green'),(1,32,1,'orange'),(0,78,20,'purple')]:a.barh(row,dur,left=start,height=.5,color=COL[c],edgecolor=COL['line'])
        a.plot(38,1,'o',color='#454545');a.annotate("到達 38 ms",(38,1),(45,1.55),fontsize=11,arrowprops={'arrowstyle':'->'});a.set(yticks=[3,2,1,0],yticklabels=["採集","模型處理","傳送／到達","播放"],xlim=(0,105),xlabel="時間（ms）");save(f,'audio-clocks')
        f,a=plot(4.3,left=.20);chunks=data['12-3']['audio_chunks'][:5]
        for i,r in enumerate(chunks):
            a.barh(i,20,left=r['deadline_ns']/1e6,height=.6,color='white',edgecolor=COL['line']);a.barh(i,20,left=r['playback_start_ns']/1e6,height=.36,color=COL['blue'],edgecolor=COL['line']);a.plot(r['arrival_ns']/1e6,i,'o',color='#a56c28')
        a.set(yticks=range(5),yticklabels=[f'塊 {i+1}' for i in range(5)],xlabel="時間（ms）",xlim=(25,190));a.invert_yaxis();save(f,'3-paths')
        d=data['12-4'];f,a=plot(3.8)
        for bits,c in zip(d['initial_bits'],['#267398','#a56c28']):t=np.linspace(0,bits/(256000-130000),100);a.plot(t*1000,(bits-t*126000)/1000,color=c,label=f'初始 {bits/256000*1000:g} ms 音訊')
        a.set(xlabel="播放開始後的時間（ms）",ylabel="尚未播放的資料（kbit）",ylim=(0,34));a.legend(frameon=False);save(f,'4-buffer')
        f,a=canvas(4.1)
        for x,y,l,c in [(.04,.63,"截圖 v",'blue'),(.62,.63,"上傳與模型判斷",'green'),(.62,.18,"執行操作",'orange'),(.04,.18,"更新介面 v+1",'blue')]:box(a,x,y,.34,.21,l,c)
        for p,q in [((.38,.735),(.62,.735)),((.79,.63),(.79,.39)),((.62,.285),(.38,.285)),((.21,.39),(.21,.63))]:arrow(a,p,q)
        save(f,'5-agent')
        draw_encoder_paths(out)
        f,a=plot(3.3,left=.23);a.barh([1,0],[1,10.24],height=.5,color=[COL['blue'],COL['green']],edgecolor=COL['line']);a.set(yticks=[1,0],yticklabels=["壓縮圖片","完整特徵"],xlabel="6.4 Mbit/s 上行傳送時間（s）",xlim=(0,11.5));save(f,'6-placement')
        f,a=canvas(5.4)
        for row,(l,c) in enumerate([("圖片：0.8 MB",'blue'),("編碼快取 EC：7.8 MiB",'green'),("視覺 token KV：56.3 MiB",'purple')]):
            y=.73-row*.28;box(a,.04,y,.49,.17,l,c,11);text(a,.57,y+.085,["重做視覺編碼\n再處理語言字首","從語言字首處理開始","從匹配字首之後繼續"][row],11)
        save(f,'cache-restart')
        f,a=plot(3.9);n=np.arange(0,41)
        for extra,c in [(0,'#267398'),(1,'#a56c28')]:a.plot(n,n*.4-data['12-7']['preparation_s']-extra,label=f'恢復 {1+extra} s',color=c)
        a.axhline(0,color='#666');a.set(xlabel="遷移後完成輪數",ylabel="累計淨節省（s）");a.legend(frameon=False);save(f,'7-migration')
        # A layer's reductions are separate handoffs with two matching participants.
        for ffn,name in [(False,'8-sync'),(True,'sync-ffn')]:
            f,a=canvas(4.1);text(a,.5,.94,"前饋輸出彙總後，進入下一層" if ffn else "注意力輸出彙總後，進入前饋",13,ha='center')
            for row in range(2):
                y=.62-row*.36;box(a,.04,y,.29,.20,('FFN' if ffn else "注意力")+f'分片 {row}','blue',11);box(a,.68,y,.28,.20,"下一層" if ffn else "前饋計算",'green',11);arrow(a,(.33,y+.10),(.68,y+.10))
            arrow(a,(.50,.72),(.50,.36));arrow(a,(.54,.36),(.54,.72));text(a,.54,.11,"兩卡歸約輸出",11,ha='center');save(f,name)
        f,a=plot(3.8,left=.18);cycle=data['12-9']['cycle_s']*1000
        for i in range(3):
            a.barh(0,25.6,left=i*cycle,height=.5,color=COL['blue'],edgecolor=COL['line']);a.barh(0,100,left=i*cycle+25.6,height=.5,color=COL['gray'],edgecolor=COL['line'])
        a.set(yticks=[0],yticklabels=["傳送端"],xlabel="時間（ms）",xlim=(0,380));text(a,20,.6,"發 25.6 ms",11);text(a,60,-.6,"等整批確認 100 ms",11);a.set_ylim(-1,1);save(f,'9-window')
        for order,name in [(False,'10-transport'),(True,'transport-per-stream')]:
            f,a=plot(3.2,left=.20)
            for row,ready,done,c in [(1,3,3 if order else 7,'blue'),(0,7,7,'green')]:
                a.barh(row,ready,height=.5,color=COL[c],edgecolor=COL['line'])
                if done>ready:a.barh(row,done-ready,left=ready,height=.5,color=COL['gray'],edgecolor=COL['line'])
                a.plot(done,row,'o',color='#454545')
            a.set(yticks=[1,0],yticklabels=["音訊","圖片"],xlim=(0,8),xlabel="資料交給應用的時刻（s）");save(f,name)
        f,a=plot(4.0,left=.20)
        for row,parts in enumerate(data['12-11']['exchange_components_us']):
            start=0
            for v,c,l in zip(parts,['gray','blue','orange','green'],["接入等待","資料幀",'SIFS','MAC ACK']):a.barh(row,v,left=start,height=.5,color=COL[c],edgecolor=COL['line'],label=l if row==0 else None);start+=v
        a.set(yticks=[0,1],yticklabels=["資料交換","回饋交換"],xlabel="空口占用（μs）",ylim=(-.5,2.4));a.legend(ncol=2,frameon=False,loc='upper left');save(f,'11-wireless')
        f,a=canvas(4.4);box(a,.30,.73,.40,.18,"使用者發出取消",'orange')
        for x,l,c in [(.04,"本地：清空播放緩衝",'blue'),(.57,"遠端：停止生成與傳送",'green')]:box(a,x,.30,.39,.23,l,c,11);arrow(a,(.5,.73),(x+.195,.53),'control')
        text(a,.235,.15,"立即停止播放",11,ha='center');text(a,.765,.15,"控制訊息到達後執行",11,ha='center');save(f,'cancel-paths')
        for shared,name in [(False,'multipath-independent'),(True,'12-multipath')]:
            f,a=canvas(4.6);box(a,.04,.39,.23,.21,"30 MB 圖片",'blue',11)
            for y,l in [(.72,'20 MB／20 Mbit/s'),(.15,'10 MB／10 Mbit/s')]:box(a,.38,y,.40,.17,l,'green',11);arrow(a,(.27,.5),(.38,y+.085))
            if shared:box(a,.82,.37,.15,.25,"共同\n出口",'orange',11);arrow(a,(.78,.805),(.89,.62));arrow(a,(.78,.235),(.89,.37));text(a,.5,.05,"共同出口 24 Mbit/s → 至少 10 s",11,ha='center')
            else:text(a,.5,.05,"兩路獨立：均在 8 s 發完自己的部分",11,ha='center')
            save(f,name)
        for i,row in enumerate(data['12-13']['matched_ASR_ms']):
            f,a=plot(3.8);a.bar([0,1],np.array(row)/1000,color=[COL['blue'],COL['green']],edgecolor=COL['line'])
            for j,v in enumerate(row):a.text(j,v/1000+.03,f'{v:.1f} ms',fontsize=12,ha='center')
            a.set(xticks=[0,1],xticklabels=["直接路徑",'Queqiao'],ylabel="請求中位數（s）",ylim=(0,1.4));save(f,'13-queqiao' if i==0 else 'queqiao-tuned')
        f,a=canvas(4.7);text(a,.04,.94,"單因素實驗設計：每步只改變一個設定",13)
        for row,(l,c) in enumerate([("連線複用 → 握手與首位元組時刻",'blue'),("視窗設定 → 在途量與確認時刻",'green'),("傳送節奏 → 出口空閒與完成時刻",'orange')]):box(a,.04,.68-row*.26,.92,.18,l,c,12)
        save(f,'experiment-design')
        for i,row in enumerate(data['12-14']['seconds']):
            f,a=plot(3.6,left=.18);start=0
            for v,c,l in zip(row,['gray','orange','green','purple','blue'],["準備","終端","模型","傳播","上傳"]):
                if v:a.barh(0,v,left=start,height=.5,color=COL[c],edgecolor=COL['line'],label=l)
                start+=v
            a.axvline(45,ls='--',color='#a56c28');a.set(yticks=[0],yticklabels=[["端側","附近","雲端"][i]],xlabel="剩餘二十輪完成時間（s）",xlim=(0,68),ylim=(-.6,1.6));a.legend(ncol=3,frameon=False,loc='upper left');save(f,'14-budgets' if i==0 else 'budgets-'+str(i))
        d=data['12-15'];f,a=plot(4.0);b=np.array(d['scan_Mbps']);a.plot(b,d['cloud_seconds'],color='#267398',label="雲端 H100");a.axhline(d['near_s'],color='#388768',label=f"附近 RTX PRO 6000：{d['near_s']:.1f} s");a.axhline(d['deadline_s'],ls='--',color='#a56c28',label=f"期限：{d['deadline_s']:g} s");a.set(xlabel="雲上行（Mbit/s）",ylabel="二十輪完成時間（s）",ylim=(0,80));a.legend(frameon=False);save(f,'15-deployment')
        for retained,name in [(True,'16-recovery'),(False,'recovery-all')]:
            rc=data['12-16']['round_s'];f,a=canvas(4.2);text(a,.04,.94,f'雲端已執行十輪，每輪 {rc:.2f} s；恢復連線需 1 s',14)
            for i in range(10):box(a,.04+i%5*.187,.66-(i//5)*.22,.17,.15,str(i+1),'green' if retained and i<9 else 'orange',12)
            text(a,.5,.22,"保留前九輪，只重做第十輪" if retained else "進度丟失，重做十輪",12,ha='center');text(a,.5,.08,f'額外 1 + {rc:.2f} = {1+rc:.2f} s' if retained else f'額外 1 + 10 × {rc:.2f} ≈ {1+10*rc:.1f} s',12,ha='center');save(f,name)
    from core_principles_figures import draw as draw_principles
    draw_principles(12, out)
    draw_local_tiers(out,data);draw_loss_repair(out,data)
    out.finish();return out.outputs,out.checks
