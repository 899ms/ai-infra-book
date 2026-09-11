"""Loss that is not congestion: Mathis rate, BBR-style goodput, reliable-stream tail, and FEC repair.

Path inputs come from references/author-context/queqiao-168ff4b/PATH-CHARACTER-DC-20260826.md:
- line 17: "| Round trip | 199-207ms, min 185.9ms |"; line 20: "| Capacity knee, downstream | ~333 Mbit/s |"
- line 35: "| Download, US->CN | UDP 1-300 Mbit/s | **~14%** | knee ~333 Mbit/s |"
- line 66: "Mathis gives `MSS/(RTT*sqrt(p))` = 1448/(0.2*sqrt(0.14)) = **0.155 Mbit/s**. We measured 0.13-0.47."
- line 831: "Re-run with one fixed file, `dashboard.wav` at 354,640 bytes"
- line 833: "One round trip is about 200ms and the model is about 30ms, so the floor is roughly 230ms"
- line 87-90: direct TCP best 105.8 Mbit/s, transport 310.4 Mbit/s; downstream 68 to 84 direct against 224 to 268
- lines 236-238: "the coded substrate carried 2270 symbols, recovered 1708 of them, and lost 5"
- lines 244-247: UDP direct 163/3200 lost p99 213.7ms; UDP via transport 34 lost p99 217.6ms; TCP via transport 0 lost p99 728.4ms
Model sources: references/text/mathis-tcp-model.txt line 81-96 (BW = (MSS/RTT) C/sqrt(p), C = sqrt(3/2) = 1.22
for periodic loss with every-packet ACK, 0.87 delayed ACK, 1.31 random loss every-packet ACK, 0.93 random
loss delayed ACK) and line 178 (the simpler bound BW < (MSS/RTT)(1/sqrt(p)) used by the path document);
references/text/bbr-ietf-draft.txt line 462 ("BBR.bdp = BBR.bw * BBR.min_rtt"), line 353 (Startup cwnd
gain 2.0) and line 2943 (ProbeBW_UP cwnd gain 2), which is where cwnd = 2 x BDP comes from.
All measured figures are reference rows only; the models below use the declared path parameters.
"""
from fractions import Fraction
from math import comb, isqrt

from ..declared import exact, input_sources as _sources
from ..units import ceil_div, positive_int


def _sqrt_fraction(value):
    """Exact square root when both numerator and denominator are perfect squares, else float."""
    n, d = value.numerator, value.denominator
    if isqrt(n) ** 2 == n and isqrt(d) ** 2 == d:
        return Fraction(isqrt(n), isqrt(d))
    return float(value) ** 0.5


def _binomial_tail(total, up_to, p):
    """P(losses <= up_to) among total symbols with loss probability p, exact rational."""
    q = 1 - p
    return sum((comb(total, i) * p ** i * q ** (total - i) for i in range(up_to + 1)), Fraction(0))


