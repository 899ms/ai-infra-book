package main

import (
 "bytes"
 "context"
 "crypto/sha256"
 "encoding/hex"
 "encoding/json"
 "fmt"
 "io"
 "net"
 "os"
 "path/filepath"
 "sync"
 "testing"
 "time"
 "github.com/bojieli/queqiao/internal/pathsim"
)

type bookLog struct { mu sync.Mutex; start time.Time; file *os.File; index int }
func (l *bookLog) event(kind string, index int, size int, note string) int64 {
 l.mu.Lock(); defer l.mu.Unlock()
 ns:=time.Since(l.start).Nanoseconds()
 row:=map[string]any{"event":l.index,"kind":kind,"frame":index,"bytes":size,"ns":ns,"note":note}
 if err:=json.NewEncoder(l.file).Encode(row);err!=nil {panic(err)}; l.index++;return ns
}
func bookSave(path string,v any) { data,err:=json.MarshalIndent(v,"","  ");if err!=nil {panic(err)};if err=os.WriteFile(path,append(data,'\n'),0600);err!=nil {panic(err)} }
func bookHash(x []byte) string {s:=sha256.Sum256(x);return hex.EncodeToString(s[:])}

func bookCase(t *testing.T, root string, pcm []byte, stack string,pool,cancelRun bool) {
 ctx,stop:=context.WithTimeout(context.Background(),45*time.Second);defer stop()
 opts:=options{congestion:"bbr-tuic",quicPool:pool}
 cfg:=pathsim.Config{OneWayDelay:20*time.Millisecond,RateBytesPerSec:12500000,QueueBytes:500000,Seed:1207}
 h,err:=startStack(ctx,stack,opts,cfg);if err!=nil {t.Fatal(err)};defer h.Close()
 warm,err:=newOrigin(1024);if err!=nil {t.Fatal(err)}
 err=warmUp(ctx,h.socks,warm);warm.Close();if err!=nil {t.Fatal(err)}
 listener,err:=net.Listen("tcp","127.0.0.1:0");if err!=nil {t.Fatal(err)};defer listener.Close()
 f,err:=os.Create(filepath.Join(root,"events.jsonl"));if err!=nil {t.Fatal(err)};defer f.Close()
 log:=&bookLog{start:time.Now(),file:f}
 originDone:=make(chan struct{});originObserved:=make(chan int64,1)
 go func(){
  defer close(originDone)
  c,e:=listener.Accept();if e!=nil {log.event("origin_accept_error",0,0,e.Error());return};defer c.Close()
  _=c.SetDeadline(time.Now().Add(35*time.Second));var req [1]byte
  if _,e=io.ReadFull(c,req[:]);e!=nil || req[0]!='g' {log.event("origin_request_error",0,0,fmt.Sprint(e));return}
  log.event("origin_request",0,1,"");peerClosed:=make(chan struct{});watchDone:=make(chan struct{})
  go func(){defer close(watchDone);var b [1]byte;n,e:=c.Read(b[:]);ns:=log.event("origin_reverse_read_end",0,n,fmt.Sprint(e));originObserved<-ns;close(peerClosed)}()
  sourceStart:=time.Now()
  for offset,index:=0,0;offset<len(pcm);index++ {
   wait:=time.Until(sourceStart.Add(time.Duration(index)*20*time.Millisecond))
   if wait>0 { select {case <-time.After(wait):case <-peerClosed:log.event("origin_stop_peer",index,0,"");return;case <-ctx.Done():return} }
   select {case <-peerClosed:log.event("origin_stop_peer",index,0,"");return;default:}
   end:=offset+1764;if end>len(pcm){end=len(pcm)}
   n,e:=c.Write(pcm[offset:end]);log.event("origin_write",index,n,fmt.Sprint(e));offset+=n
   if e!=nil || offset!=end{return}
  }
  log.event("origin_all_sent",0,len(pcm),"");_ = c.Close();<-watchDone
 }()
 c,err:=net.DialTimeout("tcp",h.socks,5*time.Second);if err!=nil {t.Fatal(err)};defer c.Close()
 _=c.SetDeadline(time.Now().Add(35*time.Second))
 if err=socksConnect(c,listener.Addr().String());err!=nil {t.Fatal(err)}
 log.event("socks_connected",0,0,"");if _,err=c.Write([]byte{'g'});err!=nil {t.Fatal(err)}
 type frame struct{ index,n int }
 type readResult struct{ data []byte; err string }
 queue:=make(chan frame,2048);received:=make(chan readResult,1);cancelled:=make(chan struct{})
 go func(){
  defer close(queue);var collected []byte
  for i:=0;;i++ {
   buf:=make([]byte,1764);n,e:=io.ReadFull(c,buf)
   if n>0 {collected=append(collected,buf[:n]...);log.event("client_frame",i,n,"");queue<-frame{i,n}}
   if cancelRun && i==9 && n==1764 {
    log.event("cancel_call",i,0,"");_ = c.Close();log.event("cancel_return",i,0,"");close(cancelled);received<-readResult{collected,"intentional_cancel"};return
   }
   if e!=nil {log.event("client_read_end",i,n,e.Error());received<-readResult{collected,e.Error()};return}
  }
 }()
 // Live software sink: three-frame prebuffer, then actual timer-paced consumption.
 pending:=[]frame{}
 for len(pending)<3 {v,ok:=<-queue;if !ok{break};pending=append(pending,v)}
 played:=0;playBytes:=0;stopped:=false
 for !stopped {
  select {case <-cancelled:log.event("sink_cancelled",played,playBytes,"");stopped=true;continue;default:}
  var v frame;var ok bool
  if len(pending)>0 {v=pending[0];pending=pending[1:];ok=true} else {
   select {case v,ok=<-queue:default:
    log.event("sink_empty_start",played,0,"")
    select {case v,ok=<-queue:case <-cancelled:log.event("sink_cancelled",played,playBytes,"");stopped=true;case <-ctx.Done():t.Fatal(ctx.Err())}
    log.event("sink_empty_end",played,0,"")
   }
  }
  if stopped{break};if !ok{log.event("sink_eof",played,playBytes,"");break}
  log.event("sink_consume",v.index,v.n,"");played++;playBytes+=v.n
  select {case <-time.After(time.Duration(v.n)*time.Second/88200):case <-cancelled:log.event("sink_cancelled",played,playBytes,"");stopped=true;case <-ctx.Done():t.Fatal(ctx.Err())}
 }
 result:=<-received;_ = c.Close()
 var observed any=nil
 select {case ns:=<-originObserved:observed=ns;case <-time.After(5*time.Second):log.event("origin_close_unobserved",0,0,"")}
 select {case <-originDone:case <-time.After(5*time.Second):t.Fatal("origin writer did not stop")}
 up,down:=h.relay.Stats();log.event("case_end",0,0,"")
 if err=os.WriteFile(filepath.Join(root,"received.pcm"),result.data,0600);err!=nil{t.Fatal(err)}
 exact:=bytes.Equal(result.data,pcm);prefix:=bytes.Equal(result.data,pcm[:len(result.data)])
 bookSave(filepath.Join(root,"result.json"),map[string]any{"stack":stack,"pool":pool,"intentional_cancel":cancelRun,"received_bytes":len(result.data),"received_sha256":bookHash(result.data),"fixture_pcm_sha256":bookHash(pcm),"complete_pcm_equal":exact,"prefix_equal":prefix,"reader_end":result.err,"sink_frames":played,"sink_bytes":playBytes,"origin_reverse_read_end_ns":observed,"upstream":up,"downstream":down,"physical_dac":nil,"model_cancel":nil})
 if cancelRun {if len(result.data)!=17640 || !prefix {t.Fatal("cancel prefix mismatch")}} else {if !exact || playBytes!=len(pcm){t.Fatal("full PCM mismatch")}}
}

func TestBookAudioReplay(t *testing.T) {
 root:=os.Getenv("BOOK_AUDIO_OUT");wavPath:=os.Getenv("BOOK_AUDIO_WAV");if root==""||wavPath==""{t.Fatal("explicit output/fixture required")}
 raw,err:=os.ReadFile(wavPath);if err!=nil{t.Fatal(err)}
 if bookHash(raw)!="8489119d2e8701e68bc1767fbb3495cd5f52d8d48692d1b7bdfa5a9f028c91f6"{t.Fatal("fixture changed")};pcm:=raw[44:]
 for _,cancelRun:=range []bool{false,true} {
  for round,pool:=range []bool{true,false,false,true} {
   for _,stack:=range []string{"baseline","queqiao"} {
    name:=fmt.Sprintf("cancel-%t/round-%d-pool-%t-%s",cancelRun,round,pool,stack)
    t.Run(name,func(t *testing.T){out:=filepath.Join(root,name);if err:=os.MkdirAll(out,0700);err!=nil{t.Fatal(err)};bookCase(t,out,pcm,stack,pool,cancelRun)})
   }
  }
 }
}
