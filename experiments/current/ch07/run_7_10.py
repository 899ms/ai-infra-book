"""Dependency scheduling with separate transport and consumption lifetimes."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('07-*.md'))
duration=dict(write=20,recovery=80,notify=2,C=50,consume=30)
rows=[]
for serial in (True,False):
 dependencies=dict(write=[],recovery=['write'],notify=['recovery'],C=['notify'] if serial else [],consume=['notify'])
 events={}
 for name in duration:
  start=max([events[p]['end_us'] for p in dependencies[name]] or [0]);events[name]=dict(start_us=start,end_us=start+duration[name],depends_on=dependencies[name])
 for name,event in events.items():assert all(events[p]['end_us']<=event['start_us'] for p in dependencies[name])
 rows.append(dict(schedule='serial_ABC' if serial else 'only_A_to_B',events=events,ABC_complete_us=max(events[n]['end_us'] for n in ('write','recovery','notify','C')),C_complete_us=events['C']['end_us'],destination_D_reusable_us=events['consume']['end_us'],including_consumer_complete_us=max(e['end_us'] for e in events.values())))
# Version changes at 2us; ready flag becomes visible at 3us.
value=lambda t: int(t>=2)
stale=value(1);flag_seen=4>=3;assert flag_seen and stale==0 and value(4)==1
paths=[dict(name='incorrect_delayed_return',read_us=1,flag_read_us=4,return_us=5,value=stale),dict(name='wait_then_read',flag_read_us=4,read_start_us=4,read_complete_us=6,value=value(4)),dict(name='speculate_validate_reread',early_read_us=1,early_value=stale,flag_and_conflict_check_us=4,reread_start_us=4,reread_complete_us=6,value=value(4))]
out=dict(exercise='7-10',schedules=rows,stale_paths=paths,scope='Deterministic dependency model with independent C resources and 2us read duration in corrected paths; notification is not consumption completion',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'7-10-results.json').write_text(json.dumps(out,indent=2)+'\n');print([(r['schedule'],r['ABC_complete_us'],r['C_complete_us'],r['destination_D_reusable_us']) for r in rows])
