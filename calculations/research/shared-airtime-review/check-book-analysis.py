#!/usr/bin/env python3
"""Independently check the three currently saved layered ledgers, no simulation."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parent
ANALYSIS=RESEARCH/'shared-airtime-book-analysis'
RUNS=RESEARCH/'shared-airtime-book-inputs/runs'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
checks=[]
for name in ['image-baseline','mixed-fifo-immediate','mixed-fifo-aggregate']:
 p=RUNS/(name+'-manifest.json');manifest=json.loads(p.read_text());ledger=json.loads((ANALYSIS/(name+'-ledger.json')).read_text())
 rp=RUNS/manifest['result_file'];r=json.loads(rp.read_text())
 assert sha(rp)==manifest['result_sha256']==ledger['result_sha256']
 assert sha(p)==ledger['manifest_sha256']
 n=len(r['wireless_attempts']);ip=0;psdu=0;rf_us=0;reserved_us=0
 for a in r['wireless_attempts']:
  assert a['outcome']=='success' and a['received'] and a['feedback_known']
  b=a['service']['ip_bytes'];ip+=b;psdu+=b+36
  # Fixed original chosen PHY, independent of service.duration fields.
  duration=20+4*((22+8*(b+36)+215)//216)
  rf_us+=duration+44;reserved_us+=34+duration+16+44
 octets=ledger['radio_octets'];seconds=ledger['air_seconds_exact']
 assert octets['ip_bytes_in_radio_attempts']==ip
 assert octets['data_psdu_bytes']==psdu and octets['mac_ack_psdu_bytes']==14*n
 assert octets['all_psdu_bytes']==psdu+14*n
 assert octets['mac_llc_fcs_over_ip']==36*n
 assert F(seconds['radio_transmit'])==F(rf_us,1000000)
 assert F(seconds['reserved'])==F(reserved_us,1000000)
 assert F(seconds['access_idle'])==F(34*n,1000000)
 assert F(seconds['remaining_non_transmit_after_access'])==F(16*n,1000000)
 assert F(r['summary']['wan_serialized_ip_bytes_by_horizon'])==r['summary']['wire_bytes']==ip
 played=[]
 for b in r['businesses']:
  for block in b.get('blocks',[]):
   if block['play_end'] is not None:assert F(block['play_end'])<=F(str(r['inputs']['network']['until']))
  if b['kind']=='tts':played.append(sum(x['play_end'] is not None for x in b['blocks']))
 checks.append(dict(case=name,result_sha256=sha(rp),attempts=n,ip_bytes=ip,all_psdu_bytes=psdu+14*n,reserved_seconds=str(F(reserved_us,1000000)),played_completed_blocks=played))
 del r
report=dict(status='PASS_THREE_EXISTING_LEDGERS',script_hashes={n:sha(ANALYSIS/n) for n in ['compare.py','summarize.py']},checks=checks,
 findings=['Revised compare baseline summary is generation-bound; original static gap was reported and corrected', 'Revised compare uses actual WAN metric; in these three complete cases it equals wire_bytes', 'play_end excludes future scheduled end in inspected application implementation', 'PSDU and MAC ACK separately counted once; no double counting found'])
(HERE/'book-analysis-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
