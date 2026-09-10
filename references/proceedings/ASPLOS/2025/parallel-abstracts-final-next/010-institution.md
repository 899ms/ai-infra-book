<!-- 从 010-institution.html 迁移的资料快照；原始 HTML SHA-256: 97b60b9cc4ae6ed6abb65996deb9007640aadf020b460f9b333c9fba7951dfa2。 -->

# Affinity-based Optimizations for TFHE on Processing-in-DRAM

Kevin Nam

, Heonhui Jung

, Hyunyoung Oh

, [Yunheung Paek](https://snu.elsevierpure.com/en/persons/yunheung-paek/)

- [College of Engineering](https://snu.elsevierpure.com/en/organisations/college-of-engineering/)
- [Department of Electrical and Computer Engineering](https://snu.elsevierpure.com/en/organisations/department-of-electrical-and-computer-engineering/)

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution › peer-review

[3   Link opens in a new tab](https://www.scopus.com/pages/publications/105002585422#tab=citedBy) Scopus citations

- [ Overview ](/en/publications/affinity-based-optimizations-for-tfhe-on-processing-in-dram/)
- [ Fingerprint ](/en/publications/affinity-based-optimizations-for-tfhe-on-processing-in-dram/fingerprints/)

## Abstract

Processing-in-memory (PIM) architectures are promising for accelerating intensive workloads due to their high internal bandwidth. This paper introduces a technique for accelerating Fully Homomorphic Encryption over the Torus (TFHE), a promising yet intensive application, on a realistic PIM system. Existing TFHE accelerators focus on exploiting parallelism, often overlooking data affinity, which leads to performance degradation in PIM due to excessive remote data accesses (RDAs). To address this, we present an affinity-based approach that optimizes the computation of TFHE on PIM. We apply algorithmic optimizations to TFHE, enabling PIM to effectively leverage its high internal bandwidth. We analyze the affinity patterns in the sub-tasks of TFHE and develop an offline scheduler that exploits our analysis to find optimal scheduling, minimizing RDAs while maintaining sufficient parallelism. To demonstrate the practicality of our work, we design a variant of an existing PIM-HBM device with minimal hardware modifications, and perform evaluations over a real FPGA-based PIM system. Our experiments demonstrate that our affinity-based optimizations outperform prior TFHE accelerators by 4.24-209× for real-world benchmarks.

[TABLE]

### Publication series

|  |  |
|----|----|
| Name | International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS |
| Volume | 2 |

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

- homomorphic encryption
- pim
- tfhe

## Access to Document

- [10.1145/3676641.3716246](https://doi.org/10.1145/3676641.3716246)

## Other files and links

- [Link to publication in Scopus](https://www.scopus.com/pages/publications/105002585422)

##  Fingerprint

Dive into the research topics of 'Affinity-based Optimizations for TFHE on Processing-in-DRAM'. Together they form a unique fingerprint.

-  In-Memory Processing Computer Science 100%
-  Data Access Computer Science 50%
-  Parallelism Computer Science 50%
-  Memory System Computer Science 50%
-  Memory Architecture Computer Science 25%
-  Performance Degradation Computer Science 25%
-  Field Programmable Gate Array Computer Science 25%
-  Intensive Application Computer Science 25%

[ View full fingerprint ](/en/publications/affinity-based-optimizations-for-tfhe-on-processing-in-dram/fingerprints/)

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

Nam, K., Jung, H., Oh, H.[, & Paek, Y.](https://snu.elsevierpure.com/en/persons/yunheung-paek/) (2025). [Affinity-based Optimizations for TFHE on Processing-in-DRAM](https://snu.elsevierpure.com/en/publications/affinity-based-optimizations-for-tfhe-on-processing-in-dram/). In *ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems* (pp. 16-31). (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS; Vol. 2). Association for Computing Machinery. [https://doi.org/10.1145/3676641.3716246](https://doi.org/10.1145/3676641.3716246)

Nam, Kevin ; Jung, Heonhui ; Oh, Hyunyoung et al. / [**Affinity-based Optimizations for TFHE on Processing-in-DRAM**](https://snu.elsevierpure.com/en/publications/affinity-based-optimizations-for-tfhe-on-processing-in-dram/). ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Association for Computing Machinery, 2025. pp. 16-31 (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS).

@inproceedings{a4077578b3d04f259ec51481f3590eb0,

title = "Affinity-based Optimizations for TFHE on Processing-in-DRAM",

abstract = "Processing-in-memory (PIM) architectures are promising for accelerating intensive workloads due to their high internal bandwidth. This paper introduces a technique for accelerating Fully Homomorphic Encryption over the Torus (TFHE), a promising yet intensive application, on a realistic PIM system. Existing TFHE accelerators focus on exploiting parallelism, often overlooking data affinity, which leads to performance degradation in PIM due to excessive remote data accesses (RDAs). To address this, we present an affinity-based approach that optimizes the computation of TFHE on PIM. We apply algorithmic optimizations to TFHE, enabling PIM to effectively leverage its high internal bandwidth. We analyze the affinity patterns in the sub-tasks of TFHE and develop an offline scheduler that exploits our analysis to find optimal scheduling, minimizing RDAs while maintaining sufficient parallelism. To demonstrate the practicality of our work, we design a variant of an existing PIM-HBM device with minimal hardware modifications, and perform evaluations over a real FPGA-based PIM system. Our experiments demonstrate that our affinity-based optimizations outperform prior TFHE accelerators by 4.24-209{\texttimes} for real-world benchmarks.",

keywords = "homomorphic encryption, pim, tfhe",

author = "Kevin Nam and Heonhui Jung and Hyunyoung Oh and Yunheung Paek",

note = "Publisher Copyright: {\textcopyright} 2025 ACM.; 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025 ; Conference date: 30-03-2025 Through 03-04-2025",

year = "2025",

month = mar,

day = "30",

doi = "10.1145/3676641.3716246",

language = "English",

series = "International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS",

publisher = "Association for Computing Machinery",

pages = "16--31",

booktitle = "ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems",

}

Nam, K, Jung, H, Oh, H[ & Paek, Y](https://snu.elsevierpure.com/en/persons/yunheung-paek/) 2025, [Affinity-based Optimizations for TFHE on Processing-in-DRAM](https://snu.elsevierpure.com/en/publications/affinity-based-optimizations-for-tfhe-on-processing-in-dram/). in *ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems.* International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS, vol. 2, Association for Computing Machinery, pp. 16-31, 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025, Rotterdam, Netherlands, 30/03/25. [https://doi.org/10.1145/3676641.3716246](https://doi.org/10.1145/3676641.3716246)

[**Affinity-based Optimizations for TFHE on Processing-in-DRAM.**](https://snu.elsevierpure.com/en/publications/affinity-based-optimizations-for-tfhe-on-processing-in-dram/) / Nam, Kevin; Jung, Heonhui; Oh, Hyunyoung et al.  
ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Association for Computing Machinery, 2025. p. 16-31 (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS; Vol. 2).

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution › peer-review

TY - GEN

T1 - Affinity-based Optimizations for TFHE on Processing-in-DRAM

AU - Nam, Kevin

AU - Jung, Heonhui

AU - Oh, Hyunyoung

AU - Paek, Yunheung

N1 - Publisher Copyright: © 2025 ACM.

PY - 2025/3/30

Y1 - 2025/3/30

N2 - Processing-in-memory (PIM) architectures are promising for accelerating intensive workloads due to their high internal bandwidth. This paper introduces a technique for accelerating Fully Homomorphic Encryption over the Torus (TFHE), a promising yet intensive application, on a realistic PIM system. Existing TFHE accelerators focus on exploiting parallelism, often overlooking data affinity, which leads to performance degradation in PIM due to excessive remote data accesses (RDAs). To address this, we present an affinity-based approach that optimizes the computation of TFHE on PIM. We apply algorithmic optimizations to TFHE, enabling PIM to effectively leverage its high internal bandwidth. We analyze the affinity patterns in the sub-tasks of TFHE and develop an offline scheduler that exploits our analysis to find optimal scheduling, minimizing RDAs while maintaining sufficient parallelism. To demonstrate the practicality of our work, we design a variant of an existing PIM-HBM device with minimal hardware modifications, and perform evaluations over a real FPGA-based PIM system. Our experiments demonstrate that our affinity-based optimizations outperform prior TFHE accelerators by 4.24-209× for real-world benchmarks.

AB - Processing-in-memory (PIM) architectures are promising for accelerating intensive workloads due to their high internal bandwidth. This paper introduces a technique for accelerating Fully Homomorphic Encryption over the Torus (TFHE), a promising yet intensive application, on a realistic PIM system. Existing TFHE accelerators focus on exploiting parallelism, often overlooking data affinity, which leads to performance degradation in PIM due to excessive remote data accesses (RDAs). To address this, we present an affinity-based approach that optimizes the computation of TFHE on PIM. We apply algorithmic optimizations to TFHE, enabling PIM to effectively leverage its high internal bandwidth. We analyze the affinity patterns in the sub-tasks of TFHE and develop an offline scheduler that exploits our analysis to find optimal scheduling, minimizing RDAs while maintaining sufficient parallelism. To demonstrate the practicality of our work, we design a variant of an existing PIM-HBM device with minimal hardware modifications, and perform evaluations over a real FPGA-based PIM system. Our experiments demonstrate that our affinity-based optimizations outperform prior TFHE accelerators by 4.24-209× for real-world benchmarks.

KW - homomorphic encryption

KW - pim

KW - tfhe

UR - https://www.scopus.com/pages/publications/105002585422

U2 - 10.1145/3676641.3716246

DO - 10.1145/3676641.3716246

M3 - Conference contribution

AN - SCOPUS:105002585422

T3 - International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS

SP - 16

EP - 31

BT - ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems

PB - Association for Computing Machinery

T2 - 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025

Y2 - 30 March 2025 through 3 April 2025

ER -

Nam K, Jung H, Oh H[, Paek Y](https://snu.elsevierpure.com/en/persons/yunheung-paek/). [Affinity-based Optimizations for TFHE on Processing-in-DRAM](https://snu.elsevierpure.com/en/publications/affinity-based-optimizations-for-tfhe-on-processing-in-dram/). In ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Association for Computing Machinery. 2025. p. 16-31. (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS). doi: 10.1145/3676641.3716246

- 
- [](https://www.facebook.com/sharer.php?u=https://snu.elsevierpure.com/en/publications/affinity-based-optimizations-for-tfhe-on-processing-in-dram/%3Futm_source%3Dfacebook%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3676641.3716246&p%5Bsummary%5D=Check+out+this+research+output+at+Seoul+National+University%3A+Affinity-based+Optimizations+for+TFHE+on+Processing-in-DRAM)
- [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMiIgaGVpZ2h0PSIyMiIgdmlld2JveD0iMCAwIDMwMCAyNzEiPgogICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Im0yMzYgMGg0NmwtMTAxIDExNSAxMTggMTU2aC05Mi42bC03Mi41LTk0LjgtODMgOTQuOGgtNDZsMTA3LTEyMy0xMTMtMTQ4aDk0LjlsNjUuNSA4Ni42em0tMTYuMSAyNDRoMjUuNWwtMTY1LTIxOGgtMjcuNHoiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)](https://twitter.com/intent/tweet?url=https://snu.elsevierpure.com/en/publications/affinity-based-optimizations-for-tfhe-on-processing-in-dram/%3Futm_source%3Dtwitter%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3676641.3716246&text=Check+out+this+research+output+at+Seoul+National+University%3A+Affinity-based+Optimizations+for+TFHE+on+Processing-in-DRAM)
- [](https://www.linkedin.com/shareArticle?mini=true&url=https://snu.elsevierpure.com/en/publications/affinity-based-optimizations-for-tfhe-on-processing-in-dram/%3Futm_source%3Dlinkedin%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3676641.3716246&summary=Check+out+this+research+output+at+Seoul+National+University%3A+Affinity-based+Optimizations+for+TFHE+on+Processing-in-DRAM)
- [](/cdn-cgi/l/email-protection#57682422353d3234236a1631313e393e232e7a35362432337265671827233e3a3e2d36233e38392472656731382572656703111f127265673839726567072538343224243e39307a3e397a1305161a713538332e6a143f32343c726567382223726567233f3e24726567253224323625343f7265673822232722237265673623726567043238223b7265671936233e3839363b72656702393e213225243e232e7264167265671631313e393e232e7a35362432337265671827233e3a3e2d36233e38392472656731382572656703111f127265673839726567072538343224243e39307a3e397a1305161a772b773f232327246d787824392279323b2432213e3225272225327934383a783239782722353b3e3436233e383924783631313e393e232e7a35362432337a3827233e3a3e2d36233e3839247a3138257a23313f327a38397a272538343224243e39307a3e397a3325363a786822233a082438222534326a323a363e3b71363a276c22233a083a32333e223a6a323a363e3b71363a276c22233a0834363a27363e30396a243f3625323b3e393c)
