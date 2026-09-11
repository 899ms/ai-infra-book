<!-- 从 cuda-compute-capabilities.html 迁移的资料快照；原始 HTML SHA-256: 8f467ad0224a5f2f1b387ae40b222b0bce1b12c2fc56a41d083b85d5e48a4ef8。 -->

<div id="main-content" class="bd-main" role="main">

<div class="bd-content">

<div class="bd-article-container">

<div class="bd-header-article d-print-none">

<div class="header-article-items header-article__inner">

<div class="header-article-items__start">

<div class="header-article-item">

- <a href="../contents.html" class="nav-link" aria-label="Home"><em></em></a>
- <a href="../index.html" class="nav-link">CUDA Programming Guide</a>
- <a href="../part5.html" class="nav-link"><span class="section-number">5. </span>Technical Appendices</a>
- <span class="ellipsis"><span class="section-number">5.1. </span>Compute Capabilities</span>

</div>

</div>

<div class="header-article-items__end">

<div class="header-article-item">

<div class="header-article-item">

<div class="d-flex justify-content-end w-100">

<a href="https://surveys.hotjar.com/4904bf71-6484-47a7-83ff-4715cceabdb5" id="openPopupButton">Is this page helpful?</a>

</div>

</div>

</div>

</div>

</div>

</div>

<div id="searchbox">

</div>

<div id="compute-capabilities" class="section">

<span id="id1"></span>

# <span class="section-number">5.1. </span>Compute Capabilities<a href="#compute-capabilities" class="headerlink" title="Link to this heading">#</a>

The general specifications and features of a compute device depend on its compute capability (see <a href="../01-introduction/cuda-platform.html#cuda-platform-compute-capability-sm-version" class="reference internal"><span class="std std-ref">Compute Capability and Streaming Multiprocessor Versions</span></a>).

<a href="#compute-capabilities-table-features-and-technical-specifications-feature-support-per-compute-capability" class="reference internal"><span class="std std-numref">Table 29</span></a>, <a href="#compute-capabilities-table-device-and-streaming-multiprocessor-sm-information-per-compute-capability" class="reference internal"><span class="std std-numref">Table 30</span></a>, and <a href="#compute-capabilities-table-memory-information-per-compute-capability" class="reference internal"><span class="std std-numref">Table 31</span></a> show the features and technical specifications associated with each compute capability that is currently supported.

All NVIDIA GPU architectures use a little-endian representation.

<div id="obtain-the-gpu-compute-capability" class="section">

<span id="compute-capabilities-querying"></span>

## <span class="section-number">5.1.1. </span>Obtain the GPU Compute Capability<a href="#obtain-the-gpu-compute-capability" class="headerlink" title="Link to this heading">#</a>

The <a href="https://developer.nvidia.com/cuda-gpus" class="reference external">CUDA GPU Compute Capability</a> page provides a comprehensive mapping from NVIDIA GPU models to their compute capability.

Alternatively, the <a href="https://docs.nvidia.com/deploy/nvidia-smi/index.html" class="reference external">nvidia-smi</a> tool, provided with the <a href="https://www.nvidia.com/en-us/drivers/" class="reference external">NVIDIA Driver</a>, can be used to get the compute capability of a GPU. For example, the following command will output the GPU names and compute capabilities available on the system:

<div class="highlight-bash notranslate">

<div class="highlight">

    nvidia-smi --query-gpu=name,compute_cap

</div>

</div>

At runtime, the compute capability can be obtained using the CUDA Runtime API <a href="https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__DEVICE.html#group__CUDART__DEVICE_1gb22e8256592b836df9a9cc36c9db7151" class="reference external">cudaDeviceGetAttribute()</a> , CUDA Driver API <a href="https://docs.nvidia.com/cuda/cuda-driver-api/group__CUDA__DEVICE.html#group__CUDA__DEVICE_1g9c3e1414f0ad901d3278a4d6645fc266" class="reference external">cuDeviceGetAttribute()</a>, or NVML API <a href="https://docs.nvidia.com/deploy/nvml-api/group__nvmlDeviceQueries.html#group__nvmlDeviceQueries_1g1f803a2fb4b7dfc0a8183b46b46ab03a" class="reference external">nvmlDeviceGetCudaComputeCapability()</a>:

