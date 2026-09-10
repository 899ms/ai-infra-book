package main
import (
 "bytes"
 "context"
 "crypto/rand"
 "crypto/tls"
 "crypto/x509"
 "encoding/json"
 "encoding/pem"
 "fmt"
 "io"
 "net"
 "os"
 "path/filepath"
 "testing"
 "sync"
 "time"
 "github.com/bojieli/queqiao/internal/baseline"
 "github.com/bojieli/queqiao/internal/identity"
 "github.com/bojieli/queqiao/internal/pep"
)
func wanCert(dir,name string,c tls.Certificate) {
 var data []byte;for _,der:=range c.Certificate {data=append(data,pem.EncodeToMemory(&pem.Block{Type:"CERTIFICATE",Bytes:der})...)}
 key,e:=x509.MarshalPKCS8PrivateKey(c.PrivateKey);if e!=nil{panic(e)}
 if e=os.WriteFile(filepath.Join(dir,name+".pem"),data,0600);e!=nil{panic(e)}
 if e=os.WriteFile(filepath.Join(dir,name+".key"),pem.EncodeToMemory(&pem.Block{Type:"PRIVATE KEY",Bytes:key}),0600);e!=nil{panic(e)}
}
func TestBookWANSetup(t *testing.T){
 dir:=os.Getenv("BOOK_WAN_PRIVATE");if dir==""{t.Fatal("private dir required")};if e:=os.MkdirAll(dir,0700);e!=nil{t.Fatal(e)}
 cert,_,e:=selfSignedCertificate();if e!=nil{t.Fatal(e)};wanCert(dir,"baseline",cert)
 token:=make([]byte,32);if _,e=rand.Read(token);e!=nil{t.Fatal(e)};if e=os.WriteFile(filepath.Join(dir,"token"),token,0600);e!=nil{t.Fatal(e)}
 _,client,e:=benchmarkCredentials(filepath.Join(dir,"provider"),"155.103.252.95:19281");if e!=nil{t.Fatal(e)}
 wanCert(dir,"client",client.Certificate)
 if e=os.WriteFile(filepath.Join(dir,"root.der"),client.Root.Raw,0600);e!=nil{t.Fatal(e)}
 bookSave(filepath.Join(dir,"client.json"),map[string]string{"provider":client.ProviderID,"gateway":client.GatewayID,"pin":client.RootPin})
}
func bookWANClient(ctx context.Context,stack string,pool bool)(*harness,error){
 dir:=os.Getenv("BOOK_WAN_PRIVATE");l,e:=net.Listen("tcp","127.0.0.1:0");if e!=nil{return nil,e}
 h:=&harness{socks:l.Addr().String(),closes:[]func(){func(){_ = l.Close()}}}
 if stack=="baseline" {
  cert,e:=os.ReadFile(filepath.Join(dir,"baseline.pem"));if e!=nil{return nil,e};roots:=x509.NewCertPool();if !roots.AppendCertsFromPEM(cert){return nil,fmt.Errorf("root parse")}
  token,e:=os.ReadFile(filepath.Join(dir,"token"));if e!=nil{return nil,e}
  c,e:=baseline.NewClient(baseline.ClientConfig{LocalAddress:"if:en0",ListenAddr:h.socks,RemoteAddr:"155.103.252.95:19280",ServerName:"queqiao.test",RootCAs:roots,Token:token,Transport:baseline.TUICTransport(),Congestion:"bbr-tuic"});if e!=nil{return nil,e}
  go func(){_ = c.ServeListener(ctx,l)}();h.closes=append(h.closes,c.Close)
 } else {
  cert,e:=tls.LoadX509KeyPair(filepath.Join(dir,"client.pem"),filepath.Join(dir,"client.key"));if e!=nil{return nil,e}
  der,e:=os.ReadFile(filepath.Join(dir,"root.der"));if e!=nil{return nil,e};root,e:=x509.ParseCertificate(der);if e!=nil{return nil,e}
  data,e:=os.ReadFile(filepath.Join(dir,"client.json"));if e!=nil{return nil,e};var ids map[string]string;if e=json.Unmarshal(data,&ids);e!=nil{return nil,e}
  cred:=identity.ClientCredentials{ProviderID:ids["provider"],GatewayID:ids["gateway"],RootPin:ids["pin"],Certificate:cert,Root:root}
  c,e:=pep.NewClient(pep.ClientConfig{LocalAddress:"if:en0",ListenAddr:h.socks,RemoteAddr:"155.103.252.95:19281",Credentials:cred,Transport:pep.TransportQUIC,EnableQUICPool:pool,Congestion:"bbr-tuic"});if e!=nil{return nil,e}
  go func(){_ = c.ServeListener(ctx,l)}()
 }
 return h,nil
}
func TestBookWANServer(t *testing.T){
 dir:=os.Getenv("BOOK_WAN_PRIVATE");out:=os.Getenv("BOOK_WAN_SERVER_OUT");if dir==""||out==""{t.Fatal("paths required")};ctx,cancel:=context.WithTimeout(context.Background(),12*time.Minute);defer cancel()
 auditFile,e:=os.Create(filepath.Join(out,"udp-peers.jsonl"));if e!=nil{t.Fatal(e)};defer auditFile.Close()
 cert,e:=tls.LoadX509KeyPair(filepath.Join(dir,"baseline.pem"),filepath.Join(dir,"baseline.key"));if e!=nil{t.Fatal(e)};token,e:=os.ReadFile(filepath.Join(dir,"token"));if e!=nil{t.Fatal(e)}
 b,e:=baseline.NewServer(baseline.ServerConfig{ListenAddr:"0.0.0.0:19280",Certificate:cert,Token:token,Transport:baseline.TUICTransport(),Congestion:"bbr-tuic"});if e!=nil{t.Fatal(e)}
 bp,e:=net.ListenPacket("udp","0.0.0.0:19280");if e!=nil{t.Fatal(e)};defer bp.Close();go func(){_ = b.Serve(ctx,&bookPeerAudit{PacketConn:bp,stack:"baseline",file:auditFile,seen:map[string]bool{}})}()
 provider,e:=identity.LoadProvider(filepath.Join(dir,"provider"));if e!=nil{t.Fatal(e)}
 q,e:=pep.NewServer(pep.ServerConfig{ListenAddr:"0.0.0.0:19281",Credentials:provider.ServerCredentials(),EnableQUIC:true,Congestion:"bbr-tuic",DestinationPolicy:pep.DestinationPolicy{AllowPrivate:true}});if e!=nil{t.Fatal(e)}
 qp,e:=net.ListenPacket("udp","0.0.0.0:19281");if e!=nil{t.Fatal(e)};defer qp.Close();go func(){_ = q.ServePacketConn(ctx,&bookPeerAudit{PacketConn:qp,stack:"queqiao",file:auditFile,seen:map[string]bool{}})}()
 small,e:=net.Listen("tcp","127.0.0.1:19283");if e!=nil{t.Fatal(e)};defer small.Close()
 go func(){for {c,e:=small.Accept();if e!=nil{return};go func(){defer c.Close();_ = c.SetDeadline(time.Now().Add(20*time.Second));var x [1]byte;if _,e:=io.ReadFull(c,x[:]);e==nil{_,_ = c.Write(make([]byte,1024))}}()}}()
 audio,e:=net.Listen("tcp","127.0.0.1:19282");if e!=nil{t.Fatal(e)};defer audio.Close()
 raw,e:=os.ReadFile(os.Getenv("BOOK_AUDIO_WAV"));if e!=nil{t.Fatal(e)};pcm:=raw[44:]
 if bookHash(pcm)!="26ae9256da89db184f63c3d8f11ea5cc029852c3167018117a9c274544f55f96"{t.Fatal("PCM identity")}
 go func(){for{c,e:=audio.Accept();if e!=nil{return};go func(){
  defer c.Close();_ = c.SetDeadline(time.Now().Add(45*time.Second));label:=make([]byte,128);if _,e:=io.ReadFull(c,label);e!=nil{return}
  name:=string(bytes.TrimRight(label,"\x00"));target:=filepath.Join(out,name);if e=os.MkdirAll(target,0700);e!=nil{panic(e)}
  f,e:=os.Create(filepath.Join(target,"origin-events.jsonl"));if e!=nil{panic(e)};defer f.Close();log:=&bookLog{start:time.Now(),file:f};log.event("origin_request",0,128,"")
  closed:=make(chan struct{});watchDone:=make(chan struct{})
  go func(){defer close(watchDone);var b [1]byte;n,e:=c.Read(b[:]);log.event("origin_reverse_read_end",0,n,fmt.Sprint(e));close(closed)}()
  start:=time.Now();total:=0
  for i,off:=0,0;off<len(pcm);i++ {
   wait:=time.Until(start.Add(time.Duration(i)*20*time.Millisecond));if wait>0 {select{case <-time.After(wait):case <-closed:log.event("origin_stop_peer",i,total,"");return;case <-ctx.Done():return}}
   select{case <-closed:log.event("origin_stop_peer",i,total,"");return;default:}
   end:=off+1764;if end>len(pcm){end=len(pcm)};n,e:=c.Write(pcm[off:end]);log.event("origin_write",i,n,fmt.Sprint(e));off+=n;total+=n
   if e!=nil{_ = c.Close();<-watchDone;return}
  }
  log.event("origin_all_sent",0,total,"");_ = c.Close();<-watchDone
 }()}}()
 bookSave(filepath.Join(out,"ready.json"),map[string]any{"baseline_udp":19280,"queqiao_udp":19281,"audio_loopback_tcp":19282,"warmup_loopback_tcp":19283,"pid":os.Getpid(),"pcm_sha256":bookHash(pcm),"ready_unix_ns":time.Now().UnixNano()})
 for {select {case <-ctx.Done():return;case <-time.After(200*time.Millisecond):if _,e:=os.Stat(filepath.Join(out,"STOP"));e==nil{return}}}
}

// Observe remote socket identities without changing encrypted datagrams or protocol code.
type bookPeerAudit struct { net.PacketConn; mu sync.Mutex; seen map[string]bool; stack string; file *os.File }
func (p *bookPeerAudit) ReadFrom(b []byte)(int,net.Addr,error) {
 n,addr,e:=p.PacketConn.ReadFrom(b)
 if e==nil {
  p.mu.Lock();defer p.mu.Unlock();key:=addr.String()
  if !p.seen[key] {p.seen[key]=true;host,port,err:=net.SplitHostPort(key);if err!=nil{return n,addr,err}
   err=json.NewEncoder(p.file).Encode(map[string]any{"stack":p.stack,"source_ip_sha256":bookHash([]byte(host)),"source_port":port,"first_datagram_bytes":n,"observed_unix_ns":time.Now().UnixNano()})
   if err!=nil{return n,addr,err}
  }
 }
 return n,addr,e
}
