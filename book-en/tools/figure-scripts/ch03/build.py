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
f,a=canvas("Figure 3-1  Prefill and Decode of the Same Model","Qwen3-8B · S=6144, P=2048, G=4 · BF16 logical KV, 144 KiB per token.",8)
box(a,.06,.70,.20,.105,"restored prefix","6144 tokens",color='light')
box(a,.32,.70,.23,.105,"Prefill: process new input","2048 tokens → first output $y_1$",color='sand');arrow(a,(.265,.75),(.31,.75))
a.text(.60,.75,"time order →",fontsize=12,color=C['muted']);a.text(.60,.70,"width does not represent actual duration",fontsize=10)
for i in range(3):
 x=.32+i*.215;box(a,x,.46,.175,.12,f'Decode {i+1}',f'input $y_{i+1}$ → output $y_{i+2}$',color='pale')
 if i<2:arrow(a,(x+.18,.52),(x+.205,.52))
arrow(a,(.43,.69),(.405,.59))
a.text(.055,.515,"only\n$G-1=3$ calls needed after",fontsize=13,linespacing=1.8)
for i,(slots,label) in enumerate([(8192,"after prefill"),(8193,"after decode 1"),(8194,"after decode 2"),(8195,"after decode 3")]):
 x=.07+i*.23;box(a,x,.22,.19,.12,label,f'{slots} positions',color='light')
