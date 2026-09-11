"""ECMP hashing of n equal flows onto m equal uplinks, and per-packet spraying reorder wait.

Exact method for the maximum load.  Each flow independently picks one of m uplinks
uniformly (the hash is treated as uniform over uplinks).  For a bound L the number of
assignments in which every uplink carries at most L flows is

    A(L) = n! * [x^n] (sum_{j=0}^{L} x^j / j!)^m,

so P(max <= L) = A(L) / m^n exactly, and E[max] = sum_{L=0}^{n-1} (1 - P(max <= L)).
The truncated exponential polynomial is raised to the m-th power with Fraction
coefficients, so every probability is an exact rational; no simulation or bound is used.
Per-packet spraying reuses packet_reorder.calculate for the striping and ordered-delivery
timeline; the path delays are declared inputs, not measured.
"""
from fractions import Fraction
from math import factorial

from ..declared import exact, input_sources as _sources
from ..units import positive_int
from . import packet_reorder


def _poly_mul(a, b, degree):
    out = [Fraction(0)] * (degree + 1)
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            if i + j > degree:
                break
            out[i + j] += x * y
    return out


def _poly_pow(base, power, degree):
    result = [Fraction(1)] + [Fraction(0)] * degree
    while power:
        if power & 1:
            result = _poly_mul(result, base, degree)
        power >>= 1
        if power:
            base = _poly_mul(base, base, degree)
    return result


def max_load_distribution(flows, uplinks):
    """Exact P(max load <= L) for L = 0..flows."""
    positive_int(flows, 'flows'); positive_int(uplinks, 'uplinks')
    if flows > 4096:
        raise ValueError('flows limited to 4096 for exact polynomial arithmetic')
    total = Fraction(uplinks) ** flows
    n_fact = factorial(flows)
    cdf = []
    for bound in range(flows + 1):
        base = [Fraction(1, factorial(j)) if j <= bound else Fraction(0) for j in range(flows + 1)]
        count = _poly_pow(base, uplinks, flows)[flows] * n_fact
        cdf.append(count / total)
    return cdf


def calculate(flows=128, uplinks=16, spray_paths=8, spray_tokens=1024, spray_packet_bytes=4096,
              spray_path_delays_ns=None, spray_path_bytes_per_second=50 * 10**9, spray_model='qwen3-8b',
              input_sources=None):
    inputs = {k: v for k, v in locals().items() if k != 'input_sources'}
    sources = _sources(inputs, input_sources)
    cdf = max_load_distribution(flows, uplinks)
    if cdf[-1] != 1:
        raise ValueError('Distribution does not sum to one')
    expected = sum((1 - cdf[bound] for bound in range(flows)), Fraction(0))
    pmf = [cdf[0]] + [cdf[i] - cdf[i - 1] for i in range(1, flows + 1)]
    ideal = Fraction(flows, uplinks)
    no_collision = (Fraction(factorial(uplinks), factorial(uplinks - flows)) / Fraction(uplinks) ** flows
                    if flows <= uplinks else Fraction(0))
    empty = uplinks * (1 - Fraction(1, uplinks)) ** flows
    p99 = next(bound for bound in range(flows + 1) if cdf[bound] >= Fraction(99, 100))
    rows = [dict(max_load=bound, probability_exact=str(pmf[bound]), probability=float(pmf[bound]),
                 cumulative_exact=str(cdf[bound])) for bound in range(flows + 1) if pmf[bound]]
    spray = None
    if spray_paths:
        delays = [1000 * (i + 1) for i in range(spray_paths)] if spray_path_delays_ns is None else spray_path_delays_ns
        if len(delays) != spray_paths:
            raise ValueError('spray_path_delays_ns must list one delay per spray path')
        reorder = packet_reorder.calculate(model=spray_model, tokens=spray_tokens, packet_bytes=spray_packet_bytes,
                                           path_delays_ns=delays, path_bytes_per_second=spray_path_bytes_per_second,
                                           lost_packets=[], recovery_delay_ns=0)
        summary = reorder['summary']
        serial = Fraction(summary['payload_bytes'] * 10**9, spray_path_bytes_per_second) + min(delays)
        spray = dict(paths=spray_paths, path_delays_ns=delays, payload_bytes=summary['payload_bytes'],
                     packet_count=summary['packet_count'],
                     first_ordered_delivery_exact_ns=summary['first_ordered_delivery_exact_ns'],
                     completion_exact_ns=summary['completion_exact_ns'],
                     peak_retained_reorder_bytes=summary['peak_retained_reorder_bytes'],
                     peak_retained_packets=summary['peak_retained_packets'],
                     reorder_area_exact_byte_ns=summary['reorder_area_exact_byte_ns'],
                     single_path_serial_counterfactual_exact_ns=str(serial),
                     spray_speedup_exact=str(serial / Fraction(summary['completion_exact_ns'])),
                     reorder_wait_exact_ns=str(Fraction(summary['completion_exact_ns'])
                                               - (Fraction(summary['payload_bytes'] * 10**9, spray_paths * spray_path_bytes_per_second) + max(delays))),
                     sources=reorder['sources'])
    return dict(schema_version=1, calculation='hash-collision', scenario=inputs, declared_input_sources=sources,
                method='exact truncated-exponential polynomial: P(max<=L) = n! [x^n] (sum_{j<=L} x^j/j!)^m / m^n',
                summary=dict(flows=flows, uplinks=uplinks, ideal_load_per_uplink_exact=str(ideal),
                             expected_max_load_exact=str(expected), expected_max_load=float(expected),
                             expected_max_over_ideal=float(expected / ideal),
                             p99_max_load=p99,
                             probability_no_collision_exact=str(no_collision), probability_no_collision=float(no_collision),
                             expected_empty_uplinks_exact=str(empty), expected_empty_uplinks=float(empty),
                             effective_uplinks_exact=str(flows / expected), effective_uplinks=float(flows / expected),
                             effective_fraction_of_nominal_cut_exact=str(ideal / expected),
                             effective_fraction_of_nominal_cut=float(ideal / expected)),
                max_load_distribution=rows, per_packet_spray=spray,
                assumptions=[
                    '每条流独立、均匀地哈希到 m 条等速上行；流大小相同。这是 ECMP 的教学模型，不是具体交换机哈希函数或实际流量分布。',
                    'n 条流是同一台叶交换机（多轨拓扑中的同一条 rail）上必须穿过脊层的流，m 是该叶的上行数（clos-cut 结果：k=64 无阻塞叶 32 条，3:1 超额订阅叶 16 条）。错位配对的八条流从八台不同的叶交换机出发，彼此不会在同一叶的上行上冲突，因此不构成一个 n=8、m=8 的场景。',
                    '最大负载分布用截断指数多项式精确计算（有理数），期望与 99 分位均为精确值；不做模拟。',
                    '有效割集 = 理想每链路流数 / E[最大负载]：假定各流受最忙链路限速到同一速率（公平共享），其余链路的空闲容量不能被已经分配的流使用。',
                    '逐包喷洒复用 packet-reorder 模型：按序号轮转路径、各路径独立串行、无丢包，接收端按连续前缀交付。路径延迟为声明输入；乱序等待 = 完成时刻减去理想并行传输加最长路径延迟。',
                ])
