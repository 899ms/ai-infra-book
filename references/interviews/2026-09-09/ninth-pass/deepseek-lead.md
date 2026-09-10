<!-- 从 deepseek-lead.html 迁移的资料快照；原始 HTML SHA-256: 3839a1ac2c0926b6f59279410fb4eefba0407e6358360a4518f202873d5e40a5。 -->

[![头像](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/6402022)

[AIGC小白入门记](/users/6402022) [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/6402022)

08-03 21:48 已编辑 浙江大学 算法工程师 发布于广东

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIGFyaWEtaGlkZGVuPSJ0cnVlIiBkYXRhLXYtNzliYTY5ZWE+PC9zdmc+) 关注

已关注 取消关注

# DeepSeek Agent开发岗三面，再面一轮就offer啦！！！

# DeepSeek Agent开发岗三面，再面一轮就offer啦！！！

> 面完出来，我在地铁上反复回味了两个小时。

这次的面试体验跟之前高德那次完全不同。高德是压力感拉满，DeepSeek这轮面完反而有点上头。面试官像一个经验丰富的技术合伙人，全程在跟我"聊设计"，而不是"考知识点"。

整个面试接近一个半小时，从项目架构一路深挖到评测体系、Badcase回流、Loop Engineering，中间还穿插了一道手撕算法。能感觉到对方是真的在评估你能不能独立负责一个Agent项目。

说实话面到后半程我已经有点兴奋了，因为讨论的问题正好是我最近一直在琢磨的方向。

下面整理一下还记得的问题和自己的一些复盘。

## 1. 自我介绍

开门见山问了这个问题。我大概花了两分钟，把自己的技术背景、最近一年主要做的事情、以及对Agent开发这个方向的兴趣点说了一下。

**要点**：不要背简历，要突出"你解决了什么问题"和"你为什么想做这个方向"。

## 2. 重点介绍AI私人助理项目

面试官对这个项目很感兴趣，让我详细讲一下。

我介绍的是一个**AI私人助理**，能接入日历、邮件、待办事项、知识库，帮用户做日程管理和信息汇总。用户可以说"帮我整理一下下周的日程并提醒我准备会议材料"，Agent会自动查询日历、生成待办、设置提醒。

面试官没有打断我，等我介绍完之后才开始提问。

## 3. AI私人助理整体架构怎么设计？解决什么问题？

这个问题要求我站在全局视角把架构说清楚。

**我的回答**：

整体分四层：

- 用户交互层：接收自然语言输入，做意图识别和实体抽取
- Agent调度层：根据意图选择合适的Agent或工作流
- 工具执行层：调用日历API、邮件API、知识库检索等
- 记忆层：短期记忆保存当前会话，长期记忆存储用户偏好和历史事实

解决的核心问题是：**让AI能主动帮用户管理个人事务，而不是被动回答**。

架构示意图：

