<!-- 从 bigint-institution.html 迁移的资料快照；原始 HTML SHA-256: 0ae879871181410e8ac4a91555d931e299bf11faec3b546a9267d4184f3b32b1。 -->

# A Compiler-Like Framework for Optimizing Cryptographic Big Integer Multiplication on GPUs

Zhuoran Ji

, Jianyu Zhao

, [Zhaorui Zhang](https://research.polyu.edu.hk/en/persons/zhaorui-zhang/)

, Jiming Xu

, Shoumeng Yan

, Lei Ju

- [The Hong Kong Polytechnic University](https://research.polyu.edu.hk/en/organisations/the-hong-kong-polytechnic-university/)

Research output: Chapter in book / Conference proceeding › Conference article published in proceeding or book › Academic research › peer-review

[1   Link opens in a new tab](https://www.scopus.com/pages/publications/85213371575#tab=citedBy) Citation (Scopus)

- [ Overview ](/en/publications/a-compiler-like-framework-for-optimizing-cryptographic-big-intege/)
- [ Fingerprint ](/en/publications/a-compiler-like-framework-for-optimizing-cryptographic-big-intege/fingerprints/)

## Abstract

With the growth of digital data and rising security concerns, techniques for privacy-preserving computation have become increasingly essential. Big integer multiplication, pivotal for these applications, is compute-intensive but poses challenges for GPU acceleration due to its complexity and the need for application-specific tailored implementations. This paper presents IMCompiler, a compiler-like framework that automatically gen-erates optimized GPU kernels for integer multiplications used in cryptosystems. It features a frontend-IR-backend structure, where the Intermediate Representation (IR) employs a segmented integer multiplication algorithm to decouple architecture-specific optimizations from high-level parameters. The frontend can then easily translate integer multiplication with various high-level parameters into the IR, while the backend focuses on fine-tuning a single GPU kernel for each device, enabling automatic code generation. Moreover, we introduce a computation diagram to facilitate the analysis of parallelization strategies, inspiring many optimizations, including two-dimensional parallelization, tailored caching strategy, index transposing, and lazy carrying. Experiments show that IMCompiler achieves a 4.47× speedup compared to the widely used baseline and 1.42 × over Nvidia's official library. The speedup will be even higher for larger integers and higher-capacity GPUs.

[TABLE]

### Publication series

|  |  |
|----|----|
| Name | Proceedings of the Annual International Symposium on Microarchitecture, MICRO |
| ISSN (Print) | 1072-4451 |

### Conference

|  |  |
|----|----|
| Conference | 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024 |
| Country/Territory | United States |
| City | Austin |
| Period | 2/11/24 → 6/11/24 |

## Keywords

- big integer
- compiler
- cryptography
- GPU

## ASJC Scopus subject areas

- Hardware and Architecture

## More information

- [10.1109/MICRO61859.2024.00036](https://doi.org/10.1109/MICRO61859.2024.00036)

## Other files and links

- [Link to publication in Scopus](https://www.scopus.com/pages/publications/85213371575)

##  Fingerprint

Dive into the research topics of 'A Compiler-Like Framework for Optimizing Cryptographic Big Integer Multiplication on GPUs'. Together they form a unique fingerprint.

-  Graphics Processing Unit Computer Science 100%
-  Compiler Computer Science 100%
-  Big Integer Keyphrases 100%
-  Intermediate Representation Computer Science 60%
-  Parallelization Computer Science 40%
-  High Level Parameter Keyphrases 40%
-  Privacy Preserving Computer Science 20%
-  Security Concern Computer Science 20%

[ View full fingerprint ](/en/publications/a-compiler-like-framework-for-optimizing-cryptographic-big-intege/fingerprints/)

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

Ji, Z., Zhao, J.[, Zhang, Z.](https://research.polyu.edu.hk/en/persons/zhaorui-zhang/), Xu, J., Yan, S., & Ju, L. (2024). [A Compiler-Like Framework for Optimizing Cryptographic Big Integer Multiplication on GPUs](https://research.polyu.edu.hk/en/publications/a-compiler-like-framework-for-optimizing-cryptographic-big-intege/). In *Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024* (pp. 380-392). (Proceedings of the Annual International Symposium on Microarchitecture, MICRO). IEEE Computer Society. [https://doi.org/10.1109/MICRO61859.2024.00036](https://doi.org/10.1109/MICRO61859.2024.00036)

Ji, Zhuoran ; Zhao, Jianyu [ ; Zhang, Zhaorui](https://research.polyu.edu.hk/en/persons/zhaorui-zhang/) et al. / [**A Compiler-Like Framework for Optimizing Cryptographic Big Integer Multiplication on GPUs**](https://research.polyu.edu.hk/en/publications/a-compiler-like-framework-for-optimizing-cryptographic-big-intege/). Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024. IEEE Computer Society, 2024. pp. 380-392 (Proceedings of the Annual International Symposium on Microarchitecture, MICRO).

@inproceedings{cec1e34c98ff4bb996f5d9e9375a184e,

title = "A Compiler-Like Framework for Optimizing Cryptographic Big Integer Multiplication on GPUs",

abstract = "With the growth of digital data and rising security concerns, techniques for privacy-preserving computation have become increasingly essential. Big integer multiplication, pivotal for these applications, is compute-intensive but poses challenges for GPU acceleration due to its complexity and the need for application-specific tailored implementations. This paper presents IMCompiler, a compiler-like framework that automatically gen-erates optimized GPU kernels for integer multiplications used in cryptosystems. It features a frontend-IR-backend structure, where the Intermediate Representation (IR) employs a segmented integer multiplication algorithm to decouple architecture-specific optimizations from high-level parameters. The frontend can then easily translate integer multiplication with various high-level parameters into the IR, while the backend focuses on fine-tuning a single GPU kernel for each device, enabling automatic code generation. Moreover, we introduce a computation diagram to facilitate the analysis of parallelization strategies, inspiring many optimizations, including two-dimensional parallelization, tailored caching strategy, index transposing, and lazy carrying. Experiments show that IMCompiler achieves a 4.47{\texttimes} speedup compared to the widely used baseline and 1.42 {\texttimes} over Nvidia's official library. The speedup will be even higher for larger integers and higher-capacity GPUs.",

keywords = "big integer, compiler, cryptography, GPU",

author = "Zhuoran Ji and Jianyu Zhao and Zhaorui Zhang and Jiming Xu and Shoumeng Yan and Lei Ju",

note = "Publisher Copyright: {\textcopyright} 2024 IEEE.; 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024 ; Conference date: 02-11-2024 Through 06-11-2024",

year = "2024",

doi = "10.1109/MICRO61859.2024.00036",

language = "English",

series = "Proceedings of the Annual International Symposium on Microarchitecture, MICRO",

publisher = "IEEE Computer Society",

pages = "380--392",

booktitle = "Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024",

address = "United States",

}

Ji, Z, Zhao, J[, Zhang, Z](https://research.polyu.edu.hk/en/persons/zhaorui-zhang/), Xu, J, Yan, S & Ju, L 2024, [A Compiler-Like Framework for Optimizing Cryptographic Big Integer Multiplication on GPUs](https://research.polyu.edu.hk/en/publications/a-compiler-like-framework-for-optimizing-cryptographic-big-intege/). in *Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024.* Proceedings of the Annual International Symposium on Microarchitecture, MICRO, IEEE Computer Society, pp. 380-392, 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024, Austin, United States, 2/11/24. [https://doi.org/10.1109/MICRO61859.2024.00036](https://doi.org/10.1109/MICRO61859.2024.00036)

[**A Compiler-Like Framework for Optimizing Cryptographic Big Integer Multiplication on GPUs.**](https://research.polyu.edu.hk/en/publications/a-compiler-like-framework-for-optimizing-cryptographic-big-intege/) / Ji, Zhuoran; Zhao, Jianyu[; Zhang, Zhaorui](https://research.polyu.edu.hk/en/persons/zhaorui-zhang/) et al.  
Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024. IEEE Computer Society, 2024. p. 380-392 (Proceedings of the Annual International Symposium on Microarchitecture, MICRO).

Research output: Chapter in book / Conference proceeding › Conference article published in proceeding or book › Academic research › peer-review

TY - GEN

T1 - A Compiler-Like Framework for Optimizing Cryptographic Big Integer Multiplication on GPUs

AU - Ji, Zhuoran

AU - Zhao, Jianyu

AU - Zhang, Zhaorui

AU - Xu, Jiming

AU - Yan, Shoumeng

AU - Ju, Lei

N1 - Publisher Copyright: © 2024 IEEE.

PY - 2024

Y1 - 2024

N2 - With the growth of digital data and rising security concerns, techniques for privacy-preserving computation have become increasingly essential. Big integer multiplication, pivotal for these applications, is compute-intensive but poses challenges for GPU acceleration due to its complexity and the need for application-specific tailored implementations. This paper presents IMCompiler, a compiler-like framework that automatically gen-erates optimized GPU kernels for integer multiplications used in cryptosystems. It features a frontend-IR-backend structure, where the Intermediate Representation (IR) employs a segmented integer multiplication algorithm to decouple architecture-specific optimizations from high-level parameters. The frontend can then easily translate integer multiplication with various high-level parameters into the IR, while the backend focuses on fine-tuning a single GPU kernel for each device, enabling automatic code generation. Moreover, we introduce a computation diagram to facilitate the analysis of parallelization strategies, inspiring many optimizations, including two-dimensional parallelization, tailored caching strategy, index transposing, and lazy carrying. Experiments show that IMCompiler achieves a 4.47× speedup compared to the widely used baseline and 1.42 × over Nvidia's official library. The speedup will be even higher for larger integers and higher-capacity GPUs.

AB - With the growth of digital data and rising security concerns, techniques for privacy-preserving computation have become increasingly essential. Big integer multiplication, pivotal for these applications, is compute-intensive but poses challenges for GPU acceleration due to its complexity and the need for application-specific tailored implementations. This paper presents IMCompiler, a compiler-like framework that automatically gen-erates optimized GPU kernels for integer multiplications used in cryptosystems. It features a frontend-IR-backend structure, where the Intermediate Representation (IR) employs a segmented integer multiplication algorithm to decouple architecture-specific optimizations from high-level parameters. The frontend can then easily translate integer multiplication with various high-level parameters into the IR, while the backend focuses on fine-tuning a single GPU kernel for each device, enabling automatic code generation. Moreover, we introduce a computation diagram to facilitate the analysis of parallelization strategies, inspiring many optimizations, including two-dimensional parallelization, tailored caching strategy, index transposing, and lazy carrying. Experiments show that IMCompiler achieves a 4.47× speedup compared to the widely used baseline and 1.42 × over Nvidia's official library. The speedup will be even higher for larger integers and higher-capacity GPUs.

KW - big integer

KW - compiler

KW - cryptography

KW - GPU

UR - https://www.scopus.com/pages/publications/85213371575

U2 - 10.1109/MICRO61859.2024.00036

DO - 10.1109/MICRO61859.2024.00036

M3 - Conference article published in proceeding or book

AN - SCOPUS:85213371575

T3 - Proceedings of the Annual International Symposium on Microarchitecture, MICRO

SP - 380

EP - 392

BT - Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024

PB - IEEE Computer Society

T2 - 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024

Y2 - 2 November 2024 through 6 November 2024

ER -

Ji Z, Zhao J[, Zhang Z](https://research.polyu.edu.hk/en/persons/zhaorui-zhang/), Xu J, Yan S, Ju L. [A Compiler-Like Framework for Optimizing Cryptographic Big Integer Multiplication on GPUs](https://research.polyu.edu.hk/en/publications/a-compiler-like-framework-for-optimizing-cryptographic-big-intege/). In Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024. IEEE Computer Society. 2024. p. 380-392. (Proceedings of the Annual International Symposium on Microarchitecture, MICRO). doi: 10.1109/MICRO61859.2024.00036

- 
- [](https://www.facebook.com/sharer.php?u=https://research.polyu.edu.hk/en/publications/a-compiler-like-framework-for-optimizing-cryptographic-big-intege/%3Futm_source%3Dfacebook%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FMICRO61859.2024.00036&p%5Bsummary%5D=Check+out+this+research+output+at+PolyU+Scholars+Hub%3A+A+Compiler-Like+Framework+for+Optimizing+Cryptographic+Big+Integer+Multiplication+on+GPUs)
- [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMiIgaGVpZ2h0PSIyMiIgdmlld2JveD0iMCAwIDMwMCAyNzEiPgogICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Im0yMzYgMGg0NmwtMTAxIDExNSAxMTggMTU2aC05Mi42bC03Mi41LTk0LjgtODMgOTQuOGgtNDZsMTA3LTEyMy0xMTMtMTQ4aDk0LjlsNjUuNSA4Ni42em0tMTYuMSAyNDRoMjUuNWwtMTY1LTIxOGgtMjcuNHoiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)](https://twitter.com/intent/tweet?url=https://research.polyu.edu.hk/en/publications/a-compiler-like-framework-for-optimizing-cryptographic-big-intege/%3Futm_source%3Dtwitter%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FMICRO61859.2024.00036&text=Check+out+this+research+output+at+PolyU+Scholars+Hub%3A+A+Compiler-Like+Framework+for+Optimizing+Cryptographic+Big+Integer+Multiplication+on+GPUs)
- [](https://www.linkedin.com/shareArticle?mini=true&url=https://research.polyu.edu.hk/en/publications/a-compiler-like-framework-for-optimizing-cryptographic-big-intege/%3Futm_source%3Dlinkedin%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FMICRO61859.2024.00036&summary=Check+out+this+research+output+at+PolyU+Scholars+Hub%3A+A+Compiler-Like+Framework+for+Optimizing+Cryptographic+Big+Integer+Multiplication+on+GPUs)
- [](/cdn-cgi/l/email-protection#91aee2e4f3fbf4f2e5acd0b4a3a1d2fefce1f8fdf4e3bcddf8faf4b4a3a1d7e3f0fcf4e6fee3fab4a3a1f7fee3b4a3a1dee1e5f8fcf8ebf8fff6b4a3a1d2e3e8e1e5fef6e3f0e1f9f8f2b4a3a1d3f8f6b4a3a1d8ffe5f4f6f4e3b4a3a1dce4fde5f8e1fdf8f2f0e5f8feffb4a3a1feffb4a3a1d6c1c4e2b7f3fef5e8acd2f9f4f2fab4a3a1fee4e5b4a3a1e5f9f8e2b4a3a1e3f4e2f4f0e3f2f9b4a3a1fee4e5e1e4e5b4a3a1f0e5b4a3a1c1fefde8c4b4a3a1c2f2f9fefdf0e3e2b4a3a1d9e4f3b4a2d0b4a3a1d0b4a3a1d2fefce1f8fdf4e3bcddf8faf4b4a3a1d7e3f0fcf4e6fee3fab4a3a1f7fee3b4a3a1dee1e5f8fcf8ebf8fff6b4a3a1d2e3e8e1e5fef6e3f0e1f9f8f2b4a3a1d3f8f6b4a3a1d8ffe5f4f6f4e3b4a3a1dce4fde5f8e1fdf8f2f0e5f8feffb4a3a1feffb4a3a1d6c1c4e2b1edb1f9e5e5e1e2abbebee3f4e2f4f0e3f2f9bfe1fefde8e4bff4f5e4bff9fabef4ffbee1e4f3fdf8f2f0e5f8feffe2bef0bcf2fefce1f8fdf4e3bcfdf8faf4bcf7e3f0fcf4e6fee3fabcf7fee3bcfee1e5f8fcf8ebf8fff6bcf2e3e8e1e5fef6e3f0e1f9f8f2bcf3f8f6bcf8ffe5f4f6f4beaee4e5fccee2fee4e3f2f4acf4fcf0f8fdb7f0fce1aae4e5fccefcf4f5f8e4fcacf4fcf0f8fdb7f0fce1aae4e5fccef2f0fce1f0f8f6fface2f9f0e3f4fdf8fffa)
