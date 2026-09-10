<!-- 从 jacen-interview-roundup.html 迁移的资料快照；原始 HTML SHA-256: 3023e4a3e2a8fa4d9b22bc524b3245ba6e632f6d3670ed7edc7b007c68bddbbe。 -->

# 面经与高频考点题库 [​](#面经与高频考点题库)

> 首次编写：2026-08-12 \| 最后更新：2026-08-12

> **AI Infra / KV Cache 面试系列**
>
> - [导读](./aiinfra_overview.html)
> - [招聘岗位全景](./aiinfra_jobs.html)
> - [KV Cache 核心知识体系](./aiinfra_kvcache_deep_dive.html)
> - **面经与高频考点** ← 当前文章
> - [系统设计专题](./aiinfra_system_design.html)
> - [2 个月面试复习计划](./aiinfra_2month_plan.html)
> - [资源汇总](./aiinfra_resources.html)

本文是"题-答"形式的高频考点库，按主题分章。每题给**答题骨架**而非完整答案--面试时用自己的话展开。技术原理详见 [KV Cache 核心知识体系](./aiinfra_kvcache_deep_dive.html)。

> ⚠️ 标注 **\[实时核对\]** 的"某公司原题"为归纳整理，非逐字还原；具体原题请查牛客/一亩三分地/脉脉最新面经。

------------------------------------------------------------------------

## 第 1 章 KV Cache 专题 [​](#第-1-章-kv-cache-专题)

### Q1.1 为什么推理要缓存 K、V 而不缓存 Q？⭐⭐⭐⭐⭐ [​](#q1-1-为什么推理要缓存-k、v-而不缓存-q-⭐⭐⭐⭐⭐)

**骨架：** 自回归解码每步 attention 需要"当前 Q × 全历史 K/V"。历史 token 的 K/V 由其自身投影得到、不依赖新 token，故可缓存复用；Q 每步都是新 token 算出的单向量，只用于当前步、无需缓存。缓存 K/V 把单步复杂度从 O(t) 降到 O(1)。

### Q1.2 手算：Llama-2-7B，8K 上下文，batch 16，KV Cache 占多少显存？⭐⭐⭐⭐⭐ [​](#q1-2-手算-llama-2-7b-8k-上下文-batch-16-kv-cache-占多少显存-⭐⭐⭐⭐⭐)