<div class="highlight-c++ notranslate">

<div class="highlight">

    #include <cuda_runtime_api.h>

    int computeCapabilityMajor, computeCapabilityMinor;
    cudaDeviceGetAttribute(&computeCapabilityMajor, cudaDevAttrComputeCapabilityMajor, device_id);
    cudaDeviceGetAttribute(&computeCapabilityMinor, cudaDevAttrComputeCapabilityMinor, device_id);

</div>

</div>

<div class="highlight-c++ notranslate">

<div class="highlight">

    #include <cuda.h>

    int computeCapabilityMajor, computeCapabilityMinor;
    cuDeviceGetAttribute(&computeCapabilityMajor, CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MAJOR, device_id);
    cuDeviceGetAttribute(&computeCapabilityMinor, CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MINOR, device_id);

</div>

</div>

<div class="highlight-c++ notranslate">

<div class="highlight">

    #include <nvml.h> // required linking with -lnvidia-ml

    int computeCapabilityMajor, computeCapabilityMinor;
    nvmlDeviceGetCudaComputeCapability(nvmlDevice, &computeCapabilityMajor, &computeCapabilityMinor);

</div>

</div>

</div>

<div id="feature-availability" class="section">

<span id="compute-capabilities-feature-availability"></span>

## <span class="section-number">5.1.2. </span>Feature Availability<a href="#feature-availability" class="headerlink" title="Link to this heading">#</a>

Most compute features introduced with a compute architecture are intended to be available on all subsequent architectures. This is shown in <a href="#compute-capabilities-table-features-and-technical-specifications-feature-support-per-compute-capability" class="reference internal"><span class="std std-numref">Table 29</span></a> by the “yes” for availability of a feature on compute capabilities subsequent to its introduction.

<div id="architecture-specific-features" class="section">

<span id="compute-capabilities-architecture-specific-features"></span>

### <span class="section-number">5.1.2.1. </span>Architecture-Specific Features<a href="#architecture-specific-features" class="headerlink" title="Link to this heading">#</a>

Beginning with devices of Compute Capability 9.0, specialized compute features that are introduced with an architecture may not be guaranteed to be available on all subsequent compute capabilities. These features are called *architecture-specific* features and target acceleration of specialized operations, such as Tensor Core operations, which are not intended for all classes of compute capabilities or may significantly change in future generations. Code must be compiled with an architecture-specific compiler target (see <a href="#compute-capabilities-feature-set-compiler-targets" class="reference internal"><span class="std std-ref">Feature Set Compiler Targets</span></a>) to enable architecture-specific features. Code compiled with an architecture-specific compiler target can only be run on the exact compute capability it was compiled for.

</div>

<div id="family-specific-features" class="section">

<span id="compute-capabilities-family-specific-features"></span>

### <span class="section-number">5.1.2.2. </span>Family-Specific Features<a href="#family-specific-features" class="headerlink" title="Link to this heading">#</a>

Beginning with devices of Compute Capability 10.0, some architecture-specific features are common to devices of more than one compute capability. The devices that contain these features are part of the same family and these features can also be called *family-specific* features. Family-specific features are guaranteed to be available on all devices in the same family. A family-specific compiler target is required to enable family-specific features. See <a href="#compute-capabilities-feature-set-compiler-targets" class="reference internal"><span class="std std-numref">Section 5.1.2.3</span></a>. Code compiled for a family-specific target can only be run on GPUs which are members of that family.

</div>

<div id="feature-set-compiler-targets" class="section">

<span id="compute-capabilities-feature-set-compiler-targets"></span>

### <span class="section-number">5.1.2.3. </span>Feature Set Compiler Targets<a href="#feature-set-compiler-targets" class="headerlink" title="Link to this heading">#</a>

There are three sets of compute features which the compiler can target:

**Baseline Feature Set**: The predominant set of compute features that are introduced with the intent to be available for subsequent compute architectures. These features and their availability are summarized in <a href="#compute-capabilities-table-features-and-technical-specifications-feature-support-per-compute-capability" class="reference internal"><span class="std std-numref">Table 29</span></a>.

