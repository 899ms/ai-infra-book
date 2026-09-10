<!-- 从 rl-answers-lead.html 迁移的资料快照；原始 HTML SHA-256: 8ba3568d130851318c4cc74501779c3c03e6cd1bb2ce37428754d98bd5a91c7e。 -->

## 核心判断

vivek 的答案有一个共同风格：**先讲机制、再讲工业默认值、最后讲取舍**。读完整份 32 答，可以提炼出三条贯穿全篇的判断：

### 1. 算法选择不再是问题，工程一致性才是

作者明说"at lab scale the choice barely matters but there are differences"——GRPO/DAPO/GSPO/CISPO 之间的差异在工业规模上被系统层抹平大半，真正决定训练能否跑通的是 token-faithful 的 rollout、logprob 一致性、weight sync 节奏，而不是 paper 里第 17 行的一个 trick。

### 2. KL 的去留是 reference anchor 与探索的折中

GRPO/DAPO 一类方法去掉 KL，并不是因为 KL 没价值，而是因为 RLVR 阶段"想走得更远"。一旦回到偏好/安全/长尾任务，KL 仍是 reference anchor；硬编码成"GRPO 不带 KL"是错误归纳。

### 3. 异步 RL 的瓶颈被锁死在三个具体细节

staleness、trainer-inference mismatch、token-in token-out 是异步 RL 三大损耗点。Prime-RL/verl/TRL 框架的差异主要体现在如何分别处理这三件事，而不是算法本身。

## 32 问与答速查：逐题入口

下面按原帖编号给出逐题入口：**算法部分有 19 个题位，其中 Algo 9 / 16 / 19 是作者明确未展开的保留项，所以实质算法答复为 16 条；Infra 部分保留 16 个题位，其中个别题也标注了作者的不确定边界。**为便于站内阅读，下面是对原答的中文转述与关键短语保留，不是逐字翻译。

**阅读方式**

先看这一节拿到"题目问什么、vivek 答什么"；再看后面的故障地图和主题分析。这样读，既能快速查原帖答复，也能理解这些短答背后的工程判断。

### Algo：19 个题位，16 条实质答复

Algo 1

### 为什么用 Actor-Critic，而不是纯 value-based 或纯 policy gradient？

**vivek 答：**纯 value-based 方法不适合大动作空间或连续动作空间，而且通常只给 greedy policy；纯 policy gradient 能处理这类动作空间，但更新方差高。Actor-Critic 保留直接 policy，用 critic 降方差，是两者折中。

读法：在 LLM RL 里，这句话也解释了为什么后来 GRPO 要想办法去掉昂贵 critic，同时仍保留 baseline 的降方差作用。

Algo 2

### KL、cross entropy、MLE 的关系是什么？

**vivek 答：**CE(p,q)=KL(p,q)+H(p)。当数据分布固定时，最小化 CE、KL 或做 MLE 会落到同一个最优点；MLE 可以看成数据分布和模型分布之间的 KL 最小化。

读法：这里的前提是数据分布固定；on-policy RL 中样本分布会随 policy 改变，所以不能把 RL 简化成普通 SFT loss。

Algo 3

### 不同环境下 reward 应该如何设计？

**vivek 答：**主要取决于 environment。数学、代码这类 verifiable 任务比写作等 non-verifiable 任务容易给 reward。关键是环境不能容易被 reward hacking，不能给模型一条"优化错误目标"的捷径；数据和 reward 都要写得很谨慎。

读法：reward 不是一个打分函数那么简单，而是训练环境接口；环境设计优先级高于算法名字。

Algo 4

### importance sampling、rejection sampling 与 Monte Carlo 在 RL 中怎么用？

**vivek 答：**importance sampling 在 async RL 中用来复用旧 policy 生成的 off-policy 样本；rejection sampling 更多用于数据过滤，比如过滤 SFT 数据、丢掉太容易或太难的样本。广义上这些都是 Monte Carlo：用采样估计期望，而不是精确计算期望。

读法：这题把异步训练、off-policy 修正和数据过滤放在同一条"采样估计"主线上。

Algo 5

### PPO 与 GRPO 的 critic / reward model / advantage 有什么差异？std normalization 是否必要？

**vivek 答：**PPO 有 critic 和 reward model；GRPO 两者都去掉。GRPO 的"critic"来自同一 prompt 多次 rollout 后取组内均值作为 baseline。baseline 降低方差，使得不是每条 rollout 都得到正向推动，组内有点 zero-sum。std normalization 不一定必要，可参考 Dr.GRPO。

读法：严格说 GRPO 去掉的是 learned value critic；RLVR 中 reward model 往往被 verifier / rule reward 替代，不是说训练没有 reward。

Algo 6

### RL training 与 test-time scaling 的区别是什么？

**vivek 答：**RL 是把 domain intelligence 嵌进权重；test-time scaling 是在已有智能基础上，用更多 thinking tokens 探索不同路径、寻找更优解。前者改变模型权重，后者花更多推理预算。

读法：这句话是整帖最好的压缩表达之一：RL 改 policy，TTS 改推理预算。

Algo 7

### PPO 为什么 clip？为什么取 min？CISPO 有什么不同？

**vivek 答：**clip 是因为不希望 policy 突然大转向，ratio 在样本间方差会变高；min 来自 TRPO 的 trust-region 思路，让更新保持 pessimistic，只在有利时移动。CISPO 不同：它 clip importance weight，而不是 clip 整个 objective，所以所有 token 仍有梯度流，能保留更多信号。

读法：PPO clip 是安全阀；CISPO 试图避免安全阀把高价值 token 信号也一起关掉。

Algo 8

### 为什么 GRPO/RLVR 里有时加 KL，有时又去 KL？

**vivek 答：**KL 存在是因为 base model 已经很好，有不想丢掉的 intelligence，不希望 RL 让模型离它太远；但同一个约束也会阻止模型走得足够远去学新 domain。因此在 RLVR 中移除 KL 有时能提升稳定性和训练效果。

读法：KL 同时是 reference anchor 和探索阻尼器；不能机械背"GRPO 不带 KL"。

Algo 9 · 原帖保留项

### 分布式训练里某个 all-reduce / loss reduction 问题

**vivek 答：**作者说不确定自己是否理解这个问题，没有展开回答。

读法：这题不计入"32 条实质答复"。题面笔记中对应的是分布式 loss / all-reduce 语义。

Algo 10

### DPO 的 reward 是什么？还会 reward hacking 吗？

**vivek 答：**DPO 的 implicit reward 已经 baked into dataset：样本被标成 good vs bad，因此不像 PPO 那样需要单独 reward model。但 reward hacking 仍会发生，因为通向目标的 backdoor 仍可能存在。这是没有单一解法的 active problem，需要强力 stress-test environment；可以通过 sudden reward jumps 或 rollout length blowups 等信号发现。

读法：DPO 不训练显式 reward model，不等于没有 reward，也不等于没有 hacking。

