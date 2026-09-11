<!-- 从 nvidia-grace-hopper-blog.html 迁移的资料快照；原始 HTML SHA-256: 1857975b830810a388df90cddbd9b5bac6de50e11560bb09e362802ac3dfe93f。 -->

<div class="main-content col-lg-9 col-md-9 mt-0" role="main">

<div class="post-card--single">

<div class="row">

<div class="col-lg-12 mb-0">

<div class="card--post-attributes">

<span class="category-name content-s"> <a href="https://developer.nvidia.com/blog/category/data-science/" data-wpel-link="internal" target="_self" rel="follow">Data Science</a> </span> <span class="post-rate-widget content-s"></span> <span class="post-lang-switcher"> </span>

<div class="posts-filter-form">

<div class="filter-item form-type-select">

English日本語

</div>

</div>

</div>

# NVIDIA Grace Hopper Superchip Architecture In-Depth

<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-1-e1670969676880-1024x576.png" class="attachment-full-page-width size-full-page-width wp-post-image" decoding="async" data-fetchpriority="high" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-1-e1670969676880-1024x576.png 1024w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-1-e1670969676880-300x169.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-1-e1670969676880-625x352.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-1-e1670969676880-179x101.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-1-e1670969676880-768x432.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-1-e1670969676880-500x281.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-1-e1670969676880-160x90.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-1-e1670969676880-362x204.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-1-e1670969676880-195x110.png 195w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-1-e1670969676880.png 1077w" sizes="(max-width: 1024px) 100vw, 1024px" width="1024" height="576" />

<div class="post-info">

<div class="post-published-date">

Nov 10, 2022

</div>

<div class="post-authors">

By <a href="https://developer.nvidia.com/blog/author/jevans/" class="author url fn" rel="author follow" data-wpel-link="internal" target="_self" title="Posts by Jonathon Evans">Jonathon Evans</a>, <a href="https://developer.nvidia.com/blog/author/mandersch/" class="author url fn" rel="author follow" data-wpel-link="internal" target="_self" title="Posts by Michael Andersch">Michael Andersch</a>, <a href="https://developer.nvidia.com/blog/author/vsethi/" class="author url fn" rel="author follow" data-wpel-link="internal" target="_self" title="Posts by Vikram Sethi">Vikram Sethi</a>, <a href="https://developer.nvidia.com/blog/author/gonzalob/" class="author url fn" rel="author follow" data-wpel-link="internal" target="_self" title="Posts by Gonzalo Brito">Gonzalo Brito</a> and <a href="https://developer.nvidia.com/blog/author/vishalm/" class="author url fn" rel="author follow" data-wpel-link="internal" target="_self" title="Posts by Vishal Mehta">Vishal Mehta</a>

</div>

<div class="card--post-attributes-secondary card--post-attributes-header">

<div class="post--rate secondary--attribute">

<div class="wpulike wpulike-heart">

<div class="wp_ulike_general_class wp_ulike_is_not_liked">

<span class="count-box wp_ulike_counter_up" ulike-counter-value="+52"></span>

</div>

</div>

Like

</div>

<div class="post--comments-count secondary--attribute">

