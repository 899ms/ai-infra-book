"""Explicit feedback delay and post-feedback offered rate over a finite fluid buffer."""
from fractions import Fraction
from ..units import positive_int
from .periodic_queue import calculate as periodic_queue


def calculate(offered_bytes_per_second=80*10**9,capacity_bytes_per_second=50*10**9,
              reduced_bytes_per_second=40*10**9,feedback_ns=20000,after_feedback_ns=100000,
              initial_queue_bytes=262144,buffer_bytes=1048576):
    inputs=locals().copy()
    for name,value in inputs.items():
        if name=='buffer_bytes' and value is None:continue
        positive_int(value,name,allow_zero=name in ('initial_queue_bytes','buffer_bytes','reduced_bytes_per_second'))
    window=feedback_ns+after_feedback_ns
    jobs=[dict(period_ns=window,on_ns=feedback_ns,offset_ns=0,rate_bytes_per_second=offered_bytes_per_second)]
    if reduced_bytes_per_second:
        jobs.append(dict(period_ns=window,on_ns=after_feedback_ns,offset_ns=feedback_ns,rate_bytes_per_second=reduced_bytes_per_second))
    result=periodic_queue(jobs=jobs,capacity_bytes_per_second=capacity_bytes_per_second,
                          window_ns=window,initial_queue_bytes=initial_queue_bytes,buffer_bytes=buffer_bytes)
    at_feedback=next(row for row in result['queue_segments'] if Fraction(row['end_exact_ns'])==feedback_ns)
    unbounded=max(Fraction(0),initial_queue_bytes+Fraction((offered_bytes_per_second-capacity_bytes_per_second)*feedback_ns,10**9))
    result['calculation']='feedback-fluid-queue';result['scenario']=inputs
    result['summary'].update(feedback_applied_ns=feedback_ns,
                             unbounded_queue_at_feedback_exact_bytes=str(unbounded),
                             bounded_queue_at_feedback_exact_bytes=at_feedback['queue_end_exact_bytes'],
                             after_feedback_rate_below_capacity=reduced_bytes_per_second<capacity_bytes_per_second)
    result['assumptions'][0]=(f'反馈算例：到达{offered_bytes_per_second/1e9:g}GB/s、出口{capacity_bytes_per_second/1e9:g}GB/s，{feedback_ns/1000:g}us后降低到{reduced_bytes_per_second/1e9:g}GB/s，再观察{after_feedback_ns/1000:g}us；'
                              +f'初始积压{initial_queue_bytes/1024:g}KiB、缓冲'+('不限' if buffer_bytes is None else f'{buffer_bytes/1024:g}KiB')+'。反馈时间与速率是输入，不是DCQCN/PFC算法生成或硬件实测。')
    result['assumptions'][1]='观察起点积压明确给定；反馈时刻切换到给定速率，观察窗口结束后不自动重复反馈周期。'
    result['assumptions'].append('只观察一次反馈和指定后续窗口，不模拟多轮控制、ECN阈值、PFC暂停、丢弃数据重传或任务完成。减到出口速率只停止增长，不自动清空已有积压；减到出口以下才有余量排空。')
    return result


