"""Native two-worker cache pressure, failover, and same-address recovery."""
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
ROUTER = '/home/ubuntu/ai-infra-book-experiments/tools/router032-venv/bin/python'
MODEL = '/home/ubuntu/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218'
PORTS = [31591, 31592]
RP, MP = 31590, 31599


def save(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')


def http(port, path, payload=None, timeout=120):
    req = urllib.request.Request(f'http://127.0.0.1:{port}{path}',
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
        return json.loads(data) if data and r.headers.get_content_type() == 'application/json' else data.decode()


def main():
    out = ROOT/'results'
    out.mkdir(exist_ok=False)
    for port in PORTS+[RP, MP]:
        with socket.socket() as s:
            s.bind(('127.0.0.1', port))
    env = os.environ.copy()
    cuda = str(ENV/'lib/python3.10/site-packages/nvidia/cu13')
    env.update(CUDA_HOME=cuda, PATH=cuda+'/bin:'+env['PATH'], LD_LIBRARY_PATH=cuda+'/lib',
        TVM_FFI_CACHE_DIR='/home/ubuntu/ai-infra-book-experiments/ch09/09-08/jit-cache-cu13-v2', OMP_NUM_THREADS='4')
    gpu_cmd = ['nvidia-smi', '--query-gpu=name,driver_version,memory.total,memory.free', '--format=csv,noheader,nounits']
    before = subprocess.check_output(gpu_cmd, env=env, text=True)
    save(out/'gpu-before.json', {'output': before})
    assert int(before.split(',')[-1]) >= 60*1024
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    source = json.loads((ROOT/'agent-prompts.json').read_text())
    target = source['requests'][-1]['prompt_token_ids']
    fillers = [tok.encode(f'Unrelated document {i}. '+f'Unique-{i} data for cache capacity observation. '*180,
                add_special_tokens=False)[:1800] for i in range(4)]
    save(out/'inputs.json', {'target': target, 'fillers': fillers})
    commands, cleanup, logs, allprocs = [], [], [], []
    workers, worker_labels = {}, {}

    def append(name, obj):
        with (out/name).open('a') as f:
            f.write(json.dumps(obj, ensure_ascii=False)+'\n')

    def stop(p, role, hard=False):
        started = time.monotonic()
        if p.poll() is None:
            os.killpg(p.pid, signal.SIGKILL if hard else signal.SIGTERM)
            try:
                p.wait(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(p.pid, signal.SIGKILL)
                p.wait(timeout=15)
        cleanup.append(dict(pid=p.pid, role=role, exit_code=p.returncode, start=started, end=time.monotonic(), hard=hard))

    def start(cmd, label, port):
        log = (out/f'{label}.log').open('x')
        logs.append(log)
        commands.append(dict(label=label, command=cmd))
        p = subprocess.Popen(cmd, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        allprocs.append((p, label))
        deadline = time.monotonic()+300
        while time.monotonic() < deadline:
            if p.poll() is not None:
                raise RuntimeError(f'{label} exited {p.returncode}')
            try:
                http(port, '/health', timeout=2)
                return p
            except (OSError, ValueError):
                time.sleep(.5)
        raise TimeoutError(label)

    def start_worker(i, label):
        cmd = [str(ENV/'bin/python'), '-m', 'sglang.launch_server', '--model-path', MODEL,
            '--host', '127.0.0.1', '--port', str(PORTS[i]), '--dtype', 'bfloat16', '--context-length', '4096',
            '--mem-fraction-static', '0.45', '--max-total-tokens', '4096', '--max-running-requests', '8',
            '--chunked-prefill-size', '1024', '--disable-cuda-graph', '--disable-piecewise-cuda-graph',
            '--attention-backend', 'triton', '--sampling-backend', 'pytorch', '--random-seed', '909',
            '--log-requests', '--log-requests-level', '0', '--log-requests-format', 'json',
            '--log-requests-target', str(out/f'{label}-requests')]
        workers[i] = start(cmd, label, PORTS[i])
        worker_labels[i] = label
        save(out/f'{label}-info.json', {'pid': workers[i].pid, 'info': http(PORTS[i], '/get_server_info')})

    def registration(trial, stage, healthy):
        deadline = time.monotonic()+120
        while time.monotonic() < deadline:
            status = http(RP, '/workers', timeout=5)
            append('registration.jsonl', dict(trial=trial, stage=stage, time=time.monotonic(), response=status))
            rows = status.get('workers', [])
            actual = {w['url']: w.get('is_healthy', False) for w in rows}
            expected = {f'http://127.0.0.1:{PORTS[i]}': flag for i, flag in healthy.items()}
            if len(rows) == 2 and all(actual.get(url) == flag for url, flag in expected.items()):
                return status
            time.sleep(.5)
        raise TimeoutError(f'registration {stage}')

    def assignment(rid):
        found = set()
        for i, label in worker_labels.items():
            for path in (out/f'{label}-requests').glob('*.log'):
                for line in path.read_text().splitlines():
                    at = line.find('{')
                    if at < 0:
                        continue
                    try:
                        row = json.loads(line[at:])
                    except ValueError:
                        continue
                    if row.get('rid') == rid and row.get('event') == 'request.finished':
                        found.add(i)
        return found

    def request(trial, stage, ids, port=RP):
        rid = f'book909life-{trial}-{stage}'
        started = time.monotonic()
        response = http(port, '/generate', dict(rid=rid, input_ids=ids,
            sampling_params=dict(temperature=0, max_new_tokens=16, ignore_eos=True)))
        end = time.monotonic()
        deadline = end+10
        found = assignment(rid)
        while len(found) != 1 and time.monotonic() < deadline:
            time.sleep(.1)
            found = assignment(rid)
        append('requests.jsonl', dict(trial=trial, stage=stage, rid=rid, port=port, start=started, end=end,
            worker_indices=sorted(found), response=response))
        assert len(found) == 1, (rid, found)
        print(trial, stage, sorted(found), response.get('meta_info', {}).get('cached_tokens'), flush=True)
        return next(iter(found))

    try:
        for trial in range(3):
            for i in range(2):
                start_worker(i, f't{trial}-w{i}-original')
            router_cmd = [ROUTER, '-m', 'sglang_router.launch_router', '--host', '127.0.0.1', '--port', str(RP),
                '--worker-urls', *[f'http://127.0.0.1:{p}' for p in PORTS], '--policy', 'cache_aware',
                '--prometheus-port', str(MP), '--disable-retries', '--log-level', 'debug',
                '--health-check-interval-secs', '2', '--health-check-timeout-secs', '1']
            router = start(router_cmd, f't{trial}-router', RP)
            registration(trial, 'initial', {0: True, 1: True})
            request(trial, 'cold', target)
            request(trial, 'warm', target)
            for i in range(2):
                for j, ids in enumerate(fillers):
                    request(trial, f'pressure-w{i}-{j}', ids, PORTS[i])
            request(trial, 'after_pressure', target)
            chosen = request(trial, 'rewarm', target)
            event = dict(trial=trial, worker=chosen, old_pid=workers[chosen].pid, killed_at=time.monotonic())
            stop(workers[chosen], 'fault-injection', hard=True)
            registration(trial, 'unhealthy', {chosen: False, 1-chosen: True})
            event['unhealthy_observed_at'] = time.monotonic()
            request(trial, 'failover', target)
            request(trial, 'failover_warm', target)
            start_worker(chosen, f't{trial}-w{chosen}-restarted')
            event['new_pid'] = workers[chosen].pid
            registration(trial, 'recovered', {0: True, 1: True})
            event['healthy_observed_at'] = time.monotonic()
            append('restart-events.jsonl', event)
            request(trial, 'after_recovery', target)
            request(trial, 'recovery_warm', target)
            # Observe the restarted worker directly even if the router chooses the survivor.
            request(trial, 'restarted_direct', target, PORTS[chosen])
            request(trial, 'restarted_direct_warm', target, PORTS[chosen])
            (out/f't{trial}-metrics.txt').write_text(str(http(MP, '/metrics')))
            stop(router, 'router')
            for i in range(2):
                stop(workers[i], 'worker')
    finally:
        for p, label in reversed(allprocs):
            if p.poll() is None:
                stop(p, label)
        for log in logs:
            log.close()
        save(out/'execution.json', dict(commands=commands, cleanup=cleanup,
            source_hashes={f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ['run.py', 'agent-prompts.json']}))
        save(out/'gpu-after.json', {'output': subprocess.check_output(gpu_cmd, env=env, text=True)})


if __name__ == '__main__':
    main()