**骨架：** 公式 ![](data:image/svg+xml;base64,PHN2ZyBzdHlsZT0ib3ZlcmZsb3c6dmlzaWJsZTttaW4taGVpZ2h0OjFweDttaW4td2lkdGg6MXB4O3ZlcnRpY2FsLWFsaWduOi0wLjQzOWV4OyIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iMTEuMjgyZXgiIGhlaWdodD0iMi4wMDlleCIgcm9sZT0iaW1nIiBmb2N1c2FibGU9ImZhbHNlIiB2aWV3Ym94PSIwIC02OTQgNDk4Ni42IDg4OCIgYXJpYS1oaWRkZW49InRydWUiPjxnIHN0cm9rZT0iY3VycmVudENvbG9yIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMCIgdHJhbnNmb3JtPSJzY2FsZSgxLC0xKSI+PGcgZGF0YS1tbWwtbm9kZT0ibWF0aCI+PGcgZGF0YS1tbWwtbm9kZT0ibW4iPjxwYXRoIGRhdGEtYz0iMzIiIGQ9Ik0xMDkgNDI5UTgyIDQyOSA2NiA0NDdUNTAgNDkxUTUwIDU2MiAxMDMgNjE0VDIzNSA2NjZRMzI2IDY2NiAzODcgNjEwVDQ0OSA0NjVRNDQ5IDQyMiA0MjkgMzgzVDM4MSAzMTVUMzAxIDI0MVEyNjUgMjEwIDIwMSAxNDlMMTQyIDkzTDIxOCA5MlEzNzUgOTIgMzg1IDk3UTM5MiA5OSA0MDkgMTg2VjE4OUg0NDlWMTg2UTQ0OCAxODMgNDM2IDk1VDQyMSAzVjBINTBWMTlWMzFRNTAgMzggNTYgNDZUODYgODFRMTE1IDExMyAxMzYgMTM3UTE0NSAxNDcgMTcwIDE3NFQyMDQgMjExVDIzMyAyNDRUMjYxIDI3OFQyODQgMzA4VDMwNSAzNDBUMzIwIDM2OVQzMzMgNDAxVDM0MCA0MzFUMzQzIDQ2NFEzNDMgNTI3IDMwOSA1NzNUMjEyIDYxOVExNzkgNjE5IDE1NCA2MDJUMTE5IDU2OVQxMDkgNTUwUTEwOSA1NDkgMTE0IDU0OVExMzIgNTQ5IDE1MSA1MzVUMTcwIDQ4OVExNzAgNDY0IDE1NCA0NDdUMTA5IDQyOVoiIHN0eWxlPSJzdHJva2Utd2lkdGg6MzsiIC8+PC9nPjxnIGRhdGEtbW1sLW5vZGU9Im1pIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSg1MDAsMCkiPjxwYXRoIGRhdGEtYz0iMUQ0M0YiIGQ9Ik0yMjggNjM3UTE5NCA2MzcgMTkyIDY0MVExOTEgNjQzIDE5MSA2NDlRMTkxIDY3MyAyMDIgNjgyUTIwNCA2ODMgMjE3IDY4M1EyNzEgNjgwIDM0NCA2ODBRNDg1IDY4MCA1MDYgNjgzSDUxOFE1MjQgNjc3IDUyNCA2NzRUNTIyIDY1NlE1MTcgNjQxIDUxMyA2MzdINDc1UTQwNiA2MzYgMzk0IDYyOFEzODcgNjI0IDM4MCA2MDBUMzEzIDMzNlEyOTcgMjcxIDI3OSAxOThUMjUyIDg4TDI0MyA1MlEyNDMgNDggMjUyIDQ4VDMxMSA0NkgzMjhRMzYwIDQ2IDM3OSA0N1Q0MjggNTRUNDc4IDcyVDUyMiAxMDZUNTY0IDE2MVE1ODAgMTkxIDU5NCAyMjhUNjExIDI3MFE2MTYgMjczIDYyOCAyNzNINjQxUTY0NyAyNjQgNjQ3IDI2MlQ2MjcgMjAzVDU4MyA4M1Q1NTcgOVE1NTUgNCA1NTMgM1Q1MzcgMFQ0OTQgLTFRNDgzIC0xIDQxOCAtMVQyOTQgMEgxMTZRMzIgMCAzMiAxMFEzMiAxNyAzNCAyNFEzOSA0MyA0NCA0NVE0OCA0NiA1OSA0Nkg2NVE5MiA0NiAxMjUgNDlRMTM5IDUyIDE0NCA2MVExNDcgNjUgMjE2IDMzOVQyODUgNjI4UTI4NSA2MzUgMjI4IDYzN1oiIHN0eWxlPSJzdHJva2Utd2lkdGg6MzsiIC8+PC9nPjxnIGRhdGEtbW1sLW5vZGU9Im1zdWIiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDExODEsMCkiPjxnIGRhdGEtbW1sLW5vZGU9Im1pIj48cGF0aCBkYXRhLWM9IjFENDVCIiBkPSJNMjEgMjg3UTIyIDI5MyAyNCAzMDNUMzYgMzQxVDU2IDM4OFQ4OSA0MjVUMTM1IDQ0MlExNzEgNDQyIDE5NSA0MjRUMjI1IDM5MFQyMzEgMzY5UTIzMSAzNjcgMjMyIDM2N0wyNDMgMzc4UTMwNCA0NDIgMzgyIDQ0MlE0MzYgNDQyIDQ2OSA0MTVUNTAzIDMzNlQ0NjUgMTc5VDQyNyA1MlE0MjcgMjYgNDQ0IDI2UTQ1MCAyNiA0NTMgMjdRNDgyIDMyIDUwNSA2NVQ1NDAgMTQ1UTU0MiAxNTMgNTYwIDE1M1E1ODAgMTUzIDU4MCAxNDVRNTgwIDE0NCA1NzYgMTMwUTU2OCAxMDEgNTU0IDczVDUwOCAxN1Q0MzkgLTEwUTM5MiAtMTAgMzcxIDE3VDM1MCA3M1EzNTAgOTIgMzg2IDE5M1Q0MjMgMzQ1UTQyMyA0MDQgMzc5IDQwNEgzNzRRMjg4IDQwNCAyMjkgMzAzTDIyMiAyOTFMMTg5IDE1N1ExNTYgMjYgMTUxIDE2UTEzOCAtMTEgMTA4IC0xMVE5NSAtMTEgODcgLTVUNzYgN1Q3NCAxN1E3NCAzMCAxMTIgMTgwVDE1MiAzNDNRMTUzIDM0OCAxNTMgMzY2UTE1MyA0MDUgMTI5IDQwNVE5MSA0MDUgNjYgMzA1UTYwIDI4NSA2MCAyODRRNTggMjc4IDQxIDI3OEgyN1EyMSAyODQgMjEgMjg3WiIgc3R5bGU9InN0cm9rZS13aWR0aDozOyIgLz48L2c+PGcgZGF0YS1tbWwtbm9kZT0iVGVYQXRvbSIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNjMzLC0xNTApIHNjYWxlKDAuNzA3KSIgZGF0YS1tangtdGV4Y2xhc3M9Ik9SRCI+PGcgZGF0YS1tbWwtbm9kZT0ibWkiPjxwYXRoIGRhdGEtYz0iMUQ0NTgiIGQ9Ik0xMjEgNjQ3UTEyMSA2NTcgMTI1IDY3MFQxMzcgNjgzUTEzOCA2ODMgMjA5IDY4OFQyODIgNjk0UTI5NCA2OTQgMjk0IDY4NlEyOTQgNjc5IDI0NCA0NzdRMTk0IDI3OSAxOTQgMjcyUTIxMyAyODIgMjIzIDI5MVEyNDcgMzA5IDI5MiAzNTRUMzYyIDQxNVE0MDIgNDQyIDQzOCA0NDJRNDY4IDQ0MiA0ODUgNDIzVDUwMyAzNjlRNTAzIDM0NCA0OTYgMzI3VDQ3NyAzMDJUNDU2IDI5MVQ0MzggMjg4UTQxOCAyODggNDA2IDI5OVQzOTQgMzI4UTM5NCAzNTMgNDEwIDM2OVQ0NDIgMzkwTDQ1OCAzOTNRNDQ2IDQwNSA0MzQgNDA1SDQzMFEzOTggNDAyIDM2NyAzODBUMjk0IDMxNlQyMjggMjU1UTIzMCAyNTQgMjQzIDI1MlQyNjcgMjQ2VDI5MyAyMzhUMzIwIDIyNFQzNDIgMjA2VDM1OSAxODBUMzY1IDE0N1EzNjUgMTMwIDM2MCAxMDZUMzU0IDY2UTM1NCAyNiAzODEgMjZRNDI5IDI2IDQ1OSAxNDVRNDYxIDE1MyA0NzkgMTUzSDQ4M1E0OTkgMTUzIDQ5OSAxNDRRNDk5IDEzOSA0OTYgMTMwUTQ1NSAtMTEgMzc4IC0xMVEzMzMgLTExIDMwNSAxNVQyNzcgOTBRMjc3IDEwOCAyODAgMTIxVDI4MyAxNDVRMjgzIDE2NyAyNjkgMTgzVDIzNCAyMDZUMjAwIDIxN1QxODIgMjIwSDE4MFExNjggMTc4IDE1OSAxMzlUMTQ1IDgxVDEzNiA0NFQxMjkgMjBUMTIyIDdUMTExIC0yUTk4IC0xMSA4MyAtMTFRNjYgLTExIDU3IC0xVDQ4IDE2UTQ4IDI2IDg1IDE3NlQxNTggNDcxTDE5NSA2MTZRMTk2IDYyOSAxODggNjMyVDE0OSA2MzdIMTQ0UTEzNCA2MzcgMTMxIDYzN1QxMjQgNjQwVDEyMSA2NDdaIiBzdHlsZT0ic3Ryb2tlLXdpZHRoOjM7IiAvPjwvZz48ZyBkYXRhLW1tbC1ub2RlPSJtaSIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNTIxLDApIj48cGF0aCBkYXRhLWM9IjFENDYzIiBkPSJNMTczIDM4MFExNzMgNDA1IDE1NCA0MDVRMTMwIDQwNSAxMDQgMzc2VDYxIDI4N1E2MCAyODYgNTkgMjg0VDU4IDI4MVQ1NiAyNzlUNTMgMjc4VDQ5IDI3OFQ0MSAyNzhIMjdRMjEgMjg0IDIxIDI4N1EyMSAyOTQgMjkgMzE2VDUzIDM2OFQ5NyA0MTlUMTYwIDQ0MVEyMDIgNDQxIDIyNSA0MTdUMjQ5IDM2MVEyNDkgMzQ0IDI0NiAzMzVRMjQ2IDMyOSAyMzEgMjkxVDIwMCAyMDJUMTgyIDExM1ExODIgODYgMTg3IDY5UTIwMCAyNiAyNTAgMjZRMjg3IDI2IDMxOSA2MFQzNjkgMTM5VDM5OCAyMjJUNDA5IDI3N1E0MDkgMzAwIDQwMSAzMTdUMzgzIDM0M1QzNjUgMzYxVDM1NyAzODNRMzU3IDQwNSAzNzYgNDI0VDQxNyA0NDNRNDM2IDQ0MyA0NTEgNDI1VDQ2NyAzNjdRNDY3IDM0MCA0NTUgMjg0VDQxOCAxNTlUMzQ3IDQwVDI0MSAtMTFRMTc3IC0xMSAxMzkgMjJRMTAyIDU0IDEwMiAxMTdRMTAyIDE0OCAxMTAgMTgxVDE1MSAyOThRMTczIDM2MiAxNzMgMzgwWiIgc3R5bGU9InN0cm9rZS13aWR0aDozOyIgLz48L2c+PC9nPjwvZz48ZyBkYXRhLW1tbC1ub2RlPSJtc3ViIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgyNTc1LjMsMCkiPjxnIGRhdGEtbW1sLW5vZGU9Im1pIj48cGF0aCBkYXRhLWM9IjFENDUxIiBkPSJNMzY2IDY4M1EzNjcgNjgzIDQzOCA2ODhUNTExIDY5NFE1MjMgNjk0IDUyMyA2ODZRNTIzIDY3OSA0NTAgMzg0VDM3NSA4M1QzNzQgNjhRMzc0IDI2IDQwMiAyNlE0MTEgMjcgNDIyIDM1UTQ0MyA1NSA0NjMgMTMxUTQ2OSAxNTEgNDczIDE1MlE0NzUgMTUzIDQ4MyAxNTNINDg3SDQ5MVE1MDYgMTUzIDUwNiAxNDVRNTA2IDE0MCA1MDMgMTI5UTQ5MCA3OSA0NzMgNDhUNDQ1IDhUNDE3IC04UTQwOSAtMTAgMzkzIC0xMFEzNTkgLTEwIDMzNiA1VDMwNiAzNkwzMDAgNTFRMjk5IDUyIDI5NiA1MFEyOTQgNDggMjkyIDQ2UTIzMyAtMTAgMTcyIC0xMFExMTcgLTEwIDc1IDMwVDMzIDE1N1EzMyAyMDUgNTMgMjU1VDEwMSAzNDFRMTQ4IDM5OCAxOTUgNDIwVDI4MCA0NDJRMzM2IDQ0MiAzNjQgNDAwUTM2OSAzOTQgMzY5IDM5NlEzNzAgNDAwIDM5NiA1MDVUNDI0IDYxNlE0MjQgNjI5IDQxNyA2MzJUMzc4IDYzN0gzNTdRMzUxIDY0MyAzNTEgNjQ1VDM1MyA2NjRRMzU4IDY4MyAzNjYgNjgzWk0zNTIgMzI2UTMyOSA0MDUgMjc3IDQwNVEyNDIgNDA1IDIxMCAzNzRUMTYwIDI5M1ExMzEgMjE0IDExOSAxMjlRMTE5IDEyNiAxMTkgMTE4VDExOCAxMDZRMTE4IDYxIDEzNiA0NFQxNzkgMjZRMjMzIDI2IDI5MCA5OEwyOTggMTA5TDM1MiAzMjZaIiBzdHlsZT0ic3Ryb2tlLXdpZHRoOjM7IiAvPjwvZz48ZyBkYXRhLW1tbC1ub2RlPSJtaSIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNTUzLC0xNTApIHNjYWxlKDAuNzA3KSI+PHBhdGggZGF0YS1jPSIyMTBFIiBkPSJNMTM3IDY4M1ExMzggNjgzIDIwOSA2ODhUMjgyIDY5NFEyOTQgNjk0IDI5NCA2ODVRMjk0IDY3NCAyNTggNTM0UTIyMCAzODYgMjIwIDM4M1EyMjAgMzgxIDIyNyAzODhRMjg4IDQ0MiAzNTcgNDQyUTQxMSA0NDIgNDQ0IDQxNVQ0NzggMzM2UTQ3OCAyODUgNDQwIDE3OFQ0MDIgNTBRNDAzIDM2IDQwNyAzMVQ0MjIgMjZRNDUwIDI2IDQ3NCA1NlQ1MTMgMTM4UTUxNiAxNDkgNTE5IDE1MVQ1MzUgMTUzUTU1NSAxNTMgNTU1IDE0NVE1NTUgMTQ0IDU1MSAxMzBRNTM1IDcxIDUwMCAzM1E0NjYgLTEwIDQxOSAtMTBINDE0UTM2NyAtMTAgMzQ2IDE3VDMyNSA3NFEzMjUgOTAgMzYxIDE5MlQzOTggMzQ1UTM5OCA0MDQgMzU0IDQwNEgzNDlRMjY2IDQwNCAyMDUgMzA2TDE5OCAyOTNMMTY0IDE1OFExMzIgMjggMTI3IDE2UTExNCAtMTEgODMgLTExUTY5IC0xMSA1OSAtMlQ0OCAxNlE0OCAzMCAxMjEgMzIwTDE5NSA2MTZRMTk1IDYyOSAxODggNjMyVDE0OSA2MzdIMTI4UTEyMiA2NDMgMTIyIDY0NVQxMjQgNjY0UTEyOSA2ODMgMTM3IDY4M1oiIHN0eWxlPSJzdHJva2Utd2lkdGg6MzsiIC8+PC9nPjwvZz48ZyBkYXRhLW1tbC1ub2RlPSJtaSIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMzU4NS42LDApIj48cGF0aCBkYXRhLWM9IjFENDYwIiBkPSJNMTMxIDI4OVExMzEgMzIxIDE0NyAzNTRUMjAzIDQxNVQzMDAgNDQyUTM2MiA0NDIgMzkwIDQxNVQ0MTkgMzU1UTQxOSAzMjMgNDAyIDMwOFQzNjQgMjkyUTM1MSAyOTIgMzQwIDMwMFQzMjggMzI2UTMyOCAzNDIgMzM3IDM1NFQzNTQgMzcyVDM2NyAzNzhRMzY4IDM3OCAzNjggMzc5UTM2OCAzODIgMzYxIDM4OFQzMzYgMzk5VDI5NyA0MDVRMjQ5IDQwNSAyMjcgMzc5VDIwNCAzMjZRMjA0IDMwMSAyMjMgMjkxVDI3OCAyNzRUMzMwIDI1OVEzOTYgMjMwIDM5NiAxNjNRMzk2IDEzNSAzODUgMTA3VDM1MiA1MVQyODkgN1QxOTUgLTEwUTExOCAtMTAgODYgMTlUNTMgODdRNTMgMTI2IDc0IDE0M1QxMTggMTYwUTEzMyAxNjAgMTQ2IDE1MVQxNjAgMTIwUTE2MCA5NCAxNDIgNzZUMTExIDU4UTEwOSA1NyAxMDggNTdUMTA3IDU1UTEwOCA1MiAxMTUgNDdUMTQ2IDM0VDIwMSAyN1EyMzcgMjcgMjYzIDM4VDMwMSA2NlQzMTggOTdUMzIzIDEyMlEzMjMgMTUwIDMwMiAxNjRUMjU0IDE4MVQxOTUgMTk2VDE0OCAyMzFRMTMxIDI1NiAxMzEgMjg5WiIgc3R5bGU9InN0cm9rZS13aWR0aDozOyIgLz48L2c+PGcgZGF0YS1tbWwtbm9kZT0ibWkiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDQwNTQuNiwwKSI+PHBhdGggZGF0YS1jPSIxRDQ0RiIgZD0iTTczIDY0N1E3MyA2NTcgNzcgNjcwVDg5IDY4M1E5MCA2ODMgMTYxIDY4OFQyMzQgNjk0UTI0NiA2OTQgMjQ2IDY4NVQyMTIgNTQyUTIwNCA1MDggMTk1IDQ3MlQxODAgNDE4TDE3NiAzOTlRMTc2IDM5NiAxODIgNDAyUTIzMSA0NDIgMjgzIDQ0MlEzNDUgNDQyIDM4MyAzOTZUNDIyIDI4MFE0MjIgMTY5IDM0MyA3OVQxNzMgLTExUTEyMyAtMTEgODIgMjdUNDAgMTUwVjE1OVE0MCAxODAgNDggMjE3VDk3IDQxNFExNDcgNjExIDE0NyA2MjNUMTA5IDYzN1ExMDQgNjM3IDEwMSA2MzdIOTZRODYgNjM3IDgzIDYzN1Q3NiA2NDBUNzMgNjQ3Wk0zMzYgMzI1VjMzMVEzMzYgNDA1IDI3NSA0MDVRMjU4IDQwNSAyNDAgMzk3VDIwNyAzNzZUMTgxIDM1MlQxNjMgMzMwTDE1NyAzMjJMMTM2IDIzNlExMTQgMTUwIDExNCAxMTRRMTE0IDY2IDEzOCA0MlExNTQgMjYgMTc4IDI2UTIxMSAyNiAyNDUgNThRMjcwIDgxIDI4NSAxMTRUMzE4IDIxOVEzMzYgMjkxIDMzNiAzMjVaIiBzdHlsZT0ic3Ryb2tlLXdpZHRoOjM7IiAvPjwvZz48ZyBkYXRhLW1tbC1ub2RlPSJtaSIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNDQ4My42LDApIj48cGF0aCBkYXRhLWM9IjFENDVEIiBkPSJNMjMgMjg3UTI0IDI5MCAyNSAyOTVUMzAgMzE3VDQwIDM0OFQ1NSAzODFUNzUgNDExVDEwMSA0MzNUMTM0IDQ0MlEyMDkgNDQyIDIzMCAzNzhMMjQwIDM4N1EzMDIgNDQyIDM1OCA0NDJRNDIzIDQ0MiA0NjAgMzk1VDQ5NyAyODFRNDk3IDE3MyA0MjEgODJUMjQ5IC0xMFEyMjcgLTEwIDIxMCAtNFExOTkgMSAxODcgMTFUMTY4IDI4TDE2MSAzNlExNjAgMzUgMTM5IC01MVQxMTggLTEzOFExMTggLTE0NCAxMjYgLTE0NVQxNjMgLTE0OEgxODhRMTk0IC0xNTUgMTk0IC0xNTdUMTkxIC0xNzVRMTg4IC0xODcgMTg1IC0xOTBUMTcyIC0xOTRRMTcwIC0xOTQgMTYxIC0xOTRUMTI3IC0xOTNUNjUgLTE5MlEtNSAtMTkyIC0yNCAtMTk0SC0zMlEtMzkgLTE4NyAtMzkgLTE4M1EtMzcgLTE1NiAtMjYgLTE0OEgtNlEyOCAtMTQ3IDMzIC0xMzZRMzYgLTEzMCA5NCAxMDNUMTU1IDM1MFExNTYgMzU1IDE1NiAzNjRRMTU2IDQwNSAxMzEgNDA1UTEwOSA0MDUgOTQgMzc3VDcxIDMxNlQ1OSAyODBRNTcgMjc4IDQzIDI3OEgyOVEyMyAyODQgMjMgMjg3Wk0xNzggMTAyUTIwMCAyNiAyNTIgMjZRMjgyIDI2IDMxMCA0OVQzNTYgMTA3UTM3NCAxNDEgMzkyIDIxNVQ0MTEgMzI1VjMzMVE0MTEgNDA1IDM1MCA0MDVRMzM5IDQwNSAzMjggNDAyVDMwNiAzOTNUMjg2IDM4MFQyNjkgMzY1VDI1NCAzNTBUMjQzIDMzNlQyMzUgMzI2TDIzMiAzMjJRMjMyIDMyMSAyMjkgMzA4VDIxOCAyNjRUMjA0IDIxMlExNzggMTA2IDE3OCAxMDJaIiBzdHlsZT0ic3Ryb2tlLXdpZHRoOjM7IiAvPjwvZz48L2c+PC9nPjwvc3ZnPg==)$`2Ln_{kv}d_{h}sbp`$。7B：L=32, n_kv=32(MHA), d_h=128, p=2。 单 token = 2×32×32×128×2 = 512KB。 总 = 512KB × 8192 × 16 ≈ 64GB。结论：远超权重（14GB），显存放不下，必须靠 PagedAttention + 量化 + 卸载等手段。

