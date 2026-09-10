<!-- 从 ultra-architecture.html 迁移的资料快照；原始 HTML SHA-256: 227bffbd0832549ab72790574f1bf34d5262b87ac617802cbe5b2d83aba5a550。 -->

[Data Center / Cloud](https://developer.nvidia.com/blog/category/data-center-cloud/)

English中文

# Inside NVIDIA Blackwell Ultra: The Chip Powering the AI Factory Era

![Blackwell Ultra illustration.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/08/Blackwell-Ultra-1024x576-png.webp)

Aug 22, 2025

By [Kyle Aubrey](https://developer.nvidia.com/blog/author/kaubrey/ "Posts by Kyle Aubrey") and [Nick Stam](https://developer.nvidia.com/blog/author/nstam/ "Posts by Nick Stam")

Like

[ Discuss (1)](#entry-content-comments)

- [L](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Finside-nvidia-blackwell-ultra-the-chip-powering-the-ai-factory-era%2F)
- [T](https://twitter.com/intent/tweet?text=Inside+NVIDIA+Blackwell+Ultra%3A+The+Chip+Powering+the+AI+Factory+Era+%7C+NVIDIA+Technical+Blog+https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Finside-nvidia-blackwell-ultra-the-chip-powering-the-ai-factory-era%2F)
- [F](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Finside-nvidia-blackwell-ultra-the-chip-powering-the-ai-factory-era%2F)
- [R](https://www.reddit.com/submit?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Finside-nvidia-blackwell-ultra-the-chip-powering-the-ai-factory-era%2F&title=Inside+NVIDIA+Blackwell+Ultra%3A+The+Chip+Powering+the+AI+Factory+Era+%7C+NVIDIA+Technical+Blog)
- [E](mailto:?subject=I'd%20like%20to%20share%20a%20link%20with%20you&body=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Finside-nvidia-blackwell-ultra-the-chip-powering-the-ai-factory-era%2F)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibnYtYWktc3VtbWFyeV9faWNvbiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iMjUiIGhlaWdodD0iMjUiIHZpZXdib3g9IjAgMCAyNSAyNSIgZmlsbD0ibm9uZSIgYXJpYS1oaWRkZW49InRydWUiPgogICAgICAgICAgICAgICAgPHBhdGggZmlsbD0iY3VycmVudENvbG9yIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTIyLjQ5MTUgMTUuMzAxOUMyMi4yOTQgMTUuMzA0NyAyMi4wOTc2IDE1LjMzMTYgMjEuOTA2NiAxNS4zODE5TDIwLjI1NCAxMi45MDE5TDIxLjkwNSAxMC40MjE5QzIyLjA5NjcgMTAuNDczMSAyMi4yOTMzIDEwLjQ5ODcgMjIuNDkxNSAxMC41MDE5QzIyLjg4NDQgMTAuNTAzMiAyMy4yNzE2IDEwLjQwNzggMjMuNjE5IDEwLjIyNDFDMjMuOTY2NSAxMC4wNDA0IDI0LjI2MzUgOS43NzQwNSAyNC40ODM5IDkuNDQ4NDVDMjQuNzA0NCA5LjEyMjg1IDI0Ljg0MTUgOC43NDc5OSAyNC44ODMyIDguMzU2ODdDMjQuOTI1IDcuOTY1NzUgMjQuODcwMSA3LjU3MDM1IDI0LjcyMzMgNy4yMDU0N0MyNC41NzY2IDYuODQwNTkgMjQuMzQyNSA2LjUxNzQxIDI0LjA0MTcgNi4yNjQzN0MyMy43NDA5IDYuMDExMzQgMjMuMzgyNSA1LjgzNjIgMjIuOTk4MiA1Ljc1NDM3QzIyLjYxMzkgNS42NzI1NSAyMi4yMTU0IDUuNjg2NTQgMjEuODM3OCA1Ljc5NTEyQzIxLjQ2MDEgNS45MDM3IDIxLjExNDkgNi4xMDM1NCAyMC44MzI2IDYuMzc3MDZMMTUuMjcwOSAzLjU5MzA1QzE1LjI4NjggMy40OTcwNSAxNS4yOTY0IDMuMzk5NDYgMTUuMjk5NiAzLjMwMTg2QzE1LjI5OTYgMi42NjUzNCAxNS4wNDcxIDIuMDU0ODkgMTQuNTk3NSAxLjYwNDhDMTQuMTQ3OSAxLjE1NDcxIDEzLjUzODEgMC45MDE4NTUgMTIuOTAyMyAwLjkwMTg1NUMxMi4yNjY1IDAuOTAxODU1IDExLjY1NjggMS4xNTQ3MSAxMS4yMDcyIDEuNjA0OEMxMC43NTc2IDIuMDU0ODkgMTAuNTA1MSAyLjY2NTM0IDEwLjUwNTEgMy4zMDE4NkMxMC41MDgzIDMuMzk5NDYgMTAuNTE3OCAzLjQ5NzA1IDEwLjUzMzggMy41OTMwNUw0Ljk3MjExIDYuMzc3MDZDNC42ODk3NiA2LjEwMjY3IDQuMzQ0MzMgNS45MDIwMiAzLjk2NjI2IDUuNzkyODFDMy41ODgxOCA1LjY4MzYgMy4xODkwOCA1LjY2OTE4IDIuODA0MTIgNS43NTA4MkMyLjQxOTE2IDUuODMyNDUgMi4wNjAxOCA2LjAwNzY0IDEuNzU4OCA2LjI2MDkzQzEuNDU3NDMgNi41MTQyMyAxLjIyMjkyIDYuODM3ODYgMS4wNzU5NSA3LjIwMzI5QzAuOTI4OTgxIDcuNTY4NzIgMC44NzQwNTggNy45NjQ3NCAwLjkxNjAyOCA4LjM1NjQ0QzAuOTU3OTk4IDguNzQ4MTMgMS4wOTU1NyA5LjEyMzQ4IDEuMzE2NjIgOS40NDkzOUMxLjUzNzY3IDkuNzc1MyAxLjgzNTQgMTAuMDQxOCAyLjE4MzU4IDEwLjIyNTNDMi41MzE3NiAxMC40MDg4IDIuOTE5NyAxMC41MDM4IDMuMzEzMTkgMTAuNTAxOUMzLjUxMTM2IDEwLjQ5ODcgMy43MDc5NCAxMC40NzE1IDMuODk4MTMgMTAuNDIxOUw1LjU1MDY2IDEyLjkwMTlMMy44OTk3MyAxNS4zODE5QzMuNzA4MTggMTUuMzMxNCAzLjUxMTIyIDE1LjMwNDYgMy4zMTMxOSAxNS4zMDE5QzIuOTIwMjkgMTUuMzAwNSAyLjUzMzA4IDE1LjM5NTkgMi4xODU2NSAxNS41Nzk2QzEuODM4MjIgMTUuNzYzMyAxLjU0MTIyIDE2LjAyOTcgMS4zMjA3NyAxNi4zNTUzQzEuMTAwMzIgMTYuNjgwOSAwLjk2MzE4OSAxNy4wNTU3IDAuOTIxNDQyIDE3LjQ0NjhDMC44Nzk2OTUgMTcuODM4IDAuOTM0NjEzIDE4LjIzMzQgMS4wODEzNiAxOC41OTgyQzEuMjI4MTEgMTguOTYzMSAxLjQ2MjE5IDE5LjI4NjMgMS43NjMwMSAxOS41MzkzQzIuMDYzODIgMTkuNzkyNCAyLjQyMjE1IDE5Ljk2NzUgMi44MDY0NiAyMC4wNDkzQzMuMTkwNzcgMjAuMTMxMiAzLjU4OTI4IDIwLjExNzIgMy45NjY5MSAyMC4wMDg2QzQuMzQ0NTUgMTkuOSA0LjY4OTc0IDE5LjcwMDIgNC45NzIxMSAxOS40MjY3TDEwLjUzMzggMjIuMjEwN0MxMC41MTc4IDIyLjMwNjcgMTAuNTA4MyAyMi40MDQzIDEwLjUwNTEgMjIuNTAxOUMxMC41MDUxIDIzLjEzODQgMTAuNzU3NiAyMy43NDg4IDExLjIwNzIgMjQuMTk4OUMxMS42NTY4IDI0LjY0OSAxMi4yNjY1IDI0LjkwMTkgMTIuOTAyMyAyNC45MDE5QzEzLjUzODEgMjQuOTAxOSAxNC4xNDc5IDI0LjY0OSAxNC41OTc1IDI0LjE5ODlDMTUuMDQ3MSAyMy43NDg4IDE1LjI5OTYgMjMuMTM4NCAxNS4yOTk2IDIyLjUwMTlDMTUuMjk1OCAyMi40MDQzIDE1LjI4NjIgMjIuMzA3MSAxNS4yNzA5IDIyLjIxMDdMMjAuODMyNiAxOS40MjY3QzIxLjExNDkgMTkuNzAxIDIxLjQ2MDQgMTkuOTAxNyAyMS44Mzg0IDIwLjAxMDlDMjIuMjE2NSAyMC4xMjAxIDIyLjYxNTYgMjAuMTM0NSAyMy4wMDA2IDIwLjA1MjlDMjMuMzg1NSAxOS45NzEzIDIzLjc0NDUgMTkuNzk2MSAyNC4wNDU5IDE5LjU0MjhDMjQuMzQ3MyAxOS4yODk1IDI0LjU4MTggMTguOTY1OSAyNC43Mjg3IDE4LjYwMDRDMjQuODc1NyAxOC4yMzUgMjQuOTMwNiAxNy44MzkgMjQuODg4NyAxNy40NDczQzI0Ljg0NjcgMTcuMDU1NiAyNC43MDkxIDE2LjY4MDIgMjQuNDg4MSAxNi4zNTQzQzI0LjI2NyAxNi4wMjg0IDIzLjk2OTMgMTUuNzYxOSAyMy42MjExIDE1LjU3ODRDMjMuMjcyOSAxNS4zOTQ5IDIyLjg4NSAxNS4yOTk5IDIyLjQ5MTUgMTUuMzAxOVpNMTIuODg4NCAyLjUwMjc0QzEzLjAxODUgMi41MDMyNCAxMy4xNDY1IDIuNTM1NTIgMTMuMjYxMyAyLjU5Njc5QzEzLjM3NjEgMi42NTgwNSAxMy40NzQyIDIuNzQ2NDQgMTMuNTQ3MSAyLjg1NDI5QzEzLjYyIDIuOTYyMTQgMTMuNjY1NSAzLjA4NjE3IDEzLjY3OTcgMy4yMTU2M0MxMy42OTM5IDMuMzQ1MDkgMTMuNjc2MyAzLjQ3NjA1IDEzLjYyODQgMy41OTcxNEwxMy42MDYgMy42NDE5NEMxMy41NDI5IDMuNzc5ODEgMTMuNDQxNiAzLjg5NjY0IDEzLjMxNDEgMy45Nzg1NUMxMy4xODY2IDQuMDYwNDUgMTMuMDM4MyA0LjEwMzk5IDEyLjg4NjggNC4xMDM5OUMxMi43MzUzIDQuMTAzOTkgMTIuNTg3IDQuMDYwNDUgMTIuNDU5NiAzLjk3ODU1QzEyLjMzMjEgMy44OTY2NCAxMi4yMzA3IDMuNzc5ODEgMTIuMTY3NiAzLjY0MTk0TDEyLjE0NTMgMy41OTg3NEMxMi4wOTcgMy40NzczMSAxMi4wNzkxIDMuMzQ1ODkgMTIuMDkzMyAzLjIxNTk2QzEyLjEwNzQgMy4wODYwMyAxMi4xNTMyIDIuOTYxNTYgMTIuMjI2NSAyLjg1MzQyQzEyLjI5OTggMi43NDUyOCAxMi4zOTg1IDIuNjU2NzggMTIuNTEzOSAyLjU5NTY0QzEyLjYyOTMgMi41MzQ1MSAxMi43NTc5IDIuNTAyNjEgMTIuODg4NCAyLjUwMjc0Wk0yMy4yNzY3IDguMTAyNzRDMjMuMjc2NyA4LjMxNDkxIDIzLjE5MjUgOC41MTg0IDIzLjA0MjYgOC42Njg0M0MyMi44OTI4IDguODE4NDUgMjIuNjg5NSA4LjkwMjc0IDIyLjQ3NzYgOC45MDI3NEMyMi4yNjU2IDguOTAyNzQgMjIuMDYyNCA4LjgxODQ1IDIxLjkxMjUgOC42Njg0M0MyMS43NjI3IDguNTE4NCAyMS42Nzg1IDguMzE0OTEgMjEuNjc4NSA4LjEwMjc0QzIxLjY3ODUgNy44OTA1NyAyMS43NjI3IDcuNjg3MDggMjEuOTEyNSA3LjUzNzA1QzIyLjA2MjQgNy4zODcwMiAyMi4yNjU2IDcuMzAyNzQgMjIuNDc3NiA3LjMwMjc0QzIyLjY4OTUgNy4zMDI3NCAyMi44OTI4IDcuMzg3MDIgMjMuMDQyNiA3LjUzNzA1QzIzLjE5MjUgNy42ODcwOCAyMy4yNzY3IDcuODkwNTcgMjMuMjc2NyA4LjEwMjc0Wk0yLjUwMDE3IDguMTAyNzRDMi41MDMgNy45MjMwNSAyLjU2NjE3IDcuNzQ5NTYgMi42Nzk1MSA3LjYxMDJDMi43OTI4NSA3LjQ3MDg1IDIuOTQ5NzYgNy4zNzM3NiAzLjEyNDk1IDcuMzM0NThDMy4zMDAxNCA3LjI5NTQgMy40ODM0IDcuMzE2NDEgMy42NDUyIDcuMzk0MjNDMy44MDcgNy40NzIwNSAzLjkzNzkyIDcuNjAyMTQgNC4wMTY4NSA3Ljc2MzU0TDQuMDM5MjMgNy44MDgzNEM0LjA5ODcxIDcuOTUzMDYgNC4xMTM3NiA4LjExMjI1IDQuMDgyNDQgOC4yNjU1OEM0LjA1MTEzIDguNDE4OSAzLjk3NDg4IDguNTU5NDEgMy44NjM0MyA4LjY2OTE0QzMuNzUxNTggOC43ODA3NiAzLjYwOTIxIDguODU2NyAzLjQ1NDI4IDguODg3MzdDMy4yOTkzNiA4LjkxODA1IDMuMTM4ODMgOC45MDIwNyAyLjk5Mjk3IDguODQxNDdDMi44NDcxIDguNzgwODYgMi43MjI0NSA4LjY3ODM1IDIuNjM0NzQgOC41NDY4N0MyLjU0NzAzIDguNDE1MzkgMi41MDAyIDguMjYwODQgMi41MDAxNyA4LjEwMjc0Wk0yLjUwMDE3IDE3LjcwMjdDMi41MDAxNyAxNy40OTA2IDIuNTg0MzYgMTcuMjg3MSAyLjczNDIyIDE3LjEzNzFDMi44ODQwOCAxNi45ODcgMy4wODczMyAxNi45MDI3IDMuMjk5MjcgMTYuOTAyN0MzLjUxMTIgMTYuOTAyNyAzLjcxNDQ1IDE2Ljk4NyAzLjg2NDMxIDE3LjEzNzFDNC4wMTQxNyAxNy4yODcxIDQuMDk4MzYgMTcuNDkwNiA0LjA5ODM2IDE3LjcwMjdDNC4wOTgzNiAxNy45MTQ5IDQuMDE0MTcgMTguMTE4NCAzLjg2NDMxIDE4LjI2ODRDMy43MTQ0NSAxOC40MTg1IDMuNTExMiAxOC41MDI3IDMuMjk5MjcgMTguNTAyN0MzLjA4NzMzIDE4LjUwMjcgMi44ODQwOCAxOC40MTg1IDIuNzM0MjIgMTguMjY4NEMyLjU4NDM2IDE4LjExODQgMi41MDAxNyAxNy45MTQ5IDIuNTAwMTcgMTcuNzAyN1pNMTIuODg4NCAyMy4zMDI3QzEyLjc1NjYgMjMuMzAyOCAxMi42MjY4IDIzLjI3MDIgMTIuNTEwNiAyMy4yMDc4QzEyLjM5NDQgMjMuMTQ1NSAxMi4yOTU1IDIzLjA1NTMgMTIuMjIyNSAyMi45NDU0QzEyLjE0OTYgMjIuODM1NSAxMi4xMDQ5IDIyLjcwOTIgMTIuMDkyNiAyMi41Nzc4QzEyLjA4MDIgMjIuNDQ2NCAxMi4xMDA1IDIyLjMxNCAxMi4xNTE3IDIyLjE5MjNDMTIuMjEyOCAyMi4wNTE5IDEyLjMxMjkgMjEuOTMxOSAxMi40NDAxIDIxLjg0NjhDMTIuNTY3MyAyMS43NjE2IDEyLjcxNjMgMjEuNzE0OCAxMi44NjkzIDIxLjcxMkMxMy4wMjIzIDIxLjcwOTEgMTMuMTcyOSAyMS43NTAzIDEzLjMwMzIgMjEuODMwNkMxMy40MzM2IDIxLjkxMSAxMy41MzgxIDIyLjAyNzEgMTMuNjA0NCAyMi4xNjUxTDEzLjYyNjggMjIuMjA5OUMxMy42ODY4IDIyLjM1NDEgMTMuNzAyNCAyMi41MTI5IDEzLjY3MTYgMjIuNjY1OUMxMy42NDA5IDIyLjgxOSAxMy41NjUxIDIyLjk1OTQgMTMuNDU0MiAyMy4wNjkxQzEzLjM3OTggMjMuMTQzNCAxMy4yOTE2IDIzLjIwMjIgMTMuMTk0NSAyMy4yNDIzQzEzLjA5NzQgMjMuMjgyNCAxMi45OTM0IDIzLjMwMjkgMTIuODg4NCAyMy4zMDI3Wk0yMi40Nzc2IDE4LjUwMjdDMjIuMzI2NyAxOC41MDE2IDIyLjE3OTMgMTguNDU3NyAyMi4wNTIzIDE4LjM3NjFDMjEuOTI1MyAxOC4yOTQ2IDIxLjgyNCAxOC4xNzg3IDIxLjc2IDE4LjA0MTlMMjEuNzM3NiAxNy45OTcxQzIxLjY5ODEgMTcuOTAyOSAyMS42Nzc3IDE3LjgwMTcgMjEuNjc3NyAxNy42OTk1QzIxLjY3NzcgMTcuNTk3MyAyMS42OTgxIDE3LjQ5NjIgMjEuNzM3NiAxNy40MDE5TDIxLjc1MiAxNy4zNzQ3QzIxLjgwOTggMTcuMjQyMiAyMS45MDIzIDE3LjEyNzkgMjIuMDE5OSAxNy4wNDM4QzIyLjEzNzQgMTYuOTU5OCAyMi4yNzU1IDE2LjkwOTIgMjIuNDE5NCAxNi44OTc0QzIyLjU2MzMgMTYuODg1NyAyMi43MDc4IDE2LjkxMzIgMjIuODM3MyAxNi45NzcxQzIyLjk2NjkgMTcuMDQwOSAyMy4wNzY4IDE3LjEzODggMjMuMTU1MiAxNy4yNjAxQzIzLjIzMzcgMTcuMzgxNSAyMy4yNzc4IDE3LjUyMTkgMjMuMjgzIDE3LjY2NjRDMjMuMjg4MSAxNy44MTA5IDIzLjI1NCAxNy45NTQxIDIzLjE4NDMgMTguMDgwOEMyMy4xMTQ2IDE4LjIwNzQgMjMuMDEyIDE4LjMxMjggMjIuODg3MiAxOC4zODU3QzIyLjc2MjUgMTguNDU4NiAyMi42MjA0IDE4LjQ5NjMgMjIuNDc2IDE4LjQ5NDdMMjIuNDc3NiAxOC41MDI3Wk0xOC4wMTg2IDkuODA4MzRMMjAuMTcxNCA4LjczMTU0QzIwLjE1NTQgOC42MzU1NCAyMC4xNDU4IDguNTM3OTQgMjAuMTQyNiA4LjQ0MDM0QzIwLjE0NTggOC4zNDI3NCAyMC4xNTU0IDguMjQ1MTQgMjAuMTcxNCA4LjE0OTE0TDE1LjI4NDEgNS43MDI3NEwxOC4wMTg2IDkuODA4MzRaTTEwLjYxNTggNS43MDQzNEw1LjczMDEyIDguMTQ5MTRDNS43NDU0NSA4LjI0NTU1IDUuNzU1MDUgOC4zNDI3OSA1Ljc1ODg4IDguNDQwMzRDNS43NTU2OSA4LjUzNzk0IDUuNzQ2MSA4LjYzNTU0IDUuNzMwMTIgOC43MzE1NEw3Ljg4Mjg4IDkuODA4MzRMMTAuNjE1OCA1LjcwNDM0Wk01LjczMDEyIDE3Ljc0OTFMNy44ODI4OCAxNi42NzIzTDEwLjYxNzQgMjAuNzc3OUw1LjczMDEyIDE4LjMzMTVDNS43NDYxIDE4LjIzNTUgNS43NTU2OSAxOC4xMzc5IDUuNzU4ODggMTguMDQwM0M1Ljc1NTA1IDE3Ljk0MjggNS43NDU0NSAxNy44NDU2IDUuNzMwMTIgMTcuNzQ5MVpNMTIuMjEwOCAxMy41MzYzTDEyLjIzMzIgMTMuNTc5NUgxMi4yMzY0QzEyLjMgMTMuNzE3NSAxMi40MDIxIDEzLjgzNDEgMTIuNTMwMyAxMy45MTU1QzEyLjY1ODUgMTMuOTk2OCAxMi44MDc0IDE0LjAzOTUgMTIuOTU5MiAxNC4wMzgzQzEzLjExMDkgMTQuMDM3MSAxMy4yNTkyIDEzLjk5MjEgMTMuMzg2MSAxMy45MDg4QzEzLjUxMyAxMy44MjU1IDEzLjYxMzIgMTMuNzA3MiAxMy42NzQ3IDEzLjU2ODNMMTMuNjg5MSAxMy41NDExQzEzLjcyOTIgMTMuNDQ0IDEzLjc0OTggMTMuMzM5OCAxMy43NDk3IDEzLjIzNDdDMTMuNzQ5NiAxMy4xMjk2IDEzLjcyODggMTMuMDI1NSAxMy42ODg1IDEyLjkyODRDMTMuNjQ4MiAxMi44MzEzIDEzLjU4OTIgMTIuNzQzMSAxMy41MTQ4IDEyLjY2ODhDMTMuNDQwNSAxMi41OTQ2IDEzLjM1MjMgMTIuNTM1NyAxMy4yNTUyIDEyLjQ5NTVDMTMuMTU4MSAxMi40NTU0IDEzLjA1NDEgMTIuNDM0OCAxMi45NDkxIDEyLjQzNDlDMTIuODQ0MSAxMi40MzUgMTIuNzQwMSAxMi40NTU5IDEyLjY0MzEgMTIuNDk2MkMxMi41NDYxIDEyLjUzNjUgMTIuNDU4MSAxMi41OTU2IDEyLjM4MzkgMTIuNjdDMTIuMzA5NyAxMi43NDQ0IDEyLjI1MDkgMTIuODMyOCAxMi4yMTA4IDEyLjkyOTlDMTIuMTcwNiAxMy4wMjYgMTIuMTQ5OSAxMy4xMjkgMTIuMTQ5OSAxMy4yMzMxQzEyLjE0OTkgMTMuMzM3MyAxMi4xNzA2IDEzLjQ0MDMgMTIuMjEwOCAxMy41MzYzWk0xNC42MDk3IDE0Ljk3MTVDMTQuMzYzNyAxNS4yMDY2IDE0LjA3MDYgMTUuMzg2NiAxMy43NDk4IDE1LjQ5OTVWMjAuMTk4N0wxNi41Nzg2IDE1Ljk1NzFMMTQuNjA5NyAxNC45NzE1Wk0xNS4zNDggMTMuMjQwM0MxNS4zNDQ4IDEzLjMzOTUgMTUuMzM1MyAxMy40Mzg3IDE1LjMxOTMgMTMuNTM3OUwxNy40NzM2IDE0LjYwODNMMTguMzg0NiAxMy4yNDAzTDE3LjQ3MiAxMS44NzIzTDE1LjMxOTMgMTIuOTQ5MUMxNS4zMzQ2IDEzLjA0NTYgMTUuMzQ0MiAxMy4xNDI4IDE1LjM0OCAxMy4yNDAzWk0xMy43NDk4IDEwLjk5MzlDMTQuMDcwNiAxMS4xMDY5IDE0LjM2MzcgMTEuMjg2OSAxNC42MDk3IDExLjUyMTlMMTYuNTc4NiAxMC41Mjk5TDEzLjc0OTggNi4yODE5NFYxMC45OTM5Wk0xMi4xNTE3IDEwLjk4NzVWNi4yODE5NEw5LjMyMjg1IDEwLjUyOTlMMTEuMjkxOCAxMS41MTU1QzExLjUzNzggMTEuMjgwNSAxMS44MzA5IDExLjEwMDUgMTIuMTUxNyAxMC45OTM5Wk0xMC41NTM1IDEzLjI0MDNDMTAuNTU2NyAxMy4xNDI3IDEwLjU2NjIgMTMuMDQ1MSAxMC41ODIyIDEyLjk0OTFMOC40Mjc4NyAxMS44NzIzTDcuNTE2OSAxMy4yNDAzTDguNDI5NDYgMTQuNjA4M0wxMC41ODIyIDEzLjUzMTVDMTAuNTY2MiAxMy40MzU1IDEwLjU1NjcgMTMuMzM3OSAxMC41NTM1IDEzLjI0MDNaTTEyLjE1MTcgMTUuNDkzMUMxMS44MzA5IDE1LjM4MDIgMTEuNTM3OCAxNS4yMDAyIDExLjI5MTggMTQuOTY1MUw5LjMyMjg1IDE1Ljk1MDdMMTIuMTUxNyAyMC4xOTg3VjE1LjQ5MzFaTTIwLjE3MTQgMTcuNzQ5MUwxOC4wMTg2IDE2LjY3MjNMMTUuMjg0MSAyMC43Nzc5TDIwLjE3MTQgMTguMzMxNUMyMC4xNTU0IDE4LjIzNTUgMjAuMTQ1OCAxOC4xMzc5IDIwLjE0MjYgMTguMDQwM0MyMC4xNDU4IDE3Ljk0MjcgMjAuMTU1NCAxNy44NDUxIDIwLjE3MTQgMTcuNzQ5MVpNMTguOTEyIDE1LjMyOTlMMjAuMjA0OSAxNS45Nzc5TDE5LjM0MzUgMTQuNjgwM0wxOC45MTIgMTUuMzI5OVpNMjAuMjA0OSAxMC41MDI3TDE4LjkxMiAxMS4xNTA3TDE5LjM0MzUgMTEuODAwM0wyMC4yMDQ5IDEwLjUwMjdaTTYuOTg5NDkgMTEuMTQ0M0w1LjY5NjU2IDEwLjUwNDNMNi41NTc5OCAxMS44MDAzTDYuOTg5NDkgMTEuMTQ0M1pNNS42OTY1NiAxNS45Nzc5TDYuOTg5NDkgMTUuMzI5OUw2LjU1Nzk4IDE0LjY4MDNMNS42OTY1NiAxNS45Nzc5WiIgLz4KICAgICAgICAgICAgPC9zdmc+)

## AI-Generated Summary

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibnYtYWktc3VtbWFyeV9fdG9nZ2xlLWljb24iIHdpZHRoPSIxNCIgaGVpZ2h0PSI5IiB2aWV3Ym94PSIwIDAgMTQgOSIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiBhcmlhLWhpZGRlbj0idHJ1ZSI+CiAgICAgICAgPHBhdGggZD0iTTEyLjU3NDIgMkw3LjQ0OTIzIDdMMi4zMjQyNSAyIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0ic3F1YXJlIiAvPgogICAgPC9zdmc+)

- [NVIDIA Blackwell Ultra GPU](https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/) delivers 15 petaFLOPS of dense NVFP4 compute through 640 fifth-generation Tensor Cores across 160 Streaming Multiprocessors.
- The dual-reticle design connects two dies with NV-HBI at 10 TB/s, functioning as a single CUDA-programmed accelerator with 208B transistors manufactured on TSMC 4NP.
- HBM3E memory capacity reaches 288 GB with 8 TB/s bandwidth, enabling 300B+ parameter models to reside entirely on-chip without offloading.
- Accelerated softmax execution doubles SFU throughput for attention-layer operations, delivering up to 2x faster attention compute compared to Blackwell GPUs.
- NVLink 5 provides 1.8 TB/s bidirectional GPU-to-GPU bandwidth supporting up to 576 GPUs in non-blocking fabric, while NVLink-C2C enables 900 GB/s coherent CPU-GPU communication.
- Enterprise features include enhanced GigaThread scheduling, Multi-Instance GPU partitioning, confidential computing with TEE-I/O, and AI-powered RAS for predictive failure monitoring.

### Next Steps

- Download the [Blackwell Architecture Technical Brief](https://resources.nvidia.com/en-us-blackwell-architecture/blackwell-architecture-technical-brief) to explore the full silicon-to-system story.
- Explore the [Pareto Frontier explainer](https://resources.nvidia.com/en-us-inference-contact-us/discover-ai-inference) to see how hardware and deployment innovations impact data center efficiency and user experience.
- Learn about [GB300 NVL72](https://www.nvidia.com/en-us/data-center/gb300-nvl72/) rack-scale system capabilities for AI factory deployments.

Powered by NVIDIA Nemotron. AI-generated content may summarize information incompletely. Verify important information. [Learn more](https://www.nvidia.com/en-us/agreements/trustworthy-ai/terms/)

As the latest member of the NVIDIA Blackwell architecture family, the NVIDIA Blackwell Ultra GPU builds on core innovations to accelerate training and AI reasoning. It fuses silicon innovations with new levels of system-level integration, delivering next-level performance, scalability, and efficiency for AI factories and the large-scale, real-time AI services they power.

With its energy-efficient dual-reticle design, high bandwidth and large-capacity HBM3E memory subsystem, fifth-generation Tensor Cores, and breakthrough [NVFP4](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/) precision format, Blackwell Ultra is raising the bar for accelerated computing. This in-depth look explains the architectural advances, why they matter, and how they translate into measurable gains for AI workloads.

## Dual-reticle design: one GPU[](#dual-reticle_design_one_gpu)

Blackwell Ultra is composed of two reticle-sized dies connected using NVIDIA High-Bandwidth Interface (NV-HBI), a custom, power-efficient die-to-die interconnect technology that provides 10 TB/s of bandwidth. Blackwell Ultra is manufactured using TSMC 4NP and features 208B transistors–2.6x more than the [NVIDIA Hopper GPU](https://www.nvidia.com/en-us/data-center/technologies/hopper-architecture/)—all while functioning as a single, NVIDIA CUDA-programmed accelerator. This enables a large increase in performance while also maintaining the familiar CUDA programming model that developers have enjoyed for nearly two decades.

### Benefits[](#benefits)

- **Unified compute domain:** 160\* Streaming Multiprocessors (SMs) across two dies, providing 640 fifth-generation Tensor Cores with 15 PetaFLOPS dense NVFP4 compute.
- **Full coherence:** Shared L2 cache with fully coherent memory accesses.
- **Maximum silicon utilization:** Peak performance per square millimeter.

![Diagram of NVIDIA Blackwell Ultra GPU showing dual reticle dies linked by a 10 TB/s NV-HBI interface. Each die contains a GigaThread Engine with MIG control, L2 cache, and 8 GPCs with a total of 640 5th generation Tensor Cores (15 PFLOPS dense NVFP4). Callouts highlight PCIe Gen 6 (256 GB/s), NVLink v5 (1,800 GB/s to NVSwitch), NVLink-C2C (900 GB/s CPU–GPU), and 288 GB HBM3E (12-hi stacks, up to 8 TB/s).](https://developer-blogs.nvidia.com/wp-content/uploads/2025/08/NVIDIA-Blackwell-Ultra-GPU-chip-png.webp)

![Diagram of NVIDIA Blackwell Ultra GPU showing dual reticle dies linked by a 10 TB/s NV-HBI interface. Each die contains a GigaThread Engine with MIG control, L2 cache, and 8 GPCs with a total of 640 5th generation Tensor Cores (15 PFLOPS dense NVFP4). Callouts highlight PCIe Gen 6 (256 GB/s), NVLink v5 (1,800 GB/s to NVSwitch), NVLink-C2C (900 GB/s CPU–GPU), and 288 GB HBM3E (12-hi stacks, up to 8 TB/s).](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%202182%201420%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

*Figure 1. NVIDIA Blackwell Ultra GPU chip explained*  
\* Blackwell Ultra GPUs contain up to 160 SMs and 288GB HBM3E Memory. Available SM count and HBM capacity varies by SKU.

## Streaming multiprocessors: compute engines for the AI Factory[](#streaming_multiprocessors_compute_engines_for_the_ai_factory)

As shown in Figure 1, the heart of Blackwell Ultra is its 160 Streaming Multiprocessors (SMs) organized into eight Graphics Processing Clusters (GPCs) in the full GPU implementation. Every SM, shown in Figure 2, is a self-contained compute engine housing:

- **128 CUDA Cores** for FP32 and INT32 operations, also FP16/BF16 and other precisions.
- **4 fifth-generation Tensor Cores** with NVIDIA second-generation Transformer Engine, optimized for FP8, FP6, and NVFP4.
- **256 KB of Tensor Memory (TMEM)** for warp-synchronous storage of intermediate results, enabling higher reuse and reduced off-chip memory traffic.
- **Special Function Units (SFUs)** for transcendental math and special operations used in AI kernels.

![Diagram of Blackwell Ultra Streaming Multiprocessor (SM) architecture showing CUDA cores, Tensor Cores, TMEM, shared memory, SFUs, Tex blocks, and other SM units.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/08/Blackwell-Ultra-SM-architecture-png.webp)

![Diagram of Blackwell Ultra Streaming Multiprocessor (SM) architecture showing CUDA cores, Tensor Cores, TMEM, shared memory, SFUs, Tex blocks, and other SM units.](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201435%201999%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

*Figure 2. Blackwell Ultra SM architecture*

## NVIDIA Tensor Cores, AI compute powerhouses[](#nvidia_tensor_cores_ai_compute_powerhouses)

When NVIDIA first introduced Tensor Cores in the Volta architecture, they fundamentally changed what GPUs could do for deep learning. Instead of executing scalar or vector operations one element at a time, Tensor Cores operate directly on small matrices—performing matrix multiply-accumulate (MMA) in a single instruction. This was a perfect match for neural networks, where the vast majority of computation comes down to multiplying and summing large grids of numbers.

Over successive generations, Tensor Cores have expanded in capability, precision formats, and parallelism:

- **NVIDIA Volta:** 8-thread MMA units, FP16 with FP32 accumulation for training.
- **NVIDIA Ampere:** Full warp-wide MMA, BF16, and TensorFloat-32 formats.
- **NVIDIA Hopper:** Warp-group MMA across 128 threads, Transformer Engine with FP8 support.

Blackwell and Blackwell Ultra take this to the next level with their fifth-generation Tensor Cores and second-generation Transformer Engine, delivering [higher throughput and lower latency](https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/%20https://resources.nvidia.com/en-us-blackwell-architecture/blackwell-architecture-technical-brief) for both dense and sparse AI workloads. Each Streaming Multiprocessor (SM) contains four Tensor Cores across the 160 SMs in Blackwell Ultra, adding up to 640 Tensor Cores upgraded to handle the newest precision format, NVFP4.

These enhancements aren’t just about raw FLOPS. The new Tensor Cores are tightly integrated with 256 KB of Tensor Memory (TMEM) per SM, optimized to keep data close to the compute units. They also support dual-thread-block MMA, where paired SMs cooperate on a single MMA operation, sharing operands and reducing redundant memory traffic.

The result is higher sustained throughput, better memory efficiency, and faster large-batch pre-training, reinforcement learning for post-training, and low-batch, high-interactivity inference.

## Ultra-charged NVFP4 performance[](#ultra-charged_nvfp4_performance)

The [introduction of NVIDIA NVFP4](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/), the new 4‑bit floating‑point format in the Blackwell GPU architecture, combines two-level scaling—an FP8 (E4M3) micro-block scale applied to 16‑value blocks plus a tensor-level FP32 scale—enabling hardware‑accelerated quantization with markedly lower error rates than standard FP4. This Tensor Core capability delivers nearly FP8‑equivalent accuracy (with often less than ~1% difference), while reducing memory footprint by [~1.8x compared to FP8 and up to ~3.5x vs. FP16](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/). NVFP4 strikes an optimal balance of accuracy, efficiency, and performance for low‑precision AI inference.

The Blackwell Ultra dense NVFP4 compute capability provides a substantial performance uplift over the original Blackwell GPU. While the base architecture delivers 10 petaFLOPS of NVFP4 performance, Ultra pushes that to 15 petaFLOPS—a [1.5x increase compared to Blackwell GPU and 7.5x increase](https://resources.nvidia.com/en-us-blackwell-architecture/blackwell-architecture-technical-brief) from NVIDIA Hopper [H100](https://www.nvidia.com/en-us/data-center/h100/) and [H200](https://www.nvidia.com/en-us/data-center/h200/) GPUs, as shown in Figure 3. This boost directly benefits large-scale inference, enabling more concurrent model instances, faster response times, and lower costs per token generated.

![Bar chart comparing dense FP8 performance on Hopper, which includes H100 and H200 at 2 petaFLOPS, vs NVFP4 performance for Blackwell (10 petaFLOPS) vs Blackwell Ultra (15 petaFLOPS) with an arrow indicating a 7.5x increase from Hopper to Blackwell Ultra and 1.5x increase from Blackwell to Blackwell Ultra.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/08/Blackwell-Ultra-Throughput-png.webp)

![Bar chart comparing dense FP8 performance on Hopper, which includes H100 and H200 at 2 petaFLOPS, vs NVFP4 performance for Blackwell (10 petaFLOPS) vs Blackwell Ultra (15 petaFLOPS) with an arrow indicating a 7.5x increase from Hopper to Blackwell Ultra and 1.5x increase from Blackwell to Blackwell Ultra.](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201388%20796%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

*Figure 3. Blackwell Ultra GPU delivers 1.5x more dense NVFP4 throughput compared to Blackwell*

## Accelerated softmax in the attention layer[](#accelerated_softmax_in_the_attention_layer)

Modern AI workloads rely heavily on attention processing with long input contexts and long output sequences for “thinking”. Transformer attention layers, in turn, stress exponentials, divisions, and other transcendental operations executed by the SM’s SFUs.

In Blackwell Ultra, SFU throughput has been doubled for key instructions used in attention, delivering up to [2x faster attention-layer](https://nvdam.widen.net/s/xqt56dflgh/nvidia-blackwell-architecture-technical-brief#%5B%7B%22num%22%3A13%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22XYZ%22%7D%2C73%2C325%2C0%5D) compute compared to Blackwell GPUs. This improvement accelerates both short and long-sequence attention, but is especially impactful for reasoning models with large context windows—where the softmax stage can become a latency bottleneck.

By accelerating the attention mechanism within transformer models, Blackwell Ultra enables:

- Faster AI reasoning with lower time-to-first-token in interactive applications.
- Lower compute costs by reducing total processing cycles per query.
- Higher system efficiency—more attention sequences processed per watt.

As depicted in Figure 4, the performance gains from the accelerated attention-layer instructions in Blackwell Ultra compound with NVFP4 precision, resulting in a step-function improvement for LLM and multimodal inference.

![Diagram showing the attention computation pipeline with doubled SFU throughput for exponential operations and 50% faster NVFP4 during batched matrix multiplies, reducing overall Softmax latency.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/08/Blackwell-Ultra-attention-layer-acceleration-png.webp)

![Diagram showing the attention computation pipeline with doubled SFU throughput for exponential operations and 50% faster NVFP4 during batched matrix multiplies, reducing overall Softmax latency.](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%20796%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

*Figure 4. Blackwell Ultra attention-layer acceleration*

## Memory: high capacity and bandwidth for multi-trillion-parameter models[](#memory_high_capacity_and_bandwidth_for_multi-trillion-parameter_models)

Blackwell Ultra doesn’t just scale compute—it scales memory capacity to meet the demands of the largest AI models. With 288 GB of HBM3e per GPU, it offers 3.6x more on-package memory than H100 and 50% more than Blackwell, as shown in Figure 5. This capacity is critical for hosting trillion-parameter models, extending context length without KV-cache offloading, and enabling high-concurrency inference in AI factories.

### High bandwidth memory features[](#high_bandwidth_memory_features)

- **Max capacity:** 288 GB, 3.6x increase over H100
- **HBM configuration:** Eight 12-Hi stacks, 16 × 512-bit controllers (8,192-bit total width)
- **Bandwidth:** 8 TB/s per GPU, 2.4x improvement over H100 (3.35 TB/s)

![Bar chart comparing GPU HBM capacity: Hopper H100 (80 GB), Hopper H200 (141 GB), Blackwell (192 GB), and Blackwell Ultra (288 GB), with an arrow labeled “3.6x” between Hopper and Blackwell Ultra.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/08/capacity-scaling-png.webp)

![Bar chart comparing GPU HBM capacity: Hopper H100 (80 GB), Hopper H200 (141 GB), Blackwell (192 GB), and Blackwell Ultra (288 GB), with an arrow labeled “3.6x” between Hopper and Blackwell Ultra.](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201110%20596%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

*Figure 5. HBM capacity scaling across GPU generations*

This massive memory footprint enables:

- **Complete model residence:** 300B+ parameter models without memory offloading.
- **Extended context lengths:** Larger KV cache capacity for transformer models.
- **Improved compute efficiency:** Higher compute-to-memory ratios for diverse workloads.

## Interconnect: built for scale[](#interconnect_built_for_scale)

Blackwell and Blackwell Ultra support fifth-generation NVIDIA NVLink for GPU-to-GPU communication over NVLink Switch, NVLink-C2C for coherent interconnect to an NVIDIA Grace CPU, and x16 PCI-Express Gen 6 interface for connection to host CPUs.

### NVLink 5 Specifications[](#nvlink_5_specifications)

- **Per-GPU Bandwidth:** 1.8 TB/s bidirectional (18 links x 100 GB/s)
- **Performance Scaling:** 2x improvement over NVLink 4 (Hopper GPU)
- **Maximum Topology:** 576 GPUs in non-blocking compute fabric
- **Rack-Scale Integration:** 72-GPU NVL72 configurations with 130 TB/s aggregate bandwidth

### Host connectivity:[](#host_connectivity)

- **PCIe Interface:** Gen6 × 16 lanes (256 GB/s bidirectional)
- **NVLink-C2C:** Grace CPU-GPU communication with memory coherency (900 GB/s)

Table 1 provides a comparison of the interconnects across generations.

| **Interconnect** | **Hopper GPU** | **Blackwell GPU** | **Blackwell Ultra GPU** |
|----|----|----|----|
| NVLink (GPU-GPU) | 900 | 1,800 | 1,800 |
| NVLink-C2C (CPU-GPU) | 900 | 900 | 900 |
| PCIe Interface | 128 (Gen 5) | 256 (Gen 6) | 256 (Gen 6) |

*Table 1. Interconnect comparison of Hopper compared to Blackwell and Blackwell Ultra (in BiD*ir GB/s)

## Advancing performance-efficiency[](#advancing_performance-efficiency)

Blackwell Ultra delivers a decisive leap over Blackwell by adding 50% more NVFP4 compute and 50% more HBM capacity per chip, enabling larger models and faster throughput without compromising efficiency. Accelerated softmax execution further boosts real-world inference speeds, driving up tokens per second per user (TPS/user) while improving data center tokens per second per megawatt (TPS/MW). Every architectural enhancement was purpose-built to push both user experience and operational efficiency to the next level.

As shown in Figure 6, plotting these two metrics for the NVIDIA Hopper HGX H100 NVL8 system, NVIDIA Blackwell HGX B200 NVL8 system, NVIDIA Blackwell GB200 NVL72 system, and NVIDIA Blackwell Ultra GB300 NVL72 system reveals a generational leap. The curve starts with Hopper NVL8 at FP8 precision and ends with Blackwell Ultra NVL72 at NVFP4 precision—showing how each architectural advance pushes the Pareto frontier up and to the right.

![Animated Pareto frontier chart transitioning through three generations of NVIDIA architecture: starting with Hopper (lowest curve), then expanding to Blackwell (mid-tier curve), and finally to Blackwell Ultra (top curve). ](https://developer-blogs.nvidia.com/wp-content/uploads/2025/08/AI-factory-output.gif)

![Animated Pareto frontier chart transitioning through three generations of NVIDIA architecture: starting with Hopper (lowest curve), then expanding to Blackwell (mid-tier curve), and finally to Blackwell Ultra (top curve). ](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201920%201080%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

*Figure 6. AI factory output evolution from Hopper to Blackwell Ultra*

These architectural innovations improve the [economics of AI inference](https://blogs.nvidia.com/blog/ai-inference-economics/) and redefine what’s possible in AI factory design—delivering more model instances, faster responses, and higher output per megawatt than any previous NVIDIA platform.

To see firsthand how innovations in hardware and deployment configurations impact data center efficiency and user experience, check out our interactive [Pareto Frontier explainer.](https://resources.nvidia.com/en-us-inference-contact-us/discover-ai-inference)

## Enterprise-grade features[](#enterprise-grade_features)

Blackwell Ultra isn’t just about raw performance—it’s designed with enterprise-grade features that simplify operations, strengthen security, and deliver reliable performance at scale.

### Advanced scheduling and management[](#advanced_scheduling_and_management)

- **Enhanced GigaThread Engine:** Next-generation work scheduler providing improved context switching performance and optimized workload distribution across all 160 SMs.
- **Multi-Instance GPU (MIG):** Blackwell Ultra GPUs can be partitioned into different-sized [MIG](https://www.nvidia.com/en-us/technologies/multi-instance-gpu/) instances. For example, an administrator can create two instances with 140 GB of memory each, four instances with 70 GB each, or seven instances with 34 GB each, enabling secure multi-tenancy with predictable performance isolation.

### Security and reliability[](#security_and_reliability)

- [**Confidential computing and secure AI**](https://www.nvidia.com/en-us/data-center/solutions/confidential-computing/)**:** Secure and performant protection for sensitive AI models and data, extending hardware-based Trusted Execution Environment (TEE) to GPUs with industry-first TEE-I/O capabilities in the Blackwell architecture and inline NVLink protection for near-identical throughput when compared to unencrypted modes.
- **[Advanced NVIDIA **Reliability, Availability, and Serviceability** (RAS) engine](https://nvdam.widen.net/s/xqt56dflgh/nvidia-blackwell-architecture-technical-brief#%5B%7B%22num%22%3A20%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22XYZ%22%7D%2C70%2C720%2C0%5D):** AI-powered reliability system monitoring thousands of parameters to predict failures, optimize maintenance schedules, and maximize system uptime in large-scale deployments.

## AI video and data processing enhancements[](#ai_video_and_data_processing_enhancements)

Blackwell Ultra also integrates specialized engines for modern AI workloads requiring multimodal data processing:

- **Video and JPEG decoding:** The NVIDIA Video Decoder (NVDEC) and NVIDIA JPEG Decoder (NVJPEG) engines are specialized fixed-function hardware units for high-throughput image and video processing.
  - NVDEC supports modern codecs like AV1, HEVC, and H.264, enabling batch or real-time video decoding directly on the GPU without using CUDA Cores. 
  - NVJPEG accelerates JPEG decompression in hardware, making large-scale image pipelines dramatically faster. 
  - Both engines are leveraged by [NVIDIA DALI](https://developer.nvidia.com/dali) (Data Loading Library), which integrates them into AI training and inference workflows for tasks like image augmentation, dataset preprocessing, and multimodal model input preparation.
- **Decompression engine:** Hardware-accelerated data decompression at 800 GB/s throughput, reducing CPU overhead and accelerating compressed dataset loading for analytics workloads. NVIDIA [nvCOMP](https://developer.nvidia.com/nvcomp) enables portable programming of the decompression engine.

## NVIDIA GPU chip summary comparison[](#nvidia_gpu_chip_summary_comparison)

To put Blackwell Ultra’s advances in perspective, Table 2 compares key chip specifications across Hopper, Blackwell, and Blackwell Ultra. It highlights the generational leap in transistor count, memory capacity, interconnect bandwidth, and precision compute throughput—as well as the architectural enhancements like attention acceleration and NVFP4. This side-by-side view shows how Blackwell Ultra scales up performance and extends capabilities critical for AI factory deployments at both node and rack scale.

[TABLE]

*Table 2. NVIDIA GPU chip comparison*

## From chip to AI factory[](#from_chip_to_ai_factory)

Blackwell Ultra GPUs form the backbone of NVIDIA’s next-generation AI infrastructure—delivering transformative performance from desktop superchips to full AI factory racks.  

### NVIDIA Grace Blackwell Ultra Superchip[](#nvidia_grace_blackwell_ultra_superchip)

This superchip couples one Grace CPU with two Blackwell Ultra GPUs through NVLink‑C2C, offering up to 30 PFLOPS dense, and 40 PFLOPS sparse, NVFP4 AI compute, and boasts 1 TB of unified memory combining HBM3E and LPDDR5X for unprecedented on-node capacity. ConnectX-8 SuperNICs provide 800 Gb/s high-speed network connectivity (See Figure 7). The NVIDIA Grace Blackwell Ultra Superchip is the foundational computing component of the GB300 NVL 72 rack-scale system.

![Photograph of the NVIDIA Grace Blackwell Ultra Superchip board, featuring a Grace CPU surrounded by LPDDR5X memory, and two Blackwell Ultra GPUs on a single module, surrounded by HBM3E memory stacks, with integrated NVIDIA ConnectX-8 SuperNICs providing high-speed network connectivity.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/08/ConnectX-8-SuperNICs-png.webp)

![Photograph of the NVIDIA Grace Blackwell Ultra Superchip board, featuring a Grace CPU surrounded by LPDDR5X memory, and two Blackwell Ultra GPUs on a single module, surrounded by HBM3E memory stacks, with integrated NVIDIA ConnectX-8 SuperNICs providing high-speed network connectivity.](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201294%20942%22%3E%3C/svg%3E)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=)

*Figure 7. NVIDIA Grace Blackwell Ultra Superchip with ConnectX-8 SuperNICs*

- **NVIDIA GB300 NVL72 rack-scale system:** This liquid-cooled rack integrates 36 Grace Blackwell Superchips, interconnected through NVLink 5 and NVLink Switching, enabling it to achieve 1.1  exaFLOPS dense FP4 compute. The [GB300 NVL72](https://www.nvidia.com/en-us/data-center/gb300-nvl72/) also enables a 50x higher AI factory output, combining 10x better latency (TPS per user) and 5x higher throughput per megawatt relative to Hopper platforms. GB300 systems also redefine rack power management. They rely on multiple power-shelf configurations to handle synchronous GPU load ramps. NVIDIA [power smoothing](https://developer.nvidia.com/blog/how-new-gb300-nvl72-features-provide-steady-power-for-ai) innovations—including energy storage and burn mechanisms—help stabilize power draw across training workloads.
- **NVIDIA HGX and DGX B300 systems:** Standardized 8 GPU Blackwell Ultra configurations. NVIDIA [HGX B300](https://www.nvidia.com/en-us/data-center/hgx/) and NVIDIA [DGX B300](https://www.nvidia.com/en-us/data-center/dgx-b300/) Systems continue to support flexible deployment models for AI infrastructure while maintaining full CUDA and NVLink compatibility.

## Complete CUDA compatibility[](#complete_cuda_compatibility)

Blackwell Ultra maintains full backward compatibility with the entire CUDA ecosystem while introducing optimizations for next-generation AI frameworks:

- **Framework integration:** Native support in SGLang, TensorRT-LLM, and vLLM with optimized kernels for NVFP4 precision and dual-die architecture.
- **NVIDIA Dynamo:** A distributed inference and scheduling framework that intelligently orchestrates workloads across thousands of GPUs, delivering up to [30x higher](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/) throughput for large-scale deployments.
- **NVIDIA Enterprise AI:** End-to-end, cloud-native AI software platform delivering optimized frameworks, SDKs, microservices, and enterprise-grade tools for developing, deploying, and managing AI workloads at scale.
- **NVIDIA development tools and CUDA libraries:**
  - CUTLASS for custom kernel development
  - Nsight Systems and Nsight Compute for profiling and tuning
  - Model Optimizer for precision-aware graph optimization
  - cuDNN for deep learning primitives
  - NCCL for multi-GPU communication
  - CUDA Graphs for reducing launch overhead

## The bottom line[](#the_bottom_line)

NVIDIA Blackwell Ultra establishes the foundation for AI factories to train and deploy intelligence at unprecedented scale and efficiency. With breakthrough innovations in dual-die integration, NVFP4 acceleration, massive memory capacity, and advanced interconnect technology, Blackwell Ultra enables AI applications that were previously computationally impossible.

As the industry transitions from proof-of-concept AI to production AI factories, Blackwell Ultra provides the computational foundation to turn AI ambitions into reality with unmatched performance, efficiency, and scale.

## Learn more[](#learn_more)

Dive deeper into the innovations powering the trillion-token era. Download the [Blackwell Architecture Technical Brief](https://resources.nvidia.com/en-us-blackwell-architecture/blackwell-architecture-technical-brief) to explore the full silicon-to-system story.

## Acknowledgments[](#acknowledgments)

*We’d like to thank Manas Mandal, Ronny Krashinsky, Vishal Mehta, Greg Palmer, Michael Andersch, Eduardo Alvarez, Ashraf Eassa, Joe DeLaere, and many other NVIDIA GPU architects, engineers, and product leaders who contributed to this post.*

*This post was updated on 9/24/25 to correct Figure 1 and the HBM configuration section to show the proper 12 HBM stacks instead of 8.*

[ Discuss (1)](#entry-content-comments)

Like

## Tags

[Data Center / Cloud](https://developer.nvidia.com/blog/category/data-center-cloud/) \| [Networking / Communications](https://developer.nvidia.com/blog/category/networking-communications/) \| [Hardware / Semiconductor](https://developer.nvidia.com/blog/recent-posts/?industry=Hardware+%2F+Semiconductor) \| [Blackwell](https://developer.nvidia.com/blog/recent-posts/?products=Blackwell) \| [GB200](https://developer.nvidia.com/blog/recent-posts/?products=GB200) \| [H100](https://developer.nvidia.com/blog/recent-posts/?products=H100) \| [H200](https://developer.nvidia.com/blog/recent-posts/?products=H200) \| [NVLink](https://developer.nvidia.com/blog/recent-posts/?products=NVLink) \| [TensorRT](https://developer.nvidia.com/blog/recent-posts/?products=TensorRT) \| [Intermediate Technical](https://developer.nvidia.com/blog/recent-posts/?learning_levels=Intermediate+Technical) \| [Deep dive](https://developer.nvidia.com/blog/recent-posts/?content_types=Deep+dive) \| [featured](https://developer.nvidia.com/blog/tag/featured/) \| [Inference Performance](https://developer.nvidia.com/blog/tag/inference-performance/)

## About the Authors

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2025/04/cropped-kyle-aubrey-131x131.png)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Kyle Aubrey**  
Kyle Aubrey is the director of Technical Marketing at NVIDIA, where he leads initiatives in AI inference and training across NVIDIA accelerated computing platforms, including Hopper, Blackwell, Rubin, and beyond. With a passion for demystifying complex technologies, he empowers diverse audiences to harness the full potential of NVIDIA's cutting-edge solutions. Kyle holds a bachelor’s degree in Electrical Engineering from Rose-Hulman Institute of Technology and an MBA from Pepperdine University.

[View all posts by Kyle Aubrey![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/kaubrey/)

![Avatar photo](https://developer-blogs.nvidia.com/wp-content/uploads/2022/03/Nick-Stam-131x131.jpg)

![Avatar photo](data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E)

**About Nick Stam**  
Nick Stam is a senior technical marketing director at NVIDIA. His team provides tech support to media and industry analysts, while also generating whitepapers and reviewer collateral. Prior to NVIDIA, Nick worked at PC Magazine USA for many years, and co-founded the ExtremeTech website. Nick has worked in various technical and management positions in the computer industry since 1980.

[View all posts by Nick Stam![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==)](https://developer.nvidia.com/blog/author/nstam/)

## Comments