![](https://uploadfiles.nowcoder.com/images/20260803/6402022_1785762865084/D2B5CA33BD970F64A6301FA75AE2EB22)

## 4. 高准确性场景怎么控制幻觉？

这个问题问的是Agent在需要精确输出的场景下如何保证可靠性。

**我的回答**：

控制幻觉有几种手段：

1.  约束解码：对于特定输出格式，用JSON Schema约束LLM的输出结构
2.  检索增强：所有事实性内容必须来自检索结果，而不是依赖模型参数记忆
3.  引用溯源：每个事实点都带上来源引用
4.  自我反思：生成后让模型自检一遍，或者用另一个模型做验证

最核心的一点：**凡是涉及具体数据（时间、地点、数字）的，必须从工具返回结果中提取，不允许模型自己编。**

![](https://uploadfiles.nowcoder.com/images/20260803/6402022_1785762920337/D2B5CA33BD970F64A6301FA75AE2EB22)

## 5. 幻觉率和引用错误率多少？业务上能否接受？

这道题问的是**实际指标**。

**我的回答**：

在我们的评测集上，幻觉率大概在3%-5%，引用错误率在2%左右。

业务上能不能接受取决于场景：

- 日程提醒类：不能接受，错了就是事故
- 信息汇总类：可以接受一定容错，但要有人工确认环节

面试官追问：怎么定义幻觉和引用错误？

我说：幻觉是"模型说了检索结果中没有的内容"，引用错误是"引用了文档但内容对不上"。前者更严重。

## 6. AI生成代码安全性问题如何解决？

这道题问的是代码执行的安全边界。

**我的回答（跟面试官确认了一下理解）**：

AI生成的代码不能直接在宿主环境里跑，必须用**沙箱隔离**。具体来说：

- 用Docker容器限制资源（CPU、内存、磁盘）
- 设置网络隔离，禁止访问内网
- 限制系统调用，不允许文件写入和进程创建
- 设置超时和内存上限，防止死循环和OOM

**面试官追问**：Python的`exec`和`eval`能直接用吗？

我说：不能。`exec`在Python里是不安全的，可以执行任意代码。即使限制了globals，仍然有办法绕过。必须用沙箱，比如`pypy`在受限环境中运行，或者用`nsjail`这种系统级隔离。

## 7. 定制了哪些能力？任务调度/状态回退/checkpoint/trace回放？

这个问题问的是Agent系统的**可观测性和可恢复性**。

**我的回答**：

我们在Agent框架里定制了四个核心能力：

- 任务调度：支持串行、并行、条件分支、循环四种执行模式
- 状态回退：当某个步骤失败时，回退到上一个稳定状态重试
- Checkpoint：每执行完一个关键步骤就保存快照，包含当前上下文、已执行动作列表、中间结果
- Trace回放：记录完整执行轨迹，用于离线调试和Badcase分析

Checkpoint的数据结构大致是：

``` prettyprint
{
  "session_id": "xxx",
  "step": 5,
  "state": {
    "messages": [...],
    "tool_results": {...},
    "current_task": "查询日历"
  },
  "checkpoint_at": "2026-07-29T14:32:00Z"
}
```

Trace回放特别有用。有时候Agent跑飞了，你不知道它怎么走到那一步的，有了完整轨迹才能定位问题。

## 8. 长期/中期/短期记忆分别怎么设计？

这道题考的是记忆分层。

**我的回答**：

- 短期记忆：当前会话的消息列表 + 工具调用结果，存在内存里
- 中期记忆：跨会话但近期（比如过去7天）的对话摘要，存在Redis里
- 长期记忆：用户偏好、历史事实、周期性任务等，存在向量数据库里

每次新请求来了之后：

![](https://uploadfiles.nowcoder.com/images/20260803/6402022_1785763013773/D2B5CA33BD970F64A6301FA75AE2EB22)

**面试官追问**：三个记忆怎么分层存储？

我说：短期用内存（快），中期用Redis（持久化+快），长期用向量库+MySQL（持久化+检索）。

## 9. 记忆滚动更新、摘要压缩、结构化压缩怎么做的？

这道题问的是记忆维护的具体机制。

**我的回答**：

**滚动更新**：当对话轮次超过阈值（比如20轮），用滑动窗口丢掉最早的消息，但保留系统指令和关键事实。

**摘要压缩**：每N轮对话触发一次摘要：

``` prettyprint
旧摘要 + 最近N轮对话 → LLM → 新摘要
```

**结构化压缩**：把对话中的事实抽取成结构化三元组：

``` prettyprint
"明天下午三点有会" → {type: "schedule", time: "2026-07-30T15:00", event: "会议"}
```

三种方式配合使用：滚动更新保证不超窗口，摘要压缩保留语义，结构化压缩便于检索。

## 10. Multi-Agent如何协作？ReAct、Path-Act

这道题问的是多Agent协同模式。

**我的回答**：

我们主要用了两种协作模式：

**ReAct模式**：单个Agent内部循环执行"推理→行动→观察"。适用于一个Agent独立完成任务的场景。

**Path-Act模式**：多个Agent按路径串行或并行执行。主Agent负责任务分解和路由，子Agent分别处理子任务，最后汇总结果。

协作流程：

![](https://uploadfiles.nowcoder.com/images/20260803/6402022_1785763083348/D2B5CA33BD970F64A6301FA75AE2EB22)

不同点是：

- ReAct：单Agent，循环迭代
- Path-Act：多Agent，路径编排

## 11. Badcase怎么定义？review拒绝/用户不采纳/高质量样本分别怎么处理？

这道题问的是Badcase管理。

**我的回答**：

我们把Badcase分成几类：

- Review拒绝：业务审核人员直接打回的案例 → 立即分析原因，修复
- 用户不采纳：用户对结果不满意或点了"没用" → 定期抽样分析
- 高质量样本：用户明确点了"有用" → 标记为正样本，入库

处理流程：

``` prettyprint
Badcase → 分类 → 分析根因 → 修复策略
    ├── 检索问题 → 优化检索策略
    ├── 模型问题 → 收集训练数据 → SFT
    └── 规则问题 → 修改Prompt或业务流程a
```

**面试官追问**：用户不采纳和review拒绝的区别？

我说：review拒绝是"内容有硬伤"，用户不采纳可能是"内容没问题但不符合预期"。前者必须修，后者需要进一步理解用户真实需求。

## 12. Badcase回流到SFT的完整链路？

这道题问的是**数据闭环**。

**我的回答**：

完整链路是这样的：

``` prettyprint
线上Badcase →
```

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMCIgaGVpZ2h0PSIxMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)剩余60%内容，订阅专栏后可继续查看/也可单篇购买

[大模型算法面经](/creation/manager/columnDetail/mXVKg4) 文章被收录于专栏

大模型算法面经

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

提示

购买单篇￥1

订阅专刊

全部评论

推荐最新楼层

[![头像](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/108599409)

[俊朗的铁锤在对齐目标](/users/108599409) [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/108599409)

门头沟学院 产品经理

写得太好啦 非技术也能看进去

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)2 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)回复 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

[发布于 08-05 23:33](/discuss/comment/22821669) 北京

[![头像](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/150030633)

[QHN沙壁](/users/150030633) [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/150030633)

四川大学 golang

主播是男生女生啊，写的真细腻

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)1 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)回复 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

[发布于 08-21 02:43](/discuss/comment/22850687) 四川

[![头像](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/352890922)

[求求来一个欧佛](/users/352890922) [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/352890922)

天津大学 测试开发

出算法题么？

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)1 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)回复 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

