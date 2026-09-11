<!-- 从 sharp-docs-intro.html 迁移的资料快照；原始 HTML SHA-256: 7059bb2686b4fa3943477cfe9626db44121a73c49a0352237828400f7fb3aaf2。 -->

<div class="main-content" role="main">

<div class="topbar">

Breadcrumbs

1.  [Networking](/)
2.  [Networking Software](/software)
3.  [Accelerator Software](/software/accelerator-software)
4.  [NVIDIA Scalable Hierarchical Aggregation and Reduction Protocol (SHARP)](/sharpum/300)
5.  [Introduction](/sharpum/300/introduction)

</div>

<div class="article-actions">

</div>

<div class="sidebar">

<div class="sidebar-actions">

</div>

## On this Page

</div>

<div>

# Introduction

</div>

<div class="section article-body fb-layout-body" searchable-content="">

NVIDIA® Scalable Hierarchical Aggregation and Reduction Protocol (SHARP)™ technology improves the performance of MPI and Machine Learning collective operation, by offloading collective operations from CPUs and GPUs to the network and eliminating the need to send data multiple times between endpoints.

This innovative approach decreases the amount of data traversing the network as aggregation nodes are reached, and dramatically reduces collective operations time. Implementing collective offloads communication algorithms supporting streaming for Machine Learning in the network also has additional benefits, such as freeing up valuable CPU and GPU resources for computation rather than using them to process communication.

With the 3rd generation of SHARP, multiple aggregation trees can be built over the same topology, enabling the aggregation and reductions benefits (also known as In-Network Computing) to many parallel jobs over the same infrastructure.

Last updated: August 01, 2022

</div>

Pagination

- <a href="/sharpum/300/known-issues" rel="prev"></a>
  <div class="page-pagination-icon">

  <img src="data:image/svg+xml;base64,PHN2ZyByb2xlPSJpbWciIGFyaWEtaGlkZGVuPSJ0cnVlIiBkYXRhLWNvbXBvbmVudD0iaWNvbiIgY2xhc3M9Imljb24gaWNvbi1hcnJvd19sZWZ0ICI+CiAgICAgICAgPHVzZSBocmVmPSIvc2hhcnB1bS9fX3RoZW1lL2NfNmMyOTczNGUtZDk0MS00NjEzLTkyOTYtOTE4ZTdlNTg3NTgyL2hlbHAtY2VudGVyLXRoZW1lLW52aWRpYS1mb3JrLzIwL2ljb25zLnN2ZyNhcnJvd19sZWZ0IiAvPgogICAgPC9zdmc+" class="icon icon-arrow_left" />

  </div>

  <div>

  <div class="page-pagination-label">

  Previous Page

  </div>

  <div class="page-pagination-title">

  Known Issues

  </div>

  </div>
- <a href="/sharpum/300/setting-up-nvidia-sharp-environment" rel="next"></a>
  <div>

  <div class="page-pagination-label">

  Next Page

  </div>

  <div class="page-pagination-title">

  Setting up NVIDIA SHARP Environment

  </div>

  </div>

  <div class="page-pagination-icon">

  <img src="data:image/svg+xml;base64,PHN2ZyByb2xlPSJpbWciIGFyaWEtaGlkZGVuPSJ0cnVlIiBkYXRhLWNvbXBvbmVudD0iaWNvbiIgY2xhc3M9Imljb24gaWNvbi1hcnJvd19yaWdodCAiPgogICAgICAgIDx1c2UgaHJlZj0iL3NoYXJwdW0vX190aGVtZS9jXzZjMjk3MzRlLWQ5NDEtNDYxMy05Mjk2LTkxOGU3ZTU4NzU4Mi9oZWxwLWNlbnRlci10aGVtZS1udmlkaWEtZm9yay8yMC9pY29ucy5zdmcjYXJyb3dfcmlnaHQiIC8+CiAgICA8L3N2Zz4=" class="icon icon-arrow_right" />

  </div>

</div>
