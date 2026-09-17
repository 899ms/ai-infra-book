"""Book-size vector drawings; geometry is designed at its final reading size."""
from pathlib import Path
import json
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

COL = dict(ink='#252525', line='#454545', blue='#CBE3F3', green='#CFE8DB',
           orange='#F9DEC0', purple='#DDCDE8', gray='#EEEEEE', white='#FFFFFF')
STYLE = {'font.size':12, 'font.weight':'normal', 'axes.titleweight':'medium', 'text.color':COL['ink'], 'axes.labelcolor':COL['ink'],
         'axes.edgecolor':COL['line'], 'xtick.color':COL['ink'], 'ytick.color':COL['ink'],
         'axes.labelsize':12, 'axes.titlesize':14, 'xtick.labelsize':11,
         'ytick.labelsize':11, 'legend.fontsize':11, 'svg.fonttype':'path',
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

MIN_PT=7.0          # floor for ordinary labels
MIN_PT_DENSE=6.0    # dense insets tolerate smaller type

def box(ax,x,y,w,h,label='',color='blue',size=12):
    patch=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.002,rounding_size=0.008',
                        facecolor=COL[color],edgecolor=COL['line'],linewidth=.9)
    ax.add_patch(patch)
    if label:
        t=text(ax,x+w/2,y+h/2,label,size,ha='center')
        # Pair each label with its box so fit_overflow can measure one against
        # the other. A translated label is much longer than the Chinese it
        # replaces and can overrun its box while still sitting inside the
        # figure, where a canvas-bounds check cannot see it.
        if not hasattr(ax,'_boxed_labels'): ax._boxed_labels=[]
        ax._boxed_labels.append((patch,t))
    return patch


def _visible_ticklabels(ax,axis):
    """Only ticks inside the view interval; the bounds check ignores the rest,
    and off-view ticks sit far outside the canvas by construction."""
    lo,hi=sorted(axis.get_view_interval())
    out=[]
    for tick in axis.get_major_ticks()+axis.get_minor_ticks():
        if lo<=tick.get_loc()<=hi:
            out.extend([l for l in (tick.label1,tick.label2) if l is not None])
    return lambda: out


def _visible_xticklabels(ax): return _visible_ticklabels(ax,ax.xaxis)
def _visible_yticklabels(ax): return _visible_ticklabels(ax,ax.yaxis)


def fit_overflow(fig,renderer,pad_frac=0.94):
    """Shrink over-wide labels until they fit their box or the canvas.

    Deliberately conservative, following the approach used in the English
    edition of the companion AI Agent book: only the font size of a run that
    actually overflows is changed. Positions are never moved, text is never
    rewrapped, and boxes are never resized, so the author's layout survives
    translation. The pass is idempotent -- running it again changes nothing.
    """
    W,H=fig.bbox.width,fig.bbox.height
    stubborn=[]

    def shrink(t,fits,floor):
        while not fits() and t.get_fontsize()>floor:
            t.set_fontsize(round(t.get_fontsize()-0.5,1))
        return fits()

    # 1. labels that belong to a box are measured against that box
    boxed=set()
    for ax in fig.axes:
        for patch,t in getattr(ax,'_boxed_labels',[]):
            boxed.add(id(t))
            def fits(patch=patch,t=t,ax=ax):
                x0,y0=ax.transData.transform((0,0))
                x1,y1=ax.transData.transform((patch.get_width(),patch.get_height()))
                bb=t.get_window_extent(renderer)
                return bb.width<=abs(x1-x0)*pad_frac and bb.height<=abs(y1-y0)*pad_frac
            if not fits() and not shrink(t,fits,MIN_PT):
                stubborn.append(t.get_text())

    # 2. tick labels are shrunk through tick_params: matplotlib rebuilds tick
    #    artists on every draw, so a size set on an individual label is lost.
    for ax in fig.axes:
        if not ax.axison: continue
        for which,getter in (('x',_visible_xticklabels(ax)),('y',_visible_yticklabels(ax))):
            for _ in range(14):
                bad=[l for l in getter() if l.get_visible() and l.get_text()
                     and not (l.get_window_extent(renderer).x0>=1
                              and l.get_window_extent(renderer).y0>=1
                              and l.get_window_extent(renderer).x1<=W-1
                              and l.get_window_extent(renderer).y1<=H-1)]
                if not bad: break
                cur=min(l.get_fontsize() for l in bad)
                if cur<=MIN_PT_DENSE:
                    stubborn.extend(l.get_text() for l in bad); break
                ax.tick_params(axis=which,labelsize=round(cur-0.5,1))
                fig.canvas.draw(); renderer=fig.canvas.get_renderer()

    # 3. every other label is measured against the canvas
    others=list(fig.texts)
    for ax in fig.axes:
        others.extend(ax.texts)
        lg=ax.get_legend()
        if lg is not None: others.extend(lg.get_texts())
        if ax.axison:
            others.extend([ax.title,ax.xaxis.label,ax.yaxis.label])
    for t in others:
        if t is None or id(t) in boxed: continue
        if not t.get_visible() or not t.get_text(): continue
        def fits(t=t):
            bb=t.get_window_extent(renderer)
            return bb.x0>=1 and bb.y0>=1 and bb.x1<=W-1 and bb.y1<=H-1
        if not fits() and not shrink(t,fits,MIN_PT_DENSE):
            stubborn.append(t.get_text())
    return stubborn

def arrow(ax,start,end,kind='data'):
    # Dashed edges denote control; solid edges carry data. Explain locally in captions.
    ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=11,
        linewidth=1,color=COL['line'],linestyle='--' if kind=='control' else '-',shrinkA=3,shrinkB=3))

class Exporter:
    def __init__(self,directory):
        self.directory=Path(directory); self.outputs=[]; self.checks=[]
    def save(self,fig,name):
        fig.canvas.draw(); renderer=fig.canvas.get_renderer()
        stubborn=fit_overflow(fig,renderer)
        if stubborn: print(f'FIT {name}: still tight: {stubborn}',flush=True)
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
        if warnings: print(f'EXPANDED {name}: canvas grown to fit {warnings}',flush=True)
        if min(sizes)<MIN_PT_DENSE: raise ValueError(f'{name}: label smaller than {MIN_PT_DENSE} pt')
        for ext in ['svg','png','pdf']:
            path=self.directory/f'{name}.{ext}'
            # Grow the saved canvas to encompass every label rather than
            # clipping it or trimming the author's wording. The book places
            # figures at a fixed fraction of the text width with the aspect
            # ratio preserved, so a slightly wider canvas simply renders a
            # little smaller instead of losing text at the edge.
            fig.savefig(path,dpi=240,bbox_inches='tight',pad_inches=0.02)
            self.outputs.append(path)
        plt.close(fig)
    def finish(self):
        (self.directory/'teaching-layout-validation.json').write_text(
            json.dumps(self.checks,ensure_ascii=False,indent=2)+'\n')
        return self.outputs
