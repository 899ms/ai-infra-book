<!-- 从 tyr-institution.html 迁移的资料快照；原始 HTML SHA-256: 7bba33536082488341979cc94af48db36f0673315dc13bab7ebf59c51905ba46。 -->

[](https://www.cmu.edu/)

 

[](/index.shtml)

- [](/index.shtml)
- 
- [Projects](/about.shtml)
  - [Big Learning Systems](/BigLearning/index.shtml)
  - [Cache Eviction Tactics](/CacheEviction/index.shtml)
  - [CARP](../CARP/index.shtml)
  - [CILES  
      (Caching Systems)](/CILES/index.shtml)
  - [Cost-efficient  
      Computing on Cloud](/CostEfficientComputing/index.shtml)
  - [Database Systems](/DatabaseSystems/index.shtml)
  - [Data Center  
      Observatory (DCO)](/DCO/index.shtml)
  - [Data Lake Scheduling](/DataLake/index.shtml)
  - [DBMS-Autotuning](/DatabaseSystems/DBMS-Autotuning/index.shtml)
  - [Declarative IO](/DeclarativeIO/index.shtml)
  - [DeltaFS](/DeltaFS/index.shtml)
  - [HeART  
      (Storage Reliability)](/HeART/index.shtml)
  - [Key-value Cache Mgmt](/kvCacheMgmt/index.shtml)
  - [Mimir: Navigating  
      Cloud Storage](/Mimir/index.shtml)
  - [ML Coded Computation](/MLCodedComputation/index.shtml)
  - [Multi-Site Data-  
      Intensive Computing](/MultiSite/index.shtml)
  - [NoisePage  
      (Auto-Driving DBMS)](/NoisePage/index.shtml)
  - [NVM Redundancy](/NVMRedundancy/index.shtml)
  - [pNFS](/pNFS/index.shtml)
  - [Zoned Storage](/ZonedStorage/index.shtml)
  - [Past Projects](/past-projects.shtml)
- [News/Jobs](/News/index.shtml)
  - [PDL News](/News/index.shtml)
  - [PDL Packet](/Publications/packet.shtml)
    - [Fall 2025](/ftp/News/newsletter25.pdf)
    - [Fall 2024](/ftp/News/newsletter24.pdf)
    - [Fall 2023](/ftp/News/newsletter23.pdf)
  - [Industry Employment  
      Opportunities](/Jobs/industry_jobs.shtml)
- [Events](/Retreat/index.shtml)
  - [Talk Series 2026](/talk-series/index.shtml)
  - [Retreat 2026](/Retreat/retreat26.shtml)
  - [Talk Series 2025](/talk-series/2025/index.shtml)
  - [Retreat 2024](/Retreat/retreat24.shtml)
  - [Talk Series 2024](/talk-series/2024/index.shtml)
  - [Retreat 2023](/Retreat/retreat23.shtml)
  - [Talk Series 2023](/talk-series/2023/index.shtml)
  - [Retreat 2022](/Retreat/retreat22.shtml)
  - [Visit Day 2022](/Retreat/svd22-1.shtml)  
  - [SDI Seminars](/SDI/index.shtml)
- [Publications](/Publications/index.shtml)
  - [Recent](/Publications/index.shtml)
  - [By Date](/Publications/pubs-date.shtml)
  - [By Project](/Publications/pubs-project.shtml)
  - [Tech Reports](/Publications/pubs-tr.shtml)
  - [Past Projects](/Publications/pubs-pastprojects.shtml)
  - [Copyright Notices](/Publications/copyright.shtml)
- [People](/People/index.shtml)
  - [Faculty](/People/index.shtml#fac)
  - [Post Docs](/People/index.shtml#postdoc)
  - [Staff](/People/index.shtml#staff)
  - [Grad Students](/People/index.shtml#grad)
  - [Undergrads](/People/index.shtml#under)
  - [PDL Alums](/People/alumni.shtml)
  - [Distinguished Alums](/People/distinguished-alumni.shtml)
- [Affiliates](/affiliates.shtml)
  - [Member Login](/Consortium/index.shtml)
      
  - [PDL Consortium](/affiliates.shtml#industry)
  - [PDL Endowed Fund](/giving.shtml)
  - [Affiliated Projects](/affiliates.shtml#CMU)
  - [Federal Sponsors](/affiliates.shtml#Gov)
- [About](/about.shtml)
  - [About](/about.shtml)
  - [Contact](/about.shtml#contact)
  - [Visitor Info](/visitor-info.shtml)
      
  - [Internal](/Internal/index.shtml)

## PARALLEL DATA LAB 

##### PDL Publications

------------------------------------------------------------------------

- [Recent](/Publications/index.shtml)
- [Pubs by Project](/Publications/pubs-project.shtml)
- [Pubs by Date](/Publications/pubs-date.shtml)
- [Tech Reports](/Publications/pubs-tr.shtml)
- [Past Project Publications](/Publications/pubs-pastprojects.shtml)
- [Code Distribution](/Publications/downloads.shtml)
- [The PDL Packet](/Publications/packet.shtml)

## PDL Abstract

### The TYR Dataflow Architecture: Improving Locality by Taming Parallelism

*2024 57th IEEE/ACM International Symposium on Microarchitecture (MICRO), November 2-6, 2024, Austin, TX.*

**Nikhil Agarwal, Mitchell Fream, Souradip Ghosh, Brian C. Schwedock\*, Nathan Beckmann**

Carnegie Mellon University  
\* Samsung

<http://www.pdl.cmu.edu/> [  
](http://www.pdl..cmu.edu/PASIS/%20)

Architectures should aim to maximize parallelism within a machine’s finite memories, but prior designs tend to extremes, either maximizing parallelism or minimizing state. In particular, prior unordered dataflow architectures suffer from a parallelism explosion that creates unbounded state, requires prohibitively large associative memories, and risks deadlock. The few architectures that successfully navigate the parallelism-state tradeoff are limited to embarrassingly parallel programs.

TYR is a new, general-purpose unordered dataflow architecture that achieves high parallelism with bounded state. The key insight is that prior unordered dataflow architectures are overly conservative, unnecessarily allocating tags from a single, global tag space. TYR exploits program structure to break up tags into local tag spaces that operate independently. Local tag spaces eliminate tag competition between co-dependent parts of the program, provably guaranteeing forward progress with only two tags per local tag space. TYR thus opens the door to an efficient, scalable implementation of unordered dataflow. Simulation of parallel programs demonstrates that TYR achieves parallelism nearly identical to a naïve unordered dataflow architecture with orders-of-magnitude less state.

**KEYWORDS:** Dataflow, parallelism, locality**  
FULL PAPER: [pdf](ACMToS-0920.pdf)**

 

#### Contact us

-   +1 (412) 268 6716
-  <contact-pdl@ece.cmu.edu>
-  [School of Computer Science](https://www.cs.cmu.edu/)
-  [Department of Electrical &  
      Computer Engineering](https://www.ece.cmu.edu/)

#### Recent Events

- ###### PDL Retreat 2026

  CMU Campus  

  [more info](/Retreat/retreat26.shtml) 

- ###### PDL Retreat 2024

  Omni Bedford Springs  

  [more info](/Retreat/retreat24.shtml) 

- ###### PDL Retreat 2023

  Omni Bedford Springs  

  [more info](/Retreat/retreat23.shtml) 

#### Social Media

- [](https://www.facebook.com/groups/107359921205/)     [](https://www.linkedin.com/groups/1578567/?msgConversationId=6450780836924055552&msgOverlay=true)
-  
- [![](/images/Titles/skibo-darkbg.png)](/index.shtml)

------------------------------------------------------------------------

Copyright © 2026 - [Legal Info](https://www.cmu.edu/legal/) - [Parallel Data Lab](/index.shtml)