> **变形题**：换成 Llama-3-8B（GQA n_kv=8）算一遍 -\> 16GB（1/4）。考 GQA 对显存的影响。

### Q1.3 PagedAttention 解决了什么问题？借鉴了什么思想？⭐⭐⭐⭐⭐ [​](#q1-3-pagedattention-解决了什么问题-借鉴了什么思想-⭐⭐⭐⭐⭐)

**骨架：** 解决朴素连续分配的内部/外部碎片 + 无法共享。借鉴 OS 虚拟内存：固定大小物理块 + 块表（逻辑-\>物理）+ 按需分配 + 写时复制共享。显存利用率 20%~40% -\> 96%+。attention kernel 改造为按块表 gather。

### Q1.4 PagedAttention 的 block_size 大小如何取舍？⭐⭐⭐⭐ [​](#q1-4-pagedattention-的-block-size-大小如何取舍-⭐⭐⭐⭐)

**骨架：** 大-\>块表短、kernel 调度开销小，但内部碎片大、共享粒度粗；小-\>碎片小、共享细，但块表长、间接寻址开销大、kernel 效率受影响。默认 16 是经验折中。

### Q1.5 连续批处理 vs 静态批处理？⭐⭐⭐⭐⭐ [​](#q1-5-连续批处理-vs-静态批处理-⭐⭐⭐⭐⭐)

