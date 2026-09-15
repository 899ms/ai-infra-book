# V4四道多键检索：全部完成

2026-09-14在作者独占的rtx-pro GPU上，完整固定V4-Flash-0731模型完成四个已冻结输入，**4/4精确三键JSON且自然stop**。Mac独立复核输入／采样、实际文档键值、重复键拒绝、输出ID、调用记录、源码SHA、监督退出与实际KV池日志。此前Qwen3-8B相同消息记录为3/4；四道题事先已知，不作为盲测或总体质量排名。

|案例|输入token|输出token|请求墙钟秒|精确JSON＋自然结束|
|---|---:|---:|---:|---|
|n512-r0|4148|28|316.199483|通过|
|n512-r1|4148|28|219.481312|通过|
|n512-r2|4148|28|217.245122|通过|
|n512-r3|4148|28|214.924986|通过|

运行使用revision `7872f01b1d1fe23eabc4c98b48bffcef5a386062`完整43层、既有私有SGLang兼容路径，CPU offload100GiB、context/max_total_tokens5120、输出上限128、temperature0、原生EOS生效。dtype参数BF16不代表纯BF16权重：实际加载日志明确quant=fp8、fmt=e4m3。最终实际池full/swa5120、c4=1280、c128=40、c4_state=320、c128_state=5120。日志中较早自动估算112640不是最终池，完整两组原文保留。

[协议](PROTOCOL.md)记录从110GiB offload调整到100GiB的原因。前一次运行因全局RAM阈值中断，已保留；本次四题从头执行，没有拼接结果。较首请求更短的后续耗时可能含初始化／编译复用因素，CPU背景工作未隔离；不把这些墙钟用作Qwen与V4或两种offload配置的性能排名。

监督正常exit0、reason=null、leftovers=[]，后续nvidia-smi确认没有GPU进程后才启动下一实验。资源采样极值在[analysis.json](analysis.json)。这些检索成功不解除既有独立小矩阵数值门槛，`strict_numerical_clearance=false`保留；也不证明其他模型、长上下文或工具任务的质量。

复核：`python3 analyze.py`，无需GPU或加载模型。原响应、输入、进程与环境／兼容原件位于`runs/multikey-exclusive-100-001/`；本地未复制编译cache、tmp和include-overlay，运行证据及源代码已取回。复跑需新name和固定远端运行环境，按`reproduce.py --execute --name NEW_NAME`执行，仍检查原140GiB RAM／80GiB GPU启动门槛和运行期阈值。
