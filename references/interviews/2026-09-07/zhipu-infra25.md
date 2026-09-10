<!-- 从 zhipu-infra25.html 迁移的资料快照；原始 HTML SHA-256: 802a3c1b03d8b203a01f3848d7f76e1cdfe2bd8591b4873b9d20ae451e1f66c7。 -->

[![头像](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/239358405)

[Hayden_CY](/users/239358405) [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/239358405)

2025-09-18 00:46 四平职业大学 机器学习 发布于新加坡

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIGFyaWEtaGlkZGVuPSJ0cnVlIiBkYXRhLXYtNzliYTY5ZWE+PC9zdmc+) 关注

已关注 取消关注

# 智谱一面

经典过简历项目，重点问了最近这段的实习经历的主要工作，并且面试官的提问全程都非常落地，投递的Infra岗位，提问感觉像是在拷打算法，罗列几个回答的不太好的问题：  
  
1、你们的场景是如何使用并行策略的？比如TP/DP等  
答：采用TP2，DP8，EP16的单机16卡的并行策略  
  
2、接着问：TP和DP应用在哪个权重计算的位置，并且两者是如何进行协同的？  
答：TP/DP应用在Attention+FFN结构中的Attention，MoE模型的FFN使用EP，如何协同没回答上来，问了很久这个地方，最后和面试官说抱歉了，这部分的工作我没有具体落地做过，所以没有仔细研究过，然后面试官很有耐心的给我讲了一遍这部分的原理，也算是学习了  
  
3、问我对推理Infra调度方面的策略有没有了解过，比如动态批处理...等几个调度方面的工作  
答：简单描述了一下动态批处理的机制，主动说没有做过这方面的落地  
  
4、还问了对于推理框架的KVCache管理策略有没有了解过？  
答：介绍了一下vLLM社区的PageAttention，但是介绍的也非常粗糙，说类似于传统OS中的页表管理，并且言多必失，我说这个Page大小需要被精心设计，不能过大也不能过小，然后被拷问了为什么不能过大以及为什么不能过小的原因，感觉回答的也不是很好，被用例子拷打了  
  
接下来就是手撕阶段了，手撕也比较抽象，手撕的是MoE层的Dispatch过程，我用C++写的：  
  
输入是token的gating_scores和k，要求返回k个专家分配到的对应的token_id  
  
