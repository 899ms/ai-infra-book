#!/usr/bin/env python3
"""Build chapter 3 figures and offline HTML from locked local evidence."""
from pathlib import Path
import argparse,base64,hashlib,html,json,re,subprocess
from matplotlib.transforms import Bbox
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
import numpy as np
import markdown
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--font');args=parser.parse_args()
import sys
sys.path.insert(0,str(HERE.parent))
from figure_style.typography import configure_font
font,family=configure_font(args.font)
plt.rcParams.update({'font.family':[family,'DejaVu Sans'],'font.size':11,'axes.unicode_minus':False,'svg.fonttype':'path','svg.hashsalt':'ch03-workloads-v1','axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white','savefig.facecolor':'white','text.color':'#193441','axes.labelcolor':'#193441','axes.edgecolor':'#b8cbd2'})
C={'ink':'#193441','blue':'#246f91','teal':'#138b83','orange':'#c9782b','pale':'#f0f6f8','light':'#e7f3ef','sand':'#fcf2e7','muted':'#55707d','line':'#cbd8df','red':'#b65757'}
for z in json.loads((HERE/'sources.json').read_text())['sources']:
 if hashlib.sha256((ROOT/z['path']).read_bytes()).hexdigest()!=z['sha256']:raise SystemExit('Source changed; review before relocking: '+z['path'])
def read(p):return json.loads((ROOT/p).read_text())
def calc(n):return read('calculations/results/'+n+'.json')
outputs=[];data={};extent_issues=[]
import sys
sys.path.insert(0,str(HERE.parent))
from math_style import normalize_figure
def save(fig,name):
 normalize_figure(fig)
 # Captions stay outside figures. Remove canvas headers and footer prose, then crop visible content.
 for artist in list(fig.texts):
  if artist.get_position()[1] > .85 or artist.get_position()[1] < .10: artist.remove()
 for ax in fig.axes:
  if not ax.axison and ax.get_position().width > .95:
   for artist in list(ax.texts):
    if artist.get_position()[1] > .85 or artist.get_position()[1] < .10: artist.remove()
 fig.canvas.draw();renderer=fig.canvas.get_renderer()
 bounds=[]
 for ax in fig.axes:
  if ax.axison: bounds.append(ax.get_tightbbox(renderer))
  else:
   for artist in [*ax.texts,*ax.patches,*ax.lines,*ax.collections]:
    if artist.get_visible():
     bb=artist.get_window_extent(renderer)
     if np.isfinite(bb.extents).all() and (bb.width or bb.height):bounds.append(bb)
 bounds.extend(t.get_window_extent(renderer) for t in fig.texts if t.get_visible())
 crop=Bbox.union(bounds).transformed(fig.dpi_scale_trans.inverted()).padded(.12)
 # Detect text escaping the canvas; interior placements are also visually reviewed.
 for t in fig.findobj(matplotlib.text.Text):
  if not t.get_visible() or not t.get_text():continue
  bb=t.get_window_extent(renderer)
  if bb.x0 < -2 or bb.y0 < -2 or bb.x1>fig.bbox.width+2 or bb.y1>fig.bbox.height+2:
   extent_issues.append({'figure':name,'text':t.get_text(),'bbox':list(bb.bounds)})
 for ext in ['svg','png']:
  p=HERE/f'{name}.{ext}';fig.savefig(p,dpi=160,bbox_inches=crop,pad_inches=0);outputs.append(p)
 plt.close(fig)
def canvas(title,subtitle,h=8):
 f=plt.figure(figsize=(14,h));a=f.add_axes([0,0,1,1]);a.set(xlim=(0,1),ylim=(0,1));a.axis('off');a.text(.045,.96,title,fontsize=23,weight='bold',va='top');a.text(.045,.895,subtitle,fontsize=11,color=C['muted'],va='top');return f,a
def box(a,x,y,w,h,title,body='',color='pale',size=12):
 a.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.005,rounding_size=0.008',edgecolor=C['line'],facecolor=C[color],lw=1));a.text(x+w/2,y+h*(.69 if body else .5),title,ha='center',va='center',weight='bold',fontsize=size)
 if body:a.text(x+w/2,y+h*.28,body,ha='center',va='center',fontsize=10,linespacing=1.55,color=C['muted'])
