## Multi-turn remote measurements and matched recomputation

[Default-threshold Chat/Agent replay](cross-mac-traces-001/README.md), [short-Chat threshold16 variant](cross-mac-chat-threshold16-001/README.md), and [cache-disabled control](trace-cold-control-001/README.md) completed 88 requests. All paired one-token outputs, page hashes and cleanup checks passed. Default Chat makes no remote GET; Agent fetches110 pages, threshold16 Chat fetches15. Higher token hit rates accompany longer request time on this connection. Matched three-policy remote routing record comparison remains pending.

## 2026-09-15: cross-Mac recovery verified

[Attempt 005](cross-mac-005/README.md) successfully published 65 pages and recovered 64 in a fresh RTX consumer from the Mac. First consumer response: 1008 storage-cache tokens, 82.641923 s; all six outputs identical, all page hashes verified, processes cleaned up. This is recovery feasibility, with full Chat/Agent remote routing still pending. Earlier failures below are retained as historical evidence.

# 网络KV：跨Mac失败与同机Docker恢复控制

SGLang0.5.13.post1原生HiCache通过dynamic storage接口接入本目录的HTTP后端，保留原生页布局与key命名。模型完整运行于rtx-pro，KV页实际跨机器传至Mac文件存储；HTTP仅监听127.0.0.1，经独立SSH反向隧道18799→18798。原生运行时相关源文件及SHA在runtime-source/。没有用预制响应或客户端缓存替代模型KV传输。

跨机器功能检查004已终止：固定1024输入token、16强制输出，生产者请求三次并等待完整64输入页发布；退出后新引擎再请求三次，须同时核验真实remote get、原生命中来源和完整输出一致。每页2,359,296 bytes，六页共14,155,776 bytes的成功传输及SHA已经独立核验，单页约60秒；此后HTTP超时，消费者未启动，不能据收到部分文件就认定完整恢复。`analyze_smoke.py`只在两引擎完整结束后接受全部证据，目前未通过或生成成功结论。

## 保留的尝试

- 001：三个生产者和三个消费者请求都返回，但两进程首请求都是冷缓存；固定等待5秒不能覆盖异步上传。后续仅出现部分未确认页，不能算持久化或远端复用。
- 002：完整批量上传在120秒socket窗口超时，原生backup线程退出；240秒发布检查失败，消费者没有启动。模型仍能推理，说明模型可用不证明存储链路正常。
- 003：改成最多8页/HTTP仍触发120秒上传超时。记录该失败后，向本次coordinator发SIGINT以执行finally清理，无GPU残留；没有继续空等已死的backup线程。
- 004：每个HTTP仅1页，120秒单调用超时不变，发布上限3600秒、每引擎总上限4800秒。收到server库存且client set已成功确认才计发布；任一RPC失败立即终止。完整1024token与64输入页未缩减。按当前约60秒/页，3600秒上限可能不足；若发生必须保留失败，不能抹去或把部分页计成完整通过。

前三版的代码和协议各保存在smoke-00N-source/，输出与日志在results-smoke-00N/，Mac收到的文件和服务账本在mac-store-smoke-00N/；未覆盖原件。每次使用新Mac存储目录，不把较早失败的部分页混入后续成功率。

`store.py`保存HTTP请求／响应元数据、逐页SHA和实际payload字节数；`remote_backend.py`对GET字节数与SHA校验后才写入CPU目标张量。文件逐页以临时文件rename发布，但没有fsync，不能声称掉电持久性。HTTPpayload不是链路总字节，计时包含SSH、真实链路、协议、CPU和文件页缓存；没有独占WAN或物理SSD带宽保证。两机器单调时钟不能直接相减，client操作时长与server自身时长分别保存。

这不是Mooncake／RDMA性能，单次功能检查也不能替代9-9完整路由比较或9-8层级容量矩阵。`trace-inputs.json`已经固定原4轮Chat与12轮Agent输入及来源SHA，待功能验证后扩展。原Chat有算术错误、Agent原任务失败；后续重放输入固定，不将新的短输出反馈进原轨迹或宣称任务成功。

## 004终态与Docker控制

004生产者exit1、监督记录无GPU残留；SSH会话也以255结束，错误为本地地址不可用／broken pipe。已停止Mac存储进程，原页与账本保留。严格docker-control在成功取回后因重复键字节不同失败。独立[docker-immutable](docker-immutable/README.md)采用原生先写保留语义，完成两引擎六请求，storage命中1008token，输出一致、SHA与清理通过；另保存并分析一页重复键差异。此页是生产者第65个发布，不属于消费者64个get，未验证未来使用该页的数值行为。该控制不替代跨机器数据，也未补齐Chat／Agent远端路由及容量矩阵。