a.text(.055,.125,"Baseline: 8192 positions = 1.125 GiB; three decodes add 432 KiB total. No re-entry into model after $y_4$ returns.",fontsize=12)
footer(a,"Prefix hits reduce recomputation, but new input and subsequent generation can still read existing context; V4 state uses respective structural accounting from Chapter 2.")
save(f,'figure-3-1-stages');data['3-1']={'kind':'teaching_structure','S':6144,'P':2048,'G':4,'kv_bytes_per_position':147456,'slots_after_calls':[8192,8193,8194,8195]}
# 3-2: workload composition, observed metrics and explicit fluid queue.
arrival=read('experiments/ch03/03-02/results/summary.json')['reports']
f=plt.figure(figsize=(15,11));f.suptitle("Figure 3-2  Conversation Length and Thinking Budget",x=.045,ha='left',y=.97,fontsize=24,weight='bold');f.text(.045,.916,"Teaching composition, actual replay, and quality diagnostics shown separately; two 60-second windows, 480 requests per group.",fontsize=11,color=C['muted'])
axs=[f.add_axes(z) for z in [[.08,.59,.37,.25],[.57,.59,.36,.25],[.08,.17,.37,.27],[.57,.17,.36,.27]]]
a=axs[0];labels=["uniform\nfront/back window","varying\nfront window","varying\nback window"];A=np.array([.5,.9,.1]);a.bar(range(3),A,color=C['blue'],label="A: 8192 input / 256 output");a.bar(range(3),1-A,bottom=A,color=C['orange'],label="B: 1024 input / 2048 output");a.set_xticks(range(3),labels);a.set_ylim(0,1.1);a.set_ylabel("request ratio");a.set_title("A  Same total, different short-window composition [teaching]",loc='left',fontsize=13);a.legend(fontsize=9,frameon=False,loc='upper left',bbox_to_anchor=(0,-.20))
a=axs[1];pref=np.array([18432,29900.8,6963.2]);dec=np.array([4604,1736.8,7471.2]);x=np.arange(3);a.bar(x-.18,pref,width=.35,label="input tokens/s",color=C['blue']);a.bar(x+.18,dec,width=.35,label="decode steps/s",color=C['teal']);a.set_xticks(x,labels);a.set_ylabel("stage positions / s");a.set_title("B  Input and subsequent generation demand [teaching]",loc='left',fontsize=13);a.legend(fontsize=9,frameon=False)
a=axs[2];x=np.arange(2)
for i,(field,lab,col) in enumerate([('ttft_p95_s','TTFT p95','blue'),('latency_p95_s',"complete request p95",'teal')]):a.bar(x+(i-.5)*.32,[z[field] for z in arrival],width=.30,label=lab,color=C[col])
a.set_xticks(x,["uniform","time-of-day variation"]);a.set_ylim(0,355);a.set_ylabel("seconds");a.set_title("C  Actual replay of same instance",loc='left',fontsize=13);a.legend(frameon=False,fontsize=10)
for i,z in enumerate(arrival):a.text(i,320,f"preemption {z['preemptions']} times",ha='center',fontsize=10)
decode_card=[z for z in calc('batch-reuse-rtxpro6000-mix')['batch_reuse_rows'] if z['batch']==64][0];decode_cards=2;service=decode_cards*decode_card['throughput_upper_tokens_per_second'];peak_backlog=(dec[2]-service)*60
a=axs[3];seconds=np.array([0,60,120,120+peak_backlog/service]);backlog=np.array([0,0,peak_backlog,0]);a.plot(seconds,backlog,color=C['orange'],lw=2.5,marker='o');a.axvline(120,color=C['muted'],ls='--',lw=1);a.set_title("D  Backlog under fixed service rate [teaching]",loc='left',fontsize=13);a.set_xlabel("time from request arrival / s");a.set_ylabel("pending decode steps");a.set_ylim(0,140000);a.annotate(f'{peak_backlog:,.0f}step',xy=(120,peak_backlog),xytext=(40,127000),arrowprops={'arrowstyle':'->'},fontsize=11);a.grid(alpha=.15)
save(f,'figure-3-2-workload-budget');data['3-2']={'kind':'separate_teaching_and_measurement','A_fraction':A.tolist(),'prefill_positions_per_second':pref.tolist(),'decode_positions_per_second':dec.tolist(),'arrival_reports':arrival,'fluid_queue':{'device':'rtx-pro6000-blackwell-ws','cards':decode_cards,'batch_per_card':64,'mean_context_tokens':2742,'service_steps_per_second':service,'seconds':seconds.tolist(),'backlog_steps':backlog.tolist()}}
# 3-3: measured round durations, engine hits, and explicitly hypothetical retention.
ag=calc('agent-thinking-on');rounds=ag['agent_rounds'];f,a=canvas("Figure 3-3  Agent Trajectory and KV Lifecycle","Four-round manual code task with thinking enabled; model/tool are wall-clock observations, cache size is conditional logical budget.",10)
ax=f.add_axes([.12,.55,.79,.27]);y=np.arange(4);mods=[z['measured_model_seconds'] for z in rounds];tools=[z['measured_tool_seconds'] for z in rounds]
ax.barh(y,mods,color=C['blue'],label="model wall clock");ax.barh(y,tools,left=mods,color=C['orange'],label="tool wall clock (short in this example)");ax.set_yticks(y,["Round 1: truncation","Round 2: write file","Round 3: test","Round 4: end"]);ax.invert_yaxis();ax.set_xlim(0,44);ax.set_xlabel("seconds (per round, non-continuous start)");ax.legend(loc='lower right',fontsize=10,frameon=False)
for i,z in enumerate(rounds):ax.text(mods[i]+.5,i,f"{mods[i]:.3f} s",va='center',fontsize=10)
a.text(.06,.46,"input / hit / output",fontsize=12,weight='bold')
for i,z in enumerate(rounds):
 x=.065+i*.232;box(a,x,.315,.205,.105,f"{z['prompt_tokens']} / {z['cached_tokens']} / {z['output_tokens']}",f"tool segment assumed retained {z['retained_logical_kv_bytes']/2**20:.2f} MiB",size=11)
