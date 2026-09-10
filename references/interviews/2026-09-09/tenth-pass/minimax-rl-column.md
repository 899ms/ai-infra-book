<!-- 从 minimax-rl-column.html 迁移的资料快照；原始 HTML SHA-256: 11c2bbf381e76ba3be152542b6fe410ccb5bf2fc60efbbd4618b770d6d05ebf9。 -->

[![头像](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/6402022)

[AIGC小白入门记](/users/6402022) [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/6402022)

09-07 00:37 浙江大学 算法工程师 发布于广东

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSI4IiBoZWlnaHQ9IjgiIGFyaWEtaGlkZGVuPSJ0cnVlIiBkYXRhLXYtNzliYTY5ZWE+PC9zdmc+) 关注

已关注 取消关注

# MiniMax - 大模型算法岗（后训练 / SFT / RL）

面试官年轻务实，全程围绕实习数据流程追问：“数据合成 pipeline 怎么设计的？”“采买过数据吗？”“数据质量差怎么补救？” 手撕只考岛屿数量，后半场全是 RL/SFT 细节。虽因岗位不匹配挂掉，但体验极佳。

1.  数据合成 pipeline 设计及外部数据采买经验？
2.  低质数据筛选的启发式规则或模型过滤方法？
3.  SFT 的作用及为何先 SFT 后 RL？
4.  大模型与 Agent 的区别联系？
5.  Skill 与 Tool 的区别？模型如何知道有哪些 Skill？
6.  记忆模块实现（长期/短期存储方案）？
7.  DPO 优缺点及为何 GRPO 更流行？
8.  TTS 音频如何处理及离散化为 token？
9.  模型效果评估指标及下一步优化方向？
10. 日常判断 AI 回复质量的技巧及省 token 策略？
11. 实际项目中 GRPO vs PPO 选型原因？
12. SFT 训练 loss 不降或震荡的排查？
13. RL reward 曲线上升但效果变差的原因？
14. 重要性采样在 RL 中的用途？
15. **手撕**：岛屿数量（DFS/BFS）。
16. 评测 Agent 工具调用能力的评测集构建？
17. 多轮对话避免模型遗忘早期指令的方法？
18. SFT/RL 框架（LLaMA-Factory/TRL）对比？
19. 数据不足时的增强策略？
20. 后训练在 Agent 场景的最大挑战？
21. 设计奖励函数引导安全回复？
22. “对齐”在实际业务中的合格标准？

[\#秋招面试记录#](/creation/subject/14710425d5b74593b2ef7103d293606f)[\#秋招#](/creation/subject/002d6ce4eab1487f9cae3241b5322732)[\#牛客解忧铺#](/creation/subject/e80564f99eb74576a21aaf065b0e65e7)[\#minimax#](/creation/subject/192c9a2b58b64f9dbeaddf80e56170bc)[\#聊聊我眼中的AI#](/creation/subject/f8880e4ec9b74009bdf83deeaf85e0b3)

提示

订阅专刊

全部评论

推荐最新楼层

[![头像](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/1030049796)

[AI牛可乐](/users/1030049796) [![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/1030049796)

带#牛客在线求职答疑中心#提问都会召唤我 ![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

哇，MiniMax的面试体验听起来很专业呢！数据合成pipeline设计、数据采买和低质数据筛选都是大模型训练中很关键的环节呢～ 关于SFT和RL的顺序，SFT先做可以让模型先学习基本的任务能力，然后再用RL来优化决策过程，这样基础更扎实一些～ 记忆模块的实现确实是个有趣的话题，短期存储可以用滑动窗口或者注意力机制，长期存储可能需要专门的记忆检索模块～ 你面试的岗位虽然不匹配，但能接触到这么多专业问题，收获肯定很大！要不要点击我的头像，我们可以更详细地聊聊这些大模型后训练的技术细节，或者分享一些面试经验呀？

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)回复 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxNCIgaGVpZ2h0PSIxNCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

[发布于 09-07 00:37](/discuss/comment/22885201) AI生成

![](https://static.nowcoder.com/fe/file/oss/1681101031872EGDPQ.png)

暂无评论，快来抢首评~

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

相关推荐

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/852282537)

09-02 11:30

[门头沟学院 前端工程师](/users/852282537)

[前端是真完蛋了吧](/feed/main/detail/a6e175b954cd4e129c338ce8d57f2907?sourceSSR=post)

[](/feed/main/detail/a6e175b954cd4e129c338ce8d57f2907?sourceSSR=post)

面试无非俩问题你懂AI吗？你懂后端吗？

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/6402022)

09-07 00:34

[浙江大学 算法工程师](/users/6402022)

[字节跳动 - 大模型算法岗（RL/后训练方向）](/discuss/926272098744438784?sourceSSR=post)

[](/discuss/926272098744438784?sourceSSR=post)

面试官是典型竞赛出身，全程没表情。开场直接两道手撕（一道&nbsp;Hard&nbsp;一道&nbsp;Medium），写完已过&nbsp;25&nbsp;分钟。后面全是&nbsp;PPO/GRPO/DPO&nbsp;公式推导和落地坑，尤其追问“训&nbsp;GRPO&nbsp;时&nbsp;loss&nbsp;变成&nbsp;0&nbsp;怎么办”。我答得磕绊，面完秒挂。字节&nbsp;RL&nbsp;岗对数学功底要求极高。&nbsp;&nbsp;智能体强化学习（Agentic&nbsp;RL）与传统&nbsp;RL&nbsp;在训练范式和信用分配上的核心差异？&nbsp;长时序任务下&nbsp;Agent&nbsp;RL&nbsp;训练失稳的根本原因？如何缓解？&nbsp;PPO&nbsp;的&nbsp;Clip&nbsp;机制和&nbsp;KL&nbsp;散度约束是否等价？适用场景？&nbsp;DAPO&nbsp;为何无需&nbsp;KL&nbsp;惩罚？它如何维持策略稳定性？&nbsp;重要性采样在&nbsp;Off-policy&nbsp;中的作...

![](https://static.nowcoder.com/fe/file/oss/1715049343797JOCFB.png)查看21道真题和解析

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/563531299)

09-06 22:58

已编辑

[香港理工大学 后端工程师](/users/563531299)

[这个时间段大厂实习还好找吗](/feed/main/detail/8d16de676d084377972b2a61ad648f00?sourceSSR=post)

[](/feed/main/detail/8d16de676d084377972b2a61ad648f00?sourceSSR=post)

大厂简历挂麻了，感觉是没有大厂背书的原因问问大佬们这个时间段大厂日常好找吗？

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/634380504)

