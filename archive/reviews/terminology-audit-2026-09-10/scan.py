"""Refresh lexical review aids; human context review determines definition quality."""
from pathlib import Path
import re,json
out=Path(__file__).resolve().parent
R=out.parents[1]/'manuscripts'
reports=[]
for n in range(1,13):
 p=next(R.glob(f'{n:02}-*.md'));seen=set();items=[];section='';fence=False;display=False
 for i,line in enumerate(p.read_text().splitlines(),1):
  if line.startswith('```'):fence=not fence
  if line.strip()=='$$':display=not display;continue
  if fence or display:continue
  if line.startswith('#'):section=line
  if line.startswith('[^'):continue
  line=re.sub(r'\[\^[^]]+\]', '',line)
  clean=re.sub(r'`[^`]*`|\$[^$]*\$|\]\([^)]*\)', '',line)
  for match in re.finditer(r'(?<![A-Za-z0-9_])[A-Za-z][A-Za-z0-9]*(?:[-/][A-Za-z0-9]+)*(?![A-Za-z0-9_])',clean):
   t=match[0]
   if len(t)<2 or t.lower() in seen:continue
   seen.add(t.lower());items.append(dict(term=t,line=i,section=section,context=clean[max(0,match.start()-40):match.end()+150]))
 reports.append(dict(chapter=n,file=str(p.relative_to(R.parent)),items=items))
(out/'first-occurrences.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')

import xml.etree.ElementTree as ET
import sys
sys.path.insert(0,str(R))
from svg_labels import svg_labels
rows=[]
for n in range(1,13):
 p=next(R.glob(f'{n:02}-*.md'));s=p.read_text();known=set(re.findall(r'[A-Za-z][A-Za-z0-9_-]{1,}',s))
 for name in re.findall(r'!\[[^\]]*\]\(([^)]+\.svg)\)',s):
  f=p.parent/name; labels=svg_labels(f);unknown=sorted(set(re.findall(r'\b[A-Za-z][A-Za-z0-9_-]{1,}\b',' '.join(labels)))-known)
  rows.append(dict(chapter=n,file=str(f.relative_to(R.parent)),labels=labels,unmatched_terms=unknown))
(out/'figure-terms.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')

print(f"Indexed {len(reports)} chapters and {len(rows)} figures")
