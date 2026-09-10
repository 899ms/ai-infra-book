<!-- 从 paper-061-landing.html 迁移的资料快照；原始 HTML SHA-256: 3dc2b4213d51148c7ec5c0ac0e7f9eed88e2abfaf1dad1540ca26c37a3a08e3a。 -->

# ZRAID: Leveraging Zone Random Write Area (ZRWA) for Alleviating Partial Parity Tax in ZNS RAID

Minwook Kim

, Seongyeop Jeong

, Jin Soo Kim

- [College of Engineering](https://snu.elsevierpure.com/en/organisations/college-of-engineering/)
- [Department of Computer Science and Engineering](https://snu.elsevierpure.com/en/organisations/department-of-computer-science-and-engineering/)

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution › peer-review

[5   Link opens in a new tab](https://www.scopus.com/pages/publications/105002370161#tab=citedBy) Scopus citations

- [ Overview ](/en/publications/zraid-leveraging-zone-random-write-area-zrwa-for-alleviating-part/)
- [ Fingerprint ](/en/publications/zraid-leveraging-zone-random-write-area-zrwa-for-alleviating-part/fingerprints/)

## Abstract

The Zoned Namespace (ZNS) SSD is an innovative technology that aims to mitigate the block interface tax associated with conventional SSDs. However, constructing a RAID system using ZNS SSDs presents a significant challenge in managing partial parity for incomplete stripes. Previous research permanently logs partial parity in a limited number of reserved zones, which not only creates bottlenecks in throughput but also exacerbates write amplification, thereby reducing the device's lifetime. We refer to these inefficiencies as the partial parity tax. In this paper, we present ZRAID, a software ZNS RAID layer that leverages the newly added Zone Random Write Area (ZRWA) feature in the ZNS Command Set, to alleviate partial parity tax. ZRWA enables in-place updates within a confined area near the write pointer. ZRAID temporarily stores partial parity within the ZRWA of data zones. Thus, partial parity writes are distributed across multiple data zones, effectively eliminating throughput bottlenecks. Furthermore, any expired partial parity in the ZRWA is overwritten by subsequent data, avoiding unnecessary flash writes. With the introduction of ZRWA, ZRAID can leverage general schedulers, overcoming the queue depth limitations of ZNS-compatible schedulers. Our evaluation with actual ZNS SSDs demonstrates a significant improvement in write throughput: up to 34.7% in the fio microbenchmark, and an average of 14.5% in db_bench on RocksDB, along with up to a 1.6x reduction in flash write amplification.

[TABLE]

### Publication series

|  |  |
|----|----|
| Name | International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS |
| Volume | 1 |

### Conference

|  |  |
|----|----|
| Conference | 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025 |
| Country/Territory | Netherlands |
| City | Rotterdam |
| Period | 30/03/25 → 3/04/25 |

### Bibliographical note

Publisher Copyright:  
© 2025 ACM.

## Keywords

- partial parity
- raid
- zone random write area (zrwa)
- zoned namespaces

## Access to Document

- [10.1145/3669940.3707248](https://doi.org/10.1145/3669940.3707248)

## Other files and links

- [Link to publication in Scopus](https://www.scopus.com/pages/publications/105002370161)

##  Fingerprint

Dive into the research topics of 'ZRAID: Leveraging Zone Random Write Area (ZRWA) for Alleviating Partial Parity Tax in ZNS RAID'. Together they form a unique fingerprint.

-  Interface Block Computer Science 100%
-  Microbenchmarks Computer Science 100%
-  Namespace Command Computer Science 100%

[ View full fingerprint ](/en/publications/zraid-leveraging-zone-random-write-area-zrwa-for-alleviating-part/fingerprints/)

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

Kim, M., Jeong, S., & Kim, J. S. (2025). [ZRAID: Leveraging Zone Random Write Area (ZRWA) for Alleviating Partial Parity Tax in ZNS RAID](https://snu.elsevierpure.com/en/publications/zraid-leveraging-zone-random-write-area-zrwa-for-alleviating-part/). In *ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems* (pp. 1151-1165). (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS; Vol. 1). Association for Computing Machinery. [https://doi.org/10.1145/3669940.3707248](https://doi.org/10.1145/3669940.3707248)

Kim, Minwook ; Jeong, Seongyeop ; Kim, Jin Soo. / [**ZRAID : Leveraging Zone Random Write Area (ZRWA) for Alleviating Partial Parity Tax in ZNS RAID**](https://snu.elsevierpure.com/en/publications/zraid-leveraging-zone-random-write-area-zrwa-for-alleviating-part/). ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Association for Computing Machinery, 2025. pp. 1151-1165 (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS).

@inproceedings{7af2fbdff7814effa4f035b831b6d791,

title = "ZRAID: Leveraging Zone Random Write Area (ZRWA) for Alleviating Partial Parity Tax in ZNS RAID",

abstract = "The Zoned Namespace (ZNS) SSD is an innovative technology that aims to mitigate the block interface tax associated with conventional SSDs. However, constructing a RAID system using ZNS SSDs presents a significant challenge in managing partial parity for incomplete stripes. Previous research permanently logs partial parity in a limited number of reserved zones, which not only creates bottlenecks in throughput but also exacerbates write amplification, thereby reducing the device's lifetime. We refer to these inefficiencies as the partial parity tax. In this paper, we present ZRAID, a software ZNS RAID layer that leverages the newly added Zone Random Write Area (ZRWA) feature in the ZNS Command Set, to alleviate partial parity tax. ZRWA enables in-place updates within a confined area near the write pointer. ZRAID temporarily stores partial parity within the ZRWA of data zones. Thus, partial parity writes are distributed across multiple data zones, effectively eliminating throughput bottlenecks. Furthermore, any expired partial parity in the ZRWA is overwritten by subsequent data, avoiding unnecessary flash writes. With the introduction of ZRWA, ZRAID can leverage general schedulers, overcoming the queue depth limitations of ZNS-compatible schedulers. Our evaluation with actual ZNS SSDs demonstrates a significant improvement in write throughput: up to 34.7\\ in the fio microbenchmark, and an average of 14.5\\ in db\\bench on RocksDB, along with up to a 1.6x reduction in flash write amplification.",

keywords = "partial parity, raid, zone random write area (zrwa), zoned namespaces",

author = "Minwook Kim and Seongyeop Jeong and Kim, \\Jin Soo\\",

note = "Publisher Copyright: {\textcopyright} 2025 ACM.; 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025 ; Conference date: 30-03-2025 Through 03-04-2025",

year = "2025",

month = mar,

day = "30",

doi = "10.1145/3669940.3707248",

language = "English",

series = "International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS",

publisher = "Association for Computing Machinery",

pages = "1151--1165",

booktitle = "ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems",

}

Kim, M, Jeong, S & Kim, JS 2025, [ZRAID: Leveraging Zone Random Write Area (ZRWA) for Alleviating Partial Parity Tax in ZNS RAID](https://snu.elsevierpure.com/en/publications/zraid-leveraging-zone-random-write-area-zrwa-for-alleviating-part/). in *ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems.* International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS, vol. 1, Association for Computing Machinery, pp. 1151-1165, 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025, Rotterdam, Netherlands, 30/03/25. [https://doi.org/10.1145/3669940.3707248](https://doi.org/10.1145/3669940.3707248)

[**ZRAID: Leveraging Zone Random Write Area (ZRWA) for Alleviating Partial Parity Tax in ZNS RAID.**](https://snu.elsevierpure.com/en/publications/zraid-leveraging-zone-random-write-area-zrwa-for-alleviating-part/) / Kim, Minwook; Jeong, Seongyeop; Kim, Jin Soo.  
ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Association for Computing Machinery, 2025. p. 1151-1165 (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS; Vol. 1).

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution › peer-review

TY - GEN

T1 - ZRAID

T2 - 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025

AU - Kim, Minwook

AU - Jeong, Seongyeop

AU - Kim, Jin Soo

N1 - Publisher Copyright: © 2025 ACM.

PY - 2025/3/30

Y1 - 2025/3/30

N2 - The Zoned Namespace (ZNS) SSD is an innovative technology that aims to mitigate the block interface tax associated with conventional SSDs. However, constructing a RAID system using ZNS SSDs presents a significant challenge in managing partial parity for incomplete stripes. Previous research permanently logs partial parity in a limited number of reserved zones, which not only creates bottlenecks in throughput but also exacerbates write amplification, thereby reducing the device's lifetime. We refer to these inefficiencies as the partial parity tax. In this paper, we present ZRAID, a software ZNS RAID layer that leverages the newly added Zone Random Write Area (ZRWA) feature in the ZNS Command Set, to alleviate partial parity tax. ZRWA enables in-place updates within a confined area near the write pointer. ZRAID temporarily stores partial parity within the ZRWA of data zones. Thus, partial parity writes are distributed across multiple data zones, effectively eliminating throughput bottlenecks. Furthermore, any expired partial parity in the ZRWA is overwritten by subsequent data, avoiding unnecessary flash writes. With the introduction of ZRWA, ZRAID can leverage general schedulers, overcoming the queue depth limitations of ZNS-compatible schedulers. Our evaluation with actual ZNS SSDs demonstrates a significant improvement in write throughput: up to 34.7% in the fio microbenchmark, and an average of 14.5% in db_bench on RocksDB, along with up to a 1.6x reduction in flash write amplification.

AB - The Zoned Namespace (ZNS) SSD is an innovative technology that aims to mitigate the block interface tax associated with conventional SSDs. However, constructing a RAID system using ZNS SSDs presents a significant challenge in managing partial parity for incomplete stripes. Previous research permanently logs partial parity in a limited number of reserved zones, which not only creates bottlenecks in throughput but also exacerbates write amplification, thereby reducing the device's lifetime. We refer to these inefficiencies as the partial parity tax. In this paper, we present ZRAID, a software ZNS RAID layer that leverages the newly added Zone Random Write Area (ZRWA) feature in the ZNS Command Set, to alleviate partial parity tax. ZRWA enables in-place updates within a confined area near the write pointer. ZRAID temporarily stores partial parity within the ZRWA of data zones. Thus, partial parity writes are distributed across multiple data zones, effectively eliminating throughput bottlenecks. Furthermore, any expired partial parity in the ZRWA is overwritten by subsequent data, avoiding unnecessary flash writes. With the introduction of ZRWA, ZRAID can leverage general schedulers, overcoming the queue depth limitations of ZNS-compatible schedulers. Our evaluation with actual ZNS SSDs demonstrates a significant improvement in write throughput: up to 34.7% in the fio microbenchmark, and an average of 14.5% in db_bench on RocksDB, along with up to a 1.6x reduction in flash write amplification.

KW - partial parity

KW - raid

KW - zone random write area (zrwa)

KW - zoned namespaces

UR - https://www.scopus.com/pages/publications/105002370161

U2 - 10.1145/3669940.3707248

DO - 10.1145/3669940.3707248

M3 - Conference contribution

AN - SCOPUS:105002370161

T3 - International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS

SP - 1151

EP - 1165

BT - ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems

PB - Association for Computing Machinery

Y2 - 30 March 2025 through 3 April 2025

ER -

Kim M, Jeong S, Kim JS. [ZRAID: Leveraging Zone Random Write Area (ZRWA) for Alleviating Partial Parity Tax in ZNS RAID](https://snu.elsevierpure.com/en/publications/zraid-leveraging-zone-random-write-area-zrwa-for-alleviating-part/). In ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Association for Computing Machinery. 2025. p. 1151-1165. (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS). doi: 10.1145/3669940.3707248

- 
- [](https://www.facebook.com/sharer.php?u=https://snu.elsevierpure.com/en/publications/zraid-leveraging-zone-random-write-area-zrwa-for-alleviating-part/%3Futm_source%3Dfacebook%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3669940.3707248&p%5Bsummary%5D=Check+out+this+research+output+at+Seoul+National+University%3A+ZRAID%3A+Leveraging+Zone+Random+Write+Area+%28ZRWA%29+for+Alleviating+Partial+Parity+Tax+in+ZNS+RAID)
- [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMiIgaGVpZ2h0PSIyMiIgdmlld2JveD0iMCAwIDMwMCAyNzEiPgogICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Im0yMzYgMGg0NmwtMTAxIDExNSAxMTggMTU2aC05Mi42bC03Mi41LTk0LjgtODMgOTQuOGgtNDZsMTA3LTEyMy0xMTMtMTQ4aDk0LjlsNjUuNSA4Ni42em0tMTYuMSAyNDRoMjUuNWwtMTY1LTIxOGgtMjcuNHoiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)](https://twitter.com/intent/tweet?url=https://snu.elsevierpure.com/en/publications/zraid-leveraging-zone-random-write-area-zrwa-for-alleviating-part/%3Futm_source%3Dtwitter%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3669940.3707248&text=Check+out+this+research+output+at+Seoul+National+University%3A+ZRAID%3A+Leveraging+Zone+Random+Write+Area+%28ZRWA%29+for+Alleviating+Partial+Parity+Tax+in+ZNS+RAID)
- [](https://www.linkedin.com/shareArticle?mini=true&url=https://snu.elsevierpure.com/en/publications/zraid-leveraging-zone-random-write-area-zrwa-for-alleviating-part/%3Futm_source%3Dlinkedin%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3669940.3707248&summary=Check+out+this+research+output+at+Seoul+National+University%3A+ZRAID%3A+Leveraging+Zone+Random+Write+Area+%28ZRWA%29+for+Alleviating+Partial+Parity+Tax+in+ZNS+RAID)
- [](/cdn-cgi/l/email-protection#526d212730383731266f0800131b167761137760621e3724372033353b3c35776062083d3c3777606200333c363d3f77606205203b2637776062132037337760627a080005137b776062343d20776062133e3e37243b33263b3c35776062023320263b333e7760620233203b262b77606206332a7760623b3c776062081c0177606200131b1674303d362b6f113a3731397760623d2726776062263a3b21776062203721373320313a7760623d2726222726776062332677606201373d273e7760621c33263b3d3c333e776062073c3b243720213b262b7761137760620800131b167761137760621e3724372033353b3c35776062083d3c3777606200333c363d3f77606205203b2637776062132037337760627a080005137b776062343d20776062133e3e37243b33263b3c35776062023320263b333e7760620233203b262b77606206332a7760623b3c776062081c0177606200131b16722e723a26262221687d7d213c277c373e2137243b3720222720377c313d3f7d373c7d2227303e3b3133263b3d3c217d2820333b367f3e3724372033353b3c357f283d3c377f20333c363d3f7f25203b26377f332037337f282025337f343d207f333e3e37243b33263b3c357f223320267d6d27263f0d213d272031376f373f333b3e74333f226927263f0d3f37363b273f6f373f333b3e74333f226927263f0d31333f22333b353c6f213a3320373e3b3c39)
