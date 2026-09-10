"""Verify prewritten arithmetic constants without importing any network candidate."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json

ROOT = Path(__file__).resolve().parent
raw = (ROOT / 'oracles.json').read_bytes()
data = json.loads(raw)
cases = {c['id']: c for c in data['cases']}
assert F(1228 * 8, 9824) == 1
assert F(92 * 8, 736) == 1
shared = cases['shared-cwnd-three-streams']['expected']
assert 3 * 1228 + 3 * 92 == shared['total_wire_bytes'] == 3960
assert 3 * 1168 == shared['unique_application_bytes']
assert 2 * 1200 == shared['maximum_flight_bytes']
assert [F(x)+2 for x in shared['data_send_starts']] == list(map(F,shared['data_arrivals']))
assert [F(x)+2 for x in shared['ack_send_starts']] == list(map(F,shared['ack_arrivals']))
assert 2 * 1168 == cases['stream-and-connection-credit-independent']['expected']['max_data_consumed_after_both']
voice = cases['datagram-loss-without-retransmission']['expected']
assert voice['declared_application_bytes'] == voice['delivered_application_bytes'] + voice['lost_application_bytes']
assert 2*1228 == voice['data_only_wire_bytes_excluding_ACK_and_probe']
reverse = cases['reverse-data-blocks-ACK']['expected']
end = F(1228 * 8, 736)
assert end == F(reverse['reverse_full_data_end'])
assert end+2 == F(reverse['ACK_arrival_at_sender'])
delay=end-2
tick=F(8,1000000)
encoded=delay//tick
assert encoded == reverse['ACK_encoded_delay']
assert encoded*tick == F(reverse['ACK_decoded_delay'])
assert encoded*tick-delay == F(reverse['ACK_encoding_residual'])
assert sum(cases['screenshot-local-version']['expected']['PNG_slices']) == 3443
result=dict(status='passed',cases=len(cases),scope='Arithmetic consistency of prewritten constants only; no candidate execution or causal validation',oracle_sha256=hashlib.sha256(raw).hexdigest(),checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(ROOT/'arithmetic-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
