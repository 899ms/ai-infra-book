# Transport controller loop 公共接入依赖清单

本清单是当前文件字节快照与接入建议，不是公共交付声明。网络候选仍在大场景审查；下表网络/适配器 hash 可能随修复更新。固定算法已审查证据保留在研究目录，接入时应分别记录迁移前 hash、公共目标 hash 与仅导入/来源包装差异。本次只读取代码与本地来源锁、核对文件字节，没有重跑算法测试。

所有表格路径以 `calculations/` 为基准；建议目标以 `src/infra_calc/` 为基准。新增一个 `transport/` 包和 `__init__.py` 收纳共享状态组件，业务入口继续用现有 `topics/transport_closed_loop.py`，不另建一套独立闭环脚本。

## 实现文件与依赖边界

| 研究输入 | 建议公共目标 | 依赖/处理 | 当前 SHA256 |
| --- | --- | --- | --- |
| `research/transport-controller-loop/calculate.py` | `topics/transport_closed_loop.py` | 扩展现有唯一网络引擎；依赖 sender、pacer，保留旧默认场景 | `97a12a1c2e94e58d31ed370b098ef576cf9575451d75097973c19f43c16552dc` |
| `research/transport-controller-loop/sender.py` | `topics/transport_sender.py` | 替换经回归认可的发送状态实现；依赖两adapter与persistent；不可双份复制发送器 | `be435d7222f2531f485e23611633c8622b3385d7ecb3e8406342b7b9a1e7b77d` |
| `research/transport-controller-loop/pacer.py` | `transport/pacer.py` | Fraction分段债务；无控制器内核依赖 | `7d5b55d04d52b9c14c96b7de0eec03ecb531d258c3d25489d07781c74209b510` |
| `research/transport-controller-loop/persistent_congestion.py` | `transport/persistent_congestion.py` | RFC9002证据谓词；无控制器依赖 | `116448af2c5c8c1bc0571c1452b032b01f3300771dae9a7e8bc7ac5ea8833a7f` |
| `research/transport-controller-loop/cubic_adapter.py` | `transport/cubic_adapter.py` | 依赖cubic、hystart；QUIC传输frontier与显式数值网格 | `cdfc2c64e387dc48e7e940d67885cfc2630f8423800976373d968b458045dc42` |
| `research/transport-controller-loop/bbr_adapter.py` | `transport/bbr_adapter.py` | 依赖bbr_state、bbr_reference；PN采样/增量flight/late ACK/EDT | `606b263d23d8c7917fd6deab94378a4639b343c43bf35087937eb9eebe7d66ba` |
| `research/congestion-controllers/cubic.py` | `transport/cubic.py` | RFC9438与RFC5681纯状态；不依赖BBR | `91be0851fb7a2e947e42578e8703bd098df98ba7432672440a2f81e677282836` |
| `research/hystart-plus-plus/calculate.py` | `transport/hystart.py` | RFC9406纯状态；保留状态API，移除独立CLI包装 | `4eb38d1b4e09a4d5922a89a6bbcb7127ed4cfbf4678afb94323aea6eb3cb139d` |
| `research/congestion-controllers/bbr_state.py` | `transport/bbr_state.py` | 依赖bbr_minmax和bbr_reference；固定Linux状态端口 | `fda8c57569767c94c9bbdbeca7e0155425542ade3c9f9356db188a131b9127c6` |
| `research/congestion-controllers/bbr_minmax.py` | `transport/bbr_minmax.py` | 依赖bbr_reference.u32；固定三样本running max | `07cdbf94e82d20115657810522d09461422815ccca539d9e61ce23ebb1397b28` |
| `research/congestion-controllers/bbr_reference.py` | `transport/bbr_reference.py` | 整数单位/时间戳/rate纯函数；官方来源接口需要公共化 | `bce5ee725bb7027195fae50356d8ddb95f8441a4721e21eaac548beeede8ba05` |

## 官方原件及公共锁复用

公共 `src/infra_calc/sources.py` 的 `records()` 读取 `configs/sources.lock.json` 的 `sources` 数组；`read_source(file)` 对唯一 downloaded 记录核 bytes 与 SHA256；`provenance(model)` 提供结果元数据。应复用此机制，新增来源记录必须保留精确 URL/revision/bytes/hash；研究锁的自定义 status 不能直接原样当公共 downloaded 状态。

下表逐一读取研究原件核对了锁中 bytes/hash，并按 SHA256 查找公共锁中已有原件；同 hash 已有公共文件直接复用。没有重新下载，也不把一次 errata 查询快照当永久无勘误保证。

