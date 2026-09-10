"""Streaming audit of complete frozen 30MB controller results, not summaries."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from bisect import bisect_right,bisect_left
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parent

class Reader:
    def __init__(self,path):self.f=path.open();self.buf='';self.pos=0;self.eof=False;self.decoder=json.JSONDecoder()
    def fill(self):
        self.buf=self.buf[self.pos:]+self.f.read(65536);self.pos=0
        if not self.buf:self.eof=True
    def white(self):
        while True:
            while self.pos<len(self.buf) and self.buf[self.pos].isspace():self.pos+=1
            if self.pos<len(self.buf):return
            self.fill()
            if self.eof:return
    def char(self,c):
        self.white();assert self.buf[self.pos:self.pos+1]==c,(c,self.buf[self.pos:self.pos+30]);self.pos+=1
    def value(self):
        self.white()
        while True:
            try:v,end=self.decoder.raw_decode(self.buf,self.pos);self.pos=end;return v
            except json.JSONDecodeError:
                remaining=self.buf[self.pos:];chunk=self.f.read(65536)
                if not chunk:raise
                self.buf=remaining+chunk;self.pos=0
    def array(self,consume):
        self.char('[');self.white()
        if self.buf[self.pos:self.pos+1]==']':self.pos+=1;return
        while True:
            consume(self.value());self.white()
            if self.buf[self.pos:self.pos+1]==']':self.pos+=1;return
            self.char(',')
    def object(self,consume):
        self.char('{');self.white()
        if self.buf[self.pos:self.pos+1]=='}':self.pos+=1;return
        while True:
            key=self.value();self.char(':');consume(key);self.white()
            if self.buf[self.pos:self.pos+1]=='}':self.pos+=1;return
            self.char(',')

def filehash(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        while chunk:=f.read(1048576):h.update(chunk)
    return h.hexdigest()

def audit(path):
    manifest=json.loads(path.with_name(path.name.replace('-result.json','-manifest.json')).read_text())
    digest=filehash(path);assert digest==manifest['result_sha256']
    for p,h in manifest['code_hashes'].items():assert filehash(Path(p))==h
    reader=Reader(path);meta={};ds=('up','down');packets={d:[] for d in ds};acks={d:[] for d in ds};ackinputs={d:[] for d in ds};counts=Counter();wire=Counter();padding=Counter();offset=Counter();lastend={d:F(0) for d in ds};lastdata={};firstdata={};phases={d:set() for d in ds};lossclasses=Counter();errors=Counter();maxerrors={};loss_times={d:{} for d in ds};samples={d:[] for d in ds};firstacked={d:{} for d in ds};bbrdelivery={d:set() for d in ds};send_snapshots={d:{} for d in ds};bbr_rtts={d:[] for d in ds};acktimes_cache={};sendtimes_cache={}
    def tx(t):
        d=t['direction'];assert t['pn']==len(packets[d]);assert not t['dropped'] and not t['probe'] and t['recovery_of'] is None
        start,end,arr=map(F,(t['send_start'],t['send_end'],t['received_at']));assert start>=lastend[d];lastend[d]=end
        assert end-start==F(t['wire_bytes']*8,meta['inputs']['links'][d]['rate_bps']);assert arr==end+F('.05')==F(t['arrival'])
        k=t['kind'];assert k in ('data','ack');assert t['quic_bytes']==(1200 if k=='data' else 64);assert t['wire_bytes']==t['quic_bytes']+28
        packets[d].append((start,arr,k));counts[d,k]+=1;wire[d]+=t['wire_bytes']
        if k=='data':
            f,=t['frames'];assert f['offset']==offset[d] and f['length']==min(1168,(30000000 if d=='up' else 5000000)-offset[d]);offset[d]+=f['length'];padding[d]+=1168-f['length'];lastdata[d]=arr;firstdata.setdefault(d,start)
        else:acks['down' if d=='up' else 'up'].append((start,arr,t['ack_snapshot']))
    def event(key,d,e):
        if key=='sender_events' and e['type']=='ack':
            ackinputs[d].append(e)
            for lo,hi in e['ranges']:
                for pn in range(lo,hi+1):firstacked[d].setdefault(pn,F(e['at']))
        elif key=='rtt_samples':samples[d].append(e)
        elif key=='losses':
            for pn in e['pns'] if 'pns' in e else [e['pn']]:lossclasses[d,packets[d][pn][2]]+=1;loss_times[d][pn]=F(e['at'])
        elif key=='timers':assert False,('unexpected timer',e)
        elif key in ('numeric_errors','pacer_errors','controller_numeric_errors'):
            old,new,err=map(F,(e['original'],e['rounded'],e['local_error']));assert new-old==err
            if key=='pacer_errors':
                q=F(meta['inputs']['controller'].get('time_quantum','0.000000001')) if e['kind']=='ready_time_ceil' else F(meta['inputs']['controller'].get('debt_quantum','0.000000000001'));assert 0<=err<q and (new/q).denominator==1
            elif key=='controller_numeric_errors':
                q=F(meta['inputs']['controller'].get('controller_quantum','0.000000000001'))/1200;assert abs(err)<=q/2 and new==round(old/q)*q
            else:assert abs(err)<=F(meta['inputs']['sender']['numeric_quantum'])
            errors[key]+=1;maxerrors[key]=max(maxerrors.get(key,F(0)),abs(err))
        elif key=='controller_events':
            counts['controller_events']+=1
            if meta['inputs']['controller']['name']=='cubic_hystart':phases[d].add(e.get('state',{}).get('phase','unknown'))
            elif meta['inputs']['controller']['name']=='bbr' and e['event']=='sent':
                rec=e['record'];pn=rec['pn'];t=packets[d][pn];assert F(rec['at'])==t[0] and rec['sent_us']==1+int(t[0]*1000000)
                assert rec['counted']==(t[2]=='data')
                if rec['counted']:
                    if d not in acktimes_cache:acktimes_cache[d]=sorted(at for n,at in firstacked[d].items() if packets[d][n][2]=='data')
                    assert rec['prior_delivered']==bisect_right(acktimes_cache[d],t[0]);send_snapshots[d][pn]=rec
            elif meta['inputs']['controller']['name']=='bbr' and e['event']=='ack':
                fresh=e['newly_counted_pns'];assert not bbrdelivery[d].intersection(fresh);assert all(packets[d][pn][2]=='data' and firstacked[d][pn]==F(e['at']) for pn in fresh);bbrdelivery[d].update(fresh)
                inp=e['callback']['input'];assert inp['total_delivered']==len(bbrdelivery[d]);phases[d].add(e['callback']['state']['mode'])
                selected=max(fresh,key=lambda pn:(send_snapshots[d][pn]['sent_us'],pn));assert selected==e['selected_pn'];snap=send_snapshots[d][selected];assert all(e['selected_send_snapshot'][k]==v for k,v in snap.items() if k not in ('acked','lost','flight_released')),[(k,v,e['selected_send_snapshot'].get(k)) for k,v in snap.items() if e['selected_send_snapshot'].get(k)!=v]
                at=F(e['at']);nowus=1+int(at*1000000);delta=len(bbrdelivery[d])-snap['prior_delivered'];sample=e['sample']
                assert inp['now_us']==nowus and sample['delivered']==delta
                snd=max(0,snap['sent_us']-snap['first_tx_us'])&0xffffffff;rcv=max(0,nowus-snap['delivered_mstamp_us'])&0xffffffff
                assert sample['snd_interval_us']==snd and sample['rcv_interval_us']==rcv
                if sample['valid']:assert sample['interval_us']==max(snd,rcv) and sample['bw_scaled']==(delta<<24)//max(snd,rcv)
                assert sample['is_app_limited']==snap['app_limited'] and e['flow_limited_at_selected_send']==snap['flow_limited']
                assert e['actual_sample_udp_bytes']==e['nominal_sample_quic_bytes']==delta*1200
                if d not in sendtimes_cache:sendtimes_cache[d]=sorted(t[0] for t in packets[d] if t[2]=='data')
                sent=bisect_left(sendtimes_cache[d],at);assert inp['inflight']==sent-len(bbrdelivery[d]);assert inp['prior_inflight']==sent-len(bbrdelivery[d])+len(fresh)
                bbr_rtts[d].append((at,inp['rtt_us']))
    maps={'sender_events','losses','timers','numeric_errors','controller_events','pacer_errors','controller_numeric_errors','ack_events','persistent_events','rtt_samples'}
    def entry(k):
        if k=='transmissions':reader.array(tx)
        elif k in ('application_events','waits'):reader.array(lambda e:None)
        elif k in maps:reader.object(lambda d:reader.array(lambda e:event(k,d,e)))
        else:meta[k]=reader.value()
    reader.object(entry);reader.f.close()
    p=meta['inputs'];assert p['upload_bytes']==30000000 and p['response_bytes']==5000000 and F(p['model_seconds'])==F('.3');assert p['pad_in_flight'] is True
    assert p['ack_policy']['every']==2 and F(p['ack_policy']['max_delay'])==F('.01');assert p['links']=={'up':{'rate_bps':20000000,'propagation':'0.05'},'down':{'rate_bps':100000000,'propagation':'0.05'}}
    def vi(n):return 1 if n<64 else 2 if n<16384 else 4 if n<2**30 else 8
    overrun=0;maxraw=F(0);maxframe=0;eligibility=Counter()
    for d in ds:
        arrived=[t[1] for t in packets[d]];previous_n=0;seenack=set();rtt_expected=[];minimum=None;srtt=None;variance=None;q=F(p['sender']['numeric_quantum']);assert len(acks[d])==len(ackinputs[d])
        for (start,at,s),inp in zip(acks[d],ackinputs[d]):
            n=bisect_right(arrived,start);pending={pn for pn in range(previous_n,n) if packets[d][pn][2]=='data'};expected=set(range(max(0,n-256),n))|pending
            claimed={pn for lo,hi in s['ranges'] for pn in range(lo,hi+1)};assert claimed==expected;previous_n=n
            assert s['covered_pending']==len(pending);largest=max(claimed);raw=start-arrived[largest];tick=F(2**s['delay_exponent'],1000000)
            assert s['largest']==largest and F(s['raw_delay'])==raw and F(s['largest_received_at'])==arrived[largest]
            assert s['encoded_delay']==raw//tick and F(s['decoded_delay'])==s['encoded_delay']*tick and F(s['encoding_error'])==F(s['decoded_delay'])-raw
            assert 0<=raw-F(s['decoded_delay'])<tick;assert s['exceeds_max_delay']==(raw>F('.01'));overrun+=s['exceeds_max_delay'];maxraw=max(maxraw,raw)
            ranges=list(reversed(s['ranges']));fields=[2,largest,s['encoded_delay'],len(ranges)-1,ranges[0][1]-ranges[0][0]]
            for a,b in zip(ranges,ranges[1:]):fields += [a[0]-b[1]-2,b[1]-b[0]]
            frame=sum(vi(v) for v in fields);assert frame==s['frame_bytes'] and frame+s['header_tag_bytes']<=64;maxframe=max(maxframe,frame)
            assert F(inp['at'])==at and inp['ranges']==s['ranges'] and F(inp['ack_delay'])==F(s['decoded_delay'])
            fresh={pn for pn in claimed-seenack if pn not in loss_times[d] or loss_times[d][pn]>=at};sample=largest in fresh and any(packets[d][pn][2]=='data' for pn in fresh);eligibility['eligible' if sample else 'ineligible']+=1
            if sample and packets[d][largest][2]=='ack':eligibility['largest_pure_ack']+=1
            if sample:
                raw_rtt=at-packets[d][largest][0];adjusted=raw_rtt
                if minimum is None:minimum=raw_rtt;srtt=raw_rtt;variance=raw_rtt/2
                else:
                    minimum=min(minimum,raw_rtt);bounded=min(F(s['decoded_delay']),F('.01'))
                    if raw_rtt>=minimum+bounded:adjusted=raw_rtt-bounded
                    variance=F(3,4)*variance+F(1,4)*abs(srtt-adjusted);srtt=F(7,8)*srtt+F(1,8)*adjusted
                rtt_expected.append(dict(at=at,pn=largest,raw=raw_rtt,adjusted=adjusted,smoothed=srtt,rttvar=variance))
                srtt=round(srtt/q)*q;variance=round(variance/q)*q
            seenack.update(claimed)
        assert len(samples[d])==len(rtt_expected),(d,len(samples[d]),len(rtt_expected))
        for actual,expected_sample in zip(samples[d],rtt_expected):
            for key,value in expected_sample.items():assert F(actual[key])==value,(d,key,actual,expected_sample)
        sample_by_time={e['at']:e for e in rtt_expected}
        for at,us in bbr_rtts[d]:assert us==(int(sample_by_time[at]['raw']*1000000) if at in sample_by_time else -1),(at,us,sample_by_time.get(at))
        assert F(meta['final_states'][d]['min_rtt'])==minimum
        assert {pn for pn,t in enumerate(packets[d]) if t[2]=='data'}<=seenack
        if p['controller']['name']=='bbr':assert len(bbrdelivery[d])==counts[d,'data']
        st=meta['final_states'][d];assert st['bytes_in_flight']==0 and st['next_timer'] is None
    assert counts['up','data']==25685 and counts['down','data']==4281 and padding==Counter(up=80,down=208)
    assert not lossclasses['up','data'] and not lossclasses['down','data']
    ackcount=counts['up','ack']+counts['down','ack'];assert sum(wire.values())==36798248+92*ackcount
    b=meta['business'];assert F(b['upload'])==F(b['model_start'])==lastdata['up'];assert F(b['model_end'])==lastdata['up']+F('.3');assert firstdata['down']>=F(b['model_end']);assert F(b['response'])==lastdata['down']
    assert meta['received_intervals']=={'up':[[0,30000000]],'down':[[0,5000000]]};assert meta['summary']['complete'] and meta['summary']['unique_received_bytes']==35000000
    assert filehash(path)==digest
    for fn,h in manifest['code_hashes'].items():assert filehash(Path(fn))==h
    return dict(status='PASS',controller=p['controller']['name'],result_sha256=digest,source_hashes=manifest['code_hashes'],business=b,counts={str(k):v for k,v in counts.items()},wire_bytes=dict(wire),ack_count=ackcount,ack_overruns=overrun,max_raw_ack_delay=str(maxraw),max_ack_frame_bytes=maxframe,loss_identity_classes={str(k):v for k,v in lossclasses.items()},rtt_eligibility_independently_derived=dict(eligibility),local_error_counts=dict(errors),max_absolute_local_errors={k:str(v) for k,v in maxerrors.items()},observed_phases={d:sorted(v) for d,v in phases.items()},rtt_samples_compared={d:len(samples[d]) for d in ds},limits='All actual sender RTT samples independently compared against wire, eligibility, delay cap, old-SRTT variance and declared quantization. BBR actual send snapshots, first-ACK delivery, selected PN, send/ACK interval, integer bandwidth, app/flow flags, pre/post flight and raw RTT callback checked (adapter explicitly selects raw, separately from sender adjusted RTT); not full Linux TCP implementation proof.')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('results',nargs='+',type=Path);a=ap.parse_args()
    for p in a.results:
        r=audit(p);(ROOT/('large-independent-'+r['controller']+'.json')).write_text(json.dumps(r,indent=2)+'\n');print(r['controller'],r['status'],r['ack_count'],r['wire_bytes'],flush=True)
