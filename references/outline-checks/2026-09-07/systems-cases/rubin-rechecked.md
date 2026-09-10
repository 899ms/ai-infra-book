<!-- 从 rubin-rechecked.html 迁移的资料快照；原始 HTML SHA-256: ba3d0c33530160ab57be6b6a783f96b23dabb24f83a0cd54e062fe0ebef178f5。 -->

[Data Center / Cloud](https://developer.nvidia.com/blog/category/data-center-cloud/)

English한국어中文

# Inside NVIDIA Rubin GPU Architecture: Powering the Era of Agentic AI

![](https://developer-blogs.nvidia.com/wp-content/uploads/2026/07/nvidia-rubin-gpu-1024x576.png)

Jul 21, 2026

By [Eduardo Alvarez](https://developer.nvidia.com/blog/author/edualvarez/ "Posts by Eduardo Alvarez"), [Vishal Mehta](https://developer.nvidia.com/blog/author/vishalm/ "Posts by Vishal Mehta") and [Farshad Ghodsian](https://developer.nvidia.com/blog/author/farshadghodsian/ "Posts by Farshad Ghodsian")

Like

[ Discuss (0)](#entry-content-comments)

- [L](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Finside-nvidia-rubin-gpu-architecture-powering-the-era-of-agentic-ai%2F)
- [T](https://twitter.com/intent/tweet?text=Inside+NVIDIA+Rubin+GPU+Architecture%3A+Powering+the+Era+of+Agentic+AI+%7C+NVIDIA+Technical+Blog+https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Finside-nvidia-rubin-gpu-architecture-powering-the-era-of-agentic-ai%2F)
- [F](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Finside-nvidia-rubin-gpu-architecture-powering-the-era-of-agentic-ai%2F)
- [R](https://www.reddit.com/submit?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Finside-nvidia-rubin-gpu-architecture-powering-the-era-of-agentic-ai%2F&title=Inside+NVIDIA+Rubin+GPU+Architecture%3A+Powering+the+Era+of+Agentic+AI+%7C+NVIDIA+Technical+Blog)
- [E](mailto:?subject=I'd%20like%20to%20share%20a%20link%20with%20you&body=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Finside-nvidia-rubin-gpu-architecture-powering-the-era-of-agentic-ai%2F)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibnYtYWktc3VtbWFyeV9faWNvbiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iMjUiIGhlaWdodD0iMjUiIHZpZXdib3g9IjAgMCAyNSAyNSIgZmlsbD0ibm9uZSIgYXJpYS1oaWRkZW49InRydWUiPgogICAgICAgICAgICAgICAgPHBhdGggZmlsbD0iY3VycmVudENvbG9yIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTIyLjQ5MTUgMTUuMzAxOUMyMi4yOTQgMTUuMzA0NyAyMi4wOTc2IDE1LjMzMTYgMjEuOTA2NiAxNS4zODE5TDIwLjI1NCAxMi45MDE5TDIxLjkwNSAxMC40MjE5QzIyLjA5NjcgMTAuNDczMSAyMi4yOTMzIDEwLjQ5ODcgMjIuNDkxNSAxMC41MDE5QzIyLjg4NDQgMTAuNTAzMiAyMy4yNzE2IDEwLjQwNzggMjMuNjE5IDEwLjIyNDFDMjMuOTY2NSAxMC4wNDA0IDI0LjI2MzUgOS43NzQwNSAyNC40ODM5IDkuNDQ4NDVDMjQuNzA0NCA5LjEyMjg1IDI0Ljg0MTUgOC43NDc5OSAyNC44ODMyIDguMzU2ODdDMjQuOTI1IDcuOTY1NzUgMjQuODcwMSA3LjU3MDM1IDI0LjcyMzMgNy4yMDU0N0MyNC41NzY2IDYuODQwNTkgMjQuMzQyNSA2LjUxNzQxIDI0LjA0MTcgNi4yNjQzN0MyMy43NDA5IDYuMDExMzQgMjMuMzgyNSA1LjgzNjIgMjIuOTk4MiA1Ljc1NDM3QzIyLjYxMzkgNS42NzI1NSAyMi4yMTU0IDUuNjg2NTQgMjEuODM3OCA1Ljc5NTEyQzIxLjQ2MDEgNS45MDM3IDIxLjExNDkgNi4xMDM1NCAyMC44MzI2IDYuMzc3MDZMMTUuMjcwOSAzLjU5MzA1QzE1LjI4NjggMy40OTcwNSAxNS4yOTY0IDMuMzk5NDYgMTUuMjk5NiAzLjMwMTg2QzE1LjI5OTYgMi42NjUzNCAxNS4wNDcxIDIuMDU0ODkgMTQuNTk3NSAxLjYwNDhDMTQuMTQ3OSAxLjE1NDcxIDEzLjUzODEgMC45MDE4NTUgMTIuOTAyMyAwLjkwMTg1NUMxMi4yNjY1IDAuOTAxODU1IDExLjY1NjggMS4xNTQ3MSAxMS4yMDcyIDEuNjA0OEMxMC43NTc2IDIuMDU0ODkgMTAuNTA1MSAyLjY2NTM0IDEwLjUwNTEgMy4zMDE4NkMxMC41MDgzIDMuMzk5NDYgMTAuNTE3OCAzLjQ5NzA1IDEwLjUzMzggMy41OTMwNUw0Ljk3MjExIDYuMzc3MDZDNC42ODk3NiA2LjEwMjY3IDQuMzQ0MzMgNS45MDIwMiAzLjk2NjI2IDUuNzkyODFDMy41ODgxOCA1LjY4MzYgMy4xODkwOCA1LjY2OTE4IDIuODA0MTIgNS43NTA4MkMyLjQxOTE2IDUuODMyNDUgMi4wNjAxOCA2LjAwNzY0IDEuNzU4OCA2LjI2MDkzQzEuNDU3NDMgNi41MTQyMyAxLjIyMjkyIDYuODM3ODYgMS4wNzU5NSA3LjIwMzI5QzAuOTI4OTgxIDcuNTY4NzIgMC44NzQwNTggNy45NjQ3NCAwLjkxNjAyOCA4LjM1NjQ0QzAuOTU3OTk4IDguNzQ4MTMgMS4wOTU1NyA5LjEyMzQ4IDEuMzE2NjIgOS40NDkzOUMxLjUzNzY3IDkuNzc1MyAxLjgzNTQgMTAuMDQxOCAyLjE4MzU4IDEwLjIyNTNDMi41MzE3NiAxMC40MDg4IDIuOTE5NyAxMC41MDM4IDMuMzEzMTkgMTAuNTAxOUMzLjUxMTM2IDEwLjQ5ODcgMy43MDc5NCAxMC40NzE1IDMuODk4MTMgMTAuNDIxOUw1LjU1MDY2IDEyLjkwMTlMMy44OTk3MyAxNS4zODE5QzMuNzA4MTggMTUuMzMxNCAzLjUxMTIyIDE1LjMwNDYgMy4zMTMxOSAxNS4zMDE5QzIuOTIwMjkgMTUuMzAwNSAyLjUzMzA4IDE1LjM5NTkgMi4xODU2NSAxNS41Nzk2QzEuODM4MjIgMTUuNzYzMyAxLjU0MTIyIDE2LjAyOTcgMS4zMjA3NyAxNi4zNTUzQzEuMTAwMzIgMTYuNjgwOSAwLjk2MzE4OSAxNy4wNTU3IDAuOTIxNDQyIDE3LjQ0NjhDMC44Nzk2OTUgMTcuODM4IDAuOTM0NjEzIDE4LjIzMzQgMS4wODEzNiAxOC41OTgyQzEuMjI4MTEgMTguOTYzMSAxLjQ2MjE5IDE5LjI4NjMgMS43NjMwMSAxOS41MzkzQzIuMDYzODIgMTkuNzkyNCAyLjQyMjE1IDE5Ljk2NzUgMi44MDY0NiAyMC4wNDkzQzMuMTkwNzcgMjAuMTMxMiAzLjU4OTI4IDIwLjExNzIgMy45NjY5MSAyMC4wMDg2QzQuMzQ0NTUgMTkuOSA0LjY4OTc0IDE5LjcwMDIgNC45NzIxMSAxOS40MjY3TDEwLjUzMzggMjIuMjEwN0MxMC41MTc4IDIyLjMwNjcgMTAuNTA4MyAyMi40MDQzIDEwLjUwNTEgMjIuNTAxOUMxMC41MDUxIDIzLjEzODQgMTAuNzU3NiAyMy43NDg4IDExLjIwNzIgMjQuMTk4OUMxMS42NTY4IDI0LjY0OSAxMi4yNjY1IDI0LjkwMTkgMTIuOTAyMyAyNC45MDE5QzEzLjUzODEgMjQuOTAxOSAxNC4xNDc5IDI0LjY0OSAxNC41OTc1IDI0LjE5ODlDMTUuMDQ3MSAyMy43NDg4IDE1LjI5OTYgMjMuMTM4NCAxNS4yOTk2IDIyLjUwMTlDMTUuMjk1OCAyMi40MDQzIDE1LjI4NjIgMjIuMzA3MSAxNS4yNzA5IDIyLjIxMDdMMjAuODMyNiAxOS40MjY3QzIxLjExNDkgMTkuNzAxIDIxLjQ2MDQgMTkuOTAxNyAyMS44Mzg0IDIwLjAxMDlDMjIuMjE2NSAyMC4xMjAxIDIyLjYxNTYgMjAuMTM0NSAyMy4wMDA2IDIwLjA1MjlDMjMuMzg1NSAxOS45NzEzIDIzLjc0NDUgMTkuNzk2MSAyNC4wNDU5IDE5LjU0MjhDMjQuMzQ3MyAxOS4yODk1IDI0LjU4MTggMTguOTY1OSAyNC43Mjg3IDE4LjYwMDRDMjQuODc1NyAxOC4yMzUgMjQuOTMwNiAxNy44MzkgMjQuODg4NyAxNy40NDczQzI0Ljg0NjcgMTcuMDU1NiAyNC43MDkxIDE2LjY4MDIgMjQuNDg4MSAxNi4zNTQzQzI0LjI2NyAxNi4wMjg0IDIzLjk2OTMgMTUuNzYxOSAyMy42MjExIDE1LjU3ODRDMjMuMjcyOSAxNS4zOTQ5IDIyLjg4NSAxNS4yOTk5IDIyLjQ5MTUgMTUuMzAxOVpNMTIuODg4NCAyLjUwMjc0QzEzLjAxODUgMi41MDMyNCAxMy4xNDY1IDIuNTM1NTIgMTMuMjYxMyAyLjU5Njc5QzEzLjM3NjEgMi42NTgwNSAxMy40NzQyIDIuNzQ2NDQgMTMuNTQ3MSAyLjg1NDI5QzEzLjYyIDIuOTYyMTQgMTMuNjY1NSAzLjA4NjE3IDEzLjY3OTcgMy4yMTU2M0MxMy42OTM5IDMuMzQ1MDkgMTMuNjc2MyAzLjQ3NjA1IDEzLjYyODQgMy41OTcxNEwxMy42MDYgMy42NDE5NEMxMy41NDI5IDMuNzc5ODEgMTMuNDQxNiAzLjg5NjY0IDEzLjMxNDEgMy45Nzg1NUMxMy4xODY2IDQuMDYwNDUgMTMuMDM4MyA0LjEwMzk5IDEyLjg4NjggNC4xMDM5OUMxMi43MzUzIDQuMTAzOTkgMTIuNTg3IDQuMDYwNDUgMTIuNDU5NiAzLjk3ODU1QzEyLjMzMjEgMy44OTY2NCAxMi4yMzA3IDMuNzc5ODEgMTIuMTY3NiAzLjY0MTk0TDEyLjE0NTMgMy41OTg3NEMxMi4wOTcgMy40NzczMSAxMi4wNzkxIDMuMzQ1ODkgMTIuMDkzMyAzLjIxNTk2QzEyLjEwNzQgMy4wODYwMyAxMi4xNTMyIDIuOTYxNTYgMTIuMjI2NSAyLjg1MzQyQzEyLjI5OTggMi43NDUyOCAxMi4zOTg1IDIuNjU2NzggMTIuNTEzOSAyLjU5NTY0QzEyLjYyOTMgMi41MzQ1MSAxMi43NTc5IDIuNTAyNjEgMTIuODg4NCAyLjUwMjc0Wk0yMy4yNzY3IDguMTAyNzRDMjMuMjc2NyA4LjMxNDkxIDIzLjE5MjUgOC41MTg0IDIzLjA0MjYgOC42Njg0M0MyMi44OTI4IDguODE4NDUgMjIuNjg5NSA4LjkwMjc0IDIyLjQ3NzYgOC45MDI3NEMyMi4yNjU2IDguOTAyNzQgMjIuMDYyNCA4LjgxODQ1IDIxLjkxMjUgOC42Njg0M0MyMS43NjI3IDguNTE4NCAyMS42Nzg1IDguMzE0OTEgMjEuNjc4NSA4LjEwMjc0QzIxLjY3ODUgNy44OTA1NyAyMS43NjI3IDcuNjg3MDggMjEuOTEyNSA3LjUzNzA1QzIyLjA2MjQgNy4zODcwMiAyMi4yNjU2IDcuMzAyNzQgMjIuNDc3NiA3LjMwMjc0QzIyLjY4OTUgNy4zMDI3NCAyMi44OTI4IDcuMzg3MDIgMjMuMDQyNiA3LjUzNzA1QzIzLjE5MjUgNy42ODcwOCAyMy4yNzY3IDcuODkwNTcgMjMuMjc2NyA4LjEwMjc0Wk0yLjUwMDE3IDguMTAyNzRDMi41MDMgNy45MjMwNSAyLjU2NjE3IDcuNzQ5NTYgMi42Nzk1MSA3LjYxMDJDMi43OTI4NSA3LjQ3MDg1IDIuOTQ5NzYgNy4zNzM3NiAzLjEyNDk1IDcuMzM0NThDMy4zMDAxNCA3LjI5NTQgMy40ODM0IDcuMzE2NDEgMy42NDUyIDcuMzk0MjNDMy44MDcgNy40NzIwNSAzLjkzNzkyIDcuNjAyMTQgNC4wMTY4NSA3Ljc2MzU0TDQuMDM5MjMgNy44MDgzNEM0LjA5ODcxIDcuOTUzMDYgNC4xMTM3NiA4LjExMjI1IDQuMDgyNDQgOC4yNjU1OEM0LjA1MTEzIDguNDE4OSAzLjk3NDg4IDguNTU5NDEgMy44NjM0MyA4LjY2OTE0QzMuNzUxNTggOC43ODA3NiAzLjYwOTIxIDguODU2NyAzLjQ1NDI4IDguODg3MzdDMy4yOTkzNiA4LjkxODA1IDMuMTM4ODMgOC45MDIwNyAyLjk5Mjk3IDguODQxNDdDMi44NDcxIDguNzgwODYgMi43MjI0NSA4LjY3ODM1IDIuNjM0NzQgOC41NDY4N0MyLjU0NzAzIDguNDE1MzkgMi41MDAyIDguMjYwODQgMi41MDAxNyA4LjEwMjc0Wk0yLjUwMDE3IDE3LjcwMjdDMi41MDAxNyAxNy40OTA2IDIuNTg0MzYgMTcuMjg3MSAyLjczNDIyIDE3LjEzNzFDMi44ODQwOCAxNi45ODcgMy4wODczMyAxNi45MDI3IDMuMjk5MjcgMTYuOTAyN0MzLjUxMTIgMTYuOTAyNyAzLjcxNDQ1IDE2Ljk4NyAzLjg2NDMxIDE3LjEzNzFDNC4wMTQxNyAxNy4yODcxIDQuMDk4MzYgMTcuNDkwNiA0LjA5ODM2IDE3LjcwMjdDNC4wOTgzNiAxNy45MTQ5IDQuMDE0MTcgMTguMTE4NCAzLjg2NDMxIDE4LjI2ODRDMy43MTQ0NSAxOC40MTg1IDMuNTExMiAxOC41MDI3IDMuMjk5MjcgMTguNTAyN0MzLjA4NzMzIDE4LjUwMjcgMi44ODQwOCAxOC40MTg1IDIuNzM0MjIgMTguMjY4NEMyLjU4NDM2IDE4LjExODQgMi41MDAxNyAxNy45MTQ5IDIuNTAwMTcgMTcuNzAyN1pNMTIuODg4NCAyMy4zMDI3QzEyLjc1NjYgMjMuMzAyOCAxMi42MjY4IDIzLjI3MDIgMTIuNTEwNiAyMy4yMDc4QzEyLjM5NDQgMjMuMTQ1NSAxMi4yOTU1IDIzLjA1NTMgMTIuMjIyNSAyMi45NDU0QzEyLjE0OTYgMjIuODM1NSAxMi4xMDQ5IDIyLjcwOTIgMTIuMDkyNiAyMi41Nzc4QzEyLjA4MDIgMjIuNDQ2NCAxMi4xMDA1IDIyLjMxNCAxMi4xNTE3IDIyLjE5MjNDMTIuMjEyOCAyMi4wNTE5IDEyLjMxMjkgMjEuOTMxOSAxMi40NDAxIDIxLjg0NjhDMTIuNTY3MyAyMS43NjE2IDEyLjcxNjMgMjEuNzE0OCAxMi44NjkzIDIxLjcxMkMxMy4wMjIzIDIxLjcwOTEgMTMuMTcyOSAyMS43NTAzIDEzLjMwMzIgMjEuODMwNkMxMy40MzM2IDIxLjkxMSAxMy41MzgxIDIyLjAyNzEgMTMuNjA0NCAyMi4xNjUxTDEzLjYyNjggMjIuMjA5OUMxMy42ODY4IDIyLjM1NDEgMTMuNzAyNCAyMi41MTI5IDEzLjY3MTYgMjIuNjY1OUMxMy42NDA5IDIyLjgxOSAxMy41NjUxIDIyLjk1OTQgMTMuNDU0MiAyMy4wNjkxQzEzLjM3OTggMjMuMTQzNCAxMy4yOTE2IDIzLjIwMjIgMTMuMTk0NSAyMy4yNDIzQzEzLjA5NzQgMjMuMjgyNCAxMi45OTM0IDIzLjMwMjkgMTIuODg4NCAyMy4zMDI3Wk0yMi40Nzc2IDE4LjUwMjdDMjIuMzI2NyAxOC41MDE2IDIyLjE3OTMgMTguNDU3NyAyMi4wNTIzIDE4LjM3NjFDMjEuOTI1MyAxOC4yOTQ2IDIxLjgyNCAxOC4xNzg3IDIxLjc2IDE4LjA0MTlMMjEuNzM3NiAxNy45OTcxQzIxLjY5ODEgMTcuOTAyOSAyMS42Nzc3IDE3LjgwMTcgMjEuNjc3NyAxNy42OTk1QzIxLjY3NzcgMTcuNTk3MyAyMS42OTgxIDE3LjQ5NjIgMjEuNzM3NiAxNy40MDE5TDIxLjc1MiAxNy4zNzQ3QzIxLjgwOTggMTcuMjQyMiAyMS45MDIzIDE3LjEyNzkgMjIuMDE5OSAxNy4wNDM4QzIyLjEzNzQgMTYuOTU5OCAyMi4yNzU1IDE2LjkwOTIgMjIuNDE5NCAxNi44OTc0QzIyLjU2MzMgMTYuODg1NyAyMi43MDc4IDE2LjkxMzIgMjIuODM3MyAxNi45NzcxQzIyLjk2NjkgMTcuMDQwOSAyMy4wNzY4IDE3LjEzODggMjMuMTU1MiAxNy4yNjAxQzIzLjIzMzcgMTcuMzgxNSAyMy4yNzc4IDE3LjUyMTkgMjMuMjgzIDE3LjY2NjRDMjMuMjg4MSAxNy44MTA5IDIzLjI1NCAxNy45NTQxIDIzLjE4NDMgMTguMDgwOEMyMy4xMTQ2IDE4LjIwNzQgMjMuMDEyIDE4LjMxMjggMjIuODg3MiAxOC4zODU3QzIyLjc2MjUgMTguNDU4NiAyMi42MjA0IDE4LjQ5NjMgMjIuNDc2IDE4LjQ5NDdMMjIuNDc3NiAxOC41MDI3Wk0xOC4wMTg2IDkuODA4MzRMMjAuMTcxNCA4LjczMTU0QzIwLjE1NTQgOC42MzU1NCAyMC4xNDU4IDguNTM3OTQgMjAuMTQyNiA4LjQ0MDM0QzIwLjE0NTggOC4zNDI3NCAyMC4xNTU0IDguMjQ1MTQgMjAuMTcxNCA4LjE0OTE0TDE1LjI4NDEgNS43MDI3NEwxOC4wMTg2IDkuODA4MzRaTTEwLjYxNTggNS43MDQzNEw1LjczMDEyIDguMTQ5MTRDNS43NDU0NSA4LjI0NTU1IDUuNzU1MDUgOC4zNDI3OSA1Ljc1ODg4IDguNDQwMzRDNS43NTU2OSA4LjUzNzk0IDUuNzQ2MSA4LjYzNTU0IDUuNzMwMTIgOC43MzE1NEw3Ljg4Mjg4IDkuODA4MzRMMTAuNjE1OCA1LjcwNDM0Wk01LjczMDEyIDE3Ljc0OTFMNy44ODI4OCAxNi42NzIzTDEwLjYxNzQgMjAuNzc3OUw1LjczMDEyIDE4LjMzMTVDNS43NDYxIDE4LjIzNTUgNS43NTU2OSAxOC4xMzc5IDUuNzU4ODggMTguMDQwM0M1Ljc1NTA1IDE3Ljk0MjggNS43NDU0NSAxNy44NDU2IDUuNzMwMTIgMTcuNzQ5MVpNMTIuMjEwOCAxMy41MzYzTDEyLjIzMzIgMTMuNTc5NUgxMi4yMzY0QzEyLjMgMTMuNzE3NSAxMi40MDIxIDEzLjgzNDEgMTIuNTMwMyAxMy45MTU1QzEyLjY1ODUgMTMuOTk2OCAxMi44MDc0IDE0LjAzOTUgMTIuOTU5MiAxNC4wMzgzQzEzLjExMDkgMTQuMDM3MSAxMy4yNTkyIDEzLjk5MjEgMTMuMzg2MSAxMy45MDg4QzEzLjUxMyAxMy44MjU1IDEzLjYxMzIgMTMuNzA3MiAxMy42NzQ3IDEzLjU2ODNMMTMuNjg5MSAxMy41NDExQzEzLjcyOTIgMTMuNDQ0IDEzLjc0OTggMTMuMzM5OCAxMy43NDk3IDEzLjIzNDdDMTMuNzQ5NiAxMy4xMjk2IDEzLjcyODggMTMuMDI1NSAxMy42ODg1IDEyLjkyODRDMTMuNjQ4MiAxMi44MzEzIDEzLjU4OTIgMTIuNzQzMSAxMy41MTQ4IDEyLjY2ODhDMTMuNDQwNSAxMi41OTQ2IDEzLjM1MjMgMTIuNTM1NyAxMy4yNTUyIDEyLjQ5NTVDMTMuMTU4MSAxMi40NTU0IDEzLjA1NDEgMTIuNDM0OCAxMi45NDkxIDEyLjQzNDlDMTIuODQ0MSAxMi40MzUgMTIuNzQwMSAxMi40NTU5IDEyLjY0MzEgMTIuNDk2MkMxMi41NDYxIDEyLjUzNjUgMTIuNDU4MSAxMi41OTU2IDEyLjM4MzkgMTIuNjdDMTIuMzA5NyAxMi43NDQ0IDEyLjI1MDkgMTIuODMyOCAxMi4yMTA4IDEyLjkyOTlDMTIuMTcwNiAxMy4wMjYgMTIuMTQ5OSAxMy4xMjkgMTIuMTQ5OSAxMy4yMzMxQzEyLjE0OTkgMTMuMzM3MyAxMi4xNzA2IDEzLjQ0MDMgMTIuMjEwOCAxMy41MzYzWk0xNC42MDk3IDE0Ljk3MTVDMTQuMzYzNyAxNS4yMDY2IDE0LjA3MDYgMTUuMzg2NiAxMy43NDk4IDE1LjQ5OTVWMjAuMTk4N0wxNi41Nzg2IDE1Ljk1NzFMMTQuNjA5NyAxNC45NzE1Wk0xNS4zNDggMTMuMjQwM0MxNS4zNDQ4IDEzLjMzOTUgMTUuMzM1MyAxMy40Mzg3IDE1LjMxOTMgMTMuNTM3OUwxNy40NzM2IDE0LjYwODNMMTguMzg0NiAxMy4yNDAzTDE3LjQ3MiAxMS44NzIzTDE1LjMxOTMgMTIuOTQ5MUMxNS4zMzQ2IDEzLjA0NTYgMTUuMzQ0MiAxMy4xNDI4IDE1LjM0OCAxMy4yNDAzWk0xMy43NDk4IDEwLjk5MzlDMTQuMDcwNiAxMS4xMDY5IDE0LjM2MzcgMTEuMjg2OSAxNC42MDk3IDExLjUyMTlMMTYuNTc4NiAxMC41Mjk5TDEzLjc0OTggNi4yODE5NFYxMC45OTM5Wk0xMi4xNTE3IDEwLjk4NzVWNi4yODE5NEw5LjMyMjg1IDEwLjUyOTlMMTEuMjkxOCAxMS41MTU1QzExLjUzNzggMTEuMjgwNSAxMS44MzA5IDExLjEwMDUgMTIuMTUxNyAxMC45OTM5Wk0xMC41NTM1IDEzLjI0MDNDMTAuNTU2NyAxMy4xNDI3IDEwLjU2NjIgMTMuMDQ1MSAxMC41ODIyIDEyLjk0OTFMOC40Mjc4NyAxMS44NzIzTDcuNTE2OSAxMy4yNDAzTDguNDI5NDYgMTQuNjA4M0wxMC41ODIyIDEzLjUzMTVDMTAuNTY2MiAxMy40MzU1IDEwLjU1NjcgMTMuMzM3OSAxMC41NTM1IDEzLjI0MDNaTTEyLjE1MTcgMTUuNDkzMUMxMS44MzA5IDE1LjM4MDIgMTEuNTM3OCAxNS4yMDAyIDExLjI5MTggMTQuOTY1MUw5LjMyMjg1IDE1Ljk1MDdMMTIuMTUxNyAyMC4xOTg3VjE1LjQ5MzFaTTIwLjE3MTQgMTcuNzQ5MUwxOC4wMTg2IDE2LjY3MjNMMTUuMjg0MSAyMC43Nzc5TDIwLjE3MTQgMTguMzMxNUMyMC4xNTU0IDE4LjIzNTUgMjAuMTQ1OCAxOC4xMzc5IDIwLjE0MjYgMTguMDQwM0MyMC4xNDU4IDE3Ljk0MjcgMjAuMTU1NCAxNy44NDUxIDIwLjE3MTQgMTcuNzQ5MVpNMTguOTEyIDE1LjMyOTlMMjAuMjA0OSAxNS45Nzc5TDE5LjM0MzUgMTQuNjgwM0wxOC45MTIgMTUuMzI5OVpNMjAuMjA0OSAxMC41MDI3TDE4LjkxMiAxMS4xNTA3TDE5LjM0MzUgMTEuODAwM0wyMC4yMDQ5IDEwLjUwMjdaTTYuOTg5NDkgMTEuMTQ0M0w1LjY5NjU2IDEwLjUwNDNMNi41NTc5OCAxMS44MDAzTDYuOTg5NDkgMTEuMTQ0M1pNNS42OTY1NiAxNS45Nzc5TDYuOTg5NDkgMTUuMzI5OUw2LjU1Nzk4IDE0LjY4MDNMNS42OTY1NiAxNS45Nzc5WiIgLz4KICAgICAgICAgICAgPC9zdmc+)

## AI-Generated Summary

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibnYtYWktc3VtbWFyeV9fdG9nZ2xlLWljb24iIHdpZHRoPSIxNCIgaGVpZ2h0PSI5IiB2aWV3Ym94PSIwIDAgMTQgOSIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiBhcmlhLWhpZGRlbj0idHJ1ZSI+CiAgICAgICAgPHBhdGggZD0iTTEyLjU3NDIgMkw3LjQ0OTIzIDdMMi4zMjQyNSAyIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0ic3F1YXJlIiAvPgogICAgPC9zdmc+)

- The [NVIDIA Vera Rubin platform](https://www.nvidia.com/en-us/data-center/technologies/rubin/) reimagines the data center as a single unit of compute to power agentic AI workloads that require sustained inference across many reasoning steps.
- The Rubin GPU delivers up to 10x more agentic throughput per unit of energy than NVIDIA Blackwell, using 336 billion transistors, 224 streaming multiprocessors, 896 Tensor Cores, and a third-generation Transformer Engine that provides up to 50 petaflops of NVFP4 performance.
- HBM4 memory doubles interface width to provide up to 22 TB/s of bandwidth and 288 GB of capacity per GPU, supporting multitrillion-parameter models, larger context windows, and high-concurrency inference without KV cache offload.
- NVLink 6 delivers 3,600 GB/s of scale-up bandwidth for all-to-all GPU communication, while counted writes streamline synchronization for device-initiated NVLink transfers to reduce latency in distributed inference.
- Vera Rubin NVL72 integrates compute, networking, liquid cooling, and Intelligent Power Smoothing into a rack-scale execution domain, with DSX MaxLPS enabling operators to provision up to 40% more GPUs within the same power budget.

### Next Steps

- Read the [Inside the NVIDIA Vera Rubin Platform: Six New Chips, One AI Supercomputer](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/) for a deeper look at the rack architecture and broader platform.
- Read the [NVIDIA Vera Rubin POD: Seven Chips, Five Rack-Scale Systems, One AI Supercomputer](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/) to learn more about NVIDIA Vera Rubin POD.

Powered by NVIDIA Nemotron. AI-generated content may summarize information incompletely. Verify important information. [Learn more](https://www.nvidia.com/en-us/agreements/trustworthy-ai/terms/)

What began as discrete AI model training and human-facing chat interfaces has evolved into always-on [AI factories](https://www.nvidia.com/en-us/glossary/ai-factory/) dedicated to producing intelligence at scale. These factories are now tasked with powering [agentic](https://www.nvidia.com/en-us/ai/) workflows that reason, plan, use tools, verify intermediate results, and execute complex multistep tasks across vast contexts.

Agentic workloads are not defined by a single prompt and response, but by sustained [inference](https://www.nvidia.com/en-us/glossary/ai-inference/) across many reasoning steps. They demand low per-step latency, high decode throughput, efficient long-context attention, large KV cache capacity, and the ability to scale models across tightly coupled GPU domains. The data center must be reimagined as a single unit of compute, a vision realized with the [NVIDIA Vera Rubin platform](https://www.nvidia.com/en-us/data-center/technologies/rubin/).

At the core of the platform is the NVIDIA Rubin GPU, designed to deliver up to 10x more agentic throughput per unit of energy than [NVIDIA Blackwell](https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/) (Figure 1). Enhanced [Tensor Cores](https://www.nvidia.com/en-us/data-center/tensor-cores/) with expanded precision flexibility, a new HBM4 memory subsystem, and the third-generation Transformer Engine—delivering up to 50 petaflops of [NVFP4](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/) performance—work together to accelerate agentic workloads efficiently.

![Chart comparing agent throughput and interactivity across NVIDIA Hopper, Blackwell, and Rubin systems, showing Rubin NVL72 plus Vera supports roughly 10 times more agents and twice as many tool calls. ](https://developer-blogs.nvidia.com/wp-content/uploads/2026/07/hopper-blackwell-rubin-throughput-interactivity-comparison.webp)

![Chart comparing agent throughput and interactivity across NVIDIA Hopper, Blackwell, and Rubin systems, showing Rubin NVL72 plus Vera supports roughly 10 times more agents and twice as many tool calls. ](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%201081%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 1. Pareto frontiers illustrating the 10x generational uplift in agentic inference performance of the Vera Rubin platform (internal 2T MoE workload)

This post examines how the NVIDIA Rubin GPU and its co-designed scale-up system address the end-to-end bottlenecks of agentic inference, from data movement and compute efficiency to long-context execution and rack-scale deployment. 

## How does Rubin GPU architecture support agentic workloads?[](#how_does_rubin_gpu_architecture_support_agentic_workloads)

The Rubin GPU (Figure 2) is constructed from reticle limited compute dies to achieve high density and efficiency. These two dies are unified on a single package through a high-speed inter-die link called the NVIDIA High-Bandwidth Interface (NV-HBI).

![Annotated diagram of the NVIDIA Rubin GPU, showing graphics processor clusters, HBM memory controllers, L2 cache, NVLink, PCIe Gen 6, and performance specifications. ](https://developer-blogs.nvidia.com/wp-content/uploads/2026/07/nvidia-rubin-gpu-chip-architecture-1.webp)

![Annotated diagram of the NVIDIA Rubin GPU, showing graphics processor clusters, HBM memory controllers, L2 cache, NVLink, PCIe Gen 6, and performance specifications. ](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%201237%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 2. NVIDIA Rubin GPU chip architecture

The architecture begins with the challenge of keeping an enormous amount of compute productive as agentic workloads shift between reasoning, generation, retrieval, and tool use. Its 336 billion transistors, 224 streaming multiprocessors (SMs), and 896 Tensor Cores provide the raw compute density, while the third-generation Transformer Engine adapts precision across numerical formats. That flexibility enables the Rubin GPU to deliver up to 50 petaflops of NVFP4 inference performance while preserving accuracy.

But performance depends on more than Tensor Core throughput. The Rubin GPU organizes compute resources into Graphics Processor Clusters (GPCs) with a large centralized L2 cache. The GigaThread Engine coordinates work, MIG Control partitions the GPU for multiple workloads, and NV-DEC accelerates decoding. Together, these capabilities help the Rubin GPU turn compute density into sustained utilization across the diverse and dynamic workloads that define large-scale agentic systems.

That utilization also depends on how quickly data can reach compute cores. Rubin integrates up to 288 GB of HBM4 memory, driven by dedicated HBM controllers and 12-Hi stacks, to deliver up to 22 TB/s of peak bandwidth. The enhanced Tensor Memory Accelerator (TMA) manages high-efficiency movement across complex data layouts, while [NVIDIA NVLink](https://www.nvidia.com/en-us/data-center/nvlink/) 6 provides 3,600 GB/s scale-up bandwidth to the NVLink Switch for all-to-all GPU-GPU communication, NVLink-C2C delivers 1,800 GB/s for coherent CPU-GPU communication, and x16 PCIe Gen 6 provides up to 256 GB/s of host connectivity.

Finally, large-scale agentic deployments must protect data as it moves through this execution domain. Confidential Computing with TEE-I/O is designed to secure data at rest, in transit, and in use across the AI factory. Together, these compute, memory, connectivity, and security capabilities form the GPU-level foundation for agentic workloads that must sustain efficient execution across increasingly large models and scale-up domains.

## How does the Rubin GPU accelerate critical inference paths? [](#how_does_the_rubin_gpu_accelerate_critical_inference_paths%C2%A0)

Peak compute alone is not enough to accelerate agentic inference. Real-world performance also depends on how efficiently the GPU moves data, executes matrix operations, processes long-context attention, and transitions between dependent kernels. This section explores the Rubin GPU features designed to reduce overhead in these critical execution paths. 

### Accelerating rack-scale MoE weight and token movement[](#accelerating_rack-scale_moe_weight_and_token_movement)

[Mixture-of-experts (MoE)](https://www.nvidia.com/en-us/glossary/mixture-of-experts/) models dynamically route tokens across many expert networks. As the number of experts grows, efficiently locating and moving expert weights becomes increasingly important to inference performance.

The Rubin GPU enhances the Tensor Memory Accelerator to reduce data-movement overhead for expert-heavy models. Its improved descriptor handling allows software to work more efficiently with tensors that share common layouts but reside at different locations in memory.

Rubin improves this with inline descriptor update support for TMA (Figure 3). Instead of modifying the descriptor in memory, the kernel can keep one unified descriptor for tensors that share the same layout and override fields such as the memory pointer and stride directly in the TMA instruction at runtime. 

![Side-by-side Blackwell and Rubin diagrams: Blackwell uses one MoE descriptor per expert, while Rubin shares one descriptor across all experts. ](https://developer-blogs.nvidia.com/wp-content/uploads/2026/07/rubin-gpu-moe-descriptor-sharing-1.webp)

![Side-by-side Blackwell and Rubin diagrams: Blackwell uses one MoE descriptor per expert, while Rubin shares one descriptor across all experts. ](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%20689%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 3. Rubin simplifies MoE descriptor sharing

This helps MoE models scale more efficiently as expert counts increase. By reducing metadata-management and data-movement overhead, Rubin enables more GPU time to be devoted to useful inference computation, supporting higher throughput for agentic workloads that rely on large MoE models.

### Doubling the efficiency of rack-scale matrix operations[](#doubling_the_efficiency_of_rack-scale_matrix_operations)

Rubin doubles the Tensor Core throughput per clock by doubling the amount of data it can process along the \\K\\ dimension. This optimization not only helps throughput bound kernels but also memory and latency bound kernels.

As model execution is split across many GPUs, each GPU often receives a smaller slice of the output work while the reduction dimension remains large. 

The benefit of a larger \\K\\ dimension is fewer \\K\\ loop iterations. In Figure 4, a GEMM that requires four \\K\\ iterations on Blackwell can be completed with two iterations on Rubin. Fewer iterations reduce loop overhead, improve Tensor Core utilization, and help both context and decode GEMMs run more efficiently at high tensor-parallel scale.

![Diagram showing Rubin processes a two-times larger K-dimension in two iterations, compared with four iterations on Blackwell. ](https://developer-blogs.nvidia.com/wp-content/uploads/2026/07/rubin-k-dimension-instruction-throughput-1.webp)

![Diagram showing Rubin processes a two-times larger K-dimension in two iterations, compared with four iterations on Blackwell. ](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%201178%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 4. Rubin doubles K-dimension instruction throughput

For models that benefit from even more compact weight representations, the Rubin Transformer Engine also supports a 3-bit lookup-table format for matrix B. Rather than store each weight directly, the format stores a 3-bit index into a small table of representative values and Rubin Tensor Cores resolve these indices inline to reduce weight storage and data movement. LUT-based representations can retain up to MXFP8 accuracy, adding another precision option to the Rubin inference toolbox.

### Addressing key challenges in long-context processing for agentic AI[](#addressing_key_challenges_in_long-context_processing_for_agentic_ai)

Long-context and agentic AI workloads put increasing pressure on attention. As context windows grow, the model must compare more tokens, normalize larger attention-score matrices, and apply those scores to the value data used to produce the next layer’s output. This makes attention one of the most important performance paths for improving tokens per second per user.

Rubin accelerates attention by combining activation sparsity with adaptive compression and improved softmax throughput. One simple, safe, and effective way to use Rubin’s new sparsity features in attention is as follows. The attention pipeline begins with a dense \\QK^T\\ computation to generate the intermediate attention scores. Rubin can then load that intermediate data from Tensor Memory into a structured 2:4 sparse compressed form, generating both nonzero values and the metadata needed to use them efficiently while reducing the scores’ write cost and storage requirements. This allows the later attention stages to operate on less data while preserving the dense output format expected by the rest of the model.

![Diagram showing a dense matrix converted to a sparse matrix with metadata, applied to attention and MLP activation stages in a transformer block.](https://developer-blogs.nvidia.com/wp-content/uploads/2026/07/nvidia-rubin-adaptive-compression-sparsity-1.webp)

![Diagram showing a dense matrix converted to a sparse matrix with metadata, applied to attention and MLP activation stages in a transformer block.](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%201214%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 5. Rubin sparsity features can be applied to the attention block and MLP block activations

This compressed intermediate representation reduces work in two key places: softmax and the second attention GEMM. Softmax can operate on the nonzero attention values, and the following multiplication with the dense \\V\\ matrix can use sparse MMA with the nonzeros from Softmax and the metadata from the original compression step. The result is less compute and data movement in the most expensive part of long-context attention improving tokens/watt, without requiring the surrounding model pipeline to change its interface.

Rubin also improves the softmax throughput. As Tensor Core throughput increases, softmax can become a bottleneck because it depends on exponential math and reductions across attention rows. Rubin increases exponential throughput, including 2x FP32 and 4x BF16/FP16 throughput versus the Blackwell baseline, helping softmax keep pace with faster matrix operations.

[TABLE]

Table 1. Exponential throughput rises from Blackwell to Rubin

* *Together, these features make the Rubin attention acceleration more than a single-kernel improvement. Activation sparsity reduces the amount of intermediate attention work, while faster exponentials reduce the softmax bottlenecks. 

### Improving kernel execution efficiency[](#improving_kernel_execution_efficiency)

As inference scales across larger models and more GPUs, raw Tensor Core throughput is only part of the performance story. The GPU also needs to move efficiently from one kernel to the next. In inference, this is especially important because activations often sit on the critical path: one kernel produces activation data, writes it to memory, and the next kernel consumes that data to continue generating the next token.

Traditional producer-consumer execution can create bubbles in the GPU timeline. A producer kernel may complete work for some tiles or thread blocks early, but the consumer may not begin useful work until a broader dependency is resolved. The Blackwell programmatic dependent launch improves this by allowing earlier consumer-kernel progress, but dependent work can still wait for required activation data to become available.

![Blackwell and Rubin timelines compare producer and consumer thread blocks; Rubin uses data-driven polling to begin consumer work sooner as producer data becomes available. ](https://developer-blogs.nvidia.com/wp-content/uploads/2026/07/blackwell-rubin-timelines-producer-consumer-thread-blocks-1.webp)

![Blackwell and Rubin timelines compare producer and consumer thread blocks; Rubin uses data-driven polling to begin consumer work sooner as producer data becomes available. ](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%201042%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 6. Producer-consumer overlap: Blackwell bulk triggering (above) and Rubin tile-level triggering (below)

Rubin enables more fine-grained coordination between dependent kernels. This allows consumer work to begin earlier as required input data becomes available, rather than waiting for a larger set of producer work to complete.

The result is a more tightly packed GPU timeline, reduced idle gaps, and improved overlap between dependent kernels. This is particularly valuable for agentic inference, where activations move sequentially through the model and kernel-to-kernel latency directly affects tokens per second per user.

## How do Rubin memory and communication sustain high-throughput inference? [](#how_do_rubin_memory_and_communication_sustain_high-throughput_inference%C2%A0)

As models, context windows, and GPU domains grow, data movement becomes as important as computation. Rubin is designed to improve the flow of weights, activations, KV cache data, and communication traffic within the GPU and across scale-up systems. The following sections look at the memory and communication innovations that help sustain high-throughput inference.

### Accelerated scale-up communications[](#accelerated_scale-up_communications)

As inference scales from a single GPU to full rack-level systems, communication becomes part of the critical performance path. When communication is fused directly inside a GPU kernel, the kernel does not stop and hand control back to the CPU; it directly writes data or performs reductions over NVLink to another GPU while computation is still in flight.

Traditional GPU-to-GPU communication requires coordination and synchronization work in addition to moving payload data. These steps can add latency and consume interconnect bandwidth, particularly when communication occurs frequently within distributed inference workloads.

Rubin introduces counted writes for device-initiated NVLink communication. This capability streamlines synchronization for GPU-to-GPU data transfers by allowing the receiving GPU to track transfer completion more efficiently.

![Side-by-side communication diagrams show Blackwell using memory barriers, acknowledgments, and atomic flags, while Rubin uses a counter update before the receiving GPU loads data. ](https://developer-blogs.nvidia.com/wp-content/uploads/2026/07/rubin-nvlink-communication-acceleration.webp)

![Side-by-side communication diagrams show Blackwell using memory barriers, acknowledgments, and atomic flags, while Rubin uses a counter update before the receiving GPU loads data. ](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%20895%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 7. Rubin accelerates NVLink communications using counted writes

NVLink fused communication with counted writes provides a lower-latency mechanism for coordinating GPU-to-GPU data movement, helping keep computation moving instead of waiting on synchronization operations. 

### Co-designing a memory subsystem for maximum power and compute efficiency[](#co-designing_a_memory_subsystem_for_maximum_power_and_compute_efficiency)

The decode, or generation, phase of inference is fundamentally memory subsystem bound. It is not about peak bandwidth specs but rather how efficiently each kernel can utilize the entire memory subsystem. Modern reasoning and agentic workloads amplify this constraint by spending more end-to-end runtime in decode: long contexts, large KV caches, and interactive token generation make achieved memory bandwidth a critical performance lever.

![Bar chart comparing Blackwell, Blackwell Ultra, and Rubin GPUs: Bandwidth rises from 8 TB/s to 22 TB/s on Rubin. ](https://developer-blogs.nvidia.com/wp-content/uploads/2026/07/memory-bandwidth-nvidia-rubin-gpu.webp)

![Bar chart comparing Blackwell, Blackwell Ultra, and Rubin GPUs: Bandwidth rises from 8 TB/s to 22 TB/s on Rubin. ](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%20944%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 8. Memory bandwidth scaling from Blackwell to Rubin

Rubin addresses this with HBM4 combined with a highly efficient localized memory subsystem. HBM4 doubles interface width relative to HBM3e. Combined with a new memory controller, deep co-engineering with the memory ecosystem, and tighter compute-memory integration, this subsystem provides up to 22 TB/s of memory bandwidth: a 2.8x increase over Blackwell and Blackwell Ultra.

Rubin also provides up to 288 GB of HBM4 per GPU, increasing available on-package capacity relative to Blackwell. Capacity and bandwidth play different but complementary roles:

- **Capacity:** Supports model residency, larger context windows, larger KV caches, and higher concurrency without unnecessary KV-cache offload.
- **Bandwidth:** Supports the token-by-token generation phase, during which model weights and KV state must be moved rapidly enough to keep compute engines productive.
- **Memory subsystem:** TMA and memory-locality strategies help software use the memory subsystem efficiently, supporting high achieved bandwidth for complex data layouts.

High-capacity, high-bandwidth HBM4 is critical for hosting multitrillion-parameter models, extending context length without KV cache offload, and supporting high-concurrency, long-horizon inference workloads.

## How is NVIDIA designing for efficiency, scalability, and reliability?[](#how_is_nvidia_designing_for_efficiency_scalability_and_reliability)

Agentic AI infrastructure must optimize more than individual GPUs; it must make effective use of power, cooling, networking, and rack-level resources across the entire AI factory. [NVIDIA Vera Rubin NVL72](https://www.nvidia.com/en-us/data-center/vera-rubin-nvl72/) extends the GPU architecture into an integrated, resilient rack-scale execution domain. This section examines how NVIDIA approaches power efficiency, operational scalability, and system-level reliability. 

### Increasing the number of GPUs within the same power budget[](#increasing_the_number_of_gpus_within_the_same_power_budget)

Agentic AI makes energy efficiency an AI-factory problem, not simply a GPU power problem. At rack scale, Vera Rubin NVL72 integrates compute, networking, liquid cooling, power steering, and Intelligent Power Smoothing with energy storage into a single execution domain designed to maximize useful token output within a fixed power envelope.

![GPU power chart shows capacitors covering spikes and filling idle-time valleys to maintain a steadier sustained AC power input. ](https://developer-blogs.nvidia.com/wp-content/uploads/2026/07/gpu-power-chart.webp)

![GPU power chart shows capacitors covering spikes and filling idle-time valleys to maintain a steadier sustained AC power input. ](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%20864%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 9. GPU power plot showing impact of power smoothing techniques

Power demand can vary sharply during AI workloads, creating transient peaks that strand available capacity and reduce factory-level throughput. Vera Rubin power supplies use state-of-charge (SoC) Intelligent Power Smoothing to absorb these swings, reducing average power consumption by approximately 10% compared with previous-generation power-smoothing techniques and reducing 50 ms peak power by approximately 20%. By delivering a steadier power profile, the system can reduce sustained maximum power requirements, benefit supporting power infrastructure and the grid, and enable more compute within the same AI factory power budget. 

At the AI-factory level, [NVIDIA DSX MaxLPS](https://www.nvidia.com/en-us/data-center/products/dsx/) extends this approach across GPUs, racks, 45°C liquid cooling, and workloads, while DSX OS provides the operational layer for scheduling, lifecycle management, and health automation. Together, they are designed to recover stranded power and increase useful compute within a fixed megawatt envelope. DSX MaxLPS can enable operators to provision up to 40% more GPUs (Figure 10) within the same power budget at energy-efficient operating points, with minimal impact on workload performance.

![Grid comparison shows unused AI factory capacity without DSX MaxLPS and up to 40% more GPU slots using DSX MaxLPS under the same power budget. ](https://developer-blogs.nvidia.com/wp-content/uploads/2026/07/power-budget-comparison-dsx-maxlps-1.webp)

![Grid comparison shows unused AI factory capacity without DSX MaxLPS and up to 40% more GPU slots using DSX MaxLPS under the same power budget. ](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%20938%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 10. For the same power budget, DSX MaxLPS enables up to 40% more GPUs

### Designing racks for resiliency and data center scalability[](#designing_racks_for_resiliency_and_data_center_scalability)

Vera Rubin NVL72 extends the Rubin GPU into a rack-scale execution domain for multitrillion-parameter and multi-rack agentic workloads. Its third-generation MGX rack architecture combines cable-free compute and switch trays, 45°C liquid cooling, dynamic rack-scale power steering, and Intelligent Power Smoothing to keep compute, networking, cooling, and power operating as one system. Hot-swappable NVLink switch trays and improved RAS capabilities further support resilient operation at scale.

This rack design is the foundation for pod-scale, multi-rack agentic systems, with open and flexible connectivity across NVLink and [NVIDIA Spectrum-X Ethernet](https://www.nvidia.com/en-us/networking/spectrumx/). 

## Learn more[](#learn_more)

The NVIDIA Rubin GPU is designed for the execution patterns of agentic AI, where long-context reasoning, multistep generation, distributed MoE decode, and low-latency interaction must operate continuously at scale. Its compute, memory, networking, rack-scale, power, cooling, and software layers are carefully co-designed to keep more of the AI factory performing useful work rather than waiting on data, communication, or power constraints. The result is an architecture built to maximize agentic performance per watt—producing more useful tokens and completed AI work within a fixed power envelope. 

For a deeper look at the rack architecture and the broader NVIDIA Vera Rubin platform, see [Inside the NVIDIA Vera Rubin Platform: Six New Chips, One AI Supercomputer](https://developer.nvidia.com/blog/inside-the-nvidia-rubin-platform-six-new-chips-one-ai-supercomputer/). To learn more about NVIDIA Vera Rubin POD, see [NVIDIA Vera Rubin POD: Seven Chips, Five Rack-Scale Systems, One AI Supercomputer](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/).

### Acknowledgments[](#acknowledgments)

*This work was made possible through the expertise and engineering contributions of Jeff Pool, Ran Zilberstein, Ronny Krashinksky, Sailaja Madduri, Shivam Raj, Xiaowei Wang, Manas Mandal, Bita Darvish, Raj Dash,* *and many other talented NVIDIA engineers.*

[ Discuss (0)](#entry-content-comments)

Like

## Tags

[Agentic AI / Generative AI](https://developer.nvidia.com/blog/category/generative-ai/) \| [Data Center / Cloud](https://developer.nvidia.com/blog/category/data-center-cloud/) \| [Developer Tools & Techniques](https://developer.nvidia.com/blog/category/development/) \| [General](https://developer.nvidia.com/blog/recent-posts/?industry=General) \| [Blackwell](https://developer.nvidia.com/blog/recent-posts/?products=Blackwell) \| [NVLink](https://developer.nvidia.com/blog/recent-posts/?products=NVLink) \| [Spectrum-X Ethernet](https://developer.nvidia.com/blog/recent-posts/?products=Spectrum-X+Ethernet) \| [Intermediate Technical](https://developer.nvidia.com/blog/recent-posts/?learning_levels=Intermediate+Technical) \| [Deep dive](https://developer.nvidia.com/blog/recent-posts/?content_types=Deep+dive) \| [AI Agent](https://developer.nvidia.com/blog/tag/ai-agent/) \| [AI Factory](https://developer.nvidia.com/blog/tag/ai-factory/) \| [AI Inference](https://developer.nvidia.com/blog/tag/ai-inference-microservices/) \| [DSX](https://developer.nvidia.com/blog/tag/dsx/) \| [featured](https://developer.nvidia.com/blog/tag/featured/) \| [Mixture of Experts (MoE)](https://developer.nvidia.com/blog/tag/mixture-of-experts-moe/) \| [NVFP4](https://developer.nvidia.com/blog/tag/nvfp4/) \| [Rubin GPU](https://developer.nvidia.com/blog/tag/rubin-gpu/) \| [Tensor Cores](https://developer.nvidia.com/blog/tag/tensor-cores/) \| [Vera Rubin](https://developer.nvidia.com/blog/tag/vera-rubin/)

## About the Authors

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2026/05/cropped-EAA_Headshot-131x131.webp)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Eduardo Alvarez**  
Eduardo Alvarez is a senior technical lead at NVIDIA, where he focuses on AI inference at scale, performance optimization, workload economic analysis, and application enablement. He has a deep background in AI systems engineering, workload optimization, and accelerated computing—focused on translating innovations into real-world applications. Before NVIDIA, Eduardo held engineering roles at various semiconductor and energy tech companies.

[View all posts by Eduardo Alvarez![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/edualvarez/)

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2021/02/vishal-131x131.png)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Vishal Mehta**  
Vishal works as a senior developer technology engineer at NVIDIA, with focus on performance optimization for GPU applications. He has been working in the field of GPU computing for over 10 years. He is keen on teaching CUDA and GPU computing to users and drives the content for the CUDA programming guide. His day-to-day activities involve collaborations with domain scientists and industry experts to improve their workloads on GPUs.

[View all posts by Vishal Mehta![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/vishalm/)

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2025/08/cropped-image4-3-131x131.jpg)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Farshad Ghodsian**  
Farshad Ghodsian is a senior technical marketing engineer at NVIDIA, where he focuses on AI training and inference at scale, performance optimization insights, new model releases, and AI engineering enablement. He brings a wealth of experience at the intersection of AI infrastructure, distributed training, GPU-accelerated computing and cloud-native MLOps—translating cutting-edge research into practical insights for developers, enterprise teams and business leaders. Prior to NVIDIA, Farshad held technical roles at leading semiconductor and consulting companies, where he helped build and manage large-scale generative AI and MLOps platforms for top technology customers.

[View all posts by Farshad Ghodsian![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/farshadghodsian/)

## Comments

Comments are closed.