def arrow(a,start,end,col='teal',rad=0):a.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=13,color=C[col],lw=1.6,connectionstyle=f'arc3,rad={rad}'))
def footer(a,t):a.text(.045,.04,t,fontsize=10.5,color=C['muted'],va='bottom')
# 3-1: calls and logical state, not wall-clock performance.
f,a=canvas("圖 3-1  同一模型的 Prefill 與 Decode","Qwen3-8B · S=6144、P=2048、G=4 · BF16 邏輯 KV，每 token 144 KiB。",8)
box(a,.06,.70,.20,.105,"已恢復字首","6144 個 token",color='light')
box(a,.32,.70,.23,.105,"Prefill：處理新輸入","2048 個 token → 首輸出 $y_1$",color='sand');arrow(a,(.265,.75),(.31,.75))
a.text(.60,.75,"時間順序 →",fontsize=12,color=C['muted']);a.text(.60,.70,"寬度不表示真實耗時",fontsize=10)
for i in range(3):
 x=.32+i*.215;box(a,x,.46,.175,.12,f'Decode {i+1}',f'輸入 $y_{i+1}$ → 輸出 $y_{i+2}$',color='pale')
 if i<2:arrow(a,(x+.18,.52),(x+.205,.52))
arrow(a,(.43,.69),(.405,.59))
a.text(.055,.515,"後續只需\n$G-1=3$ 次呼叫",fontsize=13,linespacing=1.8)
for i,(slots,label) in enumerate([(8192,"Prefill 後"),(8193,"Decode 1 後"),(8194,"Decode 2 後"),(8195,"Decode 3 後")]):
 x=.07+i*.23;box(a,x,.22,.19,.12,label,f'{slots} 個位置',color='light')
a.text(.055,.125,"基線：8192 位置 = 1.125 GiB；三次 decode 共追加 432 KiB。$y_4$ 回傳後尚未再次入模。",fontsize=12)
footer(a,"字首命中減少重算，但新輸入與後續生成仍可讀取已有上下文；V4 的狀態使用第二章各自的結構賬。")
save(f,'figure-3-1-stages');data['3-1']={'kind':'teaching_structure','S':6144,'P':2048,'G':4,'kv_bytes_per_position':147456,'slots_after_calls':[8192,8193,8194,8195]}
# 3-2: workload composition, observed metrics and explicit fluid queue.
arrival=read('experiments/ch03/03-02/results/summary.json')['reports']
f=plt.figure(figsize=(15,11));f.suptitle("圖 3-2  對話長度與思考預算",x=.045,ha='left',y=.97,fontsize=24,weight='bold');f.text(.045,.916,"教學組成、實際重放與品質診斷分別呈現；兩個時段各 60 秒，每組共 480 條請求。",fontsize=11,color=C['muted'])
axs=[f.add_axes(z) for z in [[.08,.59,.37,.25],[.57,.59,.36,.25],[.08,.17,.37,.27],[.57,.17,.36,.27]]]
a=axs[0];labels=["均勻\n前／後窗","變化\n前窗","變化\n後窗"];A=np.array([.5,.9,.1]);a.bar(range(3),A,color=C['blue'],label="A：8192 輸入／256 輸出");a.bar(range(3),1-A,bottom=A,color=C['orange'],label="B：1024 輸入／2048 輸出");a.set_xticks(range(3),labels);a.set_ylim(0,1.1);a.set_ylabel("請求比例");a.set_title("A  同總量，不同短窗組成〔教學〕",loc='left',fontsize=13);a.legend(fontsize=9,frameon=False,loc='upper left',bbox_to_anchor=(0,-.20))
a=axs[1];pref=np.array([18432,29900.8,6963.2]);dec=np.array([4604,1736.8,7471.2]);x=np.arange(3);a.bar(x-.18,pref,width=.35,label="輸入 token/s",color=C['blue']);a.bar(x+.18,dec,width=.35,label="decode 步/s",color=C['teal']);a.set_xticks(x,labels);a.set_ylabel("階段位置數 / s");a.set_title("B  輸入與後續生成需求〔教學〕",loc='left',fontsize=13);a.legend(fontsize=9,frameon=False)
a=axs[2];x=np.arange(2)
for i,(field,lab,col) in enumerate([('ttft_p95_s','TTFT p95','blue'),('latency_p95_s',"完整請求 p95",'teal')]):a.bar(x+(i-.5)*.32,[z[field] for z in arrival],width=.30,label=lab,color=C[col])
a.set_xticks(x,["均勻","時段變化"]);a.set_ylim(0,355);a.set_ylabel("秒");a.set_title("C  同一實例的實際回放",loc='left',fontsize=13);a.legend(frameon=False,fontsize=10)
for i,z in enumerate(arrival):a.text(i,320,f"搶佔 {z['preemptions']} 次",ha='center',fontsize=10)
decode_card=[z for z in calc('batch-reuse-rtxpro6000-mix')['batch_reuse_rows'] if z['batch']==64][0];decode_cards=2;service=decode_cards*decode_card['throughput_upper_tokens_per_second'];peak_backlog=(dec[2]-service)*60
a=axs[3];seconds=np.array([0,60,120,120+peak_backlog/service]);backlog=np.array([0,0,peak_backlog,0]);a.plot(seconds,backlog,color=C['orange'],lw=2.5,marker='o');a.axvline(120,color=C['muted'],ls='--',lw=1);a.set_title("D  固定服務率下的積壓〔教學〕",loc='left',fontsize=13);a.set_xlabel("從請求到達起點計時 / s");a.set_ylabel("待處理 decode 步");a.set_ylim(0,140000);a.annotate(f'{peak_backlog:,.0f} 步',xy=(120,peak_backlog),xytext=(40,127000),arrowprops={'arrowstyle':'->'},fontsize=11);a.grid(alpha=.15)
save(f,'figure-3-2-workload-budget');data['3-2']={'kind':'separate_teaching_and_measurement','A_fraction':A.tolist(),'prefill_positions_per_second':pref.tolist(),'decode_positions_per_second':dec.tolist(),'arrival_reports':arrival,'fluid_queue':{'device':'rtx-pro6000-blackwell-ws','cards':decode_cards,'batch_per_card':64,'mean_context_tokens':2742,'service_steps_per_second':service,'seconds':seconds.tolist(),'backlog_steps':backlog.tolist()}}
# 3-3: measured round durations, engine hits, and explicitly hypothetical retention.
ag=calc('agent-thinking-on');rounds=ag['agent_rounds'];f,a=canvas("圖 3-3  Agent 軌跡與 KV 生命週期","開啟 thinking 的四輪人工程式碼任務；模型／工具為牆鐘觀測，快取大小為條件式邏輯預算。",10)
ax=f.add_axes([.12,.55,.79,.27]);y=np.arange(4);mods=[z['measured_model_seconds'] for z in rounds];tools=[z['measured_tool_seconds'] for z in rounds]
ax.barh(y,mods,color=C['blue'],label="模型牆鐘");ax.barh(y,tools,left=mods,color=C['orange'],label="工具牆鐘（本例很短）");ax.set_yticks(y,["第 1 輪：截斷","第 2 輪：寫檔案","第 3 輪：測試","第 4 輪：結束"]);ax.invert_yaxis();ax.set_xlim(0,44);ax.set_xlabel("秒（逐輪，非連續起點）");ax.legend(loc='lower right',fontsize=10,frameon=False)
for i,z in enumerate(rounds):ax.text(mods[i]+.5,i,f"{mods[i]:.3f} s",va='center',fontsize=10)
a.text(.06,.46,"輸入 / 命中 / 輸出",fontsize=12,weight='bold')
for i,z in enumerate(rounds):
 x=.065+i*.232;box(a,x,.315,.205,.105,f"{z['prompt_tokens']} / {z['cached_tokens']} / {z['output_tokens']}",f"工具段假設保留 {z['retained_logical_kv_bytes']/2**20:.2f} MiB",size=11)
