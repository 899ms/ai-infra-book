# RFC9406 独立来源与合同审查

实际读取本目录固定 RFC9406 §4.2–4.3：18917 字节，SHA256 `43e3ddc1d3446142b125f018cd52aa2ff858b3f1ff9c6969924ab9fbf45d5230`。其官方原 URL 为 https://www.rfc-editor.org/rfc/rfc9406.txt。另实际请求 RFC Editor 9406 勘误查询，官方重定向页面返回 `No matching errata found`，原 HTML、查询 URL、字节/hash/日期另存 `errata-search.html` 和 `errata-search.lock.json`。这是查询时的数据库结果，不能声称将来不会有勘误。

独立预先期望见 `independent-oracles.json`，生成时未调用候选实现。只定义控制器的输入状态和数学结果，不把上游 TCP ACK 处理、RTT 样本选取和网络执行假装已经完成。

- Round 由初始化的 SND.NXT / windowEnd 和其被 ACK 的事实界定。SND.NXT 必须来自实际发送上游记录；ACK 增量既不是当轮所有发送字节，也不能直接计算结束了多少 round。跨越 marker 的 ACK 只处理一次，下一 marker 是当前真实 SND.NXT。
- 边界 ACK 先贡献该 round 的增长与新 RTT 样本，再切换下一轮，是该有限回调接口明确选定的事件归属顺序。应与真实 TCP 调用点相匹配，而非把它包装为 RFC 已完整规定的所有回调排序。
- 标准增长为 min(N,L×SMSS)，CSS 除以4；触发 CSS 的 ACK 只进行一次原 slow-start 增长。推荐非 pacing L=8，pacing L=∞；pacing 这里只是声明输入，不是已实现 pacer。
- CSS 回退文字说明要求当轮至少8个 RTT 样本；下面简写伪码省略了这个 guard。不能只抄该行 if 而在一个低 RTT 样本后立即返回 slow start。
- 每个 RTT 输入必须为上游新测得、可用于此算法的样本；rtt=null 的约定应明确表示未提供新样本，不能复用旧数值或累计空 ACK 来冒充8个测量。标准实现至少一轮一个 RTT 的要求和建议8个样本，应作为上游采样责任/不足信息暴露，不能默默用每 ACK 的时间差补齐。
- CSS 初始 partial round 计入五轮。完成第五轮才将 ssthresh 设为当前 cwnd 进入 congestion avoidance；currentRoundMinRTT 等于 baseline 不回退（严格小于），但慢启动进入 CSS 的门槛是大于等于。
- loss/ECN 在 SS 或 CSS 均设置 ssthresh=currentcwnd 并退出；这份算法自身没有规定乘 beta。拥塞控制器后续恢复/减窗必须是另一份明确接口，不可在纯 HyStart++ 输出偷偷应用 CUBIC 或 NewReno。
- RFC9406 建议仅初始 slow start 使用 HyStart++，后续回退标准 slow start；idle restart 可选使用属于 MAY。本候选可明确只实现初始阶段及禁止重启复用，不等于声称 idle 场景唯一合法行为。
- 应用受限导致 RTT 下降及 SS/CSS 往返是 RFC 预期的现象；不能无来源地丢弃 app-limited 样本来强迫 CSS 完成。

仍需独立执行边界：窗口marker精确等号/跨越、sent超前更新、不存在新数据的重复ACK、缺样本、触发边界只加一次、CSS第5轮与采样不足、loss/ECN后状态、负值/bool/未知字段、序号上界或显式非wrap域。尚未把这些预先规则称为实现验收通过。