这个写的比较艰难吧，写的速度比较慢，最后时间不太够了，面试官看了我前面的实现代码和我说：思路我看了一下基本上是正确的，时间不够了也没叫我接着讲思路，就说那我们今天就到这里吧![](https://uploadfiles.nowcoder.com/images/20220815/318889480_1660553763930/8B36D115CE5468E380708713273FEF43)  
  
PS：面试过程感觉面试官非常有耐心，真的非常专业，实打实的一线开发人员，并且也乐于分享，回答不上来或者回答错误的问题面试官都耐心的给我讲解了，感觉自己发挥的不是很好，感觉虽然过的概率不大，但还是希望智谱能给个机会![](https://uploadfiles.nowcoder.com/images/20220815/318889480_1660553763930/8B36D115CE5468E380708713273FEF43)![](https://uploadfiles.nowcoder.com/images/20220815/318889480_1660553877149/A06BE39BE3905BBC75BFCB5B4FA29649)  
  
[\#秋招#](/creation/subject/002d6ce4eab1487f9cae3241b5322732)[\#我的秋招日记#](/creation/subject/1bd9e77417b74119a9564658998d2edd)[\#发面经攒人品#](/creation/subject/c121d108a0d94e04b8821f14c3acadd5)[\#牛客AI配图神器#](/creation/subject/eb05ef0c3aad4981af85e1f84c8d3db3)[\#智谱AI#](/creation/subject/da767c9233384be9a2992ee3d1946518)

全部评论

推荐最新楼层

![](https://static.nowcoder.com/fe/file/oss/1681101031872EGDPQ.png)

暂无评论，快来抢首评~

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

相关推荐

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/1030055248)

09-04 11:24

已编辑

[深圳大学 Java](/users/1030055248)

[联想招聘一文解析\|80+岗位方向，HC多多](/discuss/925345172454481920?sourceSSR=dynamic)

[](/discuss/925345172454481920?sourceSSR=dynamic)

一、岗位全量概览&nbsp;数量是指岗位方向，并非是HC数量，岗位多多，HC多多～&nbsp;&nbsp;&nbsp;二、联想在招什么人？&nbsp;1.&nbsp;毕业时间&nbsp;毕业时间为&nbsp;2026&nbsp;年&nbsp;9&nbsp;月至&nbsp;2027&nbsp;年&nbsp;8&nbsp;月&nbsp;的海内外应届毕业生。&nbsp;2.&nbsp;技术岗位的共同要求&nbsp;&nbsp;至少一门能落地的编程语言：Python、C++、Java、Golang、Shell&nbsp;等。&nbsp;Linux、Git、网络、数据库、操作系统等基础不能太虚。&nbsp;不只会调包，还要能说明输入、处理、输出、异常和部署链路。&nbsp;需要有项目实践或研究经历，最好能说清自己负责的模块和验证结果。&nbsp;普遍要求问题分析、快速学习、跨团队协作和技术文档能力。&nbsp;&nbsp;3.&nbsp;AI&nbsp;岗位的共同要求&nbsp;&nbsp;机器学习、深度学...

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/6402022)

今天 00:43

[浙江大学 算法工程师](/users/6402022)

[月之暗面（Moonshot）- Agent 应用开发岗](/discuss/926274239747952640?sourceSSR=dynamic)

[](/discuss/926274239747952640?sourceSSR=dynamic)

面试官是工程出身，全程场景追问。我答“上下文超限用摘要”，他追“摘要丢失关键信息怎么办”，我答“分块存储”，他再追“分块后跨块关联怎么保证”——连追五层。面到后面声音发抖，虽挂但认知被重塑。&nbsp;&nbsp;背景及选择&nbsp;Agent&nbsp;方向的原因？&nbsp;完整&nbsp;Agent&nbsp;系统核心模块（相比传统应用多了什么）？&nbsp;Agent&nbsp;项目架构设计及解决的问题？&nbsp;RAG&nbsp;全流程（切分/向量检索/召回/生成）？&nbsp;文本切分策略选择及影响？&nbsp;多&nbsp;Agent&nbsp;并行执行的状态管理和结果汇总？&nbsp;上下文管理（避免过长导致效果下降）？&nbsp;大量工具时避免&nbsp;Prompt&nbsp;过长的方案？&nbsp;工具返回数据量过大的处理？&nbsp;路由机制（请求交给哪个&nbsp;Agent）？...

[![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=) 牛客解忧铺](/creation/subject/e80564f99eb74576a21aaf065b0e65e7?entranceType_var=%E5%86%85%E5%AE%B9%E6%9D%A1%E7%9B%AE)

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/277917462)

08-13 12:25

[门头沟学院 研发工程师](/users/277917462)

[双非本进大厂，每天都压力大到睡不着](/feed/main/detail/6ef290ce89c84b889c82e86b4c785788?sourceSSR=dynamic)

[](/feed/main/detail/6ef290ce89c84b889c82e86b4c785788?sourceSSR=dynamic)

虽然入职没有公司腾讯阿里那么大，但是仍然觉得误闯天家。第一次对自己的学历焦虑。身边一起校招进来的所有人都是硕士，还都是顶尖学校的。甚至连我以前觉得吃了时代红利的我的领导们，他们基本上都是硕博，真成了学历洼地。虽然我目前体感大家工作中做事都是一样的，还是忍不住自卑，自己比起他们好像确实缺少了很多拼搏的心气，他们都是很优秀地保研一直读书一直高绩点，平时谈论的都是以前去过哪个大厂实习，都是离我很遥远的公司，越来越觉得我是捡漏进来的，感觉比不上公司的每一个人在这里，学历是我最不想提到的部分……

哈哈哈，你是老六：你要想我居然和学历这么高的一起干活，证明我并不比他们这些人差啊

[![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=) 因为学历你吃到过哪些红/...](/creation/subject/c15227cd08e345f3a346cda5255e9c11?entranceType_var=%E5%86%85%E5%AE%B9%E6%9D%A1%E7%9B%AE)

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/46322437)

