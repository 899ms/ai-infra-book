# 媒体真实反馈公共迁移映射（只读准备）

本文件只规划迁移，不修改研究内核或公共实现。完整 image baseline 与四格首轮已有实际计算；由于 runner 最初未把 `network_validation.py` 纳入运行身份，主代理正在补锁后重跑。**公共迁移基线必须取补锁后五份正式 manifest 及最终独立审查的相同源码，不使用首轮漏项 manifest 作为最终验收。** 来源、代码和数学正确性是不同证据，不能互相替代。

## 最小文件映射

| 研究文件 | 建议公共位置 | 必要变化；数学保持 |
| --- | --- | --- |
| `calculate.py` 的 Network、merge/prefix、calculate | `src/infra_calc/transport/media_network.py` | 删除研究CLI/ROOT/sys.path/local_module；静态导入下列模块和已有ACK/pacer/sender。Network各事件分支原样迁移，不同时重构调度或消费算法 |
| `application.py` | `src/infra_calc/transport/media_application.py` | 保留Application和业务观察公式；模块引用改静态路径 |
| `application_validation.py` | `src/infra_calc/transport/media_application_validation.py` | 保留规范化DAG全部预检，包含端点、顺序、DATAGRAM、任务FIFO和observer约束 |
| `network_validation.py` | `src/infra_calc/transport/media_network_validation.py` | 保留布局/内存/额度/参数冲突拒绝，不把它遗漏于运行hash与迁移比较 |
| `sender.py` | 优先复用现有 `topics/transport_sender.py`；可加很薄的 `transport/media_sender.py` 接口层 | sender算法已经公共，无需再次复制。保留 `retransmittable_frames` 纯STREAM选择辅助函数；研究依赖路径锁改为公共来源验证/统一代码hash，不引入新的恢复算法 |
| `run-small.py`、`run-book.py`、输入准备脚本 | 留研究作为证据与复算入口 | 公共产物沿现有reproduce，不把研究runner放进运行时或从研究目录动态导入 |

现有 `transport/ack_receiver.py`、`pacer.py`、CUBIC/HyStart/BBR/persistent模块直接静态复用，禁止平行维护第二套控制器。研究Network是新业务网络入口，不借这次迁移统一改造旧单上传网络。旧 `topics.transport_closed_loop.calculate` 保留原 `upload_bytes` 路径数学。

## 现有 CLI 分派

保留 `calc.py transport-closed-loop --inputs ...`，不新增竞争命令。`topics/transport_closed_loop.py:calculate(inputs=None)` 顶层只新增明确分派：

- inputs为同时包含 `application`、`network` 的字典时调用 `media_network.calculate(inputs)`；外层额外未知字段应拒绝，尤其同时携带upload_bytes不得悄悄忽略。
- `inputs=None` 仍运行旧default example。其他输入继续旧upload_bytes验证/路径。
- 不以truthiness区分空application，也不通过异常捕获回退到旧路径。非法DAG直接报错。

当前 `cli.py` 已在同命令调用该函数，实际JSON路径无需另一注册；help可扩成“上传与共享媒体DAG反馈”。当前 `report.py` 首分派要求单数 `business`，媒体输出是 `businesses`，因此必须增加独立且明确的媒体分派，或让 `transport_closed_loop.markdown` 自行分派。不要把研究结果补一个虚构单数business/计算类型字段来迎合旧判据；完整数学JSON需与研究保持一致（仅来源根/元数据例外）。

媒体 Markdown 建议在 `transport/media_report.py`，从同一结果输出：业务完整/可用/停顿/缺音、计算资源、消息状态与实际依赖、逐方向wire/received/delivered区别、ACK/RTT/flow等待与必要原始轨迹。message_status目前含整个DAG节点，应明说或展示时分组，不暗改JSON。`scheduled_play_end`不等于已观察到的play_end；pureACK身份判失不等于数据丢包；serialized_wire_bytes_by_horizon区别于已开始包的完整声明wire。

## 场景与输入

建议仍归入 `scenarios/book.json` 的 `transport_closed_loop` group，利用已有 `reproduce.py` 的 `module.calculate(row['inputs'])` 循环。ID前缀建议统一 `media-feedback-`，避免混淆旧 `shared-media-*` 教学网络。