Algo 11

### trainer-inference mismatch / MoE 训推不一致来自哪里？怎么修？

**vivek 答：**mismatch 来自不同 engine、不同 expert selection、不同 kernels、quantization、rounding。一个修复方向是 replay expert selection，让 inference 和 trainer 选同样的 experts。总体目标是让 rollout policy 和 trained policy 数值上相同，否则 importance weights 就错了。

读法：这题是全帖核心之一；PPO/GRPO 的 ratio 一旦被数值不一致污染，算法再漂亮也没用。

Algo 12

### group size、LR、PPO epochs、generation length 怎么设？

**vivek 答：**group size 本质是更多 rollouts、更多可学习路径，通常 8 或 16；learning rate 在 1e-6 量级较可控；PPO epochs 通常是 1，更多 epochs 会让数据更 off-policy 并导致不稳定；generation length 完全 task-dependent，不知道任务很难量化。

读法：这些不是神秘超参，而是方差、off-policy 程度、rollout 成本和任务长度之间的平衡。

Algo 13

### Dr.GRPO / DAPO / GSPO / CISPO / MaxRL 等如何改 GRPO？

**vivek 答：**这些算法基本都是 GRPO 变体，多数为更好稳定性；lab scale 下选择差异不大，但细节有区别：Dr.GRPO 去 std；DAPO 有 clip-higher、dynamic sampling、token-level loss、overlong filtering；GSPO 用 sequence-level importance sampling 而非 token-level，对 MoE 更好；CISPO clip weight 而不是 objective；MaxRL 解决 diversity collapse。SAPO/DPPO 作者没读，未展开。

读法：作者的关键态度是"算法名差异小于系统和稳定性细节"。

Algo 14

### TRPO、PPO、AReaL 如何处理 trust region / off-policyness？

**vivek 答：**TRPO 是 constrained optimization，保持在 KL boundary 内；PPO 用 clip 近似做同一件事；AReaL 在 async setting 下通过 bounding staleness / off-policyness，而不是 hard KL，来执行类似约束。

读法：trust region 的形式会随系统形态改变；异步 RL 中 policy lag 本身就是约束对象。

Algo 15

### RL 能否 fundamentally expand LLM capability frontier？

**vivek 答：**论文倾向表明，RL 更多是在 sharpen base model 已经有的能力，而不是形成全新能力。但这个方向值得继续推；如果有足够 exploration 和 diversity，作者也不完全确定它不能创造更大扩展。

读法：这是谨慎工业判断：RL 更像 sharpener，但探索多样性可能改变边界。

Algo 16 · 原帖保留项

### ProRL / scale RL 相关论文问题

**vivek 答：**作者说自己没有读这篇论文，因此没有展开。

读法：不计入实质算法答复；后文只把它作为能力边界讨论的保留项。

Algo 17

### OPD 相比 RL / SFT 的关键改进是什么？

**vivek 答：**OPD 结合 RL 的 on-policy exploration 与 SFT 的 dense signal。RL 的主要弱点是 reward 稀疏，OPD 用 teacher 给 student 自己的 on-policy rollouts 打分来修复这一点；关键是 student 自己的 on-policy rollouts。它可用于低成本能力迁移，最近很流行。

读法：OPD 的核心不是"teacher"，而是 teacher 评 student 的状态分布，从而减轻 SFT 的 exposure bias。

Algo 18

### LLM reasoning 能力从哪里 emerge？

**vivek 答：**作者不完全确定 reasoning 从哪里 emerge，但 CoT 作用很大；pre-training 提供 baseline intelligence，post-training 则通过 reasoning 和 test-time compute 放大这种 intelligence。

读法：推理不是单阶段产物，而是 pretraining、CoT 格式、post-training 和推理预算共同作用。

Algo 19 · 原帖保留项

### DeepSeek V4 / 后续系统 RL 细节

**vivek 答：**作者说自己不记得 V4 相关内容，因此没有回答。

读法：不计入实质算法答复；不能把后续推测写成作者观点。

### Infra：16 个题位

Infra 1

### GRPO 训练显存里有哪些模型副本？如何省显存？

**vivek 答：**取决于算法和是否用 KL。带 KL 的 GRPO 需要 training policy、用于 KL 的 reference policy、inference model。省显存可以先去掉 KL，从而去掉额外 reference model；也可用 nvfp4 quantization、FSDP/EP/TP 等分布式切分，把模型和 optimizer states 分到多卡；inference copy 可量化，optimizer states 可 shard。

读法：算法选择直接改变模型副本数量；显存预算不是后置工程问题。

Infra 2

### KV cache transfer 在分布式 prefill/decode 中怎么优化？

**vivek 答：**KV cache transfer 对 disaggregated prefill/decode 很重要，可通过 NVLink 或 layer-wise overlapped transfer of KV/weights 优化。多 GPU 情况取决于同节点还是跨节点；一般 TP 帮助很大，并且应把重 KV 移动尽量留在节点内。

读法：长上下文 rollout 的吞吐不是只看算力，还看 KV cache locality 和通信拓扑。

Infra 3

### FP8 与 INT8：训练和推理分别怎么用？

**vivek 答：**FP8 有更多 exponent bits，更适合训练；INT8 在固定范围内 precision 更好，更适合 inference weights。因此训练用 FP8，推理 serving 用 INT8。

读法：量化选择还会影响 trainer-inference logprob 一致性，尤其是 RL 的 importance ratio。

Infra 4

### 长尾 rollout 如何处理？

**vivek 答：**batch 内 long-tail rollouts 可以用 PipelineRL、continuous batching、early truncation 等方法处理；这类问题大多出现在 async setups。

读法：长尾不是小优化，它决定同步 RL 里 trainer 等最慢 rollout 的时间。

Infra 5

### continuous batching 是什么？vLLM 和 SGLang 的区别是什么？

**vivek 答：**continuous batching 会混合处在不同 next-token prediction 阶段的 rollouts。vLLM 使用 paged-attention；SGLang 使用 radixattention / prefix sharing。RL 中的额外问题，是当 sequences 在不同时间结束时，要对齐完整 trajectories 和 logprobs。

读法：serving 优化会改变轨迹对齐和 logprob 管理，不只是吞吐。

Infra 6

### vLLM / SGLang 这类 rollout engine 该看哪些指标？

**vivek 答：**用 throughput（tok/s）、KV cache utilization、GPU utilization 衡量。KV cache 看 occupancy，也要观察是否 memory-bound、rollouts 是否被 kicked out。低 GPU util 通常说明在等 rollout sync 或 CPU，而不是 compute-bound。两个 engine 都暴露 scheduler/cache metrics。

读法：GPU util 高不等于训练有效；还要看样本是否有学习信号。

Infra 7

### RL 训练反向传播与并行策略怎么做？

