"""Mechanism diagrams derived from chapter-eight teaching examples."""
import json
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def draw(save, canvas, box, arrow, C, data):
    worked=json.loads((Path(__file__).resolve().parent/'teaching-validation.json').read_text())
    # Keep the timeline proportional; annotate short intervals outside the bar.
    f,a=plt.subplots(figsize=(11,3.8))
    f.subplots_adjust(left=.08,right=.96,bottom=.22,top=.88)
    queue,prefill,itl=.1,.096,.0265;first=queue+prefill;last=first+255*itl
    for x,w,c in [(0,queue,'gray'),(queue,prefill,'blue'),(first,255*itl,'teal')]:
        a.add_patch(Rectangle((x,.35),w,.28,fc=C[c],ec='white'))
    a.text((first+last)/2,.49,"255 個輸出間隔 × 26.5 ms = 6.76 s",ha='center',va='center',color='white',fontsize=13)
    a.annotate("排隊 0.1 s",xy=(.05,.63),xytext=(.05,1.00),arrowprops={'arrowstyle':'-','color':C['ink']},fontsize=11)
    a.annotate('Prefill 0.096 s',xy=(.148,.63),xytext=(.6,.81),arrowprops={'arrowstyle':'-','color':C['blue']},fontsize=11,color=C['blue'])
    a.scatter([first,last],[.35,.35],color=C['ink'],zorder=5)
    a.text(first,.22,"首 token\n0.196 s",ha='center',va='top',fontsize=11)
    a.text(last-.25,.22,"末 token\n6.95 s",ha='center',va='top',fontsize=11)
    a.axvline(7,color=C['red'],ls='--',lw=1.4)
    a.text(7.05,.90,"7 s 時限",color=C['red'],fontsize=11)
    a.set(xlim=(0,7.8),ylim=(-.18,1.15),yticks=[],xticks=[0,1,2,3,4,5,6,7],xlabel="自請求到達起 / s")
    a.spines['left'].set_visible(False)
    data['lifecycle']={'queue_s':queue,'prefill_s':prefill,'output_intervals':255,'interval_s':itl,'completion_s':last,'deadline_s':7,'source':'experiments/ch08/08-01/results/summary.json'}
    save(f,'figure-8-1-lifecycle')

    # Equal-sized cells show the rectangle + triangle decomposition exactly.
    f,axs=plt.subplots(2,1,figsize=(11,6.5))
    f.subplots_adjust(left=.12,right=.96,bottom=.13,top=.91,hspace=.85)
    pairs=[]
    for a,h in zip(axs,[0,8]):
        for row in range(4):
            for col in range(h+4):
                color=C['teal'] if col<h else C['blue'] if col<=h+row else C['gray']
                a.add_patch(Rectangle((col,row),1,1,fc=color,ec='white',lw=1.5))
        a.set(xlim=(-.05,12.05),ylim=(4.1,-.1),aspect='equal',yticks=[.5,1.5,2.5,3.5],yticklabels=["新 1","新 2","新 3","新 4"],xticks=[])
        a.tick_params(length=0);a.spines[['left','bottom']].set_visible(False)
        a.set_title(f'歷史 {h} 個位置：'+("10 個塊內配對" if h==0 else "32 個歷史配對 + 10 個塊內配對 = 42"),loc='left',fontsize=12,pad=12)
        a.text(h+2,4.65,"本塊的 4 個鍵位置",ha='center',fontsize=11)
        if h:a.text(h/2,4.65,"8 個舊歷史鍵位置",ha='center',fontsize=11)
        pairs.append({'history':h,'new':4,'history_pairs':4*h,'within_pairs':10,'total_pairs':4*h+10})
    f.text(.5,.035,"綠：存取舊歷史    藍：塊內因果存取    灰：未來位置，不存取",ha='center',fontsize=11)
    data['attention_geometry']=pairs;save(f,'figure-8-4-attention')

    f,a=canvas(4.5)
    a.text(.04,.93,"同樣的 864 MiB，可以怎樣使用？",fontsize=15,weight='bold')
    box(a,.06,.58,.63,.19,'A：864 MiB',col='blue')
    va=round(worked['cache']['A_gen5'][2]*1e3,1);vb=round(worked['cache']['B_gen5'][2]*1e3,1)
    a.text(.76,.675,f'共節省 {va} ms',va='center',fontsize=14,color=C['blue'])
    for i in range(3):box(a,.06+i*.21,.20,.203,.23,f'B{i+1}：288 MiB',f'節省 {vb} ms',size=12)
    a.text(.76,.315,f'共節省 {3*vb:.1f} ms',va='center',fontsize=14,color=C['teal'])
    data['cache_choice']={'capacity_mib':864,'A':{'size_mib':864,'net_ms':worked['cache']['A_gen5'][2]*1e3},'B':{'count':3,'each_mib':288,'each_net_ms':worked['cache']['B_gen5'][2]*1e3},'link':'PCIe Gen5 x16, 64 GB/s per direction'}
    save(f,'figure-8-7-cache-choice')

    f,a=plt.subplots(figsize=(11,4.8))
    f.subplots_adjust(left=.13,right=.93,bottom=.18,top=.93)
    for y,name,payload,metadata in [(2,'BF16',64,0),(1,'q8_0',32,2),(0,'q4_0',16,2)]:
        a.barh(y,payload,height=.5,color=C['blue'])
        a.text(payload/2,y,f'{payload} bytes',ha='center',va='center',color='white',fontsize=12)
        if metadata:
            a.barh(y,metadata,left=payload,height=.5,color=C['orange'])
            a.annotate("縮放係數 2 bytes",xy=(payload+1,y+.25),xytext=(payload+7,y+.39),fontsize=10,arrowprops={'arrowstyle':'-','color':C['orange']})
        a.text(payload+metadata+1,y,f'共 {payload+metadata}',va='center',fontsize=11)
    a.set(xlim=(0,73),ylim=(-.65,2.6),yticks=[0,1,2],yticklabels=['q4_0','q8_0','BF16'],xticks=[0,16,32,48,64],xlabel="同一組 32 個值佔用的位元組數")
    a.spines['left'].set_visible(False);a.tick_params(axis='y',length=0)
    data['kv_layout']={'values_per_group':32,'payload_bytes':[64,32,16],'scale_bytes':[0,2,2],'total_bytes':[64,34,18]}
    save(f,'figure-8-8-kv-format')

    f,a=canvas(5.8)
    xs=[.23,.40,.57,.74]
    for x,label in zip(xs,["位置 1","位置 2","位置 3","位置 4"]):a.text(x+.055,.94,label,ha='center',fontsize=11)
    for y,label in [(.70,"草稿"),(.41,"目標驗證"),(.10,"最終輸出")]:a.text(.035,y+.075,label,va='center',fontsize=13)
    for x,token in zip(xs,['a','b','c','d']):box(a,x,.70,.11,.15,token,size=16)
    for x,token,col in zip(xs,['a','b','x',"丟棄"],['teal','teal','orange','gray']):
        box(a,x,.41,.11,.15,token,col=col,size=15)
        arrow(a,(x+.055,.69),(x+.055,.58),col='orange' if token=='x' else 'gray' if token=='丢弃' else 'teal')
    for x,token,col in zip(xs,['a','b','x'],['teal','teal','orange']):
        box(a,x,.10,.11,.15,token,col=col,size=16)
        arrow(a,(x+.055,.40),(x+.055,.27),col=col)
    a.text(.625,.635,"第三處不匹配",ha='center',fontsize=11,color=C['orange'],bbox={'fc':'white','ec':'none','pad':1})
    a.text(.83,.31,"後續依賴 c\n不再採用",ha='center',fontsize=11,color=C['ink'])
    a.text(.78,.06,"保留 2 個 + 修正 1 個 = 3 個輸出",ha='center',fontsize=11)
    data['verification_example']={'draft':['a','b','c','d'],'first_mismatch':3,'replacement':'x','output':['a','b','x'],'accepted_draft_count':2}
    save(f,'figure-8-11-verification')

    f,a=plt.subplots(figsize=(10,6.2))
    f.subplots_adjust(left=.11,right=.97,bottom=.16,top=.91)
    a.add_patch(Rectangle((0,0),12,7,fc='#e5f2ec',ec='none'))
    a.axvline(12,ls='--',color=C['orange'],lw=1.5);a.axhline(7,ls='--',color=C['red'],lw=1.5)
    a.text(12.3,1.2,"12 GiB 上限",color=C['orange'],fontsize=11)
    a.text(.4,7.25,"7 s 時限",color=C['red'],fontsize=11)
    labels={'A':"記憶體不足",'B':"共享，超時",'C':"超時",'D':"共享 + 推測"}
    rows=[(r['name'],r['memory_gib'],r['time_s'],labels[r['name']]) for r in worked['design_candidates'] if r['name'] in labels]
    for name,mem,t,label in rows:
        ok=mem<=12 and t<=7;col=C['teal'] if ok else C['red']
        a.scatter(mem,t,s=85,facecolors=col if ok else 'white',edgecolors=col,lw=1.8,zorder=4)
        offset={'A':(-95,-40),'B':(10,8),'C':(10,-38),'D':(10,-30)}[name]
        a.annotate(f'{name}：{label}\n{mem:.2f} GiB，{t:.2f} s',xy=(mem,t),xytext=offset,textcoords='offset points',fontsize=11,color=col)
    a.text(1,2.0,"記憶體足夠且按期完成",fontsize=13,color=C['teal'])
    a.set(xlim=(0,21),ylim=(0,16.5),xlabel="KV 與輔助緩衝區 / GiB",ylabel="整批請求總耗時 / s",xticks=[0,6,12,18],yticks=[0,3,6,7,9,12,15]);a.grid(alpha=.12)
    data['design_plane']={'capacity_gib':12,'deadline_s':7,'device':'rtx-pro6000-blackwell-ws','configurations':[{'name':r[0],'memory_gib':r[1],'time_s':r[2]} for r in rows]}
    save(f,'figure-8-14-design')
