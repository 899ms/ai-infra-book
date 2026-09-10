<!-- 从 004-pnnl.html 迁移的资料快照；原始 HTML SHA-256: 164ac89acca43c902306711a93026c8104d687a5839a3286e87918f4e3344735。 -->

## Breadcrumb

1.  [Home](/)
2.  [Publications & Reports](/publications-reports)

August 6, 2024

Conference Paper

## DS-GL: Advancing Graph Learning via Harnessing the Power of Nature within Dynamic Systems

Share: [Share on Facebook](https://www.facebook.com/dialog/share?app_id=269100523864066&display=popup&href=https%3A%2F%2Fwww.pnnl.gov%2Fpublications%2Fds-gl-advancing-graph-learning-harnessing-power-nature-within-dynamic-systems) [Share on X (formerly Twitter)](http://twitter.com/share?url=https%3A%2F%2Fwww.pnnl.gov%2Fpublications%2Fds-gl-advancing-graph-learning-harnessing-power-nature-within-dynamic-systems&text=DS-GL%3A%20Advancing%20Graph%20Learning%20via%20Harnessing%20the%20Power%20of%20Nature%20within%20Dynamic%20Systems) [Share on LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fwww.pnnl.gov%2Fpublications%2Fds-gl-advancing-graph-learning-harnessing-power-nature-within-dynamic-systems&text=DS-GL%3A%20Advancing%20Graph%20Learning%20via%20Harnessing%20the%20Power%20of%20Nature%20within%20Dynamic%20Systems) [Email To:](mailto:?&subject=DS-GL%3A%20Advancing%20Graph%20Learning%20via%20Harnessing%20the%20Power%20of%20Nature%20within%20Dynamic%20Systems&body=https%3A%2F%2Fwww.pnnl.gov%2Fpublications%2Fds-gl-advancing-graph-learning-harnessing-power-nature-within-dynamic-systems)

## Abstract

With the rapid digitization of the world, an increasing number of real-world applications are turning to nonEuclidean data, modeled as graphs. Due to their intrinsic high complexity and irregularity, learning from graph data demands tremendous computational power. Recently, CMOS-compatible Ising machines, i.e., dynamic systems composed of CMOS components, have emerged as a new approach that harnesses the inherent power of natural annealing within dynamic systems to efficiently resolve binary optimization problems and have been adopted for traditional graph computation, such as max-cut. However, when performing complex Graph Learning (GL) tasks, Ising machines face significant hurdles: (i) they are inherently binary and thus ill-suited for real-valued problems; (ii) their expensive all-to-all coupling network that guarantees effective natural annealing poses daunting scalability concerns. To address these challenges, this paper proposes a nature-powered graph learning framework dubbed DS-GL, which is the first effort to transform the process of solving graph learning problems into the natural annealing process within a parameterized dynamic system embodied as a CMOS chip. To tackle the two major hurdles, DS-GL first augments the Ising machine architecture to modify the self-reaction term of its Hamiltonian function from linear to quadratic, effectively serving as an energy regulator. This adjustment maintains the system’s original physical interpretation while enabling it to process continuous, real-valued data. Second, to address the scaling issue, DS-GL further upgrades the real-valued dense Ising machine by decomposing it into a mesh-based multi-PE dynamic system that supports efficient distributed spatial-temporal co-annealing across different PEs through sparse interconnects. By exploiting the inherent sparsity and component structures in real-world graphs, DS-GL is able to map complex graph learning tasks onto the scalable dynamic system while maintaining high accuracy. Evaluations with three diverse GL applications across six real-world datasets, including traffic flow and COVID-19 prediction, show that DS-GL can deliver from 102× to 106× speedups and 500× energy reduction over Graph Neural Networks on GPUs, with 5% - 20% accuracy enhancement.

*Published: August 6, 2024*

## Citation

Song R., C. Wu, C. Liu, A. Li, M. Huang, and T. Geng. 2024. DS-GL: Advancing Graph Learning via Harnessing the Power of Nature within Dynamic Systems. In *ACM/IEEE 51st Annual International Symposium on Computer Architecture (ISCA 2024), June 29-July 3, 2024, Buenos Aires, Argentina*, 45-57. Los Alamitos, California:IEEE Computer Society. PNNL-SA-196761. [doi:10.1109/ISCA59077.2024.00014](https://www.doi.org/10.1109/ISCA59077.2024.00014)

### Research topics

[High-Performance Computing](/high-performance-computing)

[Graph and Data Analytics](/graph-and-data-analytics)

[Artificial Intelligence](/artificial-intelligence)

#### Related Content

AUGUST 20, 2026

Article

### [Improving the Prediction Ability of Spiking Neural Networks](/publications/improving-prediction-ability-spiking-neural-networks)

[Read](/publications/improving-prediction-ability-spiking-neural-networks)

[](/publications/improving-prediction-ability-spiking-neural-networks)

![Illustration of a starburst like network and multicolored wave](/sites/default/files/styles/thumbnail/public/media/image/IDSD_0067_WEB_SNN-NeuralNetwork_v1.jpg?h=b4f59d0b&itok=DWhP2zhF)

AUGUST 7, 2026

Article

### [PNNL Contributes to a Safe World Cup](/publications/pnnl-contributes-safe-world-cup)

[Read](/publications/pnnl-contributes-safe-world-cup)

[](/publications/pnnl-contributes-safe-world-cup)

![This photo shows scientist Nick Betzsold, sitting, looking at a monitor on a desk. A large screen to his right shows Super Bowl action.](/sites/default/files/styles/thumbnail/public/media/image/Betzsold%20Super%20Bowl_0.jpg?h=71976bb4&itok=iDXE1nZy)

JUNE 9, 2026

Article

### [New PNNL-OSU Partnership Expands on Years of Collaboration](/publications/new-pnnl-osu-partnership-expands-years-collaboration)

[Read](/publications/new-pnnl-osu-partnership-expands-years-collaboration)

[](/publications/new-pnnl-osu-partnership-expands-years-collaboration)

![PNNL and OSU sign MOU](/sites/default/files/styles/thumbnail/public/media/image/20260504%20URM%20PNNL%20Visit-65.jpg?h=e45be382&itok=risZRYfv)

[See All Publications & Reports](/publications-reports)
