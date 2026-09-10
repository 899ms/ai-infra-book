"""Hand-derived OFDM boundaries and exchange phase/timeout distinctions."""
import copy
import hashlib
import json
from pathlib import Path
from fractions import Fraction as F
from airtime import exchange, ppdu
ROOT=Path(__file__).resolve().parent
INPUT=ROOT.parent/'shared-airtime-inputs/profiles.json'
profiles=json.loads(INPUT.read_text())
reference=profiles['source_backed_reference_selection']
teaching=profiles['abstract_teaching_profile']
checks=[]

def equal(name,actual,expected):
    assert actual==expected,(name,actual,expected)
    checks.append({'case':name,'actual':actual,'expected':expected})

def reject(name,fn):
    try:fn()
    except ValueError as error:checks.append({'case':name,'rejected':str(error)})
    else:raise AssertionError(name)

before=copy.deepcopy(profiles)
data=exchange(reference,1228)
ack=exchange(reference,92,transport_ack=True)
equal('DATA PSDU excludes duplicate IP/UDP',data['data_psdu_bytes'],1264)
equal('transport ACK carrier PSDU',ack['data_psdu_bytes'],128)
equal('normal MAC ACK PSDU',data['mac_ack_psdu_bytes'],14)
equal('DATA 47 OFDM symbols',data['data_ppdu']['symbols'],47)
equal('carrier 5 OFDM symbols',ack['data_ppdu']['symbols'],5)
equal('MAC ACK at independent 6 Mbps: 6 symbols',data['mac_ack_ppdu']['symbols'],6)
equal('DATA PPDU 208 us',data['data_ppdu']['duration'],F(208,1000000))
equal('transport ACK PPDU 40 us',ack['data_ppdu']['duration'],F(40,1000000))
equal('normal MAC ACK PPDU 44 us',data['mac_ack_ppdu']['duration'],F(44,1000000))
equal('DATA reaches receiver at 242 us',data['data_receive_offset'],F(242,1000000))
equal('MAC success known at 302 us',data['mac_feedback_offset'],F(302,1000000))
equal('transport ACK carrier success at 134 us',ack['exchange_end_offset'],F(134,1000000))
equal('radio transmit excludes idle and SIFS',data['radio_transmit_seconds'],F(252,1000000))
# 24B has 214 coded input bits, 25B has 222: adding one byte crosses a symbol.
equal('24B uses one 54 Mbps symbol',ppdu(reference['phy'],24,54000000)['symbols'],1)
equal('25B uses two 54 Mbps symbols',ppdu(reference['phy'],25,54000000)['symbols'],2)
reject('unknown full timeout must not use RXSTART watchdog',lambda:exchange(reference,1228,'mac_ack_lost'))
short=copy.deepcopy(reference);short['access']['mac_ack_complete_timeout_seconds']='0.000045'
reject('45us would precede valid 60us full ACK',lambda:exchange(short,1228,'mac_ack_lost'))
failed=copy.deepcopy(reference);failed['access']['mac_ack_complete_timeout_seconds']='0.000080'
f=exchange(failed,1228,'mac_ack_lost')
equal('ACK loss still delivered DATA at 242us',f['data_receive_offset'],F(242,1000000))
equal('ACK loss only known at 322us',f['mac_feedback_offset'],F(322,1000000))
f=exchange(failed,1228,'data_lost')
equal('DATA loss yields no receiver delivery',f['data_receive_offset'],None)
equal('DATA loss emits no MAC ACK',f['mac_ack_start_offset'],None)
equal('DATA loss still waits same declared deadline',f['mac_feedback_offset'],F(322,1000000))
t=exchange(teaching,1228)
ta=exchange(teaching,92,transport_ack=True)
equal('teaching DATA reception precedes confirmation',t['data_receive_offset'],F(1))
equal('teaching exchange reserved until confirmation',t['exchange_end_offset'],F(5,4))
equal('teaching ACK endpoint reception at 1/4',ta['data_receive_offset'],F(1,4))
equal('teaching ACK exchange includes MAC once',ta['exchange_end_offset'],F(1,2))
equal('two data/two transport ACK static service',2*t['exchange_end_offset']+2*ta['exchange_end_offset'],F(7,2))
equal('two data/one transport ACK static service',2*t['exchange_end_offset']+ta['exchange_end_offset'],F(3))
equal('teaching phases are not claimed RF airtime',t['radio_transmit_seconds'],None)
equal('teaching missing MAC ACK knowledge',exchange(teaching,1228,'mac_ack_lost')['mac_feedback_offset'],F(3,2))
reject('boolean packet length',lambda:exchange(reference,True))
reject('negative packet length',lambda:exchange(reference,-1))
reject('unknown loss semantics',lambda:exchange(reference,1228,'instant-loss'))
assert profiles==before
checks.append({'case':'pure calculator does not mutate profiles','passed':True})
report={'status':'passed','checks':checks,'source_sha256':hashlib.sha256((ROOT/'airtime.py').read_bytes()).hexdigest(),'profile_sha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),'scope':'Exact one-frame service ledger only; no contention, media network or retry scheduling claim'}
(ROOT/'airtime-root-check.json').write_text(json.dumps(report,default=str,indent=2)+'\n')
print('PASS',len(checks),'phase, arithmetic and rejection checks')
