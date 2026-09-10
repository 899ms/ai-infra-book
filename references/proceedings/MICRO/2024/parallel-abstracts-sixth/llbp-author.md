<!-- 从 llbp-author.html 迁移的资料快照；原始 HTML SHA-256: 23b25c2cdd70fd7c4d5fe4152f195851f6afdb280cd8cbbeea401335f6bf9314。 -->

# David Schall

[Imperial College London](https://www.imperial.ac.uk/). Department of Computing.

![avatar.jpg](/assets/img/avatar.jpg?v=9fd003349ef5035c2ecde1435b8e3fcf)

Hi, I’m David, an Assistant Professor in the [Department of Computing](https://www.imperial.ac.uk/computing) at [Imperial College London](https://www.imperial.ac.uk/).

Previously, I completed my PhD at the University of Edinburgh under the guidance of [Prof. Boris Grot](https://homepages.inf.ed.ac.uk/bgrot/) followed by a Posdoc at the [Systems Research Group](https://dse.in.tum.de/) led by [Prof. Pramod Bhatotia](https://dse.in.tum.de/bhatotia/) at the [Technical University of Munich](https://www.tum.de/)..

My research interests span Computer Architecture and Computer Systems, with a particular focus on CPU microarchitecture, branch prediction, instruction delivery, and the hardware-software interface. During my PhD, I studied the detrimental effects of frequent context switches in modern cloud workloads \[[1](assets/pdf/JUKEBOX_ISCA22.pdf),[2](assets/pdf/IGNITE_MICRO23.pdf)\]. My most recent work explores a novel branch predictor organization that enables hierarchical branch predictor designs \[[3](assets/pdf/LLBP_MICRO24.pdf),[4](assets/pdf/LLBPX_HPCA26.pdf)\].

As Moore’s Law slows down and the world’s demand for computing power continues to grow, researchers are challenged more than ever to rethink established mechanisms and develop innovative ideas for a sustainable future. In research, I am eager to address this challenge by exploring new approaches to bring hardware and software closer together.

If you are interested in addressing these challenges together do not hesitate to contact me. I always look for motivated people.

## Student Projects

I am looking for PhD/BSc/MSc students interested to work on topics on CPU microarchitecture.

An incomplete list of projects:

- Evaluating criticality in value prediction
- Semantic hints for value predictions
- Characterization and optimization of modern data center applications
- Evaluating the performance of multi-block ahead branch predictions
- …

If one of the projects sounds interesting please contact me.

## [Selected Publications](/publications/)

1.  HPCA

    The Last-Level Branch Predictor Revisited

    David Schall, Mária Ďuračková, and [Boris Grot](https://homepages.inf.ed.ac.uk/bgrot/)

    *In Proceedings of the 32nd IEEE International Symposium on High-Performance Computer Architecture (HPCA-32)*, 2026

    Bib [PDF](/assets/pdf/LLBPX_HPCA26.pdf) [Code](https://github.com/dhschall/llbp-x) [Slides](/assets/pdf/LLBPX_HPCA26-Slides.pptx)

    ``` bibtex
    @inproceedings{schall:llbpx,
      title = {The Last-Level Branch Predictor Revisited},
      author = {Schall, David and Ďuračková, Mária and Grot, Boris},
      booktitle = {Proceedings of the 32nd IEEE International Symposium on High-Performance Computer Architecture (HPCA-32)},
      year = {2026}
    }
    ```

2.   [MICRO](https://microarch.org/)

    The Last-Level Branch Predictor

    David Schall, [Andreas Sandberg](https://andreas.sandberg.uk/), and [Boris Grot](https://homepages.inf.ed.ac.uk/bgrot/)

    *In 2024 57th IEEE/ACM International Symposium on Microarchitecture (MICRO)*, 2024

    [DOI](https://doi.org/10.1109/MICRO61859.2024.00042) Bib [PDF](/assets/pdf/LLBP_MICRO24.pdf) [Code](https://github.com/dhschall/llbp) [Slides](/assets/pdf/LLBP_MICRO24-Slides.pptx)

    ``` bibtex
    @inproceedings{0.1109/MICRO61859.2024.00042,
      author = {Schall, David and Sandberg, Andreas and Grot, Boris},
      booktitle = {2024 57th IEEE/ACM International Symposium on Microarchitecture (MICRO)},
      title = {The Last-Level Branch Predictor},
      year = {2024},
      volume = {},
      number = {},
      pages = {464-479},
      keywords = {Microarchitecture, Branch Prediction},
      doi = {10.1109/MICRO61859.2024.00042},
      series = {MICRO '24},
      publisher = {IEEE}
    }
    ```

3.   [MICRO](https://microarch.org/)

    Warming Up a Cold Front-End with Ignite

    David Schall, [Andreas Sandberg](https://andreas.sandberg.uk/), and [Boris Grot](https://homepages.inf.ed.ac.uk/bgrot/)

    *In Proceedings of the 56th Annual IEEE/ACM International Symposium on Microarchitecture*, , Toronto, ON, Canada, , 2023

    Abs [DOI](https://doi.org/10.1145/3613424.3614258) Bib [PDF](/assets/pdf/IGNITE_MICRO23.pdf) [Code](https://github.com/dhschall/gem5-fdp) [Slides](/assets/pdf/IGNITE_MICRO23-Slides.pdf)

    Serverless computing is a popular software deployment model for the cloud, in which applications are designed as a collection of stateless tasks. Developers are charged for the CPU time and memory footprint during the execution of each serverless function, which incentivizes them to reduce both runtime and memory usage. As a result, functions tend to be short (often on the order of a few milliseconds) and compact (128–256 MB). Cloud providers can pack thousands of such functions on a server, resulting in frequent context switches and a tremendous degree of interleaving. As a result, when a given memory-resident function is re-invoked, it commonly finds its on-chip microarchitectural state completely cold due to thrashing by other functions — a phenomenon termed lukewarm invocation. Our analysis shows that the cold microarchitectural state due to lukewarm invocations is highly detrimental to performance, which corroborates prior work. The main source of performance degradation is the front-end, composed of instruction delivery, branch identification via the BTB and the conditional branch prediction. State-of-the-art front-end prefetchers show only limited effectiveness on lukewarm invocations, falling considerably short of an ideal front-end. We demonstrate that the reason for this is the cold microarchitectural state of the branch identification and prediction units. In response, we introduce Ignite, a comprehensive restoration mechanism for front-end microarchitectural state targeting instructions, BTB and branch predictor via unified metadata. Ignite records an invocation’s control flow graph in compressed format and uses that to restore the front-end structures the next time the function is invoked. Ignite outperforms state-of-the-art front-end prefetchers, improving performance by an average of 43% by significantly reducing instruction, BTB and branch predictor MPKI.

    ``` bibtex
    @inproceedings{10.1145/3613424.3614258,
      author = {Schall, David and Sandberg, Andreas and Grot, Boris},
      title = {Warming Up a Cold Front-End with Ignite},
      year = {2023},
      isbn = {9798400703294},
      publisher = {Association for Computing Machinery},
      address = {New York, NY, USA},
      url = {https://doi.org/10.1145/3613424.3614258},
      doi = {10.1145/3613424.3614258},
      booktitle = {Proceedings of the 56th Annual IEEE/ACM International Symposium on Microarchitecture},
      pages = {254–267},
      numpages = {14},
      keywords = {instruction delivery, front-end prefetching and serverless, Microarchitecture},
      location = {<conf-loc>, <city>Toronto</city>, <state>ON</state>, <country>Canada</country>, </conf-loc>},
      series = {MICRO '23}
    }
    ```

4.   [ISCA](https://iscaconf.org/)

    Lukewarm serverless functions: characterization and optimization

    David Schall, Artemiy Margaritov, Dmitrii Ustiugov, and 2 more authors

    *In Proceedings of the 49th Annual International Symposium on Computer Architecture*, New York, New York, 2022

    IEEE MICRO Top Picks Honorable Mention

    Abs [DOI](https://doi.org/10.1145/3470496.3527390) Bib [PDF](/assets/pdf/JUKEBOX_ISCA22.pdf) [Code](https://github.com/vhive-serverless/vSwarm-u) [Slides](/assets/pdf/JUKEBOX_ISCA22-Slides.pdf)

    Serverless computing has emerged as a widely-used paradigm for running services in the cloud. In serverless, developers organize their applications as a set of functions, which are invoked on-demand in response to events, such as an HTTP request. To avoid long start-up delays of launching a new function instance, cloud providers tend to keep recently-triggered instances idle (or warm) for some time after the most recent invocation in anticipation of future invocations. Thus, at any given moment on a server, there may be thousands of warm instances of various functions whose executions are interleaved in time based on incoming invocations.This paper observes that (1) there is a high degree of interleaving among warm instances on a given server; (2) the individual warm functions are invoked relatively infrequently, often at the granularity of seconds or minutes; and (3) many function invocations complete within a few milliseconds. Interleaved execution of rarely invoked functions on a server leads to thrashing of each function’s microarchitectural state between invocations. Meanwhile, the short execution time of a function impedes amortization of the warm-up latency of the cache hierarchy, causing a 31–114% increase in CPI compared to execution with warm microarchitectural state. We identify on-chip misses for instructions as a major contributor to the performance loss. In response we propose Jukebox, a record-and-replay instruction prefetcher specifically designed for reducing the start-up latency of warm function instances. Jukebox requires just 32KB of metadata per function instance and boosts performance by an average of 18.7% for a wide range of functions, which translates into a corresponding throughput improvement.

    ``` bibtex
    @inproceedings{10.1145/3470496.3527390,
      note = {<p style="color:--global-theme-color">IEEE MICRO Top Picks Honorable Mention</p>},
      author = {Schall, David and Margaritov, Artemiy and Ustiugov, Dmitrii and Sandberg, Andreas and Grot, Boris},
      title = {Lukewarm serverless functions: characterization and optimization},
      year = {2022},
      isbn = {9781450386104},
      publisher = {Association for Computing Machinery},
      address = {New York, NY, USA},
      url = {https://doi.org/10.1145/3470496.3527390},
      doi = {10.1145/3470496.3527390},
      booktitle = {Proceedings of the 49th Annual International Symposium on Computer Architecture},
      pages = {757–770},
      numpages = {14},
      keywords = {serverless, microarchitecture, instruction prefetching, characterization},
      location = {New York, New York},
      series = {ISCA '22}
    }
    ```

[](/assets/pdf/resume.pdf "Cv pdf") [](mailto:d.schall@imperial.ac.uk "Email") [](https://scholar.google.com/citations?user=ZmmKWBcAAAAJ "Scholar userid") [](https://orcid.org/0000-0002-3587-3253 "Orcid id") [](https://github.com/dhschall "Github username") [](https://dblp.org/pid/321/3284.html "Dblp url")

Best way to reach me is to drop me a mail.