09-01 20:14

[携程_资深后端开发](/users/46322437) ![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

[【华为】2027届校招笔试真题复盘free分享](/discuss/924394677548130304?sourceSSR=dynamic)

[](/discuss/924394677548130304?sourceSSR=dynamic)

【华为】2027届校招笔试真题复盘来了🔥AI/软件开发/硬件/射频全方向刚刷完华为技术岗笔试，趁热把各方向真题+高频考点整理出来了，后面要考的宝子赶紧码住！📌&nbsp;笔试基本信息形式：线上双机位监控，选择题（题库抽40题）或编程题（3道）合格线：选择题岗≥60分进面，编程岗≥150分进面流程：注册简历→上机考试→综合测评→专业面试→主管面试→Offer⚠️&nbsp;实习机考通过→秋招投同岗可免考，未通过→秋招需重考

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

一键发评

名字说一下

接好运

忍耐王

蹲个公司名

求分享面经

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论

点赞成功，聊一聊 \>

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)5

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)9

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

评论

![]() 提到的真题

返回内容 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

招聘动态

[查看更多 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTIgMTIiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEyIiBoZWlnaHQ9IjEyIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)](/jobs/school/schedule?pageSource=105)

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

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/jump?type=ad&source=105&companyId=158304&url=https%3A%2F%2Fapp.mokahr.com%2Fcampus-recruitment%2Fseichitech%2F140888%3Flocale%3Dzh-CN%23%2F&entityId=13355)

精智达

2027届校园招聘

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/jump?type=ad&source=105&companyId=148717&url=https%3A%2F%2Fapp.mokahr.com%2Fcampus-recruitment%2Fweilandalu%2F98096%3Flocale%3Dzh-CN%23%2F&entityId=13359)

未岚大陆

2027届校园招聘

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/jump?type=ad&source=105&companyId=931&url=https%3A%2F%2Ftalent.antgroup.com%2Fcampus-full-list%3Ftype%3Dcampus_graduates&entityId=13259)

蚂蚁集团

2026秋季校园招聘

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

## 全站热榜

更多

- [](https://www.nowcoder.com/discuss/926381539087089664)
  1

  ... 实习转正失败别慌，手把手教你快速转战秋招（附实习简历写法）

  7765

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/595474c7b52d43098a8e494eb8d8e258)
  2

  ... 刚刚做AI 面，躺在床上没穿衣服要紧吗

  7747

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/925390107392118784)
  3

  ... 你有一份秋招说明书待查看📩

  7571

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/a6e0745d71774776afd1fe7a771f73d8)
  4

  ... 学院本 字节转正成功 秋招的第一个offer！

  7395

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926228178081705984)
  5

  ... PDD 0906 秋招 AI Agent研发岗笔试

  5669

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/9c3afcf6863b49afa2de143e0db6d387)
  6

  ... 全世界最豪的人都在大厂实习生群里。。。

  3140

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/0036fd5f789d4058abf56a3aee286d44)
  7

  ... 10道单选15道多选两个编程一个小i游戏设计

  2926

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926155090849693696)
  8

  ... 拼多多服务端开发秋招面经

  2497

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/49dc04c8c6ab44cf9c1b0d0e98cd8fb6)
  9

  ... 携程笔试10分钟速通ai coding

  2399

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926058684231225344)
  10

  ... 得物 后端一面 9.1

  2397

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

