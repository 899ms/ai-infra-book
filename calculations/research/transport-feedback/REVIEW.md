# Stage 1 发送方反馈独立审查

结论：**PASS，限已确认单路径 application-PN 发送方参考重放合同**。实际执行 `python calculations/research/transport-feedback/check-independent.py`，27组通过（13组来源/独立手算/边界，以及14个固定场景），无剩余检查失败。候选运行前后SHA一致：`1f3890671c60d9841d3dd89e289483940872c2823d7ba767b3a6b845dcbea567`。详见 `check-independent.json` 的每场景状态/定时器/丢失证据。

本审查仅写来源、checker和报告，没有修改实现、公共模块或PLAN。与作者沟通的问题由作者处理。没有执行30MB网络闭环、真实QUIC/TCP栈、CUBIC或BBR。

## 来源与勘误

来源锁实际固定并重新校验四份：RFC9000、RFC9002、RFC9221及RFC9002 **Verified Errata7539**官方HTML。适用段落、URL/bytes/SHA与计时单位详见 `SOURCE-SCOPE.md`、`sources.lock.json`。

审查初稿错误地依据未勘误§5.3正文建议先更新SRTT；根审查找到官方Verified Errata7539后，我实际下载/阅读其全文，撤正建议并在checker加入有区分力的期望：旧SRTT100ms、var50ms，latest180ms、ack_delay20ms得到adjusted160ms，**新var52.5ms、SRTT107.5ms**。错误顺序的50.625ms不得通过。最终候选采用勘误顺序，与A.7一致；这是纠正已确认技术错误，不是允许作者任择算法版本。

## 独立检查方法

小例期望在实现前next-congestion-scope/root手算上固定；checker只调用候选顶层calculate，不调用其RTT、loss、timer或union辅助函数求期望。通用检查按显式发送和ACK记录独立重放flight及应用区间：每个新PN一次发送占用，ACK/lost不重复释放，同offset多次发送保留多次wire，输出唯一区间用逐位置计数验证不重叠。流控单独按每流最高offset计算，不能用ACK累计字节或区间并集大小替代绝对MAX_DATA消耗。

通用守恒检查会使用候选报告的newly_lost事实来扣除flight，因此它**不独立证明所有输入下的丢失分类**；丢失分类/时刻由另列包阈值、时间阈值、ACK同刻和PTO手算约束。该区别保持明确，不称已有第二套完整RFC实现或穷举验证。

## 实际结果

| 检查 | 独立结果 |
|---|---|
| 原手算1：BDP/序列化 | 上行250000B、下行1250000B；理想30MB+模型0.3s+5MB及分向传播下界12.8s。仅核单位/依赖，不称候选算出完整请求 |
| 原手算2：RTT/重复ACK | 首样本100ms不扣ACK delay；第二120ms减20ms后SRTT100ms、var37.5ms；重复ACK无重复取样或增长。勘误分歧例107.5/52.5ms通过 |
| 原手算3：loss | PN0–3在0/1/2/3ms发送、103ms只ACK3；PN0在103ms按包阈值失，PN1/2分别113.5/114.5ms按时间阈值失；cwnd只从12000减至6000一次，t=0发送不被0哨兵遗漏 |
| ACK恰在loss时刻 | PN1在113.5ms被ACK，先于timer不判失；该ACK自身产生112.5ms新RTT，剩余PN2阈值移至128.5625ms。不能取消PN1却继续用旧114.5ms期望PN2 |
| 原手算4：PTO | 275ms周期、最后发送1s，PTO1.275s，仅生成2次probe机会；flight1200/cwnd12000不变、无loss。到1.55s第二次PTO体现指数退避。有效ACK同刻取消旧timer，重复旧ACK不能取消新包PTO |
| 原手算5：绝对流控 | A4+B2消耗MAX_DATA6，ACK不释放；5s收到连接8仍受A4限制，6s收到A6才可发A[4,6)。较小限额不回退，恢复A旧[0,4)不增加绝对额度 |
| 新PN/旧offset/晚ACK | 新PN恢复原offset单独占flight/wire；旧已lost包晚ACK确认有效区间但不再次释放/增长/取RTT。新恢复epoch包ACK的CA增长使6000变6240；唯一应用bytes不随重发倍增 |
| limited/ACK/PADDING | app_limited或flow_limited均抑制ACK增长；纯ACK无flight，PADDING-only可有flight，两者都不能独立产生RTT样本 |
| DATAGRAM | MAX_DATA=0仍可发送受cwnd约束的DATAGRAM；其ACK只确认运输，不变成STREAM信用或播放证据 |
| PTO probe | probe可获得cwnd例外但仍占flight；不能越过绝对流控；恢复旧offset允许且消耗一个probe机会 |
| 范围拒绝 | 构造达到persistent-congestion区间条件的历史明确ValueError，未静默输出“完整NewReno” |

12个无效输入另外实际拒绝：ACK未发PN、非零首PN、重复PN、重叠ACK范围、违反MAX_DATA发送、无PTO机会的probe、非bool limited标记、初始/更新连接或逐流限额超过2^62−1、巨大ACK范围。persistent范围拒绝另计，不当作已实现persistent congestion。

14个作者场景逐个实际重新调用calculate并核上述守恒，非只读预生成result.json。场景涵盖RTT/勘误、包与时间loss、ACK同刻、尾包PTO/探测后ACK重置、绝对流控/高水位空洞、DATAGRAM、ACK/PADDING、新PN恢复及超cwnd合法probe。

## 发现与修正

- 根审查提供Verified7539后已固定官方原件，撤正本审查早期错误建议，最终候选与独立分歧期望一致。
- 源码已有DATAGRAM分支，我补固定RFC9221，避免用9000/9002两源替代其流控/ACK语义。
- 发送时间0、恢复epoch0和首次样本使用明确空哨兵；发送方loss先于同ACK的NewReno增长，防止先涨再减。
- 绝对限额编码上界、ACK范围数量/尚未发送范围在作者最终版补齐；大范围先拒绝再展开。
- checker最初对同刻loss例错误地延用旧RTT阈值，已根据该ACK的新RTT手算改为128.5625ms并加专门断言；不是放宽实现的计时边界。

## 结论的实际边界

输入sent/ACK-arrival/MAX-arrival是显式反馈记录；本阶段没有构造接收端、反向ACK串行器、网络丢包、pacer或自动发送机，也不检查真实链路重叠。时间戳是输入恢复算法的发送时刻。`sent_bytes`是声明UDP payload（含QUIC头/tag，不含UDP/IP），不能当作全链路线速bytes。

newly-acked/lost的有限NewReno参考使用有理数，非某内核的整数舍入实现。late-lost-ACK保留业务覆盖是明确扩展，不等于完整spurious-loss恢复。persistent congestion达到范围即拒绝；ECN、迁移、其它PN空间、实际Probe调度与握手仍缺。`sender_confirmed_business`只表示发送方得到的运输确认，不是接收应用完整交付或设备播放。

30MB双方向请求、共享媒体业务、指定CUBIC/BBR、完整图12-4和原C68剩余协议对照必须在后续闭环阶段处理；stage1通过不关闭C68或相邻C69。
