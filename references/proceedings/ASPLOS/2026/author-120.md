<!-- 从 author-120.html 迁移的资料快照；原始 HTML SHA-256: 4cc13f97a117213b601cfa225d9b91962ebfb734682fd9ad7a7bdb8aa3949bcd。 -->

![Ming Liu](img/mgliu.jpg)

mgliu

I am an Assistant Professor in the [Computer Sciences Department](https://www.cs.wisc.edu) at the [University of Wisconsin-Madison](https://www.wisc.edu) (since 2021). I’m a member of the [NetLab](https://netlab.cs.wisc.edu) and [madNets](https://madnets.cs.wisc.edu) groups. I study networking and systems, with a focus on building efficient, robust, and practical computing systems for emerging hardware. My research spans two complementary directions. The first, **HW4Net**, explores how modern hardware communication fabrics, such as load-store interconnects and programmable networks, reshape the design of networked systems. The second, **Net4HW**, develops networking and system support for new hardware architectures, including chiplet-based SoCs, domain-specific accelerators, and disaggregated storage.

**I am actively looking for students. If you are interested, feel free to email me.**

### Research

Recently, we build applications, systems, protocols, and utilities for rack/cluster-scale infrastructures.

- **Scale-(In\|Up) Load-Store Interconnect**
  - Projects: [ChipletNet](proj-chipletnet.html), [SD-LSI](proj-sdlsi.html)
  - [cSwitch]() enhances Linux scheduling via a chiplet-centric switching architecture ([SOSP’26](https://sigops.org/s/conferences/sosp/2026/)).
  - [PingPoint](papers/PingPoint-sigcomm26.pdf) dissects communication behaviors of the Accelerator Chiplet Network ([SIGCOMM’26](https://conferences.sigcomm.org/sigcomm/2026/)).
  - [MemChannel](papers/MemChannel-nsdi26.pdf) develops a CSFQ-inspired transport layer for switched CXL memory pooling ([NSDI’26](https://www.usenix.org/conference/nsdi26)).
  - [PathFinder](papers/pathfinder-sigcomm25.pdf) tracks and analyzes `CXL.mem` using Intel PMUs ([SIGCOMM’25](https://conferences.sigcomm.org/sigcomm/2025/)).
  - [MegaStation](papers/MegaStation-nsdi25.pdf) realizes the MIMO baseband processing on a single-node supercomputer ([NSDI’25](https://www.usenix.org/conference/nsdi25)).
- **Disaggregated Storage**
  - Projects: [PDS](proj-pds.html)
  - [SANarch](papers/SANarch-nsdi26.pdf) compares the switched and switchless architecture for disaggregated SAN ([NSDI’26](https://www.usenix.org/conference/nsdi26)).
  - [TapDB](papers/TapDB-asplos26.pdf) understands and optimizes database pushdown over storage disaggregation ([ASPLOS’26](https://www.asplos-conference.org/asplos2026/)).
  - [ntprof](papers/ntprof-nsdi25.pdf) is a profiling utility for characterizing and analyzing the NVMe-over-TCP protocol ([NSDI’25](https://www.usenix.org/conference/nsdi25)).
  - [Flint](papers/Flint-nsdi25.pdf) builds an elastic block storage over EBOFs using shadow views ([NSDI’25](https://www.usenix.org/conference/nsdi25)).
- **Programmable Networks**
  - Projects: [CleanNIC](proj-cleannic.html), [dSys-PNF](proj-dsyspnf.html)
  - [SID](papers/SID-sigcomm26.pdf) realizes software-interposed datapath via Elastic QPs for rack-scale interconnects ([SIGCOMM’26](https://conferences.sigcomm.org/sigcomm/2026/)).
  - [SG-IOV](papers/SG-IOV-asplos26.pdf) introduces socket-granular I/O virtualization to offload container networks ([ASPLOS’26](https://www.asplos-conference.org/asplos2026/)).
  - [SCR](papers/SCR-nsdi25.pdf) provides a framework enabling packet-granular software control over the harware transport ([NSDI’25](https://www.usenix.org/conference/nsdi25)).

### Students

Zerui Guo, Wentao Hou, Yuyuan Kang, Joontaek Oh

### Service

**Program Committee Member:** NSDI 2026, ASPLOS 2026, APNet 2025, SOSP 2024, HotInfra 2024, APnet 2024, OSDI 2024, NSDI 2024, HotInfra 2023, APnet 2023, SYSTOR 2023, SIGCOMM 2022, SYSTOR 2021
