<!-- 从 genie-institution.html 迁移的资料快照；原始 HTML SHA-256: 8c328f576c48c456b2095b24d51517565930468b0acc4b06a15c580adc218802。 -->

# Genie Cache: Non-blocking Miss Handling and Replacement in Page-Table-based DRAM Cache

Youngin Kim

, [William Song](https://yonsei.elsevierpure.com/en/persons/william-song/)

- [Department of Electrical and Electronic Engineering](https://yonsei.elsevierpure.com/en/organisations/department-of-electrical-and-electronic-engineering/)

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

[3   Link opens in a new tab](https://www.scopus.com/pages/publications/85213329009#tab=citedBy) Citations (Scopus)

- [ Overview ](/en/publications/genie-cache-non-blocking-miss-handling-and-replacement-in-page-ta/)
- [ Fingerprint ](/en/publications/genie-cache-non-blocking-miss-handling-and-replacement-in-page-ta/fingerprints/)

## Abstract

This paper presents Genie Cache that enables non-blocking miss-handling and replacement in a page-table-based DRAM cache (DC). Various DC designs have been proposed to meet the growing bandwidth demand of emerging memory-bound applications. The related literature can be categorized into hardware-based (HW-based) and page-table-based (PT-based) schemes based on their tag storage methods. HW-based designs store DC metadata (e.g., tags) in on-package DRAM for scalability but use extra bandwidth and energy for metadata access. PT-based schemes store DC tags in page table entries (PTEs), enabling virtual-to-cache address translations using the existing memory management units (MMUs) without the DC bandwidth overhead. However, their miss-handling and eviction mechanisms relying on operating systems (OS) incur nontrivial latency overhead. To minimize the OS intervention, Genie Cache implements non-blocking miss handling and replacement using a hardware unit called DRAM cache management unit (DCMU) and a novel pre-write back mechanism. In Genie Cache, DC misses detected by MMUs are forwarded to the DCMU, which handles the misses by allocating page frames and updating PTEs without calling OS routines. When the PT-based DRAM cache runs low on free pages, an eviction routine is called to flush TLBs and evict a batch of cached pages to avoid frequent TLB shootdowns. Since writing back many dirty pages in a blocking manner causes substantial application stall cycles, Genie Cache proactively writes dirty pages back to off-package memory, allowing the eviction routine to simply evict cleaned pages. Experimental results show that Genie Cache achieves 51.3% speedup over the state-of-the-art PT-based design via non-blocking miss handling and replacement.

[TABLE]

## Access to Document

- [10.1109/MICRO61859.2024.00076](https://doi.org/10.1109/MICRO61859.2024.00076)

##  Fingerprint

Dive into the research topics of 'Genie Cache: Non-blocking Miss Handling and Replacement in Page-Table-based DRAM Cache'. Together they form a unique fingerprint.

-  Nonblocking Computer Science 100%
-  Page Table Computer Science 100%
-  Operating System Computer Science 50%
-  Page Table Entry Computer Science 33%
-  Memory Management Unit Computer Science 33%
-  Metadata Computer Science 33%
-  Memory Package Computer Science 16%
-  Address Translation Computer Science 16%

[ View full fingerprint ](/en/publications/genie-cache-non-blocking-miss-handling-and-replacement-in-page-ta/fingerprints/)

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

Kim, Y.[, & Song, W.](https://yonsei.elsevierpure.com/en/persons/william-song/) (2024). [Genie Cache: Non-blocking Miss Handling and Replacement in Page-Table-based DRAM Cache](https://yonsei.elsevierpure.com/en/publications/genie-cache-non-blocking-miss-handling-and-replacement-in-page-ta/). In *2024 57th IEEE/ACM International Symposium on Microarchitecture (MICRO)* (pp. 983-996) [https://doi.org/10.1109/MICRO61859.2024.00076](https://doi.org/10.1109/MICRO61859.2024.00076)

Kim, Youngin [ ; Song, William](https://yonsei.elsevierpure.com/en/persons/william-song/). / [**Genie Cache: Non-blocking Miss Handling and Replacement in Page-Table-based DRAM Cache**](https://yonsei.elsevierpure.com/en/publications/genie-cache-non-blocking-miss-handling-and-replacement-in-page-ta/). 2024 57th IEEE/ACM International Symposium on Microarchitecture (MICRO). 2024. pp. 983-996

@inproceedings{73d7f63db5cd42498ebcbcabe0d3ee19,

title = "Genie Cache: Non-blocking Miss Handling and Replacement in Page-Table-based DRAM Cache",

abstract = "This paper presents Genie Cache that enables non-blocking miss-handling and replacement in a page-table-based DRAM cache (DC). Various DC designs have been proposed to meet the growing bandwidth demand of emerging memory-bound applications. The related literature can be categorized into hardware-based (HW-based) and page-table-based (PT-based) schemes based on their tag storage methods. HW-based designs store DC metadata (e.g., tags) in on-package DRAM for scalability but use extra bandwidth and energy for metadata access. PT-based schemes store DC tags in page table entries (PTEs), enabling virtual-to-cache address translations using the existing memory management units (MMUs) without the DC bandwidth overhead. However, their miss-handling and eviction mechanisms relying on operating systems (OS) incur nontrivial latency overhead. To minimize the OS intervention, Genie Cache implements non-blocking miss handling and replacement using a hardware unit called DRAM cache management unit (DCMU) and a novel pre-write back mechanism. In Genie Cache, DC misses detected by MMUs are forwarded to the DCMU, which handles the misses by allocating page frames and updating PTEs without calling OS routines. When the PT-based DRAM cache runs low on free pages, an eviction routine is called to flush TLBs and evict a batch of cached pages to avoid frequent TLB shootdowns. Since writing back many dirty pages in a blocking manner causes substantial application stall cycles, Genie Cache proactively writes dirty pages back to off-package memory, allowing the eviction routine to simply evict cleaned pages. Experimental results show that Genie Cache achieves 51.3\\ speedup over the state-of-the-art PT-based design via non-blocking miss handling and replacement.",

author = "Youngin Kim and William Song",

year = "2024",

month = nov,

day = "6",

doi = "10.1109/MICRO61859.2024.00076",

language = "English",

isbn = "979-8-3503-5057-9",

pages = "983--996",

booktitle = "2024 57th IEEE/ACM International Symposium on Microarchitecture (MICRO)",

}

Kim, Y[ & Song, W](https://yonsei.elsevierpure.com/en/persons/william-song/) 2024, [Genie Cache: Non-blocking Miss Handling and Replacement in Page-Table-based DRAM Cache](https://yonsei.elsevierpure.com/en/publications/genie-cache-non-blocking-miss-handling-and-replacement-in-page-ta/). in *2024 57th IEEE/ACM International Symposium on Microarchitecture (MICRO).* pp. 983-996. [https://doi.org/10.1109/MICRO61859.2024.00076](https://doi.org/10.1109/MICRO61859.2024.00076)

[**Genie Cache: Non-blocking Miss Handling and Replacement in Page-Table-based DRAM Cache.**](https://yonsei.elsevierpure.com/en/publications/genie-cache-non-blocking-miss-handling-and-replacement-in-page-ta/) / Kim, Youngin[; Song, William](https://yonsei.elsevierpure.com/en/persons/william-song/).  
2024 57th IEEE/ACM International Symposium on Microarchitecture (MICRO). 2024. p. 983-996.

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

TY - GEN

T1 - Genie Cache: Non-blocking Miss Handling and Replacement in Page-Table-based DRAM Cache

AU - Kim, Youngin

AU - Song, William

PY - 2024/11/6

Y1 - 2024/11/6

N2 - This paper presents Genie Cache that enables non-blocking miss-handling and replacement in a page-table-based DRAM cache (DC). Various DC designs have been proposed to meet the growing bandwidth demand of emerging memory-bound applications. The related literature can be categorized into hardware-based (HW-based) and page-table-based (PT-based) schemes based on their tag storage methods. HW-based designs store DC metadata (e.g., tags) in on-package DRAM for scalability but use extra bandwidth and energy for metadata access. PT-based schemes store DC tags in page table entries (PTEs), enabling virtual-to-cache address translations using the existing memory management units (MMUs) without the DC bandwidth overhead. However, their miss-handling and eviction mechanisms relying on operating systems (OS) incur nontrivial latency overhead. To minimize the OS intervention, Genie Cache implements non-blocking miss handling and replacement using a hardware unit called DRAM cache management unit (DCMU) and a novel pre-write back mechanism. In Genie Cache, DC misses detected by MMUs are forwarded to the DCMU, which handles the misses by allocating page frames and updating PTEs without calling OS routines. When the PT-based DRAM cache runs low on free pages, an eviction routine is called to flush TLBs and evict a batch of cached pages to avoid frequent TLB shootdowns. Since writing back many dirty pages in a blocking manner causes substantial application stall cycles, Genie Cache proactively writes dirty pages back to off-package memory, allowing the eviction routine to simply evict cleaned pages. Experimental results show that Genie Cache achieves 51.3% speedup over the state-of-the-art PT-based design via non-blocking miss handling and replacement.

AB - This paper presents Genie Cache that enables non-blocking miss-handling and replacement in a page-table-based DRAM cache (DC). Various DC designs have been proposed to meet the growing bandwidth demand of emerging memory-bound applications. The related literature can be categorized into hardware-based (HW-based) and page-table-based (PT-based) schemes based on their tag storage methods. HW-based designs store DC metadata (e.g., tags) in on-package DRAM for scalability but use extra bandwidth and energy for metadata access. PT-based schemes store DC tags in page table entries (PTEs), enabling virtual-to-cache address translations using the existing memory management units (MMUs) without the DC bandwidth overhead. However, their miss-handling and eviction mechanisms relying on operating systems (OS) incur nontrivial latency overhead. To minimize the OS intervention, Genie Cache implements non-blocking miss handling and replacement using a hardware unit called DRAM cache management unit (DCMU) and a novel pre-write back mechanism. In Genie Cache, DC misses detected by MMUs are forwarded to the DCMU, which handles the misses by allocating page frames and updating PTEs without calling OS routines. When the PT-based DRAM cache runs low on free pages, an eviction routine is called to flush TLBs and evict a batch of cached pages to avoid frequent TLB shootdowns. Since writing back many dirty pages in a blocking manner causes substantial application stall cycles, Genie Cache proactively writes dirty pages back to off-package memory, allowing the eviction routine to simply evict cleaned pages. Experimental results show that Genie Cache achieves 51.3% speedup over the state-of-the-art PT-based design via non-blocking miss handling and replacement.

U2 - 10.1109/MICRO61859.2024.00076

DO - 10.1109/MICRO61859.2024.00076

M3 - Conference contribution

SN - 979-8-3503-5057-9

SP - 983

EP - 996

BT - 2024 57th IEEE/ACM International Symposium on Microarchitecture (MICRO)

ER -

Kim Y[, Song W](https://yonsei.elsevierpure.com/en/persons/william-song/). [Genie Cache: Non-blocking Miss Handling and Replacement in Page-Table-based DRAM Cache](https://yonsei.elsevierpure.com/en/publications/genie-cache-non-blocking-miss-handling-and-replacement-in-page-ta/). In 2024 57th IEEE/ACM International Symposium on Microarchitecture (MICRO). 2024. p. 983-996 doi: 10.1109/MICRO61859.2024.00076

- 
- [](https://www.facebook.com/sharer.php?u=https://yonsei.elsevierpure.com/en/publications/genie-cache-non-blocking-miss-handling-and-replacement-in-page-ta/%3Futm_source%3Dfacebook%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FMICRO61859.2024.00076&p%5Bsummary%5D=Check+out+this+research+output+at+Yonsei+University%3A+Genie+Cache%3A+Non-blocking+Miss+Handling+and+Replacement+in+Page-Table-based+DRAM+Cache)
- [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMiIgaGVpZ2h0PSIyMiIgdmlld2JveD0iMCAwIDMwMCAyNzEiPgogICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Im0yMzYgMGg0NmwtMTAxIDExNSAxMTggMTU2aC05Mi42bC03Mi41LTk0LjgtODMgOTQuOGgtNDZsMTA3LTEyMy0xMTMtMTQ4aDk0LjlsNjUuNSA4Ni42em0tMTYuMSAyNDRoMjUuNWwtMTY1LTIxOGgtMjcuNHoiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)](https://twitter.com/intent/tweet?url=https://yonsei.elsevierpure.com/en/publications/genie-cache-non-blocking-miss-handling-and-replacement-in-page-ta/%3Futm_source%3Dtwitter%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FMICRO61859.2024.00076&text=Check+out+this+research+output+at+Yonsei+University%3A+Genie+Cache%3A+Non-blocking+Miss+Handling+and+Replacement+in+Page-Table-based+DRAM+Cache)
- [](https://www.linkedin.com/shareArticle?mini=true&url=https://yonsei.elsevierpure.com/en/publications/genie-cache-non-blocking-miss-handling-and-replacement-in-page-ta/%3Futm_source%3Dlinkedin%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FMICRO61859.2024.00076&summary=Check+out+this+research+output+at+Yonsei+University%3A+Genie+Cache%3A+Non-blocking+Miss+Handling+and+Replacement+in+Page-Table-based+DRAM+Cache)
- [](/cdn-cgi/l/email-protection#c1feb2b4a3aba4a2b5fc86a4afa8a4e4f3f182a0a2a9a4e4f280e4f3f18faeafeca3adaea2aaa8afa6e4f3f18ca8b2b2e4f3f189a0afa5ada8afa6e4f3f1a0afa5e4f3f193a4b1ada0a2a4aca4afb5e4f3f1a8afe4f3f191a0a6a4ec95a0a3ada4eca3a0b2a4a5e4f3f18593808ce4f3f182a0a2a9a4e7a3aea5b8fc82a9a4a2aae4f3f1aeb4b5e4f3f1b5a9a8b2e4f3f1b3a4b2a4a0b3a2a9e4f3f1aeb4b5b1b4b5e4f3f1a0b5e4f3f198aeafb2a4a8e4f3f194afa8b7a4b3b2a8b5b8e4f280e4f3f186a4afa8a4e4f3f182a0a2a9a4e4f280e4f3f18faeafeca3adaea2aaa8afa6e4f3f18ca8b2b2e4f3f189a0afa5ada8afa6e4f3f1a0afa5e4f3f193a4b1ada0a2a4aca4afb5e4f3f1a8afe4f3f191a0a6a4ec95a0a3ada4eca3a0b2a4a5e4f3f18593808ce4f3f182a0a2a9a4e1bde1a9b5b5b1b2fbeeeeb8aeafb2a4a8efa4adb2a4b7a8a4b3b1b4b3a4efa2aeaceea4afeeb1b4a3ada8a2a0b5a8aeafb2eea6a4afa8a4eca2a0a2a9a4ecafaeafeca3adaea2aaa8afa6ecaca8b2b2eca9a0afa5ada8afa6eca0afa5ecb3a4b1ada0a2a4aca4afb5eca8afecb1a0a6a4ecb5a0eefeb4b5ac9eb2aeb4b3a2a4fca4aca0a8ade7a0acb1fab4b5ac9eaca4a5a8b4acfca4aca0a8ade7a0acb1fab4b5ac9ea2a0acb1a0a8a6affcb2a9a0b3a4ada8afaa)
