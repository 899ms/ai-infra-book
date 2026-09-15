"""Runs only inside a restricted Docker container; stdout is a phase ledger."""
import json,signal,time
from pathlib import Path
job=json.loads(Path('/tmp/job.json').read_text());start=time.monotonic()
def emit(**kw):print(json.dumps(dict(at_s=time.monotonic(),**kw)),flush=True)
def deadline(*args):raise TimeoutError('validation execution deadline')
emit(event='worker_start',id=job['id'])
signal.signal(signal.SIGALRM,deadline)
try:
 signal.setitimer(signal.ITIMER_REAL,2)
 code=compile(job['code'],'<model-candidate>','exec');emit(event='compiled')
 scope={};exec(code,scope);emit(event='execution_start')
 n=job['test_n'];actual=scope['solve'](n)
 if job['batch']=='B':
  a,b=0,1
  for _ in range(n):a,b=b,a+b
  expected=a
 else:expected=n*(n-1)*(2*n-1)//6
 signal.setitimer(signal.ITIMER_REAL,0)
 emit(event='feedback',status='pass' if actual==expected else 'wrong',actual=actual,expected=expected)
except BaseException as exc:
 signal.setitimer(signal.ITIMER_REAL,0)
 emit(event='feedback',status='timeout' if isinstance(exc,TimeoutError) else 'error',error=repr(exc))
