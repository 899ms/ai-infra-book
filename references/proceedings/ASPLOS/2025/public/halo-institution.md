<!-- 从 halo-institution.html 迁移的资料快照；原始 HTML SHA-256: 1f37a7a6a9634783edea51f641e117209f745504930d165eded8fd804d01ed0f。 -->

# HALO: Loop-aware Bootstrapping Management for Fully Homomorphic Encryption

Seonyoung Cheon

, Yongwoo Lee

, Hoyun Youm

, Dongkwan Kim

, Sungwoo Yun

, Kunmo Jeong

, Dongyoon Lee

, [Hanjun Kim](https://yonsei.elsevierpure.com/en/persons/hanjun-kim/)

- [Department of Electrical and Electronic Engineering](https://yonsei.elsevierpure.com/en/organisations/department-of-electrical-and-electronic-engineering/)

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

[3   Link opens in a new tab](https://www.scopus.com/pages/publications/105002386085#tab=citedBy) Citations (Scopus)

- [ Overview ](/en/publications/halo-loop-aware-bootstrapping-management-for-fully-homomorphic-en/)
- [ Fingerprint ](/en/publications/halo-loop-aware-bootstrapping-management-for-fully-homomorphic-en/fingerprints/)

## Abstract

Thanks to the computation ability on encrypted data, fully homomorphic encryption (FHE) is an attractive solution for privacy-preserving computation. Despite its advantages, FHE suffers from limited applicability in small programs because repeated FHE multiplications deplete the level of a ciphertext, which is finite. Bootstrapping reinitializes the level, thus allowing support for larger programs. However, its high computational overhead and the risk of level underflow require sophisticated bootstrapping placement, thereby increasing the programming burden. Although a recently proposed compiler automatizes the bootstrapping placement, its applicability is still limited due to lack of loop support. This work proposes the first loop-aware bootstrapping management compiler, called HALO, which optimizes bootstrapping placement in an FHE program with a loop. To correctly support bootstrapping-enabled loops, HALO matches encryption types and levels between live-in and loop-carried ciphertexts in the loops. To reduce the bootstrapping overheads, HALO decreases the number of bootstrapping within a loop body by packing the loop-carried variables to a single ciphertext, reduces wasted levels in a short loop body by unrolling the loop, and optimizes the bootstrapping latency by adjusting the target level of bootstrapping as needed. For seven machine learning programs with flat and nested loops, HALO shows 27% performance speedup compared to the state-of-the-art compiler that places bootstrapping operations on fully unrolled loops. In addition, HALO reduces the compilation time and code size by geometric means of 209.12x and 11.0x compared to the compiler, respectively.

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
| Period | 25/3/30 → 25/4/3 |

### Bibliographical note

Publisher Copyright:  
© 2025 ACM.

## All Science Journal Classification (ASJC) codes

- Software
- Information Systems
- Hardware and Architecture

## Access to Document

- [10.1145/3669940.3707275](https://doi.org/10.1145/3669940.3707275)

## Other files and links

- [Link to publication in Scopus](https://www.scopus.com/pages/publications/105002386085)

##  Fingerprint

Dive into the research topics of 'HALO: Loop-aware Bootstrapping Management for Fully Homomorphic Encryption'. Together they form a unique fingerprint.

-  Fully Homomorphic Encryption Computer Science 100%
-  Compiler Computer Science 80%
-  Ciphertext Computer Science 40%
-  Nested Loop Computer Science 20%
-  Time Compilation Computer Science 20%
-  Privacy Preserving Computer Science 20%
-  Encrypted Data Computer Science 20%
-  Machine Learning Computer Science 20%

[ View full fingerprint ](/en/publications/halo-loop-aware-bootstrapping-management-for-fully-homomorphic-en/fingerprints/)

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

Cheon, S., Lee, Y., Youm, H., Kim, D., Yun, S., Jeong, K., Lee, D.[, & Kim, H.](https://yonsei.elsevierpure.com/en/persons/hanjun-kim/) (2025). [HALO: Loop-aware Bootstrapping Management for Fully Homomorphic Encryption](https://yonsei.elsevierpure.com/en/publications/halo-loop-aware-bootstrapping-management-for-fully-homomorphic-en/). In *ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems* (pp. 572-585). (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS; Vol. 1). Association for Computing Machinery. [https://doi.org/10.1145/3669940.3707275](https://doi.org/10.1145/3669940.3707275)

Cheon, Seonyoung ; Lee, Yongwoo ; Youm, Hoyun et al. / [**HALO : Loop-aware Bootstrapping Management for Fully Homomorphic Encryption**](https://yonsei.elsevierpure.com/en/publications/halo-loop-aware-bootstrapping-management-for-fully-homomorphic-en/). ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Association for Computing Machinery, 2025. pp. 572-585 (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS).

@inproceedings{4c31a09cffb74af1882e8845f382724d,

title = "HALO: Loop-aware Bootstrapping Management for Fully Homomorphic Encryption",

abstract = "Thanks to the computation ability on encrypted data, fully homomorphic encryption (FHE) is an attractive solution for privacy-preserving computation. Despite its advantages, FHE suffers from limited applicability in small programs because repeated FHE multiplications deplete the level of a ciphertext, which is finite. Bootstrapping reinitializes the level, thus allowing support for larger programs. However, its high computational overhead and the risk of level underflow require sophisticated bootstrapping placement, thereby increasing the programming burden. Although a recently proposed compiler automatizes the bootstrapping placement, its applicability is still limited due to lack of loop support. This work proposes the first loop-aware bootstrapping management compiler, called HALO, which optimizes bootstrapping placement in an FHE program with a loop. To correctly support bootstrapping-enabled loops, HALO matches encryption types and levels between live-in and loop-carried ciphertexts in the loops. To reduce the bootstrapping overheads, HALO decreases the number of bootstrapping within a loop body by packing the loop-carried variables to a single ciphertext, reduces wasted levels in a short loop body by unrolling the loop, and optimizes the bootstrapping latency by adjusting the target level of bootstrapping as needed. For seven machine learning programs with flat and nested loops, HALO shows 27\\ performance speedup compared to the state-of-the-art compiler that places bootstrapping operations on fully unrolled loops. In addition, HALO reduces the compilation time and code size by geometric means of 209.12x and 11.0x compared to the compiler, respectively.",

keywords = "bootstrapping, ckks, compiler, fully homomorphic encryption, loop optimization, privacy-preserve machine learning",

author = "Seonyoung Cheon and Yongwoo Lee and Hoyun Youm and Dongkwan Kim and Sungwoo Yun and Kunmo Jeong and Dongyoon Lee and Hanjun Kim",

note = "Publisher Copyright: {\textcopyright} 2025 ACM.; 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025 ; Conference date: 30-03-2025 Through 03-04-2025",

year = "2025",

month = mar,

day = "30",

doi = "10.1145/3669940.3707275",

language = "English",

series = "International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS",

publisher = "Association for Computing Machinery",

pages = "572--585",

booktitle = "ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems",

}

Cheon, S, Lee, Y, Youm, H, Kim, D, Yun, S, Jeong, K, Lee, D[ & Kim, H](https://yonsei.elsevierpure.com/en/persons/hanjun-kim/) 2025, [HALO: Loop-aware Bootstrapping Management for Fully Homomorphic Encryption](https://yonsei.elsevierpure.com/en/publications/halo-loop-aware-bootstrapping-management-for-fully-homomorphic-en/). in *ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems.* International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS, vol. 1, Association for Computing Machinery, pp. 572-585, 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025, Rotterdam, Netherlands, 25/3/30. [https://doi.org/10.1145/3669940.3707275](https://doi.org/10.1145/3669940.3707275)

[**HALO: Loop-aware Bootstrapping Management for Fully Homomorphic Encryption.**](https://yonsei.elsevierpure.com/en/publications/halo-loop-aware-bootstrapping-management-for-fully-homomorphic-en/) / Cheon, Seonyoung; Lee, Yongwoo; Youm, Hoyun et al.  
ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Association for Computing Machinery, 2025. p. 572-585 (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS; Vol. 1).

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

TY - GEN

T1 - HALO

T2 - 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025

AU - Cheon, Seonyoung

AU - Lee, Yongwoo

AU - Youm, Hoyun

AU - Kim, Dongkwan

AU - Yun, Sungwoo

AU - Jeong, Kunmo

AU - Lee, Dongyoon

AU - Kim, Hanjun

N1 - Publisher Copyright: © 2025 ACM.

PY - 2025/3/30

Y1 - 2025/3/30

N2 - Thanks to the computation ability on encrypted data, fully homomorphic encryption (FHE) is an attractive solution for privacy-preserving computation. Despite its advantages, FHE suffers from limited applicability in small programs because repeated FHE multiplications deplete the level of a ciphertext, which is finite. Bootstrapping reinitializes the level, thus allowing support for larger programs. However, its high computational overhead and the risk of level underflow require sophisticated bootstrapping placement, thereby increasing the programming burden. Although a recently proposed compiler automatizes the bootstrapping placement, its applicability is still limited due to lack of loop support. This work proposes the first loop-aware bootstrapping management compiler, called HALO, which optimizes bootstrapping placement in an FHE program with a loop. To correctly support bootstrapping-enabled loops, HALO matches encryption types and levels between live-in and loop-carried ciphertexts in the loops. To reduce the bootstrapping overheads, HALO decreases the number of bootstrapping within a loop body by packing the loop-carried variables to a single ciphertext, reduces wasted levels in a short loop body by unrolling the loop, and optimizes the bootstrapping latency by adjusting the target level of bootstrapping as needed. For seven machine learning programs with flat and nested loops, HALO shows 27% performance speedup compared to the state-of-the-art compiler that places bootstrapping operations on fully unrolled loops. In addition, HALO reduces the compilation time and code size by geometric means of 209.12x and 11.0x compared to the compiler, respectively.

AB - Thanks to the computation ability on encrypted data, fully homomorphic encryption (FHE) is an attractive solution for privacy-preserving computation. Despite its advantages, FHE suffers from limited applicability in small programs because repeated FHE multiplications deplete the level of a ciphertext, which is finite. Bootstrapping reinitializes the level, thus allowing support for larger programs. However, its high computational overhead and the risk of level underflow require sophisticated bootstrapping placement, thereby increasing the programming burden. Although a recently proposed compiler automatizes the bootstrapping placement, its applicability is still limited due to lack of loop support. This work proposes the first loop-aware bootstrapping management compiler, called HALO, which optimizes bootstrapping placement in an FHE program with a loop. To correctly support bootstrapping-enabled loops, HALO matches encryption types and levels between live-in and loop-carried ciphertexts in the loops. To reduce the bootstrapping overheads, HALO decreases the number of bootstrapping within a loop body by packing the loop-carried variables to a single ciphertext, reduces wasted levels in a short loop body by unrolling the loop, and optimizes the bootstrapping latency by adjusting the target level of bootstrapping as needed. For seven machine learning programs with flat and nested loops, HALO shows 27% performance speedup compared to the state-of-the-art compiler that places bootstrapping operations on fully unrolled loops. In addition, HALO reduces the compilation time and code size by geometric means of 209.12x and 11.0x compared to the compiler, respectively.

KW - bootstrapping

KW - ckks

KW - compiler

KW - fully homomorphic encryption

KW - loop optimization

KW - privacy-preserve machine learning

UR - https://www.scopus.com/pages/publications/105002386085

UR - https://www.scopus.com/pages/publications/105002386085#tab=citedBy

U2 - 10.1145/3669940.3707275

DO - 10.1145/3669940.3707275

M3 - Conference contribution

AN - SCOPUS:105002386085

T3 - International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS

SP - 572

EP - 585

BT - ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems

PB - Association for Computing Machinery

Y2 - 30 March 2025 through 3 April 2025

ER -

Cheon S, Lee Y, Youm H, Kim D, Yun S, Jeong K et al. [HALO: Loop-aware Bootstrapping Management for Fully Homomorphic Encryption](https://yonsei.elsevierpure.com/en/publications/halo-loop-aware-bootstrapping-management-for-fully-homomorphic-en/). In ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Association for Computing Machinery. 2025. p. 572-585. (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS). doi: 10.1145/3669940.3707275

- 
- [](https://www.facebook.com/sharer.php?u=https://yonsei.elsevierpure.com/en/publications/halo-loop-aware-bootstrapping-management-for-fully-homomorphic-en/%3Futm_source%3Dfacebook%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3669940.3707275&p%5Bsummary%5D=Check+out+this+research+output+at+Yonsei+University%3A+HALO%3A+Loop-aware+Bootstrapping+Management+for+Fully+Homomorphic+Encryption)
- [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMiIgaGVpZ2h0PSIyMiIgdmlld2JveD0iMCAwIDMwMCAyNzEiPgogICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Im0yMzYgMGg0NmwtMTAxIDExNSAxMTggMTU2aC05Mi42bC03Mi41LTk0LjgtODMgOTQuOGgtNDZsMTA3LTEyMy0xMTMtMTQ4aDk0LjlsNjUuNSA4Ni42em0tMTYuMSAyNDRoMjUuNWwtMTY1LTIxOGgtMjcuNHoiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)](https://twitter.com/intent/tweet?url=https://yonsei.elsevierpure.com/en/publications/halo-loop-aware-bootstrapping-management-for-fully-homomorphic-en/%3Futm_source%3Dtwitter%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3669940.3707275&text=Check+out+this+research+output+at+Yonsei+University%3A+HALO%3A+Loop-aware+Bootstrapping+Management+for+Fully+Homomorphic+Encryption)
- [](https://www.linkedin.com/shareArticle?mini=true&url=https://yonsei.elsevierpure.com/en/publications/halo-loop-aware-bootstrapping-management-for-fully-homomorphic-en/%3Futm_source%3Dlinkedin%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3669940.3707275&summary=Check+out+this+research+output+at+Yonsei+University%3A+HALO%3A+Loop-aware+Bootstrapping+Management+for+Fully+Homomorphic+Encryption)
- [](/cdn-cgi/l/email-protection#e3dc90968189868097deaba2afacc6d0a2c6d1d3af8c8c93ce8294829186c6d1d3a18c8c979097918293938a8d84c6d1d3ae828d8284868e868d97c6d1d3858c91c6d1d3a5968f8f9ac6d1d3ab8c8e8c8e8c91938b8a80c6d1d3a68d80919a93978a8c8dc5818c879adea08b868088c6d1d38c9697c6d1d3978b8a90c6d1d3918690868291808bc6d1d38c9697939697c6d1d38297c6d1d3ba8c8d90868ac6d1d3b68d8a958691908a979ac6d0a2c6d1d3aba2afacc6d0a2c6d1d3af8c8c93ce8294829186c6d1d3a18c8c979097918293938a8d84c6d1d3ae828d8284868e868d97c6d1d3858c91c6d1d3a5968f8f9ac6d1d3ab8c8e8c8e8c91938b8a80c6d1d3a68d80919a93978a8c8dc39fc38b97979390d9cccc9a8c8d90868acd868f9086958a869193969186cd808c8ecc868dcc9396818f8a8082978a8c8d90cc8b828f8cce8f8c8c93ce8294829186ce818c8c979097918293938a8d84ce8e828d8284868e868d97ce858c91ce85968f8f9ace8b8c8e8c8e8c91938b8a80ce868dccdc96978ebc908c96918086de868e828a8fc5828e93d896978ebc8e86878a968ede868e828a8fc5828e93d896978ebc80828e93828a848dde908b8291868f8a8d88)
