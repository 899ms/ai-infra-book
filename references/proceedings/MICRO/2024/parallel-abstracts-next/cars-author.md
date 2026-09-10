<!-- 从 cars-author.html 迁移的资料快照；原始 HTML SHA-256: a5c02ccebb343d4bdc60cc8b911b1e8947ba85c067fc5a9023621f4451f96935。 -->

# Search

[](#)

[Tim Rogers](/tgrogers/)

[Tim Rogers](/tgrogers/)

- [Home](/tgrogers/#about)
- [Group](/tgrogers/#phdstudents)
- [Publications](/tgrogers/#featured)
- [Contact](/tgrogers/#contact)

- [](#)
  [Light](#) [Dark](#) [Automatic](#)

# Concurrency-Aware Register Stacks for Efficient GPU Function Calls

Ni Kang, Ahmad Alawneh, Mengchi Zhang, Tim Rogers

November, 2024

[PDF](/tgrogers/publication/kang-micro-2024/kang-micro-2024.pdf)

![](/tgrogers/publication/kang-micro-2024/featured_hu78ba0c520ba79292eafdfe8420a03191_684558_e79156b18449fce072c187ea973d6211.webp)

### Abstract

Since the early days of computers, dividing a program into functions or subroutines has been a common way to manage complexity. Functions make programs easier to read, facilitate code reuse, and provide clean interfaces for separate compilation. However, function calls incur runtime overhead. We quantify the impact of this runtime overhead on GPUs and demonstrate that the register spills/fills required to maintain the function call application binary interface place significant bandwidth and capacity pressure on shared resources. To alleviate this overhead, we introduce Concurrency-Aware Register Stacks (CARS), a hardware mechanism that re-purposes segments of the GPU register file as a software-controlled hardware stack. CARS exploits the regularity in function prologue/epilogues to rename registers pushed to the stack with linear base + offset addressing, similar to the baseline GPU. Informed by lightweight call graph analysis and dynamic function behavior, CARS balances the space devoted to register stacks with the concurrency required to hide latency in GPUs. Without harming function-free programs, CARS improves the performance and energy efficiency of twenty-two function-calling applications by 25% and 30%, respectively, outperforming idealized GPUs with impractical resources.

Type

[Conference paper](/tgrogers/publication/#paper-conference)

Publication

In *57th IEEE/ACM International Symposium on Microarchitecture (MICRO)*

- [](https://twitter.com/intent/tweet?url=http%3A%2F%2Flocalhost%3A1313%2Ftgrogers%2Fpublication%2Fkang-micro-2024%2F&text=Concurrency-Aware+Register+Stacks+for+Efficient+GPU+Function+Calls)
- [](https://www.facebook.com/sharer.php?u=http%3A%2F%2Flocalhost%3A1313%2Ftgrogers%2Fpublication%2Fkang-micro-2024%2F&t=Concurrency-Aware+Register+Stacks+for+Efficient+GPU+Function+Calls)
- [](mailto:?subject=Concurrency-Aware%20Register%20Stacks%20for%20Efficient%20GPU%20Function%20Calls&body=http%3A%2F%2Flocalhost%3A1313%2Ftgrogers%2Fpublication%2Fkang-micro-2024%2F)
- [](https://www.linkedin.com/shareArticle?url=http%3A%2F%2Flocalhost%3A1313%2Ftgrogers%2Fpublication%2Fkang-micro-2024%2F&title=Concurrency-Aware+Register+Stacks+for+Efficient+GPU+Function+Calls)
- [](whatsapp://send?text=Concurrency-Aware+Register+Stacks+for+Efficient+GPU+Function+Calls%20http%3A%2F%2Flocalhost%3A1313%2Ftgrogers%2Fpublication%2Fkang-micro-2024%2F)
- [](https://service.weibo.com/share/share.php?url=http%3A%2F%2Flocalhost%3A1313%2Ftgrogers%2Fpublication%2Fkang-micro-2024%2F&title=Concurrency-Aware+Register+Stacks+for+Efficient+GPU+Function+Calls)

![Ni Kang](/tgrogers/authors/kang/avatar_hufe979c4cfb6655e2fe8538a6275ce569_124038_270x270_fill_lanczos_center_3.png)

##### Ni Kang

###### PhD Student

- [](https://www.linkedin.com/in/ni-kang-0318aa134/)

![Ahmad Alawneh](/tgrogers/authors/alawneh/avatar_hua4e97041d782cb8794421093016de003_992631_270x270_fill_lanczos_center_3.png)

##### Ahmad Alawneh

###### PhD Graduate, 2026.

- [](https://www.linkedin.com/in/ahmad-alawneh-7ba3a2348/)
- [](https://a-alawneh.github.io)

![Mengchi Zhang](/tgrogers/authors/zhang/avatar_hu817d553f087ebc9944ce6411dd08620f_120128_270x270_fill_lanczos_center_3.png)

##### Mengchi Zhang

###### PhD Graduate, 2022.

- [](https://www.linkedin.com/in/mengchi-zhang-279ab924/)

[![Tim Rogers](/tgrogers/authors/admin/avatar_hu264fc9c9ff519b0b637d8331aa6ebbb4_5333093_270x270_fill_lanczos_center_3.png)](http://localhost:1313/tgrogers/)

##### [Tim Rogers](http://localhost:1313/tgrogers/)

###### Associate Professor of ECE

- [](/tgrogers/#contact)
- [](https://scholar.google.com/citations?user=r9czEx8AAAAJ&hl=en)
- [](https://github.com/tgrogers)
- [](https://www.linkedin.com/in/tim-rogers-2952122/)

© 2026 Tim Rogers.

Published with [Hugo Blox Builder](https://hugoblox.com/?utm_campaign=poweredby) — the free, [open source](https://github.com/HugoBlox/hugo-blox-builder) website builder that empowers creators.

##### Cite

×

[ Copy](#) [ Download](#)
