"""Book-size diagrams for sections 5.2–5.3 (420 pt wide, no tight cropping).

Existing numerical data keys remain stable; figure-index.json maps assets to captions.
"""
from pathlib import Path
import json
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch, Patch
import numpy as np

COL={'ink':'#252525','line':'#454545','blue':'#CBE3F3','green':'#CFE8DB',
     'orange':'#F9DEC0','purple':'#DDCDE8','gray':'#EEEEEE','white':'#FFFFFF'}
REPLACED={'figure-5-2-tiles','figure-5-3-banks','figure-5-4-reduction',
          'figure-5-5-boundaries','figure-5-6-fusion-buffer',
          'figure-5-7-online-softmax','figure-5-8-attention-tradeoff'}

def draw(here, data):
    outputs=[]; checks=[]
    def text(a,x,y,s,size=12,ha='left',**kw):
        return a.text(x,y,s,fontsize=size,ha=ha,va='center',color=COL['ink'],linespacing=1.4,**kw)
    def box(a,x,y,w,h,s='',c='blue',size=12):
        a.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.002,rounding_size=0.009',facecolor=COL[c],edgecolor=COL['line'],lw=.9))
        if s:text(a,x+w/2,y+h/2,s,size,ha='center')
    def arrow(a,p,q,c='line'):
        a.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=11,lw=1,color=COL[c],shrinkA=2,shrinkB=3))
    def canvas(height=3.7):
        f,a=plt.subplots(figsize=(420/72,height));f.subplots_adjust(left=.035,right=.965,bottom=.035,top=.965)
        a.set(xlim=(0,1),ylim=(0,1));a.axis('off');return f,a
    def title(a,s,y=.94):text(a,.02,y,s,14)
    def save(f,name):
        f.canvas.draw();renderer=f.canvas.get_renderer();bad=[];sizes=[]
        for t in f.findobj(matplotlib.text.Text):
            if not t.get_visible() or not t.get_text():continue
            bb=t.get_window_extent(renderer);sizes.append(t.get_fontsize())
            if bb.x0<0 or bb.y0<0 or bb.x1>f.bbox.width or bb.y1>f.bbox.height:bad.append(t.get_text())
        checks.append({'figure':name,'width_pt':420,'min_label_pt':min(sizes),'text_extent_warnings':bad})
        for ext in ['svg','png','pdf']:
            p=here/f'{name}.{ext}';f.savefig(p,dpi=240);outputs.append(p)
        plt.close(f)
    def grid(a,x,y,rows,cols,w,h,highlight,c):
        for i in range(rows):
            for j in range(cols):
                a.add_patch(Rectangle((x+j*w/cols,y+(rows-1-i)*h/rows),w/cols,h/rows,
                                     fc=COL[c] if highlight(i,j) else 'white',ec='#777777',lw=.7))
    style={'font.size':12,'text.color':COL['ink'],'axes.labelcolor':COL['ink'],
           'xtick.color':COL['ink'],'ytick.color':COL['ink'],'axes.edgecolor':COL['line'],
           'pdf.fonttype':42,'axes.titlesize':14,'axes.labelsize':12,'xtick.labelsize':11,
           'ytick.labelsize':11,'legend.fontsize':11,'svg.fonttype':'path'}
    with plt.rc_context(style):
        # One operation, then its neighbour: identical positions make reuse visible.
        f,a=canvas(4.1)
        for row,j in enumerate([0,1]):
            y=.60-row*.45
            title(a,"compute one output first" if j==0 else "then compute adjacent output",y+.31)
            grid(a,.06,y,3,4,.22,.21,lambda r,c:r==1,'blue')
            grid(a,.39,y,4,3,.19,.25,lambda r,c:c==j,'orange')
            grid(a,.73,y,3,3,.20,.21,lambda r,c:r==1 and c==j,'green')
            text(a,.335,y+.11,'×',17,ha='center');text(a,.655,y+.11,'=',17,ha='center')
            text(a,.17,y-.065,"same row of A",11,ha='center');text(a,.485,y-.065,f'column {j+1} of W',11,ha='center')
            text(a,.83,y-.065,f'C[i, j{"+1" if j else ""}]',11,ha='center')
        save(f,'figure-5-reuse-steps')
        data['reuse_steps']={'kind':'schematic','rows':3,'inner':4,'columns':3,'output_row':1,'output_columns':[0,1]}

        f,a=canvas(3.9)
        title(a,"one input pair updates entire output block")
        box(a,.04,.54,.23,.20,"A block\nm × k",'blue')
        box(a,.385,.54,.23,.20,"W block\nk × n",'orange')
        box(a,.74,.48,.22,.32,"accumulator\nm × n\nFP32",'green')
        text(a,.327,.64,'×',17,ha='center');arrow(a,(.625,.64),(.73,.64))
        text(a,.155,.435,'2mk bytes',11,ha='center');text(a,.5,.435,'2kn bytes',11,ha='center');text(a,.85,.385,'4mn bytes',11,ha='center')
        box(a,.09,.15,.56,.13,"swap in next A, W pair along K",'gray')
        arrow(a,(.65,.215),(.74,.475))
        text(a,.5,.055,"input blocks swapped; output accumulator stays resident",12,ha='center')
        save(f,'figure-5-tile-working-set')
        data['tile_working_set']={'tile':[64,64,32],'input_bytes':[4096,4096],'accumulator_bytes':16384,'lifetime':'across all K tiles'}

        f,a=plt.subplots(figsize=(420/72,3.6));f.subplots_adjust(left=.15,right=.94,top=.91,bottom=.20)
        d=data['5-2'];a.plot(d['capacity_KiB'],np.array(d['interface_MiB'])/1024,'o-',color='#267398',lw=1.8)
        for x,y,label,offset in zip(d['capacity_KiB'],d['interface_MiB'],['32 × 32','64 × 64','128 × 128'],[(7,7),(12,8),(-72,16)]):
            a.annotate(label,(x,y/1024),xytext=offset,textcoords='offset points',fontsize=12)
        a.axhline(.125,ls='--',color='#875b28',lw=1)
        a.text(28,.43,"one read/write each: 128 MiB",fontsize=11)
        a.set(xlim=(0,98),ylim=(0,7),xticks=[8,24,48,80],xlabel="local storage requirement (KiB)",ylabel="interface read/write volume (GiB)")
        save(f,'figure-5-2-tiles')

        # RTX PRO 6000 (compute capability 12.x): 100 KB shared memory per SM, 99 KB per block, i.e. 1 KiB reserved per block.
        budget,reserve=100,1
        f,a=canvas(3.0);title(a,"how many copies fit in one SM's 100 KB shared memory?")
        for y,size,c in [(.54,24,'blue'),(.19,80,'orange')]:
            count=budget//(size+reserve)
            for i in range(count):
                x=.04+.92*i*(size+reserve)/budget;w=.92*size/budget
                a.add_patch(Rectangle((x,y),w,.16,fc=COL[c],ec=COL['line'],lw=.9))
                a.add_patch(Rectangle((x+w,y),.92*reserve/budget,.16,fc=COL['gray'],ec=COL['line'],lw=.6))
                text(a,x+w/2,y+.08,f'{size} KiB',12,ha='center')
            used=count*(size+reserve)
            if used<budget:
                a.add_patch(Rectangle((.04+.92*used/budget,y),.92*(budget-used)/budget,.16,fc='white',ec=COL['line'],lw=.9))
                text(a,.04+.92*(used+budget)/2/budget,y+.08,"free",11,ha='center')
            text(a,.04,y-.075,"working set of four 64×64 output blocks" if size==24 else "working set of one 128×128 output block",12)
        text(a,.96,.075,"gray: 1 KiB reserved per block",11,ha='right')
        save(f,'figure-5-tile-residency')
        data['tile_residency']={'device':'rtx-pro6000-blackwell-ws (compute capability 12.x)','budget_KiB':budget,'reserve_KiB_per_block':reserve,'working_set_KiB':[24,80],'resident_sets':[budget//(24+reserve),budget//(80+reserve)],'constraint':'shared memory per SM; inputs and accumulator both in shared memory'}

        f,a=canvas(4.5)
        for y,stride in [(.58,32),(.09,33)]:
            title(a,f'row stride {stride} words',y+.34)
            text(a,.98,y+.34,"numbers are word addresses",11,ha='right')
            for i in range(4):
                x=.05+i*.235
                box(a,x,y+.18,.19,.08,f'lane {i}','gray',11)
                text(a,x+.095,y+.10,str(i*stride),11,ha='center')
                dest=(.49,y-.005) if stride==32 else (x+.095,y-.005)
                arrow(a,(x+.095,y+.055),dest)
                if stride==33:box(a,x,y-.09,.19,.08,f'bank {i}','green',11)
            if stride==32:box(a,.39,y-.09,.20,.08,'bank 0','orange',11)
        save(f,'figure-5-3-banks')

        f,a=canvas(4.6)
        title(a,"one group processes one row")
        box(a,.04,.72,.25,.13,"retain full row input",'blue');box(a,.38,.72,.25,.13,"compute scale factor",'green');box(a,.73,.72,.23,.13,"normalize",'green')
        arrow(a,(.30,.785),(.37,.785));arrow(a,(.64,.785),(.72,.785))
        title(a,"split row into eight segments",.60)
        for i in range(8):
            x=.045+i*.115
            box(a,x,.43,.105,.08,str(i),'blue',11)
            arrow(a,(x+.0525,.425),(.50,.32))
        text(a,.50,.555,"each segment 512 items → local sum of squares",12,ha='center')
        box(a,.33,.21,.34,.11,"merge, compute scale factor",'green')
        box(a,.04,.035,.30,.10,"reread original input",'orange')
        box(a,.65,.035,.31,.10,"normalize and write out",'green')
        arrow(a,(.67,.265),(.805,.145));arrow(a,(.35,.085),(.64,.085))
        save(f,'figure-5-4-reduction')

        f,a=canvas(4.2)
        title(a,"separate execution: intermediate result passes through next-level storage")
        box(a,.04,.70,.25,.12,'SiLU(G)','green');box(a,.70,.70,.25,.12,'T × U','green')
        box(a,.36,.46,.28,.13,"full T\n24 MiB",'orange')
        arrow(a,(.29,.755),(.39,.60));arrow(a,(.61,.60),(.70,.755))
        text(a,.24,.59,"write out",11);text(a,.71,.59,"read back",11)
        title(a,"fused execution: pass tile-by-tile to next step",.34)
        box(a,.035,.055,.93,.20,'','gray')
        box(a,.08,.10,.24,.10,'SiLU(G)','green');box(a,.40,.10,.20,.10,"local t",'orange');box(a,.69,.10,.23,.10,'t × U','green')
        arrow(a,(.325,.15),(.39,.15));arrow(a,(.605,.15),(.68,.15))
        save(f,'figure-5-fusion-path')
        data['fusion_path']={'tensor_MiB':24,'separate_MiB':120,'fused_MiB':72,'eliminated_write_read_MiB':48}

        f,a=plt.subplots(figsize=(420/72,3.5));f.subplots_adjust(left=.22,right=.91,bottom=.22,top=.82)
        d=data['5-5'];start=np.zeros(3)
        for key,c in [('required_MiB','blue'),('T_write_read_MiB','orange'),('Z_write_read_MiB','purple')]:
            vals=np.array(d[key]);a.barh(range(3),vals,left=start,color=COL[c],ec=COL['line'],lw=.8,height=.55)
            for i,v in enumerate(vals):
                if v:a.text(start[i]+v/2,i,str(v),ha='center',va='center',fontsize=12)
            start+=vals
        for i,v in enumerate(start):a.text(v+3,i,f'{v:g}',va='center',fontsize=12)
        a.set(yticks=range(3),yticklabels=["fully separated","fuse first two steps","three-step fusion"],xlim=(0,177),xticks=[0,60,120,160],xlabel="read/write volume (MiB)");a.invert_yaxis();a.spines['left'].set_visible(False);a.tick_params(axis='y',length=0)
        f.legend(handles=[Patch(fc=COL[c],ec=COL['line'],label=l) for c,l in [('blue',"required read/write"),('orange',"intermediate T"),('purple',"intermediate Z")]],loc='upper center',ncol=3,frameon=False,handlelength=1,columnspacing=1)
        save(f,'figure-5-5-boundaries')

        d=data['5-6'];ev={(e['kind'],e['tile']):e for e in d['double_buffer']}
        end=lambda e:e['start']+e['duration']
        spans=[(0,end(ev['copy',0])),(ev['compute',0]['start'],end(ev['compute',0])),(ev['compute',1]['start'],end(ev['compute',1]))]
        f,a=canvas(4.1)
        text(a,.41,.94,"slot A",14,ha='center');text(a,.80,.94,"slot B",14,ha='center')
        for y,(t0,t1),left,right in zip([.70,.43,.16],spans,["write block 0","read block 0","write block 2"],["idle","write block 1","read block 1"]):
            text(a,.0,y+.07,f'{t0:.2f}–{t1:.2f} μs'.replace('0.00','0'),12);box(a,.23,y,.34,.14,left,'blue');box(a,.63,y,.34,.14,right,'green' if right!='空闲' else 'gray')
        arrow(a,(.40,.42),(.40,.365));text(a,.40,.34,f'{end(ev["compute",0]):.2f} μs block 0 finished',11,ha='center')
        text(a,.5,.05,f'slot A freed earlier, block 2 waits for mover at {ev["copy",2]["start"]:.2f} μs idle before write',11,ha='center')
        save(f,'figure-5-buffer-slots')
        data['buffer_slots']={'intervals_us':[list(s) for s in spans],'slot_A':['write 0','read 0','write 2'],'slot_B':['idle','write 1','read 1'],'slot_A_free_us':end(ev['compute',0]),'reuse_A_us':ev['copy',2]['start']}

        f,axs=plt.subplots(2,1,figsize=(420/72,4.6));f.subplots_adjust(left=.15,right=.95,top=.82,bottom=.13,hspace=.85)
        d=data['5-6']
        for a,mode,end in zip(axs,['serial','double_buffer'],d['completion_us']):
            title_=("serial" if mode=='serial' else "double buffering")+f'：{end:.2f} μs'
            for e in d[mode]:
                y=.65 if e['kind']=='copy' else .13
                a.broken_barh([(e['start'],e['duration'])],(y,.28),facecolors=COL['blue' if e['slot']==0 else 'green'],edgecolors=COL['line'],lw=.8)
                a.text(e['start']+e['duration']/2,y+.14,str(e['tile']),ha='center',va='center',fontsize=11)
            a.set(xlim=(0,6.6),ylim=(0,1),xticks=[0,1,2,3,4,5,6],yticks=[.27,.79],yticklabels=["compute","movement"])
            a.set_title(title_,loc='left',pad=9);a.axvline(end,ls='--',lw=.8,color=COL['line'])
        axs[1].set_xlabel("Time (μs)")
        f.legend(handles=[Patch(fc=COL[c],ec=COL['line'],label=l) for c,l in [('blue',"slot A: blocks 0, 2"),('green',"slot B: blocks 1, 3")]],loc='upper center',ncol=2,frameon=False)
        save(f,'figure-5-6-fusion-buffer')

        f,a=canvas(4.2)
        title(a,"save full intermediate matrix")
        box(a,.04,.63,.24,.19,"Q, K\ncompute scores",'blue');box(a,.38,.63,.24,.19,"S → P\nfull-row softmax",'orange');box(a,.72,.63,.24,.19,"P, V\ncompute output",'green')
        arrow(a,(.285,.72),(.37,.72));arrow(a,(.625,.72),(.71,.72))
        text(a,.5,.545,"S, P 256 MiB each, written out then read back separately",12,ha='center')
        title(a,"process current block, keep statistics",.42)
        box(a,.04,.15,.25,.18,"current score block",'orange');box(a,.39,.15,.25,.18,"update\nm, ℓ, u",'green');box(a,.75,.15,.21,.18,"next block",'orange')
        arrow(a,(.30,.24),(.38,.24));arrow(a,(.65,.24),(.74,.24))
        text(a,.5,.055,"pass statistics; score buffer left for next block",12,ha='center')
        save(f,'figure-5-attention-storage')
        data['attention_storage']={'L':8192,'d':128,'QKVO_each_MiB':2,'SP_each_MiB':256,'SP_write_read_MiB':1024,'retained':['m','ell','u']}

        f,a=canvas(4.5)
        for y,label,body_,c in [(.72,"① process first block",'s = 0，V = 1\nm = 0，ℓ = 1，u = 1','blue'),
                                  (.43,"② read in second block","s = ln 2, V = 3\nm′ = ln 2, r = 1/2\nOld ℓ, u multiplied by 1/2",'orange'),
                                  (.14,"③ add second block",'ℓ′ = 0.5 + 1 = 1.5\nu′ = 0.5 + 3 = 3.5','green')]:
            text(a,.025,y+.09,label,12);box(a,.39,y,.56,.19,body_,c,12)
        arrow(a,(.67,.715),(.67,.635));arrow(a,(.67,.425),(.67,.345))
        text(a,.50,.06,"All blocks processed: u′ / ℓ′ = 7/3",12,ha='center')
        save(f,'figure-5-7-online-softmax')

        order=json.loads((here.parents[1]/'calculations/results/reduction-order.json').read_text())
        exact,ulp=order['summary']['exact_sum'],order['summary']['ulp']
        f,axs=plt.subplots(2,1,figsize=(420/72,4.8),gridspec_kw={'height_ratios':[3,1.5]});f.subplots_adjust(left=.155,right=.965,top=.90,bottom=.115,hspace=1.0)
        offsets=[v['offset_ulp'] for v in order['variants']]
        rows=list(range(len(offsets)))[::-1]
        axs[0].hlines(rows,offsets,[0]*len(offsets),color=COL['line'],lw=1)
        axs[0].scatter(offsets,rows,s=46,c='#267398',zorder=3)
        axs[0].axvline(0,color=COL['ink'],lw=1.1)
        axs[0].set_yticks(rows,[f"{v['splits']} segments" for v in order['variants']])
        axs[0].set(xlim=(-196,30),ylim=(-1.35,len(offsets)-.25))
        axs[0].set_xticks([-175,-150,-100,-50,0])
        axs[0].text(4,len(offsets)-.62,"exact value",fontsize=11,color=COL['ink'],va='center')
        axs[0].annotate('',(offsets[0],-.95),xytext=(offsets[3],-.95),arrowprops={'arrowstyle':'<|-|>','color':'#a56b30','lw':1.1})
        axs[0].text((offsets[0]+offsets[3])/2,-.68,f"differ by {order['summary']['total_ulp_gap']} ULP",fontsize=11,ha='center')
        axs[0].set_title("how segment count changes sum of squares",loc='left',fontsize=13)
        merge=[(v-exact)/ulp for v in order['merge_order']['values']]
        axs[1].scatter(merge,[0]*len(merge),s=46,c='#a56b30',zorder=3)
        for x in merge:
            axs[1].annotate(f'{x:.1f}',(x,0),xytext=(0,13),textcoords='offset points',fontsize=11,ha='center')
        axs[1].set(xlim=(-11.4,-7.0),ylim=(-.75,.95),yticks=[])
        axs[1].set_xticks([-11,-10,-9,-8])
        axs[1].set_title(f"likewise split into {order['merge_order']['splits']} segments:{order['merge_order']['orders']:,} merge orders, only {order['merge_order']['distinct_results']} results",loc='left',fontsize=13)
        for a_ in axs:
            a_.set_xlabel("distance from sum of squares to exact value (ULP)",fontsize=11)
            a_.spines['left'].set_visible(False);a_.spines['top'].set_visible(False);a_.spines['right'].set_visible(False)
            a_.tick_params(axis='both',labelsize=11,length=0 if a_ is axs[0] else 3)
        save(f,'figure-5-reduction-order')
        data['reduction_order']={'kind':'floating_point_order','source':'calculations/results/reduction-order.json',
            'width':order['summary']['width'],'splits':[v['splits'] for v in order['variants']],
            'offset_ulp':offsets,'total_ulp_gap':order['summary']['total_ulp_gap'],'scale_ulp_gap':order['summary']['scale_ulp_gap'],
            'first_output_ulp_gap':order['summary']['first_output_ulp_gap'],
            'merge_orders':order['merge_order']['orders'],'distinct_merge_results':order['merge_order']['distinct_results']}

        f,a=plt.subplots(figsize=(420/72,3.8));f.subplots_adjust(left=.17,right=.94,top=.91,bottom=.20)
        d=data['5-8'];a.scatter(d['traffic_MiB'],d['updates'],s=55,c=['#a56b30','#318262','#267398'])
        for x,y,label,off in zip(d['traffic_MiB'],d['updates'],['b = 1','b = 64','b = 128'],[(9,0),(10,10),(-64,14)]):
            a.annotate(label,(x,y),xytext=off,textcoords='offset points',fontsize=12)
        a.set_yscale('log');a.set(xlim=(230,665),ylim=(3500,1e6),xticks=[300,400,500,600],xlabel="interface read/write volume (MiB)",ylabel="block-pair update count (log scale)")
        a.set_yticks([1e4,1e5,1e6],["10K","100K","1M"]);a.grid(alpha=.15)
        save(f,'figure-5-8-attention-tradeoff')
    (here/'teaching-layout-check.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
    return outputs,checks