**vivek 答：**基本和普通 backprop 类似，但有一些调整：FSDP、EP、TP 是核心；long context 用 CP（context parallel）。理想情况下没人用 PP，因为它复杂，而且在多数 scale 下不是很必要。

读法：这是很强的工程立场：后训练栈更偏 FSDP/EP/TP/CP，尽量少用 pipeline parallel。

Infra 8

### async RL 框架的瓶颈是什么？Prime-RL / verl / TRL 怎么看？

**vivek 答：**async RL 框架包括 Prime-RL、verl、TRL。瓶颈归为三件事：rollout staleness 及其管理（importance sampling + staleness bounds）、trainer-inference mismatch、token-in token-out。mismatch 通过让 rollout engine 和 trainer 数值一致、replay expert/router decisions、在 trainer 侧计算 logprobs 而不是信任 inference engine 来修。

读法：这是全文最重要的 infra 答案之一，直接给出异步 RL 三大故障源。

Infra 9

### AReaL / partial rollout 是否保留旧 KV cache？

**vivek 答：**作者不确定 AReaL 的具体做法；有些方法保留 old KV cache，有些不保留。他认为两种做法本身没有真正的性能差异。

读法：这是作者明确标注不确定的题。更重要的概念是：KV cache 绑定生成它的 policy version，复用会牵涉 on-policy 语义。

Infra 10

### MoE 的 Expert Parallelism 如何影响 throughput？

**vivek 答：**EP 对 MoE 很关键：一组 experts 被放在一个节点或一组 GPU 上，每个设备持有子集。它通过并行 expert FFN 提升吞吐，但增加 all-to-all communication，把 token 路由到正确 expert。实际收益取决于 all-to-all 与 compute 的 overlap，以及 expert load 是否平衡。

读法：MoE RL 的瓶颈不是 active params 一个数字，而是 routing、通信重叠和负载均衡。

Infra 11

### FSDP 与 Megatron 并行方式有什么差异？

**vivek 答：**通信与计算并行化是关键。FSDP shard grads/params/optim，并按需 gather，简单很多。Megatron 使用 DP、PP、TP 的 3D parallelism，通信更显式；作者说自己没太用过 Megatron，因此不完全确定。

读法：这里的重点不是谁绝对更好，而是团队是否能承受 Megatron 的显式并行复杂度。

Infra 12

### 确定性 / batch invariance 需要什么条件？

**vivek 答：**需要 reduction order 一致、kernels 相同、batch-invariant ops。更多细节参考 Thinking Machines 的相关博客。

读法：batch-invariant 不是形式主义；它直接关系到同一条 rollout 在不同 batch 形状下 logprob 是否一致。

Infra 13

### AReaL 与 Slime 如何处理 rollout bottleneck？

**vivek 答：**作者能谈 AReaL：它 fully async with staleness control，把 rollout generation 与 training 解耦，让 trainer 不再等待最慢 rollout；通过 max off-policy steps、importance sampling，或超过阈值后移除 samples 来控制 staleness。对 Slime 作者说需要再读更多。

读法：AReaL 的核心是用 staleness 边界替代同步等待；Slime 部分不要扩展成作者已确认观点。

Infra 14

### full async staleness 的实际量级是多少？

**vivek 答：**staleness 是生成 rollout 的 policy 与正在训练的 policy 之间的 gap。作者自己的实验通常落后 1–4 steps。更多 staleness 会导致 importance sampling 不稳定，因为 ratios 会 blow up。

读法：1–4 steps 是非常具体的工业默认区间，值得单独记住。

Infra 15 · 原帖保留项

### Slime 的 data flow / Megatron 结合 / loss 计算

**vivek 答：**作者再次表示自己对 Slime 不确定，没有展开。

读法：这题不应被过度解读；后文只按一般 async rollout/trainer 架构解释可能的数据流。

Infra 16

### VeRL / TRL / AReaL / Slime 等框架选哪个？

**vivek 答：**none of them, use @PrimeIntellect。

读法：这是强产品立场，不是中立 benchmark 结论；但也说明作者认为 Prime Intellect 在 reward / verifier / async RL 平台化上更贴近他的工作流。

## 一页总览：它不是答案集，而是一张故障地图

如果只把这条长帖当成 32 道题的参考答案，会错过它最有价值的部分。它真正给出的不是"标准答案"，而是一个工业 RL 训练者遇到故障时的排查优先级：先看 reward / environment 是否诱导错目标，再看 policy update 是否被 clip、KL、advantage normalization 扭曲，再看 rollout policy 与 trainer policy 是否在数值上真的是同一个模型，最后才谈哪个 GRPO 变体更优。

### 算法层的问题，最后常常是系统层的问题

reward 突然上涨、length 爆炸、clip fraction 异常、importance weight 尾部变厚，看起来像算法失败，实际可能是 verifier 漏洞、logprob 重算不一致、MoE router replay 缺失或 batch-invariant 不满足。

### 系统层的优化，最后会改变算法语义

continuous batching、KV cache reuse、FP8/INT8 量化、异步 rollout、stale sample rejection 都不是纯吞吐优化；它们会改变样本来自哪个 policy、logprob 是否可信、advantage 是否仍代表同一个目标。

因此这份帖子的最好读法是把每个回答都归到一个故障类别中：**reward 是否可靠、policy update 是否受控、rollout 是否 faithful、并行/量化是否破坏一致性、异步是否把 on-policy 训练拖成难以修正的 off-policy 训练**。这也是 2026 年 LLM RL 面试和真实项目之间的共同交集。

## 问题背景：为什么这份答卷值得单独解读

sheriyuo 整理的 35 题主帖是 2026 年 LLM RL 方向最被引用的一份"能力地图"，目前已知有至少两位 RL 从业者完整作答（@vivek_2332 与 @pradheepraop），多位读者用中英文分享了笔记。题面笔记的解读重点在"问题在测什么能力"，而本篇解读的重心是**这份答案本身透露的工业判断**。

三条理由让这份答案有独立价值：

- **作者有清晰的产品立场**：Infra 16 题中他直接给出"none of them, use @PrimeIntellect"，结合全文对 Prime-RL、verl、TRL、AReaL 的具体评价，可以判断这份答卷至少带有明确的 Prime Intellect / Prime-RL 实践偏好，是工业界公开技术判断的少见样本。
- **答案形式是"工程默认值"**：每题 2-4 句话，几乎不给公式推导，但给出 group size 8/16、LR 1e-6、PPO epochs=1、fp8 训/int8 推这一类可立刻套用的工程默认值——这正是教科书和论文中读不到的"作坊知识"。
- **对算法变体的态度是"半否定"**：明说"all the algo are variants on grpo, mostly for better stability. at lab scale the choice barely matters"。这种态度和论文作者在论文中宣称的方法价值形成显著反差，对评估 RLHF/RLVR 项目里的"算法迭代投入产出比"很有参考意义。

**本篇与既有笔记的边界**

