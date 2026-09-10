"""Prewritten small network inputs; no candidate execution or outcome fitting."""
from pathlib import Path
import copy,json,hashlib,importlib.util
from fractions import Fraction as F
from scenario_helpers import message,application,dependency,complete_observer,teaching_network
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'shared-airtime-inputs/profiles.json'
profiles=json.loads(SOURCE.read_text());profile=profiles['abstract_teaching_profile']

def inputs(app,*,ack='immediate_each_packet',cwnd=2400,until=14,failures=()):
    n=teaching_network(app,until=until,cwnd=cwnd,ack_policy=ack)
    n['wireless_access']=dict(enabled=True,profile=copy.deepcopy(profile),max_attempts=2,retry_wait='1/2',failures=list(failures))
    return dict(application=app,network=n)
def policy(every,delay):return dict(mode='count_or_timer',every=every,max_delay=str(delay),delay_exponent=3,retain_packets=256,reorder_immediate=True,header_tag_bytes=24)
def three_up():
    messages=[message(f'd{i}',flow='file',offset=i) for i in range(3)]
    audio=dict(id='tail-audio-slot',kind='tts',endpoint='server',completion_dependencies=[dependency('d2','server')],version_changes=[],playback='slots',blocks=[dict(message_ids=['d2'],duration_seconds='1/4',slot_start_seconds='6')])
    return application('three-up-same-ready',messages,[complete_observer('file',['d0','d1','d2']),audio])

cases={}
both=application('both-directions',[message('u'),message('d',sender='server')],[complete_observer('up-complete',['u']),complete_observer('down-complete',['d'],endpoint='client')])
cases['bidirectional-shared']=inputs(both)
cases['bidirectional-disabled']=copy.deepcopy(cases['bidirectional-shared']);cases['bidirectional-disabled']['network']['wireless_access']['enabled']=False
pair=application('two-up',[message('d0',flow='file'),message('d1',flow='file',offset=1)],[complete_observer('file',['d0','d1'])])
cases['two-data-immediate']=inputs(pair)
cases['two-data-every2']=inputs(pair,ack=policy(2,4))
for label,delay in [('busy-client-ACK-refresh','1/4'),('busy-client-ACK-overrun','1/10')]:
    down=application('three-down',[message(f'd{i}',sender='server',flow='down',offset=i) for i in range(3)],[complete_observer('download',['d0','d1','d2'],endpoint='client')])
    cases[label]=inputs(down,ack=policy(2,delay),cwnd=4800)
one=application('one-up',[message('d0')],[complete_observer('file',['d0'])])
cases['same-PN-MAC-ACK-lost']=inputs(one,failures=[dict(direction='up',pn=0,attempt=1,outcome='mac_ack_lost')])
cases['MAC-data-loss-exhaustion-then-PTO']=inputs(one,failures=[dict(direction='up',pn=0,attempt=a,outcome='data_lost') for a in (1,2)])
cases['MAC-data-loss-exhaustion-then-PTO']['network']['sender']={'initial_rtt':'4/3'}
cases['tail-immediate']=inputs(three_up())
cases['tail-every4']=inputs(three_up(),ack=policy(4,4))
# Application schema only: no network engine, airtime execution or modeled timing.
spec=importlib.util.spec_from_file_location('application_preflight',ROOT.parent/'media-feedback-loop/application_validation.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
for p in cases.values():v.validate_application(p['application'])
for name in ('tail-immediate','tail-every4'):
    assert sum(m['bytes'] for m in cases[name]['application']['messages'])==3
left=copy.deepcopy(cases['tail-immediate']);right=copy.deepcopy(cases['tail-every4']);left['network'].pop('ack_policy');right['network'].pop('ack_policy');assert left==right
(ROOT/'scenarios.json').write_text(json.dumps(cases,indent=2)+'\n')
a=F(23,307)
expected={
 'bidirectional-shared':dict(first_up_air_exchange=['0','5/4'],first_down_WAN=['0','1'],first_down_AP_ready='1',first_down_air_exchange=['5/4','5/2'],up_server_delivery='2',down_client_delivery='9/4'),
 'bidirectional-disabled':dict(first_up_WAN=['0','1'],first_down_WAN=['0','1'],up_server_delivery='1',down_client_delivery='1',scope='Exact existing public disabled result must be compared separately; no radio timeline exists.'),
 'two-data-immediate':dict(data_MAC_confirmation_count=2,transport_ACK_count=2,total_success_airtime='7/2'),
 'two-data-every2':dict(data_MAC_confirmation_count=2,transport_ACK_count=1,total_success_airtime='3'),
 'busy-client-ACK-refresh':dict(first_down_air_exchange=['1','9/4'],second_down_air_exchange=['9/4','7/2'],first_client_ACK_deadline='9/4',first_client_ACK_air_start='7/2',first_client_ACK_ranges=[[0,1]],largest_received_at='13/4',raw_delay='1/4',encoded_delay=31250,exceeds_max_delay=False),
 'busy-client-ACK-overrun':dict(first_client_ACK_deadline='21/10',first_client_ACK_air_start='7/2',first_client_ACK_ranges=[[0,1]],largest_received_at='13/4',raw_delay='1/4',encoded_delay=31250,exceeds_max_delay=True),
 'same-PN-MAC-ACK-lost':dict(up_MAC_attempt_PNs=[0,0],up_DATA_air_intervals=[['0','1'],['2','3']],first_AP_receive='1',failure_known='3/2',retry_MAC_success='13/4',up_original_sender_sent_events=1,up_WAN_forward_count=1,server_unique_delivery='2'),
 'MAC-data-loss-exhaustion-then-PTO':dict(original_MAC_attempt_PNs=[0,0],failures_known=['3/2','7/2'],end_to_end_PTO='4',probe_new_PN=1,probe_air_DATA_interval=['4','5'],server_unique_delivery='6',scope='Both original MAC attempts lose DATA; no early receiver delivery/transportACK can cancel the declared PTO. PTO itself is not loss or cwnd decrease.'),
 'tail-immediate':dict(initial_cwnd_bytes=2400,server_tail_delivery='5',tail_slot_usable=True,tail_play_start='6',tail_play_end='25/4',total_success_airtime='21/4',transport_ACK_count=3),
 'tail-every4':dict(first_two_server_arrivals=['2','13/4'],first_server_ACK_deadline='6',first_ACK_AP_ready=str(6+a),first_ACK_client_receive=str(F(25,4)+a),third_DATA_air_start=str(F(13,2)+a),server_tail_delivery=str(F(17,2)+a),tail_slot_usable=False,missing_audio_seconds='1/4',total_success_airtime='19/4',transport_ACK_count=2)
}
(ROOT/'network-hand-oracles.json').write_text(json.dumps(dict(status='PREWRITTEN_NOT_EXECUTED',scope='Finite-WAN refinement of five prior local service oracles, derived before network output. Source profile remains under independent review.',alpha_WAN_ACK_seconds=str(a),cases=expected),indent=2)+'\n')
local=ROOT.parent/'shared-airtime-inputs/hand-oracles.json'
(ROOT/'local-service-oracles.json').write_bytes(local.read_bytes())
(ROOT/'scenarios-metadata.json').write_text(json.dumps(dict(status='APPLICATION_SCHEMA_VALIDATED_NETWORK_NOT_RUN',source_profile_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),prior_local_oracles_sha256=hashlib.sha256(local.read_bytes()).hexdigest(),scenario_count=len(cases),source_configuration_final=False),indent=2)+'\n')
print('prepared',len(cases),'network inputs; application schema PASS; no network run')