box(a,.06,.12,.24,.105,"分支共享〔教學示意〕","一份字首 + 各自尾部",color='light');box(a,.43,.19,.19,.075,"公共字首",color='light');box(a,.76,.245,.18,.055,"分支 A 尾部",color='sand',size=11);box(a,.76,.14,.18,.055,"分支 B 尾部",color='sand',size=11);arrow(a,(.63,.23),(.75,.27));arrow(a,(.63,.22),(.75,.17))
footer(a,"實測軌跡依序執行；未記錄真實 KV 塊的保留／回收。只加速首輪兩倍：76.510 → 58.323 s，假定其餘行為與品質不變。")
save(f,'figure-3-3-agent');data['3-3']={'kind':'measured_wall_and_conditional_state','rounds':rounds,'summary':ag['summary'],'counterfactual':calc('agent-thinking-on-double-first')['summary']}
# 3-4: stage identity, teaching timing, observed reception.
aud=calc('audio-timing-base');large=calc('audio-timing-large-buffer');intr=calc('audio-timing-interrupt');real=read('experiments/ch03/03-05/historical-arrivals/summary.json')
f,a=canvas("圖 3-4  即時互動的端到端時序","相同任務中，資料到達、開始播放、裝置靜音和後端停止計算是不同事件。",11)
for i,(title,body) in enumerate([("視覺編碼 E","640² → 400 位置\nEC 7.8125 MiB"),("語言 P → D","視覺位置 KV\n56.25 MiB"),("語音生成與接收","聲學碼 → PCM\n到達後進入緩衝"),("裝置播放","首播 / 連續供給\n打斷 / 靜音")]):
 x=.055+i*.235;box(a,x,.71,.195,.12,title,body,size=12)
 if i<3:arrow(a,(x+.20,.77),(x+.225,.77))
a.text(.055,.665,"上方是可組合的階段示意；下方是獨立的八塊音訊教學時序，不是該視覺模型的實測。",fontsize=10.5,color=C['muted'])
ax=f.add_axes([.12,.32,.80,.27]);ch=aud['audio_chunks']
for z in ch:
 i=z['chunk'];start=z['playback_start_ns']/1e6;ax.barh(i,20,left=start,height=.48,color=C['teal']);ax.plot(z['arrival_ns']/1e6,i,'o',color=C['blue']);ax.plot(z['deadline_ns']/1e6,i,'|',markersize=15,color=C['orange'])
