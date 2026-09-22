"""V4/V4.1 conversation diagrams in the shared Hands-On book style."""
from pathlib import Path
import json
import matplotlib.pyplot as plt
from figure_style import COL,STYLE,canvas,plot,text,box,arrow
ROOT=Path(__file__).resolve().parents[1]

def draw(ch,out):
    data=json.loads((ROOT/'calculations/results/v41-throughline.json').read_text())
    with plt.rc_context(STYLE):
        if ch==2:
            f,a=canvas(5.5)
            box(a,.05,.82,.90,.11,"提示 token → 編碼器 20 層",'blue')
            box(a,.05,.53,.40,.16,"編碼器末層表示\n投影為全域 KV",'green')
            box(a,.56,.53,.39,.16,"提示末尾 ≤128 token\n取編碼器輸出",'orange',11)
            arrow(a,(.25,.82),(.25,.69));arrow(a,(.75,.82),(.75,.69))
            box(a,.56,.25,.39,.16,"解碼器 20 層重放\n構建區域性 SWA",'orange',11)
            arrow(a,(.75,.53),(.75,.41));arrow(a,(.45,.61),(.56,.33))
            text(a,.26,.34,"全域 KV 供解碼器讀取",11,ha='center')
            box(a,.05,.04,.90,.12,"生成新 token：編碼器 → 解碼器 → 輸出",'purple',11)
            arrow(a,(.75,.25),(.75,.16))
            out.save(f,'figure-2-v41-ced-path')
            f,a=canvas(5.1)
            text(a,.245,.95,"V4：逐層儲存",14,ha='center');text(a,.755,.95,"V4.1：跨層共享",14,ha='center')
            for i in range(3):
                y=.69-i*.23
                box(a,.02,y,.20,.14,f'層 {i+1}\n代表層','orange')
                box(a,.29,y,.18,.14,"本層\n全域 KV",'blue');arrow(a,(.29,y+.07),(.22,y+.07))
            for i,(label,users) in enumerate([("層 2\n2:1","層 3–7"),("層 8\n2:1","層 9–13"),("層 14\n2:1","層 15–19"),("層 20\n1:1","層 21–39")]):
                y=.73-i*.18
                box(a,.54,y,.19,.13,label,'blue',11)
                box(a,.80,y,.18,.13,users,'green',11)
                arrow(a,(.73,y+.065),(.80,y+.065))
            text(a,.76,.105,"各層獨立 Q 與區域性 SWA",11,ha='center')
            text(a,.5,.025,"層編號從 0 開始；僅示意狀態與讀取",11,ha='center')
            out.save(f,'figure-2-v41-sharing')
            f,a=canvas(5.0)
            box(a,.10,.79,.80,.14,"Full：掃描全域歷史",'blue')
            box(a,.10,.55,.80,.14,"候選池：最多 16,384 個條目",'green')
            box(a,.10,.31,.80,.14,"Reindex：在池內重選 512 個",'orange')
            box(a,.10,.07,.80,.14,"Reuse：使用已有條目選擇",'purple')
            arrow(a,(.88,.79),(.88,.69))
            for y in [.55,.31]:arrow(a,(.5,y),(.5,y-.10))
            text(a,.5,.735,"選塊，每塊含 8 個快取條目",11,ha='center')
            out.save(f,'figure-2-v41-selection')
        elif ch==3:
            f,a=canvas(4.8)
            text(a,.04,.94,"從空狀態處理 8K 輸入",14)
            box(a,.04,.73,.92,.12,"普通全層：8,192 token × 40 層",'blue')
            box(a,.04,.46,.60,.15,"CED 編碼器\n8,192 token × 20 層",'blue')
            box(a,.71,.46,.25,.15,"區域性重放\n128 × 20",'orange')
            text(a,.5,.36,"327,680 → 166,400 token 層",13,ha='center')
            box(a,.04,.12,.92,.15,"另計：全域 KV 投影、注意力及其他工作",'gray',11)
            text(a,.5,.04,"生成階段仍執行完整 40 層主幹",11,ha='center')
            out.save(f,'figure-3-v41-ced')
        elif ch==5:
            f,axes=plt.subplots(2,1,figsize=(420/72,5.3));f.subplots_adjust(left=.25,right=.94,top=.92,bottom=.13,hspace=.60)
            rows=data['cache_cases'][0]['models']
            for ax,key,title in [(axes[0],'global_history_bytes',"8K 全域 KV 駐留"),(axes[1],'decode_selected_history_read_bytes',"8K 注意力 KV 與索引讀取")]:
                vals=[r[key]/2**20 for r in rows]
                ax.spines[['top','right']].set_visible(False)
                ax.barh([1,0],vals,color=[COL['blue'],COL['green']],height=.48,edgecolor=COL['line'])
                for y,v in zip([1,0],vals):ax.text(v+.4,y,f'{v:.3f}',va='center',fontsize=11)
                ax.set(yticks=[1,0],yticklabels=['V4-Flash','V4.1 Flash'],xlim=(0,34),ylim=(-.65,1.7),xticks=[0,10,20,30],xlabel='MiB');ax.set_title(title,fontsize=13)
            out.save(f,'figure-5-v41-traffic')
        elif ch==8:
            f,a=canvas(5.9)
            text(a,.04,.95,"先判斷編碼器字首狀態",14)
            for y,left,right in [(.74,"全域與編碼器 SWA 命中","編碼器處理新輸入"),(.52,"僅全域 KV 命中","重放字首末尾視窗\n再處理新輸入"),(.30,"全域 KV 未命中","編碼器重算缺失字首\n再處理新輸入")]:
                box(a,.03,y,.44,.15,left,'blue',11)
                box(a,.58,y,.39,.15,right,'orange',11);arrow(a,(.47,y+.075),(.58,y+.075))
            text(a,.5,.23,"三條路徑都繼續執行",11,ha='center')
            box(a,.03,.055,.94,.12,"解碼器末尾視窗重放 → 構建 SWA → 生成",'purple',11)
            out.save(f,'figure-8-v41-recovery')
        elif ch==9:
            f,a=plot(4.1,left=.25,bottom=.20)
            route=data['routing'];transfer=route['remote_transfer_ms'];replay=route['remote_replay_ms']
            a.barh(2,10,height=.52,color=COL['gray'],edgecolor=COL['line']);a.barh(1,transfer,height=.52,color=COL['blue'],edgecolor=COL['line']);a.barh(1,replay,left=transfer,height=.52,color=COL['orange'],edgecolor=COL['line']);a.barh(0,20,height=.52,color=COL['gray'],edgecolor=COL['line'])
            a.text(10.4,2,'10 ms',va='center',fontsize=11);a.text(route['remote_ready_ms']+.4,1,'12.666 ms',va='center',fontsize=11);a.text(20.4,0,'20 ms',va='center',fontsize=11)
            a.text(2.3,1,"傳輸",ha='center',va='center',fontsize=11);a.text(8.7,1,"編碼器恢復",ha='center',va='center',fontsize=11)
            a.set(yticks=[2,1,0],yticklabels=["A：較短佇列","B：取回與恢復","A：較長佇列"],xlim=(0,26),ylim=(-.7,2.9),xlabel="兩條路徑不同的準備時間（ms）")
            out.save(f,'figure-9-v41-routing')
