#!/usr/bin/env python3
"""Book-size roadmap using the shared Hands-On LLM-inspired figure style."""
from pathlib import Path
import sys,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from figure_style import COL,STYLE,Exporter
from figure_style.typography import configure_font
_,family=configure_font()
plt.rcParams.update(STYLE)
plt.rcParams.update({'font.family':family,'svg.hashsalt':'ai-infra-book-roadmap'})
# Coordinates are points, so label size and space can be checked at print size.
fig=plt.figure(figsize=(420/72,280/72))
ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,420),ylim=(0,280));ax.axis('off')
rows=[(204,72,'blue','第一部分  模型与负载',
       ['1  初识 AI Infra','2  模型架构','3  推理与训练负载']),
      (116,72,'green','第二部分  芯片与系统',
       ['4  加速器架构','5  算子与运行时','6  超节点','7  数据中心网络']),
      (4,96,'orange','第三部分  推理与训练系统',
       ['8  推理优化','9  分布式推理','10  训练系统','11  资源调度与运行环境','12  端边云协同'])]
for y,h,color,title,chapters in rows:
 ax.add_patch(FancyBboxPatch((4,y),412,h,boxstyle='round,pad=0,rounding_size=4',
                            facecolor=COL[color],edgecolor=COL['line'],linewidth=.9))
 ax.text(16,y+h-17,title,fontsize=14,weight='medium',va='center')
 for i,label in enumerate(chapters):
  ax.text(18+(i%2)*200,y+h-40-(i//2)*21,label,fontsize=12,va='center')
for top,bottom in [(204,188),(116,100)]:
 ax.add_patch(FancyArrowPatch((210,top-1),(210,bottom+1),arrowstyle='-|>',
                             mutation_scale=10,linewidth=1,color=COL['line']))
# Export all three formats without changing the chapter's other validation records.
out=Exporter(HERE);out.save(fig,'figure-1-book-roadmap')
(HERE/'roadmap-layout-validation.json').write_text(json.dumps(out.checks,ensure_ascii=False,indent=2)+'\n')
