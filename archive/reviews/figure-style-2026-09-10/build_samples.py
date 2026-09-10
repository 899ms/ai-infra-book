"""Independent style studies; existing chapter assets are not rebuilt."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import json
HERE=Path(__file__).resolve().parent
font=Path('/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
font_manager.fontManager.addfont(str(font))
plt.rcParams.update({'font.family':font_manager.FontProperties(fname=str(font)).get_name(),
 'font.size':12,'text.color':'#252525','axes.labelcolor':'#252525',
 'axes.unicode_minus':False,'svg.fonttype':'none','pdf.fonttype':42,
 'figure.facecolor':'white','savefig.facecolor':'white','svg.hashsalt':'infra-style-study-v1'})
C={'blue':'#CBE3F3','green':'#CFE8DB','orange':'#F9DEC0','purple':'#DDCDE8','gray':'#EEEEEE'}
checks=[]
def save(f,name):
 f.canvas.draw();r=f.canvas.get_renderer();outside=[]
 for t in f.findobj(matplotlib.text.Text):
  if t.get_visible() and t.get_text():
   b=t.get_window_extent(r)
   if b.x0<0 or b.y0<0 or b.x1>f.bbox.width or b.y1>f.bbox.height:outside.append(t.get_text())
 checks.append({'name':name,'outside_canvas':outside,'width_pt':420})
 for ext in ['svg','pdf','png']:f.savefig(HERE/f'{name}.{ext}',dpi=240)
 plt.close(f)
def box(a,x,y,w,h,label,color):
 a.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.005,rounding_size=0.008',fc=C[color],ec='#414141',lw=1))
 a.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=12,linespacing=1.35)
def arrow(a,p,q):a.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=11,lw=1,color='#414141'))
f,a=plt.subplots(figsize=(420/72,4.5));f.subplots_adjust(left=.02,right=.98,top=.98,bottom=.02);a.set(xlim=(0,1),ylim=(0,1));a.axis('off')
a.text(.04,.94,'A  保存每个位置的历史',fontsize=14)
for j in range(4):
 x=.07+j*.225;box(a,x,.70,.18,.12,f'位置 {j+1}','blue');arrow(a,(.50,.52),(x+.09,.69))
box(a,.36,.42,.28,.10,'当前查询','orange')
a.text(.5,.36,'序列越长，保存的 K、V 越多',ha='center',fontsize=12)
a.plot([.04,.96],[.31,.31],color='#cccccc',lw=.7)
a.text(.04,.25,'B  更新固定大小的状态',fontsize=14)
box(a,.04,.06,.26,.12,'旧状态','blue');box(a,.39,.06,.22,.12,'更新','green');box(a,.70,.06,.26,.12,'新状态','blue');arrow(a,(.305,.12),(.385,.12));arrow(a,(.615,.12),(.695,.12))
a.text(.5,.205,'当前 k、v',ha='center',fontsize=11);arrow(a,(.5,.20),(.5,.182))
save(f,'sample-history')
f,a=plt.subplots(figsize=(420/72,3.5));f.subplots_adjust(left=.22,right=.90,bottom=.22,top=.82)
labels=['全部分开','融合前两步','三步融合'];base=[60]*3; t=[48,0,0];z=[48,48,0]
a.barh(range(3),base,color=C['blue'],ec='#414141',lw=.8,height=.55)
a.barh(range(3),t,left=base,color=C['orange'],ec='#414141',lw=.8,height=.55)
a.barh(range(3),z,left=[60+v for v in t],color=C['purple'],ec='#414141',lw=.8,height=.55)
for i in range(3):
 a.text(30,i,'60',ha='center',va='center')
 if t[i]:a.text(84,i,'48',ha='center',va='center')
 if z[i]:a.text(60+t[i]+24,i,'48',ha='center',va='center')
 a.text(64+t[i]+z[i],i,str(60+t[i]+z[i]),va='center',fontsize=12)
a.set(yticks=range(3),yticklabels=labels,xlim=(0,177),xticks=[0,60,120,160],xlabel='读写量（MiB）');a.invert_yaxis();a.spines[['top','right','left']].set_visible(False);a.tick_params(axis='y',length=0)
from matplotlib.patches import Patch
f.legend(handles=[Patch(fc=C[c],ec='#414141',label=l) for c,l in [('blue','必要读写'),('orange','中间 T'),('purple','中间 Z')]],loc='upper center',ncol=3,frameon=False,fontsize=11,handlelength=1,columnspacing=1)
save(f,'sample-fusion')
(HERE/'sample-checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
assert not any(c['outside_canvas'] for c in checks), checks
