"""Model-led cross-generation diagrams; all quantitative labels use calculate.py."""
from pathlib import Path
import json, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from figure_style import STYLE,COL,canvas,plot,text,box,arrow,Exporter
from figure_style.typography import configure_font
ROOT=Path(__file__).resolve().parents[2]

def draw(here):
    r=json.loads((ROOT/'calculations/research/architecture-evolution-quantitative/result.json').read_text())
    out=Exporter(here)
    with plt.rc_context(STYLE):
        f,axs=plt.subplots(2,1,figsize=(420/72,4.6));f.subplots_adjust(left=.26,right=.86,hspace=.95,top=.90,bottom=.13)
        for a,m,unit,factor in [(axs[0],4096,'ms',1),(axs[1],1,'μs',1000)]:
            rows=[v for v in r['volta'] if v['rows']==m];vals=[v['compute_ms']*factor for v in rows]+[rows[0]['memory_ms']*factor]
            a.barh(range(3),vals,color=[COL['orange'],COL['green'],COL['blue']],edgecolor=COL['line']);a.set_yticks(range(3),["普通 FP32",'Tensor Core',"資料傳輸"]);a.invert_yaxis();a.set_xlim(0,max(vals)*1.23);a.set_xlabel("資源服務時間（"+unit+'）');a.set_title(f'{m:,} 行輸入',fontsize=14);a.spines[['top','right']].set_visible(False)
            for i,v in enumerate(vals):a.text(v+max(vals)*.035,i,f'{v:.3g}',va='center',fontsize=11)
        out.save(f,'figure-4-evolution-tensor-budget')

        f,a=plot(3.7,left=.24,bottom=.20)
        for i,key,label,c in [(0,'read_us_4090','RTX 4090','blue'),(1,'read_us_5090','RTX 5090','orange')]:
            vals=[v[key] for v in r['formats']];ys=[j+(i-.5)*.32 for j in range(3)]
            a.barh(ys,vals,height=.28,color=COL[c],edgecolor=COL['line'],label=label)
            for y,v in zip(ys,vals):a.text(v+.6,y,f'{v:.2f}',va='center',fontsize=11)
        a.set_yticks(range(3),[f"{z['format']}\n{z['MiB']:g} MiB" for z in r['formats']]);a.invert_yaxis();a.set_xlim(0,41);a.set_xlabel("同一權重讀取時間（μs）");a.legend(frameon=False,loc='lower right',fontsize=11)
        out.save(f,'figure-4-evolution-precision')

        f,a=canvas(4.4)
        for y,label,loader,acc in [(.72,'Ampere',"非同步複製","暫存器"),(.42,'Hopper',"TMA 搬移","暫存器"),(.12,'Blackwell SM100',"TMA 搬移",'TMEM')]:
            text(a,.03,y+.21,label,14)
            for x,w,t,c in [(.03,.20,loader,'blue'),(.29,.20,"共享記憶體",'blue'),(.55,.19,"矩陣單元",'orange'),(.80,.18,acc,'purple')]:box(a,x,y,w,.14,t,c,11)
            for x1,x2 in [(.23,.29),(.49,.55),(.74,.80)]:arrow(a,(x1,y+.07),(x2,y+.07))
        text(a,.5,.02,"輸入塊 32 KiB；輸出累加狀態 64 KiB",12,ha='center')
        out.save(f,'figure-4-evolution-nvidia-path')

        c=r['conv'];f,a=canvas(4.3)
        text(a,.03,.95,"56 × 56 × 64 輸入，3 × 3 卷積",14)
        box(a,.03,.74,.30,.12,f"輸入\n{c['input_bytes']/2**20:.3f} MiB",'blue',11)
        box(a,.45,.70,.52,.20,f"HBM 展開矩陣\n{c['expanded_bytes']/2**20:.3f} MiB（9 倍）",'purple',12)
        arrow(a,(.33,.80),(.45,.80));text(a,.36,.89,"展開",11,ha='center')
        box(a,.65,.49,.32,.12,"矩陣乘法",'orange',12);arrow(a,(.81,.70),(.81,.61))
        text(a,.03,.58,"顯式展開：先寫出，再讀入",12)
        text(a,.03,.34,"MTE 在片上組織視窗",14)
        for x,label,color in [(.03,"原始輸入",'blue'),(.37,'img2col','green'),(.71,'Cube','orange')]:box(a,x,.16,.26,.12,label,color,12)
        arrow(a,(.29,.22),(.37,.22));arrow(a,(.63,.22),(.71,.22))
        text(a,.5,.045,f"省去 HBM 寫讀 {c['explicit_expansion_roundtrip_bytes']/2**20:.3f} MiB ≈ {c['saved_hbm_service_us_at_1_2TBs']:.2f} μs",11,ha='center')
        out.save(f,'figure-4-evolution-img2col')

        f,a=canvas(4.6)
        text(a,.03,.95,"910A：同核分工，MTE 支援 img2col",14)
        box(a,.03,.73,.94,.15,'','gray')
        for x,t,c in [(.06,'Cube','orange'),(.40,"區域性緩衝",'blue'),(.74,'Vector','green')]:box(a,x,.75,.20,.11,t,c,11)
        arrow(a,(.26,.805),(.40,.805));arrow(a,(.60,.805),(.74,.805))
        text(a,.03,.65,"910B / 910C：矩陣、向量獨立控制",14)
        for x,w,t,c in [(.03,.23,'AIC','orange'),(.35,.30,"全域地址交換\n經過快取層次",'blue'),(.74,.23,'AIV','green')]:box(a,x,.43,w,.15,t,c,11)
        arrow(a,(.26,.505),(.35,.505));arrow(a,(.65,.505),(.74,.505))
        text(a,.03,.34,"950：增強 Vector，增加 CV 直連",14)
        box(a,.03,.11,.34,.15,'Cube Core\nL1 Buffer','orange',11);box(a,.63,.11,.34,.15,"Vector Core\nUB + 暫存器",'green',11)
        arrow(a,(.37,.215),(.63,.215));arrow(a,(.63,.155),(.37,.155));text(a,.50,.28,"CV 直連",11,ha='center')
        text(a,.5,.035,"矩陣與向量之間的交接留在更近的通路",11,ha='center')
        out.save(f,'figure-4-evolution-ascend')

        f,a=canvas(4.4)
        text(a,.03,.94,"QK → Softmax → PV：兩次交接",14)
        box(a,.03,.71,.26,.13,"Cube\n64 KiB 分數",'orange',11);box(a,.71,.71,.26,.13,"Vector\n64 KiB 機率",'green',11)
        box(a,.36,.66,.28,.22,"外層介面\n寫 + 讀 × 2\n256 KiB",'blue',11)
        arrow(a,(.29,.79),(.36,.79));arrow(a,(.64,.79),(.71,.79));arrow(a,(.71,.735),(.64,.70));arrow(a,(.36,.70),(.29,.735))
        text(a,.5,.56,"94 GB/s 時佔用介面約 2.79 μs",12,ha='center')
        box(a,.03,.28,.29,.14,'Cube L1','orange',12);box(a,.68,.28,.29,.14,'Vector UB','green',12)
        arrow(a,(.32,.385),(.68,.385));arrow(a,(.68,.31),(.32,.31));text(a,.5,.465,'CV：64 KiB + 64 KiB',11,ha='center')
        text(a,.5,.19,"要在 1.024 μs 內交接，CV 需 128 GB/s",11,ha='center')
        text(a,.5,.065,"外層介面釋放 256 KiB；直接通路承擔 128 KiB",11,ha='center')
        out.save(f,'figure-4-evolution-cv-budget')

        f,a=canvas(4.7)
        box(a,.03,.85,.94,.12,"統一記憶體：權重、KV 與中間資料",'blue',12)
        for x,w,label,c in [(.03,.19,'CPU','gray'),(.29,.39,'GPU','green'),(.74,.23,"獨立 Neural\nEngine",'orange')]:box(a,x,.62,w,.15,label,c,11);arrow(a,(x+w/2,.85),(x+w/2,.77))
        text(a,.03,.53,"GPU 內部的演進",14)
        for y,gen,left,right in [(.33,'M3 / M4',"通用計算",'Dynamic\nCaching'),(.10,'M5',"通用計算 +\nNeural Accelerator","第二代\nDynamic Caching")]:
            text(a,.03,y+.085,gen,12);box(a,.25,y,.42,.17,left,'orange' if gen=='M5' else 'green',11);box(a,.72,y,.25,.17,right,'blue',11);arrow(a,(.72,y+.085),(.67,y+.085))
        out.save(f,'figure-4-evolution-apple')

        f,axs=plt.subplots(2,1,figsize=(420/72,5.2));f.subplots_adjust(left=.25,right=.90,top=.91,bottom=.10,hspace=.90)
        ids=['rtx3090','rtx4090','rtx5090','a100-80gb-sxm','h100-sxm','m3-ultra-80gpu-256gb'];labels=['RTX 3090','RTX 4090','RTX 5090','A100 SXM','H100 SXM','M3 Ultra']
        vals=[next(x['read_ms'] for x in r['decode'] if x['device']==id and x['workload']=='qwen3-8b-b1-h8191-w16-balanced') for id in ids]
        for a,names,values,title,xlabel in [(axs[0],labels,vals,"8K 單請求 decode","主要載荷讀取下界（ms）"),(axs[1],labels[:-1],[next(x['prefill_matrix_ms'] for x in r['qwen_compute'] if x['device']==id) for id in ids[:-1]],"4K 輸入 prefill","矩陣計算下界（ms）")]:
            a.barh(range(len(values)),values,color=COL['blue'] if a==axs[0] else COL['orange'],edgecolor=COL['line']);a.set_yticks(range(len(values)),names);a.invert_yaxis();a.set_xlim(0,max(values)*1.24);a.set_xlabel(xlabel);a.set_title(title,fontsize=14);a.spines[['top','right']].set_visible(False)
            for y,v in enumerate(values):a.text(v+max(values)*.03,y,f'{v:.1f}',va='center',fontsize=11)
        out.save(f,'figure-4-evolution-convergence')
    (Path(here)/'evolution-layout-validation.json').write_text(json.dumps(out.checks,ensure_ascii=False,indent=2)+'\n')
    return out.outputs

if __name__=='__main__':
    _,family=configure_font();plt.rcParams['font.family']=[family,'DejaVu Sans'];draw(Path(__file__).resolve().parent)