[发布于 08-17 09:57](/discuss/comment/22842056) 浙江

[![头像](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/108281897)

[牧野星海](/users/108281897) [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/108281897)

中原工学院信息商务学院 C++

我已经OUT了，怪不得工作难找![](https://uploadfiles.nowcoder.com/images/20220815/318889480_1660553763930/8B36D115CE5468E380708713273FEF43)

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)回复 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

[发布于 08-05 10:49](/discuss/comment/22820022) 浙江

![](https://static.nowcoder.com/fe/file/oss/1681101031872EGDPQ.png)

暂无评论，快来抢首评~

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

相关推荐

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/1030035007)

08-10 16:56

[门头沟学院 后端工程师](/users/1030035007)

[我从 Java 转去做 FDE，薪资涨了 30%](/discuss/916372260636590080?sourceSSR=post)

[](/discuss/916372260636590080?sourceSSR=post)

今年年初就感觉后端干不动了，总是在裁员，于是痛定思痛，要主动换个工作，了解到了fde这个岗位，感觉算是有增长空间的岗位，于是乎就开始投简历+面试，好在皇天不负有心人，因为有技术背景，成功找到了fde的工作，今天决定重回牛客，和大家分享下我的经历，除了技术岗位以外，校招也可以考虑考虑一些：解决方案专家、fde等技术复合型岗位，职业生命周期也许会比开发更长远一些👍&nbsp;希望对要找工作的小朋友们有一些帮助吧&nbsp;FDE&nbsp;到底是做什么的？&nbsp;我面试前也以为&nbsp;FDE&nbsp;就是&nbsp;AI&nbsp;版售前，后来聊了十几家公司，发现它更像是「工程、产品、交付、客户沟通」混在一起的岗位。&nbsp;&nbsp;我是怎么投的？&nbsp;&nbsp;面试都在问什么？&nbsp;我面的十...

NOoOo0B：一人当三人用![](https://uploadfiles.nowcoder.com/images/20220815/318889480_1660553763718/D9FDAE9918A39C99254A9D8D179628E5)公司赚麻

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/500303394)

08-19 13:16

[腾讯_WXG_前端开发实习(准入职员工)](/users/500303394) ![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

[居然是开水团](/feed/main/detail/a9b5c0d2a6a748ef8b03217d848529cb?sourceSSR=post)

[](/feed/main/detail/a9b5c0d2a6a748ef8b03217d848529cb?sourceSSR=post)

话说回来我一次都没面过美团&nbsp;&nbsp;

[![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=) 我的大厂天选 CP](/creation/subject/ea6b6d3e6a8a48b183657f15df2bfbe3?entranceType_var=%E5%86%85%E5%AE%B9%E6%9D%A1%E7%9B%AE)

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/6402022)

09-04 23:14

[浙江大学 算法工程师](/users/6402022)

[拼多多 - AI Agent 开发（工程化 + 数据库方向）](/discuss/925527160763187200?sourceSSR=post)

[](/discuss/925527160763187200?sourceSSR=post)

拼多多的面试是双机位，氛围很严肃。面试官是个技术&nbsp;Leader，非常务实，开场直接让我介绍项目的“代码生成全链路”。我说到上下文超限问题，他立刻追问“1M&nbsp;也不够怎么办”，我答了工程实践方案，他点了点头。手撕算法考了&nbsp;LRU，我写了个标准版，他追问“如果要求支持泛型和过期时间呢”，我当场改代码。后半场全是数据库和缓存八股，问得极其细致，比如“B+树叶子节点存储空间大小”“索引存在硬盘还是内存”。面完感觉虽然被拷打得很惨，但答得比较扎实，两天后收到了二面通知。拼多多对工程底层的执着令人印象深刻。&nbsp;&nbsp;介绍你的&nbsp;Agent&nbsp;代码生成链路全流程，长流程下如何解决上下文超限问题？&nbsp;长流程任务的“断点恢复...

![](https://static.nowcoder.com/fe/file/oss/1715049343797JOCFB.png)查看22道真题和解析

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/363741697)

08-19 17:16

[门头沟学院 研发工程师](/users/363741697)

[AI岗工资太高了……](/feed/main/detail/2adb7d29c88d4b378d07933f76db1902?sourceSSR=post)

[](/feed/main/detail/2adb7d29c88d4b378d07933f76db1902?sourceSSR=post)

一天4500，还只是实习，吓哭了

27届看看我👀：我们也招AI岗的！欢迎来投！校招HC多：https://www.nowcoder.com/link/lianxiangqiuzhao，秋招专属内推码：ANK2027

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/6402022)

