#!/usr/bin/env python3
"""Recompute chapter-2 comparisons and V4.1 source ledgers without a GPU."""
from pathlib import Path
import hashlib
import json
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'src'))
from infra_calc.topics import chapter2_models,v41_forward
from infra_calc.report import markdown

ROOT=Path(__file__).resolve().parent
scenarios=json.loads((ROOT/'scenarios/book.json').read_text())['v41_forward']
outputs=[]
for scenario in scenarios:
    r=v41_forward.calculate(**scenario['inputs'])
    for suffix,content in [('json',json.dumps(r,ensure_ascii=False,indent=2)+'\n'),('md',markdown(r))]:
        p=ROOT/'results'/f"{scenario['id']}.{suffix}";p.write_text(content);outputs.append(p)
r=chapter2_models.calculate()
p=ROOT/'results/chapter2-model-comparison.json';p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');outputs.append(p)
manifest={'command':'python3 calculations/reproduce_ch02.py','artifacts':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in outputs]}
(ROOT/'results/chapter2-reproduction.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Recomputed',len(outputs),'chapter-2 artifacts from architecture adapters.')