box(a,.06,.12,.24,.105,"branch sharing [teaching illustration]","one prefix + separate tails",color='light');box(a,.43,.19,.19,.075,"common prefix",color='light');box(a,.76,.245,.18,.055,"branch A tail",color='sand',size=11);box(a,.76,.14,.18,.055,"branch B tail",color='sand',size=11);arrow(a,(.63,.23),(.75,.27));arrow(a,(.63,.22),(.75,.17))
footer(a,"Measured trajectory is serial; actual KV block retention/reclamation not recorded. Only first round sped up 2×: 76.510 → 58.323 s, assuming remaining behavior and quality unchanged.")
save(f,'figure-3-3-agent');data['3-3']={'kind':'measured_wall_and_conditional_state','rounds':rounds,'summary':ag['summary'],'counterfactual':calc('agent-thinking-on-double-first')['summary']}
# 3-4: stage identity, teaching timing, observed reception.
aud=calc('audio-timing-base');large=calc('audio-timing-large-buffer');intr=calc('audio-timing-interrupt');real=read('experiments/ch03/03-05/historical-arrivals/summary.json')
f,a=canvas("Figure 3-4  End-to-End Timing of Real-Time Interaction","Within same task, data arrival, playback start, device mute, and backend compute stop are different events.",11)
for i,(title,body) in enumerate([("vision encoding E","640² → 400 positions\nEC 7.8125 MiB"),("language P → D","vision position KV\n56.25 MiB"),("speech generation and reception","acoustic code → PCM\nbuffered on arrival"),("device playback","first playback / continuous supply\ninterruption / mute")]):
 x=.055+i*.235;box(a,x,.71,.195,.12,title,body,size=12)
 if i<3:arrow(a,(x+.20,.77),(x+.225,.77))
a.text(.055,.665,"Above is composable stage illustration; below is independent eight-chunk audio teaching timing, not actual measurement of this visual model.",fontsize=10.5,color=C['muted'])
ax=f.add_axes([.12,.32,.80,.27]);ch=aud['audio_chunks']
for z in ch:
 i=z['chunk'];start=z['playback_start_ns']/1e6;ax.barh(i,20,left=start,height=.48,color=C['teal']);ax.plot(z['arrival_ns']/1e6,i,'o',color=C['blue']);ax.plot(z['deadline_ns']/1e6,i,'|',markersize=15,color=C['orange'])
ax.plot([],[],'o',color=C['blue'],label="chunk arrival");ax.plot([],[],'|',markersize=13,color=C['orange'],label="scheduled playback time");ax.barh([],[],color=C['teal'],label="actual playback interval");ax.set_yticks(range(8),[f'block {i+1}' for i in range(8)]);ax.invert_yaxis();ax.set_xlim(0,260);ax.set_xticks([0,50,100,150,200,250]);ax.set_xlabel("time from capture start / ms");ax.legend(frameon=False,ncol=3,fontsize=10,loc='upper left',bbox_to_anchor=(0,1.20));ax.annotate("third chunk arrives 5 ms late",xy=(123,2),xytext=(167,1.3),arrowprops={'arrowstyle':'->','color':C['orange']},fontsize=10)
box(a,.06,.115,.27,.095,"buffer comparison [teaching]","40 ms: first play 78, stall 5 ms\n60 ms: first play 98, no stall",size=12)
box(a,.365,.115,.27,.095,"interruption projection [teaching]","123 ms sent → 130 ms mute\nbackend cancellation not simulated",size=12)
box(a,.67,.115,.27,.095,"context receipt [actual record]","First chunk 399.919 / 370.459 ms\nFirst playback, mute, cancel unknown",size=12)
footer(a,"Each chunk 20 ms, 24 kHz, mono, 2 bytes/sample: 960 bytes; model and network durations are illustrative inputs, device playback is not measured in context.")
save(f,'figure-3-4-realtime');data['3-4']={'kind':'separate_mechanism_teaching_and_historical_reception','audio_chunks':ch,'base_summary':aud['summary'],'large_buffer':large['summary'],'interrupt':intr['summary'],'historical_reception':real,'visual':{'positions':400,'ec_bytes':8192000,'kv_bytes':58982400}}
# 3-5: computational paths, matrices, parameter states.
t=calc('training-qwen3-8b-t8192');f,a=canvas("Figure 3-5  Compute and State across Inference and Training Stages","Qwen3-8B · B=1, T=8192; training computes all vocab head rows, no recomputation; each panel uses independent units.",9)
for i,(title,body) in enumerate([("forward","save activations for backward"),("backward","input gradient + weight gradient"),("parameter update","weights / optimizer state")]):
 x=.07+i*.31;box(a,x,.69,.245,.12,title,body,color=['pale','light','sand'][i]);
 if i<2:arrow(a,(x+.25,.75),(x+.30,.75))
