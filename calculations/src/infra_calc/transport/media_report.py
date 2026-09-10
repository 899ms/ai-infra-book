"""Compact media feedback reports; full packet evidence remains in JSON."""
from collections import Counter
from fractions import Fraction


def _text(value):
    return str(value).replace('|', '\\|').replace('\n', ' ')


def _number(value):
    if value is None:
        return '未提供'
    number = Fraction(str(value))
    return f'{number.numerator:,}' if number.denominator == 1 else str(number)


def _seconds(value):
    if value is None:
        return '未完成／无记录'
    return f'{float(Fraction(str(value))):.9f}'.rstrip('0').rstrip('.') + 's'


def _yes(value):
    return '是' if value is True else '否' if value is False else '未提供'


def markdown(result):
    """Render observed outcomes without running a model or expanding every packet."""
    inputs = result['inputs']
    app, net = inputs['application'], inputs['network']
    summary = result['summary']
    pending = summary.get('pending_packets', {})
    lines = [
        '# 媒体共享连接与真实反馈', '',
        f"全部业务完成（结果标志）：**{_yes(summary.get('complete'))}**；全部消息交付：{_yes(summary.get('all_messages_delivered'))}。",
        f"观察截止：{_seconds(net.get('until'))}；待发送包：上行 {_number(pending.get('up'))}、下行 {_number(pending.get('down'))}。队列为空不等于业务成功。", '',
        '## 业务交付与质量', '',
        '| 业务 | 完成 | 必要消息齐备 | 完成时刻 | 版本可用 | 缺少依赖数 |',
        '|---|---|---|---|---|---:|',
    ]
    for business in result.get('businesses', []):
        usable = _yes(business.get('usable')) if 'usable' in business else '不适用'
        lines.append(f"| {_text(business['id'])} | {_yes(business.get('complete'))} | {_yes(business.get('all_required_delivered'))} | {_seconds(business.get('complete_at'))} | {usable} | {len(business.get('missing', []))} |")
    for business in result.get('businesses', []):
        if business.get('kind') == 'screenshot':
            lines.extend(['', f"截图 {_text(business['id'])}：期望版本 {_text(business.get('expected_version', '未提供'))}，结果到达时版本 {_text(business.get('version_at_result', '未提供'))}；按序交付不能替代版本可用性。"])
        if business.get('kind') != 'tts':
            continue
        blocks = business.get('blocks', [])
        finished = sum(row.get('play_end') is not None for row in blocks)
        started = sum(row.get('play_start') is not None for row in blocks)
        lines.extend(['', f"音频 {_text(business['id'])}：首次播放 {_seconds(business.get('first_play'))}；实际播放结束 {_seconds(business.get('playback_end'))}；已开始 {started}/{len(blocks)} 块，已播放结束 {finished}/{len(blocks)} 块。",
                      f"观察期内停顿 {_seconds(business.get('stall_seconds'))}；缺失音频 {_seconds(business.get('missing_audio_seconds'))}。计划播放结束不代表观察期内实际播放结束。", '',
                      '| 音频块 | 到达 | 播放开始 | 计划播放结束 | 实际播放结束 |', '|---|---|---|---|---|'])
        for index, row in enumerate(blocks[:12]):
            lines.append(f"| {index + 1} | {_seconds(row.get('arrival'))} | {_seconds(row.get('play_start'))} | {_seconds(row.get('scheduled_play_end'))} | {_seconds(row.get('play_end'))} |")
        if len(blocks) > 12:
            lines.append(f'其余 {len(blocks) - 12} 块见完整 JSON。')
    stats = {d: Counter() for d in ('up', 'down')}
    identity = {}
    for packet in result.get('transmissions', []):
        d = packet['direction']
        row = stats[d]
        row['packets'] += 1
        row['wire'] += packet['wire_bytes']
        row['ack'] += packet['kind'] == 'ack'
        row['drop'] += bool(packet.get('dropped'))
        row['recovery'] += packet.get('recovery_of') is not None
        row['probe'] += bool(packet.get('probe'))
        frames = packet.get('frames', [])
        for frame in frames:
            row[frame['type'] + '_payload'] += frame['length']
        kinds = {frame['type'] for frame in frames}
        identity[d, packet['pn']] = ('mixed_payload' if len(kinds) > 1 else next(iter(kinds)) if kinds else packet['kind'])
    lines.extend(['', '## 实际发送与反馈', '',
                  f"已安排发送的线上字节：{_number(summary.get('wire_bytes'))}B；观察期内实际序列化字节：{_number(summary.get('serialized_wire_bytes_by_horizon'))}B。",
                  f"唯一接收业务字节：{_number(summary.get('unique_received_application_bytes'))}B；完整消息交付业务字节：{_number(summary.get('delivered_application_bytes'))}B。发送 payload 可含重传，不能当作唯一接收量。", '',
                  '| 方向 | 发送包 | ACK 包 | STREAM 发送payload B | DATAGRAM 发送payload B | 线上 B | 实际drop | 恢复包 | probe包 |',
                  '|---|---:|---:|---:|---:|---:|---:|---:|---:|'])
    for d, label in [('up', '上行'), ('down', '下行')]:
        s = stats[d]
        lines.append('| ' + label + ' | ' + ' | '.join(_number(s[k]) for k in ('packets', 'ack', 'stream_payload', 'datagram_payload', 'wire', 'drop', 'recovery', 'probe')) + ' |')
    losses = Counter()
    for d, rows in result.get('losses', {}).items():
        for row in rows:
            for pn in row.get('pns', [row.get('pn')]):
                losses[identity.get((d, pn), 'unknown')] += 1
    names = {'ack': '纯 ACK', 'stream': 'STREAM 数据', 'datagram': 'DATAGRAM', 'mixed_payload': '混合payload', 'max': 'MAX控制', 'ping': 'PING', 'unknown': '未知身份'}
    loss_text = '；'.join(f'{names.get(k, _text(k))} {_number(v)}' for k, v in sorted(losses.items())) or '无'
    lines.extend(['', f'发送方声明丢失的传输身份：{loss_text}。纯 ACK 的声明丢失不是数据丢包；声明 loss 与网络实际 drop 分列。'])
    ack_rows = [e for rows in result.get('ack_events', {}).values() for e in rows if e.get('event') == 'start']
    if ack_rows:
        maximum = max(Fraction(e['raw_delay']) for e in ack_rows)
        lines.append(f"聚合 ACK 实际快照 {len(ack_rows):,} 份；最大 raw delay {_seconds(maximum)}；超过声明 max_delay {sum(bool(e['exceeds_max_delay']) for e in ack_rows):,} 份。")
    samples = sum(len(v) for v in result.get('rtt_samples', {}).values())
    timers = Counter(e.get('kind', 'unknown') for rows in result.get('timers', {}).values() for e in rows)
    lines.append(f"实际 sender RTT 样本 {samples:,}；PTO 事件 {timers['pto']:,}。")
    waits = Counter(reason for e in result.get('waits', []) for reason in e.get('reasons', []))
    statuses = Counter(result.get('message_status', {}).values())
    lines.extend(['', '## 共享资源与等待', '',
                  '等待记录是受阻检查次数，不是累计等待时长；同一次检查可包含多个原因。', '',
                  '| 受阻原因 | 记录次数 |', '|---|---:|'])
    for reason, count in sorted(waits.items())[:12]:
        lines.append(f'| {_text(reason)} | {count:,} |')
    if not waits:
        lines.append('| 无受阻记录 | 0 |')
    if len(waits) > 12:
        lines.append(f'另有 {len(waits) - 12} 种原因见 JSON。')
    lines.extend(['', '消息与任务状态计数：' + ('；'.join(f'{_text(k)}={v:,}' for k, v in sorted(statuses.items())) or '无记录') + '。',
                  f"峰值可靠接收内存：上行 {_number(result.get('peak_receive_memory', {}).get('up'))}B、下行 {_number(result.get('peak_receive_memory', {}).get('down'))}B。", '',
                  '## 输入声明与适用范围', '',
                  f"发送调度 {_text(app['scheduling']['send'])}；计算调度 {_text(app['scheduling']['compute'])}；控制器 {_text((net.get('controller') or {}).get('name', 'reference'))}。",
                  f"声明任务 {len(app.get('compute_tasks', [])):,} 个、消息 {len(app.get('messages', [])):,} 条。计算任务耗时是输入假设，不是实测 GPU、模型或编解码延迟。", '',
                  '| 声明计算任务（最多12项） | 输入耗时 |', '|---|---:|'])
    policy = net.get('ack_policy', 'immediate_each_packet')
    if isinstance(policy, dict):
        policy_text = f"聚合 every={policy.get('every', 2)}，max_delay={_seconds(policy.get('max_delay', '0.01'))}，exponent={policy.get('delay_exponent', 3)}"
    else:
        policy_text = _text(policy)
    lines[lines.index('| 声明计算任务（最多12项） | 输入耗时 |'):lines.index('| 声明计算任务（最多12项） | 输入耗时 |')] = [
        f"ACK 策略：{policy_text}。初始 cwnd {_number(net.get('initial_cwnd'))}B；消费延迟：{'不消费／不动态释放额度' if net.get('consume_delay') is None else _seconds(net['consume_delay'])}。", '',
    ]
    for task in app.get('compute_tasks', [])[:12]:
        lines.append(f"| {_text(task['id'])} | {_seconds(task['duration_seconds'])} |")
    lines.extend(['', '这是有限单路径 QUIC 风格网络与声明媒体 DAG 的参考计算。每方向共享发送窗口、拥塞反馈与物理链路；不代表浏览器默认、真实 TCP/HTTP3 或无线媒体实现。取消、到期、版本过时与播放失败保留为业务结果。完整 JSON 保存逐包 PN、STREAM 区间、ACK、loss、RTT 和数值误差，Markdown 不展开逐包日志。'])
    return '\n'.join(lines) + '\n'
