#!/usr/bin/env python3
"""Sync Markdown chapter indexes and the reference index."""
from pathlib import Path
import re,html,json,hashlib
from urllib.parse import quote
R=Path(__file__).resolve().parents[1];O=R/'archive/outlines'
catalog=json.loads((O/'chapters.json').read_text())
assert [c['number'] for c in catalog]==list(range(1,len(catalog)+1))
assert {c['file'] for c in catalog}=={p.name for p in O.glob('[0-9][0-9]-*.md')}
chapters=[]
for entry in catalog:
    p=O/entry['file']
    s=p.read_text();s=re.sub(r'([^\n])\n(#{2,3} )',r'\1\n\n\2',s)
    s=s.replace('扩大型超节点规模','扩大超节点规模').replace('由 实验','由实验').replace('从 实验','从实验')
    p.write_text(s)
    n=int(p.name[:2]);secs=[]
    for m in re.finditer(r'^## (\d+\.\d+) ([^\n]+)\n(.*?)(?=^## |\Z)',s,re.M|re.S):
        body=m[3];subs=[dict(num=x[1],title=x[2],body=x[3].strip()) for x in re.finditer(r'^### (\d+\.\d+\.\d+) ([^\n]+)\n(.*?)(?=^### |\Z)',body,re.M|re.S)]
        secs.append(dict(num=m[1],title=m[2],intro=body.split('### ',1)[0].strip(),subs=subs))
    chapters.append(dict(n=n,path=p,title=s.splitlines()[0].split('章 ',1)[1],lead=s.split('\n\n',2)[2].split('\n## ',1)[0],sections=secs,subcount=sum(len(x['subs']) for x in secs),labs=len(re.findall(r'^> \*\*实验 ',s,re.M)),figs=len(re.findall(r'^> \*\*图 ',s,re.M))))
    assert chapters[-1]['title']==entry['title'] and n==entry['number']
    chapters[-1]['decision']=s.split('## 本章的设计决定\n',1)[1].split('\n## ',1)[0].strip()
    core=re.findall(r'^> \*\*实验 (\d+-\d+)[^\n]*〔核心〕',s,re.M)
    if not core:
        prose_core=re.search(r'核心实验仍为 ([^。]+)',s)
        if prose_core:
            core=re.findall(r'\d+-\d+',prose_core[1])
    assert core==entry['core_experiments'] and len(core)==3,(p,core)
counts=dict(sections=sum(len(c['sections']) for c in chapters),subsections=sum(c['subcount'] for c in chapters),experiments=sum(c['labs'] for c in chapters),figures=sum(c['figs'] for c in chapters))
summary=f'十二章共 {counts["sections"]} 节、{counts["subsections"]} 个小节、{counts["experiments"]} 项实验与计算、{counts["figures"]} 项配图计划'
for p in [O/'README.md']:
    s=p.read_text();prefix='outlines/' if p==R/'README.md' else ''
    entries='\n'.join(f'{c["number"]}. [{c["title"]}]({prefix}{quote(c["file"])}): {c["summary"]}' for c in catalog)
    s=re.sub(r'<!-- CHAPTERS:START -->.*?<!-- CHAPTERS:END -->','<!-- CHAPTERS:START -->\n'+entries+'\n<!-- CHAPTERS:END -->',s,flags=re.S)
    s=re.sub(r'十[二三]章共 \d+ 节、\d+ 个小节、\d+ 项实验与计算、\d+ 项配图计划',summary,s)
    p.write_text(s)

