"""Chapter 1: one question per book-size figure. Inputs come from build.py's locked evidence."""
import numpy as np
import matplotlib.pyplot as plt
from figure_style import COL, STYLE, canvas, plot, text, box, arrow, Exporter

def draw(here,data):
    out=Exporter(here)
    with plt.rc_context(STYLE):
        f,a=canvas(5.2)
        layers=[("應用與任務","要完成什麼，何時完成",'orange'),
                ("模型與負載","需要哪些計算和資料",'blue'),
                ("訓練與推理系統","安排請求、batch 和加速器",'green'),
                ("運算元與編譯執行時","把運算變成可執行程式",'purple'),
                ("處理器與儲存","計算並儲存資料",'blue'),
                ("互聯與資料中心","連線裝置，提供電力與散熱",'gray')]
        for i,(title,body,c) in enumerate(layers):
            y=.825-i*.153
            box(a,.06,y,.88,.125,title+'\n'+body,c)
            if i<5:arrow(a,(.5,y),(.5,y-.028))
        out.save(f,'figure-1-1-panorama')

        f,a=canvas(4.4)
        for x,label,c in [(.02,"應用\n組織輸入",'orange'),(.36,"服務入口\n接收請求",'gray'),(.70,"路由器\n選擇實例",'purple')]:
            box(a,x,.76,.28,.18,label,c)
        arrow(a,(.30,.85),(.36,.85));arrow(a,(.64,.85),(.70,.85))
        box(a,.02,.06,.96,.52,'','gray');text(a,.05,.53,"被選中的推理實例",14)
        box(a,.06,.17,.24,.22,"實例排程器\n組成 batch",'green')
        box(a,.38,.17,.24,.22,"CPU\n提交程式",'blue')
        box(a,.70,.17,.24,.22,"GPU\n執行運算",'orange')
        arrow(a,(.30,.28),(.38,.28));arrow(a,(.62,.28),(.70,.28))
        arrow(a,(.84,.76),(.84,.61));text(a,.49,.65,"請求進入實例",11,ha='center')
        out.save(f,'figure-1-2-request')

        f,a=canvas(3.7)
        box(a,.04,.82,.29,.13,"模型檔案",'gray');box(a,.04,.63,.92,.13,"視訊記憶體：儲存一份權重",'blue')
        arrow(a,(.18,.82),(.18,.76));text(a,.46,.875,"啟動時載入",11)
        for x,s in [(.05,"第 1 步"),(.37,"第 2 步"),(.69,"第 3 步")]:
            box(a,x,.20,.26,.23,s+"\n計算單元",'green')
            arrow(a,(x+.13,.63),(x+.13,.44))
        text(a,.50,.55,"每步從視訊記憶體讀取所需權重",12,ha='center')
        arrow(a,(.31,.31),(.37,.31));arrow(a,(.63,.31),(.69,.31))
        text(a,.5,.08,"前一步輸出成為下一步輸入",12,ha='center')
        out.save(f,'figure-1-weight-lifetime')

        f,a=canvas(4.8)
        box(a,.04,.77,.40,.17,"入口與共享儲存",'gray');box(a,.57,.77,.39,.17,"其他超節點",'purple')
        box(a,.20,.56,.60,.12,"資料中心網路",'green')
        arrow(a,(.24,.77),(.38,.68));arrow(a,(.76,.77),(.62,.68))
        box(a,.02,.025,.96,.44,'','gray');text(a,.05,.425,"放大一個超節點",14)
        box(a,.08,.27,.36,.11,"CPU 與主存",'blue');box(a,.61,.27,.31,.11,"網路卡",'green')
        arrow(a,(.5,.56),(.76,.39));arrow(a,(.44,.325),(.61,.325))
        for x in [.08,.61]:box(a,x,.07,.31,.13,"GPU 與視訊記憶體",'orange')
        arrow(a,(.235,.27),(.235,.20));arrow(a,(.765,.27),(.765,.20))
        arrow(a,(.39,.135),(.61,.135));text(a,.50,.235,"內部互聯",11,ha='center')
        out.save(f,'figure-1-3-datacenter')

        f,a=plot(3.4,left=.29)
        names=["主存存取","機房內往返","磁碟尋道"]; vals=[100,500000,10000000]
        a.barh(names,vals,color=[COL['blue'],COL['green'],COL['orange']],edgecolor=COL['line'],height=.5)
        a.set_xscale('log');a.set_xlim(10,1e8);a.set_xlabel("時間（ns，對數刻度）");a.invert_yaxis()
        for i,(v,label) in enumerate(zip(vals,['0.1 μs','0.5 ms','10 ms'])):a.text(v*1.35,i,label,va='center',fontsize=12)
        out.save(f,'figure-1-4-numbers')

        capacity=data['capacity_example']
        bf16=capacity['bf16_weight_bytes']/1e9
        int8=capacity['int8_weight_and_metadata_bytes']/1e9
        f,a=plot(3.5,left=.25)
        for y,v,c in [(3,bf16,'orange'),(2,bf16/2,'blue'),(1,bf16/2,'blue'),(0,int8,'green')]:
            a.barh(y,v,height=.55,color=COL[c],edgecolor=COL['line'])
            a.text(6,y,f'{v:.2f} GB',va='center',fontsize=12)
        a.axvline(80,color='#80542e',ls='--',lw=1);a.text(82,3.65,"單卡容量 80 GB",fontsize=11)
        a.axhline(.5,color='#999999',lw=.7)
        a.set(yticks=[3,2,1,0],yticklabels=["BF16 單卡","BF16 卡 0","BF16 卡 1","8 位元單卡"],
              xlim=(0,190),ylim=(-.55,4.05),xlabel="權重及量化附加資料（GB）",xticks=[0,40,80,120,160])
        out.save(f,'figure-1-capacity-path')

        f,a=canvas(3.0)
        box(a,.04,.58,.37,.24,"視訊記憶體\n70 GB 權重",'blue');box(a,.61,.58,.35,.24,"計算單元\n完成乘加",'green')
        arrow(a,(.41,.70),(.61,.70));text(a,.5,.45,"讀取路徑：3350 GB/s",12,ha='center')
        text(a,.5,.25,'70 GB ÷ 3350 GB/s ≈ 20.90 ms',14,ha='center')
        text(a,.5,.09,"每參數一位元組，每步完整讀取一遍",11,ha='center')
        out.save(f,'figure-1-read-path')

        f,a=plot(3.7,left=.25)
        comp=data['teaching']['compute_ms'];mem=data['teaching']['weight_read_ms']
        labels=["原加速器","算力翻倍","頻寬翻倍"];y=np.arange(3)
        a.barh(y+.16,[mem,mem,mem/2],height=.29,color=COL['blue'],edgecolor=COL['line'],label="讀取權重")
        a.barh(y-.16,[comp,comp/2,comp],height=.29,color=COL['orange'],edgecolor=COL['line'],label="矩陣計算")
        for i,v in enumerate([mem,mem,mem/2]):a.text(v+.4,i+.16,f'{v:.2f}',fontsize=12,va='center')
        a.set(yticks=y,yticklabels=labels,xlim=(0,25),xlabel="資源時間下界（ms）");a.invert_yaxis();a.legend(loc='lower right',frameon=False)
        out.save(f,'figure-1-5-budget')

        f,a=canvas(3.5)
        text(a,.04,.91,"同一份權重，為八個請求服務",14)
        box(a,.04,.64,.92,.15,"一次讀取：70 GB 權重",'blue')
        for i in range(8):
            x=.04+i*.117;box(a,x,.24,.105,.18,str(i+1),'green');arrow(a,(x+.052,.63),(x+.052,.43))
        text(a,.5,.52,"八條輸入各自完成運算",12,ha='center')
        text(a,.5,.10,"整批約 20.90 ms；每輸出 token 分攤約 2.61 ms",12,ha='center')
        out.save(f,'figure-1-batch-reuse')

        d=data['teaching_diagrams']['batch_transition'];b=np.array(d['batch'])
        f,a=plot(3.8)
        a.plot(b,comp*b,color='#a96c28',label="矩陣計算");a.axhline(mem,color='#267398',label="權重讀取")
        a.plot(b,np.maximum(comp*b,mem),color='#333333',ls='--',label="兩者最大值")
        a.axvline(d['crossing_batch'],color='#777777',ls=':',lw=1)
        a.text(156,mem+4,"約 148",fontsize=12);a.set(xlim=(0,512),ylim=(0,80),xlabel="批內請求數 B",ylabel="時間下界（ms）")
        a.legend(loc='upper left',frameon=False);out.save(f,'figure-1-batch-transition')
        f,a=plot(3.4)
        a.plot(b,d['throughput'],color='#267398',lw=1.8);a.axvline(d['crossing_batch'],ls=':',color='#777777')
        a.set(xlim=(0,512),ylim=(0,8000),xlabel="批內請求數 B",ylabel="輸出吞吐（token/s）")
        a.text(180,6200,"計算項開始主導",fontsize=12);out.save(f,'figure-1-batch-throughput')

        rows=data['measured_short_group']
        for key,ylabel,name in [('throughput',"整批輸出吞吐（token/s）",'figure-1-measured-throughput'),('tpot_ms',"每請求輸出間隔（ms）",'figure-1-measured-tpot')]:
            f,a=plot(3.3)
            vals=[r[key] for r in rows];a.plot(range(4),vals,'o-',color='#267398',lw=1.5)
            for i,v in enumerate(vals):a.annotate(f'{v:.2f}',(i,v),xytext=(0,10),textcoords='offset points',ha='center',fontsize=11)
            a.set(xlim=(-.45,3.45),ylim=(0,max(vals)*1.23),xticks=range(4),xticklabels=[r['batch'] for r in rows],xlabel="同時請求數（各檔等距排列）",ylabel=ylabel)
            out.save(f,name)

        for slug,title,items in [
            ('tpu',"增加專用計算與資料搬移資源",[("輸入緩衝",'blue'),("矩陣計算陣列",'orange'),("輸出緩衝",'green')]),
            ('smartnic',"把包處理放到資料經過的位置",[("網路資料",'blue'),("可程式設計網路卡\n完成包處理",'orange'),("主機 CPU\n執行應用",'green')]),
            ('ub',"讓多臺裝置直接交換所需資料",[("裝置 0\n計算與儲存",'blue'),("統一互聯\n傳遞資料",'green'),("裝置 1\n計算與儲存",'orange')])]:
            f,a=canvas(2.5);text(a,.04,.89,title,14)
            for i,(label,c) in enumerate(items):
                x=.03+.335*i;box(a,x,.30,.27,.34,label,c)
                if i<2:arrow(a,(x+.27,.47),(x+.335,.47))
            out.save(f,'figure-1-design-'+slug)
    from core_principles_figures import draw as draw_principles
    draw_principles(1, out)
    return out.finish()
