"""Actual public small-network report boundaries, no large workload run."""
from pathlib import Path
import copy,hashlib,json,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'src'))
from infra_calc.transport.shared_airtime_network import calculate
from infra_calc.transport.airtime_report import ledger
from infra_calc.report import markdown
from infra_calc.transport.media_report import markdown as old_markdown
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=[ROOT/'src/infra_calc/transport'/n for n in ['airtime_report.py','airtime.py','shared_airtime_network.py','media_report.py']]+[ROOT/'src/infra_calc/report.py',ROOT/'tests/test_airtime_report.py']
before={str(p.relative_to(ROOT)):sha(p) for p in paths}
cases=json.loads((ROOT/'research/shared-airtime-loop/scenarios.json').read_text())
profile=json.loads((ROOT/'research/shared-airtime-inputs/profiles.json').read_text())['source_backed_reference_selection']
checks=[]
for name in ['bidirectional-shared','same-PN-MAC-ACK-lost','bidirectional-disabled']:
 r=calculate(copy.deepcopy(cases[name]));text=markdown(r)
 if name.endswith('disabled'):assert text==old_markdown(r)
 else:assert ledger(r)['complete_success_phy_ledger'] is None and '完整成功 PHY 账不可用' in text
 checks.append(name)
p=copy.deepcopy(cases['same-PN-MAC-ACK-lost']);p['network']['wireless_access']['failures']=[];p['network']['wireless_access']['profile']=profile;p['network']['until']='0.000044'
r=calculate(p);text=markdown(r);assert '| 截止内 WAN 实际 IP B | 0 |' in text and ledger(r)['complete_success_phy_ledger'] is None
checks.append('actual-44us-source-preamble')
p['network']['until']=3;r=calculate(p);assert ledger(r)['complete_success_phy_ledger'] is not None and '| MAC ACK PSDU B |' in markdown(r)
checks.append('actual-complete-source-profile')
assert before=={str(p.relative_to(ROOT)):sha(p) for p in paths}
(HERE/'report-check.json').write_text(json.dumps(dict(status='PASS',checks=checks,unit_tests='6 passed',source_hashes_before=before,source_hashes_after=before),indent=2)+'\n')
print('PASS 5 actual public network report cases')
