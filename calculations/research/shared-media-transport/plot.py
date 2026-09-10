"""Render a traceable research timeline from one frozen scenario result.

Matplotlib is optional. Geometry represents recorded serialization and work;
propagation markers and application delivery points remain separate.
"""
import argparse
import hashlib
import json
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, required=True)
    parser.add_argument('--scenario', help='Key when the input contains a scenario map')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--until', help='Optional visible time limit, as exact rational seconds')
    args = parser.parse_args()
    raw = args.inputs.read_bytes()
    result = json.loads(raw)
    if args.scenario:
        result = result[args.scenario]
    assert result['calculation'] == 'shared-media-finite-teaching-transport'
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    exact = lambda value: float(Fraction(str(value)))
    resources = sorted({row['resource'] for row in result['work']})
    lanes = ['c2s link', 's2c link'] + ['compute: '+r for r in resources] + ['application']
    fig, ax = plt.subplots(figsize=(13, max(4.5, len(lanes)*0.75)))
    streams = sorted({row['stream'] for row in result['transmissions'] if row['kind']=='data'})
    colors = {name: plt.get_cmap('tab20')(i % 20) for i, name in enumerate(streams)}
    points = []
    for i, row in enumerate(result['transmissions']):
        y = 0 if row['direction']=='c2s' else 1
        start, end, arrival = [exact(row[k]) for k in ('start','end','arrival')]
        color = '#777777' if row['kind']=='ack' else colors[row['stream']]
        ax.broken_barh([(start,end-start)], (y-0.24,0.48), facecolors=color,
                      edgecolors='#333333' if row.get('lost') else color,
                      hatch='xx' if row.get('lost') else None)
        if not row.get('lost'):
            ax.plot([end,arrival],[y,y], color=color, alpha=0.35, linewidth=0.6)
            ax.plot(arrival,y,marker='|',color=color,markersize=4)
        points.append(dict(kind='transmission',index=i,packet=row['packet'],
                           start=row['start'],end=row['end'],arrival=row['arrival'],
                           lost=row.get('lost',False),lane=lanes[y]))
    work_groups=Counter(re.sub(r'-[0-9]+$', '', row['id']) for row in result['work'])
    labeled=set()
    for row in result['work']:
        y=2+resources.index(row['resource'])
        start,end=exact(row['start']),exact(row['end'])
        ax.broken_barh([(start,end-start)],(y-0.24,0.48),facecolors='#b08e42',edgecolors='#725c2e',linewidth=0.3)
        group=re.sub(r'-[0-9]+$', '', row['id'])
        if group not in labeled and (args.until is None or start <= exact(args.until)):
            label=group + (' ('+str(work_groups[group])+' blocks)' if work_groups[group]>1 else '')
            ax.text(start,y-0.29,label,fontsize=7,rotation=20,clip_on=True)
            labeled.add(group)
        points.append(dict(kind='work',id=row['id'],start=row['start'],end=row['end'],lane=lanes[y]))
    y=len(lanes)-1
    for index,row in enumerate(result['businesses']):
        for field in ('complete','first_play','playback_end'):
            if row.get(field) is not None and (args.until is None or exact(row[field]) <= exact(args.until)):
                at=exact(row[field])
                ax.plot(at,y,marker='o',markersize=4,color='#b3261e' if row.get('usable') is False else '#202020')
                ax.annotate(row['id']+':'+field,(at,y),xytext=(4,8+12*(index%3)),
                            textcoords='offset points',fontsize=7,rotation=20)
                points.append(dict(kind='business',id=row['id'],field=field,at=row[field],
                                   usable=row.get('usable'),lane='application'))
    if args.until is not None:
        ax.set_xlim(0,exact(args.until))
    ax.set_yticks(range(len(lanes)),lanes)
    ax.set_ylim(len(lanes)-0.4,-0.8)
    ax.set_xlabel('Time (seconds); bars = serialization/work, thin lines = propagation')
    ax.set_title((args.scenario or 'Shared media')+' — declared teaching transport')
    ax.grid(axis='x',alpha=0.2)
    if len(streams)<=12:
        handles=[Patch(color=colors[s],label=s) for s in streams]+[Patch(color='#777777',label='ACK')]
        ax.legend(handles=handles,loc='upper left',bbox_to_anchor=(1.01,1),fontsize=8)
    fig.text(0.01,0.01,'Red application point = unusable result. Expiry/cancellation do not refund sent bytes. Not measured TCP/QUIC performance.',fontsize=8)
    fig.tight_layout(rect=(0,0.04,1,1))
    args.output.mkdir(parents=True,exist_ok=True)
    for suffix in ('png','svg'):
        fig.savefig(args.output/('timeline.'+suffix),dpi=160)
    plt.close(fig)
    data=dict(scenario=args.scenario,visible_until=args.until,scope='Research timeline; one panel of planned figure 12-4',points=points,
              input_sha256=hashlib.sha256(raw).hexdigest())
    (args.output/'data.json').write_text(json.dumps(data,indent=2)+'\n')
    paths=[args.output/name for name in ('timeline.png','timeline.svg','data.json')]
    manifest=dict(input=str(args.inputs),input_sha256=data['input_sha256'],
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  calculator_sha256=hashlib.sha256((Path(__file__).parent/'calculate.py').read_bytes()).hexdigest(),
                  source_lock_sha256=hashlib.sha256((Path(__file__).parent/'sources.lock.json').read_bytes()).hexdigest(),
                  artifacts={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    (args.output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(dict(status='rendered',points=len(points),output=str(args.output))))


if __name__=='__main__':
    main()
