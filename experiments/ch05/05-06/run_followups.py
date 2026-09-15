"""Sequential exclusive-device operator experiment; preserves old runs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def main(a):
    a.output.mkdir(parents=True, exist_ok=False)
    def save(path, data):
        path.write_text(json.dumps(data, indent=2)+'\n')
    def gpu():
        text = subprocess.check_output(['nvidia-smi', '--query-compute-apps=pid,process_name,used_memory', '--format=csv,noheader,nounits'], text=True)
        return text, [int(line.split(',')[0]) for line in text.splitlines() if line.strip()]
    before, pids = gpu()
    save(a.output/'before.json', dict(time=time.time(),apps=before))
    assert not pids, 'Exclusive run requires no pre-existing CUDA processes'
    protocol = json.loads((ROOT/'protocol.json').read_text())
    records = []
    active = None
    def belongs(pid, root):
        for _ in range(20):
            if pid == root:
                return True
            try:
                status = Path(f'/proc/{pid}/status').read_text()
                pid = int(next(x for x in status.splitlines() if x.startswith('PPid:')).split()[1])
            except (OSError, StopIteration):
                return False
            if pid <= 1:
                return False
        return False
    def run(cmd, label, timeout):
        nonlocal active
        started = time.monotonic()
        with (a.output/f'{label}.log').open('x') as log, (a.output/f'{label}-gpu.jsonl').open('x') as monitor:
            active = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            while active.poll() is None:
                raw, pids = gpu()
                foreign = [pid for pid in pids if not belongs(pid, active.pid)]
                monitor.write(json.dumps(dict(time=time.time(),monotonic=time.monotonic(),apps=raw,foreign_pids=foreign))+'\n')
                monitor.flush()
                if foreign:
                    raise RuntimeError(f'External GPU activity during {label}: {foreign}')
                if time.monotonic()-started > timeout:
                    raise TimeoutError(label)
                time.sleep(.1)
            records.append(dict(label=label,command=cmd,pid=active.pid,exit_code=active.returncode,elapsed_s=time.monotonic()-started))
            active = None
            save(a.output/'execution.json',records)
            assert records[-1]['exit_code'] == 0, records[-1]
    try:
        run([sys.executable,str(ROOT/'run_agent_profile_feedback.py'),'--output',str(a.output/'agent')],'agent',600)
        selection=json.loads((a.output/'agent/summary.json').read_text())
        if selection['status']=='selected':
            run([sys.executable,str(ROOT/'heldout_agent.py'),'--search',str(a.output/'agent'),'--output',str(a.output/'agent-heldout.json')],'agent-heldout',180)
        request_root=ROOT.parent/'05-09'
        for trial in range(3):
            run([sys.executable,str(request_root/'run.py'),'--output',str(a.output/f'requests-{trial}')],f'requests-{trial}',300)
        save(a.output/'completion.json',dict(status='all_commands_finished',time=time.time(),
            source_hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ['run_followups.py','run_agent_profile_feedback.py','evaluate_agent_profile.py','protocol.json']},
            scope='Independent fourth Agent attempt with measured starting-kernel profiler feedback, same six-candidate/60s ceilings; followed by three independent 5-9 engines with 11 native/schedule pairs each. GPU exclusive; CPU load uncontrolled.'))
    finally:
        if active is not None and active.poll() is None:
            os.killpg(active.pid,signal.SIGTERM)
            try:
                active.wait(timeout=15)
            except subprocess.TimeoutExpired:
                os.killpg(active.pid,signal.SIGKILL)
                active.wait(timeout=15)
        raw,pids=gpu()
        save(a.output/'after.json',dict(time=time.time(),apps=raw,pids=pids))


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--output',type=Path,required=True)
    main(p.parse_args())
