<!-- 从 siliconflow-infra.html 迁移的资料快照；原始 HTML SHA-256: 0b27df2bb9b0d5af036f05560c7bc47d969bad9ed9d01d3635df876b85948ae6。 -->

[![头像](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/321612057)

[牛客321612057号](/users/321612057) [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/321612057)

04-13 18:18 已编辑 东北大学 C++ 发布于辽宁

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIGFyaWEtaGlkZGVuPSJ0cnVlIiBkYXRhLXYtNzliYTY5ZWE+PC9zdmc+) 关注

已关注 取消关注

# 硅基流动推理infra

cutlass: swizzle / stage用处和原理  
bankconflict  
问简历  
手撕  
blockreduce  
rmsnorm  
反问

全部评论

推荐最新楼层

![](https://static.nowcoder.com/fe/file/oss/1681101031872EGDPQ.png)

暂无评论，快来抢首评~

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

相关推荐

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/384881662)

09-03 18:52

已编辑

[中山大学 算法工程师](/users/384881662)

[【大模型面试】手撕 MHA + KV‑Cache 完整代码解析｜推理加速核心](/discuss/925094760170127360?sourceSSR=dynamic)

[](/discuss/925094760170127360?sourceSSR=dynamic)

面试题：给手写&nbsp;MHA&nbsp;加上&nbsp;KV&nbsp;Cache，说说原理与代码实现考点：&nbsp;KV‑Cache&nbsp;是大模型自回归推理最核心优化，面试常问原理、手写、区分&nbsp;Prefill/Decode&nbsp;阶段、优缺点。1、KV‑Cache&nbsp;到底解决什么痛点原生自回归推理：每生成&nbsp;1&nbsp;个新&nbsp;token，就要对全部历史序列重新计算&nbsp;K、V&nbsp;矩阵。序列越长，重复计算越严重，速度断崖式下跌。✅&nbsp;KV‑Cache&nbsp;核心思想：空间换时间&nbsp;把已经算完的历史&nbsp;Key、Value&nbsp;保存到&nbsp;GPU&nbsp;缓存。新&nbsp;token&nbsp;只计算当前步&nbsp;Q，K/V&nbsp;复用缓存，仅把新产生的&nbsp;K/V&nbsp;追加进缓存，避免重复计算历史&nbsp;token。⚠️重要：KV‑Ca...

![](https://static.nowcoder.com/fe/file/oss/1715049343797JOCFB.png)查看12道真题和解析

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/856888385)

08-10 17:34

[门头沟学院 C++](/users/856888385)

[美团大模型应用一面凉经😭](/feed/main/detail/af713b7855694811aa35b1d49f696df3?sourceSSR=dynamic)

[](/feed/main/detail/af713b7855694811aa35b1d49f696df3?sourceSSR=dynamic)

面试问题：&nbsp;1.自我介绍2.介绍一下你的实习/项目经历，并针对项目中的核心难点、解决思路以及最终业务指标进行深入追问。3.为什么&nbsp;Transformer&nbsp;架构中选择使用&nbsp;LayerNorm，而不是&nbsp;BatchNorm？Pre-LN&nbsp;和&nbsp;Post-LN&nbsp;分别有什么区别？4.SFT&nbsp;之后为什么还需要进行&nbsp;RLHF/DPO&nbsp;等对齐训练？5.QLoRA&nbsp;相比标准&nbsp;LoRA&nbsp;做了哪些改进？在消费级显卡上进行大模型微调时，显存开销可以降低多少？6.FlashAttention&nbsp;的核心原理是什么？它主要解决了大模型训练和推理过程中的什么瓶颈？7.vLLM&nbsp;推理框架中的&nbsp;PagedAttention&nbsp;机制是如何实现的？它主要解决了&nbsp;KV&nbsp;Cache&nbsp;存储中的什么问题？8.手撕两道算法题：最长有效括号二叉树层序遍历9.反问环节整体面试体验还不错，面试官比较注重沟通和思路，前面主要围绕个人经历和项目展开，后面会根据项目和简历继续深入追问，所以还是需要对自己做过的东西比较熟悉

![](https://static.nowcoder.com/fe/file/oss/1715049343797JOCFB.png)查看9道真题和解析

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/447852788)

08-20 20:59

[吉林大学 算法工程师](/users/447852788)

[智象未来 AI infra 一面](/discuss/920057298502811648?sourceSSR=dynamic)

[](/discuss/920057298502811648?sourceSSR=dynamic)

1.&nbsp;请做一个简短的自我介绍。2.&nbsp;平常是怎么学习的&nbsp;短期内有没有计划3.&nbsp;简单介绍下你这个项目4.&nbsp;从用户输入请求开始，到最终生成&nbsp;token，完整链路是什么？请求通常经历以下阶段：网关接收请求，完成鉴权、限流、超时设置和请求&nbsp;ID&nbsp;分配。Tokenizer&nbsp;或多模态处理器完成文本切分、图片解码、缩放和归一化。Scheduler&nbsp;将请求放入&nbsp;waiting&nbsp;queue，根据调度策略选择请求进入&nbsp;running&nbsp;状态。Prefill&nbsp;阶段处理完整输入，计算第一轮&nbsp;Attention，并生成初始&nbsp;KV&nbsp;Cache。Decode&nbsp;阶段每轮只处理新生成的&nbsp;token，同时读取历史&nbsp;KV&nbsp;Cache。...