昨天 22:51

[浙江大学 算法工程师](/users/6402022)

[DeepSeek（深度求索）——AI Agent 开发岗 社招一面](/discuss/926970960375214080?sourceSSR=post)

[](/discuss/926970960375214080?sourceSSR=post)

更像技术合伙人之间的设计讨论。&quot;不考知识点，聊设计、聊趋势、聊想法&quot;。全程&nbsp;90&nbsp;分钟，从项目架构到评测体系到&nbsp;Loop&nbsp;Engineering。&nbsp;开场与项目讨论&nbsp;&nbsp;&nbsp;你最近在关注&nbsp;Agent&nbsp;领域的什么新技术？——你说你关注了&nbsp;DeepSeek-Harness，你怎么理解它和&nbsp;LangChain&nbsp;的本质区别？Harness&nbsp;解决了什么&nbsp;LangChain&nbsp;解决不了的问题？&nbsp;&nbsp;&nbsp;选一个你做得最满意的&nbsp;Agent&nbsp;项目，完整讲一遍。——从业务背景到技术方案到落地效果。不要报菜名（说用了&nbsp;RAG、用了&nbsp;Multi-Agent），我要听设计决策背后的思考。&nbsp;&nbsp;&nbsp;架构设计深度追问&nbsp;...

[![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=) 秋招吐槽大会](/creation/subject/7723c7a27b8540528154e0c22a79559f?entranceType_var=%E5%86%85%E5%AE%B9%E6%9D%A1%E7%9B%AE)

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

一键发评

蹲终面结果

接好运

举报了

Hermes怎么接入

Badcase回流链路

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论

点赞成功，聊一聊 \>

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)28

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)98

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

- [](https://www.nowcoder.com/feed/main/detail/f64dea2a6fc941d19e2fecf7eb0ca3a0)
  1

  ... Bigo后端开发一面

  1.5W

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926381539087089664)
  2

  ... 实习没转正，怎么快速转战秋招？

  7183

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926534933789540352)
  3

  ... AI岗三轮面试，分别都在筛什么？？

  2713

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/9c3afcf6863b49afa2de143e0db6d387)
  4

  ... 全世界最豪的人都在大厂实习生群里。。。

  2636

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926810615115444224)
  5

  ... 美团二面 - Java后端 日常实习

  2635

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/f33655bf738846a7a67d8942dd44e86c)
  6

  ... mentor说我der是什么意思？

  2599

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/bb8c28105f364770b57ff5eb5649cc60)
  7

  ... 9.7百度agent开发日常实习面经

  2238

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/e38d2d3f169a46d1a0d66fd75e37a3cd)
  8

  ... 楷知软件测试面经(已过)

  2199

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926151771779600384)
  9

  ... 去哪儿 AI应用开发(秋招) 一面

  2117

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/595474c7b52d43098a8e494eb8d8e258)
  10

  ... 刚刚做AI 面，躺在床上没穿衣服要紧吗

  2113

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

