<!-- 从 vllm-v1.html 迁移的资料快照；原始 HTML SHA-256: 24d3a165c77534ceb416d185b4762778d96eeb1dd26bc12b53577fc57820ba7c。 -->

[![logo](../../assets/logos/vllm-logo-only-light.ico)](../.. "vLLM") vLLM

[](https://github.com/vllm-project/vllm "Go to repository")

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCA0NDggNTEyIj48IS0tIEZvbnQgQXdlc29tZSBGcmVlIDcuMS4wIGJ5IEBmb250YXdlc29tZSAtIGh0dHBzOi8vZm9udGF3ZXNvbWUuY29tIExpY2Vuc2UgLSBodHRwczovL2ZvbnRhd2Vzb21lLmNvbS9saWNlbnNlL2ZyZWUgKEljb25zOiBDQyBCWSA0LjAsIEZvbnRzOiBTSUwgT0ZMIDEuMSwgQ29kZTogTUlUIExpY2Vuc2UpIENvcHlyaWdodCAyMDI1IEZvbnRpY29ucywgSW5jLi0tPjxwYXRoIGQ9Ik00MzkuNiAyMzYuMSAyNDQgNDAuNWMtNS40LTUuNS0xMi44LTguNS0yMC40LTguNXMtMTUgMy0yMC40IDguNEwxNjIuNSA4MWw1MS41IDUxLjVjMjcuMS05LjEgNTIuNyAxNi44IDQzLjQgNDMuN2w0OS43IDQ5LjdjMzQuMi0xMS44IDYxLjIgMzEgMzUuNSA1Ni43LTI2LjUgMjYuNS03MC4yLTIuOS01Ni0zNy4zTDI0MC4zIDE5OXYxMjEuOWMyNS4zIDEyLjUgMjIuMyA0MS44IDkuMSA1NS02LjQgNi40LTE1LjIgMTAuMS0yNC4zIDEwLjFzLTE3LjgtMy42LTI0LjMtMTAuMWMtMTcuNi0xNy42LTExLjEtNDYuOSAxMS4yLTU2di0xMjNjLTIwLjgtOC41LTI0LjYtMzAuNy0xOC42LTQ1TDE0Mi42IDEwMSA4LjUgMjM1LjFDMyAyNDAuNiAwIDI0Ny45IDAgMjU1LjVzMyAxNSA4LjUgMjAuNGwxOTUuNiAxOTUuN2M1LjQgNS40IDEyLjcgOC40IDIwLjQgOC40czE1LTMgMjAuNC04LjRsMTk0LjctMTk0LjdjNS40LTUuNCA4LjQtMTIuOCA4LjQtMjAuNHMtMy0xNS04LjQtMjAuNCIgLz48L3N2Zz4=)

GitHub

[ Home ](../..)

[ User Guide ](../)

User Guide

Getting Started

Getting Started

[ Quickstart ](../../getting_started/quickstart/)

[ Installation ](../../getting_started/installation/)

Installation

