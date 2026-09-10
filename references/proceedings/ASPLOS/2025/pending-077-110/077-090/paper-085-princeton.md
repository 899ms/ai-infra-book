<!-- 从 paper-085-princeton.html 迁移的资料快照；原始 HTML SHA-256: 9de0067d3d6215a1229819af19e91853a97564e429cde0af7ccd1eca01340fd3。 -->

# Skia: Exposing Shadow Branches

Chrysanthos Pepi

, Bhargav Reddy Godala

, Krishnam Tibrewala

, Gino A. Chacon

, Paul V. Gratz

, Daniel A. Jiménez

, Gilles A. Pokam

, [David I. August](https://collaborate.princeton.edu/en/persons/david-i-august/)

- [Computer Science](https://collaborate.princeton.edu/en/organisations/6fe9befe-d4aa-477f-84d7-9754647e6e2a/)
- [Electrical and Computer Engineering](https://collaborate.princeton.edu/en/organisations/electrical-and-computer-engineering/)
- [Princeton Institute for Computational Science and Engineering](https://collaborate.princeton.edu/en/organisations/princeton-institute-for-computational-science-and-engineering/)

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

[3   Link opens in a new tab](https://www.scopus.com/pages/publications/105002559459#tab=citedBy) Scopus citations

- [ Overview ](/en/publications/skia-exposing-shadow-branches/)
- [ Fingerprint ](/en/publications/skia-exposing-shadow-branches/fingerprints/)

## Abstract

Modern processors implement a decoupled front-end, often using a form of Fetch Directed Instruction Prefetching (FDIP), to avoid front-end stalls. FDIP is driven by the Branch Prediction Unit (BPU), relying on the BPU's accuracy and branch target tracking structures to speculatively fetch instructions into the Instruction Cache (L1-I cache). As contemporary data center applications become more complex, their code footprints also grow, resulting in a high number of Branch Target Buffer (BTB) misses. These BTB missing branches typically have previously been decoded and placed in the BTB, but have since been evicted, leading to BTB misses now. FDIP can alleviate L1-I cache misses, but its reliance on the BPU's tracking structures means that when it encounters a BTB miss, the BPU may not identify the current instruction as a branch to FDIP. This can prevent FDIP from prefetching or cause it to speculate down the wrong path, further polluting the L1-I cache. We observe that the vast majority, 75%, of BTB-missing, unidentified branches are actually present in instruction cache lines that FDIP has previously fetched. Nevertheless, these missing branches have not yet been decoded and inserted into the BTB. This is because the instruction line is decoded from an entry point (which is the target of the previous taken branch) till an exit point (taken branch). We call branch instructions present in the ignored portion of the cache line ''Shadow Branches.'' Here we present Skia, a novel shadow branch decoding technique that identifies and decodes unused bytes in cache lines fetched by FDIP, inserting them into a Shadow Branch Buffer (SBB). The SBB is accessed in parallel with the BTB, allowing FDIP to speculate despite a BTB miss. With a minimal storage state of 12.25KB, Skia delivers a geomean speedup of ∼5.7% over an 8K-entry BTB (78KB) and ∼2% versus adding an equal amount of state to the BTB, across 16 front-end bound applications. Since many branches stored in the SBB are distinct compared to those in a similarly sized BTB, we consistently observe greater performance gains with Skia across all examined sizes until saturation.

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
| Period | 3/30/25 → 4/3/25 |

## All Science Journal Classification (ASJC) codes

- Software
- Information Systems
- Hardware and Architecture

## Access to Document

- [10.1145/3676641.3716273](https://doi.org/10.1145/3676641.3716273)

## Other files and links

- [Link to publication in Scopus](https://www.scopus.com/pages/publications/105002559459)

- [Link to the citations in Scopus](https://www.scopus.com/pages/publications/105002559459#tab=citedBy)

##  Fingerprint

Dive into the research topics of 'Skia: Exposing Shadow Branches'. Together they form a unique fingerprint.

-  Branch Target Buffer Keyphrases 100%
-  prefetching Computer Science 75%
-  Instruction Prefetching Keyphrases 66%
-  Cache Line Keyphrases 25%
-  Caching Keyphrases 16%
-  Instruction Cache Keyphrases 16%
-  Branch Prediction Unit Keyphrases 16%
-  Tracking Structure Keyphrases 16%

[ View full fingerprint ](/en/publications/skia-exposing-shadow-branches/fingerprints/)

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

Pepi, C., Godala, B. R., Tibrewala, K., Chacon, G. A., Gratz, P. V., Jiménez, D. A., Pokam, G. A.[, & August, D. I.](https://collaborate.princeton.edu/en/persons/david-i-august/) (2025). [Skia: Exposing Shadow Branches](https://collaborate.princeton.edu/en/publications/skia-exposing-shadow-branches/). In *ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems* (pp. 1091-1106). (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS; Vol. 2). Association for Computing Machinery. [https://doi.org/10.1145/3676641.3716273](https://doi.org/10.1145/3676641.3716273)

Pepi, Chrysanthos ; Godala, Bhargav Reddy ; Tibrewala, Krishnam et al. / [**Skia : Exposing Shadow Branches**](https://collaborate.princeton.edu/en/publications/skia-exposing-shadow-branches/). ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Association for Computing Machinery, 2025. pp. 1091-1106 (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS).

@inproceedings{d571f75f385c4f9f8308b72bf55014e8,

title = "Skia: Exposing Shadow Branches",

abstract = "Modern processors implement a decoupled front-end, often using a form of Fetch Directed Instruction Prefetching (FDIP), to avoid front-end stalls. FDIP is driven by the Branch Prediction Unit (BPU), relying on the BPU's accuracy and branch target tracking structures to speculatively fetch instructions into the Instruction Cache (L1-I cache). As contemporary data center applications become more complex, their code footprints also grow, resulting in a high number of Branch Target Buffer (BTB) misses. These BTB missing branches typically have previously been decoded and placed in the BTB, but have since been evicted, leading to BTB misses now. FDIP can alleviate L1-I cache misses, but its reliance on the BPU's tracking structures means that when it encounters a BTB miss, the BPU may not identify the current instruction as a branch to FDIP. This can prevent FDIP from prefetching or cause it to speculate down the wrong path, further polluting the L1-I cache. We observe that the vast majority, 75\\, of BTB-missing, unidentified branches are actually present in instruction cache lines that FDIP has previously fetched. Nevertheless, these missing branches have not yet been decoded and inserted into the BTB. This is because the instruction line is decoded from an entry point (which is the target of the previous taken branch) till an exit point (taken branch). We call branch instructions present in the ignored portion of the cache line ''Shadow Branches.'' Here we present Skia, a novel shadow branch decoding technique that identifies and decodes unused bytes in cache lines fetched by FDIP, inserting them into a Shadow Branch Buffer (SBB). The SBB is accessed in parallel with the BTB, allowing FDIP to speculate despite a BTB miss. With a minimal storage state of 12.25KB, Skia delivers a geomean speedup of ∼5.7\\ over an 8K-entry BTB (78KB) and ∼2\\ versus adding an equal amount of state to the BTB, across 16 front-end bound applications. Since many branches stored in the SBB are distinct compared to those in a similarly sized BTB, we consistently observe greater performance gains with Skia across all examined sizes until saturation.",

author = "Chrysanthos Pepi and Godala, \\Bhargav Reddy\\ and Krishnam Tibrewala and Chacon, \\Gino A.\\ and Gratz, \\Paul V.\\ and Jim{\\e}nez, \\Daniel A.\\ and Pokam, \\Gilles A.\\ and August, \\David I.\\",

note = "Publisher Copyright: {\textcopyright} 2025 ACM.; 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025 ; Conference date: 30-03-2025 Through 03-04-2025",

year = "2025",

month = mar,

day = "30",

doi = "10.1145/3676641.3716273",

language = "English (US)",

series = "International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS",

publisher = "Association for Computing Machinery",

pages = "1091--1106",

booktitle = "ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems",

}

Pepi, C, Godala, BR, Tibrewala, K, Chacon, GA, Gratz, PV, Jiménez, DA, Pokam, GA[ & August, DI](https://collaborate.princeton.edu/en/persons/david-i-august/) 2025, [Skia: Exposing Shadow Branches](https://collaborate.princeton.edu/en/publications/skia-exposing-shadow-branches/). in *ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems.* International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS, vol. 2, Association for Computing Machinery, pp. 1091-1106, 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025, Rotterdam, Netherlands, 3/30/25. [https://doi.org/10.1145/3676641.3716273](https://doi.org/10.1145/3676641.3716273)

[**Skia: Exposing Shadow Branches.**](https://collaborate.princeton.edu/en/publications/skia-exposing-shadow-branches/) / Pepi, Chrysanthos; Godala, Bhargav Reddy; Tibrewala, Krishnam et al.  
ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Association for Computing Machinery, 2025. p. 1091-1106 (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS; Vol. 2).

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

TY - GEN

T1 - Skia

T2 - 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025

AU - Pepi, Chrysanthos

AU - Godala, Bhargav Reddy

AU - Tibrewala, Krishnam

AU - Chacon, Gino A.

AU - Gratz, Paul V.

AU - Jiménez, Daniel A.

AU - Pokam, Gilles A.

AU - August, David I.

N1 - Publisher Copyright: © 2025 ACM.

PY - 2025/3/30

Y1 - 2025/3/30

N2 - Modern processors implement a decoupled front-end, often using a form of Fetch Directed Instruction Prefetching (FDIP), to avoid front-end stalls. FDIP is driven by the Branch Prediction Unit (BPU), relying on the BPU's accuracy and branch target tracking structures to speculatively fetch instructions into the Instruction Cache (L1-I cache). As contemporary data center applications become more complex, their code footprints also grow, resulting in a high number of Branch Target Buffer (BTB) misses. These BTB missing branches typically have previously been decoded and placed in the BTB, but have since been evicted, leading to BTB misses now. FDIP can alleviate L1-I cache misses, but its reliance on the BPU's tracking structures means that when it encounters a BTB miss, the BPU may not identify the current instruction as a branch to FDIP. This can prevent FDIP from prefetching or cause it to speculate down the wrong path, further polluting the L1-I cache. We observe that the vast majority, 75%, of BTB-missing, unidentified branches are actually present in instruction cache lines that FDIP has previously fetched. Nevertheless, these missing branches have not yet been decoded and inserted into the BTB. This is because the instruction line is decoded from an entry point (which is the target of the previous taken branch) till an exit point (taken branch). We call branch instructions present in the ignored portion of the cache line ''Shadow Branches.'' Here we present Skia, a novel shadow branch decoding technique that identifies and decodes unused bytes in cache lines fetched by FDIP, inserting them into a Shadow Branch Buffer (SBB). The SBB is accessed in parallel with the BTB, allowing FDIP to speculate despite a BTB miss. With a minimal storage state of 12.25KB, Skia delivers a geomean speedup of ∼5.7% over an 8K-entry BTB (78KB) and ∼2% versus adding an equal amount of state to the BTB, across 16 front-end bound applications. Since many branches stored in the SBB are distinct compared to those in a similarly sized BTB, we consistently observe greater performance gains with Skia across all examined sizes until saturation.

AB - Modern processors implement a decoupled front-end, often using a form of Fetch Directed Instruction Prefetching (FDIP), to avoid front-end stalls. FDIP is driven by the Branch Prediction Unit (BPU), relying on the BPU's accuracy and branch target tracking structures to speculatively fetch instructions into the Instruction Cache (L1-I cache). As contemporary data center applications become more complex, their code footprints also grow, resulting in a high number of Branch Target Buffer (BTB) misses. These BTB missing branches typically have previously been decoded and placed in the BTB, but have since been evicted, leading to BTB misses now. FDIP can alleviate L1-I cache misses, but its reliance on the BPU's tracking structures means that when it encounters a BTB miss, the BPU may not identify the current instruction as a branch to FDIP. This can prevent FDIP from prefetching or cause it to speculate down the wrong path, further polluting the L1-I cache. We observe that the vast majority, 75%, of BTB-missing, unidentified branches are actually present in instruction cache lines that FDIP has previously fetched. Nevertheless, these missing branches have not yet been decoded and inserted into the BTB. This is because the instruction line is decoded from an entry point (which is the target of the previous taken branch) till an exit point (taken branch). We call branch instructions present in the ignored portion of the cache line ''Shadow Branches.'' Here we present Skia, a novel shadow branch decoding technique that identifies and decodes unused bytes in cache lines fetched by FDIP, inserting them into a Shadow Branch Buffer (SBB). The SBB is accessed in parallel with the BTB, allowing FDIP to speculate despite a BTB miss. With a minimal storage state of 12.25KB, Skia delivers a geomean speedup of ∼5.7% over an 8K-entry BTB (78KB) and ∼2% versus adding an equal amount of state to the BTB, across 16 front-end bound applications. Since many branches stored in the SBB are distinct compared to those in a similarly sized BTB, we consistently observe greater performance gains with Skia across all examined sizes until saturation.

UR - https://www.scopus.com/pages/publications/105002559459

UR - https://www.scopus.com/pages/publications/105002559459#tab=citedBy

U2 - 10.1145/3676641.3716273

DO - 10.1145/3676641.3716273

M3 - Conference contribution

AN - SCOPUS:105002559459

T3 - International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS

SP - 1091

EP - 1106

BT - ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems

PB - Association for Computing Machinery

Y2 - 30 March 2025 through 3 April 2025

ER -

Pepi C, Godala BR, Tibrewala K, Chacon GA, Gratz PV, Jiménez DA et al. [Skia: Exposing Shadow Branches](https://collaborate.princeton.edu/en/publications/skia-exposing-shadow-branches/). In ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Association for Computing Machinery. 2025. p. 1091-1106. (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS). doi: 10.1145/3676641.3716273
