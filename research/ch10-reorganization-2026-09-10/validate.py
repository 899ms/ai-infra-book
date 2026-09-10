"""Read-only chapter audit, writing its result beside the editorial snapshots."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import ast
import hashlib
import json
import re

D = Path(__file__).resolve().parent
R = D.parents[1]
O = R / 'outlines'
p = O / '10-训练系统.md'
e = O / 'extensions/10-训练系统.md'
s, ext = p.read_text(), e.read_text()
old_s = (D / 'outline-before.txt').read_text()
old_e = (D / 'extension-before.txt').read_text()
errors = []
def check(ok, message):
    if not ok:
        errors.append(message)

def headings(t):
    return re.findall(r'^### (.+)$', t, re.M)
check(headings(s) == headings(ext), 'main/companion headings differ')
check(len(headings(s)) == 23, 'expected 23 subsections')
check(len(re.findall(r'^## 10\.', s, re.M)) == 6, 'expected six sections')
for text in [s, ext]:
    for word, count in [('实验', 10), ('图', 9)]:
        ids = re.findall(r'^> \*\*' + word + r' (10-\d+)', text, re.M)
        check(ids == [f'10-{i}' for i in range(1, count + 1)], f'{word} ordering/count')
for heading in headings(s):
    check(f'id="detail-{heading.split()[0]}"' in ext, f'companion anchor {heading}')
core = re.findall(r'^> \*\*实验 (10-\d+)[^\n]*〔核心〕', s, re.M)
check(core == ['10-3', '10-7', '10-10'], 'core experiments')
catalog = json.loads((O / 'chapters.json').read_text())
check(core == catalog[9]['core_experiments'], 'catalog cores')
# Normalize link bases to compare identity, not the main/companion location.
links = lambda t: set(re.findall(r'\]\(([^)]+)\)', t))
old_links = links(old_s + old_e.replace('](../../', '](../'))
new_links = links(s + ext.replace('](../../', '](../'))
check(old_links <= new_links, f'lost original links: {old_links - new_links}')
evidence = lambda t: set(re.findall(r'已复算（([^）]+)', t))
check(evidence(old_e) <= evidence(ext), 'lost calculation evidence keys')
link_count = 0
for path, text in [(p, s), (e, ext), (D / 'README.md', (D / 'README.md').read_text())]:
    for url in links(text):
        parts = urlsplit(url)
        if parts.scheme or url.startswith('//'):
            continue
        target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
        # This report is created below.
        if target == D / 'validation.json':
            continue
        link_count += 1
        check(target.exists(), f'missing local target: {url}')
        if parts.fragment and target.exists() and target.suffix == '.md':
            content = target.read_text()
            slug = unquote(parts.fragment)
            explicit = re.findall(r'id="([^"]+)"', content)
            generated = [re.sub(r'[^\w\-\s]', '', title.lower()).replace(' ', '-')
                         for title in re.findall(r'^#{1,6} (.+)$', content, re.M)]
            check(slug in explicit + generated, f'missing target anchor: {url}')
# Verify future insertion markers without running a book-wide calculation sync.
module = ast.parse((R / 'calculations/src/infra_calc/outline.py').read_text())
marker_count = 0
for node in ast.walk(module):
    if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id != 'insert':
        continue
    if len(node.args) != 4 or not isinstance(node.args[0], ast.Constant) or node.args[0].value != p.name:
        continue
    marker = ast.literal_eval(node.args[3])
    marker_count += 1
    check(marker in ext, f'calculation insertion marker: {marker}')
page = (R / 'skeleton.html').read_text()
article = re.search(r'<article class="card" id="ch-10">.*?</article>', page, re.S)
check(article is not None, 'missing chapter HTML')
if article:
    for heading in headings(s):
        check('id="sec-' + heading.split()[0].replace('.', '-') + '"' in article[0], f'HTML heading {heading}')
    check('6 节／23 小节 · 10 项练习（3 项核心） · 9 项配图计划' in article[0], 'HTML totals')
report = dict(status='passed' if not errors else 'failed', sections=6, subsections=23,
              previous_subsections=len(headings(old_s)), experiments=10, figures=9,
              core_experiments=core, original_links_preserved=len(old_links),
              calculation_evidence_keys_preserved=len(evidence(old_e)),
              local_links_checked=link_count, insertion_markers_checked=marker_count,
              snapshot_sha256={name: hashlib.sha256((D/name).read_bytes()).hexdigest()
                               for name in ['outline-before.txt', 'extension-before.txt']},
              errors=errors)
(D / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
