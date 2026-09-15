import hashlib
import json
from pathlib import Path

R = Path(__file__).resolve().parent
OUT = R/'results'
environment = json.loads((OUT/'environment.json').read_text())
for source, digest in environment['source_sha256'].items():
    path = Path(source)
    if path.name == 'inference.py':
        local_source = R/'sources/semantic-inference.py'
    elif path.name == 'config.json':
        local_source = R/'sources/checkpoint-config.json'
    elif path.name == 'server.py':
        local_source = R/'sources/server.py'
    else:
        local_source = R/path.name
    assert hashlib.sha256(local_source.read_bytes()).hexdigest() == digest, source
requests = json.loads((OUT/'requests.json').read_text())
events = [json.loads(line) for line in (OUT/'events.jsonl').read_text().splitlines()]
assert len(requests) == 7
assert json.loads((OUT/'completion.json').read_text()) == dict(completed=7, expected=7)
rows = []
for request in requests:
    rid = request['request']['request_id']
    trace = [e for e in events if e['request_id']==rid]
    assert all(a['time_ns']<=b['time_ns'] for a,b in zip(trace,trace[1:]))
    assert request['semantic_terminal_observed'] and request['handler_exit_observed']
    body = (OUT/f'{rid}.wav').read_bytes()
    assert len(body)==request['bytes'] and hashlib.sha256(body).hexdigest()==request['sha256']
    assert body[:4]==b'RIFF' and body[8:12]==b'WAVE' and body[36:40]==b'data'
    def one(name):
        selected = [e for e in trace if e['event']==name]
        assert len(selected)==1, (rid,name)
        return selected[0]['time_ns']
    start = one('client_start')
    end = one('handler_exit')
    emits = [e for e in trace if e['event']=='semantic_emit']
    assert all(e['status']=='success' for e in emits)
    terminal = [e for e in emits if e['action']=='next']
    assert len(terminal)==1
    chunks = [e for e in emits if e['code_shape'] is not None]
    first_frame = next(e['time_ns'] for e in trace if e['event']=='client_read' and e['total_bytes']>=1808)
    row = dict(request_id=rid, cancel=request['cancel'], bytes=len(body),
               first_pcm_frame_ms=(first_frame-start)/1e6,
               semantic_chunks=len(chunks), semantic_terminal_ms=(terminal[0]['time_ns']-start)/1e6,
               handler_exit_ms=(end-start)/1e6)
    if request['cancel']:
        cancel = one('client_cancel_begin')
        returned = one('client_cancel_return')
        row.update(client_close_ms=(returned-cancel)/1e6,
                   semantic_chunks_completed_after_cancel=sum(e['time_ns']>cancel for e in chunks),
                   semantic_chunks_completed_after_handler_exit=sum(e['time_ns']>end for e in chunks),
                   cancel_to_semantic_terminal_ms=(terminal[0]['time_ns']-cancel)/1e6,
                   cancel_to_handler_exit_ms=(end-cancel)/1e6,
                   disconnect_observed=any(e['event']=='http_disconnect_observed' for e in trace))
    rows.append(row)
data = dict(status='observed_http_and_model_terminal_boundaries', rows=rows,
            scope='Isolated compile-false Fish1.5, no upstream cancellation change, CUDA sync instrumentation, loopback; not live Queqiao model cancellation latency')
(R/'summary.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(rows,indent=2))
