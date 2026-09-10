"""Minimal ctypes declarations from the copied PortAudio header."""
import ctypes as C
LIB='/opt/homebrew/lib/libportaudio.2.dylib'
class Device(C.Structure):
 _fields_=[('structVersion',C.c_int),('name',C.c_char_p),('hostApi',C.c_int),('maxInputChannels',C.c_int),('maxOutputChannels',C.c_int),('defaultLowInputLatency',C.c_double),('defaultLowOutputLatency',C.c_double),('defaultHighInputLatency',C.c_double),('defaultHighOutputLatency',C.c_double),('defaultSampleRate',C.c_double)]
class Params(C.Structure):
 _fields_=[('device',C.c_int),('channelCount',C.c_int),('sampleFormat',C.c_ulong),('suggestedLatency',C.c_double),('hostApiSpecificStreamInfo',C.c_void_p)]
class Times(C.Structure):
 _fields_=[('inputBufferAdcTime',C.c_double),('currentTime',C.c_double),('outputBufferDacTime',C.c_double)]
CB=C.CFUNCTYPE(C.c_int,C.c_void_p,C.c_void_p,C.c_ulong,C.POINTER(Times),C.c_ulong,C.c_void_p)
def library():
 p=C.CDLL(LIB)
 p.Pa_GetVersionText.restype=C.c_char_p;p.Pa_GetDeviceInfo.argtypes=[C.c_int];p.Pa_GetDeviceInfo.restype=C.POINTER(Device)
 p.Pa_GetErrorText.argtypes=[C.c_int];p.Pa_GetErrorText.restype=C.c_char_p
 p.Pa_OpenStream.argtypes=[C.POINTER(C.c_void_p),C.c_void_p,C.POINTER(Params),C.c_double,C.c_ulong,C.c_ulong,CB,C.c_void_p]
 for name in ['Pa_StartStream','Pa_StopStream','Pa_AbortStream','Pa_CloseStream','Pa_IsStreamActive']:
  getattr(p,name).argtypes=[C.c_void_p]
 return p
def check(p,n):
 if n<0:raise RuntimeError(p.Pa_GetErrorText(n).decode())
 return n
if __name__=='__main__':
 import json
 p=library();check(p,p.Pa_Initialize());idx=p.Pa_GetDefaultOutputDevice();d=p.Pa_GetDeviceInfo(idx).contents
 print(json.dumps(dict(index=idx,name=d.name.decode(),hostApi=d.hostApi,outputChannels=d.maxOutputChannels,defaultSampleRate=d.defaultSampleRate,lowLatency=d.defaultLowOutputLatency,version=p.Pa_GetVersionText().decode())))
 check(p,p.Pa_Terminate())
