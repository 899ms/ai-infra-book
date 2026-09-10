"""Bounded observed wireless report, with a conditional complete PHY ledger."""
from collections import Counter
from fractions import Fraction as F

from .media_report import markdown as media_markdown


def ledger(result):
    """Aggregate only complete successful physical exchanges; never simulate."""
    rows = result['wireless_attempts']
    until = F(str(result['inputs']['network']['until']))
    complete = all(
        row['received'] and row['feedback_known'] and row['outcome'] == 'success'
        and F(row['end']) <= until
        and row['service']['data_ppdu'] is not None
        and row['service']['mac_ack_ppdu'] is not None
        and row['service']['radio_transmit_seconds'] is not None
        for row in rows
    )
    reservations = result.get('wireless_reservations', [])
    complete = complete and all(
        row['end'] is not None and F(row['end']) <= until for row in reservations
    )
    reserved = sum((F(row['service']['reserved_service_seconds']) for row in rows), F(0))
    observed = F(result['wireless_summary']['observed_reserved_seconds'])
    # An idle reservation that never starts DATA also cannot be converted into
    # a complete-exchange PHY ledger. Preserve the actual reservation separately.
    complete = complete and reserved == observed
    facts = dict(
        started_attempts=len(rows),
        known_feedback=sum(row['feedback_known'] for row in rows),
        known_failures=sum(row['feedback_known'] and row['outcome'] != 'success' for row in rows),
        received_attempts=sum(row['received'] for row in rows),
        retry_attempts=sum(row['attempt'] > 1 for row in rows),
        observed_reserved_seconds=str(observed),
        wan_serialized_ip_bytes=result['summary'].get('wan_serialized_ip_bytes_by_horizon'),
        complete_success_phy_ledger=None,
    )
    if not complete:
        return facts
    octets = Counter()
    radio = F(0)
    access = F(0)
    for row in rows:
        service = row['service']
        octets['ip_in_attempts'] += service['ip_bytes']
        octets['data_psdu'] += service['data_psdu_bytes']
        octets['mac_ack_psdu'] += service['mac_ack_psdu_bytes']
        radio += F(service['radio_transmit_seconds'])
        access += F(service['access_idle_seconds'])
    facts['complete_success_phy_ledger'] = dict(
        ip_in_attempts=octets['ip_in_attempts'], data_psdu=octets['data_psdu'],
        mac_ack_psdu=octets['mac_ack_psdu'],
        total_psdu=octets['data_psdu'] + octets['mac_ack_psdu'],
        mac_llc_fcs_over_ip=octets['data_psdu'] - octets['ip_in_attempts'],
        reserved_seconds=str(reserved), radio_seconds=str(radio),
        access_idle_seconds=str(access),
        other_non_transmit_seconds=str(reserved - radio - access),
    )
    return facts


def markdown(result):
    """Append a compact airtime ledger to the existing business-quality report."""
    facts = ledger(result)
    lines = [media_markdown(result).rstrip(), '', '## 单共享空口分层账', '',
             '声明的共享非抢占服务模型；不是实测 Wi-Fi、完整 DCF 或 TACK。', '',
             '| 已观测量 | 值 |', '|---|---:|',
             f"| 截止内预约占用 s | {facts['observed_reserved_seconds']} |",
             f"| 截止内 WAN 实际 IP B | {facts['wan_serialized_ip_bytes'] if facts['wan_serialized_ip_bytes'] is not None else '未提供'} |",
             f"| 已开始 MAC 尝试 | {facts['started_attempts']} |",
             f"| 接收端已收到的尝试 | {facts['received_attempts']} |",
             f"| 已知 MAC 反馈／其中失败 | {facts['known_feedback']}／{facts['known_failures']} |",
             f"| 同 PN 重试尝试 | {facts['retry_attempts']} |", '']
    full = facts['complete_success_phy_ledger']
    if full is None:
        lines += ['完整成功 PHY 账不可用：包含教学未拆分确认、失败或截止未完成的服务；不把未来整段或教学确认时间记为已观测 RF。', '']
    else:
        lines += ['以下仅汇总已完成的成功 PHY 交换；DATA PSDU 与独立 MAC ACK 分列。', '',
                  '| 完整成功交换账 | 值 |', '|---|---:|']
        for label, key in [('无线尝试中的 IP B', 'ip_in_attempts'),
                           ('DATA PSDU B', 'data_psdu'), ('MAC ACK PSDU B', 'mac_ack_psdu'),
                           ('全部 PSDU B', 'total_psdu'), ('DATA 内 LLC/MAC/FCS 等增量 B', 'mac_llc_fcs_over_ip'),
                           ('RF 发射 s', 'radio_seconds'), ('接入空等 s', 'access_idle_seconds'),
                           ('其余非发射预约 s（SIFS／传播）', 'other_non_transmit_seconds')]:
            lines.append(f'| {label} | {full[key]} |')
        lines.append('')
    lines += ['PHY 前导、符号填充与空等不换算为虚构 IP 字节；无线尝试字节不是唯一业务字节。',
              'WAN 与无线可流水重叠，累计服务不可直接加到基线完成时刻。MAC 确认不等于端到端 ACK 或业务可用；逐交换证据保留在 JSON。', '']
    return '\n'.join(lines)