**Architecture-Specific Feature Set**: A small and highly specialized set of features called architecture-specific, that are introduced to accelerate specialized operations, which are not guaranteed to be available or might change significantly on subsequent compute architectures. These features are summarized in the respective “Compute Capability \#.#” subsections. The architecture-specific feature set is a superset of the family-specific feature set. Architecture-specific compiler targets were introduced with Compute Capability 9.0 devices and are selected by using an **a** suffix in the compilation target, for example by specifying <span class="pre">`compute_100a`</span> or <span class="pre">`compute_120a`</span> as the compute target.

**Family-Specific Feature Set**: Some architecture-specific features are common to GPUs of more than one compute capability. These features are summarized in the respective “Compute Capability \#.#” subsections. With a few exceptions, later-generation devices with the same major compute capability are in the same family. <a href="#compute-capabilities-family-specific-compatibility" class="reference internal"><span class="std std-numref">Table 28</span></a> indicates the compatibility of family-specific targets with device compute capability, including exceptions. The family-specific feature set is a superset of the baseline feature set. Family-specific compiler targets were introduced with Compute Capability 10.0 devices and are selected by using an **f** suffix in the compilation target, for example by specifying <span class="pre">`compute_100f`</span> or <span class="pre">`compute_120f`</span> as the compute target.

All devices starting from compute capability 9.0 have a set of features that are architecture-specific. To utilize the complete set of these features on a specific GPU, the architecture-specific compiler target with the suffix **a** must be used. Additionally, starting from compute capability 10.0, there are sets of features that appear in multiple devices with different minor compute capabilities. These sets of instructions are called family-specific features, and the devices which share these features are said to be part of the same family. The family-specific features are a subset of the architecture-specific features that are shared by all members of that GPU family. The family-specific compiler target with the suffix **f** allows the compiler to generate code that uses this common subset of architecture-specific features.

For example:

- The <span class="pre">`compute_100`</span> compilation target does not allow the use of architecture-specific features. This target will be compatible with all devices of compute capability 10.0 and later.

- The <span class="pre">`compute_100f`</span> *family-specific* compilation target allows the use of the subset of architecture-specific features that are common across the GPU family. This target will only be compatible with devices that are part of the GPU family. In this example, it is compatible with devices of Compute Capability 10.0 and Compute Capability 10.3. The features available in the family-specific <span class="pre">`compute_100f`</span> target are a superset of the features available in the baseline <span class="pre">`compute_100`</span> target.

- The <span class="pre">`compute_100a`</span> *architecture-specific* compilation target allows the use of the complete set of architecture-specific features in Compute Capability 10.0 devices. This target will only be compatible with devices of Compute Capability 10.0 and no others. The features available in the <span class="pre">`compute_100a`</span> target form a superset of the features available in the <span class="pre">`compute_100f`</span> target.

<div class="pst-scrollable-table-container">

<table id="compute-capabilities-family-specific-compatibility" class="table-no-stripes table">
<caption><span class="caption-number">Table 28 </span><span class="caption-text">Family-Specific Compatibility</span><a href="#compute-capabilities-family-specific-compatibility" class="headerlink" title="Link to this table">#</a></caption>
<thead>
<tr class="row-odd">
<th class="head"><p>Compilation Target</p></th>
<th colspan="2" class="head"><p>Compatible with Compute Capability</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even">
<td><p><span class="pre"><code class="docutils literal notranslate">compute_100f</code></span></p></td>
<td><p>10.0</p></td>
<td><p>10.3</p></td>
</tr>
<tr class="row-odd">
<td><p><span class="pre"><code class="docutils literal notranslate">compute_103f</code></span></p></td>
<td colspan="2"><p>10.3 <a href="#fn1" class="footnote-ref" id="fnref1" role="doc-noteref"><sup>1</sup></a></p></td>
</tr>
<tr class="row-even">
<td><p><span class="pre"><code class="docutils literal notranslate">compute_110f</code></span></p></td>
<td colspan="2"><p>11.0 <a href="#fn2" class="footnote-ref" id="fnref2" role="doc-noteref"><sup>2</sup></a></p></td>
</tr>
<tr class="row-odd">
<td><p><span class="pre"><code class="docutils literal notranslate">compute_120f</code></span></p></td>
<td><p>12.0</p></td>
<td><p>12.1</p></td>
</tr>
<tr class="row-even">
<td><p><span class="pre"><code class="docutils literal notranslate">compute_121f</code></span></p></td>
<td colspan="2"><p>12.1 <a href="#fn3" class="footnote-ref" id="fnref3" role="doc-noteref"><sup>3</sup></a></p></td>
</tr>
</tbody>
</table>
<section id="footnotes" class="footnotes footnotes-end-of-document" role="doc-endnotes">
<hr />
<ol>
<li id="fn1"></li>
<li id="fn2"></li>
<li id="fn3"></li>
</ol>
</section>

