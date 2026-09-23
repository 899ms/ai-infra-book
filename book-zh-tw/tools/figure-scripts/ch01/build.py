#!/usr/bin/env python3
"""Build chapter-one figures and an HTML reading copy from fixed book evidence.
Usage: python manuscripts/ch01/build.py [--font /path/to/CJK-font.ttf]
"""
from pathlib import Path
import argparse, base64, hashlib, html, json, re, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.transforms import Bbox
import numpy as np
import markdown

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--font');args=parser.parse_args()
import sys
sys.path.insert(0,str(HERE.parent))
from figure_style.typography import configure_font
font_path,family=configure_font(args.font)
plt.rcParams.update({'font.family':[family,'DejaVu Sans'],'font.size':12,'axes.unicode_minus':False,'svg.fonttype':'path',
 'axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#BAC6CD',
 'xtick.color':'#4E6571','ytick.color':'#4E6571','text.color':'#193441','axes.labelcolor':'#193441',
 'figure.facecolor':'white','savefig.facecolor':'white','svg.hashsalt':'ai-infra-ch01-v1'})
C={'ink':'#193441','muted':'#55707D','blue':'#246F91','teal':'#138B83','orange':'#C9782B',
 'pale':'#F0F6F8','line':'#CBD8DF','light':'#E7F3EF','sand':'#FCF2E7'}
source_lock=json.loads((HERE/'sources.json').read_text())
for row in source_lock['sources']:
 p=ROOT/row['path'];actual=hashlib.sha256(p.read_bytes()).hexdigest()
 if actual!=row['sha256']:raise SystemExit(f'Source changed: {row["path"]}; review before rebuilding.')
base=json.loads((ROOT/'calculations/results/decode-budget-base.json').read_text())
# Existing result envelopes retain their independent assumptions and evidence.
res=base['summary']
if 'compute_service_seconds' not in res:
 raise SystemExit('Unexpected decode result structure')
compute_ms=res['compute_service_seconds']*1000
memory_ms=res['memory_service_seconds']*1000
measured=json.loads((ROOT/'experiments/ch01/01-04/results/analysis.json').read_text())
short=sorted([x for x in measured['groups'] if x['kind']=='short'],key=lambda x:x['batch'])
assert [x['batch'] for x in short]==[1,4,16,64]
assert abs(memory_ms-70e9/3.35e12*1000)<1e-9
assert abs(compute_ms-140e9/989.4e12*1000)<1e-9
measure_tp=[x['throughput'] for x in short];measure_tpot=[x['tpot_ms'] for x in short]
data={'historical_latency_ns':{'L1 cache':.5,'L2 cache':7,'Main memory':100,'Datacenter round trip':500000,'Disk seek':10000000},
 'teaching':{'compute_ms':compute_ms,'weight_read_ms':memory_ms,'batch':[1,4,16,64],
 'per_output_resource_lower_bound_ms':[max(compute_ms*b,memory_ms)/b for b in [1,4,16,64]],
 'excluded':['KV and workspace','conversion','non-matrix work','realized efficiency','queueing']},
 'measured_short_group':short,'measurement_scope':'Qwen3-8B BF16 / RTX PRO 6000 Blackwell / vLLM 0.23 eager / 2048 input / 256 forced output / 3 rounds per batch; throughput includes prefill; TPOT client first-to-last output / 255.'}
weight_index=json.loads((ROOT/'calculations/sources/deepseek-r1-distill-llama-70b/model.safetensors.index.json').read_text())
quantized=json.loads((ROOT/'calculations/results/dense-quant-deepseek-r1-distill-llama-70b-tp1-pp8-80gb-8192.json').read_text())
weight_bytes={row['bits']:row['physical_weight_bytes'] for row in quantized['summary']}
assert weight_bytes[16]==weight_index['metadata']['total_size']==141107412992
assert weight_bytes[8]==73725919232
assert weight_bytes[16]>80e9 and weight_bytes[16]/2+5e9<80e9
assert weight_bytes[8]+(2.5+2)*2**30<80e9
assert 3*24e9<weight_bytes[8]<4*24e9
data['capacity_example']={'model':'DeepSeek-R1-Distill-Llama-70B',
 'parameters':weight_bytes[16]//2,'bf16_weight_bytes':weight_bytes[16],
 'int8_weight_and_metadata_bytes':weight_bytes[8],
 'kv_bytes_per_8192_token_request':int(2.5*2**30),'workspace_bytes':2*2**30,
 'h100_nominal_capacity_bytes':80000000000,'rtx4090_nominal_capacity_bytes':24000000000}
