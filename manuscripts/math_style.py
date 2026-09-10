"""Consistent inline mathematics in chapters 1–3 and generated comparison prose.

Protect existing mathematics, links, code, and reference labels before normalizing
mathematical variable mentions. Product names and units remain prose.
"""
import re
PROTECTED=re.compile(r'```[\s\S]*?```|\$\$[\s\S]*?\$\$|\$[^$\n]+\$|`[^`\n]*`|\]\([^\n)]*\)|\[\^[^\]]+\]')
def normalize(text,chapter):
 text=text.replace('\x07pprox',r'\approx')
 # These are matrix products; QK Norm is the name of a normalization operation.
 text=text.replace('QK／PV',r'$QK^{\mathsf T}$ 与 $AV$').replace('QK／AV',r'$QK^{\mathsf T}$ 与 $AV$').replace('QK 与 AV',r'$QK^{\mathsf T}$ 与 $AV$')
 text=text.replace('QK 点积',r'$QK^{\mathsf T}$ 点积').replace('AV 的贡献',r'$AV$ 的贡献')
 if chapter==3:
  text=text.replace('$B=1,\\ T=8192$','$B=1,\\ P=8192$')
  text=text.replace('E→P→D',r'$\mathrm E\to\mathrm P\to\mathrm D$').replace('E/P/D',r'$\mathrm E/\mathrm P/\mathrm D$')
  text=text.replace('N/D 范围','$N$、$D$ 范围')
  for old,new in [('用 E 表示','用 $\\mathrm E$ 表示'),('P 表示语言',' $\\mathrm P$ 表示语言'),('D 表示后续',' $\\mathrm D$ 表示后续'),('影响 E','影响 $\\mathrm E$'),('阶段图中的 D','阶段图中的 $\\mathrm D$')]:text=text.replace(old,new)
 if chapter==2:
  # Leave magnitude suffixes and panel labels as upright prose.
  symbols=r'Q|K|V|X|Y|W|O|M|S|P|G|d|f|m|i|j|l|t|e|c|z|a|b'
  def prose(s):
   s=re.sub(r'(?<![A-Za-z0-9_/-])('+symbols+r')(?![A-Za-z0-9_/-])',lambda m:'$'+m[1]+'$',s)
   s=s.replace('处理 B 条','处理 $B$ 条').replace('S+i',r'$S+i$')
   return s
  parts=[];pos=0
  for match in PROTECTED.finditer(text):
   parts.extend([prose(text[pos:match.start()]),match[0]]);pos=match.end()
  parts.append(prose(text[pos:]));text=''.join(parts)
  # A numeral and variable form one expression rather than two adjacent fragments.
  text=text.replace('S+$i$','$S+i$').replace('$S$+$i$','$S+i$')
 return text


def normalize_figure(fig):
 """Render mathematical label content using Matplotlib's LaTeX mathtext."""
 from matplotlib.text import Text
 exact={
  '70 GB ÷ 3350 GB/s ≈ 20.90 ms':r'$70\,\mathrm{GB}/(3350\,\mathrm{GB/s})\approx20.90\,\mathrm{ms}$',
  '400 × 144 KiB = 56.25 MiB':r'$400\times144\,\mathrm{KiB}=56.25\,\mathrm{MiB}$',
  '100 / 50 = 2':r'$100/50=2$', '200 / 80 = 2.5':r'$200/80=2.5$',
  '64 个 token × 每个选 8 个专家':'64 个 token，每个选 8 个专家',
  'QKV → 历史访问 → Wo':r'$Q,K,V$ → 历史访问 → $W_o$',
  '32 候选 → 16 接受':'生成 32 条 → 保留 16 条',
  '已计状态访问':'历史读取与递推矩阵读写',
  '同一文本的检索实验':'同一文本的检索任务',
  'Qwen 与 V4 Flash 各 8/8\n输入 token 数、部署与精度不同\nPro／K3 未测':'Qwen 与 V4 Flash 均答对八题\n同一文本 → 各自的 token 序列\n按实际长度计算资源',
  '打断投影〔教学〕':'打断与静音',
  '123 ms 发出 → 130 ms 静音\n未模拟后端取消':'123 ms 发出 → 130 ms 静音\n控制传递与设备生效共同决定',
  '历史接收〔真实记录〕':'两次语音交互测量',
  '首块 399.919 / 370.459 ms\n首播、静音、取消未知':'首块约 400 ms／370 ms\n到达后继续解码、缓冲与播放',
  '状态合计 147.433 GB；激活和工作区另计。矩阵表未计非矩阵反向、优化器算术、重计算与通信。':'参数相关状态合计 147.433 GB；激活从前向产生，在对应反向结束后释放。',
 }
 def plain(t):
  t=re.sub(r'(?<![A-Za-z0-9])([BHPST])\s*=\s*(\d+)',lambda m:'$'+('P' if m[1]=='T' else m[1])+'='+m[2]+'$',t)
  t=re.sub(r'\b(\d+)\s*×\s*(\d+)\b',lambda m:'$'+m[1]+r'\times'+m[2]+'$',t)
  t=re.sub(r'\b(\d+) GiB × (\d+) s',lambda m:'$'+m[1]+r'\,\mathrm{GiB}\times'+m[2]+r'\,\mathrm{s}$',t)
  t=re.sub(r'(?<![A-Za-z0-9_])([QKV])(?![A-Za-z0-9_])',lambda m:'$'+m[1]+'$',t)
  t=t.replace('E/P/D',r'$\mathrm{E}/\mathrm{P}/\mathrm{D}$').replace('E→P→D',r'$\mathrm{E}\to\mathrm{P}\to\mathrm{D}$')
  t=t.replace(' × ',r' $\times$ ')
  return t
 for artist in fig.findobj(Text):
  t=artist.get_text()
  for old,new in exact.items():t=t.replace(old,new)
  parts=re.split(r'(\$[^$]*\$)',t)
  t=''.join(x if i%2 else plain(x) for i,x in enumerate(parts))
  artist.set_text(t)
