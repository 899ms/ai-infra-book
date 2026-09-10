"""Validate byte conservation and actual live receiver/sink/cancel events."""
import argparse,hashlib,json
from pathlib import Path
B=Path(__file__).absolute().parent

def analyze():
    fixture=(B/'fixture/audio.wav').read_bytes()[44:];sha=hashlib.sha256(fixture).hexdigest()
    execution=json.loads((B/'runs/execution.json').read_text());assert execution['exit_code']==0
    rows=[]
    for cancel in [False,True]:
      for round,pool in enumerate([True,False,False,True]):
       for stack in ['baseline','queqiao']:
        rel=f'cancel-{str(cancel).lower()}/round-{round}-pool-{str(pool).lower()}-{stack}'
        d=B/'runs'/rel;r=json.loads((d/'result.json').read_text());data=(d/'received.pcm').read_bytes();events=[json.loads(z) for z in (d/'events.jsonl').read_text().splitlines()]
        assert (r['stack'],r['pool'],r['intentional_cancel'])==(stack,pool,cancel)
        assert r['fixture_pcm_sha256']==sha and hashlib.sha256(data).hexdigest()==r['received_sha256']
        assert len(data)==r['received_bytes'] and data==fixture[:len(data)] and r['prefix_equal']
        last=-1
        for i,e in enumerate(events):assert e['event']==i and e['ns']>=last;last=e['ns']
        def kind(k):return [e for e in events if e['kind']==k]
        got=kind('client_frame');played=kind('sink_consume');sent=kind('origin_write')
        for group in [got,played,sent]:
         assert [e['frame'] for e in group]==list(range(len(group)))
         assert all(0<e['bytes']<=1764 for e in group)
        assert sum(e['bytes'] for e in got)==len(data)
        assert sum(e['bytes'] for e in played)==r['sink_bytes'] and len(played)==r['sink_frames']
        assert all(p['ns']>=got[p['frame']]['ns'] for p in played)
        assert played[0]['ns']>=got[2]['ns']  # Actual three-frame startup buffer.
        gaps=[];open_gap=None
        for e in events:
         if e['kind']=='sink_empty_start':assert open_gap is None;open_gap=e['ns']
         if e['kind']=='sink_empty_end':assert open_gap is not None;gaps.append(e['ns']-open_gap);open_gap=None
        assert open_gap is None
        call=kind('cancel_call');ret=kind('cancel_return');obs=kind('origin_reverse_read_end')
        if cancel:
         assert len(data)==17640 and len(call)==len(ret)==1 and not r['complete_pcm_equal']
         assert call[0]['ns']<=ret[0]['ns'] and len(kind('sink_cancelled'))==1
         assert not kind('origin_all_sent')
         observed=r['origin_reverse_read_end_ns']
         if observed is not None:
          assert len(obs)==1 and observed==obs[0]['ns'] and observed>=call[0]['ns']
          # Receiver close propagated to reverse read, not origin's local deadline.
          assert observed-call[0]['ns']<5_000_000_000 and 'timeout' not in obs[0]['note']
         propagation=None if observed is None else (observed-call[0]['ns'])/1e6
        else:
         assert data==fixture and r['complete_pcm_equal'] and sum(e['bytes'] for e in played)==len(fixture)
         assert sum(e['bytes'] for e in sent)==len(fixture) and len(kind('origin_all_sent'))==1
         assert len(got)==len(played)==672 and got[-1]['bytes']==100
         assert not call;propagation=None
        rows.append(dict(condition=rel,round=round,stack=stack,pool=pool,intentional_cancel=cancel,
            events=len(events),received_bytes=len(data),pcm_exact=not cancel and data==fixture,prefix_exact=True,
            first_complete_frame_ms=got[0]['ns']/1e6,software_sink_start_ms=played[0]['ns']/1e6,
            software_sink_bytes=r['sink_bytes'],software_sink_frames=r['sink_frames'],
            empty_buffer_waits=len(gaps),empty_buffer_waits_over_1ms=sum(g>1e6 for g in gaps),empty_buffer_wait_total_ms=sum(gaps)/1e6,
            cancel_to_origin_observation_ms=propagation,
            cancel_local_call_ms=None if not cancel else (ret[0]['ns']-call[0]['ns'])/1e6,
            origin_sent_bytes=sum(e['bytes'] for e in sent),physical_playback_ms=None,audible_stalls=None,model_cancel_ms=None))
    return dict(fixture_pcm_sha256=sha,conditions=rows,full_exact=sum(r['pcm_exact'] for r in rows),cancel_prefix_exact=sum(r['intentional_cancel'] and r['prefix_exact'] for r in rows),
       boundary='Actual loopback Queqiao/TUIC and live timer-paced software sink. Path emulated; no DAC, WAN, or model generation/cancellation.')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=B/'analysis.json');a=p.parse_args();a.out.write_text(json.dumps(analyze(),ensure_ascii=False,indent=2)+'\n')
