"""Static bounded retry contract and arithmetic, no network/policy execution."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parent
cases=['mixed-fifo-immediate','mixed-fifo-aggregate','mixed-priority-immediate','mixed-priority-aggregate']
old=[];files={}
for name in cases:
 p=RESEARCH/f'media-feedback-loop/runs/book-{name}-summary.json'
 r=json.loads(p.read_text());b=next(x for x in r['businesses'] if x['kind']=='screenshot')
 assert b['complete'] is False and b['complete_at'] is None and b['usable'] is False
 assert 'screen-action' in b['missing']
 old.append({'case':name,'screenshot_business':b})
 files[str(p.relative_to(RESEARCH))]=hashlib.sha256(p.read_bytes()).hexdigest()
# A predeclared two-slot policy template; retry nodes are dormant until client
# receives a real server rejection and chooses the single allowed retry.
contract={'status':'STATIC_INPUT_CONTRACT_NOT_CURRENT_ENGINE_EXECUTION',
 'max_retries':1,'initial_client_version':'v0','client_version_changes':[{'at':'1','version':'v1'}],
 'transport_hand_assumptions':{'up_application_bytes_per_second':3443,'down_application_bytes_per_second':32,
 'propagation_seconds':'0','packet_headers_ACK_cwnd_recovery':'excluded from this application-level hand oracle; real network must determine actual delivery later',
 'scope':'two directional nonpreemptive FIFO byte servers, not the shared radio engine'},
 'policy':{'initial_attempt':0,'retry_trigger':'failure-notice-0 message delivered to client AND retry_count<1',
 'capture_version':'read client current version only when retry capture starts',
 'server_rejection':'after old nonpreemptive task completes compare captured version with latest actual delivered client version notification',
 'client_action_commit':'only if action.attempt is active and action.version equals local version at receipt; otherwise locally reject',
 'deduplication':'attempt token and notice ID consumed once; duplicate delivery cannot create another retry',
 'retry_exhaustion':'terminal failure after attempt1 rejection; no implicit attempt2'},
 'message_templates':[
 {'id':'screen-0','sender':'client','receiver':'server','bytes':3443,'transport':'stream','flow':'screen-0','version':'v0','attempt':0,'ready':'0'},
 {'id':'version-notice','sender':'client','receiver':'server','bytes':32,'transport':'stream','flow':'control','version':'v1','ready':'1'},
 {'id':'failure-notice-0','sender':'server','receiver':'client','bytes':32,'transport':'stream','flow':'status','attempt':0,'ready_event':'server task0 end with stale version'},
 {'id':'screen-1','sender':'client','receiver':'server','bytes':3443,'transport':'stream','flow':'screen-1','version':'capture-time local version','attempt':1,'ready_event':'client capture1 end after actual failure-notice-0 delivery'},
 {'id':'action-1','sender':'server','receiver':'client','bytes':32,'transport':'stream','flow':'action','attempt':1,'version':'v1','ready_event':'server task1 end with matching delivered version'}],
 'tasks':[{'id':'server-work-0','endpoint':'server','duration_seconds':'2','nonpreemptive':True,'dependencies':['screen-0 delivered'],'operator_fixture':'vision_decision'},
 {'id':'client-capture-1','endpoint':'client','duration_seconds':'1/2','nonpreemptive':True,'dependencies':['failure-notice-0 delivered'],'matrix_flops':None,'scope':'capture/PNG work unmodeled; do not report zero total compute'},
 {'id':'server-work-1','endpoint':'server','duration_seconds':'2','nonpreemptive':True,'dependencies':['screen-1 delivered'],'operator_fixture':'vision_decision'}],
 'operator_fixture':{'identity':'tiny declared matrix-work fixture, not a real VL model and not inferred from PNG bytes',
 'operations':[{'name':'feature_projection','M':8,'K':16,'N':8,'flops':2*8*16*8},
 {'name':'action_projection','M':1,'K':8,'N':4,'flops':2*1*8*4}],
 'per_attempt_matrix_flops':2112,'failed_work_reused':False,
 'excluded':'PNG decode, preprocessing, real vision encoder, full attention/MLP, nonmatmul operators; plug separately verified VL operator ledger into task work_ref before any real-model claim'}}
version_received=1+F(32,3443)
assert 1 < version_received < 3
expected={'status':'PREWRITTEN_HAND_ARITHMETIC_NOT_CANDIDATE_OUTPUT',
 'events':[{'at':'0','event':'screen0 upload begins'}, {'at':'1','event':'screen0 server delivery and nonpreemptive work0 starts; client version changes and sends real version notice'},
 {'at':str(version_received),'event':'server receives actual version notice; work0 continues'},
 {'at':'3','event':'work0 ends, server emits stale failure notice'},
 {'at':'4','event':'client actually receives failure notice; sole retry capture starts'},
 {'at':'9/2','event':'capture ends; screen1 uploads'},
 {'at':'11/2','event':'screen1 server delivery; work1 starts'},
 {'at':'15/2','event':'work1 ends; action1 sends'},
 {'at':'17/2','event':'client receives matching v1 action and commits'}],
 'up_application_bytes':2*3443+32,'down_application_bytes':2*32,'total_application_bytes':2*3443+96,
 'one_attempt_no_failure_reference_bytes':3443+32,
 'incremental_bytes_vs_one_attempt_no_failure_reference':3443+64,
 'server_work_seconds':'4','client_retry_capture_seconds':'1/2','matrix_flops_per_attempt':2112,
 'wasted_old_attempt_matrix_flops':2112,'total_matrix_flops':4224,'valid_action_time_seconds':'17/2',
 'variants':[{'id':'drop-failure-notice-before-horizon','expected':'No retry begins before actual notice delivery; do not seed a retry at4 if transport has not delivered it.'},
 {'id':'duplicate-failure-notice','expected':'At most one capture1; duplicate notice consumes no new retry budget.'},
 {'id':'version-changes-to-v2-before-action1','expected':'Client rejects action1 locally; retry budget exhausted, terminal failure, no attempt2.'},
 {'id':'version-notice-arrives-after-work0','expected':'Server cannot use future v1 knowledge at work0 completion. Client independently rejects a mismatching v0 action; a separately specified policy branch is needed.'}]}
for name,data in [('contract.json',contract),('hand-oracles.json',expected),('old-four-case-causes.json',old)]:
 (HERE/name).write_text(json.dumps(data,indent=2)+'\n')
files['screenshot-version-retry-inputs/build.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(HERE/'inputs.lock.json').write_text(json.dumps({'files':files,'outputs':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in ['contract.json','hand-oracles.json','old-four-case-causes.json']}},indent=2)+'\n')
print('PASS static byte/matrix/time hand arithmetic; read four real failure summaries; no network execution')
if __name__=='__main__':pass
