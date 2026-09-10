<!-- 从 stepfun-main.html 迁移的资料快照；原始 HTML SHA-256: 97a18305463e4b4da9fce3ccfd56f924e7bc1e4ce98bd6a5bb624f0bc373e51c。 -->

[![头像](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/815450193)

[Varian](/users/815450193) [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/815450193)

03-23 09:30 门头沟学院 机器学习

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIGFyaWEtaGlkZGVuPSJ0cnVlIiBkYXRhLXYtNzliYTY5ZWE+PC9zdmc+) 关注

已关注 取消关注

# 阶跃大模型算法实习一面凉经

希望发出来对大家有帮助！  
1. 详细讲一下tokenizer的过程  
2. sft具体是怎么实现的  
3. deepspeed，什么情况用zero1-3？  
4. qwen，llama这些模型modeling的代码是怎么实现的？  
5. 用大模型合成问题怎么才能保证合成的问题答案是对的？  
6. 怎么判断预训练模型的好坏  
7. 怎么构造高质量的数据

全部评论

推荐最新楼层

[![头像](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/308590382)

[哈哈哈，你是老六](/users/308590382) [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/308590382)

门头沟学院 大数据开发工程师

感觉似乎没问啥东西呢

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)回复 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

[发布于 03-24 18:53](/discuss/comment/22543628) 北京

![](https://static.nowcoder.com/fe/file/oss/1681101031872EGDPQ.png)

暂无评论，快来抢首评~

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

相关推荐

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/519865582)

09-05 15:18

[华中师范大学 Java](/users/519865582)

[28届找日常实习本周参加的六场面试的面经](/discuss/925769870912884736?sourceSSR=dynamic)

[](/discuss/925769870912884736?sourceSSR=dynamic)

B站｜测试开发一面｜约&nbsp;31&nbsp;分钟开场与岗位认知请做一下自我介绍。你的专业和过往实习都偏开发，为什么选择测试开发岗位？你对测试开发岗位有什么了解？测试开发和普通测试有什么区别？你是否了解软件测试流程或软件开发流程？请介绍一下。AI&nbsp;/&nbsp;Agent谈谈你对&nbsp;AI&nbsp;Agent&nbsp;的理解。你对&nbsp;Skill&nbsp;有什么了解？你自己开发或使用过哪些&nbsp;Agent、Skill&nbsp;类产品？你做的垂直领域智能规划产品，相比通用大模型产品，独特价值在哪里？如何保证推送给用户的信息正确、准确？多轮对话轮次过多、上下文过长时，如何处理？你是否了解某&nbsp;AI&nbsp;测试&nbsp;/&nbsp;评测框架？了解其原理或做过相关实践吗？算法与项目完成一道二分...

[![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=) 面试问题记录](/creation/subject/3871fa77df8f40faa40474d054dbe5e3?entranceType_var=%E5%86%85%E5%AE%B9%E6%9D%A1%E7%9B%AE)

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/930374135)

09-05 11:27

已编辑

[纽约大学 (New York University) Java](/users/930374135)

[27届美本无实习秋招怎么办啊](/discuss/925711515359903744?sourceSSR=dynamic)

[](/discuss/925711515359903744?sourceSSR=dynamic)

NYU双专业学生，之前搞另一个专业：神经科学去了现在大四了计算机基础薄弱，做过的科研写简历上也没有用因为完全不垂直，在尝试做项目准备八股刷题，但是处境是很多直接简历挂，想日常实习可是由于人不在国内没办法回来只能卷暑期实习但是那个时候已经毕业了。&nbsp;很迷茫不知道该咋办了

[![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=) 27秋招9月行动指南](/creation/subject/70c2fd0b995a40d2ac3b68f522079428?entranceType_var=%E5%86%85%E5%AE%B9%E6%9D%A1%E7%9B%AE)

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/398545912)

08-15 11:34

[电子科技大学 Java](/users/398545912)

[这样的简历还有救吗](/feed/main/detail/f167514ba5034a348545d8ec41d91bfc?sourceSSR=dynamic)

[](/feed/main/detail/f167514ba5034a348545d8ec41d91bfc?sourceSSR=dynamic)

27届菜鸡秋招选手，求路过的好心哥哥姐姐指导一下简历

[![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=) 你的简历改到第几版了](/creation/subject/1f57d21da6e3458cb94b7a722c847e1c?entranceType_var=%E5%86%85%E5%AE%B9%E6%9D%A1%E7%9B%AE)

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/182976218)

08-26 17:51

[门头沟学院 搜索算法](/users/182976218)

[不要美化26年以前的就业环境](/feed/main/detail/db261673c17b423f829a80a9f2165e56?sourceSSR=dynamic)

[](/feed/main/detail/db261673c17b423f829a80a9f2165e56?sourceSSR=dynamic)

从23年就开始了，翻到了一些牛客的历史内容甚至今年很多AI相关岗位开的价格更是逆天，比以前还好永远都是最差的一年

不吃薯片：自己经历过23跟26两次校招，本来就是越来越难。本科基本随便投就有offer了，硕士毕业了投了好几个月才找跟本科差不多的

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/441351987)

09-03 13:19

[蚌埠坦克学院 嵌入式软件开发](/users/441351987)

[嵌入式大厂校招，面试官到底看重什么能力？](/discuss/925014989943865344?sourceSSR=dynamic)

[](/discuss/925014989943865344?sourceSSR=dynamic)

