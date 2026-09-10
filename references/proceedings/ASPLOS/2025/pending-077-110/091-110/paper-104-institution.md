<!-- 从 paper-104-institution.html 迁移的资料快照；原始 HTML SHA-256: fc89176446defbee502586567afb519b3cf9170be4e9df1fbebcfac7b89d80ed。 -->

# Faster Chaitin-like Register Allocation via Grammatical Decompositions of Control-Flow Graphs

Xuran CAI

, Amir Kafshdar Goharshady

, Hitarth SINGH

, Chun Kit LAM

- [Department of Computer Science and Engineering](https://researchportal.hkust.edu.hk/en/organisations/department-of-computer-science-and-engineering/)

Research output: Chapter in Book/Conference Proceeding/Report › Conference Paper published in a book › peer-review

[3   Link opens in a new tab](https://www.scopus.com/pages/publications/105002397393#tab=citedBy) Citations (Scopus)

- [ Overview ](/en/publications/faster-chaitin-like-register-allocation-via-grammatical-decomposi/)
- [ Fingerprint ](/en/publications/faster-chaitin-like-register-allocation-via-grammatical-decomposi/fingerprints/)

## Abstract

It is well-known that control-flow graphs (CFGs) of structured programs are sparse. This sparsity has been previously formalized in terms of graph parameters such as treewidth and pathwidth and used to design faster parameterized algorithms for numerous compiler optimization, model checking and program analysis tasks. In this work, we observe that the known graph sparsity parameters fail to exactly capture the kind of sparsity exhibited by CFGs. For example, while all structured CFGs have a treewidth of at most 7, not every graph with a treewidth of 7 or less is realizable as a CFG. As a result, current parameterized algorithms are solving the underlying graph problems over a more general family of graphs than the CFGs. To address this problem, we design a new but natural concept of graph decomposition based on a grammar that precisely captures the set of graphs that can be realized as CFGs of programs. We show that our notion of decomposition enables the same type of dynamic programming algorithms that are often used in treewidth/pathwidth-based methods. As two concrete applications, using our grammatical decomposition of CFGs, we provide asymptotically more efficient algorithms for two variants of the classical problem of register allocation as defined by Chaitin, i.e. assigning program variables to a limited number of registers such that variables with intersecting lifetimes are not assigned to the same register. Note that Chaitin's formulation of register allocation does not allow live-range splitting. Our algorithms are asymptotically faster not only in comparison with the non-parameterized solutions for these problems, but also compared to the state-of-the-art treewidth/pathwidth-based approaches in the literature. For minimum-cost register allocation over a fixed number of registers, we provide an algorithm with a runtime of O(\|G\| ·\|V\|^(5.r)) where \|G\| is the size of the program, is the set of program variables and r is the number of registers. In contrast, the previous treewidth-based algorithm had a runtime of O(\|G\|·\|V\|^(16.r)). For the decision problem of spill-free register allocation, our algorithm's runtime is O(\|G\| · r^(5.r+5)) whereas the previous works had a runtime of O(\|G\|· r^(16.r)). Finally, we provide extensive experimental results on spill-free register allocation, showcasing the scalability of our approach in comparison to previous state-of-the-art methods. Most notably, our approach can handle real-world instances with up to 20 registers, whereas previous works could only scale to 8. This is a significant improvement since most ubiquitous architectures, such as the x86 family, have 16 registers. For such architectures, our approach is the first-ever exact algorithm that scales up to solve the real-world instances of spill-free register allocation.

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

- control-flow graphs
- graph decompositions
- register allocation
- sparsity

## Access to Document

- [10.1145/3669940.3707286](https://doi.org/10.1145/3669940.3707286)Licence: [CC BY](http://creativecommons.org/licenses/by/4.0/)

## Other files and links

- [Link to publication in Web of Science](https://www.webofscience.com/wos/woscc/full-record/WOS:001481633300029)

- [Link to publication in OpenAlex](https://openalex.org/W4407218672)

##  Fingerprint

Dive into the research topics of 'Faster Chaitin-like Register Allocation via Grammatical Decompositions of Control-Flow Graphs'. Together they form a unique fingerprint.

-  Register Allocation Computer Science 100%
-  Control-Flow Graph Computer Science 100%
-  Sparsity Computer Science 37%
-  Program Variable Computer Science 25%
-  Compiler Optimization Computer Science 12%
-  Program Analysis Computer Science 12%
-  Experimental Result Computer Science 12%
-  Efficient Algorithm Computer Science 12%

[ View full fingerprint ](/en/publications/faster-chaitin-like-register-allocation-via-grammatical-decomposi/fingerprints/)

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

CAI, X., Goharshady, A. K., SINGH, H., & LAM, C. K. (2025). [Faster Chaitin-like Register Allocation via Grammatical Decompositions of Control-Flow Graphs](https://researchportal.hkust.edu.hk/en/publications/faster-chaitin-like-register-allocation-via-grammatical-decomposi/). In *ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems* (Vol. 1, pp. 463-477). (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS; Vol. 1). Association for Computing Machinery. [https://doi.org/10.1145/3669940.3707286](https://doi.org/10.1145/3669940.3707286)

CAI, Xuran ; Goharshady, Amir Kafshdar ; SINGH, Hitarth et al. / [**Faster Chaitin-like Register Allocation via Grammatical Decompositions of Control-Flow Graphs**](https://researchportal.hkust.edu.hk/en/publications/faster-chaitin-like-register-allocation-via-grammatical-decomposi/). ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Vol. 1 Association for Computing Machinery, 2025. pp. 463-477 (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS).

@inproceedings{2b1f0ce9401c4eb8bf72194fdd06b8bf,

title = "Faster Chaitin-like Register Allocation via Grammatical Decompositions of Control-Flow Graphs",

abstract = "It is well-known that control-flow graphs (CFGs) of structured programs are sparse. This sparsity has been previously formalized in terms of graph parameters such as treewidth and pathwidth and used to design faster parameterized algorithms for numerous compiler optimization, model checking and program analysis tasks. In this work, we observe that the known graph sparsity parameters fail to exactly capture the kind of sparsity exhibited by CFGs. For example, while all structured CFGs have a treewidth of at most 7, not every graph with a treewidth of 7 or less is realizable as a CFG. As a result, current parameterized algorithms are solving the underlying graph problems over a more general family of graphs than the CFGs. To address this problem, we design a new but natural concept of graph decomposition based on a grammar that precisely captures the set of graphs that can be realized as CFGs of programs. We show that our notion of decomposition enables the same type of dynamic programming algorithms that are often used in treewidth/pathwidth-based methods. As two concrete applications, using our grammatical decomposition of CFGs, we provide asymptotically more efficient algorithms for two variants of the classical problem of register allocation as defined by Chaitin, i.e. assigning program variables to a limited number of registers such that variables with intersecting lifetimes are not assigned to the same register. Note that Chaitin's formulation of register allocation does not allow live-range splitting. Our algorithms are asymptotically faster not only in comparison with the non-parameterized solutions for these problems, but also compared to the state-of-the-art treewidth/pathwidth-based approaches in the literature. For minimum-cost register allocation over a fixed number of registers, we provide an algorithm with a runtime of O(\|G\| ·\|V\|5.r) where \|G\| is the size of the program, is the set of program variables and r is the number of registers. In contrast, the previous treewidth-based algorithm had a runtime of O(\|G\|·\|V\|16.r). For the decision problem of spill-free register allocation, our algorithm's runtime is O(\|G\| · r5.r+5) whereas the previous works had a runtime of O(\|G\|· r16.r). Finally, we provide extensive experimental results on spill-free register allocation, showcasing the scalability of our approach in comparison to previous state-of-the-art methods. Most notably, our approach can handle real-world instances with up to 20 registers, whereas previous works could only scale to 8. This is a significant improvement since most ubiquitous architectures, such as the x86 family, have 16 registers. For such architectures, our approach is the first-ever exact algorithm that scales up to solve the real-world instances of spill-free register allocation.",

keywords = "control-flow graphs, graph decompositions, register allocation, sparsity",

author = "Xuran CAI and Goharshady, \\Amir Kafshdar\\ and Hitarth SINGH and LAM, \\Chun Kit\\",

note = "Publisher Copyright: {\textcopyright} 2025 ACM.; 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025 ; Conference date: 30-03-2025 Through 03-04-2025",

year = "2025",

month = mar,

day = "30",

doi = "10.1145/3669940.3707286",

language = "English",

volume = "1",

series = "International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS",

publisher = "Association for Computing Machinery",

pages = "463--477",

booktitle = "ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems",

}

CAI, X, Goharshady, AK, SINGH, H & LAM, CK 2025, [Faster Chaitin-like Register Allocation via Grammatical Decompositions of Control-Flow Graphs](https://researchportal.hkust.edu.hk/en/publications/faster-chaitin-like-register-allocation-via-grammatical-decomposi/). in *ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems.* vol. 1, International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS, vol. 1, Association for Computing Machinery, pp. 463-477, 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025, Rotterdam, Netherlands, 30/03/25. [https://doi.org/10.1145/3669940.3707286](https://doi.org/10.1145/3669940.3707286)

[**Faster Chaitin-like Register Allocation via Grammatical Decompositions of Control-Flow Graphs.**](https://researchportal.hkust.edu.hk/en/publications/faster-chaitin-like-register-allocation-via-grammatical-decomposi/) / CAI, Xuran; Goharshady, Amir Kafshdar; SINGH, Hitarth et al.  
ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Vol. 1 Association for Computing Machinery, 2025. p. 463-477 (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS; Vol. 1).

Research output: Chapter in Book/Conference Proceeding/Report › Conference Paper published in a book › peer-review

TY - GEN

T1 - Faster Chaitin-like Register Allocation via Grammatical Decompositions of Control-Flow Graphs

AU - CAI, Xuran

AU - Goharshady, Amir Kafshdar

AU - SINGH, Hitarth

AU - LAM, Chun Kit

N1 - Publisher Copyright: © 2025 ACM.

PY - 2025/3/30

Y1 - 2025/3/30

N2 - It is well-known that control-flow graphs (CFGs) of structured programs are sparse. This sparsity has been previously formalized in terms of graph parameters such as treewidth and pathwidth and used to design faster parameterized algorithms for numerous compiler optimization, model checking and program analysis tasks. In this work, we observe that the known graph sparsity parameters fail to exactly capture the kind of sparsity exhibited by CFGs. For example, while all structured CFGs have a treewidth of at most 7, not every graph with a treewidth of 7 or less is realizable as a CFG. As a result, current parameterized algorithms are solving the underlying graph problems over a more general family of graphs than the CFGs. To address this problem, we design a new but natural concept of graph decomposition based on a grammar that precisely captures the set of graphs that can be realized as CFGs of programs. We show that our notion of decomposition enables the same type of dynamic programming algorithms that are often used in treewidth/pathwidth-based methods. As two concrete applications, using our grammatical decomposition of CFGs, we provide asymptotically more efficient algorithms for two variants of the classical problem of register allocation as defined by Chaitin, i.e. assigning program variables to a limited number of registers such that variables with intersecting lifetimes are not assigned to the same register. Note that Chaitin's formulation of register allocation does not allow live-range splitting. Our algorithms are asymptotically faster not only in comparison with the non-parameterized solutions for these problems, but also compared to the state-of-the-art treewidth/pathwidth-based approaches in the literature. For minimum-cost register allocation over a fixed number of registers, we provide an algorithm with a runtime of O(\|G\| ·\|V\|5.r) where \|G\| is the size of the program, is the set of program variables and r is the number of registers. In contrast, the previous treewidth-based algorithm had a runtime of O(\|G\|·\|V\|16.r). For the decision problem of spill-free register allocation, our algorithm's runtime is O(\|G\| · r5.r+5) whereas the previous works had a runtime of O(\|G\|· r16.r). Finally, we provide extensive experimental results on spill-free register allocation, showcasing the scalability of our approach in comparison to previous state-of-the-art methods. Most notably, our approach can handle real-world instances with up to 20 registers, whereas previous works could only scale to 8. This is a significant improvement since most ubiquitous architectures, such as the x86 family, have 16 registers. For such architectures, our approach is the first-ever exact algorithm that scales up to solve the real-world instances of spill-free register allocation.

AB - It is well-known that control-flow graphs (CFGs) of structured programs are sparse. This sparsity has been previously formalized in terms of graph parameters such as treewidth and pathwidth and used to design faster parameterized algorithms for numerous compiler optimization, model checking and program analysis tasks. In this work, we observe that the known graph sparsity parameters fail to exactly capture the kind of sparsity exhibited by CFGs. For example, while all structured CFGs have a treewidth of at most 7, not every graph with a treewidth of 7 or less is realizable as a CFG. As a result, current parameterized algorithms are solving the underlying graph problems over a more general family of graphs than the CFGs. To address this problem, we design a new but natural concept of graph decomposition based on a grammar that precisely captures the set of graphs that can be realized as CFGs of programs. We show that our notion of decomposition enables the same type of dynamic programming algorithms that are often used in treewidth/pathwidth-based methods. As two concrete applications, using our grammatical decomposition of CFGs, we provide asymptotically more efficient algorithms for two variants of the classical problem of register allocation as defined by Chaitin, i.e. assigning program variables to a limited number of registers such that variables with intersecting lifetimes are not assigned to the same register. Note that Chaitin's formulation of register allocation does not allow live-range splitting. Our algorithms are asymptotically faster not only in comparison with the non-parameterized solutions for these problems, but also compared to the state-of-the-art treewidth/pathwidth-based approaches in the literature. For minimum-cost register allocation over a fixed number of registers, we provide an algorithm with a runtime of O(\|G\| ·\|V\|5.r) where \|G\| is the size of the program, is the set of program variables and r is the number of registers. In contrast, the previous treewidth-based algorithm had a runtime of O(\|G\|·\|V\|16.r). For the decision problem of spill-free register allocation, our algorithm's runtime is O(\|G\| · r5.r+5) whereas the previous works had a runtime of O(\|G\|· r16.r). Finally, we provide extensive experimental results on spill-free register allocation, showcasing the scalability of our approach in comparison to previous state-of-the-art methods. Most notably, our approach can handle real-world instances with up to 20 registers, whereas previous works could only scale to 8. This is a significant improvement since most ubiquitous architectures, such as the x86 family, have 16 registers. For such architectures, our approach is the first-ever exact algorithm that scales up to solve the real-world instances of spill-free register allocation.

KW - control-flow graphs

KW - graph decompositions

KW - register allocation

KW - sparsity

UR - https://www.webofscience.com/wos/woscc/full-record/WOS:001481633300029

UR - https://openalex.org/W4407218672

U2 - 10.1145/3669940.3707286

DO - 10.1145/3669940.3707286

M3 - Conference Paper published in a book

VL - 1

T3 - International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS

SP - 463

EP - 477

BT - ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems

PB - Association for Computing Machinery

T2 - 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025

Y2 - 30 March 2025 through 3 April 2025

ER -

CAI X, Goharshady AK, SINGH H, LAM CK. [Faster Chaitin-like Register Allocation via Grammatical Decompositions of Control-Flow Graphs](https://researchportal.hkust.edu.hk/en/publications/faster-chaitin-like-register-allocation-via-grammatical-decomposi/). In ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Vol. 1. Association for Computing Machinery. 2025. p. 463-477. (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS). doi: 10.1145/3669940.3707286

- 
- [](https://www.facebook.com/sharer.php?u=https://researchportal.hkust.edu.hk/en/publications/faster-chaitin-like-register-allocation-via-grammatical-decomposi/%3Futm_source%3Dfacebook%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3669940.3707286&p%5Bsummary%5D=Check+out+this+research+output+at+The+Hong+Kong+University+of+Science+and+Technology+Research+Portal%3A+Faster+Chaitin-like+Register+Allocation+via+Grammatical+Decompositions+of+Control-Flow+Graphs)
- [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMiIgaGVpZ2h0PSIyMiIgdmlld2JveD0iMCAwIDMwMCAyNzEiPgogICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Im0yMzYgMGg0NmwtMTAxIDExNSAxMTggMTU2aC05Mi42bC03Mi41LTk0LjgtODMgOTQuOGgtNDZsMTA3LTEyMy0xMTMtMTQ4aDk0LjlsNjUuNSA4Ni42em0tMTYuMSAyNDRoMjUuNWwtMTY1LTIxOGgtMjcuNHoiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)](https://twitter.com/intent/tweet?url=https://researchportal.hkust.edu.hk/en/publications/faster-chaitin-like-register-allocation-via-grammatical-decomposi/%3Futm_source%3Dtwitter%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3669940.3707286&text=Check+out+this+research+output+at+The+Hong+Kong+University+of+Science+and+Technology+Research+Portal%3A+Faster+Chaitin-like+Register+Allocation+via+Grammatical+Decompositions+of+Control-Flow+Graphs)
- [](https://www.linkedin.com/shareArticle?mini=true&url=https://researchportal.hkust.edu.hk/en/publications/faster-chaitin-like-register-allocation-via-grammatical-decomposi/%3Futm_source%3Dlinkedin%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3669940.3707286&summary=Check+out+this+research+output+at+The+Hong+Kong+University+of+Science+and+Technology+Research+Portal%3A+Faster+Chaitin-like+Register+Allocation+via+Grammatical+Decompositions+of+Control-Flow+Graphs)
- [](/cdn-cgi/l/email-protection#a996dadccbc3cccadd94efc8daddccdb8c9b99eac1c8c0ddc0c784c5c0c2cc8c9b99fbcccec0daddccdb8c9b99e8c5c5c6cac8ddc0c6c78c9b99dfc0c88c9b99eedbc8c4c4c8ddc0cac8c58c9b99edcccac6c4d9c6dac0ddc0c6c7da8c9b99c6cf8c9b99eac6c7dddbc6c584efc5c6de8c9b99eedbc8d9c1da8fcbc6cdd094eac1cccac28c9b99c6dcdd8c9b99ddc1c0da8c9b99dbccdaccc8dbcac18c9b99c6dcddd9dcdd8c9b99c8dd8c9b99fdc1cc8c9b99e1c6c7ce8c9b99e2c6c7ce8c9b99fcc7c0dfccdbdac0ddd08c9b99c6cf8c9b99facac0ccc7cacc8c9b99c8c7cd8c9b99fdcccac1c7c6c5c6ced08c9b99fbccdaccc8dbcac18c9b99f9c6dbddc8c58c9ae88c9b99efc8daddccdb8c9b99eac1c8c0ddc0c784c5c0c2cc8c9b99fbcccec0daddccdb8c9b99e8c5c5c6cac8ddc0c6c78c9b99dfc0c88c9b99eedbc8c4c4c8ddc0cac8c58c9b99edcccac6c4d9c6dac0ddc0c6c7da8c9b99c6cf8c9b99eac6c7dddbc6c584efc5c6de8c9b99eedbc8d9c1da89d589c1ddddd9da938686dbccdaccc8dbcac1d9c6dbddc8c587c1c2dcdadd87cccddc87c1c286ccc786d9dccbc5c0cac8ddc0c6c7da86cfc8daddccdb84cac1c8c0ddc0c784c5c0c2cc84dbcccec0daddccdb84c8c5c5c6cac8ddc0c6c784dfc0c884cedbc8c4c4c8ddc0cac8c584cdcccac6c4d9c6dac08696dcddc4f6dac6dcdbcacc94ccc4c8c0c58fc8c4d992dcddc4f6c4cccdc0dcc494ccc4c8c0c58fc8c4d992dcddc4f6cac8c4d9c8c0cec794dac1c8dbccc5c0c7c2)
