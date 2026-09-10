<!-- 从 deepseek-exam-lead.html 迁移的资料快照；原始 HTML SHA-256: 4bab033f6b5dd45550a1c7d809019b695c2e46d58a3560cfbd837fa237cf7a05。 -->

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=) ![头像](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/648015371)

[RockyDing](/users/648015371) [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/648015371)

08-02 17:32 北京科技大学 算法工程师 发布于浙江

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIGFyaWEtaGlkZGVuPSJ0cnVlIiBkYXRhLXYtNzliYTY5ZWE+PC9zdmc+) 关注

已关注 取消关注

# 2026-07-26_DeepSeek_大模型算法岗笔试面经分享（含完整答案）

# 写在前面

![alt](https://uploadfiles.nowcoder.com/images/20260601/648015371_1780313982213/D2B5CA33BD970F64A6301FA75AE2EB22#pic_center)

> 【WeThinkIn出品】栏目专注于分享Rocky的认知思考与经验感悟，范围涵盖但不限于AI行业。

> 干货AIGC、AI Agent、LLM算法工程师/开发工程师面试面经秘籍分享（持续更新）：[WeThinkIn/AIGC-Interview-Book](https://gw-c.nowcoder.com/api/sparta/jump/link?link=https%3A%2F%2Fgithub.com%2FWeThinkIn%2FAIGC-Interview-Book)欢迎大家Star～

大家好，我是Rocky。

## 大模型算法岗笔试

### 题目一：手写完整的Multi-Head Attention，不能只写框架

**回答：**

这道题不能只写四个线性层，完整回答至少要把张量形状、缩放点积、掩码语义、数值稳定性和输出投影讲清楚。

设输入为 ![](https://www.nowcoder.com/equation?tex=X%5Cin%5Cmathbb%7BR%7D%5E%7BB%5Ctimes%20S%5Ctimes%20d_%7Bmodel%7D%7D&preview=true)，头数为 ![](https://www.nowcoder.com/equation?tex=H&preview=true)，则每个头的维度为 ![](https://www.nowcoder.com/equation?tex=d_h%3Dd_%7Bmodel%7D%2FH&preview=true)。先做三组线性投影：

![](https://www.nowcoder.com/equation?tex=Q%3DXW_Q%2C%5Cquad%20K%3DXW_K%2C%5Cquad%20V%3DXW_V&preview=true)

其中 ![](https://www.nowcoder.com/equation?tex=Q%2CK%2CV&preview=true) 的形状都是 ![](https://www.nowcoder.com/equation?tex=%5BB%2CS%2Cd_%7Bmodel%7D%5D&preview=true)。将最后一维拆成多头并交换维度后，形状变为 ![](https://www.nowcoder.com/equation?tex=%5BB%2CH%2CS%2Cd_h%5D&preview=true)。每个头的注意力为：

![](https://www.nowcoder.com/equation?tex=A%3D%5Coperatorname%7Bsoftmax%7D%5Cleft(%5Cfrac%7BQK%5E%7B%5Cmathsf%20T%7D%7D%7B%5Csqrt%7Bd_h%7D%7D%2BM%5Cright)%2C%5Cqquad%0AO%3DAV&preview=true)

最后把 ![](https://www.nowcoder.com/equation?tex=H&preview=true) 个头拼回 ![](https://www.nowcoder.com/equation?tex=%5BB%2CS%2Cd_%7Bmodel%7D%5D&preview=true)，再经过 ![](https://www.nowcoder.com/equation?tex=W_O&preview=true) 得到输出。除以 ![](https://www.nowcoder.com/equation?tex=%5Csqrt%7Bd_h%7D&preview=true) 是为了控制点积方差，避免 logits 随维度增大而使 Softmax 饱和、梯度变小。

一个可以现场运行的简化实现如下。这里约定布尔 `attn_mask=True` 表示允许关注，形状可以是 `[B, 1, Q, K]` 或可广播到该形状的张量：

``` prettyprint
import math
import torch
from torch import nn


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model: int, num_heads: int, dropout: float = 0.0):
        super().__init__()
        if d_model % num_heads != 0:
            raise ValueError("d_model must be divisible by num_heads")
        self.d_model = d_model
        self.num_heads = num_heads
        self.head_dim = d_model // num_heads
        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)
        self.out_proj = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, attn_mask=None, is_causal=False):
        bsz, seq_len, _ = x.shape
        q = self.q_proj(x).view(bsz, seq_len, self.num_heads, self.head_dim)
        k = self.k_proj(x).view(bsz, seq_len, self.num_heads, self.head_dim)
        v = self.v_proj(x).view(bsz, seq_len, self.num_heads, self.head_dim)
        q = q.transpose(1, 2)  # [B, H, S, Dh]
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)

        scores = q @ k.transpose(-2, -1) / math.sqrt(self.head_dim)
        if is_causal:
            causal = torch.tril(
                torch.ones(seq_len, seq_len, dtype=torch.bool, device=x.device)
            )
            scores = scores.masked_fill(~causal, torch.finfo(scores.dtype).min)
        if attn_mask is not None:
            scores = scores.masked_fill(~attn_mask, torch.finfo(scores.dtype).min)

        weights = torch.softmax(scores.float(), dim=-1).to(scores.dtype)
        weights = self.dropout(weights)
        out = weights @ v
        out = out.transpose(1, 2).contiguous().view(bsz, seq_len, self.d_model)
        return self.out_proj(out)
```

需要主动说明几个边界。第一，`view` 只能在内存布局满足条件时安全使用，合并转置后的头通常要先 `contiguous()`；第二，因果 Mask 与 Padding Mask 的形状和广播规则不能混为一谈；第三，Cross-Attention 时 ![](https://www.nowcoder.com/equation?tex=Q&preview=true) 的长度可以与 ![](https://www.nowcoder.com/equation?tex=K%2CV&preview=true) 不同，不能把所有序列长度写死为 ![](https://www.nowcoder.com/equation?tex=S&preview=true)。在现代大模型中还可能使用 GQA/MQA、RoPE、FlashAttention 或 fused kernel，但这些是对 QKV 组织和内核的优化，不改变上述注意力的数学骨架。

### 题目二：DPO的完整训练流程推导，从数据准备到梯度更新

**回答：**

DPO 的关键不是“把语言模型直接当成奖励模型”，而是从 KL 约束下的最优策略形式中消去显式奖励模型，得到只依赖偏好对数概率的目标。

训练数据是一组三元组 ![](https://www.nowcoder.com/equation?tex=(x%2Cy_w%2Cy_l)&preview=true)：![](https://www.nowcoder.com/equation?tex=x&preview=true) 是提示，![](https://www.nowcoder.com/equation?tex=y_w&preview=true) 是偏好回答，![](https://www.nowcoder.com/equation?tex=y_l&preview=true) 是非偏好回答。参考模型 ![](https://www.nowcoder.com/equation?tex=%5Cpi_%7Bref%7D&preview=true) 通常是冻结的 SFT 模型，待训练策略是 ![](https://www.nowcoder.com/equation?tex=%5Cpi_%5Ctheta&preview=true)。

从 KL 正则化的 RLHF 目标出发：

![](https://www.nowcoder.com/equation?tex=%5Cmax_%5Cpi%5C%3B%5Cmathbb%7BE%7D_%7By%5Csim%5Cpi(%5Ccdot%7Cx)%7D%5Br(x%2Cy)%5D%0A-%5Cbeta%20D_%7BKL%7D%5Cleft(%5Cpi(%5Ccdot%7Cx)%5Cmiddle%5C%7C%5Cpi_%7Bref%7D(%5Ccdot%7Cx)%5Cright)&preview=true)

其最优策略满足：

![](https://www.nowcoder.com/equation?tex=%5Cpi%5E*(y%7Cx)%3D%5Cfrac%7B1%7D%7BZ(x)%7D%5Cpi_%7Bref%7D(y%7Cx)%5Cexp%5Cleft(%5Cfrac%7Br(x%2Cy)%7D%7B%5Cbeta%7D%5Cright)&preview=true)

于是隐式奖励可以写成：

![](https://www.nowcoder.com/equation?tex=r(x%2Cy)%3D%5Cbeta%5Clog%5Cfrac%7B%5Cpi%5E*(y%7Cx)%7D%7B%5Cpi_%7Bref%7D(y%7Cx)%7D%2B%5Cbeta%5Clog%20Z(x)&preview=true)

偏好数据常用 Bradley-Terry 模型：

![](https://www.nowcoder.com/equation?tex=P(y_w%5Csucc%20y_l%7Cx)%3D%5Csigma%5Cleft(r(x%2Cy_w)-r(x%2Cy_l)%5Cright)&preview=true)

两个回答的 ![](https://www.nowcoder.com/equation?tex=%5Cbeta%5Clog%20Z(x)&preview=true) 会相互抵消，把 ![](https://www.nowcoder.com/equation?tex=%5Cpi%5E*&preview=true) 用待训练策略近似，就得到 DPO 损失：

![](https://www.nowcoder.com/equation?tex=%5Cmathcal%7BL%7D_%7BDPO%7D(%5Ctheta)%3D-%5Clog%5Csigma%5Cleft(%5Cbeta%5Cleft%5B%0A%5Clog%5Cfrac%7B%5Cpi_%5Ctheta(y_w%7Cx)%7D%7B%5Cpi_%7Bref%7D(y_w%7Cx)%7D%0A-%5Clog%5Cfrac%7B%5Cpi_%5Ctheta(y_l%7Cx)%7D%7B%5Cpi_%7Bref%7D(y_l%7Cx)%7D%0A%5Cright%5D%5Cright)&preview=true)

其中序列对数概率是回答 token 条件概率之和：

![](https://www.nowcoder.com/equation?tex=%5Clog%5Cpi(y%7Cx)%3D%5Csum_%7Bt%5Cin%5Ctext%7Bcompletion%7D%7D%5Clog%5Cpi(y_t%7Cx%2Cy_%7B%3Ct%7D)&preview=true)

实际训练流程如下：

1.  清洗偏好对，确认 chosen/rejected 的 prompt 一致，处理重复、长度异常和标签噪声。
2.  用策略模型和冻结参考模型分别对 chosen、rejected 做 teacher forcing，只对 completion 部分累加 log-prob，不能把 prompt 和 padding 算进去。
3.  按上式计算 log-ratio、margin 和损失；只对策略模型反向传播，参考模型不更新。
4.  使用 AdamW、学习率和 ![](https://www.nowcoder.com/equation?tex=%5Cbeta&preview=true) 等超参数更新策略模型；实践中常从 SFT 模型开始，并监控 KL 漂移、偏好准确率、长度偏差和通用能力。
5.  用独立偏好集、事实性集和安全集评测，不能只看训练损失。

令括号内的量为 ![](https://www.nowcoder.com/equation?tex=z&preview=true)，梯度方向可写为 ![](https://www.nowcoder.com/equation?tex=-%5Cbeta%5Csigma(-z)%5Cnabla%20z&preview=true)：当策略模型还没有把 chosen 与 rejected 拉开时，梯度大；margin 已经很大时，样本梯度自然变小。DPO 不需要在线 rollout、单独 Reward Model 或 PPO，但它依然依赖高质量偏好数据和合理参考模型。长回答的 log-prob 还可能带来长度偏置，因此要关注长度归一化、数据配比以及 IPO、KTO、ORPO 等相邻方法的适用边界，不能把 DPO 当成对所有偏好学习问题的唯一答案。

### 题目三：MOE模型的通信开销计算和负载不均衡问题分析

**回答：**

MoE 的计算量与通信量要分开分析。设一个并行批次有 ![](https://www.nowcoder.com/equation?tex=T&preview=true) 个 token，隐藏维度为 ![](https://www.nowcoder.com/equation?tex=d&preview=true)，每个 token 选择 ![](https://www.nowcoder.com/equation?tex=k&preview=true) 个专家，专家数为 ![](https://www.nowcoder.com/equation?tex=E&preview=true)，专家并行组大小为 ![](https://www.nowcoder.com/equation?tex=P&preview=true)，每个激活值使用 ![](https://www.nowcoder.com/equation?tex=b&preview=true) 字节。

路由器先为每个 token 计算专家分数并选出 Top-![](https://www.nowcoder.com/equation?tex=k&preview=true)。在 Expert Parallel 中，token 的激活需要通过 All-to-All Dispatch 发到拥有目标专家的设备；专家计算后再通过 All-to-All Combine 将结果送回原 token 所在设备。若负载均匀、每台设备本地命中比例约为 ![](https://www.nowcoder.com/equation?tex=1%2FP&preview=true)，网络上的有效激活载荷可近似写为：

![](https://www.nowcoder.com/equation?tex=V_%7Bone-way%7D%5Capprox%20Tkd%20b%5Cleft(1-%5Cfrac%7B1%7D%7BP%7D%5Cright)&preview=true)

两次交换的总载荷约为：

![](https://www.nowcoder.com/equation?tex=V_%7Bcomm%7D%5Capprox%202Tkd%20b%5Cleft(1-%5Cfrac%7B1%7D%7BP%7D%5Cright)&preview=true)

这是粗略的聚合估计；实际还要加上路由索引、padding、元数据、协议头以及拓扑带来的非均匀开销。用延迟带宽模型表达单次通信时间：

![](https://www.nowcoder.com/equation?tex=T_%7Bcomm%7D%5Capprox%20%5Calpha%20N_%7Bcollective%7D%2B%5Cfrac%7BV_%7Bcomm%7D%7D%7BBW_%7Beff%7D%7D&preview=true)

其中 ![](https://www.nowcoder.com/equation?tex=%5Calpha&preview=true) 是集体通信启动延迟，![](https://www.nowcoder.com/equation?tex=BW_%7Beff%7D&preview=true) 是受 PCIe、NVLink、RoCE、拥塞和消息大小共同影响的有效带宽。小 batch 时延迟项突出，大 batch 时带宽和负载倾斜更关键。

计算侧，每个专家接收的 token 数约为 ![](https://www.nowcoder.com/equation?tex=Tk%2FE&preview=true)，若专家是标准两层 FFN，单 token 的矩阵乘开销大致与 ![](https://www.nowcoder.com/equation?tex=d%5Ctimes%20d_%7Bff%7D&preview=true) 成正比；因此 MoE 通过只激活少数专家降低每 token 的计算量，但并不免费：路由、All-to-All、专家权重驻留和负载倾斜会吞掉收益。比如总参数很大而激活参数较小，只能说明稀疏计算特征，不能直接推出端到端吞吐。

负载不均衡要同时看三件事：专家接收 token 数的均值和最大值、负载变异系数 `std(load)/mean(load)`，以及因为 capacity 溢出被丢弃或重路由的 token 比例。常见 capacity 为：

![](https://www.nowcoder.com/equation?tex=C%3D%5Cleft%5Clceil%20%5Cfrac%7Bc%5C%2CTk%7D%7BE%7D%5Cright%5Crceil&preview=true)

其中 ![](https://www.nowcoder.com/equation?tex=c&preview=true) 是 capacity factor。![](https://www.nowcoder.com/equation?tex=c&preview=true) 太小会丢 token，太大则浪费显存和通信；实际需按序列长度、batch、Top-![](https://www.nowcoder.com/equation?tex=k&preview=true) 和目标丢弃率调参。

造成倾斜的原因包括路由器偏置、热门 token、领域分布变化、专家容量不足和跨节点拓扑差异。可用辅助负载均衡损失、专家偏置控制、容量约束、随机路由、动态 batching 以及拓扑感知放置缓解。回答时还要区分“训练时路由均衡”和“推理时服务均衡”：后者除了 token 数，还要考虑专家所在设备的真实排队时间和通信路径。

### 题目四：推理加速的底层实现（vLLM的PagedAttention原理、投机解码的工程实现）

**回答：**

这道题应拆成两部分：PagedAttention 解决 KV Cache 的内存管理和批处理问题；投机解码通过较便宜的草稿预测减少目标模型的串行迭代次数。两者可以结合，但不是同一个算法。

### PagedAttention

标准自回归解码中，每条请求的 KV Cache 随序列长度增长。如果为每条请求预留一段连续显存，长短请求交错会产生内部碎片，动态扩容和请求结束后的回收也很困难。PagedAttention 把 KV Cache 切成固定大小的 block：

- 逻辑序列按 token 位置映射到逻辑 block；
- block table 将逻辑 block 映射到不连续的物理显存 block；
- 新 token 到来时只分配需要的 page，结束时按引用计数回收；
- 共享前缀可以让多个请求指向相同物理 block，写入时再做 Copy-on-Write。

Attention 内核按照 block table 分页读取 K、V，并完成分块归约。这样做的本质是把“连续大数组”变成操作系统式的分页地址空间，显著降低碎片、提高并发请求的显存利用率，并支持 continuous batching 和 prefix caching。它不改变注意力的理论复杂度，也不会凭空减少每个 token 的 KV 字节数；速度收益来自更高的可服务并发、较少的内存浪费和更好的调度。

### 投机解码

给定已经确认的前缀，草稿模型先自回归生成 ![](https://www.nowcoder.com/equation?tex=%5Cgamma&preview=true) 个候选 token；目标模型随后一次前向并行验证这些位置。贪心解码可以逐位置接受与目标模型一致的前缀；随机采样若要严格保持目标分布，需要使用基于目标分布与草稿分布的 rejection sampling，并在拒绝位置进行修正采样。若所有候选都接受，还可以额外接收目标模型给出的下一个 token。

设每个候选位置在此前位置均被接受的条件下的生存概率为 ![](https://www.nowcoder.com/equation?tex=p_i&preview=true)，则期望接受长度可近似写为：

![](https://www.nowcoder.com/equation?tex=%5Cmathbb%7BE%7D%5BL%5D%5Capprox%5Csum_%7Bj%3D1%7D%5E%7B%5Cgamma%7D%5Cprod_%7Bi%3D1%7D%5E%7Bj%7Dp_i&preview=true)

一次迭代的收益不是只看 ![](https://www.nowcoder.com/equation?tex=%5Cmathbb%7BE%7D%5BL%5D&preview=true)，还要除以草稿生成、目标验证、KV 读写和调度的总时间：

![](https://www.nowcoder.com/equation?tex=%5Ctext%7Bspeedup%7D%5Capprox%0A%5Cfrac%7B%5Ctext%7Bbaseline%20target%20steps%20time%7D%7D%0A%7BT_%7Bdraft%7D(%5Cgamma)%2BT_%7Bverify%7D(%5Cgamma)%2BT_%7Bschedule%7D%7D%0A%5Ctimes%20(1%2B%5Cmathbb%7BE%7D%5BL%5D)&preview=true)

这是直觉化表达，真正评测应直接测端到端 ITL、TPOT、吞吐和请求尾延迟。

工程实现的难点包括：草稿模型与目标模型 tokenizer/位置编码兼容；验证阶段正确复用和回滚 paged KV；接受长度变化时避免无效显存写入；连续 batching 下不同请求的候选长度不同；低接受率时及时退化为普通解码；以及在量化、张量并行和 prefix cache 下保持数值与调度正确。现代实现还可能使用 n-gram、EAGLE、Medusa 或半自回归草稿器，但核心判断始终是“草稿成本是否小于它节省的目标模型串行步数”。

### 题目五：DSpark推理加速框架的核心机制推导

**回答：**

DSpark 这类方法可以按“更强的草稿器 + 接受率感知的验证调度”来理解。题目中给出的版本名和基准数字应以对应正式论文、代码和硬件配置为准；面试回答的重点是把机制和可计算的收益说清楚。

传统自回归草稿器逐 token 生成，候选长度为 ![](https://www.nowcoder.com/equation?tex=%5Cgamma&preview=true) 时草稿成本近似随 ![](https://www.nowcoder.com/equation?tex=%5Cgamma&preview=true) 增长；完全并行的草稿器虽然一次预测多个位置，却缺少块内前缀依赖，后面位置的接受率容易下降。半自回归设计通常将两者折中：并行主干先产生各位置的候选表示，再由轻量顺序模块注入前缀依赖。顺序模块可以是只依赖前一位置的 Markov head，也可以通过循环状态累积更长前缀信息。

对每个候选位置，草稿器不仅输出 token，还输出一个接受置信度 ![](https://www.nowcoder.com/equation?tex=p_i&preview=true)。它应表示在前面候选已经被目标模型接受的条件下，该位置继续被接受的概率，而不是未经校准的 softmax 最大值。可以用独立验证集做逐位置温度缩放或其他校准，使预测置信度与经验接受率一致。

若一次最多验证 ![](https://www.nowcoder.com/equation?tex=%5Cgamma&preview=true) 个 token，接受长度的近似期望为：

![](https://www.nowcoder.com/equation?tex=%5Cmathbb%7BE%7D%5BL(%5Cgamma)%5D%5Capprox%5Csum_%7Bj%3D1%7D%5E%7B%5Cgamma%7D%5Cprod_%7Bi%3D1%7D%5E%7Bj%7Dp_i&preview=true)

在并发服务中，验证长度还受目标模型 batch、KV Cache、SM 利用率和通信路径影响。因此调度器不是对每个请求独立选择一个固定 ![](https://www.nowcoder.com/equation?tex=%5Cgamma&preview=true)，而是根据当前 batch 的置信度序列和实测吞吐曲线，近似求解：

![](https://www.nowcoder.com/equation?tex=%5Cmax_%7B%5Cgamma_1%2C%5Cldots%2C%5Cgamma_N%7D%0A%5Cfrac%7B%5Csum_%7Br%3D1%7D%5E%7BN%7D%5Cleft(1%2B%5Cmathbb%7BE%7D%5BL_r(%5Cgamma_r)%5D%5Cright)%7D%0A%7BT_%7Bverify%7D(%5Cgamma_1%2C%5Cldots%2C%5Cgamma_N)%2BT_%7Bdraft%7D%2BT_%7Boverhead%7D%7D&preview=true)

因此“置信度调度”真正优化的是单位时间确认 token 数，而不是盲目把候选块做长。结构化代码和数学文本往往具有更强的局部可预测性，接受率可能高于开放式对话，但这只是数据分布现象，不能当成所有任务的保证。

要讲清正确性边界：只要最终由目标模型验证，并在随机采样场景使用正确的拒绝采样修正，草稿器可以是近似的，目标分布仍可保持；置信度调度只影响效率，不应改变目标模型的输出分布。工程上还要做接受长度、草稿开销、ITL、吞吐、P99 延迟、显存和不同并发度的联合评测。只有在这些指标上稳定胜出，才算真正的推理加速，而不是单用户生成速度的局部提升。

### 题目六：DeepSeek-V4的KV缓存压缩原理与内存占用计算

**回答：**

KV Cache 的内存占用首先由层数、KV 头数、头维度、序列长度、批量和精度决定，与模型总参数量不是一回事。

标准 MHA 中，若 decoder 层数为 ![](https://www.nowcoder.com/equation?tex=L&preview=true)，每层 KV 头数为 ![](https://www.nowcoder.com/equation?tex=H_%7Bkv%7D&preview=true)，每头维度为 ![](https://www.nowcoder.com/equation?tex=d_h&preview=true)，上下文长度为 ![](https://www.nowcoder.com/equation?tex=T&preview=true)，batch 为 ![](https://www.nowcoder.com/equation?tex=B&preview=true)，每个元素占 ![](https://www.nowcoder.com/equation?tex=b&preview=true) 字节，则：

![](https://www.nowcoder.com/equation?tex=M_%7BKV%7D%3DB%5Ctimes%20T%5Ctimes%20L%5Ctimes%20H_%7Bkv%7D%5Ctimes%20d_h%5Ctimes%202%5Ctimes%20b&preview=true)

最后的 ![](https://www.nowcoder.com/equation?tex=2&preview=true) 对应 K 和 V。GQA/MQA 通过降低 ![](https://www.nowcoder.com/equation?tex=H_%7Bkv%7D&preview=true) 减少 Cache；量化通过降低 ![](https://www.nowcoder.com/equation?tex=b&preview=true) 减少字节数，但会引入误差。

以压缩 latent KV 为例，如果每个 token 每层只缓存一个维度为 ![](https://www.nowcoder.com/equation?tex=d_c&preview=true) 的共享 latent，并额外保留维度为 ![](https://www.nowcoder.com/equation?tex=d_r&preview=true) 的解耦位置编码 Key，则可近似写为：

![](https://www.nowcoder.com/equation?tex=M_%7Bcompressed%7D%5Capprox%20B%5Ctimes%20T%5Ctimes%20L%5Ctimes(d_c%2Bd_r)%5Ctimes%20b&preview=true)

解码时由 latent 经过投影恢复部分 K/V，计算换来的收益是显存和带宽下降，代价是额外矩阵乘、访问模式变化、量化/重建误差和实现复杂度。若使用分组量化，还要额外计入 scale、zero-point 等元数据；若采用分层或混合精度，不能用一个统一压缩比代替真实的逐层统计。

举例说，若某配置为 ![](https://www.nowcoder.com/equation?tex=L%3D80&preview=true)、![](https://www.nowcoder.com/equation?tex=H_%7Bkv%7D%3D8&preview=true)、![](https://www.nowcoder.com/equation?tex=d_h%3D128&preview=true)、![](https://www.nowcoder.com/equation?tex=T%3D10%5E6&preview=true)、FP16、batch 为 1，则标准 MHA 的 KV 字节数为：

![](https://www.nowcoder.com/equation?tex=80%5Ctimes10%5E6%5Ctimes8%5Ctimes128%5Ctimes2%5Ctimes2%0A%3D327.68%5Ctimes10%5E9%5Ctext%7B%20bytes%7D%0A%5Capprox305.2%5Ctext%7B%20GiB%7D&preview=true)

这个例子只用于说明量级，不能套用到其他模型。要从一个宣称的 GB 数字反推压缩率，必须知道实际层数、KV 维度、缓存精度、是否分页、是否把临时 workspace 和权重算入显存，以及 GB 还是 GiB。仅凭“模型有多少参数”无法推出 KV Cache 大小，也不能据此证明某种压缩结构。

所以这道题的严谨答法是：先写标准公式，再写 MLA/GQA/量化等压缩如何改变公式，最后从显存、带宽、重建 FLOPs 和质量损失做联合预算。任何具体版本号、参数规模或单卡数字，都应以公开模型配置和可复现实验为准，不能把未经配置支撑的数字当作理论推导结论。

### 题目七：多模态视觉原语推理框架的数学建模

**回答：**

视觉原语的核心是把空间参照从模糊的自然语言描述提升为模型可以生成、比较和验证的几何对象。可以把文本 token 与视觉原语统一成一个混合序列建模问题。

给定图像 ![](https://www.nowcoder.com/equation?tex=I&preview=true)、用户文本 ![](https://www.nowcoder.com/equation?tex=x&preview=true)，定义视觉原语集合：

![](https://www.nowcoder.com/equation?tex=%5Cmathcal%7BP%7D%3D%5C%7B%5Ctext%7Bpoint%7D(u%2Cv)%2C%5Ctext%7Bbox%7D(u_1%2Cv_1%2Cu_2%2Cv_2)%2C%0A%5Ctext%7Bmask%7D%2C%5Ctext%7Bpolygon%7D%2C%5Cldots%5C%7D%2C&preview=true)

其中坐标通常归一化到 ![](https://www.nowcoder.com/equation?tex=%5B0%2C1%5D&preview=true)，并约束 ![](https://www.nowcoder.com/equation?tex=u_1%5Cle%20u_2&preview=true)、![](https://www.nowcoder.com/equation?tex=v_1%5Cle%20v_2&preview=true)。令输出空间为文本 token 空间 ![](https://www.nowcoder.com/equation?tex=%5Cmathcal%7BV%7D&preview=true) 与原语空间 ![](https://www.nowcoder.com/equation?tex=%5Cmathcal%7BP%7D&preview=true) 的并集，模型生成混合序列 ![](https://www.nowcoder.com/equation?tex=z%3D(z_1%2C%5Cldots%2Cz_n)&preview=true)：

![](https://www.nowcoder.com/equation?tex=p(z%7CI%2Cx)%3D%5Cprod_%7Bt%3D1%7D%5E%7Bn%7Dp(z_t%7CI%2Cx%2Cz_%7B%3Ct%7D)&preview=true)

实际实现可以将原语离散化为特殊 token 加坐标 bin，例如 `[BOX, x1, y1, x2, y2]`；也可以让模型输出连续坐标分布或调用专门的 grounding head。一个通用的训练目标可以写成：

![](https://www.nowcoder.com/equation?tex=%5Cmathcal%7BL%7D%3D%5Cmathcal%7BL%7D_%7Btext%7D%0A%2B%5Clambda_%7Bcoord%7D%5Cmathcal%7BL%7D_%7Bcoord%7D%0A%2B%5Clambda_%7Bgeom%7D%5Cmathcal%7BL%7D_%7Bgeom%7D%0A%2B%5Clambda_%7Bground%7D%5Cmathcal%7BL%7D_%7Bground%7D&preview=true)

其中文本部分使用交叉熵，点/框可用 L1、Smooth L1、IoU/GIoU 损失，grounding 部分约束生成的原语确实指向图像中的目标。若是计数或空间关系任务，还需要任务损失与几何一致性约束。

视觉原语的价值在于让“左上角的红色物体”变成可计算的引用：模型可以生成一个框，再对框内目标分类；也可以比较两个框的中心坐标、IoU、包含关系和相对方向。这比完全依赖语言中的“那个”“附近”“左边”更容易验证。

面试中还要说清三个难点。第一，坐标误差会传播到后续引用，因此需要坐标量化校准、IoU 阈值和不确定性表示；第二，文本 token 与几何 token 的概率空间和损失尺度不同，![](https://www.nowcoder.com/equation?tex=%5Clambda&preview=true) 需要通过验证集校准；第三，视觉原语必须有语法约束和合法性校验，否则可能生成越界、反向框或无法落到图像的坐标。

因此，视觉原语不是简单给多模态模型加几个坐标 token，而是把感知、指代、空间关系和生成动作放进一个可执行的中间表示。它是否带来领先结果，要看数据集、标注质量、坐标编码、grounding 评测和与纯文本 CoT 的公平对比，不能只凭“引入点和框”推出效果。

### 题目八：DeepSeek MoE的无辅助损失负载均衡机制推导

**回答：**

这类“无辅助损失”方案的要点不是取消均衡控制，而是把均衡控制从主损失中的可学习惩罚项，改成路由器外部的专家偏置反馈。

设 token ![](https://www.nowcoder.com/equation?tex=t&preview=true) 对专家 ![](https://www.nowcoder.com/equation?tex=i&preview=true) 的原始路由分数为 ![](https://www.nowcoder.com/equation?tex=s_%7Bt%2Ci%7D&preview=true)，专家偏置为 ![](https://www.nowcoder.com/equation?tex=b_i&preview=true)。路由选择使用：

![](https://www.nowcoder.com/equation?tex=%5Ctilde%7Bs%7D_%7Bt%2Ci%7D%3Ds_%7Bt%2Ci%7D%2Bb_i%2C%0A%5Cqquad%0A%5Cmathcal%7BE%7D_t%3D%5Coperatorname%7BTopK%7D_i(%5Ctilde%7Bs%7D_%7Bt%2Ci%7D%2Ck)&preview=true)

关键实现细节是：偏置用于影响 Top-![](https://www.nowcoder.com/equation?tex=k&preview=true) 的选择，但专家组合权重通常仍使用未加偏置的原始路由分数并做归一化。这样偏置负责纠正“谁被选中”，尽量不直接改变主任务中的混合权重。

在一个统计窗口内，设专家 ![](https://www.nowcoder.com/equation?tex=i&preview=true) 实际接收的 token 数为 ![](https://www.nowcoder.com/equation?tex=c_i&preview=true)，平均负载为 ![](https://www.nowcoder.com/equation?tex=%5Cbar%20c%3D%5Cfrac%7B1%7D%7BE%7D%5Csum_i%20c_i&preview=true)。高负载专家应被降低偏置，低负载专家应被提高偏置。一种离散更新可写成：

![](https://www.nowcoder.com/equation?tex=b_i%5Cleftarrow%20b_i-%5Cgamma%5C%2C%5Coperatorname%7Bsign%7D(c_i-%5Cbar%20c)&preview=true)

也可以用带裁剪的比例反馈：

![](https://www.nowcoder.com/equation?tex=b_i%5Cleftarrow%5Coperatorname%7Bclip%7D%5Cleft(%0Ab_i-%5Cgamma%5Cfrac%7Bc_i-%5Cbar%20c%7D%7B%5Cbar%20c%2B%5Cepsilon%7D%2C%0Ab_%7Bmin%7D%2Cb_%7Bmax%7D%5Cright)&preview=true)

其中 ![](https://www.nowcoder.com/equation?tex=%5Cgamma&preview=true) 控制反馈速度。偏置一般按 batch 或固定 token 窗口更新，而不是对每个 token 更新，否则噪声会使路由剧烈抖动。实践还要考虑专家容量、跨节点通信、局部负载与全局负载不一致，以及偏置版本在分布式设备之间同步。

与辅助损失相比，外部偏置的优势是不会把一个需要调权重的均衡目标直接加入语言建模损失，降低主任务梯度被干扰的风险；它也能在训练早期通过反馈快速纠正热门专家。代价是它引入了一个非梯度控制回路：![](https://www.nowcoder.com/equation?tex=%5Cgamma&preview=true)、更新窗口、偏置上下界和同步延迟都需要调节；统计窗口太短会抖动，太长又响应不及时；只看 token 数还可能掩盖某些专家计算更慢或通信更远的问题。

辅助损失的典型思想是同时惩罚选择频率和平均路由概率的不均衡，例如让各专家的 `load` 与 `importance` 接近均匀；无辅助损失并不等价于“天然均衡”，它仍然要通过实时负载监控和偏置更新实现闭环控制。最后要评估的不是偏置公式本身，而是负载变异系数、token 丢弃率、All-to-All 时间、训练损失、验证效果和下游质量的综合变化。

[![alt](https://uploadfiles.nowcoder.com/images/20230528/648015371_1685272293042/6A6478DBB1D3FB8A247D83B1E792F373)](https://gw-c.nowcoder.com/api/sparta/jump/link?link=https%3A%2F%2Fwww.nowcoder.com%2Fusers%2F648015371)

[\#校招#](/creation/subject/d09b966a380b45ddaba9dc5a6bd5ee19)[\#春招#](/creation/subject/9aea3762a04c49bfb6da8d3f4705c354)[\#秋招#](/creation/subject/002d6ce4eab1487f9cae3241b5322732)[\#面经#](/creation/subject/928d551be73f40db82c0ed83286c8783)[\#实习#](/creation/subject/7ed2b413c8e64f9da9e460af91f577de)

提示

订阅专刊

全部评论

推荐最新楼层

[![头像](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/6402022)

[AIGC小白入门记](/users/6402022) [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/6402022)

浙江大学 算法工程师

大佬，抄袭内容【eepSeek大模型算法岗，笔试直接给我整不会了 ！！！】https://www.nowcoder.com/discuss/911019469990821888，不好吧？？？还没有在前面加引用？？

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)2 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)回复 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

[发布于 08-03 15:53](/discuss/comment/22816666) 北京

[![头像](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/651404281)

[贪吃的Mini大白菜](/users/651404281) [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/651404281)

北京理工大学 算法工程师

蹲蹲代码

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)回复 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

[发布于 08-19 14:51](/discuss/comment/22846994) 广东

![](https://static.nowcoder.com/fe/file/oss/1681101031872EGDPQ.png)

暂无评论，快来抢首评~

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

相关推荐

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/757611414)

09-03 09:27

[北京航空航天大学 嵌入式软件工程师](/users/757611414)

[想进大厂得学到啥程度](/discuss/924956628623818752?sourceSSR=post)

[](/discuss/924956628623818752?sourceSSR=post)

2024&nbsp;届本科上岸，目前在上海张江某原厂写&nbsp;BSP，裸机、RTOS、Linux&nbsp;内核都碰，年包税前&nbsp;45w&nbsp;base。在这一行不算多猛，但摸爬滚打这一年多，多少有点东西可以聊。背景前情学校是某&nbsp;985&nbsp;的异地校区，大一大二参加过一些嵌入式比赛，成绩一般般，主要是给简历凑点东西。那段时间我心思其实在&nbsp;C++&nbsp;上，一直琢磨着转互联网。大三才意识到该找实习了，套了个模板把简历填完，海投几天捞了几个&nbsp;offer，最后去了北京某&nbsp;RISC-V&nbsp;厂，虽然进去之后做的还是&nbsp;ARM&nbsp;SoC&nbsp;那套。本来想拿转正，卡在本科学历上没成，刚好赶上九月，干脆回学校冲秋招。那时候手里已经有几个&nbsp;offer&nbsp;兜底，心态没...

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/643998076)

今天 19:21

已编辑

[门头沟学院 Java](/users/643998076)

[小红书Agent服务端开发实习一面（已挂）](/discuss/926917172448759808?sourceSSR=post)

[](/discuss/926917172448759808?sourceSSR=post)

9.8&nbsp;面的，没怎么准备就去面了，呜呜呜1.&nbsp;自我介绍2.&nbsp;询问团队人数3.&nbsp;询问现在能否正常去实习4.&nbsp;拷打实习5.&nbsp;拷打项目&nbsp;1）&nbsp;sse&nbsp;和&nbsp;streamable-http&nbsp;的区别&nbsp;2）&nbsp;如何适配&nbsp;stdio、HTTP、SSE、Streamable&nbsp;HTTP&nbsp;的？&nbsp;&nbsp;3）&nbsp;如何处理&nbsp;MCP&nbsp;版本兼容问题？6.&nbsp;场景题&nbsp;对于像&nbsp;ChatGPT&nbsp;这种对话&nbsp;Agent，你会怎么设计会话表和消息表的字段？7.&nbsp;手撕：最长递增子序列8.&nbsp;反问阶段#小红书##Agent面经##面经##实习##牛客AI配图神器#

![](https://static.nowcoder.com/fe/file/oss/1715049343797JOCFB.png)查看9道真题和解析

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/523764268)

09-01 13:55

[广东工业大学 前端工程师](/users/523764268)

[字节oc！](/feed/main/detail/9864de8c99f0486190a4c6d6bd389a17?sourceSSR=post)

[](/feed/main/detail/9864de8c99f0486190a4c6d6bd389a17?sourceSSR=post)

秋招直接结束

我是猫熊：举报了

[![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=) 27暑期实习转正](/creation/subject/a0dd49089a404b13894558989c2cf19a?entranceType_var=%E5%86%85%E5%AE%B9%E6%9D%A1%E7%9B%AE)

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/257616219)

09-04 11:04

已编辑

[门头沟学院 后端工程师](/users/257616219)

[字节跳动9.3 Agent开发一面面经](/discuss/925342611194286080?sourceSSR=post)

[](/discuss/925342611194286080?sourceSSR=post)

项目自我介绍请你详细介绍你的AI项目；你的项目中说到了面试评分，那么简历评分的内容是如何进行结构化输出的？从哪几个维度进行评分？项目中的RAG知识用到了哪些？离线上传和在线问答环节如何进行？八股你如何理解Agent中Harness的概念？你的Agent里面运行了一个长程的任务，它假设平时只允许需要运行5分钟就能结束。然后你新运行了一次，它运行了15-20分钟，也就是说跟之前比有明显的延迟，然后你会怎么分析这个延迟是什么导致的？如何解决上述这个问题？Agent在执行过程中，肯定不可避免地要去调用一些工具，这些工具都有固定地入参，需要模型结合上下文去提供，然后在这个过程中，如何去保障工具调用的可靠...

![](https://static.nowcoder.com/fe/file/oss/1715049343797JOCFB.png)查看9道真题和解析

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

一键发评

求面经

举报了

忍耐王

蹲蹲代码

mark收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论

点赞成功，聊一聊 \>

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)5

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)4

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

评论

![]() 提到的真题

返回内容 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

招聘动态

[查看更多 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTIgMTIiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEyIiBoZWlnaHQ9IjEyIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)](/jobs/school/schedule?pageSource=105)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/jump?type=ad&source=105&companyId=1682&url=https%3A%2F%2Fjob.njcb.com.cn%2F%23%2Fcampus&entityId=13360)

南京银行2027届

全球校园招聘

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/jump?type=ad&source=105&companyId=1055&url=https%3A%2F%2Fjobs.mihoyo.com%2F%3FchannelToken%3Dxz2037b7d4-68d44f5a8ebc-0edf28e17574%23%2Fcampus&entityId=13254)

米哈游2027校园招聘

应届生&全年实习生专项

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/jump?type=ad&source=105&companyId=1950&url=https%3A%2F%2Fapp.mokahr.com%2Fsu%2Fzutnfk&entityId=13362)

FunPlus

2027届校园招聘

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/jump?type=ad&source=105&companyId=139&url=https%3A%2F%2Ftalent.baidu.com%2Fjobs%2Flist%3FrecommendCode%3DIZ118K%26recruitType%3DGRADUATE&entityId=13361)

百度

2027届校园招聘启动

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/jump?type=ad&source=105&companyId=2412&url=https%3A%2F%2Fapp.mokahr.com%2Fcampus_apply%2Fleyuansu%2F2357%23%2F&entityId=13248)

乐元素

2027校园招聘

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/jump?type=ad&source=105&companyId=676&url=https%3A%2F%2Fcareers.oppo.com%2Funiversity%2Foppo%2Fcampus%2F&entityId=13263)

OPPO

2027届全球校园招聘

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/jump?type=ad&source=105&companyId=2197&url=https%3A%2F%2Fcampus.pingan.com%2Fpaccbxkjzx&entityId=13334)

平安产险科技中心

2027届校园招聘

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/jump?type=ad&source=105&companyId=294969&url=https%3A%2F%2Fwww.nowcoder.com%2Fjobs%2Fcompany-project%3FprojectId%3D2657%26deliverSource%3D4%26activityId%3D175%26activitySuffix%3D2027QZzc%26pageSource%3D5009%26channel%3Dqzsy&entityId=13345)

Dexmal 原力灵机

2027校园招聘

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/jump?type=ad&source=105&companyId=889&url=https%3A%2F%2Fbsurl.cn%2Fv2%2Fh4ZoqoK0&entityId=13346)

vivo

2027届全球校园招聘

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/jump?type=ad&source=105&companyId=2922&url=https%3A%2F%2Fapp.mokahr.com%2Fsu%2Fyvpovf&entityId=13347)

信也科技

2027届校园招聘

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

## 全站热榜

更多

- [](https://www.nowcoder.com/discuss/926381539087089664)
  1

  ... 实习没转正，怎么快速转战秋招？

  5458

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/f64dea2a6fc941d19e2fecf7eb0ca3a0)
  2

  ... Bigo后端开发一面

  4060

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/925390107392118784)
  3

  ... 秋招er必看之👉

  4051

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/f33655bf738846a7a67d8942dd44e86c)
  4

  ... mentor说我der是什么意思？

  4043

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/9c3afcf6863b49afa2de143e0db6d387)
  5

  ... 全世界最豪的人都在大厂实习生群里。。。

  3565

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926810615115444224)
  6

  ... 美团二面 - Java后端 日常实习

  3349

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926534933789540352)
  7

  ... AI岗三轮面试，分别都在筛什么？？

  2908

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/23d5946ce1d64313b04c64058bd3a49a)
  8

  ... 感觉自己好没用，一被骂就想离职

  2456

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/595474c7b52d43098a8e494eb8d8e258)
  9

  ... 刚刚做AI 面，躺在床上没穿衣服要紧吗

  2351

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/1b3b525a70ee406b93f5f57f37743a05)
  10

  ... 室友，你朋友圈发的大厂周边，是偷的图吧？

  2191

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

## 创作者周榜

更多

正在热议

更多

[](https://www.nowcoder.com/creation/subject/7723c7a27b8540528154e0c22a79559f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招吐槽大会 \#

365152次浏览 1726人参与

[](https://www.nowcoder.com/creation/subject/14710425d5b74593b2ef7103d293606f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招面试记录 \#

663792次浏览 11261人参与

[](https://www.nowcoder.com/creation/subject/aa99cc2283b1424db067e3980fdb866f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 巨人网络2027校招 \#

43249次浏览 313人参与

[](https://www.nowcoder.com/creation/subject/b8fb04662b3e4a3698d028cff4f643f2?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 实习面试记录 \#

252807次浏览 6140人参与

[](https://www.nowcoder.com/creation/subject/2e738281915e405396a5384eed5577a5?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招第一个offer \#

21661次浏览 163人参与

[](https://www.nowcoder.com/creation/subject/8ffd8c3fdee44aa4ba6931bc3ba5f4fd?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 实习简历求拷打 \#

227018次浏览 1065人参与

[](https://www.nowcoder.com/creation/subject/a0c560e49d8a43cb89017f358b7886b1?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 联想27届秋招 \#

29387次浏览 246人参与

[](https://www.nowcoder.com/creation/subject/87d3304709694e179288006dbeccb322?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 得物求职进展汇总 \#

190881次浏览 1069人参与

[](https://www.nowcoder.com/creation/subject/a0351018891e4a26bd6520680f76cd5e?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 小厂一定不能去吗？ \#

123905次浏览 650人参与

[](https://www.nowcoder.com/creation/subject/0506c9a828c2495087eb051b399570bd?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 携程笔试 \#

219939次浏览 1139人参与

[](https://www.nowcoder.com/creation/subject/7bb26296238343b8934333f65e030bed?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 去哪儿求职进展汇总 \#

181274次浏览 1066人参与

[](https://www.nowcoder.com/creation/subject/ed7f666c434b46749c6f0430a2496bb4?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 如果重来一次你还会读研吗 \#

268111次浏览 2155人参与

[](https://www.nowcoder.com/creation/subject/3ba45316f86d4f96aae8bfbd56700b03?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 蔚来工作体验 \#

41796次浏览 96人参与

[](https://www.nowcoder.com/creation/subject/074948bf7b05432a8c63add07b000637?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 蔚来求职进展汇总 \#

138142次浏览 817人参与

[](https://www.nowcoder.com/creation/subject/efefa0916ad64b82b1d41a632ec6fdfb?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 你的秋招第一面感觉怎么样 \#

166562次浏览 886人参与

[](https://www.nowcoder.com/creation/subject/36a7990c7e5c4ba4945c56c4fdc73487?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 你认为小厂实习有用吗？ \#

170765次浏览 859人参与

[](https://www.nowcoder.com/creation/subject/c9ac480935464f57ae5c9e0f4ff3973c?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招的第一个offer，大家都拿到了吗 \#

2395544次浏览 12202人参与

[](https://www.nowcoder.com/creation/subject/fefa9c54a85746398c9e808d831afc8b?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 中国电信笔试 \#

60033次浏览 427人参与

[](https://www.nowcoder.com/creation/subject/e99186f56f2043f6bf2c70dbaf204cfc?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招的嫡长offer \#

485770次浏览 2494人参与

[](https://www.nowcoder.com/creation/subject/6c3f71b0cd9545c4978b0a46dd83b208?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 华为保温 \#

207783次浏览 685人参与

[](https://www.nowcoder.com/creation/subject/0a3bd52c3aa64914a6e7f63efd7c1552?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 抛开难度不谈，你最想去哪家公司？ \#

124343次浏览 483人参与

[](https://www.nowcoder.com/creation/subject/972f062e422d4b5fbbc029d608d773ac?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 还记得你第一次面试吗？ \#

508462次浏览 4970人参与
