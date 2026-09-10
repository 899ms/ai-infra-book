# 共享空口输入独立审查

本次结论：当前固定输入没有发现阻断性来源或算术错误。实际重新读取并核对 14 份原件的字节数与 SHA-256，独立推导五组 oracle 的 35 个字段，第五组另用事件队列计算，未调用作者的 `check-inputs.py`、任何候选网络引擎或已有模拟结果。

执行：

```sh
python3 calculations/research/shared-airtime-review/check-independent.py
```

执行报告为 `review-result.json`，包含被审输入、检查脚本和每份原件的哈希。检查脚本只写本审查目录。PASS 的含义是该输入合同的来源追踪和独立手算成立；没有运行 ns-3，没有重新下载验证远端内容，也没有执行媒体空口闭环。

## 原件逐读与可支持的结论

固定版本为 ns-3.44，release API 原件的 `id` 为 `43dce6710b8df69685e3479c1d33a571dda714ea`。以下位置均指 `../shared-airtime-inputs/sources/` 的固定原件，不依赖浮动 master。

| 原件位置 | 独立读到的实现 | 本例采用结果 |
|---|---|---|
| `ofdm-phy.cc:197,221,245,273,279` | 20 MHz 前导 16 µs、SIGNAL 4 µs；4 µs 符号；SERVICE 16 bit、tail 6 bit；符号数向上取整；只有 2.4 GHz 加 6 µs extension | 5 GHz extension 为零，不能把 PHY 时间折成任意固定 MAC 字节 |
| `wifi-mac-header.cc:964` | DATA 三地址头 24 B；双 DS 增 6 B、QoS 增 2 B；ACK 头为 10 B | 24 B 仅限已声明的 non-QoS/三地址，不适用于所有 Wi-Fi |
| `wifi-mac-trailer.h:20`、`llc-snap-header.h:23`，相应 `.cc` 序列化长度 | FCS 4 B；LLC/SNAP 8 B | MAC ACK 是 10+4=14 B；不加 LLC、IP、UDP |
| `wifi-phy.cc:871` | Configure80211a 设置 SIFS 16 µs、slot 9 µs | AIFSN=2 时声明的前置间隔为 34 µs |
| `wifi-remote-station-manager.cc:799,832` | ACK 通过 control-answer-mode 选择，遍历 basic set，按速率与调制类筛选 | 本例显式 basic set={6 Mbps} 支持 ACK 用 6 Mbps；54 Mbps DATA 不推出 54 Mbps ACK |
| `frame-exchange-manager.cc:579,290` | TXEND 后 SIFS+slot+PHY header 的 watchdog；RXSTART 正 PSDU duration 使 timer 重排 | 45 µs 不能作为完整 ACK 的硬截止 |
| `channel-access-manager.cc:518,547,702,720` | 接入与 backoff 使用 slot/IFS，另有真实竞争状态 | 本例全局 FIFO/零 backoff 是教学选择，不能称 ns-3 DCF 仿真 |

这是官方模拟器实现证据。源码注释引用 IEEE 并不意味着本审查已取得、逐条审查 IEEE 标准原文。IPv4/UDP 无选项的 20/8 B、1200/64 B QUIC 布局和速率集等属于明确选择；不是从无线设备测量得到。TACK 论文原件在锁中只提供背景，本次核对其文件完整性，不以论文标题或背景推出此模型复现了 TACK 算法或性能。

## 字节和时间的独立推导

三种 PSDU 为 `1200+20+8+8+24+4=1264 B`、`64+20+8+8+24+4=128 B`、`10+4=14 B`。54 Mbps 每符号 216 bit，6 Mbps 每符号 24 bit。

- DATA：`ceil((16+8×1264+6)/216)=47` 个符号，PPDU `20+4×47=208 µs`。
- QUIC ACK 承载 DATA：`ceil((16+8×128+6)/216)=5`，PPDU `40 µs`。
- MAC ACK：`ceil((16+8×14+6)/24)=6`，PPDU `44 µs`。
- 成功交换分别为 `34+208+16+44=302 µs` 与 `34+40+16+44=134 µs`。

## 五组 oracle 的审查

| Oracle | 独立推导与边界 |
|---|---|
| shared-nonpreemptive | 同一资源按 ready 与 available 递推得到 `[0,1]、[1,2]`；双方向各一个资源则错误地允许同时占用。1 秒已含交换，不再追加 MAC ACK。 |
| two-layer-static-account | DATA 两次共 2.5 秒；transport ACK 2 次/1 次各 0.5 秒，因此 3.5/3 秒。`mac_ack_for_data_count=2` 仅数原 DATA 的确认；所有 MAC ACK 应为 4/3，不能误读为总数始终 2。 |
| busy-channel-ACK-snapshot | 实际发送时刻 3 的最大 PN 是 1，接收于 2.75，raw delay=0.25；8 µs 单位编码 31250。原 timer 晚 2 秒与此 raw delay 是两个不同量。没有同连接新 PN 时 raw=3、编码 375000。 |
| MAC-ACK-loss-versus-end-to-end-recovery | 首次 DATA 已在 1 秒交付；1.5 秒才获知 MAC 失败，等 0.5 秒后同 PN 7 重试，3 秒只出现重复接收，3.25 秒才知道 MAC 成功。PTO=4 秒是另行声明的上游计时条件，不是从此 MAC 状态推算出的结果。 |
| fewer-ACKs-later-tail | 独立事件队列保留 credit、pending ACK 集合、timer 和全局非抢占 reservation。ACK 在 PPDU 结束释放 credit，但资源到自身 MAC 确认后才空闲。阈值 1 得 DATA 接收 1/2.75/4.5，ACK 接收 1.5/3.25/5；阈值 4 得 DATA 接收 1/2.25/6.5，ACK 接收 5.25/10.75。所有字段与预写 oracle 一致。 |

