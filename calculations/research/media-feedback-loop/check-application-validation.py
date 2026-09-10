"""Preflight acceptance and rejection cases, with failure atomicity checks."""
import copy
import hashlib
import json
from pathlib import Path
from application_validation import validate_application

ROOT = Path(__file__).resolve().parent
INPUT = ROOT.parent / 'media-feedback-inputs/normalized-inputs.json'
applications = json.loads(INPUT.read_text())
checks = []
for name, application in applications.items():
    before = copy.deepcopy(application)
    validate_application(application)
    assert application == before
    checks.append({'case': name, 'result': 'accepted unchanged'})

base = applications['hol-connection']

def reject(name, mutate):
    candidate = copy.deepcopy(base)
    mutate(candidate)
    before = copy.deepcopy(candidate)
    try:
        validate_application(candidate)
    except ValueError as error:
        assert candidate == before
        checks.append({'case': name, 'result': 'rejected unchanged', 'reason': str(error)})
    else:
        raise AssertionError(name)

reject('duplicate identity', lambda a: a['messages'][1].update(id='B0'))
reject('same endpoint', lambda a: a['messages'][0].update(receiver='client'))
reject('overlapping stream messages', lambda a: a['messages'][2].update(stream_offset=0))
reject('reliable silent expiry', lambda a: a['messages'][0].update(allow_expire=True))
reject('boolean bytes', lambda a: a['messages'][0].update(bytes=True))
reject('negative ready', lambda a: a['messages'][0].update(ready_seconds='-1'))
reject('nonfinite deadline', lambda a: a['messages'][0].update(deadline_seconds='nan'))
reject('false fragmentation metadata', lambda a: a['messages'][0]['packetization'].update(fragment_count=2))
reject('unknown dependency', lambda a: a['messages'][0].update(dependencies=[{'id':'missing','event':'message_delivered','endpoint':'client'}]))
reject('remote delivery used locally', lambda a: a['messages'][2].update(dependencies=[{'id':'B0','event':'message_delivered','endpoint':'server'}]))
reject('false local delivery', lambda a: a['messages'][2].update(dependencies=[{'id':'B0','event':'message_delivered','endpoint':'client'}]))
reject('datagram stream offset', lambda a: a['messages'][0].update(transport='datagram'))

def oversized(a):
    a['messages'][0].update(transport='datagram', stream_offset=None, bytes=1169)
    a['messages'][0]['packetization'].update(fragment_count=2, final_fragment_bytes=1)
reject('datagram cannot silently fragment', oversized)

def cycle(a):
    a['messages'] = []
    a['business_observers'] = []
    a['compute_tasks'] = [dict(id=identity, endpoint='server', resource='gpu', duration_seconds='1', ready_seconds='0', source_order=i, priority=0, dependencies=[dict(id=dependency, event='task_completed', endpoint='server')]) for i,(identity,dependency) in enumerate([('a','b'),('b','a')])]
reject('local compute dependency cycle', cycle)

reject('unsupported compute preemption', lambda a: a['scheduling'].update(compute_nonpreemptive=False))
reject('unsupported compute capacity', lambda a: a['scheduling'].update(resource_capacity_tasks=2))
reject('unknown send scheduler', lambda a: a['scheduling'].update(send='magic'))
reject('future remote version shortcut', lambda a: a['business_observers'][0].update(version_changes=[{'endpoint':'client','at_seconds':'1','version':'v2'}]))

# A missing STREAM prefix is a runtime incompleteness case, not malformed input.
gap = copy.deepcopy(base)
gap['messages'][2]['stream_offset'] = 3
validate_application(gap)
checks.append({'case':'reliable gap remains allowed, never assumed delivered', 'result':'accepted'})
report = {'status':'passed','checks':checks,'input_sha256':hashlib.sha256(INPUT.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((ROOT/'application_validation.py').read_bytes()).hexdigest(),'scope':'Input causality and shape only; no network or business completion claim'}
(ROOT/'application-validation-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'{len(checks)} preflight checks passed')