[ Discuss (12)](#entry-content-comments)

</div>

</div>

</div>

</div>

</div>

</div>

<div class="entry-meta-social">

- <a href="https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fnvidia-grace-hopper-superchip-architecture-in-depth%2F" class="for-linkedin" data-wpel-link="external" target="_blank" rel="follow">L</a>
- <a href="https://twitter.com/intent/tweet?text=NVIDIA+Grace+Hopper+Superchip+Architecture+In-Depth+%7C+NVIDIA+Technical+Blog+https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fnvidia-grace-hopper-superchip-architecture-in-depth%2F" class="for-twitter" data-wpel-link="external" target="_blank" rel="follow">T</a>
- <a href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fnvidia-grace-hopper-superchip-architecture-in-depth%2F" class="for-facebook" data-wpel-link="external" target="_blank" rel="follow">F</a>
- <a href="https://www.reddit.com/submit?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fnvidia-grace-hopper-superchip-architecture-in-depth%2F&amp;title=NVIDIA+Grace+Hopper+Superchip+Architecture+In-Depth+%7C+NVIDIA+Technical+Blog" class="for-reddit" data-wpel-link="external" target="_blank" rel="follow">R</a>
- <a href="mailto:?subject=I&#39;d%20like%20to%20share%20a%20link%20with%20you&amp;body=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fnvidia-grace-hopper-superchip-architecture-in-depth%2F" class="for-mail">E</a>

</div>

<img src="data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibnYtYWktc3VtbWFyeV9faWNvbiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB3aWR0aD0iMjUiIGhlaWdodD0iMjUiIHZpZXdib3g9IjAgMCAyNSAyNSIgZmlsbD0ibm9uZSIgYXJpYS1oaWRkZW49InRydWUiPgogICAgICAgICAgICAgICAgPHBhdGggZmlsbD0iY3VycmVudENvbG9yIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTIyLjQ5MTUgMTUuMzAxOUMyMi4yOTQgMTUuMzA0NyAyMi4wOTc2IDE1LjMzMTYgMjEuOTA2NiAxNS4zODE5TDIwLjI1NCAxMi45MDE5TDIxLjkwNSAxMC40MjE5QzIyLjA5NjcgMTAuNDczMSAyMi4yOTMzIDEwLjQ5ODcgMjIuNDkxNSAxMC41MDE5QzIyLjg4NDQgMTAuNTAzMiAyMy4yNzE2IDEwLjQwNzggMjMuNjE5IDEwLjIyNDFDMjMuOTY2NSAxMC4wNDA0IDI0LjI2MzUgOS43NzQwNSAyNC40ODM5IDkuNDQ4NDVDMjQuNzA0NCA5LjEyMjg1IDI0Ljg0MTUgOC43NDc5OSAyNC44ODMyIDguMzU2ODdDMjQuOTI1IDcuOTY1NzUgMjQuODcwMSA3LjU3MDM1IDI0LjcyMzMgNy4yMDU0N0MyNC41NzY2IDYuODQwNTkgMjQuMzQyNSA2LjUxNzQxIDI0LjA0MTcgNi4yNjQzN0MyMy43NDA5IDYuMDExMzQgMjMuMzgyNSA1LjgzNjIgMjIuOTk4MiA1Ljc1NDM3QzIyLjYxMzkgNS42NzI1NSAyMi4yMTU0IDUuNjg2NTQgMjEuODM3OCA1Ljc5NTEyQzIxLjQ2MDEgNS45MDM3IDIxLjExNDkgNi4xMDM1NCAyMC44MzI2IDYuMzc3MDZMMTUuMjcwOSAzLjU5MzA1QzE1LjI4NjggMy40OTcwNSAxNS4yOTY0IDMuMzk5NDYgMTUuMjk5NiAzLjMwMTg2QzE1LjI5OTYgMi42NjUzNCAxNS4wNDcxIDIuMDU0ODkgMTQuNTk3NSAxLjYwNDhDMTQuMTQ3OSAxLjE1NDcxIDEzLjUzODEgMC45MDE4NTUgMTIuOTAyMyAwLjkwMTg1NUMxMi4yNjY1IDAuOTAxODU1IDExLjY1NjggMS4xNTQ3MSAxMS4yMDcyIDEuNjA0OEMxMC43NTc2IDIuMDU0ODkgMTAuNTA1MSAyLjY2NTM0IDEwLjUwNTEgMy4zMDE4NkMxMC41MDgzIDMuMzk5NDYgMTAuNTE3OCAzLjQ5NzA1IDEwLjUzMzggMy41OTMwNUw0Ljk3MjExIDYuMzc3MDZDNC42ODk3NiA2LjEwMjY3IDQuMzQ0MzMgNS45MDIwMiAzLjk2NjI2IDUuNzkyODFDMy41ODgxOCA1LjY4MzYgMy4xODkwOCA1LjY2OTE4IDIuODA0MTIgNS43NTA4MkMyLjQxOTE2IDUuODMyNDUgMi4wNjAxOCA2LjAwNzY0IDEuNzU4OCA2LjI2MDkzQzEuNDU3NDMgNi41MTQyMyAxLjIyMjkyIDYuODM3ODYgMS4wNzU5NSA3LjIwMzI5QzAuOTI4OTgxIDcuNTY4NzIgMC44NzQwNTggNy45NjQ3NCAwLjkxNjAyOCA4LjM1NjQ0QzAuOTU3OTk4IDguNzQ4MTMgMS4wOTU1NyA5LjEyMzQ4IDEuMzE2NjIgOS40NDkzOUMxLjUzNzY3IDkuNzc1MyAxLjgzNTQgMTAuMDQxOCAyLjE4MzU4IDEwLjIyNTNDMi41MzE3NiAxMC40MDg4IDIuOTE5NyAxMC41MDM4IDMuMzEzMTkgMTAuNTAxOUMzLjUxMTM2IDEwLjQ5ODcgMy43MDc5NCAxMC40NzE1IDMuODk4MTMgMTAuNDIxOUw1LjU1MDY2IDEyLjkwMTlMMy44OTk3MyAxNS4zODE5QzMuNzA4MTggMTUuMzMxNCAzLjUxMTIyIDE1LjMwNDYgMy4zMTMxOSAxNS4zMDE5QzIuOTIwMjkgMTUuMzAwNSAyLjUzMzA4IDE1LjM5NTkgMi4xODU2NSAxNS41Nzk2QzEuODM4MjIgMTUuNzYzMyAxLjU0MTIyIDE2LjAyOTcgMS4zMjA3NyAxNi4zNTUzQzEuMTAwMzIgMTYuNjgwOSAwLjk2MzE4OSAxNy4wNTU3IDAuOTIxNDQyIDE3LjQ0NjhDMC44Nzk2OTUgMTcuODM4IDAuOTM0NjEzIDE4LjIzMzQgMS4wODEzNiAxOC41OTgyQzEuMjI4MTEgMTguOTYzMSAxLjQ2MjE5IDE5LjI4NjMgMS43NjMwMSAxOS41MzkzQzIuMDYzODIgMTkuNzkyNCAyLjQyMjE1IDE5Ljk2NzUgMi44MDY0NiAyMC4wNDkzQzMuMTkwNzcgMjAuMTMxMiAzLjU4OTI4IDIwLjExNzIgMy45NjY5MSAyMC4wMDg2QzQuMzQ0NTUgMTkuOSA0LjY4OTc0IDE5LjcwMDIgNC45NzIxMSAxOS40MjY3TDEwLjUzMzggMjIuMjEwN0MxMC41MTc4IDIyLjMwNjcgMTAuNTA4MyAyMi40MDQzIDEwLjUwNTEgMjIuNTAxOUMxMC41MDUxIDIzLjEzODQgMTAuNzU3NiAyMy43NDg4IDExLjIwNzIgMjQuMTk4OUMxMS42NTY4IDI0LjY0OSAxMi4yNjY1IDI0LjkwMTkgMTIuOTAyMyAyNC45MDE5QzEzLjUzODEgMjQuOTAxOSAxNC4xNDc5IDI0LjY0OSAxNC41OTc1IDI0LjE5ODlDMTUuMDQ3MSAyMy43NDg4IDE1LjI5OTYgMjMuMTM4NCAxNS4yOTk2IDIyLjUwMTlDMTUuMjk1OCAyMi40MDQzIDE1LjI4NjIgMjIuMzA3MSAxNS4yNzA5IDIyLjIxMDdMMjAuODMyNiAxOS40MjY3QzIxLjExNDkgMTkuNzAxIDIxLjQ2MDQgMTkuOTAxNyAyMS44Mzg0IDIwLjAxMDlDMjIuMjE2NSAyMC4xMjAxIDIyLjYxNTYgMjAuMTM0NSAyMy4wMDA2IDIwLjA1MjlDMjMuMzg1NSAxOS45NzEzIDIzLjc0NDUgMTkuNzk2MSAyNC4wNDU5IDE5LjU0MjhDMjQuMzQ3MyAxOS4yODk1IDI0LjU4MTggMTguOTY1OSAyNC43Mjg3IDE4LjYwMDRDMjQuODc1NyAxOC4yMzUgMjQuOTMwNiAxNy44MzkgMjQuODg4NyAxNy40NDczQzI0Ljg0NjcgMTcuMDU1NiAyNC43MDkxIDE2LjY4MDIgMjQuNDg4MSAxNi4zNTQzQzI0LjI2NyAxNi4wMjg0IDIzLjk2OTMgMTUuNzYxOSAyMy42MjExIDE1LjU3ODRDMjMuMjcyOSAxNS4zOTQ5IDIyLjg4NSAxNS4yOTk5IDIyLjQ5MTUgMTUuMzAxOVpNMTIuODg4NCAyLjUwMjc0QzEzLjAxODUgMi41MDMyNCAxMy4xNDY1IDIuNTM1NTIgMTMuMjYxMyAyLjU5Njc5QzEzLjM3NjEgMi42NTgwNSAxMy40NzQyIDIuNzQ2NDQgMTMuNTQ3MSAyLjg1NDI5QzEzLjYyIDIuOTYyMTQgMTMuNjY1NSAzLjA4NjE3IDEzLjY3OTcgMy4yMTU2M0MxMy42OTM5IDMuMzQ1MDkgMTMuNjc2MyAzLjQ3NjA1IDEzLjYyODQgMy41OTcxNEwxMy42MDYgMy42NDE5NEMxMy41NDI5IDMuNzc5ODEgMTMuNDQxNiAzLjg5NjY0IDEzLjMxNDEgMy45Nzg1NUMxMy4xODY2IDQuMDYwNDUgMTMuMDM4MyA0LjEwMzk5IDEyLjg4NjggNC4xMDM5OUMxMi43MzUzIDQuMTAzOTkgMTIuNTg3IDQuMDYwNDUgMTIuNDU5NiAzLjk3ODU1QzEyLjMzMjEgMy44OTY2NCAxMi4yMzA3IDMuNzc5ODEgMTIuMTY3NiAzLjY0MTk0TDEyLjE0NTMgMy41OTg3NEMxMi4wOTcgMy40NzczMSAxMi4wNzkxIDMuMzQ1ODkgMTIuMDkzMyAzLjIxNTk2QzEyLjEwNzQgMy4wODYwMyAxMi4xNTMyIDIuOTYxNTYgMTIuMjI2NSAyLjg1MzQyQzEyLjI5OTggMi43NDUyOCAxMi4zOTg1IDIuNjU2NzggMTIuNTEzOSAyLjU5NTY0QzEyLjYyOTMgMi41MzQ1MSAxMi43NTc5IDIuNTAyNjEgMTIuODg4NCAyLjUwMjc0Wk0yMy4yNzY3IDguMTAyNzRDMjMuMjc2NyA4LjMxNDkxIDIzLjE5MjUgOC41MTg0IDIzLjA0MjYgOC42Njg0M0MyMi44OTI4IDguODE4NDUgMjIuNjg5NSA4LjkwMjc0IDIyLjQ3NzYgOC45MDI3NEMyMi4yNjU2IDguOTAyNzQgMjIuMDYyNCA4LjgxODQ1IDIxLjkxMjUgOC42Njg0M0MyMS43NjI3IDguNTE4NCAyMS42Nzg1IDguMzE0OTEgMjEuNjc4NSA4LjEwMjc0QzIxLjY3ODUgNy44OTA1NyAyMS43NjI3IDcuNjg3MDggMjEuOTEyNSA3LjUzNzA1QzIyLjA2MjQgNy4zODcwMiAyMi4yNjU2IDcuMzAyNzQgMjIuNDc3NiA3LjMwMjc0QzIyLjY4OTUgNy4zMDI3NCAyMi44OTI4IDcuMzg3MDIgMjMuMDQyNiA3LjUzNzA1QzIzLjE5MjUgNy42ODcwOCAyMy4yNzY3IDcuODkwNTcgMjMuMjc2NyA4LjEwMjc0Wk0yLjUwMDE3IDguMTAyNzRDMi41MDMgNy45MjMwNSAyLjU2NjE3IDcuNzQ5NTYgMi42Nzk1MSA3LjYxMDJDMi43OTI4NSA3LjQ3MDg1IDIuOTQ5NzYgNy4zNzM3NiAzLjEyNDk1IDcuMzM0NThDMy4zMDAxNCA3LjI5NTQgMy40ODM0IDcuMzE2NDEgMy42NDUyIDcuMzk0MjNDMy44MDcgNy40NzIwNSAzLjkzNzkyIDcuNjAyMTQgNC4wMTY4NSA3Ljc2MzU0TDQuMDM5MjMgNy44MDgzNEM0LjA5ODcxIDcuOTUzMDYgNC4xMTM3NiA4LjExMjI1IDQuMDgyNDQgOC4yNjU1OEM0LjA1MTEzIDguNDE4OSAzLjk3NDg4IDguNTU5NDEgMy44NjM0MyA4LjY2OTE0QzMuNzUxNTggOC43ODA3NiAzLjYwOTIxIDguODU2NyAzLjQ1NDI4IDguODg3MzdDMy4yOTkzNiA4LjkxODA1IDMuMTM4ODMgOC45MDIwNyAyLjk5Mjk3IDguODQxNDdDMi44NDcxIDguNzgwODYgMi43MjI0NSA4LjY3ODM1IDIuNjM0NzQgOC41NDY4N0MyLjU0NzAzIDguNDE1MzkgMi41MDAyIDguMjYwODQgMi41MDAxNyA4LjEwMjc0Wk0yLjUwMDE3IDE3LjcwMjdDMi41MDAxNyAxNy40OTA2IDIuNTg0MzYgMTcuMjg3MSAyLjczNDIyIDE3LjEzNzFDMi44ODQwOCAxNi45ODcgMy4wODczMyAxNi45MDI3IDMuMjk5MjcgMTYuOTAyN0MzLjUxMTIgMTYuOTAyNyAzLjcxNDQ1IDE2Ljk4NyAzLjg2NDMxIDE3LjEzNzFDNC4wMTQxNyAxNy4yODcxIDQuMDk4MzYgMTcuNDkwNiA0LjA5ODM2IDE3LjcwMjdDNC4wOTgzNiAxNy45MTQ5IDQuMDE0MTcgMTguMTE4NCAzLjg2NDMxIDE4LjI2ODRDMy43MTQ0NSAxOC40MTg1IDMuNTExMiAxOC41MDI3IDMuMjk5MjcgMTguNTAyN0MzLjA4NzMzIDE4LjUwMjcgMi44ODQwOCAxOC40MTg1IDIuNzM0MjIgMTguMjY4NEMyLjU4NDM2IDE4LjExODQgMi41MDAxNyAxNy45MTQ5IDIuNTAwMTcgMTcuNzAyN1pNMTIuODg4NCAyMy4zMDI3QzEyLjc1NjYgMjMuMzAyOCAxMi42MjY4IDIzLjI3MDIgMTIuNTEwNiAyMy4yMDc4QzEyLjM5NDQgMjMuMTQ1NSAxMi4yOTU1IDIzLjA1NTMgMTIuMjIyNSAyMi45NDU0QzEyLjE0OTYgMjIuODM1NSAxMi4xMDQ5IDIyLjcwOTIgMTIuMDkyNiAyMi41Nzc4QzEyLjA4MDIgMjIuNDQ2NCAxMi4xMDA1IDIyLjMxNCAxMi4xNTE3IDIyLjE5MjNDMTIuMjEyOCAyMi4wNTE5IDEyLjMxMjkgMjEuOTMxOSAxMi40NDAxIDIxLjg0NjhDMTIuNTY3MyAyMS43NjE2IDEyLjcxNjMgMjEuNzE0OCAxMi44NjkzIDIxLjcxMkMxMy4wMjIzIDIxLjcwOTEgMTMuMTcyOSAyMS43NTAzIDEzLjMwMzIgMjEuODMwNkMxMy40MzM2IDIxLjkxMSAxMy41MzgxIDIyLjAyNzEgMTMuNjA0NCAyMi4xNjUxTDEzLjYyNjggMjIuMjA5OUMxMy42ODY4IDIyLjM1NDEgMTMuNzAyNCAyMi41MTI5IDEzLjY3MTYgMjIuNjY1OUMxMy42NDA5IDIyLjgxOSAxMy41NjUxIDIyLjk1OTQgMTMuNDU0MiAyMy4wNjkxQzEzLjM3OTggMjMuMTQzNCAxMy4yOTE2IDIzLjIwMjIgMTMuMTk0NSAyMy4yNDIzQzEzLjA5NzQgMjMuMjgyNCAxMi45OTM0IDIzLjMwMjkgMTIuODg4NCAyMy4zMDI3Wk0yMi40Nzc2IDE4LjUwMjdDMjIuMzI2NyAxOC41MDE2IDIyLjE3OTMgMTguNDU3NyAyMi4wNTIzIDE4LjM3NjFDMjEuOTI1MyAxOC4yOTQ2IDIxLjgyNCAxOC4xNzg3IDIxLjc2IDE4LjA0MTlMMjEuNzM3NiAxNy45OTcxQzIxLjY5ODEgMTcuOTAyOSAyMS42Nzc3IDE3LjgwMTcgMjEuNjc3NyAxNy42OTk1QzIxLjY3NzcgMTcuNTk3MyAyMS42OTgxIDE3LjQ5NjIgMjEuNzM3NiAxNy40MDE5TDIxLjc1MiAxNy4zNzQ3QzIxLjgwOTggMTcuMjQyMiAyMS45MDIzIDE3LjEyNzkgMjIuMDE5OSAxNy4wNDM4QzIyLjEzNzQgMTYuOTU5OCAyMi4yNzU1IDE2LjkwOTIgMjIuNDE5NCAxNi44OTc0QzIyLjU2MzMgMTYuODg1NyAyMi43MDc4IDE2LjkxMzIgMjIuODM3MyAxNi45NzcxQzIyLjk2NjkgMTcuMDQwOSAyMy4wNzY4IDE3LjEzODggMjMuMTU1MiAxNy4yNjAxQzIzLjIzMzcgMTcuMzgxNSAyMy4yNzc4IDE3LjUyMTkgMjMuMjgzIDE3LjY2NjRDMjMuMjg4MSAxNy44MTA5IDIzLjI1NCAxNy45NTQxIDIzLjE4NDMgMTguMDgwOEMyMy4xMTQ2IDE4LjIwNzQgMjMuMDEyIDE4LjMxMjggMjIuODg3MiAxOC4zODU3QzIyLjc2MjUgMTguNDU4NiAyMi42MjA0IDE4LjQ5NjMgMjIuNDc2IDE4LjQ5NDdMMjIuNDc3NiAxOC41MDI3Wk0xOC4wMTg2IDkuODA4MzRMMjAuMTcxNCA4LjczMTU0QzIwLjE1NTQgOC42MzU1NCAyMC4xNDU4IDguNTM3OTQgMjAuMTQyNiA4LjQ0MDM0QzIwLjE0NTggOC4zNDI3NCAyMC4xNTU0IDguMjQ1MTQgMjAuMTcxNCA4LjE0OTE0TDE1LjI4NDEgNS43MDI3NEwxOC4wMTg2IDkuODA4MzRaTTEwLjYxNTggNS43MDQzNEw1LjczMDEyIDguMTQ5MTRDNS43NDU0NSA4LjI0NTU1IDUuNzU1MDUgOC4zNDI3OSA1Ljc1ODg4IDguNDQwMzRDNS43NTU2OSA4LjUzNzk0IDUuNzQ2MSA4LjYzNTU0IDUuNzMwMTIgOC43MzE1NEw3Ljg4Mjg4IDkuODA4MzRMMTAuNjE1OCA1LjcwNDM0Wk01LjczMDEyIDE3Ljc0OTFMNy44ODI4OCAxNi42NzIzTDEwLjYxNzQgMjAuNzc3OUw1LjczMDEyIDE4LjMzMTVDNS43NDYxIDE4LjIzNTUgNS43NTU2OSAxOC4xMzc5IDUuNzU4ODggMTguMDQwM0M1Ljc1NTA1IDE3Ljk0MjggNS43NDU0NSAxNy44NDU2IDUuNzMwMTIgMTcuNzQ5MVpNMTIuMjEwOCAxMy41MzYzTDEyLjIzMzIgMTMuNTc5NUgxMi4yMzY0QzEyLjMgMTMuNzE3NSAxMi40MDIxIDEzLjgzNDEgMTIuNTMwMyAxMy45MTU1QzEyLjY1ODUgMTMuOTk2OCAxMi44MDc0IDE0LjAzOTUgMTIuOTU5MiAxNC4wMzgzQzEzLjExMDkgMTQuMDM3MSAxMy4yNTkyIDEzLjk5MjEgMTMuMzg2MSAxMy45MDg4QzEzLjUxMyAxMy44MjU1IDEzLjYxMzIgMTMuNzA3MiAxMy42NzQ3IDEzLjU2ODNMMTMuNjg5MSAxMy41NDExQzEzLjcyOTIgMTMuNDQ0IDEzLjc0OTggMTMuMzM5OCAxMy43NDk3IDEzLjIzNDdDMTMuNzQ5NiAxMy4xMjk2IDEzLjcyODggMTMuMDI1NSAxMy42ODg1IDEyLjkyODRDMTMuNjQ4MiAxMi44MzEzIDEzLjU4OTIgMTIuNzQzMSAxMy41MTQ4IDEyLjY2ODhDMTMuNDQwNSAxMi41OTQ2IDEzLjM1MjMgMTIuNTM1NyAxMy4yNTUyIDEyLjQ5NTVDMTMuMTU4MSAxMi40NTU0IDEzLjA1NDEgMTIuNDM0OCAxMi45NDkxIDEyLjQzNDlDMTIuODQ0MSAxMi40MzUgMTIuNzQwMSAxMi40NTU5IDEyLjY0MzEgMTIuNDk2MkMxMi41NDYxIDEyLjUzNjUgMTIuNDU4MSAxMi41OTU2IDEyLjM4MzkgMTIuNjdDMTIuMzA5NyAxMi43NDQ0IDEyLjI1MDkgMTIuODMyOCAxMi4yMTA4IDEyLjkyOTlDMTIuMTcwNiAxMy4wMjYgMTIuMTQ5OSAxMy4xMjkgMTIuMTQ5OSAxMy4yMzMxQzEyLjE0OTkgMTMuMzM3MyAxMi4xNzA2IDEzLjQ0MDMgMTIuMjEwOCAxMy41MzYzWk0xNC42MDk3IDE0Ljk3MTVDMTQuMzYzNyAxNS4yMDY2IDE0LjA3MDYgMTUuMzg2NiAxMy43NDk4IDE1LjQ5OTVWMjAuMTk4N0wxNi41Nzg2IDE1Ljk1NzFMMTQuNjA5NyAxNC45NzE1Wk0xNS4zNDggMTMuMjQwM0MxNS4zNDQ4IDEzLjMzOTUgMTUuMzM1MyAxMy40Mzg3IDE1LjMxOTMgMTMuNTM3OUwxNy40NzM2IDE0LjYwODNMMTguMzg0NiAxMy4yNDAzTDE3LjQ3MiAxMS44NzIzTDE1LjMxOTMgMTIuOTQ5MUMxNS4zMzQ2IDEzLjA0NTYgMTUuMzQ0MiAxMy4xNDI4IDE1LjM0OCAxMy4yNDAzWk0xMy43NDk4IDEwLjk5MzlDMTQuMDcwNiAxMS4xMDY5IDE0LjM2MzcgMTEuMjg2OSAxNC42MDk3IDExLjUyMTlMMTYuNTc4NiAxMC41Mjk5TDEzLjc0OTggNi4yODE5NFYxMC45OTM5Wk0xMi4xNTE3IDEwLjk4NzVWNi4yODE5NEw5LjMyMjg1IDEwLjUyOTlMMTEuMjkxOCAxMS41MTU1QzExLjUzNzggMTEuMjgwNSAxMS44MzA5IDExLjEwMDUgMTIuMTUxNyAxMC45OTM5Wk0xMC41NTM1IDEzLjI0MDNDMTAuNTU2NyAxMy4xNDI3IDEwLjU2NjIgMTMuMDQ1MSAxMC41ODIyIDEyLjk0OTFMOC40Mjc4NyAxMS44NzIzTDcuNTE2OSAxMy4yNDAzTDguNDI5NDYgMTQuNjA4M0wxMC41ODIyIDEzLjUzMTVDMTAuNTY2MiAxMy40MzU1IDEwLjU1NjcgMTMuMzM3OSAxMC41NTM1IDEzLjI0MDNaTTEyLjE1MTcgMTUuNDkzMUMxMS44MzA5IDE1LjM4MDIgMTEuNTM3OCAxNS4yMDAyIDExLjI5MTggMTQuOTY1MUw5LjMyMjg1IDE1Ljk1MDdMMTIuMTUxNyAyMC4xOTg3VjE1LjQ5MzFaTTIwLjE3MTQgMTcuNzQ5MUwxOC4wMTg2IDE2LjY3MjNMMTUuMjg0MSAyMC43Nzc5TDIwLjE3MTQgMTguMzMxNUMyMC4xNTU0IDE4LjIzNTUgMjAuMTQ1OCAxOC4xMzc5IDIwLjE0MjYgMTguMDQwM0MyMC4xNDU4IDE3Ljk0MjcgMjAuMTU1NCAxNy44NDUxIDIwLjE3MTQgMTcuNzQ5MVpNMTguOTEyIDE1LjMyOTlMMjAuMjA0OSAxNS45Nzc5TDE5LjM0MzUgMTQuNjgwM0wxOC45MTIgMTUuMzI5OVpNMjAuMjA0OSAxMC41MDI3TDE4LjkxMiAxMS4xNTA3TDE5LjM0MzUgMTEuODAwM0wyMC4yMDQ5IDEwLjUwMjdaTTYuOTg5NDkgMTEuMTQ0M0w1LjY5NjU2IDEwLjUwNDNMNi41NTc5OCAxMS44MDAzTDYuOTg5NDkgMTEuMTQ0M1pNNS42OTY1NiAxNS45Nzc5TDYuOTg5NDkgMTUuMzI5OUw2LjU1Nzk4IDE0LjY4MDNMNS42OTY1NiAxNS45Nzc5WiIgLz4KICAgICAgICAgICAgPC9zdmc+" class="nv-ai-summary__icon" />

## AI-Generated Summary

<img src="data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibnYtYWktc3VtbWFyeV9fdG9nZ2xlLWljb24iIHdpZHRoPSIxNCIgaGVpZ2h0PSI5IiB2aWV3Ym94PSIwIDAgMTQgOSIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiBhcmlhLWhpZGRlbj0idHJ1ZSI+CiAgICAgICAgPHBhdGggZD0iTTEyLjU3NDIgMkw3LjQ0OTIzIDdMMi4zMjQyNSAyIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0ic3F1YXJlIiAvPgogICAgPC9zdmc+" class="nv-ai-summary__toggle-icon" />

<div class="nv-ai-summary__body">

<div class="nv-ai-summary__content">

- The <a href="https://nvda.ws/3TKV7KV" data-wpel-link="external" target="_blank" rel="follow">NVIDIA Grace Hopper Superchip Architecture</a> combines the NVIDIA Grace CPU and NVIDIA Hopper GPU with a coherent 900 GB/s NVLink-C2C interconnect to create the first true heterogeneous accelerated platform for high-performance computing and AI workloads.
- NVLink-C2C hardware memory coherency enables CPU and GPU threads to concurrently access both CPU-resident LPDDR5X memory and GPU-resident HBM3 memory without explicit data movement, providing up to 608 GB of GPU-addressable memory per superchip and up to 150 TB across 256 NVLink-connected superchips.
- The platform supports a unified programming model across ISO C++, ISO Fortran, Python, OpenACC, OpenMP, CUDA C++, and CUDA Fortran through the <a href="https://developer.nvidia.com/hpc-sdk" data-wpel-link="internal" target="_self" rel="follow">NVIDIA HPC SDK</a>, with applications transparently benefiting from NVLink-C2C's higher bandwidth, lower latency, and hardware-accelerated atomic operations.
- The NVIDIA Grace CPU delivers up to 72 Arm Neoverse V2 cores with up to 512 GB of LPDDR5X memory at 546 GB/s bandwidth, while the NVIDIA Hopper GPU provides fourth-generation Tensor Cores, a Transformer Engine, and up to 96 GB of HBM3 memory at 3000 GB/s bandwidth.
- The NVLink Switch System connects up to 256 Grace Hopper Superchips with 115.2 TB/s all-to-all bandwidth, enabling GPU threads to address all system memory using standard load, store, and atomic operations through communication libraries such as MPI, NCCL, and NVSHMEM.

### Next Steps

- Read the <a href="https://nvda.ws/3frjtKQ" data-wpel-link="external" target="_blank" rel="follow">NVIDIA Grace Hopper Architecture whitepaper</a> for detailed performance breakthroughs over PCIe-based accelerated platforms.
- Explore the <a href="https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/" data-wpel-link="internal" target="_self" rel="follow">NVIDIA Hopper Architecture In-Depth</a> technical overview.
- Review the <a href="https://developer.nvidia.com/hpc-sdk" data-wpel-link="internal" target="_self" rel="follow">NVIDIA HPC SDK</a> for accelerated libraries, compilers, and profiling tools supporting the Grace Hopper programming model.

</div>

<div class="nv-ai-summary__disclosure">

Powered by NVIDIA Nemotron. AI-generated content may summarize information incompletely. Verify important information. <a href="https://www.nvidia.com/en-us/agreements/trustworthy-ai/terms/" rel="noreferrer noopener follow" target="_self" data-wpel-link="internal">Learn more</a>

</div>

</div>

<div class="entry-content">

The <a href="https://nvda.ws/3TKV7KV" data-wpel-link="external" target="_blank" rel="follow">NVIDIA Grace Hopper Superchip Architecture</a> is the first true heterogeneous accelerated platform for <a href="https://www.nvidia.com/en-us/high-performance-computing/" data-wpel-link="internal" target="_self" rel="follow"></a> <a href="https://www.nvidia.com/en-us/high-performance-computing/" data-wpel-link="internal" target="_self" rel="follow">high-performance computing</a> (HPC) and <a href="https://www.nvidia.com/en-us/deep-learning-ai/products/solutions/" data-wpel-link="internal" target="_self" rel="follow">AI</a> workloads. It accelerates applications with the strengths of both GPUs and CPUs while providing the simplest and most productive distributed heterogeneous programming model to date. Scientists and engineers can focus on solving the world’s most important problems.

<div class="wp-block-image">

<figure class="aligncenter size-full is-resized">
<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance.png" class="wp-image-57224" style="width:1000px;height:518px" decoding="async" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance.png 1999w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-300x155.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-625x324.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-179x93.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-768x398.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-1536x796.png 1536w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-500x259.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-160x83.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-362x188.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-212x110.png 212w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-1024x531.png 1024w" sizes="(max-width: 1999px) 100vw, 1999px" width="1999" height="1036" alt="Bar chart shows the simulations of the speedups delivered by Grace Hopper over x86 + Hopper platforms for ML Training, Databases, and HPC Applications. For ML Training: up to 4x for Natural Language Processing (NLP), 3.5x for Deep Learning Recommender Models (DLRM), and 1.9x for Graph Neural Networks (GNN). Up to 4.4x for Database Hash Join. For HPC applications, up to 3.6x for ABINIT, 1.75x for OpenFOAM, and 1.3x for multi-node GROMACS." />
<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%201036%22%3E%3C/svg%3E" class="lazyload wp-image-57224" style="width:1000px;height:518px" decoding="async" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance.png" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance.png 1999w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-300x155.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-625x324.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-179x93.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-768x398.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-1536x796.png 1536w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-500x259.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-160x83.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-362x188.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-212x110.png 212w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-1024x531.png 1024w" data-sizes="(max-width: 1999px) 100vw, 1999px" width="1999" height="1036" alt="Bar chart shows the simulations of the speedups delivered by Grace Hopper over x86 + Hopper platforms for ML Training, Databases, and HPC Applications. For ML Training: up to 4x for Natural Language Processing (NLP), 3.5x for Deep Learning Recommender Models (DLRM), and 1.9x for Graph Neural Networks (GNN). Up to 4.4x for Database Hash Join. For HPC applications, up to 3.6x for ABINIT, 1.75x for OpenFOAM, and 1.3x for multi-node GROMACS." />
<figcaption><em>Figure 1. End-user application performance simulations of Grace Hopper vs x86+Hopper (Source:</em> <a href="https://nvda.ws/3frjtKQ" data-wpel-link="external" target="_blank" rel="follow"><em>NVIDIA Grace Hopper Architecture whitepaper</em></a><em>)</em></figcaption>
</figure>

</div>

In this post, you learn all about the Grace Hopper Superchip and highlight the performance breakthroughs that NVIDIA Grace Hopper delivers. For more information about the speedups that Grace Hopper achieves  over the most powerful PCIe-based accelerated platforms using NVIDIA Hopper H100 GPUs, see the <a href="https://nvda.ws/3frjtKQ" data-wpel-link="external" target="_blank" rel="follow">NVIDIA Grace Hopper Superchip Architecture</a> whitepaper.

## Performance and productivity for strong-scaling HPC and giant AI workloads<a href="#performance_and_productivity_for_strong-scaling_hpc_and_giant_ai_workloads" class="heading-anchor-link" aria-label="Scroll to Performance and productivity for strong-scaling HPC and giant AI workloads section"><em></em></a>

The NVIDIA Grace Hopper Superchip architecture brings together the groundbreaking performance of the <a href="https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/" data-wpel-link="internal" target="_self" rel="follow">NVIDIA Hopper GPU</a> with the versatility of the <a href="https://www.nvidia.com/en-us/data-center/grace-cpu/" data-wpel-link="internal" target="_self" rel="follow">NVIDIA Grace CPU</a>, connected with a high bandwidth and memory coherent <a href="https://www.nvidia.com/en-us/data-center/nvlink-c2c/" data-wpel-link="internal" target="_self" rel="follow">NVIDIA NVLink Chip-2-Chip (C2C)</a> interconnect in a single superchip, and support for the new <a href="https://www.nvidia.com/en-us/data-center/nvlink/" data-wpel-link="internal" target="_self" rel="follow">NVIDIA NVLink Switch System</a>.

<div class="wp-block-image">

<figure class="aligncenter size-full is-resized">
<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview.png" class="wp-image-57226" style="width:1000px;height:509px" decoding="async" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview.png 1999w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-300x153.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-625x318.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-179x91.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-768x391.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-1536x782.png 1536w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-500x255.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-160x81.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-362x184.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-216x110.png 216w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-1024x521.png 1024w" sizes="(max-width: 1999px) 100vw, 1999px" width="1999" height="1018" alt="Diagram of the NVIDIA Grace Hopper Superchip showing the LPDDR5X, HBM3, NVLink, and I/O bandwidths as well as memory capacities. Hopper has up to 96 GB HBM3 at up to 3000 GB/s bandwidth. Grace has up to 512 GB LPDDR5X at up to 546 GB/s bandwidth. Grace and Hopper are connected with NVLink C2C at up to 900 GB/s bandwidth. The Grace Hopper Superchip has up to 64 PCIe Gen 5 lanes delivering up to 512 GB/s bandwidth and up to 18x NVLink for lanes delivering up to 900 GB/s to the NVLink Switch network." />
<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%201018%22%3E%3C/svg%3E" class="lazyload wp-image-57226" style="width:1000px;height:509px" decoding="async" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview.png" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview.png 1999w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-300x153.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-625x318.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-179x91.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-768x391.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-1536x782.png 1536w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-500x255.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-160x81.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-362x184.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-216x110.png 216w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-overview-1024x521.png 1024w" data-sizes="(max-width: 1999px) 100vw, 1999px" width="1999" height="1018" alt="Diagram of the NVIDIA Grace Hopper Superchip showing the LPDDR5X, HBM3, NVLink, and I/O bandwidths as well as memory capacities. Hopper has up to 96 GB HBM3 at up to 3000 GB/s bandwidth. Grace has up to 512 GB LPDDR5X at up to 546 GB/s bandwidth. Grace and Hopper are connected with NVLink C2C at up to 900 GB/s bandwidth. The Grace Hopper Superchip has up to 64 PCIe Gen 5 lanes delivering up to 512 GB/s bandwidth and up to 18x NVLink for lanes delivering up to 900 GB/s to the NVLink Switch network." />
<figcaption><em>Figure 2. NVIDIA Grace Hopper Superchip logical overview</em></figcaption>
</figure>

</div>

NVIDIA NVLink-C2C is an NVIDIA memory coherent, high-bandwidth, and low-latency superchip interconnect. It is the heart of the Grace Hopper Superchip and delivers up to 900 GB/s total bandwidth. This is 7x higher bandwidth than x16 PCIe Gen5 lanes commonly used in accelerated systems.

NVLink-C2C memory coherency increases developer productivity and performance and enables GPUs to access large amounts of memory.CPU and GPU threads can now concurrently and transparently access both CPU– and GPU-resident memory, enabling you to focus on algorithms instead of explicit memory management.

Memory coherency enables  you to transfer only the data you need, and not migrate entire pages to and from the GPU. It also enables lightweight synchronization primitives across GPU and CPU threads by enabling native atomic operations from both the CPU and GPU. NVLink-C2C with Address Translation Services (ATS) leverages the NVIDIA Hopper Direct Memory Access (DMA) copy engines for accelerating bulk transfers of pageable memory across host and device.

NVLink-C2C enables applications to oversubscribe the GPU’s memory and directly utilize NVIDIA Grace CPU’s memory at high bandwidth. With up to 512 GB of LPDDR5X CPU memory per Grace Hopper Superchip, the GPU has direct high-bandwidth access to 4x more memory than what is available with HBM. Combined with the NVIDIA NVLink Switch System, all GPU threads running on up to 256 NVLink-connected GPUs can now access up to 150 TB of memory at high bandwidth. Fourth-generation NVLink enables accessing peer memory using direct loads, stores, and atomic operations, enabling accelerated applications to solve larger problems more easily than ever.

Together with NVIDIA networking technologies, Grace Hopper Superchips provide the recipe for the next generation of HPC supercomputers and AI factories. Customers can take on larger datasets, more complex models, and new workloads, solving them more quickly than before.

The main innovations of the NVIDIA Grace Hopper Superchip are as follows:

- NVIDIA Grace CPU:
  - Up to 72x Arm Neoverse V2 cores with Armv9.0-A ISA and 4×128-bit SIMD units per core.
  - Up to 117 MB of L3 Cache.
  - Up to 512 GB of LPDDR5X memory delivering up to 546 GB/s of memory bandwidth.
  - Up to 64x PCIe Gen5 lanes.
  - NVIDIA Scalable Coherency Fabric (SCF) mesh and distributed cache with up to 3.2 TB/s memory bandwidth.
  - High developer productivity with a single CPU NUMA node.
- NVIDIA Hopper GPU:
  - Up to 144 SMs with fourth-generation Tensor Cores, Transformer Engine, DPX, and 3x higher FP32 and FP64 throughout compared to the NVIDIA A100 GPU.
  - Up to 96 GB of HBM3 memory delivering up to 3000 GB/s.
  - 60 MB L2 Cache.
  - NVLink 4 and PCIe 5.
- NVIDIA NVLink-C2C:
  - Hardware-coherent interconnect between the Grace CPU and Hopper GPU.
  - Up to 900 GB/s total bandwidth, 450 GB/s/dir.
  - The Extended GPU Memory feature enables the Hopper GPU to address all CPU memory as GPU memory. Each Hopper GPU can address up to 608 GB of memory within a superchip.
- NVIDIA NVLink Switch System:
  - Connects up to 256x NVIDIA Grace Hopper Superchips using NVLink 4.
  - Each NVLink-connected Hopper GPU can address all HBM3 and LPDDR5X memory of all superchips in the network, for up to 150 TB of GPU addressable memory.

## Programming model for performance, portability, and productivity<a href="#programming_model_for_performance_portability_and_productivity" class="heading-anchor-link" aria-label="Scroll to Programming model for performance, portability, and productivity section"><em></em></a>

Traditional heterogeneous platforms with PCIe-connected accelerators require users to follow a complex programming model that involves manually managing device memory allocations and data transfer to and from the host.

The NVIDIA Grace Hopper Superchip platform is heterogeneous and easy to program, and NVIDIA is committed to making it accessible to all developers and applications, independent of the programming language of choice.

Both the Grace Hopper Superchip and the platform are built to enable you to pick the right language for the task at hand, and the <a href="https://developer.nvidia.com/cuda-llvm-compiler" data-wpel-link="internal" target="_self" rel="follow">NVIDIA CUDA LLVM Compiler</a> APIs enable you to bring your preferred programming language to the CUDA platform with the same level of code-generation quality and optimizations as NVIDIA compilers and tools.

The languages provided by NVIDIA for the CUDA platform (Figure 3) include accelerated standard languages like ISO C++, ISO Fortran, and Python. The platform also supports directive-based programming models like OpenACC, OpenMP, CUDA C++, and CUDA Fortran. The <a href="https://developer.nvidia.com/hpc-sdk" data-wpel-link="internal" target="_self" rel="follow">NVIDIA HPC SDK</a> supports all these approaches, along with a rich set of accelerated libraries and tools for profiling and debugging.

<div class="wp-block-image">

<figure class="aligncenter size-full is-resized">
<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models.png" class="wp-image-57227" style="width:1000px;height:329px" decoding="async" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models.png 1999w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-300x99.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-625x205.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-179x59.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-768x252.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-1536x505.png 1536w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-500x164.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-160x53.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-362x119.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-335x110.png 335w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-1024x337.png 1024w" sizes="(max-width: 1999px) 100vw, 1999px" width="1999" height="657" alt="The three pillars of the NVIDIA Grace Hopper Superchip programming models are built on top of accelerated libraries, frameworks, and SDKs. The first pillar is Accelerated Standard Languages and includes programming languages like ISO C++, ISO Fortran, and Python. The second pillar is Incremental Portable Optimization and includes OpenMP and OpenACC directives. Finally, maximum performance can be obtained by specializing applications for the CUDA platform using CUDA C++ or CUDA Fortran." />
<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%20657%22%3E%3C/svg%3E" class="lazyload wp-image-57227" style="width:1000px;height:329px" decoding="async" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models.png" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models.png 1999w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-300x99.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-625x205.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-179x59.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-768x252.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-1536x505.png 1536w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-500x164.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-160x53.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-362x119.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-335x110.png 335w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-superchip-programming-models-1024x337.png 1024w" data-sizes="(max-width: 1999px) 100vw, 1999px" width="1999" height="657" alt="The three pillars of the NVIDIA Grace Hopper Superchip programming models are built on top of accelerated libraries, frameworks, and SDKs. The first pillar is Accelerated Standard Languages and includes programming languages like ISO C++, ISO Fortran, and Python. The second pillar is Incremental Portable Optimization and includes OpenMP and OpenACC directives. Finally, maximum performance can be obtained by specializing applications for the CUDA platform using CUDA C++ or CUDA Fortran." />
<figcaption><em>Figure 3.</em> <strong><em></em></strong> <em>NVIDIA Grace Hopper Superchip programming models</em></figcaption>
</figure>

</div>

NVIDIA is a member of the ISO C++ and ISO Fortran programming-language communities, which have enabled ISO C++ and ISO Fortran standard-compliant applications to run on both NVIDIA CPUs and NVIDIA GPUs without any language extensions. For more information about running ISO-conforming applications on GPUs, see <a href="https://developer.nvidia.com/blog/multi-gpu-programming-with-standard-parallel-c-part-1/" data-wpel-link="internal" target="_self" rel="follow">Multi-GPU Programming with Standard Parallel C++</a> and <a href="https://developer.nvidia.com/blog/using-fortran-standard-parallel-programming-for-gpu-acceleration/" data-wpel-link="internal" target="_self" rel="follow">Using Fortran Standard Parallel Programming For GPU Acceleration</a>.

This technology relies heavily on the hardware-accelerated memory coherency provided by NVIDIA NVLink-C2C and NVIDIA Unified Virtual Memory. As shown in Figure 4, in traditional PCIe-connected x86+Hopper systems without ATS, the CPU and the GPU have independent per-process page tables, and system-allocated memory is not directly accessible from the GPU. When a program allocates memory with the system allocator but the page entry is not available in the GPU’s page table, then accessing the memory from a GPU thread fails.

<div class="wp-block-image">

<figure class="aligncenter size-full is-resized">
<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables.jpg" class="wp-image-57228" style="width:721px;height:330px" decoding="async" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables.jpg 1441w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-300x137.jpg 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-625x286.jpg 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-179x82.jpg 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-768x351.jpg 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-500x229.jpg 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-160x73.jpg 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-362x166.jpg 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-241x110.jpg 241w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-1024x468.jpg 1024w" sizes="(max-width: 1441px) 100vw, 1441px" width="1441" height="659" alt="Diagram shows that, on noncoherent platforms with disjoint page tables, when CPU or GPU threads attempt to access a page that is not available in their own separate page tables, the access faults." />
<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201441%20659%22%3E%3C/svg%3E" class="lazyload wp-image-57228" style="width:721px;height:330px" decoding="async" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables.jpg" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables.jpg 1441w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-300x137.jpg 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-625x286.jpg 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-179x82.jpg 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-768x351.jpg 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-500x229.jpg 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-160x73.jpg 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-362x166.jpg 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-241x110.jpg 241w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-system-disjoint-page-tables-1024x468.jpg 1024w" data-sizes="(max-width: 1441px) 100vw, 1441px" width="1441" height="659" alt="Diagram shows that, on noncoherent platforms with disjoint page tables, when CPU or GPU threads attempt to access a page that is not available in their own separate page tables, the access faults." />
<figcaption><em>Figure 4. NVIDIA Hopper System with disjoint page tables</em></figcaption>
</figure>

</div>

In NVIDIA Grace Hopper Superchip-based systems, ATS enables the CPU and GPU to share a single per-process page table, enabling all CPU and GPU threads to access all system-allocated memory, which can reside on physical CPU or GPU memory. The CPU heap, CPU thread stack, global variables, memory-mapped files, and interprocess memory are accessible to all CPU and GPU threads.

<div class="wp-block-image">

<figure class="aligncenter size-full is-resized">
<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip.png" class="wp-image-57230" style="width:718px;height:336px" decoding="async" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip.png 1435w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-300x140.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-625x292.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-179x84.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-768x359.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-500x234.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-160x75.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-362x169.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-235x110.png 235w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-1024x479.png 1024w" sizes="(max-width: 1435px) 100vw, 1435px" width="1435" height="671" alt="Diagram shows that, on NVIDIA Grace Hopper Superchip systems with ATS, the CPU and GPU can both access the system page table. This enables GPU and CPU threads to access all-system allocated memory, independently of where it resides." />
<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201435%20671%22%3E%3C/svg%3E" class="lazyload wp-image-57230" style="width:718px;height:336px" decoding="async" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip.png" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip.png 1435w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-300x140.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-625x292.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-179x84.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-768x359.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-500x234.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-160x75.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-362x169.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-235x110.png 235w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/address-translation-services-grace-hopper-superchip-1024x479.png 1024w" data-sizes="(max-width: 1435px) 100vw, 1435px" width="1435" height="671" alt="Diagram shows that, on NVIDIA Grace Hopper Superchip systems with ATS, the CPU and GPU can both access the system page table. This enables GPU and CPU threads to access all-system allocated memory, independently of where it resides." />
<figcaption><em>Figure 5. Address Translation Services in an NVIDIA Grace Hopper Superchip system</em></figcaption>
</figure>

</div>

NVIDIA NVLink-C2C hardware-coherency enables the Grace CPU to cache GPU memory at cache-line granularity and for the GPU and CPU to access each other’s memory without page-migrations.

NVLink-C2C also accelerates all atomic operations supported by the CPU and GPU on system-allocated memory. <a href="https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/advanced-kernel-programming.html#scoped-atomics" data-wpel-link="internal" target="_self" rel="follow">Scoped atomic operations</a> are fully supported and enable fine-grained and scalable synchronization across all threads in the system.

The runtime backs system-allocated memory with physical memory on first touch, either on LPDDR5X or HBM3, depending on whether a CPU or a GPU thread accesses it first. From an OS perspective, the Grace CPU and Hopper GPU are just two separate NUMA nodes. System-allocated memory is migratable so the runtime can change its physical memory backing to improve application performance or deal with memory pressure.

For PCIe-based platforms such as x86 or Arm, you can use the same Unified Memory programming model as the NVIDIA Grace Hopper model. That will eventually be possible through the <a href="https://on-demand.gputechconf.com/gtc/2017/presentation/s7764_john-hubbardgpus-using-hmm-blur-the-lines-between-cpu-and-gpu.pdf" data-wpel-link="external" target="_blank" rel="follow">Heterogeneous Memory Management (HMM) feature</a>, which is a combination of Linux kernel features and NVIDIA driver features that use software to emulate memory coherence between CPUs and GPUs.

On NVIDIA Grace Hopper, these applications transparently benefit from the higher-bandwidth, lower-latency, higher atomic throughput, and hardware acceleration for memory coherency provided by NVLink-C2C, without any software changes.

## Superchip architectural features<a href="#superchip_architectural_features" class="heading-anchor-link" aria-label="Scroll to Superchip architectural features section"><em></em></a>

Here’s a look at the main innovations of the NVIDIA Grace Hopper architecture:

- NVIDIA Grace CPU
- NVIDIA Hopper GPU
- NVLink-C2C
- NVLink Switch System
- Extended GPU memory

### NVIDIA Grace CPU<a href="#nvidia_grace_cpu" class="heading-anchor-link" aria-label="Scroll to NVIDIA Grace CPU section"><em></em></a>

As the parallel compute capabilities of GPUs continue to triple every generation, a fast and efficient CPU is critical to prevent the serial and CPU-only fractions of modern workloads from dominating performance.

NVIDIA Grace CPU is the <a href="https://www.nvidia.com/en-us/data-center/" data-wpel-link="internal" target="_self" rel="follow">first NVIDIA data center</a> <a href="https://www.nvidia.com/en-us/data-center/" data-wpel-link="internal" target="_self" rel="follow">CPU</a>, and it is <a href="https://developer.nvidia.com/blog/inside-nvidia-grace-cpu-nvidia-amps-up-superchip-engineering-for-hpc-and-ai/" data-wpel-link="internal" target="_self" rel="follow">built from the ground up to create HPC and AI</a> <a href="https://developer.nvidia.com/blog/inside-nvidia-grace-cpu-nvidia-amps-up-superchip-engineering-for-hpc-and-ai/" data-wpel-link="internal" target="_self" rel="follow">superchips</a>. Grace provides up to 72 Arm Neoverse V2 CPU cores with the <a href="https://www.arm.com/company/news/2021/03/arms-answer-to-the-future-of-ai-armv9-architecture" data-wpel-link="external" target="_blank" rel="follow">Armv9.0-A ISA</a>, and 4×128-bit wide SIMD units per core with support for Arm’s <a href="https://developer.arm.com/documentation/102340/0001/Introducing-SVE2" data-wpel-link="external" target="_blank" rel="follow">Scalable Vector Extensions 2</a> <a href="https://developer.arm.com/documentation/102340/0001/Introducing-SVE2" data-wpel-link="external" target="_blank" rel="follow">(SVE2)</a> SIMD instruction set.

NVIDIA Grace delivers leading per-thread performance, while providing higher energy efficiency than traditional CPUs. The 72 CPU cores deliver up to a 370 (estimated) score on <a href="http://spec.org/cpu2017/" data-wpel-link="external" target="_blank" rel="follow">SPECrate 2017_int_base</a>, ensuring high-performance to satisfy the demands of both HPC and AI heterogeneous workloads.

<div class="wp-block-image">

<figure class="aligncenter size-full is-resized">
<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu.png" class="wp-image-57231" style="width:1000px;height:482px" decoding="async" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu.png 1999w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-300x145.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-625x301.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-179x86.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-768x370.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-1536x740.png 1536w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-500x241.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-160x77.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-362x174.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-228x110.png 228w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-1024x493.png 1024w" sizes="(max-width: 1999px) 100vw, 1999px" width="1999" height="963" alt="Bar chart hows simulations of the speedups and energy savings delivered by the Grace CPUs in NVIDIA Grace Hopper Superchips over AMD Milan 7763. OpenFOAM HPC Motorbike Large benchmark is 2.5x faster and uses 3.5x less energy. NEMO GYRE_PISCES, scaling factor nn_GYRE=25, benchmark is 1.6x faster and uses 2.2x less energy. BWA Whole Human Genome (HG002 30x) benchmark is 1.5x faster and uses 2.0x less energy." />
<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%20963%22%3E%3C/svg%3E" class="lazyload wp-image-57231" style="width:1000px;height:482px" decoding="async" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu.png" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu.png 1999w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-300x145.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-625x301.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-179x86.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-768x370.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-1536x740.png 1536w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-500x241.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-160x77.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-362x174.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-228x110.png 228w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/end-user-app-performance-grace-cpu-1024x493.png 1024w" data-sizes="(max-width: 1999px) 100vw, 1999px" width="1999" height="963" alt="Bar chart hows simulations of the speedups and energy savings delivered by the Grace CPUs in NVIDIA Grace Hopper Superchips over AMD Milan 7763. OpenFOAM HPC Motorbike Large benchmark is 2.5x faster and uses 3.5x less energy. NEMO GYRE_PISCES, scaling factor nn_GYRE=25, benchmark is 1.6x faster and uses 2.2x less energy. BWA Whole Human Genome (HG002 30x) benchmark is 1.5x faster and uses 2.0x less energy." />
<figcaption><em>Figure 6. End-user application performance and energy saving simulations of the NVIDIA Grace CPU in the Grace Hopper Superchip vs AMD Milan 7763 shows that the Grace CPU is up to 2.5x faster while using 4x less energy</em></figcaption>
</figure>

</div>

Modern GPU workloads in machine learning and data science need access to huge amounts of memory. Typically, these workloads would have to use multiple GPUs to store the dataset in HBM memory.

The NVIDIA Grace CPU provides up to 512 GB of LPDDR5X memory, which delivers the optimal balance between memory capacity, energy efficiency, and performance. It supplies up to 546 GB/s of LPDDR5X memory bandwidth, which NVLink-C2C makes accessible to the GPU at 900 GB/s total bandwidth.

A single NVIDIA Grace Hopper Superchip provides the Hopper GPU with a total of 608 GB of fast-accessible memory, almost the total amount of slow memory available in a DGX-A100-80; an eight-GPU system of the previous generation.

This is made possible by the NVIDIA SCF shown in Figure 7, a mesh fabric and distributed cache that provides up to 3.2 TB/s of total bisection bandwidth to realize the full performance of CPU cores, memory, system I/Os, and NVLink-C2C. The CPU cores and SCF Cache partitions (SCCs) are distributed throughout the mesh, while Cache Switch Nodes (CSNs) route data through the fabric and serve as interfaces between the CPU cores, cache memory, and the rest of the system.

<div class="wp-block-image">

<figure class="aligncenter size-full is-resized wp-lightbox-container" data-wp-context="{&quot;imageId&quot;:&quot;6aa397b80dbfa&quot;}" data-wp-interactive="core/image" data-wp-key="6aa397b80dbfa">
<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview.png" class="wp-image-57232" style="width:797px;height:658px" decoding="async" data-wp-class--hide="state.isContentHidden" data-wp-class--show="state.isContentVisible" data-wp-init="callbacks.setButtonStyles" data-wp-on--click="actions.showLightbox" data-wp-on--load="callbacks.setButtonStyles" data-wp-on--pointerdown="actions.preloadImage" data-wp-on--pointerenter="actions.preloadImageWithDelay" data-wp-on--pointerleave="actions.cancelPreload" data-wp-on-window--resize="callbacks.setButtonStyles" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview.png 1062w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-300x248.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-625x516.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-139x115.png 139w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-768x634.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-363x300.png 363w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-109x90.png 109w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-362x299.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-133x110.png 133w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-1024x846.png 1024w" sizes="(max-width: 1062px) 100vw, 1062px" width="1062" height="877" alt="Diagram shows how two cores and two groups of SCC are connected to the CSNs that route data traffic to LPDDR5X, PCIe, and NVLink." />
<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201062%20877%22%3E%3C/svg%3E" class="lazyload wp-image-57232" style="width:797px;height:658px" decoding="async" data-wp-class--hide="state.isContentHidden" data-wp-class--show="state.isContentVisible" data-wp-init="callbacks.setButtonStyles" data-wp-on--click="actions.showLightbox" data-wp-on--load="callbacks.setButtonStyles" data-wp-on--pointerdown="actions.preloadImage" data-wp-on--pointerenter="actions.preloadImageWithDelay" data-wp-on--pointerleave="actions.cancelPreload" data-wp-on-window--resize="callbacks.setButtonStyles" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview.png" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview.png 1062w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-300x248.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-625x516.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-139x115.png 139w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-768x634.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-363x300.png 363w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-109x90.png 109w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-362x299.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-133x110.png 133w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/scf-overview-1024x846.png 1024w" data-sizes="(max-width: 1062px) 100vw, 1062px" width="1062" height="877" alt="Diagram shows how two cores and two groups of SCC are connected to the CSNs that route data traffic to LPDDR5X, PCIe, and NVLink." />
<img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDEyIDEyIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0yIDBhMiAyIDAgMCAwLTIgMnYyaDEuNVYyYS41LjUgMCAwIDEgLjUtLjVoMlYwSDJabTIgMTAuNUgyYS41LjUgMCAwIDEtLjUtLjVWOEgwdjJhMiAyIDAgMCAwIDIgMmgydi0xLjVaTTggMTJ2LTEuNWgyYS41LjUgMCAwIDAgLjUtLjVWOEgxMnYyYTIgMiAwIDAgMS0yIDJIOFptMi0xMmEyIDIgMCAwIDEgMiAydjJoLTEuNVYyYS41LjUgMCAwIDAtLjUtLjVIOFYwaDJaIiAvPgogICAgICAgICAgICA8L3N2Zz4=" />
<figcaption><em>Figure 7. SCF logical overview</em></figcaption>
</figure>

</div>

### NVIDIA Hopper GPU<a href="#nvidia_hopper_gpu" class="heading-anchor-link" aria-label="Scroll to NVIDIA Hopper GPU section"><em></em></a>

The <a href="https://resources.nvidia.com/en-us-tensor-core/gtc22-whitepaper-hopper" data-wpel-link="internal" target="_self" rel="follow">NVIDIA Hopper GPU</a> is the ninth-generation NVIDIA data center GPU. It is designed to deliver orders-of-magnitude improvements for large-scale AI and HPC applications compared to previous NVIDIA Ampere GPU generations. The Hopper GPU also features multiple innovations:

- New fourth-generation Tensor Cores perform faster matrix computations than ever before on an even broader array of AI and HPC tasks.
- A new transformer engine enables H100 to deliver up to 9x faster AI training and up to 30x faster AI inference speedups on large language models compared to the prior generation NVIDIA A100 GPU.
- Improved features for spatial and temporal data locality and asynchronous execution enable applications to always keep all units busy and maximize power efficiency.
- Secure <a href="https://www.nvidia.com/en-us/technologies/multi-instance-gpu/" data-wpel-link="internal" target="_self" rel="follow">Multi-Instance GPU (MIG</a><a href="https://www.nvidia.com/en-us/technologies/multi-instance-gpu/" data-wpel-link="internal" target="_self" rel="follow">)</a> partitions the GPU into isolated, right-sized instances to maximize quality of service (QoS) for smaller workloads.

<div class="wp-block-image">

<figure class="aligncenter size-full is-resized">
<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai.png" class="wp-image-57233" style="width:1000px;height:434px" decoding="async" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai.png 1999w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-300x130.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-625x271.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-179x78.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-768x333.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-1536x667.png 1536w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-500x217.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-160x69.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-362x157.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-253x110.png 253w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-1024x445.png 1024w" sizes="(max-width: 1999px) 100vw, 1999px" width="1999" height="868" alt="First chart shows performance improvements on HPC applications (climate modeling, genomics, Lattice QCD, or 3D FFT). Second chart shows AI inference latency improvements for Megatron Turing NLG 530B. Third chart shows AI training covering Mask R-CNN, GPT-3 with 16B and 175B parameters, DLRM with 14-TB Embedding tables, and MoE Switch-XXL with 395B parameters." />
<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%20868%22%3E%3C/svg%3E" class="lazyload wp-image-57233" style="width:1000px;height:434px" decoding="async" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai.png" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai.png 1999w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-300x130.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-625x271.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-179x78.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-768x333.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-1536x667.png 1536w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-500x217.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-160x69.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-362x157.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-253x110.png 253w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-next-gen-ai-1024x445.png 1024w" data-sizes="(max-width: 1999px) 100vw, 1999px" width="1999" height="868" alt="First chart shows performance improvements on HPC applications (climate modeling, genomics, Lattice QCD, or 3D FFT). Second chart shows AI inference latency improvements for Megatron Turing NLG 530B. Third chart shows AI training covering Mask R-CNN, GPT-3 with 16B and 175B parameters, DLRM with 14-TB Embedding tables, and MoE Switch-XXL with 395B parameters." />
<figcaption><em>Figure 8. NVIDIA Hopper GPU enables next-generation AI and HPC breakthroughs</em></figcaption>
</figure>

</div>

<span id="_msocom_1"></span>NVIDIA Hopper is the first truly asynchronous GPU. Its Tensor Memory Accelerator (TMA) and asynchronous transaction barrier enable threads to overlap and pipeline independent data movement and data processing, enabling applications to fully utilize all units.

New spatial and temporal locality features like thread block clusters, distributed shared memory, and thread block reconfiguration provide applications with fast access to larger amounts of shared memory and tools. This enables applications to better reuse data while it’s on-chip, further improving application performance.

<div class="wp-block-image">

<figure class="aligncenter size-full is-resized">
<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution.png" class="wp-image-57235" style="width:1000px;height:362px" decoding="async" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution.png 1999w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-300x109.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-625x226.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-179x65.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-768x278.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-1536x556.png 1536w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-500x181.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-160x58.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-362x131.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-304x110.png 304w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-1024x370.png 1024w" sizes="(max-width: 1999px) 100vw, 1999px" width="1999" height="723" alt="On the left, the diagram shows a pipeline that overlaps independent data processing and data movement between producer and consumer threads, which enables keeping all units fully utilized. On the right, the bar chart shows the impact of leveraging Hopper’s new spatial and temporal locality features on application performance." />
<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%20723%22%3E%3C/svg%3E" class="lazyload wp-image-57235" style="width:1000px;height:362px" decoding="async" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution.png" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution.png 1999w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-300x109.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-625x226.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-179x65.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-768x278.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-1536x556.png 1536w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-500x181.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-160x58.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-362x131.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-304x110.png 304w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hopper-gpu-async-execution-1024x370.png 1024w" data-sizes="(max-width: 1999px) 100vw, 1999px" width="1999" height="723" alt="On the left, the diagram shows a pipeline that overlaps independent data processing and data movement between producer and consumer threads, which enables keeping all units fully utilized. On the right, the bar chart shows the impact of leveraging Hopper’s new spatial and temporal locality features on application performance." />
<figcaption><em>Figure 9. NVIDIA Hopper GPU asynchronous execution enables overlapping independent data-movement with computation (left). New spatial and temporal locality features improve application performance (right).</em></figcaption>
</figure>

</div>

For more information, see <a href="https://resources.nvidia.com/en-us-tensor-core" data-wpel-link="internal" target="_self" rel="follow">NVIDIA H100 Tensor Core Architecture Overview</a> and <a href="https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/" data-wpel-link="internal" target="_self" rel="follow">NVIDIA Hopper Architecture In-Depth</a>.

### NVLink-C2C: A high-bandwidth, chip-to-chip interconnect for superchips<a href="#nvlink-c2c_a_high-bandwidth_chip-to-chip_interconnect_for_superchips" class="heading-anchor-link" aria-label="Scroll to NVLink-C2C: A high-bandwidth, chip-to-chip interconnect for superchips section"><em></em></a>

NVIDIA Grace Hopper fuses an NVIDIA Grace CPU and NVIDIA Hopper GPU into a single superchip through the NVIDIA NVLink-C2C, a 900 GB/s chip-to-chip coherent interconnect that enables programming the Grace Hopper Superchip with a unified programming model.

The NVLink Chip-2-Chip (C2C) interconnect provides a high-bandwidth direct connection between a Grace CPU and a Hopper GPU to create the Grace Hopper Superchip, which is designed for drop-in acceleration of AI and HPC applications.

With 900 GB/s of bidirectional bandwidth, NVLink-C2C provides 7x the bandwidth of x16 PCIe Gen links at lower latency. NVLink-C2C also only uses 1.3 picojoules per bit transferred, which is greater than 5x more energy-efficient than PCIe Gen 5.

Furthermore, NVLink-C2C is a coherent memory interconnect with native hardware support for system-wide atomic operations. This improves the performance of memory accesses to non-local memory, such as CPU and GPU threads accessing memory resident in the other device. Hardware coherency also improves the performance of synchronization primitives, reducing the time the GPU or CPU wait on each other and increasing total system utilization.

Finally, hardware coherency also simplifies the development of heterogeneous computing applications using popular programming languages and frameworks. For more information, see the NVIDIA Grace Hopper Programming Model section.

### NVLink Switch System<a href="#nvlink_switch_system" class="heading-anchor-link" aria-label="Scroll to NVLink Switch System section"><em></em></a>

The NVIDIA NVLink Switch System combines fourth-generation NVIDIA NVLink technology with the new third-generation NVIDIA NVSwitch. A single level of the NVSwitch connects up to eight Grace Hopper Superchips, and a second level in a fat-tree topology enables networking up to 256 Grace Hopper Superchips with NVLink. A Grace Hopper Superchip pair exchanges data at up to 900 GB/s.

With up to 256 Grace Hopper Superchips, the network delivers up to 115.2 TB/s all-to-all bandwidth. This is 9x the all-to-all bandwidth of the <a href="https://www.nvidia.com/en-us/networking/products/infiniband/" data-wpel-link="internal" target="_self" rel="follow">NVIDIA InfiniBand</a> NDR400.

<div class="wp-block-image">

<figure class="aligncenter size-full is-resized">
<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch.png" class="wp-image-57236" style="width:678px;height:338px" decoding="async" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch.png 1356w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-300x149.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-625x311.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-179x89.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-768x382.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-500x249.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-160x80.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-362x180.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-221x110.png 221w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-1024x510.png 1024w" sizes="(max-width: 1356px) 100vw, 1356px" width="1356" height="675" alt="Logical overview of the NVLink 4 NVSwitch chip including the PHY Lanes, PORT logic and SHARP accelerators, and cross-bar." />
<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201356%20675%22%3E%3C/svg%3E" class="lazyload wp-image-57236" style="width:678px;height:338px" decoding="async" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch.png" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch.png 1356w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-300x149.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-625x311.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-179x89.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-768x382.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-500x249.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-160x80.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-362x180.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-221x110.png 221w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/nvlink-4-nvswitch-1024x510.png 1024w" data-sizes="(max-width: 1356px) 100vw, 1356px" width="1356" height="675" alt="Logical overview of the NVLink 4 NVSwitch chip including the PHY Lanes, PORT logic and SHARP accelerators, and cross-bar." />
<figcaption><em>Figure 10. Logical overview of NVIDIA NVLink 4 NVSwitch</em></figcaption>
</figure>

</div>

The fourth-generation NVIDIA NVLink technology enables GPU threads to address up to 150 TB of memory provided by all superchips in the NVLink network using normal memory operations, atomic operations, and bulk transfers. Communication libraries like <a href="https://developer.nvidia.com/networking/hpc-x" data-wpel-link="internal" target="_self" rel="follow">MPI</a>, <a href="https://developer.nvidia.com/nccl" data-wpel-link="internal" target="_self" rel="follow">NCCL</a>, or <a href="https://developer.nvidia.com/nvshmem" data-wpel-link="internal" target="_self" rel="follow">NVSHMEM</a> transparently leverage the NVLink Switch System when available.

### Extended GPU memory<a href="#extended_gpu_memory" class="heading-anchor-link" aria-label="Scroll to Extended GPU memory section"><em></em></a>

The NVIDIA Grace Hopper Superchip is designed to accelerate applications with exceptionally large memory footprints, larger than the capacity of the HBM3 and LPDDR5X memory of a single superchip. For more information, see the NVIDIA Grace Hopper Accelerated Applications section.

The Extended GPU Memory (EGM) feature over the high-bandwidth NVLink-C2C enables GPUs to access all the system memory efficiently. EGM provides up to 150 TBs of system memory in a multi-node NVSwitch-connected system. With EGM, physical memory can be allocated to be accessible from any GPU thread in the multi-node system. All GPUs can access EGM at the minimum of GPU-GPU NVLink or NVLink-C2C speed.

Memory accesses within a Grace Hopper Superchip configuration go through the local high-bandwidth NVLink-C2C at 900 GB/s total. Remote memory accesses are performed through GPU NVLink and, depending on the memory being accessed, also NVLink-C2C (Figure 11). With EGM, GPU threads can now access all memory resources available over the NVSwitch fabric, both LPDDR5X and HBM3, at 450 GB/s.

<div class="wp-block-image">

<figure class="aligncenter size-full is-resized">
<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip.png" class="wp-image-57237" style="width:1000px;height:281px" decoding="async" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip.png 1999w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-300x84.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-625x176.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-179x50.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-768x216.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-1536x432.png 1536w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-500x141.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-160x45.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-362x102.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-391x110.png 391w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-1024x288.png 1024w" sizes="(max-width: 1999px) 100vw, 1999px" width="1999" height="562" alt="Diagram shows the access paths taken by memory accesses from a Hopper GPU to its local LPPDR5X (path via C2C), to a peer GPU HBM3 (path via NVLink), and to a peer CPU LPDDR5X (path via NVLink to peer GPU, then C2C to LPDDR5X)." />
<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201999%20562%22%3E%3C/svg%3E" class="lazyload wp-image-57237" style="width:1000px;height:281px" decoding="async" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip.png" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip.png 1999w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-300x84.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-625x176.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-179x50.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-768x216.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-1536x432.png 1536w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-500x141.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-160x45.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-362x102.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-391x110.png 391w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/memory-access-grace-hopper-superchip-1024x288.png 1024w" data-sizes="(max-width: 1999px) 100vw, 1999px" width="1999" height="562" alt="Diagram shows the access paths taken by memory accesses from a Hopper GPU to its local LPPDR5X (path via C2C), to a peer GPU HBM3 (path via NVLink), and to a peer CPU LPDDR5X (path via NVLink to peer GPU, then C2C to LPDDR5X)." />
<figcaption><em>Figure 11. Memory accesses across NVLink-connected Grace Hopper Superchips</em></figcaption>
</figure>

</div>

## NVIDIA HGX Grace Hopper<a href="#nvidia_hgx_grace_hopper" class="heading-anchor-link" aria-label="Scroll to NVIDIA HGX Grace Hopper section"><em></em></a>

NVIDIA HGX Grace Hopper has a single Grace Hopper Superchip per node, paired with BlueField-3 NICs or OEM-Defined I/O and optionally an NVLink Switch System. It can be air– or liquid-cooled and has up to 1,000W TDP.

<div class="wp-block-image">

<figure class="aligncenter size-full is-resized">
<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband.jpg" class="wp-image-57238" style="width:276px;height:259px" decoding="async" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband.jpg 551w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-300x281.jpg 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-123x115.jpg 123w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-320x300.jpg 320w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-96x90.jpg 96w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-362x340.jpg 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-117x110.jpg 117w" sizes="(max-width: 551px) 100vw, 551px" width="551" height="517" alt="3D Render of an NVIDIA HGX Grace Hopper with InfiniBand system." />
<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20551%20517%22%3E%3C/svg%3E" class="lazyload wp-image-57238" style="width:276px;height:259px" decoding="async" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband.jpg" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband.jpg 551w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-300x281.jpg 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-123x115.jpg 123w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-320x300.jpg 320w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-96x90.jpg 96w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-362x340.jpg 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-117x110.jpg 117w" data-sizes="(max-width: 551px) 100vw, 551px" width="551" height="517" alt="3D Render of an NVIDIA HGX Grace Hopper with InfiniBand system." />
<figcaption><em>Figure 12. NVIDIA HGX Grace Hopper with InfiniBand</em></figcaption>
</figure>

</div>

## NVIDIA HGX Grace Hopper with InfiniBand<a href="#nvidia_hgx_grace_hopper_with_infiniband" class="heading-anchor-link" aria-label="Scroll to NVIDIA HGX Grace Hopper with InfiniBand section"><em></em></a>

NVIDIA HGX Grace Hopper ** **with Infiniband (Figure 13) is ideal for the scale-out of traditional machine learning (ML) and HPC workloads that are not bottlenecked by network communication overheads of InfiniBand, which is one of the fastest interconnects available.

Each node contains one Grace Hopper Superchip and one or more PCIe devices like NVMe solid-state drives and BlueField-3 DPUs, NVIDIA ConnectX-7 NICs, or OEM-defined I/O. With 16x PCIe Gen 5 lanes, an NDR400 InfiniBand NIC provides up to 100 GB/s of total bandwidth across the superchips. Combined with NVIDIA BlueField-3 DPUs, this platform is easy to manage and deploy and uses a traditional HPC and AI cluster networking architecture.

<div class="wp-block-image">

<figure class="aligncenter size-full is-resized">
<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc.png" class="wp-image-57239" style="width:1055px;height:465px" decoding="async" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc.png 1406w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-300x132.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-625x276.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-179x79.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-768x339.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-500x220.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-160x71.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-362x160.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-249x110.png 249w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-1024x452.png 1024w" sizes="(max-width: 1406px) 100vw, 1406px" width="1406" height="620" alt="Diagram shows an NVIDIA HGX Grace Hopper Superchip with Infiniband networking system. There is hardware coherency within each Grace Hopper Superchip. Each Superchip is connected with a BlueField 3 DPU through PCIe, which are then connected at 100 GB/s total bandwidth with NVIDIA Quantum-2 InfiniBand NDR400 Switches." />
<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201406%20620%22%3E%3C/svg%3E" class="lazyload wp-image-57239" style="width:1055px;height:465px" decoding="async" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc.png" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc.png 1406w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-300x132.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-625x276.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-179x79.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-768x339.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-500x220.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-160x71.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-362x160.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-249x110.png 249w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/hgx-grace-hopper-infiniband-scale-out-ml-hpc-1024x452.png 1024w" data-sizes="(max-width: 1406px) 100vw, 1406px" width="1406" height="620" alt="Diagram shows an NVIDIA HGX Grace Hopper Superchip with Infiniband networking system. There is hardware coherency within each Grace Hopper Superchip. Each Superchip is connected with a BlueField 3 DPU through PCIe, which are then connected at 100 GB/s total bandwidth with NVIDIA Quantum-2 InfiniBand NDR400 Switches." />
<figcaption><em>Figure 13. NVIDIA HGX Grace Hopper with InfiniBand for scale-out ML and HPC workloads</em></figcaption>
</figure>

</div>

## NVIDIA HGX Grace Hopper with NVLink Switch<a href="#nvidia_hgx_grace_hopper_with_nvlink_switch" class="heading-anchor-link" aria-label="Scroll to NVIDIA HGX Grace Hopper with NVLink Switch section"><em></em></a>

NVIDIA HGX Grace Hopper with NVLink Switch is ideal for strong scaling giant machine learning and HPC workloads. It enables all GPU threads in the NVLink-connected domain to address up to 150 TB of memory at up to 900 GB/s total bandwidth per superchip in a 256-GPU NVLink-connected system. The a simple programming model uses pointer load, store, and atomic operations. Its 450 GB/s all-reduce bandwidth and up to 115.2 TB/s bisection bandwidth make this platform ideal for strong-scaling the world’s largest and most challenging AI training and HPC workloads.

NVLink-connected domains are networked with NVIDIA InfiniBand networking, for example, NVIDIA ConnectX-7 NICs or NVIDIA BlueField-3 data processing units (DPUs) paired with NVIDIA Quantum 2 NDR switches or OEM-defined I/O solutions.

<div class="wp-block-image">

<figure class="aligncenter size-full is-resized">
<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system.png" class="wp-image-57240" style="width:1058px;height:529px" decoding="async" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system.png 1410w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-300x150.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-625x313.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-179x90.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-768x384.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-500x250.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-160x80.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-362x181.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-220x110.png 220w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-1024x512.png 1024w" sizes="(max-width: 1410px) 100vw, 1410px" width="1410" height="705" alt="Diagram shows an NVIDIA HGX Grace Hopper with NVLink Switch System . There is hardware coherency within each Grace Hopper Superchip. Each Grace Hopper Superchip within a cluster of up to 256 Grace Hopper Superchips is connected with each other via the NVLink Switch System. Each Superchip is also connected with a BlueField 3 DPU through PCIe, which are then connected at 100 GB/s total bandwidth with NVIDIA Quantum-2 InfiniBand NDR400 Switches." />
<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%201410%20705%22%3E%3C/svg%3E" class="lazyload wp-image-57240" style="width:1058px;height:529px" decoding="async" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system.png" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system.png 1410w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-300x150.png 300w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-625x313.png 625w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-179x90.png 179w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-768x384.png 768w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-500x250.png 500w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-160x80.png 160w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-362x181.png 362w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-220x110.png 220w, https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/grace-hopper-nvlink-switch-system-1024x512.png 1024w" data-sizes="(max-width: 1410px) 100vw, 1410px" width="1410" height="705" alt="Diagram shows an NVIDIA HGX Grace Hopper with NVLink Switch System . There is hardware coherency within each Grace Hopper Superchip. Each Grace Hopper Superchip within a cluster of up to 256 Grace Hopper Superchips is connected with each other via the NVLink Switch System. Each Superchip is also connected with a BlueField 3 DPU through PCIe, which are then connected at 100 GB/s total bandwidth with NVIDIA Quantum-2 InfiniBand NDR400 Switches." />
<figcaption><em>Figure 14. NVIDIA HGX Grace Hopper with NVLink Switch System for strong-scaling giant ML and HPC workloads</em></figcaption>
</figure>

</div>

## Delivering performance breakthroughs<a href="#delivering_performance_breakthroughs" class="heading-anchor-link" aria-label="Scroll to Delivering performance breakthroughs section"><em></em></a>

The <a href="https://resources.nvidia.com/en-us-grace-cpu/nvidia-grace-hopper" data-wpel-link="internal" target="_self" rel="follow">NVIDIA Grace Hopper Superchip Architecture</a> whitepaper expands on the details covered in this post. It walks you through how Grace Hopper delivers the performance breakthroughs shown on Figure 1 over what is currently the most powerful PCIe-based accelerated platforms powered by NVIDIA Hopper H100 PCIe GPUs.

Do you have any applications that would be perfect for the NVIDIA Grace Hopper Superchip? Let us know in the comments\!

### Acknowledgments<a href="#acknowledgments" class="heading-anchor-link" aria-label="Scroll to Acknowledgments section"><em></em></a>

*We would like to thank Jack Choquette, Ronny Krashinsky, John Hubbard, Mark Hummel, Greg Palmer, Ryan Wells, Alex Ishii, Jonah Alben, and* *the many NVIDIA architects and engineers who contributed to this post*.

</div>

<div class="card--post-attributes-secondary">

<div class="post--comments-count secondary--attribute">

[ Discuss (12)](#entry-content-comments)

</div>

<div class="post--rate secondary--attribute">

<div class="wpulike wpulike-heart">

<div class="wp_ulike_general_class wp_ulike_is_not_liked">

<span class="count-box wp_ulike_counter_up" ulike-counter-value="+52"></span>

</div>

</div>

Like

</div>

</div>

<div class="card--post-attributes-secondary tags">

<div class="caption">

## Tags

</div>

<div class="content-s post-tags--list mt-0">

<a href="https://developer.nvidia.com/blog/category/data-center-cloud/" data-wpel-link="internal" target="_self" rel="follow">Data Center / Cloud</a> \| <a href="https://developer.nvidia.com/blog/category/data-science/" data-wpel-link="internal" target="_self" rel="follow">Data Science</a> \| <a href="https://developer.nvidia.com/blog/recent-posts/?industry=HPC+%2F+Scientific+Computing" data-wpel-link="internal" target="_self" rel="follow">HPC / Scientific Computing</a> \| <a href="https://developer.nvidia.com/blog/recent-posts/?products=CUDA" data-wpel-link="internal" target="_self" rel="follow">CUDA</a> \| <a href="https://developer.nvidia.com/blog/recent-posts/?products=Grace+CPU" data-wpel-link="internal" target="_self" rel="follow">Grace CPU</a> \| <a href="https://developer.nvidia.com/blog/recent-posts/?learning_levels=Intermediate+Technical" data-wpel-link="internal" target="_self" rel="follow">Intermediate Technical</a> \| <a href="https://developer.nvidia.com/blog/recent-posts/?content_types=Tutorial" data-wpel-link="internal" target="_self" rel="follow">Tutorial</a> \| <a href="https://developer.nvidia.com/blog/tag/featured/" data-wpel-link="internal" target="_self" rel="follow">featured</a>

</div>

</div>

<div class="post-authors-list">

<div class="entry-content-author">

<div class="caption">

## About the Authors

</div>

<div class="media author-info">

<div class="author-media-left media-left">

<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/08/image2-e1660679098753-131x131.jpg" class="avatar avatar-131 photo" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/08/image2-e1660679098753-262x262.jpg 2x" decoding="async" width="131" height="131" alt="Jonathon Evans" />

<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E" class="lazyload avatar avatar-131 photo" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/08/image2-e1660679098753-131x131.jpg" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/08/image2-e1660679098753-262x262.jpg 2x" decoding="async" width="131" height="131" alt="Jonathon Evans" />

</div>

<div class="author-media-body media-body">

**About Jonathon Evans**  
Jonathon Evans is an NVIDIA Distinguished Engineer and architecture lead for the NVIDIA Grace CPU. Jonathon joined NVIDIA in 2007 as a member of the GPU Architecture team. His prior work on GPU includes leading the GPU’s context management and scheduling HW team, and contributions to Async Compute, Unified Memory, Multi Instance GPU, and WDDM HW Scheduling.

<div id="author-link">

<a href="https://developer.nvidia.com/blog/author/jevans/" rel="author follow" data-wpel-link="internal" target="_self">View all posts by Jonathon Evans<img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==" /></a>

</div>

</div>

</div>

<div class="media author-info">

<div class="author-media-left media-left">

<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/03/Michael-Andersch-131x131.jpg" class="avatar avatar-131 photo" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/03/Michael-Andersch.jpg 2x" decoding="async" width="131" height="131" alt="Avatar photo" />

<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E" class="lazyload avatar avatar-131 photo" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/03/Michael-Andersch-131x131.jpg" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/03/Michael-Andersch.jpg 2x" decoding="async" width="131" height="131" alt="Avatar photo" />

</div>

<div class="author-media-body media-body">

**About Michael Andersch**  
Michael Andersch is a principal GPU architect and senior architecture manager at NVIDIA. He started his career in the Compute Architecture team, where he focused on advancing the GPU's capabilities for the world's diverse set of CUDA workloads. In recent years, Michael has driven both hardware and software improvements specifically to increase the performance of deep neural network training, and his team is now involved wherever training performance is critical; from tuning the latest neural networks in the deep learning community to designing next-generation GPUs.

<div id="author-link">

<a href="https://developer.nvidia.com/blog/author/mandersch/" rel="author follow" data-wpel-link="internal" target="_self">View all posts by Michael Andersch<img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==" /></a>

</div>

</div>

</div>

<div class="media author-info">

<div class="author-media-left media-left">

<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/vikram-sethi-131x131.jpg" class="avatar avatar-131 photo" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/vikram-sethi.jpg 2x" decoding="async" width="131" height="131" alt="Avatar photo" />

<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E" class="lazyload avatar avatar-131 photo" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/vikram-sethi-131x131.jpg" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/11/vikram-sethi.jpg 2x" decoding="async" width="131" height="131" alt="Avatar photo" />

</div>

<div class="author-media-body media-body">

**About Vikram Sethi**  
Vikram Sethi is an NVIDIA Distinguished Engineer and software and system architect with over 20 years of experience working on hypervisors, kernels, device drivers, and firmware. He is the lead system software architect for NVIDIA Grace. Vikram represents NVIDIA software in industry consortiums, including Compute Express Link (CXL), PCIe, and UCIe.

<div id="author-link">

<a href="https://developer.nvidia.com/blog/author/vsethi/" rel="author follow" data-wpel-link="internal" target="_self">View all posts by Vikram Sethi<img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==" /></a>

</div>

</div>

</div>

<div class="media author-info">

<div class="author-media-left media-left">

<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/03/Gonzalo-Brito-1.jpg" class="avatar avatar-131 photo" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/03/Gonzalo-Brito-1.jpg 2x" decoding="async" width="131" height="131" alt="Avatar photo" />

<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E" class="lazyload avatar avatar-131 photo" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2022/03/Gonzalo-Brito-1.jpg" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2022/03/Gonzalo-Brito-1.jpg 2x" decoding="async" width="131" height="131" alt="Avatar photo" />

</div>

<div class="author-media-body media-body">

**About Gonzalo Brito**  
Gonzalo Brito is a GPU architect at NVIDIA, focusing on the Memory Consistency and Programming Model. He is also an ISO C++ committee member, contributing to the Concurrency and Parallelism Study Group. With a background in HPC performance modeling and optimization, he is passionate about simplifying heterogeneous programming models and teaching parallel programming. Before joining NVIDIA, he researched HPC methods for multi-physics problems in particle-laden flows at the Institute of Aerodynamics of RWTH Aachen.

<div id="author-link">

<a href="https://developer.nvidia.com/blog/author/gonzalob/" rel="author follow" data-wpel-link="internal" target="_self">View all posts by Gonzalo Brito<img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==" /></a>

</div>

</div>

</div>

<div class="media author-info">

<div class="author-media-left media-left">

<img src="https://developer-blogs.nvidia.com/wp-content/uploads/2021/02/vishal-131x131.png" class="avatar avatar-131 photo" srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2021/02/vishal-262x262.png 2x" decoding="async" width="131" height="131" alt="Avatar photo" />

<img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20131%20131%22%3E%3C/svg%3E" class="lazyload avatar avatar-131 photo" data-src="https://developer-blogs.nvidia.com/wp-content/uploads/2021/02/vishal-131x131.png" data-srcset="https://developer-blogs.nvidia.com/wp-content/uploads/2021/02/vishal-262x262.png 2x" decoding="async" width="131" height="131" alt="Avatar photo" />

</div>

<div class="author-media-body media-body">

**About Vishal Mehta**  
Vishal works as a senior developer technology engineer at NVIDIA, with focus on performance optimization for GPU applications. He has been working in the field of GPU computing for over 10 years. He is keen on teaching CUDA and GPU computing to users and drives the content for the CUDA programming guide. His day-to-day activities involve collaborations with domain scientists and industry experts to improve their workloads on GPUs.

<div id="author-link">

<a href="https://developer.nvidia.com/blog/author/vishalm/" rel="author follow" data-wpel-link="internal" target="_self">View all posts by Vishal Mehta<img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDMyMCA2MTIiPjxwYXRoIGQ9Ik0zMDUgMjM5YzkuNCA5LjQgOS40IDI0LjYgMCAzMy45TDExMyA0NjVjLTkuNCA5LjQtMjQuNiA5LjQtMzMuOSAwcy05LjQtMjQuNiAwLTMzLjlsMTc1LTE3NUw3OSA4MWMtOS40LTkuNC05LjQtMjQuNiAwLTMzLjlzMjQuNi05LjQgMzMuOSAwTDMwNSAyMzl6IiAvPjwvc3ZnPg==" /></a>

</div>

</div>

</div>

</div>

</div>

<div id="entry-content-comments" class="entry-content-comments">

<div id="pf-disqus-thread" class="container">

<div id="respond" class="row">

<div class="col-md-12 related-posts-comments mb-0">

## Comments

</div>

</div>

<div class="row">

<div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">

<div id="wpdc-comments" class="wpdc-comments-loading" post-id="57192">

</div>

</div>

</div>

</div>

</div>

<div id="main-content-end">

</div>

</div>
