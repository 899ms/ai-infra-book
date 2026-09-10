"""One sealed media case per process; full traces, guarded inputs and source identity."""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent.parent
CASES=('mixed-fifo-immediate','mixed-fifo-aggregate','mixed-priority-immediate','mixed-priority-aggregate','image-baseline')

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while data:=f.read(1048576):h.update(data)
    return h.hexdigest()

def verify_inputs():
    rows=json.loads((ROOT/'run-book-inputs.lock.json').read_text())
    for row in rows:
        p=ROOT/row['file']
        if p.stat().st_size!=row['bytes'] or digest(p)!=row['sha256']:raise ValueError('sealed book input changed: '+row['file'])
    for lock in ('book-input-sources.lock.json',):
        for row in json.loads((ROOT/lock).read_text()):
            p=ROOT/row['file']
            if p.stat().st_size!=row['bytes'] or digest(p)!=row['sha256']:raise ValueError('normalized input source changed: '+row['file'])
    return {row['file']:row['sha256'] for row in rows}

def runtime_hashes():
    paths=[ROOT/f for f in ('calculate.py','application.py','application_validation.py','network_validation.py','sender.py','run-book.py','sender-dependencies.lock.json','run-book-inputs.lock.json')]
    for row in json.loads((ROOT/'sender-dependencies.lock.json').read_text()):
        p=PROJECT/row['file']
        if p.stat().st_size!=row['bytes'] or digest(p)!=row['sha256']:raise ValueError('frozen sender dependency changed: '+row['file'])
        paths.append(p)
    tree=ast.parse((PROJECT/'src/infra_calc/transport/reference_sources.py').read_text())
    for node in tree.body:
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SOURCE_FILES' for t in node.targets):
            for files in ast.literal_eval(node.value).values():paths.extend(PROJECT/f for f in files)
    for row in json.loads((PROJECT/'configs/sources.lock.json').read_text())['sources']:
        if row.get('revision')=='RFC9221':paths.append(PROJECT/row['file'])
    return {str(p.resolve().relative_to(PROJECT.resolve())):digest(p) for p in sorted(set(paths))}

def pilot(base):
    p=copy.deepcopy(base);app=p['application'];ends={};totals={'client_to_server':0,'server_to_client':0};count=0
    for m in app['messages']:
        if m['transport']!='stream' or m['bytes']!=25000:raise ValueError('pilot only supports original image 25KB block DAG')
        key=(m['sender'],m['flow_id']);m['bytes']=250;m['stream_offset']=ends.get(key,0);m['application_offset']=m['stream_offset'];ends[key]=m['stream_offset']+250
        m['packetization'].update(fragment_count=1,final_fragment_bytes=250)
        totals['client_to_server' if m['sender']=='client' else 'server_to_client']+=250;count+=1
    app['id']='image-pilot-300kb-50kb'
    app['accounting'].update(application_bytes_by_direction=totals,application_bytes=sum(totals.values()),fragment_count=count)
    p['network']['initial_max_stream_data']={d:{} for d in ('up','down')}
    for (origin,flow),end in ends.items():p['network']['initial_max_stream_data']['up' if origin=='client' else 'down'][flow]=end
    assert totals=={'client_to_server':300000,'server_to_client':50000}
    return p

def run(case,small=False):
    if small and case!='image-baseline':raise ValueError('--pilot only permits image-baseline; mixed deadlines are not rescaled')
    locked=verify_inputs();before=runtime_hashes();started=time.monotonic()
    base=json.loads((ROOT/'image-baseline-inputs.json').read_text()) if case=='image-baseline' else json.loads((ROOT/'book-inputs.json').read_text())[case]
    inputs=pilot(base) if small else base
    label='pilot-image-300kb-50kb' if small else 'book-'+case
    folder=ROOT/'runs';folder.mkdir(exist_ok=True)
    effective=folder/(label+'-inputs.json');effective.write_text(json.dumps(inputs,indent=2)+'\n')
    spec=importlib.util.spec_from_file_location('media_runner_candidate',ROOT/'calculate.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    manifest=dict(status='running',case=case,pilot=small,workload_label=('REDUCED 300KB upload / 50KB response; not original book workload' if small else 'Full sealed book case'),inputs_lock=locked,source_hashes_before=before,effective_input_file=str(effective.relative_to(ROOT)),effective_input_sha256=digest(effective))
    mpath=folder/(label+'-manifest.json');partial=folder/(label+'-result.partial.json')
    mpath.write_text(json.dumps(manifest,indent=2)+'\n')
    try:
        result=module.calculate(inputs)
        with partial.open('w') as f:json.dump(result,f,indent=2);f.write('\n')
        after=runtime_hashes();newlocked=verify_inputs()
        manifest.update(source_hashes_after=after,elapsed_seconds=round(time.monotonic()-started,6),result_sha256=digest(partial),result_bytes=partial.stat().st_size)
        if after!=before or newlocked!=locked:
            manifest.update(status='REJECTED_SOURCE_OR_INPUT_DRIFT',result_file=str(partial.relative_to(ROOT)))
            raise RuntimeError('source/input identity changed; result not accepted')
        target=folder/(label+'-result.json');partial.replace(target)
        summary=dict(case=case,pilot=small,workload_label=manifest['workload_label'],summary=result.get('summary'),businesses=result.get('businesses'),transmission_count=len(result['transmissions']),effective_input_sha256=manifest['effective_input_sha256'],result_sha256=manifest['result_sha256'])
        spath=folder/(label+'-summary.json');spath.write_text(json.dumps(summary,indent=2)+'\n')
        manifest.update(status='COMPLETE_STABLE_IDENTITY_NOT_INDEPENDENT_ACCEPTANCE',result_file=str(target.relative_to(ROOT)),summary_file=str(spath.relative_to(ROOT)),summary_sha256=digest(spath))
    except Exception as error:
        try:manifest.setdefault('source_hashes_after',runtime_hashes())
        except Exception as identity_error:manifest['source_recheck_error']=type(identity_error).__name__+': '+str(identity_error)
        if manifest['status']=='running':manifest['status']='FAILED'
        manifest.update(error=type(error).__name__+': '+str(error),elapsed_seconds=round(time.monotonic()-started,6))
        mpath.write_text(json.dumps(manifest,indent=2)+'\n');raise
    mpath.write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(dict(status=manifest['status'],pilot=small,manifest=str(mpath.relative_to(ROOT)),elapsed_seconds=manifest['elapsed_seconds'],transmission_count=len(result['transmissions']))))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--case',required=True,choices=CASES);parser.add_argument('--pilot',action='store_true');args=parser.parse_args();run(args.case,args.pilot)