from reference_numbers import reference_numbers
data['reference_numbers']=reference_numbers()
assert data['reference_numbers']['calls'][0]['matrix_flops']==29688662589440
assert data['reference_numbers']['calls'][1]['matrix_flops']==16344743936
(HERE/'figure-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
outputs=[]
import sys
sys.path.insert(0,str(HERE.parent))
from math_style import normalize_figure
def save(fig,name):
 normalize_figure(fig)
 # Crop to visible content, excluding the full-canvas bounds of diagram axes.
 fig.canvas.draw()
 renderer=fig.canvas.get_renderer()
 bounds=[]
 for ax in fig.axes:
  if ax.axison:
   bounds.append(ax.get_tightbbox(renderer))
  else:
   for artist in [*ax.texts,*ax.patches,*ax.lines,*ax.collections]:
    if artist.get_visible():
     bound=artist.get_window_extent(renderer)
     if np.isfinite(bound.extents).all() and (bound.width or bound.height):
      bounds.append(bound)
 bounds.extend(t.get_window_extent(renderer) for t in fig.texts if t.get_visible())
 crop=Bbox.union(bounds).transformed(fig.dpi_scale_trans.inverted()).padded(.015)
 for ext in ['svg','png']:
  p=HERE/f'{name}.{ext}';fig.savefig(p,dpi=160,bbox_inches=crop,pad_inches=0,metadata={'Creator':'AI Infra book / chapter 1'} if ext=='svg' else None)
  outputs.append(p)
 plt.close(fig)
def canvas(h=8.5):
 fig=plt.figure(figsize=(13,h));ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
 return fig,ax
def box(ax,x,y,w,h,title,body='',color='pale',size=13):
 p=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.006,rounding_size=0.009',
  lw=1,edgecolor=C['line'],facecolor=C.get(color,color));ax.add_patch(p)
 ax.text(x+w/2,y+h*.68 if body else y+h/2,title,ha='center',va='center',fontsize=size,weight='bold')
 if body:ax.text(x+w/2,y+h*.28,body,ha='center',va='center',fontsize=10.5,color=C['muted'],linespacing=1.5)
 return p
def arrow(ax,a,b,color='teal',both=False,rad=0):
 ax.add_patch(FancyArrowPatch(a,b,arrowstyle='<->' if both else '-|>',mutation_scale=14,
  color=C[color],linewidth=1.5,connectionstyle=f'arc3,rad={rad}'))

# 1-1: editable vector teaching diagram.
fig,ax=canvas(9.7)
layers=[("應用與任務","對話、程式碼、語音；目標與服務要求"),("模型與負載","模型結構、輸入輸出；計算與資料需求"),
 ("訓練與推理系統","請求排程、狀態管理、多裝置執行"),("運算子與編譯執行時","運算子庫、編譯器、裝置執行安排"),
 ("處理器與儲存","CPU、GPU、NPU；主記憶體、視訊記憶體與片上儲存"),("互聯與資料中心","裝置連線、超節點、網路與資源位置")]
for i,(title,body) in enumerate(layers):
 w=.40+i*.04;x=.375-w/2;y=.79-i*.085
 box(ax,x,y,w,.066,title,body,size=13)
 if i<5:arrow(ax,(.375,y-.002),(.375,y-.018))
box(ax,.74,.37,.21,.485,'',color='light')
ax.text(.845,.815,"跨層平台能力",ha='center',fontsize=14,weight='bold')
for y,t,b in [(.72,"資源排程","分配資源與安排任務"),(.59,"執行環境","承載程式碼與隔離任務"),(.46,"觀測與計費","記錄執行與資源消耗")]:
 ax.text(.845,y,t,ha='center',fontsize=13,weight='bold');ax.text(.845,y-.04,b,ha='center',fontsize=10.5,color=C['muted'])
box(ax,.07,.28,.88,.058,"共同物理條件：工藝與封裝 · 供電與散熱 · 容量與可靠性",size=12)
save(fig,'figure-1-1-panorama')

