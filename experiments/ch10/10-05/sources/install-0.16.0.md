<!-- 从 install-0.16.0.html 迁移的资料快照；原始 HTML SHA-256: 926f49affccafacf74cb3304adbac533e7a4856763959f789e35a706fe774bca。 -->

- [](../index.html)
- Megatron Core Installation

<a id="megatron-core-installation"></a>

# Megatron Core Installation
Installation is supported using Docker and pip.

<a id="system-requirements"></a>

## System Requirements
<a id="hardware-requirements"></a>

### Hardware Requirements
- **FP8 Support**: NVIDIA Hopper, Ada, Blackwell GPUs

- **Recommended**: NVIDIA Turing architecture or later

<a id="software-requirements"></a>

### Software Requirements
- **CUDA/cuDNN/NCCL**: Latest stable versions

- **PyTorch**: Latest stable version

- **Transformer Engine**: Latest stable version

- **Python**: 3.12 recommended

<a id="docker-installation-recommended"></a>

## Docker Installation (Recommended)
We strongly recommend using the previous releases of [PyTorch NGC Container](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/pytorch) rather than the latest one for optimal compatibility with Megatron Core release and testing matrix. Our releases are always based on the previous month’s NGC container, so this ensures compatibility and stability.

**Note:** The NGC PyTorch container constraints the python environment globally via `PIP_CONSTRAINT`. In the following examples we will unset the variable.

This container comes with all dependencies pre-installed with compatible versions and optimized configurations for NVIDIA GPUs:

- PyTorch (latest stable version)

- CUDA, cuDNN, NCCL (latest stable versions)

- Support for FP8 on NVIDIA Hopper, Ada, and Blackwell GPUs

- For best performance, use NVIDIA Turing GPU architecture generations and later

    # Run container with mounted directories
    docker run --runtime --nvidia --gpus all -it --rm \
      -v /path/to/megatron:/workspace/megatron \
      -v /path/to/dataset:/workspace/dataset \
      -v /path/to/checkpoints:/workspace/checkpoints \
      -e PIP_CONSTRAINT= \
      nvcr.io/nvidia/pytorch:25.04-py3

<a id="pip-installation"></a>

## Pip Installation
Megatron Core installation offers support for two NGC PyTorch containers:

- `dev`: Moving head that supports the most recent upstream dependencies

- `lts`: Long-term support of NGC PyTorch 24.01

Both containers can be combined with `mlm`, which adds package dependencies for Megatron-LM on top of Megatron Core.

1.  Install the latest release dependencies

        pip install "setuptools<80.0.0,>=77.0.0" "packaging>=24.2"
        pip install --no-build-isolation megatron-core[dev]

2.  Next choose one of the following options:

- For running an Megatron LM application

        ```bash
        pip install "setuptools<80.0.0,>=77.0.0" "packaging>=24.2"
        pip install --no-build-isolation megatron-core[mlm,dev]
        ```

- Install packages for LTS support NGC PyTorch 24.01

        ```bash
        pip install "setuptools<80.0.0,>=77.0.0" "packaging>=24.2"
        pip install --no-build-isolation megatron-core[lts]
        ```

- For running an Megatron LM application

        ```bash
        pip install "setuptools<80.0.0,>=77.0.0" "packaging>=24.2"
        pip install --no-build-isolation megatron-core[mlm,lts]
        ```

- For a version of Megatron Core with only Torch, run

        ```bash
        pip install megatron-core
        ```

[](quickstart.html "previous page")

previous

Quick Start

[](../user-guide/data-preparation.html "next page")

next

Data Preparation

On this page

- [System Requirements](#system-requirements)
  - [Hardware Requirements](#hardware-requirements)
  - [Software Requirements](#software-requirements)
- [Docker Installation (Recommended)](#docker-installation-recommended)
- [Pip Installation](#pip-installation)
