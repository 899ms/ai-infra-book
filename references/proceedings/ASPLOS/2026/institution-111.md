<!-- 从 institution-111.html 迁移的资料快照；原始 HTML SHA-256: 5c34541ce442dcb3896932b71fc893b1a6af9acdc030ada4d3ddf47e66c56e3a。 -->

# TempGraph : an efficient chain-driven temporal graph computing framework on the GPU

Copy

Zhao, Jin, Wang, Qian, He, Ligang, Zhang, Yu, Di, Sheng, He, Bingsheng, Wang, Xinlei, Yu, Hui, Qi, Hao, Lin, Longlong, Yu, Linchen, Liao, Xiaofei and Jin, Hai (2025) *TempGraph : an efficient chain-driven temporal graph computing framework on the GPU.* In: 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Rotterdam, Netherlands, 30 Mar - 03 Apr 2025. Published in: Proceedings of 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, 3 pp. 230-246. ISBN 9798400710803. doi:[10.1145/3676642.3736116](https://doi.org/10.1145/3676642.3736116)

[TABLE]

Official URL: <https://doi.org/10.1145/3676642.3736116>

[Request Changes to record.](https://warwick.ac.uk/services/library/staff/warwick-research-publications/request-changes-to-your-research-record#191864)

## Abstract

Tackling temporal path problems in temporal graphs is essential for time-sensitive applications. Although many solutions have been proposed to handle temporal path problems, due to the intrinsic time constraints, these solutions require the vertices of the temporal graph to be sequentially handled along the time-dependent chains (i.e., the temporal dependencies between these vertices) to form the temporal path. This sequential temporal nature poses the challenges of poor parallelism and slow convergence speed, preventing existing solutions from fully leveraging the massive parallelism and high internal bandwidth of GPU to handle temporal path problems. To overcome these challenges, this paper proposes TempGraph, an efficient chain-driven GPU-based temporal graph computing framework. Specifically, it transforms the temporal graph into a set of disjoint time-dependent chains that can elegantly expose the temporal dependency between the vertices while facilitating the fast path exploration along these chains over GPU. Furthermore, TempGraph employs a novel Generate-Activate-Compute execution model to decouple the temporal dependency between different chains through maintaining a set of shortcuts for them, which enables multiple chains to be concurrently handled by massive GPU threads, achieving fast convergence speed and high parallelism on the GPU. Experiments on an A100 GPU show that TempGraph outperforms the state-of-the-art GPU-based solutions by 3.0-16.2×. Besides, TempGraph on an A100 GPU gains 33.9-368.9× speedups compared to the cutting-edge CPU-based system TeGraph on a 128-core CPU machine.

[TABLE]

### Export / Share Citation

BibTeX HTML Citation EndNote OpenURL ContextObject in Span Reference Manager Simple Metadata Multiline CSV JSON Dublin Core ASCII Citation OpenURL ContextObject METS OPENAIRE RDF+N3 Refer RIOXX2 XML RDF+XML Atom EP3 XML MODS MPEG-21 DIDL RDF+N-Triples Ideate

Export

[![](https://warwick.ac.uk/services/library/webbridge.gif)](http://fs6jr8lx8q.search.serialssolutions.com/?spage=230&isbn=9798400710803&date=2025-08-06&genre=proceeding&aufirst=Jin&atitle=TempGraph%20:%20an%20efficient%20chain-driven%20temporal%20graph%20computing%20framework%20on%20the%20GPU&epage=246&aulast=Zhao&title=30th%20ACM%20International%20Conference%20on%20Architectural%20Support%20for%20Programming%20Languages%20and%20Operating%20Systems&volume=3)

  

[Request changes or add full text files to a record](https://warwick.ac.uk/services/library/staff/warwick-research-publications/request-changes-to-your-research-record#191864)

### Repository staff actions (login required)

|  |  |
|----|----|
| [![View Item](/style/images/action_view.png)](/cgi/users/home?screen=EPrint%3A%3AView&eprintid=191864) | View Item |
