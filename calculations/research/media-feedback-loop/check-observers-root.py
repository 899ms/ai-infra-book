"""Business observation cutoff and local-version hand cases; no network trace."""
import copy
import hashlib
import json
from pathlib import Path
from fractions import Fraction as F
from application import Application

ROOT = Path(__file__).resolve().parent
apps = json.loads((ROOT.parent/'media-feedback-inputs/normalized-inputs.json').read_text())
checks = []

def observe(app, completed, until):
    actor = Application(app, lambda *args: None, lambda *args: None, lambda: F(0))
    actor.completed = {key:F(value) for key,value in completed.items()}
    return actor.observers(F(until))

screen = next(copy.deepcopy(a) for a in apps.values() if any(o['kind']=='screenshot' for o in a['business_observers']))
o = next(o for o in screen['business_observers'] if o['kind']=='screenshot')
o['version_changes'] = [dict(endpoint=o['endpoint'],at_seconds='2',version='v2'),dict(endpoint=o['endpoint'],at_seconds='1',version=o['version'])]
received = {dep['id']:'3' for dep in o['completion_dependencies']}
row = next(r for r in observe(screen,received,'5') if r['id']==o['id'])
checks.append(dict(case='version selected chronologically at actual result',passed=row['version_at_result']=='v2' and row['usable'] is False,observed=row))

audio = next(copy.deepcopy(a) for a in apps.values() if any(o['kind']=='tts' and o['playback']=='reliable' for o in a['business_observers']))
o = next(o for o in audio['business_observers'] if o['kind']=='tts')
for i,block in enumerate(o['blocks']):
    block['slot_start_seconds']=str(10+i*2)
    block['duration_seconds']='2'
received = {identity:'1' for block in o['blocks'] for identity in block['message_ids']}
row = next(r for r in observe(audio,received,'5') if r['id']==o['id'])
checks.append(dict(case='future reliable playback is not an observed first play',passed=row['first_play'] is None and row['complete'] is False,observed=row))
report={'status':'passed' if all(c['passed'] for c in checks) else 'failed','checks':checks,'application_sha256':hashlib.sha256((ROOT/'application.py').read_bytes()).hexdigest(),'scope':'Local observation contract only; no claim that network generated these delivery events'}
path=ROOT/'observer-root-check.json'
if path.exists() and json.loads(path.read_text())['status']=='failed':
    archive=ROOT/'observer-root-check-before-fix.json'
    if not archive.exists():archive.write_bytes(path.read_bytes())
path.write_text(json.dumps(report,indent=2)+'\n')
print(report['status'], [(c['case'],c['passed']) for c in checks])
raise SystemExit(report['status']!='passed')