ax.plot([],[],'o',color=C['blue'],label="塊到達");ax.plot([],[],'|',markersize=13,color=C['orange'],label="原定播放時刻");ax.barh([],[],color=C['teal'],label="實際播放區間");ax.set_yticks(range(8),[f'塊 {i+1}' for i in range(8)]);ax.invert_yaxis();ax.set_xlim(0,260);ax.set_xticks([0,50,100,150,200,250]);ax.set_xlabel("從採集起點計時 / ms");ax.legend(frameon=False,ncol=3,fontsize=10,loc='upper left',bbox_to_anchor=(0,1.20));ax.annotate("第三塊晚到 5 ms",xy=(123,2),xytext=(167,1.3),arrowprops={'arrowstyle':'->','color':C['orange']},fontsize=10)
box(a,.06,.115,.27,.095,"緩衝對照〔教學〕","40 ms：首播 78，停頓 5 ms\n60 ms：首播 98，無停頓",size=12)
box(a,.365,.115,.27,.095,"打斷投影〔教學〕","123 ms 發出 → 130 ms 靜音\n未模擬後端取消",size=12)
box(a,.67,.115,.27,.095,"上下文接收〔真實記錄〕","首塊 399.919 / 370.459 ms\n首播、靜音、取消未知",size=12)
footer(a,"每塊 20 ms、24 kHz、單聲道、2 bytes/sample：960 bytes；模型與網路時長是教學輸入，裝置播放並非上下文實測。")
save(f,'figure-3-4-realtime');data['3-4']={'kind':'separate_mechanism_teaching_and_historical_reception','audio_chunks':ch,'base_summary':aud['summary'],'large_buffer':large['summary'],'interrupt':intr['summary'],'historical_reception':real,'visual':{'positions':400,'ec_bytes':8192000,'kv_bytes':58982400}}
# 3-5: computational paths, matrices, parameter states.
t=calc('training-qwen3-8b-t8192');f,a=canvas("圖 3-5  推理與各訓練階段的計算和狀態","Qwen3-8B · B=1、T=8192；訓練計算所有詞表頭行，無重計算；各面板使用獨立單位。",9)
for i,(title,body) in enumerate([("前向","儲存反向所需的活化值"),("反向","輸入梯度 + 權重梯度"),("參數更新","權重 / 最佳化器狀態")]):
 x=.07+i*.31;box(a,x,.69,.245,.12,title,body,color=['pale','light','sand'][i]);
 if i<2:arrow(a,(x+.25,.75),(x+.30,.75))
a.text(.07,.625,"推理使用前向；預訓練、中期訓練與 SFT 使用同一基本更新路徑，各階段採用不同的資料、標籤和序列長度。",fontsize=11)
ax=f.add_axes([.10,.23,.37,.29]);vals=[t['summary'][k]/1e12 for k in ['forward_matrix_flops','backward_matrix_flops','training_matrix_flops','six_nd_flops']];ax.barh(range(4),vals,color=[C['blue'],C['teal'],C['ink'],C['orange']]);ax.set_yticks(range(4),["前向矩陣","反向矩陣","兩者合計","總參數 $6ND$"]);ax.invert_yaxis();ax.set_xlim(0,515);ax.set_xlabel('TFLOPs');ax.set_title("A  矩陣分項計算",loc='left',fontsize=13)
for i,v in enumerate(vals):ax.text(v+7,i,f'{v:.3f}',va='center',fontsize=10)
ax=f.add_axes([.64,.23,.29,.29]);states=t['parameter_state_bytes'];labels=["BF16 權重","FP32 梯度",'FP32 master',"Adam 一階","Adam 二階"];sv=[v/1e9 for v in states.values()];ax.barh(range(5),sv,color=[C['blue'],C['teal'],C['orange'],C['muted'],C['muted']]);ax.set_yticks(range(5),labels);ax.invert_yaxis();ax.set_xlim(0,42);ax.set_xlabel("十進位制 GB");ax.set_title("B  未分片的參數相關狀態",loc='left',fontsize=13)
for i,v in enumerate(sv):ax.text(v+.8,i,f'{v:.3f}',va='center',fontsize=10)
a.text(.06,.12,"狀態合計 147.433 GB；活化值和工作區另計。矩陣表未計非矩陣反向、最佳化器算術、重計算與通訊。",fontsize=11)
footer(a,"「三倍前向」來自本例每個矩陣的兩個梯度；不能用全部參數量或可訓練參數佔比推斷任意訓練路徑。")
save(f,'figure-3-5-training');data['3-5']={'kind':'analytical_subaccounts','scenario':t['scenario'],'summary':t['summary'],'parameter_state_bytes':states,'training_matrix_rows':t['training_matrix_rows']}
# 3-6: RL/OPD dataflow and same accepted target.
rl=calc('rl-qwen8-base');low=calc('rl-qwen8-low-acceptance');f,a=canvas("圖 3-6  RL／OPD 的工作與資料流","先統一同一批有效樣本，再比較各階段工作；數值使用 Qwen3-8B 教學設定，不是 V4 執行。",10)
for x,title,body in [(.06,"策略生成","生成的回答"),(.30,"回饋 / 驗證","規則、模型或環境"),(.54,"篩選與組織","選擇訓練樣本"),(.78,"策略更新","前向 / 反向 / 更新")]:box(a,x,.70,.17,.12,title,body,size=12)
for x in [.23,.47,.71]:arrow(a,(x+.004,.76),(x+.06,.76))
box(a,.32,.52,.20,.085,"可選教師前向","OPD：學生軌跡 → 教師分佈",color='sand',size=11);arrow(a,(.15,.695),(.32,.56));arrow(a,(.52,.56),(.78,.715))
arrow(a,(.865,.695),(.865,.445),'orange');arrow(a,(.865,.445),(.145,.445),'orange');arrow(a,(.145,.445),(.145,.695),'orange');a.text(.54,.463,"權重版本就緒後用於下一批生成",ha='center',fontsize=11,color=C['orange'])
ax=f.add_axes([.12,.17,.77,.20]);fields=['rollout_prefill','rollout_decode','reference_scoring','policy_update'];colors=['blue','teal','orange','ink'];labels=["生成輸入","後續生成",'Reference',"更新"];left=np.zeros(2)
for name,lab,col in zip(fields,labels,colors):
 vals=np.array([next(z['matrix_flops'] for z in d['rl_stages'] if z['name']==name)/1e12 for d in [rl,low]]);ax.barh([0,1],vals,left=left,label=lab,color=C[col],height=.45);left+=vals
