#!/usr/bin/env python3
"""Fixed-work 1024-GPU training: TP/DP placement, hierarchical traffic and recovery."""
import argparse
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def evaluate(c,size,profile):
    total,tp=c['gpus'],c['tp']
    if total%size or size%tp:
        raise ValueError('supernode must contain whole TP groups and divide cluster')
    dp=total//tp; q=size//tp; hosts=total//size
    local_bw=c['local_Bps']*profile.get('local_multiplier',1)
    export_bw=min(size*c['nic_Bps'],profile.get('egress_cap_Bps',float('inf')))
    gradient=c['parameters']*c['gradient_bytes']/tp
    local_rs_ag=2*(q-1)*c['local_alpha_s']+2*(q-1)/q*gradient/local_bw
    per_rank=2*(hosts-1)/hosts*gradient/q
    exported=per_rank*size
    network=2*(hosts-1)*c['remote_alpha_s']+max(per_rank/c['nic_Bps'],exported/export_bw)
    hierarchical=local_rs_ag+network
    # Contiguous DP ring: q DP members on each supernode, TP coordinates in separate rings.
    # One boundary sender per TP coordinate, without striping that edge across idle NICs.
    flat_rank=2*(dp-1)/dp*gradient
    flat=2*(dp-1)*c['remote_alpha_s']+max(flat_rank/c['nic_Bps'],tp*flat_rank/export_bw)
    grad_time=min(flat,hierarchical)
    local_tokens=c['global_tokens']/dp
    message=local_tokens*c['hidden']*c['activation_bytes']
    tp_time=4*c['layers']*(2*(tp-1)*c['local_alpha_s']+2*(tp-1)/tp*message/local_bw)
    compute=6*c['parameters']*c['global_tokens']/total/c['effective_Fps']
    step=compute+tp_time+grad_time+c['update_s']
    rate=total/c['gpu_mtbf_hours']/3600+hosts/c['domain_mtbf_hours']/3600
    recovery=c['restart_fixed_s']+size*c['restore_bytes_per_gpu']/c['restore_Bps']
    overhead=c['checkpoint_s']/c['checkpoint_interval_s']+rate*(c['checkpoint_interval_s']/2+recovery)
    return dict(supernode_gpus=size,supernodes=hosts,tp=tp,dp=dp,local_dp=q,profile=profile['name'],gradient_shard_bytes=gradient,per_rank_remote_bytes=per_rank,per_supernode_remote_bytes=exported,egress_Bps=export_bw,compute_s=compute,tp_s=tp_time,local_gradient_s=local_rs_ag,remote_gradient_s=network,hierarchical_s=hierarchical,flat_s=flat,chosen='hierarchical' if hierarchical<flat else 'flat',step_s=step,tokens_per_s=c['global_tokens']/step,recovery_s=recovery,interruption_rate_per_hour=rate*3600,overhead_fraction=overhead,effective_tokens_per_s=c['global_tokens']/step/(1+overhead))


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--scenario',type=Path,default=ROOT/'calculations/scenarios/supernode-scaling-example.json');p.add_argument('--output-dir',type=Path,default=ROOT/'calculations/results');args=p.parse_args()
    c=json.loads(args.scenario.read_text());results=[evaluate(c,s,profile) for profile in c['profiles'] for s in c['supernode_sizes']]
    sweep=[]
    for profile in c['profiles']:
        for size in c['supernode_sizes']:
            options=[evaluate(dict(c,tp=tp),size,profile) for tp in c['tp_candidates'] if size%tp==0 and tp<=size]
            best=min(options,key=lambda r:r['step_s'])
            sweep.append(dict(profile=profile['name'],supernode_gpus=size,best_tp=best['tp'],candidates=options))
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/'supernode-scaling-book.json').write_text(json.dumps(dict(assumptions=c['assumptions'],results=results,tp_sweep=sweep),ensure_ascii=False,indent=2)+'\n')
    lines=['# 固定 1024 卡训练与超节点大小','', '运行：`python3 calculations/supernode_scaling.py`。输入见 [固定场景](../scenarios/supernode-scaling-example.json)。','',*c['assumptions'],'','| 网络条件 | 超节点卡数 | 每节点跨域 GB | 本地梯度 ms | 跨域梯度 ms | 选择 | 步时间 s | token/s | 含恢复开销 token/s |','|---|---:|---:|---:|---:|---|---:|---:|---:|']
    for r in results:
        lines.append(f"| {r['profile']} | {r['supernode_gpus']} | {r['per_supernode_remote_bytes']/1e9:.1f} | {r['local_gradient_s']*1e3:.1f} | {r['remote_gradient_s']*1e3:.1f} | {r['chosen']} | {r['step_s']:.3f} | {r['tokens_per_s']:.0f} | {r['effective_tokens_per_s']:.0f} |")
    lines+=['','## 重新比较 TP 与 DP','', '| 网络条件 | 超节点卡数 | 最优候选 TP | 候选 TP: 步时间秒 |','|---|---:|---:|---|']
    for r in sweep:
        entries=', '.join(f"{x['tp']}: {x['step_s']:.3f}" for x in r['candidates'])
        lines.append(f"| {r['profile']} | {r['supernode_gpus']} | {r['best_tp']} | {entries} |")
    (args.output_dir/'supernode-scaling-book.md').write_text('\n'.join(lines)+'\n');print('\n'.join(lines))


if __name__=='__main__':main()
