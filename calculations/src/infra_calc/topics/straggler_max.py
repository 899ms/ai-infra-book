"""Synchronous step time as the maximum over N ranks, detection signal, three responses, spike rollback.

Per-rank compute time is declared normal with mean = chapter 10.6's 52.2 s single-card compute and a
declared standard deviation.  E[max of N iid normals] = mu + sigma * E[Z_(N)] with
E[Z_(N)] = integral z * N * phi(z) * Phi(z)^(N-1) dz, evaluated by composite Simpson quadrature on
[-12, 12] with the standard library (math.erf); the truncation error is below 1e-12 for N <= 10^6.
The evict response reuses checkpoint_interval.calculate (its first-order loss and Poisson retry model);
the loss-spike rollback rate enters that model as an additional job-level rate through
common_job_mtbf_seconds, so L(tau) = c/tau + (lambda_hw + lambda_spike)(tau/2 + r) is computed there.
"""
from fractions import Fraction
from math import erf, exp, pi, sqrt

from ..declared import exact, input_sources as _sources
from ..units import positive_int
from . import checkpoint_interval


def _phi(z):
    return exp(-z * z / 2) / sqrt(2 * pi)


def _Phi(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


def expected_standard_max(n, intervals=24000, bound=12.0):
    """E[max of n standard normals] by composite Simpson on [-bound, bound]."""
    positive_int(n, 'n')
    if n == 1:
        return 0.0
    if intervals % 2:
        raise ValueError('intervals must be even for Simpson quadrature')
    h = 2 * bound / intervals
    total = 0.0
    for i in range(intervals + 1):
        z = -bound + i * h
        f = z * n * _phi(z) * _Phi(z) ** (n - 1)
        weight = 1 if i in (0, intervals) else 4 if i % 2 else 2
        total += weight * f
    return total * h / 3


def _tail_probability(n, k):
    """P(at least one of n ranks exceeds mu + k sigma)."""
    return 1 - _Phi(k) ** n


def calculate(mean_compute_seconds='52.2', declared_sigma_seconds='1.044', overhead_seconds='4.5',
              ranks=(8, 48, 1024), straggler_k_sigma='3', model='qwen3-8b', checkpoint_devices=48,
              device_mtbf_seconds=365 * 86400, declared_spike_mtbf_seconds=7 * 86400,
              save_bandwidth_bytes_per_second=8 * 10**9, recovery_ns=120 * 10**9,
              intervals_seconds=(300, 600, 900, 1800, 3600), input_sources=None):
    inputs = {k: v for k, v in locals().items() if k != 'input_sources'}
    sources = _sources(inputs, input_sources)
    mean = exact(mean_compute_seconds, 'mean_compute_seconds')
    sigma = exact(declared_sigma_seconds, 'declared_sigma_seconds')
    overhead = exact(overhead_seconds, 'overhead_seconds', allow_zero=True)
    k = exact(straggler_k_sigma, 'straggler_k_sigma')
    for name in ('checkpoint_devices', 'device_mtbf_seconds', 'declared_spike_mtbf_seconds', 'save_bandwidth_bytes_per_second'):
        positive_int(inputs[name], name)
    if not isinstance(ranks, (list, tuple)) or not ranks:
        raise ValueError('ranks must be a nonempty list')
    rows = []
    for n in ranks:
        positive_int(n, 'ranks')
        z = expected_standard_max(n)
        expected_max = float(mean) + float(sigma) * z
        step = expected_max + float(overhead)
        wait_mean_rank = expected_max - float(mean)
        straggler_time = float(mean + k * sigma)
        z_rest = expected_standard_max(n - 1) if n > 1 else 0.0
        rest_max = float(mean) + float(sigma) * z_rest
        redistributed_mean = mean * n / (n - 1) if n > 1 else mean
        redistributed_max = float(redistributed_mean) + float(sigma) * z_rest
        rows.append(dict(ranks=n, expected_standard_max=z, expected_max_seconds=expected_max,
                         expected_step_seconds=step, expected_step_over_mean_step=step / float(mean + overhead),
                         expected_wait_for_mean_rank_seconds=wait_mean_rank,
                         wait_fraction_of_compute=wait_mean_rank / float(mean),
                         probability_some_rank_beyond_k_sigma=_tail_probability(n, float(k)),
                         detection=dict(signal='per-rank bucket AllReduce wait = step_end - own compute end',
                                        straggler_seconds=straggler_time,
                                        wait_of_others_if_one_rank_at_k_sigma=max(0.0, straggler_time - rest_max),
                                        wait_of_straggler=0.0),
                         responses=dict(
                             wait=dict(step_seconds=max(straggler_time, rest_max) + float(overhead)),
                             redistribute=dict(remaining_ranks=n - 1, mean_seconds_exact=str(redistributed_mean),
                                               step_seconds=redistributed_max + float(overhead),
                                               note='straggler removed, its work spread evenly; no migration cost modeled'),
                             evict=dict(note='restart from last checkpoint; cost from checkpoint model below'))))
    base = checkpoint_interval.calculate(model=model, devices=checkpoint_devices, device_mtbf_seconds=device_mtbf_seconds,
                                         common_job_mtbf_seconds=None, save_bandwidth_bytes_per_second=save_bandwidth_bytes_per_second,
                                         recovery_ns=recovery_ns, intervals_seconds=list(intervals_seconds))
    spike = checkpoint_interval.calculate(model=model, devices=checkpoint_devices, device_mtbf_seconds=device_mtbf_seconds,
                                          common_job_mtbf_seconds=declared_spike_mtbf_seconds,
                                          save_bandwidth_bytes_per_second=save_bandwidth_bytes_per_second,
                                          recovery_ns=recovery_ns, intervals_seconds=list(intervals_seconds))
    save_cost = Fraction(base['summary']['blocking_save_cost_exact_seconds'])
    recovery = Fraction(recovery_ns, 10**9)
    evict = [dict(useful_interval_seconds=row['useful_interval_seconds'],
                  expected_lost_work_seconds=row['useful_interval_seconds'] / 2,
                  recovery_seconds=float(recovery), save_cost_seconds=float(save_cost),
                  evict_cost_seconds=row['useful_interval_seconds'] / 2 + float(recovery),
                  hardware_first_order_loss=row['first_order_loss'])
             for row in base['checkpoint_interval_rows']]
    ledger = [dict(useful_interval_seconds=a['useful_interval_seconds'],
                   hardware_only_loss_exact=a['first_order_loss_exact'], hardware_only_loss=a['first_order_loss'],
                   with_spike_rollback_loss_exact=b['first_order_loss_exact'], with_spike_rollback_loss=b['first_order_loss'],
                   poisson_retained_hardware_only=a['poisson_retained_useful_fraction'],
                   poisson_retained_with_spike=b['poisson_retained_useful_fraction'])
              for a, b in zip(base['checkpoint_interval_rows'], spike['checkpoint_interval_rows'])]
    return dict(schema_version=1, calculation='straggler-max', scenario=inputs, declared_input_sources=sources,
                sources=base['sources'], rows=rows,
                evict_response=dict(checkpoint_payload_bytes=base['summary']['checkpoint_payload_bytes'],
                                    blocking_save_cost_exact_seconds=str(save_cost), rows=evict),
                checkpoint_loss=dict(hardware_rate_exact_per_second=base['summary']['job_failure_rate_exact_per_second'],
                                     spike_rate_exact_per_second=str(Fraction(1, declared_spike_mtbf_seconds)),
                                     combined_rate_exact_per_second=spike['summary']['job_failure_rate_exact_per_second'],
                                     first_order_optimal_interval_hardware_only=base['summary']['first_order_optimal_useful_interval_seconds'],
                                     first_order_optimal_interval_with_spike=spike['summary']['first_order_optimal_useful_interval_seconds'],
                                     rows=ledger),
                summary=dict(expected_step_seconds={str(r['ranks']): r['expected_step_seconds'] for r in rows},
                             expected_standard_max={str(r['ranks']): r['expected_standard_max'] for r in rows},
                             mean_step_seconds=float(mean + overhead)),
                assumptions=[
                    f'每 rank 计算时间为独立同分布正态（均值取第 10.6 节 48 卡方案的 52.2 s 单卡计算，标准差为声明输入）；同步步时间 = 最大值 + 声明的通信与输入等待（本次为 {float(overhead):.2f} s）。正态尾部允许负值，但在所用 σ 下概率可忽略。',
                    'E[max] 用阶次统计积分的复合 Simpson 数值求积（标准库），不是精确有理数；未模拟相关性、周期性抖动或持续性慢卡。',
                    '检测信号是每 rank 在桶 AllReduce 上的等待：均值 rank 的期望等待 = E[max] - μ；一张卡慢到 μ+kσ 时，其余卡等待 ≈ 该卡时间减其余 N-1 卡的最大值。',
                    '三种响应：等待（步时间取慢卡时间）、重分配（去掉慢卡后均匀摊派，均值乘 N/(N-1)，不计迁移成本）、驱逐（从检查点重启，成本 = 期望丢失工作 τ/2 + 恢复时间，复用 checkpoint-interval 的保存成本）。',
                    'loss spike 回滚率作为作业级共同冲击率加入 checkpoint-interval 的一阶损失与 Poisson 模型：L(τ)=c/τ+(λ_hw+λ_spike)(τ/2+r)。spike 的 MTBF 为声明值，未归档实测。',
                ])