## 创作者周榜

更多

正在热议

更多

[](https://www.nowcoder.com/creation/subject/14710425d5b74593b2ef7103d293606f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招面试记录 \#

638398次浏览 10880人参与

[](https://www.nowcoder.com/creation/subject/ed7f666c434b46749c6f0430a2496bb4?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 如果重来一次你还会读研吗 \#

266579次浏览 2144人参与

[](https://www.nowcoder.com/creation/subject/a0c560e49d8a43cb89017f358b7886b1?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 联想27届秋招 \#

28841次浏览 246人参与

[](https://www.nowcoder.com/creation/subject/78ed665a6ab346518335eef031477ff3?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 公司情报交流地 \#

187692次浏览 1447人参与

[](https://www.nowcoder.com/creation/subject/a0351018891e4a26bd6520680f76cd5e?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 小厂一定不能去吗？ \#

120300次浏览 595人参与

[](https://www.nowcoder.com/creation/subject/b62b67cb34e44436813fde4ef104b1b7?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 面试体验感最好的是哪家？ \#

455205次浏览 3930人参与

[](https://www.nowcoder.com/creation/subject/aa99cc2283b1424db067e3980fdb866f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 巨人网络2027校招 \#

32778次浏览 266人参与

[](https://www.nowcoder.com/creation/subject/ab6324e3456444b78b5f778d6694331b?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 一起聊美团 \#

428515次浏览 2228人参与

[](https://www.nowcoder.com/creation/subject/713eba51c80a49d082f992d06ad166a5?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 字节跳动工作体验 \#

911392次浏览 6780人参与

[](https://www.nowcoder.com/creation/subject/4bddc3568fbd45c587782dc517829dde?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 我想象的工作vs实际工作 \#

778122次浏览 5115人参与

[](https://www.nowcoder.com/creation/subject/8ffd8c3fdee44aa4ba6931bc3ba5f4fd?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 实习简历求拷打 \#

225372次浏览 1029人参与

[](https://www.nowcoder.com/creation/subject/8d0f18169875441b8be175a08364e0a7?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 牛油的搬砖plog \#

239398次浏览 1435人参与

[](https://www.nowcoder.com/creation/subject/0506c9a828c2495087eb051b399570bd?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 携程笔试 \#

216035次浏览 1100人参与

[](https://www.nowcoder.com/creation/subject/d57181d37f7a43a89c9631419365446f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 一人分享一道面试手撕题 \#

179789次浏览 4173人参与

[](https://www.nowcoder.com/creation/subject/64b0b4da76b844588e0fad09b5a8beaf?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 实习生应该准时下班吗 \#

392045次浏览 1863人参与

[](https://www.nowcoder.com/creation/subject/394b5e276c7a478fb4998e7484d9afcd?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 应届生，你找到工作了吗 \#

224114次浏览 1068人参与

[](https://www.nowcoder.com/creation/subject/f5f6b053d5f54abeae0a60e4e9878c28?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 影石Insta360求职进展汇总 \#

209182次浏览 1433人参与

[](https://www.nowcoder.com/creation/subject/e99186f56f2043f6bf2c70dbaf204cfc?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招的嫡长offer \#

482953次浏览 2447人参与

[](https://www.nowcoder.com/creation/subject/972f062e422d4b5fbbc029d608d773ac?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 还记得你第一次面试吗？ \#

506652次浏览 4956人参与

[](https://www.nowcoder.com/creation/subject/fa5f24a2835746abb811f58bb221de5f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 运营人求职交流聚集地 \#

300601次浏览 1157人参与

[](https://www.nowcoder.com/creation/subject/88311cd09474472087ca1155d3b8a548?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 职场中那些令人叹为观止的八卦 \#

119943次浏览 500人参与

[](https://www.nowcoder.com/creation/subject/6cd1ad014b82471b9db31480ccc1a348?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 汇川技术求职进展汇总 \#

212795次浏览 1086人参与