a.text(.07,.625,"Inference uses forward pass; pretraining, mid-stage training, and SFT use same basic update path, with different data, labels, and sequence lengths per stage.",fontsize=11)
ax=f.add_axes([.10,.23,.37,.29]);vals=[t['summary'][k]/1e12 for k in ['forward_matrix_flops','backward_matrix_flops','training_matrix_flops','six_nd_flops']];ax.barh(range(4),vals,color=[C['blue'],C['teal'],C['ink'],C['orange']]);ax.set_yticks(range(4),["forward matrix","backward matrix","combined total","total parameters $6ND$"]);ax.invert_yaxis();ax.set_xlim(0,515);ax.set_xlabel('TFLOPs');ax.set_title("A  Matrix-wise Compute Breakdown",loc='left',fontsize=13)
for i,v in enumerate(vals):ax.text(v+7,i,f'{v:.3f}',va='center',fontsize=10)
ax=f.add_axes([.64,.23,.29,.29]);states=t['parameter_state_bytes'];labels=["BF16 weights","FP32 gradients",'FP32 master',"Adam 1st moment","Adam 2nd moment"];sv=[v/1e9 for v in states.values()];ax.barh(range(5),sv,color=[C['blue'],C['teal'],C['orange'],C['muted'],C['muted']]);ax.set_yticks(range(5),labels);ax.invert_yaxis();ax.set_xlim(0,42);ax.set_xlabel("decimal GB");ax.set_title("B  Unsharded Parameter-Related State",loc='left',fontsize=13)
for i,v in enumerate(sv):ax.text(v+.8,i,f'{v:.3f}',va='center',fontsize=10)
a.text(.06,.12,"Total state 147.433 GB; activations and workspace counted separately. Matrix table excludes non-matrix backward, optimizer arithmetic, recomputation, and communication.",fontsize=11)
footer(a,"\"Triple forward\" comes from two gradients per matrix in this example; cannot infer arbitrary training path from total parameter count or trainable parameter ratio.")
save(f,'figure-3-5-training');data['3-5']={'kind':'analytical_subaccounts','scenario':t['scenario'],'summary':t['summary'],'parameter_state_bytes':states,'training_matrix_rows':t['training_matrix_rows']}
# 3-6: RL/OPD dataflow and same accepted target.
rl=calc('rl-qwen8-base');low=calc('rl-qwen8-low-acceptance');f,a=canvas("Figure 3-6  RL/OPD Work and Data Flow","First normalize valid samples in same batch, then compare stage work; values use Qwen3-8B teaching configuration, not V4 run.",10)
for x,title,body in [(.06,"policy generation","generated response"),(.30,"feedback / verification","rules, model, or environment"),(.54,"filtering and organization","select training samples"),(.78,"policy update","forward / backward / update")]:box(a,x,.70,.17,.12,title,body,size=12)
for x in [.23,.47,.71]:arrow(a,(x+.004,.76),(x+.06,.76))
box(a,.32,.52,.20,.085,"optional teacher forward pass","OPD: student trajectory → teacher distribution",color='sand',size=11);arrow(a,(.15,.695),(.32,.56));arrow(a,(.52,.56),(.78,.715))
arrow(a,(.865,.695),(.865,.445),'orange');arrow(a,(.865,.445),(.145,.445),'orange');arrow(a,(.145,.445),(.145,.695),'orange');a.text(.54,.463,"weight version ready for next batch generation",ha='center',fontsize=11,color=C['orange'])
ax=f.add_axes([.12,.17,.77,.20]);fields=['rollout_prefill','rollout_decode','reference_scoring','policy_update'];colors=['blue','teal','orange','ink'];labels=["generation input","subsequent generation",'Reference',"update"];left=np.zeros(2)
for name,lab,col in zip(fields,labels,colors):
 vals=np.array([next(z['matrix_flops'] for z in d['rl_stages'] if z['name']==name)/1e12 for d in [rl,low]]);ax.barh([0,1],vals,left=left,label=lab,color=C[col],height=.45);left+=vals
