"""Additional textbook diagrams: data reuse, padding, capacity, layout, locality and time."""
import numpy as np
from matplotlib.patches import Rectangle

def draw_additions(plt,C,canvas,box,arrow,save,data):
    # One unchanged weight matrix serves either one row or many rows.
    f,axes=plt.subplots(1,2,figsize=(12,5));f.subplots_adjust(left=.03,right=.98,bottom=.06,top=.94,wspace=.10)
    for a,m in zip(axes,[1,256]):
        a.set(xlim=(0,1),ylim=(0,1));a.axis('off')
        a.text(.5,.94,f'{m} row input',ha='center',fontsize=15)
        box(a,.33,.41,.38,.28,"same weights\n32 MiB",'pale',13)
        ys=[.55] if m==1 else [.75,.65,.55,.45,.35]
        for y in ys:
            a.add_patch(Rectangle((.015,y-.025),.15,.05,fc=C['teal']))
            arrow(a,(.17,y),(.32,.55))
            a.add_patch(Rectangle((.84,y-.025),.14,.05,fc=C['orange']))

        for y in ys:arrow(a,(.72,.55),(.83,y))
        a.text(.085,.20,"input row",ha='center');a.text(.91,.20,"output row",ha='center')
        if m==256:a.text(.085,.27,'⋮',ha='center',fontsize=18);a.text(.91,.27,'⋮',ha='center',fontsize=18)
        a.text(.51,.075,"weight reads per row:"+('32 MiB' if m==1 else '128 KiB'),ha='center',fontsize=12)
    save(f,'figure-4-1-reuse');data['4-1']={'weight_bytes':33554432,'rows':[1,256],'weight_bytes_per_row':[33554432,131072]}

    # Show one expert at equal row granularity; then total work on a common scale.
    f=plt.figure(figsize=(12,6));top=f.add_axes([.06,.42,.90,.53]);top.set(xlim=(0,1),ylim=(0,1));top.axis('off')
    top.text(.20,.93,"256 experts, 2 rows each",ha='center',fontsize=13)
    top.text(.72,.93,"8 experts, 64 rows each",ha='center',fontsize=13)
    for col,count in [(0,2),(1,64)]:
        x0=.13 if col==0 else .52
        for tile in range(1 if col==0 else 4):
            for row in range(16):
                y=.76-row*.032
                top.add_patch(Rectangle((x0+tile*.11,y),.085,.027,fc=C['teal'] if row+tile*16<count else '#e5eaee',ec='white',lw=.3))
        top.text(.20 if col==0 else .72,.13,"padded to 16 rows" if col==0 else "4 full compute blocks",ha='center',fontsize=12)
    a=f.add_axes([.19,.12,.75,.22]);a.barh([1,0],[512,512],color=C['teal'],label="valid input row");a.barh([1,0],[3584,0],left=[512,512],color='#dce3e8',label="zero-padded row")
    a.set_yticks([1,0],["256 experts total","8 experts total"]);a.set_xlim(0,4400);a.set_xlabel("rows actually executed across all experts");a.legend(frameon=False,ncol=2,loc='lower right',bbox_to_anchor=(1,1.06))
    a.text(4096+45,1,'4096',va='center');a.text(512+45,0,'512',va='center')
    save(f,'figure-4-3-expert-rows');data['4-3']={'assignments':512,'experts':[256,8],'rows_per_expert':[2,64],'padded_rows':[4096,512],'tile_rows':16}

    # Each band uses one physical capacity axis; overflow remains visible.
    W=16381470720;workspace=2*2**30;K=1207959552;cap=24e9
    f,a=plt.subplots(figsize=(12,5));f.subplots_adjust(left=.19,right=.97,bottom=.18,top=.84)
    for y,(b,mult) in enumerate([(4,1),(5,1),(2,2)]):
        left=0
        for size,color,label in [(W,C['blue'],"weights"),(workspace,C['orange'],"workspace")]:
            a.barh(y,size/1e9,left=left,height=.56,color=color,edgecolor='white',label=label if y==0 else None)
            if size==W:a.text(left+size/2e9,y,'16.4 GB',ha='center',va='center',color='white',fontsize=12)
            left+=size/1e9
        for j in range(b):
            a.barh(y,K*mult/1e9,left=left,height=.56,color=C['teal'],edgecolor='white',label="KV per request" if y==0 and j==0 else None);left+=K*mult/1e9
        if left>24:a.add_patch(Rectangle((24,y-.28),left-24,.56,fc='none',ec=C['red'],hatch='////',lw=1.3))
        a.text(left+.16,y,"exceeds capacity" if left>24 else "capacity",va='center',color=C['red'] if left>24 else C['ink'],fontsize=11)
    a.axvline(24,ls='--',color=C['red']);a.text(24,-.63,"RTX 4090's 24 GB",ha='center',color=C['red'],fontsize=11)
    a.set_yticks(range(3),["8192 positions × 4 requests","8192 positions × 5 requests","16384 positions × 2 requests"]);a.invert_yaxis();a.set_xlim(0,27);a.set_xlabel("Memory Footprint / GB");a.legend(frameon=False,ncol=3,loc='upper left',bbox_to_anchor=(0,1.22))
    save(f,'figure-4-6-capacity');data['4-6']={'weight_bytes':W,'workspace_bytes':workspace,'kv_bytes_per_request':K,'capacity_bytes':cap,'cases':[{'requests':b,'context_multiplier':m,'total_bytes':W+workspace+b*m*K} for b,m in [(4,1),(5,1),(2,2)]]}

    # Addresses and useful bytes: the short blue segment has an explicit zoom.
    f,a=plt.subplots(figsize=(12,5.8));f.subplots_adjust(left=.17,right=.97,bottom=.17,top=.87)
    for y,label in enumerate(["row 0","row 1","row 2","row 127"]):
        a.broken_barh([(0,8192)],(y-.22,.44),facecolors='#e6ecef')
        a.broken_barh([(0,256)],(y-.22,.44),facecolors=C['blue'])
    a.set(xlim=(-100,8400),ylim=(3.6,-.8),xlabel="byte offset from row start");a.set_yticks(range(4),["row 0","row 1","row 2","row 127"]);a.set_xticks([0,4096,8192],['0','4096','8192'])
    a.text(4350,-.5,"8192 bytes/row: read 256 bytes, skip rest",ha='center',fontsize=12)
    a.text(4200,2.55,"⋮  124 rows omitted  ⋮",ha='center',fontsize=12)
    a.annotate("actual read per row: 256 bytes",xy=(128,0),xytext=(1800,.48),arrowprops={'arrowstyle':'->','color':C['blue']},fontsize=12)
    a.text(300,3.47,"all blue: 32 KiB",color=C['blue'],fontsize=12)
    save(f,'figure-4-8-layout');data['4-8']={'row_stride_bytes':8192,'read_bytes_per_row':256,'rows':128,'payload_bytes':32768,'address_span_bytes':1040640}

    # Keep large weights beside arithmetic; the die link / per-die HBM ratio decides the remote cost.
    from derive import die_locality
    dl=die_locality()
    save_data={'weights_per_die_bytes':dl['weights_per_die_bytes'],'activation_bytes':dl['activation_bytes'],'cases':dl['cases']}
    data['4-10']=save_data

    # Plot service time, not another unexplained performance summary.
    m=np.arange(1,257);F=2*m*4096**2;V=2*(4096**2+2*m*4096);compute=F/165.2e12*1e6;memory=V/1.008e12*1e6
    f,a=plt.subplots(figsize=(11,5.7));f.subplots_adjust(left=.10,right=.96,bottom=.15,top=.94)
    a.fill_between(m,0,np.maximum(compute,memory),where=m<=178,color='#e5f2ee');a.fill_between(m,0,np.maximum(compute,memory),where=m>=179,color='#e8eff6')
    a.plot(m,compute,color=C['blue'],lw=2.5,label="matrix computation");a.plot(m,memory,color=C['teal'],lw=2.5,label="off-chip data transfer");a.axvline(179,ls=':',color=C['orange'])
    a.text(85,8,"data transfer slower",ha='center',color=C['teal'],fontsize=13);a.text(219,12,"matrix computation slower",ha='center',color=C['blue'],fontsize=13)
    a.annotate("from row 179, computation takes longer",xy=(179,compute[178]),xytext=(85,49),arrowprops={'arrowstyle':'->','color':C['orange']},fontsize=11)
    a.set(xlim=(1,256),ylim=(0,60),xlabel="input rows per call M",ylabel="time / μs");a.set_xticks([1,64,128,179,256]);a.legend(frameon=False,loc='upper left')
    save(f,'figure-4-13-roofline');data['4-13']={'rows':m.tolist(),'compute_us':compute.tolist(),'memory_us':memory.tolist(),'peak_flops':165.2e12,'bandwidth_bytes_per_second':1.008e12}
