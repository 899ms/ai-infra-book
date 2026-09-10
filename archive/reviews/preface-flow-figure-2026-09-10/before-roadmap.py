#!/usr/bin/env python3
"""Render the twelve-chapter reading roadmap with the book's pinned typography."""
from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from figure_style.typography import configure_font
_, family = configure_font()
plt.rcParams.update({'font.family': family, 'svg.fonttype': 'path',
                     'svg.hashsalt': 'ai-infra-book-roadmap', 'font.size': 12})
fig, ax = plt.subplots(figsize=(10, 6.8))
fig.subplots_adjust(left=.015, right=.985, top=.985, bottom=.015)
ax.set(xlim=(0, 1), ylim=(0, 1)); ax.axis('off')
ink = '#193441'
rows = [
    (.70, '#E7F3EF', '第一部分 · 模型与负载', '需要完成什么工作？',
     ['1  初识 AI Infra', '2  模型架构', '3  推理与训练负载'], '计算、数据与任务要求'),
    (.38, '#F0F6F8', '第二部分 · 芯片与系统', '资源怎样承担这些工作？',
     ['4  加速器架构', '5  算子与运行时', '6  超节点', '7  数据中心网络'], '执行能力与协作代价'),
    (.02, '#FCF2E7', '第三部分 · 推理与训练系统', '怎样组织服务并完成任务？',
     ['8  推理优化', '9  分布式推理', '10  训练系统',
      '11  资源调度与运行环境', '12  端边云协同'], None),
]
for y, color, title, question, chapters, transition in rows:
    height = .29 if y == .02 else .25
    ax.add_patch(FancyBboxPatch((.02,y),.96,height,boxstyle='round,pad=0.008,rounding_size=.012',
                               linewidth=1,edgecolor='#CBD8DF',facecolor=color))
    ax.text(.045,y+height-.05,title,fontsize=15,weight='bold',color=ink,va='center')
    ax.text(.045,y+height-.095,question,fontsize=11,color='#55707D',va='center')
    for i, chapter in enumerate(chapters):
        col, row = i % 2, i // 2
        ax.text(.055+col*.48,y+height-.15-row*.051,chapter,fontsize=12,color=ink,va='center')
    if transition:
        ax.add_patch(FancyArrowPatch((.50,y-.01),(.50,y-.062),arrowstyle='-|>',
                                    mutation_scale=14,linewidth=1.4,color='#138B83'))
        ax.text(.53,y-.037,transition,fontsize=10,color='#55707D',va='center')
for ext in ('svg','png'):
    fig.savefig(HERE/f'figure-1-book-roadmap.{ext}',dpi=180,facecolor='white')
plt.close(fig)
