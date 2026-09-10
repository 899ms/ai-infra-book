# 单共享空口研究到公共项目的接入清单

本文件为只读迁移方案，不代表公共接入已完成。本次保留已拆分后的前十二章结构，正文落点为第12章、12.4.1/实验12-5和图12-5第一面板；不恢复第13章，不覆盖作者并发修改。

## 固定数学与模块边界

| 当前研究输入/实现 | 建议公共位置 | 接入方式与不可改变的语义 |
|---|---|---|
| `research/shared-airtime-loop/airtime.py` | `src/infra_calc/transport/airtime.py` | 保留 Fraction、符号取整、IP bytes 已含28B、DATA接收与MAC确认分时刻、教学 RF=null、45µs RXSTART 不冒充完整ACK超时 |
| `research/shared-airtime-loop/calculate.py` | `src/infra_calc/transport/shared_airtime_network.py` | 静态相对导入 `.media_network` 和 `.airtime`，去掉 sys.path/importlib/研究路径；复用公共媒体 Application、sender、ACK receiver、控制器，不复制第二套 |
| `shared-airtime-inputs/profiles.json` | `scenarios/shared-airtime-profiles.json` | 保留官方实现支持的选择与纯教学 profile 分离、未知实测字段 null；场景内 profile 的字节身份与中央 profile 锁关联 |
| `shared-airtime-inputs/sources/*` 共14原件 | `sources/shared-airtime/*` | 原件逐字节迁移，保留 LICENSE、release API、官方 Wi-Fi设计文档和 TACK 作者原件；不重抓浮动最新文件来替换已验版本 |
| `shared-airtime-book-analysis/summarize.py` 的纯账本聚合 | `src/infra_calc/transport/airtime_report.py` | 提取纯结果→分层账本函数；拒绝未完成/失败交换进入“完整成功账”，未来另写 observed-phase 账，不能默默外推 |
| `shared-airtime-book-analysis/compare.py` | 公共结果比较/图数据提取函数 | 比较使用公共产物及其 manifest，不依赖研究目录；旧基线 input/result/summary 必须绑定，不仅同名文件 |

已验证网络数学冻结版本：`calculate.py` SHA-256 `37c442824b5b127407658a75b21638882ee5a75ff08156cfc716b141d1b75f6b`；airtime helper `131ce04a522e641ece9a851f9e6ab3b1771b7fc83a5417be3b2a52c53a717658`。迁移时保存源/目标哈希、包装 diff 和 AST/函数主体差异说明。研究独立脚本和历史证据保留，公共运行不得动态导入研究文件。

## 官方来源接入

`configs/sources.lock.json` 既有记录字段为 model/repository/revision/upstream_file/url/file/sha256/bytes/downloaded_at/status。将14个研究 lock 记录映射到统一字段，`file` 改公共相对路径，其余 URL/revision/bytes/hash 不变；不同锁结构转换不能遗漏原始 revision。

复用 `src/infra_calc/sources.py` 的 `records/read_source/verify_sources` 和 `transport/reference_sources.py`：新增独立 `shared_airtime` 来源组，静态列出原件，由公共校验返回元数据。不要每个场景复制下载器或继续输出研究绝对路径 `wireless_reference_root`。迁移结果允许明示来源元数据路径差异，数学 payload 必须完整相等。

ns-3.44 提交固定 `43dce6710b8df69685e3479c1d33a571dda714ea`。这是官方实现证据；未获取完整 IEEE 标准正文，不标成 IEEE 逐条认证。TACK 仅作动机，未实现 TACK TCP 机制。未来更新官方原件需独立版本更新流程，不能借迁移换值。

## 统一 CLI 与场景注册

现有 `topics/transport_closed_loop.py:calculate` 对 `{application,network}` 分支导入 `transport.media_network.calculate`；`cli.py` 已有 `transport-closed-loop --inputs … --format json/md`，无需另开一套普通计算 CLI。

建议在该媒体分支按 `network.wireless_access` 选择公共 `shared_airtime_network.calculate`。缺省和显式 enabled:false 必须回旧媒体入口，维持原结果完整结构；enabled:true 才进入共享空口。严格保留已有外层 application/network 验证，不以 dispatch 旁路验证。

正式批量列表为 `scenarios/book.json` 的 `transport_closed_loop` 组，`src/infra_calc/reproduce.py` 已逐该组调用模块 calculate/save。保留旧 ID，新增：

