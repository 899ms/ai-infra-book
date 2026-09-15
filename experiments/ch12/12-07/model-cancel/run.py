import hashlib
import http.client
import importlib.util
import json
import os
from pathlib import Path
import socket
import struct
import threading
import time

R = Path(__file__).resolve().parent
OUT = R/'results'
OUT.mkdir(exist_ok=False)
spec = importlib.util.spec_from_file_location('recorded_fish_server', R/'sources/server.py')
service = importlib.util.module_from_spec(spec)
spec.loader.exec_module(service)
import torch
import fish_speech.models.text2semantic.inference as semantic

events = []
lock = threading.Lock()
local = threading.local()
done = {}
handler_done = {}
def log(event, request_id, **fields):
    row = dict(event=event, request_id=request_id, time_ns=time.perf_counter_ns(), **fields)
    with lock:
        events.append(row)
        with (OUT/'events.jsonl').open('a') as f:
            f.write(json.dumps(row)+'\n')
    return row

original_launch = service.launch_thread_safe_queue
def observed_launch(**kwargs):
    queue = original_launch(**kwargs)
    class Input:
        def put(self, item):
            rid = local.rid
            target = item.response_queue
            class Output:
                def put(self, response):
                    torch.cuda.synchronize()
                    action = getattr(response.response, 'action', None)
                    codes = getattr(response.response, 'codes', None)
                    log('semantic_emit', rid, status=response.status, action=action,
                        code_shape=list(codes.shape) if codes is not None else None)
                    target.put(response)
                    if response.status == 'error' or action == 'next':
                        done[rid].set()
            log('semantic_enqueued', rid)
            queue.put(semantic.GenerateRequest(item.request, Output()))
    return Input()
service.launch_thread_safe_queue = observed_launch
checkpoint = Path('/home/ubuntu/.cache/huggingface/hub/models--fishaudio--fish-speech-1.5/snapshots/275a984d33c33659e39eed41ff5bcd6e67517f4c')
sources = [R/'run.py', R/'PROTOCOL.md', R/'sources/server.py', Path(semantic.__file__), checkpoint/'config.json']
(OUT/'environment.json').write_text(json.dumps(dict(pid=os.getpid(), torch=torch.__version__,
    gpu=torch.cuda.get_device_name(), compile=False, checkpoint=str(checkpoint),
    semantic_module=semantic.__file__, source_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}),indent=2)+'\n')
speech = service.Speech(str(checkpoint), 'cuda', False, str(OUT/'empty-voices'))

class Handler(service.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def log_message(self, *args): pass
    def do_POST(self):
        request = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        rid = request.pop('request_id')
        local.rid = rid
        generator = speech.synthesize(request)
        try:
            log('handler_start', rid)
            self.send_response(200)
            self.send_header('Content-Type', 'audio/wav')
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(service.wav_header())
            self.wfile.flush()
            for pcm in generator:
                self.wfile.write(pcm)
                self.wfile.flush()
                log('pcm_sent', rid, bytes=len(pcm))
        except (BrokenPipeError, ConnectionResetError) as error:
            log('http_disconnect_observed', rid, error=type(error).__name__)
        except Exception as error:
            log('handler_error', rid, error=repr(error))
        finally:
            generator.close()
            self.close_connection = True
            log('handler_exit', rid)
            handler_done[rid].set()

server = service.ThreadingHTTPServer(('127.0.0.1', 19284), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
text = ('This experiment measures the difference between closing an audio connection and stopping a speech model. '
        'The transport can stop delivering sound while the model continues to prepare the remaining words. '
        'Every event is recorded on the same clock so that these boundaries can be checked independently. ')*3
cases = [('warmup', False, 'The isolated speech experiment is ready.')]
for pair in range(3):
    order = [False, True] if pair % 2 == 0 else [True, False]
    cases += [(f'pair{pair}-'+('cancel' if cancel else 'full'), cancel, text) for cancel in order]
records = []
try:
    for rid, cancel, content in cases:
        done[rid] = threading.Event()
        handler_done[rid] = threading.Event()
        request = dict(request_id=rid, text=content, chunk_length=80, max_new_tokens=512,
                       top_p=.7, repetition_penalty=1.2, temperature=.7)
        log('client_start', rid, cancel=cancel)
        connection = http.client.HTTPConnection('127.0.0.1',19284,timeout=180)
        connection.connect()
        sock = connection.sock
        connection.request('POST','/v1/tts',json.dumps(request),{'Content-Type':'application/json'})
        response = connection.getresponse()
        assert response.status == 200
        body = bytearray()
        while True:
            chunk = response.read1(1808 if cancel else 16384)
            if not chunk: break
            body.extend(chunk)
            log('client_read', rid, bytes=len(chunk), total_bytes=len(body))
            if cancel and len(body) >= 1808:
                log('client_cancel_begin', rid, received_bytes=len(body))
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii',1,0))
                response.close()
                connection.close()
                log('client_cancel_return', rid)
                break
        response.close()
        connection.close()
        log('client_done', rid, bytes=len(body))
        (OUT/f'{rid}.wav').write_bytes(body)
        terminal = done[rid].wait(180)
        handler = handler_done[rid].wait(30)
        records.append(dict(request=request, cancel=cancel, semantic_terminal_observed=terminal,
                            handler_exit_observed=handler, bytes=len(body), sha256=hashlib.sha256(body).hexdigest()))
        (OUT/'requests.json').write_text(json.dumps(records,indent=2)+'\n')
        assert terminal and handler, rid
        assert not any(e['request_id']==rid and (e['event']=='handler_error' or e.get('status')=='error') for e in events), rid
        print(rid, 'terminal observed', len(body), flush=True)
finally:
    server.shutdown()
    server.server_close()
    (OUT/'completion.json').write_text(json.dumps(dict(completed=len(records), expected=len(cases)))+'\n')
