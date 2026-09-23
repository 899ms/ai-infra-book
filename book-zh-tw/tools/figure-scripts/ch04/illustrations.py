"""Additional textbook diagrams: data reuse, padding, capacity, layout, locality and time."""
import numpy as np
from matplotlib.patches import Rectangle

def draw_additions(plt,C,canvas,box,arrow,save,data):
    # One unchanged weight matrix serves either one row or many rows.
    f,axes=plt.subplots(1,2,figsize=(12,5));f.subplots_adjust(left=.03,right=.98,bottom=.06,top=.94,wspace=.10)
    for a,m in zip(axes,[1,256]):
        a.set(xlim=(0,1),ylim=(0,1));a.axis('off')
        a.text(.5,.94,f'{m} 行輸入',ha='center',fontsize=15)
        box(a,.33,.41,.38,.28,"同一份權重\n32 MiB",'pale',13)
        ys=[.55] if m==1 else [.75,.65,.55,.45,.35]
        for y in ys:
            a.add_patch(Rectangle((.015,y-.025),.15,.05,fc=C['teal']))
            arrow(a,(.17,y),(.32,.55))
            a.add_patch(Rectangle((.84,y-.025),.14,.05,fc=C['orange']))

        for y in ys:arrow(a,(.72,.55),(.83,y))
        a.text(.085,.20,"輸入行",ha='center');a.text(.91,.20,"輸出行",ha='center')
        if m==256:a.text(.085,.27,'⋮',ha='center',fontsize=18);a.text(.91,.27,'⋮',ha='center',fontsize=18)
        a.text(.51,.075,"每行分攤權重讀取："+('32 MiB' if m==1 else '128 KiB'),ha='center',fontsize=12)
    save(f,'figure-4-1-reuse');data['4-1']={'weight_bytes':33554432,'rows':[1,256],'weight_bytes_per_row':[33554432,131072]}

    # Show one expert at equal row granularity; then total work on a common scale.
    f=plt.figure(figsize=(12,6));top=f.add_axes([.06,.42,.90,.53]);top.set(xlim=(0,1),ylim=(0,1));top.axis('off')
    top.text(.20,.93,"256 個專家，每個專家 2 行",ha='center',fontsize=13)
    top.text(.72,.93,"8 個專家，每個專家 64 行",ha='center',fontsize=13)
    for col,count in [(0,2),(1,64)]:
        x0=.13 if col==0 else .52
        for tile in range(1 if col==0 else 4):
            for row in range(16):
                y=.76-row*.032
                top.add_patch(Rectangle((x0+tile*.11,y),.085,.027,fc=C['teal'] if row+tile*16<count else '#e5eaee',ec='white',lw=.3))
        top.text(.20 if col==0 else .72,.13,"補齊為 16 行" if col==0 else "4 個完整計算塊",ha='center',fontsize=12)
    a=f.add_axes([.19,.12,.75,.22]);a.barh([1,0],[512,512],color=C['teal'],label="有效輸入行");a.barh([1,0],[3584,0],left=[512,512],color='#dce3e8',label="補零行")
    a.set_yticks([1,0],["256 個專家合計","8 個專家合計"]);a.set_xlim(0,4400);a.set_xlabel("全部專家實際執行的行數");a.legend(frameon=False,ncol=2,loc='lower right',bbox_to_anchor=(1,1.06))
    a.text(4096+45,1,'4096',va='center');a.text(512+45,0,'512',va='center')
    save(f,'figure-4-3-expert-rows');data['4-3']={'assignments':512,'experts':[256,8],'rows_per_expert':[2,64],'padded_rows':[4096,512],'tile_rows':16}

    # Each band uses one physical capacity axis; overflow remains visible.
    W=16381470720;workspace=2*2**30;K=1207959552;cap=24e9
    f,a=plt.subplots(figsize=(12,5));f.subplots_adjust(left=.19,right=.97,bottom=.18,top=.84)
    for y,(b,mult) in enumerate([(4,1),(5,1),(2,2)]):
        left=0
        for size,color,label in [(W,C['blue'],"權重"),(workspace,C['orange'],"工作區")]:
            a.barh(y,size/1e9,left=left,height=.56,color=color,edgecolor='white',label=label if y==0 else None)
            if size==W:a.text(left+size/2e9,y,'16.4 GB',ha='center',va='center',color='white',fontsize=12)
            left+=size/1e9
        for j in range(b):
            a.barh(y,K*mult/1e9,left=left,height=.56,color=C['teal'],edgecolor='white',label="每條請求的 KV" if y==0 and j==0 else None);left+=K*mult/1e9
        if left>24:a.add_patch(Rectangle((24,y-.28),left-24,.56,fc='none',ec=C['red'],hatch='////',lw=1.3))
        a.text(left+.16,y,"超出容量" if left>24 else "可容納",va='center',color=C['red'] if left>24 else C['ink'],fontsize=11)
    a.axvline(24,ls='--',color=C['red']);a.text(24,-.63,"RTX 4090 的 24 GB",ha='center',color=C['red'],fontsize=11)
    a.set_yticks(range(3),["8192 位置 × 4 請求","8192 位置 × 5 請求","16384 位置 × 2 請求"]);a.invert_yaxis();a.set_xlim(0,27);a.set_xlabel("記憶體佔用 / GB");a.legend(frameon=False,ncol=3,loc='upper left',bbox_to_anchor=(0,1.22))
    save(f,'figure-4-6-capacity');data['4-6']={'weight_bytes':W,'workspace_bytes':workspace,'kv_bytes_per_request':K,'capacity_bytes':cap,'cases':[{'requests':b,'context_multiplier':m,'total_bytes':W+workspace+b*m*K} for b,m in [(4,1),(5,1),(2,2)]]}

    # Addresses and useful bytes: the short blue segment has an explicit zoom.
    f,a=plt.subplots(figsize=(12,5.8));f.subplots_adjust(left=.17,right=.97,bottom=.17,top=.87)
    for y,label in enumerate(["第 0 行","第 1 行","第 2 行","第 127 行"]):
        a.broken_barh([(0,8192)],(y-.22,.44),facecolors='#e6ecef')
        a.broken_barh([(0,256)],(y-.22,.44),facecolors=C['blue'])
    a.set(xlim=(-100,8400),ylim=(3.6,-.8),xlabel="相對於每行起點的位元組偏移");a.set_yticks(range(4),["第 0 行","第 1 行","第 2 行","第 127 行"]);a.set_xticks([0,4096,8192],['0','4096','8192'])
    a.text(4350,-.5,"每行 8192 bytes：讀取 256 bytes，跳過其餘部分",ha='center',fontsize=12)
    a.text(4200,2.55,"⋮  中間 124 行省略  ⋮",ha='center',fontsize=12)
    a.annotate("每行實際讀取 256 bytes",xy=(128,0),xytext=(1800,.48),arrowprops={'arrowstyle':'->','color':C['blue']},fontsize=12)
    a.text(300,3.47,"全部藍色：32 KiB",color=C['blue'],fontsize=12)
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
    a.plot(m,compute,color=C['blue'],lw=2.5,label="矩陣計算");a.plot(m,memory,color=C['teal'],lw=2.5,label="片外資料傳輸");a.axvline(179,ls=':',color=C['orange'])
    a.text(85,8,"資料傳輸較慢",ha='center',color=C['teal'],fontsize=13);a.text(219,12,"矩陣計算較慢",ha='center',color=C['blue'],fontsize=13)
    a.annotate("從 179 行起計算耗時更長",xy=(179,compute[178]),xytext=(85,49),arrowprops={'arrowstyle':'->','color':C['orange']},fontsize=11)
    a.set(xlim=(1,256),ylim=(0,60),xlabel="一次呼叫的輸入行數 M",ylabel="時間 / μs");a.set_xticks([1,64,128,179,256]);a.legend(frameon=False,loc='upper left')
    save(f,'figure-4-13-roofline');data['4-13']={'rows':m.tolist(),'compute_us':compute.tolist(),'memory_us':memory.tolist(),'peak_flops':165.2e12,'bandwidth_bytes_per_second':1.008e12}
