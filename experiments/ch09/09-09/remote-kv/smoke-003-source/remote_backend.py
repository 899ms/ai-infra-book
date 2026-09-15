"""SGLang dynamic backend: native page layout, actual HTTP/SSH remote storage."""
import hashlib,json,os,time,urllib.request
from pathlib import Path
import torch
from store import pack,unpack
from sglang.srt.mem_cache.hicache_storage import HiCacheFile
class RemoteKV(HiCacheFile):
 def __init__(self,config,kwargs=None):
  super().__init__(config,file_path=os.environ['BOOK_UNUSED_LOCAL_CACHE'])
  self.url=os.environ['BOOK_REMOTE_KV_URL'];self.trace=os.environ['BOOK_REMOTE_KV_TRACE']
 def rpc(self,op,meta,blobs=()):
  data=pack(meta,blobs);start=time.monotonic();response=None;err=None
  try:
   req=urllib.request.Request(self.url+'/'+op,data=data,headers={'Content-Type':'application/octet-stream'})
   with urllib.request.urlopen(req,timeout=120) as f:response=f.read()
   return unpack(response)
  except Exception as e:err=repr(e);raise
  finally:
   row=dict(op=op,start_s=start,end_s=time.monotonic(),request_bytes=len(data),response_bytes=len(response) if response else 0,meta=meta,error=err,pid=os.getpid())
   fd=os.open(self.trace,os.O_APPEND|os.O_CREAT|os.O_WRONLY,0o600)
   try:os.write(fd,(json.dumps(row)+'\n').encode())
   finally:os.close(fd)
 def exists(self,key):return self.rpc('exists',dict(keys=[self._get_suffixed_key(key)]))[0]['exists'][0]
 def _collect_existing_component_keys(self,keys,pool_transfers=None):
  names={self._get_component_key(k) for k in keys}
  for t in pool_transfers or []:names.update(self._get_component_key(k,t.name) for k in keys)
  names=sorted(names);answer=self.rpc('exists',dict(keys=names))[0]['exists'];return {k+'.bin' for k,v in zip(names,answer) if v}
 def get(self,key,target_location,target_sizes=None):return self.batch_get([key],[target_location])[0]
 def batch_get(self,keys,target_locations,target_sizes=None):
  result=[]
  for i in range(0,len(keys),8):result.extend(self._batch_get_chunk(keys[i:i+8],target_locations[i:i+8]))
  return result
 def _batch_get_chunk(self,keys,target_locations,target_sizes=None):
  names=[self._get_suffixed_key(k) for k in keys];meta,data=self.rpc('get',dict(keys=names));offset=0;out=[]
  assert len(meta['entries'])==len(names)==len(target_locations)
  for k,e,target in zip(names,meta['entries'],target_locations):
   n=e['bytes'];b=data[offset:offset+n];offset+=n;assert k==e['key'] and hashlib.sha256(b).hexdigest()==e['sha256']
   if not e['found']:out.append(None);continue
   assert n==target.numel()*target.element_size() and target.is_contiguous()
   target.view(torch.uint8).reshape(-1).copy_(torch.frombuffer(bytearray(b),dtype=torch.uint8));out.append(target)
  assert offset==len(data);return out
 def set(self,key,value=None,target_location=None,target_sizes=None):return self.batch_set([key],[value])
 def batch_set(self,keys,values=None,target_locations=None,target_sizes=None):
  for i in range(0,len(keys),8):
   if not self._batch_set_chunk(keys[i:i+8],values[i:i+8]):return False
  return True
 def _batch_set_chunk(self,keys,values=None,target_locations=None,target_sizes=None):
  blobs=[v.contiguous().view(torch.uint8).numpy().tobytes() for v in values]
  entries=[dict(key=self._get_suffixed_key(k),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()) for k,b in zip(keys,blobs)]
  meta,_=self.rpc('set',dict(entries=entries),blobs);assert len(meta['entries'])==len(keys);return True
 def clear(self):raise RuntimeError('Remote evidence is never cleared by engine')
