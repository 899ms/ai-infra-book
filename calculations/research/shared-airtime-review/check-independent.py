#!/usr/bin/env python3
"""Independent arithmetic and tiny abstract event oracle; does not execute ns-3."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import heapq
import json

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / 'shared-airtime-inputs'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scalar(value):
    if isinstance(value, list):
        return [scalar(x) for x in value]
    if isinstance(value, bool):
        return value
    return F(value)


def schedule(threshold):
    """Quarter-second event clock. ACK snapshot at service start, credit at receipt.

    No loss, propagation, MAC contention or PHY simulation. The sole medium
    stays reserved after data/ACK payload reception until its MAC exchange ends.
    """
    queue = []
    serial = 0

    def event(at, kind, value=None):
        nonlocal serial
        serial += 1
        heapq.heappush(queue, (at, serial, kind, value))

    now = 0
    busy = False
    sent = 0
    flight = set()
    pending = set()
    deadline = None
    arrivals = []
    ack_arrivals = []
    ack_intervals = []
    reservations = []
    while True:
        while queue and queue[0][0] == now:
            _, _, kind, value = heapq.heappop(queue)
            if kind == 'idle':
                busy = False
            elif kind == 'data_received':
                arrivals.append(F(now, 4))
                if not pending:
                    deadline = now + 16
                    event(deadline, 'timer')
                pending.add(value)
            elif kind == 'ack_received':
                flight.difference_update(value)
                ack_arrivals.append(F(now, 4))
            # A stale timer merely wakes the loop; current deadline controls readiness.
        if not busy:
            if pending and (len(pending) >= threshold or now >= deadline):
                snapshot = set(pending)
                pending.clear()
                deadline = None
                busy = True
                event(now + 1, 'ack_received', snapshot)
                event(now + 2, 'idle')
                interval = [F(now, 4), F(now + 2, 4)]
                ack_intervals.append(interval)
                reservations.append(interval)
            elif sent < 3 and len(flight) < 2:
                pn = sent
                sent += 1
                flight.add(pn)
                busy = True
                event(now + 4, 'data_received', pn)
                event(now + 5, 'idle')
                reservations.append([F(now, 4), F(now + 5, 4)])
        if not queue:
            break
        now = queue[0][0]
        assert now <= 48
    assert len(arrivals) == 3 and not flight and not pending
    assert all(a[1] <= b[0] for a, b in zip(reservations, reservations[1:]))
    return {'data_arrivals': arrivals, 'ACK_intervals': ack_intervals,
            'transport_ACK_receiver_arrivals': ack_arrivals,
            'total_airtime': sum(end - start for start, end in reservations),
            'tail_complete': arrivals[-1], 'tail_slot_usable': arrivals[-1] <= 5}


def main():
    locks = json.loads((INPUT / 'sources.lock.json').read_text())
    sources = []
    for entry in locks:
        path = INPUT / entry['file']
        assert path.stat().st_size == entry['bytes']
        assert digest(path) == entry['sha256']
        sources.append({'file': entry['file'], 'bytes': entry['bytes'],
                        'sha256': digest(path), 'url': entry['url']})
    commit = json.loads((INPUT / 'sources/ns3-release-commit.json').read_text())
    assert commit['id'] == '43dce6710b8df69685e3479c1d33a571dda714ea'
    profile = json.loads((INPUT / 'profiles.json').read_text())
    phy = profile['source_backed_reference_selection']['phy']
    assert phy['basic_rate_set_bps'] == [6000000]
    assert phy['band'] == '5GHz' and phy['channel_width_hz'] == 20000000
    layout = profile['source_backed_reference_selection']['layout']
    assert [layout[k] for k in ['ipv4_header_bytes', 'udp_header_bytes', 'llc_snap_bytes',
                               'data_mac_header_bytes', 'mac_fcs_bytes']] == [20, 8, 8, 24, 4]
    # Integer bit/symbol arithmetic, independently from author's check implementation.
    def ppdu_us(psdu, mbps):
        symbols = (16 + 8 * psdu + 6 + 4 * mbps - 1) // (4 * mbps)
        return 20 + 4 * symbols

    sizes = [1200 + 20 + 8 + 8 + 24 + 4, 64 + 20 + 8 + 8 + 24 + 4, 10 + 4]
    durations = [ppdu_us(sizes[0], 54), ppdu_us(sizes[1], 54), ppdu_us(sizes[2], 6)]
    assert sizes == [1264, 128, 14] and durations == [208, 40, 44]
    assert 16 + 2 * 9 + 208 + 16 + 44 == 302
    assert 16 + 2 * 9 + 40 + 16 + 44 == 134
    cases = {x['id']: x for x in json.loads((INPUT / 'hand-oracles.json').read_text())['cases']}
    checks = []
    def equal(case, key, actual):
        assert scalar(actual) == scalar(cases[case]['expected'][key]), (case, key, actual)
        checks.append({'case': case, 'field': key, 'derived': actual})

    name = 'shared-nonpreemptive'
    available = 0
    intervals = []
    for ready in [0, 0]:
        start = max(ready, available)
        available = start + 1
        intervals.append([start, available])
    equal(name, 'shared_intervals', intervals)
    equal(name, 'shared_finish', available)
    equal(name, 'independent_serializers_intervals', [[0, 1], [0, 1]])

    name = 'two-layer-static-account'
    equal(name, 'mac_ack_for_data_count', 2)
    for threshold, suffix in [(1, 'immediate'), (2, 'every2')]:
        ack_count = (2 + threshold - 1) // threshold
        equal(name, 'transport_ack_count_' + suffix, ack_count)
        equal(name, suffix + '_total_seconds', 2 * F(5, 4) + ack_count * F(1, 2))

    name = 'busy-channel-ACK-snapshot'
    received = {0: F(0), 1: F(11, 4)}
    start = F(3)
    largest = max(pn for pn, at in received.items() if at <= start)
    raw = start - received[largest]
    equal(name, 'largest_pn', largest)
    equal(name, 'ack_snapshot_ranges', [[0, largest]])
    equal(name, 'deadline', 0 + 1)
    equal(name, 'raw_delay_seconds', raw)
    equal(name, 'encoded_delay', raw * 1000000 // 8)
    equal(name, 'decoded_delay_seconds', F(raw * 1000000 // 8) * F(8, 1000000))
    equal(name, 'exceeds_max_delay', raw > 1)
    equal(name, 'deadline_lateness_seconds', start - 1)
    variant = cases[name]['variant_no_new_PN']
    assert F(variant['raw_delay_seconds']) == start - received[0] == 3
    assert variant['encoded_delay'] == (start - received[0]) * 1000000 // 8 == 375000

    name = 'MAC-ACK-loss-versus-end-to-end-recovery'
    # Receiver de-duplicates on immutable transport PN; MAC retry has no new PN.
    delivery_times = {}
    attempts = [(7, F(1)), (7, F(3))]
    for pn, at in attempts:
        delivery_times.setdefault(pn, at)
    equal(name, 'mac_attempt_pns', [pn for pn, _ in attempts])
    equal(name, 'unique_application_contributions', len(delivery_times))
    equal(name, 'first_receiver_delivery', delivery_times[7])
    equal(name, 'second_receive_duplicate_at', attempts[1][1])
    equal(name, 'sender_MAC_success_known', F(3, 2) + F(1, 2) + 1 + F(1, 4))

    name = 'fewer-ACKs-later-tail'
    outcomes = {}
    for threshold, policy in [(1, 'immediate'), (4, 'every4')]:
        outcomes[policy] = schedule(threshold)
        for key, value in outcomes[policy].items():
            equal(name, policy + '_' + key, value)
    equal(name, 'every4_missing_audio_seconds', F(1, 4) if not outcomes['every4']['tail_slot_usable'] else 0)
    equal(name, 'airtime_saved_seconds', outcomes['immediate']['total_airtime'] - outcomes['every4']['total_airtime'])

    counterexamples = {
        '45us_as_full_ack_timeout': {'rxstart_after_data_end_us': 16 + 20,
                                     'watchdog_after_data_end_us': 16 + 9 + 20,
                                     'ack_complete_after_data_end_us': 16 + 44,
                                     'false_failure_us_early': 60 - 45},
        'ack_rate_copied_from_data': {'wrong_ack_ppdu_us': ppdu_us(14, 54),
                                     'correct_ack_ppdu_us': 44,
                                     'wrong_data_exchange_us': 34 + 208 + 16 + ppdu_us(14, 54)},
        'duplicate_ip_udp_overhead': {'wrong_psdu_bytes': 1264 + 28,
                                     'wrong_data_ppdu_us': ppdu_us(1264 + 28, 54)},
        'no_symbol_ceiling': {'wrong_data_ppdu_us': F(20) + F(16 + 8 * 1264 + 6, 54),
                              'correct_data_ppdu_us': 208},
        'deadline_lateness_is_not_ack_delay': {'lateness_seconds': 2, 'raw_delay_seconds': F(1, 4)},
        'mac_confirmation_is_not_transport_credit': {'MAC_success_first_data': F(5, 4),
                                                    'every4_transport_credit_first_return': F(21, 4)},
        'airtime_is_not_tail_or_walltime': {'every4_service': F(19, 4), 'tail': F(13, 2),
                                          'last_exchange_end': 11},
    }
    report = {'status': 'PASS_INDEPENDENT_SOURCE_AND_ARITHMETIC_REVIEW',
              'scope': 'Pinned local original rehash/read; five hand oracles; independent quarter-second event model for case 5. Not ns-3 execution or IEEE text verification.',
              'checker_sha256': digest(Path(__file__)),
              'input_sha256': {name: digest(INPUT / name) for name in ['sources.lock.json', 'profiles.json', 'hand-oracles.json', 'CONTRACT.md']},
              'sources': sources, 'psdu_bytes': sizes, 'ppdu_us': durations,
              'oracle_checks': checks, 'counterexamples': counterexamples}
    (HERE / 'review-result.json').write_text(json.dumps(report, indent=2, default=str) + '\n')
    print(f'PASS: {len(sources)} original hashes; {len(cases)} oracles; {len(checks)} derived field comparisons; {len(counterexamples)} counterexamples')


if __name__ == '__main__':
    main()