| 研究原件 | bytes / SHA256 | 官方 URL 与 revision | 公共复用或建议目标 |
| --- | --- | --- | --- |
| `research/transport-controller-loop/sources/rfc9000.txt` | 403442 / `f88aae47f8b18e102024916e975e919201d8dde689cba79b01079eaedd402e22` | [RFC9000](https://www.rfc-editor.org/rfc/rfc9000.txt) | 复用 `sources/protocol-rfc/rfc9000.txt` |
| `research/transport-controller-loop/sources/rfc9002.txt` | 89071 / `3a8a54eea1ad5d1c134a548bf15edfa0e21bfb4106dbd7db3c09cace842099af` | [RFC9002](https://www.rfc-editor.org/rfc/rfc9002.txt) | 复用 `sources/protocol-rfc/rfc9002.txt` |
| `research/transport-controller-loop/sources/rfc9002-errata7539.html` | 8446 / `685a6ef4fabde4fe163d1e86d6fb7aea7ded40ceab07a8a70e8027a4a9d0e23a` | [RFC9002 Verified Errata7539](https://www.rfc-editor.org/errata/eid7539) | 复用 `sources/protocol-rfc/rfc9002-errata7539.html` |
| `research/congestion-controllers/sources/rfc9438.txt` | 73704 / `baa4dd77295e27b9fa5c79993e962e70f728409bd1a48b9029bae4b551b0348a` | [RFC9438](https://www.rfc-editor.org/rfc/rfc9438.txt) | `sources/congestion-controllers/rfc9438.txt`（新增） |
| `research/congestion-controllers/sources/rfc5681.txt` | 44339 / `a2d99a2421d5c57b248394f26ba44fc364aa546680fbf10ff0aa7034dad8b87d` | [RFC5681](https://www.rfc-editor.org/rfc/rfc5681.txt) | 复用 `sources/connection-window/rfc5681.txt`, `sources/protocol-rfc/rfc5681.txt` |
| `research/hystart-plus-plus/sources/rfc9406.txt` | 18917 / `43e3ddc1d3446142b125f018cd52aa2ff858b3f1ff9c6969924ab9fbf45d5230` | [RFC9406](https://www.rfc-editor.org/rfc/rfc9406.txt) | `sources/congestion-controllers/rfc9406.txt`（新增） |
| `research/hystart-plus-plus/errata-check.html` | 7052 / `4765d07ace49aa20e0ce7001016c50329f1309640d1e0a024a5577c0494572db` | [RFC9406 errata search snapshot 2026-09-09](https://www.rfc-editor.org/errata_search.php?rfc=9406) | `sources/congestion-controllers/errata-check.html`（新增） |
| `research/congestion-controller-inputs/sources/tcp_bbr.c` | 42724 / `ba7d0706259dfef5bf455f26ac4bab65f43b9209b9cfd4f761c64c89816bdfe4` | [ffc253263a1375a65fa6c9f62a893e9767fbebfa](https://raw.githubusercontent.com/torvalds/linux/ffc253263a1375a65fa6c9f62a893e9767fbebfa/net/ipv4/tcp_bbr.c) | `sources/congestion-controllers/tcp_bbr.c`（新增） |
| `research/congestion-controller-inputs/sources/tcp_rate.c` | 8436 / `52d682c760573819a36bfef45a094ea8615a39d56c0248569d96f9e6e47b2b23` | [ffc253263a1375a65fa6c9f62a893e9767fbebfa](https://raw.githubusercontent.com/torvalds/linux/ffc253263a1375a65fa6c9f62a893e9767fbebfa/net/ipv4/tcp_rate.c) | `sources/congestion-controllers/tcp_rate.c`（新增） |
| `research/congestion-controller-inputs/sources/tcp.h` | 78187 / `de555f117e5b039040c94ce693ba5e0c74bb7a4f11df00e0d72de95988f1b553` | [ffc253263a1375a65fa6c9f62a893e9767fbebfa](https://raw.githubusercontent.com/torvalds/linux/ffc253263a1375a65fa6c9f62a893e9767fbebfa/include/net/tcp.h) | `sources/congestion-controllers/tcp.h`（新增） |
| `research/congestion-controllers/bbr-sources/win_minmax.h` | 832 / `deef538ecd6a56ed99345497b254b1c480f45b1a5b0cb3e30a37bd4a9420db31` | [ffc253263a1375a65fa6c9f62a893e9767fbebfa](https://raw.githubusercontent.com/torvalds/linux/ffc253263a1375a65fa6c9f62a893e9767fbebfa/include/linux/win_minmax.h) | `sources/congestion-controllers/win_minmax.h`（新增） |
| `research/congestion-controllers/bbr-sources/win_minmax.c` | 3435 / `6d7fabb8cdb2a53e485341435483b408a0183f4e349cf894343ac5febcb3fe86` | [ffc253263a1375a65fa6c9f62a893e9767fbebfa](https://raw.githubusercontent.com/torvalds/linux/ffc253263a1375a65fa6c9f62a893e9767fbebfa/lib/win_minmax.c) | `sources/congestion-controllers/win_minmax.c`（新增） |

Linux BBR 的 `tcp_bbr.c`、`tcp_rate.c`、`include/net/tcp.h`、`lib/win_minmax.c`、`include/linux/win_minmax.h` 全部固定 commit `ffc253263a1375a65fa6c9f62a893e9767fbebfa`。无需拉整库或运行时编译 C；原样 C harness 是研究验收证据，不是公共计算依赖。RFC9438/CUBIC、RFC9406/HyStart++ 与 Linux v6.6 BBR 不应合称同一个 Linux TCP 控制器实现。

## 动态导入和来源读取迁移

1. `calculate.py` 的 `spec_from_file_location` sender/pacer 改为包内静态导入；`sender.py` 的 adapter/persistent 动态导入同样改为明确模块或工厂映射。保留独立 NewReno 默认行为，不根据是否能导入临时研究文件选择控制器。
2. `cubic_adapter.py` 的 `pinned_module` 及硬编码研究路径改为 `from . import cubic, hystart`；`bbr_adapter.py` 去掉 `sys.path` 插入和研究相对路径；`bbr_state.py`、`bbr_minmax.py` 的裸导入改为相对导入。纯算法数学主体与整数位宽不变。
3. 统一 `transport/reference_sources.py` 或同等小来源函数使用公共 `read_source`/`provenance`，按实际控制器选取来源；CUBIC sources、HyStart verify_sources、BBR reference.sources、sender 与 persistent 的研究目录读锁均替换为这一层。不要把 RFC9438 当 NewReno 必需算法依据，也不要漏掉 BBR minmax 与 tcp.h。
4. `bbr-adapter-lock.json` 当前锁的是研究 Python 实现，不能误作为官方源文件锁；公共 Python 自动进入复算代码 hash 清单，另在迁移记录保存研究前后 hash 与证据引用。公共包不得运行时依赖 `research/` 中的 .py 或锁。
5. 研究 calculate.py 内置 scenarios()/argparse、各 controller 的独立示例 CLI 不迁为一堆入口；保留需要的状态 API，有限输入统一放 scenarios，复算统一注册。原 harness/check/独立审查 JSON 留作研究证据。

## 现有公共注册位置与需要增量修改处

- `src/infra_calc/cli.py`：已有 topics import（约36行）、`transport-closed-loop` parser（约294行）、dispatch（约1167行）。优先扩展既有命令的输入 schema，不必增加另一个几乎同义 CLI。
- `scenarios/book.json`：已有 `transport_closed_loop` 分组；新三控制器有限输入作为 `{id, inputs}` 加入此组，建议新 id 前缀 `controller-loop-`，旧 `closed-loop-*` id 与默认不填充语义保持。可提供 `scenarios/controller-loop-example.json` 作独立 CLI 输入；前缀此处只是建议，最终以 root 注册为准。
- `src/infra_calc/reproduce.py`：已有协议循环（约439行）调用 `module.calculate(row["inputs"])` 并 save JSON/Markdown，再进入 protocol_rows 索引。因此沿现有分组无需再写一个结果执行器。生成结果位于 `results/<id>.json` 与 `.md`，manifest 按既有 run()/verify_results() 更新。
- `reproduce.py:input_hashes()` 已递归收集 `src/infra_calc/**/*.py`、configs/*.json 与 book.json；新增 `sources/congestion-controllers` 原件必须显式纳入输入收集（或按新增公共锁记录枚举），不能只让锁变了而原件不进入 manifest。
- `src/infra_calc/outline.py` 目前 transport 段（约1101行）明确尚无 CUBIC/BBR 自适应 pacing；必须等公共验收后由 root 更新这一范围声明。不要提前删掉限制，也不要恢复用户已拆分的旧章节结构。
- 后续绘图如采用新结果，使用现有 render/verify/data/manifest 模式，精确列出实际 result、source、config 输入；现有 shared-media 图不能凭新引擎存在就声称覆盖自适应控制器完整对照。

## 接入前应保留的验收边界

已固定的 CUBIC/HyStart/BBR/minmax 算法证据与新 QUIC 适配验收是两层：BBR 的每 PN 采样、原 PN late ACK、控制包填充、packet/UDPbytes 单位、external EDT、app/flow limited 和 recovery 都需保留合同。三控制器主对照统一 pad_in_flight=True；已有不填充 NewReno 教学场景不偷换输入。发送器共同 pacer 使用分段债务，不混入 adapter 内部旧 deadline 诊断。

网络大例尚未在本清单宣称验收通过；实际业务成片时间还受固定业务输入、即时 ACK、队列容量、drop trace、消费与服务耗时假设影响。接入需先冻结网络与适配器 hash，再做公共/研究数学 payload 对照；允许变化只限明确来源元数据/路径，不能把重新编号或 trace 丢字段当作等价。

公共接入应迁移一个实现依赖图，保留旧研究快照作证据；不复制 C harness 生成物、完整大 trace 或研究 baselines/ 历史 adapter 为第二套公共实现。
