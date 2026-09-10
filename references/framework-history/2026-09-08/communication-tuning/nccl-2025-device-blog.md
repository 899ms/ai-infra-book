<!-- 从 nccl-2025-device-blog.html 迁移的资料快照；原始 HTML SHA-256: be1d31f4e052a7985a258cc6a3008f9e064f83b6c41401ba272396081b884f03。 -->

[Networking / Communications](https://developer.nvidia.com/blog/category/networking-communications/)

English中文

# Fusing Communication and Compute with New Device API and Copy Engine Collectives in NVIDIA NCCL 2.28

![](https://developer-blogs.nvidia.com/wp-content/uploads/2025/07/NVIDIA-NCCL-technical-blog-png.webp)

Nov 10, 2025

By [Sylvain Jeaugey](https://developer.nvidia.com/blog/author/sjeaugey/ "Posts by Sylvain Jeaugey"), [John Bachan](https://developer.nvidia.com/blog/author/jbachan/ "Posts by John Bachan"), [Pak Markthub](https://developer.nvidia.com/blog/author/pmarkthub/ "Posts by Pak Markthub"), [Zhenhao He](https://developer.nvidia.com/blog/author/zhenhaoh/ "Posts by Zhenhao He"), [Sirshak Das](https://developer.nvidia.com/blog/author/sirshakd/ "Posts by Sirshak Das") and [Farshad Ghodsian](https://developer.nvidia.com/blog/author/farshadghodsian/ "Posts by Farshad Ghodsian")

Like

[ Discuss (0)](#entry-content-comments)

- [L](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Ffusing-communication-and-compute-with-new-device-api-and-copy-engine-collectives-in-nvidia-nccl-2-28%2F)
- [T](https://twitter.com/intent/tweet?text=Fusing+Communication+and+Compute+with+New+Device+API+and+Copy+Engine+Collectives+in+NVIDIA+NCCL+2.28+%7C+NVIDIA+Technical+Blog+https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Ffusing-communication-and-compute-with-new-device-api-and-copy-engine-collectives-in-nvidia-nccl-2-28%2F)
- [F](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Ffusing-communication-and-compute-with-new-device-api-and-copy-engine-collectives-in-nvidia-nccl-2-28%2F)
- [R](https://www.reddit.com/submit?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Ffusing-communication-and-compute-with-new-device-api-and-copy-engine-collectives-in-nvidia-nccl-2-28%2F&title=Fusing+Communication+and+Compute+with+New+Device+API+and+Copy+Engine+Collectives+in+NVIDIA+NCCL+2.28+%7C+NVIDIA+Technical+Blog)
- [E](mailto:?subject=I'd%20like%20to%20share%20a%20link%20with%20you&body=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Ffusing-communication-and-compute-with-new-device-api-and-copy-engine-collectives-in-nvidia-nccl-2-28%2F)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibnYtYWktc3VtbWFyeV9faWNvbiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iMjUiIGhlaWdodD0iMjUiIHZpZXdib3g9IjAgMCAyNSAyNSIgZmlsbD0ibm9uZSIgYXJpYS1oaWRkZW49InRydWUiPgogICAgICAgICAgICAgICAgPHBhdGggZmlsbD0iY3VycmVudENvbG9yIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTIyLjQ5MTUgMTUuMzAxOUMyMi4yOTQgMTUuMzA0NyAyMi4wOTc2IDE1LjMzMTYgMjEuOTA2NiAxNS4zODE5TDIwLjI1NCAxMi45MDE5TDIxLjkwNSAxMC40MjE5QzIyLjA5NjcgMTAuNDczMSAyMi4yOTMzIDEwLjQ5ODcgMjIuNDkxNSAxMC41MDE5QzIyLjg4NDQgMTAuNTAzMiAyMy4yNzE2IDEwLjQwNzggMjMuNjE5IDEwLjIyNDFDMjMuOTY2NSAxMC4wNDA0IDI0LjI2MzUgOS43NzQwNSAyNC40ODM5IDkuNDQ4NDVDMjQuNzA0NCA5LjEyMjg1IDI0Ljg0MTUgOC43NDc5OSAyNC44ODMyIDguMzU2ODdDMjQuOTI1IDcuOTY1NzUgMjQuODcwMSA3LjU3MDM1IDI0LjcyMzMgNy4yMDU0N0MyNC41NzY2IDYuODQwNTkgMjQuMzQyNSA2LjUxNzQxIDI0LjA0MTcgNi4yNjQzN0MyMy43NDA5IDYuMDExMzQgMjMuMzgyNSA1LjgzNjIgMjIuOTk4MiA1Ljc1NDM3QzIyLjYxMzkgNS42NzI1NSAyMi4yMTU0IDUuNjg2NTQgMjEuODM3OCA1Ljc5NTEyQzIxLjQ2MDEgNS45MDM3IDIxLjExNDkgNi4xMDM1NCAyMC44MzI2IDYuMzc3MDZMMTUuMjcwOSAzLjU5MzA1QzE1LjI4NjggMy40OTcwNSAxNS4yOTY0IDMuMzk5NDYgMTUuMjk5NiAzLjMwMTg2QzE1LjI5OTYgMi42NjUzNCAxNS4wNDcxIDIuMDU0ODkgMTQuNTk3NSAxLjYwNDhDMTQuMTQ3OSAxLjE1NDcxIDEzLjUzODEgMC45MDE4NTUgMTIuOTAyMyAwLjkwMTg1NUMxMi4yNjY1IDAuOTAxODU1IDExLjY1NjggMS4xNTQ3MSAxMS4yMDcyIDEuNjA0OEMxMC43NTc2IDIuMDU0ODkgMTAuNTA1MSAyLjY2NTM0IDEwLjUwNTEgMy4zMDE4NkMxMC41MDgzIDMuMzk5NDYgMTAuNTE3OCAzLjQ5NzA1IDEwLjUzMzggMy41OTMwNUw0Ljk3MjExIDYuMzc3MDZDNC42ODk3NiA2LjEwMjY3IDQuMzQ0MzMgNS45MDIwMiAzLjk2NjI2IDUuNzkyODFDMy41ODgxOCA1LjY4MzYgMy4xODkwOCA1LjY2OTE4IDIuODA0MTIgNS43NTA4MkMyLjQxOTE2IDUuODMyNDUgMi4wNjAxOCA2LjAwNzY0IDEuNzU4OCA2LjI2MDkzQzEuNDU3NDMgNi41MTQyMyAxLjIyMjkyIDYuODM3ODYgMS4wNzU5NSA3LjIwMzI5QzAuOTI4OTgxIDcuNTY4NzIgMC44NzQwNTggNy45NjQ3NCAwLjkxNjAyOCA4LjM1NjQ0QzAuOTU3OTk4IDguNzQ4MTMgMS4wOTU1NyA5LjEyMzQ4IDEuMzE2NjIgOS40NDkzOUMxLjUzNzY3IDkuNzc1MyAxLjgzNTQgMTAuMDQxOCAyLjE4MzU4IDEwLjIyNTNDMi41MzE3NiAxMC40MDg4IDIuOTE5NyAxMC41MDM4IDMuMzEzMTkgMTAuNTAxOUMzLjUxMTM2IDEwLjQ5ODcgMy43MDc5NCAxMC40NzE1IDMuODk4MTMgMTAuNDIxOUw1LjU1MDY2IDEyLjkwMTlMMy44OTk3MyAxNS4zODE5QzMuNzA4MTggMTUuMzMxNCAzLjUxMTIyIDE1LjMwNDYgMy4zMTMxOSAxNS4zMDE5QzIuOTIwMjkgMTUuMzAwNSAyLjUzMzA4IDE1LjM5NTkgMi4xODU2NSAxNS41Nzk2QzEuODM4MjIgMTUuNzYzMyAxLjU0MTIyIDE2LjAyOTcgMS4zMjA3NyAxNi4zNTUzQzEuMTAwMzIgMTYuNjgwOSAwLjk2MzE4OSAxNy4wNTU3IDAuOTIxNDQyIDE3LjQ0NjhDMC44Nzk2OTUgMTcuODM4IDAuOTM0NjEzIDE4LjIzMzQgMS4wODEzNiAxOC41OTgyQzEuMjI4MTEgMTguOTYzMSAxLjQ2MjE5IDE5LjI4NjMgMS43NjMwMSAxOS41MzkzQzIuMDYzODIgMTkuNzkyNCAyLjQyMjE1IDE5Ljk2NzUgMi44MDY0NiAyMC4wNDkzQzMuMTkwNzcgMjAuMTMxMiAzLjU4OTI4IDIwLjExNzIgMy45NjY5MSAyMC4wMDg2QzQuMzQ0NTUgMTkuOSA0LjY4OTc0IDE5LjcwMDIgNC45NzIxMSAxOS40MjY3TDEwLjUzMzggMjIuMjEwN0MxMC41MTc4IDIyLjMwNjcgMTAuNTA4MyAyMi40MDQzIDEwLjUwNTEgMjIuNTAxOUMxMC41MDUxIDIzLjEzODQgMTAuNzU3NiAyMy43NDg4IDExLjIwNzIgMjQuMTk4OUMxMS42NTY4IDI0LjY0OSAxMi4yNjY1IDI0LjkwMTkgMTIuOTAyMyAyNC45MDE5QzEzLjUzODEgMjQuOTAxOSAxNC4xNDc5IDI0LjY0OSAxNC41OTc1IDI0LjE5ODlDMTUuMDQ3MSAyMy43NDg4IDE1LjI5OTYgMjMuMTM4NCAxNS4yOTk2IDIyLjUwMTlDMTUuMjk1OCAyMi40MDQzIDE1LjI4NjIgMjIuMzA3MSAxNS4yNzA5IDIyLjIxMDdMMjAuODMyNiAxOS40MjY3QzIxLjExNDkgMTkuNzAxIDIxLjQ2MDQgMTkuOTAxNyAyMS44Mzg0IDIwLjAxMDlDMjIuMjE2NSAyMC4xMjAxIDIyLjYxNTYgMjAuMTM0NSAyMy4wMDA2IDIwLjA1MjlDMjMuMzg1NSAxOS45NzEzIDIzLjc0NDUgMTkuNzk2MSAyNC4wNDU5IDE5LjU0MjhDMjQuMzQ3MyAxOS4yODk1IDI0LjU4MTggMTguOTY1OSAyNC43Mjg3IDE4LjYwMDRDMjQuODc1NyAxOC4yMzUgMjQuOTMwNiAxNy44MzkgMjQuODg4NyAxNy40NDczQzI0Ljg0NjcgMTcuMDU1NiAyNC43MDkxIDE2LjY4MDIgMjQuNDg4MSAxNi4zNTQzQzI0LjI2NyAxNi4wMjg0IDIzLjk2OTMgMTUuNzYxOSAyMy42MjExIDE1LjU3ODRDMjMuMjcyOSAxNS4zOTQ5IDIyLjg4NSAxNS4yOTk5IDIyLjQ5MTUgMTUuMzAxOVpNMTIuODg4NCAyLjUwMjc0QzEzLjAxODUgMi41MDMyNCAxMy4xNDY1IDIuNTM1NTIgMTMuMjYxMyAyLjU5Njc5QzEzLjM3NjEgMi42NTgwNSAxMy40NzQyIDIuNzQ2NDQgMTMuNTQ3MSAyLjg1NDI5QzEzLjYyIDIuOTYyMTQgMTMuNjY1NSAzLjA4NjE3IDEzLjY3OTcgMy4yMTU2M0MxMy42OTM5IDMuMzQ1MDkgMTMuNjc2MyAzLjQ3NjA1IDEzLjYyODQgMy41OTcxNEwxMy42MDYgMy42NDE5NEMxMy41NDI5IDMuNzc5ODEgMTMuNDQxNiAzLjg5NjY0IDEzLjMxNDEgMy45Nzg1NUMxMy4xODY2IDQuMDYwNDUgMTMuMDM4MyA0LjEwMzk5IDEyLjg4NjggNC4xMDM5OUMxMi43MzUzIDQuMTAzOTkgMTIuNTg3IDQuMDYwNDUgMTIuNDU5NiAzLjk3ODU1QzEyLjMzMjEgMy44OTY2NCAxMi4yMzA3IDMuNzc5ODEgMTIuMTY3NiAzLjY0MTk0TDEyLjE0NTMgMy41OTg3NEMxMi4wOTcgMy40NzczMSAxMi4wNzkxIDMuMzQ1ODkgMTIuMDkzMyAzLjIxNTk2QzEyLjEwNzQgMy4wODYwMyAxMi4xNTMyIDIuOTYxNTYgMTIuMjI2NSAyLjg1MzQyQzEyLjI5OTggMi43NDUyOCAxMi4zOTg1IDIuNjU2NzggMTIuNTEzOSAyLjU5NTY0QzEyLjYyOTMgMi41MzQ1MSAxMi43NTc5IDIuNTAyNjEgMTIuODg4NCAyLjUwMjc0Wk0yMy4yNzY3IDguMTAyNzRDMjMuMjc2NyA4LjMxNDkxIDIzLjE5MjUgOC41MTg0IDIzLjA0MjYgOC42Njg0M0MyMi44OTI4IDguODE4NDUgMjIuNjg5NSA4LjkwMjc0IDIyLjQ3NzYgOC45MDI3NEMyMi4yNjU2IDguOTAyNzQgMjIuMDYyNCA4LjgxODQ1IDIxLjkxMjUgOC42Njg0M0MyMS43NjI3IDguNTE4NCAyMS42Nzg1IDguMzE0OTEgMjEuNjc4NSA4LjEwMjc0QzIxLjY3ODUgNy44OTA1NyAyMS43NjI3IDcuNjg3MDggMjEuOTEyNSA3LjUzNzA1QzIyLjA2MjQgNy4zODcwMiAyMi4yNjU2IDcuMzAyNzQgMjIuNDc3NiA3LjMwMjc0QzIyLjY4OTUgNy4zMDI3NCAyMi44OTI4IDcuMzg3MDIgMjMuMDQyNiA3LjUzNzA1QzIzLjE5MjUgNy42ODcwOCAyMy4yNzY3IDcuODkwNTcgMjMuMjc2NyA4LjEwMjc0Wk0yLjUwMDE3IDguMTAyNzRDMi41MDMgNy45MjMwNSAyLjU2NjE3IDcuNzQ5NTYgMi42Nzk1MSA3LjYxMDJDMi43OTI4NSA3LjQ3MDg1IDIuOTQ5NzYgNy4zNzM3NiAzLjEyNDk1IDcuMzM0NThDMy4zMDAxNCA3LjI5NTQgMy40ODM0IDcuMzE2NDEgMy42NDUyIDcuMzk0MjNDMy44MDcgNy40NzIwNSAzLjkzNzkyIDcuNjAyMTQgNC4wMTY4NSA3Ljc2MzU0TDQuMDM5MjMgNy44MDgzNEM0LjA5ODcxIDcuOTUzMDYgNC4xMTM3NiA4LjExMjI1IDQuMDgyNDQgOC4yNjU1OEM0LjA1MTEzIDguNDE4OSAzLjk3NDg4IDguNTU5NDEgMy44NjM0MyA4LjY2OTE0QzMuNzUxNTggOC43ODA3NiAzLjYwOTIxIDguODU2NyAzLjQ1NDI4IDguODg3MzdDMy4yOTkzNiA4LjkxODA1IDMuMTM4ODMgOC45MDIwNyAyLjk5Mjk3IDguODQxNDdDMi44NDcxIDguNzgwODYgMi43MjI0NSA4LjY3ODM1IDIuNjM0NzQgOC41NDY4N0MyLjU0NzAzIDguNDE1MzkgMi41MDAyIDguMjYwODQgMi41MDAxNyA4LjEwMjc0Wk0yLjUwMDE3IDE3LjcwMjdDMi41MDAxNyAxNy40OTA2IDIuNTg0MzYgMTcuMjg3MSAyLjczNDIyIDE3LjEzNzFDMi44ODQwOCAxNi45ODcgMy4wODczMyAxNi45MDI3IDMuMjk5MjcgMTYuOTAyN0MzLjUxMTIgMTYuOTAyNyAzLjcxNDQ1IDE2Ljk4NyAzLjg2NDMxIDE3LjEzNzFDNC4wMTQxNyAxNy4yODcxIDQuMDk4MzYgMTcuNDkwNiA0LjA5ODM2IDE3LjcwMjdDNC4wOTgzNiAxNy45MTQ5IDQuMDE0MTcgMTguMTE4NCAzLjg2NDMxIDE4LjI2ODRDMy43MTQ0NSAxOC40MTg1IDMuNTExMiAxOC41MDI3IDMuMjk5MjcgMTguNTAyN0MzLjA4NzMzIDE4LjUwMjcgMi44ODQwOCAxOC40MTg1IDIuNzM0MjIgMTguMjY4NEMyLjU4NDM2IDE4LjExODQgMi41MDAxNyAxNy45MTQ5IDIuNTAwMTcgMTcuNzAyN1pNMTIuODg4NCAyMy4zMDI3QzEyLjc1NjYgMjMuMzAyOCAxMi42MjY4IDIzLjI3MDIgMTIuNTEwNiAyMy4yMDc4QzEyLjM5NDQgMjMuMTQ1NSAxMi4yOTU1IDIzLjA1NTMgMTIuMjIyNSAyMi45NDU0QzEyLjE0OTYgMjIuODM1NSAxMi4xMDQ5IDIyLjcwOTIgMTIuMDkyNiAyMi41Nzc4QzEyLjA4MDIgMjIuNDQ2NCAxMi4xMDA1IDIyLjMxNCAxMi4xNTE3IDIyLjE5MjNDMTIuMjEyOCAyMi4wNTE5IDEyLjMxMjkgMjEuOTMxOSAxMi40NDAxIDIxLjg0NjhDMTIuNTY3MyAyMS43NjE2IDEyLjcxNjMgMjEuNzE0OCAxMi44NjkzIDIxLjcxMkMxMy4wMjIzIDIxLjcwOTEgMTMuMTcyOSAyMS43NTAzIDEzLjMwMzIgMjEuODMwNkMxMy40MzM2IDIxLjkxMSAxMy41MzgxIDIyLjAyNzEgMTMuNjA0NCAyMi4xNjUxTDEzLjYyNjggMjIuMjA5OUMxMy42ODY4IDIyLjM1NDEgMTMuNzAyNCAyMi41MTI5IDEzLjY3MTYgMjIuNjY1OUMxMy42NDA5IDIyLjgxOSAxMy41NjUxIDIyLjk1OTQgMTMuNDU0MiAyMy4wNjkxQzEzLjM3OTggMjMuMTQzNCAxMy4yOTE2IDIzLjIwMjIgMTMuMTk0NSAyMy4yNDIzQzEzLjA5NzQgMjMuMjgyNCAxMi45OTM0IDIzLjMwMjkgMTIuODg4NCAyMy4zMDI3Wk0yMi40Nzc2IDE4LjUwMjdDMjIuMzI2NyAxOC41MDE2IDIyLjE3OTMgMTguNDU3NyAyMi4wNTIzIDE4LjM3NjFDMjEuOTI1MyAxOC4yOTQ2IDIxLjgyNCAxOC4xNzg3IDIxLjc2IDE4LjA0MTlMMjEuNzM3NiAxNy45OTcxQzIxLjY5ODEgMTcuOTAyOSAyMS42Nzc3IDE3LjgwMTcgMjEuNjc3NyAxNy42OTk1QzIxLjY3NzcgMTcuNTk3MyAyMS42OTgxIDE3LjQ5NjIgMjEuNzM3NiAxNy40MDE5TDIxLjc1MiAxNy4zNzQ3QzIxLjgwOTggMTcuMjQyMiAyMS45MDIzIDE3LjEyNzkgMjIuMDE5OSAxNy4wNDM4QzIyLjEzNzQgMTYuOTU5OCAyMi4yNzU1IDE2LjkwOTIgMjIuNDE5NCAxNi44OTc0QzIyLjU2MzMgMTYuODg1NyAyMi43MDc4IDE2LjkxMzIgMjIuODM3MyAxNi45NzcxQzIyLjk2NjkgMTcuMDQwOSAyMy4wNzY4IDE3LjEzODggMjMuMTU1MiAxNy4yNjAxQzIzLjIzMzcgMTcuMzgxNSAyMy4yNzc4IDE3LjUyMTkgMjMuMjgzIDE3LjY2NjRDMjMuMjg4MSAxNy44MTA5IDIzLjI1NCAxNy45NTQxIDIzLjE4NDMgMTguMDgwOEMyMy4xMTQ2IDE4LjIwNzQgMjMuMDEyIDE4LjMxMjggMjIuODg3MiAxOC4zODU3QzIyLjc2MjUgMTguNDU4NiAyMi42MjA0IDE4LjQ5NjMgMjIuNDc2IDE4LjQ5NDdMMjIuNDc3NiAxOC41MDI3Wk0xOC4wMTg2IDkuODA4MzRMMjAuMTcxNCA4LjczMTU0QzIwLjE1NTQgOC42MzU1NCAyMC4xNDU4IDguNTM3OTQgMjAuMTQyNiA4LjQ0MDM0QzIwLjE0NTggOC4zNDI3NCAyMC4xNTU0IDguMjQ1MTQgMjAuMTcxNCA4LjE0OTE0TDE1LjI4NDEgNS43MDI3NEwxOC4wMTg2IDkuODA4MzRaTTEwLjYxNTggNS43MDQzNEw1LjczMDEyIDguMTQ5MTRDNS43NDU0NSA4LjI0NTU1IDUuNzU1MDUgOC4zNDI3OSA1Ljc1ODg4IDguNDQwMzRDNS43NTU2OSA4LjUzNzk0IDUuNzQ2MSA4LjYzNTU0IDUuNzMwMTIgOC43MzE1NEw3Ljg4Mjg4IDkuODA4MzRMMTAuNjE1OCA1LjcwNDM0Wk01LjczMDEyIDE3Ljc0OTFMNy44ODI4OCAxNi42NzIzTDEwLjYxNzQgMjAuNzc3OUw1LjczMDEyIDE4LjMzMTVDNS43NDYxIDE4LjIzNTUgNS43NTU2OSAxOC4xMzc5IDUuNzU4ODggMTguMDQwM0M1Ljc1NTA1IDE3Ljk0MjggNS43NDU0NSAxNy44NDU2IDUuNzMwMTIgMTcuNzQ5MVpNMTIuMjEwOCAxMy41MzYzTDEyLjIzMzIgMTMuNTc5NUgxMi4yMzY0QzEyLjMgMTMuNzE3NSAxMi40MDIxIDEzLjgzNDEgMTIuNTMwMyAxMy45MTU1QzEyLjY1ODUgMTMuOTk2OCAxMi44MDc0IDE0LjAzOTUgMTIuOTU5MiAxNC4wMzgzQzEzLjExMDkgMTQuMDM3MSAxMy4yNTkyIDEzLjk5MjEgMTMuMzg2MSAxMy45MDg4QzEzLjUxMyAxMy44MjU1IDEzLjYxMzIgMTMuNzA3MiAxMy42NzQ3IDEzLjU2ODNMMTMuNjg5MSAxMy41NDExQzEzLjcyOTIgMTMuNDQ0IDEzLjc0OTggMTMuMzM5OCAxMy43NDk3IDEzLjIzNDdDMTMuNzQ5NiAxMy4xMjk2IDEzLjcyODggMTMuMDI1NSAxMy42ODg1IDEyLjkyODRDMTMuNjQ4MiAxMi44MzEzIDEzLjU4OTIgMTIuNzQzMSAxMy41MTQ4IDEyLjY2ODhDMTMuNDQwNSAxMi41OTQ2IDEzLjM1MjMgMTIuNTM1NyAxMy4yNTUyIDEyLjQ5NTVDMTMuMTU4MSAxMi40NTU0IDEzLjA1NDEgMTIuNDM0OCAxMi45NDkxIDEyLjQzNDlDMTIuODQ0MSAxMi40MzUgMTIuNzQwMSAxMi40NTU5IDEyLjY0MzEgMTIuNDk2MkMxMi41NDYxIDEyLjUzNjUgMTIuNDU4MSAxMi41OTU2IDEyLjM4MzkgMTIuNjdDMTIuMzA5NyAxMi43NDQ0IDEyLjI1MDkgMTIuODMyOCAxMi4yMTA4IDEyLjkyOTlDMTIuMTcwNiAxMy4wMjYgMTIuMTQ5OSAxMy4xMjkgMTIuMTQ5OSAxMy4yMzMxQzEyLjE0OTkgMTMuMzM3MyAxMi4xNzA2IDEzLjQ0MDMgMTIuMjEwOCAxMy41MzYzWk0xNC42MDk3IDE0Ljk3MTVDMTQuMzYzNyAxNS4yMDY2IDE0LjA3MDYgMTUuMzg2NiAxMy43NDk4IDE1LjQ5OTVWMjAuMTk4N0wxNi41Nzg2IDE1Ljk1NzFMMTQuNjA5NyAxNC45NzE1Wk0xNS4zNDggMTMuMjQwM0MxNS4zNDQ4IDEzLjMzOTUgMTUuMzM1MyAxMy40Mzg3IDE1LjMxOTMgMTMuNTM3OUwxNy40NzM2IDE0LjYwODNMMTguMzg0NiAxMy4yNDAzTDE3LjQ3MiAxMS44NzIzTDE1LjMxOTMgMTIuOTQ5MUMxNS4zMzQ2IDEzLjA0NTYgMTUuMzQ0MiAxMy4xNDI4IDE1LjM0OCAxMy4yNDAzWk0xMy43NDk4IDEwLjk5MzlDMTQuMDcwNiAxMS4xMDY5IDE0LjM2MzcgMTEuMjg2OSAxNC42MDk3IDExLjUyMTlMMTYuNTc4NiAxMC41Mjk5TDEzLjc0OTggNi4yODE5NFYxMC45OTM5Wk0xMi4xNTE3IDEwLjk4NzVWNi4yODE5NEw5LjMyMjg1IDEwLjUyOTlMMTEuMjkxOCAxMS41MTU1QzExLjUzNzggMTEuMjgwNSAxMS44MzA5IDExLjEwMDUgMTIuMTUxNyAxMC45OTM5Wk0xMC41NTM1IDEzLjI0MDNDMTAuNTU2NyAxMy4xNDI3IDEwLjU2NjIgMTMuMDQ1MSAxMC41ODIyIDEyLjk0OTFMOC40Mjc4NyAxMS44NzIzTDcuNTE2OSAxMy4yNDAzTDguNDI5NDYgMTQuNjA4M0wxMC41ODIyIDEzLjUzMTVDMTAuNTY2MiAxMy40MzU1IDEwLjU1NjcgMTMuMzM3OSAxMC41NTM1IDEzLjI0MDNaTTEyLjE1MTcgMTUuNDkzMUMxMS44MzA5IDE1LjM4MDIgMTEuNTM3OCAxNS4yMDAyIDExLjI5MTggMTQuOTY1MUw5LjMyMjg1IDE1Ljk1MDdMMTIuMTUxNyAyMC4xOTg3VjE1LjQ5MzFaTTIwLjE3MTQgMTcuNzQ5MUwxOC4wMTg2IDE2LjY3MjNMMTUuMjg0MSAyMC43Nzc5TDIwLjE3MTQgMTguMzMxNUMyMC4xNTU0IDE4LjIzNTUgMjAuMTQ1OCAxOC4xMzc5IDIwLjE0MjYgMTguMDQwM0MyMC4xNDU4IDE3Ljk0MjcgMjAuMTU1NCAxNy44NDUxIDIwLjE3MTQgMTcuNzQ5MVpNMTguOTEyIDE1LjMyOTlMMjAuMjA0OSAxNS45Nzc5TDE5LjM0MzUgMTQuNjgwM0wxOC45MTIgMTUuMzI5OVpNMjAuMjA0OSAxMC41MDI3TDE4LjkxMiAxMS4xNTA3TDE5LjM0MzUgMTEuODAwM0wyMC4yMDQ5IDEwLjUwMjdaTTYuOTg5NDkgMTEuMTQ0M0w1LjY5NjU2IDEwLjUwNDNMNi41NTc5OCAxMS44MDAzTDYuOTg5NDkgMTEuMTQ0M1pNNS42OTY1NiAxNS45Nzc5TDYuOTg5NDkgMTUuMzI5OUw2LjU1Nzk4IDE0LjY4MDNMNS42OTY1NiAxNS45Nzc5WiIgLz4KICAgICAgICAgICAgPC9zdmc+)

## AI-Generated Summary

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibnYtYWktc3VtbWFyeV9fdG9nZ2xlLWljb24iIHdpZHRoPSIxNCIgaGVpZ2h0PSI5IiB2aWV3Ym94PSIwIDAgMTQgOSIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiBhcmlhLWhpZGRlbj0idHJ1ZSI+CiAgICAgICAgPHBhdGggZD0iTTEyLjU3NDIgMkw3LjQ0OTIzIDdMMi4zMjQyNSAyIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0ic3F1YXJlIiAvPgogICAgPC9zdmc+)

- [NVIDIA Collective Communications Library (NCCL) 2.28](https://developer.nvidia.com/nccl) introduces GPU-initiated networking, device APIs for communication-compute fusion, and copy-engine-based collectives to increase throughput and reduce latency across multi-GPU and multi-node systems.
- The new device API enables kernels to initiate data movement directly through three operation modes: Load/Store Accessible, Multimem, and GPU-Initiated Networking, removing host-driven synchronization overhead.
- Copy-engine-based collectives offload NVLink transfers from streaming multiprocessors to dedicated hardware, achieving zero-SM operation for collectives such as AlltoAll and AllGather while maintaining comparable peak bandwidth.
- NCCL Inspector provides a low-overhead profiling plugin for always-on observability, capturing per-communicator performance metrics, event traces, and structured JSON output for analysis.
- Developer experience improvements include new host APIs for AlltoAll, Gather, and Scatter, grouped symmetric kernel support, a CMake-based build system for Linux, and a flexible environment plugin API for programmatic configuration management.

### Next Steps

- Explore the [NVIDIA/nccl GitHub repository](https://github.com/NVIDIA/nccl) for source code and examples.
- Review the [NCCL documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html) to learn about tuning NCCL for your system architecture.

Powered by NVIDIA Nemotron. AI-generated content may summarize information incompletely. Verify important information. [Learn more](https://www.nvidia.com/en-us/agreements/trustworthy-ai/terms/)

The latest release of the [NVIDIA Collective Communications Library (NCCL)](https://developer.nvidia.com/nccl) introduces a groundbreaking fusion of communication and computation for higher throughput, reduced latency, and maximized GPU utilization across multi-GPU and multi-node systems.

NCCL 2.28 focuses on **GPU-initiated networking, device APIs for communication-compute fusion, copy-engine-based collectives**, and **new APIs** for developers to build efficient, scalable distributed applications. Alongside these performance innovations, this release also enhances the developer experience with expanded APIs, improved tooling, and cleaner integration paths, empowering developers to write custom communication kernels and scale their applications with greater flexibility and efficiency.

## Release highlights [](#release_highlights%C2%A0)

Improvements to performance, monitoring, reliability, and quality of service are supported through the following features: 

- **Device API:** enables development of custom device kernels for communication/compute fusion, including **GPU-initiated networking**, for kernels to perform network operations directly.
- **Copy Engine (CE) -based collectives:** Developers can use CEs to drive NVIDIA NVLink transfers, reducing compute-resource contention for streaming multiprocessors (SM).
- **NCCL Inspector:** Provides a low-overhead profiling plugin that enables always-on observability and analysis of NCCL communication patterns.

## How the NCCL device API enables direct kernel communication[](#how_the_nccl_device_api_enables_direct_kernel_communication)

NCCL 2.28 introduces a device-side communication API for direct communication within NVIDIA CUDA kernels. Previously, all NCCL operations were host-initiated, introducing synchronization overhead. With the new API, kernels initiate data movement directly, integrating communication with compute operations, which yields more throughput and less overhead. To use the new API, you must use data buffers with symmetric memory windows.

Currently, three operation modes are supported: 

- **Load/Store Accessible (LSA)**: For communication between devices accessible via memory load/store operations, using CUDA P2P.
- **Multimem**: For communication between devices using the hardware multicast feature provided by NVLink SHARP
- **GPU Initiated Networking (GIN)**: For communication between devices initiated by the GPU using the network.

![Flowchart showing three NCCL Device API operation modes for GPU memory communication. “LSA” (Load/Store Accessible Memory) enables access to remote memory over PCI for load/store operations. “Multimem” (NVLink Sharp) provides multicast load/reduce operations over NVLink. “GIN” (GPU-Initiated Networking) supports put, wait, and signal operations over network mechanisms such as GDAKI and Proxy. The diagram maps each mode to its corresponding interconnect technology.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/NCCL-2.28-Device-API-Modes-png.webp)

![Flowchart showing three NCCL Device API operation modes for GPU memory communication. “LSA” (Load/Store Accessible Memory) enables access to remote memory over PCI for load/store operations. “Multimem” (NVLink Sharp) provides multicast load/reduce operations over NVLink. “GIN” (GPU-Initiated Networking) supports put, wait, and signal operations over network mechanisms such as GDAKI and Proxy. The diagram maps each mode to its corresponding interconnect technology.](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%202666%20910%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

*Figure 1.* **** *Three modes of operation are supported via the Device API for memory communication and underlying communication mechanisms*

More information is available in the [online documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/deviceapi.html#).

Special mention should be made of **GPU-Initiated Networking (GIN)**, newly introduced in NCCL 2.28.7, that enables GPUs to manage their own network operations without CPU intervention. Kernels can directly enqueue data transfers, signals, and synchronization steps, removing bottlenecks caused by host-driven control paths.

## Accelerating NCCL performance with copy engine offload[](#accelerating_nccl_performance_with_copy_engine_offload)

Achieving top communication performance at scale requires more SMs to saturate NVLink bandwidth. This increasing allocation for communication tasks creates resource competition with compute kernels, which can reduce overall application performance.

CE collectives offload communication tasks within the NVLink domain from SMs to dedicated hardware CEs. In contrast to traditional NCCL collectives, CE-based collectives achieve zero-SM operation. This approach applies to collectives that require only data movement, such as AlltoAll and AllGather. This frees up SM resources for computational workloads and improves the overlap of communication and computation. Both can now execute concurrently without competing for the same hardware resources.

CE-based collectives employ several optimizations for enhanced performance. For instance, they utilize batched APIs (e.g., `cudaMemcpyBatchAsync`) to group multiple CE operations into single calls, reducing CUDA driver overhead. Additionally, they use NVLink multicast optimization to broadcast synchronization signals efficiently. 

These collectives achieve performance comparable to SM-based collectives without requiring SM resources. The following figure shows that CE-based AllGather achieves higher peak bandwidth than SM-based AllGather. This performance advantage also partially stems from CE-initiated NVLink transactions using larger transaction widths compared to SM-initiated transactions.

![Line chart titled “Allgather Bandwidth – Size (1 Node – 8 GPUs Blackwell Umbriel)” comparing CE Multicast, CE Unicast, SM Symmetric (NCCL Optimized), and SM NonSymmetric (NCCL Default). The x-axis shows message sizes from 4 MB to 4 GB, and the y-axis shows bandwidth in GBps. CE Multicast achieves the highest bandwidth at larger message sizes, peaking around 780 GBps, while SM NonSymmetric peaks near 620 GBps—indicating a 1.25× bandwidth gain for CE Multicast over SM Symmetric at 4 GB.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/ALLGather-performance-png.webp)

![Line chart titled “Allgather Bandwidth – Size (1 Node – 8 GPUs Blackwell Umbriel)” comparing CE Multicast, CE Unicast, SM Symmetric (NCCL Optimized), and SM NonSymmetric (NCCL Default). The x-axis shows message sizes from 4 MB to 4 GB, and the y-axis shows bandwidth in GBps. CE Multicast achieves the highest bandwidth at larger message sizes, peaking around 780 GBps, while SM NonSymmetric peaks near 620 GBps—indicating a 1.25× bandwidth gain for CE Multicast over SM Symmetric at 4 GB.](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%201006%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

*Figure 2. NCCL AllGather performance with CE-based and SM-based implementation*

Review the requirements and learn how to enable CE collectives in the [NCCL documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/bufferreg.html?highlight=copy%20engine#zero-cta-optimization).

## Profiling and observability made easy with NCCL Inspector[](#profiling_and_observability_made_easy_with_nccl_inspector)

The NCCL Inspector is an observability, profiling, and analysis plugin that provides detailed, per-communicator and per-collective performance and metadata logging. This plugin should be used in always-running mode. It’s designed to help users analyze and debug NCCL collective operations by generating structured JSON output for each operation, enabling insights into communication patterns and performance characteristics during a distributed workload run using NCCL. 

The NCCL Inspector uses the NCCL Profiler plugin interface architecture to integrate into NCCL use cases. Key features include:

- **Per-communicator tracking:** The inspector tracks each NCCL communicator individually, enabling users to analyze performance patterns across different communication contexts. This is particularly valuable in complex distributed applications where multiple communicators may be used for different purposes.
- **Always-on:** The low overhead of the plugin means that the inspector can be used in production workloads to provide observability into NCCL without diminished performance. 
- **Event tracing:** The plugin captures detailed event traces, including collective start/stop events, kernel channel operations, and timing information.
- **Performance metrics:** NCCL Inspector calculates and reports key performance metrics, including algorithmic bandwidth, bus bandwidth, execution time, timing source information (GPU vs CPU timing), message sizes, and collective types.

The plugin is designed to work alongside other NCCL plugins and can provide valuable data for tuner plugins that use performance feedback to optimize communication patterns. While the current design doesn’t provide direct shared context between the NCCL Inspector and the tuner plugins, the detailed performance data generated by the inspector can be used by external analysis tools to inform tuning decisions.

![Line chart titled “HCA-Only ReduceScatter,” showing collective bus bandwidth versus collective sequence number for three NCCL Inspector runs. The x-axis spans sequence numbers from 0 to about 2,800, and the y-axis shows collective bus bandwidth. Three lines represent individual runs: green for 8.39MB_r_32 (highest), blue for 8.40MB_r_32, and red for 5.85MB_r_32 (lowest), each remaining mostly stable across the range.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/Dashboard-visualization-png.webp)

![Line chart titled “HCA-Only ReduceScatter,” showing collective bus bandwidth versus collective sequence number for three NCCL Inspector runs. The x-axis spans sequence numbers from 0 to about 2,800, and the y-axis shows collective bus bandwidth. Three lines represent individual runs: green for 8.39MB_r_32 (highest), blue for 8.40MB_r_32, and red for 5.85MB_r_32 (lowest), each remaining mostly stable across the range.](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20935%20458%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

*Figure 3. Elastic and Kibana dashboard visualization of NCCL Inspector data *

The plugin operates independently of network-specific implementations, making it compatible with various network technologies supported by NCCL. This ensures that the inspector can provide insights regardless of the underlying network infrastructure used.

More information can be found in [ext-profiler/inspector/README.md](https://github.com/NVIDIA/nccl/tree/master/ext-profiler/inspector).

## Improved developer experience with NCCL 2.28[](#improved_developer_experience_with_nccl_228)

NCCL 2.28 also extends beyond core communication and compute fusion by delivering a suite of enhancements that improve flexibility, performance tuning, and the developer experience. New APIs, kernel orchestration, configuration, profiling, and build systems allow developers to gain greater control over communication workflows with improved observability and streamlined deployments across diverse hardware and environments. The following quick run-through highlights these improvements.

### New host APIs for AllToAll, Gather, and Scatter[](#new_host_apis_for_alltoall_gather_and_scatter)

Introducing native host-level APIs for AlltoAll, Gather, and Scatter operations enables NCCL to apply advanced optimizations. For example, NCCL can use copy engines to reduce SM usage for these communication patterns, an optimization also introduced in this release. These performance enhancements are only possible with dedicated native APIs.

### Symmetric kernels group call support[](#symmetric_kernels_group_call_support)

Single symmetric kernels already provide excellent latency, bandwidth, and resource usage when used in an NVLINK domain. NCCL 2.28 adds support for grouped symmetric kernels for improved performance and resource usage. Users can register window buffers as usual and call multiple NCCL collectives between `ncclGroupStart()` and `ncclGroupEnd()`. During launch, NCCL automatically detects potential collectives that can use symmetric kernels and groups and schedules them into a single kernel for higher efficiency. For window buffer registration, please refer to [NCCL Window Buffer Registration](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/bufferreg.html#window-registration).

### Flexible config management with NCCL environment plugin[](#flexible_config_management_with_nccl_environment_plugin)

Optimizing communication parameters is crucial for performance, and NCCL offers robust mechanisms for this through configuration files and environment variables. When different jobs require unique NCCL versions and configurations, manual version matching is needed with current file-based methods, which doesn’t integrate well with modern deployment systems like databases or cloud schedulers.

The new NCCL environment plugin API offers a flexible, programmatic alternative with key advantages:

- **Programmatic version matching** automatically applies the correct configuration for each NCCL version.
- **Storage agnostic configuration** uses settings from files, databases, or environment variables.
- **Enhanced flexibility and control** by overriding some parameters programmatically while preserving others for fine-grained control.
- **Initialization and resource management** start once and stay active through runtime, and cleanly release resources.
- **Future-proof and** ready for new per-communicator configurations.

When enabled, the plugin integrates with the NCCL parameter subsystem and overrides lower-priority configuration mechanisms, ensuring a consistent, version-aware setup. It simplifies large-scale, multi-environment deployments, freeing users from the limitations of static file-based systems.

### Shared context for plugins[](#shared_context_for_plugins)

AI model training increasingly spans multiple data centers, creating major challenges for communication libraries. A redesigned plugin system supporting shared contexts and per-communicator tuning replaces global initialization and enables context‑aware optimizations across diverse network environments.

The following network plugin API has been updated:

``` brush:
// Network plugin v11
ncclResult_t (*init)(void** ctx, uint64_t commId, ncclNetCommConfig_v11_t* config, ...)
ncclResult_t (*finalize)(void* ctx);
ncclResult_t (*listen)(void* ctx, ...);
ncclResult_t (*connect)(void* ctx, int dev, void* handle, ...);
```

Each communicator now initializes with a commId and network config, returning a per-communicator context handle (ctx) for isolation and fine‑grained tuning. This mechanism, already used in tuner and profiler plugins, now extends to the network plugin. Developers can also place code for network, tuner, and profiler plugins in one .so library via the [NCCL_NET_PLUGIN variable](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html#nccl-net-plugin) to enable shared contexts and inter‑plugin communication.

### NCCL profiler API events[](#nccl_profiler_api_events)

Previously, the NCCL profiler plugin interface didn’t capture NCCL API calls or CUDA kernel launch events, making it unable to correlate launches, collective operations, or point-to-point events with the corresponding NCCL API calls.

The profiler now enables:

- Displaying API events in user order. This ensures correct sequencing, even if operations are grouped with ncclGroupStart/ncclGroupEnd, which may alter scheduling order.
- Measuring NCCL operation overhead on the CPU, i.e., the time taken by NCCL to schedule an operation after the user’s API call.
- Correlating CUDA kernel launches directly with the originating NCCL API calls.
- Linking collective and point-to-point tasks scheduled by NCCL to their original API calls. API events persist across graph launches, allowing lower-level tasks for each graph launch to be correlated with the user’s original API call.

### CMake-based build system[](#cmake-based_build_system)

NCCL now also supports **CMake** for Linux builds, offering a modernized alternative to Make. The CMake system simplifies integration into larger build pipelines and cross-platform projects while maintaining compatibility with legacy systems. With standardized CMake support, projects can now leverage familiar workflows used across the broader CUDA and HPC ecosystem, improving reproducibility and reducing maintenance overhead. The result is a more flexible, modular, and developer-friendly build experience.

## Get started with NCCL 2.28[](#get_started_with_nccl_228)

Discover what’s new in NCCL 2.28 and push the boundaries of distributed training with enhanced scalability, optimized collective performance, and improved cross-node efficiency.

For detailed documentation, source code, and community support, visit the [NVIDIA/nccl](https://github.com/NVIDIA/nccl) GitHub repository and checkout the provided [examples](https://github.com/NVIDIA/nccl/tree/master/examples). To learn more about tuning NCCL for your system architecture, see the [NCCL documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html).

[ Discuss (0)](#entry-content-comments)

Like

## Tags

[Data Center / Cloud](https://developer.nvidia.com/blog/category/data-center-cloud/) \| [Networking / Communications](https://developer.nvidia.com/blog/category/networking-communications/) \| [Cloud Services](https://developer.nvidia.com/blog/recent-posts/?industry=Cloud+Services) \| [NCCL](https://developer.nvidia.com/blog/recent-posts/?products=NCCL) \| [Advanced Technical](https://developer.nvidia.com/blog/recent-posts/?learning_levels=Advanced+Technical) \| [Tutorial](https://developer.nvidia.com/blog/recent-posts/?content_types=Tutorial) \| [featured](https://developer.nvidia.com/blog/tag/featured/)

## About the Authors

![Avatar photo](https://developer.nvidia.com/blog/wp-content/uploads/2018/09/Sylvain-Jeaugey_avatar_1537829685.jpg)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Sylvain Jeaugey**  
Sylvain Jeaugey is a senior software engineer at NVIDIA developing the NCCL library since its creation in 2015. He has 15 years of experience in large scale distributed computing. He has been working on various MPI implementations, developing and integrating high-speed networks technologies, and designing large network fabrics.

[View all posts by Sylvain Jeaugey![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/sjeaugey/)

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2025/07/cropped-john-bachan-131x131.png)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About John Bachan**  
John Bachan is a NCCL developer. He joined NVIDIA in 2020 after working at Lawrence Berkeley Lab on the PGAS communication library UPC++.

[View all posts by John Bachan![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/jbachan/)

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/Pak-Markthub-131x131.jpg)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Pak Markthub**  
Pak Markthub is a senior software engineer at NVIDIA. He leads the research and development of GPUDirect Async—Kernel Initiate and Kernel Submit technologies, in addition to assisting the development of other core GPUDirect technologies. Pak received a Ph.D. in mathematical and computing sciences from the Tokyo Institute of Technology, Japan. He has spent nearly a decade in the high-performance computing (HPC) field related to GPU communication technologies.

[View all posts by Pak Markthub![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/pmarkthub/)

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2025/06/cropped-zhenhao-he-131x131.jpg)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Zhenhao He**  
Zhenhao He is a senior software engineer at NVIDIA working on NCCL since November 2024. Before joining NVIDIA, he conducted systems research at ETH Zurich, focusing on hardware acceleration for networking and data processing. He holds both a PhD and a master’s degree from ETH Zurich.

[View all posts by Zhenhao He![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/zhenhaoh/)

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2025/11/cropped-unnamed-3-131x131.jpg)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Sirshak Das**  
Sirshak Das is a senior software engineer at NVIDIA, working in the AI Data-Infra Optimization group, where he focuses on optimizing communication efficiency for large-scale AI workloads. Before joining NVIDIA, he held engineering roles at several organizations, including Microsoft, Arm, Indiana University, Cisco, and Verizon, where he worked on technologies spanning cloud networking, FPGA- and DPU-based SmartNICs, user-space TCP/IP stacks, and router and switch operating systems.

[View all posts by Sirshak Das![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/sirshakd/)

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2025/08/cropped-image4-3-131x131.jpg)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Farshad Ghodsian**  
Farshad Ghodsian is a senior technical marketing engineer at NVIDIA, where he focuses on AI training and inference at scale, performance optimization insights, new model releases, and AI engineering enablement. He brings a wealth of experience at the intersection of AI infrastructure, distributed training, GPU-accelerated computing and cloud-native MLOps—translating cutting-edge research into practical insights for developers, enterprise teams and business leaders. Prior to NVIDIA, Farshad held technical roles at leading semiconductor and consulting companies, where he helped build and manage large-scale generative AI and MLOps platforms for top technology customers.

[View all posts by Farshad Ghodsian![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/farshadghodsian/)

## Comments