ax.set_yticks([0,1],["生成 32 條 → 保留 16 條","生成 64 條 → 保留 16 條"]);ax.invert_yaxis();ax.set_xlim(0,4050);ax.set_xlabel("已計矩陣 TFLOPs");ax.legend(ncol=4,frameon=False,fontsize=10,loc='upper center',bbox_to_anchor=(.5,1.37))
for i,v in enumerate(left):ax.text(v+45,i,f'{v:.3f}',va='center',fontsize=10)
footer(a,"本例不呼叫教師模型。一次 BF16 權重快照為 16.381 GB；最佳化器狀態另行儲存。")
save(f,'figure-3-6-rl');data['3-6']={'kind':'teaching_analytical_cycle','base_stages':rl['rl_stages'],'low_acceptance_stages':low['rl_stages'],'base':rl['summary'],'low_acceptance':low['summary'],'scenario':rl['scenario']}
# 3-7: real public points, independent holdout, conditional lifetime proxy.
fit=calc('datablations-real-c4-eight-point-fit');result=fit['primary']['result'];life=calc('real-c4-lifecycle-512-128')['variants'][0];law=result['law']
f=plt.figure(figsize=(15,10));f.suptitle("圖 3-7  訓練預算與生命週期成本",x=.045,y=.97,ha='left',fontsize=24,weight='bold');f.text(.045,.91,"六個 C4 點擬合、兩個事前留出；成本按 40% MFU 折算為 H100 SXM GPU 時間。",fontsize=11,color=C['muted'])
a=f.add_axes([.09,.47,.34,.35]);a.plot([2,7.6],[2,7.6],color=C['line'],lw=1)
resids=[]
for split,col,marker,lab in [('fit','blue','o',"擬合：6 點"),('holdout','orange','^',"留出：2 點")]:
 rows=[z for z in fit['records'] if z['split']==split];obs=[z['loss'] for z in rows];pred=[law['E']+law['A']*(z['N']/law['N0'])**(-law['alpha'])+law['B']*(z['D']/law['D0'])**(-law['beta']) for z in rows];a.scatter(obs,pred,color=C[col],marker=marker,s=75,label=lab);resids += [{'id':z['id'],'split':split,'residual':p-z['loss']} for z,p in zip(rows,pred)]
