"""Static migration proof and actual public execution against sealed full traces."""
from pathlib import Path
import ast, copy, gc, importlib.util, json, sys, time
ROOT=Path(__file__).resolve().parent
CALC=ROOT.parent.parent
PROJECT=CALC.parent
RESEARCH=ROOT.parent/'media-feedback-loop'
sys.path.insert(0,str(CALC/'src'))
from infra_calc.topics import transport_closed_loop as topic, transport_sender
from infra_calc.transport import media_network,media_sender,ack_receiver,pacer
spec=importlib.util.spec_from_file_location('comparison',ROOT.parent/'transport-controller-loop/integration/check-network-public.py')
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
def hashes():
    files=list((CALC/'src/infra_calc/transport').glob('*.py'))
    files += [CALC/'src/infra_calc/topics'/n for n in ('transport_closed_loop.py','transport_sender.py')]
    files += [RESEARCH/n for n in ('calculate.py','application.py','application_validation.py','network_validation.py','sender.py')]
    return {str(p.relative_to(PROJECT)):helper.filehash(p) for p in sorted(files)}
def tree(path):return ast.parse(path.read_text())
def dump(node):return ast.dump(node,include_attributes=False)
def named(path):return {n.name:n for n in tree(path).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def static_check():
    pub=CALC/'src/infra_calc/transport'
    for n in ('application','application_validation','network_validation'):
        assert (RESEARCH/(n+'.py')).read_bytes()==(pub/('media_'+n+'.py')).read_bytes()
    old=named(RESEARCH/'calculate.py');new=named(pub/'media_network.py')
    assert set(new)==set(old)-{'main','local_module'}
    for n in new:assert dump(old[n])==dump(new[n]),n
    a=named(RESEARCH/'sender.py');b=named(pub/'media_sender.py')
    assert dump(a['retransmittable_frames'])==dump(b['retransmittable_frames'])
    a['create_sender'].body=a['create_sender'].body[1:]
    assert dump(a['create_sender'])==dump(b['create_sender'])
    a=tree(ROOT/'transport_closed_loop.before.py.txt');b=tree(CALC/'src/infra_calc/topics/transport_closed_loop.py')
    fn=next(n for n in b.body if isinstance(n,ast.FunctionDef) and n.name=='calculate')
    assert isinstance(fn.body[0],ast.If)
    fn.body=fn.body[1:]
    assert dump(a)==dump(b),'topic changed beyond added dispatch'
    assert media_network.sender is media_sender and media_sender._public is transport_sender
    assert media_network.Receiver is ack_receiver.Receiver and media_network.Pacer is pacer.Pacer
    for p in ({'application':{}},{'network':{}},{'application':{},'network':{},'upload_bytes':1}):
        try:topic.calculate(p)
        except ValueError:pass
        else:raise AssertionError('outer dispatch accepted ambiguous input')
    return {'exact_modules':3,'network_math_functions_and_classes':list(new),'topic_only_change':'strict initial media dispatch','sender_change':'remove research dependency verifier; same public delegate','static_bindings':'passed','strict_outer_rejections':3}
def main():
    before=hashes();static=static_check();checks=[]
    mapping=json.loads((ROOT/'scenario-mapping.json').read_text())
    registered={r['id']:r['inputs'] for r in json.loads((CALC/'scenarios/book.json').read_text())['transport_closed_loop']}
    smallpath=RESEARCH/'result.json';small=json.loads(smallpath.read_text())
    sm=json.loads((RESEARCH/'result-manifest.json').read_text())
    assert helper.filehash(smallpath)==sm['result_sha256']
    for name in ('calculate.py','application.py','application_validation.py','network_validation.py','sender.py'):
        assert helper.filehash(RESEARCH/name)==sm['code_hashes'][name]
    def record(name,actual,elapsed,count,path):
        assert hashes()==before,'runtime source drift'
        checks.append(dict(scenario=name,public_id=mapping[name],status='passed',elapsed_seconds=elapsed,compared=count,transmissions=len(actual['transmissions']),summary=actual['summary'],reference_file=str(path.relative_to(PROJECT)),reference_sha256=helper.filehash(path)))
        (ROOT/'public-check.partial.json').write_text(json.dumps(dict(checks=checks,code_hashes=before),indent=2)+'\n')
        print(name+': complete math passed',flush=True)
    for name,expected in small.items():
        inputs=registered[mapping[name]];assert inputs==expected['inputs']
        start=time.monotonic();actual=topic.calculate(inputs)
        for key in helper.EXCLUDED:actual.pop(key,None);expected.pop(key,None)
        assert json.dumps(actual,sort_keys=True)==json.dumps(expected,sort_keys=True),name
        record(name,actual,time.monotonic()-start,{'mode':'complete typed JSON equality'},smallpath)
        del actual
    del small;gc.collect()
    for name in mapping:
        if name in ('image-baseline','mixed-fifo-immediate','mixed-fifo-aggregate','mixed-priority-immediate','mixed-priority-aggregate'):
            manifestpath=RESEARCH/f'runs/book-{name}-manifest.json'
            manifest=json.loads(manifestpath.read_text());path=RESEARCH/manifest['result_file']
            assert manifest['source_hashes_before']==manifest['source_hashes_after']
            assert 'research/media-feedback-loop/network_validation.py' in manifest['source_hashes_before']
            for filename,digest in manifest['source_hashes_before'].items():assert helper.filehash(CALC/filename)==digest,filename
            assert helper.filehash(path)==manifest['result_sha256']
            start=time.monotonic();actual=topic.calculate(registered[mapping[name]])
            reader=helper.Reader(path);count={'scalars':0,'list_items':0}
            helper.compare(reader,actual,(),count);reader.white();assert reader.eof;reader.f.close()
            assert helper.filehash(path)==manifest['result_sha256']
            record(name,actual,time.monotonic()-start,count,path)
            checks[-1]['reference_manifest_sha256']=helper.filehash(manifestpath)
            del actual;gc.collect()
    assert len(checks)==19 and before==hashes()
    (ROOT/'public-check.json').write_text(json.dumps(dict(status='passed',cases=19,excluded_fields=sorted(helper.EXCLUDED),static_migration=static,checks=checks,code_hashes=before,checker_sha256=helper.filehash(Path(__file__))),indent=2)+'\n')
if __name__=='__main__':main()