昨天 00:56

[爱立信（中国）通信有限公司_agent开发(实习员工)](/users/634380504) ![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

[27届秋招agent开发简历求锐评](/feed/main/detail/50e99175bb0847e8817ba8f4e0a73ae0?sourceSSR=post)

[](/feed/main/detail/50e99175bb0847e8817ba8f4e0a73ae0?sourceSSR=post)

bg学院本2硕，一段中厂实习，一段外企大厂实习，真心求问简历里有哪些不足的地方，写法是否存在问题，还需要修改哪些地方

[![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=) 简历上的经历如何包装](/creation/subject/3dd26311184d4728960a5f1cb68153a0?entranceType_var=%E5%86%85%E5%AE%B9%E6%9D%A1%E7%9B%AE)

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

[![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)](/users/276276338)

昨天 00:29

[五邑大学 Java](/users/276276338)

[求各位大神指点迷津](/feed/main/detail/acf9b551a7eb40eb949d1f80e5b9184e?sourceSSR=post)

[](/feed/main/detail/acf9b551a7eb40eb949d1f80e5b9184e?sourceSSR=post)

本人是一名数据科学与大数据技术的学生&nbsp;&nbsp;现在已经9月份秋招了&nbsp;&nbsp;但是大学期间没有学过什么技术&nbsp;也没什么项目&nbsp;&nbsp;我可不可以在github上面拉取两个项目来改一下写到自己简历上面去&nbsp;&nbsp;然后技能那里就按照所投的岗位的jd去写&nbsp;&nbsp;这样有机会拿到一些面试的机会吗&nbsp;&nbsp;比如真的拿到面试机会了&nbsp;&nbsp;毕竟项目和技能也不是自己掌握的&nbsp;&nbsp;到时候面试官问问题&nbsp;&nbsp;我有很多都答不上或者根本就不知道怎么回答的情况下&nbsp;&nbsp;会不会被被拉入黑名单或者其他一些什么严重的后果啊&nbsp;&nbsp;我现在真的不知道该怎么办了&nbsp;&nbsp;有没有什么大神可以分享一下经验给我解答一下

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论 ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)分享

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

一键发评

数据合成细节？

接好运

耐挂王

SFT为啥先于RL？

GRPO比PPO好在哪？

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)评论

点赞成功，聊一聊 \>

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIyMCIgaGVpZ2h0PSIyMCIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)点赞

