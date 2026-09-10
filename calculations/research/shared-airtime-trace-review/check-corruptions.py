"""Ensure independent trace checks reject specific altered physical evidence."""
from pathlib import Path
import copy
import importlib.util
import json

ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('trace_check',ROOT/'check-trace.py')
check=importlib.util.module_from_spec(spec);spec.loader.exec_module(check)
path=ROOT.parent/'shared-airtime-loop/result.json'
source=json.loads(path.read_text())['same-PN-MAC-ACK-lost']
mutations={
    'radio-overlap':lambda r:r['wireless_reservations'][1].update(start='1'),
    'wrong-ppdu-end':lambda r:r['wireless_attempts'][0].update(data_end='2'),
    'early-failure-knowledge':lambda r:r['wireless_attempts'][0].update(feedback_at='1'),
    'duplicate-transport-sent':lambda r:r['sender_events']['up'].append(copy.deepcopy(r['sender_events']['up'][0])),
    'free-wan-serialization':lambda r:r['transmissions'][0].update(wan_end='1'),
    'invented-business-byte':lambda r:r['summary'].update(unique_received_application_bytes=2),
    'wrong-observed-airtime':lambda r:r['wireless_summary'].update(observed_reserved_seconds='0'),
    'wrong-mac-duplicate-flag':lambda r:r['wireless_attempts'][1].update(duplicate_at_hop_receiver=False),
}
results={}
for name,mutation in mutations.items():
    altered=copy.deepcopy(source);mutation(altered)
    try:check.check(altered)
    except AssertionError:results[name]='rejected'
    else:raise AssertionError('accepted corruption: '+name)
prefix_path=ROOT.parent/'shared-airtime-loop/check-prefix-output.json'
prefix=json.loads(prefix_path.read_text())['result']
check.check(prefix)
(ROOT/'corruption-check.json').write_text(json.dumps(dict(status='passed',corruptions=results,preamble_horizon='passed',input_sha256=check.sha(path),prefix_result_sha256=check.sha(prefix_path),checker_sha256=check.sha(ROOT/'check-trace.py')),indent=2)+'\n')
print('rejected eight corruptions; accepted saved preamble cutoff')
