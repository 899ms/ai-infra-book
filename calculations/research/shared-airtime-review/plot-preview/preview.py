"""Research-only visual preview of AST plotting body; never call formal render."""
import ast,json,hashlib
from pathlib import Path
from fractions import Fraction as F
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
source=ROOT/'src/infra_calc/shared_airtime_plot.py'
text=source.read_text();tree=ast.parse(text)
ns={'F':F}
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name=='compact':exec(compile(ast.Module(body=[node],type_ignores=[]),str(source),'exec'),ns)
full=[];scan=[]
for name in ['image-baseline','mixed-fifo-immediate','mixed-fifo-aggregate','mixed-priority-immediate','mixed-priority-aggregate']:
 a=json.loads((ROOT/f'research/shared-airtime-book-inputs/runs/{name}-result.json').read_text())
 b=json.loads((ROOT/f'research/media-feedback-loop/runs/book-{name}-result.json').read_text())
 full.append({'name':name,'wireless':ns['compact'](a),'wan_only':ns['compact'](b)})
 del a,b
for size in [320,640,960]:
 for n in [1,2,4]:
  name=f'media-{size}B-ack{n}';r=json.loads((ROOT/f'research/shared-airtime-scan-inputs/runs/{name}-result.json').read_text())
  scan.append({'name':name,**ns['compact'](r)})
data={'full':full,'scan':scan}
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='render')
# Copy only the drawing statements, after formal verify and data extraction,
# stopping before formal manifest/data output. Write exclusively research PNG/SVG.
start=next(i for i,n in enumerate(node.body) if isinstance(n,ast.Import) and any(x.name=='matplotlib' for x in n.names))
end=next(i for i,n in enumerate(node.body) if isinstance(n,ast.Expr) and ast.unparse(n).startswith("(DIRECTORY / 'data.json')"))
body=[]
for n in node.body[start:end]:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='data' for t in n.targets):continue
 body.append(n)
exec(compile(ast.Module(body=body,type_ignores=[]),'<research-only-drawing-copy>','exec'),{'data':data,'F':F,'DIRECTORY':HERE})
(HERE/'preview-data.json').write_text(json.dumps({'source_sha256':hashlib.sha256(text.encode()).hexdigest(),'scope':'Research preview, no formal render/verify invocation',**data},indent=2)+'\n')
print('research preview saved',HERE/'figure.png')
