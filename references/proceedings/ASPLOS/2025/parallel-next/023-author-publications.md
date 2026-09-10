<!-- 从 023-author-publications.html 迁移的资料快照；原始 HTML SHA-256: 831e93202dcc69a46055ba29b234e1889381940a96b8feec0fb8b83450249fd1。 -->

# Publications

## 2025

1.  CCGrid 2025

    rInfer: A Generic and High-Performance Framework for Remote Inference with Heterogeneous Accelerators

    **Zhen Jin**, Yiquan Chen, Yijing Wang, Yin Du, Keyao Zhang, Jiexiong Xu, Wenhai Lin, Jingchang Qin, Kanghua Fang, and Wenzhi Chen

    *In 2025 IEEE 25th International Symposium on Cluster, Cloud and Internet Computing (CCGrid)*, 2025

    [DOI](https://doi.org/10.1109/CCGRID64434.2025.00052)

2.  ASPLOS 2025

    OS2G: A High-Performance DPU Offloading Architecture for GPU-based Deep Learning with Object Storage

    **Zhen Jin**, Yiquan Chen, Mingxu Liang, Yijing Wang, Guoju Fang, Ao Zhou, Keyao Zhang, Jiexiong Xu, Wenhai Lin, Yiquan Lin, Shushu Zhao, Wenkai Shi, Zhenhua He, Shishun Cai, and Wenzhi Chen

    *In Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 2*, Rotterdam, Netherlands, 2025

    [DOI](https://doi.org/10.1145/3676641.3716265)

3.  HPCA 2025

    NVMePass: A Lightweight, High-performance and Scalable NVMe Virtualization Architecture with I/O Queues Passthrough

    Yiquan Chen^(\*), **Zhen Jin^(\*)**, Yijing Wang, Yi Chen, Jiexiong Xu, Hao Yu, Jinlong Chen, Wenhai Lin, Kanghua Fang, Keyao Zhang, Chengkun Wei, Qiang Liu, Yuan Xie, and Wenzhi Chen

    *In 2025 IEEE International Symposium on High Performance Computer Architecture (HPCA)* , Mar 2025

    Abs [DOI](https://doi.org/10.1109/HPCA61900.2025.00105)

    Most data-intensive applications currently run on NVMe storage, and virtualization is essential in cloud computing. Existing NVMe virtualization technologies include software-based and hardware-assisted. Virtio suffers from severe performance degradation, and polling-based solutions consume too many valuable CPU resources. Hardware-assisted solutions provide high performance and no CPU usage but have the challenges of developing dedicated hardware.In this paper, we propose NVMePass, a novel software-hardware co-design NVMe passthrough virtualization architecture designed to achieve high performance and no CPU overhead while maintaining high scalability. The key ideas of NVMePass are NVMe I/O queues passthrough for VMs and a mechanism to ensure security. The NVMePass supports DMA and interrupts remapping for VMs without hypervisor involvement, eliminating virtualization overhead and providing near-native performance. Isolation is achieved by I/O queues and logical block address resources exclusively allocated to VMs. We propose NVMe Resource Domain (NRD) and implement it in the NVMe controller to intercept illegal I/O requests. Thus, isolation and security are fully achieved. Results from our experiments show that NVMePass can provide comparable performance to VFIO, with an IOPS of \mathbf1 0 0. 1 % - 1 0 0. 5 % of VFIO. Furthermore, compared to SPDK-Vhost, NVMePass achieves \mathbf4 0. 0 % lower latency when running 150 VMs, and NVMePass has an improvement of \mathbf6 8. 0 % OPS performance in a real-world application when running 100 VMs.

## 2024

1.  HPCA 2024

    LightPool: A NVMe-oF-based High-performance and Lightweight Storage Pool Architecture for Cloud-Native Distributed Database

    Jiexiong Xu, Yiquan Chen, Yijing Wang, Wenhui Shi, Guoju Fang, Yi Chen, Huasheng Liao, Yang Wang, Hai Lin, **Zhen Jin**, Qiang Liu, and Wenzhi Chen

    *In 2024 IEEE International Symposium on High-Performance Computer Architecture (HPCA)*, Mar 2024

    [DOI](https://doi.org/10.1109/HPCA57654.2024.00079)

2.  CCGrid 2024

    CINDA: Don’t Ignore Instructions When Cloning Memory Access Behavior

    Wenhai Lin, Yiquan Chen, Jiexiong Xu, **Zhen Jin**, Peiyu Liu, Shishun Cai, Yuzhong Zhang, Jingchang Qin, Yiquan Lin, and Wenzhi Chen

    *In 2024 IEEE 24th International Symposium on Cluster, Cloud and Internet Computing (CCGrid)*, Mar 2024

    [DOI](https://doi.org/10.1109/CCGrid59990.2024.00063)

3.  CCGrid 2024

    BlueJay: A Platform to Quantifying the Impact of Memory Latency on Datacenter Application Performance

    Jingchang Qin, Yiquan Chen, Shishun Cai, Wenhai Lin, Jiexiong Xu, **Zhen Jin**, Lifa Cao, Zijie Zheng, Yuzhong Zhang, Yi Chen, and Wenzhi Chen

    *In 2024 IEEE 24th International Symposium on Cluster, Cloud and Internet Computing (CCGrid)*, Mar 2024

    [DOI](https://doi.org/10.1109/CCGrid59990.2024.00061)

4.  IEEE Micro 2024

    Optimizing NVMe Storage for Large-Scale Deployment: Key Technologies and Strategies in Alibaba Cloud

    Yiquan Chen, Yuan Xie, Yijing Wang, Jiexiong Xu, **Zhen Jin**, Anyu Li, Xiaoyan Fu, Qiang Liu, and Wenzhi Chen

    *IEEE Micro*, Mar 2024

    [DOI](https://doi.org/10.1109/MM.2024.3426514)

5.  TCAD 2024

    PARS: A Pattern-Aware Spatial Data Prefetcher Supporting Multiple Region Sizes

    Yiquan Lin, Wenhai Lin, Jiexiong Xu, Yiquan Chen, **Zhen Jin**, Jingchang Qin, Jiahao He, Shishun Cai, Yuzhong Zhang, Zonghui Wang, and Wenzhi Chen

    *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems*, Mar 2024

    [DOI](https://doi.org/10.1109/TCAD.2024.3442981)

6.  Electronics 2024

    BTIP: Branch Triggered Instruction Prefetcher Ensuring Timeliness

    Wenhai Lin, Yiquan Lin, Yiquan Chen, Shishun Cai, **Zhen Jin**, Jiexiong Xu, Yuzhong Zhang, and Wenzhi Chen

    *Electronics*, Mar 2024

## 2023

1.  CLUSTER 2023

    JACO: JAva Code Layout Optimizer Enabling Continuous Optimization without Pausing Application Services

    Wenhai Lin, Jingchang Qin, Yiquan Chen, **Zhen Jin**, Jiexiong Xu, Yuzhong Zhang, Shishun Cai, Lirong Fu, Yi Chen, and Wenzhi Chen

    *In 2023 IEEE International Conference on Cluster Computing (CLUSTER)*, Mar 2023

    [DOI](https://doi.org/10.1109/CLUSTER52292.2023.00032)

2.  CCGrid 2023

    HyQ: Hybrid I/O Queue Architecture for NVMe over Fabrics to Enable High- Performance Hardware Offloading

    Yiquan Chen, Jinlong Chen, Yijing Wang, Yi Chen, **Zhen Jin**, Jiexiong Xu, Guoju Fang, Wenhai Lin, Chengkun Wei, and Wenzhi Chen

    *In 2023 IEEE/ACM 23rd International Symposium on Cluster, Cloud and Internet Computing (CCGrid)*, Mar 2023

    [DOI](https://doi.org/10.1109/CCGrid57682.2023.00012)