ax.set_yticks([0,1],["generate 32 → keep 16","generate 64 → keep 16"]);ax.invert_yaxis();ax.set_xlim(0,4050);ax.set_xlabel("counted matrix TFLOPs");ax.legend(ncol=4,frameon=False,fontsize=10,loc='upper center',bbox_to_anchor=(.5,1.37))
for i,v in enumerate(left):ax.text(v+45,i,f'{v:.3f}',va='center',fontsize=10)
footer(a,"This example doesn't call teacher model. One BF16 weight snapshot is 16.381 GB; optimizer state saved separately.")
save(f,'figure-3-6-rl');data['3-6']={'kind':'teaching_analytical_cycle','base_stages':rl['rl_stages'],'low_acceptance_stages':low['rl_stages'],'base':rl['summary'],'low_acceptance':low['summary'],'scenario':rl['scenario']}
# 3-7: real public points, independent holdout, conditional lifetime proxy.
fit=calc('datablations-real-c4-eight-point-fit');result=fit['primary']['result'];life=calc('real-c4-lifecycle-512-128')['variants'][0];law=result['law']
f=plt.figure(figsize=(15,10));f.suptitle("Figure 3-7 Training Budget and Lifecycle Cost",x=.045,y=.97,ha='left',fontsize=24,weight='bold');f.text(.045,.91,"Six C4 points fitted, two held out in advance; cost converted to H100 SXM GPU time at 40% MFU.",fontsize=11,color=C['muted'])
a=f.add_axes([.09,.47,.34,.35]);a.plot([2,7.6],[2,7.6],color=C['line'],lw=1)
resids=[]
for split,col,marker,lab in [('fit','blue','o',"fit: 6 points"),('holdout','orange','^',"held out: 2 points")]:
 rows=[z for z in fit['records'] if z['split']==split];obs=[z['loss'] for z in rows];pred=[law['E']+law['A']*(z['N']/law['N0'])**(-law['alpha'])+law['B']*(z['D']/law['D0'])**(-law['beta']) for z in rows];a.scatter(obs,pred,color=C[col],marker=marker,s=75,label=lab);resids += [{'id':z['id'],'split':split,'residual':p-z['loss']} for z,p in zip(rows,pred)]
