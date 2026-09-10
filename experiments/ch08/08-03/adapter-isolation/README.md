# 8-3：两个LoRA adapter的缓存身份与单槽切换

相同1536token输入依次运行基础模型、A、B再切回，基础模型和两个adapter首次使用均未命中彼此的前缀；各自重复请求及切回后均命中1520token。一个GPU adapter槽位实际完成A→B→A切换，而两个adapter保持CPU注册。

| 顺序 | 请求身份 | cached tokens | 请求结束时GPU槽位 | CPU注册ID |
|---:|---|---:|---|---|
|0|基础模型|0|空|空|
|1|基础模型|1520|空|空|
|2|A|0|80301|80301|
|3|A|1520|80301|80301|
|4|B|0|80302|80301、80302|
|5|B|1520|80302|80301、80302|
|6|A|1520|80301|80301、80302|
|7|基础模型|1520|80301|80301、80302|

最后一条基础模型请求的原生调度身份没有LoRA，但GPU槽位仍存A。槽位驻留不等于当前请求选择；同样，adapter退出GPU槽位不等于对应KV前缀必须失效。这里的观察只覆盖两个不同、固定名称和ID，不能当作认证、恶意名称冲突或多租户安全证明。

## 控制权重与实际记录

A/B是未训练的非零控制LoRA，各覆盖Qwen3-8B36层q_proj，rank8、alpha8、BF16。各72个A/B张量，标准库独立解析safetensors并核对形状、SHA和非零元素：A为2359296、B为2359294；两文件SHA不同。prepare.py按Torch2.11固定seed80301/80302和标准差.05生成，不从外部下载adapter，不将控制权重当作微调成果。

1055个只读调度快照逐项核对请求LoRA名称／ID、真实块引用和空闲／请求拥有／保留守恒；最终无请求、454空闲块加1保留块。worker的原生LoRA manager返回CPU注册表及GPU lora_index_to_id，确认槽位变化。未复制整个GPU权重张量或插桩投影差值，因此不声称本轮独立证明了每次LoRA数值乘加的效果。

八条请求全部完成64token强制输出，同身份复用前后输出精确一致；本合成重复文本下不同身份输出也全部相同。没有为获得不同文本而重跑，不能从相同输出反推权重相同或推断adapter质量。无自然任务成功率、并发租户尾延迟或加载速度排名。

实际vLLM0.23的kv_cache_utils.py以lora_name生成额外块哈希键，源码随包保存；本次请求使用不同不可变名称book-control-a-v1/b-v1及ID80301/80302。结果支持该固定身份条件下的KV命中隔离，不推断同名换权重的行为。

## 配置与独立复现

RTX PRO6000Blackwell、Qwen3-8B BF16固定快照、Torch2.11cu130；KV1GiB、APC开启、maxlen2048、maxseq1、chunk512、eager；一个GPU LoRA槽、两个CPU LoRA槽、最大rank8。greedy64输出、ignore_eos，配置及执行源码SHA保存在results/environment.json。只读观察器调用父调度器并保持返回值不变。

```sh
python reproduce.py --model /path/to/frozen/Qwen3-8B/snapshot
```

在同一vLLM环境的独立副本先移走封存run/results和analysis.json，再执行；输出存在则拒绝覆盖。已提供adapter文件，无需安装PEFT或重跑prepare.py。若研究新的控制权重，在另一空adapters目录运行prepare.py，不能要求新权重匹配旧manifest。独立分析仅需Python标准库。

results/保留全部输出、原始块快照和每次worker状态；source/保留实际安装的缓存键、LoRA请求和worker管理源码。verify.py核验封存并重跑分析，要求analysis逐字一致。最终guard exit0/41.493s、无残留或资源终止；无失败批次需清理，未停止其他服务或修改calculations。

实际trained adapter质量、投影数值效应、并发slot竞争／每租户延迟及完整多adapter部署仍待，8-3保持部分交付；全书最终跨session审计尚未开始。