第五组解释：阈值 4 在第一帧接收 1 秒启动 4 秒 timer。第二帧后两份 credit 都未返回，所以空口暂时空闲。ACK 在 5 秒开送、5.25 秒到达；资源仍占用到 5.5 秒，第三帧只能在 5.5 秒开始、6.5 秒接收。总服务 4.75 秒不含空闲，最后一次交换结束 11 秒，三者不能互换。

## 已保留的具体反例

这些是可复验的错误替代模型，**不是声称当前输入包含这些错误**。

1. **把 45 µs 当完整 ACK 超时**：DATA TXEND 后 SIFS 16 µs，再用 20 µs 接收 PHY 前导/header，36 µs 可发生 RXSTART，早于 45 µs watchdog；完整 ACK 在 60 µs 才结束。错误超时会在合法完成前 15 µs 判失败。源码 `RxStartIndication` 的 timer 重排正是不能省略的状态边界；本审查没有把 36 µs 代替所有真实 PHY 的通用 RXSTART 时刻。
2. **ACK 速率直接复制 DATA 54 Mbps**：14 B 的错误 ACK PPDU 只有 24 µs，使 DATA 交换算成 282 µs，而本例是 302 µs，少 20 µs。
3. **重复加已有 IPv4/UDP 28 B**：PSDU 从 1264 变 1292 B，符号数增加到 48，DATA PPDU 误成 212 µs。
4. **取消符号向上取整**：DATA PPDU 会误成 `623/3=207⅔ µs` 的连续时间；精确错误值由脚本保存为有理数 `20+(16+8×1264+6)/54`，而正确值必须为 208 µs。不能用平滑 bit/rate 替代符号填充。
5. **将 deadline lateness 当 ACK delay**：同一忙时例会错报 2 秒；最大 PN 实际 raw delay 为 0.25 秒。
6. **MAC 确认释放端到端 credit**：第一帧 MAC 成功在 1.25 秒；阈值 4 例真正首次 transport credit 返回是 5.25 秒。提前 4 秒返还会消除本来存在的窗口停顿。
7. **用少服务推出早播放**：减少一次 ACK 节省 0.5 秒服务，尾帧仍迟 2 秒到达，丢失 0.25 秒固定槽音频。这是同一手算输入的反例，不是无线部署的性能预测。

后续实现仍需另审 MAC 重试/去重、共享资源与 WAN 串联、ACK 发送时快照和传播/接收事件、媒体 DAG 及真实 sender 的接合。本审查通过不覆盖这些尚未执行的机制。

## 新增 exchange helper 独立验收

随后只读审查 `../shared-airtime-loop/airtime.py` 并实际执行 `check-helper-independent.py`：75 项检查通过；被审源码 SHA-256 为 `131ce04a522e641ece9a851f9e6ab3b1771b7fc83a5417be3b2a52c53a717658`，运行前后未变。报告 `helper-review-result.json` 保留每个实际值与独立期望。没有发现该固定 profile 范围内的阻断性缺陷。

测试没有调用作者测试或用作者输出填期望，包括：

- 输入 `ip_bytes=1228` 仅加 LLC/MAC/FCS 36 B 得 1264 B；QUIC ACK 输入 92 B 得 128 B。
- 正常 DATA 接收在 reservation 起点后 242 µs，MAC 确认 302 µs；RF 发射仅 208+44=252 µs，不能把 34 µs 前置空等和 16 µs SIFS 算 RF。
- 54 Mbps 下 24/25 B PSDU 跨越 1/2 符号，51/52 B 跨越 2/3；6 Mbps 下 3/4 B 跨越 2/3，6/7 B 跨越 3/4。检查了符号数、padding 和时长。
- 声明 TXEND 后 80 µs 完整超时，两种损失的反馈都在 322 µs。DATA 丢失无接收、无 MAC ACK 发射，RF 为 208 µs；MAC ACK 丢失保留 242 µs DATA 接收与 44 µs ACK 发射，RF 为 252 µs。两者均不由 helper 提前改变 sender。
- 完整超时未知必须拒绝失败模拟；即使人为填 45 µs，也因为早于合法 ACK 完成而拒绝。
- 非零双向传播测试：每程 10 µs，DATA 接收 252 µs，MAC ACK 开送 268 µs、返回 322 µs；RF 不变。
- 教学 profile 加 1/8 秒 contention 后，正常反馈为 11/8 秒；失败计时依 DATA TXSTART 得 13/8 秒。所有教学结果 `radio_transmit_seconds=null`，不把含 SIFS 的 indivisible confirmation 段捏造成 RF 秒数。
- 教学 transport ACK 在 1/4 秒被端点接收，1/2 秒交换结束；严格拒绝 bool/string/零/负 IP 字节和非 bool flags。

helper 通过不覆盖排队、退避、重试状态机、去重及端到端连接控制，也没有证明任意修改的 PHY 参数是实际可用的标准模式。接入者仍需显式限制所支持 profile 并保持输入来源分类。
