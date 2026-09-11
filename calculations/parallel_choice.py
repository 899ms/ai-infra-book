#!/usr/bin/env python3
"""Rank the chapter-six TP/replica candidates under explicit memory and SLO inputs."""
import argparse
import json
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def evaluate(config):
    h=4096; kv=1024; layers=36
    # Same per-layer weight, KV and output-head accounting as ch06/continuity_model.py.
    layer_bytes=(3*h*12288+(2*h*4096+2*h*kv))*2
    choices=[]
    for tp in config['tp_candidates']:
        if config['gpus']%tp or 32%tp or 8%tp:
            continue
        cross=tp>config['gpus_per_host']
        alpha=config['cross_alpha_s'] if cross else config['local_alpha_s']
        bw=config['cross_Bps'] if cross else config['local_Bps']
        instances=config['gpus']//tp
        max_history=config['history']+config['steps']
        # Norm weights remain replicated. Fixed full weight count follows chapter-six source.
        norm_bytes=(2*layers+1)*h*2
        memory=(16381470720-norm_bytes)/tp+norm_bytes+2*layers*kv*2*max_history/tp+config['workspace_bytes']
        service=0.
        for i in range(config['steps']):
            payload=layers*layer_bytes+2*layers*kv*2*(config['history']+i+1)+151936*h*2
            local=payload/config['hbm_Bps']/tp
            ring=2*(tp-1)*alpha+2*(tp-1)/tp*8192/bw
            service+=local+72*ring+config['serial_s']
        ends=[(r//instances+1)*service for r in range(config['requests'])]
        ontime=sum(t<=config['deadline_s'] for t in ends)
        cost=config['gpus']*max(ends)*config['cost_per_gpu_second']
        reasons=[]
        if memory>config['memory_bytes']:reasons.append('每卡容量不足')
        if ontime<math.ceil(config['requests']*config['required_fraction']):reasons.append('按时完成比例不足')
        choices.append(dict(tp=tp,instances=instances,cross_host=cross,memory_bytes=memory,service_s=service,completion_s=ends,ontime=ontime,cost=cost,cost_per_ontime=cost/ontime if ontime else None,rejections=reasons))
    feasible=[x for x in choices if not x['rejections']]
    winner=min(feasible,key=lambda x:x['cost_per_ontime'])['tp'] if feasible else None
    return dict(name=config['name'],candidates=choices,winner_tp=winner)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario',type=Path,default=ROOT/'calculations/scenarios/parallel-choice-example.json')
    parser.add_argument('--output-dir',type=Path,default=ROOT/'calculations/results')
    args=parser.parse_args(); s=json.loads(args.scenario.read_text())
    results=[evaluate(dict(s['common'],**case)) for case in s['cases']]
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'parallel-choice-book.json').write_text(json.dumps(dict(assumptions=s['assumptions'],results=results),ensure_ascii=False,indent=2)+'\n')
    lines=['# 从硬件、模型与期限选择切分','', '运行：`python3 calculations/parallel_choice.py`。修改 [输入](../scenarios/parallel-choice-example.json) 后可用 `--scenario` 重算。','',*s['assumptions']]
    for result in results:
        lines+=['',f"## {result['name']}",'','| TP | 实例数 | 单会话 ms | 全部完成 ms | 按时数 | 每个按时会话成本 | 判断 |','|---|---:|---:|---:|---:|---:|---|']
        for c in result['candidates']:
            cost=f"{c['cost_per_ontime']:.3f}" if c['cost_per_ontime'] is not None else '—'
            lines.append(f"| {c['tp']} | {c['instances']} | {c['service_s']*1e3:.3f} | {max(c['completion_s'])*1e3:.3f} | {c['ontime']} | {cost} | {'；'.join(c['rejections']) or '可行'} |")
        lines+=['',f"选择：TP={result['winner_tp']}。" if result['winner_tp'] else '没有候选满足约束；应扩展候选或修改资源／目标。']
    (args.output_dir/'parallel-choice-book.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__=='__main__':main()
