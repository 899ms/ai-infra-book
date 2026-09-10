<!-- 从 116-arxiv.html 迁移的资料快照；原始 HTML SHA-256: 2cb4becd45229aa318a80bf5f1cd6c11d86493cfddb29762b7c353fbfc7a4640。 -->

# Computer Science \> Machine Learning

**arXiv:2410.18038** (cs)

\[Submitted on 23 Oct 2024 ([v1](https://arxiv.org/abs/2410.18038v1)), last revised 16 Feb 2025 (this version, v2)\]

# Title:POD-Attention: Unlocking Full Prefill-Decode Overlap for Faster LLM Inference

Authors:[Aditya K Kamath](https://arxiv.org/search/cs?searchtype=author&query=Kamath,+A+K), [Ramya Prabhu](https://arxiv.org/search/cs?searchtype=author&query=Prabhu,+R), [Jayashree Mohan](https://arxiv.org/search/cs?searchtype=author&query=Mohan,+J), [Simon Peter](https://arxiv.org/search/cs?searchtype=author&query=Peter,+S), [Ramachandran Ramjee](https://arxiv.org/search/cs?searchtype=author&query=Ramjee,+R), [Ashish Panwar](https://arxiv.org/search/cs?searchtype=author&query=Panwar,+A)

View a PDF of the paper titled POD-Attention: Unlocking Full Prefill-Decode Overlap for Faster LLM Inference, by Aditya K Kamath and 5 other authors

[View PDF](/pdf/2410.18038) [HTML (experimental)](https://arxiv.org/html/2410.18038v2)

> Abstract:Each request in LLM inference goes through two phases: compute-bound prefill and memory-bandwidth-bound decode. To improve GPU utilization, recent systems use hybrid batching that combines the prefill and decode phases of different requests into the same batch. This approach optimizes linear operations but remains inefficient for attention computation because existing attention kernels specialize execution independently for the prefill and decode phases.  
> In this paper, we present POD-Attention - the first GPU kernel that efficiently computes attention for hybrid batches. POD-Attention aims to maximize the utilization of both compute and memory bandwidth by carefully allocating the GPU's resources such that prefill and decode operations happen concurrently on the same multiprocessor. POD-Attention speeds up attention computation by up to \$59\\\$ (mean \$28\\\$), enabling higher throughput and lower latency LLM inference compared to the use of independently optimized prefill and decode attention kernels.

[TABLE]

## Submission history

From: Aditya Kamath \[[view email](/show-email/915059ca/2410.18038)\]  
**[\[v1\]](/abs/2410.18038v1)** Wed, 23 Oct 2024 17:06:56 UTC (7,321 KB)  
**\[v2\]** Sun, 16 Feb 2025 18:09:25 UTC (7,357 KB)  

Full-text links:

## Access Paper:

- View a PDF of the paper titled POD-Attention: Unlocking Full Prefill-Decode Overlap for Faster LLM Inference, by Aditya K Kamath and 5 other authors

- [View PDF](/pdf/2410.18038)

- [HTML (experimental)](https://arxiv.org/html/2410.18038v2)

- [TeX Source](/src/2410.18038)

[![license icon](https://arxiv.org/icons/licenses/by-4.0.png) view license](http://creativecommons.org/licenses/by/4.0/ "Rights to this article")

### Current browse context:

cs.LG

[\< prev](/prevnext?id=2410.18038&function=prev&context=cs.LG "previous in cs.LG (accesskey p)")   \|   [next \>](/prevnext?id=2410.18038&function=next&context=cs.LG "next in cs.LG (accesskey n)")   

[new](/list/cs.LG/new) \| [recent](/list/cs.LG/recent) \| [2024-10](/list/cs.LG/2024-10)

Change to browse by:

[cs](/abs/2410.18038?context=cs)  
[cs.DC](/abs/2410.18038?context=cs.DC)  

### References & Citations

- [NASA ADS](https://ui.adsabs.harvard.edu/abs/arXiv:2410.18038)
- [Google Scholar](https://scholar.google.com/scholar_lookup?arxiv_id=2410.18038)
- [Semantic Scholar](https://api.semanticscholar.org/arXiv:2410.18038)

export BibTeX citation

Loading...

## BibTeX formatted citation

×

Data provided by:

### Bookmark

[![BibSonomy](/static/browse/0.3.4/images/icons/social/bibsonomy.png)](http://www.bibsonomy.org/BibtexHandler?requTask=upload&url=https://arxiv.org/abs/2410.18038&description=POD-Attention:%20Unlocking%20Full%20Prefill-Decode%20Overlap%20for%20Faster%20LLM%20Inference "Bookmark on BibSonomy") [![Reddit](/static/browse/0.3.4/images/icons/social/reddit.png)](https://reddit.com/submit?url=https://arxiv.org/abs/2410.18038&title=POD-Attention:%20Unlocking%20Full%20Prefill-Decode%20Overlap%20for%20Faster%20LLM%20Inference "Bookmark on Reddit")

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

IArxiv recommender toggle

IArxiv Recommender *([What is IArxiv?](https://iarxiv.org/about))*

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

[Which authors of this paper are endorsers?](/auth/show-endorsers/2410.18038) \| [Disable MathJax](javascript:setMathjaxCookie()) ([What is MathJax?](https://info.arxiv.org/help/mathjax.html))