[![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=) AI-Agent面试实战...](/creation/manager/columnDetail/0ox51k)

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/379472365)

09-02 22:08

[中山大学 算法工程师](/users/379472365)

[拼多多人才计划大模型一面](/feed/main/detail/0e97e548c7f04813977f1263c2f2c0c0?sourceSSR=dynamic)

[](/feed/main/detail/0e97e548c7f04813977f1263c2f2c0c0?sourceSSR=dynamic)

1.&nbsp;模型引入内化机制的核心设计目标是什么？是否仅仅是为了节省上下文&nbsp;Token&nbsp;开销？2.&nbsp;若长期对通用知识、通用能力做持续内化迭代，是否会累积知识偏差，最终引发知识冲突、模型幻觉等问题？如何规避？3.&nbsp;对比纯外化检索、纯上下文填充方案，你目前的内化架构除了节省&nbsp;Token，真正的核心优势和业务增益体现在哪里？4.&nbsp;传统强化学习、常规模型对齐方案已经可以满足模型能力迭代需求，你这套内化+Agent&nbsp;新增流程的不可替代性和设计意义是什么？5.&nbsp;你整套框架的&nbsp;Agentic&nbsp;智能体特性&nbsp;具体落地在哪些模块？如何体现自主决策、任务拆解、迭代优化能力？6.&nbsp;整体训练流程存在明显耗时不均衡问题，大量算力耗时集中在模型&nbsp;Rollout&nbsp;推理阶段，行业普遍存在&nbsp;GPU&nbsp;利用率偏低的问题，你是否有对应的优化方案？7.&nbsp;针对模型内化能力，你设计了哪些可量化指标，精准验证内化带来的模型性能提升？8.&nbsp;抛开Token节省、工程优化层面，从模型智能性、任务泛化性角度，阐述内化机制的不可替代必要性。9.&nbsp;你整套自动化迭代框架，本质是否等价于自动化搜参、自动化调参的工程框架？核心差异化在哪里？10.&nbsp;多Agent协作架构的设计必要性是什么？是否仅为缩减上下文长度？实际落地中上下文节省的量化收益是多少？11.&nbsp;项目配套知识库的整体规模、存储与组织架构是什么？单次任务推理会筛选、输入哪些知识库内容？12.&nbsp;你的框架是否具备自动化特征挖掘、特征构造的能力？整体方案是否只是简单的自动化调参工程封装，无算法创新？13.代码手撕:自注意力机制&nbsp;核心原理、计算流程与代码实现

![](https://static.nowcoder.com/fe/file/oss/1715049343797JOCFB.png)查看13道真题和解析

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/407412033)

08-27 13:55

已编辑

[中国科学院大学 自然语言处理](/users/407412033)

[字节火山方舟一面，项目被问得有点狠](/discuss/921927475611869184?sourceSSR=dynamic)

[](/discuss/921927475611869184?sourceSSR=dynamic)

岗位：机器学习平台研发&nbsp;/&nbsp;机器学习系统调度方向时长：约&nbsp;58min&nbsp;（2026.8.26）整体流程：项目深挖&nbsp;→&nbsp;OS&nbsp;/&nbsp;网络基础&nbsp;→&nbsp;手撕算法&nbsp;→&nbsp;反问。1.&nbsp;项目自我介绍从做过的项目里挑一个收获最大的，详细介绍技术架构和核心技术点这个项目最大的技术难点是什么介绍一下&nbsp;Agent&nbsp;Infra&nbsp;/&nbsp;Agent&nbsp;Runtime&nbsp;相关工作Agent&nbsp;调用&nbsp;Sandbox&nbsp;的链路如何做容错Sandbox&nbsp;运行过程中挂掉怎么办？项目部分基本不是问八股，而是沿着简历一直往下追，比较关注真正做了什么、为什么这么设计以及异常情况怎么处理。2.&nbsp;操作系统为什么操作系统需要区分用户态和内核态？什么情况下会发...

![](https://static.nowcoder.com/fe/file/oss/1715049343797JOCFB.png)查看16道真题和解析

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

一键发评

swizzle原理？

接好运

忍耐王

stage指什么？

手撕考啥题？

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论

点赞成功，聊一聊 \>

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)4

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

评论

![]() 提到的真题

返回内容 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

## 全站热榜

更多

