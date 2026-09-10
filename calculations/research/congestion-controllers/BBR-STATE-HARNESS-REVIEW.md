# BBR 整状态 C 桩独立审查：修正后限定范围 PASS

本次独立阅读了 `check-bbr-state-c.py`、生成 C、固定 v6.6 `tcp_bbr.c`、`tcp.h` 相关类型/helper、Python 状态实现与结果轨迹。BBR 从 BW_SCALE 到 bbr_get_info 前的算法主体原样提取，另附 bbr_set_state；实测生成文件包含该原始主体，未将 Python 逻辑重写为所谓 C oracle。minmax 为同 commit 原件。源码锁与 LP64 静态断言明确。

原四个输入缺陷已实际复验：delivered 与累计差不符、srtt_us_x8=2**32、edt_ns=2**64、rtt_us=2**63 均拒绝。rtt_us/interval_us 是 LP64 long，不能误当作 s32；合法长 RTT 赋给 u32 min_rtt_us 的截断另有作者 C 用例。

独立发现并通知修正：固定 tcp.h 的 tcp_stamp_us_delta 返回 u32，先用有符号差截到零再隐式截断。原 C 桩返回 u64、Python update_cycle 使用无限精度时间差，导致超过2**32微秒间隔时可以共同错误换 phase。167组原测试没有这一边界，所以先前 C/Python 相等不能证明该域正确。作者已改为原样提取固定 tcp.h helper，Python 实现对应 u64→s64→max0→u32 语义。本人实际重跑修正版 C harness：197回调×38字段和6个helper边界全通过；6个helper另用独立常数期望0/1/1/0/4294967295/100000核验。最终state hash fda8c57569767c94c9bbdbeca7e0155425542ade3c9f9356db188a131b9127c6，提取完整算法主体和helper均实测字串与固定原件相同，详见 bbr-state-harness-independent.json。

38项每回调比较含 BBR 模式、round、cycle、ProbeRTT、full_bw、policer、窗口/pacing、ACK aggregation 与 minmax 三样本；mode 有显式映射，prev_ca 字段名映射，未舍弃这些结果中的误差。原轨迹观察到0..7所有phase值，主要来自不同随机初draw；这与连续完整8phase转换覆盖不同，作者已增加一条连续8phase转换路径并实际通过。

桩层仍显式供应 TCP 核心状态：ACK/SACK fresh计数、已选择skb的 rate_sample、累计delivered/lost、inflight、CA state、应用受限和ACK延迟标志、srtt及EDT。没有执行 TCP 收发、ACK/SACK选择、丢失判定或队列。tcp_packets_in_flight 直接返回输入；tcp_min_rtt 返回声明值。时钟与随机数受控；原夹具每场景重复同一随机draw。GSO/MAX_TCP_HEADER/SMSS/pacingshift固定profile未覆盖所有ABI和配置。cmpxchg 简化仅用于初始化零状态，未证明并发行为。ssthresh/undo回调状态有比较，原函数返回值未作为独立字段覆盖。

修正后所有回调再次通过，仅证明声明输入轨迹上的固定算法与有限桩一致，不能宣称完整Linux TCP或网络闭环。真实回调序列的可实现性与TCP核心适配仍须独立合同和验证。
