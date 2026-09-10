"""Book-size vector drawings; geometry is designed at its final reading size."""
from pathlib import Path
import json
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

COL = dict(ink='#252525', line='#454545', blue='#CBE3F3', green='#CFE8DB',
           orange='#F9DEC0', purple='#DDCDE8', gray='#EEEEEE', white='#FFFFFF')
STYLE = {'font.size':12, 'text.color':COL['ink'], 'axes.labelcolor':COL['ink'],
         'axes.edgecolor':COL['line'], 'xtick.color':COL['ink'], 'ytick.color':COL['ink'],
         'axes.labelsize':12, 'axes.titlesize':14, 'xtick.labelsize':11,
         'ytick.labelsize':11, 'legend.fontsize':11, 'svg.fonttype':'none',
         'pdf.fonttype':42, 'figure.facecolor':'white', 'savefig.facecolor':'white'}

def canvas(height=3.6):
    fig, ax = plt.subplots(figsize=(420/72, height))
    fig.subplots_adjust(left=.035,right=.965,bottom=.035,top=.965)
    ax.set(xlim=(0,1),ylim=(0,1)); ax.axis('off')
    return fig, ax

def plot(height=3.6, left=.17, bottom=.20):
    fig, ax = plt.subplots(figsize=(420/72,height))
    fig.subplots_adjust(left=left,right=.95,bottom=bottom,top=.93)
    ax.spines[['top','right']].set_visible(False)
    return fig, ax

def text(ax,x,y,label,size=12,ha='left',**kw):
    return ax.text(x,y,label,fontsize=size,ha=ha,va='center',linespacing=1.4,**kw)

def box(ax,x,y,w,h,label='',color='blue',size=12):
    patch=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.002,rounding_size=0.008',
                        facecolor=COL[color],edgecolor=COL['line'],linewidth=.9)
    ax.add_patch(patch)
    if label: text(ax,x+w/2,y+h/2,label,size,ha='center')
    return patch

def arrow(ax,start,end,kind='data'):
    # Dashed edges denote control; solid edges carry data. Explain locally in captions.
    ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=11,
        linewidth=1,color=COL['line'],linestyle='--' if kind=='control' else '-',shrinkA=3,shrinkB=3))

class Exporter:
    def __init__(self,directory):
        self.directory=Path(directory); self.outputs=[]; self.checks=[]
    def save(self,fig,name):
        fig.canvas.draw(); renderer=fig.canvas.get_renderer(); warnings=[]; sizes=[]
        labels=list(fig.texts)
        for ax in fig.axes:
            labels.extend(ax.texts)
            legend=ax.get_legend()
            if legend is not None: labels.extend(legend.get_texts())
            if ax.axison:
                labels.extend([ax.title,ax.xaxis.label,ax.yaxis.label])
                for axis in [ax.xaxis,ax.yaxis]:
                    lo,hi=sorted(axis.get_view_interval())
                    for tick in axis.get_major_ticks()+axis.get_minor_ticks():
                        if lo<=tick.get_loc()<=hi: labels.extend([tick.label1,tick.label2])
                    labels.append(axis.get_offset_text())
        for t in labels:
            if not t.get_visible() or not t.get_text(): continue
            bb=t.get_window_extent(renderer); sizes.append(t.get_fontsize())
            if bb.x0<0 or bb.y0<0 or bb.x1>fig.bbox.width or bb.y1>fig.bbox.height:
                warnings.append(t.get_text())
        record=dict(figure=name,width_pt=round(fig.get_figwidth()*72,4),
                    min_label_pt=min(sizes),text_extent_warnings=warnings)
        self.checks.append(record)
        if warnings: raise ValueError(f'{name}: labels outside canvas: {warnings}')
        if min(sizes)<11: raise ValueError(f'{name}: label smaller than 11 pt')
        for ext in ['svg','png','pdf']:
            path=self.directory/f'{name}.{ext}'
            fig.savefig(path,dpi=240); self.outputs.append(path)
        plt.close(fig)
    def finish(self):
        (self.directory/'teaching-layout-validation.json').write_text(
            json.dumps(self.checks,ensure_ascii=False,indent=2)+'\n')
        return self.outputs
