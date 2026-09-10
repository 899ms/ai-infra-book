# 两个图像生成代表：固定源码与可复算矩阵账

2026-09-09。所有新增材料在本目录，`sources.json`逐项记录URL、完整revision、字节、SHA256。diffusers固定到`040c7cde626504d14caf63b13b8b25b6a9f62120`；GitHub返回的revision元数据保存在`diffusers-revision.json`。只读取源码，不安装或执行远程代码；没有生成图片、下载权重或测量性能。

## 已核的关键区别

Qwen-Image-2512模型revision `25468b98e3276ca6700de15c6628e51b7de54a26`，FLUX.2-klein-4B为`e7b7dc27f91deacad38e78976d1f2b499d76a294`。component config已存在于公共`calculations/configs/models/`，不重复改写。

- [Qwen pipeline](https://raw.githubusercontent.com/huggingface/diffusers/040c7cde626504d14caf63b13b8b25b6a9f62120/src/diffusers/pipelines/qwenimage/pipeline_qwenimage.py)：170–173与prepare_latents、584行证明VAE空间8倍和外部2×2 packing；`in_channels//4=16`。64已是packing后宽度，不能再乘4。输出投影的`patch_size²×out_channels=4×16=64`与输入一致。
- [FLUX pipeline](https://raw.githubusercontent.com/huggingface/diffusers/040c7cde626504d14caf63b13b8b25b6a9f62120/src/diffusers/pipelines/flux2/pipeline_flux2_klein.py)：200、369–395、490–509、788、905–918证明VAE空间8倍，raw32通道到packed128；生成noise直接建立packed通道形状，pack仅展平空间，不再patchify。VAE最终前才unpatchify。
- 1024²→raw latent空间128²→2×2打包4096图像位置。Qwen张量`[B,4096,64]`、FLUX`[B,4096,128]`；BF16、B=1分别512KiB和1MiB。单帧Qwen的时间维为1，不应用视频时间压缩。
- [FLUX官方model_index](https://huggingface.co/black-forest-labs/FLUX.2-klein-4B/resolve/e7b7dc27f91deacad38e78976d1f2b499d76a294/model_index.json)有`is_distilled=true`。pipeline593–594由`guidance_scale>1 and not is_distilled`决定trueCFG；不能由transformer的`guidance_embeds=false`推出是否运行CFG。所选distilled4B即使guidance=8也只跑一次分支。
- Qwen pipeline548–583、640–673：trueCFG要求scale>1且存在negative prompt，正/负两次顺序forward，然后含norm的重缩放；正负文本长度可以不同，完整矩阵FLOPs不必正好翻倍。

## DiT矩阵预算

统一D=3072，图像位置I，实际DiT文本embedding长度T，S=I+T，B为图像batch。乘加按2 FLOPs，非因果joint attention的QK+PV为`4BS²D`每层。Qwen的T须来自模板截取后的embedding；FLUX默认max_length512，text encoder9/18/27层输出拼成7680维，不能把三层拼接误算成1536文本位置。

[Qwen transformer](https://raw.githubusercontent.com/huggingface/diffusers/040c7cde626504d14caf63b13b8b25b6a9f62120/src/diffusers/models/transformers/transformer_qwenimage.py)633–679、870–906：60双流块；每流Q/K/V/out是D→D；`FeedForward(gelu-approximate)`使用[FeedForward默认mult4](https://raw.githubusercontent.com/huggingface/diffusers/040c7cde626504d14caf63b13b8b25b6a9f62120/src/diffusers/models/attention.py)，FF是D→4D→D。合并两流每块线性工作`24BSD²`，但图像/文本权重并不共享。每块还有两套按batch执行的D→6D调制，额外`24BD²`，不乘S。

[FLUX transformer](https://raw.githubusercontent.com/huggingface/diffusers/040c7cde626504d14caf63b13b8b25b6a9f62120/src/diffusers/models/transformers/transformer_flux2.py)301–324、748–784、807–912、1140–1219：5双流+20单流；FF为SwiGLU，inner=3D，输入D→6D，输出3D→D。双流的QKVO+FF为`26BSD²`；单流融合矩阵D→9D和4D→D，仍为`26BSD²`，每块另加`4BS²D`。三套调制分别D→6D、D→6D、D→3D，仅每forward一次共享，合计`30BD²`，不能再乘25层。

两者还计入图像输入、文本输入、时间MLP(256→D→D)、输出AdaLN条件投影D→2D和图像输出投影。Qwen输入/输出宽64、文本宽3584；FLUX128与7680。bias、Norm、激活、RoPE、Softmax、CFG重缩放和scheduler更新不在矩阵FLOPs里，必须明确列缺项。

当I=4096,T=512,B=1，按独立闭式与逐矩阵求和均得：

| 模型 | 单分支、单forward矩阵FLOPs | 题设步骤与分支 | 去噪矩阵FLOPs |
|---|---:|---|---:|
| Qwen-Image-2512 | 78,303,922,225,152 | 50步、2分支 | 7,830,392,222,515,200 |
| FLUX.2-klein-4B | 34,820,178,051,072 | 4步、1分支 | 139,280,712,204,288 |

步骤50和4采用已归档官方模型卡示例：`calculations/research/generative-media-candidates/Qwen--Qwen-Image-2512/README.md`87行及`black-forest-labs--FLUX.2-klein-4B/README.md`70行。模型卡在候选manifest里已有来源，当前独立image-generation锁主要封存实现与model_index；若后续希望单模块来源也直接展示模型卡，可将这两原件纳入独立锁。步骤均是输入，不把scheduler的1000训练timesteps当推理步数。

## 文本/VAE与边界

文本encode在去噪循环前一次/分支，VAE decode在完成去噪后一次batch；latent-only输出不调用VAE。仅列文本embedding输出、raw/packed latent、声明dtype的RGB张量字节；两个阶段的内部FLOPs、完整生成FLOPs及时间均为null。不能把RGB float张量12MiB说成PNG/JPEG文件大小，也不能据VAE force_upcast字段推断全部实际运行dtype。静态VAE内部卷积、时序缓存、归一化与中间激活仍需后续专项审计。

## 已实施状态与验收

后续主代理授权后已独立实现`calculations/src/infra_calc/topics/image_generation.py`与`tests/test_image_generation.py`，3项专用测试通过：小坐标bijection验证packing；两个模型的独立闭式验证全部列出的矩阵；调制只算一次/逐层区别、CFG正负不同长度、distilled忽略guidance、步骤和text/VAE调用分离、未计项保持null及尺寸不整除拒绝。

源码与独立锁当前已暂停修改，等待主代理统一集成CLI/reproduce/outline。本模块不是完整DiT/文本/VAE参数索引核验、完整生成工作量或可达性能声明；保持简短正文算例，完整矩阵表由CLI输出。

## 按书的定位组织：步骤、依赖与资源需求

正文应围绕一次生成请求怎样完成，把模型结构压缩为产生这些需求的配置输入。建议用下面的执行路径，矩阵表留在附表或CLI；不用模型架构介绍占据主篇幅。

```text
prompt/tokenizer
  → text encoder conditional ─────────────→ 条件embedding（跨全部去噪步保留）
  → text encoder unconditional（仅真CFG）→ 负条件embedding（同上）
noise初始化/packed latent
  → 对每个 scheduler timestep：
      DiT conditional(latent, timestep, cond embedding)
      → DiT unconditional(同一latent, timestep, neg embedding)〔仅真CFG；固定pipeline串行〕
      → CFG合并/归一化重缩放〔仅真CFG〕
      → scheduler更新latent
      → 下一个timestep
  → unpack/denormalize
  → VAE decode〔输出图片时〕
  → postprocess/图片编码/交付
```

Qwen真CFG是一个循环迭代中两次模型调用，不是两张独立输出图片；distilled FLUX同一步只有一分支。两分支使用同一套DiT权重，不能将权重容量乘2。依赖跨step严格串联；同一请求的后一步不能仅因有空闲GPU就提前计算。不同请求或batch的并行需另给队列与放置，不能由单请求的FLOPs比直接得到吞吐比。

### 现有产物能给出的每步与每请求账

| 资源/量 | 已有依据 | 计量边界 |
|---|---|---|
| 每分支每step矩阵FLOPs | `image_generation_matrices`逐GEMM、QK、PV | 全部已列矩阵，非矩阵和text/VAE未知 |
| 每step矩阵FLOPs | 加本步全部分支，各自保留T | 正负T不同不能简单乘2 |
| 每请求去噪矩阵FLOPs | 上项×固定实际循环步数 | 不包含完整请求其余阶段 |
| 每GEMM接口字节 | lhs/rhs/output逻辑字节 | 单分支单forward、每矩阵一次、列明block repeats；不是HBM实测 |
| 每请求上述接口需求 | 对各分支的逻辑字段求和再乘steps | 是给定未融合数学接口账，不用于宣称已搬相同HBM字节 |
| 常驻矩阵权重子集 | 一份conditional路径的matrix_weight_elements | 参数容量不乘steps/CFG/batch；bias/norm、text、VAE权重仍缺 |
| 跨step保留边界 | packed latent、正/负text embedding | 已精确计算张量容量，不能据此当全部live memory |
| 输出边界 | raw latent、明确dtype的RGB tensor | 文件codec/字节未知，不能用RGB量替代网络计费 |

1024²、B=1、BF16时，Qwen current latent为0.5MiB，FLUX为1MiB；Qwen512文本位置的每分支embedding为3.5MiB，FLUX512位置embedding为7.5MiB。Qwen真CFG须保留两份embedding，总7MiB；不把它们与循环内临时对象混称完整峰值。

**live memory尚需补独立生命周期账。** 当前实现没有输出系统峰值；其权重小计、边界latent、GEMM输出不能直接相加得到峰值。下一项应沿固定pipeline/attention后端标记：权重常驻/卸载、text embedding常驻、当前latent、cond/neg prediction、CFG组合及norm缓冲、scheduler旧/新latent、block中间与attention scratch、VAE输入/输出及workspace。Qwen分支串行可复用部分block临时区，但cond prediction在negative forward时仍存活；这些是应测试的生命周期依赖，不是当前实测峰值。框架变量、张量alias、融合、缓存allocator与释放时刻均可能改变真实live set。大型全score逻辑输出尤其不能误算成FlashAttention必需常驻量。

### 关键路径、期限和吞吐的验收

单请求有声明的串行时间关系可写为：

`T_request = T_prepare + T_text_cond + [T_text_neg] + Σ_s(T_DiT_cond,s + [T_DiT_neg,s + T_CFG,s] + T_update,s) + T_VAE + T_postprocess + T_delivery`。

这给测量与阶段缺项表，不自动给数值。权重加载是否冷启动、offload传输是否暴露、text/VAE能否在别的请求旁重叠、各步是否重复编译、scheduler/同步开销均需明确。T_text/T_VAE未知时整体时间仍未知；不许拿去噪矩阵FLOPs除峰值填上整张图片时间。

对目标q张/s，去噪矩阵供给至少满足`q × 每请求去噪矩阵FLOPs ≤ 可用同精度dense矩阵FLOPs/s`，但这只是必要条件；向量/Softmax、memory、text、VAE、CPU codec、传输分别需独立供给，且共享同一设备时不能给每个阶段都分配整卡。q乘逻辑GEMM接口字节也不能直接当HBM带宽需求；必须先确定融合与驻留的实际接口。需要latency SLO时，所有串行依赖和排队加入；需要cost/image时分母是满足同质量和期限的交付图片，不是NFE数或名义采样张数。

优先补测记录应至少含：固定model/source revision、真实text与negative长度、H/W/B、dtype及是否量化、有效timesteps与每步真实调用、每阶段GPU事件和跨引擎墙钟、attention后端、冷/热状态、CPU/GPU权重驻留、峰值live tensor/allocator统计范围、输出编码格式以及质量门槛。同样步骤/分辨率并不保证两个模型同质量；正文只用上述需求解释Infra压力，避免以架构/参数量排优劣。

## 后续内部阶段审计进展（尚未进入计算模块）

进一步核读固定transformers `0720e206c6ba28887e4d60ef60a6a089f6c1cc76` 的Qwen3/Qwen2.5-VL和同diffusers版本VAE依赖：

- 两个pipeline调用完整ForCausalLM/ForConditionalGeneration；即使只消费hidden，所读源码仍运行全词表lm_head。FLUX选取hidden9/18/27不使最后9层停止，36层仍执行；Qwen同理完整28层并返回logits。要省掉这些工作需明确替换模型调用路径，不能把优化后的假想工作当原pipeline事实。
- Qwen编码输入包含模板前34位置，随后才裁掉，因此无padding的同长batch情景下DiT T对应encoder T+34。FLUX默认固定padding到512，没有同样的34位置截取；三层hidden拼接不增加文本序列长度。
- FLUX调用明确use_cache=False，Qwen未传该项而config开启use_cache。Qwen临时K/V在text阶段返回对象里，不能当跨denoise步骤的DiT KV；该cache可以在编码返回后释放。
- `output_hidden_states=True`保存每层输出，最终`lm_head`同时产出全词表logits；文本阶段live必要集合应包含这些返回张量，不仅最后用于DiT的embedding。浮点执行dtype需外部给定，config里float32/dtype字段不证明runtime实际权重dtype。
- Qwen VAE `_decode`清cache后逐帧调用。静态首帧的两个upsample3d位置只设置`Rep`哨兵，跳过time_conv和时间翻倍，仍做2D空间上采样。普通causal Conv3d使用3×3×3核和前置两帧零padding；密集核乘加与非零padding有效乘加必须分开。首帧临时feature-cache clone持续保存到整个decoder结束清理，容量不能忽略。
- FLUX VAE普通2D Decoder为post_quant、conv_in、两resnet加单头mid attention、四级各3resnet及前三次nearest+conv、norm/SiLU/conv_out。它和Qwen的空间upsample通道规则不同：FLUX保持该级通道，Qwenupsample卷积将out_dim减半，下一块再按目标宽度投影。

## 内部阶段现已实施（2026-09-09后续更新）

前述“尚未进入计算模块”是冻结期间的审计状态；解除冻结后已实现`image_stages.py`并接入原`image_generation.py`。原字段兼容，新text/VAE工作值不再为null，完整非矩阵FLOPs、实测时间和系统峰值仍未知。6项image测试（旧3+新增3）通过。

- `image_text_encoder_steps/matrices`：每个正负条件各自Tencoder、全部层、全词表head、有效因果与dense-square attention两种口径、全部返回hidden/logits/临时KV必要集合。默认Qwen Tencoder546、每分支7.780694777856TF，2分支15.561389555712TF；FLUX T512、36层4.196266934272TF。text阶段不乘50/4去噪步骤。
- `image_vae_convolutions`：Qwen39项卷积/投影逻辑行、FLUX40项，每行输入/输出、核、权重/偏置、dense kernel与nonpadding乘加、边界张量和feature-cache clone。默认Qwen dense kernel+attention11.682587869184TF，nonpadding4.694839773440TF；FLUX10.474653483008TF和10.442021800960TF。空间mid attention为单头16384位置，无因果三角裁剪；静态time-upsample卷积执行数为0。VAE仅最终一次，latent-only路径为0。
- `image_stage_nonmatrix`：text RMSNorm/RoPE/SiLU/SwiGLU乘法/residual、有效Softmax exp/比较/归约；VAE L2/GroupNorm、SiLU/bias/residual、Softmax与nearest输出元素。不同单位分列，没有把exp或向量个数当FLOPs相加；DiT完整非矩阵、Norm全部底层算术和转换/图片编码尚需后续量化。
- `image_stage_lifetimes`：prompt embeddings跨去噪保留，cond预测跨negative forward保留；text全部hidden/logits/临时KV只存活于特征抽取；Qwen首帧30份causal feature-cache clone在decoder内累计到2,416,443,392 B然后clear_cache。这个缓存必要容量与最大的单卷积输入/输出量均非完整allocator/live peak；没有将其冒充实测显存。

新增测试以独立闭式核全LM层/head，逐空间/时间tap枚举核VAE边界zero padding与dense乘加差，核30份clone、步数变化不重做text/VAE、关闭CFG不改变VAE、FLUX隐藏层选择不截断执行。主代理负责统一CLI/报告/场景/outline及全量复算。

## 参考非矩阵、边界事件与服务下界（后续迭代）

新增`image_execution.py`并沿原入口返回`image_reference_operations`、`image_boundary_memory_events`与`image_matrix_service_bound`。图像9项专项测试通过。普通算术、比较和exp/sqrt/rsqrt/tanh分列；声明算法为中心方差LayerNorm、平方均值RMS、L2 normalize、稳定Softmax（含score scale）、sigmoid×x的SiLU、tanh近似GELU。参考FP32归约不是所有torch kernel真实dtype声明。

DiT已追加每层Norm、QK Norm、RoPE apply、Softmax、调制broadcast与gate/residual、GELU/SwiGLU、时间/条件SiLU、Qwen线性bias和FP16 clip；text/VAE既有逐元素库存转成相同参考算法单位。CFG含两次逐向量norm与组合，Euler按FP32 sample更新、回转tensor dtype；固定scheduler原件已进入独立锁。仍缺frequency/position/timestep特征构造、转换、随机数/setup、完整codec以及后端额外归约，`complete_nonmatrix_coverage=false`，不声称请求所有指令已闭合。

事件图在明确的无alias边界调度下依次分配/释放text返回、条件embedding、latent、cond/neg prediction、参考FP32 scheduler输入/输出与回转buffer、Qwen feature-cache、RGB输出。它包含871个默认Qwen事件、47个默认FLUX事件；默认边界图峰值分别2,429,550,592B与260,440,064B。权重、block/conv内部、完整CFG norm scratch、VAE workspace、allocator及postprocess未在图内；这是声明子图峰值，不能拿来判断设备能容纳整条管线，完整runtime peak仍unknown。

可选`effective_matrix_service`要求输入dtype匹配、FP32 accumulator、dense状态和精确正有效FLOPs/s。下界按text→每个DiT分支/step→VAE的串行矩阵路径，采用有效因果/nonpadding直接算法工作；不提供有效供给时保持unknown。特殊函数、访存、IO、排队和非矩阵供给仍缺，因此下界/对应matrix-only throughput上界不能用作可达性能或SLO结论。测试覆盖精度/稀疏不匹配拒绝、阶段重复次数不误乘、逐生命周期区间重建峰值与CFG跨负分支存活。

### 2026-09-09 固定源码 setup 工作补账

实现 `image_setup.py`，保留旧结果字段并新增 `image_setup_operations`、`image_setup_data_operations`、`image_setup_remaining`。每次 transformer 调用的 256 维 timestep 特征，按 128 个指数频率、B×128 外积与显式 scale、sin/cos 及两次拼接计；log/exp/sin/cos/pow/polar 单列特殊调用，不换算为任意 FLOP 常数。文本编码器 RoPE 只在对应文本分支执行一次，Qwen 为 3×B×T×64 角度，FLUX/Qwen3 为 B×T×64；不乘去噪步数。

Qwen 配置默认 `use_layer3d_rope=False`，必须读 `QwenEmbedRope` 而非下方相似类。构造正负 4096-position complex64 表只列 model_initialization，4 MiB 持久表不混入请求运算或声称已进入原边界峰值。`_compute_video_freqs` 按 image shape/device 缓存；`forward` 没有缓存装饰器，文本长度不改变 image key，外层 image cat 每次调用照常执行。新增 `qwen_shape_cache_warm` 显式控制本次请求开始前图像形状缓存是否已预热，默认冷。FLUX 每调用重建 image/text 的四轴频率；源程序取 batch 第一份 IDs，因此 DiT frequency 不乘 B，text encoder RoPE 仍乘 B。标准非 NPU/MPS 路径频率 FP64，repeat 后 cos/sin 转 FP32；后端分支不套用此口径。

Scheduler 限固定 deterministic FlowMatch Euler 动态 exponential shift 配置，mu 分段、sigma endpoint、time-shift、Qwen terminal stretch、timestep scale 一次 setup。NumPy linspace 内部算法计数未知保留 null；追加 terminal zero 为数据操作，不增加 denoise 次数。arange/索引整数操作、Cartesian product、stack/concat/repeat、normal 样本、显式类型转换分列非 FLOPs；same-dtype 请求为零转换，不从逻辑读写推断设备流量。已有生命周期图未加入全部 setup 临时量、构造表与 backend workspace，因此仍仅为声明边界图，complete_nonmatrix_coverage=false，全请求 FLOPs/时间继续 null。

验证：`python3 -m unittest discover -s calculations/tests -p 'test_image*.py' -q`，12 项通过。新增测试独立核对 CFG 不同 T 共享 image-cache、构造不混入请求、warm 仍执行外层 cat、DiT/text batch 差异、FP64→FP32语义字节、scheduler 一次 setup 及 same-dtype 零转换。未新增远程来源，使用原 image-generation.lock.json 已锁 diffusers/transformers 原件。

### 2026-09-09 timestep setup 临时生命周期补图

新增 `image_setup_lifetimes.py`，选择固定 `embeddings.py:get_timestep_embedding` 完整函数及上层 `timesteps_proj.to(...)` 输出转换，按明确 eager 求值组织展开：arange → 指数乘法 → 指数除法 → exp → 输入 FP32 转换（仅异 dtype）→ outer → scale → sin/cos/cat → flip cat → 模型 dtype 转换（仅异 dtype）。赋值 RHS 先分配，旧 binding 后释放；命名 exponent 留到 helper 返回，timesteps_proj 留到 learned projector 消费后。同 dtype cast 不伪造缓冲，view 不增加独立存储。单次 helper 临时量声明峰值为 `512 + 2560×batch` 字节，来自 exponent 与旧 scaled、sin、cos 和 concat 输出的共同存活；它不是算子融合或实际 allocator 的预测。

新增结果 `image_setup_boundary_memory_events` 与 `image_setup_boundary_memory_summary`，旧边界图原样保留以便比较。新图逐个重放旧事件并在每个 prediction 之前插入该 branch 的 timestep 生命周期；negative 分支期间已有 conditional prediction 留在图内。原 latent、prediction、scheduler 和 VAE cache 不重复分配。`peak_increment_bytes` 使用完整事件图峰值相减，而非把 helper 峰值直接叠到各阶段峰值。新增构造微型图的独立测试证明差别，另验证旧事件投影完全相等、same-dtype alias、CFG overlap 和全部 setup 临时量释放。15 项 image 定向测试通过。

此扩展只增加被选定函数的临时存储：caller 所有 timestep 输入及 scheduler 数组、RoPE 的构造与持久表、learned timestep projector 激活、其余 block 内部仍不在图内；`actual_allocator_peak_bytes=null`。没有把更多生命周期留空误写为完整请求内存或硬件可装入结论。
