"""Explicitly seal five derived inputs; validate construction without advancing events."""
import copy
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CALC=ROOT.parent.parent
MEDIA=ROOT.parent/'media-feedback-loop'
RADIO=ROOT.parent/'shared-airtime-inputs'
LOOP=ROOT.parent/'shared-airtime-loop'
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):
    (ROOT/name).write_text(json.dumps(data,indent=2)+'\n')
def row(p,**metadata):
    return dict(file=os.path.relpath(p,ROOT),bytes=p.stat().st_size,sha256=sha(p),**metadata)
def verify_rows(base,rows):
    for r in rows:
        p=base/r['file']
        assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],str(p)
def main():
    for lock in ('run-book-inputs.lock.json','book-input-sources.lock.json'):
        verify_rows(MEDIA,json.loads((MEDIA/lock).read_text()))
    official=json.loads((RADIO/'sources.lock.json').read_text());verify_rows(RADIO,official)
    original=json.loads((MEDIA/'book-inputs.json').read_text())
    original['image-baseline']=json.loads((MEDIA/'image-baseline-inputs.json').read_text())
    profile=json.loads((RADIO/'profiles.json').read_text())['source_backed_reference_selection']
    assert profile['access']['mac_ack_complete_timeout_seconds'] is None
    spec=importlib.util.spec_from_file_location('airtime_book_validation',LOOP/'calculate.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    cases={};checks={}
    for name,base in original.items():
        assert 'wireless_access' not in base['network']
        p=copy.deepcopy(base)
        p['network']['wireless_access']=dict(enabled=True,profile=copy.deepcopy(profile),max_attempts=1,retry_wait='0',failures=[])
        restored=copy.deepcopy(p);del restored['network']['wireless_access'];assert restored==base
        assert p['network']['links']=={'up':{'rate_bps':20000000,'propagation':'0.05'},'down':{'rate_bps':100000000,'propagation':'0.05'}}
        module.Network(p) # Constructor validation only; no run/advance.
        messages=p['application']['messages'];counts={'up':0,'down':0};payload={'up':0,'down':0}
        for m in messages:
            d='up' if m['sender']=='client' else 'down'
            counts[d]+=m['packetization']['fragment_count'];payload[d]+=m['bytes']
        n=sum(counts.values())
        checks[name]=dict(changed_paths=['network.wireless_access'],all_other_fields_equal=True,links=p['network']['links'],until=p['network']['until'],declared_application_bytes=payload,declared_data_packets=counts,no_retry_all_declared_data_wire_bytes=n*1228,no_retry_all_declared_data_airtime_seconds=str(__import__('fractions').Fraction(n*302,1000000)),conditional_ack_wire_bounds=[0,n*92],conditional_ack_airtime_bounds_seconds=['0',str(__import__('fractions').Fraction(n*134,1000000))],accounting_scope='All declared data once. ACK upper bound applies only if no transport retries/probes/MAX and no duplicate-trigger ACK; actual deadline expiration/cancellation may reduce data. Not a completion prediction.')
        cases[name]=p
    write('book-inputs.json',cases)
    write('input-differences.json',dict(status='FIVE_CONSTRUCTORS_VALIDATED_NO_EVENTS_RUN',source_configuration_final=False,cases=checks))
    sourcepaths=[MEDIA/f for f in ('book-inputs.json','image-baseline-inputs.json','run-book-inputs.lock.json','book-input-sources.lock.json')]+[RADIO/'profiles.json',RADIO/'sources.lock.json',LOOP/'INTERFACE-CONTRACT.md']
    sources=[row(p) for p in sourcepaths]
    for r in official:
        sources.append(row(RADIO/r['file'],**{k:v for k,v in r.items() if k not in ('file','bytes','sha256')}))
    for r in json.loads((MEDIA/'book-input-sources.lock.json').read_text()):sources.append(row(MEDIA/r['file']))
    write('sources.lock.json',sources)
    # Broad package inventory deliberately includes validation and future helper modules.
    paths=set((CALC/'src/infra_calc').rglob('*.py'))|{LOOP/'calculate.py',LOOP/'airtime.py',ROOT/'prepare.py',ROOT/'run-book.py',CALC/'configs/sources.lock.json'}
    publiclock=json.loads((CALC/'configs/sources.lock.json').read_text())
    tree=ast.parse((CALC/'src/infra_calc/transport/reference_sources.py').read_text())
    for node in tree.body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SOURCE_FILES' for t in node.targets):
            for files in ast.literal_eval(node.value).values():paths.update(CALC/f for f in files)
    for r in publiclock['sources']:
        if r.get('revision')=='RFC9221':paths.add(CALC/r['file'])
    write('runtime.lock.json',[row(p) for p in sorted(paths)])
    write('inputs.lock.json',[row(ROOT/f) for f in ('book-inputs.json','input-differences.json','sources.lock.json','runtime.lock.json')])
    print('PASS: 5 exact single-field derivations; constructor validation only; no events advanced')
if __name__=='__main__':main()