- [ GPU ](../../getting_started/installation/gpu/)
- [ CPU ](../../getting_started/installation/cpu/)
- [ TPU ](https://docs.vllm.ai/projects/tpu/en/latest/getting_started/installation/)

[ Examples ](../../examples/)

Examples

Applications

Applications

- [ API Server ](../../examples/applications/api_server/)
- [ Chatbot ](../../examples/applications/chatbot/)
- [ Rag ](../../examples/applications/rag/)

Basic

Basic

- [ Offline Inference ](../../examples/basic/offline_inference/)
- [ Online Serving ](../../examples/basic/online_serving/)

Deployment

Deployment

- [ Async LLM Streaming ](../../examples/deployment/async_llm_streaming/)
- [ Helm Charts ](../../examples/deployment/chart-helm/)
- [ LLM Engine Example ](../../examples/deployment/llm_engine_example/)
- [ Sagemaker-Entrypoint ](../../examples/deployment/sagemaker-entrypoint/)

Disaggregated

Disaggregated

- [ Disaggregated Encoder ](../../examples/disaggregated/disaggregated_encoder/)
- [ Disaggregated Serving ](../../examples/disaggregated/disaggregated_serving/)
- [ Ec Both Encoder ](../../examples/disaggregated/ec_both_encoder/)
- [ Disaggregated Prefill V1 ](../../examples/disaggregated/example_connector/)
- [ Flexkv Connector ](../../examples/disaggregated/flexkv_connector/)
- [ KV Load Failure Recovery Test ](../../examples/disaggregated/kv_load_failure_recovery_offline/)
- [ LMCache Examples ](../../examples/disaggregated/lmcache/)
- [ Mooncake Connector ](../../examples/disaggregated/mooncake_connector/)

Features

Features

- [ Automatic Prefix Caching ](../../examples/features/automatic_prefix_caching/)
- [ Batch Invariance ](../../examples/features/batch_invariance/)
- [ Context Extension ](../../examples/features/context_extension/)
- [ Data Parallel ](../../examples/features/data_parallel/)
- [ Kv Events ](../../examples/features/kv_events/)
- [ Logging Configuration ](../../examples/features/logging_configuration/)
- [ Custom Logits Processors ](../../examples/features/logits_processor/)
- [ LoRA ](../../examples/features/lora/)
- [ Offline Inference with the OpenAI Batch file format ](../../examples/features/openai_batch/)
- [ Pause Resume ](../../examples/features/pause_resume/)
- [ Profiling ](../../examples/features/profiling/)
- [ Prompt Embed ](../../examples/features/prompt_embed/)
- [ Reset Kv ](../../examples/features/reset_kv/)
- [ Sharded State ](../../examples/features/sharded_state/)
- [ Speculative Decoding ](../../examples/features/speculative_decoding/)
- [ Structured Outputs ](../../examples/features/structured_outputs/)
- [ Tensorize vLLM Model ](../../examples/features/tensorize_vllm_model/)
- [ Torchrun ](../../examples/features/torchrun/)

Generate

Generate

- [ Batched Chat Completions Online ](../../examples/generate/batched_chat_completions_online/)
- [ Multimodal ](../../examples/generate/multimodal/)
- [ Qwen 1M Offline ](../../examples/generate/qwen_1m_offline/)

Observability

Observability

- [ Monitoring Dashboards ](../../examples/observability/dashboards/)
- [ Metrics ](../../examples/observability/metrics/)
- [ Setup OpenTelemetry POC ](../../examples/observability/opentelemetry/)
- [ Prometheus and Grafana ](../../examples/observability/prometheus_grafana/)

Pooling

Pooling

- [ Classify ](../../examples/pooling/classify/)
- [ Embed ](../../examples/pooling/embed/)
- [ Plugin ](../../examples/pooling/plugin/)
- [ Reward ](../../examples/pooling/reward/)
- [ Score ](../../examples/pooling/score/)
- [ Token Classify ](../../examples/pooling/token_classify/)
- [ Token Embed ](../../examples/pooling/token_embed/)

Ray Serving

Ray Serving

- [ Batch LLM Inference ](../../examples/ray_serving/batch_llm_inference/)
- [ Elastic Ep ](../../examples/ray_serving/elastic_ep/)
- [ Multi-Node-Serving ](../../examples/ray_serving/multi-node-serving/)
- [ Ray Serve Deepseek ](../../examples/ray_serving/ray_serve_deepseek/)
- [ Run Cluster ](../../examples/ray_serving/run_cluster/)

Reasoning

Reasoning

- [ OpenAI Chat Completion Tool Calls With Reasoning ](../../examples/reasoning/openai_chat_completion_tool_calls_with_reasoning/)
- [ OpenAI Chat Completion With Reasoning ](../../examples/reasoning/openai_chat_completion_with_reasoning/)
- [ OpenAI Chat Completion With Reasoning Streaming ](../../examples/reasoning/openai_chat_completion_with_reasoning_streaming/)
- [ OpenAI Responses Client ](../../examples/reasoning/openai_responses_client/)

RL

RL

- [ RLHF Async New APIs ](../../examples/rl/rlhf_async_new_apis/)
- [ RLHF Http IPC ](../../examples/rl/rlhf_http_ipc/)
- [ RLHF Http NCCL ](../../examples/rl/rlhf_http_nccl/)
- [ RLHF IPC Fsdp Ep ](../../examples/rl/rlhf_ipc_fsdp_ep/)
- [ RLHF NCCL Fsdp Ep ](../../examples/rl/rlhf_nccl_fsdp_ep/)
- [ RLHF Sparse NCCL ](../../examples/rl/rlhf_sparse_nccl/)
- [ Routed Experts E2E ](../../examples/rl/routed_experts_e2e/)
- [ Skip Loading Weights In Engine Init ](../../examples/rl/skip_loading_weights_in_engine_init/)

Scale Out

Scale Out

- [ Init ](../../examples/scale_out/__init__/)
- [ Example Mm Serve ](../../examples/scale_out/example_mm_serve/)
- [ Token Generation Client ](../../examples/scale_out/token_generation_client/)

Speech To Text

Speech To Text

- [ Lid ](../../examples/speech_to_text/lid/)
- [ OpenAI ](../../examples/speech_to_text/openai/)
- [ Realtime ](../../examples/speech_to_text/realtime/)

Tool Calling

Tool Calling

- [ Chat With Tools Offline ](../../examples/tool_calling/chat_with_tools_offline/)
- [ OpenAI Chat Completion Client With Tools ](../../examples/tool_calling/openai_chat_completion_client_with_tools/)
- [ OpenAI Chat Completion Client With Tools Required ](../../examples/tool_calling/openai_chat_completion_client_with_tools_required/)
- [ OpenAI Chat Completion Client With Tools Xlam ](../../examples/tool_calling/openai_chat_completion_client_with_tools_xlam/)
- [ OpenAI Chat Completion Client With Tools Xlam Streaming ](../../examples/tool_calling/openai_chat_completion_client_with_tools_xlam_streaming/)
- [ OpenAI Responses Client With Mcp Tools ](../../examples/tool_calling/openai_responses_client_with_mcp_tools/)
- [ OpenAI Responses Client With Tools ](../../examples/tool_calling/openai_responses_client_with_tools/)

General

General

vLLM V1 [ vLLM V1 ](./)

Table of contents

- [ Differences from V0 ](#differences-from-v0)
  - [ Chunked Prefill ](#chunked-prefill)
  - [ CUDA Graphs ](#cuda-graphs)
  - [ Semantic Changes to Logprobs ](#semantic-changes-to-logprobs)
    - [ Logprobs Calculation ](#logprobs-calculation)
    - [ Prompt Logprobs with Prefix Caching ](#prompt-logprobs-with-prefix-caching)
- [ Feature Support ](#feature-support)
  - [ Hardware ](#hardware)
  - [ Models ](#models)
    - [ Pooling Models ](#pooling-models)
    - [ Mamba Models ](#mamba-models)
    - [ Encoder-Decoder Models ](#encoder-decoder-models)
  - [ Features ](#features)
    - [ Removed Features ](#removed-features)
      - [ Sampling features ](#sampling-features)
      - [ KV Cache features ](#kv-cache-features)
      - [ Structured Output features ](#structured-output-features)

[ Frequently Asked Questions ](../faq/)

[ Production Metrics ](../metrics/)

[ Reproducibility ](../reproducibility/)

[ Security ](../security/)

[ Troubleshooting ](../troubleshooting/)

[ Usage Stats Collection ](../usage_stats/)

Inference and Serving

Inference and Serving

[ Offline Inference ](../../serving/offline_inference/)

[ Online Serving ](../../serving/online_serving/)

Online Serving

- [ Derenderer APIs ](../../serving/online_serving/derenderer/)
- [ Generative Scoring ](../../serving/online_serving/generative_scoring/)
- [ OpenAI-Compatible Server ](../../serving/online_serving/openai_compatible_server/)
- [ Renderer APIs ](../../serving/online_serving/renderer/)
- [ Speech to Text APIs ](../../serving/online_serving/speech_to_text/)

[ Context Parallel Deployment ](../../serving/context_parallel_deployment/)

[ Data Parallel Deployment ](../../serving/data_parallel_deployment/)

[ Troubleshooting distributed deployments ](../../serving/distributed_troubleshooting/)

[ Expert Parallel Deployment ](../../serving/expert_parallel_deployment/)

[ Parallelism and Scaling ](../../serving/parallelism_scaling/)

Integrations

Integrations

- [ Claude Code ](../../serving/integrations/claude_code/)
- [ Codex ](../../serving/integrations/codex/)
- [ LangChain ](../../serving/integrations/langchain/)
- [ LlamaIndex ](../../serving/integrations/llamaindex/)

Deployment

Deployment

[ Using Docker ](../../deployment/docker/)

[ Using Kubernetes ](../../deployment/k8s/)

[ Using Nginx ](../../deployment/nginx/)

Frameworks

Frameworks

- [ Anyscale ](../../deployment/frameworks/anyscale/)
- [ AnythingLLM ](../../deployment/frameworks/anything-llm/)
- [ AutoGen ](../../deployment/frameworks/autogen/)
- [ BentoML ](../../deployment/frameworks/bentoml/)
- [ Cerebrium ](../../deployment/frameworks/cerebrium/)
- [ Chatbox ](../../deployment/frameworks/chatbox/)
- [ Crusoe ](../../deployment/frameworks/crusoe/)
- [ Dify ](../../deployment/frameworks/dify/)
- [ dstack ](../../deployment/frameworks/dstack/)
- [ Haystack ](../../deployment/frameworks/haystack/)
- [ Helm ](../../deployment/frameworks/helm/)
- [ Hugging Face Inference Endpoints ](../../deployment/frameworks/hf_inference_endpoints/)
- [ LiteLLM ](../../deployment/frameworks/litellm/)
- [ Lobe Chat ](../../deployment/frameworks/lobe-chat/)
- [ LWS ](../../deployment/frameworks/lws/)
- [ Modal ](../../deployment/frameworks/modal/)
- [ Open WebUI ](../../deployment/frameworks/open-webui/)
- [ Retrieval-Augmented Generation ](../../deployment/frameworks/retrieval_augmented_generation/)
- [ RunPod ](../../deployment/frameworks/runpod/)
- [ SkyPilot ](../../deployment/frameworks/skypilot/)
- [ Streamlit ](../../deployment/frameworks/streamlit/)
- [ NVIDIA Triton ](../../deployment/frameworks/triton/)

Integrations

Integrations

- [ AIBrix ](../../deployment/integrations/aibrix/)
- [ NVIDIA Dynamo ](../../deployment/integrations/dynamo/)
- [ KAITO ](../../deployment/integrations/kaito/)
- [ KServe ](../../deployment/integrations/kserve/)
- [ Kthena ](../../deployment/integrations/kthena/)
- [ KubeAI ](../../deployment/integrations/kubeai/)
- [ KubeRay ](../../deployment/integrations/kuberay/)
- [ Llama Stack ](../../deployment/integrations/llamastack/)
- [ llm-d ](../../deployment/integrations/llm-d/)
- [ llmaz ](../../deployment/integrations/llmaz/)
- [ Production stack ](../../deployment/integrations/production-stack/)

Training

Training

[ Async Reinforcement Learning ](../../training/async_rl/)

[ What is Layerwise (Re)loading? ](../../training/layerwise/)

[ Reinforcement Learning from Human Feedback ](../../training/rlhf/)

[ Sampling Mask (Distribution Replay) ](../../training/sampling_mask/)

[ Transformers Reinforcement Learning ](../../training/trl/)

[ Weight Transfer ](../../training/weight_transfer/)

Weight Transfer

- [ Base Classes and Custom Engines ](../../training/weight_transfer/base/)
- [ IPC Engine ](../../training/weight_transfer/ipc/)
- [ NCCL Engine ](../../training/weight_transfer/nccl/)

[ Configuration ](../../configuration/)

Configuration

- [ Conserving Memory ](../../configuration/conserving_memory/)
- [ Engine Arguments ](../../configuration/engine_args/)
- [ Environment Variables ](../../configuration/env_vars/)
- [ Model Resolution ](../../configuration/model_resolution/)
- [ Optimization and Tuning ](../../configuration/optimization/)
- [ Server Arguments ](../../configuration/serve_args/)
- [ TPU ](https://docs.vllm.ai/projects/tpu/en/latest/)

Models

Models

[ Supported Models ](../../models/supported_models/)

[ Generative Models ](../../models/generative_models/)

[ Pooling Models ](../../models/pooling_models/)

Pooling Models

- [ Classification Usages ](../../models/pooling_models/classify/)
- [ Embedding Usages ](../../models/pooling_models/embed/)
- [ Reward Usages ](../../models/pooling_models/reward/)
- [ Scoring Usages ](../../models/pooling_models/scoring/)
- [ Specific Model Examples ](../../models/pooling_models/specific_models/)
- [ Token Classification Usages ](../../models/pooling_models/token_classify/)
- [ Token Embedding Usages ](../../models/pooling_models/token_embed/)

Extensions

Extensions

- [ Loading model weights with fastsafetensors ](../../models/extensions/fastsafetensor/)
- [ Loading Model Weights with InstantTensor ](../../models/extensions/instanttensor/)
- [ Loading models with Run:ai Model Streamer ](../../models/extensions/runai_model_streamer/)
- [ Loading models with CoreWeave's Tensorizer ](../../models/extensions/tensorizer/)

Hardware Supported Models

Hardware Supported Models

- [ CPU - Intel® Xeon® ](../../models/hardware_supported_models/cpu/)
- [ XPU - Intel® GPUs ](../../models/hardware_supported_models/xpu/)
- [ TPU ](https://docs.vllm.ai/projects/tpu/en/latest/recommended_models_features/)

[ Features ](../../features/)

Features

[ Automatic Prefix Caching ](../../features/automatic_prefix_caching/)

[ Batch Invariance ](../../features/batch_invariance/)

[ Context Extension ](../../features/context_extension/)

[ Custom Arguments ](../../features/custom_arguments/)

[ Custom Logits Processors ](../../features/custom_logitsprocs/)

[ Disaggregated Encoder ](../../features/disagg_encoder/)

[ Disaggregated Prefilling (experimental) ](../../features/disagg_prefill/)

[ IndexCache ](../../features/index_cache/)

[ Interleaved Thinking ](../../features/interleaved_thinking/)

[ KV Offloading Usage Guide ](../../features/kv_offloading_usage/)

[ LoRA Adapters ](../../features/lora/)

[ MooncakeConnector Usage Guide ](../../features/mooncake_connector_usage/)

[ MooncakeStoreConnector Usage Guide ](../../features/mooncake_store_connector_usage/)

[ MoRIIOConnector Usage Guide ](../../features/moriio_connector_usage/)

[ Multimodal Inputs ](../../features/multimodal_inputs/)

[ NixlConnector Compatibility Matrix ](../../features/nixl_connector_compatibility/)

[ NixlConnector Usage Guide ](../../features/nixl_connector_usage/)

[ Per-Request Metrics ](../../features/per_request_metrics/)

[ Prompt Embedding Inputs ](../../features/prompt_embeds/)

[ Reasoning Outputs ](../../features/reasoning_outputs/)

[ Sleep Mode ](../../features/sleep_mode/)

[ Structured Outputs ](../../features/structured_outputs/)

[ Tool Calling ](../../features/tool_calling/)

[ Quantization ](../../features/quantization/)

Quantization

[ AutoAWQ ](../../features/quantization/auto_awq/)

[ B12X Linear Backend ](../../features/quantization/b12x/)

[ BitsAndBytes ](../../features/quantization/bnb/)

[ FP8 ViT Encoder Attention ](../../features/quantization/fp8_vit_attn/)

[ GGUF ](../../features/quantization/gguf/)

[ GPTQModel ](../../features/quantization/gptqmodel/)

[ Intel Quantization Support ](../../features/quantization/inc/)

[ NVIDIA Model Optimizer ](../../features/quantization/modelopt/)

[ Online Quantization ](../../features/quantization/online/)

[ Quantized KV Cache ](../../features/quantization/quantized_kvcache/)

[ AMD Quark ](../../features/quantization/quark/)

[ TorchAO ](../../features/quantization/torchao/)

[ LLM Compressor ](../../features/quantization/llm_compressor/)

LLM Compressor

- [ FP8 W8A8 ](../../features/quantization/llm_compressor/fp8/)
- [ INT4 W4A16 ](../../features/quantization/llm_compressor/int4/)
- [ INT8 W4A8 ](../../features/quantization/llm_compressor/int8_w4a8/)
- [ INT8 W8A8 ](../../features/quantization/llm_compressor/int8_w8a8/)

[ Speculative Decoding ](../../features/speculative_decoding/)

Speculative Decoding

- [ Adaptive Verification ](../../features/speculative_decoding/adaptive_verification/)
- [ Draft Models ](../../features/speculative_decoding/draft_model/)
- [ Dynamic Speculative Decoding ](../../features/speculative_decoding/dynamic_speculative_decoding/)
- [ EAGLE Draft Models ](../../features/speculative_decoding/eagle/)
- [ Hidden State Extraction ](../../features/speculative_decoding/extract_hidden_states/)
- [ MLP Draft Models ](../../features/speculative_decoding/mlp/)
- [ MTP (Multi-Token Prediction) ](../../features/speculative_decoding/mtp/)
- [ N-Gram Speculation ](../../features/speculative_decoding/n_gram/)
- [ Parallel Draft Models ](../../features/speculative_decoding/parallel_draft_model/)
- [ vLLM-Project/Speculators ](../../features/speculative_decoding/speculators/)
- [ Suffix Decoding ](../../features/speculative_decoding/suffix/)

[ Developer Guide ](../../contributing/)

Developer Guide

General

General

- [ Deprecation Policy ](../../contributing/deprecation_policy/)
- [ Dockerfile ](../../contributing/dockerfile/dockerfile/)
- [ Editing Agent Instructions ](../../contributing/editing-agent-instructions/)
- [ Incremental Compilation Workflow ](../../contributing/incremental_build/)
- [ Profiling vLLM ](../../contributing/profiling/)
- [ Vulnerability Management ](../../contributing/vulnerability_management/)

[ Model Implementation ](../../contributing/model/)

Model Implementation

- [ Basic Model ](../../contributing/model/basic/)
- [ Registering a Model ](../../contributing/model/registration/)
- [ Unit Testing ](../../contributing/model/tests/)
- [ Multi-Modal Support ](../../contributing/model/multimodal/)
- [ Speech-to-Text (Transcription/Translation) Support ](../../contributing/model/transcription/)

CI

CI

- [ CI Failures ](../../contributing/ci/failures/)
- [ Nightly Builds of vLLM Wheels ](../../contributing/ci/nightly_builds/)
- [ Update PyTorch version on vLLM OSS CI/CD ](../../contributing/ci/update_pytorch_version/)

Design Documents

Design Documents

Plugins

Plugins

- [ Endpoint Plugins ](../../design/endpoint_plugins/)
- [ IO Processor Plugins ](../../design/io_processor_plugins/)
- [ LoRA Resolver Plugins ](../../design/lora_resolver_plugins/)
- [ Plugin System ](../../design/plugin_system/)

[ Architecture Overview ](../../design/arch_overview/)

[ Attention Backend Feature Support ](../../design/attention_backends/)

[ CUDA Graphs ](../../design/cuda_graphs/)

[ Vision Encoder (ViT) CUDA Graphs ](../../design/cuda_graphs_multimodal/)

[ CustomOp ](../../design/custom_op/)

[ Dual Batch Overlap ](../../design/dbo/)

[ How to debug the vLLM-torch.compile integration ](../../design/debug_vllm_compile/)

[ Fused MoE Modular Kernel ](../../design/fused_moe_modular_kernel/)

[ Fusion torch.compile passes ](../../design/fusions/)

[ Integration with Hugging Face ](../../design/huggingface_integration/)

[ Hybrid KV Cache Manager ](../../design/hybrid_kv_cache_manager/)

[ Logits Processors ](../../design/logits_processors/)

[ Metrics ](../../design/metrics/)

[ Multi-Modal Data Processing ](../../design/mm_processing/)

[ Model Runner V2 Design Document ](../../design/model_runner_v2/)

[ Fused MoE Kernel Features ](../../design/moe_kernel_features/)

[ Python Multiprocessing ](../../design/multiprocessing/)

[ NIXL KV Cache Lease Renewal ](../../design/nixl_kv_cache_lease/)

[ NIXL push-mode KV transfer ](../../design/nixl_kv_push_connector/)

[ Optimization Levels ](../../design/optimization_levels/)

[ Paged Attention ](../../design/paged_attention/)

[ Automatic Prefix Caching ](../../design/prefix_caching/)

[ torch.compile integration ](../../design/torch_compile/)

[ torch.compile with Multimodal Encoders ](../../design/torch_compile_multimodal/)

[ vLLM IR: Functional Intermediate Representation ](../../design/vllm_ir/)

[ Benchmarking ](../../benchmarking/)

Benchmarking

- [ Benchmark CLI ](../../benchmarking/cli/)
- [ Parameter Sweeps ](../../benchmarking/sweeps/)
- [ Performance Dashboard ](../../benchmarking/dashboard/)

[ API Reference ](../../api/)

API Reference

[ vllm ](../../api/vllm/)

vllm

[ collect_env ](../../api/vllm/collect_env/)

[ connections ](../../api/vllm/connections/)

[ env_override ](../../api/vllm/env_override/)

[ envs ](../../api/vllm/envs/)

[ exceptions ](../../api/vllm/exceptions/)

[ forward_context ](../../api/vllm/forward_context/)

[ logger ](../../api/vllm/logger/)

[ logits_process ](../../api/vllm/logits_process/)

[ logprobs ](../../api/vllm/logprobs/)

[ model_inspection ](../../api/vllm/model_inspection/)

[ outputs ](../../api/vllm/outputs/)

[ pooling_params ](../../api/vllm/pooling_params/)

[ sampling_params ](../../api/vllm/sampling_params/)

[ scalar_type ](../../api/vllm/scalar_type/)

[ scripts ](../../api/vllm/scripts/)

[ sequence ](../../api/vllm/sequence/)

[ tasks ](../../api/vllm/tasks/)

[ version ](../../api/vllm/version/)

[ assets ](../../api/vllm/assets/)

assets

- [ audio ](../../api/vllm/assets/audio/)
- [ base ](../../api/vllm/assets/base/)
- [ image ](../../api/vllm/assets/image/)
- [ video ](../../api/vllm/assets/video/)

[ benchmarks ](../../api/vllm/benchmarks/)

benchmarks

[ latency ](../../api/vllm/benchmarks/latency/)

[ mm_processor ](../../api/vllm/benchmarks/mm_processor/)

[ plot ](../../api/vllm/benchmarks/plot/)

[ serve ](../../api/vllm/benchmarks/serve/)

[ startup ](../../api/vllm/benchmarks/startup/)

[ throughput ](../../api/vllm/benchmarks/throughput/)

[ datasets ](../../api/vllm/benchmarks/datasets/)

datasets

- [ create_txt_slices_dataset ](../../api/vllm/benchmarks/datasets/create_txt_slices_dataset/)
- [ datasets ](../../api/vllm/benchmarks/datasets/datasets/)
- [ utils ](../../api/vllm/benchmarks/datasets/utils/)

[ lib ](../../api/vllm/benchmarks/lib/)

lib

- [ endpoint_request_func ](../../api/vllm/benchmarks/lib/endpoint_request_func/)
- [ ready_checker ](../../api/vllm/benchmarks/lib/ready_checker/)
- [ utils ](../../api/vllm/benchmarks/lib/utils/)

[ sweep ](../../api/vllm/benchmarks/sweep/)

sweep

- [ cli ](../../api/vllm/benchmarks/sweep/cli/)
- [ param_sweep ](../../api/vllm/benchmarks/sweep/param_sweep/)
- [ plot ](../../api/vllm/benchmarks/sweep/plot/)
- [ plot_pareto ](../../api/vllm/benchmarks/sweep/plot_pareto/)
- [ serve ](../../api/vllm/benchmarks/sweep/serve/)
- [ serve_workload ](../../api/vllm/benchmarks/sweep/serve_workload/)
- [ server ](../../api/vllm/benchmarks/sweep/server/)
- [ startup ](../../api/vllm/benchmarks/sweep/startup/)
- [ utils ](../../api/vllm/benchmarks/sweep/utils/)

[ compilation ](../../api/vllm/compilation/)

compilation

[ backends ](../../api/vllm/compilation/backends/)

[ base_static_graph ](../../api/vllm/compilation/base_static_graph/)

[ breakable_cudagraph ](../../api/vllm/compilation/breakable_cudagraph/)

[ caching ](../../api/vllm/compilation/caching/)

[ codegen ](../../api/vllm/compilation/codegen/)

[ compiler_interface ](../../api/vllm/compilation/compiler_interface/)

[ counter ](../../api/vllm/compilation/counter/)

[ cuda_graph ](../../api/vllm/compilation/cuda_graph/)

[ decorators ](../../api/vllm/compilation/decorators/)

[ monitor ](../../api/vllm/compilation/monitor/)

[ partition_rules ](../../api/vllm/compilation/partition_rules/)

[ piecewise_backend ](../../api/vllm/compilation/piecewise_backend/)

[ wrapper ](../../api/vllm/compilation/wrapper/)

[ passes ](../../api/vllm/compilation/passes/)

passes

[ fx_utils ](../../api/vllm/compilation/passes/fx_utils/)

[ inductor_pass ](../../api/vllm/compilation/passes/inductor_pass/)

[ pass_manager ](../../api/vllm/compilation/passes/pass_manager/)

[ vllm_inductor_pass ](../../api/vllm/compilation/passes/vllm_inductor_pass/)

[ fusion ](../../api/vllm/compilation/passes/fusion/)

fusion

- [ act_quant_fusion ](../../api/vllm/compilation/passes/fusion/act_quant_fusion/)
- [ add_rms_fusion ](../../api/vllm/compilation/passes/fusion/add_rms_fusion/)
- [ allreduce_rms_fusion ](../../api/vllm/compilation/passes/fusion/allreduce_rms_fusion/)
- [ attn_quant_fusion ](../../api/vllm/compilation/passes/fusion/attn_quant_fusion/)
- [ collective_fusion ](../../api/vllm/compilation/passes/fusion/collective_fusion/)
- [ matcher_utils ](../../api/vllm/compilation/passes/fusion/matcher_utils/)
- [ mla_attn_quant_fusion ](../../api/vllm/compilation/passes/fusion/mla_attn_quant_fusion/)
- [ mla_rope_kvcache_cat_fusion ](../../api/vllm/compilation/passes/fusion/mla_rope_kvcache_cat_fusion/)
- [ qk_norm_rope_fusion ](../../api/vllm/compilation/passes/fusion/qk_norm_rope_fusion/)
- [ qk_norm_rope_kvcache_fusion ](../../api/vllm/compilation/passes/fusion/qk_norm_rope_kvcache_fusion/)
- [ rms_quant_fusion ](../../api/vllm/compilation/passes/fusion/rms_quant_fusion/)
- [ rocm_aiter_fusion ](../../api/vllm/compilation/passes/fusion/rocm_aiter_fusion/)
- [ rope_kvcache_fusion ](../../api/vllm/compilation/passes/fusion/rope_kvcache_fusion/)
- [ sequence_parallelism ](../../api/vllm/compilation/passes/fusion/sequence_parallelism/)

[ ir ](../../api/vllm/compilation/passes/ir/)

ir

- [ clone_elimination ](../../api/vllm/compilation/passes/ir/clone_elimination/)
- [ inplace_functionalization ](../../api/vllm/compilation/passes/ir/inplace_functionalization/)
- [ lowering_pass ](../../api/vllm/compilation/passes/ir/lowering_pass/)
- [ utils ](../../api/vllm/compilation/passes/ir/utils/)

[ utility ](../../api/vllm/compilation/passes/utility/)

utility

- [ fix_functionalization ](../../api/vllm/compilation/passes/utility/fix_functionalization/)
- [ noop_elimination ](../../api/vllm/compilation/passes/utility/noop_elimination/)
- [ post_cleanup ](../../api/vllm/compilation/passes/utility/post_cleanup/)
- [ scatter_split_replace ](../../api/vllm/compilation/passes/utility/scatter_split_replace/)
- [ split_coalescing ](../../api/vllm/compilation/passes/utility/split_coalescing/)

[ config ](../../api/vllm/config/)

config

- [ attention ](../../api/vllm/config/attention/)
- [ cache ](../../api/vllm/config/cache/)
- [ compilation ](../../api/vllm/config/compilation/)
- [ device ](../../api/vllm/config/device/)
- [ diffusion ](../../api/vllm/config/diffusion/)
- [ ec_manager_config ](../../api/vllm/config/ec_manager_config/)
- [ ec_transfer ](../../api/vllm/config/ec_transfer/)
- [ fault_tolerance ](../../api/vllm/config/fault_tolerance/)
- [ kernel ](../../api/vllm/config/kernel/)
- [ kv_events ](../../api/vllm/config/kv_events/)
- [ kv_transfer ](../../api/vllm/config/kv_transfer/)
- [ load ](../../api/vllm/config/load/)
- [ lora ](../../api/vllm/config/lora/)
- [ mamba ](../../api/vllm/config/mamba/)
- [ model ](../../api/vllm/config/model/)
- [ model_arch ](../../api/vllm/config/model_arch/)
- [ multimodal ](../../api/vllm/config/multimodal/)
- [ observability ](../../api/vllm/config/observability/)
- [ offload ](../../api/vllm/config/offload/)
- [ parallel ](../../api/vllm/config/parallel/)
- [ pooler ](../../api/vllm/config/pooler/)
- [ profiler ](../../api/vllm/config/profiler/)
- [ quantization ](../../api/vllm/config/quantization/)
- [ reasoning ](../../api/vllm/config/reasoning/)
- [ scheduler ](../../api/vllm/config/scheduler/)
- [ speculative ](../../api/vllm/config/speculative/)
- [ speech_to_text ](../../api/vllm/config/speech_to_text/)
- [ structured_outputs ](../../api/vllm/config/structured_outputs/)
- [ utils ](../../api/vllm/config/utils/)
- [ vllm ](../../api/vllm/config/vllm/)
- [ weight_transfer ](../../api/vllm/config/weight_transfer/)

[ cute_utils ](../../api/vllm/cute_utils/)

cute_utils

- [ cvt ](../../api/vllm/cute_utils/cvt/)
- [ mbarrier ](../../api/vllm/cute_utils/mbarrier/)

[ device_allocator ](../../api/vllm/device_allocator/)

device_allocator

- [ cumem ](../../api/vllm/device_allocator/cumem/)
- [ sleep_mode_backend ](../../api/vllm/device_allocator/sleep_mode_backend/)
- [ xpumem ](../../api/vllm/device_allocator/xpumem/)

[ distributed ](../../api/vllm/distributed/)

distributed

[ communication_op ](../../api/vllm/distributed/communication_op/)

[ kv_events ](../../api/vllm/distributed/kv_events/)

[ nixl_utils ](../../api/vllm/distributed/nixl_utils/)

[ parallel_state ](../../api/vllm/distributed/parallel_state/)

[ stateless_coordinator ](../../api/vllm/distributed/stateless_coordinator/)

[ utils ](../../api/vllm/distributed/utils/)

[ device_communicators ](../../api/vllm/distributed/device_communicators/)

device_communicators

- [ aiter_custom_all_reduce ](../../api/vllm/distributed/device_communicators/aiter_custom_all_reduce/)
- [ all2all ](../../api/vllm/distributed/device_communicators/all2all/)
- [ all_reduce_utils ](../../api/vllm/distributed/device_communicators/all_reduce_utils/)
- [ base_device_communicator ](../../api/vllm/distributed/device_communicators/base_device_communicator/)
- [ cpu_communicator ](../../api/vllm/distributed/device_communicators/cpu_communicator/)
- [ cuda_communicator ](../../api/vllm/distributed/device_communicators/cuda_communicator/)
- [ cuda_wrapper ](../../api/vllm/distributed/device_communicators/cuda_wrapper/)
- [ custom_all_reduce ](../../api/vllm/distributed/device_communicators/custom_all_reduce/)
- [ flashinfer_all_reduce ](../../api/vllm/distributed/device_communicators/flashinfer_all_reduce/)
- [ mnnvl_compat ](../../api/vllm/distributed/device_communicators/mnnvl_compat/)
- [ pynccl ](../../api/vllm/distributed/device_communicators/pynccl/)
- [ pynccl_allocator ](../../api/vllm/distributed/device_communicators/pynccl_allocator/)
- [ pynccl_wrapper ](../../api/vllm/distributed/device_communicators/pynccl_wrapper/)
- [ quick_all_reduce ](../../api/vllm/distributed/device_communicators/quick_all_reduce/)
- [ ray_communicator ](../../api/vllm/distributed/device_communicators/ray_communicator/)
- [ shm_broadcast ](../../api/vllm/distributed/device_communicators/shm_broadcast/)
- [ shm_object_storage ](../../api/vllm/distributed/device_communicators/shm_object_storage/)
- [ symm_mem ](../../api/vllm/distributed/device_communicators/symm_mem/)
- [ xpu_communicator ](../../api/vllm/distributed/device_communicators/xpu_communicator/)

[ ec_transfer ](../../api/vllm/distributed/ec_transfer/)

ec_transfer

[ ec_transfer_state ](../../api/vllm/distributed/ec_transfer/ec_transfer_state/)

[ ec_connector ](../../api/vllm/distributed/ec_transfer/ec_connector/)

ec_connector

[ base ](../../api/vllm/distributed/ec_transfer/ec_connector/base/)

[ example_connector ](../../api/vllm/distributed/ec_transfer/ec_connector/example_connector/)

[ factory ](../../api/vllm/distributed/ec_transfer/ec_connector/factory/)

[ utils ](../../api/vllm/distributed/ec_transfer/ec_connector/utils/)

[ cpu ](../../api/vllm/distributed/ec_transfer/ec_connector/cpu/)

cpu

[ common ](../../api/vllm/distributed/ec_transfer/ec_connector/cpu/common/)

[ connector ](../../api/vllm/distributed/ec_transfer/ec_connector/cpu/connector/)

[ ec_shared_region ](../../api/vllm/distributed/ec_transfer/ec_connector/cpu/ec_shared_region/)

[ scheduler ](../../api/vllm/distributed/ec_transfer/ec_connector/cpu/scheduler/)

scheduler

- [ embedding_cache ](../../api/vllm/distributed/ec_transfer/ec_connector/cpu/scheduler/embedding_cache/)
- [ step_tracker ](../../api/vllm/distributed/ec_transfer/ec_connector/cpu/scheduler/step_tracker/)

[ worker ](../../api/vllm/distributed/ec_transfer/ec_connector/cpu/worker/)

worker

- [ descriptor_buffers ](../../api/vllm/distributed/ec_transfer/ec_connector/cpu/worker/descriptor_buffers/)

[ elastic_ep ](../../api/vllm/distributed/elastic_ep/)

elastic_ep

- [ elastic_execute ](../../api/vllm/distributed/elastic_ep/elastic_execute/)
- [ elastic_state ](../../api/vllm/distributed/elastic_ep/elastic_state/)
- [ standby_state ](../../api/vllm/distributed/elastic_ep/standby_state/)

[ eplb ](../../api/vllm/distributed/eplb/)

eplb

[ async_worker ](../../api/vllm/distributed/eplb/async_worker/)

[ eplb_communicator ](../../api/vllm/distributed/eplb/eplb_communicator/)

[ eplb_state ](../../api/vllm/distributed/eplb/eplb_state/)

[ eplb_utils ](../../api/vllm/distributed/eplb/eplb_utils/)

[ rebalance_execute ](../../api/vllm/distributed/eplb/rebalance_execute/)

[ policy ](../../api/vllm/distributed/eplb/policy/)

policy

- [ abstract ](../../api/vllm/distributed/eplb/policy/abstract/)
- [ default ](../../api/vllm/distributed/eplb/policy/default/)

[ kv_transfer ](../../api/vllm/distributed/kv_transfer/)

kv_transfer

[ kv_transfer_state ](../../api/vllm/distributed/kv_transfer/kv_transfer_state/)

[ kv_connector ](../../api/vllm/distributed/kv_transfer/kv_connector/)

kv_connector

[ base ](../../api/vllm/distributed/kv_transfer/kv_connector/base/)

[ factory ](../../api/vllm/distributed/kv_transfer/kv_connector/factory/)

[ utils ](../../api/vllm/distributed/kv_transfer/kv_connector/utils/)

[ v1 ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/)

v1

[ base ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/base/)

[ decode_bench_connector ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/decode_bench_connector/)

[ example_connector ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/example_connector/)

[ example_hidden_states_connector ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/example_hidden_states_connector/)

[ flexkv_connector ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/flexkv_connector/)

[ lmcache_connector ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/lmcache_connector/)

[ lmcache_mp_connector ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/lmcache_mp_connector/)

[ metrics ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/metrics/)

[ multi_connector ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/multi_connector/)

[ offloading_connector ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/offloading_connector/)

[ simple_cpu_offload_connector ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/simple_cpu_offload_connector/)

[ ssm_conv_transfer_utils ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/ssm_conv_transfer_utils/)

[ hf3fs ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/hf3fs/)

hf3fs

[ hf3fs_client ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/hf3fs/hf3fs_client/)

[ hf3fs_connector ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/hf3fs/hf3fs_connector/)

[ hf3fs_metadata_server ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/hf3fs/hf3fs_metadata_server/)

[ utils ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/hf3fs/utils/)

utils

- [ common ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/hf3fs/utils/common/)
- [ gather_scatter_helper ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/hf3fs/utils/gather_scatter_helper/)
- [ hf3fs_mock_client ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/hf3fs/utils/hf3fs_mock_client/)

[ lmcache_integration ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/lmcache_integration/)

lmcache_integration

- [ multi_process_adapter ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/lmcache_integration/multi_process_adapter/)
- [ utils ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/lmcache_integration/utils/)
- [ vllm_v1_adapter ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/lmcache_integration/vllm_v1_adapter/)

[ mooncake ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/mooncake/)

mooncake

[ mooncake_connector ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/mooncake/mooncake_connector/)

[ mooncake_utils ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/mooncake/mooncake_utils/)

[ rdma_utils ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/mooncake/rdma_utils/)

[ stats ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/mooncake/stats/)

[ store ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/mooncake/store/)

store

- [ connector ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/mooncake/store/connector/)
- [ coordinator ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/mooncake/store/coordinator/)
- [ data ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/mooncake/store/data/)
- [ metrics ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/mooncake/store/metrics/)
- [ protocol ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/mooncake/store/protocol/)
- [ scheduler ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/mooncake/store/scheduler/)
- [ worker ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/mooncake/store/worker/)

[ moriio ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/moriio/)

moriio

- [ moriio_common ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/moriio/moriio_common/)
- [ moriio_connector ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/moriio/moriio_connector/)
- [ moriio_engine ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/moriio/moriio_engine/)
- [ moriio_layout ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/moriio/moriio_layout/)

[ nixl ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/nixl/)

nixl

- [ base_scheduler ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/nixl/base_scheduler/)
- [ base_worker ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/nixl/base_worker/)
- [ connector ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/nixl/connector/)
- [ metadata ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/nixl/metadata/)
- [ pull_scheduler ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/nixl/pull_scheduler/)
- [ pull_worker ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/nixl/pull_worker/)
- [ push_scheduler ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/nixl/push_scheduler/)
- [ push_worker ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/nixl/push_worker/)
- [ scheduler ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/nixl/scheduler/)
- [ stats ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/nixl/stats/)
- [ tp_mapping ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/nixl/tp_mapping/)
- [ utils ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/nixl/utils/)
- [ worker ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/nixl/worker/)

[ offloading ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/offloading/)

offloading

- [ canonical_mapping ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/offloading/canonical_mapping/)
- [ common ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/offloading/common/)
- [ config ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/offloading/config/)
- [ events ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/offloading/events/)
- [ metrics ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/offloading/metrics/)
- [ scheduler ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/offloading/scheduler/)
- [ worker ](../../api/vllm/distributed/kv_transfer/kv_connector/v1/offloading/worker/)

[ weight_transfer ](../../api/vllm/distributed/weight_transfer/)

weight_transfer

- [ base ](../../api/vllm/distributed/weight_transfer/base/)
- [ clients ](../../api/vllm/distributed/weight_transfer/clients/)
- [ factory ](../../api/vllm/distributed/weight_transfer/factory/)
- [ ipc_engine ](../../api/vllm/distributed/weight_transfer/ipc_engine/)
- [ nccl_common ](../../api/vllm/distributed/weight_transfer/nccl_common/)
- [ nccl_engine ](../../api/vllm/distributed/weight_transfer/nccl_engine/)
- [ packed_tensor ](../../api/vllm/distributed/weight_transfer/packed_tensor/)
- [ sparse_nccl_engine ](../../api/vllm/distributed/weight_transfer/sparse_nccl_engine/)

[ engine ](../../api/vllm/engine/)

engine

- [ arg_utils ](../../api/vllm/engine/arg_utils/)
- [ async_llm_engine ](../../api/vllm/engine/async_llm_engine/)
- [ llm_engine ](../../api/vllm/engine/llm_engine/)
- [ protocol ](../../api/vllm/engine/protocol/)

[ entrypoints ](../../api/vllm/entrypoints/)

entrypoints

[ chat_utils ](../../api/vllm/entrypoints/chat_utils/)

[ grpc_server ](../../api/vllm/entrypoints/grpc_server/)

[ launcher ](../../api/vllm/entrypoints/launcher/)

[ llm ](../../api/vllm/entrypoints/llm/)

[ offline_utils ](../../api/vllm/entrypoints/offline_utils/)

[ anthropic ](../../api/vllm/entrypoints/anthropic/)

anthropic

- [ api_router ](../../api/vllm/entrypoints/anthropic/api_router/)
- [ protocol ](../../api/vllm/entrypoints/anthropic/protocol/)
- [ serving ](../../api/vllm/entrypoints/anthropic/serving/)

[ cli ](../../api/vllm/entrypoints/cli/)

cli

[ collect_env ](../../api/vllm/entrypoints/cli/collect_env/)

[ launch ](../../api/vllm/entrypoints/cli/launch/)

[ main ](../../api/vllm/entrypoints/cli/main/)

[ openai ](../../api/vllm/entrypoints/cli/openai/)

[ run_batch ](../../api/vllm/entrypoints/cli/run_batch/)

[ serve ](../../api/vllm/entrypoints/cli/serve/)

[ types ](../../api/vllm/entrypoints/cli/types/)

[ benchmark ](../../api/vllm/entrypoints/cli/benchmark/)

benchmark

- [ base ](../../api/vllm/entrypoints/cli/benchmark/base/)
- [ latency ](../../api/vllm/entrypoints/cli/benchmark/latency/)
- [ main ](../../api/vllm/entrypoints/cli/benchmark/main/)
- [ mm_processor ](../../api/vllm/entrypoints/cli/benchmark/mm_processor/)
- [ serve ](../../api/vllm/entrypoints/cli/benchmark/serve/)
- [ startup ](../../api/vllm/entrypoints/cli/benchmark/startup/)
- [ sweep ](../../api/vllm/entrypoints/cli/benchmark/sweep/)
- [ throughput ](../../api/vllm/entrypoints/cli/benchmark/throughput/)

[ cohere ](../../api/vllm/entrypoints/cohere/)

cohere

- [ api_router ](../../api/vllm/entrypoints/cohere/api_router/)
- [ cohere_chat_message ](../../api/vllm/entrypoints/cohere/cohere_chat_message/)
- [ protocol ](../../api/vllm/entrypoints/cohere/protocol/)
- [ serving ](../../api/vllm/entrypoints/cohere/serving/)

[ generate ](../../api/vllm/entrypoints/generate/)

generate

[ api_router ](../../api/vllm/entrypoints/generate/api_router/)

[ factories ](../../api/vllm/entrypoints/generate/factories/)

[ base ](../../api/vllm/entrypoints/generate/base/)

base

- [ serving ](../../api/vllm/entrypoints/generate/base/serving/)

[ beam_search ](../../api/vllm/entrypoints/generate/beam_search/)

beam_search

- [ offline ](../../api/vllm/entrypoints/generate/beam_search/offline/)
- [ online ](../../api/vllm/entrypoints/generate/beam_search/online/)
- [ utils ](../../api/vllm/entrypoints/generate/beam_search/utils/)

[ generative_scoring ](../../api/vllm/entrypoints/generate/generative_scoring/)

generative_scoring

- [ api_router ](../../api/vllm/entrypoints/generate/generative_scoring/api_router/)
- [ serving ](../../api/vllm/entrypoints/generate/generative_scoring/serving/)

[ mcp ](../../api/vllm/entrypoints/mcp/)

mcp

- [ tool ](../../api/vllm/entrypoints/mcp/tool/)
- [ tool_server ](../../api/vllm/entrypoints/mcp/tool_server/)

[ openai ](../../api/vllm/entrypoints/openai/)

openai

[ api_server ](../../api/vllm/entrypoints/openai/api_server/)

[ cli_args ](../../api/vllm/entrypoints/openai/cli_args/)

[ dp_supervisor ](../../api/vllm/entrypoints/openai/dp_supervisor/)

[ run_batch ](../../api/vllm/entrypoints/openai/run_batch/)

[ chat_completion ](../../api/vllm/entrypoints/openai/chat_completion/)

chat_completion

- [ api_router ](../../api/vllm/entrypoints/openai/chat_completion/api_router/)
- [ batch_serving ](../../api/vllm/entrypoints/openai/chat_completion/batch_serving/)
- [ protocol ](../../api/vllm/entrypoints/openai/chat_completion/protocol/)
- [ serving ](../../api/vllm/entrypoints/openai/chat_completion/serving/)

[ completion ](../../api/vllm/entrypoints/openai/completion/)

completion

- [ api_router ](../../api/vllm/entrypoints/openai/completion/api_router/)
- [ protocol ](../../api/vllm/entrypoints/openai/completion/protocol/)
- [ serving ](../../api/vllm/entrypoints/openai/completion/serving/)

[ engine ](../../api/vllm/entrypoints/openai/engine/)

engine

- [ protocol ](../../api/vllm/entrypoints/openai/engine/protocol/)

[ models ](../../api/vllm/entrypoints/openai/models/)

models

- [ api_router ](../../api/vllm/entrypoints/openai/models/api_router/)
- [ protocol ](../../api/vllm/entrypoints/openai/models/protocol/)
- [ serving ](../../api/vllm/entrypoints/openai/models/serving/)

[ parser ](../../api/vllm/entrypoints/openai/parser/)

parser

- [ harmony_utils ](../../api/vllm/entrypoints/openai/parser/harmony_utils/)

[ responses ](../../api/vllm/entrypoints/openai/responses/)

responses

- [ api_router ](../../api/vllm/entrypoints/openai/responses/api_router/)
- [ context ](../../api/vllm/entrypoints/openai/responses/context/)
- [ harmony ](../../api/vllm/entrypoints/openai/responses/harmony/)
- [ protocol ](../../api/vllm/entrypoints/openai/responses/protocol/)
- [ serving ](../../api/vllm/entrypoints/openai/responses/serving/)
- [ streaming_events ](../../api/vllm/entrypoints/openai/responses/streaming_events/)
- [ utils ](../../api/vllm/entrypoints/openai/responses/utils/)

[ pooling ](../../api/vllm/entrypoints/pooling/)

pooling

[ factories ](../../api/vllm/entrypoints/pooling/factories/)

[ offline ](../../api/vllm/entrypoints/pooling/offline/)

[ typing ](../../api/vllm/entrypoints/pooling/typing/)

[ utils ](../../api/vllm/entrypoints/pooling/utils/)

[ base ](../../api/vllm/entrypoints/pooling/base/)

base

- [ io_processor ](../../api/vllm/entrypoints/pooling/base/io_processor/)
- [ protocol ](../../api/vllm/entrypoints/pooling/base/protocol/)
- [ serving ](../../api/vllm/entrypoints/pooling/base/serving/)

[ classify ](../../api/vllm/entrypoints/pooling/classify/)

classify

- [ api_router ](../../api/vllm/entrypoints/pooling/classify/api_router/)
- [ io_processor ](../../api/vllm/entrypoints/pooling/classify/io_processor/)
- [ protocol ](../../api/vllm/entrypoints/pooling/classify/protocol/)
- [ serving ](../../api/vllm/entrypoints/pooling/classify/serving/)

[ embed ](../../api/vllm/entrypoints/pooling/embed/)

embed

- [ api_router ](../../api/vllm/entrypoints/pooling/embed/api_router/)
- [ io_processor ](../../api/vllm/entrypoints/pooling/embed/io_processor/)
- [ protocol ](../../api/vllm/entrypoints/pooling/embed/protocol/)
- [ serving ](../../api/vllm/entrypoints/pooling/embed/serving/)

[ pooling ](../../api/vllm/entrypoints/pooling/pooling/)

pooling

- [ api_router ](../../api/vllm/entrypoints/pooling/pooling/api_router/)
- [ io_processor ](../../api/vllm/entrypoints/pooling/pooling/io_processor/)
- [ protocol ](../../api/vllm/entrypoints/pooling/pooling/protocol/)
- [ serving ](../../api/vllm/entrypoints/pooling/pooling/serving/)

[ scoring ](../../api/vllm/entrypoints/pooling/scoring/)

scoring

- [ api_router ](../../api/vllm/entrypoints/pooling/scoring/api_router/)
- [ io_processor ](../../api/vllm/entrypoints/pooling/scoring/io_processor/)
- [ protocol ](../../api/vllm/entrypoints/pooling/scoring/protocol/)
- [ serving ](../../api/vllm/entrypoints/pooling/scoring/serving/)
- [ typing ](../../api/vllm/entrypoints/pooling/scoring/typing/)
- [ utils ](../../api/vllm/entrypoints/pooling/scoring/utils/)

[ scale_out ](../../api/vllm/entrypoints/scale_out/)

scale_out

[ factories ](../../api/vllm/entrypoints/scale_out/factories/)

[ derender ](../../api/vllm/entrypoints/scale_out/derender/)

derender

- [ api_router ](../../api/vllm/entrypoints/scale_out/derender/api_router/)
- [ serving ](../../api/vllm/entrypoints/scale_out/derender/serving/)

[ render ](../../api/vllm/entrypoints/scale_out/render/)

render

- [ api_router ](../../api/vllm/entrypoints/scale_out/render/api_router/)
- [ serving ](../../api/vllm/entrypoints/scale_out/render/serving/)

[ token_in_token_out ](../../api/vllm/entrypoints/scale_out/token_in_token_out/)

token_in_token_out

- [ api_router ](../../api/vllm/entrypoints/scale_out/token_in_token_out/api_router/)
- [ mm_serde ](../../api/vllm/entrypoints/scale_out/token_in_token_out/mm_serde/)
- [ protocol ](../../api/vllm/entrypoints/scale_out/token_in_token_out/protocol/)
- [ serving ](../../api/vllm/entrypoints/scale_out/token_in_token_out/serving/)

[ serve ](../../api/vllm/entrypoints/serve/)

serve

[ dev ](../../api/vllm/entrypoints/serve/dev/)

dev

[ cache ](../../api/vllm/entrypoints/serve/dev/cache/)

cache

- [ api_router ](../../api/vllm/entrypoints/serve/dev/cache/api_router/)

[ rlhf ](../../api/vllm/entrypoints/serve/dev/rlhf/)

rlhf

- [ api_router ](../../api/vllm/entrypoints/serve/dev/rlhf/api_router/)

[ rpc ](../../api/vllm/entrypoints/serve/dev/rpc/)

rpc

- [ api_router ](../../api/vllm/entrypoints/serve/dev/rpc/api_router/)

[ server_info ](../../api/vllm/entrypoints/serve/dev/server_info/)

server_info

- [ api_router ](../../api/vllm/entrypoints/serve/dev/server_info/api_router/)

[ sleep ](../../api/vllm/entrypoints/serve/dev/sleep/)

sleep

- [ api_router ](../../api/vllm/entrypoints/serve/dev/sleep/api_router/)

[ elastic_ep ](../../api/vllm/entrypoints/serve/elastic_ep/)

elastic_ep

- [ api_router ](../../api/vllm/entrypoints/serve/elastic_ep/api_router/)
- [ middleware ](../../api/vllm/entrypoints/serve/elastic_ep/middleware/)

[ engine ](../../api/vllm/entrypoints/serve/engine/)

engine

- [ serving ](../../api/vllm/entrypoints/serve/engine/serving/)
- [ typing ](../../api/vllm/entrypoints/serve/engine/typing/)

[ exception_handling ](../../api/vllm/entrypoints/serve/exception_handling/)

exception_handling

[ error_response ](../../api/vllm/entrypoints/serve/exception_handling/error_response/)

[ register ](../../api/vllm/entrypoints/serve/exception_handling/register/)

[ utils ](../../api/vllm/entrypoints/serve/exception_handling/utils/)

[ handlers ](../../api/vllm/entrypoints/serve/exception_handling/handlers/)

handlers

- [ exception ](../../api/vllm/entrypoints/serve/exception_handling/handlers/exception/)
- [ http ](../../api/vllm/entrypoints/serve/exception_handling/handlers/http/)
- [ validation ](../../api/vllm/entrypoints/serve/exception_handling/handlers/validation/)
- [ vllm_error ](../../api/vllm/entrypoints/serve/exception_handling/handlers/vllm_error/)

[ fault_tolerance ](../../api/vllm/entrypoints/serve/fault_tolerance/)

fault_tolerance

- [ api_router ](../../api/vllm/entrypoints/serve/fault_tolerance/api_router/)

[ instrumentator ](../../api/vllm/entrypoints/serve/instrumentator/)

instrumentator

- [ basic ](../../api/vllm/entrypoints/serve/instrumentator/basic/)
- [ health ](../../api/vllm/entrypoints/serve/instrumentator/health/)
- [ metrics ](../../api/vllm/entrypoints/serve/instrumentator/metrics/)
- [ offline_docs ](../../api/vllm/entrypoints/serve/instrumentator/offline_docs/)

[ lora ](../../api/vllm/entrypoints/serve/lora/)

lora

- [ api_router ](../../api/vllm/entrypoints/serve/lora/api_router/)
- [ protocol ](../../api/vllm/entrypoints/serve/lora/protocol/)

[ profile ](../../api/vllm/entrypoints/serve/profile/)

profile

- [ api_router ](../../api/vllm/entrypoints/serve/profile/api_router/)

[ sagemaker ](../../api/vllm/entrypoints/serve/sagemaker/)

sagemaker

- [ api_router ](../../api/vllm/entrypoints/serve/sagemaker/api_router/)

[ tokenize ](../../api/vllm/entrypoints/serve/tokenize/)

tokenize

- [ api_router ](../../api/vllm/entrypoints/serve/tokenize/api_router/)
- [ protocol ](../../api/vllm/entrypoints/serve/tokenize/protocol/)
- [ serving ](../../api/vllm/entrypoints/serve/tokenize/serving/)

[ utils ](../../api/vllm/entrypoints/serve/utils/)

utils

- [ api_utils ](../../api/vllm/entrypoints/serve/utils/api_utils/)
- [ constants ](../../api/vllm/entrypoints/serve/utils/constants/)
- [ fingerprint ](../../api/vllm/entrypoints/serve/utils/fingerprint/)
- [ orca_metrics ](../../api/vllm/entrypoints/serve/utils/orca_metrics/)
- [ request_logger ](../../api/vllm/entrypoints/serve/utils/request_logger/)
- [ server_utils ](../../api/vllm/entrypoints/serve/utils/server_utils/)
- [ ssl ](../../api/vllm/entrypoints/serve/utils/ssl/)
- [ tool_calls_utils ](../../api/vllm/entrypoints/serve/utils/tool_calls_utils/)

[ speech_to_text ](../../api/vllm/entrypoints/speech_to_text/)

speech_to_text

[ factories ](../../api/vllm/entrypoints/speech_to_text/factories/)

[ base ](../../api/vllm/entrypoints/speech_to_text/base/)

base

- [ protocol ](../../api/vllm/entrypoints/speech_to_text/base/protocol/)
- [ serving ](../../api/vllm/entrypoints/speech_to_text/base/serving/)
- [ utils ](../../api/vllm/entrypoints/speech_to_text/base/utils/)

[ realtime ](../../api/vllm/entrypoints/speech_to_text/realtime/)

realtime

- [ api_router ](../../api/vllm/entrypoints/speech_to_text/realtime/api_router/)
- [ connection ](../../api/vllm/entrypoints/speech_to_text/realtime/connection/)
- [ metrics ](../../api/vllm/entrypoints/speech_to_text/realtime/metrics/)
- [ protocol ](../../api/vllm/entrypoints/speech_to_text/realtime/protocol/)
- [ serving ](../../api/vllm/entrypoints/speech_to_text/realtime/serving/)

[ transcription ](../../api/vllm/entrypoints/speech_to_text/transcription/)

transcription

- [ api_router ](../../api/vllm/entrypoints/speech_to_text/transcription/api_router/)
- [ protocol ](../../api/vllm/entrypoints/speech_to_text/transcription/protocol/)
- [ serving ](../../api/vllm/entrypoints/speech_to_text/transcription/serving/)

[ translation ](../../api/vllm/entrypoints/speech_to_text/translation/)

translation

- [ api_router ](../../api/vllm/entrypoints/speech_to_text/translation/api_router/)
- [ protocol ](../../api/vllm/entrypoints/speech_to_text/translation/protocol/)
- [ serving ](../../api/vllm/entrypoints/speech_to_text/translation/serving/)

[ inputs ](../../api/vllm/inputs/)

inputs

- [ engine ](../../api/vllm/inputs/engine/)
- [ llm ](../../api/vllm/inputs/llm/)
- [ preprocess ](../../api/vllm/inputs/preprocess/)

[ ir ](../../api/vllm/ir/)

ir

[ op ](../../api/vllm/ir/op/)

[ tolerances ](../../api/vllm/ir/tolerances/)

[ util ](../../api/vllm/ir/util/)

[ ops ](../../api/vllm/ir/ops/)

ops

- [ layernorm ](../../api/vllm/ir/ops/layernorm/)

[ kernels ](../../api/vllm/kernels/)

kernels

[ aiter_ops ](../../api/vllm/kernels/aiter_ops/)

[ oink_ops ](../../api/vllm/kernels/oink_ops/)

[ vllm_c ](../../api/vllm/kernels/vllm_c/)

[ helion ](../../api/vllm/kernels/helion/)

helion

[ case_key ](../../api/vllm/kernels/helion/case_key/)

[ config_manager ](../../api/vllm/kernels/helion/config_manager/)

[ register ](../../api/vllm/kernels/helion/register/)

[ utils ](../../api/vllm/kernels/helion/utils/)

[ ops ](../../api/vllm/kernels/helion/ops/)

ops

- [ dynamic_per_token_scaled_fp8_quant ](../../api/vllm/kernels/helion/ops/dynamic_per_token_scaled_fp8_quant/)
- [ fused_qk_norm_rope ](../../api/vllm/kernels/helion/ops/fused_qk_norm_rope/)
- [ per_token_group_fp8_quant ](../../api/vllm/kernels/helion/ops/per_token_group_fp8_quant/)
- [ rms_norm_dynamic_per_token_quant ](../../api/vllm/kernels/helion/ops/rms_norm_dynamic_per_token_quant/)
- [ rms_norm_per_block_quant ](../../api/vllm/kernels/helion/ops/rms_norm_per_block_quant/)
- [ silu_and_mul_per_block_quant ](../../api/vllm/kernels/helion/ops/silu_and_mul_per_block_quant/)
- [ silu_mul_fp8 ](../../api/vllm/kernels/helion/ops/silu_mul_fp8/)

[ triton ](../../api/vllm/kernels/triton/)

triton

- [ qkv_padded_fp8_quant ](../../api/vllm/kernels/triton/qkv_padded_fp8_quant/)

[ logging_utils ](../../api/vllm/logging_utils/)

logging_utils

- [ access_log_filter ](../../api/vllm/logging_utils/access_log_filter/)
- [ dump_input ](../../api/vllm/logging_utils/dump_input/)
- [ formatter ](../../api/vllm/logging_utils/formatter/)
- [ lazy ](../../api/vllm/logging_utils/lazy/)
- [ log_time ](../../api/vllm/logging_utils/log_time/)
- [ torch_tensor ](../../api/vllm/logging_utils/torch_tensor/)

[ lora ](../../api/vllm/lora/)

lora

[ lora_model ](../../api/vllm/lora/lora_model/)

[ lora_weights ](../../api/vllm/lora/lora_weights/)

[ model_manager ](../../api/vllm/lora/model_manager/)

[ peft_helper ](../../api/vllm/lora/peft_helper/)

[ request ](../../api/vllm/lora/request/)

[ resolver ](../../api/vllm/lora/resolver/)

[ utils ](../../api/vllm/lora/utils/)

[ worker_manager ](../../api/vllm/lora/worker_manager/)

[ layers ](../../api/vllm/lora/layers/)

layers

- [ base ](../../api/vllm/lora/layers/base/)
- [ base_linear ](../../api/vllm/lora/layers/base_linear/)
- [ column_parallel_linear ](../../api/vllm/lora/layers/column_parallel_linear/)
- [ fused_moe ](../../api/vllm/lora/layers/fused_moe/)
- [ logits_processor ](../../api/vllm/lora/layers/logits_processor/)
- [ replicated_linear ](../../api/vllm/lora/layers/replicated_linear/)
- [ row_parallel_linear ](../../api/vllm/lora/layers/row_parallel_linear/)
- [ utils ](../../api/vllm/lora/layers/utils/)
- [ vocal_parallel_embedding ](../../api/vllm/lora/layers/vocal_parallel_embedding/)

[ ops ](../../api/vllm/lora/ops/)

ops

[ torch_ops ](../../api/vllm/lora/ops/torch_ops/)

torch_ops

- [ lora_ops ](../../api/vllm/lora/ops/torch_ops/lora_ops/)

[ triton_ops ](../../api/vllm/lora/ops/triton_ops/)

triton_ops

- [ fp8_kernel_utils ](../../api/vllm/lora/ops/triton_ops/fp8_kernel_utils/)
- [ fused_moe_lora_fp8_op ](../../api/vllm/lora/ops/triton_ops/fused_moe_lora_fp8_op/)
- [ fused_moe_lora_op ](../../api/vllm/lora/ops/triton_ops/fused_moe_lora_op/)
- [ kernel_utils ](../../api/vllm/lora/ops/triton_ops/kernel_utils/)
- [ lora_expand_fp8_op ](../../api/vllm/lora/ops/triton_ops/lora_expand_fp8_op/)
- [ lora_expand_op ](../../api/vllm/lora/ops/triton_ops/lora_expand_op/)
- [ lora_kernel_metadata ](../../api/vllm/lora/ops/triton_ops/lora_kernel_metadata/)
- [ lora_shrink_fp8_op ](../../api/vllm/lora/ops/triton_ops/lora_shrink_fp8_op/)
- [ lora_shrink_op ](../../api/vllm/lora/ops/triton_ops/lora_shrink_op/)
- [ utils ](../../api/vllm/lora/ops/triton_ops/utils/)

[ xpu_ops ](../../api/vllm/lora/ops/xpu_ops/)

xpu_ops

- [ lora_ops ](../../api/vllm/lora/ops/xpu_ops/lora_ops/)

[ punica_wrapper ](../../api/vllm/lora/punica_wrapper/)

punica_wrapper

- [ punica_base ](../../api/vllm/lora/punica_wrapper/punica_base/)
- [ punica_cpu ](../../api/vllm/lora/punica_wrapper/punica_cpu/)
- [ punica_gpu ](../../api/vllm/lora/punica_wrapper/punica_gpu/)
- [ punica_selector ](../../api/vllm/lora/punica_wrapper/punica_selector/)
- [ punica_xpu ](../../api/vllm/lora/punica_wrapper/punica_xpu/)
- [ utils ](../../api/vllm/lora/punica_wrapper/utils/)

[ model_executor ](../../api/vllm/model_executor/)

model_executor

[ custom_op ](../../api/vllm/model_executor/custom_op/)

[ parameter ](../../api/vllm/model_executor/parameter/)

[ utils ](../../api/vllm/model_executor/utils/)

[ hw_agnostic ](../../api/vllm/model_executor/hw_agnostic/)

hw_agnostic

[ custom_op ](../../api/vllm/model_executor/hw_agnostic/custom_op/)

[ layers ](../../api/vllm/model_executor/hw_agnostic/layers/)

layers

- [ activation ](../../api/vllm/model_executor/hw_agnostic/layers/activation/)
- [ layernorm ](../../api/vllm/model_executor/hw_agnostic/layers/layernorm/)

[ kernels ](../../api/vllm/model_executor/kernels/)

kernels

[ attention ](../../api/vllm/model_executor/kernels/attention/)

attention

[ dsa ](../../api/vllm/model_executor/kernels/attention/dsa/)

dsa

- [ dcp_indexer_cutedsl ](../../api/vllm/model_executor/kernels/attention/dsa/dcp_indexer_cutedsl/)

[ linear ](../../api/vllm/model_executor/kernels/linear/)

linear

[ base ](../../api/vllm/model_executor/kernels/linear/base/)

[ zentorch_utils ](../../api/vllm/model_executor/kernels/linear/zentorch_utils/)

[ cute_dsl ](../../api/vllm/model_executor/kernels/linear/cute_dsl/)

cute_dsl

- [ ll_bf16 ](../../api/vllm/model_executor/kernels/linear/cute_dsl/ll_bf16/)
- [ skinny_gemm ](../../api/vllm/model_executor/kernels/linear/cute_dsl/skinny_gemm/)

[ mixed_precision ](../../api/vllm/model_executor/kernels/linear/mixed_precision/)

mixed_precision

- [ allspark ](../../api/vllm/model_executor/kernels/linear/mixed_precision/allspark/)
- [ conch ](../../api/vllm/model_executor/kernels/linear/mixed_precision/conch/)
- [ cpu ](../../api/vllm/model_executor/kernels/linear/mixed_precision/cpu/)
- [ cutlass ](../../api/vllm/model_executor/kernels/linear/mixed_precision/cutlass/)
- [ dynamic_4bit ](../../api/vllm/model_executor/kernels/linear/mixed_precision/dynamic_4bit/)
- [ exllama ](../../api/vllm/model_executor/kernels/linear/mixed_precision/exllama/)
- [ humming ](../../api/vllm/model_executor/kernels/linear/mixed_precision/humming/)
- [ MPLinearKernel ](../../api/vllm/model_executor/kernels/linear/mixed_precision/MPLinearKernel/)
- [ machete ](../../api/vllm/model_executor/kernels/linear/mixed_precision/machete/)
- [ marlin ](../../api/vllm/model_executor/kernels/linear/mixed_precision/marlin/)
- [ rdna3_w4a16 ](../../api/vllm/model_executor/kernels/linear/mixed_precision/rdna3_w4a16/)
- [ rdna_hybrid_w4a16 ](../../api/vllm/model_executor/kernels/linear/mixed_precision/rdna_hybrid_w4a16/)
- [ triton_w4a16 ](../../api/vllm/model_executor/kernels/linear/mixed_precision/triton_w4a16/)
- [ xpu ](../../api/vllm/model_executor/kernels/linear/mixed_precision/xpu/)
- [ zentorch ](../../api/vllm/model_executor/kernels/linear/mixed_precision/zentorch/)

[ mxfp4 ](../../api/vllm/model_executor/kernels/linear/mxfp4/)

mxfp4

- [ aiter ](../../api/vllm/model_executor/kernels/linear/mxfp4/aiter/)
- [ b12x ](../../api/vllm/model_executor/kernels/linear/mxfp4/b12x/)
- [ base ](../../api/vllm/model_executor/kernels/linear/mxfp4/base/)
- [ emulation ](../../api/vllm/model_executor/kernels/linear/mxfp4/emulation/)
- [ flashinfer ](../../api/vllm/model_executor/kernels/linear/mxfp4/flashinfer/)
- [ humming ](../../api/vllm/model_executor/kernels/linear/mxfp4/humming/)
- [ marlin ](../../api/vllm/model_executor/kernels/linear/mxfp4/marlin/)
- [ xpu ](../../api/vllm/model_executor/kernels/linear/mxfp4/xpu/)

[ mxfp6 ](../../api/vllm/model_executor/kernels/linear/mxfp6/)

mxfp6

- [ base ](../../api/vllm/model_executor/kernels/linear/mxfp6/base/)
- [ emulation ](../../api/vllm/model_executor/kernels/linear/mxfp6/emulation/)

[ mxfp8 ](../../api/vllm/model_executor/kernels/linear/mxfp8/)

mxfp8

- [ b12x ](../../api/vllm/model_executor/kernels/linear/mxfp8/b12x/)
- [ emulation ](../../api/vllm/model_executor/kernels/linear/mxfp8/emulation/)
- [ flashinfer ](../../api/vllm/model_executor/kernels/linear/mxfp8/flashinfer/)
- [ humming ](../../api/vllm/model_executor/kernels/linear/mxfp8/humming/)
- [ Mxfp8LinearKernel ](../../api/vllm/model_executor/kernels/linear/mxfp8/Mxfp8LinearKernel/)
- [ marlin ](../../api/vllm/model_executor/kernels/linear/mxfp8/marlin/)
- [ rocm_native ](../../api/vllm/model_executor/kernels/linear/mxfp8/rocm_native/)
- [ xpu ](../../api/vllm/model_executor/kernels/linear/mxfp8/xpu/)

[ nvfp4 ](../../api/vllm/model_executor/kernels/linear/nvfp4/)

nvfp4

- [ b12x ](../../api/vllm/model_executor/kernels/linear/nvfp4/b12x/)
- [ base ](../../api/vllm/model_executor/kernels/linear/nvfp4/base/)
- [ cutlass ](../../api/vllm/model_executor/kernels/linear/nvfp4/cutlass/)
- [ emulation ](../../api/vllm/model_executor/kernels/linear/nvfp4/emulation/)
- [ fbgemm ](../../api/vllm/model_executor/kernels/linear/nvfp4/fbgemm/)
- [ flashinfer ](../../api/vllm/model_executor/kernels/linear/nvfp4/flashinfer/)
- [ humming ](../../api/vllm/model_executor/kernels/linear/nvfp4/humming/)
- [ marlin ](../../api/vllm/model_executor/kernels/linear/nvfp4/marlin/)

[ scaled_mm ](../../api/vllm/model_executor/kernels/linear/scaled_mm/)

scaled_mm

- [ aiter ](../../api/vllm/model_executor/kernels/linear/scaled_mm/aiter/)
- [ BlockScaledMMLinearKernel ](../../api/vllm/model_executor/kernels/linear/scaled_mm/BlockScaledMMLinearKernel/)
- [ b12x_block ](../../api/vllm/model_executor/kernels/linear/scaled_mm/b12x_block/)
- [ b12x_tensor ](../../api/vllm/model_executor/kernels/linear/scaled_mm/b12x_tensor/)
- [ cpu ](../../api/vllm/model_executor/kernels/linear/scaled_mm/cpu/)
- [ cutlass ](../../api/vllm/model_executor/kernels/linear/scaled_mm/cutlass/)
- [ deep_gemm ](../../api/vllm/model_executor/kernels/linear/scaled_mm/deep_gemm/)
- [ flashinfer ](../../api/vllm/model_executor/kernels/linear/scaled_mm/flashinfer/)
- [ humming ](../../api/vllm/model_executor/kernels/linear/scaled_mm/humming/)
- [ marlin ](../../api/vllm/model_executor/kernels/linear/scaled_mm/marlin/)
- [ pytorch ](../../api/vllm/model_executor/kernels/linear/scaled_mm/pytorch/)
- [ rocm ](../../api/vllm/model_executor/kernels/linear/scaled_mm/rocm/)
- [ ScaledMMLinearKernel ](../../api/vllm/model_executor/kernels/linear/scaled_mm/ScaledMMLinearKernel/)
- [ triton ](../../api/vllm/model_executor/kernels/linear/scaled_mm/triton/)
- [ xpu ](../../api/vllm/model_executor/kernels/linear/scaled_mm/xpu/)
- [ zentorch ](../../api/vllm/model_executor/kernels/linear/scaled_mm/zentorch/)

[ mhc ](../../api/vllm/model_executor/kernels/mhc/)

mhc

- [ aiter ](../../api/vllm/model_executor/kernels/mhc/aiter/)
- [ tilelang ](../../api/vllm/model_executor/kernels/mhc/tilelang/)
- [ tilelang_kernels ](../../api/vllm/model_executor/kernels/mhc/tilelang_kernels/)
- [ torch ](../../api/vllm/model_executor/kernels/mhc/torch/)
- [ triton ](../../api/vllm/model_executor/kernels/mhc/triton/)

[ layers ](../../api/vllm/model_executor/layers/)

layers

[ activation ](../../api/vllm/model_executor/layers/activation/)

[ attention_layer_base ](../../api/vllm/model_executor/layers/attention_layer_base/)

[ batch_invariant ](../../api/vllm/model_executor/layers/batch_invariant/)

[ conv ](../../api/vllm/model_executor/layers/conv/)

[ fused_allreduce_gemma_rms_norm ](../../api/vllm/model_executor/layers/fused_allreduce_gemma_rms_norm/)

[ fused_qk_norm_rope ](../../api/vllm/model_executor/layers/fused_qk_norm_rope/)

[ layernorm ](../../api/vllm/model_executor/layers/layernorm/)

[ lightning_attn ](../../api/vllm/model_executor/layers/lightning_attn/)

[ linear ](../../api/vllm/model_executor/layers/linear/)

[ logits_processor ](../../api/vllm/model_executor/layers/logits_processor/)

[ mhc ](../../api/vllm/model_executor/layers/mhc/)

[ mla ](../../api/vllm/model_executor/layers/mla/)

[ resampler ](../../api/vllm/model_executor/layers/resampler/)

[ sparse_attn_indexer ](../../api/vllm/model_executor/layers/sparse_attn_indexer/)

[ utils ](../../api/vllm/model_executor/layers/utils/)

[ vocab_parallel_embedding ](../../api/vllm/model_executor/layers/vocab_parallel_embedding/)

[ attention ](../../api/vllm/model_executor/layers/attention/)

attention

- [ attention ](../../api/vllm/model_executor/layers/attention/attention/)
- [ chunked_local_attention ](../../api/vllm/model_executor/layers/attention/chunked_local_attention/)
- [ cross_attention ](../../api/vllm/model_executor/layers/attention/cross_attention/)
- [ encoder_only_attention ](../../api/vllm/model_executor/layers/attention/encoder_only_attention/)
- [ kv_transfer_utils ](../../api/vllm/model_executor/layers/attention/kv_transfer_utils/)
- [ mla_attention ](../../api/vllm/model_executor/layers/attention/mla_attention/)
- [ mm_encoder_attention ](../../api/vllm/model_executor/layers/attention/mm_encoder_attention/)
- [ pcp ](../../api/vllm/model_executor/layers/attention/pcp/)
- [ prefill_prefix_lm_attention ](../../api/vllm/model_executor/layers/attention/prefill_prefix_lm_attention/)
- [ rswa_attention ](../../api/vllm/model_executor/layers/attention/rswa_attention/)
- [ sparse_mla_attention ](../../api/vllm/model_executor/layers/attention/sparse_mla_attention/)
- [ sparse_mla_mask ](../../api/vllm/model_executor/layers/attention/sparse_mla_mask/)
- [ static_sink_attention ](../../api/vllm/model_executor/layers/attention/static_sink_attention/)

[ fused_moe ](../../api/vllm/model_executor/layers/fused_moe/)

fused_moe

[ activation ](../../api/vllm/model_executor/layers/fused_moe/activation/)

[ all2all_utils ](../../api/vllm/model_executor/layers/fused_moe/all2all_utils/)

[ config ](../../api/vllm/model_executor/layers/fused_moe/config/)

[ deep_gemm_utils ](../../api/vllm/model_executor/layers/fused_moe/deep_gemm_utils/)

[ eep_reconfigure ](../../api/vllm/model_executor/layers/fused_moe/eep_reconfigure/)

[ expert_map_manager ](../../api/vllm/model_executor/layers/fused_moe/expert_map_manager/)

[ fused_flydsl_moe ](../../api/vllm/model_executor/layers/fused_moe/fused_flydsl_moe/)

[ fused_moe ](../../api/vllm/model_executor/layers/fused_moe/fused_moe/)

[ fused_moe_method_base ](../../api/vllm/model_executor/layers/fused_moe/fused_moe_method_base/)

[ fused_moe_modular_method ](../../api/vllm/model_executor/layers/fused_moe/fused_moe_modular_method/)

[ hpc_moe ](../../api/vllm/model_executor/layers/fused_moe/hpc_moe/)

[ layer ](../../api/vllm/model_executor/layers/fused_moe/layer/)

[ modular_kernel ](../../api/vllm/model_executor/layers/fused_moe/modular_kernel/)

[ moe_align_block_size ](../../api/vllm/model_executor/layers/fused_moe/moe_align_block_size/)

[ moe_fused_mul_sum ](../../api/vllm/model_executor/layers/fused_moe/moe_fused_mul_sum/)

[ moe_output ](../../api/vllm/model_executor/layers/fused_moe/moe_output/)

[ moe_permute_unpermute ](../../api/vllm/model_executor/layers/fused_moe/moe_permute_unpermute/)

[ routed_experts ](../../api/vllm/model_executor/layers/fused_moe/routed_experts/)

[ routed_experts_capturer ](../../api/vllm/model_executor/layers/fused_moe/routed_experts_capturer/)

[ topk_weight_and_reduce ](../../api/vllm/model_executor/layers/fused_moe/topk_weight_and_reduce/)

[ unquantized_fused_moe_method ](../../api/vllm/model_executor/layers/fused_moe/unquantized_fused_moe_method/)

[ utils ](../../api/vllm/model_executor/layers/fused_moe/utils/)

[ experts ](../../api/vllm/model_executor/layers/fused_moe/experts/)

experts

- [ aiter_mxfp4_w4a8_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/aiter_mxfp4_w4a8_moe/)
- [ aiter_mxfp8_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/aiter_mxfp8_moe/)
- [ batched_deep_gemm_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/batched_deep_gemm_moe/)
- [ cpu_int4_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/cpu_int4_moe/)
- [ cpu_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/cpu_moe/)
- [ cutlass_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/cutlass_moe/)
- [ deep_gemm_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/deep_gemm_moe/)
- [ fallback ](../../api/vllm/model_executor/layers/fused_moe/experts/fallback/)
- [ flashinfer_b12x_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/flashinfer_b12x_moe/)
- [ flashinfer_cutedsl_batched_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/flashinfer_cutedsl_batched_moe/)
- [ flashinfer_cutedsl_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/flashinfer_cutedsl_moe/)
- [ flashinfer_cutlass_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/flashinfer_cutlass_moe/)
- [ fused_batched_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/fused_batched_moe/)
- [ fused_humming_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/fused_humming_moe/)
- [ gpt_oss_triton_kernels_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/gpt_oss_triton_kernels_moe/)
- [ int4_emulation_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/int4_emulation_moe/)
- [ lora_context ](../../api/vllm/model_executor/layers/fused_moe/experts/lora_context/)
- [ lora_experts_mixin ](../../api/vllm/model_executor/layers/fused_moe/experts/lora_experts_mixin/)
- [ marlin_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/marlin_moe/)
- [ mxfp8_emulation_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/mxfp8_emulation_moe/)
- [ mxfp8_native_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/mxfp8_native_moe/)
- [ nvfp4_emulation_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/nvfp4_emulation_moe/)
- [ ocp_mx_emulation_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/ocp_mx_emulation_moe/)
- [ rocm_aiter_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/rocm_aiter_moe/)
- [ triton_cutlass_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/triton_cutlass_moe/)
- [ triton_deep_gemm_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/triton_deep_gemm_moe/)
- [ triton_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/triton_moe/)
- [ trtllm_bf16_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/trtllm_bf16_moe/)
- [ trtllm_fp8_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/trtllm_fp8_moe/)
- [ trtllm_lora_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/trtllm_lora_moe/)
- [ trtllm_mxfp4_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/trtllm_mxfp4_moe/)
- [ trtllm_mxint4_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/trtllm_mxint4_moe/)
- [ trtllm_nvfp4_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/trtllm_nvfp4_moe/)
- [ xpu_moe ](../../api/vllm/model_executor/layers/fused_moe/experts/xpu_moe/)

[ oracle ](../../api/vllm/model_executor/layers/fused_moe/oracle/)

oracle

- [ base ](../../api/vllm/model_executor/layers/fused_moe/oracle/base/)
- [ fp8 ](../../api/vllm/model_executor/layers/fused_moe/oracle/fp8/)
- [ int8 ](../../api/vllm/model_executor/layers/fused_moe/oracle/int8/)
- [ int_wna16 ](../../api/vllm/model_executor/layers/fused_moe/oracle/int_wna16/)
- [ mxfp4 ](../../api/vllm/model_executor/layers/fused_moe/oracle/mxfp4/)
- [ mxfp8 ](../../api/vllm/model_executor/layers/fused_moe/oracle/mxfp8/)
- [ nvfp4 ](../../api/vllm/model_executor/layers/fused_moe/oracle/nvfp4/)
- [ unquantized ](../../api/vllm/model_executor/layers/fused_moe/oracle/unquantized/)
- [ w4a8 ](../../api/vllm/model_executor/layers/fused_moe/oracle/w4a8/)
- [ w4a8_int8 ](../../api/vllm/model_executor/layers/fused_moe/oracle/w4a8_int8/)

[ prepare_finalize ](../../api/vllm/model_executor/layers/fused_moe/prepare_finalize/)

prepare_finalize

- [ batched ](../../api/vllm/model_executor/layers/fused_moe/prepare_finalize/batched/)
- [ deepep_ht ](../../api/vllm/model_executor/layers/fused_moe/prepare_finalize/deepep_ht/)
- [ deepep_ll ](../../api/vllm/model_executor/layers/fused_moe/prepare_finalize/deepep_ll/)
- [ deepep_v2 ](../../api/vllm/model_executor/layers/fused_moe/prepare_finalize/deepep_v2/)
- [ flashinfer_nvlink_one_sided ](../../api/vllm/model_executor/layers/fused_moe/prepare_finalize/flashinfer_nvlink_one_sided/)
- [ flashinfer_nvlink_two_sided ](../../api/vllm/model_executor/layers/fused_moe/prepare_finalize/flashinfer_nvlink_two_sided/)
- [ mori ](../../api/vllm/model_executor/layers/fused_moe/prepare_finalize/mori/)
- [ naive_dp_ep ](../../api/vllm/model_executor/layers/fused_moe/prepare_finalize/naive_dp_ep/)
- [ nixl_ep ](../../api/vllm/model_executor/layers/fused_moe/prepare_finalize/nixl_ep/)
- [ no_dp_ep ](../../api/vllm/model_executor/layers/fused_moe/prepare_finalize/no_dp_ep/)

[ router ](../../api/vllm/model_executor/layers/fused_moe/router/)

router

- [ aiter_shared_routed_fused_moe_router ](../../api/vllm/model_executor/layers/fused_moe/router/aiter_shared_routed_fused_moe_router/)
- [ base_router ](../../api/vllm/model_executor/layers/fused_moe/router/base_router/)
- [ bf16x3_router_gemm_cutedsl ](../../api/vllm/model_executor/layers/fused_moe/router/bf16x3_router_gemm_cutedsl/)
- [ custom_routing_router ](../../api/vllm/model_executor/layers/fused_moe/router/custom_routing_router/)
- [ dsv4_topk ](../../api/vllm/model_executor/layers/fused_moe/router/dsv4_topk/)
- [ fused_moe_router ](../../api/vllm/model_executor/layers/fused_moe/router/fused_moe_router/)
- [ fused_topk_bias_router ](../../api/vllm/model_executor/layers/fused_moe/router/fused_topk_bias_router/)
- [ fused_topk_router ](../../api/vllm/model_executor/layers/fused_moe/router/fused_topk_router/)
- [ gate_linear ](../../api/vllm/model_executor/layers/fused_moe/router/gate_linear/)
- [ grouped_topk_router ](../../api/vllm/model_executor/layers/fused_moe/router/grouped_topk_router/)
- [ router_factory ](../../api/vllm/model_executor/layers/fused_moe/router/router_factory/)
- [ routing_simulator_router ](../../api/vllm/model_executor/layers/fused_moe/router/routing_simulator_router/)
- [ zero_expert_router ](../../api/vllm/model_executor/layers/fused_moe/router/zero_expert_router/)

[ runner ](../../api/vllm/model_executor/layers/fused_moe/runner/)

runner

- [ moe_runner ](../../api/vllm/model_executor/layers/fused_moe/runner/moe_runner/)
- [ moe_runner_interface ](../../api/vllm/model_executor/layers/fused_moe/runner/moe_runner_interface/)
- [ shared_experts ](../../api/vllm/model_executor/layers/fused_moe/runner/shared_experts/)

[ fusion ](../../api/vllm/model_executor/layers/fusion/)

fusion

- [ quant_activation ](../../api/vllm/model_executor/layers/fusion/quant_activation/)

[ hpc ](../../api/vllm/model_executor/layers/hpc/)

hpc

- [ hpc_module ](../../api/vllm/model_executor/layers/hpc/hpc_module/)
- [ rope_norm ](../../api/vllm/model_executor/layers/hpc/rope_norm/)

[ mamba ](../../api/vllm/model_executor/layers/mamba/)

mamba

[ abstract ](../../api/vllm/model_executor/layers/mamba/abstract/)

[ mamba_mixer ](../../api/vllm/model_executor/layers/mamba/mamba_mixer/)

[ mamba_mixer2 ](../../api/vllm/model_executor/layers/mamba/mamba_mixer2/)

[ mamba_utils ](../../api/vllm/model_executor/layers/mamba/mamba_utils/)

[ short_conv ](../../api/vllm/model_executor/layers/mamba/short_conv/)

[ gdn ](../../api/vllm/model_executor/layers/mamba/gdn/)

gdn

- [ base ](../../api/vllm/model_executor/layers/mamba/gdn/base/)
- [ kimi_gdn_linear_attn ](../../api/vllm/model_executor/layers/mamba/gdn/kimi_gdn_linear_attn/)
- [ olmo_gdn_linear_attn ](../../api/vllm/model_executor/layers/mamba/gdn/olmo_gdn_linear_attn/)
- [ qwen_gdn_linear_attn ](../../api/vllm/model_executor/layers/mamba/gdn/qwen_gdn_linear_attn/)

[ linear ](../../api/vllm/model_executor/layers/mamba/linear/)

linear

- [ bailing_linear_attn ](../../api/vllm/model_executor/layers/mamba/linear/bailing_linear_attn/)
- [ base ](../../api/vllm/model_executor/layers/mamba/linear/base/)
- [ minimax_linear_attn ](../../api/vllm/model_executor/layers/mamba/linear/minimax_linear_attn/)

[ ops ](../../api/vllm/model_executor/layers/mamba/ops/)

ops

[ causal_conv1d ](../../api/vllm/model_executor/layers/mamba/ops/causal_conv1d/)

[ gather_initial_states ](../../api/vllm/model_executor/layers/mamba/ops/gather_initial_states/)

[ layernorm_gated ](../../api/vllm/model_executor/layers/mamba/ops/layernorm_gated/)

[ mamba_ssm ](../../api/vllm/model_executor/layers/mamba/ops/mamba_ssm/)

[ replayssm_config ](../../api/vllm/model_executor/layers/mamba/ops/replayssm_config/)

[ selective_state_update_replayssm_output_only ](../../api/vllm/model_executor/layers/mamba/ops/selective_state_update_replayssm_output_only/)

[ ssd_bmm ](../../api/vllm/model_executor/layers/mamba/ops/ssd_bmm/)

[ ssd_chunk_scan ](../../api/vllm/model_executor/layers/mamba/ops/ssd_chunk_scan/)

[ ssd_chunk_state ](../../api/vllm/model_executor/layers/mamba/ops/ssd_chunk_state/)

[ ssd_combined ](../../api/vllm/model_executor/layers/mamba/ops/ssd_combined/)

[ ssd_state_passing ](../../api/vllm/model_executor/layers/mamba/ops/ssd_state_passing/)

[ ssu_dispatch ](../../api/vllm/model_executor/layers/mamba/ops/ssu_dispatch/)

[ triton_helpers ](../../api/vllm/model_executor/layers/mamba/ops/triton_helpers/)

[ cpu ](../../api/vllm/model_executor/layers/mamba/ops/cpu/)

cpu

- [ causal_conv1d ](../../api/vllm/model_executor/layers/mamba/ops/cpu/causal_conv1d/)
- [ gdn_attention ](../../api/vllm/model_executor/layers/mamba/ops/cpu/gdn_attention/)
- [ mamba_ssm ](../../api/vllm/model_executor/layers/mamba/ops/cpu/mamba_ssm/)

[ gdn_chunk_cutedsl ](../../api/vllm/model_executor/layers/mamba/ops/gdn_chunk_cutedsl/)

gdn_chunk_cutedsl

- [ kernel_h ](../../api/vllm/model_executor/layers/mamba/ops/gdn_chunk_cutedsl/kernel_h/)
- [ kernel_kkt_inv_uw ](../../api/vllm/model_executor/layers/mamba/ops/gdn_chunk_cutedsl/kernel_kkt_inv_uw/)
- [ kernel_o ](../../api/vllm/model_executor/layers/mamba/ops/gdn_chunk_cutedsl/kernel_o/)

[ minimax_rms_norm ](../../api/vllm/model_executor/layers/minimax_rms_norm/)

minimax_rms_norm

- [ lamport_workspace ](../../api/vllm/model_executor/layers/minimax_rms_norm/lamport_workspace/)
- [ rms_norm_tp ](../../api/vllm/model_executor/layers/minimax_rms_norm/rms_norm_tp/)

[ pooler ](../../api/vllm/model_executor/layers/pooler/)

pooler

[ abstract ](../../api/vllm/model_executor/layers/pooler/abstract/)

[ activations ](../../api/vllm/model_executor/layers/pooler/activations/)

[ common ](../../api/vllm/model_executor/layers/pooler/common/)

[ special ](../../api/vllm/model_executor/layers/pooler/special/)

[ seqwise ](../../api/vllm/model_executor/layers/pooler/seqwise/)

seqwise

- [ heads ](../../api/vllm/model_executor/layers/pooler/seqwise/heads/)
- [ methods ](../../api/vllm/model_executor/layers/pooler/seqwise/methods/)
- [ poolers ](../../api/vllm/model_executor/layers/pooler/seqwise/poolers/)

[ tokwise ](../../api/vllm/model_executor/layers/pooler/tokwise/)

tokwise

- [ heads ](../../api/vllm/model_executor/layers/pooler/tokwise/heads/)
- [ methods ](../../api/vllm/model_executor/layers/pooler/tokwise/methods/)
- [ poolers ](../../api/vllm/model_executor/layers/pooler/tokwise/poolers/)

[ quantization ](../../api/vllm/model_executor/layers/quantization/)

quantization

[ auto_awq ](../../api/vllm/model_executor/layers/quantization/auto_awq/)

[ auto_gptq ](../../api/vllm/model_executor/layers/quantization/auto_gptq/)

[ awq_triton ](../../api/vllm/model_executor/layers/quantization/awq_triton/)

[ base_config ](../../api/vllm/model_executor/layers/quantization/base_config/)

[ experts_int8 ](../../api/vllm/model_executor/layers/quantization/experts_int8/)

[ fbgemm_fp8 ](../../api/vllm/model_executor/layers/quantization/fbgemm_fp8/)

[ fp8 ](../../api/vllm/model_executor/layers/quantization/fp8/)

[ fp_quant ](../../api/vllm/model_executor/layers/quantization/fp_quant/)

[ humming ](../../api/vllm/model_executor/layers/quantization/humming/)

[ input_quant_fp8 ](../../api/vllm/model_executor/layers/quantization/input_quant_fp8/)

[ kv_cache ](../../api/vllm/model_executor/layers/quantization/kv_cache/)

[ modelopt ](../../api/vllm/model_executor/layers/quantization/modelopt/)

[ moe_wna16 ](../../api/vllm/model_executor/layers/quantization/moe_wna16/)

[ mxfp4 ](../../api/vllm/model_executor/layers/quantization/mxfp4/)

[ qutlass_utils ](../../api/vllm/model_executor/layers/quantization/qutlass_utils/)

[ torchao ](../../api/vllm/model_executor/layers/quantization/torchao/)

[ compressed_tensors ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/)

compressed_tensors

[ compressed_tensors ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors/)

[ compressed_tensors_embedding ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors_embedding/)

[ triton_scaled_mm ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/triton_scaled_mm/)

[ utils ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/utils/)

[ compressed_tensors_moe ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors_moe/)

compressed_tensors_moe

- [ compressed_tensors_moe ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors_moe/compressed_tensors_moe/)
- [ compressed_tensors_moe_w4a4_mxfp4 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors_moe/compressed_tensors_moe_w4a4_mxfp4/)
- [ compressed_tensors_moe_w4a4_nvfp4 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors_moe/compressed_tensors_moe_w4a4_nvfp4/)
- [ compressed_tensors_moe_w4a8_fp8 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors_moe/compressed_tensors_moe_w4a8_fp8/)
- [ compressed_tensors_moe_w4a8_int8 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors_moe/compressed_tensors_moe_w4a8_int8/)
- [ compressed_tensors_moe_w4a16_flydsl ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors_moe/compressed_tensors_moe_w4a16_flydsl/)
- [ compressed_tensors_moe_w8a8_fp8 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors_moe/compressed_tensors_moe_w8a8_fp8/)
- [ compressed_tensors_moe_w8a8_int8 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors_moe/compressed_tensors_moe_w8a8_int8/)
- [ compressed_tensors_moe_w8a8_mxfp8 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors_moe/compressed_tensors_moe_w8a8_mxfp8/)
- [ compressed_tensors_moe_wna16 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors_moe/compressed_tensors_moe_wna16/)
- [ compressed_tensors_moe_wna16_rdna3 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors_moe/compressed_tensors_moe_wna16_rdna3/)
- [ rocm_moe_rdna ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/compressed_tensors_moe/rocm_moe_rdna/)

[ schemes ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/schemes/)

schemes

- [ compressed_tensors_scheme ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/schemes/compressed_tensors_scheme/)
- [ compressed_tensors_w4a4_mxfp4 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/schemes/compressed_tensors_w4a4_mxfp4/)
- [ compressed_tensors_w4a4_nvfp4 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/schemes/compressed_tensors_w4a4_nvfp4/)
- [ compressed_tensors_w4a8_fp8 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/schemes/compressed_tensors_w4a8_fp8/)
- [ compressed_tensors_w4a8_int ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/schemes/compressed_tensors_w4a8_int/)
- [ compressed_tensors_w8a8_fp8 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/schemes/compressed_tensors_w8a8_fp8/)
- [ compressed_tensors_w8a8_int8 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/schemes/compressed_tensors_w8a8_int8/)
- [ compressed_tensors_w8a8_mxfp8 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/schemes/compressed_tensors_w8a8_mxfp8/)
- [ compressed_tensors_w8a16_fp8 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/schemes/compressed_tensors_w8a16_fp8/)
- [ compressed_tensors_wNa4 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/schemes/compressed_tensors_wNa4/)
- [ compressed_tensors_wNa8 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/schemes/compressed_tensors_wNa8/)
- [ compressed_tensors_wNa8o8 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/schemes/compressed_tensors_wNa8o8/)
- [ compressed_tensors_wNa16 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/schemes/compressed_tensors_wNa16/)

[ transform ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/transform/)

transform

[ linear ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/transform/linear/)

[ module ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/transform/module/)

[ utils ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/transform/utils/)

[ schemes ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/transform/schemes/)

schemes

- [ linear_qutlass_nvfp4 ](../../api/vllm/model_executor/layers/quantization/compressed_tensors/transform/schemes/linear_qutlass_nvfp4/)

[ inc ](../../api/vllm/model_executor/layers/quantization/inc/)

inc

[ config_parser ](../../api/vllm/model_executor/layers/quantization/inc/config_parser/)

[ inc ](../../api/vllm/model_executor/layers/quantization/inc/inc/)

[ inc_linear ](../../api/vllm/model_executor/layers/quantization/inc/inc_linear/)

[ schemes ](../../api/vllm/model_executor/layers/quantization/inc/schemes/)

schemes

- [ factory ](../../api/vllm/model_executor/layers/quantization/inc/schemes/factory/)
- [ inc_ark_ops ](../../api/vllm/model_executor/layers/quantization/inc/schemes/inc_ark_ops/)
- [ inc_mxfp4_linear ](../../api/vllm/model_executor/layers/quantization/inc/schemes/inc_mxfp4_linear/)
- [ inc_mxfp4_moe ](../../api/vllm/model_executor/layers/quantization/inc/schemes/inc_mxfp4_moe/)
- [ inc_mxfp4_scheme ](../../api/vllm/model_executor/layers/quantization/inc/schemes/inc_mxfp4_scheme/)
- [ inc_mxfp8_linear ](../../api/vllm/model_executor/layers/quantization/inc/schemes/inc_mxfp8_linear/)
- [ inc_mxfp8_scheme ](../../api/vllm/model_executor/layers/quantization/inc/schemes/inc_mxfp8_scheme/)
- [ inc_scheme ](../../api/vllm/model_executor/layers/quantization/inc/schemes/inc_scheme/)
- [ inc_wna16_linear ](../../api/vllm/model_executor/layers/quantization/inc/schemes/inc_wna16_linear/)
- [ inc_wna16_scheme ](../../api/vllm/model_executor/layers/quantization/inc/schemes/inc_wna16_scheme/)

[ online ](../../api/vllm/model_executor/layers/quantization/online/)

online

- [ base ](../../api/vllm/model_executor/layers/quantization/online/base/)
- [ fp8 ](../../api/vllm/model_executor/layers/quantization/online/fp8/)
- [ int8 ](../../api/vllm/model_executor/layers/quantization/online/int8/)
- [ moe_base ](../../api/vllm/model_executor/layers/quantization/online/moe_base/)
- [ mxfp4 ](../../api/vllm/model_executor/layers/quantization/online/mxfp4/)
- [ mxfp8 ](../../api/vllm/model_executor/layers/quantization/online/mxfp8/)
- [ nvfp4 ](../../api/vllm/model_executor/layers/quantization/online/nvfp4/)

[ quark ](../../api/vllm/model_executor/layers/quantization/quark/)

quark

[ quark ](../../api/vllm/model_executor/layers/quantization/quark/quark/)

[ quark_moe ](../../api/vllm/model_executor/layers/quantization/quark/quark_moe/)

[ utils ](../../api/vllm/model_executor/layers/quantization/quark/utils/)

[ schemes ](../../api/vllm/model_executor/layers/quantization/quark/schemes/)

schemes

- [ quark_nvfp4 ](../../api/vllm/model_executor/layers/quantization/quark/schemes/quark_nvfp4/)
- [ quark_ocp_mx ](../../api/vllm/model_executor/layers/quantization/quark/schemes/quark_ocp_mx/)
- [ quark_scheme ](../../api/vllm/model_executor/layers/quantization/quark/schemes/quark_scheme/)
- [ quark_w4a8_mxfp4_fp8 ](../../api/vllm/model_executor/layers/quantization/quark/schemes/quark_w4a8_mxfp4_fp8/)
- [ quark_w8a8_fp8 ](../../api/vllm/model_executor/layers/quantization/quark/schemes/quark_w8a8_fp8/)
- [ quark_w8a8_int8 ](../../api/vllm/model_executor/layers/quantization/quark/schemes/quark_w8a8_int8/)

[ turboquant ](../../api/vllm/model_executor/layers/quantization/turboquant/)

turboquant

- [ centroids ](../../api/vllm/model_executor/layers/quantization/turboquant/centroids/)
- [ config ](../../api/vllm/model_executor/layers/quantization/turboquant/config/)

[ utils ](../../api/vllm/model_executor/layers/quantization/utils/)

utils

- [ allspark_utils ](../../api/vllm/model_executor/layers/quantization/utils/allspark_utils/)
- [ flashinfer_fp4_moe ](../../api/vllm/model_executor/layers/quantization/utils/flashinfer_fp4_moe/)
- [ flashinfer_mxint4_moe ](../../api/vllm/model_executor/layers/quantization/utils/flashinfer_mxint4_moe/)
- [ flashinfer_utils ](../../api/vllm/model_executor/layers/quantization/utils/flashinfer_utils/)
- [ fp8_utils ](../../api/vllm/model_executor/layers/quantization/utils/fp8_utils/)
- [ gptq_utils ](../../api/vllm/model_executor/layers/quantization/utils/gptq_utils/)
- [ humming_utils ](../../api/vllm/model_executor/layers/quantization/utils/humming_utils/)
- [ int8_utils ](../../api/vllm/model_executor/layers/quantization/utils/int8_utils/)
- [ layer_utils ](../../api/vllm/model_executor/layers/quantization/utils/layer_utils/)
- [ machete_utils ](../../api/vllm/model_executor/layers/quantization/utils/machete_utils/)
- [ marlin_utils ](../../api/vllm/model_executor/layers/quantization/utils/marlin_utils/)
- [ marlin_utils_fp4 ](../../api/vllm/model_executor/layers/quantization/utils/marlin_utils_fp4/)
- [ marlin_utils_fp8 ](../../api/vllm/model_executor/layers/quantization/utils/marlin_utils_fp8/)
- [ marlin_utils_test ](../../api/vllm/model_executor/layers/quantization/utils/marlin_utils_test/)
- [ mxfp4_utils ](../../api/vllm/model_executor/layers/quantization/utils/mxfp4_utils/)
- [ mxfp6_utils ](../../api/vllm/model_executor/layers/quantization/utils/mxfp6_utils/)
- [ mxfp8_utils ](../../api/vllm/model_executor/layers/quantization/utils/mxfp8_utils/)
- [ nvfp4_emulation_utils ](../../api/vllm/model_executor/layers/quantization/utils/nvfp4_emulation_utils/)
- [ nvfp4_utils ](../../api/vllm/model_executor/layers/quantization/utils/nvfp4_utils/)
- [ ocp_mx_utils ](../../api/vllm/model_executor/layers/quantization/utils/ocp_mx_utils/)
- [ quant_utils ](../../api/vllm/model_executor/layers/quantization/utils/quant_utils/)
- [ w8a8_utils ](../../api/vllm/model_executor/layers/quantization/utils/w8a8_utils/)

[ rotary_embedding ](../../api/vllm/model_executor/layers/rotary_embedding/)

rotary_embedding

- [ base ](../../api/vllm/model_executor/layers/rotary_embedding/base/)
- [ common ](../../api/vllm/model_executor/layers/rotary_embedding/common/)
- [ deepseek_scaling_rope ](../../api/vllm/model_executor/layers/rotary_embedding/deepseek_scaling_rope/)
- [ dual_chunk_rope ](../../api/vllm/model_executor/layers/rotary_embedding/dual_chunk_rope/)
- [ dynamic_ntk_alpha_rope ](../../api/vllm/model_executor/layers/rotary_embedding/dynamic_ntk_alpha_rope/)
- [ dynamic_ntk_scaling_rope ](../../api/vllm/model_executor/layers/rotary_embedding/dynamic_ntk_scaling_rope/)
- [ ernie45_vl_rope ](../../api/vllm/model_executor/layers/rotary_embedding/ernie45_vl_rope/)
- [ fope ](../../api/vllm/model_executor/layers/rotary_embedding/fope/)
- [ gemma4_rope ](../../api/vllm/model_executor/layers/rotary_embedding/gemma4_rope/)
- [ linear_scaling_rope ](../../api/vllm/model_executor/layers/rotary_embedding/linear_scaling_rope/)
- [ llama3_rope ](../../api/vllm/model_executor/layers/rotary_embedding/llama3_rope/)
- [ llama4_vision_rope ](../../api/vllm/model_executor/layers/rotary_embedding/llama4_vision_rope/)
- [ mrope ](../../api/vllm/model_executor/layers/rotary_embedding/mrope/)
- [ mrope_interleaved ](../../api/vllm/model_executor/layers/rotary_embedding/mrope_interleaved/)
- [ ntk_scaling_rope ](../../api/vllm/model_executor/layers/rotary_embedding/ntk_scaling_rope/)
- [ phi3_long_rope_scaled_rope ](../../api/vllm/model_executor/layers/rotary_embedding/phi3_long_rope_scaled_rope/)
- [ telechat3_scaling_rope ](../../api/vllm/model_executor/layers/rotary_embedding/telechat3_scaling_rope/)
- [ xdrope ](../../api/vllm/model_executor/layers/rotary_embedding/xdrope/)
- [ yarn_scaling_rope ](../../api/vllm/model_executor/layers/rotary_embedding/yarn_scaling_rope/)

[ model_loader ](../../api/vllm/model_executor/model_loader/)

model_loader

[ base_loader ](../../api/vllm/model_executor/model_loader/base_loader/)

[ default_loader ](../../api/vllm/model_executor/model_loader/default_loader/)

[ dummy_loader ](../../api/vllm/model_executor/model_loader/dummy_loader/)

[ ep_weight_filter ](../../api/vllm/model_executor/model_loader/ep_weight_filter/)

[ modelexpress_loader ](../../api/vllm/model_executor/model_loader/modelexpress_loader/)

[ mtp_validation ](../../api/vllm/model_executor/model_loader/mtp_validation/)

[ runai_streamer_loader ](../../api/vllm/model_executor/model_loader/runai_streamer_loader/)

[ sharded_state_loader ](../../api/vllm/model_executor/model_loader/sharded_state_loader/)

[ tensorizer ](../../api/vllm/model_executor/model_loader/tensorizer/)

[ tensorizer_loader ](../../api/vllm/model_executor/model_loader/tensorizer_loader/)

[ utils ](../../api/vllm/model_executor/model_loader/utils/)

[ weight_utils ](../../api/vllm/model_executor/model_loader/weight_utils/)

[ reload ](../../api/vllm/model_executor/model_loader/reload/)

reload

- [ layerwise ](../../api/vllm/model_executor/model_loader/reload/layerwise/)
- [ meta ](../../api/vllm/model_executor/model_loader/reload/meta/)
- [ sanitize ](../../api/vllm/model_executor/model_loader/reload/sanitize/)
- [ torchao_decorator ](../../api/vllm/model_executor/model_loader/reload/torchao_decorator/)
- [ types ](../../api/vllm/model_executor/model_loader/reload/types/)
- [ utils ](../../api/vllm/model_executor/model_loader/reload/utils/)

[ models ](../../api/vllm/model_executor/models/)

models

[ AXK1 ](../../api/vllm/model_executor/models/AXK1/)

[ adapters ](../../api/vllm/model_executor/models/adapters/)

[ afmoe ](../../api/vllm/model_executor/models/afmoe/)

[ aimv2 ](../../api/vllm/model_executor/models/aimv2/)

[ apertus ](../../api/vllm/model_executor/models/apertus/)

[ arcee ](../../api/vllm/model_executor/models/arcee/)

[ arctic ](../../api/vllm/model_executor/models/arctic/)

[ aria ](../../api/vllm/model_executor/models/aria/)

[ audioflamingo3 ](../../api/vllm/model_executor/models/audioflamingo3/)

[ bagel ](../../api/vllm/model_executor/models/bagel/)

[ bailing_moe ](../../api/vllm/model_executor/models/bailing_moe/)

[ bailing_moe_linear ](../../api/vllm/model_executor/models/bailing_moe_linear/)

[ bailing_moe_mtp ](../../api/vllm/model_executor/models/bailing_moe_mtp/)

[ bailing_moe_v3 ](../../api/vllm/model_executor/models/bailing_moe_v3/)

[ bailing_moe_v3_mtp ](../../api/vllm/model_executor/models/bailing_moe_v3_mtp/)

[ bee ](../../api/vllm/model_executor/models/bee/)

[ bert ](../../api/vllm/model_executor/models/bert/)

[ bert_with_rope ](../../api/vllm/model_executor/models/bert_with_rope/)

[ blip ](../../api/vllm/model_executor/models/blip/)

[ blip2 ](../../api/vllm/model_executor/models/blip2/)

[ bloom ](../../api/vllm/model_executor/models/bloom/)

[ chameleon ](../../api/vllm/model_executor/models/chameleon/)

[ chatglm ](../../api/vllm/model_executor/models/chatglm/)

[ cheers ](../../api/vllm/model_executor/models/cheers/)

[ clip ](../../api/vllm/model_executor/models/clip/)

[ cohere2_moe ](../../api/vllm/model_executor/models/cohere2_moe/)

[ cohere2_vision ](../../api/vllm/model_executor/models/cohere2_vision/)

[ cohere_asr ](../../api/vllm/model_executor/models/cohere_asr/)

[ cohere_eagle ](../../api/vllm/model_executor/models/cohere_eagle/)

[ colbert ](../../api/vllm/model_executor/models/colbert/)

[ colmodernvbert ](../../api/vllm/model_executor/models/colmodernvbert/)

[ colpali ](../../api/vllm/model_executor/models/colpali/)

[ colqwen3 ](../../api/vllm/model_executor/models/colqwen3/)

[ colqwen3_5 ](../../api/vllm/model_executor/models/colqwen3_5/)

[ commandr ](../../api/vllm/model_executor/models/commandr/)

[ config ](../../api/vllm/model_executor/models/config/)

[ conformer_encoder ](../../api/vllm/model_executor/models/conformer_encoder/)

[ cosmos3 ](../../api/vllm/model_executor/models/cosmos3/)

[ cosmos3_edge ](../../api/vllm/model_executor/models/cosmos3_edge/)

[ dbrx ](../../api/vllm/model_executor/models/dbrx/)

[ deepencoder ](../../api/vllm/model_executor/models/deepencoder/)

[ deepencoder2 ](../../api/vllm/model_executor/models/deepencoder2/)

[ deepseek_eagle ](../../api/vllm/model_executor/models/deepseek_eagle/)

[ deepseek_eagle3 ](../../api/vllm/model_executor/models/deepseek_eagle3/)

[ deepseek_mtp ](../../api/vllm/model_executor/models/deepseek_mtp/)

[ deepseek_ocr ](../../api/vllm/model_executor/models/deepseek_ocr/)

[ deepseek_ocr2 ](../../api/vllm/model_executor/models/deepseek_ocr2/)

[ deepseek_v2 ](../../api/vllm/model_executor/models/deepseek_v2/)

[ deepseek_vl2 ](../../api/vllm/model_executor/models/deepseek_vl2/)

[ diffusion_gemma ](../../api/vllm/model_executor/models/diffusion_gemma/)

[ dots_ocr ](../../api/vllm/model_executor/models/dots_ocr/)

[ eagle2_5_vl ](../../api/vllm/model_executor/models/eagle2_5_vl/)

[ ernie45 ](../../api/vllm/model_executor/models/ernie45/)

[ ernie45_moe ](../../api/vllm/model_executor/models/ernie45_moe/)

[ ernie45_vl ](../../api/vllm/model_executor/models/ernie45_vl/)

[ ernie45_vl_moe ](../../api/vllm/model_executor/models/ernie45_vl_moe/)

[ ernie_mtp ](../../api/vllm/model_executor/models/ernie_mtp/)

[ exaone ](../../api/vllm/model_executor/models/exaone/)

[ exaone4 ](../../api/vllm/model_executor/models/exaone4/)

[ exaone4_5 ](../../api/vllm/model_executor/models/exaone4_5/)

[ exaone4_5_mtp ](../../api/vllm/model_executor/models/exaone4_5_mtp/)

[ exaone_moe ](../../api/vllm/model_executor/models/exaone_moe/)

[ exaone_moe_mtp ](../../api/vllm/model_executor/models/exaone_moe_mtp/)

[ extract_hidden_states ](../../api/vllm/model_executor/models/extract_hidden_states/)

[ fairseq2_llama ](../../api/vllm/model_executor/models/fairseq2_llama/)

[ falcon ](../../api/vllm/model_executor/models/falcon/)

[ falcon_h1 ](../../api/vllm/model_executor/models/falcon_h1/)

[ fireredasr2 ](../../api/vllm/model_executor/models/fireredasr2/)

[ fireredlid ](../../api/vllm/model_executor/models/fireredlid/)

[ flex_olmo ](../../api/vllm/model_executor/models/flex_olmo/)

[ funasr ](../../api/vllm/model_executor/models/funasr/)

[ funaudiochat ](../../api/vllm/model_executor/models/funaudiochat/)

[ gemma ](../../api/vllm/model_executor/models/gemma/)

[ gemma2 ](../../api/vllm/model_executor/models/gemma2/)

[ gemma3 ](../../api/vllm/model_executor/models/gemma3/)

[ gemma3_mm ](../../api/vllm/model_executor/models/gemma3_mm/)

[ gemma3n ](../../api/vllm/model_executor/models/gemma3n/)

[ gemma3n_audio_utils ](../../api/vllm/model_executor/models/gemma3n_audio_utils/)

[ gemma3n_mm ](../../api/vllm/model_executor/models/gemma3n_mm/)

[ gemma4 ](../../api/vllm/model_executor/models/gemma4/)

[ gemma4_dspark ](../../api/vllm/model_executor/models/gemma4_dspark/)

[ gemma4_mm ](../../api/vllm/model_executor/models/gemma4_mm/)

[ gemma4_mtp ](../../api/vllm/model_executor/models/gemma4_mtp/)

[ gemma4_unified ](../../api/vllm/model_executor/models/gemma4_unified/)

[ glm ](../../api/vllm/model_executor/models/glm/)

[ glm4 ](../../api/vllm/model_executor/models/glm4/)

[ glm4_1v ](../../api/vllm/model_executor/models/glm4_1v/)

[ glm4_moe ](../../api/vllm/model_executor/models/glm4_moe/)

[ glm4_moe_lite ](../../api/vllm/model_executor/models/glm4_moe_lite/)

[ glm4_moe_lite_mtp ](../../api/vllm/model_executor/models/glm4_moe_lite_mtp/)

[ glm4_moe_mtp ](../../api/vllm/model_executor/models/glm4_moe_mtp/)

[ glm4v ](../../api/vllm/model_executor/models/glm4v/)

[ glm_ocr ](../../api/vllm/model_executor/models/glm_ocr/)

[ glm_ocr_mtp ](../../api/vllm/model_executor/models/glm_ocr_mtp/)

[ glmasr ](../../api/vllm/model_executor/models/glmasr/)

[ glmasr_utils ](../../api/vllm/model_executor/models/glmasr_utils/)

[ gpt2 ](../../api/vllm/model_executor/models/gpt2/)

[ gpt_j ](../../api/vllm/model_executor/models/gpt_j/)

[ gpt_neox ](../../api/vllm/model_executor/models/gpt_neox/)

[ gpt_oss ](../../api/vllm/model_executor/models/gpt_oss/)

[ granite ](../../api/vllm/model_executor/models/granite/)

[ granite4_vision ](../../api/vllm/model_executor/models/granite4_vision/)

[ granite_speech ](../../api/vllm/model_executor/models/granite_speech/)

[ granite_speech_plus ](../../api/vllm/model_executor/models/granite_speech_plus/)

[ granitemoe ](../../api/vllm/model_executor/models/granitemoe/)

[ granitemoehybrid ](../../api/vllm/model_executor/models/granitemoehybrid/)

[ granitemoeshared ](../../api/vllm/model_executor/models/granitemoeshared/)

[ gritlm ](../../api/vllm/model_executor/models/gritlm/)

[ h2ovl ](../../api/vllm/model_executor/models/h2ovl/)

[ hrm_text ](../../api/vllm/model_executor/models/hrm_text/)

[ hunyuan_v1 ](../../api/vllm/model_executor/models/hunyuan_v1/)

[ hunyuan_vision ](../../api/vllm/model_executor/models/hunyuan_vision/)

[ hy_v3 ](../../api/vllm/model_executor/models/hy_v3/)

[ hy_v3_mtp ](../../api/vllm/model_executor/models/hy_v3_mtp/)

[ hyperclovax ](../../api/vllm/model_executor/models/hyperclovax/)

[ hyperclovax_vision ](../../api/vllm/model_executor/models/hyperclovax_vision/)

[ hyperclovax_vision_v2 ](../../api/vllm/model_executor/models/hyperclovax_vision_v2/)

[ idefics2_vision_model ](../../api/vllm/model_executor/models/idefics2_vision_model/)

[ idefics3 ](../../api/vllm/model_executor/models/idefics3/)

[ interfaces ](../../api/vllm/model_executor/models/interfaces/)

[ interfaces_base ](../../api/vllm/model_executor/models/interfaces_base/)

[ intern_vit ](../../api/vllm/model_executor/models/intern_vit/)

[ internlm2 ](../../api/vllm/model_executor/models/internlm2/)

[ interns1 ](../../api/vllm/model_executor/models/interns1/)

[ interns1_pro ](../../api/vllm/model_executor/models/interns1_pro/)

[ interns1_vit ](../../api/vllm/model_executor/models/interns1_vit/)

[ interns2_mobius ](../../api/vllm/model_executor/models/interns2_mobius/)

[ interns2_preview ](../../api/vllm/model_executor/models/interns2_preview/)

[ internvl ](../../api/vllm/model_executor/models/internvl/)

[ iquest_loopcoder ](../../api/vllm/model_executor/models/iquest_loopcoder/)

[ isaac ](../../api/vllm/model_executor/models/isaac/)

[ jais2 ](../../api/vllm/model_executor/models/jais2/)

[ jamba ](../../api/vllm/model_executor/models/jamba/)

[ jina ](../../api/vllm/model_executor/models/jina/)

[ jina_vl ](../../api/vllm/model_executor/models/jina_vl/)

[ kanana_v ](../../api/vllm/model_executor/models/kanana_v/)

[ keye ](../../api/vllm/model_executor/models/keye/)

[ keye_vl1_5 ](../../api/vllm/model_executor/models/keye_vl1_5/)

[ kimi_audio ](../../api/vllm/model_executor/models/kimi_audio/)

[ kimi_k25 ](../../api/vllm/model_executor/models/kimi_k25/)

[ kimi_k25_vit ](../../api/vllm/model_executor/models/kimi_k25_vit/)

[ kimi_vl ](../../api/vllm/model_executor/models/kimi_vl/)

[ laguna ](../../api/vllm/model_executor/models/laguna/)

[ laguna_dflash ](../../api/vllm/model_executor/models/laguna_dflash/)

[ lfm2 ](../../api/vllm/model_executor/models/lfm2/)

[ lfm2_moe ](../../api/vllm/model_executor/models/lfm2_moe/)

[ lfm2_siglip2 ](../../api/vllm/model_executor/models/lfm2_siglip2/)

[ lfm2_vl ](../../api/vllm/model_executor/models/lfm2_vl/)

[ lightonocr ](../../api/vllm/model_executor/models/lightonocr/)

[ llama ](../../api/vllm/model_executor/models/llama/)

[ llama4 ](../../api/vllm/model_executor/models/llama4/)

[ llama4_eagle ](../../api/vllm/model_executor/models/llama4_eagle/)

[ llama_eagle ](../../api/vllm/model_executor/models/llama_eagle/)

[ llama_eagle3 ](../../api/vllm/model_executor/models/llama_eagle3/)

[ llava ](../../api/vllm/model_executor/models/llava/)

[ llava_next ](../../api/vllm/model_executor/models/llava_next/)

[ llava_next_video ](../../api/vllm/model_executor/models/llava_next_video/)

[ llava_onevision ](../../api/vllm/model_executor/models/llava_onevision/)

[ llava_onevision2 ](../../api/vllm/model_executor/models/llava_onevision2/)

[ longcat_flash ](../../api/vllm/model_executor/models/longcat_flash/)

[ longcat_flash_mtp ](../../api/vllm/model_executor/models/longcat_flash_mtp/)

[ longcat_flash_ngram ](../../api/vllm/model_executor/models/longcat_flash_ngram/)

[ mamba ](../../api/vllm/model_executor/models/mamba/)

[ mamba2 ](../../api/vllm/model_executor/models/mamba2/)

[ medusa ](../../api/vllm/model_executor/models/medusa/)

[ mellum ](../../api/vllm/model_executor/models/mellum/)

[ midashenglm ](../../api/vllm/model_executor/models/midashenglm/)

[ mimo ](../../api/vllm/model_executor/models/mimo/)

[ mimo_audio ](../../api/vllm/model_executor/models/mimo_audio/)

[ mimo_mtp ](../../api/vllm/model_executor/models/mimo_mtp/)

[ mimo_v2 ](../../api/vllm/model_executor/models/mimo_v2/)

[ mimo_v2_mtp ](../../api/vllm/model_executor/models/mimo_v2_mtp/)

[ mimo_v2_omni ](../../api/vllm/model_executor/models/mimo_v2_omni/)

[ minicpm ](../../api/vllm/model_executor/models/minicpm/)

[ minicpm3 ](../../api/vllm/model_executor/models/minicpm3/)

[ minicpm_eagle ](../../api/vllm/model_executor/models/minicpm_eagle/)

[ minicpmo ](../../api/vllm/model_executor/models/minicpmo/)

[ minicpmv ](../../api/vllm/model_executor/models/minicpmv/)

[ minicpmv4_6 ](../../api/vllm/model_executor/models/minicpmv4_6/)

[ minimax_m2 ](../../api/vllm/model_executor/models/minimax_m2/)

[ mistral ](../../api/vllm/model_executor/models/mistral/)

[ mistral3 ](../../api/vllm/model_executor/models/mistral3/)

[ mistral_eagle ](../../api/vllm/model_executor/models/mistral_eagle/)

[ mistral_large_3 ](../../api/vllm/model_executor/models/mistral_large_3/)

[ mistral_large_3_eagle ](../../api/vllm/model_executor/models/mistral_large_3_eagle/)

[ mixtral ](../../api/vllm/model_executor/models/mixtral/)

[ mllama4 ](../../api/vllm/model_executor/models/mllama4/)

[ mlp_speculator ](../../api/vllm/model_executor/models/mlp_speculator/)

[ modernbert ](../../api/vllm/model_executor/models/modernbert/)

[ module_mapping ](../../api/vllm/model_executor/models/module_mapping/)

[ molmo ](../../api/vllm/model_executor/models/molmo/)

[ molmo2 ](../../api/vllm/model_executor/models/molmo2/)

[ moondream3 ](../../api/vllm/model_executor/models/moondream3/)

[ moonvit ](../../api/vllm/model_executor/models/moonvit/)

[ moss_audio ](../../api/vllm/model_executor/models/moss_audio/)

[ moss_transcribe_diarize ](../../api/vllm/model_executor/models/moss_transcribe_diarize/)

[ mpt ](../../api/vllm/model_executor/models/mpt/)

[ muse_glimmer ](../../api/vllm/model_executor/models/muse_glimmer/)

[ nano_nemotron_vl ](../../api/vllm/model_executor/models/nano_nemotron_vl/)

[ nemotron ](../../api/vllm/model_executor/models/nemotron/)

[ nemotron_h ](../../api/vllm/model_executor/models/nemotron_h/)

[ nemotron_h_mtp ](../../api/vllm/model_executor/models/nemotron_h_mtp/)

[ nemotron_nas ](../../api/vllm/model_executor/models/nemotron_nas/)

[ nemotron_parse ](../../api/vllm/model_executor/models/nemotron_parse/)

[ nemotron_vl ](../../api/vllm/model_executor/models/nemotron_vl/)

[ nvlm_d ](../../api/vllm/model_executor/models/nvlm_d/)

[ olmo3 ](../../api/vllm/model_executor/models/olmo3/)

[ olmo_hybrid ](../../api/vllm/model_executor/models/olmo_hybrid/)

[ olmoe ](../../api/vllm/model_executor/models/olmoe/)

[ openai_privacy_filter ](../../api/vllm/model_executor/models/openai_privacy_filter/)

[ opencua ](../../api/vllm/model_executor/models/opencua/)

[ openpangu ](../../api/vllm/model_executor/models/openpangu/)

[ openpangu_mtp ](../../api/vllm/model_executor/models/openpangu_mtp/)

[ openpangu_vl ](../../api/vllm/model_executor/models/openpangu_vl/)

[ openvla ](../../api/vllm/model_executor/models/openvla/)

[ opt ](../../api/vllm/model_executor/models/opt/)

[ orion ](../../api/vllm/model_executor/models/orion/)

[ ovis ](../../api/vllm/model_executor/models/ovis/)

[ ovis2_5 ](../../api/vllm/model_executor/models/ovis2_5/)

[ paddleocr_vl ](../../api/vllm/model_executor/models/paddleocr_vl/)

[ paligemma ](../../api/vllm/model_executor/models/paligemma/)

[ parakeet ](../../api/vllm/model_executor/models/parakeet/)

[ param2moe ](../../api/vllm/model_executor/models/param2moe/)

[ phi ](../../api/vllm/model_executor/models/phi/)

[ phi3 ](../../api/vllm/model_executor/models/phi3/)

[ phi3v ](../../api/vllm/model_executor/models/phi3v/)

[ phi4mm ](../../api/vllm/model_executor/models/phi4mm/)

[ phi4mm_audio ](../../api/vllm/model_executor/models/phi4mm_audio/)

[ phi4mm_utils ](../../api/vllm/model_executor/models/phi4mm_utils/)

[ phi4siglip ](../../api/vllm/model_executor/models/phi4siglip/)

[ phimoe ](../../api/vllm/model_executor/models/phimoe/)

[ pixtral ](../../api/vllm/model_executor/models/pixtral/)

[ plamo3 ](../../api/vllm/model_executor/models/plamo3/)

[ qianfan_ocr ](../../api/vllm/model_executor/models/qianfan_ocr/)

[ qwen2 ](../../api/vllm/model_executor/models/qwen2/)

[ qwen2_5_omni_thinker ](../../api/vllm/model_executor/models/qwen2_5_omni_thinker/)

[ qwen2_5_vl ](../../api/vllm/model_executor/models/qwen2_5_vl/)

[ qwen2_audio ](../../api/vllm/model_executor/models/qwen2_audio/)

[ qwen2_moe ](../../api/vllm/model_executor/models/qwen2_moe/)

[ qwen2_rm ](../../api/vllm/model_executor/models/qwen2_rm/)

[ qwen2_vl ](../../api/vllm/model_executor/models/qwen2_vl/)

[ qwen3 ](../../api/vllm/model_executor/models/qwen3/)

[ qwen3_5 ](../../api/vllm/model_executor/models/qwen3_5/)

[ qwen3_5_mtp ](../../api/vllm/model_executor/models/qwen3_5_mtp/)

[ qwen3_asr ](../../api/vllm/model_executor/models/qwen3_asr/)

[ qwen3_asr_forced_aligner ](../../api/vllm/model_executor/models/qwen3_asr_forced_aligner/)

[ qwen3_asr_realtime ](../../api/vllm/model_executor/models/qwen3_asr_realtime/)

[ qwen3_dflash ](../../api/vllm/model_executor/models/qwen3_dflash/)

[ qwen3_dflash2 ](../../api/vllm/model_executor/models/qwen3_dflash2/)

[ qwen3_dspark ](../../api/vllm/model_executor/models/qwen3_dspark/)

[ qwen3_eagle3 ](../../api/vllm/model_executor/models/qwen3_eagle3/)

[ qwen3_moe ](../../api/vllm/model_executor/models/qwen3_moe/)

[ qwen3_next ](../../api/vllm/model_executor/models/qwen3_next/)

[ qwen3_next_mtp ](../../api/vllm/model_executor/models/qwen3_next_mtp/)

[ qwen3_omni_moe_thinker ](../../api/vllm/model_executor/models/qwen3_omni_moe_thinker/)

[ qwen3_vl ](../../api/vllm/model_executor/models/qwen3_vl/)

[ qwen3_vl_moe ](../../api/vllm/model_executor/models/qwen3_vl_moe/)

[ radio ](../../api/vllm/model_executor/models/radio/)

[ registry ](../../api/vllm/model_executor/models/registry/)

[ rnj1 ](../../api/vllm/model_executor/models/rnj1/)

[ roberta ](../../api/vllm/model_executor/models/roberta/)

[ rvl ](../../api/vllm/model_executor/models/rvl/)

[ sarvam ](../../api/vllm/model_executor/models/sarvam/)

[ seed_oss ](../../api/vllm/model_executor/models/seed_oss/)

[ siglip ](../../api/vllm/model_executor/models/siglip/)

[ siglip2navit ](../../api/vllm/model_executor/models/siglip2navit/)

[ skyworkr1v ](../../api/vllm/model_executor/models/skyworkr1v/)

[ smolvlm ](../../api/vllm/model_executor/models/smolvlm/)

[ solar ](../../api/vllm/model_executor/models/solar/)

[ stablelm ](../../api/vllm/model_executor/models/stablelm/)

[ step1 ](../../api/vllm/model_executor/models/step1/)

[ step3_text ](../../api/vllm/model_executor/models/step3_text/)

[ step3_vl ](../../api/vllm/model_executor/models/step3_vl/)

[ step3p5 ](../../api/vllm/model_executor/models/step3p5/)

[ step3p5_mtp ](../../api/vllm/model_executor/models/step3p5_mtp/)

[ step3p7 ](../../api/vllm/model_executor/models/step3p7/)

[ step_vl ](../../api/vllm/model_executor/models/step_vl/)

[ telechat2 ](../../api/vllm/model_executor/models/telechat2/)

[ teleflm ](../../api/vllm/model_executor/models/teleflm/)

[ terratorch ](../../api/vllm/model_executor/models/terratorch/)

[ ultravox ](../../api/vllm/model_executor/models/ultravox/)

[ unlimited_ocr ](../../api/vllm/model_executor/models/unlimited_ocr/)

[ utils ](../../api/vllm/model_executor/models/utils/)

[ vision ](../../api/vllm/model_executor/models/vision/)

[ voxtral ](../../api/vllm/model_executor/models/voxtral/)

[ voxtral_realtime ](../../api/vllm/model_executor/models/voxtral_realtime/)

[ voyage ](../../api/vllm/model_executor/models/voyage/)

[ whisper ](../../api/vllm/model_executor/models/whisper/)

[ whisper_causal ](../../api/vllm/model_executor/models/whisper_causal/)

[ whisper_utils ](../../api/vllm/model_executor/models/whisper_utils/)

[ zamba2 ](../../api/vllm/model_executor/models/zamba2/)

[ transformers ](../../api/vllm/model_executor/models/transformers/)

transformers

[ base ](../../api/vllm/model_executor/models/transformers/base/)

[ causal ](../../api/vllm/model_executor/models/transformers/causal/)

[ fuser ](../../api/vllm/model_executor/models/transformers/fuser/)

[ fx_utils ](../../api/vllm/model_executor/models/transformers/fx_utils/)

[ layers ](../../api/vllm/model_executor/models/transformers/layers/)

[ legacy ](../../api/vllm/model_executor/models/transformers/legacy/)

[ moe ](../../api/vllm/model_executor/models/transformers/moe/)

[ multimodal ](../../api/vllm/model_executor/models/transformers/multimodal/)

[ pooling ](../../api/vllm/model_executor/models/transformers/pooling/)

[ utils ](../../api/vllm/model_executor/models/transformers/utils/)

[ fusers ](../../api/vllm/model_executor/models/transformers/fusers/)

fusers

- [ base ](../../api/vllm/model_executor/models/transformers/fusers/base/)
- [ glu ](../../api/vllm/model_executor/models/transformers/fusers/glu/)
- [ mla ](../../api/vllm/model_executor/models/transformers/fusers/mla/)
- [ moe ](../../api/vllm/model_executor/models/transformers/fusers/moe/)
- [ packed_qkv ](../../api/vllm/model_executor/models/transformers/fusers/packed_qkv/)
- [ qkv ](../../api/vllm/model_executor/models/transformers/fusers/qkv/)
- [ rms_norm ](../../api/vllm/model_executor/models/transformers/fusers/rms_norm/)

[ offloader ](../../api/vllm/model_executor/offloader/)

offloader

- [ base ](../../api/vllm/model_executor/offloader/base/)
- [ prefetch ](../../api/vllm/model_executor/offloader/prefetch/)
- [ prefetch_ops ](../../api/vllm/model_executor/offloader/prefetch_ops/)
- [ uva ](../../api/vllm/model_executor/offloader/uva/)

[ warmup ](../../api/vllm/model_executor/warmup/)

warmup

- [ b12x_warmup ](../../api/vllm/model_executor/warmup/b12x_warmup/)
- [ cutedsl_warmup ](../../api/vllm/model_executor/warmup/cutedsl_warmup/)
- [ deep_gemm_warmup ](../../api/vllm/model_executor/warmup/deep_gemm_warmup/)
- [ deepseek_v4_mhc_warmup ](../../api/vllm/model_executor/warmup/deepseek_v4_mhc_warmup/)
- [ fa4_cutedsl_warmup ](../../api/vllm/model_executor/warmup/fa4_cutedsl_warmup/)
- [ flashinfer_autotune_cache ](../../api/vllm/model_executor/warmup/flashinfer_autotune_cache/)
- [ flashinfer_sparse_mla_warmup ](../../api/vllm/model_executor/warmup/flashinfer_sparse_mla_warmup/)
- [ jit_warmup ](../../api/vllm/model_executor/warmup/jit_warmup/)
- [ jit_warmup_triton_helper ](../../api/vllm/model_executor/warmup/jit_warmup_triton_helper/)
- [ kernel_warmup ](../../api/vllm/model_executor/warmup/kernel_warmup/)
- [ kimi_k3_triton_warmup ](../../api/vllm/model_executor/warmup/kimi_k3_triton_warmup/)
- [ minimax_m3_msa_warmup ](../../api/vllm/model_executor/warmup/minimax_m3_msa_warmup/)
- [ qwen_triton_warmup ](../../api/vllm/model_executor/warmup/qwen_triton_warmup/)
- [ sparse_mla_triton_warmup ](../../api/vllm/model_executor/warmup/sparse_mla_triton_warmup/)
- [ v1_block_table_warmup ](../../api/vllm/model_executor/warmup/v1_block_table_warmup/)

[ models ](../../api/vllm/models/)

models

[ common ](../../api/vllm/models/common/)

common

[ ops ](../../api/vllm/models/common/ops/)

ops

- [ fused_allreduce_rms_norm ](../../api/vllm/models/common/ops/fused_allreduce_rms_norm/)
- [ fused_qk_rmsnorm ](../../api/vllm/models/common/ops/fused_qk_rmsnorm/)
- [ sequence_parallel ](../../api/vllm/models/common/ops/sequence_parallel/)

[ deepseek_v4 ](../../api/vllm/models/deepseek_v4/)

deepseek_v4

[ attention ](../../api/vllm/models/deepseek_v4/attention/)

[ compressor ](../../api/vllm/models/deepseek_v4/compressor/)

[ eager_scratch ](../../api/vllm/models/deepseek_v4/eager_scratch/)

[ quant_config ](../../api/vllm/models/deepseek_v4/quant_config/)

[ sparse_mla ](../../api/vllm/models/deepseek_v4/sparse_mla/)

[ amd ](../../api/vllm/models/deepseek_v4/amd/)

amd

- [ dspark ](../../api/vllm/models/deepseek_v4/amd/dspark/)
- [ model ](../../api/vllm/models/deepseek_v4/amd/model/)
- [ mtp ](../../api/vllm/models/deepseek_v4/amd/mtp/)
- [ rocm ](../../api/vllm/models/deepseek_v4/amd/rocm/)

[ common ](../../api/vllm/models/deepseek_v4/common/)

common

[ rope ](../../api/vllm/models/deepseek_v4/common/rope/)

[ ops ](../../api/vllm/models/deepseek_v4/common/ops/)

ops

- [ cache_utils ](../../api/vllm/models/deepseek_v4/common/ops/cache_utils/)
- [ fused_compress_quant_cache ](../../api/vllm/models/deepseek_v4/common/ops/fused_compress_quant_cache/)
- [ fused_indexer_q ](../../api/vllm/models/deepseek_v4/common/ops/fused_indexer_q/)
- [ fused_inv_rope_fp8_quant ](../../api/vllm/models/deepseek_v4/common/ops/fused_inv_rope_fp8_quant/)
- [ fused_mtp_input_rmsnorm ](../../api/vllm/models/deepseek_v4/common/ops/fused_mtp_input_rmsnorm/)
- [ save_partial_states ](../../api/vllm/models/deepseek_v4/common/ops/save_partial_states/)

[ nvidia ](../../api/vllm/models/deepseek_v4/nvidia/)

nvidia

[ dspark ](../../api/vllm/models/deepseek_v4/nvidia/dspark/)

[ flashinfer_sparse ](../../api/vllm/models/deepseek_v4/nvidia/flashinfer_sparse/)

[ flashmla ](../../api/vllm/models/deepseek_v4/nvidia/flashmla/)

[ model ](../../api/vllm/models/deepseek_v4/nvidia/model/)

[ mtp ](../../api/vllm/models/deepseek_v4/nvidia/mtp/)

[ ops ](../../api/vllm/models/deepseek_v4/nvidia/ops/)

ops

- [ dequant_gather_k_cutedsl ](../../api/vllm/models/deepseek_v4/nvidia/ops/dequant_gather_k_cutedsl/)
- [ fused_indexer_q_cutedsl ](../../api/vllm/models/deepseek_v4/nvidia/ops/fused_indexer_q_cutedsl/)
- [ o_proj ](../../api/vllm/models/deepseek_v4/nvidia/ops/o_proj/)
- [ prepare_megamoe ](../../api/vllm/models/deepseek_v4/nvidia/ops/prepare_megamoe/)
- [ sparse_attn_compress_cutedsl ](../../api/vllm/models/deepseek_v4/nvidia/ops/sparse_attn_compress_cutedsl/)

[ xpu ](../../api/vllm/models/deepseek_v4/xpu/)

xpu

- [ dspark ](../../api/vllm/models/deepseek_v4/xpu/dspark/)
- [ model ](../../api/vllm/models/deepseek_v4/xpu/model/)
- [ mtp ](../../api/vllm/models/deepseek_v4/xpu/mtp/)
- [ xpu_qnorm_rope_kv_fp8_insert ](../../api/vllm/models/deepseek_v4/xpu/xpu_qnorm_rope_kv_fp8_insert/)
- [ xpu_sparse ](../../api/vllm/models/deepseek_v4/xpu/xpu_sparse/)
- [ xpu_sparse_decode_fp8 ](../../api/vllm/models/deepseek_v4/xpu/xpu_sparse_decode_fp8/)

[ deepseek_v32 ](../../api/vllm/models/deepseek_v32/)

deepseek_v32

[ attention ](../../api/vllm/models/deepseek_v32/attention/)

[ amd ](../../api/vllm/models/deepseek_v32/amd/)

amd

- [ model ](../../api/vllm/models/deepseek_v32/amd/model/)
- [ mtp ](../../api/vllm/models/deepseek_v32/amd/mtp/)
- [ rocm ](../../api/vllm/models/deepseek_v32/amd/rocm/)

[ common ](../../api/vllm/models/deepseek_v32/common/)

common

- [ kernels ](../../api/vllm/models/deepseek_v32/common/kernels/)

[ nvidia ](../../api/vllm/models/deepseek_v32/nvidia/)

nvidia

[ glm52_low_latency_gemm ](../../api/vllm/models/deepseek_v32/nvidia/glm52_low_latency_gemm/)

[ model ](../../api/vllm/models/deepseek_v32/nvidia/model/)

[ mtp ](../../api/vllm/models/deepseek_v32/nvidia/mtp/)

[ ops ](../../api/vllm/models/deepseek_v32/nvidia/ops/)

ops

- [ fused_q_cutedsl ](../../api/vllm/models/deepseek_v32/nvidia/ops/fused_q_cutedsl/)

[ dots3_note ](../../api/vllm/models/dots3_note/)

dots3_note

[ common ](../../api/vllm/models/dots3_note/common/)

common

- [ processor ](../../api/vllm/models/dots3_note/common/processor/)
- [ video ](../../api/vllm/models/dots3_note/common/video/)

[ nvidia ](../../api/vllm/models/dots3_note/nvidia/)

nvidia

- [ attention ](../../api/vllm/models/dots3_note/nvidia/attention/)
- [ audio ](../../api/vllm/models/dots3_note/nvidia/audio/)
- [ audio_encoder ](../../api/vllm/models/dots3_note/nvidia/audio_encoder/)
- [ model ](../../api/vllm/models/dots3_note/nvidia/model/)
- [ mtp ](../../api/vllm/models/dots3_note/nvidia/mtp/)
- [ multimodal ](../../api/vllm/models/dots3_note/nvidia/multimodal/)
- [ vision ](../../api/vllm/models/dots3_note/nvidia/vision/)
- [ vision_attention ](../../api/vllm/models/dots3_note/nvidia/vision_attention/)
- [ vision_moe ](../../api/vllm/models/dots3_note/nvidia/vision_moe/)

[ inkling ](../../api/vllm/models/inkling/)

inkling

[ configs ](../../api/vllm/models/inkling/configs/)

[ amd ](../../api/vllm/models/inkling/amd/)

amd

[ attention ](../../api/vllm/models/inkling/amd/attention/)

[ layernorm ](../../api/vllm/models/inkling/amd/layernorm/)

[ logits_processor ](../../api/vllm/models/inkling/amd/logits_processor/)

[ mlp ](../../api/vllm/models/inkling/amd/mlp/)

[ model ](../../api/vllm/models/inkling/amd/model/)

[ moe ](../../api/vllm/models/inkling/amd/moe/)

[ mtp ](../../api/vllm/models/inkling/amd/mtp/)

[ sconv_swa_attn ](../../api/vllm/models/inkling/amd/sconv_swa_attn/)

[ short_conv ](../../api/vllm/models/inkling/amd/short_conv/)

[ ops ](../../api/vllm/models/inkling/amd/ops/)

ops

[ fa4_rel_attention ](../../api/vllm/models/inkling/amd/ops/fa4_rel_attention/)

[ fa4_warmup ](../../api/vllm/models/inkling/amd/ops/fa4_warmup/)

[ lamport ](../../api/vllm/models/inkling/amd/ops/lamport/)

[ mm_towers ](../../api/vllm/models/inkling/amd/ops/mm_towers/)

[ norm ](../../api/vllm/models/inkling/amd/ops/norm/)

[ qkvr_prep ](../../api/vllm/models/inkling/amd/ops/qkvr_prep/)

[ rel_attention_decode ](../../api/vllm/models/inkling/amd/ops/rel_attention_decode/)

[ sconv ](../../api/vllm/models/inkling/amd/ops/sconv/)

[ silu_and_mul ](../../api/vllm/models/inkling/amd/ops/silu_and_mul/)

[ gluon ](../../api/vllm/models/inkling/amd/ops/gluon/)

gluon

- [ rel_mha_decode_gfx950 ](../../api/vllm/models/inkling/amd/ops/gluon/rel_mha_decode_gfx950/)
- [ rel_mha_extend_gfx950 ](../../api/vllm/models/inkling/amd/ops/gluon/rel_mha_extend_gfx950/)
- [ utils ](../../api/vllm/models/inkling/amd/ops/gluon/utils/)

[ common ](../../api/vllm/models/inkling/common/)

common

- [ mm_preprocess ](../../api/vllm/models/inkling/common/mm_preprocess/)
- [ towers ](../../api/vllm/models/inkling/common/towers/)

[ nvidia ](../../api/vllm/models/inkling/nvidia/)

nvidia

[ attention ](../../api/vllm/models/inkling/nvidia/attention/)

[ layernorm ](../../api/vllm/models/inkling/nvidia/layernorm/)

[ logits_processor ](../../api/vllm/models/inkling/nvidia/logits_processor/)

[ mlp ](../../api/vllm/models/inkling/nvidia/mlp/)

[ model ](../../api/vllm/models/inkling/nvidia/model/)

[ moe ](../../api/vllm/models/inkling/nvidia/moe/)

[ mtp ](../../api/vllm/models/inkling/nvidia/mtp/)

[ sconv_swa_attn ](../../api/vllm/models/inkling/nvidia/sconv_swa_attn/)

[ short_conv ](../../api/vllm/models/inkling/nvidia/short_conv/)

[ ops ](../../api/vllm/models/inkling/nvidia/ops/)

ops

- [ fa4_rel_attention ](../../api/vllm/models/inkling/nvidia/ops/fa4_rel_attention/)
- [ lamport ](../../api/vllm/models/inkling/nvidia/ops/lamport/)
- [ mm_towers ](../../api/vllm/models/inkling/nvidia/ops/mm_towers/)
- [ norm ](../../api/vllm/models/inkling/nvidia/ops/norm/)
- [ qkvr_prep ](../../api/vllm/models/inkling/nvidia/ops/qkvr_prep/)
- [ sconv ](../../api/vllm/models/inkling/nvidia/ops/sconv/)
- [ silu_and_mul ](../../api/vllm/models/inkling/nvidia/ops/silu_and_mul/)

[ kimi_k3 ](../../api/vllm/models/kimi_k3/)

kimi_k3

[ amd ](../../api/vllm/models/kimi_k3/amd/)

amd

[ kda ](../../api/vllm/models/kimi_k3/amd/kda/)

[ kda_metadata ](../../api/vllm/models/kimi_k3/amd/kda_metadata/)

[ latent_moe_runner ](../../api/vllm/models/kimi_k3/amd/latent_moe_runner/)

[ linear ](../../api/vllm/models/kimi_k3/amd/linear/)

[ model ](../../api/vllm/models/kimi_k3/amd/model/)

[ mtp ](../../api/vllm/models/kimi_k3/amd/mtp/)

[ ops ](../../api/vllm/models/kimi_k3/amd/ops/)

ops

[ attn_res ](../../api/vllm/models/kimi_k3/amd/ops/attn_res/)

[ kda_decode ](../../api/vllm/models/kimi_k3/amd/ops/kda_decode/)

[ third_party ](../../api/vllm/models/kimi_k3/amd/ops/third_party/)

third_party

[ kda ](../../api/vllm/models/kimi_k3/amd/ops/third_party/kda/)

kda

- [ chunk ](../../api/vllm/models/kimi_k3/amd/ops/third_party/kda/chunk/)
- [ chunk_intra ](../../api/vllm/models/kimi_k3/amd/ops/third_party/kda/chunk_intra/)
- [ chunk_intra_token_parallel ](../../api/vllm/models/kimi_k3/amd/ops/third_party/kda/chunk_intra_token_parallel/)
- [ fused_recurrent ](../../api/vllm/models/kimi_k3/amd/ops/third_party/kda/fused_recurrent/)

[ common ](../../api/vllm/models/kimi_k3/common/)

common

- [ mm_preprocess ](../../api/vllm/models/kimi_k3/common/mm_preprocess/)
- [ mtp ](../../api/vllm/models/kimi_k3/common/mtp/)

[ nvidia ](../../api/vllm/models/kimi_k3/nvidia/)

nvidia

[ dspark_mla ](../../api/vllm/models/kimi_k3/nvidia/dspark_mla/)

[ kda ](../../api/vllm/models/kimi_k3/nvidia/kda/)

[ kda_metadata ](../../api/vllm/models/kimi_k3/nvidia/kda_metadata/)

[ latent_moe_runner ](../../api/vllm/models/kimi_k3/nvidia/latent_moe_runner/)

[ low_latency_gemm ](../../api/vllm/models/kimi_k3/nvidia/low_latency_gemm/)

[ mla ](../../api/vllm/models/kimi_k3/nvidia/mla/)

[ model ](../../api/vllm/models/kimi_k3/nvidia/model/)

[ mtp ](../../api/vllm/models/kimi_k3/nvidia/mtp/)

[ ops ](../../api/vllm/models/kimi_k3/nvidia/ops/)

ops

[ attn_res ](../../api/vllm/models/kimi_k3/nvidia/ops/attn_res/)

[ fused_mla_key_concat_kv_cache ](../../api/vllm/models/kimi_k3/nvidia/ops/fused_mla_key_concat_kv_cache/)

[ latent_moe_tail ](../../api/vllm/models/kimi_k3/nvidia/ops/latent_moe_tail/)

[ vision_fa4_warmup ](../../api/vllm/models/kimi_k3/nvidia/ops/vision_fa4_warmup/)

[ cute_dsl ](../../api/vllm/models/kimi_k3/nvidia/ops/cute_dsl/)

cute_dsl

[ gemm_rs ](../../api/vllm/models/kimi_k3/nvidia/ops/cute_dsl/gemm_rs/)

[ latent_moe_tail ](../../api/vllm/models/kimi_k3/nvidia/ops/cute_dsl/latent_moe_tail/)

latent_moe_tail

- [ allreduce_rmsnorm_reduce_scatter_early_exit ](../../api/vllm/models/kimi_k3/nvidia/ops/cute_dsl/latent_moe_tail/allreduce_rmsnorm_reduce_scatter_early_exit/)
- [ fused_add_multicast_gemm ](../../api/vllm/models/kimi_k3/nvidia/ops/cute_dsl/latent_moe_tail/fused_add_multicast_gemm/)
- [ fused_add_multicast_skinny_gemm ](../../api/vllm/models/kimi_k3/nvidia/ops/cute_dsl/latent_moe_tail/fused_add_multicast_skinny_gemm/)
- [ lamport_copy ](../../api/vllm/models/kimi_k3/nvidia/ops/cute_dsl/latent_moe_tail/lamport_copy/)
- [ primitives ](../../api/vllm/models/kimi_k3/nvidia/ops/cute_dsl/latent_moe_tail/primitives/)

[ third_party ](../../api/vllm/models/kimi_k3/nvidia/ops/third_party/)

third_party

[ kda ](../../api/vllm/models/kimi_k3/nvidia/ops/third_party/kda/)

kda

- [ chunk ](../../api/vllm/models/kimi_k3/nvidia/ops/third_party/kda/chunk/)
- [ chunk_intra ](../../api/vllm/models/kimi_k3/nvidia/ops/third_party/kda/chunk_intra/)
- [ chunk_intra_token_parallel ](../../api/vllm/models/kimi_k3/nvidia/ops/third_party/kda/chunk_intra_token_parallel/)
- [ fused_recurrent ](../../api/vllm/models/kimi_k3/nvidia/ops/third_party/kda/fused_recurrent/)

[ minimax_m3 ](../../api/vllm/models/minimax_m3/)

minimax_m3

[ amd ](../../api/vllm/models/minimax_m3/amd/)

amd

[ model ](../../api/vllm/models/minimax_m3/amd/model/)

[ mtp ](../../api/vllm/models/minimax_m3/amd/mtp/)

[ sparse_attention_msa ](../../api/vllm/models/minimax_m3/amd/sparse_attention_msa/)

[ ops ](../../api/vllm/models/minimax_m3/amd/ops/)

ops

- [ gemma_rmsnorm ](../../api/vllm/models/minimax_m3/amd/ops/gemma_rmsnorm/)
- [ index_topk ](../../api/vllm/models/minimax_m3/amd/ops/index_topk/)
- [ sparse_attn ](../../api/vllm/models/minimax_m3/amd/ops/sparse_attn/)
- [ sparse_pa ](../../api/vllm/models/minimax_m3/amd/ops/sparse_pa/)
- [ swiglu_oai ](../../api/vllm/models/minimax_m3/amd/ops/swiglu_oai/)

[ common ](../../api/vllm/models/minimax_m3/common/)

common

[ indexer ](../../api/vllm/models/minimax_m3/common/indexer/)

[ mm_preprocess ](../../api/vllm/models/minimax_m3/common/mm_preprocess/)

[ sparse_attention ](../../api/vllm/models/minimax_m3/common/sparse_attention/)

[ vision_tower ](../../api/vllm/models/minimax_m3/common/vision_tower/)

[ ops ](../../api/vllm/models/minimax_m3/common/ops/)

ops

- [ index_topk ](../../api/vllm/models/minimax_m3/common/ops/index_topk/)
- [ sparse_attn ](../../api/vllm/models/minimax_m3/common/ops/sparse_attn/)

[ nvidia ](../../api/vllm/models/minimax_m3/nvidia/)

nvidia

[ indexer_msa ](../../api/vllm/models/minimax_m3/nvidia/indexer_msa/)

[ model ](../../api/vllm/models/minimax_m3/nvidia/model/)

[ msa_cutlass_sparse_decode ](../../api/vllm/models/minimax_m3/nvidia/msa_cutlass_sparse_decode/)

[ mtp ](../../api/vllm/models/minimax_m3/nvidia/mtp/)

[ sparse_attention_msa ](../../api/vllm/models/minimax_m3/nvidia/sparse_attention_msa/)

[ ops ](../../api/vllm/models/minimax_m3/nvidia/ops/)

ops

- [ index_decode_score ](../../api/vllm/models/minimax_m3/nvidia/ops/index_decode_score/)

[ multimodal ](../../api/vllm/multimodal/)

multimodal

[ audio ](../../api/vllm/multimodal/audio/)

[ cache ](../../api/vllm/multimodal/cache/)

[ encoder_budget ](../../api/vllm/multimodal/encoder_budget/)

[ gpu_ipc_memory ](../../api/vllm/multimodal/gpu_ipc_memory/)

[ hasher ](../../api/vllm/multimodal/hasher/)

[ image ](../../api/vllm/multimodal/image/)

[ inputs ](../../api/vllm/multimodal/inputs/)

[ parse ](../../api/vllm/multimodal/parse/)

[ registry ](../../api/vllm/multimodal/registry/)

[ utils ](../../api/vllm/multimodal/utils/)

[ video ](../../api/vllm/multimodal/video/)

[ media ](../../api/vllm/multimodal/media/)

media

- [ audio ](../../api/vllm/multimodal/media/audio/)
- [ base ](../../api/vllm/multimodal/media/base/)
- [ connector ](../../api/vllm/multimodal/media/connector/)
- [ image ](../../api/vllm/multimodal/media/image/)
- [ video ](../../api/vllm/multimodal/media/video/)

[ processing ](../../api/vllm/multimodal/processing/)

processing

- [ context ](../../api/vllm/multimodal/processing/context/)
- [ dummy_inputs ](../../api/vllm/multimodal/processing/dummy_inputs/)
- [ inputs ](../../api/vllm/multimodal/processing/inputs/)
- [ processor ](../../api/vllm/multimodal/processing/processor/)

[ video_prune ](../../api/vllm/multimodal/video_prune/)

video_prune

- [ evs ](../../api/vllm/multimodal/video_prune/evs/)
- [ vidcom2 ](../../api/vllm/multimodal/video_prune/vidcom2/)

[ parser ](../../api/vllm/parser/)

parser

[ abstract_parser ](../../api/vllm/parser/abstract_parser/)

[ deepseek_v4 ](../../api/vllm/parser/deepseek_v4/)

[ deepseek_v32 ](../../api/vllm/parser/deepseek_v32/)

[ gemma4 ](../../api/vllm/parser/gemma4/)

[ glm47_moe ](../../api/vllm/parser/glm47_moe/)

[ harmony ](../../api/vllm/parser/harmony/)

[ inkling ](../../api/vllm/parser/inkling/)

[ kimi_k2 ](../../api/vllm/parser/kimi_k2/)

[ kimi_k3 ](../../api/vllm/parser/kimi_k3/)

[ ling3 ](../../api/vllm/parser/ling3/)

[ metrics ](../../api/vllm/parser/metrics/)

[ minimax_m2 ](../../api/vllm/parser/minimax_m2/)

[ mistral ](../../api/vllm/parser/mistral/)

[ nemotron_v3 ](../../api/vllm/parser/nemotron_v3/)

[ parser_manager ](../../api/vllm/parser/parser_manager/)

[ qwen3 ](../../api/vllm/parser/qwen3/)

[ seed_oss ](../../api/vllm/parser/seed_oss/)

[ utils ](../../api/vllm/parser/utils/)

[ engine ](../../api/vllm/parser/engine/)

engine

- [ adapters ](../../api/vllm/parser/engine/adapters/)
- [ events ](../../api/vllm/parser/engine/events/)
- [ incremental_lexer ](../../api/vllm/parser/engine/incremental_lexer/)
- [ parser_engine ](../../api/vllm/parser/engine/parser_engine/)
- [ parser_engine_config ](../../api/vllm/parser/engine/parser_engine_config/)
- [ registered_adapters ](../../api/vllm/parser/engine/registered_adapters/)
- [ streaming_parser_engine ](../../api/vllm/parser/engine/streaming_parser_engine/)
- [ token_id_scanner ](../../api/vllm/parser/engine/token_id_scanner/)

[ platforms ](../../api/vllm/platforms/)

platforms

- [ cpu ](../../api/vllm/platforms/cpu/)
- [ cuda ](../../api/vllm/platforms/cuda/)
- [ interface ](../../api/vllm/platforms/interface/)
- [ rocm ](../../api/vllm/platforms/rocm/)
- [ tpu ](../../api/vllm/platforms/tpu/)
- [ xpu ](../../api/vllm/platforms/xpu/)
- [ zen_cpu ](../../api/vllm/platforms/zen_cpu/)

[ plugins ](../../api/vllm/plugins/)

plugins

[ endpoint_plugins ](../../api/vllm/plugins/endpoint_plugins/)

endpoint_plugins

- [ interface ](../../api/vllm/plugins/endpoint_plugins/interface/)

[ io_processors ](../../api/vllm/plugins/io_processors/)

io_processors

- [ interface ](../../api/vllm/plugins/io_processors/interface/)

[ lora_resolvers ](../../api/vllm/plugins/lora_resolvers/)

lora_resolvers

- [ filesystem_resolver ](../../api/vllm/plugins/lora_resolvers/filesystem_resolver/)
- [ hf_hub_resolver ](../../api/vllm/plugins/lora_resolvers/hf_hub_resolver/)

[ profiler ](../../api/vllm/profiler/)

profiler

- [ layerwise_profile ](../../api/vllm/profiler/layerwise_profile/)
- [ utils ](../../api/vllm/profiler/utils/)
- [ wrapper ](../../api/vllm/profiler/wrapper/)

[ ray ](../../api/vllm/ray/)

ray

- [ lazy_utils ](../../api/vllm/ray/lazy_utils/)
- [ ray_env ](../../api/vllm/ray/ray_env/)

[ reasoning ](../../api/vllm/reasoning/)

reasoning

- [ abs_reasoning_parsers ](../../api/vllm/reasoning/abs_reasoning_parsers/)
- [ basic_parsers ](../../api/vllm/reasoning/basic_parsers/)
- [ cohere_command_reasoning_parser ](../../api/vllm/reasoning/cohere_command_reasoning_parser/)
- [ deepseek_r1_reasoning_parser ](../../api/vllm/reasoning/deepseek_r1_reasoning_parser/)
- [ deepseek_v3_reasoning_parser ](../../api/vllm/reasoning/deepseek_v3_reasoning_parser/)
- [ deepseek_v4_engine_reasoning_parser ](../../api/vllm/reasoning/deepseek_v4_engine_reasoning_parser/)
- [ ernie45_reasoning_parser ](../../api/vllm/reasoning/ernie45_reasoning_parser/)
- [ gemma4_engine_reasoning_parser ](../../api/vllm/reasoning/gemma4_engine_reasoning_parser/)
- [ gemma4_utils ](../../api/vllm/reasoning/gemma4_utils/)
- [ glm47_moe_reasoning_parser ](../../api/vllm/reasoning/glm47_moe_reasoning_parser/)
- [ gptoss_reasoning_parser ](../../api/vllm/reasoning/gptoss_reasoning_parser/)
- [ granite_reasoning_parser ](../../api/vllm/reasoning/granite_reasoning_parser/)
- [ hunyuan_a13b_reasoning_parser ](../../api/vllm/reasoning/hunyuan_a13b_reasoning_parser/)
- [ hy_v3_reasoning_parser ](../../api/vllm/reasoning/hy_v3_reasoning_parser/)
- [ identity_reasoning_parser ](../../api/vllm/reasoning/identity_reasoning_parser/)
- [ inkling_reasoning_parser ](../../api/vllm/reasoning/inkling_reasoning_parser/)
- [ kimi_k2_reasoning_parser ](../../api/vllm/reasoning/kimi_k2_reasoning_parser/)
- [ kimi_k3_reasoning_parser ](../../api/vllm/reasoning/kimi_k3_reasoning_parser/)
- [ ling3_reasoning_parser ](../../api/vllm/reasoning/ling3_reasoning_parser/)
- [ minimax_m2_reasoning_parser ](../../api/vllm/reasoning/minimax_m2_reasoning_parser/)
- [ minimax_m3_reasoning_parser ](../../api/vllm/reasoning/minimax_m3_reasoning_parser/)
- [ mistral_reasoning_parser ](../../api/vllm/reasoning/mistral_reasoning_parser/)
- [ muse_glimmer_reasoning_parser ](../../api/vllm/reasoning/muse_glimmer_reasoning_parser/)
- [ nemotron_v3_engine_reasoning_parser ](../../api/vllm/reasoning/nemotron_v3_engine_reasoning_parser/)
- [ olmo3_reasoning_parser ](../../api/vllm/reasoning/olmo3_reasoning_parser/)
- [ poolside_v1_reasoning_parser ](../../api/vllm/reasoning/poolside_v1_reasoning_parser/)
- [ qwen3_engine_reasoning_parser ](../../api/vllm/reasoning/qwen3_engine_reasoning_parser/)
- [ seed_oss_engine_reasoning_parser ](../../api/vllm/reasoning/seed_oss_engine_reasoning_parser/)
- [ step3_reasoning_parser ](../../api/vllm/reasoning/step3_reasoning_parser/)
- [ step3p5_reasoning_parser ](../../api/vllm/reasoning/step3p5_reasoning_parser/)

[ renderers ](../../api/vllm/renderers/)

renderers

[ base ](../../api/vllm/renderers/base/)

[ cohere ](../../api/vllm/renderers/cohere/)

[ deepseek_v4 ](../../api/vllm/renderers/deepseek_v4/)

[ deepseek_v32 ](../../api/vllm/renderers/deepseek_v32/)

[ embed_utils ](../../api/vllm/renderers/embed_utils/)

[ hf ](../../api/vllm/renderers/hf/)

[ inkling ](../../api/vllm/renderers/inkling/)

[ inkling_encoding ](../../api/vllm/renderers/inkling_encoding/)

[ kimi_k3 ](../../api/vllm/renderers/kimi_k3/)

[ mistral ](../../api/vllm/renderers/mistral/)

[ online_derenderer ](../../api/vllm/renderers/online_derenderer/)

[ online_renderer ](../../api/vllm/renderers/online_renderer/)

[ params ](../../api/vllm/renderers/params/)

[ registry ](../../api/vllm/renderers/registry/)

[ terratorch ](../../api/vllm/renderers/terratorch/)

[ inputs ](../../api/vllm/renderers/inputs/)

inputs

- [ preprocess ](../../api/vllm/renderers/inputs/preprocess/)
- [ tokenize ](../../api/vllm/renderers/inputs/tokenize/)

[ tilelang_utils ](../../api/vllm/tilelang_utils/)

tilelang_utils

[ tokenizers ](../../api/vllm/tokenizers/)

tokenizers

- [ deepseek_v4 ](../../api/vllm/tokenizers/deepseek_v4/)
- [ deepseek_v4_encoding ](../../api/vllm/tokenizers/deepseek_v4_encoding/)
- [ deepseek_v32 ](../../api/vllm/tokenizers/deepseek_v32/)
- [ deepseek_v32_encoding ](../../api/vllm/tokenizers/deepseek_v32_encoding/)
- [ detokenizer_utils ](../../api/vllm/tokenizers/detokenizer_utils/)
- [ fastokens ](../../api/vllm/tokenizers/fastokens/)
- [ hf ](../../api/vllm/tokenizers/hf/)
- [ kimi_audio ](../../api/vllm/tokenizers/kimi_audio/)
- [ mistral ](../../api/vllm/tokenizers/mistral/)
- [ protocol ](../../api/vllm/tokenizers/protocol/)
- [ registry ](../../api/vllm/tokenizers/registry/)

[ tool_parsers ](../../api/vllm/tool_parsers/)

tool_parsers

- [ abstract_tool_parser ](../../api/vllm/tool_parsers/abstract_tool_parser/)
- [ apertus_tool_parser ](../../api/vllm/tool_parsers/apertus_tool_parser/)
- [ cohere_command_tool_parser ](../../api/vllm/tool_parsers/cohere_command_tool_parser/)
- [ deepseekv3_tool_parser ](../../api/vllm/tool_parsers/deepseekv3_tool_parser/)
- [ deepseekv4_engine_tool_parser ](../../api/vllm/tool_parsers/deepseekv4_engine_tool_parser/)
- [ deepseekv31_tool_parser ](../../api/vllm/tool_parsers/deepseekv31_tool_parser/)
- [ deepseekv32_engine_tool_parser ](../../api/vllm/tool_parsers/deepseekv32_engine_tool_parser/)
- [ dots_tool_parser ](../../api/vllm/tool_parsers/dots_tool_parser/)
- [ ernie45_tool_parser ](../../api/vllm/tool_parsers/ernie45_tool_parser/)
- [ functiongemma_tool_parser ](../../api/vllm/tool_parsers/functiongemma_tool_parser/)
- [ gemma4_engine_tool_parser ](../../api/vllm/tool_parsers/gemma4_engine_tool_parser/)
- [ gemma4_utils ](../../api/vllm/tool_parsers/gemma4_utils/)
- [ gigachat3_tool_parser ](../../api/vllm/tool_parsers/gigachat3_tool_parser/)
- [ glm47_moe_tool_parser ](../../api/vllm/tool_parsers/glm47_moe_tool_parser/)
- [ gptoss_tool_parser ](../../api/vllm/tool_parsers/gptoss_tool_parser/)
- [ granite4_tool_parser ](../../api/vllm/tool_parsers/granite4_tool_parser/)
- [ granite_20b_fc_tool_parser ](../../api/vllm/tool_parsers/granite_20b_fc_tool_parser/)
- [ granite_tool_parser ](../../api/vllm/tool_parsers/granite_tool_parser/)
- [ hermes_tool_parser ](../../api/vllm/tool_parsers/hermes_tool_parser/)
- [ hunyuan_a13b_tool_parser ](../../api/vllm/tool_parsers/hunyuan_a13b_tool_parser/)
- [ hy_v3_tool_parser ](../../api/vllm/tool_parsers/hy_v3_tool_parser/)
- [ inkling_tool_parser ](../../api/vllm/tool_parsers/inkling_tool_parser/)
- [ internlm2_tool_parser ](../../api/vllm/tool_parsers/internlm2_tool_parser/)
- [ jamba_tool_parser ](../../api/vllm/tool_parsers/jamba_tool_parser/)
- [ kimi_k2_tool_parser ](../../api/vllm/tool_parsers/kimi_k2_tool_parser/)
- [ kimi_k3_tool_parser ](../../api/vllm/tool_parsers/kimi_k3_tool_parser/)
- [ lfm2_tool_parser ](../../api/vllm/tool_parsers/lfm2_tool_parser/)
- [ ling3_tool_parser ](../../api/vllm/tool_parsers/ling3_tool_parser/)
- [ llama4_pythonic_tool_parser ](../../api/vllm/tool_parsers/llama4_pythonic_tool_parser/)
- [ llama_tool_parser ](../../api/vllm/tool_parsers/llama_tool_parser/)
- [ longcat_tool_parser ](../../api/vllm/tool_parsers/longcat_tool_parser/)
- [ minicpm5xml_tool_parser ](../../api/vllm/tool_parsers/minicpm5xml_tool_parser/)
- [ minimax_m2_tool_parser ](../../api/vllm/tool_parsers/minimax_m2_tool_parser/)
- [ minimax_m3_tool_parser ](../../api/vllm/tool_parsers/minimax_m3_tool_parser/)
- [ mistral_tool_parser ](../../api/vllm/tool_parsers/mistral_tool_parser/)
- [ muse_glimmer_tool_parser ](../../api/vllm/tool_parsers/muse_glimmer_tool_parser/)
- [ olmo3_tool_parser ](../../api/vllm/tool_parsers/olmo3_tool_parser/)
- [ phi4mini_tool_parser ](../../api/vllm/tool_parsers/phi4mini_tool_parser/)
- [ poolside_v1_tool_parser ](../../api/vllm/tool_parsers/poolside_v1_tool_parser/)
- [ pythonic_tool_parser ](../../api/vllm/tool_parsers/pythonic_tool_parser/)
- [ qwen3_engine_tool_parser ](../../api/vllm/tool_parsers/qwen3_engine_tool_parser/)
- [ rust_tool_parser ](../../api/vllm/tool_parsers/rust_tool_parser/)
- [ seed_oss_engine_tool_parser ](../../api/vllm/tool_parsers/seed_oss_engine_tool_parser/)
- [ step3_tool_parser ](../../api/vllm/tool_parsers/step3_tool_parser/)
- [ step3p5_tool_parser ](../../api/vllm/tool_parsers/step3p5_tool_parser/)
- [ streaming ](../../api/vllm/tool_parsers/streaming/)
- [ structural_tag_registry ](../../api/vllm/tool_parsers/structural_tag_registry/)
- [ utils ](../../api/vllm/tool_parsers/utils/)
- [ xlam_tool_parser ](../../api/vllm/tool_parsers/xlam_tool_parser/)

[ tracing ](../../api/vllm/tracing/)

tracing

- [ otel ](../../api/vllm/tracing/otel/)
- [ utils ](../../api/vllm/tracing/utils/)

[ transformers_utils ](../../api/vllm/transformers_utils/)

transformers_utils

[ config ](../../api/vllm/transformers_utils/config/)

[ config_parser_base ](../../api/vllm/transformers_utils/config_parser_base/)

[ dynamic_module ](../../api/vllm/transformers_utils/dynamic_module/)

[ model_arch_config_convertor ](../../api/vllm/transformers_utils/model_arch_config_convertor/)

[ processor ](../../api/vllm/transformers_utils/processor/)

[ repo_utils ](../../api/vllm/transformers_utils/repo_utils/)

[ runai_utils ](../../api/vllm/transformers_utils/runai_utils/)

[ s3_utils ](../../api/vllm/transformers_utils/s3_utils/)

[ utils ](../../api/vllm/transformers_utils/utils/)

[ chat_templates ](../../api/vllm/transformers_utils/chat_templates/)

chat_templates

- [ registry ](../../api/vllm/transformers_utils/chat_templates/registry/)

[ triton_utils ](../../api/vllm/triton_utils/)

triton_utils

- [ allocation ](../../api/vllm/triton_utils/allocation/)
- [ force_first_config ](../../api/vllm/triton_utils/force_first_config/)
- [ importing ](../../api/vllm/triton_utils/importing/)
- [ tensor_descriptor ](../../api/vllm/triton_utils/tensor_descriptor/)

[ usage ](../../api/vllm/usage/)

usage

- [ usage_lib ](../../api/vllm/usage/usage_lib/)

[ utils ](../../api/vllm/utils/)

utils

- [ argparse_utils ](../../api/vllm/utils/argparse_utils/)
- [ async_utils ](../../api/vllm/utils/async_utils/)
- [ b12x ](../../api/vllm/utils/b12x/)
- [ cache ](../../api/vllm/utils/cache/)
- [ collection_utils ](../../api/vllm/utils/collection_utils/)
- [ counter ](../../api/vllm/utils/counter/)
- [ cpu_resource_utils ](../../api/vllm/utils/cpu_resource_utils/)
- [ cpu_triton_utils ](../../api/vllm/utils/cpu_triton_utils/)
- [ deep_gemm ](../../api/vllm/utils/deep_gemm/)
- [ flashinfer ](../../api/vllm/utils/flashinfer/)
- [ func_utils ](../../api/vllm/utils/func_utils/)
- [ gc_utils ](../../api/vllm/utils/gc_utils/)
- [ gpu_sync_debug ](../../api/vllm/utils/gpu_sync_debug/)
- [ hashing ](../../api/vllm/utils/hashing/)
- [ hpc ](../../api/vllm/utils/hpc/)
- [ humming ](../../api/vllm/utils/humming/)
- [ import_utils ](../../api/vllm/utils/import_utils/)
- [ jit_monitor ](../../api/vllm/utils/jit_monitor/)
- [ jsontree ](../../api/vllm/utils/jsontree/)
- [ math_utils ](../../api/vllm/utils/math_utils/)
- [ mem_constants ](../../api/vllm/utils/mem_constants/)
- [ mem_utils ](../../api/vllm/utils/mem_utils/)
- [ mistral ](../../api/vllm/utils/mistral/)
- [ multi_stream_utils ](../../api/vllm/utils/multi_stream_utils/)
- [ nccl ](../../api/vllm/utils/nccl/)
- [ network_utils ](../../api/vllm/utils/network_utils/)
- [ numa_utils ](../../api/vllm/utils/numa_utils/)
- [ nvtx_pytorch_hooks ](../../api/vllm/utils/nvtx_pytorch_hooks/)
- [ ompmultiprocessing ](../../api/vllm/utils/ompmultiprocessing/)
- [ platform_utils ](../../api/vllm/utils/platform_utils/)
- [ print_utils ](../../api/vllm/utils/print_utils/)
- [ registry ](../../api/vllm/utils/registry/)
- [ serial_utils ](../../api/vllm/utils/serial_utils/)
- [ sparse_utils ](../../api/vllm/utils/sparse_utils/)
- [ system_utils ](../../api/vllm/utils/system_utils/)
- [ tensor_schema ](../../api/vllm/utils/tensor_schema/)
- [ torch_utils ](../../api/vllm/utils/torch_utils/)
- [ tqdm_utils ](../../api/vllm/utils/tqdm_utils/)

[ v1 ](../../api/vllm/v1/)

v1

[ cudagraph_dispatcher ](../../api/vllm/v1/cudagraph_dispatcher/)

[ kv_cache_interface ](../../api/vllm/v1/kv_cache_interface/)

[ kv_cache_spec_registry ](../../api/vllm/v1/kv_cache_spec_registry/)

[ outputs ](../../api/vllm/v1/outputs/)

[ request ](../../api/vllm/v1/request/)

[ serial_utils ](../../api/vllm/v1/serial_utils/)

[ utils ](../../api/vllm/v1/utils/)

[ attention ](../../api/vllm/v1/attention/)

attention

[ backend ](../../api/vllm/v1/attention/backend/)

[ selector ](../../api/vllm/v1/attention/selector/)

[ backends ](../../api/vllm/v1/attention/backends/)

backends

[ cpu_attn ](../../api/vllm/v1/attention/backends/cpu_attn/)

[ fa_utils ](../../api/vllm/v1/attention/backends/fa_utils/)

[ flash_attn ](../../api/vllm/v1/attention/backends/flash_attn/)

[ flash_attn_diffkv ](../../api/vllm/v1/attention/backends/flash_attn_diffkv/)

[ flashinfer ](../../api/vllm/v1/attention/backends/flashinfer/)

[ flex_attention ](../../api/vllm/v1/attention/backends/flex_attention/)

[ gdn_attn ](../../api/vllm/v1/attention/backends/gdn_attn/)

[ hpc_attn ](../../api/vllm/v1/attention/backends/hpc_attn/)

[ linear_attn ](../../api/vllm/v1/attention/backends/linear_attn/)

[ mamba1_attn ](../../api/vllm/v1/attention/backends/mamba1_attn/)

[ mamba2_attn ](../../api/vllm/v1/attention/backends/mamba2_attn/)

[ mamba_attn ](../../api/vllm/v1/attention/backends/mamba_attn/)

[ registry ](../../api/vllm/v1/attention/backends/registry/)

[ rocm_aiter_fa ](../../api/vllm/v1/attention/backends/rocm_aiter_fa/)

[ rocm_aiter_unified_attn ](../../api/vllm/v1/attention/backends/rocm_aiter_unified_attn/)

[ rocm_attn ](../../api/vllm/v1/attention/backends/rocm_attn/)

[ short_conv_attn ](../../api/vllm/v1/attention/backends/short_conv_attn/)

[ triton_attn ](../../api/vllm/v1/attention/backends/triton_attn/)

[ triton_attn_diffkv ](../../api/vllm/v1/attention/backends/triton_attn_diffkv/)

[ turboquant_attn ](../../api/vllm/v1/attention/backends/turboquant_attn/)

[ utils ](../../api/vllm/v1/attention/backends/utils/)

[ mla ](../../api/vllm/v1/attention/backends/mla/)

mla

[ aiter_triton_mla ](../../api/vllm/v1/attention/backends/mla/aiter_triton_mla/)

[ compressor_utils ](../../api/vllm/v1/attention/backends/mla/compressor_utils/)

[ cpu_mla ](../../api/vllm/v1/attention/backends/mla/cpu_mla/)

[ cutlass_mla ](../../api/vllm/v1/attention/backends/mla/cutlass_mla/)

[ flashattn_mla ](../../api/vllm/v1/attention/backends/mla/flashattn_mla/)

[ flashattn_mla_sparse ](../../api/vllm/v1/attention/backends/mla/flashattn_mla_sparse/)

[ flashinfer_mla ](../../api/vllm/v1/attention/backends/mla/flashinfer_mla/)

[ flashinfer_mla_sparse ](../../api/vllm/v1/attention/backends/mla/flashinfer_mla_sparse/)

[ flashinfer_mla_sparse_sm120 ](../../api/vllm/v1/attention/backends/mla/flashinfer_mla_sparse_sm120/)

[ flashmla ](../../api/vllm/v1/attention/backends/mla/flashmla/)

[ flashmla_sparse ](../../api/vllm/v1/attention/backends/mla/flashmla_sparse/)

[ indexer ](../../api/vllm/v1/attention/backends/mla/indexer/)

[ rocm_aiter_mla ](../../api/vllm/v1/attention/backends/mla/rocm_aiter_mla/)

[ rocm_aiter_mla_sparse ](../../api/vllm/v1/attention/backends/mla/rocm_aiter_mla_sparse/)

[ sparse_swa ](../../api/vllm/v1/attention/backends/mla/sparse_swa/)

[ sparse_utils ](../../api/vllm/v1/attention/backends/mla/sparse_utils/)

[ tokenspeed_mla ](../../api/vllm/v1/attention/backends/mla/tokenspeed_mla/)

[ triton_mla ](../../api/vllm/v1/attention/backends/mla/triton_mla/)

[ xpu_mla_sparse ](../../api/vllm/v1/attention/backends/mla/xpu_mla_sparse/)

[ prefill ](../../api/vllm/v1/attention/backends/mla/prefill/)

prefill

- [ aiter_flash_attn ](../../api/vllm/v1/attention/backends/mla/prefill/aiter_flash_attn/)
- [ base ](../../api/vllm/v1/attention/backends/mla/prefill/base/)
- [ flash_attn ](../../api/vllm/v1/attention/backends/mla/prefill/flash_attn/)
- [ flashinfer ](../../api/vllm/v1/attention/backends/mla/prefill/flashinfer/)
- [ registry ](../../api/vllm/v1/attention/backends/mla/prefill/registry/)
- [ selector ](../../api/vllm/v1/attention/backends/mla/prefill/selector/)
- [ tokenspeed_mla ](../../api/vllm/v1/attention/backends/mla/prefill/tokenspeed_mla/)
- [ trtllm_ragged ](../../api/vllm/v1/attention/backends/mla/prefill/trtllm_ragged/)

[ ops ](../../api/vllm/v1/attention/ops/)

ops

[ chunked_prefill_paged_decode ](../../api/vllm/v1/attention/ops/chunked_prefill_paged_decode/)

[ common ](../../api/vllm/v1/attention/ops/common/)

[ dcp_alltoall ](../../api/vllm/v1/attention/ops/dcp_alltoall/)

[ dcp_utils ](../../api/vllm/v1/attention/ops/dcp_utils/)

[ flashmla ](../../api/vllm/v1/attention/ops/flashmla/)

[ flydsl_turboquant_decode ](../../api/vllm/v1/attention/ops/flydsl_turboquant_decode/)

[ int4_per_token_head ](../../api/vllm/v1/attention/ops/int4_per_token_head/)

[ merge_attn_states ](../../api/vllm/v1/attention/ops/merge_attn_states/)

[ paged_attn ](../../api/vllm/v1/attention/ops/paged_attn/)

[ prefix_prefill ](../../api/vllm/v1/attention/ops/prefix_prefill/)

[ rocm_aiter_mla_sparse ](../../api/vllm/v1/attention/ops/rocm_aiter_mla_sparse/)

[ triton_attention_helpers ](../../api/vllm/v1/attention/ops/triton_attention_helpers/)

[ triton_decode_attention ](../../api/vllm/v1/attention/ops/triton_decode_attention/)

[ triton_fp8_mqa_logits ](../../api/vllm/v1/attention/ops/triton_fp8_mqa_logits/)

[ triton_merge_attn_states ](../../api/vllm/v1/attention/ops/triton_merge_attn_states/)

[ triton_prefill_attention ](../../api/vllm/v1/attention/ops/triton_prefill_attention/)

[ triton_reshape_and_cache_flash ](../../api/vllm/v1/attention/ops/triton_reshape_and_cache_flash/)

[ triton_turboquant_decode ](../../api/vllm/v1/attention/ops/triton_turboquant_decode/)

[ triton_turboquant_store ](../../api/vllm/v1/attention/ops/triton_turboquant_store/)

[ triton_unified_attention ](../../api/vllm/v1/attention/ops/triton_unified_attention/)

[ triton_unified_attention_diffkv ](../../api/vllm/v1/attention/ops/triton_unified_attention_diffkv/)

[ vit_attn_wrappers ](../../api/vllm/v1/attention/ops/vit_attn_wrappers/)

[ xpu_mla_sparse ](../../api/vllm/v1/attention/ops/xpu_mla_sparse/)

[ flydsl_kernels ](../../api/vllm/v1/attention/ops/flydsl_kernels/)

flydsl_kernels

- [ tq_decode ](../../api/vllm/v1/attention/ops/flydsl_kernels/tq_decode/)
- [ tq_decode_gqa6 ](../../api/vllm/v1/attention/ops/flydsl_kernels/tq_decode_gqa6/)

[ turboquant_soa ](../../api/vllm/v1/attention/ops/turboquant_soa/)

turboquant_soa

- [ triton_turboquant_decode ](../../api/vllm/v1/attention/ops/turboquant_soa/triton_turboquant_decode/)
- [ triton_turboquant_decode_v2 ](../../api/vllm/v1/attention/ops/turboquant_soa/triton_turboquant_decode_v2/)
- [ triton_turboquant_store ](../../api/vllm/v1/attention/ops/turboquant_soa/triton_turboquant_store/)
- [ triton_turboquant_unified_attention ](../../api/vllm/v1/attention/ops/turboquant_soa/triton_turboquant_unified_attention/)

[ core ](../../api/vllm/v1/core/)

core

[ block_pool ](../../api/vllm/v1/core/block_pool/)

[ encoder_cache_manager ](../../api/vllm/v1/core/encoder_cache_manager/)

[ kv_cache_coordinator ](../../api/vllm/v1/core/kv_cache_coordinator/)

[ kv_cache_manager ](../../api/vllm/v1/core/kv_cache_manager/)

[ kv_cache_metrics ](../../api/vllm/v1/core/kv_cache_metrics/)

[ kv_cache_utils ](../../api/vllm/v1/core/kv_cache_utils/)

[ single_type_kv_cache_manager ](../../api/vllm/v1/core/single_type_kv_cache_manager/)

[ sched ](../../api/vllm/v1/core/sched/)

sched

- [ async_scheduler ](../../api/vllm/v1/core/sched/async_scheduler/)
- [ interface ](../../api/vllm/v1/core/sched/interface/)
- [ output ](../../api/vllm/v1/core/sched/output/)
- [ request_queue ](../../api/vllm/v1/core/sched/request_queue/)
- [ scheduler ](../../api/vllm/v1/core/sched/scheduler/)
- [ utils ](../../api/vllm/v1/core/sched/utils/)

[ engine ](../../api/vllm/v1/engine/)

engine

- [ async_llm ](../../api/vllm/v1/engine/async_llm/)
- [ coordinator ](../../api/vllm/v1/engine/coordinator/)
- [ core ](../../api/vllm/v1/engine/core/)
- [ core_client ](../../api/vllm/v1/engine/core_client/)
- [ detokenizer ](../../api/vllm/v1/engine/detokenizer/)
- [ exceptions ](../../api/vllm/v1/engine/exceptions/)
- [ input_processor ](../../api/vllm/v1/engine/input_processor/)
- [ llm_engine ](../../api/vllm/v1/engine/llm_engine/)
- [ logprobs ](../../api/vllm/v1/engine/logprobs/)
- [ output_processor ](../../api/vllm/v1/engine/output_processor/)
- [ parallel_sampling ](../../api/vllm/v1/engine/parallel_sampling/)
- [ tensor_ipc ](../../api/vllm/v1/engine/tensor_ipc/)
- [ utils ](../../api/vllm/v1/engine/utils/)

[ executor ](../../api/vllm/v1/executor/)

executor

- [ abstract ](../../api/vllm/v1/executor/abstract/)
- [ multiproc_executor ](../../api/vllm/v1/executor/multiproc_executor/)
- [ ray_env_utils ](../../api/vllm/v1/executor/ray_env_utils/)
- [ ray_executor ](../../api/vllm/v1/executor/ray_executor/)
- [ ray_executor_v2 ](../../api/vllm/v1/executor/ray_executor_v2/)
- [ ray_utils ](../../api/vllm/v1/executor/ray_utils/)
- [ uniproc_executor ](../../api/vllm/v1/executor/uniproc_executor/)
- [ vllm_net_devices ](../../api/vllm/v1/executor/vllm_net_devices/)

[ fault_tolerance ](../../api/vllm/v1/fault_tolerance/)

fault_tolerance

- [ engine_core_sentinel ](../../api/vllm/v1/fault_tolerance/engine_core_sentinel/)
- [ utils ](../../api/vllm/v1/fault_tolerance/utils/)

[ kv_offload ](../../api/vllm/v1/kv_offload/)

kv_offload

[ base ](../../api/vllm/v1/kv_offload/base/)

[ config ](../../api/vllm/v1/kv_offload/config/)

[ factory ](../../api/vllm/v1/kv_offload/factory/)

[ file_mapper ](../../api/vllm/v1/kv_offload/file_mapper/)

[ cpu ](../../api/vllm/v1/kv_offload/cpu/)

cpu

[ common ](../../api/vllm/v1/kv_offload/cpu/common/)

[ gpu_worker ](../../api/vllm/v1/kv_offload/cpu/gpu_worker/)

[ manager ](../../api/vllm/v1/kv_offload/cpu/manager/)

[ shared_offload_region ](../../api/vllm/v1/kv_offload/cpu/shared_offload_region/)

[ spec ](../../api/vllm/v1/kv_offload/cpu/spec/)

[ swap_blocks_triton ](../../api/vllm/v1/kv_offload/cpu/swap_blocks_triton/)

[ policies ](../../api/vllm/v1/kv_offload/cpu/policies/)

policies

- [ arc ](../../api/vllm/v1/kv_offload/cpu/policies/arc/)
- [ base ](../../api/vllm/v1/kv_offload/cpu/policies/base/)
- [ factory ](../../api/vllm/v1/kv_offload/cpu/policies/factory/)
- [ lru ](../../api/vllm/v1/kv_offload/cpu/policies/lru/)

[ tiering ](../../api/vllm/v1/kv_offload/tiering/)

tiering

[ async_lookup ](../../api/vllm/v1/kv_offload/tiering/async_lookup/)

[ base ](../../api/vllm/v1/kv_offload/tiering/base/)

[ factory ](../../api/vllm/v1/kv_offload/tiering/factory/)

[ manager ](../../api/vllm/v1/kv_offload/tiering/manager/)

[ metrics ](../../api/vllm/v1/kv_offload/tiering/metrics/)

[ spec ](../../api/vllm/v1/kv_offload/tiering/spec/)

[ example ](../../api/vllm/v1/kv_offload/tiering/example/)

example

- [ manager ](../../api/vllm/v1/kv_offload/tiering/example/manager/)

[ fs ](../../api/vllm/v1/kv_offload/tiering/fs/)

fs

- [ io ](../../api/vllm/v1/kv_offload/tiering/fs/io/)
- [ manager ](../../api/vllm/v1/kv_offload/tiering/fs/manager/)
- [ thread_pool ](../../api/vllm/v1/kv_offload/tiering/fs/thread_pool/)

[ obj ](../../api/vllm/v1/kv_offload/tiering/obj/)

obj

- [ config ](../../api/vllm/v1/kv_offload/tiering/obj/config/)
- [ manager ](../../api/vllm/v1/kv_offload/tiering/obj/manager/)

[ p2p ](../../api/vllm/v1/kv_offload/tiering/p2p/)

p2p

[ manager ](../../api/vllm/v1/kv_offload/tiering/p2p/manager/)

[ control ](../../api/vllm/v1/kv_offload/tiering/p2p/control/)

control

- [ base ](../../api/vllm/v1/kv_offload/tiering/p2p/control/base/)
- [ zmq ](../../api/vllm/v1/kv_offload/tiering/p2p/control/zmq/)

[ data ](../../api/vllm/v1/kv_offload/tiering/p2p/data/)

data

- [ base ](../../api/vllm/v1/kv_offload/tiering/p2p/data/base/)
- [ nixl ](../../api/vllm/v1/kv_offload/tiering/p2p/data/nixl/)

[ session ](../../api/vllm/v1/kv_offload/tiering/p2p/session/)

session

- [ client ](../../api/vllm/v1/kv_offload/tiering/p2p/session/client/)
- [ protocol ](../../api/vllm/v1/kv_offload/tiering/p2p/session/protocol/)
- [ server ](../../api/vllm/v1/kv_offload/tiering/p2p/session/server/)
- [ session ](../../api/vllm/v1/kv_offload/tiering/p2p/session/session/)

[ metrics ](../../api/vllm/v1/metrics/)

metrics

- [ loggers ](../../api/vllm/v1/metrics/loggers/)
- [ perf ](../../api/vllm/v1/metrics/perf/)
- [ prometheus ](../../api/vllm/v1/metrics/prometheus/)
- [ ray_wrappers ](../../api/vllm/v1/metrics/ray_wrappers/)
- [ reader ](../../api/vllm/v1/metrics/reader/)
- [ stats ](../../api/vllm/v1/metrics/stats/)
- [ utils ](../../api/vllm/v1/metrics/utils/)

[ pool ](../../api/vllm/v1/pool/)

pool

- [ late_interaction ](../../api/vllm/v1/pool/late_interaction/)
- [ late_interaction_runner ](../../api/vllm/v1/pool/late_interaction_runner/)
- [ metadata ](../../api/vllm/v1/pool/metadata/)

[ sample ](../../api/vllm/v1/sample/)

sample

[ metadata ](../../api/vllm/v1/sample/metadata/)

[ rejection_sampler ](../../api/vllm/v1/sample/rejection_sampler/)

[ sampler ](../../api/vllm/v1/sample/sampler/)

[ thinking_budget_state ](../../api/vllm/v1/sample/thinking_budget_state/)

[ logits_processor ](../../api/vllm/v1/sample/logits_processor/)

logits_processor

- [ builtin ](../../api/vllm/v1/sample/logits_processor/builtin/)
- [ interface ](../../api/vllm/v1/sample/logits_processor/interface/)
- [ state ](../../api/vllm/v1/sample/logits_processor/state/)

[ ops ](../../api/vllm/v1/sample/ops/)

ops

- [ bad_words ](../../api/vllm/v1/sample/ops/bad_words/)
- [ logprobs ](../../api/vllm/v1/sample/ops/logprobs/)
- [ penalties ](../../api/vllm/v1/sample/ops/penalties/)
- [ topk_topp_sampler ](../../api/vllm/v1/sample/ops/topk_topp_sampler/)
- [ topk_topp_triton ](../../api/vllm/v1/sample/ops/topk_topp_triton/)

[ simple_kv_offload ](../../api/vllm/v1/simple_kv_offload/)

simple_kv_offload

- [ copy_backend ](../../api/vllm/v1/simple_kv_offload/copy_backend/)
- [ cuda_mem_ops ](../../api/vllm/v1/simple_kv_offload/cuda_mem_ops/)
- [ disk_backend ](../../api/vllm/v1/simple_kv_offload/disk_backend/)
- [ manager ](../../api/vllm/v1/simple_kv_offload/manager/)
- [ metadata ](../../api/vllm/v1/simple_kv_offload/metadata/)
- [ worker ](../../api/vllm/v1/simple_kv_offload/worker/)

[ spec_decode ](../../api/vllm/v1/spec_decode/)

spec_decode

[ custom_class_proposer ](../../api/vllm/v1/spec_decode/custom_class_proposer/)

[ dflash ](../../api/vllm/v1/spec_decode/dflash/)

[ draft_model ](../../api/vllm/v1/spec_decode/draft_model/)

[ eagle ](../../api/vllm/v1/spec_decode/eagle/)

[ extract_hidden_states ](../../api/vllm/v1/spec_decode/extract_hidden_states/)

[ gemma4 ](../../api/vllm/v1/spec_decode/gemma4/)

[ llm_base_proposer ](../../api/vllm/v1/spec_decode/llm_base_proposer/)

[ medusa ](../../api/vllm/v1/spec_decode/medusa/)

[ metadata ](../../api/vllm/v1/spec_decode/metadata/)

[ metrics ](../../api/vllm/v1/spec_decode/metrics/)

[ ngram_proposer ](../../api/vllm/v1/spec_decode/ngram_proposer/)

[ ngram_proposer_gpu ](../../api/vllm/v1/spec_decode/ngram_proposer_gpu/)

[ step3p5 ](../../api/vllm/v1/spec_decode/step3p5/)

[ suffix_decoding ](../../api/vllm/v1/spec_decode/suffix_decoding/)

[ utils ](../../api/vllm/v1/spec_decode/utils/)

[ vocab_mapping ](../../api/vllm/v1/spec_decode/vocab_mapping/)

[ dynamic ](../../api/vllm/v1/spec_decode/dynamic/)

dynamic

- [ utils ](../../api/vllm/v1/spec_decode/dynamic/utils/)

[ structured_output ](../../api/vllm/v1/structured_output/)

structured_output

- [ backend_guidance ](../../api/vllm/v1/structured_output/backend_guidance/)
- [ backend_lm_format_enforcer ](../../api/vllm/v1/structured_output/backend_lm_format_enforcer/)
- [ backend_outlines ](../../api/vllm/v1/structured_output/backend_outlines/)
- [ backend_types ](../../api/vllm/v1/structured_output/backend_types/)
- [ backend_xgrammar ](../../api/vllm/v1/structured_output/backend_xgrammar/)
- [ request ](../../api/vllm/v1/structured_output/request/)
- [ utils ](../../api/vllm/v1/structured_output/utils/)

[ worker ](../../api/vllm/v1/worker/)

worker

[ block_table ](../../api/vllm/v1/worker/block_table/)

[ cp_utils ](../../api/vllm/v1/worker/cp_utils/)

[ cpu_model_runner ](../../api/vllm/v1/worker/cpu_model_runner/)

[ cpu_worker ](../../api/vllm/v1/worker/cpu_worker/)

[ dp_utils ](../../api/vllm/v1/worker/dp_utils/)

[ ec_connector_model_runner_mixin ](../../api/vllm/v1/worker/ec_connector_model_runner_mixin/)

[ encoder_cudagraph ](../../api/vllm/v1/worker/encoder_cudagraph/)

[ encoder_cudagraph_defs ](../../api/vllm/v1/worker/encoder_cudagraph_defs/)

[ gpu_input_batch ](../../api/vllm/v1/worker/gpu_input_batch/)

[ gpu_model_runner ](../../api/vllm/v1/worker/gpu_model_runner/)

[ gpu_ubatch_wrapper ](../../api/vllm/v1/worker/gpu_ubatch_wrapper/)

[ gpu_worker ](../../api/vllm/v1/worker/gpu_worker/)

[ kv_connector_model_runner_mixin ](../../api/vllm/v1/worker/kv_connector_model_runner_mixin/)

[ lora_model_runner_mixin ](../../api/vllm/v1/worker/lora_model_runner_mixin/)

[ mamba_utils ](../../api/vllm/v1/worker/mamba_utils/)

[ startup_plan ](../../api/vllm/v1/worker/startup_plan/)

[ tpu_input_batch ](../../api/vllm/v1/worker/tpu_input_batch/)

[ ubatch_utils ](../../api/vllm/v1/worker/ubatch_utils/)

[ ubatching ](../../api/vllm/v1/worker/ubatching/)

[ utils ](../../api/vllm/v1/worker/utils/)

[ worker_base ](../../api/vllm/v1/worker/worker_base/)

[ workspace ](../../api/vllm/v1/worker/workspace/)

[ xpu_model_runner ](../../api/vllm/v1/worker/xpu_model_runner/)

[ xpu_worker ](../../api/vllm/v1/worker/xpu_worker/)

[ cpu ](../../api/vllm/v1/worker/cpu/)

cpu

- [ buffer_utils ](../../api/vllm/v1/worker/cpu/buffer_utils/)
- [ model_runner ](../../api/vllm/v1/worker/cpu/model_runner/)
- [ shm ](../../api/vllm/v1/worker/cpu/shm/)

[ gpu ](../../api/vllm/v1/worker/gpu/)

gpu

[ async_utils ](../../api/vllm/v1/worker/gpu/async_utils/)

[ attn_utils ](../../api/vllm/v1/worker/gpu/attn_utils/)

[ block_table ](../../api/vllm/v1/worker/gpu/block_table/)

[ buffer_utils ](../../api/vllm/v1/worker/gpu/buffer_utils/)

[ cp_utils ](../../api/vllm/v1/worker/gpu/cp_utils/)

[ cudagraph_utils ](../../api/vllm/v1/worker/gpu/cudagraph_utils/)

[ dp_utils ](../../api/vllm/v1/worker/gpu/dp_utils/)

[ ec_connector ](../../api/vllm/v1/worker/gpu/ec_connector/)

[ eplb_utils ](../../api/vllm/v1/worker/gpu/eplb_utils/)

[ input_batch ](../../api/vllm/v1/worker/gpu/input_batch/)

[ kv_connector ](../../api/vllm/v1/worker/gpu/kv_connector/)

[ lora_utils ](../../api/vllm/v1/worker/gpu/lora_utils/)

[ model_runner ](../../api/vllm/v1/worker/gpu/model_runner/)

[ pcp_manager ](../../api/vllm/v1/worker/gpu/pcp_manager/)

[ pp_utils ](../../api/vllm/v1/worker/gpu/pp_utils/)

[ shutdown ](../../api/vllm/v1/worker/gpu/shutdown/)

[ states ](../../api/vllm/v1/worker/gpu/states/)

[ structured_outputs ](../../api/vllm/v1/worker/gpu/structured_outputs/)

[ warmup ](../../api/vllm/v1/worker/gpu/warmup/)

[ metrics ](../../api/vllm/v1/worker/gpu/metrics/)

metrics

- [ logits ](../../api/vllm/v1/worker/gpu/metrics/logits/)

[ mm ](../../api/vllm/v1/worker/gpu/mm/)

mm

- [ encoder_cache ](../../api/vllm/v1/worker/gpu/mm/encoder_cache/)
- [ encoder_runner ](../../api/vllm/v1/worker/gpu/mm/encoder_runner/)
- [ lora ](../../api/vllm/v1/worker/gpu/mm/lora/)
- [ rope ](../../api/vllm/v1/worker/gpu/mm/rope/)

[ model_states ](../../api/vllm/v1/worker/gpu/model_states/)

model_states

- [ default ](../../api/vllm/v1/worker/gpu/model_states/default/)
- [ encoder_decoder ](../../api/vllm/v1/worker/gpu/model_states/encoder_decoder/)
- [ encoder_only ](../../api/vllm/v1/worker/gpu/model_states/encoder_only/)
- [ interface ](../../api/vllm/v1/worker/gpu/model_states/interface/)
- [ mamba_hybrid ](../../api/vllm/v1/worker/gpu/model_states/mamba_hybrid/)
- [ mm_pruning ](../../api/vllm/v1/worker/gpu/model_states/mm_pruning/)

[ pool ](../../api/vllm/v1/worker/gpu/pool/)

pool

- [ pooling_runner ](../../api/vllm/v1/worker/gpu/pool/pooling_runner/)

[ sample ](../../api/vllm/v1/worker/gpu/sample/)

sample

- [ bad_words ](../../api/vllm/v1/worker/gpu/sample/bad_words/)
- [ gumbel ](../../api/vllm/v1/worker/gpu/sample/gumbel/)
- [ logit_bias ](../../api/vllm/v1/worker/gpu/sample/logit_bias/)
- [ logprob ](../../api/vllm/v1/worker/gpu/sample/logprob/)
- [ min_p ](../../api/vllm/v1/worker/gpu/sample/min_p/)
- [ output ](../../api/vllm/v1/worker/gpu/sample/output/)
- [ penalties ](../../api/vllm/v1/worker/gpu/sample/penalties/)
- [ prompt_logprob ](../../api/vllm/v1/worker/gpu/sample/prompt_logprob/)
- [ sampler ](../../api/vllm/v1/worker/gpu/sample/sampler/)
- [ states ](../../api/vllm/v1/worker/gpu/sample/states/)
- [ thinking_budget ](../../api/vllm/v1/worker/gpu/sample/thinking_budget/)

[ spec_decode ](../../api/vllm/v1/worker/gpu/spec_decode/)

spec_decode

[ adaptive_verification ](../../api/vllm/v1/worker/gpu/spec_decode/adaptive_verification/)

[ rejection_sampler ](../../api/vllm/v1/worker/gpu/spec_decode/rejection_sampler/)

[ rejection_sampler_utils ](../../api/vllm/v1/worker/gpu/spec_decode/rejection_sampler_utils/)

[ speculator ](../../api/vllm/v1/worker/gpu/spec_decode/speculator/)

[ utils ](../../api/vllm/v1/worker/gpu/spec_decode/utils/)

[ autoregressive ](../../api/vllm/v1/worker/gpu/spec_decode/autoregressive/)

autoregressive

- [ cudagraph_utils ](../../api/vllm/v1/worker/gpu/spec_decode/autoregressive/cudagraph_utils/)
- [ speculator ](../../api/vllm/v1/worker/gpu/spec_decode/autoregressive/speculator/)

[ dflash ](../../api/vllm/v1/worker/gpu/spec_decode/dflash/)

dflash

- [ cudagraph ](../../api/vllm/v1/worker/gpu/spec_decode/dflash/cudagraph/)
- [ speculator ](../../api/vllm/v1/worker/gpu/spec_decode/dflash/speculator/)
- [ utils ](../../api/vllm/v1/worker/gpu/spec_decode/dflash/utils/)

[ dflash2 ](../../api/vllm/v1/worker/gpu/spec_decode/dflash2/)

dflash2

- [ speculator ](../../api/vllm/v1/worker/gpu/spec_decode/dflash2/speculator/)

[ dspark ](../../api/vllm/v1/worker/gpu/spec_decode/dspark/)

dspark

- [ speculator ](../../api/vllm/v1/worker/gpu/spec_decode/dspark/speculator/)
- [ utils ](../../api/vllm/v1/worker/gpu/spec_decode/dspark/utils/)

[ eagle ](../../api/vllm/v1/worker/gpu/spec_decode/eagle/)

eagle

- [ eagle3_utils ](../../api/vllm/v1/worker/gpu/spec_decode/eagle/eagle3_utils/)
- [ speculator ](../../api/vllm/v1/worker/gpu/spec_decode/eagle/speculator/)
- [ utils ](../../api/vllm/v1/worker/gpu/spec_decode/eagle/utils/)

[ gemma4 ](../../api/vllm/v1/worker/gpu/spec_decode/gemma4/)

gemma4

- [ speculator ](../../api/vllm/v1/worker/gpu/spec_decode/gemma4/speculator/)

[ mtp ](../../api/vllm/v1/worker/gpu/spec_decode/mtp/)

mtp

- [ speculator ](../../api/vllm/v1/worker/gpu/spec_decode/mtp/speculator/)

[ multi_module_mtp ](../../api/vllm/v1/worker/gpu/spec_decode/multi_module_mtp/)

multi_module_mtp

- [ speculator ](../../api/vllm/v1/worker/gpu/spec_decode/multi_module_mtp/speculator/)

[ sentinel ](../../api/vllm/v1/worker/sentinel/)

sentinel

- [ gpu_worker_sentinel ](../../api/vllm/v1/worker/sentinel/gpu_worker_sentinel/)

[ CLI Reference ](../../cli/)

CLI Reference

vllm

vllm

[ chat ](../../cli/chat/)

[ complete ](../../cli/complete/)

[ run-batch ](../../cli/run-batch/)

[ serve ](../../cli/serve/)

[ bench ](../../cli/bench/)

bench

[ latency ](../../cli/bench/latency/)

[ mm-processor ](../../cli/bench/mm_processor/)

[ serve ](../../cli/bench/serve/)

[ startup ](../../cli/bench/startup/)

[ throughput ](../../cli/bench/throughput/)

[ sweep ](../../cli/bench/sweep/)

sweep

- [ plot ](../../cli/bench/sweep/plot/)
- [ plot_pareto ](../../cli/bench/sweep/plot_pareto/)
- [ serve ](../../cli/bench/sweep/serve/)
- [ serve_workload ](../../cli/bench/sweep/serve_workload/)
- [ startup ](../../cli/bench/sweep/startup/)

[ launch ](../../cli/launch/)

launch

- [ render ](../../cli/launch/render/)

Community

Community

[ Contact Us ](../../community/contact_us/)

[ Meetups ](../../community/meetups/)

[ Sponsors ](../../community/sponsors/)

Governance

Governance

- [ Collaboration Policy ](../../governance/collaboration/)
- [ Committers ](../../governance/committers/)
- [ Governance Process ](../../governance/process/)

[ Blog ](https://blog.vllm.ai)

[ Forum ](https://discuss.vllm.ai)

[ Slack ](https://slack.vllm.ai)

Table of contents

- [ Differences from V0 ](#differences-from-v0)
  - [ Chunked Prefill ](#chunked-prefill)
  - [ CUDA Graphs ](#cuda-graphs)
  - [ Semantic Changes to Logprobs ](#semantic-changes-to-logprobs)
    - [ Logprobs Calculation ](#logprobs-calculation)
    - [ Prompt Logprobs with Prefix Caching ](#prompt-logprobs-with-prefix-caching)
- [ Feature Support ](#feature-support)
  - [ Hardware ](#hardware)
  - [ Models ](#models)
    - [ Pooling Models ](#pooling-models)
    - [ Mamba Models ](#mamba-models)
    - [ Encoder-Decoder Models ](#encoder-decoder-models)
  - [ Features ](#features)
    - [ Removed Features ](#removed-features)
      - [ Sampling features ](#sampling-features)
      - [ KV Cache features ](#kv-cache-features)
      - [ Structured Output features ](#structured-output-features)

1.  [ Home ](../..)
2.  [ User Guide ](../)
3.  [ General ](./)

[![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEwIDIwSDZWNGg3djVoNXYzLjFsMi0yVjhsLTYtNkg2Yy0xLjEgMC0yIC45LTIgMnYxNmMwIDEuMS45IDIgMiAyaDR6bTEwLjItN2MuMSAwIC4zLjEuNC4ybDEuMyAxLjNjLjIuMi4yLjYgMCAuOGwtMSAxLTIuMS0yLjEgMS0xYy4xLS4xLjItLjIuNC0uMm0wIDMuOUwxNC4xIDIzSDEydi0yLjFsNi4xLTYuMXoiIC8+PC9zdmc+)](https://github.com/vllm-project/vllm/edit/main/docs/usage/v1_guide.md "Edit this page")

# vLLM V1[¶](#vllm-v1 "Permanent link")

Announcement

We have fully deprecated V0. Please read [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAxNiAxNiI+PHBhdGggZD0iTTggMGM0LjQyIDAgOCAzLjU4IDggOGE4LjAxIDguMDEgMCAwIDEtNS40NSA3LjU5Yy0uNC4wOC0uNTUtLjE3LS41NS0uMzggMC0uMjcuMDEtMS4xMy4wMS0yLjIgMC0uNzUtLjI1LTEuMjMtLjU0LTEuNDggMS43OC0uMiAzLjY1LS44OCAzLjY1LTMuOTUgMC0uODgtLjMxLTEuNTktLjgyLTIuMTUuMDgtLjIuMzYtMS4wMi0uMDgtMi4xMiAwIDAtLjY3LS4yMi0yLjIuODItLjY0LS4xOC0xLjMyLS4yNy0yLS4yN3MtMS4zNi4wOS0yIC4yN2MtMS41My0xLjAzLTIuMi0uODItMi4yLS44Mi0uNDQgMS4xLS4xNiAxLjkyLS4wOCAyLjEyLS41MS41Ni0uODIgMS4yOC0uODIgMi4xNSAwIDMuMDYgMS44NiAzLjc1IDMuNjQgMy45NS0uMjMuMi0uNDQuNTUtLjUxIDEuMDctLjQ2LjIxLTEuNjEuNTUtMi4zMy0uNjYtLjE1LS4yNC0uNi0uODMtMS4yMy0uODItLjY3LjAxLS4yNy4zOC4wMS41My4zNC4xOS43My45LjgyIDEuMTMuMTYuNDUuNjggMS4zMSAyLjY5Ljk0IDAgLjY3LjAxIDEuMy4wMSAxLjQ5IDAgLjIxLS4xNS40NS0uNTUuMzhBNy45OTUgNy45OTUgMCAwIDEgMCA4YzAtNC40MiAzLjU4LTggOC04IiAvPjwvc3ZnPg==) RFC \#18571](https://github.com/vllm-project/vllm/issues/18571) for more details.

If you have a use case that works on V0 Engine but not V1, please share it on [GitHub](https://github.com/vllm-project/vllm) or in the [vLLM Slack](https://inviter.co/vllm-slack).

vLLM V0 successfully supported a wide range of models and hardware, but as new features were developed independently, the system grew increasingly complex. This complexity made it harder to integrate new capabilities and introduced technical debt, revealing the need for a more streamlined and unified design.

Building on V0’s success, vLLM V1 retains the stable and proven components from V0 (such as the models, GPU kernels, and utilities). At the same time, it significantly re-architects the core systems, covering the scheduler, KV cache manager, worker, sampler, and API server, to provide a cohesive, maintainable framework that better accommodates continued growth and innovation.

Specifically, V1 aims to:

- Provide a **simple, modular, and easy-to-hack codebase**.
- Ensure **high performance** with near-zero CPU overhead.
- **Combine key optimizations** into a unified architecture.
- Require **zero configs** by enabling features/optimizations by default.

We see significant performance improvements from upgrading to V1 core engine, in particular for long context scenarios. Please see performance benchmark (To be added).

For more details, check out the vLLM V1 blog post [vLLM V1: A Major Upgrade to vLLM’s Core Architecture](https://blog.vllm.ai/2025/01/27/v1-alpha-release.html) (published Jan 27, 2025).

This living user guide outlines a few known **important changes and limitations** introduced by vLLM V1. The team has been working actively to bring V1 as the default engine, therefore this guide will be updated constantly as more features get supported on vLLM V1.

## Differences from V0[¶](#differences-from-v0 "Permanent link")

This section lists some differences in behavior between V0 and V1.

### Chunked Prefill[¶](#chunked-prefill "Permanent link")

Chunked prefill is enabled by default whenever possible, unlike in V0 where it was conditionally enabled based on model characteristics.

### CUDA Graphs[¶](#cuda-graphs "Permanent link")

CUDA graph capture takes up more memory in V1 than in V0.

### Semantic Changes to Logprobs[¶](#semantic-changes-to-logprobs "Permanent link")

#### Logprobs Calculation[¶](#logprobs-calculation "Permanent link")

By default, logprobs in V1 are now returned immediately once computed from the model’s raw output (i.e. before applying any logits post-processing such as temperature scaling or penalty adjustments). As a result, the returned logprobs do not reflect the final adjusted probabilities used during sampling.

You can adjust this behavior by setting the `--logprobs-mode` flag. Four modes are supported: `raw_logprobs` (default), `processed_logprobs`, `raw_logits`, `processed_logits`. Raw means the values before applying any logit processors, like bad words. Processed means the values after applying all processors, including temperature and top_k/top_p.

#### Prompt Logprobs with Prefix Caching[¶](#prompt-logprobs-with-prefix-caching "Permanent link")

While V1 supports passing prompt logprobs with prefix caching enabled, it no longer caches the logprobs. For a request requiring prompt logprobs, the engine will ignore the prefix cache and recompute the prefill of full prompt to generate the logprobs.

## Feature Support[¶](#feature-support "Permanent link")

For each item, its support in vLLM V1 falls into one of the following states:

- **🟢 Functional**: Fully operational with optimizations comparable to or better than V0.
- **🟡 In Progress**: Planned to be in vLLM V1, with open PRs/RFCs.
- **🔴 Removed**: Dropped from vLLM V1. Will only consider re-introducing if there is strong demand.

Note

vLLM V1’s unified scheduler treats both prompt and output tokens the same way by using a simple dictionary (e.g., `{request_id: num_tokens}`) to dynamically allocate a fixed token budget per request, enabling features like chunked prefills, prefix caching, and speculative decoding without a strict separation between prefill and decode phases.

The V1 scheduler supports multiple scheduling policies, including First-Come, First-Served (FCFS) and priority-based scheduling (where requests are processed based on assigned priority, with FCFS as a tie-breaker), configurable via the `--scheduling-policy` argument.

### Hardware[¶](#hardware "Permanent link")

| Hardware      | Status |
|---------------|--------|
| **NVIDIA**    | 🟢     |
| **AMD**       | 🟢     |
| **INTEL GPU** | 🟢     |
| **TPU**       | 🟢     |
| **CPU**       | 🟢     |

Note

More hardware platforms may be supported via plugins, e.g.:

- [vllm-ascend](https://github.com/vllm-project/vllm-ascend)
- [vllm-spyre](https://github.com/vllm-project/vllm-spyre)
- [vllm-gaudi](https://github.com/vllm-project/vllm-gaudi)
- [vllm-openvino](https://github.com/vllm-project/vllm-openvino)

Please check their corresponding repositories for more details.

### Models[¶](#models "Permanent link")

| Model Type                 | Status                    |
|----------------------------|---------------------------|
| **Decoder-only Models**    | 🟢                        |
| **Encoder-Decoder Models** | 🟢 (Whisper), 🔴 (Others) |
| **Pooling Models**         | 🟢                        |
| **Mamba Models**           | 🟢                        |
| **Multimodal Models**      | 🟢                        |

See below for the status of models that are not yet supported or have more features planned in V1.

#### Pooling Models[¶](#pooling-models "Permanent link")

Now fully supported, with prefix caching and chunked prefill newly available for last-pooling models.

We are working on enabling prefix caching and chunked prefill for more categories of pooling models.

#### Mamba Models[¶](#mamba-models "Permanent link")

Models using selective state-space mechanisms instead of standard transformer attention are supported. Models that use Mamba-2 and Mamba-1 layers (e.g., `Mamba2ForCausalLM`, `MambaForCausalLM`, `FalconMambaForCausalLM`) are supported.

Hybrid models that combine Mamba-2 and Mamba-1 layers with standard attention layers are also supported (e.g., [`Zamba2ForCausalLM`](../../api/vllm/model_executor/models/zamba2/#vllm.model_executor.models.zamba2.Zamba2ForCausalLM "            Zamba2ForCausalLM"), `NemotronHForCausalLM`, `FalconH1ForCausalLM` and `GraniteMoeHybridForCausalLM`, `JambaForCausalLM`).

Hybrid models with mechanisms different to Mamba are also supported (e.g, `Lfm2ForCausalLM`).

Please note that prefix caching is not yet supported for any of the above models.

#### Encoder-Decoder Models[¶](#encoder-decoder-models "Permanent link")

Whisper is supported natively. Other encoder-decoder models are supported via the plugin system:

- **BART**: `BartForConditionalGeneration` is supported via the official [bart-plugin](https://github.com/vllm-project/bart-plugin).
- **Florence-2**: `Florence2ForConditionalGeneration` is supported via the official [bart-plugin](https://github.com/vllm-project/bart-plugin).

For other encoder-decoder models (e.g., `MllamaForConditionalGeneration`), we recommend following a similar pattern by implementing support through the [plugin system](../../design/plugin_system/).

### Features[¶](#features "Permanent link")

| Feature | Status |
|----|----|
| **Prefix Caching** | 🟢 Functional |
| **Chunked Prefill** | 🟢 Functional |
| **LoRA** | 🟢 Functional |
| **Logprobs Calculation** | 🟢 Functional |
| **FP8 KV Cache** | 🟢 Functional |
| **Spec Decode** | 🟢 Functional |
| **Prompt Logprobs with Prefix Caching** | 🟢 Functional |
| **Structured Output Alternative Backends** | 🟢 Functional |
| **Concurrent Partial Prefills** | 🟡 [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAxNiAxNiI+PHBhdGggZD0iTTggMGM0LjQyIDAgOCAzLjU4IDggOGE4LjAxIDguMDEgMCAwIDEtNS40NSA3LjU5Yy0uNC4wOC0uNTUtLjE3LS41NS0uMzggMC0uMjcuMDEtMS4xMy4wMS0yLjIgMC0uNzUtLjI1LTEuMjMtLjU0LTEuNDggMS43OC0uMiAzLjY1LS44OCAzLjY1LTMuOTUgMC0uODgtLjMxLTEuNTktLjgyLTIuMTUuMDgtLjIuMzYtMS4wMi0uMDgtMi4xMiAwIDAtLjY3LS4yMi0yLjIuODItLjY0LS4xOC0xLjMyLS4yNy0yLS4yN3MtMS4zNi4wOS0yIC4yN2MtMS41My0xLjAzLTIuMi0uODItMi4yLS44Mi0uNDQgMS4xLS4xNiAxLjkyLS4wOCAyLjEyLS41MS41Ni0uODIgMS4yOC0uODIgMi4xNSAwIDMuMDYgMS44NiAzLjc1IDMuNjQgMy45NS0uMjMuMi0uNDQuNTUtLjUxIDEuMDctLjQ2LjIxLTEuNjEuNTUtMi4zMy0uNjYtLjE1LS4yNC0uNi0uODMtMS4yMy0uODItLjY3LjAxLS4yNy4zOC4wMS41My4zNC4xOS43My45LjgyIDEuMTMuMTYuNDUuNjggMS4zMSAyLjY5Ljk0IDAgLjY3LjAxIDEuMy4wMSAxLjQ5IDAgLjIxLS4xNS40NS0uNTUuMzhBNy45OTUgNy45OTUgMCAwIDEgMCA4YzAtNC40MiAzLjU4LTggOC04IiAvPjwvc3ZnPg==) In Progress](https://github.com/vllm-project/vllm/issues/14003) |
| **best_of** | 🔴 [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAxNiAxNiI+PHBhdGggZD0iTTggMGM0LjQyIDAgOCAzLjU4IDggOGE4LjAxIDguMDEgMCAwIDEtNS40NSA3LjU5Yy0uNC4wOC0uNTUtLjE3LS41NS0uMzggMC0uMjcuMDEtMS4xMy4wMS0yLjIgMC0uNzUtLjI1LTEuMjMtLjU0LTEuNDggMS43OC0uMiAzLjY1LS44OCAzLjY1LTMuOTUgMC0uODgtLjMxLTEuNTktLjgyLTIuMTUuMDgtLjIuMzYtMS4wMi0uMDgtMi4xMiAwIDAtLjY3LS4yMi0yLjIuODItLjY0LS4xOC0xLjMyLS4yNy0yLS4yN3MtMS4zNi4wOS0yIC4yN2MtMS41My0xLjAzLTIuMi0uODItMi4yLS44Mi0uNDQgMS4xLS4xNiAxLjkyLS4wOCAyLjEyLS41MS41Ni0uODIgMS4yOC0uODIgMi4xNSAwIDMuMDYgMS44NiAzLjc1IDMuNjQgMy45NS0uMjMuMi0uNDQuNTUtLjUxIDEuMDctLjQ2LjIxLTEuNjEuNTUtMi4zMy0uNjYtLjE1LS4yNC0uNi0uODMtMS4yMy0uODItLjY3LjAxLS4yNy4zOC4wMS41My4zNC4xOS43My45LjgyIDEuMTMuMTYuNDUuNjggMS4zMSAyLjY5Ljk0IDAgLjY3LjAxIDEuMy4wMSAxLjQ5IDAgLjIxLS4xNS40NS0uNTUuMzhBNy45OTUgNy45OTUgMCAwIDEgMCA4YzAtNC40MiAzLjU4LTggOC04IiAvPjwvc3ZnPg==) Removed](https://github.com/vllm-project/vllm/issues/13361) |
| **Per-Request Logits Processors** | 🔴 [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAxNiAxNiI+PHBhdGggZD0iTTggMGM0LjQyIDAgOCAzLjU4IDggOGE4LjAxIDguMDEgMCAwIDEtNS40NSA3LjU5Yy0uNC4wOC0uNTUtLjE3LS41NS0uMzggMC0uMjcuMDEtMS4xMy4wMS0yLjIgMC0uNzUtLjI1LTEuMjMtLjU0LTEuNDggMS43OC0uMiAzLjY1LS44OCAzLjY1LTMuOTUgMC0uODgtLjMxLTEuNTktLjgyLTIuMTUuMDgtLjIuMzYtMS4wMi0uMDgtMi4xMiAwIDAtLjY3LS4yMi0yLjIuODItLjY0LS4xOC0xLjMyLS4yNy0yLS4yN3MtMS4zNi4wOS0yIC4yN2MtMS41My0xLjAzLTIuMi0uODItMi4yLS44Mi0uNDQgMS4xLS4xNiAxLjkyLS4wOCAyLjEyLS41MS41Ni0uODIgMS4yOC0uODIgMi4xNSAwIDMuMDYgMS44NiAzLjc1IDMuNjQgMy45NS0uMjMuMi0uNDQuNTUtLjUxIDEuMDctLjQ2LjIxLTEuNjEuNTUtMi4zMy0uNjYtLjE1LS4yNC0uNi0uODMtMS4yMy0uODItLjY3LjAxLS4yNy4zOC4wMS41My4zNC4xOS43My45LjgyIDEuMTMuMTYuNDUuNjggMS4zMSAyLjY5Ljk0IDAgLjY3LjAxIDEuMy4wMSAxLjQ5IDAgLjIxLS4xNS40NS0uNTUuMzhBNy45OTUgNy45OTUgMCAwIDEgMCA4YzAtNC40MiAzLjU4LTggOC04IiAvPjwvc3ZnPg==) Removed](https://github.com/vllm-project/vllm/pull/13360) |
| **GPU \<\> CPU KV Cache Swapping** | 🔴 Removed |
| **Request-level Structured Output Backend** | 🔴 Removed |

Note

vLLM V1’s unified scheduler treats both prompt and output tokens the same way by using a simple dictionary (e.g., `{request_id: num_tokens}`) to dynamically allocate a fixed token budget per request, enabling features like chunked prefills, prefix caching, and speculative decoding without a strict separation between prefill and decode phases.

#### Removed Features[¶](#removed-features "Permanent link")

As part of the major architectural rework in vLLM V1, several legacy features have been removed.

##### Sampling features[¶](#sampling-features "Permanent link")

- **best_of**: This feature has been removed due to limited usage. See details at [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAxNiAxNiI+PHBhdGggZD0iTTggMGM0LjQyIDAgOCAzLjU4IDggOGE4LjAxIDguMDEgMCAwIDEtNS40NSA3LjU5Yy0uNC4wOC0uNTUtLjE3LS41NS0uMzggMC0uMjcuMDEtMS4xMy4wMS0yLjIgMC0uNzUtLjI1LTEuMjMtLjU0LTEuNDggMS43OC0uMiAzLjY1LS44OCAzLjY1LTMuOTUgMC0uODgtLjMxLTEuNTktLjgyLTIuMTUuMDgtLjIuMzYtMS4wMi0uMDgtMi4xMiAwIDAtLjY3LS4yMi0yLjIuODItLjY0LS4xOC0xLjMyLS4yNy0yLS4yN3MtMS4zNi4wOS0yIC4yN2MtMS41My0xLjAzLTIuMi0uODItMi4yLS44Mi0uNDQgMS4xLS4xNiAxLjkyLS4wOCAyLjEyLS41MS41Ni0uODIgMS4yOC0uODIgMi4xNSAwIDMuMDYgMS44NiAzLjc1IDMuNjQgMy45NS0uMjMuMi0uNDQuNTUtLjUxIDEuMDctLjQ2LjIxLTEuNjEuNTUtMi4zMy0uNjYtLjE1LS4yNC0uNi0uODMtMS4yMy0uODItLjY3LjAxLS4yNy4zOC4wMS41My4zNC4xOS43My45LjgyIDEuMTMuMTYuNDUuNjggMS4zMSAyLjY5Ljk0IDAgLjY3LjAxIDEuMy4wMSAxLjQ5IDAgLjIxLS4xNS40NS0uNTUuMzhBNy45OTUgNy45OTUgMCAwIDEgMCA4YzAtNC40MiAzLjU4LTggOC04IiAvPjwvc3ZnPg==) RFC \#13361](https://github.com/vllm-project/vllm/issues/13361).
- **Per-Request Logits Processors**: In V0, users could pass custom processing functions to adjust logits on a per-request basis. In vLLM V1, this feature has been removed. Instead, we now support **global logits processors** which are set at startup time, see [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAxNiAxNiI+PHBhdGggZD0iTTggMGM0LjQyIDAgOCAzLjU4IDggOGE4LjAxIDguMDEgMCAwIDEtNS40NSA3LjU5Yy0uNC4wOC0uNTUtLjE3LS41NS0uMzggMC0uMjcuMDEtMS4xMy4wMS0yLjIgMC0uNzUtLjI1LTEuMjMtLjU0LTEuNDggMS43OC0uMiAzLjY1LS44OCAzLjY1LTMuOTUgMC0uODgtLjMxLTEuNTktLjgyLTIuMTUuMDgtLjIuMzYtMS4wMi0uMDgtMi4xMiAwIDAtLjY3LS4yMi0yLjIuODItLjY0LS4xOC0xLjMyLS4yNy0yLS4yN3MtMS4zNi4wOS0yIC4yN2MtMS41My0xLjAzLTIuMi0uODItMi4yLS44Mi0uNDQgMS4xLS4xNiAxLjkyLS4wOCAyLjEyLS41MS41Ni0uODIgMS4yOC0uODIgMi4xNSAwIDMuMDYgMS44NiAzLjc1IDMuNjQgMy45NS0uMjMuMi0uNDQuNTUtLjUxIDEuMDctLjQ2LjIxLTEuNjEuNTUtMi4zMy0uNjYtLjE1LS4yNC0uNi0uODMtMS4yMy0uODItLjY3LjAxLS4yNy4zOC4wMS41My4zNC4xOS43My45LjgyIDEuMTMuMTYuNDUuNjggMS4zMSAyLjY5Ljk0IDAgLjY3LjAxIDEuMy4wMSAxLjQ5IDAgLjIxLS4xNS40NS0uNTUuMzhBNy45OTUgNy45OTUgMCAwIDEgMCA4YzAtNC40MiAzLjU4LTggOC04IiAvPjwvc3ZnPg==) RFC \#17799](https://github.com/vllm-project/vllm/issues/17799).

##### KV Cache features[¶](#kv-cache-features "Permanent link")

- **GPU \<\> CPU KV Cache Swapping**: with the new simplified core architecture, vLLM V1 no longer requires KV cache swapping to handle request preemptions.

##### Structured Output features[¶](#structured-output-features "Permanent link")

- **Request-level Structured Output Backend**: Removed; alternative backends (outlines, guidance) with fallbacks are supported now.

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTIxIDEzLjFjLS4xIDAtLjMuMS0uNC4ybC0xIDEgMi4xIDIuMSAxLTFjLjItLjIuMi0uNiAwLS44bC0xLjMtMS4zYy0uMS0uMS0uMi0uMi0uNC0uMm0tMS45IDEuOC02LjEgNlYyM2gyLjFsNi4xLTYuMXpNMTIuNSA3djUuMmw0IDIuNC0xIDFMMTEgMTNWN3pNMTEgMjEuOWMtNS4xLS41LTktNC44LTktOS45QzIgNi41IDYuNSAyIDEyIDJjNS4zIDAgOS42IDQuMSAxMCA5LjMtLjMtLjEtLjYtLjItMS0uMnMtLjcuMS0xIC4yQzE5LjYgNy4yIDE2LjIgNCAxMiA0Yy00LjQgMC04IDMuNi04IDggMCA0LjEgMy4xIDcuNSA3LjEgNy45bC0uMS4yeiIgLz48L3N2Zz4=) July 24, 2026

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEzIDIwaC0yVjhsLTUuNSA1LjUtMS40Mi0xLjQyTDEyIDQuMTZsNy45MiA3LjkyLTEuNDIgMS40MkwxMyA4eiIgLz48L3N2Zz4=) Back to top