</div>

<span class="label"><span class="fn-bracket">\[</span>1<span class="fn-bracket">\]</span></span> <span class="backrefs">(<a href="#id2" role="doc-backlink">1</a>,<a href="#id3" role="doc-backlink">2</a>,<a href="#id4" role="doc-backlink">3</a>)</span>

Some families only contain a single member when they are created. They may be expanded in the future to include more devices.

</div>

</div>

<div id="features-and-technical-specifications" class="section">

<span id="compute-capabilities-features-and-technical-specifications"></span>

## <span class="section-number">5.1.3. </span>Features and Technical Specifications<a href="#features-and-technical-specifications" class="headerlink" title="Link to this heading">#</a>

<div class="pst-scrollable-table-container">

<table id="compute-capabilities-table-features-and-technical-specifications-feature-support-per-compute-capability" class="small table-no-stripes longtable table">
<caption><span class="caption-number">Table 29 </span><span class="caption-text">Feature Support per Compute Capability</span><a href="#compute-capabilities-table-features-and-technical-specifications-feature-support-per-compute-capability" class="headerlink" title="Link to this table">#</a></caption>
<thead>
<tr class="row-odd">
<th class="head"><p><strong>Feature Support</strong></p></th>
<th colspan="6" class="head"><p><strong>Compute Capability</strong></p></th>
</tr>
</thead>
<tbody>
<tr class="row-even">
<td><p>(Unlisted features are supported for all compute capabilities)</p></td>
<td><p>7.x</p></td>
<td><p>8.x</p></td>
<td><p>9.0</p></td>
<td><p>10.x</p></td>
<td><p>11.0</p></td>
<td><p>12.x</p></td>
</tr>
<tr class="row-odd">
<td><p>Atomic functions operating on 128-bit integer values in shared and global memory (<a href="cpp-language-extensions.html#atomic-functions" class="reference internal"><span class="std std-ref">Atomic Functions</span></a>)</p></td>
<td colspan="2"><p>No</p></td>
<td colspan="4"><p>Yes</p></td>
</tr>
<tr class="row-even">
<td><p>Atomic addition operating on <span class="pre"><code class="docutils literal notranslate">float2</code></span> and <span class="pre"><code class="docutils literal notranslate">float4</code></span> floating point vectors in global memory (<a href="cpp-language-extensions.html#atomicadd" class="reference internal"><span class="std std-ref">atomicAdd()</span></a>)</p></td>
<td colspan="2"><p>No</p></td>
<td colspan="4"><p>Yes</p></td>
</tr>
<tr class="row-odd">
<td><p>Warp reduce functions (<a href="cpp-language-extensions.html#warp-reduce-functions" class="reference internal"><span class="std std-ref">Warp Reduce Functions</span></a>)</p></td>
<td><p>No</p></td>
<td colspan="5"><p>Yes</p></td>
</tr>
<tr class="row-even">
<td><p>Bfloat16-precision floating-point operations</p></td>
<td><p>No</p></td>
<td colspan="5"><p>Yes</p></td>
</tr>
<tr class="row-odd">
<td><p>128-bit-precision floating-point operations</p></td>
<td colspan="3"><p>No</p></td>
<td colspan="3"><p>Yes</p></td>
</tr>
<tr class="row-even">
<td><p>Hardware-accelerated <span class="pre"><code class="docutils literal notranslate">memcpy_async</code></span> (<a href="../04-special-topics/pipelines.html#pipelines" class="reference internal"><span class="std std-ref">Pipelines</span></a>)</p></td>
<td><p>No</p></td>
<td colspan="5"><p>Yes</p></td>
</tr>
<tr class="row-odd">
<td><p>Hardware-accelerated Split Arrive/Wait Barrier (<a href="../04-special-topics/async-barriers.html#asynchronous-barriers" class="reference internal"><span class="std std-ref">Asynchronous Barriers</span></a>)</p></td>
<td><p>No</p></td>
<td colspan="5"><p>Yes</p></td>
</tr>
<tr class="row-even">
<td><p>L2 Cache Residency Management (<a href="../04-special-topics/l2-cache-control.html#advanced-kernels-l2-control" class="reference internal"><span class="std std-ref">L2 Cache Control</span></a>)</p></td>
<td><p>No</p></td>
<td colspan="5"><p>Yes</p></td>
</tr>
<tr class="row-odd">
<td><p>DPX Instructions for Accelerated Dynamic Programming (<a href="cpp-language-extensions.html#dpx-instructions" class="reference internal"><span class="std std-ref">Dynamic Programming eXtension (DPX) Instructions</span></a>)</p></td>
<td colspan="2"><p>Multiple Instr.</p></td>
<td colspan="2"><p>Native</p></td>
<td colspan="2"><p>Multiple Instr.</p></td>
</tr>
<tr class="row-even">
<td><p>Distributed Shared Memory</p></td>
<td colspan="2"><p>No</p></td>
<td colspan="4"><p>Yes</p></td>
</tr>
<tr class="row-odd">
<td><p>Thread Block Cluster (<a href="../02-basics/intro-to-cuda-cpp.html#thread-block-clusters" class="reference internal"><span class="std std-ref">Thread Block Clusters</span></a>)</p></td>
<td colspan="2"><p>No</p></td>
<td colspan="4"><p>Yes</p></td>
</tr>
<tr class="row-even">
<td><p>Tensor Memory Accelerator (TMA) unit (<a href="../04-special-topics/async-copies.html#async-copies-tma" class="reference internal"><span class="std std-ref">Using the Tensor Memory Accelerator (TMA)</span></a>)</p></td>
<td colspan="2"><p>No</p></td>
<td colspan="4"><p>Yes</p></td>
</tr>
</tbody>
</table>

