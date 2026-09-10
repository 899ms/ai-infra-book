"""Source identity and independent input arithmetic; no wireless simulation."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
ROOT=Path(__file__).resolve().parent
rows=json.loads((ROOT/'sources.lock.json').read_text());checks=[]
assert len({r['file'] for r in rows})==len(rows)
for r in rows:
 data=(ROOT/r['file']).read_bytes();assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256'];checks.append(r['file'])
assert {p.name for p in (ROOT/'sources').iterdir() if p.is_file()}=={Path(r['file']).name for r in rows}
assert json.loads((ROOT/'sources/ns3-release-commit.json').read_text())['id']=='43dce6710b8df69685e3479c1d33a571dda714ea'
p=json.loads((ROOT/'profiles.json').read_text());s=p['source_backed_reference_selection'];layout=s['layout'];phy=s['phy'];access=s['access']
assert all(v is None for v in p['deployment_observation'].values())
assert 'WIFI_MAC_FCS_LENGTH = 4' in (ROOT/'sources/wifi-mac-trailer.h').read_text()
assert 'LLC_SNAP_HEADER_LENGTH = 8' in (ROOT/'sources/llc-snap-header.h').read_text()
def ceiling(x):return -(-x.numerator//x.denominator)
def ppdu(size,rate):
 nbits=phy['service_bits']+size*8+phy['tail_bits'];symbol=F(phy['ofdm_symbol_seconds']);n=ceiling(F(nbits)/(rate*symbol))
 return F(phy['preamble_seconds'])+F(phy['signal_header_seconds'])+n*symbol+F(phy['signal_extension_seconds'])
extra=sum(layout[k] for k in ('ipv4_header_bytes','udp_header_bytes','llc_snap_bytes','data_mac_header_bytes','mac_fcs_bytes','security_overhead_bytes'))
data=layout['quic_packet_bytes']+extra;transport_ack=layout['quic_ack_packet_bytes']+extra;mac_ack=layout['normal_mac_ack_header_bytes']+layout['normal_mac_ack_fcs_bytes']
assert (data,transport_ack,mac_ack)==(1264,128,14)
td=ppdu(data,phy['data_rate_bps']);tq=ppdu(transport_ack,phy['data_rate_bps']);tm=ppdu(mac_ack,phy['mac_ack_rate_bps']);assert (td,tq,tm)==(F(208,1000000),F(40,1000000),F(44,1000000))
idle=F(access['pre_exchange_idle_seconds']);sifs=F(access['sifs_seconds']);assert idle==sifs+2*F(access['slot_seconds'])
assert td+idle+sifs+tm==F(302,1000000);assert tq+idle+sifs+tm==F(134,1000000)
assert F(access['source_rxstart_watchdog_seconds'])<sifs+tm and access['mac_ack_complete_timeout_seconds'] is None
h=json.loads((ROOT/'hand-oracles.json').read_text())['cases'];assert len(h)==5
assert h[0]['expected']['shared_intervals']==[[0,1],[1,2]]
assert 2*(F(1)+F(1,4))+2*F(1,2)==F(h[1]['expected']['immediate_total_seconds'])
assert 2*(F(1)+F(1,4))+F(1,2)==F(h[1]['expected']['every2_total_seconds'])
raw=F(3)-F(11,4);assert raw==F(h[2]['expected']['raw_delay_seconds']);assert raw/F(8,1000000)==h[2]['expected']['encoded_delay'];assert F(3)/F(8,1000000)==h[2]['variant_no_new_PN']['encoded_delay']
assert F(h[3]['given']['first_failure_known'])+F(h[3]['given']['retry_wait'])==2;assert h[3]['expected']['mac_attempt_pns']==[7,7]
e=h[4]['expected'];assert F(e['immediate_total_airtime'])==3*F(5,4)+3*F(1,2);assert F(e['every4_total_airtime'])==3*F(5,4)+2*F(1,2)
assert F(e['immediate_tail_complete'])<5<F(e['every4_tail_complete'])
for mode in ('immediate','every4'):
 for interval,arr in zip(e[mode+'_ACK_intervals'],e[mode+'_transport_ACK_receiver_arrivals']):assert F(interval[0])+F(1,4)==F(arr)<F(interval[1])
out=dict(status='PASS_INPUTS_ONLY_NOT_NETWORK_EXECUTION',verified_source_count=len(checks),source_files=checks,ns3_commit='43dce6710b8df69685e3479c1d33a571dda714ea',reference_arithmetic=dict(data_psdu_bytes=data,transport_ack_psdu_bytes=transport_ack,mac_ack_psdu_bytes=mac_ack,data_ppdu_seconds=str(td),transport_ack_ppdu_seconds=str(tq),mac_ack_ppdu_seconds=str(tm),data_exchange_seconds=str(td+idle+sifs+tm),transport_ack_exchange_seconds=str(tq+idle+sifs+tm)),hand_oracle_count=5,inputs_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ('profiles.json','hand-oracles.json','sources.lock.json')},scope='Official source identity and chosen-profile arithmetic verified; no compiled ns-3, standards conformance claim, MAC state execution or full media run.')
(ROOT/'check-result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