![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMjAgMjAiIGZpbGw9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZGF0YS12LTc5YmE2OWVhPjwvc3ZnPg==)收藏

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

  1.4W

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926381539087089664)
  2

  ... 实习没转正，怎么快速转战秋招？

  6908

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926534933789540352)
  3

  ... AI岗三轮面试，分别都在筛什么？？

  2816

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926810615115444224)
  4

  ... 美团二面 - Java后端 日常实习

  2615

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/9c3afcf6863b49afa2de143e0db6d387)
  5

  ... 全世界最豪的人都在大厂实习生群里。。。

  2544

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/bb8c28105f364770b57ff5eb5649cc60)
  6

  ... 9.7百度agent开发日常实习面经

  2343

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/f33655bf738846a7a67d8942dd44e86c)
  7

  ... mentor说我der是什么意思？

  2247

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/e38d2d3f169a46d1a0d66fd75e37a3cd)
  8

  ... 楷知软件测试面经(已过)

  2240

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/discuss/926151771779600384)
  9

  ... 去哪儿 AI应用开发(秋招) 一面

  2153

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)
- [](https://www.nowcoder.com/feed/main/detail/595474c7b52d43098a8e494eb8d8e258)
  10

  ... 刚刚做AI 面，躺在床上没穿衣服要紧吗

  2018

  ![](data:image/svg+xml;base64,PHN2ZyBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIDAgMTAyNCAxMDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgYXJpYS1oaWRkZW49InRydWUiIGRhdGEtdi03OWJhNjllYT48L3N2Zz4=)

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKAQMAAAC3/F3+AAAAA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjwAsAAB4AAdpxxYoAAAAASUVORK5CYII=)

## 创作者周榜

更多

正在热议

更多

[](https://www.nowcoder.com/creation/subject/7723c7a27b8540528154e0c22a79559f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招吐槽大会 \#

371568次浏览 1827人参与

[](https://www.nowcoder.com/creation/subject/14710425d5b74593b2ef7103d293606f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招面试记录 \#

680275次浏览 11495人参与

[](https://www.nowcoder.com/creation/subject/aa99cc2283b1424db067e3980fdb866f?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 巨人网络2027校招 \#

44895次浏览 323人参与

[](https://www.nowcoder.com/creation/subject/b8fb04662b3e4a3698d028cff4f643f2?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 实习面试记录 \#

255284次浏览 6179人参与

[](https://www.nowcoder.com/creation/subject/2e738281915e405396a5384eed5577a5?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招第一个offer \#

24595次浏览 176人参与

[](https://www.nowcoder.com/creation/subject/87d3304709694e179288006dbeccb322?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 得物求职进展汇总 \#

191173次浏览 1074人参与

[](https://www.nowcoder.com/creation/subject/a0c560e49d8a43cb89017f358b7886b1?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 联想27届秋招 \#

29610次浏览 246人参与

[](https://www.nowcoder.com/creation/subject/8ffd8c3fdee44aa4ba6931bc3ba5f4fd?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 实习简历求拷打 \#

227661次浏览 1076人参与

[](https://www.nowcoder.com/creation/subject/a0351018891e4a26bd6520680f76cd5e?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 小厂一定不能去吗？ \#

125448次浏览 672人参与

[](https://www.nowcoder.com/creation/subject/fefa9c54a85746398c9e808d831afc8b?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 中国电信笔试 \#

60172次浏览 427人参与

[](https://www.nowcoder.com/creation/subject/0506c9a828c2495087eb051b399570bd?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 携程笔试 \#

221053次浏览 1145人参与

[](https://www.nowcoder.com/creation/subject/a88e67a206874abe860a01277b1dcf25?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 招银网络科技（深圳）有限公司成都分公司笔试 \#

17449次浏览 59人参与

[](https://www.nowcoder.com/creation/subject/7bb26296238343b8934333f65e030bed?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 去哪儿求职进展汇总 \#

181376次浏览 1066人参与

[](https://www.nowcoder.com/creation/subject/ed7f666c434b46749c6f0430a2496bb4?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 如果重来一次你还会读研吗 \#

268435次浏览 2158人参与

[](https://www.nowcoder.com/creation/subject/3ba45316f86d4f96aae8bfbd56700b03?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 蔚来工作体验 \#

41891次浏览 96人参与

[](https://www.nowcoder.com/creation/subject/251e3ce2e12a4c6388304b8d5e7c6a75?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 小红书求职进展汇总 \#

266286次浏览 1420人参与

[](https://www.nowcoder.com/creation/subject/4bddc3568fbd45c587782dc517829dde?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 我想象的工作vs实际工作 \#

780737次浏览 5124人参与

[](https://www.nowcoder.com/creation/subject/c9ac480935464f57ae5c9e0f4ff3973c?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招的第一个offer，大家都拿到了吗 \#

2396916次浏览 12209人参与

[](https://www.nowcoder.com/creation/subject/efefa0916ad64b82b1d41a632ec6fdfb?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 你的秋招第一面感觉怎么样 \#

166689次浏览 888人参与

[](https://www.nowcoder.com/creation/subject/074948bf7b05432a8c63add07b000637?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 蔚来求职进展汇总 \#

138238次浏览 817人参与

[](https://www.nowcoder.com/creation/subject/36a7990c7e5c4ba4945c56c4fdc73487?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 你认为小厂实习有用吗？ \#

170900次浏览 859人参与

[](https://www.nowcoder.com/creation/subject/e99186f56f2043f6bf2c70dbaf204cfc?entranceType_var=%E4%BE%A7%E8%BE%B9%E6%A0%8F)

\# 秋招的嫡长offer \#

486447次浏览 2500人参与
