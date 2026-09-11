"""Check changed chapter structure, source snapshots and reproducible teaching results."""
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
BASE=Path(__file__).resolve().parent
checks=[]
def check(condition,label):
    if not condition:raise AssertionError(label)
    checks.append(label)
for ch in (1,4,5,6,7,9,10):
    p=next((ROOT/'manuscripts').glob(f'{ch:02}-*.md'));s=p.read_text()
    check(s.rfind('## 本章小结')>s.rfind('\n[^'),'summary follows source notes '+str(ch))
    captions=re.findall(r'^\*图 '+str(ch)+r'-(\d+)[：\s]',s,re.M)
    check(captions==list(map(str,range(1,len(captions)+1))),'figure sequence '+str(ch))
    refs=re.findall(r'!\[[^\n]*\]\(([^)]+)\)',s)
    check(len(captions)==len(refs),'all figures captioned '+str(ch))
    check(all((p.parent/ref).exists() for ref in refs),'assets exist '+str(ch))
    check(len(re.findall(r'^\$\$$',s,re.M))%2==0,'display math delimiters '+str(ch))
    check(not re.search(r'图 [679]-[A-Z]|\\n\\n',s),'no temporary labels '+str(ch))
    used=set(re.findall(r'\[\^([^\]]+)\](?!:)',s));defined=set(re.findall(r'^\[\^([^\]]+)\]:',s,re.M))
    check(used<=defined,'notes resolve '+str(ch))
requirements={
    1:['矩阵在一张卡内可以分块执行','每块由谁计算'],
    4:['为后续的切分与调度','共享出口'],
    5:['分块还可以越过一张卡的边界','合并计入 96 KiB','选择步骤','沿哪个维度切分','三种切分方向'],
    6:['上下文并行','序列并行','六种并行方式','事务层','Load／Store','busbw','给定模型与硬件','当前四个候选均不可行'],
    7:['固定 1024 卡','256','200 GB/s','检查点','枚举张量并行 8、16、32、64'],
    9:['Expert Disaggregation','两次通信阶段','CRAFT','1.90 倍','skew','V2']}
for ch,terms in requirements.items():
    s=next((ROOT/'manuscripts').glob(f'{ch:02}-*.md')).read_text()
    for term in terms:check(term in s,'required topic '+str(ch)+' '+term)
for row in json.loads((BASE/'sources.json').read_text()):
    p=ROOT/row['file'];check(hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],'source hash '+row['name'])
for ch in (6,7,9):
    for path in [ROOT/f'manuscripts/ch{ch:02}/ub-ep-layout-validation.json',ROOT/'manuscripts/ch06/parallel-layout-validation.json',ROOT/'manuscripts/ch05/structure-layout-validation.json']:
      if not path.exists():continue
      for row in json.loads(path.read_text()):
        check(row['width_pt']==420 and row['min_label_pt']>=11 and not row['text_extent_warnings'],'layout '+row['figure'])
        for ext in ('svg','png','pdf'):check((path.parent/(row['figure']+'.'+ext)).exists(),'format '+row['figure']+'.'+ext)
with tempfile.TemporaryDirectory() as td:
    for script,result in [('ep_skew','ep-skew-book'),('parallel_choice','parallel-choice-book'),('supernode_scaling','supernode-scaling-book')]:
        subprocess.run(['python3',str(ROOT/f'calculations/{script}.py'),'--output-dir',td],check=True,stdout=subprocess.DEVNULL)
        for ext in ('json','md'):
            check((Path(td)/(result+'.'+ext)).read_bytes()==(ROOT/f'calculations/results/{result}.{ext}').read_bytes(),'reproducible '+result+'.'+ext)
for pattern in ('test_ep_skew.py','test_parallel_choice.py'):
    subprocess.run(['python3','-m','unittest','discover','-s',str(ROOT/'calculations/tests'),'-p',pattern],check=True)
(BASE/'validation.json').write_text(json.dumps(dict(passed=True,checks=checks),ensure_ascii=False,indent=2)+'\n')
print(f'PASS: {len(checks)} content, source, layout and reproducibility checks; 12 numerical tests')
