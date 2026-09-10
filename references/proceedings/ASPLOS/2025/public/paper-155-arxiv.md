<!-- 从 paper-155-arxiv.html 迁移的资料快照；原始 HTML SHA-256: d43b3d9a43c152da4a4c45f41e59f0a48d1d8f05e4fa4ff7e0049b43f9274c9c。 -->

# Computer Science \> Hardware Architecture

**arXiv:2502.07578** (cs)

\[Submitted on 11 Feb 2025 ([v1](https://arxiv.org/abs/2502.07578v1)), last revised 3 May 2025 (this version, v3)\]

# Title:PIM Is All You Need: A CXL-Enabled GPU-Free System for Large Language Model Inference

Authors:[Yufeng Gu](https://arxiv.org/search/cs?searchtype=author&query=Gu,+Y), [Alireza Khadem](https://arxiv.org/search/cs?searchtype=author&query=Khadem,+A), [Sumanth Umesh](https://arxiv.org/search/cs?searchtype=author&query=Umesh,+S), [Ning Liang](https://arxiv.org/search/cs?searchtype=author&query=Liang,+N), [Xavier Servot](https://arxiv.org/search/cs?searchtype=author&query=Servot,+X), [Onur Mutlu](https://arxiv.org/search/cs?searchtype=author&query=Mutlu,+O), [Ravi Iyer](https://arxiv.org/search/cs?searchtype=author&query=Iyer,+R), [Reetuparna Das](https://arxiv.org/search/cs?searchtype=author&query=Das,+R)

View a PDF of the paper titled PIM Is All You Need: A CXL-Enabled GPU-Free System for Large Language Model Inference, by Yufeng Gu and 7 other authors

[View PDF](/pdf/2502.07578) [HTML (experimental)](https://arxiv.org/html/2502.07578v3)

> Abstract:Large Language Model (LLM) inference uses an autoregressive manner to generate one token at a time, which exhibits notably lower operational intensity compared to earlier Machine Learning (ML) models such as encoder-only transformers and Convolutional Neural Networks. At the same time, LLMs possess large parameter sizes and use key-value caches to store context information. Modern LLMs support context windows with up to 1 million tokens to generate versatile text, audio, and video content. A large key-value cache unique to each prompt requires a large memory capacity, limiting the inference batch size. Both low operational intensity and limited batch size necessitate a high memory bandwidth. However, contemporary hardware systems for ML model deployment, such as GPUs and TPUs, are primarily optimized for compute throughput. This mismatch challenges the efficient deployment of advanced LLMs and makes users pay for expensive compute resources that are poorly utilized for the memory-bound LLM inference tasks.  
> We propose CENT, a CXL-ENabled GPU-Free sysTem for LLM inference, which harnesses CXL memory expansion capabilities to accommodate substantial LLM sizes, and utilizes near-bank processing units to deliver high memory bandwidth, eliminating the need for expensive GPUs. CENT exploits a scalable CXL network to support peer-to-peer and collective communication primitives across CXL devices. We implement various parallelism strategies to distribute LLMs across these devices. Compared to GPU baselines with maximum supported batch sizes and similar average power, CENT achieves 2.3\$\times\$ higher throughput and consumes 2.9\$\times\$ less energy. CENT enhances the Total Cost of Ownership (TCO), generating 5.2\$\times\$ more tokens per dollar than GPUs.

[TABLE]

## Submission history

From: Yufeng Gu \[[view email](/show-email/fb3128c3/2502.07578)\]  
**[\[v1\]](/abs/2502.07578v1)** Tue, 11 Feb 2025 14:25:20 UTC (5,291 KB)  
**[\[v2\]](/abs/2502.07578v2)** Fri, 21 Mar 2025 21:10:02 UTC (5,259 KB)  
**\[v3\]** Sat, 3 May 2025 04:07:07 UTC (5,405 KB)  

Full-text links:

## Access Paper:

- View a PDF of the paper titled PIM Is All You Need: A CXL-Enabled GPU-Free System for Large Language Model Inference, by Yufeng Gu and 7 other authors

- [View PDF](/pdf/2502.07578)

- [HTML (experimental)](https://arxiv.org/html/2502.07578v3)

- [TeX Source](/src/2502.07578)

[![license icon](https://arxiv.org/icons/licenses/by-nc-sa-4.0.png) view license](http://creativecommons.org/licenses/by-nc-sa/4.0/ "Rights to this article")

### Current browse context:

cs.AR

[\< prev](/prevnext?id=2502.07578&function=prev&context=cs.AR "previous in cs.AR (accesskey p)")   \|   [next \>](/prevnext?id=2502.07578&function=next&context=cs.AR "next in cs.AR (accesskey n)")   

[new](/list/cs.AR/new) \| [recent](/list/cs.AR/recent) \| [2025-02](/list/cs.AR/2025-02)

Change to browse by:

[cs](/abs/2502.07578?context=cs)  

### References & Citations

- [NASA ADS](https://ui.adsabs.harvard.edu/abs/arXiv:2502.07578)
- [Google Scholar](https://scholar.google.com/scholar_lookup?arxiv_id=2502.07578)
- [Semantic Scholar](https://api.semanticscholar.org/arXiv:2502.07578)

export BibTeX citation

Loading...

## BibTeX formatted citation

×

Data provided by:

### Bookmark

[![BibSonomy](/static/browse/0.3.4/images/icons/social/bibsonomy.png)](http://www.bibsonomy.org/BibtexHandler?requTask=upload&url=https://arxiv.org/abs/2502.07578&description=PIM%20Is%20All%20You%20Need:%20A%20CXL-Enabled%20GPU-Free%20System%20for%20Large%20Language%20Model%20Inference "Bookmark on BibSonomy") [![Reddit](/static/browse/0.3.4/images/icons/social/reddit.png)](https://reddit.com/submit?url=https://arxiv.org/abs/2502.07578&title=PIM%20Is%20All%20You%20Need:%20A%20CXL-Enabled%20GPU-Free%20System%20for%20Large%20Language%20Model%20Inference "Bookmark on Reddit")

Bibliographic Tools

# Bibliographic and Citation Tools

Bibliographic Explorer Toggle

Bibliographic Explorer *([What is the Explorer?](https://info.arxiv.org/labs/showcase.html#arxiv-bibliographic-explorer))*

Connected Papers Toggle

Connected Papers *([What is Connected Papers?](https://www.connectedpapers.com/about))*

Litmaps Toggle

Litmaps *([What is Litmaps?](https://www.litmaps.co/))*

scite.ai Toggle

scite Smart Citations *([What are Smart Citations?](https://www.scite.ai/))*

Code, Data, Media

# Code, Data and Media Associated with this Article

alphaXiv Toggle

alphaXiv *([What is alphaXiv?](https://alphaxiv.org/))*

Links to Code Toggle

CatalyzeX Code Finder for Papers *([What is CatalyzeX?](https://www.catalyzex.com))*

DagsHub Toggle

DagsHub *([What is DagsHub?](https://dagshub.com/))*

GotitPub Toggle

Gotit.pub *([What is GotitPub?](http://gotit.pub/faq))*

Huggingface Toggle

Hugging Face *([What is Huggingface?](https://huggingface.co/huggingface))*

ScienceCast Toggle

ScienceCast *([What is ScienceCast?](https://sciencecast.org/welcome))*

Demos

# Demos

Replicate Toggle

Replicate *([What is Replicate?](https://replicate.com/docs/arxiv/about))*

Spaces Toggle

Hugging Face Spaces *([What is Spaces?](https://huggingface.co/docs/hub/spaces))*

Spaces Toggle

TXYZ.AI *([What is TXYZ.AI?](https://txyz.ai))*

Related Papers

# Recommenders and Search Tools

Link to Influence Flower

Influence Flower *([What are Influence Flowers?](https://influencemap.cmlab.dev/))*

Core recommender toggle

CORE Recommender *([What is CORE?](https://core.ac.uk/services/recommender))*

- Author
- Venue
- Institution
- Topic

![](data:image/svg+xml;base64,PHN2ZyBpZD0iZmxvd2VyLWdyYXBoLWF1dGhvciI+PC9zdmc+)

![](data:image/svg+xml;base64,PHN2ZyBpZD0iZmxvd2VyLWdyYXBoLXZlbnVlIj48L3N2Zz4=)

![](data:image/svg+xml;base64,PHN2ZyBpZD0iZmxvd2VyLWdyYXBoLWluc3QiPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyBpZD0iZmxvd2VyLWdyYXBoLXRvcGljIj48L3N2Zz4=)

About arXivLabs

# arXivLabs: experimental projects with community collaborators

arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website.

Both individuals and organizations that work with arXivLabs have embraced and accepted our values of openness, community, excellence, and user data privacy. arXiv is committed to these values and only works with partners that adhere to them.

Have an idea for a project that will add value for arXiv's community? [**Learn more about arXivLabs**](https://info.arxiv.org/labs/index.html).

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHJvbGU9InByZXNlbnRhdGlvbiIgdmlld2JveD0iMCAwIDYzNS41NzIgODExIj48cGF0aCBkPSJNMTc1LjYgNjc2djI3aC0yN3YtMjd6bS01NCAyN3YyN2gyN3YtMjd6bS0yNyAyN3YyN2gyN3YtMjd6bTM5Ni01NHYyN2gtMjd2LTI3em0wIDI3djI3aDI3di0yN3ptMjcgMjd2MjdoMjd2LTI3em0tMjctNDE0aDI3djI3aC0yN3ptMjcgMGgyN3YtMjdoLTI3em0yNy0yN2gyN3YtMjdoLTI3em0tMzk2IDQ1aC0yN3YtMjdoMjd6bS0yNy01NGgtMjd2MjdoMjd6bS0yNy0yN2gtMjd2MjdoMjd6IiAvPjxwYXRoIGQ9Ik05NC42IDczMHYyN2gtMjd2LTI3em00NzcgMHYyN2gtMjd2LTI3em0tMjctNDk1aDI3djI3aC0yN3ptLTQ1MCAxOGgtMjd2LTI3aDI3em00NzcgOWgyN3YyN2gtMjd6bS01NCA0OTVoMjd2MjdoLTI3em0tNDIzIDBoMjd2MjdoLTI3em0tNTQtNTA0aDI3djI3aC0yN3oiIGZpbGw9IiM2NjYiIC8+PHBhdGggZD0iTTY3LjYgNzMwdjI3aC0yN3YtMjd6bTU0IDU0djI3aC0yN3YtMjd6bTAtMTA4djI3aDI3di0yN3ptLTI3IDI3djI3aDI3di0yN3ptLTgxIDB2MjdoMjd2LTI3em01ODUgMjd2MjdoLTI3di0yN3ptLTEwOC01NHYyN2gyN3YtMjd6bTI3IDI3djI3aDI3di0yN3ptODEgMHYyN2gyN3YtMjd6bS01NC00OTVoMjd2MjdoLTI3em0tNTQgMTA4aDI3di0yN2gtMjd6bTI3LTI3aDI3di0yN2gtMjd6bTAtODFoMjd2LTI3aC0yN3ptLTQyMyAxOGgtMjd2LTI3aDI3em01NCA1NGgtMjd2MjdoMjd6bS0yNy0yN2gtMjd2MjdoMjd6bTAtODFoLTI3djI3aDI3em00MjMgNjEydjI3aC0yN3YtMjd6bTgxLTUyMnYyN2gtMjd2LTI3em0tNTg1LTl2MjdoLTI3di0yN3oiIGZpbGw9IiM5OTkiIC8+PHBhdGggZD0iTTk0LjYgNzg0djI3aC0yN3YtMjd6bS0yNy0yN3YyN2gyN3YtMjd6bS0yNy01NHYyN2gyN3YtMjd6bTI3IDB2MjdoMjd2LTI3em0wLTI3djI3aDI3di0yN3ptMjcgMHYyN2gyN3YtMjd6bTAtMjd2MjdoMjd2LTI3em0yNyAwdjI3aDI3di0yN3ptLTEwOCA4MXYyN2gyN3YtMjd6bTU1OCA1NHYyN2gtMjd2LTI3em0tMjctMjd2MjdoMjd2LTI3em0yNy01NHYyN2gyN3YtMjd6bS0yNyAwdjI3aDI3di0yN3ptMC0yN3YyN2gyN3YtMjd6bS0yNyAwdjI3aDI3di0yN3ptMC0yN3YyN2gyN3YtMjd6bS0yNyAwdjI3aDI3di0yN3ptMTA4IDgxdjI3aDI3di0yN3ptMC00OTVoMjd2MjdoLTI3em0tMjcgMjdoMjd2LTI3aC0yN3ptLTU0LTI3aDI3di0yN2gtMjd6bTAgMjdoMjd2LTI3aC0yN3ptLTI3IDBoMjd2LTI3aC0yN3ptMCAyN2gyN3YtMjdoLTI3em0tMjcgMGgyN3YtMjdoLTI3em0wIDI3aDI3di0yN2gtMjd6bTgxLTEwOGgyN3YtMjdoLTI3em0tNTA0IDQ1aC0yN3YtMjdoMjd6bTI3LTI3aC0yN3YyN2gyN3ptNTQtMjdoLTI3djI3aDI3em0wIDI3aC0yN3YyN2gyN3ptMjcgMGgtMjd2MjdoMjd6bTAgMjdoLTI3djI3aDI3em0yNyAwaC0yN3YyN2gyN3ptMCAyN2gtMjd2MjdoMjd6bS04MS0xMDhoLTI3djI3aDI3eiIgZmlsbD0iI2NjYyIgLz48cGF0aCBkPSJNNTk4LjYgNjY1LjFINDEuNUMtNzYuNSA2NjcgMTc2IDI4MC4yIDE3NiAyODAuMmg1M2E0Ni41IDQ2LjUgMCAwMTYyLjgtNTYuMyAyOS4yIDI5LjIgMCAxMTI4LjUgMzUuOWgtMWE0Ni41IDQ2LjUgMCAwMS0xLjUgMjAuM2wxNDIuNS0uMXMyNTUuMyAzODcgMTM4LjMgMzg1LjF6TTI5MSAxODFhMjkuMyAyOS4zIDAgMTAtMjkuMi0yOS4zQTI5LjMgMjkuMyAwIDAwMjkxIDE4MXptNjUuNC02Ni44YTIyLjQgMjIuNCAwIDEwLTIyLjUtMjIuNCAyMi40IDIyLjQgMCAwMDIyLjUgMjIuNHoiIGZpbGw9IiNmYzAiIC8+PHBhdGggZD0iTTI0NS41IDE3MlYxMGgxNTN2MTYyczMyNCA0OTUgMTk4IDQ5NWgtNTU4Yy0xMjYgMCAyMDctNDk1IDIwNy00OTV6bTEyNiA1NGg1Nm0tMTMgNzJoNTZtLTkgNzJoNTZtLTIwIDcyaDU2bS0yMiA3Mmg1Nm0tMjkgNzJoNTZtLTQ1Ny00NWMyMC44IDQxLjcgODcuMyA4MSAxNjAuNyA4MSA3Mi4xIDAgMTQyLjEtMzguMiAxNjMuNC04MSIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDAwIiBzdHJva2UtbWl0ZXJsaW1pdD0iMTAiIHN0cm9rZS13aWR0aD0iMjAiIC8+PHBhdGggZD0iTTI3My4zIDQyMS43YzAgMzEtOS44IDU2LjMtMjEuOSA1Ni4zcy0yMS44LTI1LjItMjEuOC01Ni4zIDkuOC01Ni4zIDIxLjgtNTYuMyAyMS45IDI1LjIgMjEuOSA1Ni4zem0xMTQuNC01Ni4zYy0xMiAwLTIxLjggMjUuMi0yMS44IDU2LjNzOS43IDU2LjMgMjEuOCA1Ni4zIDIxLjktMjUuMiAyMS45LTU2LjMtOS44LTU2LjMtMjEuOS01Ni4zek0xNTAuMSA1MjYuNmMtMTguMiA2LjctMjcuNSAyMi45LTIzLjIgMzAuMnMxNC44LTUuNSAzMy0xMi4yIDM3LjQtNC45IDMzLTEyLjItMjQuNS0xMi42LTQyLjgtNS44em0yOTYgNS44Yy00LjIgNy4zIDE0LjkgNS41IDMzLjEgMTIuMnMyOC43IDE5LjUgMzMgMTIuMi01LTIzLjUtMjMuMi0zMC4yLTM4LjUtMS41LTQyLjggNS44eiIgLz48L3N2Zz4=)

[Which authors of this paper are endorsers?](/auth/show-endorsers/2502.07578) \| [Disable MathJax](javascript:setMathjaxCookie()) ([What is MathJax?](https://info.arxiv.org/help/mathjax.html))
