<!-- 从 rl-secondary.html 迁移的资料快照；原始 HTML SHA-256: d712a98d498d7449a46a9a5367ec93a5c95a1c8e9fff5e348d523368c49fcbdc。 -->

## 核心判断：这是一张 RL 岗位雷达图，不是一套标准答案

**一句话解读：**作者整理的“RL Interview Questions 2026”真正揭示的是岗位范式变化：LLM 后训练里的 RL 已经不再是单独的算法问题，而是由 **采样、奖励、优势估计、trust region、推理服务、分布式训练、权重同步、环境系统和评估闭环**共同决定的复杂工程科学。

如果把它当成“35 道面试题”，会感觉每题都很散；如果把它当成能力地图，它其实非常完整。算法部分从 REINFORCE/PPO/GRPO 一路追到 DAPO、GSPO、CISPO、DPPO、MaxRL、OPD；Infra 部分从显存里有几个模型追到 KV cache、continuous batching、异步 rollout、MoE Expert Parallelism、batch invariance 和 slime/AReaL/VeRL 这类框架差异。两部分共同指向一个结论：

**现代 LLM RL 的面试不再接受“只懂公式”或“只会跑框架”。候选人必须能把 loss、logprob、rollout、cache、parallelism、staleness 和 reward 的因果链讲清楚。**

Policy Gradient PPO / GRPO RLVR Agentic RL vLLM / SGLang MoE Async RL OPD

## 阅读路线：35 题实际对应五条主线