# Keep all source rows, updating primary chapter use and appending the new fixed configuration.
p=O/'source-map.md';s=p.read_text();meta=json.loads((R/'references/outline-checks/2026-09-07/scaling-history/sources.json').read_text())+json.loads((R/'references/outline-checks/2026-09-07/systems-cases/sources.json').read_text())+json.loads((R/'references/outline-checks/2026-09-07/edge-media/sources.json').read_text())+json.loads((R/'references/outline-checks/2026-09-07/model-accounting/sources.json').read_text())+json.loads((R/'references/outline-checks/2026-09-07/platform-routing/sources.json').read_text())+json.loads((R/'references/outline-checks/2026-09-07/execution-feedback/sources.json').read_text())+json.loads((R/'references/outline-checks/2026-09-07/framework-evolution/sources.json').read_text())
meta += json.loads((R/'references/proceedings/selected-sources.json').read_text()) + json.loads((R/'references/framework-history/2026-09-07/lora/sources.json').read_text())
meta += json.loads((R/'references/framework-history/2026-09-07/flashinfer/sources.json').read_text())
meta += json.loads((R/'references/framework-history/2026-09-07/startup/sources.json').read_text())
meta += json.loads((R/'references/framework-history/2026-09-08/attention/sources.json').read_text())
meta += json.loads((R/'references/framework-history/2026-09-08/chunk-scheduling/sources.json').read_text())
meta += json.loads((R/'references/framework-history/2026-09-08/overlap-placement/sources.json').read_text())
meta += json.loads((R/'references/framework-history/2026-09-08/rl-consistency/sources.json').read_text())
meta += json.loads((R/'references/framework-history/2026-09-08/collective-paths/sources.json').read_text())
meta += json.loads((R/'references/framework-history/2026-09-08/checkpoint-loading/sources.json').read_text())
meta += json.loads((R/'references/framework-history/2026-09-08/communication-tuning/sources.json').read_text())
meta += json.loads((R/'references/framework-history/2026-09-08/workload-generation/sources.json').read_text())
meta += json.loads((R/'references/framework-history/2026-09-08/speculative-execution/sources.json').read_text())
meta += json.loads((R/'references/framework-history/2026-09-08/rollout-tail/sources.json').read_text())
meta += json.loads((R/'references/framework-history/2026-09-08/offload-execution/sources.json').read_text())
meta += json.loads((R/'references/framework-history/2026-09-08/multimodal-execution/sources.json').read_text())
meta += json.loads((R/'references/interviews/2026-09-08/fourth-pass/sources.json').read_text())
meta += [x for x in json.loads((R/'references/interviews/2026-09-08/fifth-pass/sources.json').read_text()) if x['evidence_type'] == 'official_documentation']
meta += json.loads((R/'references/framework-history/2026-09-08/pcie-staging/sources.json').read_text())
meta += json.loads((R/'references/framework-history/2026-09-08/kernel-orchestration/sources.json').read_text())
meta += json.loads((R/'references/framework-history/2026-09-08/cache-routing/sources.json').read_text())
meta += json.loads((R/'references/framework-history/2026-09-08/structured-generation/sources.json').read_text())
meta += [x for x in json.loads((R/'references/framework-history/2026-09-08/ep-reconfiguration/sources.json').read_text()) if '-pr' not in x['id']]
meta += [x for x in json.loads((R/'references/framework-history/2026-09-08/cache-events/sources.json').read_text()) if x['id'] in ['vllm-current-kv-publisher','dynamo-native-offload-fixed','dynamo-event-recovery-fixed','dynamo-sglang-hicache','dynamo-router-design','dynamo-config-tuning','dynamo-local-indexer','dynamo-recovery-state']]
meta += [x for x in json.loads((R/'references/framework-history/2026-09-08/weight-handoff/sources.json').read_text()) if x['id'] in ['vllm-sleep-current','vllm-transfer-current','vllm-transfer-rdt','vllm-worker-current','vllm-sleep-2025','vllm-rdt-2026','sglang-rl-guide-fixed','verl-v1-async-fixed','verl-vllm-server','verl-sglang-server','sglang-memory-2025','vllm-native-rl-2026-fixed-url']]
meta += json.loads((R/'references/proceedings/ASPLOS/2024/selected-sources.json').read_text())
meta += [x for x in json.loads((R/'references/proceedings/ISCA/2024/selected-sources.json').read_text()) if x['id'] in ['isca24-public-011-author', 'isca24-public-014']]
meta += [x for x in json.loads((R/'references/proceedings/ASPLOS/2025/selected-sources.json').read_text()) if x['id'] in ['asplos25-public-pdf-94','asplos25-iks-pdf','asplos25-faiss-faiss-indexes','asplos25-faiss-guidelines-to-choose-an-index']]
meta += json.loads((R/'references/outline-checks/2026-09-08/system-abstraction/sources.json').read_text())
meta += [x for x in json.loads((R/'references/framework-history/2026-09-08/kv-quantization/sources.json').read_text()) if x['reading_status'] == 'selected_text_read']
meta += [x for x in json.loads((R/'references/framework-history/2026-09-08/hybrid-state/sources.json').read_text()) if x['reading_status'] == 'selected_text_read']
meta += [x for x in json.loads((R/'references/proceedings/ISCA/2025/selected-sources.json').read_text()) if x['id'] in ['isca25-paper-033', 'isca25-paper-055']]
meta += [x for x in json.loads((R/'references/proceedings/MICRO/2024/sources.json').read_text()) if x['id'] == 'micro24-paper-011']
for x in meta:
    if f'| `{x["id"]}` |' not in s:
        note='失败／空响应；不作正文证据' if x.get('reading_status','').startswith('failed') else '已归档；固定快照'
        s+=f'| `{x["id"]}` | [{x["title"]}](../{x["file"]}) | 补充 | 补充／版本参照 | {note} |\n'
lines=[]
for line in s.splitlines():
    if line.startswith('| `'):
        cells=[x.strip() for x in line.split('|')[1:-1]];links=re.findall(r'\]\((\.\./[^)]+)\)',cells[1]);cited=[str(c['n']) for c in chapters if any(u in c['path'].read_text() for u in links)]
        if cited:
            body=[str(c['n']) for c in chapters if any(u in c['path'].read_text().split('## 写作资料',1)[0] for u in links)]
            cells[3]=('正文 '+','.join(body)+'；' if body else '')+'章末 '+','.join(cited)
        else:
            extended=[str(c['n']) for c in chapters if any(u.replace('../','../../',1) in (O/'extensions'/c['path'].name).read_text() for u in links)]
            cells[3]='扩写 '+','.join(extended) if extended else '补充／版本参照'
        line='| '+' | '.join(cells)+' |'
    lines.append(line)
p.write_text('\n'.join(lines)+'\n')
for x in meta:assert hashlib.sha256((R/x['file']).read_bytes()).hexdigest()==x['sha256']
print(summary)