a.set(xlim=(2,7.6),ylim=(2,7.6),xlabel="觀測損失 / nats·token⁻¹",ylabel="預測損失 / nats·token⁻¹");a.set_title("A  公開點與預測",loc='left',fontsize=13);a.legend(frameon=False,fontsize=10)
a=f.add_axes([.09,.18,.34,.15]);a.bar(range(8),[z['residual'] for z in resids],color=[C['blue'] if z['split']=='fit' else C['orange'] for z in resids]);a.axhline(0,lw=.8,color=C['line']);a.set_xticks(range(8),['F1','F2','F3','F4','F5','F6','H1','H2']);a.set_ylabel("預測 − 觀測");a.set_ylim(-.026,.033);a.set_title("留出 RMSE = 0.019345 nats/token",loc='left',fontsize=11)
a=f.add_axes([.58,.25,.36,.57]);calls=np.linspace(0,4e8,250)
for z,col in zip(life['lifecycle']['rows'],['orange','teal','blue','muted']):a.plot(calls/1e8,(z['upfront_cost']+calls*z['cost_per_call'])/3600,color=C[col],linestyle='--' if z['outside_fit_box'] else '-',lw=2,label=f"{z['N']/1e9:g}B"+("（外推）" if z['outside_fit_box'] else ''))
cross=(life['lifecycle']['rows'][0]['upfront_cost']-life['lifecycle']['rows'][1]['upfront_cost'])/(life['lifecycle']['rows'][1]['cost_per_call']-life['lifecycle']['rows'][0]['cost_per_call']);a.axvline(cross/1e8,color=C['line'],lw=1);a.text(cross/1e8+.06,1000,"0.1B / 0.5B\n約 2.048 億次交叉",fontsize=10);a.set(xlabel="累計呼叫 / 億次",ylabel="H100 SXM GPU 小時",xlim=(0,4),ylim=(0,1200));a.set_title("B  目標損失 2.9 的成本估算",loc='left',fontsize=13);a.legend(frameon=False,fontsize=10)
f.text(.53,.155,"$P=512$、$G=128$；每呼叫 $2N(P+G-1)$。\n0.1B 所需訓練 D≈298.6B，超出擬合上界約 3.28 倍。",fontsize=11,linespacing=1.7)
f.text(.045,.055,"擬合係數依賴這組資料與預定網格；同損失不等於同任務品質。虛線表示模型參數量或訓練資料量超出擬合範圍。",fontsize=10.5,color=C['muted'])
save(f,'figure-3-7-scaling');data['3-7']={'kind':'public_observations_and_conditional_proxy','records':fit['records'],'law':law,'residuals':resids,'fit_sse':result['fit_sse'],'holdout_rmse':result['holdout_rmse'],'lifecycle':life['lifecycle'],'crossing_calls':cross}
# 3-8: historical scale/data and separate MoE parameter categories.
hist=calc('training-history-published');hr={z['input']['id']:z for z in hist['training_history_rows']};ids=['llama1-7b','llama2-7b','llama31-8b','qwen25-7b-proxy','qwen3-8b-proxy'];names=['Llama 1 6.7B\n2023 · 1T','Llama 2 ~7B\n2023 · 2T','Llama 3.1 ~8B\n2024 · ~15T','Qwen2.5 ~7B\n2024 · ~18T','Qwen3 ~8B\n2025 · ~36T']
f,a=canvas("圖 3-8  Llama 與 Qwen 的模型—資料選擇","上下文投入按報告中的模型規模估算；Qwen token 為 family 披露，產品點不是受控 Scaling Law 實驗。",9)
ax=f.add_axes([.16,.26,.30,.51]);ratios=[hr[k]['input']['training_tokens']/hr[k]['input']['parameter_proxy'] for k in ids];ax.barh(range(5),ratios,color=[C['blue']]*3+[C['teal']]*2);ax.set_yticks(range(5),names);ax.invert_yaxis();ax.set_xlim(0,5400);ax.set_xlabel("訓練 token / 參數");ax.set_title("A  相近規模 dense 模型",loc='left',fontsize=13)
for i,v in enumerate(ratios):ax.text(v+90,i,f'{v:,.0f}',va='center',fontsize=10)
ax=f.add_axes([.63,.26,.31,.51]);mids=['deepseek-v3-pretraining','deepseek-v4-flash','deepseek-v4-pro'];ctx=[hr[k]['parameter_context'] for k in mids];y=np.arange(3);tot=[z['total_reported']/1e9 for z in ctx];act=[z['active_reported']/1e9 for z in ctx];ax.barh(y-.17,tot,height=.30,color=C['blue'],label="總參數：估算容量");ax.barh(y+.17,act,height=.30,color=C['orange'],label="每 token 選用參數：估算計算量");ax.set_yticks(y,['V3 · 2024\n14.8T','V4-Flash · 2026\n32T','V4-Pro · 2026\n33T']);ax.invert_yaxis();ax.set_xlim(0,1900);ax.set_xlabel("十億參數 B");ax.set_title("B  MoE 總參數與選用參數",loc='left',fontsize=13);ax.legend(frameon=False,fontsize=10,loc='upper center',bbox_to_anchor=(.5,-.17))
for i,(v,w) in enumerate(zip(tot,act)):ax.text(v+25,i-.17,f'{v:g}',va='center',fontsize=10);ax.text(w+25,i+.17,f'{w:g}',va='center',fontsize=10)
a.text(.06,.135,"D/N 從約 149 到約 4500，說明相近參數規模可投入更多訓練；能力差異還涉及資料、訓練方法和評測。",fontsize=11)
footer(a,"6ND 按給定參數量估算；MoE 每 token 選用參數量不能替代全部矩陣、狀態更新與最佳化器工作，跨模型不據本圖排名品質。")
save(f,'figure-3-8-history');data['3-8']={'kind':'reported_history_and_analytical_ratios','dense_rows':[hr[k] for k in ids],'ratios':ratios,'moe_rows':[hr[k] for k in mids]}
# 3-9: hardware-separated GPU-hour panels, missing values distinct from zero.
f,a=canvas("圖 3-9  公開 GPU 小時與訓練階段","不同裝置分面，橫軸範圍不同；GPU 小時不能直接跨硬體解釋為算力或效率。",9)
for rect,keys,title,lim in [([.13,.40,.21,.37],['llama1-7b','llama1-65b','llama2-7b','llama2-70b'],'A  A100 80GB',2.1),([.48,.40,.20,.37],['llama31-8b','llama31-70b','llama31-405b'],'B  H100 80GB',36)]:
 ax=f.add_axes(rect);vals=[hr[k]['input']['gpu_hours']/1e6 for k in keys];ax.barh(range(len(keys)),vals,color=C['blue']);ax.set_yticks(range(len(keys)),[k.replace('llama31','Llama 3.1').replace('llama1','Llama 1').replace('llama2','Llama 2').replace('-',' ') for k in keys]);ax.invert_yaxis();ax.set_xlim(0,lim);ax.set_title(title,loc='left',fontsize=13);ax.set_xlabel("百萬 GPU 小時")
 for i,v in enumerate(vals):ax.text(v+lim*.025,i,f'{v:.3f}',va='center',fontsize=10)