</div>

Note that the KB and K units used in the following tables correspond to 1024 bytes (i.e., a KiB) and 1024 respectively.

<div class="pst-scrollable-table-container">

<table id="compute-capabilities-table-device-and-streaming-multiprocessor-sm-information-per-compute-capability" class="small table-no-stripes longtable table">
<caption><span class="caption-number">Table 30 </span><span class="caption-text">Device and Streaming Multiprocessor (SM) Information per Compute Capability</span><a href="#compute-capabilities-table-device-and-streaming-multiprocessor-sm-information-per-compute-capability" class="headerlink" title="Link to this table">#</a></caption>
<colgroup>
<col style="width: 42%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
<col style="width: 5%" />
</colgroup>
<thead>
<tr class="row-odd">
<th class="head"></th>
<th colspan="10" class="head"><p><strong>Compute Capability</strong></p></th>
</tr>
</thead>
<tbody>
<tr class="row-even">
<td></td>
<td><p>7.5</p></td>
<td><p>8.0</p></td>
<td><p>8.6</p></td>
<td><p>8.7</p></td>
<td><p>8.9</p></td>
<td><p>9.0</p></td>
<td><p>10.0</p></td>
<td><p>10.3</p></td>
<td><p>11.0</p></td>
<td><p>12.x</p></td>
</tr>
<tr class="row-odd">
<td><p>Ratio of FP32 to FP64 Throughput <a href="#fn1" class="footnote-ref" id="fnref1" role="doc-noteref"><sup>1</sup></a></p></td>
<td><p>32:1</p></td>
<td><p>2:1</p></td>
<td colspan="3"><p>64:1</p></td>
<td colspan="2"><p>2:1</p></td>
<td colspan="3"><p>64:1</p></td>
</tr>
<tr class="row-even">
<td><p>Maximum number of resident grids per device (Concurrent Kernel Execution)</p></td>
<td colspan="10"><p>128</p></td>
</tr>
<tr class="row-odd">
<td><p>Maximum dimensionality of a grid</p></td>
<td colspan="10"><p>3</p></td>
</tr>
<tr class="row-even">
<td><p>Maximum x-dimension of a grid</p></td>
<td colspan="10"><p>2<sup>31</sup>-1</p></td>
</tr>
<tr class="row-odd">
<td><p>Maximum y- or z-dimension of a grid</p></td>
<td colspan="10"><p>65535</p></td>
</tr>
<tr class="row-even">
<td><p>Maximum dimensionality of a thread block</p></td>
<td colspan="10"><p>3</p></td>
</tr>
<tr class="row-odd">
<td><p>Maximum x- or y-dimensionality of a thread block</p></td>
<td colspan="10"><p>1024</p></td>
</tr>
<tr class="row-even">
<td><p>Maximum z-dimension of a thread block</p></td>
<td colspan="10"><p>64</p></td>
</tr>
<tr class="row-odd">
<td><p>Maximum number of threads per block</p></td>
<td colspan="10"><p>1024</p></td>
</tr>
<tr class="row-even">
<td><p>Warp size</p></td>
<td colspan="10"><p>32</p></td>
</tr>
<tr class="row-odd">
<td><p>Maximum number of resident blocks per SM</p></td>
<td><p>16</p></td>
<td><p>32</p></td>
<td colspan="2"><p>16</p></td>
<td><p>24</p></td>
<td colspan="3"><p>32</p></td>
<td colspan="2"><p>24</p></td>
</tr>
<tr class="row-even">
<td><p>Maximum number of resident warps per SM</p></td>
<td><p>32</p></td>
<td><p>64</p></td>
<td colspan="3"><p>48</p></td>
<td colspan="3"><p>64</p></td>
<td colspan="2"><p>48</p></td>
</tr>
<tr class="row-odd">
<td><p>Maximum number of resident threads per SM</p></td>
<td><p>1024</p></td>
<td><p>2048</p></td>
<td colspan="3"><p>1536</p></td>
<td colspan="3"><p>2048</p></td>
<td colspan="2"><p>1536</p></td>
</tr>
<tr class="row-even">
<td><p>Green contexts: minimum SM partition size for useFlags 0</p></td>
<td><p>2</p></td>
<td colspan="4"><p>4</p></td>
<td colspan="5"><p>8</p></td>
</tr>
<tr class="row-odd">
<td><p>Green contexts: SM co-scheduled alignment per partition for useFlags 0</p></td>
<td colspan="5"><p>2</p></td>
<td colspan="5"><p>8</p></td>
</tr>
</tbody>
</table>
<section id="footnotes" class="footnotes footnotes-end-of-document" role="doc-endnotes">
<hr />
<ol>
<li id="fn1"></li>
</ol>
</section>

