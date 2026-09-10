"""Download pinned official sources and only the headers of all weight shards."""
import concurrent.futures
import datetime
import hashlib
import json
import struct
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
MODEL = 'deepseek-v4.1-flash'
REPO = 'deepseek-ai/DeepSeek-V4.1-Flash'
REV = 'df42c109f1defefcbfcedbe7d905718a12266e40'
BASE = f'https://huggingface.co/{REPO}/resolve/{REV}/'

def get(url, interval=None):
    for attempt in range(4):
        try:
            headers = {'User-Agent': 'ai-infra-book-calculations/0.1'}
            if interval:
                headers['Range'] = interval
                url_request = url + '?header_range=' + interval.removeprefix('bytes=')
            else:
                url_request = url
            with urlopen(Request(url_request, headers=headers), timeout=45) as r:
                if interval:
                    start, end = map(int, interval.removeprefix('bytes=').split('-'))
                    if r.status != 206 or not r.headers.get('Content-Range', '').startswith(f'bytes {start}-{end}/'):
                        raise ValueError('Server must honor bounded Range')
                    data = r.read(end-start+2)
                    if len(data) != end-start+1:
                        raise ValueError('Invalid range response length')
                else:
                    data = r.read()
            return data
        except Exception:
            if attempt == 3:
                raise
            time.sleep(attempt+1)

def save(upstream, local, interval=None):
    url = BASE + upstream
    data = get(url, interval)
    path = ROOT / local
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    row = dict(model=MODEL, repository=REPO, revision=REV, upstream_file=upstream,
               url=url + ('?header_range='+interval.removeprefix('bytes=') if interval else ''),
               file=local, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data),
               downloaded_at=datetime.datetime.now(datetime.timezone.utc).isoformat(), status='downloaded')
    if interval:
        row['http_range'] = interval
    return row

def shard(name):
    n = struct.unpack('<Q', get(BASE+name, 'bytes=0-7'))[0]
    if not 0 < n < 32*1024*1024:
        raise ValueError('Invalid safetensors header size')
    return save(name, f'sources/{MODEL}/headers/{name}.header.bin', f'bytes=0-{n+7}')

def main():
    names = ['config.json', 'README.md', 'LICENSE', 'model.safetensors.index.json',
             'DeepSeek_V41_Tech_Report.pdf', 'inference/config.json', 'inference/README.md',
             'inference/model.py', 'inference/kernel.py', 'inference/engram.py',
             'inference/vision.py', 'inference/convert.py', 'inference/generate.py',
             'inference/image_processor.py', 'evaluation/README.md']
    jobs = [(n, f'configs/models/{MODEL}/{n}' if n in ('config.json', 'inference/config.json') else f'sources/{MODEL}/{n}') for n in names]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        rows = list(pool.map(lambda p: save(*p), jobs))
        index = json.loads((ROOT/f'sources/{MODEL}/model.safetensors.index.json').read_text())
        rows += list(pool.map(shard, sorted(set(index['weight_map'].values()))))
    lock_path = ROOT/'configs/sources.lock.json'
    lock = json.loads(lock_path.read_text())
    lock['sources'] = [r for r in lock['sources'] if r['file'] not in {x['file'] for x in rows}] + rows
    lock_path.write_text(json.dumps(lock, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'sources': len(rows), 'downloaded_bytes': sum(r['bytes'] for r in rows)}))

if __name__ == '__main__':
    main()
