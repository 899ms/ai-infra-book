from pathlib import Path
import json,re,hashlib,math,sys
root=Path.cwd();r=root/'research/ch04-whole-chapter-review-2026-09-11';p=root/'manuscripts/04-加速器架构.md';s=p.read_text();old=(r/'before.md').read_text();body=s.split('[^qwen]:')[0]
figs=re.findall(r'\*图 (4-\d+)　',body);assert figs==[f'4-{i}' for i in range(1,35)]
assets=re.findall(r'!\[[^\n]*\]\(([^)]+)\)',body);assert set(assets)==set(re.findall(r'!\[[^\n]*\]\(([^)]+)\)',old))
headers=set(re.findall(r'^#{2,3} (4\.\d+(?:\.\d+)?) ',body,re.M))
for ref in re.findall(r'第 (4\.\d+(?:\.\d+)?) 节',body):assert ref in headers,ref
used=set(re.findall(r'\[\^([^]]+)\]',body));defined=set(re.findall(r'^\[\^([^]]+)\]:',s,re.M));assert used==defined,(used-defined,defined-used)
for link in re.findall(r'\]\(([^)]+)\)',s):
 if not link.startswith(('http','#')):assert (p.parent/link.split('#')[0]).exists(),link
paras=[x for x in body.split('\n\n') if len(x)>80 and not x.startswith(('!','*','$','|','>'))];assert len(paras)==len(set(paras))
# Independent service budgets for the newly stated handoff example.
ceil=lambda x,y:math.ceil(x/y)
softmax=ceil(3*32*128-32,128)+ceil(32*127,128)+ceil(32*128,16)*2
assert softmax==640
assert 2*32*128*128/8192==128
assert 32*128*4/128==128 and 32*128*2/128==64
# Newly stated cost result and changed thought exercise.
annual=100*10000*.5*365*24*3600*.5/1e6
assert round(annual/10000)==788
separate=4*(2+8192/100000);combined=3+2+4*8192/100000
v={'passed':True,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sections':len(re.findall(r'^## ',body,re.M)),'subsections':len(re.findall(r'^### ',body,re.M)),'figures':len(figs),'same_figure_assets':True,'examples':len(re.findall(r'\*\*例 4-\d',body)),'experiments':len(re.findall(r'\*\*实验 4-\d',body)),'footnotes':len(used),'all_local_links_and_section_references_valid':True,'no_exact_duplicate_prose_paragraphs':True,'handoff_softmax_ticks':softmax,'annual_saving_dollars':annual,'thought_exercise_solution_us':{'separate_last':separate,'separate_first':2+8192/100000,'merged_all':combined},'chinese_characters_before':len(re.findall('[\u4e00-\u9fff]',old)),'chinese_characters_after':len(re.findall('[\u4e00-\u9fff]',s))}
(r/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');print(json.dumps(v,ensure_ascii=False))