**骨架：** 静态：凑批后跑到最长序列结束，短序列空转 + padding。连续：iteration 级调度，每步可插入/踢出请求，配合分页免 padding，吞吐显著提升。开销在每步调度 + KV 分配释放 + kernel 重组（用 CUDA Graph 摊薄）。

### Q1.6 为什么 decode 阶段 MFU 很低？怎么提升？⭐⭐⭐⭐⭐ [​](#q1-6-为什么-decode-阶段-mfu-很低-怎么提升-⭐⭐⭐⭐⭐)

**骨架：** decode 是 memory-bound：每步只算 1 个新 token 的 Q（小 GEMV），却要把全量 KV 从 HBM 搬到 SM。算力闲置、带宽打满。提升：增大 batch 把多个 GEMV 拼成 GEMM 提高算力利用率（直到带宽或显存打满）、用 FlashAttention/FlashDecoding 降访存、投机解码减少串行步数、量化 KV 降带宽。

### Q1.7 prefill 和 decode 为什么是相反瓶颈？混部有什么问题？⭐⭐⭐⭐⭐ [​](#q1-7-prefill-和-decode-为什么是相反瓶颈-混部有什么问题-⭐⭐⭐⭐⭐)

**骨架：** prefill compute-bound（大 GEMM）、decode memory-bound（小 GEMV）。混部时 prefill 的大计算堵 decode（延迟 spike），decode 的小请求让 prefill 拼不大 batch（算力浪费）。解法：chunked prefill（单实例时间分片）/ PD 分离（跨实例物理分离）。

### Q1.8 chunked prefill 的 chunk size 怎么选？⭐⭐⭐⭐ [​](#q1-8-chunked-prefill-的-chunk-size-怎么选-⭐⭐⭐⭐)

**骨架：** 太大退化全量 prefill 卡 decode；太小 prefill 效率低 + launch 开销大。按"decode 延迟 SLO + prefill 吞吐"折中，常几百~上千 token。

### Q1.9 GQA/MQA/MLA 的区别与压缩比？⭐⭐⭐⭐⭐ [​](#q1-9-gqa-mqa-mla-的区别与压缩比-⭐⭐⭐⭐⭐)

**骨架：**

- GQA：多 query 头共享一组 KV，压缩比 = n_kv/n_h，质量近 MHA，主流。
- MQA：所有头共享一组 KV（n_kv=1），压缩最狠，质量略降。
- MLA：低秩压缩缓存 latent（d_c + d_rope），而非完整 K/V，压缩比可达数十倍（DeepSeek-V3 约 57x），质量保持。本质是"表示压缩"而非"结构共享"。

### Q1.10 MLA 为什么要把 RoPE 解耦？⭐⭐⭐⭐ [​](#q1-10-mla-为什么要把-rope-解耦-⭐⭐⭐⭐)

**骨架：** RoPE 对 K 注入位置旋转，破坏低秩可压缩性。MLA 把 K 拆 nope（可压进 latent c_KV）+ rope（k_pe，单独缓存不压缩），query 对应拆分。这样 latent 部分可低秩压缩，rope 部分保留位置信息。

### Q1.11 MLA 对推理引擎的工程影响？⭐⭐⭐⭐ [​](#q1-11-mla-对推理引擎的工程影响-⭐⭐⭐⭐)

**骨架：** 不能当普通 KV 处理：需 latent cache 专用 attention kernel（上投影 + 解耦 RoPE）、调度器要管理 latent 而非 K/V、TP 切分方式不同、分离式推理传输的是 latent（更小，反而是优势）。

### Q1.12 KV Cache 量化为什么 K 用 per-channel、V 用 per-token？⭐⭐⭐⭐ [​](#q1-12-kv-cache-量化为什么-k-用-per-channel、v-用-per-token-⭐⭐⭐⭐)

**骨架：** K 的离群值沿 channel 分布，per-channel 缩放更稳；V 相对平滑且逐 token 更新，per-token 利于在线。FP8（Hopper 原生）是工程甜点。

### Q1.13 什么是 attention sink？StreamingLLM 怎么工作？⭐⭐⭐⭐ [​](#q1-13-什么是-attention-sink-streamingllm-怎么工作-⭐⭐⭐⭐)

**骨架：** softmax 要把概率质量分配出去，序列开头几个 token 充当"注意力垃圾桶"吸走过量 attention。朴素滑窗丢弃 sink 会导致质量崩。StreamingLLM 保留 sink（前几个 token）+ 最近滑窗，固定显存流式生成超长序列。代价：窗口外内容无法回忆。

### Q1.14 RadixAttention 的收益场景与开销？⭐⭐⭐⭐⭐ [​](#q1-14-radixattention-的收益场景与开销-⭐⭐⭐⭐⭐)

**骨架：** 收益：任何共享前缀场景--多轮对话、并行采样、few-shot、结构化生成。命中率越高 prefill 省得越多。开销：树查找、节点维护、并发锁、占用 KV 不能淘汰给新请求（命中率低时反伤吞吐）。淘汰用 LRU + 引用计数。

### Q1.15 为什么要做 prefill-decode 分离？核心难点？⭐⭐⭐⭐⭐ [​](#q1-15-为什么要做-prefill-decode-分离-核心难点-⭐⭐⭐⭐⭐)

