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
 "os/exec"
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
 sinkLog,err:=os.Create(filepath.Join(root,"device.log"));if err!=nil{t.Fatal(err)};defer sinkLog.Close()
 sinkCmd:=exec.Command("python3",os.Getenv("BOOK_AUDIO_SINK"),"--out",root)
 sinkCmd.Stdout=sinkLog;sinkCmd.Stderr=sinkLog
 pipe,err:=sinkCmd.StdinPipe();if err!=nil{t.Fatal(err)}
 if err=sinkCmd.Start();err!=nil{t.Fatal(err)}
 log.event("device_process_started",0,0,"")
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
 type readResult struct{ data []byte; err string }
 received:=make(chan readResult,1)
 go func(){
  defer pipe.Close();var collected []byte
  for i:=0;;i++ {
   buf:=make([]byte,1764);n,e:=io.ReadFull(c,buf)
   if n>0 {
    collected=append(collected,buf[:n]...);log.event("client_frame",i,n,"")
    if _,werr:=pipe.Write(buf[:n]);werr!=nil {received<-readResult{collected,werr.Error()};return}
   }
   if cancelRun && i==9 && n==1764 {
    log.event("cancel_call",i,0,"");_ = c.Close();log.event("cancel_return",i,0,"");received<-readResult{collected,"intentional_cancel"};return
   }
   if e!=nil {log.event("client_read_end",i,n,e.Error());received<-readResult{collected,e.Error()};return}
  }
 }()
 result:=<-received;_ = c.Close()
 if err=sinkCmd.Wait();err!=nil{t.Fatal(err)}
 log.event("device_process_ended",0,0,"")
 sinkBytes,err:=os.ReadFile(filepath.Join(root,"device-consumed.pcm"));if err!=nil{t.Fatal(err)}
 playBytes:=len(sinkBytes);played:=0
 var observed any=nil
 select {case ns:=<-originObserved:observed=ns;case <-time.After(5*time.Second):log.event("origin_close_unobserved",0,0,"")}
 select {case <-originDone:case <-time.After(5*time.Second):t.Fatal("origin writer did not stop")}
 up,down:=h.relay.Stats();log.event("case_end",0,0,"")
 if err=os.WriteFile(filepath.Join(root,"received.pcm"),result.data,0600);err!=nil{t.Fatal(err)}
 exact:=bytes.Equal(result.data,pcm);prefix:=bytes.Equal(result.data,pcm[:len(result.data)])
 bookSave(filepath.Join(root,"result.json"),map[string]any{"stack":stack,"pool":pool,"intentional_cancel":cancelRun,"received_bytes":len(result.data),"received_sha256":bookHash(result.data),"fixture_pcm_sha256":bookHash(pcm),"complete_pcm_equal":exact,"prefix_equal":prefix,"reader_end":result.err,"sink_frames":played,"sink_bytes":playBytes,"origin_reverse_read_end_ns":observed,"upstream":up,"downstream":down,"physical_device_callback":true,"muted":true,"model_cancel":nil})
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
