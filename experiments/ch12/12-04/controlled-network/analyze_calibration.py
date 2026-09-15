import hashlib
import json
import re
from pathlib import Path

R=Path(__file__).resolve().parent
C=R/'calibration'
assert json.loads((C/'completion.json').read_text())['completed_profiles']==3
rows=[]
for label in ['unshaped','rtt80-rate20-loss0','rtt80-rate20-loss01']:
    ping=json.loads((C/(label+'-ping.json')).read_text())
    tcp=json.loads((C/(label+'-tcp.json')).read_text())
    server=json.loads((C/(label+'-server.json')).read_text())
    assert tcp['exit_code']==server['exit_code']==0
    measurement=json.loads(tcp['stdout'])
    assert 'error' not in measurement
    match=re.search(r'= ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+) ms',ping['stdout'])
    assert match,ping
    qdisc=json.loads((C/(label+'-after.json')).read_text())
    rows.append(dict(profile=label,ping_min_ms=float(match[1]),ping_mean_ms=float(match[2]),
                     ping_max_ms=float(match[3]),tcp_receiver_mbit_s=measurement['end']['sum_received']['bits_per_second']/1e6,
                     tcp_retransmits=measurement['end']['sum_sent']['retransmits'],
                     qdisc=json.loads(qdisc['stdout'])))
assert json.loads((C/'qdisc-cleanup.json').read_text())['exit_code']==0
(R/'calibration-summary.json').write_text(json.dumps(dict(status='measured_namespace_shaping',profiles=rows,
    scope='Docker network-none loopback netem calibration; 10 pings/3-second TCP per profile; not a physical WAN or completed application comparison',
    source_sha256={f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in ['Dockerfile','calibrate.py','image-inspect.json']}),indent=2)+'\n')
print(json.dumps([{k:v for k,v in r.items() if k!='qdisc'} for r in rows],indent=2))
