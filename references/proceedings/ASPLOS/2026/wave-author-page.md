<!-- 从 wave-author-page.html 迁移的资料快照；原始 HTML SHA-256: 34bdb5a3fa63cdd1568ce4333c2da8a34bc1a65db6155ace0ebc9f9d207c724b。 -->

[Mengyuan (Marvin) Li](./index.html) [About](#myname) [Research](#interests) [SEPT Lab](sept_lab.html) [Publications](#mypublication) [Services](#myservices) [Teaching](25fall_699.html)

🌙 Dark

# Mengyuan (Marvin) Li

**Assistant Professor** [\[Google Scholar\]](https://scholar.google.com/citations?user=cgjqyuoAAAAJ&hl=en&oi=ao)

TEE, Confidential Computing, Verifiable AI, Side-Channel Attacks, and AI Systems Security

Thomas Lord Department of Computer Science  
Ming Hsieh Department of Electrical and Computer Engineering  
University of Southern California

E-mail: **mengyuanli@usc.edu**

[![Mengyuan (Marvin) Li](./files/mengyuan_2026.jpg)](./files/mengyuan_2026.jpg)

## About me

Mengyuan (Marvin) Li is an Assistant Professor of Computer Science Department at University of Southern California. He leads the [**SEPT Lab**](./sept_lab.html) (**SE**curity, **P**rivacy, and **T**rust), where the group focuses on cutting-edge research in systems and security and is actively looking for motivated PhD, MS, and undergraduate students. Prior to USC, he was a postdoc researcher in CSAIL at MIT (2022 - 2024), working with Prof. [Mengjia Yan](https://people.csail.mit.edu/mengjia/). Mengyuan graduated from [The Ohio State University (OSU)](http://www.osu.edu/) with a Ph.D. in Computer Science and Engineering in 2022, advised by Prof. [Yinqian Zhang](http://web.cse.ohio-state.edu/~yinqian/). Before coming to OSU, he graduated from [Shanghai Jiao Tong University (SJTU)](http://en.sjtu.edu.cn/) with the Bachelor's degree of Electronic Engineering.

## Research

My research focuses on the design of trustworthy computing environments through the tight integration of advanced hardware mechanisms and software systems. This co-design is essential for ensuring secure computation and data privacy, across platforms spanning personal devices to cloud AI systems. My group works on Trusted Execution Environments (TEE), confidential computing, verifiable AI, side-channel attacks, and broader AI systems security.

- • Uncovering, Understanding, and Defending Against System and Hardware Vulnerabilities, including cloud system security, CPU security, GPU security, and AI system security.

- • Software-Hardware Co-Design for Secure and Efficient AI Systems.

These topic pages summarize the main problems, representative papers, and teaching material behind the research directions that readers often search for directly.

### [TEE and Confidential Computing](./tee-confidential-computing.html)

Research on TEE-based systems and performance optimization, attacks on confidential computing platforms, and defenses for secure cloud and AI infrastructure.

**Keywords:** TEE, confidential computing, AMD SEV/SEV-SNP, SGX, confidential VMs/GPUs.

### [Verifiable AI](./verifiable-ai.html)

Research on verification of LLM inference, privacy-preserving model oversight, and system support for trustworthy AI deployment.

**Keywords:** verifiable AI, zero-knowledge verification, LLM inference, model oversight, trustworthy AI.

### [AI Agent Security](./ai-agent-security.html)

Research on using TEE and runtime monitoring to monitor agent execution and build trusted infrastructure for LLM systems and AI agents.

**Keywords:** AI agent security, TEE, runtime monitoring, trusted infrastructure, LLM systems, agent execution.

## News

2026

Paper "MC-ORAM: A Mask-Assisted and Counter-Based Non-Deterministic ORAM Inside VM-Based TEEs" accepted to ISCA'26.

2026

Paper "Hollow-LLM Attack: Computationally Trivial Weights in Zero-Knowledge Verification of LLM Inference" accepted to IEEE S&P'26.

2026

Paper "SCALE: Tackling Communication Bottlenecks in Confidential Multi-GPU ML" accepted to IEEE HPCA'26.

2026

Paper "WAVE: Leveraging Architecture Observation for Privacy-Preserving Model Oversight" accepted to ACM ASPLOS'26.

2025

Paper "Chekhov's Gun: Uncovering Hidden Risks in macOS Application-Sandboxed PID-Domain Services" accepted to ACM CCS'25.

2025

Paper "A Close Look at RMP Entry Caching and Its Security Implications in SEV-SNP" accepted to HASP'25.

2025

Paper "Few-Shot Graph Out-of-Distribution Detection with LLMs" published in Lecture Notes in Computer Science.

2024

Joined USC as Assistant Professor in the Thomas Lord Department of Computer Science.

2024

Paper "SoK: Understanding Design Choices and Pitfalls of Trusted Execution Environments" accepted to ACM ASIACCS'24.

2023

Paper "CipherH: Automated Detection of Ciphertext Side-channel Vulnerabilities" accepted to USENIX Security'23.

2022

Two papers accepted to IEEE S&P'22: "A Systematic Look at Ciphertext Side Channels" and "vSGX: Virtualizing SGX Enclaves on AMD SEV".

2021

Paper "CROSSLINE" accepted to ACM CCS'21 and received Best Paper Award (Runner-Up).

2021

Paper "CIPHERLEAKS" accepted to USENIX Security'21. AMD issued security bulletin and CVE.

## Publications

MC-ORAM: A Mask-Assisted and Counter-Based Non-Deterministic ORAM Inside VM-Based TEEs

Yongqin Wang, Rachit Rajat, Jonghyun Lee, Mengyuan Li, Murali Annavaram

IEEE/ACM International Symposium on Computer Architecture (ISCA) 2026

[\[link\]](index.html)

Hollow-LLM Attack: Computationally Trivial Weights in Zero-Knowledge Verification of LLM Inference

Chen Gong, Beijie Liu, Mengyuan Li

IEEE Symposium on Security and Privacy (S&P) 2026

[\[pdf\]](./files/hollow-llm.pdf) [\[reference\]](./files/hollow-llm.bib)

SCALE: Tackling Communication Bottlenecks in Confidential Multi-GPU ML

Joongun Park, Yongqin Wang, Huan Xu, Hanjiang Wu, Mengyuan Li, Tushar Krishna

IEEE International Symposium on High-Performance Computer Architecture (HPCA) 2026

[\[link\]](https://2026.hpca-conf.org/details/hpca-2026-main-conference/97/SCALE-Tackling-Communication-Bottlenecks-in-Confidential-Multi-GPU-ML)

WAVE: Leveraging Architecture Observation for Privacy-Preserving Model Oversight

Haoxuan Xu\*, Chen Gong\*, Beijie Liu\*, Haizhong Zheng, Beidi Chen, Mengyuan Li (\*equal contribution)

ACM International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS) 2026

[\[link\]](https://dl.acm.org/doi/epdf/10.1145/3779212.3790247)

Few-Shot Graph Out-of-Distribution Detection with LLMs

Haoyan Xu, Zhengtao Yao, Yushun Dong, Ziyi Wang, Ryan Rossi, Mengyuan Li, Yue Zhao

Joint European Conference on Machine Learning and Knowledge Discovery in Databases (ECML-PKDD) 2025

[\[link\]](https://link.springer.com/chapter/10.1007/978-3-032-06078-5_18)

Chekhov's Gun: Uncovering Hidden Risks in macOS Application-Sandboxed PID-Domain Services

Minghao Lin, Jiaxun Zhu, Tingting Yin, Zechao Cai, Guanxing Wen, Yanan Guo, Mengyuan Li

ACM Conference on Computer and Communications Security (CCS) 2025

[\[link\]](https://dl.acm.org/doi/abs/10.1145/3719027.3765205)

A Close Look at RMP Entry Caching and Its Security Implications in SEV-SNP

Alexis Bagia, Vincent Quentin Ulitzsch, Daniël Trujillo, Mengyuan Li, Mengjia Yan, Jean-Pierre Seifert

14th International Workshop on Hardware and Architectural Support for Security and Privacy (HASP) 2025

[\[link\]](https://dl.acm.org/doi/abs/10.1145/3768725.3768727)

Security bulletin from AMD [\[AMD-SB-3036\]](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-3036.html)

Ditto: Elastic Confidential VMs with Secure and Dynamic CPU Scaling

Shixuan Zhao\*, Mengyuan Li\*, Mengjia Yan, Zhiqiang Lin (\*equal contribution)

Under Submission

[\[arxiv\]](https://arxiv.org/pdf/2409.15542)

Bridge the Future: High-Performance Networks in Confidential VMs without Trusted I/O devices

Mengyuan Li, Shashvat Srivastava, Mengjia Yan

Under Submission

[\[arxiv\]](https://arxiv.org/pdf/2403.03360.pdf)

SoK: Understanding Design Choices and Pitfalls of Trusted Execution Environments

Mengyuan Li, Yuheng Yang, Guoxing Chen, Mengjia Yan, Yinqian Zhang

ACM ASIACCS'24

[\[pdf\]](./files/asiaccs_sok.pdf)

CipherH: Automated Detection of Ciphertext Side-channel Vulnerabilities in Cryptographic Implementations

Sen Deng, Mengyuan Li, Yining Tang, Shuai Wang, Shoumeng Yan, Yinqian Zhang

USENIX Security Symposium'23

[\[pdf\]](https://www.usenix.org/system/files/sec23summer_289-deng-prepub.pdf)

PWRLEAK: Exploiting Power Reporting Interface for Side-channel Attacks on AMD SEV

Wubing Wang, Mengyuan Li, Yinqian Zhang, Zhiqiang Lin

20th Conference on Detection of Intrusions and Malware & Vulnerability Assessment (DIMVA 2023)

[\[pdf\]](https://link.springer.com/chapter/10.1007/978-3-031-35504-2_3)

Security bulletin from AMD [\[AMD-SB-3004\]](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-3004.html), CVE [\[CVE-2023-20575\]](https://nvd.nist.gov/vuln/detail/CVE-2023-20575)

A Systematic Look at Ciphertext Side Channels

Mengyuan Li\*, Luca Wilke\*, Jan Wichelmann, Thomas Eisenbarth, Radu Teodorescu, Yinqian Zhang (\*equal contribution)

IEEE Symposium on Security and Privacy'22 (Acceptance rate: 57/407=14.0%)

[\[pdf\]](https://ieeexplore.ieee.org/document/9833768)

Security bulletin from AMD [\[AMD-SB-1033\]](https://www.amd.com/en/resources/product-security/bulletin/amd-sb-1033.html), CVE [\[CVE-2021-46744\]](https://nvd.nist.gov/vuln/detail/CVE-2021-46744)  
An official [\[White Paper\]](https://www.amd.com/system/files/documents/221404394-a_security_wp_final.pdf) from AMD for TEE developers and users to write code in a Ciphertext Side-channel-resistant way.

vSGX: Virtualizing SGX Enclaves on AMD SEV

Shixuan Zhao, Mengyuan Li, Yinqian Zhang, Zhiqiang Lin

IEEE Symposium on Security and Privacy'22 (Acceptance rate: 54/327=15.2%)

[\[pdf\]](https://ieeexplore.ieee.org/document/9833694)

TLB Poisoning Attacks on AMD Secure Encrypted Virtualization

Mengyuan Li, Yinqian Zhang, Huibo Wang, Kang Li, Yueqiang Chen

The 2021 Annual Computer Security Applications Conference (ACSAC 2021) (Acceptance rate: 56/326=15.2%)

[\[pdf\]](http://web.cse.ohio-state.edu/~li.7533/paper/acsac21-11.pdf)

Security bulletin from AMD [\[AMD-SB-1023\]](https://www.amd.com/en/corporate/product-security/bulletin/amd-sb-1023), CVE [\[CVE-2021-26340\]](https://nvd.nist.gov/vuln/detail/CVE-2021-26340), Announcement from [Lenovo](https://support.lenovo.com/us/en/product_security/LEN-75179)

CROSSLINE: Breaking "Security-by-Crash" based Memory Isolation in AMD SEV

Mengyuan Li, Yinqian Zhang, Zhiqiang Lin

ACM Conference on Computer and Communications Security'21, Nov. 2021 (Acceptance rate: 196/879=22.3%)

[\[pdf\]](https://arxiv.org/pdf/2008.00146.pdf) [\[bib\]](http://web.cse.ohio-state.edu/~li.7533/bib/crossline.bib)

Best Paper Awards (Runner-Ups) (14/879=1.6%) [\[plaque\]](https://raw.githubusercontent.com/acmccs2021/acm-ccs-2021/main/best-paper-awards-runner-up/ACM%20CCS%202021_BestPaperAward_RunnerUp%20(6).jpg) [\[link\]](https://sigsac.org/ccs/CCS2021/ccs-awards.html)

CIPHERLEAKS: Breaking Constant-time Cryptography on AMD SEV via the Ciphertext Side Channel

Mengyuan Li, Yinqian Zhang, Huibo Wang, Kang Li, Yueqiang Chen

USENIX Security Symposium'21, Virtual, Aug. 2021 (Acceptance rate: 248/1319=18.8%)

[\[pdf\]](https://www.usenix.org/system/files/sec21-li-mengyuan.pdf) [\[bib\]](http://web.cse.ohio-state.edu/~li.7533/bib/cipherleaks.bib) [\[Website\]](https://cipherleaks.com/)

AMD filed an embargo for the ciphertext side channel identified in the paper and announced a security [bulletin](https://www.amd.com/en/corporate/product-security/bulletin/amd-sb-1013) together with a hardware patch for SEV-SNP in August 2021 [\[CVE-2020-12966\]](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-12966)

Defeating speculative-execution attacks on SGX with HyperRace

Guoxing Chen, Mengyuan Li, Fengwei Zhang, Yinqian Zhang

IEEE Conference on Dependable and Secure Computing'19, Hangzhou, China, Nov. 2021

[\[pdf\]](http://web.cse.ohio-state.edu/~li.7533/paper/hyperrace-idsc19.pdf) [\[bib\]](http://web.cse.ohio-state.edu/~li.7533/bib/cipherleaks.bib)

Exploiting Unprotected I/O Operations in AMD's Secure Encrypted Virtualization

Mengyuan Li, Yinqian Zhang, Zhiqiang Lin, Yan Solihin

USENIX Security Symposium'19, Santa Clara, CA, Aug. 2019 (Acceptance rate: 113/697=16.2%)

[\[pdf\]](https://yinqian.org/papers/sec19b.pdf) [\[bib\]](http://web.cse.ohio-state.edu/~li.7533/bib/sevio.bib)

Peeking Behind the Curtains of Serverless Platforms

Liang Wang, Mengyuan Li, Yinqian Zhang, Thomas Ristenpart, Michael Swift

USENIX ATC'18, Boston, MA, USA, July. 2018 (Acceptance rate: 76/378=20.1%)

[\[pdf\]](https://www.usenix.org/system/files/conference/atc18/atc18-wang-liang.pdf) [\[Github\]](https://github.com/liangw89/faas_measure) [\[bib\]](http://web.cse.ohio-state.edu/~li.7533/bib/atc18.bib)

Stacco: Differentially Analyzing Side-Channel Traces for Detecting SSL/TLS Vulnerabilities in Secure Enclaves

Yuan Xiao, Mengyuan Li, Sanchuan Chen, Yinqian Zhang

ACM Conference on Computer and Communications Security'17, Dallas, TX, USA, Oct. 2017 (Acceptance rate: 151/843=17.9%)

[\[pdf\]](https://acmccs.github.io/papers/p859-xiaoA.pdf) [\[arxiv\]](https://arxiv.org/abs/1707.03473) [\[Github\]](https://github.com/OSUSecLab/Stacco) [\[bib\]](http://web.cse.ohio-state.edu/~li.7533/bib/ccs17.bib)

When CSI Meets Public WiFi: Inferring Your Mobile Phone Password via WiFi Signals

Mengyuan Li, Yan Meng, Junyi Liu, Haojin Zhu, Xiaohui Liang, Yao Liu, Na Ruan

ACM Conference on Computer and Communications Security'16, Vienna, Austria, Oct. 2016 (Acceptance rate: 137/831=16.5%)

[\[pdf\]](https://nsec.sjtu.edu.cn/publications/2016/When.pdf) [\[slides\]](https://nsec.sjtu.edu.cn/publications/2016/CCS%202016.pdf) [\[bib\]](http://web.cse.ohio-state.edu/~li.7533/bib/ccs16.bib) [\[Demo\]](https://nsec.sjtu.edu.cn/publications/2016/ccs2016.mp4) [\[Youtube\]](https://www.youtube.com/watch?v=ZJrTVU_eajE)

## Professional Services

### Program Committee

ACM Conference on Computer and Communications Security (CCS)

2024

IEEE European Symposium on Security and Privacy (EuroS&P)

2024

International Conference on Applied Cryptography and Network Security (ACNS)

2023

### Reviewer

IEEE Transactions on Dependable and Secure Computing (TDSC)

2021, 2022, 2023

IEEE Transactions on Parallel and Distributed Systems (TPDS)

2023

IEEE Transactions on Mobile Computing (TMC)

2021, 2022

IEEE/ACM Transactions on Networking (TNET)

2021, 2022

IEEE Transactions on Emerging Topics in Computing (TETCSI)

2022

### External Reviewer

IEEE Symposium on Security and Privacy (Oakland)

2020, 2022, 2023

ACM Conference on Computer and Communications Security (CCS)

2019, 2020, 2022, 2023

USENIX Security Symposium

2021

ISOC Network and Distributed System Security Symposium (NDSS)

2019

ACM Asia Conference on Computer and Communications Security (AsiaCCS)

2020

ACM Cloud Computing Security Workshop (CCSW)

2021

Mengyuan (Marvin) Li  ·  © 2026

![](https://app.ardalio.com/7/2/2213221.png)

 ·  University of Southern California  ·  [Google Scholar](https://scholar.google.com/citations?user=cgjqyuoAAAAJ&hl=en&oi=ao)  ·  [SEPT Lab](./sept_lab.html)  ·  <mengyuanli@usc.edu>
