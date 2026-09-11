#!/usr/bin/env python3
"""Rank the chapter-six TP/instance candidates under explicit memory and deadline inputs.

Model shapes come from calculations/configs/models/<model>/config.json, HBM capacity,
bandwidth and matrix rate from calculations/configs/hardware.json.  The interconnect
inputs (NVLink bandwidth, per-round latency, measured cross-server AllReduce time) are
declared in the scenario together with their sources.
"""
import argparse
import json
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def hardware(device_id):
    table=json.loads((ROOT/'calculations/configs/hardware.json').read_text())
    items=table if isinstance(table,list) else table.get('devices',table)
    d=next(x for x in items if x['id']==device_id)
    rate=next(r for r in d['peak_rates'] if r['input_precision'] in ('BF16','FP16') and r['sparsity']=='dense' and r['execution_unit']=='tensor')
    return dict(capacity=int(d['memory']['nominal_capacity']*1e9),hbm=d['memory']['bandwidth_bytes_per_second'],flops=rate['tera_ops_per_second']*1e12)


def model(name):
    c=json.loads((ROOT/f'calculations/configs/models/{name}/config.json').read_text())
    L,h,f=c['num_hidden_layers'],c['hidden_size'],c['intermediate_size']
    qh,kvh,d,v=c['num_attention_heads'],c['num_key_value_heads'],c['head_dim'],c['vocab_size']
    read=L*((2*h*qh*d+2*h*kvh*d)+3*h*f)*2+v*h*2
    norms=(L*(2*h+2*d)+h)*2
    return dict(layers=L,hidden=h,qh=qh,kvh=kvh,d=d,weight_read=read,resident=read+v*h*2+norms,norms=norms,
                kv_token=2*L*kvh*d*2,message=h*2,allreduces=2*L)


def evaluate(config):
    m=model(config['model']);hw=hardware(config['device'])
    choices=[]
    for tp in config['tp_candidates']:
        if config['gpus']%tp or m['qh']%tp:
            continue
        cross=tp>config['gpus_per_host']
        if cross:
            allreduce=config['cross_allreduce_s']
        else:
            alpha,bw=config['local_alpha_s'],config['local_Bps']
            allreduce=0. if tp==1 else 2*(tp-1)*alpha+2*(tp-1)/tp*m['message']/bw
        instances=config['gpus']//tp
        positions=config['history']+config['steps']
        shards=min(tp,m['kvh'])
        per_instance=math.ceil(config['requests']/instances)
        weights=(m['resident']-m['norms'])/tp+m['norms']
        memory=weights+m['kv_token']*positions/shards*per_instance+config['workspace_bytes']
        service=0.
        for i in range(config['steps']):
            kv=m['kv_token']*(config['history']+i+1)
            local=(m['weight_read']/tp+kv/shards)/hw['hbm']
            flops=(m['weight_read']+4*m['qh']*m['d']*(config['history']+i+1)*m['layers'])/tp/hw['flops']
            service+=max(local,flops)+m['allreduces']*allreduce
        ends=[(r//instances+1)*service for r in range(config['requests'])]
        ontime=sum(t<=config['deadline_s'] for t in ends)
        gpu_seconds=config['gpus']*max(ends)
        reasons=[]
        if memory>hw['capacity']:reasons.append('每卡容量不足')
        if ontime<math.ceil(config['requests']*config['required_fraction']):reasons.append('按时完成比例不足')
        choices.append(dict(tp=tp,instances=instances,cross_host=cross,memory_bytes=memory,service_s=service,completion_s=ends,
                            ontime=ontime,gpu_seconds=gpu_seconds,gpu_seconds_per_ontime=gpu_seconds/ontime if ontime else None,rejections=reasons))
    feasible=[x for x in choices if not x['rejections']]
    winner=min(feasible,key=lambda x:x['gpu_seconds_per_ontime'])['tp'] if feasible else None
    return dict(name=config['name'],candidates=choices,winner_tp=winner)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenario',type=Path,default=ROOT/'calculations/scenarios/parallel-choice-example.json')
    parser.add_argument('--output-dir',type=Path,default=ROOT/'calculations/results')
    args=parser.parse_args(); s=json.loads(args.scenario.read_text())
    results=[evaluate(dict(s['common'],**case)) for case in s['cases']]
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'parallel-choice-book.json').write_text(json.dumps(dict(assumptions=s['assumptions'],sources=s['sources'],results=results),ensure_ascii=False,indent=2)+'\n')
    lines=['# 从硬件、模型与期限选择切分','', '运行：`python3 calculations/parallel_choice.py`。修改 [输入](../scenarios/parallel-choice-example.json) 后可用 `--scenario` 重算。','',*s['assumptions'],'','来源：',*[f'- {x}' for x in s['sources']]]
    for result in results:
        lines+=['',f"## {result['name']}",'','| TP | 实例数 | 每卡内存 GB | 单会话 ms | 全部完成 ms | 按时数 | 每个按时会话的 GPU·s | 判断 |','|---|---:|---:|---:|---:|---:|---:|---|']
        for c in result['candidates']:
            cost=f"{c['gpu_seconds_per_ontime']:.3f}" if c['gpu_seconds_per_ontime'] is not None else '—'
            lines.append(f"| {c['tp']} | {c['instances']} | {c['memory_bytes']/1e9:.2f} | {c['service_s']*1e3:.3f} | {max(c['completion_s'])*1e3:.3f} | {c['ontime']} | {cost} | {'；'.join(c['rejections']) or '可行'} |")
        lines+=['',f"选择：TP={result['winner_tp']}。" if result['winner_tp'] else '没有候选满足约束；应扩展候选或修改资源／目标。']
    (args.output_dir/'parallel-choice-book.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))


if __name__=='__main__':main()