</div>

<span class="label"><span class="fn-bracket">\[</span><a href="#id5" role="doc-backlink">2</a><span class="fn-bracket">\]</span></span>

Non-Tensor Core throughputs. For more information on throughput see the <a href="https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#arithmetic-instructions-throughput-native-arithmetic-instructions" class="reference external">CUDA Best Practices Guide</a>

<div class="pst-scrollable-table-container">

<table id="compute-capabilities-table-memory-information-per-compute-capability" class="small table-no-stripes longtable table" style="width:100%;">
<caption><span class="caption-number">Table 31 </span><span class="caption-text">Memory Information per Compute Capability</span><a href="#compute-capabilities-table-memory-information-per-compute-capability" class="headerlink" title="Link to this table">#</a></caption>
<colgroup>
<col style="width: 44%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
</colgroup>
<thead>
<tr class="row-odd">
<th class="head"></th>
<th colspan="9" class="head"><p><strong>Compute Capability</strong></p></th>
</tr>
</thead>
<tbody>
<tr class="row-even">
<td></td>
<td><p>7.5</p></td>
<td><p>8.0</p></td>
<td><p>8.6</p></td>
<td><p>8.7</p></td>
<td><p>8.9</p></td>
<td><p>9.0</p></td>
<td><p>10.x</p></td>
<td><p>11.0</p></td>
<td><p>12.x</p></td>
</tr>
<tr class="row-odd">
<td><p>Number of 32-bit registers per SM</p></td>
<td colspan="9"><p>64 K</p></td>
</tr>
<tr class="row-even">
<td><p>Maximum number of 32-bit registers per thread block</p></td>
<td colspan="9"><p>64 K</p></td>
</tr>
<tr class="row-odd">
<td><p>Maximum number of 32-bit registers per thread</p></td>
<td colspan="9"><p>255</p></td>
</tr>
<tr class="row-even">
<td><p>Maximum amount of shared memory per SM</p></td>
<td><p>64 KB</p></td>
<td><p>164 KB</p></td>
<td><p>100 KB</p></td>
<td><p>164 KB</p></td>
<td><p>100 KB</p></td>
<td colspan="3"><p>228 KB</p></td>
<td><p>100 KB</p></td>
</tr>
<tr class="row-odd">
<td><p>Maximum amount of shared memory per thread block <a href="#fn1" class="footnote-ref" id="fnref1" role="doc-noteref"><sup>1</sup></a></p></td>
<td><p>64 KB</p></td>
<td><p>163 KB</p></td>
<td><p>99 KB</p></td>
<td><p>163 KB</p></td>
<td><p>99 KB</p></td>
<td colspan="3"><p>227 KB</p></td>
<td><p>99 KB</p></td>
</tr>
<tr class="row-even">
<td><p>Number of shared memory banks</p></td>
<td colspan="9"><p>32</p></td>
</tr>
<tr class="row-odd">
<td><p>Maximum amount of local memory per thread</p></td>
<td colspan="9"><p>512 KB</p></td>
</tr>
<tr class="row-even">
<td><p>Constant memory size</p></td>
<td colspan="9"><p>64 KB</p></td>
</tr>
<tr class="row-odd">
<td><p>Cache working set per SM for constant memory</p></td>
<td colspan="9"><p>8 KB</p></td>
</tr>
<tr class="row-even">
<td><p>Cache working set per SM for texture memory</p></td>
<td><p>32 or 64 KB</p></td>
<td><p>28 KB ~ 192 KB</p></td>
<td><p>28 KB ~ 128 KB</p></td>
<td><p>28 KB ~ 192 KB</p></td>
<td><p>28 KB ~ 128 KB</p></td>
<td colspan="3"><p>28 KB ~ 256 KB</p></td>
<td><p>28 KB ~ 128 KB</p></td>
</tr>
</tbody>
</table>
<section id="footnotes" class="footnotes footnotes-end-of-document" role="doc-endnotes">
<hr />
<ol>
<li id="fn1"></li>
</ol>
</section>

