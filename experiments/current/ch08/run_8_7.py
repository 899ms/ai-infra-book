"""Exact speculative-round expectation and marginal cost comparison."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('08-*.md'));a=F(3,4)
def row(m,grouped=False):
 n=sum((a**j for j in range(m+1)),F(0));t=F(263,10)+F(36,10)*(4*((m+3)//4) if grouped else m)
 # Rejection at each position, or all accepted plus one target output.
 distribution=[(j,(1-a)*a**(j-1)) for j in range(1,m+1)]+[(m+1,a**m)]
 assert sum(p for _,p in distribution)==1 and sum(j*p for j,p in distribution)==n
 return dict(draft_length=m,expected_tokens_exact=str(n),expected_tokens=float(n),round_ms=float(t),ms_per_token=float(t/n),ms_per_token_exact=str(t/n))
serial=[row(m) for m in (1,2,4,8)];group=[row(m,True) for m in (4,5)]
dn=a**5;dt=F(144,10);old=F(group[0]['ms_per_token_exact'])
assert dt/dn>old and group[1]['ms_per_token']>group[0]['ms_per_token']
out=dict(exercise='8-7',serial_candidates=serial,best_requested_serial_candidate=min(serial,key=lambda r:r['ms_per_token'])['draft_length'],grouped_candidates=group,marginal_4_to_5=dict(additional_expected_tokens_exact=str(dn),additional_ms=float(dt),marginal_ms_per_extra_token=float(dt/dn),previous_ms_per_token=float(old)),scope='Ratio of expected long-run output to round time; constant conditional acceptance 3/4, no EOS truncation; not expectation of per-round T/N or measured DFlash timing',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'8-7-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
