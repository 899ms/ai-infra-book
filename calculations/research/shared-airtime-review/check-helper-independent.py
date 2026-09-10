#!/usr/bin/env python3
"""Independent fixed numbers and symbol-boundary checks of exchange helper."""
import copy
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'shared-airtime-loop/airtime.py'
PROFILE = HERE.parent / 'shared-airtime-inputs/profiles.json'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
before = sha(SOURCE)
spec = importlib.util.spec_from_file_location('reviewed_airtime', SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
p = json.loads(PROFILE.read_text())
reference = p['source_backed_reference_selection']
teaching = p['abstract_teaching_profile']
checks = []


def eq(label, actual, expected):
    assert actual == expected, (label, actual, expected)
    checks.append({'check': label, 'actual': actual, 'expected': expected})


def reject(label, call):
    try:
        call()
    except ValueError:
        checks.append({'check': label, 'rejected': True})
    else:
        raise AssertionError(label)


# The caller passes an IP packet, so this is 1200 QUIC + one IP/UDP 28.
a = module.exchange(reference, 1228)
for key, value in {'data_psdu_bytes':1264, 'mac_ack_psdu_bytes':14,
                   'data_start_offset':F(34,1000000), 'data_end_offset':F(242,1000000),
                   'data_receive_offset':F(242,1000000), 'mac_ack_start_offset':F(258,1000000),
                   'mac_ack_end_offset':F(302,1000000), 'mac_feedback_offset':F(302,1000000),
                   'reserved_service_seconds':F(302,1000000),
                   'radio_transmit_seconds':F(252,1000000),
                   'data_and_confirmation_phase_seconds':F(268,1000000)}.items():
    eq('source.success.'+key, a[key], value)
ack = module.exchange(reference, 92, transport_ack=True)
eq('QUIC ACK PSDU contains one IP/UDP', ack['data_psdu_bytes'], 128)
eq('QUIC ACK complete reservation', ack['exchange_end_offset'], F(134,1000000))
eq('QUIC ACK carrier received before MAC confirmation', ack['data_receive_offset'], F(74,1000000))

# At 54 Mbps: 24 bytes uses 214 coded-input bits, 25 uses 222 and crosses 216.
# At 6 Mbps: 3 bytes uses 46 bits, 4 uses 54 and crosses 48.
for rate, pairs in [(54000000, [(24,1),(25,2),(51,2),(52,3)]),
                    (6000000, [(3,2),(4,3),(6,3),(7,4)])]:
    for size, count in pairs:
        result = module.ppdu(reference['phy'], size, rate)
        eq(f'symbols.{rate}.{size}', result['symbols'], count)
        eq(f'padding.{rate}.{size}', result['symbol_padding_bits'], count*(rate//250000)-(22+8*size))
        eq(f'duration.{rate}.{size}', result['duration'], F(20+4*count,1000000))

for outcome in ['data_lost','mac_ack_lost']:
    reject('unknown source full timeout: '+outcome, lambda: module.exchange(reference,1228,outcome))
    selected = copy.deepcopy(reference)
    selected['access']['mac_ack_complete_timeout_seconds'] = '0.000080'
    result = module.exchange(selected,1228,outcome)
    eq(outcome+'.failure after TXEND', result['mac_feedback_offset'], F(322,1000000))
    eq(outcome+'.reservation', result['reserved_service_seconds'], F(322,1000000))
    eq(outcome+'.receive', result['data_receive_offset'], None if outcome=='data_lost' else F(242,1000000))
    eq(outcome+'.MAC ACK emitted', result['mac_ack_end_offset'], None if outcome=='data_lost' else F(302,1000000))
    eq(outcome+'.RF', result['radio_transmit_seconds'], F(208 if outcome=='data_lost' else 252,1000000))
    selected['access']['mac_ack_complete_timeout_seconds'] = '0.000045'
    reject('RXSTART 45us cannot serve as full ACK: '+outcome, lambda: module.exchange(selected,1228,outcome))

selected = copy.deepcopy(reference)
selected['access']['radio_propagation_selected_seconds'] = '0.000010'
result = module.exchange(selected,1228)
eq('propagated DATA arrives +10us', result['data_receive_offset'], F(252,1000000))
eq('propagated ACK transmitted after remote SIFS', result['mac_ack_start_offset'], F(268,1000000))
eq('propagated ACK returns +10us', result['mac_feedback_offset'], F(322,1000000))
eq('propagation adds no transmitted RF', result['radio_transmit_seconds'], F(252,1000000))

selected = copy.deepcopy(teaching)
selected['contention_seconds'] = '1/8'
for outcome in ['success','data_lost','mac_ack_lost']:
    result = module.exchange(selected,1228,outcome)
    eq('teaching.'+outcome+'.no invented RF', result['radio_transmit_seconds'], None)
    eq('teaching.'+outcome+'.relative timeout', result['mac_feedback_offset'], F(11,8) if outcome=='success' else F(13,8))
    eq('teaching.'+outcome+'.received', result['data_receive_offset'], None if outcome=='data_lost' else F(9,8))
result = module.exchange(teaching,92,transport_ack=True)
eq('teaching ACK payload receipt', result['data_receive_offset'], F(1,4))
eq('teaching ACK confirmation complete', result['mac_feedback_offset'], F(1,2))
eq('teaching indivisible confirmation not RF', result['radio_transmit_seconds'], None)
for invalid in [True, 0, -1, '1228']:
    reject('strict IP bytes '+repr(invalid), lambda: module.exchange(reference,invalid))
reject('nonboolean ACK flag', lambda:module.exchange(reference,1228,transport_ack=1))
reject('nonboolean switch flag', lambda:module.exchange(reference,1228,direction_switch=1))
eq('source stable before/after', sha(SOURCE), before)
report = {'status':'PASS', 'scope':'Independent exact helper cases, not network/PHY execution',
          'source_sha256':before,'profiles_sha256':sha(PROFILE), 'checker_sha256':sha(Path(__file__)),
          'checks':checks}
(HERE/'helper-review-result.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
print(f'PASS {len(checks)} independent helper checks; source {before}')