ax=f.add_axes([.82,.40,.13,.37]);st=hist['stage_reports'][0]['input']['parts'];vals=[st[k]/1e6 for k in ['pretraining','context_extension','posttraining']];ax.barh(range(3),vals,color=[C['blue'],C['teal'],C['orange']]);ax.set_yticks(range(3),["V3 預訓練","上下文擴充","後訓練"]);ax.invert_yaxis();ax.set_xlim(0,3.5);ax.set_title('C  H800',loc='left',fontsize=13);ax.set_xlabel("百萬 GPU 小時")
for i,v in enumerate(vals):ax.text(v+.07,i,f'{v:.3f}',va='center',fontsize=10)
box(a,.06,.155,.41,.115,"未披露完整預訓練 GPU 小時","Qwen2.5 / Qwen3 / Qwen3.5 / V4\n未知值不畫成零",color='pale',size=12)
box(a,.53,.155,.41,.115,"Qwen3 表 21：另一個統計範圍","特定 8B 後訓練：RL 17,920；OPD 1,800 小時\n兩條替代分支，不相加，不填入預訓練列",color='sand',size=12)
footer(a,"Llama 1 65B 在持續 2048 卡假設下約 20.80 天；405B 的 78.43 天需先對齊小時與最大卡數範圍，且只是條件下界。")
save(f,'figure-3-9-gpu-hours');data['3-9']={'kind':'reported_gpu_hours_by_hardware_and_scope','history_rows':hist['training_history_rows'],'stage_reports':hist['stage_reports'],'missing_is_zero':False}
# Additional mechanism diagrams share this chapter's font and output handling.
import sys
sys.path.insert(0,str(HERE.parent))
from teaching_figures import draw as draw_teaching_figures
data['teaching_diagrams']=draw_teaching_figures(3,save,ROOT)

