# 共享空口完整轨迹独立代数检查

`check-trace.py` 不导入候选 Network、airtime 组件或公开 sender；从保存输入重算选定教学/OFDM公式，再逐项审查保存结果。每次只读一个结果文件，可处理单个完整结果或小例name→result映射；一次不加载五个完整大例。当前只实际执行已存在10小例及一个前导截止结果，没有启动任何网络模拟或大例。

```sh
python calculations/research/shared-airtime-trace-review/check-trace.py
python calculations/research/shared-airtime-trace-review/check-trace.py --result path/to/full-result.json --output path/to/review.json
python calculations/research/shared-airtime-trace-review/check-corruptions.py
```

检查包括全局reservation非重叠和观察区间裁剪；每次DATA、SIFS/MAC确认、MAC反馈/失败时刻与传输/接收标志；同PN尝试只对应一次sender.sent，本跳重复身份；每个源PN/frames/bytes与发送事件对应；每个真实到达传输ACK才产生一次sender ACK反馈，MAC确认不生成免费端到端反馈；AP首收到到WAN、每向WAN串行与可选router服务的精确耗时；按消息范围去重的唯一收到字节与已交付消息的覆盖、可靠流连续前缀；旧PHY字节前缀保持null、WAN前缀独立计量。

OFDM公式在本脚本独立使用符号向上取整、SERVICE16/tail6、输入前导/头与速率；不读取airtime组件输出作为期望。教学模式的确认段包含间隔，因此纯RF时长必须null。字节守恒从实际received记录重建，不用summary作为计算起点。可靠前缀按实际接收时刻预计算，按业务交付时刻查询；无线预约用索引，避免每尝试扫描全部预约。

`small-check.json` 保存10个实际已存结果的检查、原结果SHA、14官方输入来源的校验及前后完整运行代码/来源hash。源码hash表示本次复核环境，并不单独证明任意外部结果由该版本生成；后续完整结果还须核其生成manifest。`corruption-check.json`另证实八个明确损坏的轨迹被拒绝，并实际通过44µs前导截止结果。

范围限制：此脚本不重新推导调度选择是否最优，不复现随机DCF/IEEE实现，不独立重跑RTT/拥塞控制器算法，也不重建全部应用任务/取消/播放政策。它验证已报告交付具有必要的字节覆盖/时刻条件，但不能单凭覆盖证明任务依赖或业务质量正确。输入归一化、源ACK快照范围、应用因果、独立预写绝对时刻和控制器专项仍需各自检查。单文件JSON目前整体载入；若未来文件规模超过可用内存，应改逐顶层数组读取，不能偷偷跳过大数组。原研究内核与公共文件未修改。

## 完整单图保存轨迹审查

`check-bound-result.py --case image-baseline` 已实际读取并核查283,897,398字节完整结果（SHA `44955a7478d5da294273e49ac530b884953beb5a9111e828d020b6898680c5c1`），输出 `image-baseline-check.json`。先验证生成manifest的前后源码集合相等、各绑定文件当前SHA、输入副本SHA与结果内inputs一致、结果长度/SHA，检查完成后再复核；不是仅记录当前源码后推断生成身份。

实际核查61,600条端到端记录和61,600次无线交换，业务唯一35,000,000B，原IP包账40,656,000B。30,800次DATA交换各302µs，30,800次传输ACK承载交换各134µs，累计服务为 `302µs×30800+134µs×30800=13.4288s`。完整图片在15.993881866s交付；同分块、同原业务/WAN输入去除无线后的基线为14.8839358s，增量1.109946066s。该差值是增加整个声明无线服务的结果，不能再分解成独立控制器收益而无额外对照。

13.4288s不是应当简单加到基线上的延迟：WAN和无线段会流水重叠。完整图片交付前已有13.265528s无线预约服务，之后仍有0.163272s用于后续确认，最后无线交换结束16.157153866s；完整交付和全部反馈排空是两个终点。该审查没有重新执行网络，也没有将第一完整单图的通过推广为四个混合大例或完整C69验收。

单图分层手算也已实际逐attempt核验：DATA与传输ACK承载帧、MAC ACK合计43,736,000 PSDU字节；RF发射10.3488s、接入等待2.0944s、SIFS0.9856s，三者和13.4288s。PSDU字节不含PHY前导/符号填充的“等效字节”，RF时间不含接入等待/SIFS。

随后已实际检查 `mixed-fifo-immediate` 完整保存轨迹并通过；证据 `mixed-fifo-immediate-check.json`。该结果的生成manifest、输入、完整结果及运行绑定逐文件复核，应用唯一字节/可靠前缀按真实接收记录检查；本脚本仍不替代完整播放/版本/取消因果专项。

## 九格载荷/ACK扫描

`check-scan-inputs.py`先于读取扫描结果，实际核对9格输入、逐对象ACK配对、符号/尾片/单位手算和本地业务依赖，输出`scan-input-review.json`，没有发现需修输入。`pad_in_flight=false`及无独立controller pacer明确属于300KB/50KB新教学负载，320/640/960B不代表等质量codec。

随后`check-scan-results.py`核生成manifest的739个绑定文件、九份完整结果及72个媒体块实际DATAGRAM接收和固定播放槽，输出`scan-check.json`。全部九格均8/8按时、缺音零；每个载荷大小对应真实ACK数274/144/78，并非静态阈值比较器308/155/78。该结果不能称“减少ACK改善了播放”，因为所有格已经按时；也不能把音频大小变化解释为已证明的同质量压缩收益。配对只在同一载荷大小下控制变量为ACK阈值，完整图片/ACK反馈时刻及服务差异应另读对应轨迹。

最后 `mixed-priority-aggregate` 完整轨迹（SHA `c337a9ab591d9382387562cb4df46d646938b2d7aeb04711e3094c30e2686e91`）已实际完成独立生成manifest/输入/来源绑定与逐轨迹审查，见同名 `-check.json`。至此单图和混合四格五份完整保存结果均通过本目录的有限代数检查；这不代替主审后续五例比较、业务专项或公共接入验收。