- 十个机制小例建议前缀 `shared-airtime-`；现有独立审查另有源 profile/horizon/下行去重边界，必要用公共 tests 覆盖，不必全部扩成书中算例。
- 五个原书完整例：`shared-airtime-image-baseline`、`shared-airtime-mixed-{fifo,priority}-{immediate,aggregate}`，来自 `shared-airtime-book-inputs` 固定输入；只新增无线配置，原30MB/5MB、媒体DAG/任务/槽保持不变。
- 九个有限扫描：`shared-airtime-scan-media-{320,640,960}B-ack{1,2,4}`，来自 `shared-airtime-scan-inputs/scenarios.json`。这是300KB/50KB新教学背景，不替代原书大例；pad_in_flight=false、同20ms轨迹/100ms起固定槽/max_delay10ms，不冒充等质量codec。
- 一个可编辑读者入口 `scenarios/shared-airtime-example.json`；profile与业务假设可读，不引用研究目录。

## 分层报告与守恒

`report.py` 当前先把带 sender_events/final_states/transmissions/businesses/message_status 的结果送 `transport/media_report.py`。新增无线报告需在通用媒体识别前检测无线字段，或在 media_report 中显式调用共享账本；否则新无线账会被既有分支吞掉。保持原 disabled Markdown 不变。

至少展示：原始业务 offered/sent/received/delivered/usable、传输 ACK 数/字节、同 PN MAC attempts、MAC ACK PSDU、DATA PSDU、PHY RF 时间、接入空等、SIFS/传播、总预约/截止内实际占用、WAN实际 IP 串行量。逐交换 trace 保留在 JSON，Markdown采用可读摘要和有限示例，不铺数万行。

不得把 `summary.wire_bytes` 无条件称为截止时刻 WAN bytes；新版使用 `wan_serialized_ip_bytes_by_horizon`。PHY 截止时旧均匀字节比值字段是 null，不能重新补一个近似数。DATA PSDU 已含 LLC/MAC/FCS，MAC ACK14B另加一次；前导/填充/空等不是虚构字节。无线和WAN可流水重叠，不能把累计无线服务直接加到原基线完成时间。

played blocks 数 `play_end!=null`，不能数未来 scheduled_play_end。部分已播时长另按实际 horizon 裁剪；队列排空不证明音频按槽播放或截图动作可用。取消/过期场景应分离 offered条件下界与实际发包服务。

## 图12-5第一面板与第12章证据

新增 `src/infra_calc/shared_airtime_plot.py`，沿既有 `media_feedback_plot.py` 的 render()/verify()、SVG/PNG、精确 data.json、输入/输出 hash manifest。图数据只读取公共结果及公共来源/profile/源码，正式 reproduce 完成后正常 render，禁止绕过 stale verify。

第一面板有限展示：五完整例无线/WAN基线配对的成片与播放质量；同九格 ACK阈值×声明媒体字节量的实际 ACK 数、无线占用及成片/缺音。明确静态 ceil ACK 包账不是实际 ACK 数，scan全部播放成功不推出其他负载保证。不同大小图背景与完整原书例不能混在一条同条件曲线上。

在 `cli.py` 注册仅图命令，在 `reproduce.py` 的 figures verify 流程增加图验证；配合统一 figure manifest。`outline.py` 当前第12章已有 `C68-media-feedback` 插入，建议另设 C69共享空口证据块，引用新增结果、来源选择、图12-5第一面板与有限scope。执行章节同步前重新读作者最新章节，保留其第13章拆分成果和新增内容。

## 验收顺序与版本证据

1. 封存研究版本及全部手算/独立小例、5完整逐trace审查、9扫描运行与独立审查证据。未完成的审查不能只凭 generation manifest 标完成。
2. 公共迁移只改导入/来源包装；实际公共重算并比对完整数学字段。保留映射表，明列仅来源路径允许差异。
3. 旧19场景必须在公共统一入口实际重算：14小例+5完整。研究已做显式disabled完整回归，仍需公共迁移后回归，不能以旧研究结果代替新代码执行。
4. 公共 tests 覆盖共享reservation、WAN追加、下行同PN MAC去重、ACK实际源发送快照、重试知识、45µs、44µs前导截止、downWAN途中arrivalNone、PSDU与RF账。
5. 新5完整+9扫描（及注册小例）全公共重算、逐结果hash/算术/业务对照，再走统一 suite 和 reproduce。注册多少 ID 就做对应 JSON/MD 实际 CLI；不要只核JSON忽略report路径。
6. reproduce 的输入清单纳入全部公共源/profile/source lock；输入哈希稳定、全部产物生成完成后才 render 图、视觉QA、verify、章节同步/网页生成并更新进度。修改图脚本若属于统一输入须重新绑定正式manifest，不将旧manifest与新图混用。

## 不阻塞本包的 C69 保留缺口

双路径/first-wins/RAW汇合瓶颈、真实蜂窝费用和能源、共享故障概率、版本过时或动作失败后真实通知→新截图/重试的有界闭环、图12-5第二部分、匹配客户端 TCP/H3/TACK 实测继续保留。它们不能被本共享空口子账勾成完成；但也不要求先实现所有 TCP 握手/拥塞/恢复变体才能接入已经固定的此包。