题面笔记（rl-interview-questions-2026.html）按 35 题逐题给出"考点 + 完整机制 + 边界"。本篇则反其道：把同一份题的同一份答案按"主题"重排，附上"作者用这个答案表达什么判断"的解读，重复内容（题面、机制、术语）刻意压缩。

## 批判性校正：五处最容易被误读的地方

这份答卷价值很高，但它是 compressed notes，不是完整教材。读者如果照字面背诵，容易在五个地方产生偏差：

**GRPO 没有丢掉 reward**更准确地说，GRPO 通常丢掉 learned value critic；在 RLVR 中，learned reward model 被 verifier / rule-based reward 替代。把它说成"不需要 reward"会遮蔽最核心的 environment design 问题。

**CE/KL/MLE 等价有前提**CE(p,q)=KL(p,q)+H(p) 只在数据分布 p 固定时给出同一最优点。SFT 里 p 固定；on-policy RL 里 p 随 policy 诱导分布变化，这也是为什么 RL 不能被简单还原成加权 SFT。

**DPO 不是没有 reward**DPO 的 reward 是隐式的 policy-reference log ratio。它不需要单独 reward model，但 preference data 的长度、风格、refusal、模板痕迹仍会成为可被 hacking 的 backdoor。

**KV cache 不是普通缓存**KV cache 绑定了生成它的 policy version。跨权重更新复用旧 KV 严格说会改变 rollout 的身份；可以作为异步近似，但必须和 staleness、importance sampling、sample rejection 一起讨论。

**框架选择不能只看一句推荐**Prime-RL、verl、TRL、AReaL、slime 的差异取决于训练 backend、rollout engine、MoE 支持、agent environment、是否 fully async、团队是否能维护 Megatron/FSDP 栈。"use Prime" 是作者立场，不是通用结论。

**阅读原则**

这类高密度长帖应按"判断力样本"读，而不是按"标准答案"背。每个短答都应该追问三个问题：它假设了什么任务分布？它隐含了什么系统条件？换到不可验证任务、多模态任务或长时程 agent 环境后还成立吗？

## 方法学：从 32 答中反推一份"Prime Intellect 视角下的 RL 后训练栈"

把 32 答按作者隐含的关注点重新分类，可以得到一张 6 层技术栈地图：

\\\text{RL 后训练栈} = \underbrace{\text{Reward/Env}}\_{\text{算法语义}} \circ \underbrace{\text{Policy Update}}\_{\text{PPO/GRPO 变体}} \circ \underbrace{\text{Logprob Consistency}}\_{\text{train-infer match}} \circ \underbrace{\text{Rollout Engine}}\_{\text{vLLM/SGLang}} \circ \underbrace{\text{Parallelism}}\_{\text{FSDP/EP/TP/CP}} \circ \underbrace{\text{Async Orchestration}}\_{\text{Prime-RL/verl/TRL/AReaL}}\\

vivek 的 32 答可以被读成这 6 层栈的逐层表态：

| 层级 | 对应的 Q 编号 | vivek 的关键表态 | 反推出的工程判断 |
|----|----|----|----|
| Reward/Env | Algo 3, 10, 17 | "env shouldn't be prone to reward hacking"；OPD 用 teacher 评 on-policy rollouts | env 设计优先于算法选型；reward 是接口不是函数 |
| Policy Update | Algo 1, 5, 7, 8, 13, 14 | GRPO 主体、变体主要在"stability"；KL 在 RLVR 可去、在偏好/安全保留 | 把 70% 调试精力放在 trust region/clip/aggregation，而不是新算法 |
| Logprob Consistency | Algo 11, Infra 12, 13 | "replaying expert selection"；"batch invariant ops"；引用 Thinking Machines blog | MoE 和量化场景必须把 trainer/inference 做成数值一致 |
| Rollout Engine | Infra 2, 4, 5, 6 | vLLM=paged-attn，SGLang=radixattention；kv cache util 是核心监控 | RL 项目的吞吐主要看 rollout engine scheduler，调度策略比 batch 形式更重要 |
| Parallelism | Infra 1, 3, 7, 10, 11 | "ideally no one uses pp"；EP 的关键是 all-to-all 与 compute overlap | MoE 模型训练中 EP+TP 是默认；PP 只在不得已时启用 |
| Async Orchestration | Infra 8, 9, 13, 14, 15, 16 | staleness 1-4 步、importance sampling + staleness bounds、replay expert/router | 异步 RL 的本质是"控制三个差距"：policy lag、numerical drift、I/O 同步 |

## 算法判断的工程含义（Algo 1, 2, 3, 5, 6, 7, 8）

vivek 在第一组算法题的回答里，把"教科书叙述"压缩成了"工业默认值"。这些回答几乎不重复 RL 教材里已经写清楚的部分，而是直接给"为什么这样选、代价是什么"。

### Algo 1 — Actor-Critic 不是"算法选择"，是"显存与方差预算"的选择

vivek 的回答把 AC 拆成：*pure value-based* 在大/连续动作空间天然不适配（只给 greedy policy），*pure policy gradient* 高方差，*actor-critic* 用 critic 减方差。这里值得注意的是，他没有说 AC "更稳定"——这是教科书表述——而是说"best of both" 的工程含义：**critic 的角色从理论上的状态价值函数，转到了工程上的方差降低器**。这一观点直接呼应 GRPO：用 group baseline 替代 learned critic，节省一个与 actor 同量级的模型副本。

### Algo 2 — KL/CE/MLE 的等价只在数据分布固定时成立

vivek 用一句话写完："*ce(p,q) = kl(p,q) + entropy(p). minimizing any of them lands you in the same place. mle is just kl between data dist and model dist.*" 这是 LLM RL 文献里被反复复述的恒等式，但他的表达精确切中了一个微妙点：**等价性依赖 p 固定**。SFT 时 p 是数据分布，确实不变；RL 时 p 是策略诱导分布，会随更新漂移——这就是为什么"在 RL 里最小化 CE"和"在 SFT 里最小化 CE"行为完全不同。

**推论**

任何把 RL 表述成"对 SFT loss 加权"的工作，本质上都要回答"这个加权是否修改了诱导分布 p"。这能立刻区分出 SFT→DPO→IPO→SimPO 一条线和 SFT→RLHF→GRPO 一条线的根本差异。

### Algo 3 — Reward 设计的核心是"防 reward hacking"，不是"打分"

vivek 把 reward 拆成 verifiable（math/code）与 non-verifiable（writing）。这一拆法在 2025-2026 年间已成为 RLHF→RLVR 转向的共识标志。但他的核心句是"env shouldn't be prone to reward hacking, there shouldn't be an easy path to optimizing the wrong solution"——这是**把 reward 视为环境属性而非函数属性**。Algo 10 里他又引用 @willccbb 强调 DPO 也有 backdoor：reward hacking 是 closed-form 偏好目标和可执行 verifier 共同的失败模式，缓解办法是 stress-test env 和监控 reward/rollout 长度突变。

