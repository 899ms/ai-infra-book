"""Reproduce stated analytical scenarios; no hardware throughput claims."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,math
P=Path(__file__).resolve().parent
ROOT=P.parents[2]
image=800000;feature=400*10240*2
local=F(131,100)/F('165.2');remote=F(131,100)/F('989.4')
rows=[]
for bandwidth in [800000,50000000000]:
 rows.append(dict(bandwidth_bytes_s=bandwidth,local_encode_s=float(local),remote_encode_s=float(remote),local_and_feature_s=float(local+F(feature,bandwidth)),remote_and_image_s=float(remote+F(image,bandwidth)),extra_feature_transfer_s=float(F(feature-image,bandwidth)),extra_local_encode_s=float(local-remote)))
migration=F(64*2**20,10000000)+1
min_round=math.ceil((migration+1)/F('.4'))
assert (min_round-1)*F('.4')<migration+1<=min_round*F('.4')
frames=30800;data=F(302,10**6);ack=F(134,10**6)
airtime_before=frames*(data+ack);airtime_after=frames*data+frames//2*ack
buffers=[]
for rate in [256000,384000]:
 initial=rate*F('.06');t=initial/(rate-130000)
 assert initial+130000*t-rate*t==0
 buffers.append(dict(playback_bits_s=rate,initial_bits=int(initial),exhaust_s=float(t)))
size=30*10**6
split=[F(2,3),F(1,3)];times=[F(size*8)*x/b for x,b in zip(split,[20000000,10000000])]
assert times[0]==times[1]==8
failure=F('.02')+(1-F('.02'))*F('.1')*F('.05')
# Enumerate independent endpoint/access outcomes as a cross-check.
enumerated=F(0)
for endpoint in [0,1]:
 for a in [0,1]:
  for b in [0,1]:
   prob=(F('.02') if endpoint else F('.98'))*(F('.1') if a else F('.9'))*(F('.05') if b else F('.95'))
   if endpoint or (a and b):enumerated+=prob
assert enumerated==failure
source=ROOT/'manuscripts/12-端边云协同.md'
out=dict(exercises=['12-3','12-5','12-6'],kind='analytical_stated_conditions',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()},vision=dict(image_bytes=image,feature_bytes=feature,paths=rows,migration_s=float(migration),net_saved_s={str(n):float(n*F('.4')-migration) for n in [10,20,40]},restore2s_min_rounds=min_round),ack=dict(before_s=float(airtime_before),after_s=float(airtime_after),saved_s=float(airtime_before-airtime_after),buffers=buffers),dual_path=dict(split=[float(x) for x in split],path_bytes=[int(size*x) for x in split],finish_s=float(times[0]),shared_exit_lower_bound_s=float(F(size*8,24000000)),replication_failure=float(failure),perfect_access_failure=.02,duplicate_extra_bytes=8*640))
(P/'12-3-5-6-results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