很多同学准备嵌入式校招，默认路径是：先刷&nbsp;C&nbsp;指针，再刷&nbsp;RTOS&nbsp;八股，再背&nbsp;SPI/I2C&nbsp;时序，最后临场背项目介绍。结果一面还能过，二面开始就崩。不是题没见过，而是面试官追问两层之后，发现你会的是“名词”，不是“能力”。那面试官到底在筛什么？先给结论大厂嵌入式校招，面试官真正看重的通常不是你“知道多少概念”，而是下面四件事能不能同时成立：基础能不能推理：不是背定义，而是能从现象推到原因。项目能不能深挖：能不能讲清数据路径、异常路径、设计取舍。排障有没有方法：偶现问题来了，你是乱试，还是分层定位。系统有没有边界感：MCU、RTOS、Linux、驱动、协议之间，你知道自己在哪一层。一句话说：...

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

一键发评

蹲蹲细节

接好运

忍耐王

求代码链接

mark收藏了

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论

点赞成功，聊一聊 \>

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)2

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

  3.0W

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/927003894100525056)
  2

  ... 混子转AI开发，我的速通路线

  2.2W

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/4ecad43528d449c9b6619a49d8648311)
  3

  ... 9.8 快手—一面

  4383

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/f33655bf738846a7a67d8942dd44e86c)
  4

  ... mentor说我der是什么意思？

  4230

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/9c3afcf6863b49afa2de143e0db6d387)
  5

  ... 全世界最豪的人都在大厂实习生群里。。。

  4216

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/e38d2d3f169a46d1a0d66fd75e37a3cd)
  6

  ... 楷知软件测试面经(已过)

  3917

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/bb8c28105f364770b57ff5eb5649cc60)
  7

  ... 9.7百度agent开发日常实习面经

  3782

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/b3f4bf99c2d74299b17d57d7781e59ae)
  8

  ... 一年实习转正失败。。。

  3121

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926534933789540352)
  9

  ... AI岗三轮面试，分别都在筛什么？？

  3026

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/d0e6d2d60aff4927928badbfac635fe7)
  10

  ... 字节意向

  3013

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

## 创作者周榜

更多

正在热议

更多

[](https://www.nowcoder.com/creation/subject/7723c7a27b8540528154e0c22a79559f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招吐槽大会 \#

375705次浏览 1915人参与

[](https://www.nowcoder.com/creation/subject/2e738281915e405396a5384eed5577a5?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招第一个offer \#

27876次浏览 207人参与

[](https://www.nowcoder.com/creation/subject/a0c560e49d8a43cb89017f358b7886b1?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 联想27届秋招 \#

29735次浏览 246人参与

[](https://www.nowcoder.com/creation/subject/14710425d5b74593b2ef7103d293606f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招面试记录 \#

688225次浏览 11689人参与

[](https://www.nowcoder.com/creation/subject/b8fb04662b3e4a3698d028cff4f643f2?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 实习面试记录 \#

256456次浏览 6189人参与

[](https://www.nowcoder.com/creation/subject/d27627b42fdc4f77bb82eae4f239a923?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 百度秋招提前批进度 \#

212353次浏览 1977人参与

[](https://www.nowcoder.com/creation/subject/aa99cc2283b1424db067e3980fdb866f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 巨人网络2027校招 \#

63579次浏览 333人参与

[](https://www.nowcoder.com/creation/subject/50ecdb5aa60942719fdddbabc08015a7?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 谈薪时HR压价该怎么应对 \#

338021次浏览 3430人参与

[](https://www.nowcoder.com/creation/subject/a0351018891e4a26bd6520680f76cd5e?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 小厂一定不能去吗？ \#

126014次浏览 687人参与

[](https://www.nowcoder.com/creation/subject/b073a08183be4a90a30f974b66c24560?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 机械求职避坑tips \#

129106次浏览 694人参与

[](https://www.nowcoder.com/creation/subject/5f8ea57ddc094736b507c7611066374e?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 哪个瞬间让你对大厂祛魅了？ \#

699907次浏览 4376人参与

[](https://www.nowcoder.com/creation/subject/8ffd8c3fdee44aa4ba6931bc3ba5f4fd?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 实习简历求拷打 \#

228041次浏览 1084人参与

[](https://www.nowcoder.com/creation/subject/e3552ae8abf848448d657b9bd981459b?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 你找工作想离家近 or 离家远？ \#

63051次浏览 413人参与

[](https://www.nowcoder.com/creation/subject/0506c9a828c2495087eb051b399570bd?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 携程笔试 \#

221472次浏览 1147人参与

[](https://www.nowcoder.com/creation/subject/373a7330af104e0cbbbe3ad85a6155f1?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 机械人，你最希望上岸的公司是？ \#

232012次浏览 1954人参与

[](https://www.nowcoder.com/creation/subject/abed91ce3b81448781438d7c2ccc9357?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 豪迈求职进展汇总 \#

35168次浏览 163人参与

[](https://www.nowcoder.com/creation/subject/ed7f666c434b46749c6f0430a2496bb4?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 如果重来一次你还会读研吗 \#

268569次浏览 2159人参与

[](https://www.nowcoder.com/creation/subject/4bddc3568fbd45c587782dc517829dde?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 我想象的工作vs实际工作 \#

781219次浏览 5126人参与

[](https://www.nowcoder.com/creation/subject/972f062e422d4b5fbbc029d608d773ac?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 还记得你第一次面试吗？ \#

509325次浏览 4978人参与

[](https://www.nowcoder.com/creation/subject/e99186f56f2043f6bf2c70dbaf204cfc?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招的嫡长offer \#

486798次浏览 2508人参与

[](https://www.nowcoder.com/creation/subject/87d3304709694e179288006dbeccb322?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 得物求职进展汇总 \#

191322次浏览 1080人参与

[](https://www.nowcoder.com/creation/subject/e5c7312e6cce49a588220fee462004a0?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 硬件/芯片校招攻略 \#

28184次浏览 327人参与
