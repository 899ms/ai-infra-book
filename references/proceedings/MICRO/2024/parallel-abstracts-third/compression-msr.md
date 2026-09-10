<!-- 从 compression-msr.html 迁移的资料快照；原始 HTML SHA-256: 28a7cd325ecd409dd958735fdf18b4f8090e3701da87615f0ebd1e9ed5bcac94。 -->

# Memory Allocation under Hardware Compression

- Muhammad Laghari ,
- Yuqing Liu ,
- Gagandeep Panwar ,
- David Bears ,
- Chandler Jearls ,
- Raghavendra Srinivas ,
- [Esha Choukse](https://www.microsoft.com/en-us/research/people/eschouks/) ,
- Kirk Cameron ,
- Ali R. Butt ,
- Xun Jian

***[MICRO](https://microarch.org/micro57/)*** \| November 2024

[Download BibTex](https://www.microsoft.com/en-us/research/publication/memory-allocation-under-hardware-compression/bibtex/)

As the scaling of DRAM density slows physically, a promising solution is to scale it up logically via hardware memory compression, which enhances CPU’s memory controller (MC) to squeeze more data into DRAM. Hardware-compressed memory decouples OS-managed physical memory from actual memory (i.e., DRAM); the MC spends a dynamically varying amount of DRAM on each physical page, depending on how compressible are its values.

The newly-decoupled actual memory effectively forms a new layer of memory beyond the traditional layers of virtual, pseudo- physical, and physical memory. We note unlike these traditional memory layers, each with its own specialized allocation interface (e.g., malloc/mmap for virtual memory, page tables+MMU for physical memory), this new layer of memory introduced by hardware memory compression still awaits its own unique memory allocation interface; its absence makes the allocation of actual memory imprecise and, sometimes, even impossible.

Imprecisely allocating less actual memory, and/or unable to allocate more, can harm performance. Even imprecisely allocating more actual memory to some jobs can be harmful as it can lead to allocating less to other jobs in highly-consolidated/utilized memory systems, where compression is useful.

To restore precise memory allocation, we design a new memory allocation specialized for this new layer of memory by architecting a new MMU-like component to add to the memory controller and tackling the corresponding design challenges. In our full-system FPGA evaluations, jobs perform stably when colocated with jobs of different sizes (e.g., with only 1%-2% average performance variation, down from 19%-89% under the prior art).

Opens in a new tab

[Publication](https://www.microsoft.com/en-us/research/people/eschouks/publications/)

## Research Areas

- [Systems and networking](https://www.microsoft.com/en-us/research/research-area/systems-and-networking/)
