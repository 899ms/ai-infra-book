<!-- 从 cuda-sync.html 迁移的资料快照；原始 HTML SHA-256: 0a4a9ad69b5bdf2727b33b933e8d99b5fc9b6ca4f95445309ac1b4033f1f1252。 -->

NVIDIACUDA Toolkit Documentation

Search In: Entire Site Just This Document

clear search

search

[CUDA Toolkit v13.3.0](../index.html "The root of the site.")

[CUDA Runtime API](index.html "CUDA Runtime API")

- [1. Difference between the driver and runtime APIs](driver-vs-runtime-api.html#driver-vs-runtime-api)

- [2. API synchronization behavior](api-sync-behavior.html#api-sync-behavior)

- [3. Stream synchronization behavior](stream-sync-behavior.html#stream-sync-behavior)

- [4. Graph object thread safety](graphs-thread-safety.html#graphs-thread-safety)

- [5. Rules for version mixing](version-mixing-rules.html#version-mixing-rules)

- [6. Modules](modules.html#modules)

  - [6.1. Device Management](group__CUDART__DEVICE.html#group__CUDART__DEVICE)

  - [6.2. Device Management \[DEPRECATED\]](group__CUDART__DEVICE__DEPRECATED.html#group__CUDART__DEVICE__DEPRECATED)

  - [6.3. Error Handling](group__CUDART__ERROR.html#group__CUDART__ERROR)

  - [6.4. Stream Management](group__CUDART__STREAM.html#group__CUDART__STREAM)

  - [6.5. Event Management](group__CUDART__EVENT.html#group__CUDART__EVENT)

  - [6.6. External Resource Interoperability](group__CUDART__EXTRES__INTEROP.html#group__CUDART__EXTRES__INTEROP)

  - [6.7. Execution Control](group__CUDART__EXECUTION.html#group__CUDART__EXECUTION)

  - [6.8. Execution Control \[DEPRECATED\]](group__CUDART__EXECUTION__DEPRECATED.html#group__CUDART__EXECUTION__DEPRECATED)

  - [6.9. Occupancy](group__CUDART__OCCUPANCY.html#group__CUDART__OCCUPANCY)

  - [6.10. Memory Management](group__CUDART__MEMORY.html#group__CUDART__MEMORY)

  - [6.11. Memory Management \[DEPRECATED\]](group__CUDART__MEMORY__DEPRECATED.html#group__CUDART__MEMORY__DEPRECATED)

  - [6.12. Stream Ordered Memory Allocator](group__CUDART__MEMORY__POOLS.html#group__CUDART__MEMORY__POOLS)

  - [6.13. Unified Addressing](group__CUDART__UNIFIED.html#group__CUDART__UNIFIED)

  - [6.14. Peer Device Memory Access](group__CUDART__PEER.html#group__CUDART__PEER)

  - [6.15. OpenGL Interoperability](group__CUDART__OPENGL.html#group__CUDART__OPENGL)

  - [6.16. OpenGL Interoperability \[DEPRECATED\]](group__CUDART__OPENGL__DEPRECATED.html#group__CUDART__OPENGL__DEPRECATED)

  - [6.17. Direct3D 9 Interoperability](group__CUDART__D3D9.html#group__CUDART__D3D9)

  - [6.18. Direct3D 9 Interoperability \[DEPRECATED\]](group__CUDART__D3D9__DEPRECATED.html#group__CUDART__D3D9__DEPRECATED)

  - [6.19. Direct3D 10 Interoperability](group__CUDART__D3D10.html#group__CUDART__D3D10)

  - [6.20. Direct3D 10 Interoperability \[DEPRECATED\]](group__CUDART__D3D10__DEPRECATED.html#group__CUDART__D3D10__DEPRECATED)

  - [6.21. Direct3D 11 Interoperability](group__CUDART__D3D11.html#group__CUDART__D3D11)

  - [6.22. Direct3D 11 Interoperability \[DEPRECATED\]](group__CUDART__D3D11__DEPRECATED.html#group__CUDART__D3D11__DEPRECATED)

  - [6.23. VDPAU Interoperability](group__CUDART__VDPAU.html#group__CUDART__VDPAU)

  - [6.24. EGL Interoperability](group__CUDART__EGL.html#group__CUDART__EGL)

  - [6.25. Graphics Interoperability](group__CUDART__INTEROP.html#group__CUDART__INTEROP)

  - [6.26. Texture Object Management](group__CUDART__TEXTURE__OBJECT.html#group__CUDART__TEXTURE__OBJECT)

  - [6.27. Surface Object Management](group__CUDART__SURFACE__OBJECT.html#group__CUDART__SURFACE__OBJECT)

  - [6.28. Version Management](group__CUDART____VERSION.html#group__CUDART____VERSION)

  - [6.29. Error Log Management Functions](group__CUDART__LOGS.html#group__CUDART__LOGS)

  - [6.30. Graph Management](group__CUDART__GRAPH.html#group__CUDART__GRAPH)

  - [6.31. Driver Entry Point Access](group__CUDART__DRIVER__ENTRY__POINT.html#group__CUDART__DRIVER__ENTRY__POINT)

  - [6.32. Library Management](group__CUDART__LIBRARY.html#group__CUDART__LIBRARY)

  - [6.33. Execution Context Management](group__CUDART__EXECUTION__CONTEXT.html#group__CUDART__EXECUTION__CONTEXT)

  - [6.34. C++ API Routines](group__CUDART__HIGHLEVEL.html#group__CUDART__HIGHLEVEL)

  - [6.35. Interactions with the CUDA Driver API](group__CUDART__DRIVER.html#group__CUDART__DRIVER)

  - [6.36. Logical Endpoint](group__CUDART__FABRIC.html#group__CUDART__FABRIC)

  - [6.37. Profiler Control](group__CUDART__PROFILER.html#group__CUDART__PROFILER)

  - [6.38. Data types used by CUDA Runtime](group__CUDART__TYPES.html#group__CUDART__TYPES)

- [7. Data Structures](annotated.html#annotated)

  - [7.1. \_\_cudaOccupancyB2DHelper](class____cudaOccupancyB2DHelper.html#class____cudaOccupancyB2DHelper)

  - [7.2. cudaAccessPolicyWindow](structcudaAccessPolicyWindow.html#structcudaAccessPolicyWindow)

  - [7.3. cudaArrayMemoryRequirements](structcudaArrayMemoryRequirements.html#structcudaArrayMemoryRequirements)

  - [7.4. cudaArraySparseProperties](structcudaArraySparseProperties.html#structcudaArraySparseProperties)

  - [7.5. cudaAsyncNotificationInfo_t](structcudaAsyncNotificationInfo__t.html#structcudaAsyncNotificationInfo__t)

  - [7.6. cudaChannelFormatDesc](structcudaChannelFormatDesc.html#structcudaChannelFormatDesc)

  - [7.7. cudaChildGraphNodeParams](structcudaChildGraphNodeParams.html#structcudaChildGraphNodeParams)

  - [7.8. cudaConditionalNodeParams](structcudaConditionalNodeParams.html#structcudaConditionalNodeParams)

  - [7.9. cudaDeviceProp](structcudaDeviceProp.html#structcudaDeviceProp)

  - [7.10. cudaDevResource](structcudaDevResource.html#structcudaDevResource)

  - [7.11. cudaDevSmResource](structcudaDevSmResource.html#structcudaDevSmResource)

  - [7.12. cudaDevSmResourceGroupParams](structcudaDevSmResourceGroupParams.html#structcudaDevSmResourceGroupParams)

  - [7.13. cudaDevWorkqueueConfigResource](structcudaDevWorkqueueConfigResource.html#structcudaDevWorkqueueConfigResource)

  - [7.14. cudaDevWorkqueueResource](structcudaDevWorkqueueResource.html#structcudaDevWorkqueueResource)

  - [7.15. cudaEglFrame](structcudaEglFrame.html#structcudaEglFrame)

  - [7.16. cudaEglPlaneDesc](structcudaEglPlaneDesc.html#structcudaEglPlaneDesc)

  - [7.17. cudaEventRecordNodeParams](structcudaEventRecordNodeParams.html#structcudaEventRecordNodeParams)

  - [7.18. cudaEventWaitNodeParams](structcudaEventWaitNodeParams.html#structcudaEventWaitNodeParams)

  - [7.19. cudaExtent](structcudaExtent.html#structcudaExtent)

  - [7.20. cudaExternalMemoryBufferDesc](structcudaExternalMemoryBufferDesc.html#structcudaExternalMemoryBufferDesc)

  - [7.21. cudaExternalMemoryHandleDesc](structcudaExternalMemoryHandleDesc.html#structcudaExternalMemoryHandleDesc)

  - [7.22. cudaExternalMemoryMipmappedArrayDesc](structcudaExternalMemoryMipmappedArrayDesc.html#structcudaExternalMemoryMipmappedArrayDesc)

  - [7.23. cudaExternalSemaphoreHandleDesc](structcudaExternalSemaphoreHandleDesc.html#structcudaExternalSemaphoreHandleDesc)

  - [7.24. cudaExternalSemaphoreSignalNodeParams](structcudaExternalSemaphoreSignalNodeParams.html#structcudaExternalSemaphoreSignalNodeParams)

  - [7.25. cudaExternalSemaphoreSignalNodeParamsV2](structcudaExternalSemaphoreSignalNodeParamsV2.html#structcudaExternalSemaphoreSignalNodeParamsV2)

  - [7.26. cudaExternalSemaphoreSignalParams](structcudaExternalSemaphoreSignalParams.html#structcudaExternalSemaphoreSignalParams)

  - [7.27. cudaExternalSemaphoreWaitNodeParams](structcudaExternalSemaphoreWaitNodeParams.html#structcudaExternalSemaphoreWaitNodeParams)

  - [7.28. cudaExternalSemaphoreWaitNodeParamsV2](structcudaExternalSemaphoreWaitNodeParamsV2.html#structcudaExternalSemaphoreWaitNodeParamsV2)

  - [7.29. cudaExternalSemaphoreWaitParams](structcudaExternalSemaphoreWaitParams.html#structcudaExternalSemaphoreWaitParams)

  - [7.30. cudaFuncAttributes](structcudaFuncAttributes.html#structcudaFuncAttributes)

  - [7.31. cudaGraphEdgeData](structcudaGraphEdgeData.html#structcudaGraphEdgeData)

  - [7.32. cudaGraphExecUpdateResultInfo](structcudaGraphExecUpdateResultInfo.html#structcudaGraphExecUpdateResultInfo)

  - [7.33. cudaGraphInstantiateParams](structcudaGraphInstantiateParams.html#structcudaGraphInstantiateParams)

  - [7.34. cudaGraphKernelNodeUpdate](structcudaGraphKernelNodeUpdate.html#structcudaGraphKernelNodeUpdate)

  - [7.35. cudaGraphNodeParams](structcudaGraphNodeParams.html#structcudaGraphNodeParams)

  - [7.36. cudaGraphRecaptureCallbackData](structcudaGraphRecaptureCallbackData.html#structcudaGraphRecaptureCallbackData)

  - [7.37. cudaHostNodeParams](structcudaHostNodeParams.html#structcudaHostNodeParams)

  - [7.38. cudaHostNodeParamsV2](structcudaHostNodeParamsV2.html#structcudaHostNodeParamsV2)

  - [7.39. cudaIpcEventHandle_t](structcudaIpcEventHandle__t.html#structcudaIpcEventHandle__t)

  - [7.40. cudaIpcMemHandle_t](structcudaIpcMemHandle__t.html#structcudaIpcMemHandle__t)

  - [7.41. cudaKernelNodeParams](structcudaKernelNodeParams.html#structcudaKernelNodeParams)

  - [7.42. cudaKernelNodeParamsV2](structcudaKernelNodeParamsV2.html#structcudaKernelNodeParamsV2)

  - [7.43. cudaLaunchAttribute](structcudaLaunchAttribute.html#structcudaLaunchAttribute)

  - [7.44. cudaLaunchAttributeValue](unioncudaLaunchAttributeValue.html#unioncudaLaunchAttributeValue)

  - [7.45. cudaLaunchConfig_t](structcudaLaunchConfig__t.html#structcudaLaunchConfig__t)

  - [7.46. cudaLaunchMemSyncDomainMap](structcudaLaunchMemSyncDomainMap.html#structcudaLaunchMemSyncDomainMap)

  - [7.47. cudaMemAccessDesc](structcudaMemAccessDesc.html#structcudaMemAccessDesc)

  - [7.48. cudaMemAllocNodeParams](structcudaMemAllocNodeParams.html#structcudaMemAllocNodeParams)

  - [7.49. cudaMemAllocNodeParamsV2](structcudaMemAllocNodeParamsV2.html#structcudaMemAllocNodeParamsV2)

  - [7.50. cudaMemcpy3DOperand](structcudaMemcpy3DOperand.html#structcudaMemcpy3DOperand)

  - [7.51. cudaMemcpy3DParms](structcudaMemcpy3DParms.html#structcudaMemcpy3DParms)

  - [7.52. cudaMemcpy3DPeerParms](structcudaMemcpy3DPeerParms.html#structcudaMemcpy3DPeerParms)

  - [7.53. cudaMemcpyAttributes](structcudaMemcpyAttributes.html#structcudaMemcpyAttributes)

  - [7.54. cudaMemcpyNodeParams](structcudaMemcpyNodeParams.html#structcudaMemcpyNodeParams)

  - [7.55. cudaMemFreeNodeParams](structcudaMemFreeNodeParams.html#structcudaMemFreeNodeParams)

  - [7.56. cudaMemLocation](structcudaMemLocation.html#structcudaMemLocation)

  - [7.57. cudaMemPoolProps](structcudaMemPoolProps.html#structcudaMemPoolProps)

  - [7.58. cudaMemPoolPtrExportData](structcudaMemPoolPtrExportData.html#structcudaMemPoolPtrExportData)

  - [7.59. cudaMemsetParams](structcudaMemsetParams.html#structcudaMemsetParams)

  - [7.60. cudaMemsetParamsV2](structcudaMemsetParamsV2.html#structcudaMemsetParamsV2)

  - [7.61. cudaOffset3D](structcudaOffset3D.html#structcudaOffset3D)

  - [7.62. cudaPitchedPtr](structcudaPitchedPtr.html#structcudaPitchedPtr)

  - [7.63. cudaPointerAttributes](structcudaPointerAttributes.html#structcudaPointerAttributes)

  - [7.64. cudaPos](structcudaPos.html#structcudaPos)

  - [7.65. cudaResourceDesc](structcudaResourceDesc.html#structcudaResourceDesc)

  - [7.66. cudaResourceViewDesc](structcudaResourceViewDesc.html#structcudaResourceViewDesc)

  - [7.67. cudaTextureDesc](structcudaTextureDesc.html#structcudaTextureDesc)

  - [7.68. CUuuid_st](structCUuuid__st.html#structCUuuid__st)

- [8. Data Fields](functions.html#functions)

- [9. Deprecated List](deprecated.html#deprecated)

## Search Results

[\< Previous](driver-vs-runtime-api.html) \| [Next \>](stream-sync-behavior.html)

CUDA Runtime API ([PDF](../pdf/CUDA_Runtime_API.pdf)) - v13.3.0 ([older](https://developer.nvidia.com/cuda-toolkit-archive)) - Last updated May 26, 2026 - [Send Feedback](mailto:CUDAIssues@nvidia.com?subject=CUDA%20Toolkit%20Documentation%20Feedback:%20CUDA%20Runtime%20API)

## 2. API synchronization behavior

The API provides memcpy/memset functions in both synchronous and asynchronous forms, the latter having an "Async" suffix. This is a misnomer as each function may exhibit synchronous or asynchronous behavior depending on the arguments passed to the function. The synchronous forms of these APIs issue these copies through the default stream.

Any CUDA API call may block or synchronize for various reasons such as contention for or unavailability of internal resources. Such behavior is subject to change and undocumented behavior should not be relied upon.

## Memcpy

In the reference documentation, each memcpy function is categorized as synchronous or asynchronous, corresponding to the definitions below.

**Synchronous**

1.  For transfers from pageable host memory to device memory, a stream sync is performed before the copy is initiated. The function will return once the pageable buffer has been copied to the staging memory for DMA transfer to device memory, but the DMA to final destination may not have completed.

2.  For transfers from pinned host memory to device memory, the function is synchronous with respect to the host.

3.  For transfers from device to either pageable or pinned host memory, the function returns only once the copy has completed.

4.  For transfers from device memory to device memory, no host-side synchronization is performed.

5.  For transfers from any host memory to any host memory, the function is fully synchronous with respect to the host.

**Asynchronous**

1.  For transfers between device memory and pageable host memory, the function might be synchronous with respect to host.

2.  For transfers from any host memory to any host memory, the function is fully synchronous with respect to the host.

3.  If pageable memory must first be staged to pinned memory, the driver may synchronize with the stream and stage the copy into pinned memory.

4.  For all other transfers, the function should be fully asynchronous.

## Memset

The cudaMemset functions are asynchronous with respect to the host except when the target memory is pinned host memory. The Async versions are always asynchronous with respect to the host.

## Kernel Launches

Kernel launches are asynchronous with respect to the host. Details of concurrent kernel execution and data transfers can be found in the CUDA Programmers Guide.

------------------------------------------------------------------------

![](../common/formatting/NVIDIA-LogoBlack.svg)

[Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) \| [Manage My Privacy](https://www.nvidia.com/en-us/privacy-center/) \| [Do Not Sell or Share My Data](https://www.nvidia.com/en-us/preferences/email-preferences/) \| [Terms of Service](https://www.nvidia.com/en-us/about-nvidia/terms-of-service/) \| [Accessibility](https://www.nvidia.com/en-us/about-nvidia/accessibility/) \| [Corporate Policies](https://www.nvidia.com/en-us/about-nvidia/company-policies/) \| [Product Security](https://www.nvidia.com/en-us/product-security/) \| [Contact](https://www.nvidia.com/en-us/contact/)

Copyright © 2026 NVIDIA Corporation
