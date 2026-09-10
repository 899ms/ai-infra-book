"""Muted real CoreAudio callback consumes pipe PCM; record starvation and API times."""
import argparse,ctypes as C,hashlib,json,os,threading,time
from pathlib import Path
from pa import LIB,Params,CB,library,check
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
lib=library();check(lib,lib.Pa_Initialize());device=lib.Pa_GetDefaultOutputDevice();info=lib.Pa_GetDeviceInfo(device).contents
assert info.name.decode()=='MacBook Pro Speakers','Use and record the intended physical output device'
start=time.monotonic_ns();startwall=time.time_ns();data=bytearray();consumed=bytearray();reads=[];callbacks=[]
ready=threading.Event();eof=threading.Event();cancel=threading.Event();reader_error=[]
def read():
 try:
  while True:
   block=os.read(0,4096);now=time.monotonic_ns()
   reads.append(dict(ns=now,unix_ns=time.time_ns(),bytes=len(block),offset=len(data)))
   if not block:break
   data.extend(block)
   if len(data)>=5292:ready.set()
  eof.set()
  if len(data)<1183744:cancel.set()
  ready.set()
 except BaseException as e:reader_error.append(repr(e));cancel.set();ready.set()
thread=threading.Thread(target=read,daemon=True);thread.start();position=0;cb_error=[]
@CB
def callback(inp,out,frames,timing,flags,user):
 global position
 try:
  now=time.monotonic_ns();before=len(data)-position;want=int(frames)*2;take=min(before,want)//2*2
  piece=bytes(data[position:position+take]);consumed.extend(piece);position+=take
  end=eof.is_set();is_cancel=cancel.is_set();starved=(want-take) if not end and not is_cancel else 0
  C.memset(out,0,want) # Stream-local mute. Device callback still advances with hardware timing.
  tt=timing.contents
  callbacks.append(dict(ns=now,unix_ns=time.time_ns(),frames=int(frames),flags=int(flags),buffer_before=before,consumed_bytes=take,cumulative_consumed=position,
    starvation_bytes=starved,tail_padding_bytes=(want-take) if end and not is_cancel else 0,eof=end,cancel=is_cancel,
    api_current_time=tt.currentTime,api_output_dac_time=tt.outputBufferDacTime))
  return 2 if is_cancel else (1 if end and position==len(data) else 0)
 except BaseException as e:cb_error.append(repr(e));C.memset(out,0,int(frames)*2);return 2
params=Params(device,1,8,info.defaultLowOutputLatency,None);stream=C.c_void_p()
check(lib,lib.Pa_OpenStream(C.byref(stream),None,C.byref(params),44100,882,0,callback,None))
assert ready.wait(40),'No PCM prebuffer'
buffer_at_start=len(data);start_call=time.monotonic_ns();check(lib,lib.Pa_StartStream(stream));start_return=time.monotonic_ns()
limit=time.monotonic()+40;abort_call=abort_return=None
while True:
 if cancel.is_set():
  abort_call=time.monotonic_ns();check(lib,lib.Pa_AbortStream(stream));abort_return=time.monotonic_ns();break
 active=check(lib,lib.Pa_IsStreamActive(stream))
 if not active:break
 assert time.monotonic()<limit,'Audio stream deadline exceeded'
 time.sleep(.005)
check(lib,lib.Pa_CloseStream(stream));thread.join(2);assert not thread.is_alive()
check(lib,lib.Pa_Terminate());assert not cb_error and not reader_error,(cb_error,reader_error)
(a.out/'device-reads.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in reads))
(a.out/'device-callbacks.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in callbacks))
(a.out/'device-consumed.pcm').write_bytes(consumed)
x=dict(device_index=device,device_name='MacBook Pro Speakers',requested_sample_rate=44100,requested_frames=882,channels=1,output_muted=True,
 portaudio_library=LIB,library_sha256=hashlib.sha256(Path(LIB).read_bytes()).hexdigest(),portaudio_version=lib.Pa_GetVersionText().decode(),
 start_ns=start,start_unix_ns=startwall,stream_start_call_ns=start_call,stream_start_return_ns=start_return,buffer_at_start=buffer_at_start,
 abort_call_ns=abort_call,abort_return_ns=abort_return,received_bytes=len(data),received_sha256=hashlib.sha256(data).hexdigest(),
 consumed_bytes=len(consumed),consumed_sha256=hashlib.sha256(consumed).hexdigest(),cancel=cancel.is_set(),callbacks=len(callbacks),
 acoustic_onset_ns=None,model_cancel_ns=None,callback_errors=cb_error,reader_errors=reader_error)
(a.out/'device.json').write_text(json.dumps(x,indent=2)+'\n')
assert callbacks and (cancel.is_set() or position==len(data))
