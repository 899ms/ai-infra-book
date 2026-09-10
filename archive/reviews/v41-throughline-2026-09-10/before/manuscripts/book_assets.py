"""Derive the active figure index from the canonical chapter manuscript."""
from pathlib import Path
import json,re

def sync_figure_index(directory):
    directory=Path(directory)
    chapter=int(directory.name[2:])
    md=next(directory.parent.glob(f'{chapter:02}-*.md'))
    pairs=re.findall(r'!\[[^\n]*\]\(([^)]+)\)\s*\n\s*\*图\s+(\d+-\d+)[：\s]+([^\n]+)\*',md.read_text())
    assert len(pairs)==len(re.findall(r'!\[',md.read_text()))
    path=directory/'figure-index.json'
    old=json.loads(path.read_text()) if path.exists() else []
    schema=set(old[0]) if old else {'number','file','caption'}
    rows=[]
    for i,(asset,number,caption) in enumerate(pairs,1):
        assert number==f'{chapter}-{i}',(md,number,i)
        values=dict(number=i,figure=number,asset=asset,file=Path(asset).name,name=Path(asset).stem,caption=caption)
        rows.append({k:values[k] for k in schema if k in values})
    path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    return [path,Path(__file__),directory.parent/'core_principles_figures.py',directory.parent/'teaching_reading.py']
