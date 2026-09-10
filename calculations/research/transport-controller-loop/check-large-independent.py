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
    expected_hash=manifest['result_sha256']; assert filehash(path)==expected_hash
    for filename,digest in manifest['code_hashes'].items():assert filehash(ROOT/filename)==digest
    reader=Reader(path); meta={};directions=('up','down')
    packets={d:{} for d in directions};offset={d:0 for d in directions};lastend={d:F(0) for d in directions}
    wire=Counter();kindcount=Counter();padding=Counter();lastdata={d:F(0) for d in directions};firstdata={}
    acked={d:{} for d in directions};snapshots={d:{} for d in directions};delivered={d:set() for d in directions}
    counts=Counter();phases={d:set() for d in directions};losses=Counter();times_cache={};send_cache={}
    def transmission(t):
        d=t['direction'];pn=t['pn'];assert pn==len(packets[d]);assert not t['dropped'] and not t['probe'] and t['recovery_of'] is None
        start,end,arr=map(F,(t['send_start'],t['send_end'],t['received_at']))
        assert start>=lastend[d];lastend[d]=end
        assert end-start==F(t['wire_bytes']*8,meta['inputs']['links'][d]['rate_bps'])
        assert arr==F(t['arrival'])==end+F('0.05')
        kind=t['kind'];assert kind in ('data','ack')
        assert t['quic_bytes']==(1200 if kind=='data' else 64) and t['wire_bytes']==t['quic_bytes']+28
        packets[d][pn]=(start,arr,kind,t['quic_bytes'])
        kindcount[d,kind]+=1;wire[d]+=t['wire_bytes']
        if kind=='data':
            assert len(t['frames'])==1;f=t['frames'][0];assert f['type']=='stream' and f['offset']==offset[d]
            assert f['length']==min(1168,(30000000 if d=='up' else 5000000)-offset[d]);offset[d]+=f['length']
            padding[d]+=1200-32-f['length'];lastdata[d]=arr;firstdata.setdefault(d,start)
    def sender_event(d,e):
        if e['type']!='ack':return
        for a,b in e['ranges']:
            for pn in range(a,b+1):
                assert pn in packets[d] and packets[d][pn][1]<=F(e['at'])
                acked[d].setdefault(pn,F(e['at']))
    def error(category,d,e):
        old,new,err=map(F,(e['original'],e['rounded'],e['local_error']));assert new-old==err
        if category=='pacer_errors':
            q=F(meta['inputs']['controller'].get('time_quantum','0.000000001')) if e['kind']=='ready_time_ceil' else F(meta['inputs']['controller'].get('debt_quantum','0.000000000001'))
            assert 0<=err<q and (new/q).denominator==1
        elif category=='controller_numeric_errors':
            q=F(meta['inputs']['controller'].get('controller_quantum','0.000000000001'))/1200
            assert abs(err)<=q/2 and new==round(old/q)*q
        else:assert abs(err)<=F(meta['inputs']['sender']['numeric_quantum'])
        counts[category]+=1
    def controller(d,e):
        name=meta['inputs']['controller']['name'];counts['controller_events']+=1
        if name=='cubic_hystart':
            state=e.get('state',{});phases[d].add(state.get('phase','unknown'));assert F(state['cwnd_bytes'])>0
            return
        assert name=='bbr';kind=e['event']
        if kind=='sent':
            r=e['record'];start,_,k,size=packets[d][r['pn']]
            assert F(r['at'])==start and r['sent_us']==1+int(start*1000000) and r['sent_bytes']==size
            assert r['counted']==(k=='data')
            if r['counted']:
                if d not in times_cache:times_cache[d]=sorted(t for pn,t in acked[d].items() if packets[d][pn][2]=='data')
                assert r['prior_delivered']==bisect_right(times_cache[d],start)
                snapshots[d][r['pn']]=r
        elif kind=='ack':
            fresh=e['newly_counted_pns'];at=F(e['at']);assert not delivered[d].intersection(fresh)
            assert all(acked[d][pn]==at for pn in fresh);delivered[d].update(fresh)
            selected=max(fresh,key=lambda pn:(snapshots[d][pn]['sent_us'],pn));assert e['selected_pn']==selected
            s=snapshots[d][selected];sample=e['sample'];inp=e['callback']['input']
            assert inp['total_delivered']==len(delivered[d]);delta=len(delivered[d])-s['prior_delivered']
            assert inp['now_us']==1+int(at*1000000)
            if d not in send_cache:send_cache[d]=sorted(t[0] for t in packets[d].values() if t[2]=='data')
            sent_so_far=bisect_left(send_cache[d],at)
            assert inp['inflight']==sent_so_far-len(delivered[d])
            assert inp['prior_inflight']==sent_so_far-len(delivered[d])+len(fresh)
            raw=at-packets[d][max(fresh)][0]
            assert inp['rtt_us']==int(raw*1000000)
            assert sample['delivered']==delta
            send=max(0,s['sent_us']-s['first_tx_us'])&0xffffffff
            recv=max(0,1+int(at*1000000)-s['delivered_mstamp_us'])&0xffffffff
            assert sample['snd_interval_us']==send and sample['rcv_interval_us']==recv
            if sample['valid']:
                assert sample['interval_us']==max(send,recv)
                assert sample['bw_scaled']==(delta<<24)//sample['interval_us']
            assert sample['is_app_limited']==s['app_limited']
            assert e['flow_limited_at_selected_send']==s['flow_limited']
            assert e['actual_sample_udp_bytes']==e['nominal_sample_quic_bytes']==delta*1200
            phases[d].add(e['callback']['state']['mode']);assert e['cwnd_bytes']>0
    array_keys={'transmissions','application_events','waits'}
    map_keys={'sender_events','losses','timers','numeric_errors','controller_events','controller_numeric_errors','pacer_errors','persistent_events'}
    def entry(key):
        if key in array_keys:
            reader.array(transmission if key=='transmissions' else lambda e:None)
        elif key in map_keys:
            def direction(d):
                def consume(e):
                    if key=='sender_events':sender_event(d,e)
                    elif key in ('numeric_errors','controller_numeric_errors','pacer_errors'):error(key,d,e)
                    elif key=='controller_events':controller(d,e)
                    elif key in ('losses','timers','persistent_events'):losses[key]+=1
                reader.array(consume)
            reader.object(direction)
        else:meta[key]=reader.value()
    reader.object(entry);reader.f.close()
    p=meta['inputs'];assert p['upload_bytes']==30000000 and p['response_bytes']==5000000 and F(p['model_seconds'])==F('.3')
    assert p['pad_in_flight'] is True and p['sender']['initial_cwnd']==12000
    assert p['links']=={'up':{'rate_bps':20000000,'propagation':'0.05'},'down':{'rate_bps':100000000,'propagation':'0.05'}}
    assert kindcount==Counter({('up','data'):25685,('down','data'):4281,('up','ack'):4281,('down','ack'):25685})
    assert wire==Counter(up=31935032,down=7620088) and padding==Counter(up=80,down=208)
    assert offset==dict(up=30000000,down=5000000) and not any(losses.values())
    assert meta['received_intervals']==dict(up=[[0,30000000]],down=[[0,5000000]])
    b=meta['business'];assert F(b['upload'])==F(b['model_start'])==lastdata['up']
    assert F(b['model_end'])==lastdata['up']+F('.3') and firstdata['down']>=F(b['model_end']) and F(b['response'])==lastdata['down']
    assert meta['summary']['complete'] and meta['summary']['wire_bytes']==39555120 and meta['summary']['unique_received_bytes']==35000000
    assert meta['summary']['pending_packets']==dict(up=0,down=0)
    for d in directions:
        st=meta['final_states'][d];assert st['bytes_in_flight']==0 and st['next_timer'] is None
        assert st['max_data_consumed']==offset[d]
        assert {pn for pn in acked[d] if packets[d][pn][2]=='data'}=={pn for pn in packets[d] if packets[d][pn][2]=='data'}
        if p['controller']['name']=='bbr':assert len(delivered[d])==kindcount[d,'data']
    assert filehash(path)==expected_hash
    for filename,digest in manifest['code_hashes'].items():assert filehash(ROOT/filename)==digest
    assert b==manifest['business'] and meta['summary']==manifest['summary']
    return dict(status='passed',source_hashes=manifest['code_hashes'],result_file=path.name,result_sha256=expected_hash,controller=p['controller']['name'],inputs=p,wire_bytes=dict(wire),padding_bytes=dict(padding),packets=sum(kindcount.values()),business=b,local_error_counts=dict(counts),observed_controller_phases={d:sorted(v) for d,v in phases.items()},scope='one full frozen trace; streaming physical, byte, numeric and controller-state audit')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('results',nargs='+',type=Path);a=ap.parse_args()
    for p in a.results:
        r=audit(p);out=ROOT/('large-independent-'+r['controller']+'.json');out.write_text(json.dumps(r,indent=2)+'\n');print(r['controller'],'PASS',r['business'],flush=True)
