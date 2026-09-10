<!-- 从 paper-108-institution.html 迁移的资料快照；原始 HTML SHA-256: c1079d7ed4ca69c0cd9f8112a312ed886a69bc09ba53d5712d8d1fbce473a67d。 -->

# Manta: Hybrid-Sensitive Type Inference Toward Type-Assisted Bug Detection for Stripped Binaries

Chengfeng Ye

, Yuandao Cai^(\*)

, Anshunkang Zhou

, [Heqing Huang](https://scholars.cityu.edu.hk/en/persons/heqhuang/)

, Hao Ling

, Charles Zhang

^(\*)Corresponding author for this work

- [Department of Computer Science](https://scholars.cityu.edu.hk/en/organisations/department-of-computer-science/)

Research output: Chapters, Conference Papers, Creative and Literary Works › RGC 32 - Refereed conference paper (with host publication) › peer-review

[2   Link opens in a new tab](https://www.scopus.com/pages/publications/105006975767#tab=citedBy) Citations (Scopus)

- [ Overview ](/en/publications/manta-hybrid-sensitive-type-inference-toward-type-assisted-bug-de/)
- [ Fingerprint ](/en/publications/manta-hybrid-sensitive-type-inference-toward-type-assisted-bug-de/fingerprints/)

## Abstract

Static binary bug detection has been a prominent approach for ensuring the security of binaries used in our daily lives. However, the type information lost in binaries prevents the improvement opportunity for a static analyzer to utilize type information to prune away infeasible facts and increase analysis precision. To make binary bug detection more practical with higher precision, in this work, we propose the first hybrid-sensitive type inference, Manta, that combines data-flow analysis with different sensitivities to complement each other and infer precise types for many variables. The inferred types are then used to assist with bug detection by pruning infeasible indirect call targets and data dependencies. Our experiments indicate Manta outperforms prior work by inferring types with 78.7% precision and 97.2% recall. Based on the inferred types, we can prune away 81.3% more infeasible indirect-call targets compared to existing type analysis techniques and perform program slicing on binaries with 61.1% similarity to that on source code. Moreover, Manta has led to 86 new developer-confirmed vulnerabilities in many popular IoT firmware, with 64 CVE/PSV IDs assigned.

[TABLE]

### Conference

[TABLE]

### Bibliographical note

Information for this record is provided by the author(s) concerned.

## Access Output

- [10.1145/3622781.3674177](https://doi.org/10.1145/3622781.3674177)

## Other Access Options

[Check CityUHK Library](https://julac.hosted.exlibrisgroup.com/openurl/852JULAC_CUH/852JULAC_CUH:CUH?ctx_ver=Z39.88-2004&ctx_tim=2026-09-09T02%3A24%3A09HKT&ctx_enc=info%3Aofi%2FencUTF-8&url_ver=Z39.88-2004&url_ctx_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Actx&rft.genre=bookitem&rft_val_fmt=info%3Aofi%2Fkev%3Afmt%3Abook&rfr_id=info%3Asid%2Fpure.atira.dk%3Apure&rft.atitle=Manta&rft_id=info%3Adoi%2F10.1145%2F3622781.3674177&rft.aulast=Ye&rft.aufirst=Chengfeng&rft.auinit=C&rft.date=2025-04-10&rft.isbn=979-8-4007-0391-1&rft.volume=4&rft.pages=170-187&rft.btitle=ASPLOS%20%2724%20-%20Proceedings%20of%20the%2029th%20ACM%20International%20Conference%20on%20Architectural%20Support%20for%20Programming%20Languages%20and%20Operating%20Systems&rft.pub=Association%20for%20Computing%20Machinery&rft.place=New%20York%2C%20NY)

## Permanent Link

- [Right click to copy link](https://hdl.handle.net/2031/fd5e0947-3e05-46a6-9c77-90eed8c982bc)

##  Fingerprint

Dive into the research topics of 'Manta: Hybrid-Sensitive Type Inference Toward Type-Assisted Bug Detection for Stripped Binaries'. Together they form a unique fingerprint.

-  Type Information Computer Science 100%
-  Type Inference Computer Science 100%
-  Analysis Technique Computer Science 50%
-  Data Dependency Computer Science 50%
-  Data-Flow Analysis Computer Science 50%
-  Source Coding Computer Science 50%
-  Inferring Type Computer Science 50%
-  Internet-Of-Things Computer Science 50%

[ View full fingerprint ](/en/publications/manta-hybrid-sensitive-type-inference-toward-type-assisted-bug-de/fingerprints/)

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

Ye, C., Cai, Y., Zhou, A.[, Huang, H.](https://scholars.cityu.edu.hk/en/persons/heqhuang/), Ling, H., & Zhang, C. (2025). [Manta: Hybrid-Sensitive Type Inference Toward Type-Assisted Bug Detection for Stripped Binaries](https://scholars.cityu.edu.hk/en/publications/manta-hybrid-sensitive-type-inference-toward-type-assisted-bug-de/). In *ASPLOS '24 - Proceedings of the 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems* (Vol. 4, pp. 170-187). Association for Computing Machinery. [https://doi.org/10.1145/3622781.3674177](https://doi.org/10.1145/3622781.3674177)

Ye, Chengfeng ; Cai, Yuandao ; Zhou, Anshunkang et al. / [**Manta : Hybrid-Sensitive Type Inference Toward Type-Assisted Bug Detection for Stripped Binaries**](https://scholars.cityu.edu.hk/en/publications/manta-hybrid-sensitive-type-inference-toward-type-assisted-bug-de/). ASPLOS '24 - Proceedings of the 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Vol. 4 New York, NY : Association for Computing Machinery, 2025. pp. 170-187

@inproceedings{fd5e09473e0546a69c7790eed8c982bc,

title = "Manta: Hybrid-Sensitive Type Inference Toward Type-Assisted Bug Detection for Stripped Binaries",

abstract = "Static binary bug detection has been a prominent approach for ensuring the security of binaries used in our daily lives. However, the type information lost in binaries prevents the improvement opportunity for a static analyzer to utilize type information to prune away infeasible facts and increase analysis precision. To make binary bug detection more practical with higher precision, in this work, we propose the first hybrid-sensitive type inference, Manta, that combines data-flow analysis with different sensitivities to complement each other and infer precise types for many variables. The inferred types are then used to assist with bug detection by pruning infeasible indirect call targets and data dependencies. Our experiments indicate Manta outperforms prior work by inferring types with 78.7\\ precision and 97.2\\ recall. Based on the inferred types, we can prune away 81.3\\ more infeasible indirect-call targets compared to existing type analysis techniques and perform program slicing on binaries with 61.1\\ similarity to that on source code. Moreover, Manta has led to 86 new developer-confirmed vulnerabilities in many popular IoT firmware, with 64 CVE/PSV IDs assigned.",

author = "Chengfeng Ye and Yuandao Cai and Anshunkang Zhou and Heqing Huang and Hao Ling and Charles Zhang",

note = "Information for this record is provided by the author(s) concerned.; 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS 2024), ASPLOS {\textquoteright}24 ; Conference date: 27-04-2024 Through 01-05-2024",

year = "2025",

month = apr,

day = "10",

doi = "10.1145/3622781.3674177",

language = "English",

isbn = "979-8-4007-0391-1",

volume = "4",

pages = "170--187",

booktitle = "ASPLOS '24 - Proceedings of the 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems",

publisher = "Association for Computing Machinery",

address = "United States",

url = "https://www.asplos-conference.org/asplos2024/",

}

Ye, C, Cai, Y, Zhou, A[, Huang, H](https://scholars.cityu.edu.hk/en/persons/heqhuang/), Ling, H & Zhang, C 2025, [Manta: Hybrid-Sensitive Type Inference Toward Type-Assisted Bug Detection for Stripped Binaries](https://scholars.cityu.edu.hk/en/publications/manta-hybrid-sensitive-type-inference-toward-type-assisted-bug-de/). in *ASPLOS '24 - Proceedings of the 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems.* vol. 4, Association for Computing Machinery, New York, NY, pp. 170-187, 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS 2024), San Diego, California, United States, 27/04/24. [https://doi.org/10.1145/3622781.3674177](https://doi.org/10.1145/3622781.3674177)

[**Manta: Hybrid-Sensitive Type Inference Toward Type-Assisted Bug Detection for Stripped Binaries.**](https://scholars.cityu.edu.hk/en/publications/manta-hybrid-sensitive-type-inference-toward-type-assisted-bug-de/) / Ye, Chengfeng; Cai, Yuandao; Zhou, Anshunkang et al.  
ASPLOS '24 - Proceedings of the 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Vol. 4 New York, NY: Association for Computing Machinery, 2025. p. 170-187.

Research output: Chapters, Conference Papers, Creative and Literary Works › RGC 32 - Refereed conference paper (with host publication) › peer-review

TY - GEN

T1 - Manta

T2 - 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS 2024)

AU - Ye, Chengfeng

AU - Cai, Yuandao

AU - Zhou, Anshunkang

AU - Huang, Heqing

AU - Ling, Hao

AU - Zhang, Charles

N1 - Information for this record is provided by the author(s) concerned.

PY - 2025/4/10

Y1 - 2025/4/10

N2 - Static binary bug detection has been a prominent approach for ensuring the security of binaries used in our daily lives. However, the type information lost in binaries prevents the improvement opportunity for a static analyzer to utilize type information to prune away infeasible facts and increase analysis precision. To make binary bug detection more practical with higher precision, in this work, we propose the first hybrid-sensitive type inference, Manta, that combines data-flow analysis with different sensitivities to complement each other and infer precise types for many variables. The inferred types are then used to assist with bug detection by pruning infeasible indirect call targets and data dependencies. Our experiments indicate Manta outperforms prior work by inferring types with 78.7% precision and 97.2% recall. Based on the inferred types, we can prune away 81.3% more infeasible indirect-call targets compared to existing type analysis techniques and perform program slicing on binaries with 61.1% similarity to that on source code. Moreover, Manta has led to 86 new developer-confirmed vulnerabilities in many popular IoT firmware, with 64 CVE/PSV IDs assigned.

AB - Static binary bug detection has been a prominent approach for ensuring the security of binaries used in our daily lives. However, the type information lost in binaries prevents the improvement opportunity for a static analyzer to utilize type information to prune away infeasible facts and increase analysis precision. To make binary bug detection more practical with higher precision, in this work, we propose the first hybrid-sensitive type inference, Manta, that combines data-flow analysis with different sensitivities to complement each other and infer precise types for many variables. The inferred types are then used to assist with bug detection by pruning infeasible indirect call targets and data dependencies. Our experiments indicate Manta outperforms prior work by inferring types with 78.7% precision and 97.2% recall. Based on the inferred types, we can prune away 81.3% more infeasible indirect-call targets compared to existing type analysis techniques and perform program slicing on binaries with 61.1% similarity to that on source code. Moreover, Manta has led to 86 new developer-confirmed vulnerabilities in many popular IoT firmware, with 64 CVE/PSV IDs assigned.

U2 - 10.1145/3622781.3674177

DO - 10.1145/3622781.3674177

M3 - RGC 32 - Refereed conference paper (with host publication)

SN - 979-8-4007-0391-1

VL - 4

SP - 170

EP - 187

BT - ASPLOS '24 - Proceedings of the 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems

PB - Association for Computing Machinery

CY - New York, NY

Y2 - 27 April 2024 through 1 May 2024

ER -

Ye C, Cai Y, Zhou A[, Huang H](https://scholars.cityu.edu.hk/en/persons/heqhuang/), Ling H, Zhang C. [Manta: Hybrid-Sensitive Type Inference Toward Type-Assisted Bug Detection for Stripped Binaries](https://scholars.cityu.edu.hk/en/publications/manta-hybrid-sensitive-type-inference-toward-type-assisted-bug-de/). In ASPLOS '24 - Proceedings of the 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Vol. 4. New York, NY: Association for Computing Machinery. 2025. p. 170-187 doi: 10.1145/3622781.3674177

- 
- [](https://www.facebook.com/sharer.php?u=https://scholars.cityu.edu.hk/en/publications/manta-hybrid-sensitive-type-inference-toward-type-assisted-bug-de/%3Futm_source%3Dfacebook%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3622781.3674177&p%5Bsummary%5D=Check+out+this+research+output+at+CityUHK+Scholars%3A+Manta%3A+Hybrid-Sensitive+Type+Inference+Toward+Type-Assisted+Bug+Detection+for+Stripped+Binaries)
- [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMiIgaGVpZ2h0PSIyMiIgdmlld2JveD0iMCAwIDMwMCAyNzEiPgogICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Im0yMzYgMGg0NmwtMTAxIDExNSAxMTggMTU2aC05Mi42bC03Mi41LTk0LjgtODMgOTQuOGgtNDZsMTA3LTEyMy0xMTMtMTQ4aDk0LjlsNjUuNSA4Ni42em0tMTYuMSAyNDRoMjUuNWwtMTY1LTIxOGgtMjcuNHoiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)](https://twitter.com/intent/tweet?url=https://scholars.cityu.edu.hk/en/publications/manta-hybrid-sensitive-type-inference-toward-type-assisted-bug-de/%3Futm_source%3Dtwitter%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3622781.3674177&text=Check+out+this+research+output+at+CityUHK+Scholars%3A+Manta%3A+Hybrid-Sensitive+Type+Inference+Toward+Type-Assisted+Bug+Detection+for+Stripped+Binaries)
- [](https://www.linkedin.com/shareArticle?mini=true&url=https://scholars.cityu.edu.hk/en/publications/manta-hybrid-sensitive-type-inference-toward-type-assisted-bug-de/%3Futm_source%3Dlinkedin%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3622781.3674177&summary=Check+out+this+research+output+at+CityUHK+Scholars%3A+Manta%3A+Hybrid-Sensitive+Type+Inference+Toward+Type-Assisted+Bug+Detection+for+Stripped+Binaries)
- [](/cdn-cgi/l/email-protection#6e511d1b0c040b0d1a53230f001a0f4b5d2f4b5c5e26170c1c070a433d0b001d071a07180b4b5c5e3a171e0b4b5c5e2700080b1c0b000d0b4b5c5e3a01190f1c0a4b5c5e3a171e0b432f1d1d071d1a0b0a4b5c5e2c1b094b5c5e2a0b1a0b0d1a0701004b5c5e08011c4b5c5e3d1a1c071e1e0b0a4b5c5e2c07000f1c070b1d480c010a17532d060b0d054b5c5e011b1a4b5c5e1a06071d4b5c5e1c0b1d0b0f1c0d064b5c5e011b1a1e1b1a4b5c5e0f1a4b5c5e2d071a173b26254b5c5e3d0d0601020f1c1d4b5d2f4b5c5e230f001a0f4b5d2f4b5c5e26170c1c070a433d0b001d071a07180b4b5c5e3a171e0b4b5c5e2700080b1c0b000d0b4b5c5e3a01190f1c0a4b5c5e3a171e0b432f1d1d071d1a0b0a4b5c5e2c1b094b5c5e2a0b1a0b0d1a0701004b5c5e08011c4b5c5e3d1a1c071e1e0b0a4b5c5e2c07000f1c070b1d4e124e061a1a1e1d5441411d0d0601020f1c1d400d071a171b400b0a1b400605410b00411e1b0c02070d0f1a0701001d41030f001a0f4306170c1c070a431d0b001d071a07180b431a171e0b430700080b1c0b000d0b431a01190f1c0a431a171e0b430f1d1d071d1a0b0a430c1b09430a0b41511b1a03311d011b1c0d0b530b030f0702480f031e551b1a0331030b0a071b03530b030f0702480f031e551b1a03310d0f031e0f070900531d060f1c0b02070005)
