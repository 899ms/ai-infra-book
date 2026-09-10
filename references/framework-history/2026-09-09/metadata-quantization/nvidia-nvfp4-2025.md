<!-- 从 nvidia-nvfp4-2025.html 迁移的资料快照；原始 HTML SHA-256: 3b061dc9278d69451df6c5a7053ea154547bbaf6e59e64dce7ba827097c1b0ed。 -->

[Data Center / Cloud](https://developer.nvidia.com/blog/category/data-center-cloud/)

English中文

# Introducing NVFP4 for Efficient and Accurate Low-Precision Inference

![](https://developer-blogs.nvidia.com/wp-content/uploads/2025/06/nvidia-blackwell-1024x576-png.webp)

Jun 24, 2025

By [Eduardo Alvarez](https://developer.nvidia.com/blog/author/edualvarez/ "Posts by Eduardo Alvarez"), [Omri Almog](https://developer.nvidia.com/blog/author/oalmog/ "Posts by Omri Almog"), [Eric Chung](https://developer.nvidia.com/blog/author/erchung/ "Posts by Eric Chung"), [Simon Layton](https://developer.nvidia.com/blog/author/slayton/ "Posts by Simon Layton"), [Dusan Stosic](https://developer.nvidia.com/blog/author/dstosic/ "Posts by Dusan Stosic"), [Ronny Krashinsky](https://developer.nvidia.com/blog/author/rkrashinsky/ "Posts by Ronny Krashinsky") and [Kyle Aubrey](https://developer.nvidia.com/blog/author/kaubrey/ "Posts by Kyle Aubrey")

Like

[ Discuss (3)](#entry-content-comments)

- [L](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fintroducing-nvfp4-for-efficient-and-accurate-low-precision-inference%2F)
- [T](https://twitter.com/intent/tweet?text=Introducing+NVFP4+for+Efficient+and+Accurate+Low-Precision+Inference+%7C+NVIDIA+Technical+Blog+https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fintroducing-nvfp4-for-efficient-and-accurate-low-precision-inference%2F)
- [F](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fintroducing-nvfp4-for-efficient-and-accurate-low-precision-inference%2F)
- [R](https://www.reddit.com/submit?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fintroducing-nvfp4-for-efficient-and-accurate-low-precision-inference%2F&title=Introducing+NVFP4+for+Efficient+and+Accurate+Low-Precision+Inference+%7C+NVIDIA+Technical+Blog)
- [E](mailto:?subject=I'd%20like%20to%20share%20a%20link%20with%20you&body=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fintroducing-nvfp4-for-efficient-and-accurate-low-precision-inference%2F)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibnYtYWktc3VtbWFyeV9faWNvbiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iMjUiIGhlaWdodD0iMjUiIHZpZXdib3g9IjAgMCAyNSAyNSIgZmlsbD0ibm9uZSIgYXJpYS1oaWRkZW49InRydWUiPgogICAgICAgICAgICAgICAgPHBhdGggZmlsbD0iY3VycmVudENvbG9yIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTIyLjQ5MTUgMTUuMzAxOUMyMi4yOTQgMTUuMzA0NyAyMi4wOTc2IDE1LjMzMTYgMjEuOTA2NiAxNS4zODE5TDIwLjI1NCAxMi45MDE5TDIxLjkwNSAxMC40MjE5QzIyLjA5NjcgMTAuNDczMSAyMi4yOTMzIDEwLjQ5ODcgMjIuNDkxNSAxMC41MDE5QzIyLjg4NDQgMTAuNTAzMiAyMy4yNzE2IDEwLjQwNzggMjMuNjE5IDEwLjIyNDFDMjMuOTY2NSAxMC4wNDA0IDI0LjI2MzUgOS43NzQwNSAyNC40ODM5IDkuNDQ4NDVDMjQuNzA0NCA5LjEyMjg1IDI0Ljg0MTUgOC43NDc5OSAyNC44ODMyIDguMzU2ODdDMjQuOTI1IDcuOTY1NzUgMjQuODcwMSA3LjU3MDM1IDI0LjcyMzMgNy4yMDU0N0MyNC41NzY2IDYuODQwNTkgMjQuMzQyNSA2LjUxNzQxIDI0LjA0MTcgNi4yNjQzN0MyMy43NDA5IDYuMDExMzQgMjMuMzgyNSA1LjgzNjIgMjIuOTk4MiA1Ljc1NDM3QzIyLjYxMzkgNS42NzI1NSAyMi4yMTU0IDUuNjg2NTQgMjEuODM3OCA1Ljc5NTEyQzIxLjQ2MDEgNS45MDM3IDIxLjExNDkgNi4xMDM1NCAyMC44MzI2IDYuMzc3MDZMMTUuMjcwOSAzLjU5MzA1QzE1LjI4NjggMy40OTcwNSAxNS4yOTY0IDMuMzk5NDYgMTUuMjk5NiAzLjMwMTg2QzE1LjI5OTYgMi42NjUzNCAxNS4wNDcxIDIuMDU0ODkgMTQuNTk3NSAxLjYwNDhDMTQuMTQ3OSAxLjE1NDcxIDEzLjUzODEgMC45MDE4NTUgMTIuOTAyMyAwLjkwMTg1NUMxMi4yNjY1IDAuOTAxODU1IDExLjY1NjggMS4xNTQ3MSAxMS4yMDcyIDEuNjA0OEMxMC43NTc2IDIuMDU0ODkgMTAuNTA1MSAyLjY2NTM0IDEwLjUwNTEgMy4zMDE4NkMxMC41MDgzIDMuMzk5NDYgMTAuNTE3OCAzLjQ5NzA1IDEwLjUzMzggMy41OTMwNUw0Ljk3MjExIDYuMzc3MDZDNC42ODk3NiA2LjEwMjY3IDQuMzQ0MzMgNS45MDIwMiAzLjk2NjI2IDUuNzkyODFDMy41ODgxOCA1LjY4MzYgMy4xODkwOCA1LjY2OTE4IDIuODA0MTIgNS43NTA4MkMyLjQxOTE2IDUuODMyNDUgMi4wNjAxOCA2LjAwNzY0IDEuNzU4OCA2LjI2MDkzQzEuNDU3NDMgNi41MTQyMyAxLjIyMjkyIDYuODM3ODYgMS4wNzU5NSA3LjIwMzI5QzAuOTI4OTgxIDcuNTY4NzIgMC44NzQwNTggNy45NjQ3NCAwLjkxNjAyOCA4LjM1NjQ0QzAuOTU3OTk4IDguNzQ4MTMgMS4wOTU1NyA5LjEyMzQ4IDEuMzE2NjIgOS40NDkzOUMxLjUzNzY3IDkuNzc1MyAxLjgzNTQgMTAuMDQxOCAyLjE4MzU4IDEwLjIyNTNDMi41MzE3NiAxMC40MDg4IDIuOTE5NyAxMC41MDM4IDMuMzEzMTkgMTAuNTAxOUMzLjUxMTM2IDEwLjQ5ODcgMy43MDc5NCAxMC40NzE1IDMuODk4MTMgMTAuNDIxOUw1LjU1MDY2IDEyLjkwMTlMMy44OTk3MyAxNS4zODE5QzMuNzA4MTggMTUuMzMxNCAzLjUxMTIyIDE1LjMwNDYgMy4zMTMxOSAxNS4zMDE5QzIuOTIwMjkgMTUuMzAwNSAyLjUzMzA4IDE1LjM5NTkgMi4xODU2NSAxNS41Nzk2QzEuODM4MjIgMTUuNzYzMyAxLjU0MTIyIDE2LjAyOTcgMS4zMjA3NyAxNi4zNTUzQzEuMTAwMzIgMTYuNjgwOSAwLjk2MzE4OSAxNy4wNTU3IDAuOTIxNDQyIDE3LjQ0NjhDMC44Nzk2OTUgMTcuODM4IDAuOTM0NjEzIDE4LjIzMzQgMS4wODEzNiAxOC41OTgyQzEuMjI4MTEgMTguOTYzMSAxLjQ2MjE5IDE5LjI4NjMgMS43NjMwMSAxOS41MzkzQzIuMDYzODIgMTkuNzkyNCAyLjQyMjE1IDE5Ljk2NzUgMi44MDY0NiAyMC4wNDkzQzMuMTkwNzcgMjAuMTMxMiAzLjU4OTI4IDIwLjExNzIgMy45NjY5MSAyMC4wMDg2QzQuMzQ0NTUgMTkuOSA0LjY4OTc0IDE5LjcwMDIgNC45NzIxMSAxOS40MjY3TDEwLjUzMzggMjIuMjEwN0MxMC41MTc4IDIyLjMwNjcgMTAuNTA4MyAyMi40MDQzIDEwLjUwNTEgMjIuNTAxOUMxMC41MDUxIDIzLjEzODQgMTAuNzU3NiAyMy43NDg4IDExLjIwNzIgMjQuMTk4OUMxMS42NTY4IDI0LjY0OSAxMi4yNjY1IDI0LjkwMTkgMTIuOTAyMyAyNC45MDE5QzEzLjUzODEgMjQuOTAxOSAxNC4xNDc5IDI0LjY0OSAxNC41OTc1IDI0LjE5ODlDMTUuMDQ3MSAyMy43NDg4IDE1LjI5OTYgMjMuMTM4NCAxNS4yOTk2IDIyLjUwMTlDMTUuMjk1OCAyMi40MDQzIDE1LjI4NjIgMjIuMzA3MSAxNS4yNzA5IDIyLjIxMDdMMjAuODMyNiAxOS40MjY3QzIxLjExNDkgMTkuNzAxIDIxLjQ2MDQgMTkuOTAxNyAyMS44Mzg0IDIwLjAxMDlDMjIuMjE2NSAyMC4xMjAxIDIyLjYxNTYgMjAuMTM0NSAyMy4wMDA2IDIwLjA1MjlDMjMuMzg1NSAxOS45NzEzIDIzLjc0NDUgMTkuNzk2MSAyNC4wNDU5IDE5LjU0MjhDMjQuMzQ3MyAxOS4yODk1IDI0LjU4MTggMTguOTY1OSAyNC43Mjg3IDE4LjYwMDRDMjQuODc1NyAxOC4yMzUgMjQuOTMwNiAxNy44MzkgMjQuODg4NyAxNy40NDczQzI0Ljg0NjcgMTcuMDU1NiAyNC43MDkxIDE2LjY4MDIgMjQuNDg4MSAxNi4zNTQzQzI0LjI2NyAxNi4wMjg0IDIzLjk2OTMgMTUuNzYxOSAyMy42MjExIDE1LjU3ODRDMjMuMjcyOSAxNS4zOTQ5IDIyLjg4NSAxNS4yOTk5IDIyLjQ5MTUgMTUuMzAxOVpNMTIuODg4NCAyLjUwMjc0QzEzLjAxODUgMi41MDMyNCAxMy4xNDY1IDIuNTM1NTIgMTMuMjYxMyAyLjU5Njc5QzEzLjM3NjEgMi42NTgwNSAxMy40NzQyIDIuNzQ2NDQgMTMuNTQ3MSAyLjg1NDI5QzEzLjYyIDIuOTYyMTQgMTMuNjY1NSAzLjA4NjE3IDEzLjY3OTcgMy4yMTU2M0MxMy42OTM5IDMuMzQ1MDkgMTMuNjc2MyAzLjQ3NjA1IDEzLjYyODQgMy41OTcxNEwxMy42MDYgMy42NDE5NEMxMy41NDI5IDMuNzc5ODEgMTMuNDQxNiAzLjg5NjY0IDEzLjMxNDEgMy45Nzg1NUMxMy4xODY2IDQuMDYwNDUgMTMuMDM4MyA0LjEwMzk5IDEyLjg4NjggNC4xMDM5OUMxMi43MzUzIDQuMTAzOTkgMTIuNTg3IDQuMDYwNDUgMTIuNDU5NiAzLjk3ODU1QzEyLjMzMjEgMy44OTY2NCAxMi4yMzA3IDMuNzc5ODEgMTIuMTY3NiAzLjY0MTk0TDEyLjE0NTMgMy41OTg3NEMxMi4wOTcgMy40NzczMSAxMi4wNzkxIDMuMzQ1ODkgMTIuMDkzMyAzLjIxNTk2QzEyLjEwNzQgMy4wODYwMyAxMi4xNTMyIDIuOTYxNTYgMTIuMjI2NSAyLjg1MzQyQzEyLjI5OTggMi43NDUyOCAxMi4zOTg1IDIuNjU2NzggMTIuNTEzOSAyLjU5NTY0QzEyLjYyOTMgMi41MzQ1MSAxMi43NTc5IDIuNTAyNjEgMTIuODg4NCAyLjUwMjc0Wk0yMy4yNzY3IDguMTAyNzRDMjMuMjc2NyA4LjMxNDkxIDIzLjE5MjUgOC41MTg0IDIzLjA0MjYgOC42Njg0M0MyMi44OTI4IDguODE4NDUgMjIuNjg5NSA4LjkwMjc0IDIyLjQ3NzYgOC45MDI3NEMyMi4yNjU2IDguOTAyNzQgMjIuMDYyNCA4LjgxODQ1IDIxLjkxMjUgOC42Njg0M0MyMS43NjI3IDguNTE4NCAyMS42Nzg1IDguMzE0OTEgMjEuNjc4NSA4LjEwMjc0QzIxLjY3ODUgNy44OTA1NyAyMS43NjI3IDcuNjg3MDggMjEuOTEyNSA3LjUzNzA1QzIyLjA2MjQgNy4zODcwMiAyMi4yNjU2IDcuMzAyNzQgMjIuNDc3NiA3LjMwMjc0QzIyLjY4OTUgNy4zMDI3NCAyMi44OTI4IDcuMzg3MDIgMjMuMDQyNiA3LjUzNzA1QzIzLjE5MjUgNy42ODcwOCAyMy4yNzY3IDcuODkwNTcgMjMuMjc2NyA4LjEwMjc0Wk0yLjUwMDE3IDguMTAyNzRDMi41MDMgNy45MjMwNSAyLjU2NjE3IDcuNzQ5NTYgMi42Nzk1MSA3LjYxMDJDMi43OTI4NSA3LjQ3MDg1IDIuOTQ5NzYgNy4zNzM3NiAzLjEyNDk1IDcuMzM0NThDMy4zMDAxNCA3LjI5NTQgMy40ODM0IDcuMzE2NDEgMy42NDUyIDcuMzk0MjNDMy44MDcgNy40NzIwNSAzLjkzNzkyIDcuNjAyMTQgNC4wMTY4NSA3Ljc2MzU0TDQuMDM5MjMgNy44MDgzNEM0LjA5ODcxIDcuOTUzMDYgNC4xMTM3NiA4LjExMjI1IDQuMDgyNDQgOC4yNjU1OEM0LjA1MTEzIDguNDE4OSAzLjk3NDg4IDguNTU5NDEgMy44NjM0MyA4LjY2OTE0QzMuNzUxNTggOC43ODA3NiAzLjYwOTIxIDguODU2NyAzLjQ1NDI4IDguODg3MzdDMy4yOTkzNiA4LjkxODA1IDMuMTM4ODMgOC45MDIwNyAyLjk5Mjk3IDguODQxNDdDMi44NDcxIDguNzgwODYgMi43MjI0NSA4LjY3ODM1IDIuNjM0NzQgOC41NDY4N0MyLjU0NzAzIDguNDE1MzkgMi41MDAyIDguMjYwODQgMi41MDAxNyA4LjEwMjc0Wk0yLjUwMDE3IDE3LjcwMjdDMi41MDAxNyAxNy40OTA2IDIuNTg0MzYgMTcuMjg3MSAyLjczNDIyIDE3LjEzNzFDMi44ODQwOCAxNi45ODcgMy4wODczMyAxNi45MDI3IDMuMjk5MjcgMTYuOTAyN0MzLjUxMTIgMTYuOTAyNyAzLjcxNDQ1IDE2Ljk4NyAzLjg2NDMxIDE3LjEzNzFDNC4wMTQxNyAxNy4yODcxIDQuMDk4MzYgMTcuNDkwNiA0LjA5ODM2IDE3LjcwMjdDNC4wOTgzNiAxNy45MTQ5IDQuMDE0MTcgMTguMTE4NCAzLjg2NDMxIDE4LjI2ODRDMy43MTQ0NSAxOC40MTg1IDMuNTExMiAxOC41MDI3IDMuMjk5MjcgMTguNTAyN0MzLjA4NzMzIDE4LjUwMjcgMi44ODQwOCAxOC40MTg1IDIuNzM0MjIgMTguMjY4NEMyLjU4NDM2IDE4LjExODQgMi41MDAxNyAxNy45MTQ5IDIuNTAwMTcgMTcuNzAyN1pNMTIuODg4NCAyMy4zMDI3QzEyLjc1NjYgMjMuMzAyOCAxMi42MjY4IDIzLjI3MDIgMTIuNTEwNiAyMy4yMDc4QzEyLjM5NDQgMjMuMTQ1NSAxMi4yOTU1IDIzLjA1NTMgMTIuMjIyNSAyMi45NDU0QzEyLjE0OTYgMjIuODM1NSAxMi4xMDQ5IDIyLjcwOTIgMTIuMDkyNiAyMi41Nzc4QzEyLjA4MDIgMjIuNDQ2NCAxMi4xMDA1IDIyLjMxNCAxMi4xNTE3IDIyLjE5MjNDMTIuMjEyOCAyMi4wNTE5IDEyLjMxMjkgMjEuOTMxOSAxMi40NDAxIDIxLjg0NjhDMTIuNTY3MyAyMS43NjE2IDEyLjcxNjMgMjEuNzE0OCAxMi44NjkzIDIxLjcxMkMxMy4wMjIzIDIxLjcwOTEgMTMuMTcyOSAyMS43NTAzIDEzLjMwMzIgMjEuODMwNkMxMy40MzM2IDIxLjkxMSAxMy41MzgxIDIyLjAyNzEgMTMuNjA0NCAyMi4xNjUxTDEzLjYyNjggMjIuMjA5OUMxMy42ODY4IDIyLjM1NDEgMTMuNzAyNCAyMi41MTI5IDEzLjY3MTYgMjIuNjY1OUMxMy42NDA5IDIyLjgxOSAxMy41NjUxIDIyLjk1OTQgMTMuNDU0MiAyMy4wNjkxQzEzLjM3OTggMjMuMTQzNCAxMy4yOTE2IDIzLjIwMjIgMTMuMTk0NSAyMy4yNDIzQzEzLjA5NzQgMjMuMjgyNCAxMi45OTM0IDIzLjMwMjkgMTIuODg4NCAyMy4zMDI3Wk0yMi40Nzc2IDE4LjUwMjdDMjIuMzI2NyAxOC41MDE2IDIyLjE3OTMgMTguNDU3NyAyMi4wNTIzIDE4LjM3NjFDMjEuOTI1MyAxOC4yOTQ2IDIxLjgyNCAxOC4xNzg3IDIxLjc2IDE4LjA0MTlMMjEuNzM3NiAxNy45OTcxQzIxLjY5ODEgMTcuOTAyOSAyMS42Nzc3IDE3LjgwMTcgMjEuNjc3NyAxNy42OTk1QzIxLjY3NzcgMTcuNTk3MyAyMS42OTgxIDE3LjQ5NjIgMjEuNzM3NiAxNy40MDE5TDIxLjc1MiAxNy4zNzQ3QzIxLjgwOTggMTcuMjQyMiAyMS45MDIzIDE3LjEyNzkgMjIuMDE5OSAxNy4wNDM4QzIyLjEzNzQgMTYuOTU5OCAyMi4yNzU1IDE2LjkwOTIgMjIuNDE5NCAxNi44OTc0QzIyLjU2MzMgMTYuODg1NyAyMi43MDc4IDE2LjkxMzIgMjIuODM3MyAxNi45NzcxQzIyLjk2NjkgMTcuMDQwOSAyMy4wNzY4IDE3LjEzODggMjMuMTU1MiAxNy4yNjAxQzIzLjIzMzcgMTcuMzgxNSAyMy4yNzc4IDE3LjUyMTkgMjMuMjgzIDE3LjY2NjRDMjMuMjg4MSAxNy44MTA5IDIzLjI1NCAxNy45NTQxIDIzLjE4NDMgMTguMDgwOEMyMy4xMTQ2IDE4LjIwNzQgMjMuMDEyIDE4LjMxMjggMjIuODg3MiAxOC4zODU3QzIyLjc2MjUgMTguNDU4NiAyMi42MjA0IDE4LjQ5NjMgMjIuNDc2IDE4LjQ5NDdMMjIuNDc3NiAxOC41MDI3Wk0xOC4wMTg2IDkuODA4MzRMMjAuMTcxNCA4LjczMTU0QzIwLjE1NTQgOC42MzU1NCAyMC4xNDU4IDguNTM3OTQgMjAuMTQyNiA4LjQ0MDM0QzIwLjE0NTggOC4zNDI3NCAyMC4xNTU0IDguMjQ1MTQgMjAuMTcxNCA4LjE0OTE0TDE1LjI4NDEgNS43MDI3NEwxOC4wMTg2IDkuODA4MzRaTTEwLjYxNTggNS43MDQzNEw1LjczMDEyIDguMTQ5MTRDNS43NDU0NSA4LjI0NTU1IDUuNzU1MDUgOC4zNDI3OSA1Ljc1ODg4IDguNDQwMzRDNS43NTU2OSA4LjUzNzk0IDUuNzQ2MSA4LjYzNTU0IDUuNzMwMTIgOC43MzE1NEw3Ljg4Mjg4IDkuODA4MzRMMTAuNjE1OCA1LjcwNDM0Wk01LjczMDEyIDE3Ljc0OTFMNy44ODI4OCAxNi42NzIzTDEwLjYxNzQgMjAuNzc3OUw1LjczMDEyIDE4LjMzMTVDNS43NDYxIDE4LjIzNTUgNS43NTU2OSAxOC4xMzc5IDUuNzU4ODggMTguMDQwM0M1Ljc1NTA1IDE3Ljk0MjggNS43NDU0NSAxNy44NDU2IDUuNzMwMTIgMTcuNzQ5MVpNMTIuMjEwOCAxMy41MzYzTDEyLjIzMzIgMTMuNTc5NUgxMi4yMzY0QzEyLjMgMTMuNzE3NSAxMi40MDIxIDEzLjgzNDEgMTIuNTMwMyAxMy45MTU1QzEyLjY1ODUgMTMuOTk2OCAxMi44MDc0IDE0LjAzOTUgMTIuOTU5MiAxNC4wMzgzQzEzLjExMDkgMTQuMDM3MSAxMy4yNTkyIDEzLjk5MjEgMTMuMzg2MSAxMy45MDg4QzEzLjUxMyAxMy44MjU1IDEzLjYxMzIgMTMuNzA3MiAxMy42NzQ3IDEzLjU2ODNMMTMuNjg5MSAxMy41NDExQzEzLjcyOTIgMTMuNDQ0IDEzLjc0OTggMTMuMzM5OCAxMy43NDk3IDEzLjIzNDdDMTMuNzQ5NiAxMy4xMjk2IDEzLjcyODggMTMuMDI1NSAxMy42ODg1IDEyLjkyODRDMTMuNjQ4MiAxMi44MzEzIDEzLjU4OTIgMTIuNzQzMSAxMy41MTQ4IDEyLjY2ODhDMTMuNDQwNSAxMi41OTQ2IDEzLjM1MjMgMTIuNTM1NyAxMy4yNTUyIDEyLjQ5NTVDMTMuMTU4MSAxMi40NTU0IDEzLjA1NDEgMTIuNDM0OCAxMi45NDkxIDEyLjQzNDlDMTIuODQ0MSAxMi40MzUgMTIuNzQwMSAxMi40NTU5IDEyLjY0MzEgMTIuNDk2MkMxMi41NDYxIDEyLjUzNjUgMTIuNDU4MSAxMi41OTU2IDEyLjM4MzkgMTIuNjdDMTIuMzA5NyAxMi43NDQ0IDEyLjI1MDkgMTIuODMyOCAxMi4yMTA4IDEyLjkyOTlDMTIuMTcwNiAxMy4wMjYgMTIuMTQ5OSAxMy4xMjkgMTIuMTQ5OSAxMy4yMzMxQzEyLjE0OTkgMTMuMzM3MyAxMi4xNzA2IDEzLjQ0MDMgMTIuMjEwOCAxMy41MzYzWk0xNC42MDk3IDE0Ljk3MTVDMTQuMzYzNyAxNS4yMDY2IDE0LjA3MDYgMTUuMzg2NiAxMy43NDk4IDE1LjQ5OTVWMjAuMTk4N0wxNi41Nzg2IDE1Ljk1NzFMMTQuNjA5NyAxNC45NzE1Wk0xNS4zNDggMTMuMjQwM0MxNS4zNDQ4IDEzLjMzOTUgMTUuMzM1MyAxMy40Mzg3IDE1LjMxOTMgMTMuNTM3OUwxNy40NzM2IDE0LjYwODNMMTguMzg0NiAxMy4yNDAzTDE3LjQ3MiAxMS44NzIzTDE1LjMxOTMgMTIuOTQ5MUMxNS4zMzQ2IDEzLjA0NTYgMTUuMzQ0MiAxMy4xNDI4IDE1LjM0OCAxMy4yNDAzWk0xMy43NDk4IDEwLjk5MzlDMTQuMDcwNiAxMS4xMDY5IDE0LjM2MzcgMTEuMjg2OSAxNC42MDk3IDExLjUyMTlMMTYuNTc4NiAxMC41Mjk5TDEzLjc0OTggNi4yODE5NFYxMC45OTM5Wk0xMi4xNTE3IDEwLjk4NzVWNi4yODE5NEw5LjMyMjg1IDEwLjUyOTlMMTEuMjkxOCAxMS41MTU1QzExLjUzNzggMTEuMjgwNSAxMS44MzA5IDExLjEwMDUgMTIuMTUxNyAxMC45OTM5Wk0xMC41NTM1IDEzLjI0MDNDMTAuNTU2NyAxMy4xNDI3IDEwLjU2NjIgMTMuMDQ1MSAxMC41ODIyIDEyLjk0OTFMOC40Mjc4NyAxMS44NzIzTDcuNTE2OSAxMy4yNDAzTDguNDI5NDYgMTQuNjA4M0wxMC41ODIyIDEzLjUzMTVDMTAuNTY2MiAxMy40MzU1IDEwLjU1NjcgMTMuMzM3OSAxMC41NTM1IDEzLjI0MDNaTTEyLjE1MTcgMTUuNDkzMUMxMS44MzA5IDE1LjM4MDIgMTEuNTM3OCAxNS4yMDAyIDExLjI5MTggMTQuOTY1MUw5LjMyMjg1IDE1Ljk1MDdMMTIuMTUxNyAyMC4xOTg3VjE1LjQ5MzFaTTIwLjE3MTQgMTcuNzQ5MUwxOC4wMTg2IDE2LjY3MjNMMTUuMjg0MSAyMC43Nzc5TDIwLjE3MTQgMTguMzMxNUMyMC4xNTU0IDE4LjIzNTUgMjAuMTQ1OCAxOC4xMzc5IDIwLjE0MjYgMTguMDQwM0MyMC4xNDU4IDE3Ljk0MjcgMjAuMTU1NCAxNy44NDUxIDIwLjE3MTQgMTcuNzQ5MVpNMTguOTEyIDE1LjMyOTlMMjAuMjA0OSAxNS45Nzc5TDE5LjM0MzUgMTQuNjgwM0wxOC45MTIgMTUuMzI5OVpNMjAuMjA0OSAxMC41MDI3TDE4LjkxMiAxMS4xNTA3TDE5LjM0MzUgMTEuODAwM0wyMC4yMDQ5IDEwLjUwMjdaTTYuOTg5NDkgMTEuMTQ0M0w1LjY5NjU2IDEwLjUwNDNMNi41NTc5OCAxMS44MDAzTDYuOTg5NDkgMTEuMTQ0M1pNNS42OTY1NiAxNS45Nzc5TDYuOTg5NDkgMTUuMzI5OUw2LjU1Nzk4IDE0LjY4MDNMNS42OTY1NiAxNS45Nzc5WiIgLz4KICAgICAgICAgICAgPC9zdmc+)

## AI-Generated Summary

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibnYtYWktc3VtbWFyeV9fdG9nZ2xlLWljb24iIHdpZHRoPSIxNCIgaGVpZ2h0PSI5IiB2aWV3Ym94PSIwIDAgMTQgOSIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiBhcmlhLWhpZGRlbj0idHJ1ZSI+CiAgICAgICAgPHBhdGggZD0iTTEyLjU3NDIgMkw3LjQ0OTIzIDdMMi4zMjQyNSAyIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0ic3F1YXJlIiAvPgogICAgPC9zdmc+)

- [NVIDIA Blackwell](https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/) introduces NVFP4, a 4-bit floating point format that uses high-precision E4M3 FP8 scaling factors and a two-level micro-block strategy to preserve model accuracy at ultra-low precision.
- NVFP4 reduces quantization error by applying a fine-grained FP8 scale to each 16-value micro-block and a second-level FP32 scalar per tensor, achieving 1% or less accuracy degradation versus FP8 on DeepSeek-R1-0528 benchmarks.
- The format cuts model memory footprint by approximately 3.5x relative to FP16 and 1.8x compared to FP8, enabling larger models to fit within the 40 TB memory budget of an [NVIDIA GB300 NVL72](https://www.nvidia.com/en-us/data-center/gb300-nvl72/) rack-scale system.
- Blackwell and Blackwell Ultra GPUs deliver up to 25x and 50x energy efficiency gains per token respectively over an [NVIDIA H100 Tensor Core](https://www.nvidia.com/en-us/data-center/h100/) baseline when running NVFP4 workloads.

### Next Steps

- Quantize models to NVFP4 using [TensorRT Model Optimizer](https://github.com/NVIDIA/TensorRT-Model-Optimizer/tree/main) for streamlined post-training and quantization-aware training workflows.
- Deploy NVFP4 models on [NVIDIA TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) or [vLLM](https://github.com/vllm-project/vllm) for inference serving.
- Download prequantized NVFP4 checkpoints such as [DeepSeek-R1-0528-FP4](https://huggingface.co/nvidia/DeepSeek-R1-0528-FP4) from Hugging Face for immediate deployment.

Powered by NVIDIA Nemotron. AI-generated content may summarize information incompletely. Verify important information. [Learn more](https://www.nvidia.com/en-us/agreements/trustworthy-ai/terms/)

To get the most out of AI, optimizations are critical. When developers think about optimizing AI models for inference, model compression techniques—such as quantization, distillation, and pruning—typically come to mind. The most common of the three, without a doubt, is quantization. This is typically due to its post-optimization task-specific accuracy performance and broad choice of supported frameworks and techniques. 

Yet the main challenge with model quantization is the potential loss of model intelligence or task-specific accuracy, particularly when transitioning from higher precision data types like FP32 down to the latest FP4 format. [NVIDIA Blackwell](https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/) provides maximum flexibility with support for FP64, FP32/TF32, FP16/BF16, INT8/FP8, FP6, and FP4 data formats. Figure 1 compares the smallest supported floating-point data type and corresponding dense/sparse performance across NVIDIA Ampere, Hopper, and Blackwell GPUs, showcasing the evolution of performance and data type support across GPU generations.

![Bar chart titled "Evolution of Performance Across GPU Generations" that compares the smallest floating-point data type supported performance (dense/sparse measured in petaflops) across three different NVIDIA GPU generations: A100 (0.3/0.6 petaflops), H100 (1.9/3.9 petaflops), B200 (9/18 petaflops), B300 (13/18 petaflops), GB200 (10/20 petaflops), and GB300 (15/20 petaflops). ](https://developer-blogs.nvidia.com/wp-content/uploads/2025/06/performance-evolution-nvidia-gpu-generations-png.webp)

![Bar chart titled "Evolution of Performance Across GPU Generations" that compares the smallest floating-point data type supported performance (dense/sparse measured in petaflops) across three different NVIDIA GPU generations: A100 (0.3/0.6 petaflops), H100 (1.9/3.9 petaflops), B200 (9/18 petaflops), B300 (13/18 petaflops), GB200 (10/20 petaflops), and GB300 (15/20 petaflops). ](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20803%20471%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

*Figure 1. Peak low-precision performance across NVIDIA GPU architectures*

The latest fifth-generation NVIDIA Blackwell Tensor Cores pave the way for various ultra-low precision formats, enabling both research and real-world scenarios. Table 1 compares the three primary 4-bit floating point formats supported in NVIDIA Blackwell—FP4, MXFP4, and NVFP4—highlighting key differences in structure, memory usage, and accuracy. It illustrates how NVFP4 builds on the simplicity of earlier formats while maintaining model accuracy.

[TABLE]

*Table 1. Comparison of Blackwell-supported 4-bit floating point formats*

This post introduces NVFP4, a state-of-the-art data type, and explains how it was purpose-built to help developers scale more efficiently on Blackwell, with the best accuracy at ultra-low precision.

## What is NVFP4?[](#what_is_nvfp4)

NVFP4 is an innovative 4-bit floating point format introduced with the NVIDIA Blackwell GPU architecture. NVFP4 builds on the concept of low-bit “micro” floating-point formats and grants greater flexibility to developers by providing an additional format to choose from.

The structure of NVFP4 is similar to most floating-point 4-bit formats (E2M1), meaning that it has 1 sign bit, 2 exponent bits, and 1 mantissa bit. The value in the format ranges approximately -6 to 6. For example, the values in the range could include 0.0, 0.5, 1.0, 1.5, 2, 3, 4, 6 (same for the negative range). 

One of the key challenges in ultra-low precision formats is maintaining numerical accuracy across a wide dynamic range of tensor values. NVFP4 addresses this concern with two architectural innovations that make it highly effective for AI inference:

- High-precision scale encoding
- A two-level micro-block scaling strategy 

This strategy applies a fine-grained E4M3 scaling factor to each 16-value *micro-block*, a compact subset of the larger tensor, while also leveraging a second-level FP32 scalar applied per tensor. Together, these two levels of scaling enable more accurate value representation and significantly reduce quantization error (Figure 2).

![A diagram showing NVFP4’s internal 4-bit structure (E2M1: sign, exponent, mantissa) and how groups of 16 values each share an FP8 (E4M3) scale factor, demonstrating per-block scaling. These blocks are then globally normalized using a higher precision FP32 (E8M23) scale factor, illustrating NVFP4’s dual-scaling mechanism for maintaining numerical accuracy in low-precision inference. ](https://developer-blogs.nvidia.com/wp-content/uploads/2025/06/nvfp4-two-level-scaling.gif)

![A diagram showing NVFP4’s internal 4-bit structure (E2M1: sign, exponent, mantissa) and how groups of 16 values each share an FP8 (E4M3) scale factor, demonstrating per-block scaling. These blocks are then globally normalized using a higher precision FP32 (E8M23) scale factor, illustrating NVFP4’s dual-scaling mechanism for maintaining numerical accuracy in low-precision inference. ](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20853%20480%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 2. NVFP4 two-level scaling per-block and per-tensor precision structure

## High-precision scaling: Encoding more signal, less error[](#high-precision_scaling_encoding_more_signal_less_error)

To get value out of the shared micro-block scaling, NVFP4 encodes blocks using E4M3 FP8 precision. NVFP4 uses the E4M3 FP8 format variant that enables non-power-of-two scaling factors with fractional precision. This added flexibility enables more accurate encoding of the tensor’s actual distribution. Figure 3 shows an example of a full precision input matrix and the resulting quantized matrices using E8M0 and E4M3 scaling.

![The diagram compares full-precision input values with their quantized counterparts using two formats: E8M0 (used in MXFP4) and E4M3 (used in NVFP4). The top row shows coarse quantized values snapped to power-of-two scales (E8M0), while the bottom row shows NVFP4 using finer-grained E4M3 fractional scaling. NVFP4 better matches original values, reducing error by selecting a more accurate shared scale factor for each block. This illustrates how NVFP4 retains more numerical fidelity in low-bit inference.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/06/quantization-precision-power-of-two-fractional-scaling-comparison-png.webp)

![The diagram compares full-precision input values with their quantized counterparts using two formats: E8M0 (used in MXFP4) and E4M3 (used in NVFP4). The top row shows coarse quantized values snapped to power-of-two scales (E8M0), while the bottom row shows NVFP4 using finer-grained E4M3 fractional scaling. NVFP4 better matches original values, reducing error by selecting a more accurate shared scale factor for each block. This illustrates how NVFP4 retains more numerical fidelity in low-bit inference.](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20735%20317%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 3. *Comparison of quantization precision highlighting power-of-two versus fractional scaling (second-level FP32 scaling omitted for simplicity)*

NVFP4’s more precise scaling factor with E4M3 results in a reduced range of scale values. This is counteracted by utilizing a second-level scaling factor. This second-level scaling factor is done at a per-tensor level with FP32 (illustrated in Figure 2), which adjusts the original tensor’s distribution such that the micro-blocks can be effectively encoded using E4M3 scale factors.

![A visual number line comparing how original floating-point scaling factors (yellow dots) are quantized using E8M0 (top) and E4M3 (bottom) formats. E8M0 restricts scales to power-of-two steps, causing coarser quantization and a higher mean squared error (MSE) of 0.72. E4M3 supports fractional scaling, allowing closer approximation of the original values and a lower MSE of 0.08. This figure illustrates the benefit of using finer-grained E4M3 scaling for encoding quantization scales, not tensor elements. ](https://developer-blogs.nvidia.com/wp-content/uploads/2025/06/e8m0-e4m3-quantization-error-comparion.gif)

![A visual number line comparing how original floating-point scaling factors (yellow dots) are quantized using E8M0 (top) and E4M3 (bottom) formats. E8M0 restricts scales to power-of-two steps, causing coarser quantization and a higher mean squared error (MSE) of 0.72. E4M3 supports fractional scaling, allowing closer approximation of the original values and a lower MSE of 0.08. This figure illustrates the benefit of using finer-grained E4M3 scaling for encoding quantization scales, not tensor elements. ](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20853%20303%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 4. Comparison of quantization error when encoding scaling factors with E8M0 versus E4M3 (second-level FP32 scaling omitted for simplicity)

The animation in Figure 4 is a numberline representation of the matrix conversion in Figure 3. This example maps the original full precision values (represented by yellow circles) to their corresponding position along the dynamic range of the quantized datatype. The figure of merit is the average mean squared error (MSE) of the mappings from the original values to their representations in the quantized datatypes E8M0 and E4M3. Lower MSE is better with 0.08 average for E4M3. 

What makes E4M3 “better on average” is that it picks that one fractional scale so that, when the squared (or absolute) errors over all 16 values are summed, the total error is generally smaller than an E8M0‐quantized block. In other words: 

- **E8M0** = Snaps the scale factor to nearest 2ⁿ, which can create a large quantization error for the block maximum (amax) and can often lead to larger overall quantization errors for blocks.
- **E4M3** = Finds one scale factor that makes the block errors collectively as small as possible—often improving accuracy for the block maximum (amax)—though some values might be slightly less accurate, the block as a whole retains higher fidelity.

You might ask yourself, why would we ever want to use E8M0? The answer is, when simplicity is the highest priority. E8M0 scale factors have slightly reduced computational complexity (that is, they don’t require an extra per-tensor software scaling factor) and can be adequate for activations and weights that are less sensitive to the precision of scale factors. E4M3 adjusts its scaling factor to each small block of values, allowing for finer fit across wider ranges of inputs. That additional flexibility is what translates to a lower overall rounding error

NVIDIA Blackwell fifth-generation Tensor Core architecture implements NVFP4 and can automatically handle the microscaled FP4 data including the grouping of elements, dynamic scaling, and 4-bit matrix operations.

## Micro-block scaling for efficient model compression[](#micro-block_scaling_for_efficient_model_compression)

Another key component of NVFP4 is the block floating-point representation, where micro-blocks share a common scaling factor. By reducing the group size from 32 elements to 16 values per block, NVFP4 enables finer-grained scaling than MXFP4. 

Large tensors in AI models often mix large and small numbers, and a single “umbrella” scaling can lead to significant quantization errors that degrade model performance. The tighter grouping in NVFP4 offers twice as many opportunities to match the local dynamic range of the data, significantly reducing those errors.

To better understand how NVFP4 improves quantization accuracy, it helps to compare it directly to MXFP4, its predecessor. Both formats rely on grouped value blocks and shared scale factors, but a key innovation in NVFP4 lies in its smaller block size and robust scaling. By cutting the block size in half—from 32 values to 16—NVFP4 enables more localized adaptation to the data’s dynamic range. This makes it easier to preserve small-but-important differences in model weights or activations. Figure 5 illustrates how this works in practice.

![A visual comparison between MXFP4 and NVFP4 block structures. The top shows MXFP4 using a 32-value block with one shared coarse power-of-two scale. The bottom illustrates NVFP4 using smaller 16-value blocks, each with its own dynamically computed FP8 scaling factor. A magnified micro-block demonstrates the equation x = xq × s, where 4-bit encoded values (xq) are scaled by a local s factor. This structure improves quantization accuracy by better matching local data ranges within tensors.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/06/comparison-nvfp4-mxfp4-block-structure-1.gif)

![A visual comparison between MXFP4 and NVFP4 block structures. The top shows MXFP4 using a 32-value block with one shared coarse power-of-two scale. The bottom illustrates NVFP4 using smaller 16-value blocks, each with its own dynamically computed FP8 scaling factor. A magnified micro-block demonstrates the equation x = xq × s, where 4-bit encoded values (xq) are scaled by a local s factor. This structure improves quantization accuracy by better matching local data ranges within tensors.](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20833%20358%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 5. NVFP4 enables finer-grained quantization compared to MXFP4 with micro-block scaling

How does it work? Inside each 16-value quantized block, every 4-bit encoded value \\x_q\\ (between the range of -6 to +6) is reconstructed using:

\\x = x_q \times s\\

In this equation, \\s\\ is a higher precision FP8 (E4M3) scaling factor. By recomputing \\s\\ for each group of 16 elements, NVFP4 minimizes quantization error at 4-bit precision, while still significantly reducing memory and compute complexity compared to higher-precision formats. This structure makes NVFP4 excel at preserving model intelligence.

## NVFP4 versus FP8: Model performance and memory efficiency[](#nvfp4_versus_fp8_model_performance_and_memory_efficiency)

Quantization benefits are driven by two factors: reduced memory burden and simplified compute operations. These two factors reduce pressure on memory bandwidth which can improve output token throughput. It can also improve overall end-to-end latency performance as a result of simplified attention layer computations which yield direct benefits during prefill. For a deep dive into these metrics and how they contribute to the overall inference performance story, see [LLM Inference Benchmarking: Fundamental Concepts](https://developer.nvidia.com/blog/llm-benchmarking-fundamental-concepts/).

### Model performance[](#model_performance)

Inference performance optimizations must strive to preserve model intelligence, a balance that NVFP4 is designed to deliver. Figure 6 illustrates this point by comparing the accuracy of DeepSeek-R1-0528 across seven different evaluations, highlighting the minimal accuracy difference between the FP8 and NVFP4 quantized versions of the model.

![Bar chart comparing DeepSeek-R1 0528 model accuracy in FP8 versus NVFP4 across seven benchmarks: MMLU-PRO (85% vs 84%), GPQA Diamond (81% vs 80%), HLE (15% vs 14%), LIVECODEBENCH (77% versus 76%), SCICODE (40% versus 40%), Math-500 (98% versus 98%), and AIME 2024 (89% versus 91%). The chart highlights near-identical accuracy between the two formats, validating NVFP4’s ability to preserve model quality during 4-bit quantization. ](https://developer-blogs.nvidia.com/wp-content/uploads/2025/06/nvfp4-model-accuracy-comparison-png.webp)

![Bar chart comparing DeepSeek-R1 0528 model accuracy in FP8 versus NVFP4 across seven benchmarks: MMLU-PRO (85% vs 84%), GPQA Diamond (81% vs 80%), HLE (15% vs 14%), LIVECODEBENCH (77% versus 76%), SCICODE (40% versus 40%), Math-500 (98% versus 98%), and AIME 2024 (89% versus 91%). The chart highlights near-identical accuracy between the two formats, validating NVFP4’s ability to preserve model quality during 4-bit quantization. ](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201086%20537%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

Figure 6. NVFP4 enables minimal accuracy loss from FP8 to FP4 quantization 

The analysis showcases the 1% or less accuracy degradation on key language modeling tasks for DeepSeek-R1-0528, when quantized from its original FP8 format to NVFP4 using [post-training quantization (PTQ)](https://developer.nvidia.com/blog/optimizing-llms-for-performance-and-accuracy-with-post-training-quantization/). In the case of AIME 2024, NVFP4 is even 2% better in accuracy.

### Memory[](#memory)

FP8 is supported by Hopper and Blackwell, and has enabled significant benefits in memory and latency/throughput over the previously smallest supported 16-bit floating-point datatypes, FP16/BF16. Now, NVFP4 offers an accurate and compact data type for AI workloads on Blackwell. NVFP4 stores one 4-bit value plus minor overhead of one FP8 scale per 16 values (4.5 bits per value) and one FP32 per tensor second-level scaling factor. This reduces the model memory footprint by approximately 3.5x relative to FP16, and approximately 1.8x compared to FP8. 

When this analysis is extended to an [NVIDIA GB300 NVL72](https://www.nvidia.com/en-us/data-center/gb300-nvl72/) rack-scale system, which contains 36 Grace Blackwell Ultra Superchips, each with one NVIDIA Grace CPU and two NVIDIA Blackwell Ultra GPUs, the total memory budget increases to 40 TB per system. This HBM and Grace memory budget partnered with the memory size and accuracy advantages of NVFP4 provide significant benefits for large scale AI inference deployments, particularly in overcoming the challenges posed by [test-time scaling](https://blogs.nvidia.com/blog/ai-scaling-laws/). 

## FP4 energy efficiency [](#fp4_energy_efficiency%C2%A0)

Reducing precision not only speeds up inference and reduces memory footprints, but also improves performance per watt. Each 4-bit operation requires less energy for data movement and arithmetic than a higher-precision data type. Innovations such as liquid cooling and FP4 support in the Blackwell Tensor Core architecture enable Blackwell and Blackwell Ultra to deliver substantial energy efficiency gains, up to 25x and 50x, respectively, compared to an [NVIDIA H100 Tensor Core](https://www.nvidia.com/en-us/data-center/h100/) baseline as shown in Figure 7.

![Line graph titled “50x More Energy Efficient per Token versus Hopper” showing energy required per token (Joules per Token) for GPT-MoE-1.8T from 2014 to 2025 across NVIDIA GPU generations: Kepler (42,000 J/Token), Pascal (17,460), Volta (1,200), Ampere (150), Hopper (10), Blackwell (0.4), and Blackwell Ultra (0.2). The graph demonstrates exponential energy efficiency improvements, with FP4 and architectural advances driving a 200,000x efficiency gain over 10 years. ](https://developer-blogs.nvidia.com/wp-content/uploads/2025/06/50x-more-energy-efficient-per-token-graph-png.webp)

![Line graph titled “50x More Energy Efficient per Token versus Hopper” showing energy required per token (Joules per Token) for GPT-MoE-1.8T from 2014 to 2025 across NVIDIA GPU generations: Kepler (42,000 J/Token), Pascal (17,460), Volta (1,200), Ampere (150), Hopper (10), Blackwell (0.4), and Blackwell Ultra (0.2). The graph demonstrates exponential energy efficiency improvements, with FP4 and architectural advances driving a 200,000x efficiency gain over 10 years. ](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20787%20456%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

*Figure 7. NVFP4 enables up to 50x energy efficiency per token for Blackwell Ultra versus Hopper for GPT-MoE 1.8T*

## Get started with NVFP4[](#get_started_with_nvfp4)

The inference ecosystem is rapidly embracing NVFP4 precision to meet the escalating demands of AI. If you’re looking to quantize your model to NVFP4, NVIDIA [TensorRT Model Optimizer](https://github.com/NVIDIA/TensorRT-Model-Optimizer/tree/main) and [LLM Compressor](https://github.com/vllm-project/llm-compressor) both offer streamlined workflows to do so. It is easier than ever to apply PTQ, QAT, and other advanced quantization techniques to quantize your model to NVFP4.

Once quantized, the NVFP4 model can be easily exported to a Unified Hugging Face Checkpoint and deployed on [NVIDIA TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) and [vLLM](https://github.com/vllm-project/vllm), which offers early NVFP4 support, with upcoming support in [SGLang](https://github.com/sgl-project/sglang). These frameworks are part of a rapidly expanding ecosystem embracing NVFP4 precision. TensorRT Model Optimizer also supports quantization of non-LLM models and exporting to ONNX format. You don’t have to start from scratch, either: Hugging Face already hosts NVFP4 prequantized checkpoints ready for deployment, including some of the most popular: [DeepSeek-R1-0528](https://huggingface.co/nvidia/DeepSeek-R1-0528-FP4), [Llama 3](https://huggingface.co/nvidia/Llama-3.1-405B-Instruct-FP4), and [FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev-onnx).

Whether you’re optimizing from scratch or adopting prequantized models, NVFP4 is gaining momentum across real-world deployments—with more tutorials and code samples coming soon. Stay tuned.

Learn how NVIDIA Blackwell NVL72 runs 10x faster and delivers 1/10 the token cost for MoE models in this [blog](https://blogs.nvidia.com/blog/mixture-of-experts-frontier-models/).

[ Discuss (3)](#entry-content-comments)

Like

## Tags

[Agentic AI / Generative AI](https://developer.nvidia.com/blog/category/generative-ai/) \| [Data Center / Cloud](https://developer.nvidia.com/blog/category/data-center-cloud/) \| [Cloud Services](https://developer.nvidia.com/blog/recent-posts/?industry=Cloud+Services) \| [Blackwell](https://developer.nvidia.com/blog/recent-posts/?products=Blackwell) \| [TensorRT](https://developer.nvidia.com/blog/recent-posts/?products=TensorRT) \| [TensorRT-LLM](https://developer.nvidia.com/blog/recent-posts/?products=TensorRT-LLM) \| [Intermediate Technical](https://developer.nvidia.com/blog/recent-posts/?learning_levels=Intermediate+Technical) \| [Deep dive](https://developer.nvidia.com/blog/recent-posts/?content_types=Deep+dive) \| [News](https://developer.nvidia.com/blog/recent-posts/?content_types=News) \| [AI Inference](https://developer.nvidia.com/blog/tag/ai-inference-microservices/) \| [featured](https://developer.nvidia.com/blog/tag/featured/) \| [Inference Performance](https://developer.nvidia.com/blog/tag/inference-performance/) \| [LLMs](https://developer.nvidia.com/blog/tag/large-language-models/) \| [Sustainable Computing](https://developer.nvidia.com/blog/tag/sustainable-computing/)

## About the Authors

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2026/05/cropped-EAA_Headshot-131x131.webp)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Eduardo Alvarez**  
Eduardo Alvarez is a senior technical lead at NVIDIA, where he focuses on AI inference at scale, performance optimization, workload economic analysis, and application enablement. He has a deep background in AI systems engineering, workload optimization, and accelerated computing—focused on translating innovations into real-world applications. Before NVIDIA, Eduardo held engineering roles at various semiconductor and energy tech companies.

[View all posts by Eduardo Alvarez![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/edualvarez/)

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2025/03/cropped-omri-almog-131x131.jpg)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Omri Almog**  
Omri Almog is a senior product manager in the AI Platform Software group at NVIDIA, responsible for managing products that optimize models for inference. Omri earned his bachelor’s degree from Oregon State University and his master’s degree from the University of California, Santa Barbara.

[View all posts by Omri Almog![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/oalmog/)

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2025/06/cropped-eric-chung-131x131.png)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Eric Chung**  
Eric Chung is vice president of AI Computing at NVIDIA, where he leads efforts to scale AI through breakthroughs in model efficiency, low-precision numerics, software resiliency, and agent technologies. Most recently, his teams created and deployed Puzzle, a distillation-driven neural architecture search framework used to optimize inference in NVIDIA state-of-the-art Nemotron reasoning models. Previously, Eric led AI supercomputing and hardware-software co-design efforts at Microsoft, where his team co-founded the OCP MX Alliance and introduced the MXFP formats now deployed ubiquitously across AI hardware, including NVIDIA Blackwell. He holds a PhD in Electrical and Computer Engineering from Carnegie Mellon University.

[View all posts by Eric Chung![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/erchung/)

![Avatar photo](https://developer.nvidia.com/blog/wp-content/uploads/2018/12/Simon-Layton_avatar_1543876369.jpg)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Simon Layton**  
Simon Layton is a Senior Developer Technology Engineer on the Deep Learning Frameworks team at Nvidia.

[View all posts by Simon Layton![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/slayton/)

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2021/01/dusan-stosic-131x131.png)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Dusan Stosic**  
Dusan Stosic is a senior architect in Compute Architecture at NVIDIA. His focus is on accelerating deep neural network training and inference with precision arithmetic and other unconventional techniques. He holds a PhD in computer science from the Federal University of Pernambuco, Brazil and in physics from the University of Antwerp, Belgium.

[View all posts by Dusan Stosic![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/dstosic/)

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2020/05/ronny-131x131.jpg)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Ronny Krashinsky**  
Ronny Krashinsky is an NVIDIA distinguished engineer who has architected GPUs for 12 years. He began his NVIDIA career in research, and later joined the Streaming Multiprocessor team to architect the Volta SM. Ronny now leads a team exploring and developing deep-learning features across NVIDIA Ampere, Hopper, and future GPU architectures.

[View all posts by Ronny Krashinsky![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/rkrashinsky/)

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2025/04/cropped-kyle-aubrey-131x131.png)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Kyle Aubrey**  
Kyle Aubrey is the director of Technical Marketing at NVIDIA, where he leads initiatives in AI inference and training across NVIDIA accelerated computing platforms, including Hopper, Blackwell, Rubin, and beyond. With a passion for demystifying complex technologies, he empowers diverse audiences to harness the full potential of NVIDIA's cutting-edge solutions. Kyle holds a bachelor’s degree in Electrical Engineering from Rose-Hulman Institute of Technology and an MBA from Pepperdine University.

[View all posts by Kyle Aubrey![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/kaubrey/)

## Comments