**骨架：** 二者瓶颈相反，混部互拖。分离后各自最优配置（prefill 多算力、decode 多带宽/显存），goodput 提升。难点：KV 跨实例传输（RDMA/带宽/延迟）、全局调度与路由、KV 池一致性与复用、容错。Mooncake 是 KVCache-centric 代表，把 KV 当全局可复用资源。

### Q1.16 TP=2 时每张卡 KV Cache 是原来的多少？为什么 DP 不能（单卡视角）减 KV？⭐⭐⭐⭐ [​](#q1-16-tp-2-时每张卡-kv-cache-是原来的多少-为什么-dp-不能-单卡视角-减-kv-⭐⭐⭐⭐)

**骨架：** 1/2（TP 按头切分，每卡只存自己头的 KV，不复制）。DP 是复制整模型到各组处理不同请求，单卡 KV 不变。所以 TP 能缓解单卡 KV 显存压力，DP 不能。

### Q1.17 投机解码对 KV Cache 有什么影响？⭐⭐⭐⭐ [​](#q1-17-投机解码对-kv-cache-有什么影响-⭐⭐⭐⭐)

**骨架：** draft 猜 k 个、target 并行验证。接受的 token KV 保留、拒绝的回滚丢弃，draft/target 各维护 KV。本质是用多余算力换串行 decode 步数减少，memory-bound 场景收益大。

### Q1.18 KV Cache 卸载到 CPU 什么时候划算？⭐⭐⭐ [​](#q1-18-kv-cache-卸载到-cpu-什么时候划算-⭐⭐⭐)

**骨架：** 代价是 PCIe 传输延迟/带宽。划算条件：显存受限需高并发、容忍较高单次延迟、且换入换出能与计算 overlap + 命中复用。否则传输成本 \> 收益。

------------------------------------------------------------------------

## 第 2 章 推理引擎与系统 [​](#第-2-章-推理引擎与系统)

### Q2.1 vLLM / SGLang / TensorRT-LLM 的定位与差异？⭐⭐⭐⭐⭐ [​](#q2-1-vllm-sglang-tensorrt-llm-的定位与差异-⭐⭐⭐⭐⭐)

**骨架：**

- **vLLM**：PagedAttention 起家，易用、社区大、模型覆盖广，研究与通用 serving 首选。
- **SGLang**：RadixAttention + 结构化生成 + 高性能调度，前缀复用/复杂控制流场景强，工程优化激进（CUDA Graph、overlap）。
- **TensorRT-LLM**：NVIDIA 官方，深度硬件协同、kernel 极致优化，吞吐/延迟最优但开发/定制门槛高、模型适配慢。

### Q2.2 设计一个 LLM serving 系统，画架构 ⭐⭐⭐⭐⭐（系统设计题，见第 5 章） [​](#q2-2-设计一个-llm-serving-系统-画架构-⭐⭐⭐⭐⭐-系统设计题-见第-5-章)

### Q2.3 连续批处理下如何处理请求优先级与抢占？⭐⭐⭐⭐ [​](#q2-3-连续批处理下如何处理请求优先级与抢占-⭐⭐⭐⭐)

**骨架：** 调度器按优先级排序 ready 队列；显存不足时**抢占**低优先级请求--将其 KV 换出到 CPU（swap）而非丢弃，高优先级完成后换回恢复。vLLM 的 preemption 机制即此。要权衡 swap 开销 vs 重算开销。

### Q2.4 如何度量推理系统性能？TTFT/TPOT/ITL/Goodput 各是什么？⭐⭐⭐⭐⭐ [​](#q2-4-如何度量推理系统性能-ttft-tpot-itl-goodput-各是什么-⭐⭐⭐⭐⭐)

**骨架：**

- **TTFT**（Time To First Token）：首 token 延迟，prefill 主导，影响体验。
- **TPOT**（Time Per Output Token）：单 token 平均生成时间，decode 主导。
- **ITL**（Inter-Token Latency）：相邻 token 间延迟，关注尾延迟抖动。
- **Goodput**：在满足 SLO（如 TTFT/TPOT 阈值）前提下的有效吞吐，比裸 throughput 更贴近线上价值。

### Q2.5 如何在不停服的情况下升级模型/引擎？⭐⭐⭐ [​](#q2-5-如何在不停服的情况下升级模型-引擎-⭐⭐⭐)

**骨架：** 蓝绿部署/灰度、权重热加载、KV Cache 是否可复用（同模型可复用，换模型不可）、长连接请求优雅 drain、多版本路由。分离式架构下 decode 实例可逐台滚动。

### Q2.6 长上下文（百万 token）推理的主要挑战？⭐⭐⭐⭐ [​](#q2-6-长上下文-百万-token-推理的主要挑战-⭐⭐⭐⭐)

**骨架：** KV Cache 显存爆炸（线性增长）、decode 访存线性增长变慢、attention O(n²) prefill 计算爆炸。解法：GQA/MLA 减 KV、量化、卸载/分层、sliding window/streaming、Ring Attention/CP 切分 attention、PD 分离 + KV 池复用。

------------------------------------------------------------------------

## 第 3 章 Attention 与算子 [​](#第-3-章-attention-与算子)

### Q3.1 FlashAttention 的核心思想？为什么快？⭐⭐⭐⭐⭐ [​](#q3-1-flashattention-的核心思想-为什么快-⭐⭐⭐⭐⭐)

**骨架：** 标准 attention 要把 N×N attention 矩阵写回 HBM，访存大。FlashAttention 用 **tiling（分块）+ online softmax**，在 SRAM 内分块计算、用数值稳定技巧增量算 softmax，避免实例化完整 N×N 矩阵，把 attention 从 HBM-bound 变 SRAM-bound。HBM 访问从 O(n²) 量级降到 O(n²·d²/M)（M=SRAM 大小，见原论文 Theorem 1）。不减 FLOPs，减访存。

### Q3.2 FlashAttention-2/3 改进了什么？⭐⭐⭐⭐ [​](#q3-2-flashattention-2-3-改进了什么-⭐⭐⭐⭐)

**骨架：** v2 优化了 GPU 占用率与 work partitioning（减少非 matmul 计算、更好的并行划分）。v3 针对 Hopper：用 TMA（异步拷贝）、FP8、warp-specialization（生产者-消费者）进一步压榨硬件。FlashDecoding 则针对 decode 场景沿 seq 维度切分并行。

### Q3.3 PagedAttention 的 kernel 和 FlashAttention 如何结合？⭐⭐⭐⭐ [​](#q3-3-pagedattention-的-kernel-和-flashattention-如何结合-⭐⭐⭐⭐)

**骨架：** PagedAttention 需按块表 gather 非连续 KV，在 FlashAttention 的 tiling 框架基础上增加按块索引取数、处理变长与共享块。vLLM 的 PagedAttention CUDA kernel 即此结合。

### Q3.4 写一个简单 attention kernel 要注意什么？（CUDA）⭐⭐⭐⭐ [​](#q3-4-写一个简单-attention-kernel-要注意什么-cuda-⭐⭐⭐⭐)

**骨架：** memory coalescing（连续线程访问连续地址）、shared memory tiling（K/V 分块进 SRAM）、online softmax 数值稳定、occupancy（block/grid 配置）、避免 bank conflict、异步拷贝（cp.async/TMA）。decode 场景 Q 小，重点在 K/V 复用与并行切分 seq。

### Q3.5 量化算子（FP8/INT8）的坑？⭐⭐⭐ [​](#q3-5-量化算子-fp8-int8-的坑-⭐⭐⭐)

**骨架：** 离群值导致精度崩（per-channel/per-token 缩放、smoothquant 平滑）、scale/dequant 的额外算力、硬件原生支持与否（Hopper FP8 原生）、混合精度（敏感层保留高精度）。

### Q3.6 reduce 类算子有哪些优化方案？（真实面经题）⭐⭐⭐⭐ [​](#q3-6-reduce-类算子有哪些优化方案-真实面经题-⭐⭐⭐⭐)