### Algo 5 — GRPO 的"baseline = group mean"，std normalization 可选

vivek 的描述：PPO 用 critic + reward model，GRPO 丢掉两者，用多次 rollout 的均值做 baseline。"std normalization isn't necessary, see dr.grpo"——这是 Dr.GRPO 的核心修正（去掉 std 项能减少长度偏置）。这种"半可选"的表述比论文里的"必须"更接近工业事实：**normalization 不是中性操作，它会改变哪些 prompt 主导梯度**。

\\ \hat{A}\_i^{\text{GRPO}} = r_i - \mu_G \quad\text{（baseline 部分）};\qquad \hat{A}\_i^{\text{with std}} = \frac{r_i - \mu_G}{\sigma_G} \\

### Algo 6 — RL = 嵌入领域智能到权重；TTS = 在预算内找最佳路径

这是 32 答里最精炼的隐喻之一："*rl is about embedding domain intelligence into the weights. test-time scaling is, given that intelligence, finding the best path to a solution and exploring different ones with more thinking tokens. one shapes the model weights while the other spends more on inference budget.*" 这种把 RL 和 test-time scaling 分到"权重 vs 推理预算"两个轴上的视角，与最近 RL-as-search 的论文（MaxRL、ProRL）形成清晰对应：**RL 的边际收益取决于"能 search 到多远的答案"**。

### Algo 7 — clip + min 来自 TRPO 的 trust region；CISPO 改变了梯度被 mask 的方式

vivek 的对比：

- **PPO 的 clip**：裁剪的是 ratio，目的是不让策略剧烈转向、让 ratio 方差过大；`min` 来自 TRPO 的 trust region，让更新"乐观但悲观"——只在有利时才移动。
- **CISPO**：不裁剪整个 objective，而是裁剪 importance weight 本身。差别是所有 token 仍保留梯度流，信号利用率更高。

这一对照是回答"为什么不 clip 会怎样"的工业版答案：clip 不是美学，是 PPO 在多 epoch reuse rollout 时防止 importance weight 爆炸的安全阀。

### Algo 8 — KL 是 reference anchor，去 KL 是为了"走得更远"

vivek 的解释非常精炼："*kl is there because you already have a good base model with intelligence you don't want to move too far from. but you also want to learn new domains via rl. it gets dropped because that same constraint stops you from moving far enough to actually learn, which you don't want. so removing kl helps stability and training in rlvr.*"

这一表述把 KL 拆成了"防止走远"和"帮助到达"两个对立功能：**KL 同时是稳定器和阻尼器**。在 RLVR 里，verifier 提供了更强的稳定信号（正确答案 hard-coded），KL 就可以被弱化；在 RLHF 里，reward model 是软的、不在分布外的，KL 必须保留以防 reward hacking。

## GRPO 家族、trust region 与实现细节（Algo 7, 8, 13, 14）

Algo 13 的回答是整份 32 答中最具"工业地图"价值的一段——把近年所有 GRPO 变体放在同一张表上做横向比较。

| 方法 | 核心修改 | vivek 的定位 | 对应失效模式 |
|----|----|----|----|
| Dr.GRPO | 去 std normalization，修正 loss aggregation | 处理长度偏置与低方差 group 被过度放大 | 长 CoT 数据上 pass@1 与长度强相关时 |
| DAPO | clip-higher、dynamic sampling、token-level loss、overlong filtering | 提高有效梯度比例，给低概率正确 token 上升空间 | 标准 GRPO 在难 prompt group 上 0 梯度 |
| GSPO | sequence-level IS（不是 token-level） | "much better for moe"——MoE 长尾 token-level ratio 噪声被抹平 | MoE 训练中 token-level IS 极端波动 |
| CISPO | 裁 importance weight，不 mask 整个 token | 保留所有 token 的梯度流 | PPO clip 把高信息 token 完全冻结 |
| MaxRL | 从 pass@k / MLE 视角重构目标 | 解决 diversity collapse | RLVR 后 pass@k 退化（GRPO 的常见副作用） |
| AReaL | 异步 RL 中用 staleness bound 替代硬 KL | 把 trust region 换成"policy lag 边界" | 异步训练中 KL 不再反映真实 off-policy 程度 |

这张表背后有一个被多次重复的判断：**所有这些变体的差异在"工业规模"上被系统层抹平大半**。这并不是说变体没用，而是说"在跑得起来的工业 RL 系统上，clip/aggregation/sampling 这些细节的影响 ≥ 算法差异"。这也是 vivek 反复回到"在 lab scale the choice barely matters"的本意。

Algo 14 中，他把 TRPO/PPO/DPPO/AReaL 串成一条线：**trust region 始终是 off-policy 偏差的边界，形式可以是 KL（TRPO）、clip（PPO）、policy divergence（DPPO）或 staleness（AReaL 异步）**。这条线对设计自己的异步 RL 训练栈的人最有用：选哪种 trust region 形式取决于你能控制的是 rollout 时序还是 KL 计算。

## 能力边界与训练阶段（Algo 15, 16, 18）

这一组答案代表 vivek 对"RL 能不能扩展 LLM 能力 frontier"这一根本问题的判断，与实验室论文的乐观叙事形成清晰反差。

### Algo 15 — RL "主要"是放大已有能力，不是创造新能力

原句：*"the papers suggest rl mostly sharpens abilities already in the base model rather than forming new ones. cool direction to push on though, with enough exploration and diversity i'm not fully sure it can't."*

这种"sharpen rather than form"的态度在 2026 年 RL 论文中（ProRL、MaxRL、RL-VLM-FT）开始被显式承认，但工业 RL 训练者通常私下共识。重要的是 vivek 留了半句口子："**with enough exploration and diversity**"——能力扩展的可能性不在 RL 算法本身，而在 sampling diversity 和 verifier coverage。这是后续工作（如 RL with intrinsic motivation、self-generated tasks）真正能突破的方向。

### Algo 18 — 推理能力是"基座 + 格式 + 探索 + verifier + 稳定训练"五层共同 emergence

vivek 拒绝单因果叙事："*cot plays a big part. also pre-training for baseline intelligence and post-training for amplifying the intelligence using reasoning and test-time compute.*" 这与近期一系列"a-ha moment"研究的解释一致：推理能力不是 RL 凭空创造的，是 pretraining 提供 baseline 智能 + CoT 格式 + RL/RLVR 放大 + TTS 利用的复合产物。

### Algo 16 — ProRL 类工作的 scale 边界

vivek 承认"haven't read the paper"——这是一个诚实的边界声明。但他在 Algo 15、16、18 上的态度形成一致：**RL scale 的瓶颈不在 GPU 数，而在 prompt 难度分布、rollout 数、verifier 质量、训练稳定性和吞吐**。扩 batch 不是 scale，扩有效 token 用量（成功 rollout / 总 rollout）和 verifier coverage 才是。