1. 小例：研究 `scenarios.json` 的14项原样注册为 `media-feedback-<name>`，其中已包含flow阻塞其他流进展、真实消费、DATAGRAM尾丢PING、可靠恢复、取消、版本和播放负例。
2. 完整五例：`media-feedback-image-baseline`；`media-feedback-mixed-fifo-immediate`、`media-feedback-mixed-fifo-aggregate`、`media-feedback-mixed-priority-immediate`、`media-feedback-mixed-priority-aggregate`。输入严格取最终 `image-baseline-inputs.json` 与 `book-inputs.json`。
3. 可编辑入口：`scenarios/media-feedback-example.json` 采用已验小截图；另可提供 `scenarios/media-feedback-mixed-example.json` 一个完整四格输入。字段就是 `{application,network}`，不引入研究文件路径引用语法。

总计建议19行、38份JSON/MD。五大例须保留1400个原图/成片块的边界：30800个基础图像数据包，不合并成旧单字节流29966包。四格只有发送调度和ACK策略变化，compute FIFO、业务DAG与声明网络供给相同。不要将因取消/过期而未发送的bytes当作输入被删减。

## 来源与哈希依赖

- 网络 RFC9000/9002/勘误、DATAGRAM RFC9221，以及已选controller官方源码均复用已有公共来源，使用 `sender.reference_sources(include_datagram=True)` 的实际需求选择；无需重复登记同一官方文件。
- `sender-dependencies.lock.json` 是研究封存校验；公共统一 `reproduce.input_hashes()` 已递归追踪 `src/**/*.py`，确认四个新运行文件及可选薄sender辅助都进入其中。研究 runner 漏掉network_validation的事故应在迁移检查中用“公共运行模块集合完全列出”防止重演。
- 应用来自冻结规范化DAG，不是RFC数值。保留 `run-book-inputs.lock.json`、`book-input-sources.lock.json`、`media-feedback-inputs/inputs.lock.json` 的追溯关系；公开输入直接保存规范化JSON，不依赖运行时读取research路径。若复制来源说明/原始输入到公共configs，则加入统一input_hashes并给原文件/原SHA映射。
- PNG字节、PCM格式、模型时间/播放槽等依原输入说明区分固定文件字节与声明参数。此迁移不需要重新下载模型或用参数量推导音频wire。
- 公共JSON允许变化的仅来源引用元数据/根路径；不追加静默默认网络配置、不更改rtt_samples或业务完整性定义。

## 必要验收与执行顺序

先冻结迁移输入、保存全部研究/公共Python SHA及逐文件diff，再做以下有界检查：

1. 静态主体一致：Network、Application、两类validation、STREAM恢复选择，以及公共ACK/pacer/sender绑定。只白名单移除研究动态导入/CLI与来源封存包装，不能把函数整个排除比较。
2. 现有独立小例在公共API上实际执行：共享cwnd、多STREAM/MAX、DATAGRAM不重发/PING、取消有序缺口与端点、非抢占、高数字优先、反向ACK竞争、截图时序、观察截止。已有来源预写oracle保留，不以研究等值代替独立期望。
3. 19新场景公共/研究完整数学JSON逐项比较（来源元数据除外）；五大例必须实际重算，可逐文件读取，不能仅对摘要或重复使用研究值。核前后完整代码与结果manifest，含network_validation。
4. 旧接口回归：原16（旧10+控制器6）与ACK新增10，至少小例全跑并对四/三对应大例采用既有完整封存比较；最终管线实际重生成所有注册场景后逐JSON比对。输入为None仍是旧example，混合外层字段/错误DAG不应被旧路径吞掉。
5. 每个新场景实际CLI JSON/MD；MD必须含业务失败原因和实际指标，可靠文件未完成/过期缺音/旧截图不可显示成功。默认已有Markdown照旧可渲染。
6. 主代理协调全suite、reproduce、verify-results、章节同步和网页链接；只有上述阶段通过，才将当前“研究已验”更新为“公共接入已验”。本文件未执行这些公共迁移动作。

## 图与正文依赖

沿第12章12.3及扩写新加独立 `C68-media-feedback` 证据块，保持旧教学shared-media和握手实验的适用范围。`outline.py` 引用最终media-feedback结果ID与命令；不要恢复第13章或把本结果移到不存在的章节。

图12-4新增/更新面板应从公共完整结果直接提取：四格业务完成/首次播放/缺音/旧版本/取消，至少一段真实ACK与共享窗口的时间轴；此前同trace HOL教学图仍另标，不冒称此次四格同时改变了TCP/H3协议。若暂未完成画图，注册计算结果不自动勾选完整图12-4。图模块、CLI图入口、reproduce render/verify、manifest和本地链接由主代理协调，不能在网络迁移同时修改图逻辑导致验收变量增多。

本包不关闭匹配TCP/H3实测、握手与媒体统一、无线MAC ACK、RESET_STREAM或C69。公共迁移应先保持已经独立验证的有限数学与解释，进一步机制另开工作包。
