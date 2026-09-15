"""Inventory current exercise text and historical completion claims separately."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
HEADER = re.compile(r'^(?:>\s*)?(?:\d+\.\s*)?\*\*(?:(实验|练习|习题)\s+)?(\d+-\d+)(?=[　\s〔·：])')


def main():
    legacy = json.loads((ROOT/'experiments/inventory.json').read_text())
    rows = []
    for p in sorted((ROOT/'manuscripts').glob('[0-9]*.md')):
        manuscript = p.read_text()
        lines = manuscript.splitlines()
        definitions = dict(re.findall(r'^\[\^([^\]]+)\]:\s*(.*)$', manuscript, re.M))
        starts = [(i, HEADER.match(line)) for i,line in enumerate(lines) if HEADER.match(line)]
        for i, match in starts:
            end = i+1
            if lines[i].startswith('>'):
                while end < len(lines) and not HEADER.match(lines[end]) and (lines[end].startswith('>') or not lines[end].strip()):
                    end += 1
            else:
                while end < len(lines) and not (HEADER.match(lines[end]) or lines[end].startswith(('##','[^'))):
                    end += 1
            chapter = int(match[2].split('-')[0])
            body = '\n'.join(lines[i:end]).strip()
            citations = {key: definitions[key] for key in re.findall(r'\[\^([^\]]+)\]',body) if key in definitions}
            evidence = []
            for link in re.findall(r'\]\(([^)]+)\)', body+'\n'+'\n'.join(citations.values())):
                url = urlsplit(unquote(link))
                if url.scheme or not url.path:
                    continue
                target = (p.parent/url.path).resolve()
                try:
                    name = str(target.relative_to(ROOT))
                except ValueError:
                    continue
                if name not in [e['path'] for e in evidence]:
                    evidence.append(dict(path=name,exists=target.exists()))
            rows.append(dict(id=match[2], kind=match[1] or 'numbered_exercise', source=str(p.relative_to(ROOT)),
                             line=i+1, requirements=body, requirements_sha256=hashlib.sha256(body.encode()).hexdigest(),
                             source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                             explicit_evidence=evidence, resolved_footnotes=citations,
                             completion='current_exercise_completed' if (chapter in (1,2,3,4,5,11) or match[2] in ("6-1","6-2","6-3","6-4","6-5","6-6","6-7","6-8","6-9","6-10","6-11","7-1","7-2","7-3","7-4","7-5","7-6","7-7","7-8","7-9","7-10","7-11","7-12","7-13","7-14","7-15","8-1","8-2","8-3","8-4","8-5","8-6","8-7","8-8","8-9","9-1","9-2","9-3","9-4","9-5","9-6","9-7","9-8","9-9","9-10","9-11","10-1","10-2","10-3","10-4","10-5","10-6","10-7","10-8","10-9","10-10","12-1","12-2","12-3","12-5","12-6","12-8","12-9","12-4","12-10","12-7")) else 'chapter_checks_only_protocol_review_not_complete',
                             new_answer=f'experiments/current/ch{chapter:02d}/README.md' if (chapter in (1,2,3,4,5,11) or match[2] in ("6-1","6-2","6-3","6-4","6-5","6-6","6-7","6-8","6-9","6-10","6-11","7-1","7-2","7-3","7-4","7-5","7-6","7-7","7-8","7-9","7-10","7-11","7-12","7-13","7-14","7-15","8-1","8-2","8-3","8-4","8-5","8-6","8-7","8-8","8-9","9-1","9-2","9-3","9-4","9-5","9-6","9-7","9-8","9-9","9-10","9-11","10-1","10-2","10-3","10-4","10-5","10-6","10-7","10-8","10-9","10-10","12-1","12-2","12-3","12-5","12-6","12-8","12-9","12-4","12-10","12-7")) else None))
    lfs = json.loads(subprocess.check_output(['git','lfs','ls-files','--json'],cwd=ROOT,text=True))['files']
    attributes = subprocess.check_output(['git','check-attr','--stdin','-z','filter'], cwd=ROOT,
                                        input=b''.join(e['name'].encode()+b'\0' for e in lfs)).split(b'\0')
    missing_attributes = [attributes[i].decode() for i in range(0,len(attributes)-1,3) if attributes[i+2]!=b'lfs']
    actual_pointers = [e['name'] for e in lfs if (ROOT/e['name']).stat().st_size < 200
                       and (ROOT/e['name']).read_bytes().startswith(b'version https://git-lfs.github.com/spec/v1\n')]
    missing = [dict(id=e['id'],path=p) for e in legacy for p in e.get('evidence',[]) if not (ROOT/p).exists()]
    stale_sources = [dict(id=e['id'],source=e['source']) for e in legacy if not (ROOT/e['source']).exists()]
    report = dict(current_exercise_blocks=len(rows), unique_current_ids=len(set(e['id'] for e in rows)),
                  chapter_counts=dict(Counter(e['id'].split('-')[0] for e in rows)),
                  duplicate_current_ids=[k for k,v in Counter(e['id'] for e in rows).items() if v>1],
                  historical_inventory_count=len(legacy), historical_status_counts=dict(Counter(e['status'] for e in legacy)),
                  historical_gaps=[dict(id=e['id'],directory=e['directory'],remaining=e['remaining']) for e in legacy if e.get('remaining')],
                  missing_historical_evidence_paths=missing, missing_historical_source_paths=stale_sources,
                  lfs_files=len(lfs), lfs_unhydrated=[e['name'] for e in lfs if not e['checkout']],
                  lfs_paths_without_filter=missing_attributes, lfs_actual_pointer_files=actual_pointers,
                  whole_book_complete=False,
                  limitation='Chapter verification and artifact presence do not prove every current subquestion or historical experimental protocol is finished.')
    for name,value in [('current-exercises.json',rows),('audit.json',report)]:
        (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    table = ['# 当前正文逐题清单', '', '题目以当前正文为准。章节检查通过不等于每个子问题已独立完成；历史实验目录不能只按同号自动匹配。', '',
             '| 编号 | 正文位置 | 题目直接引用证据数 | 本轮检查范围 |', '| --- | --- | --- | --- |']
    for e in rows:
        table.append(f"| {e['kind']} {e['id']} | [{e['source']}:{e['line']}](../../{e['source']}) | {len(e['explicit_evidence'])} | {'当前题目计算和解释已补齐' if e['new_answer'] else '现有章节验证；仍需逐协议对照'} |")
    (HERE/'current-index.md').write_text('\n'.join(table)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['historical_gaps']},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
