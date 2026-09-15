"""Validate each state contract and summarize all measured outcomes."""
import hashlib
import json
from pathlib import Path
import statistics

R=Path(__file__).resolve().parent
reports=[]
for name in ['results']:
    out=R/name
    env=json.loads((out/'environment.json').read_text())
    for file,digest in env['source_hashes'].items():
        assert hashlib.sha256((R/file).read_bytes()).hexdigest()==digest,(name,file)
    assert json.loads((out/'cleanup.json').read_text())['remaining_containers']==[]
    assert json.loads((out/'completion.json').read_text())['count']==12
    cases=[json.loads(s) for s in (out/'cases.jsonl').read_text().splitlines()]
    ledger=[json.loads(s) for s in (out/'external-ledger.jsonl').read_text().splitlines()]
    assert len(cases)==12 and len({r['request']['request_id'] for r in ledger})==len(ledger)
    for r in ledger:
        assert r['start']<=r['end'] and r['request']['request_id']==r['response']['request_id']
    observations=[]
    for row in cases:
        creation=row['creation'];first=creation['first_tool']['response'];before=row['before']['response']
        assert first['counter']==0 and first['file_marker'] is None
        assert before['counter']==1 and before['memory_nonce']==first['memory_nonce']
        assert before['file_marker']['trial']==row['trial'] and before['file_marker']['path']==row['path']
        rec=dict(trial=row['trial'],path=row['path'],create_to_first_tool_s=creation['end']-creation['start'],
            create_api_s=creation['created']-creation['start'])
        if row['path']=='pause':
            after=row['after']['response']
            assert row['paused_inspect']['state']['Paused'] and row['same_connection']
            assert all(after[k]==before[k] for k in ['memory_nonce','counter','file_marker','hostname','pid'])
            rec.update(state_contract='same_memory_file_identity_and_connection',
                operation_api_s=row['unpause']['end']-row['unpause']['start'],
                operation_to_first_tool_s=row['after']['end']-row['unpause']['start'])
        elif row['path'] in ['clean_rebuild','filesystem']:
            after=row['after']['response']
            assert row['new_container']!=row['container'] and after['memory_nonce']!=before['memory_nonce']
            assert after['counter']==0
            assert after['file_marker']==(before['file_marker'] if row['path']=='filesystem' else None)
            rec.update(state_contract='file_only_new_memory' if row['path']=='filesystem' else 'clean_file_and_memory',
                operation_to_first_tool_s=row['recovery']['end']-row['recovery']['start'])
            if row['path']=='filesystem':
                assert all(row['original_after_commit']['response'][k]==before[k] for k in ['memory_nonce','counter','file_marker'])
                rec['save_api_s']=row['commit']['end']-row['commit']['start']
        else:
            assert all(row['original_after']['response'][k]==before[k] for k in ['memory_nonce','counter','file_marker'])
            assert row['checkpoint']['exit_code']==0 and len(row['derivatives'])==2
            assert len({d['container'] for d in row['derivatives']}|{row['container']})==3
            successes=[]
            for d in row['derivatives']:
                success=d['restore']['exit_code']==0
                successes.append(success)
                if success:
                    assert all(d['first_tool']['response'][k]==before[k] for k in ['memory_nonce','counter','file_marker'])
                    assert d['mutated']['response']['counter']>before['counter']
            assert successes==[True,True]
            assert len(row['derivatives_rechecked'])==2
            for i,(d,rechecked) in enumerate(zip(row['derivatives'],row['derivatives_rechecked'])):
                assert rechecked['container']==d['container']
                expected=before['counter']+i+10
                assert d['mutated']['response']['counter']==expected
                assert rechecked['state']['response']['counter']==expected
                assert rechecked['state']['response']['memory_nonce']==before['memory_nonce']
                assert rechecked['state']['response']['file_marker']==before['file_marker']
            rec.update(state_contract='checkpoint_two_independent_restores_verified',
                live_capture_exit_code=row['live_checkpoint']['exit_code'],
                capture_api_s=row['checkpoint']['end']-row['checkpoint']['start'],
                clone_restore_success=successes,restore_errors=[d['restore']['stderr'] for d in row['derivatives']],
                successful_restore_latency_s=None if not any(successes) else [d['first_tool']['end']-d['restore']['start'] for d in row['derivatives'] if d['restore']['exit_code']==0])
        observations.append(rec)
    for path in ['pause','clean_rebuild','filesystem','checkpoint']:
        assert sorted(r['trial'] for r in observations if r['path']==path)==[0,1,2]
    reports.append(dict(run=name,verified_cases=12,external_events=len(ledger),rows=observations,
        metrics=[dict(path=path,median_create_to_first_tool_s=statistics.median(r['create_to_first_tool_s'] for r in observations if r['path']==path),
            median_operation_to_first_tool_s=statistics.median(r['operation_to_first_tool_s'] for r in observations if r['path']==path) if path!='checkpoint' else None)
            for path in ['pause','clean_rebuild','filesystem','checkpoint']]))
summary=dict(status='measured_state_contracts_verified',author_substitution='Docker on rtx-pro instead of E2B',
    reports=reports,scope='12 cases in isolated Docker24/CRIU4.2.1, UNIX control; three checkpoint trials with two independently mutated and rechecked clones each; content-store retry intervention retained.',
    checkpoint_restore_complete=True)
(R/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='reports'},indent=2))
for report in reports:
    print(report['run'],json.dumps(report['metrics']))