def calculate(rtt_seconds='0.2', knee_bits_per_second=333 * 10**6, loss_probability='0.14', mss_bytes=1448,
              request_bytes=354640, declared_model_seconds='0.03', fec_symbol_bytes=1448, fec_target='0.999',
              fec_extra_losses=(0, 1), reference=None, input_sources=None):
    inputs = {k: v for k, v in locals().items() if k != 'input_sources'}
    sources = _sources(inputs, input_sources)
    rtt = exact(rtt_seconds, 'rtt_seconds')
    knee = exact(knee_bits_per_second, 'knee_bits_per_second')
    p = exact(loss_probability, 'loss_probability')
    model_seconds = exact(declared_model_seconds, 'declared_model_seconds', allow_zero=True)
    target = exact(fec_target, 'fec_target')
    positive_int(mss_bytes, 'mss_bytes'); positive_int(request_bytes, 'request_bytes'); positive_int(fec_symbol_bytes, 'fec_symbol_bytes')
    if not 0 < p < 1 or not 0 < target < 1:
        raise ValueError('loss probability and FEC target must lie strictly between 0 and 1')
    reference = {} if reference is None else reference
    # Mathis steady state.
    root = _sqrt_fraction(p)
    mathis_bits = Fraction(mss_bytes * 8) / rtt / root if isinstance(root, Fraction) else float(mss_bytes * 8) / float(rtt) / root
    # BBR-style: pace at the knee with cwnd = 2 BDP, goodput (1-p) x knee.
    bdp_bytes = knee * rtt / 8
    bbr_goodput = (1 - p) * knee
    # Reliable stream of n packets with independent loss, ideal selective repair once per RTT.
    n = ceil_div(request_bytes, mss_bytes)
    serialization = Fraction(request_bytes * 8) / knee
    serial_budget = rtt + model_seconds + serialization
    expected_losses = n * p
    round_cdf = []
    r = 0
    expected_rounds = Fraction(0)
    while True:
        cdf = (1 - p ** r) ** n  # P(all n delivered within r rounds)
        round_cdf.append(cdf)
        expected_rounds += 1 - cdf
        if cdf >= Fraction(999999, 1000000) or r > 60:
            break
        r += 1
    p99_rounds = next(i for i, c in enumerate(round_cdf) if c >= Fraction(99, 100))
    p50_rounds = next(i for i, c in enumerate(round_cdf) if c >= Fraction(1, 2))
    expected_completion = serial_budget + (expected_rounds - 1) * rtt
    p99_completion = serial_budget + (p99_rounds - 1) * rtt
    # FEC: k data symbols + r repair symbols; block decodes if losses <= r (+ extra tolerance rows).
    k = ceil_div(request_bytes, fec_symbol_bytes)
    fec_rows = []
    for extra in fec_extra_losses:
        positive_int(extra, 'fec_extra_losses', allow_zero=True)
        repair = extra
        while _binomial_tail(k + repair, repair - extra, p) < target:
            repair += 1
            if repair > 10 * k:
                raise ValueError('FEC search did not converge')
        prob = _binomial_tail(k + repair, repair - extra, p)
        fec_rows.append(dict(tolerated_extra_losses=extra, data_symbols=k, repair_symbols=repair, total_symbols=k + repair,
                             overhead_ratio_exact=str(Fraction(repair, k)), overhead_ratio=float(Fraction(repair, k)),
                             block_recovery_probability=float(prob), expected_losses_in_block=float((k + repair) * p),
                             repair_over_expected_losses=float(Fraction(repair) / ((k + repair) * p))))
    single_rtt_completion = serial_budget
    reference_rows = dict(
        mathis_measured_mbit_per_second='0.13-0.47 (document line 66)',
        direct_tcp_sustained_mbit_per_second='3.6-105.8 upload; 68-84 downstream (lines 87-90)',
        transport_sustained_mbit_per_second='0.4-310.4 upload; 224-268 downstream (lines 87-90)',
        coded_symbols=dict(carried=2270, recovered=1708, lost=5, recovered_fraction_exact=str(Fraction(1708, 2270)),
                           residual_loss_exact=str(Fraction(5, 2270)), source_lines='236-238'),
        frame_sessions_16x200=dict(udp_direct=dict(lost=163, delivered=3037, p50_ms=193.6, p99_ms=213.7),
                                   udp_transport=dict(lost=34, delivered=3166, p50_ms=208.2, p99_ms=217.6),
                                   tcp_transport=dict(lost=0, delivered=3200, p50_ms=208.4, p99_ms=728.4),
                                   path_loss_during_run='3.6%', source_lines='244-247'),
        fixed_file_request_ms=dict(new_connection=dict(direct_p50=1185.3, transport_p50=301.6),
                                   warm_tuned=dict(direct_p50=240.9, transport_p50=236.5, direct_p99=251.7, transport_p99=246.4),
                                   source_lines='831-838'),
        **reference)
    summary = dict(mathis_mbit_per_second=float(mathis_bits) / 10**6, bbr_ideal_goodput_mbit_per_second=float(bbr_goodput) / 10**6,
                   bdp_bytes=float(bdp_bytes), packets=n, expected_losses=float(expected_losses),
                   serial_budget_seconds=float(serial_budget), expected_completion_seconds=float(expected_completion),
                   p99_completion_seconds=float(p99_completion), expected_rounds=float(expected_rounds), p99_rounds=p99_rounds,
                   fec_repair_symbols=fec_rows[0]['repair_symbols'] if fec_rows else None,
                   fec_overhead_ratio=fec_rows[0]['overhead_ratio'] if fec_rows else None)
    return dict(schema_version=1, calculation='wan-loss-model', scenario=inputs, declared_input_sources=sources, summary=summary,
                path=dict(rtt_seconds_exact=str(rtt), knee_bits_per_second=int(knee), loss_probability_exact=str(p),
                          bdp_bytes_exact=str(bdp_bytes), bdp_bytes=float(bdp_bytes), bdp_packets=float(bdp_bytes / mss_bytes)),
                mathis=dict(formula='MSS/(RTT*sqrt(p))', bits_per_second=float(mathis_bits),
                            mbit_per_second=float(mathis_bits) / 10**6,
                            seconds_for_request=float(request_bytes * 8 / mathis_bits),
                            fraction_of_knee=float(mathis_bits / knee),
                            with_constant_c={label: dict(c=c, mbit_per_second=float(mathis_bits) * c / 10**6,
                                                         seconds_for_request=float(request_bytes * 8 / mathis_bits) / c)
                                             for label, c in (('periodic_loss_every_ack_1.22', 1.22), ('periodic_loss_delayed_ack_0.87', 0.87),
                                                              ('random_loss_every_ack_1.31', 1.31), ('random_loss_delayed_ack_0.93', 0.93))}),
                bbr_ideal=dict(cwnd_bytes_exact=str(2 * bdp_bytes), goodput_bits_per_second_exact=str(bbr_goodput),
                               goodput_mbit_per_second=float(bbr_goodput) / 10**6,
                               seconds_for_request=float(Fraction(request_bytes * 8) / bbr_goodput),
                               goodput_over_mathis=float(bbr_goodput / mathis_bits)),
                reliable_stream=dict(packets=n, expected_losses=float(expected_losses),
                                     serialization_seconds=float(serialization),
                                     serial_budget_seconds_exact=str(serial_budget), serial_budget_seconds=float(serial_budget),
                                     rounds_cdf=[float(c) for c in round_cdf],
                                     expected_rounds=float(expected_rounds), p50_rounds=p50_rounds, p99_rounds=p99_rounds,
                                     expected_completion_seconds=float(expected_completion),
                                     p99_completion_seconds=float(p99_completion),
                                     expected_over_budget=float(expected_completion / serial_budget),
                                     p99_over_budget=float(p99_completion / serial_budget),
                                     no_loss_completion_seconds=float(single_rtt_completion)),
                fec=dict(symbol_bytes=fec_symbol_bytes, target_block_recovery=str(target), rows=fec_rows),
                reference_rows=reference_rows,
                assumptions=[
                    '路径参数（RTT、拐点、擦除率、MSS、请求大小、模型时间）取自鹊桥路径文档并在 docstring 逐行引用；文档中的测量值只作对照行，不参与推导。',
                    'Mathis 公式给出独立随机丢包下 TCP 的稳态速率；BBR 理想行假定以拐点速率 pacing、cwnd=2×BDP、丢包只损失有效载荷 (1-p)。',
                    '可靠流模型：n=ceil(大小/MSS) 个报文独立丢失，每轮 RTT 一次理想选择性重传（重传也可能再丢），完成 = 串行预算 + 额外轮数×RTT。不含拥塞窗口收缩、慢启动或 RTO，因此是有利于 TCP 的下界。',
                    '串行预算 = RTT + 模型时间 + 请求按拐点速率串行化；文档用约 200 ms 往返和 30 ms 模型给出约 230 ms 的下限，本模块另加串行化项。',
                    'FEC：k 个数据符号加 r 个修复符号，块内丢失不超过 r 即可恢复，用二项分布尾精确求最小 r；额外容忍行给出比最小 r 再多承受的丢失数。不模拟符号大小对时延的影响或分块策略。',
                ])
