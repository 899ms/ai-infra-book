"""Observe native SGLang prefix eviction and process restart on one shared GPU.

Uses the archived Agent prompt unchanged. Never stops pre-existing services.
"""
import hashlib
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import time
import urllib.request

ROOT = Path(__file__).resolve().parent
ENV = Path('/home/ubuntu/ai-infra-book-experiments/tools/sglang0513-venv')
MODEL = '/home/ubuntu/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218'
PORT = 31491


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def http(path, payload=None, timeout=120):
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(f'http://127.0.0.1:{PORT}{path}', data=body,
                                 headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        data = response.read()
        return json.loads(data) if data else None


def main():
    out = ROOT / 'results'
    out.mkdir(exist_ok=False)
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', PORT))
    env = os.environ.copy()
    cuda = str(ENV / 'lib/python3.10/site-packages/nvidia/cu13')
    env.update(CUDA_HOME=cuda, PATH=cuda+'/bin:'+env['PATH'],
               LD_LIBRARY_PATH=cuda+'/lib:/home/ubuntu/OpenRealtime/.runtime/latest-deploy/nvml',
               TVM_FFI_CACHE_DIR='/home/ubuntu/ai-infra-book-experiments/ch09/09-08/jit-cache-cu13-v2',
               OMP_NUM_THREADS='4')
    gpu_cmd = ['nvidia-smi', '--query-gpu=name,memory.total,memory.free,utilization.gpu', '--format=csv,noheader,nounits']
    before = subprocess.check_output(gpu_cmd, env=env, text=True)
    save(out/'gpu-before.json', {'output': before})
    assert int(before.split(',')[2]) >= 26*1024, 'Need 26 GiB free; no service started'
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    source = json.loads((ROOT/'agent-prompts.json').read_text())
    target = source['requests'][-1]['prompt_token_ids']
    assert len(target) + 16 < 4096
    # Unique early tokens prevent sharing with the target and with other fillers.
    fillers = []
    for i in range(4):
        text = f'Unrelated document {i}. ' + (f'Unique-{i} data for cache capacity observation. ' * 180)
        fillers.append(tokenizer.encode(text, add_special_tokens=False)[:1800])
    save(out/'inputs.json', {'target': target, 'fillers': fillers,
                            'origin': source.get('origin'), 'target_id': source['requests'][-1]['id']})
    cmd = [str(ENV/'bin/python'), '-m', 'sglang.launch_server', '--model-path', MODEL,
           '--host', '127.0.0.1', '--port', str(PORT), '--dtype', 'bfloat16',
           '--context-length', '4096', '--mem-fraction-static', '0.90',
           '--max-total-tokens', '4096', '--max-running-requests', '8',
           '--chunked-prefill-size', '1024', '--disable-cuda-graph', '--disable-piecewise-cuda-graph',
           '--attention-backend', 'triton', '--sampling-backend', 'pytorch', '--random-seed', '909']
    save(out/'protocol.json', {'command': cmd, 'trials': 3, 'max_new_tokens': 16,
                             'temperature': 0, 'ignore_eos': True,
                             'scope': 'One worker; no router or remote KV; chronological cache lifecycle, shared GPU.',
                             'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                               for p in [Path(__file__), ROOT/'agent-prompts.json']}})
    process = None
    cleanup = []
    logs = []
    def stop():
        nonlocal process
        if process is None:
            return
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=15)
        cleanup.append({'pid': process.pid, 'exit_code': process.returncode})
        process = None
    def start(label):
        nonlocal process
        log = (out/f'server-{label}.txt').open('x')
        logs.append(log)
        t = time.monotonic()
        process = subprocess.Popen(cmd, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        deadline = t+240
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError(f'worker exited: {process.returncode}')
            try:
                http('/health', timeout=2)
                save(out/f'server-{label}.json', {'pid': process.pid, 'ready_seconds': time.monotonic()-t,
                                                'info': http('/get_server_info')})
                return
            except (OSError, ValueError):
                time.sleep(.5)
        raise TimeoutError('worker readiness')
    def request(trial, stage, ids):
        t = time.monotonic()
        response = http('/generate', {'input_ids': ids,
                        'sampling_params': {'temperature': 0, 'max_new_tokens': 16, 'ignore_eos': True}})
        row = {'trial': trial, 'stage': stage, 'pid': process.pid, 'start': t,
               'end': time.monotonic(), 'response': response}
        with (out/'requests.jsonl').open('a') as file:
            file.write(json.dumps(row, ensure_ascii=False)+'\n')
        print(trial, stage, response.get('meta_info', {}).get('cached_tokens'), flush=True)
    try:
        for trial in range(3):
            start(f'{trial}-before')
            request(trial, 'cold', target)
            request(trial, 'warm', target)
            for i, ids in enumerate(fillers):
                request(trial, f'pressure-{i}', ids)
            request(trial, 'after_pressure', target)
            request(trial, 'rewarm', target)
            stop()
            start(f'{trial}-restart')
            request(trial, 'after_restart', target)
            request(trial, 'restart_warm', target)
            stop()
    finally:
        stop()
        for log in logs:
            log.close()
        save(out/'cleanup.json', cleanup)
        save(out/'gpu-after.json', {'output': subprocess.check_output(gpu_cmd, env=env, text=True)})


if __name__ == '__main__':
    main()
