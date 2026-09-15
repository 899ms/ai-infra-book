import gzip,hashlib,json,statistics
from pathlib import Path
R=Path(__file__).resolve().parent
D=R/'results'
order=json.loads((D/'order.json').read_text())
assert len(order)==9 and {(r['trial'],r['mode']) for r in order}=={(t,m) for t in range(3) for m in ['recorded','coalesce64k','whole']}
assert json.loads((D/'completion.json').read_text())==dict(subruns=9,exit_codes=[0]*9)
executions=json.loads((D/'executions.json').read_text())
assert [(r['trial'],r['mode']) for r in executions]==[(r['trial'],r['mode']) for r in order]
assert all(r['exit_code']==0 and r['start_ns']<r['end_ns'] for r in executions)
baseline=json.loads((R.parent/'tts-network/tts-fixture.json').read_text())
request_hash=hashlib.sha256((R/'request.json').read_bytes()).hexdigest()
audio_hash=hashlib.sha256((R/'audio.wav').read_bytes()).hexdigest()
records=[]
for setting in order:
    name=f"trial{setting['trial']}-{setting['mode']}"
    folder=D/name
    fixture=json.loads((R/(setting['mode']+'-fixture.json')).read_text())
    assert fixture['baseline_fixture_sha256']==hashlib.sha256((R.parent/'tts-network/tts-fixture.json').read_bytes()).hexdigest()
    offset=0
    for part in fixture['release_plan']:
        assert part['offset']==offset
        offset+=part['bytes']
        expected=next(r['ready_s'] for r in baseline['release_plan'] if r['offset']+r['bytes']>=offset)
        assert part['ready_s']==expected
    assert offset==(R/'audio.wav').stat().st_size
    env=json.loads((folder/'environment.json').read_text())
    assert env['fixture']==fixture and not env['smoke']
    assert env['source_sha256']==hashlib.sha256((R/'run_network.py').read_bytes()).hexdigest()
    assert env['payload_sha256']==request_hash and env['response_sha256']==audio_hash
    for phase in ['before','after']:
        q=json.loads((D/(name+'-'+phase+'.json')).read_text())
        assert len(q)==1 and q[0]['kind']=='netem'
        options=q[0]['options']
        assert options['delay']['delay']==.04 and options['rate']['rate']==2500000 and options['loss-random']['loss']==.001
        assert q[0]['backlog']==q[0]['qlen']==0
    complete=json.loads((folder/'completion.json').read_text())
    assert complete==dict(done=True,requests=10,failures=0,listeners_closed=True)
    assert not json.loads((folder/'server-errors.json').read_text())
    connections={r['id']:r for r in json.loads((folder/'connections.json').read_text())}
    assert len(connections)==8
    for c in connections.values():
        assert c['start']<=c['ready']<=c['closed'] and not c['session_resumed']
        assert c['alpn']==('http/1.1' if c['protocol']=='h1' else 'h3')
        if c['protocol']=='h1':assert c['tls']=='TLSv1.3' and c['certificate_sha256']==env['certificate_sha256']
        else:assert not c['early_data_accepted']
    for proto in ['h1','h3']:
        servers=json.loads((folder/(proto+'-server.json')).read_text())
        assert len(servers)==5
        for server in servers:
            assert server['sha256']==request_hash and server['bytes']==env['payload_bytes']
            assert len(server['releases'])==len(fixture['release_plan'])
            for actual,planned in zip(server['releases'],fixture['release_plan']):
                assert (actual['offset'],actual['bytes'])==(planned['offset'],planned['bytes'])
                assert actual['at']-server['service_start']>=planned['ready_s']
    raw=[json.loads(x) for x in (folder/'requests.jsonl').read_text().splitlines()]
    assert len(raw)==10
    for row in raw:
        assert row['valid'] and row['error'] is None and row['sha256']==audio_hash and row['bytes']==env['response_bytes']
        assert row['start']<=row['connection_ready']<=row['send']<=row['first_headers']<=row['first_data']<=row['end']<=row['validation_end']
        assert connections[row['connection']]['protocol']==row['protocol']
        offset=0
        for arrival in row['arrivals']:
            offset+=arrival['bytes'];assert offset==arrival['total']
        assert offset==env['response_bytes']
        first=next(e['at'] for e in row['arrivals'] if e['total']>=1808)
        three=next(e['at'] for e in row['arrivals'] if e['total']>=5336)
        records.append(dict(mode=setting['mode'],trial=setting['trial'],protocol=row['protocol'],reuse=row['reuse'],warmup=row['warmup'],index=row['index'],
                            first_frame_ms=(first-row['start'])*1000,three_frames_ms=(three-row['start'])*1000,
                            first_body_ms=(row['first_data']-row['start'])*1000,complete_ms=(row['validation_end']-row['start'])*1000))
    for proto in ['h1','h3']:
        for reuse in [False,True]:
            pair=sorted((r for r in raw if not r['warmup'] and r['protocol']==proto and r['reuse']==reuse),key=lambda r:r['index'])
            assert len(pair)==2 and all(r['trial']==setting['trial'] for r in pair)
            assert pair[0]['validation_end']<=pair[1]['start']
            assert len({r['connection'] for r in pair})==(1 if reuse else 2)
    responses=0
    for path in folder.glob('qlog-*.json.gz'):
        for trace in json.load(gzip.open(path,'rt'))['traces']:
            for event in trace['events']:
                if event['name']=='http:frame_parsed' and event['data']['frame']['frame_type']=='headers':
                    headers={h['name']:h['value'] for h in event['data']['frame']['headers']}
                    assert headers[':status']=='200';responses+=1
    assert responses==5
groups=[]
for mode in ['recorded','coalesce64k','whole']:
    for proto in ['h1','h3']:
        for reuse in [False,True]:
            rows=[r for r in records if not r['warmup'] and (r['mode'],r['protocol'],r['reuse'])==(mode,proto,reuse)]
            assert len(rows)==6
            groups.append(dict(mode=mode,protocol=proto,reuse=reuse,requests=len(rows),**{k:statistics.median(r[k] for r in rows) for k in ['first_body_ms','first_frame_ms','three_frames_ms','complete_ms']}))
result=dict(status='90 verified TTS chunk-policy transfers',formal_requests=72,warmups=18,groups=groups,records=records,
            scope='Real HTTP transfer with fixed source availability replay; not GPU synthesis or acoustic playback')
(R/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(groups,indent=2))