(HERE/'figure-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(HERE/'figure-layout-check.json').write_text(json.dumps({'outside_canvas_text':extent_issues},ensure_ascii=False,indent=2)+'\n')
from teaching_revision import draw as draw_revision
outputs.extend(draw_revision(HERE,data))
outputs=list(dict.fromkeys(outputs))
md=HERE.parent/'03-推理与训练负载.md';raw=md.read_text()
maths=[]
def protect_math(match):
 text=match.group(0);display=text.startswith('$$');latex=text[2:-2] if display else text[1:-1]
 token=f'MATHPLACEHOLDER{len(maths)}END';maths.append({'latex':latex.strip(),'display':display,'token':token})
 return ('\n\n'+token+'\n\n') if display else token
protected=re.sub(r'\$\$[\s\S]*?\$\$|\$[^$\n]+\$',protect_math,raw)
body=markdown.markdown(protected,extensions=['tables','footnotes','fenced_code','toc'],output_format='html')
node_code="const fs=require('fs'),k=require(process.argv[1]);let a=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(a.map(x=>k.renderToString(x.latex,{displayMode:x.display,throwOnError:true,output:'htmlAndMathml'}))))"
result=subprocess.run(['node','-e',node_code,str(HERE/'vendor/katex/katex.js')],input=json.dumps(maths),text=True,capture_output=True)
if result.returncode: raise SystemExit(result.stderr)
rendered=json.loads(result.stdout)
for entry,result in zip(maths,rendered):
 body=body.replace('<p>'+entry['token']+'</p>',result) if entry['display'] else body.replace(entry['token'],result)
math_css=(HERE/'vendor/katex/katex.min.css').read_text()
def font_data(match):
 path=HERE/'vendor/katex'/match[1];suffix=path.suffix[1:]
 return 'url(data:font/'+suffix+';base64,'+base64.b64encode(path.read_bytes()).decode()+')'
math_css=re.sub(r'url\((fonts/[^)]+)\)',font_data,math_css)
body=re.sub(r'<table>(.*?)</table>',r'<div class="table-scroll"><table>\1</table></div>',body,flags=re.S)
(HERE/'math-validation.json').write_text(json.dumps({'renderer':'KaTeX 0.16.11','expressions':len(maths),'display_expressions':sum(x['display'] for x in maths),'errors':[]},indent=2)+'\n')

for p in outputs:
 if p.suffix=='.svg':body=body.replace('src="ch03/'+p.name+'"','src="data:image/png;base64,'+base64.b64encode(p.with_suffix('.png').read_bytes()).decode()+'"')
css='''body{margin:0;background:#fafaf8;color:#243640;font:18px/1.95 Georgia,"Songti SC",serif}main{max-width:960px;margin:auto;padding:50px 38px 90px;background:white}h1,h2,h3{font-family:Arial,"PingFang SC",sans-serif;line-height:1.45;color:#163747}h1{font-size:36px}h2{font-size:28px;border-top:1px solid #d5e1e4;margin-top:65px;padding-top:28px}h3{font-size:23px;margin-top:40px}p{margin:1em 0}a{color:#246f91;text-underline-offset:3px}img{display:block;width:100%;height:auto;margin:26px auto 10px}em{font-size:15px;color:#55707d}table{border-collapse:collapse;width:100%;font-size:15px;line-height:1.7;margin:24px 0}td,th{padding:10px 12px;border-bottom:1px solid #d5e1e4;text-align:left}th{background:#edf4f6}blockquote{margin:28px 0;padding:16px 24px;border-left:4px solid #138b83;background:#f1f8f6;font-size:16px}code{font:0.85em/1.65 Menlo,monospace;background:#f0f4f6;overflow-wrap:anywhere}pre{white-space:pre-wrap}.equation{font:20px/1.8 Georgia,"Songti SC",serif;text-align:center;background:#f7f9fa;padding:18px 12px;margin:25px 0;overflow-wrap:anywhere}nav{font:16px/1.9 Arial,"PingFang SC",sans-serif;background:#f0f6f8;padding:18px 24px}nav a{display:block}.footnote{font-size:14px;line-height:1.8}.footnote li{margin-bottom:12px}@media(max-width:650px){main{padding:25px 18px}body{font-size:17px}table{display:block;overflow-x:auto}h1{font-size:29px}h2{font-size:25px}.equation{font-size:17px}}@media print{main{max-width:none;padding:0}h2,h3{break-after:avoid}img,blockquote{break-inside:avoid}body{font-size:11pt}}'''
css+=' main{max-width:760px}img{max-width:720px}@media print{img{width:420pt;max-width:100%}}'
css+=math_css+' .katex{font-size:1.04em}.katex-display{overflow-x:auto;overflow-y:hidden;padding:12px 0}.table-scroll{overflow-x:auto;max-width:100%}@media(max-width:650px){table{display:table}}'
nav=''.join('<a href="#'+ident+'">'+title+'</a>' for ident,title in re.findall(r'<h2 id="([^"]+)">(3\.\d+ [^<]+)</h2>',body))
page="<!doctype html><html lang=\"zh-CN\"><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>第 3 章 推理與訓練負載</title><style>"+css+'</style><main><nav>'+nav+'</nav>'+body+'</main></html>'
import sys
sys.path.insert(0,str(HERE.parent))
from teaching_reading import readable_diagrams
from preview_output import preview_path
page=readable_diagrams(page)
html_path=preview_path(HERE.parent/"03-推理與訓練負載.html");html_path.write_text(page)
from book_assets import sync_figure_index
active_assets=sync_figure_index(HERE)
artifacts=outputs+[HERE/'figure-data.json',html_path,md]+active_assets
(HERE/'manifest.json').write_text(json.dumps({'chapter':3,'generator':'manuscripts/ch03/build.py','figures':len(re.findall(r'!\[',raw)),'font_family':family,'outputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in artifacts if not (p.parent==ROOT/'manuscripts' and re.match(r'^[01][0-9]-',p.name))]},ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(outputs)} figure files and reading HTML; {len(extent_issues)} text extent warnings.')
