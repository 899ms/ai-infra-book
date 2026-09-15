"""Render event-index values directly from original return/call events."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
chains=json.loads((R/'request-chains.json').read_text())
s='# 首完成请求：原始事件索引\n\nPID/seq定位原始JSONL；seq从1开始。本表直接读取原始return字段，不能把缺少的其他字段默认为false。先前表的progress值误写false，保留在REQUEST-EVIDENCE-before-correction.md；原始trace、分析与图未改变。\n\n'
for group in json.loads((R/'summary.json').read_text())['groups']:
 c=next(c for c in chains if c['group']==group['group'] and c['rid']==group['first_completed_rid'])
 s+=f"## {c['group']} / {c['rid']}\n\n| 阶段 | PID / seq | monotonic_ns | 源码行 / 值 |\n|---|---|---:|---|\n"
 for label,key in [('rate return','rate'),('prefetch return','prefetch'),('progress final','progress'),('pop return','pop'),('prefill call','prefill')]:
  e=c[key][-1] if isinstance(c[key],list) else c[key]
  p=R/'results'/c['group']/f"events.{e['pid']}.jsonl";raw=json.loads(p.read_text().splitlines()[e['seq']-1]);assert raw['seq']==e['seq'] and raw['request_id']==c['rid']
  value=raw['return'] if raw['phase']=='return' else raw.get('locals',{})
  s+=f"| {label} | {e['pid']} / {e['seq']} | {raw['monotonic_ns']} | {raw['method']}:{raw['line']} / `{json.dumps(value,ensure_ascii=False)}` |\n"
 s+=f"\nAPI首完成cached_tokens={group['first_cached_tokens']}。\n\n"
(R/'REQUEST-EVIDENCE.md').write_text(s)
