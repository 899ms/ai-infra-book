#!/usr/bin/env python3
"""Reproduce the explicitly assumed chapter-ten running design exercise."""
from pathlib import Path
from fractions import Fraction
import json, math
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
source=json.loads((ROOT/'calculations/results/training-deadline-book.json').read_text())
F=source['summary']['task_training_matrix_flops']
N=8190735360
assumptions=dict(kind='teaching_design_not_measurement',parameters=N,effective_tokens=10**11,sequence_tokens=8192,sequences_per_update=384,deadline_days=30,planned_nontraining_days=5,device_peak_flops=165200000000000,local_efficiency=.4,net_device_gib=22,additional_live_gib=10,exposed_communication_seconds=4,input_wait_seconds=.5,checkpoint_bytes=14*N,checkpoint_bandwidth_bytes_per_second=8000000000,checkpoint_useful_interval_seconds=1800,device_mtbf_days=365,recovery_seconds=120,input_workers=4,sequences_per_worker_second=2)
b=384*8192;steps=math.ceil(Fraction(10**11,b));c=Fraction(14*N,8000000000)
rows=[]
for p in (32,48):
 local=Fraction(F,10**11)*b/(p*165200000000000*Fraction(2,5))
 base=local+Fraction(9,2);lam=Fraction(p,365*86400)
 loss=c/1800+lam*(900+120)
 budget=Fraction(25*86400,steps)/(1+loss)
 rows.append(dict(devices=p,hosts=p//8,microbatches_per_device=384//p,persistent_gib=16*N/p/2**30,peak_budget_gib=16*N/p/2**30+10,local_seconds=float(local),base_step_seconds=float(base),save_loss=float(c/1800),redo_loss=float(lam*900),recovery_loss=float(lam*120),total_loss=float(loss),base_training_days=float(steps*base/86400),finish_days=float(5+steps*base*(1+loss)/86400),max_base_step_seconds=float(budget),max_communication_seconds=float(budget-local-Fraction(1,2)),minimum_local_efficiency=float(local*Fraction(2,5)/(budget-Fraction(9,2)))))
out=dict(assumptions=assumptions,source='calculations/results/training-deadline-book.json',task_matrix_flops=F,tokens_per_update=b,updates=steps,raw_step_budget_seconds=25*86400/steps,candidates=rows)
(HERE/'design-case.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
lines=['# 贯穿设计题：32 卡与 48 卡\n','此题以既有 Qwen3-8B 矩阵工作为来源，其余配置和服务时间作为显式教学输入。它给出条件式系统设计结果，不是新执行的 GPU 基准。\n','## 条件\n','- 100B 有效 token；384 条 8192-token 序列组成一次训练迭代；最后不足满批时保守地仍按完整步时安排。','- RTX 4090 dense BF16 峰值 165.2 TFLOP/s；单卡计算效率 40%，计时涵盖设备内的前后向计算、非矩阵运算及参数更新，通信等待与输入另加。','- 四台或六台八卡主机；全组 ZeRO-3；TP=PP=1；每卡单序列微批，分别累积 12／8 次。','- 每卡可用显存 22 GiB，全部激活、完整模块参数、工作区的同时存活附加量上限设为 10 GiB；实现需以保存策略和模块粒度满足该目标。','- 两套方案每步通信等待预算 4 s，平均输入等待 0.5 s；四个数据准备进程各准备两条序列/s。这些是设计输入，不是从网卡标称速率推得的实测。','- 每 1800 s 有用训练同步保存一次；检查点 14N bytes，写速率 8 GB/s；每卡独立 MTBF 为 365 天，任一卡故障中断作业，恢复 120 s。','- 保存及恢复使用正文一阶模型；5 天预留用于启动、评估与计划性停顿，不重复包括保存和故障成本。\n','## 复算\n','以每卡分配的计算量除以设备峰值与效率得到单卡计算时间，加 4.5 s 得每步训练时间。保存恢复附加比例为 c/1800 + λ×900 + λ×120。总天数为 5 + 训练迭代次数×每步训练时间×(1+附加比例)/86400。\n','| 卡数 | 峰值预算/GiB | 单卡计算/s | 每步训练时间/s | 附加比例 | 完成/天 | 每步训练时间上限/s | 最低单卡计算效率 |','|---|---:|---:|---:|---:|---:|---:|---:|']
for r in rows:lines.append(f"| {r['devices']} | {r['peak_budget_gib']:.3f} | {r['local_seconds']:.3f} | {r['base_step_seconds']:.3f} | {r['total_loss']:.5%} | {r['finish_days']:.3f} | {r['max_base_step_seconds']:.3f} | {r['minimum_local_efficiency']:.3%} |")
lines+=['\n数值源和完整输入见 [design-case.json](design-case.json)，执行 `python3 manuscripts/ch10/design-case.py` 可复算。正文保留足以判断 30 天期限的精度。']
(HERE/'design-case.md').write_text('\n'.join(lines)+'\n')