## 创作者周榜

更多

正在热议

更多

[](https://www.nowcoder.com/creation/subject/7723c7a27b8540528154e0c22a79559f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招吐槽大会 \#

370528次浏览 1815人参与

[](https://www.nowcoder.com/creation/subject/14710425d5b74593b2ef7103d293606f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招面试记录 \#

677976次浏览 11464人参与

[](https://www.nowcoder.com/creation/subject/aa99cc2283b1424db067e3980fdb866f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 巨人网络2027校招 \#

44560次浏览 322人参与

[](https://www.nowcoder.com/creation/subject/b8fb04662b3e4a3698d028cff4f643f2?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 实习面试记录 \#

254970次浏览 6173人参与

[](https://www.nowcoder.com/creation/subject/2e738281915e405396a5384eed5577a5?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招第一个offer \#

24010次浏览 175人参与

[](https://www.nowcoder.com/creation/subject/87d3304709694e179288006dbeccb322?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 得物求职进展汇总 \#

191103次浏览 1074人参与

[](https://www.nowcoder.com/creation/subject/a0c560e49d8a43cb89017f358b7886b1?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 联想27届秋招 \#

29559次浏览 246人参与

[](https://www.nowcoder.com/creation/subject/8ffd8c3fdee44aa4ba6931bc3ba5f4fd?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 实习简历求拷打 \#

227548次浏览 1074人参与

[](https://www.nowcoder.com/creation/subject/a0351018891e4a26bd6520680f76cd5e?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 小厂一定不能去吗？ \#

125204次浏览 671人参与

[](https://www.nowcoder.com/creation/subject/fefa9c54a85746398c9e808d831afc8b?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 中国电信笔试 \#

60161次浏览 427人参与

[](https://www.nowcoder.com/creation/subject/0506c9a828c2495087eb051b399570bd?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 携程笔试 \#

220885次浏览 1144人参与

[](https://www.nowcoder.com/creation/subject/a88e67a206874abe860a01277b1dcf25?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 招银网络科技（深圳）有限公司成都分公司笔试 \#

17423次浏览 59人参与

[](https://www.nowcoder.com/creation/subject/7bb26296238343b8934333f65e030bed?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 去哪儿求职进展汇总 \#

181362次浏览 1066人参与

[](https://www.nowcoder.com/creation/subject/ed7f666c434b46749c6f0430a2496bb4?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 如果重来一次你还会读研吗 \#

268401次浏览 2156人参与

[](https://www.nowcoder.com/creation/subject/3ba45316f86d4f96aae8bfbd56700b03?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 蔚来工作体验 \#

41868次浏览 96人参与

[](https://www.nowcoder.com/creation/subject/251e3ce2e12a4c6388304b8d5e7c6a75?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 小红书求职进展汇总 \#

266276次浏览 1420人参与

[](https://www.nowcoder.com/creation/subject/4bddc3568fbd45c587782dc517829dde?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 我想象的工作vs实际工作 \#

780563次浏览 5124人参与

[](https://www.nowcoder.com/creation/subject/c9ac480935464f57ae5c9e0f4ff3973c?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招的第一个offer，大家都拿到了吗 \#

2396647次浏览 12209人参与

[](https://www.nowcoder.com/creation/subject/efefa0916ad64b82b1d41a632ec6fdfb?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 你的秋招第一面感觉怎么样 \#

166678次浏览 888人参与

[](https://www.nowcoder.com/creation/subject/074948bf7b05432a8c63add07b000637?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 蔚来求职进展汇总 \#

138220次浏览 817人参与

[](https://www.nowcoder.com/creation/subject/36a7990c7e5c4ba4945c56c4fdc73487?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 你认为小厂实习有用吗？ \#

170870次浏览 859人参与

[](https://www.nowcoder.com/creation/subject/e99186f56f2043f6bf2c70dbaf204cfc?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招的嫡长offer \#

486354次浏览 2499人参与
