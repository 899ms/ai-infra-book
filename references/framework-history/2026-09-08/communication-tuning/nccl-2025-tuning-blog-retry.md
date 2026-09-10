<!-- 从 nccl-2025-tuning-blog-retry.html 迁移的资料快照；原始 HTML SHA-256: d3c555af4fa55381ba06a02bde069ae1a1392dd4401032f25af358960a96cb51。 -->

[Networking / Communications](https://developer.nvidia.com/blog/category/networking-communications/)

English中文

# Understanding NCCL Tuning to Accelerate GPU-to-GPU Communication

![](https://developer-blogs.nvidia.com/wp-content/uploads/2025/07/neon-green-cube-1024x576-png.webp)

Jul 22, 2025

By [Ben Williams](https://developer.nvidia.com/blog/author/bewilliams/ "Posts by Ben Williams"), [Misbah Mubarak](https://developer.nvidia.com/blog/author/misbahmubarak/ "Posts by Misbah Mubarak"), [Keith Caton](https://developer.nvidia.com/blog/author/kcaton/ "Posts by Keith Caton") and [Matthew Nicely](https://developer.nvidia.com/blog/author/mnicely/ "Posts by Matthew Nicely")

Like

[ Discuss (0)](#entry-content-comments)

- [L](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Funderstanding-nccl-tuning-to-accelerate-gpu-to-gpu-communication%2F)
- [T](https://twitter.com/intent/tweet?text=Understanding+NCCL+Tuning+to+Accelerate+GPU-to-GPU+Communication+%7C+NVIDIA+Technical+Blog+https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Funderstanding-nccl-tuning-to-accelerate-gpu-to-gpu-communication%2F)
- [F](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Funderstanding-nccl-tuning-to-accelerate-gpu-to-gpu-communication%2F)
- [R](https://www.reddit.com/submit?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Funderstanding-nccl-tuning-to-accelerate-gpu-to-gpu-communication%2F&title=Understanding+NCCL+Tuning+to+Accelerate+GPU-to-GPU+Communication+%7C+NVIDIA+Technical+Blog)
- [E](mailto:?subject=I'd%20like%20to%20share%20a%20link%20with%20you&body=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Funderstanding-nccl-tuning-to-accelerate-gpu-to-gpu-communication%2F)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibnYtYWktc3VtbWFyeV9faWNvbiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iMjUiIGhlaWdodD0iMjUiIHZpZXdib3g9IjAgMCAyNSAyNSIgZmlsbD0ibm9uZSIgYXJpYS1oaWRkZW49InRydWUiPgogICAgICAgICAgICAgICAgPHBhdGggZmlsbD0iY3VycmVudENvbG9yIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTIyLjQ5MTUgMTUuMzAxOUMyMi4yOTQgMTUuMzA0NyAyMi4wOTc2IDE1LjMzMTYgMjEuOTA2NiAxNS4zODE5TDIwLjI1NCAxMi45MDE5TDIxLjkwNSAxMC40MjE5QzIyLjA5NjcgMTAuNDczMSAyMi4yOTMzIDEwLjQ5ODcgMjIuNDkxNSAxMC41MDE5QzIyLjg4NDQgMTAuNTAzMiAyMy4yNzE2IDEwLjQwNzggMjMuNjE5IDEwLjIyNDFDMjMuOTY2NSAxMC4wNDA0IDI0LjI2MzUgOS43NzQwNSAyNC40ODM5IDkuNDQ4NDVDMjQuNzA0NCA5LjEyMjg1IDI0Ljg0MTUgOC43NDc5OSAyNC44ODMyIDguMzU2ODdDMjQuOTI1IDcuOTY1NzUgMjQuODcwMSA3LjU3MDM1IDI0LjcyMzMgNy4yMDU0N0MyNC41NzY2IDYuODQwNTkgMjQuMzQyNSA2LjUxNzQxIDI0LjA0MTcgNi4yNjQzN0MyMy43NDA5IDYuMDExMzQgMjMuMzgyNSA1LjgzNjIgMjIuOTk4MiA1Ljc1NDM3QzIyLjYxMzkgNS42NzI1NSAyMi4yMTU0IDUuNjg2NTQgMjEuODM3OCA1Ljc5NTEyQzIxLjQ2MDEgNS45MDM3IDIxLjExNDkgNi4xMDM1NCAyMC44MzI2IDYuMzc3MDZMMTUuMjcwOSAzLjU5MzA1QzE1LjI4NjggMy40OTcwNSAxNS4yOTY0IDMuMzk5NDYgMTUuMjk5NiAzLjMwMTg2QzE1LjI5OTYgMi42NjUzNCAxNS4wNDcxIDIuMDU0ODkgMTQuNTk3NSAxLjYwNDhDMTQuMTQ3OSAxLjE1NDcxIDEzLjUzODEgMC45MDE4NTUgMTIuOTAyMyAwLjkwMTg1NUMxMi4yNjY1IDAuOTAxODU1IDExLjY1NjggMS4xNTQ3MSAxMS4yMDcyIDEuNjA0OEMxMC43NTc2IDIuMDU0ODkgMTAuNTA1MSAyLjY2NTM0IDEwLjUwNTEgMy4zMDE4NkMxMC41MDgzIDMuMzk5NDYgMTAuNTE3OCAzLjQ5NzA1IDEwLjUzMzggMy41OTMwNUw0Ljk3MjExIDYuMzc3MDZDNC42ODk3NiA2LjEwMjY3IDQuMzQ0MzMgNS45MDIwMiAzLjk2NjI2IDUuNzkyODFDMy41ODgxOCA1LjY4MzYgMy4xODkwOCA1LjY2OTE4IDIuODA0MTIgNS43NTA4MkMyLjQxOTE2IDUuODMyNDUgMi4wNjAxOCA2LjAwNzY0IDEuNzU4OCA2LjI2MDkzQzEuNDU3NDMgNi41MTQyMyAxLjIyMjkyIDYuODM3ODYgMS4wNzU5NSA3LjIwMzI5QzAuOTI4OTgxIDcuNTY4NzIgMC44NzQwNTggNy45NjQ3NCAwLjkxNjAyOCA4LjM1NjQ0QzAuOTU3OTk4IDguNzQ4MTMgMS4wOTU1NyA5LjEyMzQ4IDEuMzE2NjIgOS40NDkzOUMxLjUzNzY3IDkuNzc1MyAxLjgzNTQgMTAuMDQxOCAyLjE4MzU4IDEwLjIyNTNDMi41MzE3NiAxMC40MDg4IDIuOTE5NyAxMC41MDM4IDMuMzEzMTkgMTAuNTAxOUMzLjUxMTM2IDEwLjQ5ODcgMy43MDc5NCAxMC40NzE1IDMuODk4MTMgMTAuNDIxOUw1LjU1MDY2IDEyLjkwMTlMMy44OTk3MyAxNS4zODE5QzMuNzA4MTggMTUuMzMxNCAzLjUxMTIyIDE1LjMwNDYgMy4zMTMxOSAxNS4zMDE5QzIuOTIwMjkgMTUuMzAwNSAyLjUzMzA4IDE1LjM5NTkgMi4xODU2NSAxNS41Nzk2QzEuODM4MjIgMTUuNzYzMyAxLjU0MTIyIDE2LjAyOTcgMS4zMjA3NyAxNi4zNTUzQzEuMTAwMzIgMTYuNjgwOSAwLjk2MzE4OSAxNy4wNTU3IDAuOTIxNDQyIDE3LjQ0NjhDMC44Nzk2OTUgMTcuODM4IDAuOTM0NjEzIDE4LjIzMzQgMS4wODEzNiAxOC41OTgyQzEuMjI4MTEgMTguOTYzMSAxLjQ2MjE5IDE5LjI4NjMgMS43NjMwMSAxOS41MzkzQzIuMDYzODIgMTkuNzkyNCAyLjQyMjE1IDE5Ljk2NzUgMi44MDY0NiAyMC4wNDkzQzMuMTkwNzcgMjAuMTMxMiAzLjU4OTI4IDIwLjExNzIgMy45NjY5MSAyMC4wMDg2QzQuMzQ0NTUgMTkuOSA0LjY4OTc0IDE5LjcwMDIgNC45NzIxMSAxOS40MjY3TDEwLjUzMzggMjIuMjEwN0MxMC41MTc4IDIyLjMwNjcgMTAuNTA4MyAyMi40MDQzIDEwLjUwNTEgMjIuNTAxOUMxMC41MDUxIDIzLjEzODQgMTAuNzU3NiAyMy43NDg4IDExLjIwNzIgMjQuMTk4OUMxMS42NTY4IDI0LjY0OSAxMi4yNjY1IDI0LjkwMTkgMTIuOTAyMyAyNC45MDE5QzEzLjUzODEgMjQuOTAxOSAxNC4xNDc5IDI0LjY0OSAxNC41OTc1IDI0LjE5ODlDMTUuMDQ3MSAyMy43NDg4IDE1LjI5OTYgMjMuMTM4NCAxNS4yOTk2IDIyLjUwMTlDMTUuMjk1OCAyMi40MDQzIDE1LjI4NjIgMjIuMzA3MSAxNS4yNzA5IDIyLjIxMDdMMjAuODMyNiAxOS40MjY3QzIxLjExNDkgMTkuNzAxIDIxLjQ2MDQgMTkuOTAxNyAyMS44Mzg0IDIwLjAxMDlDMjIuMjE2NSAyMC4xMjAxIDIyLjYxNTYgMjAuMTM0NSAyMy4wMDA2IDIwLjA1MjlDMjMuMzg1NSAxOS45NzEzIDIzLjc0NDUgMTkuNzk2MSAyNC4wNDU5IDE5LjU0MjhDMjQuMzQ3MyAxOS4yODk1IDI0LjU4MTggMTguOTY1OSAyNC43Mjg3IDE4LjYwMDRDMjQuODc1NyAxOC4yMzUgMjQuOTMwNiAxNy44MzkgMjQuODg4NyAxNy40NDczQzI0Ljg0NjcgMTcuMDU1NiAyNC43MDkxIDE2LjY4MDIgMjQuNDg4MSAxNi4zNTQzQzI0LjI2NyAxNi4wMjg0IDIzLjk2OTMgMTUuNzYxOSAyMy42MjExIDE1LjU3ODRDMjMuMjcyOSAxNS4zOTQ5IDIyLjg4NSAxNS4yOTk5IDIyLjQ5MTUgMTUuMzAxOVpNMTIuODg4NCAyLjUwMjc0QzEzLjAxODUgMi41MDMyNCAxMy4xNDY1IDIuNTM1NTIgMTMuMjYxMyAyLjU5Njc5QzEzLjM3NjEgMi42NTgwNSAxMy40NzQyIDIuNzQ2NDQgMTMuNTQ3MSAyLjg1NDI5QzEzLjYyIDIuOTYyMTQgMTMuNjY1NSAzLjA4NjE3IDEzLjY3OTcgMy4yMTU2M0MxMy42OTM5IDMuMzQ1MDkgMTMuNjc2MyAzLjQ3NjA1IDEzLjYyODQgMy41OTcxNEwxMy42MDYgMy42NDE5NEMxMy41NDI5IDMuNzc5ODEgMTMuNDQxNiAzLjg5NjY0IDEzLjMxNDEgMy45Nzg1NUMxMy4xODY2IDQuMDYwNDUgMTMuMDM4MyA0LjEwMzk5IDEyLjg4NjggNC4xMDM5OUMxMi43MzUzIDQuMTAzOTkgMTIuNTg3IDQuMDYwNDUgMTIuNDU5NiAzLjk3ODU1QzEyLjMzMjEgMy44OTY2NCAxMi4yMzA3IDMuNzc5ODEgMTIuMTY3NiAzLjY0MTk0TDEyLjE0NTMgMy41OTg3NEMxMi4wOTcgMy40NzczMSAxMi4wNzkxIDMuMzQ1ODkgMTIuMDkzMyAzLjIxNTk2QzEyLjEwNzQgMy4wODYwMyAxMi4xNTMyIDIuOTYxNTYgMTIuMjI2NSAyLjg1MzQyQzEyLjI5OTggMi43NDUyOCAxMi4zOTg1IDIuNjU2NzggMTIuNTEzOSAyLjU5NTY0QzEyLjYyOTMgMi41MzQ1MSAxMi43NTc5IDIuNTAyNjEgMTIuODg4NCAyLjUwMjc0Wk0yMy4yNzY3IDguMTAyNzRDMjMuMjc2NyA4LjMxNDkxIDIzLjE5MjUgOC41MTg0IDIzLjA0MjYgOC42Njg0M0MyMi44OTI4IDguODE4NDUgMjIuNjg5NSA4LjkwMjc0IDIyLjQ3NzYgOC45MDI3NEMyMi4yNjU2IDguOTAyNzQgMjIuMDYyNCA4LjgxODQ1IDIxLjkxMjUgOC42Njg0M0MyMS43NjI3IDguNTE4NCAyMS42Nzg1IDguMzE0OTEgMjEuNjc4NSA4LjEwMjc0QzIxLjY3ODUgNy44OTA1NyAyMS43NjI3IDcuNjg3MDggMjEuOTEyNSA3LjUzNzA1QzIyLjA2MjQgNy4zODcwMiAyMi4yNjU2IDcuMzAyNzQgMjIuNDc3NiA3LjMwMjc0QzIyLjY4OTUgNy4zMDI3NCAyMi44OTI4IDcuMzg3MDIgMjMuMDQyNiA3LjUzNzA1QzIzLjE5MjUgNy42ODcwOCAyMy4yNzY3IDcuODkwNTcgMjMuMjc2NyA4LjEwMjc0Wk0yLjUwMDE3IDguMTAyNzRDMi41MDMgNy45MjMwNSAyLjU2NjE3IDcuNzQ5NTYgMi42Nzk1MSA3LjYxMDJDMi43OTI4NSA3LjQ3MDg1IDIuOTQ5NzYgNy4zNzM3NiAzLjEyNDk1IDcuMzM0NThDMy4zMDAxNCA3LjI5NTQgMy40ODM0IDcuMzE2NDEgMy42NDUyIDcuMzk0MjNDMy44MDcgNy40NzIwNSAzLjkzNzkyIDcuNjAyMTQgNC4wMTY4NSA3Ljc2MzU0TDQuMDM5MjMgNy44MDgzNEM0LjA5ODcxIDcuOTUzMDYgNC4xMTM3NiA4LjExMjI1IDQuMDgyNDQgOC4yNjU1OEM0LjA1MTEzIDguNDE4OSAzLjk3NDg4IDguNTU5NDEgMy44NjM0MyA4LjY2OTE0QzMuNzUxNTggOC43ODA3NiAzLjYwOTIxIDguODU2NyAzLjQ1NDI4IDguODg3MzdDMy4yOTkzNiA4LjkxODA1IDMuMTM4ODMgOC45MDIwNyAyLjk5Mjk3IDguODQxNDdDMi44NDcxIDguNzgwODYgMi43MjI0NSA4LjY3ODM1IDIuNjM0NzQgOC41NDY4N0MyLjU0NzAzIDguNDE1MzkgMi41MDAyIDguMjYwODQgMi41MDAxNyA4LjEwMjc0Wk0yLjUwMDE3IDE3LjcwMjdDMi41MDAxNyAxNy40OTA2IDIuNTg0MzYgMTcuMjg3MSAyLjczNDIyIDE3LjEzNzFDMi44ODQwOCAxNi45ODcgMy4wODczMyAxNi45MDI3IDMuMjk5MjcgMTYuOTAyN0MzLjUxMTIgMTYuOTAyNyAzLjcxNDQ1IDE2Ljk4NyAzLjg2NDMxIDE3LjEzNzFDNC4wMTQxNyAxNy4yODcxIDQuMDk4MzYgMTcuNDkwNiA0LjA5ODM2IDE3LjcwMjdDNC4wOTgzNiAxNy45MTQ5IDQuMDE0MTcgMTguMTE4NCAzLjg2NDMxIDE4LjI2ODRDMy43MTQ0NSAxOC40MTg1IDMuNTExMiAxOC41MDI3IDMuMjk5MjcgMTguNTAyN0MzLjA4NzMzIDE4LjUwMjcgMi44ODQwOCAxOC40MTg1IDIuNzM0MjIgMTguMjY4NEMyLjU4NDM2IDE4LjExODQgMi41MDAxNyAxNy45MTQ5IDIuNTAwMTcgMTcuNzAyN1pNMTIuODg4NCAyMy4zMDI3QzEyLjc1NjYgMjMuMzAyOCAxMi42MjY4IDIzLjI3MDIgMTIuNTEwNiAyMy4yMDc4QzEyLjM5NDQgMjMuMTQ1NSAxMi4yOTU1IDIzLjA1NTMgMTIuMjIyNSAyMi45NDU0QzEyLjE0OTYgMjIuODM1NSAxMi4xMDQ5IDIyLjcwOTIgMTIuMDkyNiAyMi41Nzc4QzEyLjA4MDIgMjIuNDQ2NCAxMi4xMDA1IDIyLjMxNCAxMi4xNTE3IDIyLjE5MjNDMTIuMjEyOCAyMi4wNTE5IDEyLjMxMjkgMjEuOTMxOSAxMi40NDAxIDIxLjg0NjhDMTIuNTY3MyAyMS43NjE2IDEyLjcxNjMgMjEuNzE0OCAxMi44NjkzIDIxLjcxMkMxMy4wMjIzIDIxLjcwOTEgMTMuMTcyOSAyMS43NTAzIDEzLjMwMzIgMjEuODMwNkMxMy40MzM2IDIxLjkxMSAxMy41MzgxIDIyLjAyNzEgMTMuNjA0NCAyMi4xNjUxTDEzLjYyNjggMjIuMjA5OUMxMy42ODY4IDIyLjM1NDEgMTMuNzAyNCAyMi41MTI5IDEzLjY3MTYgMjIuNjY1OUMxMy42NDA5IDIyLjgxOSAxMy41NjUxIDIyLjk1OTQgMTMuNDU0MiAyMy4wNjkxQzEzLjM3OTggMjMuMTQzNCAxMy4yOTE2IDIzLjIwMjIgMTMuMTk0NSAyMy4yNDIzQzEzLjA5NzQgMjMuMjgyNCAxMi45OTM0IDIzLjMwMjkgMTIuODg4NCAyMy4zMDI3Wk0yMi40Nzc2IDE4LjUwMjdDMjIuMzI2NyAxOC41MDE2IDIyLjE3OTMgMTguNDU3NyAyMi4wNTIzIDE4LjM3NjFDMjEuOTI1MyAxOC4yOTQ2IDIxLjgyNCAxOC4xNzg3IDIxLjc2IDE4LjA0MTlMMjEuNzM3NiAxNy45OTcxQzIxLjY5ODEgMTcuOTAyOSAyMS42Nzc3IDE3LjgwMTcgMjEuNjc3NyAxNy42OTk1QzIxLjY3NzcgMTcuNTk3MyAyMS42OTgxIDE3LjQ5NjIgMjEuNzM3NiAxNy40MDE5TDIxLjc1MiAxNy4zNzQ3QzIxLjgwOTggMTcuMjQyMiAyMS45MDIzIDE3LjEyNzkgMjIuMDE5OSAxNy4wNDM4QzIyLjEzNzQgMTYuOTU5OCAyMi4yNzU1IDE2LjkwOTIgMjIuNDE5NCAxNi44OTc0QzIyLjU2MzMgMTYuODg1NyAyMi43MDc4IDE2LjkxMzIgMjIuODM3MyAxNi45NzcxQzIyLjk2NjkgMTcuMDQwOSAyMy4wNzY4IDE3LjEzODggMjMuMTU1MiAxNy4yNjAxQzIzLjIzMzcgMTcuMzgxNSAyMy4yNzc4IDE3LjUyMTkgMjMuMjgzIDE3LjY2NjRDMjMuMjg4MSAxNy44MTA5IDIzLjI1NCAxNy45NTQxIDIzLjE4NDMgMTguMDgwOEMyMy4xMTQ2IDE4LjIwNzQgMjMuMDEyIDE4LjMxMjggMjIuODg3MiAxOC4zODU3QzIyLjc2MjUgMTguNDU4NiAyMi42MjA0IDE4LjQ5NjMgMjIuNDc2IDE4LjQ5NDdMMjIuNDc3NiAxOC41MDI3Wk0xOC4wMTg2IDkuODA4MzRMMjAuMTcxNCA4LjczMTU0QzIwLjE1NTQgOC42MzU1NCAyMC4xNDU4IDguNTM3OTQgMjAuMTQyNiA4LjQ0MDM0QzIwLjE0NTggOC4zNDI3NCAyMC4xNTU0IDguMjQ1MTQgMjAuMTcxNCA4LjE0OTE0TDE1LjI4NDEgNS43MDI3NEwxOC4wMTg2IDkuODA4MzRaTTEwLjYxNTggNS43MDQzNEw1LjczMDEyIDguMTQ5MTRDNS43NDU0NSA4LjI0NTU1IDUuNzU1MDUgOC4zNDI3OSA1Ljc1ODg4IDguNDQwMzRDNS43NTU2OSA4LjUzNzk0IDUuNzQ2MSA4LjYzNTU0IDUuNzMwMTIgOC43MzE1NEw3Ljg4Mjg4IDkuODA4MzRMMTAuNjE1OCA1LjcwNDM0Wk01LjczMDEyIDE3Ljc0OTFMNy44ODI4OCAxNi42NzIzTDEwLjYxNzQgMjAuNzc3OUw1LjczMDEyIDE4LjMzMTVDNS43NDYxIDE4LjIzNTUgNS43NTU2OSAxOC4xMzc5IDUuNzU4ODggMTguMDQwM0M1Ljc1NTA1IDE3Ljk0MjggNS43NDU0NSAxNy44NDU2IDUuNzMwMTIgMTcuNzQ5MVpNMTIuMjEwOCAxMy41MzYzTDEyLjIzMzIgMTMuNTc5NUgxMi4yMzY0QzEyLjMgMTMuNzE3NSAxMi40MDIxIDEzLjgzNDEgMTIuNTMwMyAxMy45MTU1QzEyLjY1ODUgMTMuOTk2OCAxMi44MDc0IDE0LjAzOTUgMTIuOTU5MiAxNC4wMzgzQzEzLjExMDkgMTQuMDM3MSAxMy4yNTkyIDEzLjk5MjEgMTMuMzg2MSAxMy45MDg4QzEzLjUxMyAxMy44MjU1IDEzLjYxMzIgMTMuNzA3MiAxMy42NzQ3IDEzLjU2ODNMMTMuNjg5MSAxMy41NDExQzEzLjcyOTIgMTMuNDQ0IDEzLjc0OTggMTMuMzM5OCAxMy43NDk3IDEzLjIzNDdDMTMuNzQ5NiAxMy4xMjk2IDEzLjcyODggMTMuMDI1NSAxMy42ODg1IDEyLjkyODRDMTMuNjQ4MiAxMi44MzEzIDEzLjU4OTIgMTIuNzQzMSAxMy41MTQ4IDEyLjY2ODhDMTMuNDQwNSAxMi41OTQ2IDEzLjM1MjMgMTIuNTM1NyAxMy4yNTUyIDEyLjQ5NTVDMTMuMTU4MSAxMi40NTU0IDEzLjA1NDEgMTIuNDM0OCAxMi45NDkxIDEyLjQzNDlDMTIuODQ0MSAxMi40MzUgMTIuNzQwMSAxMi40NTU5IDEyLjY0MzEgMTIuNDk2MkMxMi41NDYxIDEyLjUzNjUgMTIuNDU4MSAxMi41OTU2IDEyLjM4MzkgMTIuNjdDMTIuMzA5NyAxMi43NDQ0IDEyLjI1MDkgMTIuODMyOCAxMi4yMTA4IDEyLjkyOTlDMTIuMTcwNiAxMy4wMjYgMTIuMTQ5OSAxMy4xMjkgMTIuMTQ5OSAxMy4yMzMxQzEyLjE0OTkgMTMuMzM3MyAxMi4xNzA2IDEzLjQ0MDMgMTIuMjEwOCAxMy41MzYzWk0xNC42MDk3IDE0Ljk3MTVDMTQuMzYzNyAxNS4yMDY2IDE0LjA3MDYgMTUuMzg2NiAxMy43NDk4IDE1LjQ5OTVWMjAuMTk4N0wxNi41Nzg2IDE1Ljk1NzFMMTQuNjA5NyAxNC45NzE1Wk0xNS4zNDggMTMuMjQwM0MxNS4zNDQ4IDEzLjMzOTUgMTUuMzM1MyAxMy40Mzg3IDE1LjMxOTMgMTMuNTM3OUwxNy40NzM2IDE0LjYwODNMMTguMzg0NiAxMy4yNDAzTDE3LjQ3MiAxMS44NzIzTDE1LjMxOTMgMTIuOTQ5MUMxNS4zMzQ2IDEzLjA0NTYgMTUuMzQ0MiAxMy4xNDI4IDE1LjM0OCAxMy4yNDAzWk0xMy43NDk4IDEwLjk5MzlDMTQuMDcwNiAxMS4xMDY5IDE0LjM2MzcgMTEuMjg2OSAxNC42MDk3IDExLjUyMTlMMTYuNTc4NiAxMC41Mjk5TDEzLjc0OTggNi4yODE5NFYxMC45OTM5Wk0xMi4xNTE3IDEwLjk4NzVWNi4yODE5NEw5LjMyMjg1IDEwLjUyOTlMMTEuMjkxOCAxMS41MTU1QzExLjUzNzggMTEuMjgwNSAxMS44MzA5IDExLjEwMDUgMTIuMTUxNyAxMC45OTM5Wk0xMC41NTM1IDEzLjI0MDNDMTAuNTU2NyAxMy4xNDI3IDEwLjU2NjIgMTMuMDQ1MSAxMC41ODIyIDEyLjk0OTFMOC40Mjc4NyAxMS44NzIzTDcuNTE2OSAxMy4yNDAzTDguNDI5NDYgMTQuNjA4M0wxMC41ODIyIDEzLjUzMTVDMTAuNTY2MiAxMy40MzU1IDEwLjU1NjcgMTMuMzM3OSAxMC41NTM1IDEzLjI0MDNaTTEyLjE1MTcgMTUuNDkzMUMxMS44MzA5IDE1LjM4MDIgMTEuNTM3OCAxNS4yMDAyIDExLjI5MTggMTQuOTY1MUw5LjMyMjg1IDE1Ljk1MDdMMTIuMTUxNyAyMC4xOTg3VjE1LjQ5MzFaTTIwLjE3MTQgMTcuNzQ5MUwxOC4wMTg2IDE2LjY3MjNMMTUuMjg0MSAyMC43Nzc5TDIwLjE3MTQgMTguMzMxNUMyMC4xNTU0IDE4LjIzNTUgMjAuMTQ1OCAxOC4xMzc5IDIwLjE0MjYgMTguMDQwM0MyMC4xNDU4IDE3Ljk0MjcgMjAuMTU1NCAxNy44NDUxIDIwLjE3MTQgMTcuNzQ5MVpNMTguOTEyIDE1LjMyOTlMMjAuMjA0OSAxNS45Nzc5TDE5LjM0MzUgMTQuNjgwM0wxOC45MTIgMTUuMzI5OVpNMjAuMjA0OSAxMC41MDI3TDE4LjkxMiAxMS4xNTA3TDE5LjM0MzUgMTEuODAwM0wyMC4yMDQ5IDEwLjUwMjdaTTYuOTg5NDkgMTEuMTQ0M0w1LjY5NjU2IDEwLjUwNDNMNi41NTc5OCAxMS44MDAzTDYuOTg5NDkgMTEuMTQ0M1pNNS42OTY1NiAxNS45Nzc5TDYuOTg5NDkgMTUuMzI5OUw2LjU1Nzk4IDE0LjY4MDNMNS42OTY1NiAxNS45Nzc5WiIgLz4KICAgICAgICAgICAgPC9zdmc+)

## AI-Generated Summary

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibnYtYWktc3VtbWFyeV9fdG9nZ2xlLWljb24iIHdpZHRoPSIxNCIgaGVpZ2h0PSI5IiB2aWV3Ym94PSIwIDAgMTQgOSIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiBhcmlhLWhpZGRlbj0idHJ1ZSI+CiAgICAgICAgPHBhdGggZD0iTTEyLjU3NDIgMkw3LjQ0OTIzIDdMMi4zMjQyNSAyIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0ic3F1YXJlIiAvPgogICAgPC9zdmc+)

- [NVIDIA Collective Communications Library (NCCL)](https://developer.nvidia.com/nccl) uses an internal cost model and dynamic scheduler to select protocols, algorithms, CTA counts, and chunk sizes for GPU-to-GPU communication.
- Default tuning decisions can become suboptimal on diverse platforms due to factors such as network switch vendor, virtualization, CPU, or PCI configuration.
- Tuner plugins provide the recommended method to override specific tuning decisions without modifying application code, using a minimal interface to select protocols, algorithms, and CTA counts per operation.
- A case study demonstrates how the [example tuner plugin](https://github.com/NVIDIA/nccl/tree/master/ext-tuner/example) analyzes S-curve performance data, generates optimized CSV configurations, and loads them to correct algorithm and protocol selections across message sizes.
- Environment variables and ncclCommInitRankConfig offer alternative override mechanisms but are global or code-dependent and recommended primarily for benchmarking rather than production use.

### Next Steps

- Learn more about [NCCL](https://developer.nvidia.com/nccl) to understand the library's capabilities and tuning options.
- Read the [NCCL documentation](https://docs.nvidia.com/deeplearning/sdk/nccl-developer-guide/index.html) for detailed guidance on cost models, environment variables, and troubleshooting.
- Download the [NCCL software](https://github.com/NVIDIA/nccl/) to access the example tuner plugin and begin implementing custom tuning for your platform.

Powered by NVIDIA Nemotron. AI-generated content may summarize information incompletely. Verify important information. [Learn more](https://www.nvidia.com/en-us/agreements/trustworthy-ai/terms/)

The [NVIDIA Collective Communications Library (NCCL)](https://developer.nvidia.com/nccl) is essential for fast GPU-to-GPU communication in AI workloads, using various optimizations and tuning to boost performance. However, as platforms diversify, default NCCL settings may not always deliver optimal results. This post discusses why tuning is important and how users can enhance performance with custom tuner plugins. It also presents a case study of successful retuning. 

## Overview of NCCL tuning [](#overview_of_nccl_tuning%C2%A0)

When NCCL is presented with an operation to run, it must choose the correct value for the following variables: 

- Number of CTAs used to drive the operation 
- Protocol 
- Algorithm 
- Chunk sizing 

To make these decisions, it is presented with these inputs: 

- Collective operation 
- Message size 
- Communicator dimensions 
- Number of concurrent operations in an `ncclGroup` 
- Whether the presented buffer is registered 
- Topology and graph information 

NCCL looks at these inputs and computes the perceived optimal output through an internal cost model and dynamic scheduler. More details about this process are provided in subsequent sections. 

NCCL will then check whether a tuner plugin has been loaded. If the plugin is loaded, it will select tuning properties for each operation. This selection is built into a plan and broken into kernel and proxy operations before submission of the collective operation.

### NCCL cost model [](#nccl_cost_model%C2%A0)

The NCCL cost model is at the core of default tuning decisions. This model evaluates the cost of collective operations in terms of time elapsed. The purpose of the cost model is to select the correct protocol and algorithm**.** The cost model considers many factors, including GPU, topology, network, and algorithmic properties. The NCCL team continues to optimize the cost model to provide users with the best out-of-the-box tuning. For more details, see the [NCCL documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/index.html).

### Dynamic scheduler [](#dynamic_scheduler%C2%A0)

Once operations are enqueued, the decision of chunk size (buffering) and Cooperative Thread Array (CTA) quantity are determined by a separate dynamic scheduling algorithm. More CTAs are needed to drive peak bandwidth. Smaller chunks and fewer CTAs can be better for smaller message size collectives for better pipelining and latency. In addition, when many operations are progressed in parallel through [NCCL Group Call](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/api/group.html#ncclgroupend) [semantics](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/api/group.html#ncclgroupend), those operations may need to be scheduled on fewer CTAs to allow for parallel execution.

### Platform tuning variations [](#platform_tuning_variations%C2%A0)

NCCL default tuning always tries to make the best decision, factoring in differences in system and network. Sometimes, due to a variety of factors like network switch vendor, virtualization, CPU, or PCI configuration, NCCL tunings need to be tweaked to reach optimal performance. When this happens, overriding NCCL default tunings can help optimize performance. In these cases, tuner plugins are the recommended workaround for tuning, as described in the following section.

### Tuner plugins [](#tuner_plugins%C2%A0)

Tuner plugins are the recommended method to spot-fix tuning on any platform. They provide a mechanism to override NCCL default tuning decisions, made by the cost model, through a plugin model. They are loaded and work transparently for any end user. They have the flexibility to fix tuning across any dimension or type of collective.

Typically, cluster admins or platform providers will maintain a tuner plugin and provide it to their users in a recipe to ensure NCCL is selecting the best tuning parameters on their platform. Tuner plugins work well in applications, because they are transparent to the workload. The tuner plugin has a [minimal interface](https://github.com/NVIDIA/nccl/blob/master/src/include/plugin/tuner/tuner_v4.h) (as of NCCL 2.27), with a focus on selecting the right protocol and algorithm, and overriding the CTA count if necessary. 

When a tuner plugin is loaded, it’s given NCCL dimensions, ranks, and a context object which should be used to identify communicators in a multicommunicator program. The primary function in the tuner is `getCollInfo`, the point at which costs of operations are overridden.

`getCollInfo` is provided with the NCCL cost model predictions as a hint, and the tuner plugin may always choose to keep those defaults. This is important for cases where a particular algorithm and protocol aren’t compatible, or won’t work on the current topology. Those values will be set to -1.0 by the cost model. Tuner plugins are the recommended method to fix workload tuning. Read on for a practical example.

## How to avoid overtuning NCCL [](#how_to_avoid_overtuning_nccl%C2%A0)

NCCL default CTA counts and buffer sizes are carefully selected to maximize end-to-end workload performance. Increasing these values will usually result in better communication benchmark performance. However, optimizing an end-to-end workload is different from optimizing NCCL in isolation. 

NCCL can run communication operations on up to 64 CTAs simultaneously (as of NCCL 2.27). While increasing the NCCL CTA counts above the default values often improves the performance of an operation, it can impact the workload performance. The effects of interference on chip resources, as well as CTA starvation, can wreak havoc on end-to-end performance. 

The NCCL design philosophy is to take just enough CTAs to saturate the line rate of available transports at large message sizes, but no more. As discussed in prior release posts, user buffer registration, collective networking, or the new symmetric memory APIs can also help with improving NCCL performance using fewer CTAs. 

If you are intimately familiar with your workload configuration and the amount of idle GPU resources, you’re welcome to experiment with increasing NCCL CTA and buffer sizes and see if it makes an improvement.

## Addressing tuning problems [](#addressing_tuning_problems%C2%A0)

It’s important to carefully consider whether tuning is a problem for your specific application, and whether manual correction will do more good than harm. The benefit of doing so depends on the degree of the tuning error, and how much that error affects end-to-end workload times. Any selective override of tuning results is a maintenance burden, and potentially prevents improvements in future NCCL tuning from propagating back to your workload. While those overrides are in place, any default choices by NCCL are ignored. 

If you notice a specific issue with tuning on your platform, report it through the [NVIDIA/nccl](https://github.com/NVIDIA/nccl/issues) GitHub repo. 

## Options for tuning override[](#options_for_tuning_override)

This section explains the options available to override tunings. 

### Tuner plugins [](#tuner_plugins%C2%A0)

As explained in a previous section, tuner plugins are the recommended method to override tuning.

### Environment variables [](#environment_variables%C2%A0)

NCCL makes extensive use of [environment variables](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html) to allow users to configure it. There are special environment variables enabled to force library tuning. It’s important to be careful when setting these values. It is often the case that overwriting one of these values will help with a specific performance issue, but copying and pasting that variable will prevent NCCL from ever using its defaults again. 

If these variables are used in your workload configs, regularly reexamine if they should still be set as changes to your workload, new NCCL versions, or as other system configuration updates roll out.

In addition to the maintainability issue, these variables are a global setting that will apply to all NCCL communicators in a process. Their values may be cached by NCCL (over the lifespan of a process), so setting them to one value and changing them later won’t have an effect. In general, these are recommended for benchmarking, as opposed to operation. 

To override the algorithm and protocol selections, use [`NCCL_ALGO`](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html#nccl-algo) and [`NCCL_PROTO`](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html#nccl-proto). You can also experiment with increasing [`NCCL_MIN_CTAS`](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html#nccl-min-ctas) or `NCCL_NCHANNELS_PER_NET_PEER` to try to increase the quantity of CTAs used to drive operations. [`NCCL_BUFFSIZE`](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html#nccl-min-ctas) and `NCCL_P2P_CHUNKSIZE` are also key tuning parameters for the size of buffering given to each CTA. 

### `ncclCommInitRankConfig` [](#ncclcomminitrankconfig%C2%A0)

NCCL enables users to override configurations per communicator. For more details, see the [NCCL documentation](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/communicators.html#creating-a-communicator-with-options). This allows for CTA tuning (among other settings) but doesn’t support protocol or algorithm tuning. This is only an option if you have access to your applications’ NCCL-layer codebase and can result in the same issues with config management as with the environment variables.

### Ensure good foundational performance [](#ensure_good_foundational_performance%C2%A0)

Ensuring that NCCL and your system are set up correctly is the key to achieving good performance. Tuning selections can’t make a difference if the underlying system isn’t able to perform. See the [troubleshooting](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting.html) section of the NCCL documentation to learn about common issues.

## Case study: Spot-fixing default tuning [](#case_study_spot-fixing_default_tuning%C2%A0)

This section walks through using the [example tuner plugin](https://github.com/NVIDIA/nccl/tree/master/ext-tuner/example), provided in the NCCL GitHub repo, to address incorrect algorithm and protocol selections in an example scenario. 

### Analyzing S-curves [](#analyzing_s-curves%C2%A0)

The example NCCL S-curve shown in Figure 1 is a plot of the reported bus bandwidth, or overall hardware bandwidth utilization, against message size.

![This is a plot diagram showing a nice blue S-shaped curve.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/07/nccl-s-curve-plot-1-png.webp)

![This is a plot diagram showing a nice blue S-shaped curve.](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201161%20704%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 1. An NCCL S-curve plot of the reported bus bandwidth, or overall hardware bandwidth utilization, against message size

This is a well-tuned, clean S-curve. Assuming this platform has up to 200 GB/s of hardware links to saturate, it is clearly reaching line rate. At very small message sizes, the performance is dominated by latency. As the message sizes increase, the bandwidth utilization increases, eventually leveling off at the line rate of the hardware. 

Figure 2 compares the well-tuned S-curve to a suboptimally tuned S-curve.

![This is a plot diagram showing a nice blue s-shaped curve compared to a poorly tuned jagged-shaped orange curve.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/07/well-tuned-s-curve-suboptimally-tuned-s-curve-plot-comparison-1-png.webp)

![This is a plot diagram showing a nice blue s-shaped curve compared to a poorly tuned jagged-shaped orange curve.](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201253%20755%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 2. Comparison of a well-tuned S-curve to a suboptimally tuned S-curve

You can clearly see a dip in performance when increasing message size from 2 MB to 4 MB. If you ever see performance dipping when increasing message size, that’s a strong signal of a bad transitional point in tuning. There are also plateaus of BusBW when doubling message size at multiple points, from 4 MB to 8 MB, and from 128 MB to 256 MB. This shouldn’t ever happen, assuming good fundamental hardware performance. 

Data like this is a strong signal that NCCL is selecting the wrong algorithm and protocol at certain message sizes. 

To fix this, first confirm that tuning is in fact the problem, and not base performance. It’s recommended to benchmark NCCL performance (typically with [NCCL Tests](https://github.com/NVIDIA/nccl-tests)) with the relevant tuning environment variables, sweeping [`NCCL_PROTO`](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html#nccl-proto) and [`NCCL_ALGO`](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html#nccl-algo) across the valid values. Figure 3 shows how NCCL tuning affects network performance. You can see the clear tradeoffs in performance between the different algorithms and protocols. Simple is the most bandwidth-optimized protocol, while LL is the most latency optimized. LL128 lies in the middle. Ring has the best peak bandwidth utilization, but Tree is logarithmic and performs very well at medium message sizes. 

![A plot diagram with multiple lines in different colors to show how NCCL tuning affects network performance. Not all are a perfect S-curve shape.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/07/plot-results-nccl-tuned-parameters-bandwidth-utilization-2-png.webp)

![A plot diagram with multiple lines in different colors to show how NCCL tuning affects network performance. Not all are a perfect S-curve shape.](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201251%20755%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 3. Results of tuned parameters impacting bandwidth utilization and performance results

Looking at these curves, you can rule out platform performance as a root cause. The different combinations of tuning parameters look as expected. In this case, the likely cause is incorrect NCCL tunings. 

To help figure out the problem, plot the default tuning decisions on top of the sweep, as shown in Figure 4.

![A plot diagram with multiple lines in different colors to show how NCCL tuning affects network performance compared to the baseline.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/07/nccl-tuning-network-performance-plot-png.webp)

![A plot diagram with multiple lines in different colors to show how NCCL tuning affects network performance compared to the baseline.](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201247%20756%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 4. Example plot lines depicting the results of tuned parameters depicting bandwidth utilization overlaid to help identify specific bottlenecks impacting performance results

You can see clearly where the default tuning selection goes bad, starting around 4 MB, and continuing until around 512 MB message sizes. Ideally, at every message size, NCCL selects the best performing protocol and algorithm. 

### How to fix tunings using a tuner plugin[](#how_to_fix_tunings_using_a_tuner_plugin)

To fix these tunings, use a tuner plugin. Forcing a single protocol or algorithm won’t fix anything, as you want a variety of selections over message sizes. So a tuner plugin is the only option. 

This example uses the reference open source [example tuner plugin](https://github.com/NVIDIA/nccl/tree/master/ext-tuner/example) available on GitHub. The example tuner plugin is a reference implementation of a selective override config-file approach. The plugin reads tuning configurations from a CSV-based configuration file, allowing targeted overrides of given message sizes, scales, or operations, without recompiling the plugin. 

To begin, take the raw tuning data and convert it into the format usable by the plugin. Fortunately, the plugin comes with a make command invoking a script which turns raw tuning data into the CSV override format the plugin is looking for. The output shows the automated ranges being created in the config file. 

``` brush:
make optimize-config CSV_FILE=my_raw_data.csv OUTPUT=my_new_tunings.conf METRIC=latency_us 
 
Auto-ranging enabled: will create one bucket per unique size in data 
Loaded 180 performance data points 
Dimension 4 nodes, 32 ranks: 30 size ranges from 30 unique sizes: 
  Range 1: 0 - 12 bytes (6 data points, sizes: 8) 
  Range 2: 13 - 24 bytes (6 data points, sizes: 16) 
  Range 3: 25 - 48 bytes (6 data points, sizes: 32) 
  Range 4: 49 - 96 bytes (6 data points, sizes: 64) 
  Range 5: 97 - 192 bytes (6 data points, sizes: 128) 
  Range 6: 193 - 384 bytes (6 data points, sizes: 256) 
  Range 7: 385 - 768 bytes (6 data points, sizes: 512 
... 
Combined 30 ranges into 4 ranges (reduced by 26) 
Optimal for allreduce [0-98304] nodes=4 ranks=32: tree/ll channels=-1 (latency_us=49.130) 
Optimal for allreduce [98305-12582912] nodes=4 ranks=32: tree/ll128 channels=-1 (latency_us=101.400) 
Optimal for allreduce [12582913-100663296] nodes=4 ranks=32: ring/ll128 channels=-1 (latency_us=634.800) 
Optimal for allreduce [100663297-4294967296] nodes=4 ranks=32: ring/simple channels=-1 (latency_us=2967.600) 
... 
Creating new file: my_new_tunings.conf 
Created my_new_tunings.conf with 30 optimized configurations
```

#### Loading the plugin with fixed tunings 

Next, rerun NCCL with the generated optimized CSV file. Run an `all_reduce_perf` benchmark again, with the CSV plugin loaded and the [TUNING debug subsystem](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html#nccl-debug-subsys) enabled. You can see in the output that it was successfully loaded.

``` brush:
f1d6821f5ab3:1075:1081 [0] NCCL INFO TUNER/Plugin: Plugin name set by env to libnccl-tuner-example.so 
f1d6821f5ab3:1075:1081 [0] NCCL INFO TUNER/Plugin: Using tuner plugin Example 
f1d6821f5ab3:1075:1081 [0] NCCL INFO Initializing tuner for 4 nodes, 32 ranks 
f1d6821f5ab3:1075:1081 [0] NCCL INFO TUNER/ExamplePlugin: Loaded config: allreduce [0-98304] tree/ll channels=-1 nodes=4 ranks=32 pipeOps=any regBuff=any 
f1d6821f5ab3:1075:1081 [0] NCCL INFO TUNER/ExamplePlugin: Loaded config: allreduce [98305-12582912] tree/ll128 channels=-1 nodes=4 ranks=32 pipeOps=any regBuff=any 
f1d6821f5ab3:1075:1081 [0] NCCL INFO TUNER/ExamplePlugin: Loaded config: allreduce [12582913-100663296] ring/ll128 channels=-1 nodes=32 ranks=8 pipeOps=any regBuff=any 
f1d6821f5ab3:1075:1081 [0] NCCL INFO TUNER/ExamplePlugin: Loaded config: allreduce [100663297-4294967296] ring/simple channels=-1 nodes=32 ranks=8 pipeOps=any regBuff=any 
f1d6821f5ab3:1075:1081 [0] NCCL INFO TUNER/ExamplePlugin: Loaded 4 tuning configurations from my_new_tunings.conf
```

### Final results [](#final_results%C2%A0)

As shown in Figure 5, the tunings have been overridden and now work great. This is good news for any users that need to unblock without modifying any application or library code. 

![A plot diagram with multiple lines in different colors to show how NCCL tuning affects network performance. The right NCCL parameter tuning can produce smooth S-curves across each run.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/07/plot-results-properly-tuned-parameters-nccl-bandwidth-utilization-performance-1-png.webp)

![A plot diagram with multiple lines in different colors to show how NCCL tuning affects network performance. The right NCCL parameter tuning can produce smooth S-curves across each run.](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201250%20767%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 5. Final plot lines depicting the results of properly tuned parameters impacting bandwidth utilization and performance results

## Get started with NCCL tuning[](#get_started_with_nccl_tuning)

NCCL tuning is an important aspect of maximizing hardware performance and achieving line rate across message sizes and job dimensions in AI and HPC workloads. By leveraging tuner plugins, you can overcome any limitations of default tunings. As illustrated in the case study presented in this post, the [example tuner plugin](https://github.com/NVIDIA/nccl/tree/master/ext-tuner/example) can serve as a spot-fix for any tuning problems that may arise.

Learn more about [NCCL](https://developer.nvidia.com/nccl), read the [NCCL documentation](https://docs.nvidia.com/deeplearning/sdk/nccl-developer-guide/index.html), download the [NCCL software](https://github.com/NVIDIA/nccl/), and discuss this topic on the [NVIDIA Developer Forum](https://forums.developer.nvidia.com/c/accelerated-computing/gpu-accelerated-libraries/12). For even more information, check out these related posts:

- [Memory Efficiency, Faster Initialization, and Cost Estimation with NVIDIA Collective Communications Library 2.22](https://developer.nvidia.com/blog/memory-efficiency-faster-initialization-and-cost-estimation-with-nvidia-collective-communications-library-2-22/)
- [New Scaling Algorithm and Initialization with NVIDIA Collective Communications Library 2.23](https://developer.nvidia.com/blog/new-scaling-algorithm-and-initialization-with-nvidia-collective-communications-library-2-23/) 
- [Networking Reliability and Observability at Scale with NCCL 2.24](https://developer.nvidia.com/blog/networking-reliability-and-observability-at-scale-with-nccl-2-24/)
- [Improved Performance and Monitoring Capabilities with NVIDIA Collective Communications Library 2.26](https://developer.nvidia.com/blog/improved-performance-and-monitoring-capabilities-with-nvidia-collective-communications-library-2-26/) 
- [Enabling Fast Inference and Resilient Training with NCCL 2.27](https://developer.nvidia.com/blog/enabling-fast-inference-and-resilient-training-with-nccl-2-27/)

[ Discuss (0)](#entry-content-comments)

Like

## Tags

[Data Center / Cloud](https://developer.nvidia.com/blog/category/data-center-cloud/) \| [Networking / Communications](https://developer.nvidia.com/blog/category/networking-communications/) \| [General](https://developer.nvidia.com/blog/recent-posts/?industry=General) \| [NCCL](https://developer.nvidia.com/blog/recent-posts/?products=NCCL) \| [NVSHMEM](https://developer.nvidia.com/blog/recent-posts/?products=NVSHMEM) \| [Intermediate Technical](https://developer.nvidia.com/blog/recent-posts/?learning_levels=Intermediate+Technical) \| [Deep dive](https://developer.nvidia.com/blog/recent-posts/?content_types=Deep+dive) \| [Tutorial](https://developer.nvidia.com/blog/recent-posts/?content_types=Tutorial) \| [featured](https://developer.nvidia.com/blog/tag/featured/)

## About the Authors

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2024/08/Ben-Williams-131x131.jpg)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Ben Williams**  
Ben Williams is a senior software engineer at NVIDIA. He is a developer of the NCCL library with an emphasis on GPU-network interactions and system topology. He graduated from Iowa State University with a master’s degree in Computer Engineering in 2017.

[View all posts by Ben Williams![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/bewilliams/)

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2025/07/cropped-Misbah-131x131.jpeg)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Misbah Mubarak**  
Misbah Mubarak is a distinguished software engineer in the GPU software team at Nvidia. She has over 10 years of experience in large-scale, high-performance & distributed computing; network technologies; and the design of cloud network fabrics.

[View all posts by Misbah Mubarak![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/misbahmubarak/)

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2025/07/keith-caton-131x131.jpg)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Keith Caton**  
Keith Caton is a GPU communications performance engineer and developer. He joined NVIDIA in 2024. He has five years of HPC experience and CUDA development in the fields of GPU communication and kinematic/RF simulations.

[View all posts by Keith Caton![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/kcaton/)

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2021/04/matthew-nicely-131x131.jpg)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Matthew Nicely**  
Matthew Nicely is a senior product manager over Deep Learning Compilers at NVIDIA, working with cuDNN and CUTLASS. At NVIDIA, he has worked as a public sector solution architect and CUDA Math Libraries product manager. In 2019, he received his Ph.D. in computer engineering, focusing on algorithm optimizations on GPUs.

[View all posts by Matthew Nicely![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/mnicely/)

## Comments