def incast(senders=(8, 16, 64), sender_bytes_per_second=50 * 10**9, egress_bytes_per_second=50 * 10**9,
           free_buffer_bytes=1048576, declared_one_hop_cable_m=30, declared_propagation_ns_per_m=5,
           mtu_bytes=1500, declared_end_to_end_rtt_ns=20000, input_sources=None):
    """N-1 senders at rate B into one receiver port: allowed feedback delay and required buffer.

    Feedback distance rows: one-hop pause (PFC style, references/text/dcqcn.txt lines 450-458: "A PAUSE
    message sent to an upstream device takes some time to arrive and take effect. To avoid packet drops,
    the PAUSE sender must reserve enough buffer to process any packets it may receive during this time.
    This includes packets that were in flight when the PAUSE was sent, and the packets sent by the
    upstream device while it is processing the PAUSE message.") versus end-to-end feedback (declared RTT).
    The one-hop distance is modeled as pause-frame propagation upstream plus in-flight data propagation
    downstream plus one MTU serialization at the sender rate; cable length and ns/m are declared inputs.
    """
    from ..declared import exact, input_sources as _sources
    inputs = {k: v for k, v in locals().items() if k not in ('input_sources', 'exact', '_sources')}
    sources = _sources(inputs, input_sources)
    rate = exact(sender_bytes_per_second, 'sender_bytes_per_second')
    egress = exact(egress_bytes_per_second, 'egress_bytes_per_second')
    positive_int(free_buffer_bytes, 'free_buffer_bytes'); positive_int(mtu_bytes, 'mtu_bytes')
    positive_int(declared_one_hop_cable_m, 'declared_one_hop_cable_m'); positive_int(declared_propagation_ns_per_m, 'declared_propagation_ns_per_m')
    positive_int(declared_end_to_end_rtt_ns, 'declared_end_to_end_rtt_ns')
    if not isinstance(senders, (list, tuple)) or not senders:
        raise ValueError('senders must be a nonempty list of receiver-group sizes N')
    propagation = declared_one_hop_cable_m * declared_propagation_ns_per_m
    serialization = Fraction(mtu_bytes * 10**9) / rate
    one_hop_ns = 2 * propagation + serialization
    distances = [dict(name='one_hop_pause', feedback_ns_exact=str(one_hop_ns), feedback_ns=float(one_hop_ns),
                      components=dict(pause_propagation_ns=propagation, in_flight_propagation_ns=propagation,
                                      mtu_serialization_ns_exact=str(serialization))),
                 dict(name='end_to_end', feedback_ns_exact=str(declared_end_to_end_rtt_ns), feedback_ns=float(declared_end_to_end_rtt_ns),
                      components=dict(declared_rtt_ns=declared_end_to_end_rtt_ns))]
    rows = []
    for n in senders:
        positive_int(n, 'N')
        if n < 2:
            raise ValueError('N must include at least one sender besides the receiver')
        offered = (n - 1) * rate
        excess = offered - egress
        row = dict(N=n, senders=n - 1, offered_bytes_per_second_exact=str(offered), excess_bytes_per_second_exact=str(excess),
                   allowed_feedback_ns_exact=None, allowed_feedback_ns=None, required_buffer_bytes={}, fluid_check={})
        if excess <= 0:
            row['note'] = 'offered rate does not exceed egress; no feedback needed'
            rows.append(row); continue
        allowed = Fraction(free_buffer_bytes * 10**9) / excess
        row['allowed_feedback_ns_exact'] = str(allowed); row['allowed_feedback_ns'] = float(allowed)
        for distance in distances:
            need = Fraction(distance['feedback_ns_exact']) * excess / 10**9
            row['required_buffer_bytes'][distance['name']] = dict(exact=str(need), bytes=float(need),
                                                                   fits_free_buffer=need <= free_buffer_bytes,
                                                                   fraction_of_free_buffer_exact=str(need / free_buffer_bytes))
        floor_ns = int(allowed)
        if floor_ns >= 1 and int(offered) == offered and int(egress) == egress:
            check = calculate(offered_bytes_per_second=int(offered), capacity_bytes_per_second=int(egress),
                              reduced_bytes_per_second=0, feedback_ns=floor_ns, after_feedback_ns=max(1, floor_ns),
                              initial_queue_bytes=0, buffer_bytes=free_buffer_bytes)['summary']
            row['fluid_check'] = dict(feedback_ns=floor_ns, dropped_exact_bytes=check['dropped_exact_bytes'],
                                      peak_queue_exact_bytes=check['peak_queue_exact_bytes'])
        rows.append(row)
    return dict(schema_version=1, calculation='incast-feedback', scenario=inputs, declared_input_sources=sources,
                feedback_distances=distances, rows=rows,
                summary=dict(free_buffer_bytes=free_buffer_bytes,
                             one_hop_feedback_ns=float(one_hop_ns), end_to_end_feedback_ns=declared_end_to_end_rtt_ns,
                             allowed_feedback_ns={str(r['N']): r['allowed_feedback_ns'] for r in rows},
                             end_to_end_fits={str(r['N']): (r['required_buffer_bytes'].get('end_to_end') or {}).get('fits_free_buffer') for r in rows},
                             one_hop_fits={str(r['N']): (r['required_buffer_bytes'].get('one_hop_pause') or {}).get('fits_free_buffer') for r in rows}),
                assumptions=[
                    'N-1 个发送方同时以速率 B 向一个出口发送，出口速率 B_out；反馈到达前积压以 (N-1)B - B_out 线性增长，允许的反馈时延 = 空闲缓冲/超额速率。流体模型，无报文粒度、无 ECN 概率标记。',
                    '一跳暂停的反馈距离 = 暂停帧上行传播 + 已在线数据下行传播 + 一个 MTU 的串行化；线缆长度与每米传播时延是声明输入。端到端反馈距离取声明 RTT。均不含交换机处理与排队时延。',
                    'fluid_check 用本模块的单次反馈流体队列复算：反馈时延取允许值向下取整 ns，反馈后发送降为 0，确认不丢包；这是自洽检查，不是协议模拟。',
                    '需要的缓冲 = 反馈距离 × 超额速率，是单个出口端口、单优先级的下界；实际交换机按端口/优先级预留 headroom（DCQCN 论文给出每端口每优先级 22.4 KB 的一例，随 MTU 与链路而变）。',
                ])