[1. 为什么 2026 年 RL 面试突然全栈化](#problem) [2. LLM RL 训练循环的共同机制](#mechanism) [3. 算法 19 题逐题深解](#algorithm-questions) [4. Infra 16 题逐题深解](#infra-questions) [5. 术语解释与概念边界](#terms) [6. 证据边界与准备策略](#limits)

| 主线 | 覆盖问题 | 真正考察 | 高质量回答的共同特征 |
|----|----|----|----|
| RL 基础 | Actor-Critic、KL/CE/MLE、reward、Monte Carlo、advantage | 是否理解 policy gradient 的方差、偏差和采样语义 | 能说明 baseline 不改变期望但降低方差，能区分 reward scale、prompt difficulty 与 loss aggregation |
| PPO/GRPO 系列 | clipping、KL、GRPO、DAPO、GSPO、CISPO、DPPO、MaxRL | 是否知道“实现细节就是算法目标的一部分” | 能把每个方法映射到：advantage、ratio、clip、mask、normalization、aggregation、采样策略 |
| 能力边界 | RL 能否扩展 LLM 能力、ProRL、OPD、推理能力 emergence、DeepSeek 系统演进 | 是否能做研究判断，而非复述论文口号 | 能区分“放大已有潜能”“改变采样分布”“创造新知识”“利用 test-time compute” |
| Rollout / Serving | KV cache、continuous batching、vLLM/SGLang、长尾 rollout、利用率 | 是否理解 generation 是 LLM RL 的主要成本中心 | 能解释 prefix sharing、cache locality、server mode、request-level async 与训练信号一致性的关系 |
| 分布式训练与框架 | model copies、backprop、多机通信、EP、long context、determinism、AReaL/slime/VeRL | 是否能在真实系统约束下选择方案 | 先问模型规模、硬件、任务形态、同步/异步、MoE/稠密、reward 成本，再给方案 |

## 问题背景：为什么 RL 面试从公式题变成系统题

传统 RL 面试常围绕 Bellman equation、Q-learning、policy gradient、Actor-Critic、TRPO/PPO 展开。LLM 后训练把问题改写了：我们通常不是从随机策略训练一个 agent，而是在一个已经很强的 base model 上做能力定向、偏好对齐或 verifiable reward 训练。模型已有强先验，动作空间巨大，环境通常是语言、代码、工具调用或 verifier，reward 常常稀疏，rollout 极其昂贵。

这带来四个变化。

### 1. 训练瓶颈从 backward 迁移到 rollout

在 reasoning RLVR 或 Agentic RL 中，生成候选答案、执行工具、跑测试、调用搜索、维护多轮上下文，往往比一次参数更新更耗时。PPO/GRPO 的公式只解释“如何更新”，但真实吞吐由 rollout engine、cache、batching、环境并发和权重同步决定。

### 2. 算法设计被显存和通信约束塑形

GRPO 去掉 critic，不只是统计学习上的选择，也是显存和工程复杂度约束下的选择。DAPO dynamic sampling 看似只是过滤无学习信号的 prompt，实际要求框架能处理变长 batch 和额外生成成本。

### 3. logprob 一致性成为一等公民

PPO/GRPO/CISPO 都依赖当前策略与旧策略的概率比。如果 rollout engine 和 training engine 的 tokenizer、precision、batch shape、MoE routing 或 kernel 行为不一致，importance ratio 就会被污染，clip 与 advantage 再正确也没用。

### 4. Agentic RL 引入长尾和状态分布问题

数学题可以单轮生成后判分；代码、浏览器、终端和工具调用任务会产生长程、多轮、重尾 episode。同步 batch 会被最慢样本拖住，异步系统又会引入 stale policy 和 off-policy bias。

因此，这份问题清单不是在问“你背过哪些算法名”，而是在问：当你面对一个真实 LLM RL 训练系统时，能否定位瓶颈、判断哪些近似可接受、哪些实现细节会改变优化目标，以及哪些论文技巧在你的硬件和任务上根本不成立。

## 共同机制：LLM RL 训练循环到底在发生什么

无论叫 PPO、GRPO、DAPO、CISPO，LLM RL 训练大多可以抽象成以下链路：

| 阶段 | 输入 | 处理 | 输出 | 典型失败条件 |
|----|----|----|----|----|
| 采样 | prompt / task、当前或旧 policy、采样参数 | 生成一个或多个 response / trajectory | tokens、old logprobs、KV cache、环境轨迹 | 采样太保守没有探索；太激进产生无效轨迹；多轮任务长尾拖慢 batch |
| 打分 | response、reference answer、test suite、reward model 或 verifier | 给 sequence 或 step 赋 reward | 标量 reward、过程反馈、pass/fail | reward hacking、稀疏信号、错误 verifier、全对/全错 group 无梯度 |
| 优势估计 | reward、group、baseline、value model 或 batch statistics | 减 baseline、可能除以 std、可能做 leave-one-out | advantage | normalization 放大错误样本；长度归一化引入偏置；跨任务 reward scale 冲突 |
| 策略更新 | advantage、old/current logprob、clip 或 KL 约束 | 用 policy gradient 提高好轨迹概率、降低坏轨迹概率 | 更新后的 actor weights | ratio 爆炸、clip 过度 mask、staleness 过大、logprob 计算不一致 |
| 权重同步 | 训练后的 actor weights | 同步到 rollout engine 或 serving cluster | 新的 rollout policy | 同步慢导致 GPU idle；异步太深导致 off-policy；resharding 复杂 |

用公式看，最朴素的 policy gradient 是：

\\ \nabla\_\theta J(\theta) = \mathbb{E}\_{y \sim \pi\_\theta(\cdot\|x)}\left\[\nabla\_\theta \log \pi\_\theta(y\|x)\\ r(x,y)\right\] \\

减去不依赖动作的 baseline 后，期望梯度不变，但方差下降：

\\ \nabla\_\theta J(\theta) = \mathbb{E}\left\[\nabla\_\theta \log \pi\_\theta(y\|x)\\ (r(x,y)-b(x))\right\] \\

PPO/GRPO 再引入旧策略与当前策略的概率比：

\\ \rho_t(\theta)=\frac{\pi\_\theta(a_t\|s_t)}{\pi\_{\theta\_{old}}(a_t\|s_t)} \\

这个 ratio 是现代 LLM RL 系统里最容易被工程细节污染的量：旧策略是哪个版本？old logprob 是 rollout 时保存的还是训练时重算的？推理 engine 和训练 engine 是否同精度、同 tokenizer、同 MoE routing？异步 rollout 的样本 stale 几步？这些问题决定了 loss 是否还在优化你以为的目标。

## 算法 19 题逐题深解：每题真正想听什么

下面不是“唯一标准答案”，而是把每道题拆成考点、回答骨架和常见误区。真实面试里最重要的是先限定场景：数学 RLVR、代码 RL、偏好对齐、工具调用 Agent、MoE 模型、异步系统，答案都可能不同。

### 1. 为什么要用 Actor-Critic，而不是纯 Critic？

考点是否理解值函数方法和策略梯度方法各自适合什么动作空间。

纯 Critic 方法学习的是 value 或 Q-value，再通过取最大值选择动作。它在离散且动作空间相对小的环境里很自然，但 LLM 的动作是词表级 token，且每一步状态是长前缀；如果对每个 token 精确估计 Q-value，计算和泛化都很困难。Actor 直接参数化策略 \\\pi\_\theta(a\|s)\\，可以用模型原本的 next-token distribution 表达动作分布；Critic 则作为 baseline 估计状态价值，降低 policy gradient 方差。

现代 LLM RL 的反转在于：PPO 的 Critic 很贵，通常与 actor 同量级；GRPO/RLOO/Dr.GRPO 等方法尝试用 group baseline 或 leave-one-out baseline 替代 learned critic。因此高质量回答不是简单说“Actor-Critic 更稳定”，而是要说清：**在 LLM 场景里，actor 是天然存在的语言模型，critic 是昂贵的方差降低器；是否需要 critic 取决于 reward 稀疏性、group sampling 成本、显存预算和任务形态。**

### 2. KL 散度、交叉熵、MLE 的关系是什么？

考点是否能把监督学习、分布匹配和 RL regularization 联系起来。

交叉熵可以写成真实分布 \\p\\ 对模型分布 \\q\\ 的期望负对数似然：\\H(p,q)=H(p)+D\_{KL}(p\\q)\\。当数据分布 \\p\\ 固定时，最小化交叉熵等价于最小化 forward KL，也等价于最大似然估计。SFT 本质上是在 teacher/human 数据分布给出的 token 上做 MLE。

RL 里的 KL 常用于约束策略不要偏离 reference policy 或 old policy。偏好优化和 distillation 里 forward KL / reverse KL 的行为也不同：forward KL 更偏覆盖 teacher 分布，reverse KL 更偏 mode-seeking。LLM 后训练里的很多方法可以从“在哪个状态分布上、用哪个 KL 方向、对哪个 teacher/reference”来理解。

### 3. 不同 RL 场景应该如何设计 Reward？

考点是否知道 reward 不是分数函数，而是训练目标的接口。

数学和代码 RLVR 可以用规则 verifier、单元测试、答案匹配等 verifiable reward；偏好对齐常用 reward model 或 pairwise preference；Agentic RL 可能需要 outcome reward、process reward、tool-use validity、格式约束、成本惩罚和安全约束共同组成。设计 reward 时要回答四个问题：奖励是否可验证？是否密集？是否容易被 hack？是否和产品目标一致？

典型陷阱是把格式奖励、长度奖励、正确性奖励简单相加，却没有校准 scale；或者只给最终 pass/fail，导致长程任务 credit assignment 极差；或者 reward model 只在参考分布上可靠，RL 后 policy 出分布后被 reward hacking 利用。

### 4. 如何理解 RL 中的 importance sampling / rejection sampling 等 Monte Carlo 方法？

考点是否理解“我们只能采样估计期望”，以及 off-policy 修正为什么必要。

RL 目标通常是对策略诱导分布下的回报求期望，真实期望不可精确计算，只能通过 rollout 做 Monte Carlo 估计。importance sampling 用 \\\pi\_\theta / \pi\_{old}\\ 修正“样本来自旧策略，但目标是当前策略”的分布错配。PPO 的 ratio 本质上就是 importance weight，再用 clipping 控制方差。

rejection sampling 在 LLM 训练里也常见：先生成多个候选，再用 verifier 或 reward 过滤高质量样本，用于 SFT、distillation 或构造 preference 数据。它和 RL 的区别在于，rejection sampling 常把保留下来的样本当作离线监督目标，而 RL 需要显式处理采样策略、概率比和梯度估计。

### 5. PPO / GRPO 的 advantage 怎么算？为什么减 baseline？一定要除以 std 吗？

考点这是全篇最核心的问题之一。

PPO 通常用 critic 和 GAE 估计每个 token/state 的 advantage；GRPO 不训练 critic，而是对同一 prompt 采样 \\G\\ 个回答，用 group reward 做相对优势：

\\ \hat{A}\_i = \frac{r_i - \mu_G}{\sigma_G} \\

减 baseline 的意义是降低方差；只要 baseline 不依赖当前 action，就不会改变期望梯度。但“除以 std”不是数学必需，而是 scale normalization。它能让不同 prompt 的 reward scale 更可比，也可能放大低方差 group：例如 8 个回答里 7 个正确、1 个轻微错误，std 很小，那个差异可能被放大成过大的训练信号。Dr.GRPO 和 MaxRL 一类工作都提醒：normalization 不是中性操作，它会改变哪些 prompt 主导梯度。

### 6. RL training 和 test-time scaling 各自如何 explore？

考点是否能区分“训练时改变 policy”和“推理时增加搜索”。

RL training 的探索来自 on-policy sampling：模型生成多个候选或 trajectory，reward/verifier 选择哪些行为应被强化。训练后，policy 的概率分布会改变。test-time scaling 则是在不改权重的情况下增加推理计算，例如采样更多候选、树搜索、自一致性、verifier reranking、工具调用重试、反思修正等。

二者关系是互补的：test-time scaling 可以发现模型低概率但正确的解；RL training 可以把这些解的模式内化到模型中，提高 pass@1 或降低推理成本。边界是：如果模型从未能采样到有效轨迹，RL 没有正信号；如果 verifier 不可靠，test-time search 也会放大错误。

### 7. PPO 如何 clip？为什么取 min？不 clip 会怎样？CISPO 怎么做？

考点是否真正理解 PPO 的 trust region 近似。

PPO 目标常写为：

\\ L^{PPO}=\mathbb{E}\left\[\min\left(\rho_t\hat{A}\_t,\operatorname{clip}(\rho_t,1-\epsilon,1+\epsilon)\hat{A}\_t\right)\right\] \\

取 min 是为了保守：正 advantage 的 token 概率涨太多后停止继续奖励；负 advantage 的 token 概率降太多后停止继续惩罚。不 clip 会让多 epoch reuse rollout 时策略快速远离旧策略，importance ratio 方差变大，训练不稳定。

CISPO 的批评是：PPO 的 hard mask 会让超出 clip 区间的 token 直接失去梯度，而这些 token 可能是推理行为跃迁的关键 token。CISPO 选择 clip importance weight，但不删除 token 的梯度流，以获得稳定性与学习效率之间的折中。

### 8. GRPO 为什么加 KL？KL 怎么算？为什么 DAPO、GSPO 又去掉或弱化 KL？

考点是否知道 KL 是 reference anchor，不是装饰项。

GRPO 原始形式中会加入相对 reference model 的 KL penalty，目的是防止 policy 过度偏离原模型，保留语言质量、安全性和通用能力。在 RLHF 中，KL 尤其重要，因为 reward model 往往只在 reference 附近可靠；偏离太远会 reward hacking。

在数学/代码 RLVR 中，如果 reward 是强 verifier，KL 可以变小甚至移除，因为正确性信号更硬，且过强 KL 会压制模型探索长链推理。DAPO、GSPO 等方法的变化往往来自经验：某些 setting 下 KL regularization 不是主要稳定器，clip、sampling、loss aggregation 和 logprob 一致性更关键。但不能泛化成“KL 没用”；在开放式偏好、安全、多任务或弱 verifier 场景，KL anchor 仍可能必要。

### 9. LLM 训练时如果不小心多 All Reduce 了几次 loss，会发生什么？

考点这是分布式训练基本功题。

如果 loss 或梯度在 data parallel 维度上被重复 all-reduce / average，梯度 scale 会被错误缩放。常见后果包括：有效 learning rate 变小或变大、梯度统计和日志 loss 不一致、不同并行维度上的 normalization 错误、训练变慢甚至不稳定。更隐蔽的是，在 PPO/GRPO 里，loss reduction 方式本身就影响 token/sequence/prompt 权重；多一次错误聚合可能改变训练目标，而不仅是数值比例。

面试回答要说明具体并行语境：DP、TP、PP、FSDP、sequence parallel、gradient accumulation 的 reduction 语义不同。不能只说“loss 变小”。

### 10. DPO 的 reward 是什么？会不会 reward hacking？如何解决？

考点是否理解 DPO 把 reward model 隐式化了。

DPO 从 Bradley-Terry preference model 出发，把偏好对 \\(y_w,y_l)\\ 的优化写成 policy 与 reference policy log-ratio 的分类目标。其隐式 reward 可理解为：

\\ r\_\theta(x,y) \propto \beta \left(\log \pi\_\theta(y\|x)-\log \pi\_{ref}(y\|x)\right) \\

DPO 不显式训练 reward model，因此避免了一部分在线 RL reward hacking，但并不免疫：如果 preference 数据有偏、chosen/rejected 构造错误、长度/style confound 强，模型仍会学习偏好数据里的捷径。缓解方法包括更干净的 preference 数据、长度控制、reference anchor、IPO/KTO/ORPO 等变体、在线验证、拒绝采样质量控制和独立评估。

### 11. 有哪些解决 MoE 训推不一致问题的算法或工程方法？

考点是否知道 MoE 会放大 logprob mismatch。

MoE 的 router、expert parallelism、top-k routing、capacity、dropless/drop token、精度和 batch shape 都会影响输出概率。训练与推理不一致会直接污染 RL 的 old/current logprob ratio。解决方向包括：保持训练和推理使用一致的 tokenizer、chat template、precision 和 LM head；保存 rollout logprob；用同一 serving engine 进行生成和 scoring；FP32 logits 或 FP32 LM head；对 routing 做 deterministic 控制；监控 training-time 与 inference-time logprob correlation；对异常 ratio 做 filtering 或 clipping。

算法层面，GSPO/DPPO/CISPO 等对 token ratio 噪声或 trust region 定义做调整，也可以部分缓解低概率 token 与框架 mismatch 带来的不稳定，但不能替代系统一致性。

### 12. RL 训练时 group size / learning rate / PPO epoch / generation length 如何设置？

考点是否能把超参和成本、方差、staleness 联系起来。

- **Group size：**越大，GRPO advantage 估计更稳定，prompt 内比较更可靠；但 rollout 成本线性上升，且 prefix cache 与并发能力成为瓶颈。
- **Learning rate：**过大导致 policy 快速偏离 old policy，ratio 爆炸；异步或多 epoch 场景尤其危险。
- **PPO epoch：**复用 rollout 提高样本效率，但每多训一轮都更 off-policy，需要 ratio/clip/KL 控制。
- **Generation length：**太短截断正确推理，太长增加 KV cache 和长尾；还会和 length penalty、overlong reward shaping、loss aggregation 相互作用。

高质量回答应给出调参原则，而不是死记数值：先看 reward 稀疏度、全对/全错比例、clip fraction、KL、ratio 分布、response length 分布、GPU 利用率和 wall-clock throughput。

### 13. Dr.GRPO / DAPO / GSPO / CISPO / SAPO / DPPO / MaxRL / SimKO 如何改进 GRPO？缺点是什么？

考点是否能把新方法归类，而不是背论文名。

| 方法 | 主要改动 | 解决的问题 | 代价 / 边界 |
|----|----|----|----|
| Dr.GRPO | 去除有害 std / length normalization，修正 loss aggregation | 减少长度偏置和低方差 group 被过度放大 | 不同任务上是否去 std 仍需验证；scale 混合任务可能仍需归一化 |
| DAPO | asymmetric clipping、dynamic sampling、token-level aggregation、overlong shaping | 提高有效梯度比例，给低概率正确 token 更多上升空间 | dynamic sampling 增加 rollout 成本，要求框架支持变长 batch |
| GSPO | sequence-level importance ratio | 缓解长序列 token-level ratio 噪声，适配部分 MoE 场景 | sequence ratio 可能掩盖局部 token 问题；实现细节影响大 |
| CISPO | clip IS weight，但不 hard mask token 梯度 | 保留高信息 token 的学习信号 | 需要精细监控 ratio 长尾；过松仍可能不稳定 |
| SAPO | 用 soft gate 替代硬 clipping | 让 trust region 过渡更平滑，减少梯度突变 | 引入额外温度/形状超参；实证范围仍需看具体任务 |
| DPPO | 用 policy divergence 而非 sampled-token ratio 定义 trust region | 低概率 token 的 ratio 不一定代表整体策略变化 | 近似 divergence 的计算和阈值选择复杂 |
| MaxRL | 从 pass@k / MLE 角度重构目标 | 保留多样性，改善 test-time scaling 友好性 | 依赖多样本成功统计；极难 prompt 仍可能无正信号 |
| SimKO | 重分配 top-k 候选梯度，缓解 top-1 collapse | 减少分布塌缩，保持 pass@k 能力 | 需要更细的候选分布建模和额外计算 |

### 14. TRPO / DPPO / AReaL 如何用 trust region 约束 RL objective？

考点trust region 的定义不是唯一的。

TRPO 用 KL constraint 直接限制新旧 policy 的分布距离；PPO 用 clipped ratio 作为近似。DPPO 认为 sampled-token ratio 对低概率 token 太敏感，因此改用估计的 policy divergence 作为 mask 或约束。AReaL 面对异步 RL，还要把 staleness 纳入 trust region：样本来自哪个 policy version？旧 policy 与当前 policy 差几步？clip bound 是否要随 stale 程度调整？

答案的关键是：trust region 不是为了形式美，而是为了控制 reuse rollout、异步采样和大步更新带来的 off-policy 偏差。

### 15. RL 能否 fundamentally expand LLM 的 capability frontier？

考点研究判断力。

谨慎答案是：RL 可以扩展“可采样、可验证、可强化”的能力边界，但很难凭空创造 base model 完全没有的知识和技能。RL 的强项是把低概率正确行为拉高，把 test-time search 中偶然出现的成功模式内化，把 verifier 能判断的目标优化得更好。它的弱点是：没有正样本就没有学习信号，reward 错了会学错，verifier 覆盖不到的能力无法直接强化。

因此，RL 更像能力激活器、分布重塑器和搜索策略训练器，而不是魔法知识注入器。真正的 frontier 扩展通常来自 pretraining/mid-training、数据、环境、verifier、test-time compute 与 RL 的组合。

### 16. 结合 ProRL 等工作，如何思考 scale RL 训练边界？

考点scale 不是简单加 GPU。

RL scale 的边界至少有五个：prompt 难度分布、rollout 数量、verifier 质量、训练稳定性和系统吞吐。扩大 rollout 可以提高探索，但 generation 成本、KV cache、长尾、staleness 会迅速成为瓶颈；扩大难题比例可以推动能力，但如果成功率长期为零，反而没有梯度；加大模型规模可能提高可采样成功率，但也放大权重同步和 MoE 通信问题。

所以 scale RL 不是“更大 batch、更长训练”，而是持续调节 curriculum、采样温度、group size、过滤策略、reward 密度、异步深度和评估闭环。

### 17. OPD 相比传统 RL / SFT 的改进是什么？有哪些应用？

考点是否理解 state distribution mismatch。

SFT 在 teacher/human 数据状态上训练，容易出现 exposure bias：模型实际生成时进入自己的状态分布，老师轨迹里没有这些前缀。RL 使用 on-policy rollout，状态分布对齐，但 reward 稀疏且高方差。OPD，即 on-policy distillation，让 student 先生成自己的 trajectory，再让 teacher 在这些 student states 上提供 dense supervision。

因此 OPD 介于 SFT 和 RL 之间：像 RL 一样 on-policy，像 SFT/distillation 一样有密集 teacher 信号。它适合 teacher-to-student reasoning distillation、agent 多轮纠偏、verifier 训练、弱到强迁移、以及无法直接设计强 reward 但可以让 teacher 提供反馈的场景。边界是：teacher 必须真的比 student 强，且 teacher 与 student 的思维模式不能完全不兼容；否则 OPD 可能只是把 student 拉向一个不可达或不适合的分布。

### 18. LLM 推理能力在哪个训练阶段产生？

考点是否拒绝单因果叙事。

推理能力不是某一个阶段突然凭空产生。预训练提供语言、知识、模式匹配和隐式算法基础；mid-training 可以把模型推向数学、代码、长上下文或 agent 轨迹分布；SFT 教模型用可读格式表达推理；RL/RLVR 强化正确性、验证、反思、搜索和长链行为；test-time scaling 再通过采样/搜索放大可用能力。

所谓 “Aha moment” 更像是模型已有潜能在 reward、采样和训练压力下显性化，而不是 RL 单独创造了推理。成熟回答要把 emergence 拆成：能力基座、行为格式、探索概率、verifier 信号和训练稳定性。

### 19. 从 DeepSeek R1 到后续系统，RL 部分可能有哪些改进？MoE RL 有什么不同？

考点是否能把公开系统演进抽象为工程方向，而不是编造版本细节。

公开讨论中，R1 代表了 RLVR 对 reasoning behavior 的强刺激：用 verifiable reward 鼓励长链推理、反思和自我验证。后续系统的 RL 改进通常会围绕几个方向：更好的 reward/verifier、更精细的 credit assignment、更强的 rollout throughput、更稳定的 MoE 训推一致性、更低成本的异步训练、更好的 distillation 和多任务 post-training pipeline。

MoE RL 的不同在于：active parameters 与 total parameters 分离，expert routing 会影响吞吐和 logprob；EP 引入 all-to-all；不同 batch shape 可能改变 routing 或数值；训练和推理 engine 的差异更容易放大。因此 MoE RL 不是把 dense RL recipe 直接搬过去，而是要把 router、expert load balance、FP8/FP32 边界、EP 通信和 logprob 对齐一起设计。

## Infra 16 题逐题深解：真正的瓶颈通常不在 loss 上

Infra 部分是这篇文章最有含金量的地方。它逼迫读者承认：两个团队都说自己在“跑 GRPO”，最终效果和效率可能完全不同，因为 rollout engine、权重同步、batching、cache、parallelism、precision 和 staleness 都不一样。

### 1. 不考虑 CPU offload，GRPO 训练时显存里有几个模型？优化能省多少显存？

常见角色包括 actor、rollout、reference、critic、reward。PPO 通常需要 critic；GRPO 的核心节省就是去掉 critic，用 group baseline 替代 value model。若 reward 是规则 verifier，则不需要 reward model；若 reward 是模型，还要额外显存。actor 训练态还包含 optimizer state、gradients、activations；rollout/reference 通常只需要 inference weights 和 KV cache。

不能死答“几个模型”，必须先问：actor/rollout 是否 colocate？reference 是否共享 base 或 offload？reward 是函数还是模型？FSDP/ZeRO/Megatron 怎么 shard？优化手段包括去 critic、LoRA、gradient checkpointing、ZeRO/FSDP、activation recompute、CPU offload、reference 合并/延迟计算、rollout 与 actor 权重共享、FP8 inference、KV cache 优化等。

### 2. 分布式推理：KV cache 传输优化和多卡通信策略

RL rollout 常生成大量长回答，decode 阶段受 KV cache 和内存带宽限制。优化方向包括 paged attention、prefix cache、radix tree prefix sharing、prompt group 内共享前缀、KV cache eviction、PD disaggregation、tensor parallelism、pipeline parallelism、DP-aware routing、同一 agent trajectory 路由到同一 cache locality。

多卡通信上，prefill 和 decode 的瓶颈不同：prefill 更像大矩阵计算，decode 更受带宽和 cache 管理限制；TP 会引入每层通信，EP 会引入 all-to-all，长上下文还会引入 context parallel。RL 系统要优化的是 end-to-end rollout latency 和 tail latency，而不只是单请求 tokens/s。

### 3. INT8 与 FP8 优劣对比，训练和推理分别用什么精度？

INT8 多用于推理量化，生态成熟，吞吐和显存收益明显，但训练中梯度、optimizer state 和高动态范围激活更难处理。FP8 保留浮点指数，适合 Transformer 训练/推理的混合精度路径，尤其在 H100/Blackwell 等硬件上有更好支持。FP8 常见格式包括 E4M3 和 E5M2，前者精度更高、范围较小，后者范围更大。

LLM RL 里还要额外关心 logprob 一致性。即使推理用 FP8 提速，LM head/logits、reward-sensitive scoring 或 importance ratio 相关路径可能需要 BF16/FP32，避免量化误差把 ratio 搞坏。

### 4. RL rollout 中的长尾问题是什么？有哪些解决方案？

长尾问题指不同 trajectory 完成时间差异极大：有的数学回答几十 token 结束，有的代码任务要跑测试数分钟，有的 agent 工具调用会卡住。同步 batch 会等待最慢样本，导致 GPU idle。

解决方案包括 request-level async、partial rollout、over-generate 后取先完成样本、超时截断、环境并发池、server mode inference、分离 rollout/training GPU、长任务 checkpoint/resume、按任务类型调度、tail latency-aware routing。关键取舍是：减少等待通常会引入 staleness、样本偏差或丢弃部分数据，需要在算法上补偿。

### 5. continuous batching 在 RL 训练时有什么问题？vLLM 和 SGLang 区别是什么？

continuous batching 能动态把不同请求合到同一 decode batch，提高推理吞吐。但 RL 里它带来额外问题：请求顺序和 batch shape 变化可能影响数值确定性；不同请求长度导致 KV cache 碎片；多轮 agent 需要 cache locality；old logprob 保存和重算必须对齐；动态 batch 让复现实验更难。

vLLM 以 PagedAttention 和高吞吐 serving 生态著称；SGLang 强调结构化生成、radix cache、复杂 agent/programmatic workload 的调度能力，并常被 agentic RL 系统用作 rollout server。实际选择要看任务：单轮大吞吐、复杂多轮、prefix sharing、工具调用、框架集成和权重同步路径。

### 6. vLLM / SGLang 怎么看利用率？训练里的 KV cache 利用率怎么看？

不能只看 GPU utilization。推理系统要看 tokens/s、request latency、time-to-first-token、decode throughput、prefix cache hit rate、KV cache block usage、eviction、batch size、queueing delay、tail latency。RL 系统还要看 rollout wall-clock 占比、环境等待时间、训练等待 rollout 的时间、权重同步时间和有效样本率。

KV cache 利用率要结合 context length 分布、group size、prefix sharing、multi-turn affinity 和 block fragmentation。一个系统 GPU 利用率高，不代表 RL 训练快；如果高利用率来自无效长回答、全错 group 或 stale rollout，它对训练没有价值。

### 7. 多机多卡 RL 训练时如何实现反向传播？

大模型训练常组合 DP、TP、PP、FSDP/ZeRO、sequence/context parallel。反向传播时，TP 内需要对切分矩阵相关梯度通信，DP/FSDP 需要 reduce-scatter / all-gather，PP 需要流水线调度，长上下文可能需要 context parallel 通信。RL 与普通 SFT 的差别在于输入来自 rollout buffer，loss 还依赖 old logprob、advantage、mask、KL 和 per-token weighting。

回答时要说明：rollout 生成不参与反向传播；训练阶段用保存的 tokens 和 old logprobs 重新 forward 当前 policy，计算 current logprob，再通过 PPO/GRPO 类 loss 对 actor 反传。

### 8. RL 训练有哪些异步框架？解决同步训练什么问题？

同步训练流程是 generate all → score all → train → sync。它简单、确定、易 debug，但会被 rollout 长尾和权重同步拖慢。异步框架通过 rollout/training overlap、request-level async、fully async buffer、versioned policy 和 stale correction 提高吞吐。

代表性思路包括 VeRL 的 async/AgentLoop、AReaL 的 fully asynchronous RL、slime 的 SGLang-native rollout + Megatron training、TorchForge 的 service abstraction 等。它们解决的是 GPU idle、长尾 episode、环境并发和训练/推理资源耦合问题；代价是 staleness、复现难度和系统复杂度。

### 9. AReaL 或 partial rollout 框架会不会保存之前 policy 的 KV cache？

这题真正考的是：partial rollout 恢复时，cache 与 policy version 是否一致。KV cache 是某个模型权重、某个前缀下的中间状态。如果 policy 已更新，旧 KV cache 严格来说对应旧权重；继续用它生成新 token 会造成混合 policy trajectory。

实践上有几种选择：保存完整文本前缀而不是 KV cache，恢复时用新 policy 重新 prefill；保存旧 cache 并把 trajectory 标记为旧 policy，训练时用对应 old logprob 和 staleness correction；或在短 stale、工程收益足够时接受近似。高质量回答要指出这不是单纯缓存问题，而是 on-policy 语义问题。

### 10. MoE 的 Expert Parallelism 对 throughput 的影响

EP 把不同专家分布到不同 GPU/节点，降低每卡 expert 参数压力，但会引入 token dispatch 和 all-to-all 通信。吞吐取决于 active expert 数、top-k routing、load balance、capacity factor、batch size、token permutation、网络带宽和 expert 计算/通信 overlap。

在 RL 中，batch shape 比预训练更不稳定：response length、动态过滤、agent 长尾都会改变 token 分布，可能导致 expert load imbalance。MoE RL 因此需要同时看 tokens/s、expert utilization、dropped tokens、routing entropy、all-to-all 时间和 logprob 一致性。

### 11. Long context 场景下 compute-communication overlap，Megatron 和 FSDP 的 parallelism 差异

长上下文放大 attention compute、KV cache、activation memory 和跨卡通信。常见策略包括 sequence/context parallel、activation checkpointing、FlashAttention、ring attention、overlap all-gather/reduce-scatter、pipeline bubble 优化、prefill/decode 分离。

Megatron 更强调 TP/PP/CP/EP 等多维并行的显式组合，适合超大规模训练但配置复杂；FSDP 更偏参数 sharding 和 PyTorch 生态易用性，适合较灵活的中大规模训练。选择不是信仰问题，而取决于模型规模、节点网络、MoE、长上下文长度、团队工程能力和是否要与 rollout engine 快速同步。

### 12. 确定性模式怎么开？什么是 batch invariance？atomic add 能解决吗？

确定性模式涉及固定随机种子、禁用非确定性 kernel、设置 deterministic algorithm、固定数据顺序、固定采样参数、控制 CUDA/cuDNN/cuBLAS 行为、避免动态 batch 引入顺序变化。但 LLM serving 的 continuous batching 和 MoE routing 会让完全确定性很难。

Batch invariance 指同一个样本的输出或 logprob 不应因为和哪些其他样本同 batch 而改变。导致不变性破坏的原因包括浮点归约顺序、padding/position 处理、attention mask、MoE capacity/routing、quantization scale、atomic add 非确定性等。atomic add 可能是原因之一，但不能“解决”问题；它通常引入非确定性归约，真正解决要靠 deterministic kernel、固定路由、批无关 normalization 和一致的 scoring 路径。

### 13. AReaL 和 slime 对 RL rollout bottleneck 的理解有什么不同？

AReaL 的关键词是 fully asynchronous RL：通过异步 rollout、训练和 staleness-aware correction 减少同步等待，把 policy version 和 trust region 纳入算法设计。slime 的关键词是 SGLang-native 和环境驱动：让 rollout engine 以服务形式被环境调用，适配多轮 agent、工具调用和复杂环境，同时用 Megatron/FSDP 承担训练。

抽象地说，AReaL 更像从 RL 算法和异步训练一致性出发理解瓶颈；slime 更像从 agentic rollout 的 serving 架构、环境解耦和 SGLang cache/调度能力出发理解瓶颈。两者都承认 generation 和长尾是核心，但切入点不同。

### 14. full async staleness 怎么看，训练时大概是多少？

staleness 是 rollout policy version 与训练当前 policy version 的差距。一步 stale 通常可由 PPO/GRPO 的 importance ratio 和 clipping 承受；多步 stale 可能导致 ratio 长尾、clip fraction 上升、有效梯度下降甚至发散。

实际可接受值没有固定答案，取决于 learning rate、KL/clip、reward 稀疏性、模型变化速度和任务难度。工程上要监控 policy version lag、ratio distribution、KL、clip fraction、reward 曲线和训练稳定性。越早期训练、越高 LR、越稀疏 reward，越不能放任 stale。

### 15. slime 里 data 怎么流，Megatron 怎么结合，loss 怎么算？

slime 类系统的典型数据流是：环境或 rollout function 调用 SGLang server 生成 trajectory；数据进入 buffer；训练端从 buffer 取 tokens、attention mask、old logprob、reward、advantage 等；Megatron/FSDP actor 对这些 tokens 做 forward，得到 current logprob；再按 GRPO/DAPO/GSPO/PPO 类目标计算 loss 并反传；更新后把权重同步回 rollout engine。

关键是环境和训练解耦：环境可以是代码 sandbox、搜索、终端、浏览器或多轮 agent；训练只需要标准化后的 trajectory。loss 不是在 SGLang 里反传，而是在训练 engine 中用 rollout 记录重算当前 policy probability。

### 16. VeRL / TRL / Unsloth / AReaL / slime 你会选哪个？

这题没有绝对答案，重点是选型逻辑。

- **TRL：**适合入门、单机/小规模、快速验证算法和数据 pipeline。
- **Unsloth：**适合低成本 fine-tuning 和资源受限实验，但不一定覆盖复杂 RL infra。
- **VeRL：**适合开源生态较成熟、算法覆盖广、需要 PPO/GRPO/agent loop 与 Ray 资源管理的场景。
- **AReaL：**适合重点研究异步 RL、staleness-aware training、PPO-like 变体配置切换的场景。
- **slime：**适合 SGLang-native、多轮 agentic rollout、环境驱动、Megatron 训练和复杂 serving 集成。

真正的回答应该先问：模型多大？稠密还是 MoE？数学 RLVR 还是 agentic RL？几张卡还是多节点？是否需要异步？是否有自定义环境？是否要求生产 serving 一致？

## 关键证据：这 35 题为什么能代表 2026 RL 能力结构

### 证据 1：算法变体集中修同一批细节

Dr.GRPO、DAPO、GSPO、CISPO、DPPO、SAPO、MaxRL 等方法并不是互不相关的新大陆，而是在 advantage normalization、loss aggregation、importance ratio、clipping/masking、trust region 和采样效率上做局部但关键的修正。这说明 LLM RL 的核心不是“换一个名字”，而是把每个 reduction、ratio 和 mask 的统计含义弄清楚。

### 证据 2：GRPO 的流行本身就是系统约束的产物

去掉 critic 直接改变显存占用和训练复杂度。一个算法如果节省一个同量级 value model，就会让大模型 RL 从“不现实”变成“可跑”。这证明算法选择无法脱离硬件与框架。

### 证据 3：rollout generation 是 LLM RL 的主要成本中心

在 reasoning 和 agentic 任务里，生成、工具调用、测试执行和长上下文 decode 经常占据大部分时间。于是 KV cache、continuous batching、prefix sharing、server mode、async rollout 成为面试题，而不是 infra 工程师的边缘知识。

### 证据 4：训练-推理一致性会直接改变 RL loss

如果 old logprob 或 current logprob 因 precision、MoE routing、batch shape、tokenizer 或 serving kernel 差异而不一致，PPO/GRPO 的 ratio 就不是理论里的 ratio。系统误差会伪装成算法不稳定。

## 术语解释与概念边界

### RLVR

Reinforcement Learning with Verifiable Rewards。用可自动验证的奖励训练模型，例如数学答案检查、代码测试、规则 verifier。优点是 reward 更硬；难点是 reward 稀疏和 credit assignment。

### GRPO

Group Relative Policy Optimization。对同一 prompt 采样多条回答，用组内相对 reward 做 baseline，省掉 PPO 的 critic。

### Advantage

某个动作或轨迹相对 baseline 好多少。它不是 reward 本身，而是“比预期好/坏”的训练信号。

### Importance Ratio

当前策略与生成样本的旧策略对同一 token/trajectory 的概率比。PPO/GRPO 用它修正 rollout reuse 带来的分布错配。

### Trust Region

限制新旧 policy 差距的机制。PPO 用 clipped ratio 近似，TRPO 用 KL constraint，DPPO 试图用 divergence mask。

### KV Cache

Transformer decode 时保存每层 key/value，避免重复计算历史 token。长上下文和多轮 agent 中，它直接决定推理显存和延迟。

### Continuous Batching

推理服务把不同时间到达、不同长度的请求动态合批，提高 decode 吞吐。RL 中要额外关注 logprob 一致性和确定性。

### Staleness

异步 RL 中 rollout policy 与训练当前 policy 的版本差距。stale 越大，off-policy bias 和 ratio 方差通常越大。

### Expert Parallelism

MoE 中把专家分布到不同设备上。降低单卡参数压力，但引入 token dispatch、all-to-all 和 load balance 问题。

### OPD

On-Policy Distillation。student 在自己的状态分布上生成轨迹，由 teacher 提供监督，兼具 on-policy 状态对齐和 dense teacher signal。

## 边界与风险：这份清单不能替代真实训练经验

**最重要的边界：**这 35 题没有唯一标准答案。很多问题必须先限定任务、模型、硬件和框架。直接背诵“GRPO 怎么算”“DAPO 有四点改进”“slime 用 SGLang”只能覆盖表层；真正面试会追问为什么、什么时候失效、你会如何监控和调参。

- **Data 没被纳入：**原文明确排除了 Data 题，但现实中数据构造、prompt curriculum、verifier 覆盖、环境质量往往决定 RL 上限。
- **算法名变化很快：**2026 年 RL 后训练论文和框架迭代极快，方法名不是重点，背后的偏差-方差-吞吐-一致性 trade-off 才是重点。
- **部分系统细节依赖实现：**同样叫 GRPO，不同框架在 loss aggregation、KL 处理、old logprob、dynamic filtering、sequence packing 上可能不同。
- **公开资料不足以还原闭源系统：**涉及 DeepSeek、MiniMax、GLM、商业训练平台时，只能依据公开报告抽象方向，不能把推测当事实。

## 工程 / 研究启发：如何用这份清单准备和自测

### 1. 用“一条训练链路”串起所有题

不要按题号死记。把每个问题放回 rollout → reward → advantage → ratio/clip/KL → backprop → weight sync → next rollout 的链路中。你会发现：算法题和 infra 题其实在问同一个系统的不同截面。

### 2. 每个新算法都按六格表拆解

| 拆解维度 | 应该回答的问题 |
|----|----|
| Baseline / Advantage | 它如何降低方差？是否引入 prompt、length、task scale 偏置？ |
| Ratio / KL | 它如何处理 old/current policy mismatch？是否依赖 logprob 一致性？ |
| Clip / Trust Region | 它是 hard mask、soft gate、clip weight 还是 divergence constraint？ |
| Sampling | 是否需要多样本、dynamic sampling、过滤全对/全错或额外 verifier？ |
| Loss Aggregation | 按 token、sequence、prompt 还是 batch 聚合？会不会改变长度和难度权重？ |
| System Cost | 需要额外模型、更多 rollout、更复杂 buffer、异步 correction 或特殊 serving 吗？ |

### 3. 面试回答先给场景，再给方案

例如被问“是否需要 KL”，不要直接说需要或不需要。先区分：如果是偏好 reward model，KL anchor 很重要；如果是强 verifier 的数学 RLVR，KL 可以很小；如果是开放式 agent 任务，KL、格式约束、安全约束和 process reward 可能都需要。能主动限定前提，是高级候选人与背题候选人的区别。

### 4. 自测标准

- 能否手推 REINFORCE baseline 为什么不引入 bias？
- 能否解释 PPO clip 在正/负 advantage 下分别 mask 什么？
- 能否说清 GRPO 为什么省显存，也为什么多耗 rollout？
- 能否解释 std normalization 什么时候有害？
- 能否说明 DAPO dynamic sampling 对框架有什么要求？
- 能否解释 old logprob 为什么不能随便重算？
- 能否画出 actor、rollout、reference、critic、reward 的显存角色？
- 能否说明 continuous batching 为什么会影响 RL 确定性？
- 能否解释 staleness 如何进入 importance ratio？
- 能否根据任务选择 VeRL、AReaL、slime 或 TRL？

## 证据边界与资料索引

本文以公开的 X Article 与知乎中文原文为主线，结合公开的 RL for LLMs 算法综述、AReaL 文档和 agentic RL infra 讨论材料进行解释。本文目标是把问题清单转写成读者可学习的知识地图，不提供唯一参考答案；涉及闭源系统和未来版本的部分仅抽象公开材料中可验证的方向，不推断未公开实现。

- [RL Interview Questions 2026 — X Article by sheriyuo](https://x.com/sheriyuo/status/2063295181131247674)
- [2026 年 RL 方向面经合集 — 知乎中文原文](https://zhuanlan.zhihu.com/p/2046740446353811230)
- [AReaL Documentation: PPO, GRPO, and Related Algorithms](https://areal-project.github.io/AReaL/en/algorithms/grpo_series.html)
- [State of RL for reasoning LLMs](https://aweers.de/blog/2026/rl-for-llms/)
- [RL Infra for Large-Scale Agentic Training](https://blog.guanghan.ai/post/260208_rl_infra/)
- [A Survey of On-Policy Distillation for Large Language Models](https://arxiv.org/html/2604.00626v3)
- [Post-Training is About States, Not Tokens: A State Distribution View of SFT, RL, and On-Policy Distillation](https://arxiv.org/html/2605.22731)