> 来源：[百融云创 AI Infra 面经](https://www.nowcoder.com/discuss/724396208503947264)。

**骨架：** reduce（求和/最大/均值等）是 CUDA 经典优化题，层次化展开：

1.  **朴素版**：单 block 顺序累加，串行瓶颈。
2.  **共享内存 + 分块**：block 内先各自加载到 shared memory，分块并行 reduce。
3.  **解决 bank conflict**：步长访问避免 32 路 bank 冲突，调整索引模式。
4.  **warp 级 reduce**：用 `__shfl_down_sync` / `__shfl_xor_sync` 在寄存器内做 warp 内 reduce，免走 shared memory，最内层最快。
5.  **树形 vs 交错（pairwise）**：交错式（相邻配对）访存连续、利于 coalescing，优于朴素树形。
6.  **展开最后一个 warp**：当剩余数据 ≤ warp 大小时，展开循环避免同步开销。
7.  **针对 shape 优化**：大 N 用多 block + 最终 block 间 reduce（atomic 或二次 kernel）；小 N 少 launch 开销。第一维 reduce 还是最后一维 reduce 影响访存连续性（尽量沿连续维度 reduce）。

**追问点**：warp shuffle 为什么比 shared memory 快（免访存、无 bank conflict）；block 间 reduce 用 atomic 还是两段 kernel（两段更稳）；reduce 维度选择对 coalescing 的影响。

------------------------------------------------------------------------

## 第 4 章 分布式与通信 [​](#第-4-章-分布式与通信)

### Q4.1 TP/PP/DP/EP/CP 各切什么？⭐⭐⭐⭐⭐ [​](#q4-1-tp-pp-dp-ep-cp-各切什么-⭐⭐⭐⭐⭐)

**骨架：**

- **DP**：数据并行，各卡完整模型处理不同 batch，梯度 all-reduce。
- **TP**：张量并行，单层权重按头/维切到多卡，每层 all-reduce。
- **PP**：流水并行，按层切到多 stage，micro-batch 流水，有 bubble。
- **EP**：专家并行，MoE 专家分布到多卡，token 路由 all-to-all。
- **CP**：上下文并行，长序列 attention 沿 seq 切分（Ring/Ulysses Attention）。

### Q4.2 TP 为什么能减单卡 KV Cache？通信开销？⭐⭐⭐⭐ [​](#q4-2-tp-为什么能减单卡-kv-cache-通信开销-⭐⭐⭐⭐)

**骨架：** TP 按头切，每卡只存自己头的 KV，单卡 KV 按 TP 等比缩小、不复制。代价：每层 attention 后 all-reduce 输出，通信量正比 hidden×batch×seq，随层数线性增加。TP 过大会通信主导，通常 2~8。

### Q4.3 流水并行 bubble 怎么产生？怎么减？⭐⭐⭐⭐ [​](#q4-3-流水并行-bubble-怎么产生-怎么减-⭐⭐⭐⭐)

**骨架：** PP 前/后向有依赖，micro-batch 间形成空档（bubble）。减法：增多 micro-batch（1F1B 调度）、interleaved schedule（把每 stage 再分虚拟层交错）、零气泡（ZB-H1/2/3 把 bubble 用独立反向补）。

### Q4.4 NCCL all-reduce 的实现（Ring）原理？⭐⭐⭐⭐ [​](#q4-4-nccl-all-reduce-的实现-ring-原理-⭐⭐⭐⭐)

**骨架：** Ring all-reduce：节点成环，分 chunk 沿环传递并累加，N-1 步完成 reduce-scatter，再 N-1 步 all-gather。通信量 2(N-1)·data/N，带宽利用率高。大规模下用 tree+ring 混合、拓扑感知。

### Q4.5 通信与计算如何 overlap？⭐⭐⭐⭐ [​](#q4-5-通信与计算如何-overlap-⭐⭐⭐⭐)

**骨架：** 把通信拆成可异步块，用独立 stream/CUDA stream 与计算 stream 并发；梯度分桶 all-reduce（bucket）与反向计算重叠；PP 用插Bubble 填通信。关键：通信量/算力配比、避免同步点。

### Q4.6 Ring Attention / CP 如何支持超长上下文？⭐⭐⭐ [​](#q4-6-ring-attention-cp-如何支持超长上下文-⭐⭐⭐)

**骨架：** 把 seq 切到多卡，每卡持有一段 Q 和对应 KV，K/V 块沿环传递，每卡增量计算 attention。显存与计算分摊到多卡，支持超长。代价：环形通信延迟、负载/顺序敏感。

------------------------------------------------------------------------

## 第 5 章 系统设计题 [​](#第-5-章-系统设计题)

> 完整工作示例（含架构图与权衡分析）见 [系统设计专题](./aiinfra_system_design.html)。本章给框架骨架。

### Q5.1 设计一个支持高并发的 LLM 推理服务（端到端）⭐⭐⭐⭐⭐ [​](#q5-1-设计一个支持高并发的-llm-推理服务-端到端-⭐⭐⭐⭐⭐)

**答题框架（按此结构展开）：**

1.  **澄清需求**：QPS、SLO（TTFT/TPOT/P99）、上下文长度、模型规模、是否多模态、是否多租户、预算。
2.  **整体架构**：网关/负载均衡 -\> 调度器 -\> 推理引擎集群（prefill 池 + decode 池，PD 分离）-\> KV Cache 池 -\> 模型权重存储 -\> 监控。
3.  **核心组件**：
    - 调度器：连续批处理 + 优先级 + 抢占；prefill/decode 路由。
    - KV Cache：PagedAttention 分页 + 前缀缓存/RadixAttention + 量化 + 分层卸载。
    - 分离式：prefill 算完 KV 传给 decode 池（RDMA/压缩/overlap）。
    - 多租户：显存配额、KV 隔离、优先级、公平调度。
4.  **瓶颈与优化**：decode memory-bound-\>大 batch/量化/投机解码；长上下文-\>CP/卸载/MLA；TTFT-\>chunked prefill。
5.  **可靠与运维**：滚动升级、故障转移、热加载、监控（goodput/尾延迟/OOM）。
6.  **成本**：batch 提升利用率、分离式按画像配比、KV 复用减少重算。

> 面试官常追问：TTFT 怎么降？显存不够怎么办？怎么支持百万 context？怎么计费/隔离？--每个都对应上面一个组件。

### Q5.2 设计 KV Cache 池化服务（Mooncake 风格）⭐⭐⭐⭐ [​](#q5-2-设计-kv-cache-池化服务-mooncake-风格-⭐⭐⭐⭐)

**骨架：** KV 作为全局资源：prefill 实例产出 KV -\> 写入全局池（DRAM+SSD 分层）-\> decode 实例按需取。命中即跳过 prefill。设计：全局索引（前缀-\>KV 位置）、LRU 淘汰、引用计数、传输压缩（MLA latent 天然小）、路由与负载均衡、一致性（copy-on-write）。难点：传输带宽、池容量规划、命中率建模。

### Q5.3 如何把一个新模型接入推理引擎？⭐⭐⭐⭐ [​](#q5-3-如何把一个新模型接入推理引擎-⭐⭐⭐⭐)

**骨架：** 模型结构适配（attention 类型：MHA/GQA/MLA、MoE 路由、位置编码）、权重转换与分片（TP/PP）、attention kernel 适配（paged/MLA）、调度器适配（KV 布局）、量化支持、benchmark 验证精度与性能。MLA/MoE 类新结构是工程难点。

### Q5.4 如何优化线上推理成本？⭐⭐⭐⭐ [​](#q5-4-如何优化线上推理成本-⭐⭐⭐⭐)

**骨架：** 提利用率（连续批处理/大 batch/PD 分离）、KV 复用（prefix/radix/池化）减少重算、量化（W8A8/FP8/INT4 权重 + KV 量化）、投机解码减步数、speculative + PD 分离组合、按峰谷弹性扩缩、硬件选型（性价比芯片/ spot）。

------------------------------------------------------------------------

## 第 6 章 Coding 与算法 [​](#第-6-章-coding-与算法)

> AI Infra 岗的 coding 轮通常不如纯算法岗难，但**会考系统/并行相关**。

### 高频类型 [​](#高频类型)

1.  **手写 attention**（Python/CUDA 简化版）：考察对 attention 计算与访存的理解。
2.  **手写 PagedAttention 简化逻辑**：块表、按块 gather、变长。
3.  **调度器模拟**：给定请求流，模拟连续批处理下每步 batch 组成与显存占用。
4.  **LRU / 引用计数 / Radix Tree**：KV 缓存淘汰与共享数据结构。
5.  **经典 LeetCode**（中等为主）：数组/字符串/DP/图，部分公司考 Hard。

### 例题骨架 [​](#例题骨架)

- **LRU Cache**（LeetCode 146）：哈希表 + 双向链表，O(1) get/put。RadixAttention 淘汰的基础。
- **模拟连续批处理**：维护 ready 队列 + 显存预算，每步选能放下的请求拼 batch，处理生成/完成/抢占。考的是把调度逻辑写清楚。
- **手写 scaled dot-product attention**：含 mask、causal、数值稳定 softmax。常要求解释复杂度与访存。

------------------------------------------------------------------------

## 第 7 章 公司面经碎片（\[实时核对\]，结构化归纳） [​](#第-7-章-公司面经碎片-实时核对-结构化归纳)

> 以下为多家公司 AI Infra/推理方向面经的**共性高频点**归纳，非逐字原题。具体原题与时间请查实时渠道。 **7.0 节为 2026-08-12 实时抓取自牛客的真实面经帖**（链接已核实可达），可作最新风向参考。

### 7.0 真实面经（2026-08-12 抓取自牛客，✅ 链接已核实） [​](#_7-0-真实面经-2026-08-12-抓取自牛客-✅-链接已核实)

| 公司/岗位 | 帖子 | 抓取到的真实考点 |
|----|----|----|
| 快手 · AI Infra（2026 校招） | [nowcoder 904326953174323200](https://www.nowcoder.com/discuss/904326953174323200) | 访存优化：局部性原理(时间/空间)、数据结构重排(SoA/AoS)、cache line alignment、prefetching、循环优化(tiling/循环融合) |
| 美团 · 北斗大模型 | [nowcoder 914814345970782208](https://www.nowcoder.com/discuss/914814345970782208) | LoRA 微调原理；SFT loss 如何只算回答部分(忽略 padding token)；Attention 显存优化策略(KV Cache 复用、batch 拼接)；分布式训练 Zero-… |
| 百融云创 · AI Infra（已口头 offer） | [nowcoder 724396208503947264](https://www.nowcoder.com/discuss/724396208503947264) | 4 轮技术+HR 全流程；**"reduce 类算子有哪些优化方案？"**（warp shuffle/共享内存/分块/向量化）；针对 shape 的优化讨论 |
| 华为海思 · 图灵业务部 ai-infra | [nowcoder 899808901892239360](https://www.nowcoder.com/discuss/899808901892239360) | AI 算子开发方向；一面专业面；偏软硬协同 |
| 面试题（KV Cache 专题） | [nowcoder 831225479913865216](https://www.nowcoder.com/discuss/831225479913865216) | **"KV Cache 在训练和推理中的差异是什么？加速价值多大？吞吐与延迟如何权衡？"**（结合 vLLM）--典型深挖题 |
| 系统设计题 | [nowcoder 831226141108097024](https://www.nowcoder.com/discuss/831226141108097024) | **"大模型项目从架构角度怎么搭？模型选型(开/闭源)、推理框架(vLLM/TensorRT-LLM/自研)如何选？"** |

**资源帖（同期抓取）：**

- [AI-Compass：LLM 推理框架+部署生态（vLLM/SGLang/LMDeploy 对比）](https://www.nowcoder.com/discuss/776560660057464832)
- [LLM 必知必会(十二)：vLLM 性能飞跃部署实践](https://www.nowcoder.com/discuss/626190790787690496)

> 启示：2026 校招中，**访存优化（cache line/SoA-AoS/tiling）**、**KV Cache 训练vs推理差异+吞吐延迟权衡**、**推理框架选型系统设计**是高频出现的实题，与本 Wiki [第 1 章 KV Cache](#第-1-章-kv-cache-专题)、[第 3 章 Attention/算子](#第-3-章-attention-与算子)、[系统设计专题](./aiinfra_system_design.html) 高度对应。建议把上述帖子逐篇精读，原题回填本节。

### 7.1 头部大模型公司（DeepSeek / Moonshot / 智谱 类） [​](#_7-1-头部大模型公司-deepseek-moonshot-智谱-类)

- **几乎必考自家架构**：DeepSeek 考 MLA 原理与压缩比推导、MoE 路由；Moonshot 考长上下文 KV 管理、Mooncake 分离式与 KV 池；智谱考 SGLang 协同与 GLM 系列结构。
- **深挖源码**：问 vLLM/SGLang 调度器、PagedAttention 细节、kernel 实现。
- **系统设计**：设计分离式推理、KV 池化、长上下文服务。
- **手撕**：attention / 简化 PagedAttention / 调度模拟。

### 7.2 大厂（字节/阿里/腾讯/华为 类） [​](#_7-2-大厂-字节-阿里-腾讯-华为-类)

- **广度 + 工程化**：分布式（TP/PP/EP/CP）、NCCL、通信 overlap、流水 bubble。
- **线上系统**：多租户、抢占、滚动升级、监控、成本。
- **算子**：CUDA 基础、FlashAttention 原理、量化算子。
- **Coding**：中等 LeetCode + 手撕 attention。
- **华为/昇腾**：软硬协同、芯片侧算子适配、与 NVIDIA 生态差异。

### 7.3 芯片厂（NVIDIA/AMD/国产芯片 类） [​](#_7-3-芯片厂-nvidia-amd-国产芯片-类)

- **重 kernel/编译**：CUDA/Triton 实战、CUTLASS、GPU 微架构（warp/shared mem/TMA/async）、profiling（Nsight）、图编译（TRT/XLA/MLIR）。
- **算子优化**：给一个低效 kernel 让你优化，讲 occupancy/coalescing/tiling。
- **KV Cache 相关**：paged/MLA/FP8 算子的硬件实现。

### 7.4 海外（NVIDIA/Meta/Microsoft/Together 类） [​](#_7-4-海外-nvidia-meta-microsoft-together-类)

- 英文沟通 + 系统设计 + coding（中等~难）。
- 重视开源贡献与论文（vLLM/FlashAttention/Megatron 贡献是强加分）。
- 系统设计题偏大：跨区域 serving、成本、容错。

------------------------------------------------------------------------

## 第 8 章 行为面与文化匹配（常被忽视） [​](#第-8-章-行为面与文化匹配-常被忽视)

- 为什么从原方向转 AI Infra？（讲清动机与迁移能力）
- 做过的最有挑战的 infra 项目？（STAR：情境-任务-行动-结果，量化收益）
- 与算法/产品方协作的冲突？（沟通与权衡）
- 对某开源项目（vLLM/SGLang）的看法/贡献？（技术品味）
- 对加班/oncall 的态度、稳定性期望。（双向选择）

------------------------------------------------------------------------

## 第 9 章 反直觉判断题（深挖区分度）⭐⭐⭐⭐ [​](#第-9-章-反直觉判断题-深挖区分度-⭐⭐⭐⭐)

> 面试官爱用这类题压人：第一反应的答案往往是错的。判断 + 给理由。

- **"增大 batch 一定提升 decode 吞吐吗？"** ❌ 不一定。decode memory-bound，batch 增大先把多个小 GEMV 拼成大 GEMM 提升利用率-\>吞吐升；但到 HBM 带宽打满后吞吐见顶，再增 batch 只会撑爆 KV Cache 显存、触发 swap/抢占，反而掉速。
- **"PagedAttention 减少计算量吗？"** ❌ 不减。它优化的是显存利用率与共享，计算量基本不变（kernel 间接寻址还略增开销）。
- **"KV Cache 卸载到 CPU 一定更省/更快吗？"** ❌ 不一定。PCIe 传输有延迟与带宽成本，必须与计算 overlap 且命中复用才划算；否则传输 \> 收益。
- **"MLA 的 latent 能直接当普通 KV 喂给标准 attention kernel 吗？"** ❌ 不能。需上投影 + 解耦 RoPE 专用 kernel（或吸收技巧），否则语义错误。
- **"TP 越大越好吗？"** ❌ 不。TP 每层 all-reduce 通信随卡数线性增，过大通信主导算力；通常 2~8 为宜，再大上 PP/EP。
- **"投机解码总是加速吗？"** ❌ 不。draft 接受率低、prefill 占比高、或算力已打满时不赚甚至亏（多余验证算力）。
- **"GQA 质量一定比 MHA 差吗？"** ❌ 在主流规模上几乎无损，Llama-3/Qwen2 全用 GQA；只有极端小模型/细粒度任务可能略降。
- **"StreamingLLM 能真正记住百万 token 全部内容吗？"** ❌ 不能。只保留 sink + 近窗，窗口外内容不可回忆；它是"流式不崩"，不是"全量记忆"。
- **"前缀缓存命中率低时也无害吧？"** ❌ 有害。索引维护、占用的 KV 不能淘汰给新请求，命中率低时反而降吞吐；需动态退化为不缓存。
- **"量化 KV Cache 用 INT8 一定比 FP8 省更多吗？"** ❌ 同为 8bit 时显存一样省；FP8 在 Hopper 上原生计算、精度损失更小，工程上常优于 INT8。
- **"连续批处理能减少单 token 的计算量吗？"** ❌ 不能。它提升的是利用率/吞吐，单 token 计算量不变。
- **"PD 分离后 prefill 和 decode 就互不影响了？"** ❌ 仍有 KV 传输耦合：prefill 产 KV、decode 消费 KV，传输带宽与路由调度是新的耦合点与瓶颈。

------------------------------------------------------------------------

## 复习建议 [​](#复习建议)

- 先把第 1 章 KV Cache 专题吃透（本 Wiki 技术主线），这是最高频也是最能拉开差距的。
- 第 5 章系统设计要**能画图讲满 20 分钟**，反复练。
- 第 3、4 章按目标公司侧重取舍：大模型公司重第 3 章+源码，大厂重第 4 章+工程，芯片厂重第 3 章 kernel。
- 第 6 章 coding 每天 1-2 题保持手感，重点练 attention/调度/LRU 类。

------------------------------------------------------------------------

## 附录 A：参考代码（手撕对照） [​](#附录-a-参考代码-手撕对照)

> 仅供复习对照，面试时用自己话写。简化版，省略边界处理与性能优化。

### A.1 Scaled Dot-Product Attention（含 causal mask，numpy） [​](#a-1-scaled-dot-product-attention-含-causal-mask-numpy)

python

``` shiki
import numpy as np

def softmax(x, axis=-1):
    x = x - np.max(x, axis=axis, keepdims=True)   # 数值稳定
    e = np.exp(x)
    return e / np.sum(e, axis=axis, keepdims=True)

def attention(Q, K, V, mask=None):
    # Q: (n_q, d), K: (n_kv, d), V: (n_kv, d_v)
    d = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d)            # (n_q, n_kv)
    if mask is not None:
        scores = np.where(mask == 0, -1e9, scores)
    attn = softmax(scores, axis=-1)          # (n_q, n_kv)
    return attn @ V                          # (n_q, d_v)

def causal_mask(n):
    return np.tril(np.ones((n, n)))          # 下三角为 1

# 用法：单条序列 self-attention，Q=K=V=X（投影后）
n, d = 8, 64
X = np.random.randn(n, d)
out = attention(X, X, X, mask=causal_mask(n))
```

1  
2  
3  
4  
5  
6  
7  
8  
9  
10  
11  
12  
13  
14  
15  
16  
17  
18  
19  
20  
21  
22  
23  

### A.2 带 KV Cache 的 Decode 单步 [​](#a-2-带-kv-cache-的-decode-单步)

python

``` shiki
def decode_step(x_new, Wq, Wk, Wv, Wo, kv_cache, pos):
    # x_new: (1, d)  当前新 token 的 hidden
    # kv_cache: dict{'K': (t, d), 'V': (t, d)}  历史缓存
    q = x_new @ Wq                          # (1, d)
    k_new = x_new @ Wk                      # (1, d)
    v_new = x_new @ Wv                      # (1, d)
    # 追加到 cache
    K = np.concatenate([kv_cache['K'], k_new], axis=0)   # (t+1, d)
    V = np.concatenate([kv_cache['V'], v_new], axis=0)   # (t+1, d)
    kv_cache['K'], kv_cache['V'] = K, V
    # attention：当前 q 对全部历史 K/V（decode 无需 causal，因为只看历史+自己）
    out = attention(q, K, V)                # (1, d)
    return out @ Wo, kv_cache

# 对比：不用 cache 时每步要重算全部历史 K/V -> O(t)；用 cache 只算新 token -> O(1) 新计算
```

1  
2  
3  
4  
5  
6  
7  
8  
9  
10  
11  
12  
13  
14  
15  

### A.3 PagedAttention 块表 gather（简化 numpy 语义） [​](#a-3-pagedattention-块表-gather-简化-numpy-语义)

python

``` shiki
# 物理块池：每个块存 block_size 个 token 的 KV
block_size = 4
pool_K = {}   # physical_block_id -> (block_size, d)
pool_V = {}

def gather_kv(block_table, seq_len):
    # block_table: list[int]  逻辑块号 -> 物理块号
    # 按 block_table 把该请求的 KV 拼成连续逻辑序列
    Ks, Vs = [], []
    for logical, physical in enumerate(block_table):
        blk_K = pool_K[physical]            # (block_size, d)
        blk_V = pool_V[physical]
        Ks.append(blk_K); Vs.append(blk_V)
    K = np.concatenate(Ks, axis=0)[:seq_len]   # 截断到实际长度
    V = np.concatenate(Vs, axis=0)[:seq_len]
    return K, V
# 关键：物理上不连续（pool 中任意位置），靠 block_table 映射成逻辑连续
# 共享：两个请求前缀相同 -> block_table 指向同一组物理块（引用计数）
# 分叉：要写新 token 时 copy-on-write，复制该块再写
```

1  
2  
3  
4  
5  
6  
7  
8  
9  
10  
11  
12  
13  
14  
15  
16  
17  
18  
19  

### A.4 LRU Cache（RadixAttention 淘汰基础，LeetCode 146） [​](#a-4-lru-cache-radixattention-淘汰基础-leetcode-146)

python

``` shiki
class Node:
    def __init__(self, key=None, val=None):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.mp = {}                        # key -> Node
        self.head = Node()                  # 哨兵：最近用
        self.tail = Node()                  # 哨兵：最久未用
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, n):
        n.prev.next = n.next
        n.next.prev = n.prev

    def _add_front(self, n):
        n.next = self.head.next
        n.prev = self.head
        self.head.next.prev = n
        self.head.next = n

    def get(self, key):
        if key not in self.mp: return -1
        n = self.mp[key]
        self._remove(n); self._add_front(n)  # 提到最近
        return n.val

    def put(self, key, val):
        if key in self.mp:
            self.mp[key].val = val
            self._remove(self.mp[key]); self._add_front(self.mp[key])
            return
        n = Node(key, val)
        self.mp[key] = n
        self._add_front(n)
        if len(self.mp) > self.cap:
            lru = self.tail.prev             # 淘汰最久未用
            self._remove(lru)
            del self.mp[lru.key]
```

1  
2  
3  
4  
5  
6  
7  
8  
9  
10  
11  
12  
13  
14  
15  
16  
17  
18  
19  
20  
21  
22  
23  
24  
25  
26  
27  
28  
29  
30  
31  
32  
33  
34  
35  
36  
37  
38  
39  
40  
41  
42  

> 练习目标：A.1/A.2 能 10 分钟内默写无误；A.3 能讲清块表语义；A.4 是 LeetCode 146，3 分钟默写。能默写这些，"手撕"轮基本稳。

------------------------------------------------------------------------

下一篇：[系统设计专题](./aiinfra_system_design.html)。
