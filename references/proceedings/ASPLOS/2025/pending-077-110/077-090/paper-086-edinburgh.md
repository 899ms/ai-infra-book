<!-- 从 paper-086-edinburgh.html 迁移的资料快照；原始 HTML SHA-256: 60df68477f65b466d1a98457acf35db2d169d62367915ef047f9a00095a602fd。 -->

# Hierarchical prefetching: A software-hardware instruction prefetcher for server applications

Tingji Zhang

, [Boris Grot](https://www.research.ed.ac.uk/en/persons/boris-grot/)

, Wenjian He

, Yashuai Lv

, Peng Qu^(\*)

, Fang Su

, Wenxin Wang

, Guowei Zhang

, Xuefeng Zhang

, Youhui Zhang^(\*)

^(\*)Corresponding author for this work

- [School of Informatics](https://www.research.ed.ac.uk/en/organisations/school-of-informatics/)
- [Computer Systems](https://www.research.ed.ac.uk/en/organisations/computer-systems/)
- [Institute for Computing Systems Architecture ](https://www.research.ed.ac.uk/en/organisations/institute-for-computing-systems-architecture/)

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

- [ Overview ](/en/publications/hierarchical-prefetching-a-software-hardware-instruction-prefetch/)
- [ Fingerprint ](/en/publications/hierarchical-prefetching-a-software-hardware-instruction-prefetch/fingerprints/)

## Abstract

The large working set of instructions in server-side applications causes a significant bottleneck in the front-end, even for high-performance processors equipped with fetch-directed instruction prefetching (FDIP). Prefetchers specifically designed for server scenarios typically rely on a record-and-replay mechanism that exploits the repetitiveness of instruction sequences. However, the efficacy of these techniques is compromised by discrepancies between actual and predicted control flows, resulting in loss of coverage and timeliness. This paper proposes Hierarchical Prefetching, a novel approach that tackles the limitations of existing prefetchers. It identifies common coarse-grained functionality blocks (called Bundles) within the server code and prefetches them as a whole. Bundles are significantly larger than typical prefetch targets, encompassing tens to hundreds of kilobytes of code. The approach combines simple software analysis of code for bundle formation and light-weight hardware for record-and-replay prefetching. The prefetcher requires under 2KB of on-chip storage by keeping most of the metadata in main memory. Experiments with 11 popular server workloads reveal that Hierarchical Prefetching significantly improves miss coverage and timeliness over prior techniques, achieving a 6.6% average performance gain over FDIP.

[TABLE]

### Conference

[TABLE]

## Keywords / Materials (for Non-textual outputs)

- front-end bottleneck
- instruction prefetching
- microarchitecture

## Access to Document

- [10.1145/3676641.3716260](https://doi.org/10.1145/3676641.3716260)Licence: [Creative Commons: Attribution (CC-BY)](http://creativecommons.org/licenses/by/4.0/)

&nbsp;

- [ZhangEtalASPLOS2025HierarchicalPrefetching](/files/521674398/ZhangEtalASPLOS2025HierarchicalPrefetching.pdf)Final published version, 1.44 MBLicence: [Creative Commons: Attribution (CC-BY)](http://creativecommons.org/licenses/by/4.0/)

##  Fingerprint

Dive into the research topics of 'Hierarchical prefetching: A software-hardware instruction prefetcher for server applications'. Together they form a unique fingerprint.

-  Server Application Computer Science 100%
-  prefetching Computer Science 100%
-  Prefetch Computer Science 33%
-  Performance Gain Computer Science 16%
-  Average Performance Computer Science 16%
-  Main Memory Computer Science 16%
-  Working Set Computer Science 16%
-  Control Flow Computer Science 16%

[ View full fingerprint ](/en/publications/hierarchical-prefetching-a-software-hardware-instruction-prefetch/fingerprints/)

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

Zhang, T.[, Grot, B.](https://www.research.ed.ac.uk/en/persons/boris-grot/), He, W., Lv, Y., Qu, P., Su, F., Wang, W., Zhang, G., Zhang, X., & Zhang, Y. (2025). [Hierarchical prefetching: A software-hardware instruction prefetcher for server applications](https://www.research.ed.ac.uk/en/publications/hierarchical-prefetching-a-software-hardware-instruction-prefetch/). In *Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems* (Vol. 2, pp. 529-544). Association for Computing Machinery (ACM). [https://doi.org/10.1145/3676641.3716260](https://doi.org/10.1145/3676641.3716260)

Zhang, Tingji [ ; Grot, Boris](https://www.research.ed.ac.uk/en/persons/boris-grot/) ; He, Wenjian et al. / [**Hierarchical prefetching : A software-hardware instruction prefetcher for server applications**](https://www.research.ed.ac.uk/en/publications/hierarchical-prefetching-a-software-hardware-instruction-prefetch/). Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Vol. 2 New York, NY, USA : Association for Computing Machinery (ACM), 2025. pp. 529-544

@inproceedings{efe681b7f3064b19b642d192115462a8,

title = "Hierarchical prefetching: A software-hardware instruction prefetcher for server applications",

abstract = "The large working set of instructions in server-side applications causes a significant bottleneck in the front-end, even for high-performance processors equipped with fetch-directed instruction prefetching (FDIP). Prefetchers specifically designed for server scenarios typically rely on a record-and-replay mechanism that exploits the repetitiveness of instruction sequences. However, the efficacy of these techniques is compromised by discrepancies between actual and predicted control flows, resulting in loss of coverage and timeliness. This paper proposes Hierarchical Prefetching, a novel approach that tackles the limitations of existing prefetchers. It identifies common coarse-grained functionality blocks (called Bundles) within the server code and prefetches them as a whole. Bundles are significantly larger than typical prefetch targets, encompassing tens to hundreds of kilobytes of code. The approach combines simple software analysis of code for bundle formation and light-weight hardware for record-and-replay prefetching. The prefetcher requires under 2KB of on-chip storage by keeping most of the metadata in main memory. Experiments with 11 popular server workloads reveal that Hierarchical Prefetching significantly improves miss coverage and timeliness over prior techniques, achieving a 6.6\\ average performance gain over FDIP.",

keywords = "front-end bottleneck, instruction prefetching, microarchitecture",

author = "Tingji Zhang and Boris Grot and Wenjian He and Yashuai Lv and Peng Qu and Fang Su and Wenxin Wang and Guowei Zhang and Xuefeng Zhang and Youhui Zhang",

year = "2025",

month = mar,

day = "30",

doi = "10.1145/3676641.3716260",

language = "English",

volume = "2",

pages = "529--544",

booktitle = "Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems",

publisher = "Association for Computing Machinery (ACM)",

address = "United States",

note = "The 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS '25 ; Conference date: 30-03-2025 Through 03-04-2025",

url = "https://www.asplos-conference.org/asplos2025/",

}

Zhang, T[, Grot, B](https://www.research.ed.ac.uk/en/persons/boris-grot/), He, W, Lv, Y, Qu, P, Su, F, Wang, W, Zhang, G, Zhang, X & Zhang, Y 2025, [Hierarchical prefetching: A software-hardware instruction prefetcher for server applications](https://www.research.ed.ac.uk/en/publications/hierarchical-prefetching-a-software-hardware-instruction-prefetch/). in *Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems.* vol. 2, Association for Computing Machinery (ACM), New York, NY, USA, pp. 529-544, The 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Rotterdam, Netherlands, 30/03/25. [https://doi.org/10.1145/3676641.3716260](https://doi.org/10.1145/3676641.3716260)

[**Hierarchical prefetching: A software-hardware instruction prefetcher for server applications.**](https://www.research.ed.ac.uk/en/publications/hierarchical-prefetching-a-software-hardware-instruction-prefetch/) / Zhang, Tingji[; Grot, Boris](https://www.research.ed.ac.uk/en/persons/boris-grot/); He, Wenjian et al.  
Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Vol. 2 New York, NY, USA: Association for Computing Machinery (ACM), 2025. p. 529-544.

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

TY - GEN

T1 - Hierarchical prefetching

T2 - The 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems

AU - Zhang, Tingji

AU - Grot, Boris

AU - He, Wenjian

AU - Lv, Yashuai

AU - Qu, Peng

AU - Su, Fang

AU - Wang, Wenxin

AU - Zhang, Guowei

AU - Zhang, Xuefeng

AU - Zhang, Youhui

N1 - Conference code: 30

PY - 2025/3/30

Y1 - 2025/3/30

N2 - The large working set of instructions in server-side applications causes a significant bottleneck in the front-end, even for high-performance processors equipped with fetch-directed instruction prefetching (FDIP). Prefetchers specifically designed for server scenarios typically rely on a record-and-replay mechanism that exploits the repetitiveness of instruction sequences. However, the efficacy of these techniques is compromised by discrepancies between actual and predicted control flows, resulting in loss of coverage and timeliness. This paper proposes Hierarchical Prefetching, a novel approach that tackles the limitations of existing prefetchers. It identifies common coarse-grained functionality blocks (called Bundles) within the server code and prefetches them as a whole. Bundles are significantly larger than typical prefetch targets, encompassing tens to hundreds of kilobytes of code. The approach combines simple software analysis of code for bundle formation and light-weight hardware for record-and-replay prefetching. The prefetcher requires under 2KB of on-chip storage by keeping most of the metadata in main memory. Experiments with 11 popular server workloads reveal that Hierarchical Prefetching significantly improves miss coverage and timeliness over prior techniques, achieving a 6.6% average performance gain over FDIP.

AB - The large working set of instructions in server-side applications causes a significant bottleneck in the front-end, even for high-performance processors equipped with fetch-directed instruction prefetching (FDIP). Prefetchers specifically designed for server scenarios typically rely on a record-and-replay mechanism that exploits the repetitiveness of instruction sequences. However, the efficacy of these techniques is compromised by discrepancies between actual and predicted control flows, resulting in loss of coverage and timeliness. This paper proposes Hierarchical Prefetching, a novel approach that tackles the limitations of existing prefetchers. It identifies common coarse-grained functionality blocks (called Bundles) within the server code and prefetches them as a whole. Bundles are significantly larger than typical prefetch targets, encompassing tens to hundreds of kilobytes of code. The approach combines simple software analysis of code for bundle formation and light-weight hardware for record-and-replay prefetching. The prefetcher requires under 2KB of on-chip storage by keeping most of the metadata in main memory. Experiments with 11 popular server workloads reveal that Hierarchical Prefetching significantly improves miss coverage and timeliness over prior techniques, achieving a 6.6% average performance gain over FDIP.

KW - front-end bottleneck

KW - instruction prefetching

KW - microarchitecture

U2 - 10.1145/3676641.3716260

DO - 10.1145/3676641.3716260

M3 - Conference contribution

VL - 2

SP - 529

EP - 544

BT - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems

PB - Association for Computing Machinery (ACM)

CY - New York, NY, USA

Y2 - 30 March 2025 through 3 April 2025

ER -

Zhang T[, Grot B](https://www.research.ed.ac.uk/en/persons/boris-grot/), He W, Lv Y, Qu P, Su F et al. [Hierarchical prefetching: A software-hardware instruction prefetcher for server applications](https://www.research.ed.ac.uk/en/publications/hierarchical-prefetching-a-software-hardware-instruction-prefetch/). In Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Vol. 2. New York, NY, USA: Association for Computing Machinery (ACM). 2025. p. 529-544 doi: 10.1145/3676641.3716260
