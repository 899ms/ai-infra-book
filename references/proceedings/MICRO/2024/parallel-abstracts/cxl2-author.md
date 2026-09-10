<!-- 从 cxl2-author.html 迁移的资料快照；原始 HTML SHA-256: a9053a92504a33e9d95b458963caa56e4fed5b87a9a292d69479b8476c7136fa。 -->

# Search

[](#)

[Ipoom Jeong](/)

[Ipoom Jeong](/)

- [Home](/#about)
- [Publications](/#recent)
- [Projects](/#projects)
- [Posts](/#posts)
- [Events](/#events)
- [Contact](/#contact)

- [](#)
- [](#)
  [Light](#) [Dark](#) [Automatic](#)

# Demystifying a CXL Type-2 Device: A Heterogeneous Cooperative Computing Perspective

Houxiang Ji, Srikar Vanavasam, Yang Zhou, Qirong Xia, Jinghan Huang, Yifan Yuan, Ren Wang, Pekon Gupta, Bhushan Chitlur, Ipoom Jeong, Nam Sung Kim

November, 2024

[PDF](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10764537&casa_token=J_x57OKKsjcAAAAA:aNHpaPCkxR9RUUcIFGf0EanD0a62kSG-cowfTPcHJFHZUsnuKCkv8LQyL4zJKAjD2YAi6mmssA) [Cite](#)

### Abstract

CXL is the latest interconnect technology built on PCIe, providing three protocols to facilitate three distinct types of devices, each with unique capabilities. Among these devices, a CXL Type-2 device has become commercially available, followed by CXL Type-3 devices. Therefore, it is timely to understand capabilities and characteristics of the CXL Type-2 device, as well as explore suitable applications. In this work, first, we delve into three key features of a CXL Type-2 device: cache-coherent device accelerator to host memory, device accelerator to device memory, and host CPU to device memory accesses. Second, using microbenchmarks, we comprehensively characterize the latency and bandwidth of these memory accesses with a CXL Type-2 device, and then compare them with those of equivalent memory accesses with comparable devices, such as emulated CXL Type-2, CXL Type-3, and PCIe devices. Lastly, as applications that exploit the unique capabilities of a CXL Type-2 device, we propose two CXL-based Linux memory optimization features: compressed RAM cache for swap (zswap) and memory deduplication (ksm). Our evaluation shows that Redis, when running with traditional CPU-based zswap and ksm, suffers from a tail latency increase of 4.5–10.3× compared to Redis running alone. While PCIebased zswap and ksm still experience a tail latency increase of up to 8.1×, CXL-based zswap and ksm practically eliminate the tail latency increase with faster and more efficient host-device communication than PCIe-based zswap and ksm.

Type

[Conference paper](/publication/#1)

Publication

IEEE/ACM International Symposium on Microarchitecture (MICRO)

[CPU](/tag/cpu/) [CXL](/tag/cxl/) [Memory](/tag/memory/) [Accelerator](/tag/accelerator/) [Systems](/tag/systems/) [datacenter](/tag/datacenter/)

- [](https://twitter.com/intent/tweet?url=https%3A%2F%2Fipoom-jeong.com%2Fpublication%2Fdemystifying-a-cxl-type-2-device-a-heterogeneous-cooperative-computing-perspective%2F&text=Demystifying+a+CXL+Type-2+Device%3A+A+Heterogeneous+Cooperative+Computing+Perspective)
- [](https://www.facebook.com/sharer.php?u=https%3A%2F%2Fipoom-jeong.com%2Fpublication%2Fdemystifying-a-cxl-type-2-device-a-heterogeneous-cooperative-computing-perspective%2F&t=Demystifying+a+CXL+Type-2+Device%3A+A+Heterogeneous+Cooperative+Computing+Perspective)
- [](mailto:?subject=Demystifying%20a%20CXL%20Type-2%20Device%3A%20A%20Heterogeneous%20Cooperative%20Computing%20Perspective&body=https%3A%2F%2Fipoom-jeong.com%2Fpublication%2Fdemystifying-a-cxl-type-2-device-a-heterogeneous-cooperative-computing-perspective%2F)
- [](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Fipoom-jeong.com%2Fpublication%2Fdemystifying-a-cxl-type-2-device-a-heterogeneous-cooperative-computing-perspective%2F&title=Demystifying+a+CXL+Type-2+Device%3A+A+Heterogeneous+Cooperative+Computing+Perspective)
- [](whatsapp://send?text=Demystifying+a+CXL+Type-2+Device%3A+A+Heterogeneous+Cooperative+Computing+Perspective%20https%3A%2F%2Fipoom-jeong.com%2Fpublication%2Fdemystifying-a-cxl-type-2-device-a-heterogeneous-cooperative-computing-perspective%2F)
- [](https://service.weibo.com/share/share.php?url=https%3A%2F%2Fipoom-jeong.com%2Fpublication%2Fdemystifying-a-cxl-type-2-device-a-heterogeneous-cooperative-computing-perspective%2F&title=Demystifying+a+CXL+Type-2+Device%3A+A+Heterogeneous+Cooperative+Computing+Perspective)

[![Ipoom Jeong](/authors/admin/avatar_huad2f8dffb8b9403000ab1f52586690c3_58877_270x270_fill_q75_lanczos_center.jpg)](https://ipoom-jeong.com)

##### [Ipoom Jeong](https://ipoom-jeong.com)

###### Assistant Professor

My research interests include CPU/GPU microarchitectures, memory/storage system designs, and smart-I/O devices

- [](mailto:jip9110@gmail.com)
- [](https://www.linkedin.com/in/ipoom-jeong)
- [](https://scholar.google.com/citations?user=iGTEZKcAAAAJ&hl=ko&oi=ao)
- [](/uploads/resume.pdf)

© 2026 Me. This work is licensed under [CC BY NC ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0)

[ ](https://creativecommons.org/licenses/by-nc-nd/4.0)

Published with [Wowchemy](https://wowchemy.com/?utm_campaign=poweredby) — the free, [open source](https://github.com/wowchemy/wowchemy-hugo-themes) website builder that empowers creators.

##### Cite

×

[ Copy](#) [ Download](#)
