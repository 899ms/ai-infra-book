import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=Path(__file__).absolute().parent;s=json.loads((r/'analysis.json').read_text());fig,ax=plt.subplots(figsize=(7,4),layout='constrained')
values=[100*s[m]['cached_tokens']/s[m]['prompt_tokens'] for m in ['off','on','grouped']]
b=ax.bar(['Round robin\nAPC off','Round robin\nAPC on','Client grouped\nAPC on'],values,color=['#909aa6','#4d83b7','#cf843b']);ax.bar_label(b,fmt='%.2f%%',padding=3);ax.set_ylim(0,80);ax.set_ylabel('Reported cached tokens / all prompt tokens (%)');ax.set_title('Same 12 prompts and outputs, different request order');ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
for ext in ['png','svg','pdf']:fig.savefig(r/('cache-order.'+ext),dpi=160)
