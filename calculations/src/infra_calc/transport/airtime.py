"""Exact declared single-frame exchange segments, without contention simulation.

ip_bytes already includes IP/UDP. MAC ACK is a separate PHY frame. Offsets
are relative to exchange reservation, including declared access idle time.
"""
from fractions import Fraction as F


def seconds(value, label, positive=False):
    if isinstance(value, bool):
        raise ValueError(label)
    try:
        result = F(str(value))
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError(label) from error
    if result < 0 or (positive and result == 0):
        raise ValueError(label)
    return result


def integer(value, label, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(label)
    return value


def ppdu(phy, psdu_bytes, rate_bps):
    """Selected unaggregated legacy OFDM symbol ledger; not arbitrary Wi-Fi."""
    integer(psdu_bytes, 'PSDU bytes', 1)
    rate = seconds(rate_bps, 'PHY rate', True)
    symbol = seconds(phy['ofdm_symbol_seconds'], 'symbol duration', True)
    per_symbol = rate * symbol
    if per_symbol.denominator != 1:
        raise ValueError('noninteger data bits per OFDM symbol')
    service = integer(phy['service_bits'], 'SERVICE bits')
    tail = integer(phy['tail_bits'], 'tail bits')
    bits = service + 8 * psdu_bytes + tail
    symbols = (bits + per_symbol.numerator - 1) // per_symbol.numerator
    preamble = seconds(phy['preamble_seconds'], 'preamble')
    header = seconds(phy['signal_header_seconds'], 'SIGNAL header')
    extension = seconds(phy['signal_extension_seconds'], 'signal extension')
    return dict(psdu_bytes=psdu_bytes, service_bits=service, payload_bits=8*psdu_bytes,
                tail_bits=tail, data_bits_per_symbol=per_symbol.numerator,
                symbols=symbols, symbol_padding_bits=symbols*per_symbol.numerator-bits,
                preamble_seconds=preamble, header_seconds=header,
                payload_symbol_seconds=symbols*symbol, extension_seconds=extension,
                duration=preamble+header+symbols*symbol+extension)


def exchange(profile, ip_bytes, outcome='success', *, transport_ack=False,
             direction_switch=False):
    """Return exact service offsets; caller owns queueing, retries and causality.

    Source-backed failure timeout is explicitly relative to DATA TXEND.
    Teaching failure timeout is explicitly relative to DATA TXSTART.
    A missing timeout rejects failure simulation rather than using RXSTART's
    45 us monitor as a complete-ACK timeout. No sender state is advanced here.
    """
    integer(ip_bytes, 'IP packet bytes', 1)
    if outcome not in ('success', 'data_lost', 'mac_ack_lost'):
        raise ValueError('unknown exchange outcome')
    if type(transport_ack) is not bool or type(direction_switch) is not bool:
        raise ValueError('exchange flags must be booleans')
    if 'phy' in profile:
        phy, layout, access = profile['phy'], profile['layout'], profile['access']
        extra = sum(integer(layout[k], k) for k in
                    ('llc_snap_bytes','data_mac_header_bytes','mac_fcs_bytes','security_overhead_bytes'))
        psdu = ip_bytes + extra
        data = ppdu(phy, psdu, phy['data_rate_bps'])
        ack_size = sum(integer(layout[k], k) for k in
                       ('normal_mac_ack_header_bytes','normal_mac_ack_fcs_bytes'))
        ack = ppdu(phy, ack_size, phy['mac_ack_rate_bps'])
        idle = seconds(access['pre_exchange_idle_seconds'], 'access idle')
        idle += integer(access['backoff_slots_selected'], 'backoff slots') * seconds(access['slot_seconds'], 'slot')
        if direction_switch:
            idle += seconds(access['direction_switch_extra_seconds'], 'switch delay')
        propagation = seconds(access['radio_propagation_selected_seconds'], 'radio propagation')
        sifs = seconds(access['sifs_seconds'], 'SIFS')
        data_duration, ack_duration = data['duration'], ack['duration']
        timeout = access.get('mac_ack_complete_timeout_seconds')
        fail_from_data_start = None if timeout is None else data_duration + seconds(timeout, 'full ACK timeout after TXEND')
        mode = 'declared legacy OFDM reference'
    else:
        idle = seconds(profile['contention_seconds'], 'teaching access idle')
        propagation = seconds(profile['propagation_seconds'], 'teaching propagation')
        if transport_ack:
            # The teaching whole ACK exchange includes its own MAC confirmation.
            whole = seconds(profile['transport_ack_whole_exchange_seconds'], 'ACK exchange', True)
            ack_duration = seconds(profile['transport_ack_post_data_sifs_plus_mac_ack_seconds'], 'teaching ACK confirmation')
            data_duration = seconds(profile['transport_ack_ppdu_seconds'], 'teaching ACK data', True)
            if data_duration + ack_duration != whole or profile['whole_exchange_includes_own_mac_ack'] is not True:
                raise ValueError('inconsistent teaching whole ACK exchange')
        else:
            data_duration = seconds(profile['data_ppdu_seconds'], 'teaching data', True)
            ack_duration = seconds(profile['post_data_sifs_plus_mac_ack_seconds'], 'teaching confirmation')
        sifs = F(0)  # Confirmation is indivisible in this teaching profile.
        timeout = profile.get('full_ack_failure_known_from_data_txstart_seconds')
        fail_from_data_start = None if timeout is None else seconds(timeout, 'teaching timeout from TXSTART')
        psdu, ack_size = None, None
        data, ack = None, None
        mode = 'declared teaching phase times, not an IEEE PHY'
    data_start = idle
    data_end = idle + data_duration
    nominal_receive = data_end + propagation
    ack_start = nominal_receive + sifs
    ack_end = ack_start + ack_duration
    success_known = ack_end + propagation
    if outcome == 'success':
        feedback = success_known
    else:
        if fail_from_data_start is None:
            raise ValueError('failure needs an explicit full-ACK timeout')
        feedback = data_start + fail_from_data_start
        if feedback < success_known:
            raise ValueError('failure declared before a valid ACK could complete')
    return dict(mode=mode, outcome=outcome, ip_bytes=ip_bytes, data_psdu_bytes=psdu,
                mac_ack_psdu_bytes=ack_size, data_ppdu=data, mac_ack_ppdu=ack,
                access_idle_seconds=idle, data_start_offset=data_start,
                data_end_offset=data_end, nominal_data_receive_offset=nominal_receive,
                data_receive_offset=None if outcome=='data_lost' else nominal_receive,
                mac_ack_start_offset=None if outcome=='data_lost' else ack_start,
                mac_ack_end_offset=None if outcome=='data_lost' else ack_end,
                mac_feedback_offset=feedback, exchange_end_offset=feedback,
                reserved_service_seconds=feedback,
                radio_transmit_seconds=(data_duration+(F(0) if outcome=='data_lost' else ack_duration)) if data is not None else None,
                data_and_confirmation_phase_seconds=data_duration+(F(0) if outcome=='data_lost' else sifs+ack_duration),
                note='Offsets do not authorize end-to-end ACK, cwnd, flow credit or retry before their actual events.')