## DPO、OPD 与 on-policy distillation（Algo 10, 17）

### Algo 10 — DPO 的隐式 reward 与 reward hacking

vivek 给出 DPO 的标准刻画：偏好对 (chosen/rejected) 隐式提供 reward 信号，不再需要单独 reward model。但 reward hacking 仍然存在——"*there's a backdoor to the solution you're chasing*"，源自偏好数据本身的偏置（长度、style、refusal 等 confound）。监控手段是 reward 突然跳跃、rollout 长度爆炸等信号。

**边界**

vivek 引用了 @willccbb 的观点——这意味着 DPO 在 2026 年的工业实践中被视为"在线 RL 不可用时的退路"，而非首选。RLVR 时代偏好对齐正在让位给 verifiable reward 的直接优化。

### Algo 17 — OPD 的关键 trick 是"teacher 评 on-policy rollout"

vivek 把 OPD 拆成：*on-policy exploration from RL + dense signal from SFT*。关键句是 "*having a teacher score the student's own (on-policy) rollouts (important part)*"——on-policy 这一限定是 OPD 与普通 SFT-distill 的关键区别。SFT 在 teacher 数据分布上训练，OPD 在 student 自己的状态分布上由 teacher 评分，这才能解决 SFT 的 exposure bias。

应用边界：teacher 必须比 student 强，且 teacher 与 student 的"思维模式"不能完全不兼容；否则 OPD 会把 student 拉向一个不可达或不适合的分布。vivek 的描述与近期 self-distillation（Spielberg）、weak-to-strong (OpenAI super-alignment) 工作形成对照：

- OPD 的"teacher scores student rollouts"是 **weak-to-strong alignment** 在推理/Agentic 任务上的具体化；
- 与 RL 的"reward model scores student rollouts"在结构上同构，区别是 OPD 的"teacher"是另一个 LLM 而非标量 reward。

## 训练超参与 trainer-inference 一致性（Algo 11, 12）

### Algo 11 — trainer-inference mismatch 来自 5 个具体来源

vivek 给出清单："*different engine, different expert selection, different kernels, quantization, rounding*"，并引用 Thinking Machines blog。这一句把 MoE 训推不一致的所有常见根因压缩在一行里：

1.  推理引擎 vs 训练引擎不同（SGLang/vLLM vs Megatron/FSDP）
2.  MoE expert 选择不一致（router 决策受 batch shape 影响）
3.  kernel 行为差异（attention/MLP 的不同实现路径）
4.  量化方案不同（int4/int8/fp8/nvfp4 之间的精度漂移）
5.  rounding 顺序（reduction order、batch-invariant 缺失）

修复方向有两类：(a) replaying expert selection，让推理和训练选相同的 experts；(b) 让 rollout policy 和 trained policy 数值相同，否则 importance weight 错。这正是 Infra 12、13 中他再次展开的内容。

### Algo 12 — 训练超参的"工业默认值"

vivek 给出的数值是 2026 年 RL 后训练的"作坊共识"：

| 超参 | 默认值 | 为什么 |
|----|----|----|
| Group size | 8 / 16 | 更多 rollouts = 更稳定的 advantage 估计；超出后 GPU 利用率下降 |
| Learning rate | 1e-6 量级 | 大 LR 让 policy 快速偏离 old policy，ratio 爆炸 |
| PPO epochs | 1 | 多 epoch 让数据更 off-policy，clip 难以控制 |
| Generation length | task-dependent | 太短截断推理；太长拖慢 batch；与 length penalty 互相作用 |

注意他没有给 KL 系数或 clip range——因为这两个参数高度依赖具体任务，**工业上"先跑起来看 KL/clip fraction/response length 分布"再调**。

## Infra 视角：显存、量化、并行（Infra 1, 3, 7, 10, 11, 12）

### Infra 1 — 显存 = 几个模型副本 × 各自的并行度

核心判断："*for grpo with kl you need the training policy, reference policy for kl and the inference model.*" 这是 RL 显存预算的标准 3 副本结构（actor + ref + rollout）。vivek 的优化建议序列是：(1) 去掉 KL → 拿掉 ref model；(2) 引入 nvfp4 量化；(3) FSDP + EP + TP 分片 + ZeRO-style 优化器分片。

**推论**

任何宣称"我能用 X 张卡跑 Y 参数的 RL"的项目，都必须先回答这三个副本分别占多少显存、是否被量化、是否被卸载。Prime-RL/verl/TRL 框架的差异在第一行"哪个副本可以共享"上就分出了优化档位。

### Infra 3 — fp8 训 / int8 推

原句：*"fp8 has more exponent bits which is better for training. int8 has more precision in a fixed range, better for inference weights."* 这是一个非显然的硬件-算法对照：

- **fp8 (E4M3/E5M2)**：更多 exponent bits → 动态范围大，更适合梯度/激活的"中间值跨度大"的训练场景；
- **int8**：固定范围 + 等距精度 → 推理时权重分布相对稳定，更适合查表式 forward。

这一选择直接影响 trainer-inference 一致性（呼应 Algo 11）：训练用 fp8，rollout 用 int8，`logprob` 的数值会有系统性偏差，必须在 loss 端补偿。

### Infra 7、10、11 — 并行策略选择

vivek 的并行栈总结：

| 并行维度 | 职责 | vivek 的关键判断 |
|----|----|----|
| FSDP | 分片 grads/params/optim | 按需 gather，"much simpler" |
| TP | 切分 attention/MLP 头 | 多机时尽量保持在同一节点 |
| EP | 切分 MoE experts | "all-to-all 与 compute overlap 是关键" |
| CP | 长 context 切分 | long context 必备 |
| PP | layer 切分 | "ideally no one uses pp, it's complex and not really necessary at most scales" |

PP 不推荐这条尤其值得标注：**在多数 RL 训练规模下，TP+EP+FSDP+CP 已能覆盖 70B/200B/400B 模型的并行需求，PP 引入的 bubble 和 checkpoint 复杂度是负收益**。Megatron-LM 系（DP+PP+TP 3D 并行）虽然在预训练仍主流，但 RL 后训练栈更倾向 FSDP/EP 中心的"轻 PP"或"无 PP"方案。

### Infra 12 — 数值一致性的具体含义

vivek 给了 RL 数值一致性的 3 个必要条件：reduction order 相同 + 相同 kernel + batch-invariant ops。这正是 Thinking Machines "LLM Training Randomness" 系列博客的核心结论。当这些不满足时，`logprob` 在训练侧和推理侧会有系统性偏差，PPO/GRPO 的 importance ratio 被污染。

## Infra 视角：rollout 服务与吞吐（Infra 2, 4, 5, 6）

这一组回答把"rollout engine"作为 RL 项目中独立的基础设施层级展开。

### Infra 2 — KV cache transfer 在 disaggregated prefill/decode 中关键