a.set(xlim=(2,7.6),ylim=(2,7.6),xlabel="observed loss / nats·token⁻¹",ylabel="predicted loss / nats·token⁻¹");a.set_title("A Public Points and Predictions",loc='left',fontsize=13);a.legend(frameon=False,fontsize=10)
a=f.add_axes([.09,.18,.34,.15]);a.bar(range(8),[z['residual'] for z in resids],color=[C['blue'] if z['split']=='fit' else C['orange'] for z in resids]);a.axhline(0,lw=.8,color=C['line']);a.set_xticks(range(8),['F1','F2','F3','F4','F5','F6','H1','H2']);a.set_ylabel("predicted − observed");a.set_ylim(-.026,.033);a.set_title("Held-out RMSE = 0.019345 nats/token",loc='left',fontsize=11)
a=f.add_axes([.58,.25,.36,.57]);calls=np.linspace(0,4e8,250)
for z,col in zip(life['lifecycle']['rows'],['orange','teal','blue','muted']):a.plot(calls/1e8,(z['upfront_cost']+calls*z['cost_per_call'])/3600,color=C[col],linestyle='--' if z['outside_fit_box'] else '-',lw=2,label=f"{z['N']/1e9:g}B"+("(extrapolation)" if z['outside_fit_box'] else ''))
cross=(life['lifecycle']['rows'][0]['upfront_cost']-life['lifecycle']['rows'][1]['upfront_cost'])/(life['lifecycle']['rows'][1]['cost_per_call']-life['lifecycle']['rows'][0]['cost_per_call']);a.axvline(cross/1e8,color=C['line'],lw=1);a.text(cross/1e8+.06,1000,"0.1B / 0.5B\n~204.8M crossings",fontsize=10);a.set(xlabel="cumulative calls / 100M",ylabel="H100 SXM GPU-hours",xlim=(0,4),ylim=(0,1200));a.set_title("B Cost Estimate for Target Loss 2.9",loc='left',fontsize=13);a.legend(frameon=False,fontsize=10)
f.text(.53,.155,"$P=512$, $G=128$; per call $2N(P+G-1)$.\n0.1B requires training D≈298.6B, ~3.28× beyond fit upper bound.",fontsize=11,linespacing=1.7)
f.text(.045,.055,"Fit coefficients depend on this dataset and preset grid; same loss doesn't mean same task quality. Dashed line indicates model parameters or training data beyond fit range.",fontsize=10.5,color=C['muted'])
save(f,'figure-3-7-scaling');data['3-7']={'kind':'public_observations_and_conditional_proxy','records':fit['records'],'law':law,'residuals':resids,'fit_sse':result['fit_sse'],'holdout_rmse':result['holdout_rmse'],'lifecycle':life['lifecycle'],'crossing_calls':cross}
# 3-8: historical scale/data and separate MoE parameter categories.
hist=calc('training-history-published');hr={z['input']['id']:z for z in hist['training_history_rows']};ids=['llama1-7b','llama2-7b','llama31-8b','qwen25-7b-proxy','qwen3-8b-proxy'];names=['Llama 1 6.7B\n2023 · 1T','Llama 2 ~7B\n2023 · 2T','Llama 3.1 ~8B\n2024 · ~15T','Qwen2.5 ~7B\n2024 · ~18T','Qwen3 ~8B\n2025 · ~36T']
f,a=canvas("Figure 3-8 Llama and Qwen Model–Data Selection","Context input estimated from model scale in reports; Qwen tokens are family-disclosed, product points aren't controlled Scaling Law experiments.",9)
ax=f.add_axes([.16,.26,.30,.51]);ratios=[hr[k]['input']['training_tokens']/hr[k]['input']['parameter_proxy'] for k in ids];ax.barh(range(5),ratios,color=[C['blue']]*3+[C['teal']]*2);ax.set_yticks(range(5),names);ax.invert_yaxis();ax.set_xlim(0,5400);ax.set_xlabel("training tokens / parameters");ax.set_title("A Similar-Scale Dense Models",loc='left',fontsize=13)
for i,v in enumerate(ratios):ax.text(v+90,i,f'{v:,.0f}',va='center',fontsize=10)
ax=f.add_axes([.63,.26,.31,.51]);mids=['deepseek-v3-pretraining','deepseek-v4-flash','deepseek-v4-pro'];ctx=[hr[k]['parameter_context'] for k in mids];y=np.arange(3);tot=[z['total_reported']/1e9 for z in ctx];act=[z['active_reported']/1e9 for z in ctx];ax.barh(y-.17,tot,height=.30,color=C['blue'],label="total params: capacity estimate");ax.barh(y+.17,act,height=.30,color=C['orange'],label="active params: FLOPs estimate");ax.set_yticks(y,['V3 · 2024\n14.8T','V4-Flash · 2026\n32T','V4-Pro · 2026\n33T']);ax.invert_yaxis();ax.set_xlim(0,1900);ax.set_xlabel("billion parameters B");ax.set_title("B MoE Total and Activated Parameters",loc='left',fontsize=13);ax.legend(frameon=False,fontsize=10,loc='upper center',bbox_to_anchor=(.5,-.17))
for i,(v,w) in enumerate(zip(tot,act)):ax.text(v+25,i-.17,f'{v:g}',va='center',fontsize=10);ax.text(w+25,i+.17,f'{w:g}',va='center',fontsize=10)
a.text(.06,.135,"D/N ranges from ~149 to ~4500, showing similar parameter counts can absorb more training; capability differences also involve data, training methods, and evaluation.",fontsize=11)
footer(a,"6ND estimated from given parameter count; MoE activated params can't replace full matrix, state update, and optimizer work; don't rank quality across models from this figure.")
save(f,'figure-3-8-history');data['3-8']={'kind':'reported_history_and_analytical_ratios','dense_rows':[hr[k] for k in ids],'ratios':ratios,'moe_rows':[hr[k] for k in mids]}
# 3-9: hardware-separated GPU-hour panels, missing values distinct from zero.
f,a=canvas("Figure 3-9 Public GPU Hours and Training Stages","Different device facets, different x-axis ranges; GPU hours can't be directly interpreted across hardware as compute power or efficiency.",9)
for rect,keys,title,lim in [([.13,.40,.21,.37],['llama1-7b','llama1-65b','llama2-7b','llama2-70b'],'A  A100 80GB',2.1),([.48,.40,.20,.37],['llama31-8b','llama31-70b','llama31-405b'],'B  H100 80GB',36)]:
 ax=f.add_axes(rect);vals=[hr[k]['input']['gpu_hours']/1e6 for k in keys];ax.barh(range(len(keys)),vals,color=C['blue']);ax.set_yticks(range(len(keys)),[k.replace('llama31','Llama 3.1').replace('llama1','Llama 1').replace('llama2','Llama 2').replace('-',' ') for k in keys]);ax.invert_yaxis();ax.set_xlim(0,lim);ax.set_title(title,loc='left',fontsize=13);ax.set_xlabel("million GPU hours")
 for i,v in enumerate(vals):ax.text(v+lim*.025,i,f'{v:.3f}',va='center',fontsize=10)