</div>

<span class="label"><span class="fn-bracket">\[</span><a href="#id6" role="doc-backlink">3</a><span class="fn-bracket">\]</span></span>

Kernels relying on shared memory allocations over 48 KB per block must use dynamic shared memory and require an explicit opt-in, see <a href="../03-advanced/advanced-kernel-programming.html#advanced-kernel-l1-shared-config" class="reference internal"><span class="std std-ref">Configuring L1/Shared Memory Balance</span></a>.

<div class="pst-scrollable-table-container">

| Compute Capability | Unified Data Cache Size (KB) | SMEM Capacity Sizes (KB) |
|----|----|----|
| 7.5 | 96 | 32, 64 |
| 8.0 | 192 | 0, 8, 16, 32, 64, 100, 132, 164 |
| 8.6 | 128 | 0, 8, 16, 32, 64, 100 |
| 8.7 | 192 | 0, 8, 16, 32, 64, 100, 132, 164 |
| 8.9 | 128 | 0, 8, 16, 32, 64, 100 |
| 9.0 | 256 | 0, 8, 16, 32, 64, 100, 132, 164, 196, 228 |
| 10.x | 256 | 0, 8, 16, 32, 64, 100, 132, 164, 196, 228 |
| 11.0 | 256 | 0, 8, 16, 32, 64, 100, 132, 164, 196, 228 |
| 12.x | 128 | 0, 8, 16, 32, 64, 100 |

<span class="caption-number">Table 32 </span><span class="caption-text">Shared Memory Capacity per Compute Capability</span><a href="#compute-capabilities-table-shared-memory-capacity-per-compute-capability" class="headerlink" title="Link to this table">#</a> {#compute-capabilities-table-shared-memory-capacity-per-compute-capability}

</div>

