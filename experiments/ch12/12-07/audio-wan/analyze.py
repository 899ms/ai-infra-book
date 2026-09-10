import argparse,hashlib,json
from pathlib import Path
B=Path(__file__).absolute().parent

def analyze():
 e=json.loads((B/'runs/execution.json').read_text());assert e['exit_code']==0
 pcm=(B/'fixture/audio.wav').read_bytes()[44:];rows=[]
 for iscancel in [False,True]:
  for round,pool in enumerate([True,False,False,True]):
   for stack in ['baseline','queqiao']:
    name=f'cancel-{str(iscancel).lower()}/round-{round}-pool-{str(pool).lower()}-{stack}';d=B/'runs/client'/name
    r=json.loads((d/'result.json').read_text());dev=json.loads((d/'device.json').read_text())
    rec=(d/'received.pcm').read_bytes();cons=(d/'device-consumed.pcm').read_bytes()
    assert rec==pcm[:len(rec)] and cons==rec[:len(cons)]
    assert len(rec)==dev['received_bytes']==r['received_bytes'] and len(cons)==dev['consumed_bytes']
    assert hashlib.sha256(rec).hexdigest()==dev['received_sha256']==r['received_sha256']
    assert hashlib.sha256(cons).hexdigest()==dev['consumed_sha256']
    assert dev['cancel']==iscancel and dev['output_muted'] and dev['device_name']=='MacBook Pro Speakers'
    assert not dev['callback_errors'] and not dev['reader_errors']
    assert dev['buffer_at_start']>=5292
    callbacks=[json.loads(z) for z in (d/'device-callbacks.jsonl').read_text().splitlines()]
    reads=[json.loads(z) for z in (d/'device-reads.jsonl').read_text().splitlines()]
    net=[json.loads(z) for z in (d/'events.jsonl').read_text().splitlines()]
    pos=0;last=-1;lastdac=-1
    for cb in callbacks:
     assert cb['ns']>=last and cb['api_output_dac_time']>=lastdac;last=cb['ns'];lastdac=cb['api_output_dac_time']
     assert cb['frames']==882 and cb['consumed_bytes']%2==0
     assert cb['consumed_bytes']==min(cb['buffer_before'],cb['frames']*2)//2*2
     pos+=cb['consumed_bytes'];assert pos==cb['cumulative_consumed']
     assert 0<=cb['starvation_bytes']<=cb['frames']*2
    assert pos==len(cons) and len(callbacks)==dev['callbacks']
    off=0;last=-1
    for x in reads:assert x['offset']==off and x['ns']>=last;off+=x['bytes'];last=x['ns']
    assert off==len(rec) and reads[-1]['bytes']==0
    if iscancel:
     assert len(rec)==17640 and dev['abort_call_ns']<=dev['abort_return_ns']
     eof=[x for x in reads if not x['bytes']][0]
     abort_after_eof=(dev['abort_return_ns']-eof['ns'])/1e6
    else:
     assert rec==cons==pcm and dev['abort_call_ns'] is None;abort_after_eof=None
    first=next(c for c in callbacks if c['consumed_bytes'])
    firstpipe=next(x for x in reads if x['bytes'])
    origin=[json.loads(z) for z in (B/'runs/server'/name/'origin-events.jsonl').read_text().splitlines()]
    writes=[z for z in origin if z['kind']=='origin_write'];total=sum(z['bytes'] for z in writes)
    assert [z['frame'] for z in writes]==list(range(len(writes)))
    if not iscancel:assert total==len(pcm) and any(z['kind']=='origin_all_sent' for z in origin)
    else:assert total>=17640 and any(z['kind']=='origin_reverse_read_end' and z['note']=='EOF' for z in origin)
    gaps=[(b['ns']-a['ns'])/1e6 for a,b in zip(writes,writes[1:])]

    # Both are Python monotonic timestamps. PortAudio's separate time-base delta is only API reported.
    rows.append(dict(condition=name,round=round,stack=stack,pool=pool,intentional_cancel=iscancel,
      received_bytes=len(rec),consumed_bytes=len(cons),callbacks=len(callbacks),buffer_at_start=dev['buffer_at_start'],
      origin_written_bytes=total,origin_max_interwrite_ms=max(gaps,default=0),cross_host_cancel_ms=None,
      first_pipe_to_callback_ms=(first['ns']-firstpipe['ns'])/1e6,
      api_first_callback_to_dac_ms=(first['api_output_dac_time']-first['api_current_time'])*1000,
      source_starvation_bytes=sum(c['starvation_bytes'] for c in callbacks),
      driver_output_underflow_callbacks=sum(bool(c['flags']&4) for c in callbacks),
      tail_padding_bytes=sum(c['tail_padding_bytes'] for c in callbacks),
      api_dac_span_s=callbacks[-1]['api_output_dac_time']-callbacks[0]['api_output_dac_time'],
      pipe_eof_to_abort_return_ms=abort_after_eof,
      abort_call_duration_ms=None if not iscancel else (dev['abort_return_ns']-dev['abort_call_ns'])/1e6,
      acoustic_first_sound_ms=None,audible_stalls=None,model_cancel_ms=None))
 assert len(rows)==16
 return dict(conditions=rows,full_pcm_equal=8,cancel_prefix_equal=8,boundary='Two hosts over current OS route through utun1024; authenticated native UDP application traffic, no SSH data tunnel. Device muted; no acoustic/model cancellation evidence; unsynchronised host clocks.')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=B/'analysis.json');a=p.parse_args();a.out.write_text(json.dumps(analyze(),indent=2)+'\n')