ax=f.add_axes([.82,.40,.13,.37]);st=hist['stage_reports'][0]['input']['parts'];vals=[st[k]/1e6 for k in ['pretraining','context_extension','posttraining']];ax.barh(range(3),vals,color=[C['blue'],C['teal'],C['orange']]);ax.set_yticks(range(3),["V3 pretraining","context extension","post-training"]);ax.invert_yaxis();ax.set_xlim(0,3.5);ax.set_title('C  H800',loc='left',fontsize=13);ax.set_xlabel("million GPU hours")
for i,v in enumerate(vals):ax.text(v+.07,i,f'{v:.3f}',va='center',fontsize=10)
box(a,.06,.155,.41,.115,"full pretraining GPU hours undisclosed","Qwen2.5 / Qwen3 / Qwen3.5 / V4\nUnknown values not plotted as zero",color='pale',size=12)
box(a,.53,.155,.41,.115,"Qwen3 Table 21: different statistical scope","Specific 8B post-training: RL 17,920; OPD 1,800 hours\ntwo alternative branches, not summed, not filled into pretraining column",color='sand',size=12)
footer(a,"Llama 1 65B at sustained 2048-card assumption ~20.80 days; 405B's 78.43 days requires first aligning hours and max card range, and is only a conditional lower bound.")
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
page="<!doctype html><html lang=\"en\"><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Chapter 3 Inference and Training Workloads</title><style>"+css+'</style><main><nav>'+nav+'</nav>'+body+'</main></html>'
import sys
sys.path.insert(0,str(HERE.parent))
from teaching_reading import readable_diagrams
from preview_output import preview_path
page=readable_diagrams(page)
html_path=preview_path(HERE.parent/"03-inference-and-training-workloads.html");html_path.write_text(page)
from book_assets import sync_figure_index
active_assets=sync_figure_index(HERE)
artifacts=outputs+[HERE/'figure-data.json',html_path,md]+active_assets
(HERE/'manifest.json').write_text(json.dumps({'chapter':3,'generator':'manuscripts/ch03/build.py','figures':len(re.findall(r'!\[',raw)),'font_family':family,'outputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in artifacts if not (p.parent==ROOT/'manuscripts' and re.match(r'^[01][0-9]-',p.name))]},ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(outputs)} figure files and reading HTML; {len(extent_issues)} text extent warnings.')