vivek 的核心句：*"kv cache transfer matters for disaggregated prefill or decode. optimized via nvlink or layer-wise overlapped transfer of the kv/weights. multi-gpu depends on whether it's the same node or different node. generally tp helps a lot and you want to keep heavy kv movement within a node."*

这一段把 disaggregated inference 的工程权衡讲清楚：

- **同节点**：用 NVLink 直接传 KV cache，latency 低；
- **跨节点**：用 layer-wise 重叠 transfer，掩盖通信延迟；
- **TP**：在 KV cache 通信中起放大作用，TP 度越高 cache 越大。

### Infra 4 — 长尾 rollout 的处理

vivek 给出三个方法名：*pipelinerl, continuous batching, early truncation*。其中 pipelinerl（Sequential Pipeline RL）把整个 batch 拆成 pipeline，long-tail 不再阻塞同步；continuous batching 是 vLLM/SGLang 通用做法；early truncation 是最朴素的截断。注意这三个方法是**同步 RL**的修，正式解决长尾需要异步 RL（Infra 8、13）。

### Infra 5 — vLLM vs SGLang 的本质区别

vivek 的对照很干净：

- **vLLM = paged-attention**：把 KV cache 按 page 管理，减少碎片；
- **SGLang = radixattention**：用 radix tree 做 prefix sharing，长 prompt/共享前缀场景下命中率更高。

RL 项目的额外约束：*aligning complete trajectories and logprobs when sequences finish at different times*。这是 vLLM/SGLang 在 RL 中必须支持的特性（部分由 TRL/verl 的 trainer-side logprob 重算兜底）。

### Infra 6 — 监控指标三件套

throughput (tok/s) + kv cache util + gpu util。vivek 强调：

- **kv cache util 偏低** → memory bound，rollout 被踢出（kicked out）会拖慢 batch；
- **gpu util 偏低** → 你在等什么东西（rollout 同步、CPU、IO），不是 compute-bound。

这套监控清单是 RL 训练栈的"基本功"——任何一份 RL Infra 报告都该给出这三类指标的时间序列和 breakdown。

## Infra 视角：异步 RL 框架与 staleness（Infra 8, 9, 13, 14, 15, 16）

这一部分是 32 答里最贴近 Prime Intellect 自身产品的部分。异步 RL 是 Prime-RL/verl/TRL 的核心战场。

### Infra 8 — 异步 RL 的三大瓶颈

vivek 把所有异步 RL 框架的瓶颈归到三件事：

1.  **staleness of rollouts** → 用 importance sampling + staleness bounds 控制；
2.  **trainer-inference mismatch** → 让 rollout 引擎和 trainer 数值一致、replay expert/router decisions、logprob 在 trainer 侧重算；
3.  **token-in token-out** → 异步生成-训练间的 I/O 同步。

Prime-RL/verl/TRL/AReaL 的差异主要在如何分别处理这三件事。vivek 在 Infra 16 直接给出推荐：*"none of them, use @PrimeIntellect"*——这暗示 Prime Intellect 的产品定位是把这三件事统一处理的 RL platform。

### Infra 9 — 旧 KV cache 是否保留

vivek 不确定 AReaL 细节，但表态 "*there's no real perf difference between the two as such*"——即"保留旧 KV cache"与"重建"在异步 RL 中没有系统性性能差异。这与直觉相反：直觉上保留能省一次 prefill。但实际 I/O 模式下，token 流转和权重同步的代价已经吞掉了这个收益。

### Infra 13 — AReaL 的设计

vivek 给出 AReaL 的核心机制：*fully async with staleness control, decoupling rollout generation from training, the trainer never is waiting on the slowest rollout*。控制 staleness 的方法有三类：

- **max off-policy steps bound**：硬阈值；
- **importance sampling**：用 IS 修正 stale samples；
- **rejection**：超过阈值直接丢弃 samples。

vivek 对 Slime 的两次"not sure"也值得标注——Slime 在异步 RL 中是较新的方案，作者的有限了解暗示这份答卷写作时（2026-06）Slime 还没有广泛进入工业 RL 实践者的视野。

### Infra 14 — staleness 的实际量级

原句：*"the experiments i run are usually 1-4 steps behind. more staleness leads to instability in importance sampling since the ratios blow up."* 这是**工业 RL 训练的真实量级**——1-4 步 stale 是稳态，超过这个范围 importance ratio 的尾部会让 loss 失稳。这一数字对设计自己的异步 RL 系统的工程师是直接的工程参数。

### Infra 16 — Prime Intellect 推荐

vivek 明确给出推荐："*none of them, use @PrimeIntellect*"。结合他在 Infra 1、8、13 中的具体描述（Prime-RL + verifiers + 异步架构），可以判断 Prime Intellect 的产品定位是"统一 reward / verifier / 异步训练" 的 RL post-training 平台。在 2026 年 RL 工具市场（verl/OpenRLHF/trl/AReaL/slime/prime-rl）中，这是一条与传统"框架 + 论文"路径不同的产品路径。

## 术语解释（首次出现时）

本节只解释 @vivek_2332 的答案中首次出现、且不属于 sheriyuo 题面笔记已经覆盖的核心术语。

**Trust region**策略更新前后分布的"信任区间"，TRPO 用硬 KL 约束，PPO 用 clip 近似，AReaL 用 staleness 替代。

**Importance ratio (ρ)**\\\rho_t(\theta)=\dfrac{\pi\_\theta(a_t\|s_t)}{\pi\_{\theta\_{old}}(a_t\|s_t)}\\，PPO/GRPO 优化的核心量，**极易被 trainer-inference mismatch 污染**。

**Staleness**生成 rollout 时所用 policy 与当前 trainer policy 的版本差距。1-4 步是稳态区间。

**Batch-invariant ops**reduction order 固定的算子——同一输入无论 batch 形状如何，输出位级相同。RL 数值一致性的必要条件（见 Thinking Machines blog）。

**RadixAttention**SGLang 的核心数据结构：radix tree 上做 prefix sharing，长 prompt / 共享前缀场景下 KV cache 命中率显著高于 paged attention。

**On-policy distillation (OPD)**teacher 评 student 自己的（on-policy）rollouts 而非 teacher 数据分布上的 rollouts。解决 SFT 的 exposure bias，结构上同构于"用 reward model 评 student rollouts"的 RL。

**Reference policy**RLHF/RLVR 中用于 KL anchor 的"原模型"。去 KL 等于把 reference policy 从优化目标里拿掉。

**nvfp4**NVIDIA fp4 量化格式（E2M1 + 共享 exponent block）。相比 int4/fp8，在保证 loss 收敛的前提下进一步压低显存。Prime-RL 等框架的推荐优化点之一。

**Verifiers**规则 verifier / reward model 的统称。@willccbb（will brown）的 verifiers 库是 Prime Intellect 推荐的可执行验证栈。

## 边界与风险

**这份答案不能直接当教程**

