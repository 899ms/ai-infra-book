"""Run the existing PDF builder with isolated auxiliary files, preserving repo sources."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
builder=ROOT/'book/build_pdf.py'
source=builder.read_text()
old="work = HERE / 'build' / name"
new="work = ROOT / 'build/ub-ep-review/latex' / name"
assert source.count(old)==1
sys.argv=[str(builder),'--output-dir',str(ROOT/'build/ub-ep-review/full')]
exec(compile(source.replace(old,new),str(builder),'exec'),{'__name__':'__main__','__file__':str(builder)})
