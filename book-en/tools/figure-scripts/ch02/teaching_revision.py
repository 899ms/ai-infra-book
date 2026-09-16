"""Chapter 2 drawings follow the objects from one position to a whole request."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,name):out.save(f,'figure-2-'+name)
    def cells(a,x,y,count,w=.65,h=.10,colors=None,labels=None):
        for j in range(count):
            box(a,x+j*w/count,y,w/count-.006,h,labels[j] if labels else str(j+1),colors[j] if colors else 'blue',11)
    def bars(name,labels,values,xlabel,colors=None):
        f,a=plot(4.1 if len(values)>4 else 3.4,left=.31)
        a.barh(range(len(values)),values,color=colors or COL['blue'],edgecolor=COL['line'],height=.55)
        a.set(yticks=range(len(values)),yticklabels=labels,xlim=(0,max(values)*1.28),xlabel=xlabel);a.invert_yaxis()
        for i,v in enumerate(values):a.text(v+max(values)*.025,i,f'{v:,.2f}',va='center',fontsize=11)
        save(f,name)
    with plt.rc_context(STYLE):
        for mode,name,title in [('rnn','1-dependencies',"same layer completes previous token first"),('causal','causal-dependencies',"each token in this layer reads previous layer's causal prefix")]:
            f,a=canvas(3.7);text(a,.04,.94,title,14)
            xs=[.23,.44,.65,.86];ys=[.18,.46,.74]
            for l,y in enumerate(ys):
                text(a,.04,y,["input","Layer 1","Layer 2"][l],11)
                for j,x in enumerate(xs):
                    if l:
                        for k in ([j] if mode=='rnn' else range(j+1)):
                            arrow(a,(xs[k],ys[l-1]+.04),(x,y-.04))
                        if mode=='rnn' and j:arrow(a,(xs[j-1]+.035,y),(x-.035,y))
                    a.scatter(x,y,s=450,facecolor=COL['blue'],edgecolor=COL['line'],zorder=5)
            for j,x in enumerate(xs):text(a,x,.055,f'token {j+1}',11,ha='center')
            save(f,name)

        f,a=canvas(4.3);text(a,.04,.94,"same input produces three representations",14)
        box(a,.30,.74,.40,.12,"current token hidden vector",'gray')
        for x,label,c in [(.04,"query Q",'orange'),(.36,"key K",'blue'),(.68,"value V",'green')]:
            arrow(a,(.5,.74),(x+.14,.62));box(a,x,.46,.28,.16,label,c)
        text(a,.50,.34,"query matches keys to get per-token coefficients",12,ha='center')
        box(a,.09,.10,.82,.14,"sum token values by coefficient to form output",'purple')
        arrow(a,(.5,.29),(.5,.25));save(f,'qkv-objects')

        f,a=canvas(3.7);text(a,.04,.94,"2 tokens already present, then input 3 more tokens",14)
        for i in range(3):
            y=.66-i*.19;text(a,.04,y+.065,f'New token {i+1}',11)
            for j in range(5):
                a.add_patch(Rectangle((.29+j*.125,y),.12,.13,facecolor=COL['blue'] if j<2 else COL['green'] if j<3+i else COL['white'],edgecolor=COL['line'],lw=.8))
                if j<3+i:text(a,.35+j*.125,y+.065,'✓',12,ha='center')
        text(a,.415,.84,"existing context",11,ha='center');text(a,.73,.84,"current input",11,ha='center')
        text(a,.5,.065,"old context pairs 6 + intra-block causal pairs 6",12,ha='center');save(f,'causal-pairs')

        f,a=canvas(4.8);text(a,.04,.95,"layer exchanges info first, then transforms features",14)
        stages=[("input: 4096 numbers per token",'gray'),("Norm → Attention → Output Projection",'blue'),("Elementwise add with sublayer input",'green'),("Norm → FFN",'orange'),("Elementwise add with sublayer input",'green')]
        for i,(s,c) in enumerate(stages):
            y=.77-i*.16;box(a,.19,y,.76,.115,s,c)
            if i<4:arrow(a,(.57,y),(.57,y-.045))
        for y1,y2 in [(.77,.507),(.45,.187)]:
            a.plot([.19,.065,.065,.19],[y1+.035,y1+.035,y2,y2],color=COL['line'],lw=1)
            arrow(a,(.065,y2),(.19,y2))
        text(a,.05,.055,"left bypass retains sublayer input for residual add",11);save(f,'2-layer')

        f,a=canvas(3.9);box(a,.30,.80,.40,.12,"input X: 4096 dim",'gray')
        box(a,.04,.55,.40,.14,"gate projection → SiLU",'orange');box(a,.56,.55,.40,.14,"up projection",'blue')
        arrow(a,(.5,.80),(.24,.69));arrow(a,(.5,.80),(.76,.69))
        text(a,.24,.46,"12288 dim",11,ha='center');text(a,.76,.46,"12288 dim",11,ha='center')
        box(a,.30,.26,.40,.13,"elementwise multiply",'green');arrow(a,(.24,.43),(.4,.40));arrow(a,(.76,.43),(.6,.40))
        box(a,.20,.04,.60,.13,"down projection: returns 4096 dim",'purple');arrow(a,(.5,.26),(.5,.17));save(f,'ffn-gates')

        f,a=canvas(4.2);text(a,.04,.94,"each step appends one token, rereads existing context",14)
        for i,n in enumerate([4,5,6,7]):
            y=.71-i*.18;text(a,.03,y+.05,f'Step {i+1}step',11)
            cells(a,.22,y,n+1,w=.70,h=.12,colors=['blue']*n+['orange'])
        text(a,.5,.07,"blue: context read this step; orange: appended this step",11,ha='center');save(f,'history')
        f,a=plot(3.4)
        B=np.arange(1,65);W=data['teaching_diagrams']['history']['shared_weight_bytes']/2**30
        a.axhline(W,color='#267398',label="Weights read per batch");a.plot(B,B*8192*147456/2**30,color='#a56c28',label="8K token KV × request count")
        a.set(xlim=(0,64),ylim=(0,75),xlabel="Requests per batch",ylabel="Logical read volume (GiB)");a.legend(frameon=False)
        save(f,'history-batch')

        f,a=canvas(5.6)
        for row,(title,groups) in enumerate([("MHA: one KV group per query",4),("GQA: one KV group per two queries",2),("MQA: one KV group per four queries",1)]):
            top=.95-row*.32;text(a,.04,top,title,14)
            for j in range(4):
                x=.10+j*.225;box(a,x,top-.13,.15,.07,f'Q{j+1}','orange',11)
                g=j if groups==4 else j//2 if groups==2 else 0;dest=.10+(g+.5)*.825/groups
                arrow(a,(x+.075,top-.13),(dest,top-.20))
            for g in range(groups):
                x=.10+g*.825/groups;box(a,x,top-.28,.825/groups-.02,.08,f'KV {g+1}','blue',11)
        save(f,'3-sharing')
        bars('4-cache',["MHA: 32 groups","GQA: 8 groups","MQA: 1 group"],data['figure_2_4']['qwen_variants_mib'],"8K context state capacity (MiB)")

        f,a=canvas(4.8)
        text(a,.04,.94,"path 1: expand each context token first",14)
        box(a,.04,.69,.25,.13,"latent c",'blue');box(a,.38,.69,.25,.13,"expanded key K",'green');box(a,.72,.69,.24,.13,"dot-product score",'purple')
        arrow(a,(.29,.755),(.38,.755));arrow(a,(.63,.755),(.72,.755))
        text(a,.32,.60,"context computes K = c Uₖ first",12)
        text(a,.04,.46,"path 2: transform current query first",14)
        box(a,.04,.22,.25,.13,"current query q",'orange');box(a,.38,.22,.25,.13,"transformed query",'orange');box(a,.72,.22,.24,.13,"dot-product score",'purple')
        arrow(a,(.29,.285),(.38,.285));arrow(a,(.63,.285),(.72,.285))
        box(a,.71,.035,.25,.10,"latent c",'blue');arrow(a,(.835,.135),(.835,.22))
        text(a,.04,.09,"query computes q Uₖᵀ first",12)
        save(f,'mla-paths')
        bars('mla-capacity',["Compact latent","Expand per-head KV"],data['figure_2_4']['k3_mla_paths_mib'],"Kimi K3 24-layer MLA state (MiB)")

        f,a=canvas(4.3);text(a,.04,.94,"form compressed entries first, then query selects",14)
        cells(a,.05,.72,8,w=.90,h=.11)
        for i in range(2):
            arrow(a,(.27+i*.45,.71),(.27+i*.45,.59));box(a,.10+i*.45,.45,.34,.13,f'Compressed entry {i+1}','green')
        text(a,.5,.35,"example: every 4 tokens merged into 1 entry",11,ha='center')
        box(a,.04,.08,.25,.13,"current query",'orange');box(a,.38,.08,.25,.13,"scan index",'purple');box(a,.72,.08,.24,.13,"read selected entries",'green',11)
        arrow(a,(.29,.145),(.38,.145));arrow(a,(.63,.145),(.72,.145));save(f,'5-sparse')
        c=data['figure_2_5']['components'];bars('sparse-capacity',["Window state","Compressed representation","Index entry","Compression buffer"],[c['window_history_bytes']/2**20,c['compressed_history_bytes']/2**20,c['index_history_bytes']/2**20,data['figure_2_5']['compressor_buffer_bytes']/2**20],"DeepSeek V4-Flash 8K context state (MiB)")
        f,a=canvas(3.4)
        for i in range(4):
            x=.04+i*.24;box(a,x,.56,.20,.17,f'Arrival {i+1}\nWithin block {i+1}/4','orange' if i==3 else 'blue',11)
            if i<3:arrow(a,(x+.20,.64),(x+.24,.64))
        box(a,.62,.12,.33,.17,"publish compressed entry",'green');arrow(a,(.86,.56),(.79,.29))
        text(a,.05,.28,"first three steps update same buffer\nfourth step completes one block",12);save(f,'compression-steps')

        f,a=canvas(3.9);text(a,.04,.94,"context grows, state matrix stays same size",14)
        for x,title,c in [(.04,"Old state",'blue'),(.37,"New key-value outer product",'orange'),(.70,"New state",'green')]:
            for i in range(3):
                for j in range(3):a.add_patch(Rectangle((x+j*.08,.46+i*.08),.08,.08,facecolor=COL[c],edgecolor=COL['line'],lw=.7))
            text(a,x+.12,.36,title,12,ha='center')
        text(a,.32,.58,'+',16,ha='center');text(a,.655,.58,'=',16,ha='center')
        box(a,.22,.09,.56,.13,"current query × new state → output",'purple');save(f,'recurrence')

        f,a=canvas(4.1);text(a,.04,.94,"model config determines attention type",14)
        box(a,.05,.62,.40,.18,"30-layer linear attention\nfixed recurrent state",'blue');box(a,.55,.62,.40,.18,"10-layer full attention\nper-token context",'green')
        box(a,.20,.34,.60,.13,"in-layer normalization and residual connection",'gray')
        arrow(a,(.25,.62),(.4,.47));arrow(a,(.75,.62),(.6,.47))
        box(a,.06,.07,.41,.16,"Routed experts: 8 of 256",'orange',11);box(a,.57,.07,.37,.16,"shared experts",'purple')
        arrow(a,(.4,.34),(.27,.23));arrow(a,(.6,.34),(.76,.23));save(f,'6-hybrid')
        import json
        comparison=json.loads((here/'model-comparison.json').read_text())
        d=comparison['state_curves']
        names=dict(zip([x['model_id'] for x in comparison['models']],['V4.1 Flash','Qwen3-8B','Qwen3.6','V4-Flash','Kimi K3']))
        for field,name,ylabel in [('resident_bytes','7-state-growth',"Per-request state capacity (GiB)"),('accounted_access_bytes','state-access',"State access per step (GiB)")]:
            f,a=plot(4.4,left=.19,bottom=.18)
            for key,col in zip(names,['#965466','#267398','#72558c','#388768','#a56c28']):
                a.plot(np.array(d['lengths'])/1024,np.array(d[field][key])/2**30,'o-',label=names[key],color=col)
            a.set(xscale='log',yscale='log',xlabel="Context length (K tokens, log scale)",ylabel=ylabel+", log scale")
            a.legend(frameon=False,fontsize=11,loc='upper left');save(f,name)

        f,a=canvas(4.0);text(a,.04,.94,"same dispatch count, experts accessed may differ",14)
        for y,title,n,c in [(.58,"Distributed: covers 256 experts",256,'blue'),(.17,"Centralized: covers 8 experts",8,'orange')]:
            box(a,.04,y,.34,.19,"64 tokens\n8 selected each",'gray');arrow(a,(.38,y+.095),(.54,y+.095))
            box(a,.54,y,.42,.19,f'{n} experts\navg per expert: {512/n:.0f} rows',c)
            text(a,.04,y-.07,title,12)
        save(f,'expert-reuse')

        f,a=canvas(4.3)
        for i,(title,streams) in enumerate([("Standard residual: keep one bypass",1),("mHC: keep four paths, then mix back",4)]):
            y=.56-i*.43;text(a,.04,y+.32,title,14)
            for j in range(streams):box(a,.04+j*.10,y+.11,.075,.09,str(j+1),'blue',11)
            box(a,.55,y+.09,.39,.14,"Sublayer input 4096-dim",'orange',11)
            arrow(a,(.44 if streams==4 else .13,y+.155),(.55,y+.155))
            text(a,.05,y-.04,"One original input added to sublayer output" if streams==1 else "Four paths merge for sublayer, then mix sublayer output",11)
        save(f,'8-residual')

        arch=data['teaching_diagrams']['architecture']
        for key,label,name in [('layers',"Backbone layer count",'architecture'),('hidden',"Backbone hidden dim",'architecture-width'),('experts',"Routed experts per MoE layer",'architecture-experts')]:bars(name,['DeepSeek\nV4.1 Flash','Qwen3-8B','Qwen3.6','DeepSeek\nV4-Flash','Kimi K3'],arch[key],label)
        models=data['teaching_diagrams']['resource_comparison']['models']
        for key,div,label,name in [('uniform_bf16_bytes',1e9,"Full BF16 weights (GB)",'resources'),('decode_matrix_flops',1e9,"8K-context single-step matmul (GFLOPs)",'resources-compute'),('state_8192_bytes',2**20,"8K-context state (MiB)",'resources-state')]:bars(name,['DeepSeek\nV4.1 Flash','Qwen3-8B','Qwen3.6','DeepSeek\nV4-Flash',"Kimi K3\ncompact"],[m[key]/div for m in models],label)

        # Compare 8K with exactly 1M visible positions; retain 200K in JSON.
        long_data=json.loads((here/'long-context-comparison.json').read_text())
        f,a=plot(6.0,left=.32,bottom=.17)
        f.subplots_adjust(top=.84)
        labels=['DeepSeek\nV4.1 Flash','Qwen3-8B','Qwen3.6','DeepSeek\nV4-Flash',"Kimi K3\ncompact"]
        for start,offset,color,label in [(0,-.18,COL['blue'],"8K context"),(10,.18,COL['orange'],"1M visible tokens")]:
            vals=[r['matrix_flops']/1e9 for r in long_data['models'][start:start+5]]
            yy=np.arange(5)+offset
            a.barh(yy,np.array(vals)-1,left=1,height=.30,color=color,edgecolor=COL['line'],label=label)
            for y,value in zip(yy,vals):a.text(value*1.08,y,f'{value:,.2f}',va='center',fontsize=11)
        a.set(yticks=range(5),yticklabels=labels,xscale='log',xlim=(1,19000),
              xlabel="Single-step matmul (GFLOPs, log scale)",ylim=(4.65,-.65))
        a.set_xticks([1,10,100,1000,10000],['1','10','100','1000','10000'])
        a.minorticks_off()
        a.legend(loc='upper left',bbox_to_anchor=(0,1.16),ncol=1,frameon=False)
        a.grid(axis='x',alpha=.15)
        save(f,'long-context-compute')

        rows=data['figure_2_9']['capacity_rows'];f,a=plot(3.8,left=.26,bottom=.25);left=np.zeros(3)
        for key,label,col in [('weight_bytes',"weights",'blue'),('workspace_bytes',"Workspace reserve",'orange'),('kv_bytes_per_request',"KV/request",'green')]:
            vals=np.array([r[key]/1e9 for r in rows]);a.barh(range(3),vals,left=left,height=.5,label=label,color=COL[col],edgecolor=COL['line']);left+=vals
        for i,r in enumerate(rows):a.plot([r['capacity_bytes']/1e9]*2,[i-.35,i+.35],color=COL['ink'],lw=1.2)
        a.set(yticks=range(3),yticklabels=['Qwen BF16\nRTX 4090','70B 8-bit\nH100 SXM','70B 4-bit\nH100 SXM'],xlim=(0,85),xlabel="Capacity (GB)");a.invert_yaxis();a.legend(loc='upper center',bbox_to_anchor=(.5,-.22),ncol=3,frameon=False);save(f,'9-capacity')
        d=data['figure_2_9']['history_capacity'];bars('history-capacity',["8K context","32K context"],d['maximum_requests'],"Independent requests allowed by capacity")

        f,a=canvas(4.8);text(a,.04,.94,"input 128 tokens, return 4 tokens",14)
        for i in range(4):
            y=.72-i*.21
            box(a,.03,y,.24,.14,"128 inputs" if i==0 else f'Input y{i}','blue',11)
            box(a,.36,y,.27,.14,'prefill' if i==0 else f'decode {i}','orange')
            box(a,.72,y,.25,.14,f'Output y{i+1}','green')
            arrow(a,(.27,y+.07),(.36,y+.07));arrow(a,(.63,y+.07),(.72,y+.07))
            text(a,.49,y-.045,f'Retained {128+i} tokens',11,ha='center')
        save(f,'10-request')
        bars('request-compute',['DeepSeek\nV4.1 Flash','Qwen3-8B','Qwen3.6','DeepSeek\nV4-Flash',"Kimi K3\ncompact"],[r['matrix_flops']/1e12 for r in comparison['requests']],"full request matrix operations (TFLOPs)")
    from core_principles_figures import draw as draw_principles
    draw_principles(2, out)
    from v41_case_figures import draw as draw_v41
    draw_v41(2, out)
    return out.finish()
