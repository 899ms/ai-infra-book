#!/usr/bin/env python3
"""Render long-context/request tables from the calculations package results."""
from pathlib import Path
import hashlib,json,re
H=Path(__file__).resolve().parent;R=H.parents[1]
p=R/'calculations/results/chapter2-model-comparison.json';d=json.loads(p.read_text())
(H/'long-context-comparison.json').write_text(json.dumps({'models':d['long_context'],'scope':d['scope'],'qwen3_200k_scope':d['long_context_scope'],'source_file':str(p.relative_to(R)),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},ensure_ascii=False,indent=2)+'\n')
name=lambda x: x['model'].replace('V4.1 Flash','DeepSeek V4.1 Flash').replace('V4-Flash','DeepSeek V4-Flash')
table=["| Model | 8K Context Interaction (GFLOPs) | 1M Context Interaction (GFLOPs) | 8K State (GiB) | 1M State (GiB) |",'| --- | ---: | ---: | ---: | ---: |']
for x,y in zip(d['long_context'][:5],d['long_context'][10:15]):
 assert x['model_id']==y['model_id']
 table.append(f"| {name(x)} | {x['history_interaction_flops']/1e9:.2f} | {y['history_interaction_flops']/1e9:.2f} | {x['state_bytes']/2**30:.3f} | {y['state_bytes']/2**30:.3f} |")
request=["| Model | Full Request FLOPs (TFLOPs) | Implementation Used |",'| --- | ---: | --- |']
paths=["CED + tail-window replay, index within candidate set","effective causal attention","rectangular full attention with chunked linear branch","effective main attention with reference index","compact MLA with chunked KDA; decode uses recurrent KDA"]
for x,path in zip(d['requests'],paths):request.append(f"| {name(x)} | {x['matrix_flops']/1e12:.2f} | {path} |")
md=H.parent/'02-模型架构.md';s=md.read_text()
for marker,t in [("**Table 2-E",table),('### 2.6.3',request)]:
 start=s.index(marker);m=re.search(r'^\|.*(?:\n\|.*)*',s[start:],re.M);a=start+m.start();b=start+m.end();s=s[:a]+'\n'.join(t)+s[b:]
md.write_text(s)
print('Rendered five-model long-context and complete-request tables.')
