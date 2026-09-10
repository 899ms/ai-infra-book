# 公共接入独立审查：PASS

已实际执行 `python calculations/research/transport-closed-loop-integration/check-public.py`。九个小场景的公共 API 输出与冻结候选逐数学字段相同，涵盖上传/模型/响应、cwnd、绝对额度、反馈判失、PTO、ACK 丢失、有限路由器丢弃、消费更新及缺额度未完成。仅排除两项明确变化的来源路径/元数据字段，未通过舍入、忽略时间字段或只比较总时间放宽等价性。

另实际验证默认 `calculate()` 与候选默认输入一致，运行公共 CLI 的 JSON 和 Markdown 输出。CLI 使用绝对流控消费样例，JSON 与同输入公共 API 完全相同；Markdown 非空且是该 topic 报告。具体文件 SHA256 见 `public-check.json`。

公共来源映射保持三个闭环依据：RFC9000、RFC9002、Verified Errata7539；sender 兼容 DATAGRAM 分支额外复用 RFC9221。四个 revision 在公共总锁各出现一次，逐份 read_source 核字节与哈希通过。新增勘误独立 provenance group，不改变旧 protocol-rfc 七条合同。ACK Delay 边界和勘误适用性见 `SOURCE-MAPPING.md`，没有将未经修正的 RTT 次序作为另一个模式。

这是公共 API/CLI 接线与来源适配检查。独立物理手算、三个路由器边界和原书 30MB/5MB 的九组验收在 `../transport-closed-loop/independent-check.json`；本次不重复执行大型路径，不自行全量 reproduce。公共完整流水线、大结果重生和 PLAN 由根任务验收；媒体、多流、CUBIC/BBR 闭环仍未因本次公共接入完成。

## 完整交付补验

根要求的完整交付审查已实际执行 `check-delivery.py` 并通过：10 个公共固定 JSON 逐全部数学 payload 对冻结候选结果相同；随后以 book.json 中各场景的实际输入调用 CLI，共 20 次（每场景 JSON 与 Markdown），所有输出与现有公共 results 整文件逐字节一致。包含两次原书 30MB/5MB 的实际计算，不只复用小例或比较汇总。

调用前后公共 transport_closed_loop、transport_sender、CLI、总来源锁和 book 场景文件 SHA256 完全相同。详细 20 次文件大小/哈希与耗时见 `delivery-check.json`。此次只执行指定 topic，未触发或替代根的全量 reproduce。