# Separate logical request path from the physical resource map.
fig,ax=canvas(10.5)
for x,title,body in [(.05,"應用／Agent","使用者輸入、上下文、工具結果"),(.37,"服務入口","鑑權、配額、請求檢查"),(.69,"請求路由","目標模型、負載 → 選擇副本")]:
 box(ax,x,.74,.26,.105,title,body,size=13)
arrow(ax,(.315,.793),(.36,.793));arrow(ax,(.635,.793),(.68,.793))
box(ax,.05,.25,.68,.425,'',color='light')
ax.text(.075,.64,"選中的推理實例（可跨多張卡）",fontsize=14,weight='bold')
box(ax,.08,.51,.27,.082,"文字 → token","輸入處理／tokenizer",size=12)
box(ax,.42,.51,.27,.082,"排隊與實例排程","安排 batch、分配狀態空間",size=12)
arrow(ax,(.355,.55),(.41,.55))
ax.plot([.82,.82,.66,.66,.215,.215],[.73,.70,.70,.61,.61,.60],color=C['teal'],lw=1.5)
arrow(ax,(.215,.62),(.215,.595))
box(ax,.08,.365,.27,.092,"CPU 執行時","提交運算子與裝置工作",size=12)
box(ax,.42,.365,.27,.092,"GPU 執行組","prefill → decode 逐步生成",size=12)
arrow(ax,(.555,.50),(.555,.478));ax.plot([.555,.215],[.478,.478],color=C['teal'],lw=1.5);arrow(ax,(.215,.478),(.215,.465))
arrow(ax,(.355,.41),(.41,.41))
box(ax,.42,.275,.27,.048,"HBM：權重、KV、工作區",size=11)
arrow(ax,(.555,.36),(.555,.33),both=True)
ax.text(.215,.292,"多卡時：交換中間結果、同步",ha='center',fontsize=10.5,color=C['muted'])
ax.annotate('',xy=(.70,.39),xytext=(.70,.445),arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=-1.4',color=C['teal'],lw=1.5))
box(ax,.78,.49,.17,.11,"其他模型副本","服務別的請求",size=12)
box(ax,.78,.29,.17,.11,"模型儲存","啟動／切換時載入",size=12)
ax.annotate('',xy=(.70,.299),xytext=(.775,.335),arrowprops=dict(arrowstyle='->',ls='--',color=C['orange'],lw=1.5))
box(ax,.08,.095,.27,.085,"將輸出串流回傳至應用程式","顯示文字／決定是否呼叫工具",size=12)
box(ax,.42,.095,.27,.085,"輸出處理","token → 文字、結束判斷",size=12)
ax.plot([.70,.745,.745,.555],[.37,.37,.21,.21],color=C['teal'],lw=1.5)
arrow(ax,(.555,.21),(.555,.19));arrow(ax,(.415,.138),(.355,.138))
ax.plot([.055,.03,.03,.03],[.138,.138,.79,.79],color=C['teal'],lw=1.3)
arrow(ax,(.03,.79),(.045,.79))
ax.text(.77,.16,"工具回饋可發起下一次呼叫；\n實例內逐 token 迴圈\n不重新選擇外部副本。",fontsize=10.5,color=C['muted'],linespacing=1.7)
save(fig,'figure-1-2-request')

fig,ax=canvas(11)
box(ax,.045,.555,.91,.305,'',color='pale')
ax.text(.07,.825,"資料中心",fontsize=14,weight='bold')
box(ax,.075,.70,.25,.075,"入口與 CPU 服務",size=12)
box(ax,.675,.70,.25,.075,"共享儲存／檢查點",size=12)
box(ax,.37,.70,.25,.075,"資料中心網路","服務、儲存與模型通訊",size=12)
arrow(ax,(.33,.739),(.36,.739),both=True);arrow(ax,(.63,.739),(.665,.739),both=True)
for x,title in [(.08,"超節點 A"),(.39,"超節點 B"),(.70,"超節點 …")]:
 box(ax,x,.585,.22,.067,title,size=12)
 ax.plot([x+.11,x+.11],[.66,.679],color=C['teal'],lw=1.5)
ax.plot([.19,.81],[.679,.679],color=C['teal'],lw=1.5);arrow(ax,(.5,.696),(.5,.681),both=True)
ax.text(.065,.52,"放大超節點 A：伺服器／計算託盤 + 內部高速互聯",fontsize=14,weight='bold')
box(ax,.045,.095,.91,.39,'',color='light')
for x,label in [(.075,"伺服器／計算託盤 1"),(.545,"伺服器／計算託盤 2 …")]:
 box(ax,x,.205,.38,.25,'',color='pale')
 ax.text(x+.19,.429,label,ha='center',fontsize=12,weight='bold')
 box(ax,x+.018,.345,.095,.049,"主記憶體",size=11)
 box(ax,x+.157,.345,.095,.049,'CPU',size=11)
 box(ax,x+.293,.345,.07,.049,'NIC',size=11)
 arrow(ax,(x+.117,.37),(x+.151,.37),both=True)
 arrow(ax,(x+.257,.37),(x+.287,.37),both=True)
 for dx in [.04,.205]:
  box(ax,x+dx,.228,.135,.069,'GPU + HBM',size=11)
  arrow(ax,(x+dx+.067,.221),(x+dx+.067,.174),both=True)
 ax.plot([x+.107,x+.272],[.315,.315],color=C['blue'],lw=1.3)
 arrow(ax,(x+.204,.34),(x+.204,.316),'blue',both=True)
 for dx in [.107,.272]:arrow(ax,(x+dx,.315),(x+dx,.303),'blue',both=True)
 ax.text(x+.19,.321,"主機介面",ha='center',fontsize=8.5,color=C['blue'],bbox=dict(facecolor=C['pale'],edgecolor='none',pad=.1))
box(ax,.09,.112,.81,.055,"超節點內部高速互聯（scale-up）：連線各 GPU，可含交換晶片",color='sand',size=12)
# NIC uplinks leave the supernode; GPU memory traffic need not be CPU-relayed.
for x in [.438,.908]:
 ax.plot([x,x],[.40,.49],color=C['orange'],lw=1.5)
ax.text(.67,.493,"NIC → 跨超節點網路（scale-out）",ha='center',fontsize=10,color=C['orange'])
save(fig,'figure-1-3-datacenter')

# 1-2: primary-source historical numbers and separate hardware resource cards.
fig=plt.figure(figsize=(13,8.8))
fig.text(.055,.905,"A  Jeff Dean，2009：同一時間軸上的不同操作（對數刻度）",fontsize=13,weight='bold')
ax=fig.add_axes([.23,.47,.68,.36]);values=[.5,7,100,500000,10000000]
labels=["L1 快取存取","L2 快取存取","主記憶體存取","同資料中心往返","磁碟尋道"];display=['0.5 ns','7 ns','100 ns','0.5 ms','10 ms']
for i,(v,label) in enumerate(zip(values,display)):
 ax.plot([.1,v],[i,i],color=C['line'],linewidth=3);ax.scatter(v,i,color=C['blue'],s=75,zorder=3)
 ax.annotate(label,(v,i),xytext=(9,0),textcoords='offset points',va='center',fontsize=11)
ax.set_xscale('log');ax.set_xlim(.1,1e9);ax.set_ylim(4.6,-.6);ax.set_yticks(range(5),labels)
ax.set_xticks([1,10,100,1000,1e4,1e5,1e6,1e7,1e8],['1 ns','10 ns','100 ns','1 µs','10 µs','100 µs','1 ms','10 ms','100 ms'])
ax.tick_params(axis='x',labelsize=9);ax.grid(axis='x',color='#E8EFF2');ax.spines['left'].set_visible(False);ax.tick_params(axis='y',length=0,pad=15)
fig.text(.055,.365,"B  H100 SXM：本章固定資源卡（容量、算力與頻寬）",fontsize=13,weight='bold')
bx=fig.add_axes([0,0,1,1]);bx.axis('off');bx.set(xlim=(0,1),ylim=(0,1))
for x,title,val,desc in [(.06,"視訊記憶體容量",'80 GB',"能否同時放下這些資料？"),(.365,"HBM 頻寬",'3.35 TB/s',"讀寫這些位元組至少多久？"),(.67,"矩陣計算吞吐",'989.4 TFLOP/s',"這些矩陣運算至少多久？")]:
 box(bx,x,.13,.27,.185,'',color='pale');bx.text(x+.135,.275,title,ha='center',fontsize=12,color=C['muted'])
 bx.text(x+.135,.22,val,ha='center',fontsize=21,weight='bold',color=C['teal']);bx.text(x+.135,.165,desc,ha='center',fontsize=10.5)
save(fig,'figure-1-4-numbers')

# 1-3: actual fixed results, split teaching and measurement (no fabricated matching).
fig,axs=plt.subplots(2,2,figsize=(13,10));fig.subplots_adjust(left=.095,right=.95,top=.84,bottom=.13,hspace=.55,wspace=.33)
fig.text(.055,.914,"上排：70B／H100 教學下界，僅計權重與近似矩陣運算量",fontsize=12,color=C['blue'])
a=axs[0,0];y=np.arange(3)
a.barh(y-.16,[compute_ms,compute_ms/2,compute_ms],height=.29,label="計算項",color=C['teal'])
a.barh(y+.16,[memory_ms,memory_ms,memory_ms/2],height=.29,label="讀取項",color=C['orange'])
a.set_yticks(y,["基準","算力翻倍","頻寬翻倍"]);a.invert_yaxis();a.set_xscale('log');a.set_xlim(.04,110)
a.set_xticks([.1,1,10,100],['0.1','1','10','100']);a.set_xlabel("資源服務時間（ms，對數刻度）",fontsize=10)
a.set_title("A  先比較計算與讀取",loc='left',fontsize=13,weight='bold',pad=12)
for i,v in enumerate([compute_ms,compute_ms/2,compute_ms]):a.text(v*1.1,i-.16,f'{v:.4f}',va='center',fontsize=10)
for i,v in enumerate([memory_ms,memory_ms,memory_ms/2]):a.text(v*1.08,i+.16,f'{v:.2f}',va='center',fontsize=10)
a.legend(loc='lower right',fontsize=9,frameon=False);a.grid(axis='x',alpha=.15)
a=axs[0,1];batches=[1,4,16,64];share=data['teaching']['per_output_resource_lower_bound_ms']
a.plot(range(4),share,'o-',lw=2.2,color=C['blue']);a.set_yscale('log');a.set_ylim(.2,50);a.set_yticks([.5,1,2,5,10,20],['0.5','1','2','5','10','20'])
a.set_xticks(range(4),batches);a.set_xlabel("理想共享一次權重讀取的請求數",fontsize=10);a.set_ylabel("每輸出分攤下界（ms）",fontsize=10)
a.set_title("B  複用降低每輸出分攤成本",loc='left',fontsize=13,weight='bold',pad=12)
for i,v in enumerate(share):a.annotate(f'{v:.2f}',(i,v),xytext=(0,9),textcoords='offset points',ha='center',fontsize=10)
a.text(.03,.045,"整批下界仍約 20.90 ms；\n分攤成本不是單使用者輸出間隔。",transform=a.transAxes,fontsize=9.5,color=C['muted']);a.grid(axis='y',alpha=.15)
for a,vals,title,ylabel,col in [(axs[1,0],measure_tp,"C  實測：整批吞吐提高","輸出 token/s",C['teal']),
 (axs[1,1],measure_tpot,"D  實測：單請求間隔也增長","客戶端 TPOT（ms）",C['orange'])]:
 a.plot(range(4),vals,'o-',lw=2.2,color=col);a.set_xticks(range(4),batches);a.set_xlabel("同時請求數（按測試檔位）",fontsize=10);a.set_ylabel(ylabel,fontsize=10)
 a.set_title(title,loc='left',fontsize=13,weight='bold',pad=12);a.set_ylim(0,max(vals)*1.25);a.grid(axis='y',alpha=.15)
 for i,v in enumerate(vals):a.annotate(f'{v:.2f}',(i,v),xytext=(0,10),textcoords='offset points',ha='center',fontsize=10)
save(fig,'figure-1-5-budget')


# Additional mechanism diagrams share this chapter's font and output handling.
import sys
sys.path.insert(0,str(HERE.parent))
from teaching_figures import draw as draw_teaching_figures
data['teaching_diagrams']=draw_teaching_figures(1,save,ROOT)
(HERE/'figure-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

from teaching_revision import draw as draw_revision
outputs.extend(draw_revision(HERE,data))
outputs=list(dict.fromkeys(outputs))

# Reading copy: embed PNGs to make display independent of local CJK SVG font support.
md=HERE.parent/'01-初识 AI Infra.md';raw=md.read_text()
import subprocess
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

for name in [p.stem for p in outputs if p.suffix=='.png']:
 encoded=base64.b64encode((HERE/f'{name}.png').read_bytes()).decode()
 body=body.replace(f'src="ch01/{name}.svg"',f'src="data:image/png;base64,{encoded}"')
css='''body{margin:0;background:#fafaf8;color:#243640;font:18px/1.95 Georgia,"Songti SC","Noto Serif CJK SC",serif}main{max-width:900px;margin:auto;padding:60px 36px 100px;background:white}h1,h2,h3{font-family:Arial,"PingFang SC","Noto Sans CJK SC",sans-serif;line-height:1.4;color:#163747}h1{font-size:36px;margin:10px 0 36px}h2{font-size:28px;border-top:1px solid #d5e1e4;margin-top:70px;padding-top:32px}h3{font-size:23px;margin-top:38px}p{margin:1.1em 0}a{color:#167c86;text-underline-offset:3px}img{width:100%;height:auto;display:block;margin:30px auto 16px}img+p,em{color:#59717c}table{border-collapse:collapse;width:100%;font-size:16px;margin:25px 0}th,td{padding:12px;border-bottom:1px solid #d5e1e4;text-align:left}th{background:#edf5f6}pre{background:#f1f6f7;padding:20px;overflow:auto;line-height:1.8;font-size:15px}code{font-family:Menlo,Consolas,monospace}blockquote{margin:30px 0;padding:5px 22px;border-left:4px solid #218a83;background:#f1f7f4;font-size:17px}.footnote{margin-top:70px;font-size:14px;line-height:1.8}.edition{font:13px Arial,sans-serif;letter-spacing:.12em;color:#68828c}.nav{font:15px/2 Arial,"PingFang SC",sans-serif;border:1px solid #d5e1e4;background:#f6f9f9;padding:16px 22px;margin-bottom:32px}.nav a{display:block}@media(max-width:650px){main{padding:26px 18px 65px}body{font-size:17px}h1{font-size:30px}h2{font-size:25px}table{font-size:13px}th,td{padding:8px}}@media print{body{background:white;font-size:11pt}main{max-width:none;padding:0}h2,h3{break-after:avoid}img,table,blockquote{break-inside:avoid}.nav,.edition{display:none}a{color:inherit}}'''
css+=' main{max-width:760px}img{max-width:720px} @media print{img{width:420pt;max-width:100%}main{max-width:none}}'
css+=math_css+' .katex{font-size:1.04em}.katex-display{overflow-x:auto;overflow-y:hidden;padding:12px 0}.table-scroll{overflow-x:auto;max-width:100%}'
heads=re.findall(r'<h2 id="([^"]+)">([^<]+)</h2>',body)
nav="<nav class=\"nav\" aria-label=\"本章目录\">"+''.join(f'<a href="#{html.escape(k)}">{html.escape(v)}</a>' for k,v in heads)+'</nav>'
page="<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>第 1 章 初識 AI Infra</title><style>"+css+"</style></head><body><main><div class=\"edition\">AI INFRA · 第一章圖文修訂 · 2026-09-10</div>"+nav+body+'</main></body></html>'
import sys
sys.path.insert(0,str(HERE.parent))
from teaching_reading import readable_diagrams
from preview_output import preview_path
page=readable_diagrams(page)
ht=preview_path(md);ht.write_text(page);outputs.append(ht)
from book_assets import sync_figure_index
outputs.extend(sync_figure_index(HERE))
manifest={'source_lock':'sources.json','font':str(font_path),'matplotlib':matplotlib.__version__,
 'chapter':{'file':str(md.relative_to(ROOT)),'sha256':hashlib.sha256(md.read_bytes()).hexdigest()},
 'outputs':[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in outputs]}
(HERE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'figures':len(re.findall(r'!\[',raw)),'formats':['SVG','PNG','PDF'],'html':str(ht),'font':family},ensure_ascii=False))
