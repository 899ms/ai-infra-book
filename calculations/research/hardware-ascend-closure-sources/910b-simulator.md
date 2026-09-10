<!-- 从 910b-simulator.html 迁移的资料快照；原始 HTML SHA-256: 1749a26d6282b216a94ee08d1ad11741f1b4804d78bd147f2a206ff5a815f3e0。 -->

[昇腾文档](/document)![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIGNsYXNzPSJvLXN2Zy1pY29uIG8taWNvbi1jaGV2cm9uLXJpZ2h0IHR5cGUtZmlsbCI+PCEtLXYtaWYtLT48L3N2Zz4=)

[故障案例](/document/caselibrary)![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIGNsYXNzPSJvLXN2Zy1pY29uIG8taWNvbi1jaGV2cm9uLXJpZ2h0IHR5cGUtZmlsbCI+PCEtLXYtaWYtLT48L3N2Zz4=)

使用msProf工具做算子仿真调优时报错161001![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIGNsYXNzPSJvLXN2Zy1pY29uIG8taWNvbi1jaGV2cm9uLXJpZ2h0IHR5cGUtZmlsbCI+PCEtLXYtaWYtLT48L3N2Zz4=)

使用msProf工具做算子仿真调优时报错161001

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIGNsYXNzPSJvLXN2Zy1pY29uIGljb24tdGltZSB0eXBlLWZpbGwgaW5mby1pdGVtLWljb24iIGRhdGEtdi1mZTVmNWQ4Nj48IS0tLS0+PC9zdmc+)2026/02/05

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIGNsYXNzPSJvLXN2Zy1pY29uIGljb24tdmlldyB0eXBlLWZpbGwgaW5mby1pdGVtLWljb24iIGRhdGEtdi1mZTVmNWQ4Nj48IS0tLS0+PC9zdmc+)595

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMTYgMTYiIGNsYXNzPSJvLXN2Zy1pY29uIGljb24tc2ltcGxlLXN0YXIgdHlwZS1maWxsIHJhdGUtc2ltcGxlLXN0YXIiIGRhdGEtdi00ZWU3ODQyMD48IS0tLS0+PC9zdmc+)

暂无评分

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMTYgMTYiIGNsYXNzPSJvLXN2Zy1pY29uIGljb24tZmxvd2VyIHR5cGUtZmlsbCBzY29yZS1pbWciIGRhdGEtdi00ZWU3ODQyMD48IS0tLS0+PC9zdmc+)

我要评分

问题信息

| 问题来源 | 产品大类 | 关键字                       |
|----------|----------|------------------------------|
| 社区工单 | 算子开发 | msProf、算子仿真调优、161001 |

#### 问题现象描述

使用msProf工具的msprof op simulator功能进行算子仿真调优，以基于可执行文件方式执行命令时，报错提示“aclnnSqrtGetWorkspaceSize failed. ERROR: 161001”，并且子进程以状态码139退出，导致仿真任务失败，无法完成算子调优。

执行命令为：msprof op simulator --soc-version=Ascend910B --output=./output_data ./execute_sqrt_op

#### 原因分析

以基于可执行文件方式使用msprof op simulator开启算子仿真调优时，--soc-version参数需要指定为用户实际使用的芯片型号（如Ascend910B4）。

#### 解决措施

参考如下操作获取具体芯片型号，并指定给--soc-version参数（[参考文档](https://www.hiascend.com/document/detail/zh/canncommercial/82RC1/devaids/optool/atlasopdev_16_0083.html)）：

步骤1、使用 npu-smi info 命令查询具体芯片型号

**图1** 查询具体芯片型号 ![](https://www.hiascend.com/doc_center/source/zh/case/07ab4a9975cd47d2b97c093fc2a75c21/zh-cn_image_0000002549856229.png)

步骤2、根据具体芯片型号修改执行命令。

以图1为例，执行命令为：msprof op simulator --soc-version=Ascend910B1 --output=./output_data ./execute_sqrt_op

本页内容

- 问题信息
- 问题现象描述
- 原因分析
- 解决措施

![](data:image/svg+xml;base64,PHN2ZyBmaWxsPSJub25lIiB3aWR0aD0iMCIgaGVpZ2h0PSIwIiBjbGFzcz0ic3ZnLWRlZiIgZGF0YS12LTAxMGZhOWNmPjxkZWZzIGRhdGEtdi0wMTBmYTljZj48bGluZWFyZ3JhZGllbnQgaWQ9ImZsb2F0LWJ0bi1zdmctYWN0aXZlIiB4MT0iMCUiIHkxPSI1MCUiIHgyPSIxMDAlIiB5Mj0iNTAlIiBkYXRhLXYtMDEwZmE5Y2Y+PHN0b3Agc3RvcC1jb2xvcj0iIzJlNTNmYSIgb2Zmc2V0PSIwJSIgZGF0YS12LTAxMGZhOWNmPjwvc3RvcD48c3RvcCBzdG9wLWNvbG9yPSIjN2IyNWY0IiBvZmZzZXQ9IjEwMCUiIGRhdGEtdi0wMTBmYTljZj48L3N0b3A+PC9saW5lYXJncmFkaWVudD48L2RlZnM+PC9zdmc+)

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQgMjQiIGNsYXNzPSJvLXN2Zy1pY29uIGljb24tYmFja3RvcCB0eXBlLWZpbGwgaWNvbi0yNCIgZGF0YS12LTAxMGZhOWNmPjwhLS0tLT48L3N2Zz4=)
