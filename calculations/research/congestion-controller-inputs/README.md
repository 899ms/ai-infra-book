# 固定 CUBIC／BBR 控制器来源与独立手算

2026-09-09。本目录完成 `../shared-media-integration/next-congestion-scope.md` 的控制器来源封存与手算6–8。没有实现控制器、移植协议栈或执行 transport-feedback。所有下载原件来自 RFC Editor 或 torvalds/linux 官方仓库的固定 commit；未修改公共来源锁。

## 原件核验

`sources.lock.json` 保存精确下载URL、revision、bytes、SHA256和取回日。三个预先登记的文件全部逐字节吻合原scope；写入后重新读取计算hash也一致：

| 文件 | bytes | SHA256 |
| --- | ---: | --- |
| sources/rfc9438.txt | 73704 | baa4dd77295e27b9fa5c79993e962e70f728409bd1a48b9029bae4b551b0348a |
| sources/tcp_bbr.c | 42724 | ba7d0706259dfef5bf455f26ac4bab65f43b9209b9cfd4f761c64c89816bdfe4 |
| sources/tcp_rate.c | 8436 | 52d682c760573819a36bfef45a094ea8615a39d56c0248569d96f9e6e47b2b23 |

CUBIC是RFC9438；Linux两个C文件是v6.6对应commit `ffc253263a1375a65fa6c9f62a893e9767fbebfa`。不是latest BBR、不是BBRv2/v3，也不是TCP完整栈封存。额外只封存同commit `include/net/tcp.h`（78187B）用于`rate_sample`字段与wrap-safe `before()/after()`，hash见锁；没有无界拉库。header没有此前预登记hash，状态明确为新增依赖，不假称吻合预先记录。

## 实际读取与单位合同

- RFC9438 §4.2–4.7（文本约432–720行）：`t`为拥塞避免epoch的有效秒数；W_max、cwnd_epoch、cwnd、W_est用segment单位，C相应为segment/s³。`K³=(W_max-cwnd_epoch)/C`。t不包括应用受限导致cwnd不更新的时间。每个新ACK才更新，不能按时钟把曲线值直接赋cwnd。
- §4.2的target是W_cubic(t+smoothed_RTT)夹在当前cwnd和1.5×cwnd之间。§4.3 W_est每新ACK按alpha×segments_acked/cwnd更新，beta0.7对应alpha9/17；达到cwnd_prior还有alpha切换。若Reno友好分支胜出按W_est，非Reno凹/凸分支每新ACK增量为(target-cwnd)/cwnd。
- §4.6给出flight_size×beta减窗、loss最小2SMSS、ECE最小1SMSS、ssthresh最小2SMSS；不能把beta=0.7减窗70与本手算独立种子96.8混在一个epoch。fast convergence、启动、HyStart++、恢复及app-limited策略仍需完整实现时选择/封存，不能由几个算式宣称整个RFC控制器完成。
- `tcp_bbr.c` 68–195行：BW_SCALE24，即packets/μs乘2²⁴；gain用BBR_SCALE8即整数/256。RTT用μs，bandwidth max滤波按10个packet-timed round，minRTT窗口10秒；PROBE_RTT最低4包且至少200ms及一个packet round。`min_rtt_stamp`、probe_rtt_done_stamp是jiffies，非μs，完整实现必须固定HZ及jiffies舍入。
- 同文件240–253行：pacing换算先乘MSS bytes、gain，再右移8，再乘990000，最后右移24；1% margin与整步舍入不可忽略。socket cap在其它调用路径继续限制，算例只给该函数返回值。MSS1500B是本次手算输入，不是25KB教学分段也不是自动包含封装的MTU。
- 同文件759–800行：有效sample先检查delivered≥0、interval_us>0；`!before(prior_delivered,next_rtt_delivered)`开始新packet round，next值更新为当前tp->delivered，rtt_cnt增1。采样带宽为floor(delivered×2²⁴/interval_us)。app-limited低样本不压低max BW，但达到或超过既有max的app-limited样本仍可进入滤波，不能笼统写“所有app-limited样本都忽略”。
- 同文件872–1005行：full_bw判据仅新round且非app-limited执行；阈值整数乘320后右移8。3轮无显著增长才full_bw_reached。STARTUP→DRAIN与DRAIN→PROBE_BW有独立inflight条件。PROBE_RTT还受idle_restart、minRTT过期、4包、jiffies截止、至少一个round及cwnd恢复约束。
- `tcp_rate.c`已完整阅读（209行）：发送skb快照prior delivered/timestamp/app-limited；ACK/SACK选择较新发送记录、避免SACK再累计ACK重复用样本。样本分母max(send interval, ACK interval)，不是相邻ACK间距。无prior timestamp、SACK reneging会使样本无效；interval小于minRTT亦无效。delivered为取样区间交付数，不必等于本次newly ACKed。采样中包括恢复与app-limited状态，不能只输入当前ACK包数。
- `tcp.h` 276–280、1035–1064行确认32-bit wrap-safe before比较及rate_sample字段类型/单位；delivered/interval允许负值表示无效，prior_delivered与next阈值为u32。不能用普通无限精度整数比较替代计数回绕语义。

## 独立算例结果及scope纠正

`controller-oracles.json`仅保存有限算术事实，不是控制器输出。

CUBIC种子Wmax100、epoch96.8、C0.4令K=2；t=0/2/3的曲线96.8/100/100.4。另取当前cwnd100、t2、RTT1、W_est96.8、单段新ACK：W_est更新后仍低于W_cubic(t)，target100.4，因此新cwnd为100.004。曲线100、target100.4、ACK更新100.004三个数不可混同。一般立方根未求解，此例K为精确整数。

BBR delivered10、send100000μs、ACK20000μs：原始100segments/s，定点带宽floor(10×2²⁴/100000)=1677，不能按ACK压缩算500segments/s。high_gain为739/256（2.88671875），drain为88/256；本带宽与声明MSS1500代入源码整步换算得到428493B/s，非“100×1500×2.885”直接乘法。

**scope第8例的10/12存在整数解释陷阱**：若它们是Linux内部整数，floor(10×320/256)=12，所以样本12满足增长阈值，full_bw变12、计数归零。要表达抽象10→12未达到1.25倍，应显式用共同尺度，例如full_bw1000、样本1200，阈值1250，3个合格新round计数1/2/3后达到full_bw。两个分支均记录为oracle，不能默默保留错误的位精确期望。

packet-round例区分prior99<next100不启动、prior100==next100启动并设置next=当前delivered130、后续prior110<130不启动、prior130启动；另给next0xfffffffe、prior1的合法u32回绕例。单纯elapsed一个RTT不构成这个判据。

## 后续实施边界

完整移植还需要Linux minmax滤波、时钟、TCP发送/ACK/SACK/recovery语义、TSO与pacing cap、PROBE_BW随机相位、ACK aggregation、长期policer检测、idle和loss状态完整定义。当前不添加这些代码，也不把QUIC ACK/PTO当作Linux TCP回调。CUBIC与BBR后续应分别标“RFC规则实现”和“固定Linux控制器移植”；只有与发送方反馈/媒体业务闭环接入并独立验收后，才更新公共控制器完成范围。