<a href="#compute-capabilities-table-tensor-core-data-types-per-compute-capability" class="reference internal"><span class="std std-numref">Table 33</span></a> shows the input data types supported by Tensor Core acceleration. The Tensor Core feature set is available within the CUDA compilation toolchain through inline PTX. It is strongly recommended that applications use this feature set through CUDA-X libraries such as cuDNN, cuBLAS, and cuFFT, for example, or through <a href="https://docs.nvidia.com/cutlass/index.html" class="reference external">CUTLASS</a>, a collection of CUDA C++ template abstractions and Python domain-specific languages (DSLs) designed to enable high-performance matrix-matrix multiplication (GEMM) and related computations across all levels within CUDA.

<div class="pst-scrollable-table-container">

<table id="compute-capabilities-table-tensor-core-data-types-per-compute-capability" class="small table-no-stripes table">
<caption><span class="caption-number">Table 33 </span><span class="caption-text">Input Data Types Supported by Tensor Core Acceleration per Compute Capability</span><a href="#compute-capabilities-table-tensor-core-data-types-per-compute-capability" class="headerlink" title="Link to this table">#</a></caption>
<thead>
<tr class="row-odd">
<th class="head"><p>Compute Capability</p></th>
<th colspan="9" class="head"><p>Tensor Core Input Data Types</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even">
<td></td>
<td><p>FP64</p></td>
<td><p>TF32</p></td>
<td><p>BF16</p></td>
<td><p>FP16</p></td>
<td><p>FP8</p></td>
<td><p>FP6</p></td>
<td><p>FP4</p></td>
<td><p>INT8</p></td>
<td><p>INT4</p></td>
</tr>
<tr class="row-odd">
<td><p>7.5</p></td>
<td colspan="3"></td>
<td><p>Yes</p></td>
<td colspan="3"></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
</tr>
<tr class="row-even">
<td><p>8.0</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td colspan="3"></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
</tr>
<tr class="row-odd">
<td><p>8.6</p></td>
<td></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td colspan="3"></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
</tr>
<tr class="row-even">
<td><p>8.7</p></td>
<td></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td colspan="3"></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
</tr>
<tr class="row-odd">
<td><p>8.9</p></td>
<td></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td colspan="2"></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
</tr>
<tr class="row-even">
<td><p>9.0</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td colspan="2"></td>
<td><p>Yes</p></td>
<td></td>
</tr>
<tr class="row-odd">
<td><p>10.0</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td></td>
</tr>
<tr class="row-even">
<td><p>10.3</p></td>
<td></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td></td>
</tr>
<tr class="row-odd">
<td><p>11.0</p></td>
<td></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td></td>
</tr>
<tr class="row-even">
<td><p>12.x</p></td>
<td></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td><p>Yes</p></td>
<td></td>
</tr>
</tbody>
</table>

</div>

</div>

</div>

<div class="prev-next-area">

<a href="../part5.html" class="left-prev" title="previous page"><em></em></a>

<div class="prev-next-info">

previous

<span class="section-number">5. </span>Technical Appendices

</div>

<a href="environment-variables.html" class="right-next" title="next page"></a>

<div class="prev-next-info">

next

<span class="section-number">5.2. </span>CUDA Environment Variables

</div>

</div>

</div>

<div id="pst-secondary-sidebar" class="bd-sidebar-secondary bd-toc">

<div class="sidebar-secondary-items sidebar-secondary__inner">

<div class="sidebar-secondary-item">

<div id="pst-page-navigation-heading-2" class="page-toc tocsection onthispage">

On this page

</div>

- <a href="#obtain-the-gpu-compute-capability" class="reference internal nav-link">5.1.1. Obtain the GPU Compute Capability</a>
- <a href="#feature-availability" class="reference internal nav-link">5.1.2. Feature Availability</a>
  - <a href="#architecture-specific-features" class="reference internal nav-link">5.1.2.1. Architecture-Specific Features</a>
  - <a href="#family-specific-features" class="reference internal nav-link">5.1.2.2. Family-Specific Features</a>
  - <a href="#feature-set-compiler-targets" class="reference internal nav-link">5.1.2.3. Feature Set Compiler Targets</a>
- <a href="#features-and-technical-specifications" class="reference internal nav-link">5.1.3. Features and Technical Specifications</a>

</div>

</div>

</div>

</div>

</div>
