"""Read-only figure extraction/semantics check; never render or call verify."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent.parent
sys.path.insert(0,str(PROJECT/'src'))
from infra_calc import media_feedback_plot as plot

source=Path(plot.__file__)
source_before=hashlib.sha256(source.read_bytes()).hexdigest()
extracted=plot.extract()
saved=json.loads((plot.DIRECTORY/'data.json').read_text())['cases']
assert saved==extracted, 'saved figure payload differs from current official inputs'
checks=[]
for row in extracted:
    path=PROJECT/f"results/media-feedback-{row['name']}.json"
    raw=path.read_bytes()
    result=json.loads(raw)
    app=result['inputs']['application']
    delivered={k:F(v) for k,v in result['delivered'].items()}
    image=next(o for o in app['business_observers'] if o['kind']=='image')
    image_time=max(delivered[d['id']] for d in image['completion_dependencies'])
    assert image_time==F(row['image']['complete_at'])
    assert image_time<17 # Panel A fixed axis bound includes all actual labels.
    audio=next(o for o in app['business_observers'] if o['kind']=='tts')
    until=F(str(result['inputs']['network']['until']))
    independently_played=F(0)
    independently_missing=F(0)
    offered_duration=F(0)
    first=None
    for block in audio['blocks']:
        duration=F(block['duration_seconds']); slot=F(block['slot_start_seconds'])
        offered_duration+=duration
        eligible=slot<=until and all(identity in delivered and delivered[identity]<=slot for identity in block['message_ids'])
        if eligible:
            independently_played+=min(duration,until-slot)
            if first is None:first=slot
        elif slot<=until:
            independently_missing+=min(duration,until-slot)
    # Current four complete-horizon cases have no partially played block.
    plotted_played=sum(F(b['play_end'])-F(b['play_start']) for b in row['audio']['blocks'] if b['play_start'] is not None and b['play_end'] is not None)
    assert offered_duration==F(4,25)
    assert plotted_played==independently_played
    assert F(row['audio']['missing_audio_seconds'])==independently_missing
    assert independently_played+independently_missing==offered_duration
    assert (None if row['audio']['first_play'] is None else F(row['audio']['first_play']))==first
    assert not row['screenshot']['all_required_delivered'] and not row['screenshot']['usable']
    selected=[{k:t.get(k) for k in ('direction','pn','kind','message_id','send_start','send_end','received_at')}
              for t in result['transmissions'] if F(t['send_start'])<=F(1,2)]
    assert selected==row['early_transmissions']
    counts={d:{kind:sum(t['direction']==d and (t['kind']=='ack')==(kind=='ack') for t in selected)
               for kind in ('ack','non_ack')} for d in ('up','down')}
    assert result['inputs']['network']['links']=={'up':{'rate_bps':20000000,'propagation':'0.05'},'down':{'rate_bps':100000000,'propagation':'0.05'}}
    assert app['scheduling']['compute']=='fifo'
    checks.append(dict(case=row['name'],result_sha256=hashlib.sha256(raw).hexdigest(),
                       image_complete_exact=str(image_time),image_label=f'{float(image_time):.6f} s',
                       played_exact=str(plotted_played),missing_exact=str(independently_missing),
                       first_play_exact=None if first is None else str(first),
                       early_marker_counts=counts,screenshot_usable=False))
assert source_before==hashlib.sha256(source.read_bytes()).hexdigest()
assert 'upper lane: download; lower: upload' in source.read_text()
report=dict(status='PASS',checks=checks,plot_source_sha256=source_before,
            saved_png_sha256=hashlib.sha256((plot.DIRECTORY/'figure.png').read_bytes()).hexdigest(),
            saved_data_sha256=hashlib.sha256((plot.DIRECTORY/'data.json').read_bytes()).hexdigest(),
            checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            visual_review='Saved first PNG inspected. Known old x-label swaps directions; current source already says upper download/lower upload. No additional visible error found.',
            semantics={'panel_A':'Required final-image messages fully delivered at client; rounded6-decimal labels',
                       'panel_B':'Independent slot eligibility reproduces all played/missing durations; full-horizon cases have no partial playback',
                       'panel_C':'Only send_start<=.5 included; bars are actual non-ACK serializer intervals, gray vertical ticks ACK start only. Inverted y makes negative offset/down upper and positive offset/up lower.'},
            limits=['ACK ticks do not draw ACK service width and cannot be read as occupancy.',
                    'Current played formula sums completed blocks; do not generalize to a horizon truncating a currently-playing block without updating extraction.',
                    'No render, verify, public edit, or stale manifest bypass was performed.'])
(ROOT/'figure-data-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(status='PASS',cases=len(checks),plot_source_sha256=source_before,checks=checks)))
