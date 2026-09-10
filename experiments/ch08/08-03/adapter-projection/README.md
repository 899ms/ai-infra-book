# 8-3：确认LoRA在真实投影中产生数值变化

在相同512行真实模型输入上，第0层QKV投影确实应用了两个控制adapter的Q增量，未适配的K、V部分逐元素保持不变。此前完整文本输出相同，不能据此判断LoRA未生效。

| 检查 | adapter A | adapter B |
|---|---:|---:|
| 改变的Q元素（总2097152个） | 2075974 | 2074420 |
| Q增量相对CPU FP64参考误差 | 1.3271% | 1.4141% |
| Q完整输出相对参考误差 | 0.1681% | 0.1657% |
| K、V与基础输出逐元素一致 | 是 | 是 |
| 运行时Q adapter张量与封存权重一致 | 是 | 是 |

增量审计预设2%相对L2界限，两项通过；它用于容纳该BF16实现与FP64数学重建之间的舍入差异，不是模型任务质量门槛。并未调大阈值或更换权重来获得通过。

## 捕获与独立核验

复用 [adapter-isolation](../adapter-isolation/README.md) 的两份非零、未训练rank8控制权重。新运行分别调用基础模型、A、B，APC关闭，取原合成提示的前512token；每个请求仅强制生成1个token，用于触发完整模型执行，不作答案质量评测。三请求全部正常完成。

只读forward hook安装在实际`model.layers.0.self_attn.qkv_proj` LoRA包装模块，保存完整输入[512,4096]、输出[512,6144]，以及该GPU槽的三组LoRA A/B堆叠张量。三个输入逐元素相同。前4096维是Q，后1024+1024维是K、V；实际包装实现源码在results/native_projection.py，模块身份及源码SHA在capture.json。

分析器独立解析原safetensors BF16张量，检查运行时Q的A/B精确匹配、K/V适配张量全零，然后在CPU FP64计算`(X @ A.T) @ B.T`（alpha/r=1），与实际adapter输出减基础输出比较。FP64完整输出参考是捕获的基础BF16输出加该增量，不冒充从原基础模型FP64权重重算的投影。

RTX CPU审计先生成analysis.json，Mac M2 Max CPU以Torch2.14重算，所有离散判断一致，浮点报告在1e-10相对／1e-12绝对容差内吻合；该跨CPU报告复核容差与上述2%增量误差界限不同。未依赖NumPy或PEFT。

这验证第0层的完整512行QKV数值路径，不代表其他35层逐层验证、训练质量或推理加速。捕获会增加CPU复制开销，不使用本轮时间做性能排名。原两份adapter权重和此前结果未修改。

## 独立复现

相同vLLM0.23/Torch2.11cu130环境，独立副本中先移走run/results/analysis.json，执行：

```sh
python reproduce.py --model /path/to/frozen/Qwen3-8B/snapshot
```

输出目录存在则拒绝覆盖。只核对已有证据可在安装Torch的CPU环境运行：

```sh
python analyze.py --check
python verify.py
```

目录自带adapter、hook、驱动和审计，无相邻实验或calculations执行依赖。三个.pt均为实际捕获，所有源SHA、原始请求与worker状态保留。最终guard exit0/13.825s、无资源终止或残留；没有失败批次需清理，未停止其他服务。

本项补上此前仅有身份与槽位证据的数值缺口。trained adapter质量、并发槽竞争、每租户尾延迟与全书最终跨session复核仍待。