vivek 自己说"correct me if anything's off, happy to hear feedback"——原帖里有多处直接声明"not sure / haven't read"（Algo 9、13 中的 SAPO/DPPO、Algo 16、Algo 19、Infra 9、Infra 11 中的 Megatron、Infra 13/15 中的 Slime）。这些边界标记得很诚实，但也意味着：把每条表态都当成普适工程真理会过拟合到 Prime Intellect 自己的工作流。

- **作者立场偏置**：原帖明确推荐 Prime Intellect，并对 verl/TRL/AReaL 有具体评价。这与"中立综述"性质不同——读者应意识到 RL 工具市场仍在快速演化，2026 H2 的格局可能显著不同。
- **工业规模 ≠ 论文规模**：多次出现"at lab scale the choice barely matters"。这句话在千万-亿级 token 训练上是有道理的，但对百亿-千亿级参数、特殊任务（长 CoT、多模态、Agentic）的 RL，算法差异可能仍显著。
- **未涉及的边界**：vivek 没有回答：(a) RLHF 与 RLVR 的可组合训练 pipeline（先 RLHF 偏好对齐、再 RLVR 推理强化）；(b) 多模态 RL 的 rollout 工程；(c) RL with tools 的 long-context KV cache 策略。这些方向在他的 32 题里只是边缘提及。
- **未读论文**：vivek 明说没读过 ProRL/v4/Slime 的论文，因此对"RL scale 边界"的态度是带保留的；Pradheepraop（另一位答题者）也独立做了完整答案，可作为交叉参考。
- **RL 训练者 vs RL 研究者的差异**：这份答卷是工业实践者视角，重"能跑通"；论文读者会期待更细致的理论对照（如 GRPO 收敛性证明）。

## 工程 / 研究启发

从这份 32 答中能读出的最大启发不在任何具体技巧，而在**对工业 RL 训练栈的心智模型**：

1.  **把 70% 调试精力放在 trust region / clip / aggregation / logprob consistency 上，剩下 30% 给算法变体**。这是与论文阅读完全不同的优先级。
2.  **把 RL 栈视为 6 层：Reward/Env → Policy Update → Logprob Consistency → Rollout Engine → Parallelism → Async Orchestration**。每层都有独立的工程默认值，问题通常出在层与层的接口（典型如 trainer-inference 数值一致性）。
3.  **把 KL 当作 reference anchor，不当作装饰**。RLVR 阶段可去、RLHF 阶段必须保留；把"GRPO 不带 KL"硬编码到所有任务上会丢失一半任务的能力。
4.  **异步 RL 的真实瓶颈是 staleness 1-4 步区间的 importance ratio 尾部**。超过这个范围需要 rejection 或更复杂的修正（AReaL 的策略）。
5.  **能力扩展不在 RL 本身，而在"exploration × diversity × verifier coverage"**。RL 主要是 sharpener 不是 creator——这一观点是 2026 年最值得记住的工业判断之一。
6.  **算法选型收敛到 GRPO 一族**。Dr.GRPO/DAPO/GSPO/CISPO/MaxRL 的差异是稳定性细节，不是新算法族。RL 项目在做算法选型时，不必追逐最新方法；先把基线跑稳再按需引入一项 trick。

对正在准备 RL/RLHF 方向面试的读者：这份 32 答可以当成"**工业实践者的答卷**"——它告诉读者在真实工作里这些概念怎么被使用、哪些细节是判断力所在、哪些是"作坊知识"。把 32 答与 sheriyuo 题面笔记的"考点"视角配对读，会得到比单读任一份都完整的认知。

## 证据边界与资料索引

本篇解读基于一份公开 X (Twitter) 帖文，是 @vivek_2332 对 @sheriyuo 整理的 *RL Interview Questions 2026* 35 道面经的 32 答答卷（算法 16 + Infra 16）。本文对原帖做主题重排、概念补全和批判性校正；不是原帖作者观点的逐字转述。

为避免把短帖误读成完整教材，本文补充参考了若干公开论文、项目文档与技术博客，用于核对 GRPO 家族、异步 RL、DPO、OPD、train-inference mismatch、vLLM/SGLang、Prime-RL 等概念的通用含义。具体工程实现仍以各项目当前版本为准。

- [@vivek_2332: "went through most of these. dumping my answers..." 原帖](https://x.com/vivek_2332/status/2063566811749331353)（2026-06-07；互动数据会随平台变化）
- [@sheriyuo: RL Interview Questions 2026 题面原帖与 X Article](https://x.com/sheriyuo/status/2063295181131247674)（2026-06-06）
- [DAPO: An Open-Source LLM Reinforcement Learning System at Scale](https://arxiv.org/html/2503.14476)：用于核对 clip-higher、dynamic sampling、token-level loss、overlong shaping 等 DAPO 机制。
- [Group Sequence Policy Optimization](https://arxiv.org/html/2507.18071v2)：用于核对 GSPO 的 sequence-level importance ratio 与 MoE 稳定性动机。
- [MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention](https://arxiv.org/html/2506.13585)：包含 CISPO 作为 MiniMax-M1 训练 recipe 的公开说明。
- [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/html/2501.12948v1)：用于理解 RLVR、GRPO 与 reasoning emergence 的背景。
- [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](https://arxiv.org/pdf/2305.18290)：用于核对 DPO 的隐式 reward 与 reference policy log-ratio 解释。
- [Thinking Machines: On-Policy Distillation](https://thinkingmachines.ai/blog/on-policy-distillation/)：用于核对 OPD 的 on-policy rollout 与 teacher supervision 关系。
- [Thinking Machines: Defeating Nondeterminism in LLM Inference](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)：用于核对 batch invariance、reduction order 与推理确定性的系统问题。
- [AReaL Asynchronous RL 文档](https://areal-project.github.io/AReaL/en/algorithms/async.html)：用于核对 fully async RL、max off-policyness 与 staleness 控制。
- [PrimeIntellect-ai/prime-rl README](https://github.com/PrimeIntellect-ai/prime-rl/blob/main/README.md)：用于核对 Prime-RL 的 fully async、FSDP2、vLLM、FP8 inference、PD disaggregation、EP/CP 等定位。
- 既有题面解读笔记：[RL Interview Questions 2026：从面经到 LLM/Agentic RL 全栈能力地图](/notes/tech-analysis/rl-interview-questions-2026.html)

证据边界：(1) X 平台内容可能被删除、修改或因登录状态呈现不同；本文只依赖公开可见文本，不依赖精确互动量；(2) vivek 对 ProRL、DeepSeek V4、AReaL KV cache、Slime 等话题保留了"not sure / haven't read"声明，本文没有把这些部分扩展为确定事实；(3) 文中关于 Prime Intellect 的判断来自原帖中对 @PrimeIntellect 的推荐与 Prime-RL 公开资料，只说明技术立场和工具偏好，不推断未公开的组织关系。
