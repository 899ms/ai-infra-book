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
            box(a,.05,.82,.90,.11,"prompt tokens → encoder 20 layers",'blue')
            box(a,.05,.53,.40,.16,"encoder final-layer representation\nprojected to global KV",'green')
            box(a,.56,.53,.39,.16,"prompt tail ≤128 tokens\ntakes encoder output",'orange',11)
            arrow(a,(.25,.82),(.25,.69));arrow(a,(.75,.82),(.75,.69))
            box(a,.56,.25,.39,.16,"decoder 20-layer replay\nbuilds local SWA",'orange',11)
            arrow(a,(.75,.53),(.75,.41));arrow(a,(.45,.61),(.56,.33))
            text(a,.26,.34,"global KV for decoder read",11,ha='center')
            box(a,.05,.04,.90,.12,"generate new token: encoder → decoder → output",'purple',11)
            arrow(a,(.75,.25),(.75,.16))
            out.save(f,'figure-2-v41-ced-path')
            f,a=canvas(5.1)
            text(a,.245,.95,"V4: layer-by-layer save",14,ha='center');text(a,.755,.95,"V4.1: cross-layer sharing",14,ha='center')
            for i in range(3):
                y=.69-i*.23
                box(a,.02,y,.20,.14,f'Layer {i+1}\nrepresentative layer','orange')
                box(a,.29,y,.18,.14,"this layer\nglobal KV",'blue');arrow(a,(.29,y+.07),(.22,y+.07))
            for i,(label,users) in enumerate([("Layer 2\n2:1","Layer 3–7"),("Layer 8\n2:1","Layer 9–13"),("Layer 14\n2:1","Layer 15–19"),("Layer 20\n1:1","Layer 21–39")]):
                y=.73-i*.18
                box(a,.54,y,.19,.13,label,'blue',11)
                box(a,.80,y,.18,.13,users,'green',11)
                arrow(a,(.73,y+.065),(.80,y+.065))
            text(a,.76,.105,"per-layer independent Q and local SWA",11,ha='center')
            text(a,.5,.025,"layer index starts at 0; state and reads shown schematically",11,ha='center')
            out.save(f,'figure-2-v41-sharing')
            f,a=canvas(5.0)
            box(a,.10,.79,.80,.14,"Full: scan global history",'blue')
            box(a,.10,.55,.80,.14,"candidate pool: up to 16,384 entries",'green')
            box(a,.10,.31,.80,.14,"Reindex: reselect 512 within pool",'orange')
            box(a,.10,.07,.80,.14,"Reuse: select from existing entries",'purple')
            arrow(a,(.88,.79),(.88,.69))
            for y in [.55,.31]:arrow(a,(.5,y),(.5,y-.10))
            text(a,.5,.735,"select block, 8 cache entries each",11,ha='center')
            out.save(f,'figure-2-v41-selection')
        elif ch==3:
            f,a=canvas(4.8)
            text(a,.04,.94,"Process 8K input from empty state",14)
            box(a,.04,.73,.92,.12,"Standard full layers: 8,192 tokens × 40 layers",'blue')
            box(a,.04,.46,.60,.15,"CED encoder\n8,192 tokens × 20 layers",'blue')
            box(a,.71,.46,.25,.15,"Local replay\n128 × 20",'orange')
            text(a,.5,.36,"327,680 → 166,400 token layer",13,ha='center')
            box(a,.04,.12,.92,.15,"Separately: global KV projection, attention, and other work",'gray',11)
            text(a,.5,.04,"Generation still runs full 40-layer backbone",11,ha='center')
            out.save(f,'figure-3-v41-ced')
        elif ch==5:
            f,axes=plt.subplots(2,1,figsize=(420/72,5.3));f.subplots_adjust(left=.25,right=.94,top=.92,bottom=.13,hspace=.60)
            rows=data['cache_cases'][0]['models']
            for ax,key,title in [(axes[0],'global_history_bytes',"8K global KV resident"),(axes[1],'decode_selected_history_read_bytes',"8K attention KV and index read")]:
                vals=[r[key]/2**20 for r in rows]
                ax.spines[['top','right']].set_visible(False)
                ax.barh([1,0],vals,color=[COL['blue'],COL['green']],height=.48,edgecolor=COL['line'])
                for y,v in zip([1,0],vals):ax.text(v+.4,y,f'{v:.3f}',va='center',fontsize=11)
                ax.set(yticks=[1,0],yticklabels=['V4-Flash','V4.1 Flash'],xlim=(0,34),ylim=(-.65,1.7),xticks=[0,10,20,30],xlabel='MiB');ax.set_title(title,fontsize=13)
            out.save(f,'figure-5-v41-traffic')
        elif ch==8:
            f,a=canvas(5.9)
            text(a,.04,.95,"First check encoder prefix state",14)
            for y,left,right in [(.74,"Global and encoder SWA hit","Encoder processes new input"),(.52,"Global KV hit only","Replay prefix end window\nthen process new input"),(.30,"Global KV miss","Encoder recomputes missing prefix\nthen processes new input")]:
                box(a,.03,y,.44,.15,left,'blue',11)
                box(a,.58,y,.39,.15,right,'orange',11);arrow(a,(.47,y+.075),(.58,y+.075))
            text(a,.5,.23,"All three paths continue",11,ha='center')
            box(a,.03,.055,.94,.12,"Decoder end-window replay → build SWA → generate",'purple',11)
            out.save(f,'figure-8-v41-recovery')
        elif ch==9:
            f,a=plot(4.1,left=.25,bottom=.20)
            route=data['routing'];transfer=route['remote_transfer_ms'];replay=route['remote_replay_ms']
            a.barh(2,10,height=.52,color=COL['gray'],edgecolor=COL['line']);a.barh(1,transfer,height=.52,color=COL['blue'],edgecolor=COL['line']);a.barh(1,replay,left=transfer,height=.52,color=COL['orange'],edgecolor=COL['line']);a.barh(0,20,height=.52,color=COL['gray'],edgecolor=COL['line'])
            a.text(10.4,2,'10 ms',va='center',fontsize=11);a.text(route['remote_ready_ms']+.4,1,'12.666 ms',va='center',fontsize=11);a.text(20.4,0,'20 ms',va='center',fontsize=11)
            a.text(2.3,1,"transmission",ha='center',va='center',fontsize=11);a.text(8.7,1,"Encoder recovery",ha='center',va='center',fontsize=11)
            a.set(yticks=[2,1,0],yticklabels=["A: shorter queue","B: retrieval and recovery","A: longer queue"],xlim=(0,26),ylim=(-.7,2.9),xlabel="Different preparation time for two paths (ms)")
            out.save(f,'figure-9-v41-routing')
