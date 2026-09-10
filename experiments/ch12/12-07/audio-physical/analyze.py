"""Validate physical-interface audio, including cancellation before first callback."""
import argparse,hashlib,json
from pathlib import Path
B=Path(__file__).absolute().parent

def analyze():
 execution=json.loads((B/'runs/execution.json').read_text())
 assert execution['exit_code'] in (0,1)
 old=B/'runs/executed-sink.py'
 assert hashlib.sha256((old if old.exists() else B/'sink.py').read_bytes()).hexdigest()==execution['device_driver_sha256']
 pcm=(B/'fixture/audio.wav').read_bytes()[44:];rows=[];legacy=0
 for cancel in [False,True]:
  for round,pool in enumerate([True,False,False,True]):
   for stack in ['baseline','queqiao']:
    name=f'cancel-{str(cancel).lower()}/round-{round}-pool-{str(pool).lower()}-{stack}';d=B/'runs/client'/name
    dev=json.loads((d/'device.json').read_text());net=[json.loads(z) for z in (d/'events.jsonl').read_text().splitlines()]
    got=[z for z in net if z['kind']=='client_frame'];expected=17640 if cancel else len(pcm)
    assert sum(z['bytes'] for z in got)==expected==dev['received_bytes']
    assert [z['frame'] for z in got]==list(range(len(got)))
    assert dev['received_sha256']==hashlib.sha256(pcm[:expected]).hexdigest()
    raw=d/'received.pcm';has_raw=raw.exists()
    if has_raw:assert raw.read_bytes()==pcm[:expected]
    cb=[json.loads(z) for z in (d/'device-callbacks.jsonl').read_text().splitlines()]
    cons=(d/'device-consumed.pcm').read_bytes();assert cons==pcm[:len(cons)]
    assert hashlib.sha256(cons).hexdigest()==dev['consumed_sha256'] and len(cons)==dev['consumed_bytes']
    assert len(cb)==dev['callbacks'] and sum(c['consumed_bytes'] for c in cb)==len(cons)
    off=0;last=-1
    for c in cb:
     assert c['ns']>=last;last=c['ns'];off+=c['consumed_bytes'];assert off==c['cumulative_consumed']
     assert c['consumed_bytes']==min(c['buffer_before'],c['frames']*2)//2*2
    assert dev['cancel']==cancel and not dev['callback_errors'] and not dev['reader_errors'] and dev['output_muted']
    reads=[json.loads(z) for z in (d/'device-reads.jsonl').read_text().splitlines()];offset=0;last=-1
    for r in reads:assert r['offset']==offset and r['ns']>=last;offset+=r['bytes'];last=r['ns']
    assert offset==expected and reads[-1]['bytes']==0
    if cancel:
     assert dev['abort_call_ns']<=dev['abort_return_ns']
     assert len([r for r in net if r['kind']=='cancel_call'])==len([r for r in net if r['kind']=='cancel_return'])==1
     if not has_raw:
      # Original wrapper exited on an over-strict post-measurement assertion.
      assert not cb and not cons and not (d/'result.json').exists()
      legacy+=1
    else:assert cb and cons==pcm and has_raw
    origin=[json.loads(z) for z in (B/'runs/server'/name/'origin-events.jsonl').read_text().splitlines()]
    assert all(y['ns']>=x['ns'] for x,y in zip(origin,origin[1:]))
    written=sum(z['bytes'] for z in origin if z['kind']=='origin_write')
    if cancel:assert any(z['kind']=='origin_reverse_read_end' and z['note']=='EOF' for z in origin)
    else:assert written==len(pcm) and any(z['kind']=='origin_all_sent' for z in origin)
    first=next((c for c in cb if c['consumed_bytes']),None)
    rows.append(dict(condition=name,round=round,pool=pool,stack=stack,intentional_cancel=cancel,received_bytes=expected,
      received_pcm_file_retained=has_raw,received_sha_verified=True,consumed_bytes=len(cons),callbacks=len(cb),zero_callback_cancel=cancel and not cb,
      first_network_frame_ms=got[0]['ns']/1e6,buffer_at_start=dev['buffer_at_start'],
      first_pipe_to_callback_ms=None if first is None else (first['ns']-reads[0]['ns'])/1e6,
      source_starvation_bytes=sum(c['starvation_bytes'] for c in cb),driver_output_underflow_callbacks=sum(bool(c['flags']&4) for c in cb),
      tail_padding_bytes=sum(c['tail_padding_bytes'] for c in cb),origin_written_bytes=written,
      pipe_eof_to_abort_return_ms=None if not cancel else (dev['abort_return_ns']-reads[-1]['ns'])/1e6,
      cross_host_cancel_ms=None,acoustic_onset_ms=None,model_cancel_ms=None))
 ref=json.loads((B/'interface-reference/result.json').read_text())['probes'];pr=json.loads((B/'interface-reference/peer.jsonl').read_text().splitlines()[-1])['received']
 bound={v['source_ip_sha256'] for r,v in zip(ref,pr) if r['bound']};unbound={v['source_ip_sha256'] for r,v in zip(ref,pr) if not r['bound']}
 peers=[json.loads(z) for z in (B/'runs/server/udp-peers.jsonl').read_text().splitlines()]
 assert bound.isdisjoint(unbound) and {r['stack'] for r in peers}=={'baseline','queqiao'}
 assert all(r['source_ip_sha256'] in bound for r in peers)
 if execution['exit_code']==1:assert legacy==3
 return dict(validation='passed',native_wrapper_exit_code=execution['exit_code'],legacy_post_measurement_assertions=legacy,conditions=rows,
  binding_evidence=dict(native_spec='if:en0',probe_kernel_index=ref[0]['kernel_bound_if'],bound_source_hashes=sorted(bound),unbound_source_hashes=sorted(unbound),observed_remote_peers=len(peers),both_stacks_match_bound_source=True),
  boundary='Patched baseline socket creation only; real bound-interface native UDP. Zero callbacks can be a valid early cancel. Three legacy cases retain input SHA/length and read events, not a reconstructed PCM file. No acoustic/model cancel or cross-host time inference.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=B/'analysis.json');a=p.parse_args();a.out.write_text(json.dumps(analyze(),indent=2)+'\n')
