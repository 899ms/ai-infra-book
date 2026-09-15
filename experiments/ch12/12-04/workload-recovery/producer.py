"""Recorded model-output availability, independent of response connection life."""
import asyncio,hashlib,time
NOW=time.perf_counter
class Operation:
 def __init__(self,identity,fixture,source_request):
  self.identity=identity;self.fixture=fixture;self.source_request_sha256=hashlib.sha256(source_request).hexdigest();self.start_s=NOW();self.available=0;self.releases=[];self.condition=asyncio.Condition();self.done_s=None
  self.task=asyncio.create_task(self.produce())
 async def produce(self):
  for p in self.fixture['release_plan']:
   await asyncio.sleep(max(0,self.start_s+p['ready_s']-NOW()))
   assert p['offset']==self.available
   async with self.condition:
    self.available+=p['bytes'];self.releases.append(dict(offset=p['offset'],bytes=p['bytes'],at_s=NOW()));self.condition.notify_all()
  assert self.available==len(self.fixture['response']);self.done_s=NOW()
 async def suffix_parts(self,offset):
  assert 0<=offset<len(self.fixture['response'])
  for p in self.fixture['release_plan']:
   end=p['offset']+p['bytes'];begin=max(offset,p['offset'])
   if end<=begin:continue
   async with self.condition:await self.condition.wait_for(lambda:self.available>=end)
   yield begin,self.fixture['response'][begin:end]
 def record(self):
  return dict(identity=self.identity,start_s=self.start_s,done_s=self.done_s,available=self.available,source_request_sha256=self.source_request_sha256,response_sha256=hashlib.sha256(self.fixture['response']).hexdigest(),release_plan=self.fixture['release_plan'],releases=self.releases)