- [](https://www.nowcoder.com/feed/main/detail/f64dea2a6fc941d19e2fecf7eb0ca3a0)
  1

  ... Bigo后端开发一面

  1.0W

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926381539087089664)
  2

  ... 实习没转正，怎么快速转战秋招？

  5660

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926810615115444224)
  3

  ... 美团二面 - Java后端 日常实习

  2705

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/f33655bf738846a7a67d8942dd44e86c)
  4

  ... mentor说我der是什么意思？

  2622

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/9c3afcf6863b49afa2de143e0db6d387)
  5

  ... 全世界最豪的人都在大厂实习生群里。。。

  2373

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926534933789540352)
  6

  ... AI岗三轮面试，分别都在筛什么？？

  2229

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/23d5946ce1d64313b04c64058bd3a49a)
  7

  ... 感觉自己好没用，一被骂就想离职

  1885

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/bb8c28105f364770b57ff5eb5649cc60)
  8

  ... 9.7百度agent开发日常实习面经

  1823

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/b3f4bf99c2d74299b17d57d7781e59ae)
  9

  ... 一年实习转正失败。。。

  1787

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926151771779600384)
  10

  ... 去哪儿 AI应用开发(秋招) 一面

  1785

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

## 创作者周榜

更多

正在热议

更多

[](https://www.nowcoder.com/creation/subject/7723c7a27b8540528154e0c22a79559f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招吐槽大会 \#

369585次浏览 1805人参与

[](https://www.nowcoder.com/creation/subject/14710425d5b74593b2ef7103d293606f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招面试记录 \#

675138次浏览 11440人参与

[](https://www.nowcoder.com/creation/subject/aa99cc2283b1424db067e3980fdb866f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 巨人网络2027校招 \#

44335次浏览 321人参与

[](https://www.nowcoder.com/creation/subject/b8fb04662b3e4a3698d028cff4f643f2?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 实习面试记录 \#

254517次浏览 6168人参与

[](https://www.nowcoder.com/creation/subject/2e738281915e405396a5384eed5577a5?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招第一个offer \#

23729次浏览 174人参与

[](https://www.nowcoder.com/creation/subject/87d3304709694e179288006dbeccb322?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 得物求职进展汇总 \#

191024次浏览 1074人参与

[](https://www.nowcoder.com/creation/subject/a0c560e49d8a43cb89017f358b7886b1?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 联想27届秋招 \#

29504次浏览 246人参与

[](https://www.nowcoder.com/creation/subject/8ffd8c3fdee44aa4ba6931bc3ba5f4fd?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 实习简历求拷打 \#

227425次浏览 1073人参与

[](https://www.nowcoder.com/creation/subject/a0351018891e4a26bd6520680f76cd5e?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 小厂一定不能去吗？ \#

124922次浏览 669人参与

[](https://www.nowcoder.com/creation/subject/fefa9c54a85746398c9e808d831afc8b?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 中国电信笔试 \#

60125次浏览 427人参与

[](https://www.nowcoder.com/creation/subject/0506c9a828c2495087eb051b399570bd?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 携程笔试 \#

220714次浏览 1143人参与

[](https://www.nowcoder.com/creation/subject/a88e67a206874abe860a01277b1dcf25?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 招银网络科技（深圳）有限公司成都分公司笔试 \#

17414次浏览 59人参与

[](https://www.nowcoder.com/creation/subject/7bb26296238343b8934333f65e030bed?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 去哪儿求职进展汇总 \#

181337次浏览 1066人参与

[](https://www.nowcoder.com/creation/subject/ed7f666c434b46749c6f0430a2496bb4?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 如果重来一次你还会读研吗 \#

268322次浏览 2156人参与

[](https://www.nowcoder.com/creation/subject/3ba45316f86d4f96aae8bfbd56700b03?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 蔚来工作体验 \#

41849次浏览 96人参与

[](https://www.nowcoder.com/creation/subject/251e3ce2e12a4c6388304b8d5e7c6a75?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 小红书求职进展汇总 \#

266239次浏览 1420人参与

[](https://www.nowcoder.com/creation/subject/4bddc3568fbd45c587782dc517829dde?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 我想象的工作vs实际工作 \#

780377次浏览 5124人参与

[](https://www.nowcoder.com/creation/subject/c9ac480935464f57ae5c9e0f4ff3973c?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招的第一个offer，大家都拿到了吗 \#

2396332次浏览 12206人参与

[](https://www.nowcoder.com/creation/subject/efefa0916ad64b82b1d41a632ec6fdfb?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 你的秋招第一面感觉怎么样 \#

166653次浏览 888人参与

[](https://www.nowcoder.com/creation/subject/074948bf7b05432a8c63add07b000637?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 蔚来求职进展汇总 \#

138197次浏览 817人参与

[](https://www.nowcoder.com/creation/subject/36a7990c7e5c4ba4945c56c4fdc73487?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 你认为小厂实习有用吗？ \#

170816次浏览 859人参与

[](https://www.nowcoder.com/creation/subject/e99186f56f2043f6bf2c70dbaf204cfc?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招的嫡长offer \#

486238次浏览 2499人参与
