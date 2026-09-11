"""Resident blocks/warps per SM, binding limit, latency-hiding check and MMA count for one GEMM tile.

SM limits for compute capability 9.0 are taken from references/text/nvidia-hopper-tuning.txt:
- line 52: "The maximum number of concurrent warps per SM remains the same as in NVIDIA Ampere GPU
  architecture (that is, 64)"
- line 53: "The register file size is 64K 32-bit registers per SM."
- line 54: "The maximum number of registers per thread is 255."
- line 55: "The maximum number of thread blocks per SM is 32 for devices of compute capability 9.0"
- line 56: "shared memory capacity per SM is 228 KB"
- line 57: "the maximum shared memory per thread block is 227 KB."
- line 111: "CUDA reserves 1 KB of shared memory per thread block."
The same limits appear in references/text/cuda-compute-capabilities.txt (CUDA 13.2.1 programming guide,
Table 30/31, compute capability 9.0 column): line 227 "resident blocks per SM" = 32, line 235 "resident warps
per SM" = 64, line 242 "resident threads per SM" = 2048, line 274 "registers per SM" = 64 K, line 277
"registers per thread" = 255, line 294 shared memory per SM = 228 KB; the occupancy definition is
references/text/cuda-writing-kernels.txt ("the ratio of the number of active warps to the maximum number of
active warps supported by the SM").
Device figures from references/text/nvidia-h100-spec.txt line 383 ("GPU Memory Bandwidth 3.35TB/s",
H100 SXM column) and references/text/nvidia-h100.txt line 644 ("The H100 SXM5 GPU has 132 SMs").
Warp size (32 threads), the DRAM latency, the outstanding loads per warp and the MMA instruction shape
are not in the archived texts and are therefore declared_* inputs.  The 128x128x64 BF16 tile working
set (operands 32 KiB + FP32 accumulator 64 KiB = 96 KiB) is chapter 4.3.2's number, reproduced here
through gemm_tiles.account so the two stay identical.
"""
from fractions import Fraction

from ..declared import exact, input_sources as _sources
from ..units import positive_int
from .gemm_tiles import account

LIMITS_CC90 = dict(max_threads_per_sm=2048, max_warps_per_sm=64, registers_per_sm=65536, max_registers_per_thread=255,
                   max_blocks_per_sm=32, shared_memory_per_sm_bytes=228 * 1024,
                   max_shared_memory_per_block_bytes=227 * 1024, reserved_shared_per_block_bytes=1024)


def calculate(threads_per_block=256, declared_registers_per_thread=128, tile_m=128, tile_n=128, tile_k=64,
              accumulator_in_shared=True, extra_shared_bytes=0, declared_warp_size=32,
              hbm_bytes_per_second=3350 * 10**9, sms=132, declared_latency_ns=600,
              declared_outstanding_loads_per_warp=4, declared_load_bytes_per_thread=16,
              declared_mma_shape=(16, 8, 16), input_sources=None):
    inputs = {k: v for k, v in locals().items() if k != 'input_sources'}
    sources = _sources(inputs, input_sources)
    for name in ('threads_per_block', 'declared_registers_per_thread', 'tile_m', 'tile_n', 'tile_k', 'declared_warp_size',
                 'sms', 'declared_latency_ns', 'declared_outstanding_loads_per_warp', 'declared_load_bytes_per_thread'):
        positive_int(inputs[name], name)
    positive_int(extra_shared_bytes, 'extra_shared_bytes', allow_zero=True)
    hbm = exact(hbm_bytes_per_second, 'hbm_bytes_per_second')
    if not isinstance(accumulator_in_shared, bool):
        raise ValueError('accumulator_in_shared must be boolean')
    if threads_per_block % declared_warp_size:
        raise ValueError('threads_per_block must be a whole number of warps')
    if declared_registers_per_thread > LIMITS_CC90['max_registers_per_thread']:
        raise ValueError('registers per thread exceed the architectural maximum')
    limits = dict(LIMITS_CC90)
    tile = account(tile_m, tile_k, tile_n, tile_m, tile_k, tile_n)
    operand_bytes = 2 * tile_m * tile_k + 2 * tile_k * tile_n
    accumulator_bytes = 4 * tile_m * tile_n
    if tile['reserved_working_bytes'] != operand_bytes + accumulator_bytes:
        raise ValueError('gemm_tiles working set decomposition mismatch')
    shared_per_block = operand_bytes + (accumulator_bytes if accumulator_in_shared else 0) + extra_shared_bytes
    if shared_per_block > limits['max_shared_memory_per_block_bytes']:
        raise ValueError('shared memory per block exceeds the per-block maximum')
    warps_per_block = threads_per_block // declared_warp_size
    accumulator_registers_per_thread = 0 if accumulator_in_shared else (tile_m * tile_n) // threads_per_block
    if not accumulator_in_shared and (tile_m * tile_n) % threads_per_block:
        raise ValueError('accumulator must divide evenly over threads when held in registers')
    registers_per_thread = declared_registers_per_thread + accumulator_registers_per_thread
    if registers_per_thread > limits['max_registers_per_thread']:
        raise ValueError('registers per thread including the accumulator exceed 255')
    by = dict(
        threads=limits['max_warps_per_sm'] * declared_warp_size // threads_per_block,
        registers=limits['registers_per_sm'] // (threads_per_block * registers_per_thread),
        shared_memory=limits['shared_memory_per_sm_bytes'] // (shared_per_block + limits['reserved_shared_per_block_bytes']),
        blocks=limits['max_blocks_per_sm'],
    )
    resident_blocks = min(by.values())
    binding = [name for name, value in by.items() if value == resident_blocks]
    resident_warps = resident_blocks * warps_per_block
    occupancy = Fraction(resident_warps, limits['max_warps_per_sm'])
    needed_in_flight = hbm * declared_latency_ns / 10**9
    needed_per_sm = needed_in_flight / sms
    available_per_sm = resident_warps * declared_outstanding_loads_per_warp * declared_warp_size * declared_load_bytes_per_thread
    available_gpu = available_per_sm * sms
    m, n, k = declared_mma_shape
    for name, value in (('mma_m', m), ('mma_n', n), ('mma_k', k)):
        positive_int(value, name)
    if tile_m % m or tile_n % n or tile_k % k:
        raise ValueError('tile must be a whole number of MMA instruction shapes')
    mma_per_tile = (tile_m // m) * (tile_n // n) * (tile_k // k)
    flops_per_mma = 2 * m * n * k
    if mma_per_tile * flops_per_mma != 2 * tile_m * tile_n * tile_k:
        raise ValueError('MMA count does not reproduce the tile FLOPs')
    return dict(schema_version=1, calculation='sm-occupancy', scenario=inputs, declared_input_sources=sources,
                summary=dict(resident_blocks=resident_blocks, resident_warps=resident_warps, occupancy=float(occupancy),
                             binding_limits=binding, shared_bytes_per_block=shared_per_block,
                             registers_per_thread=registers_per_thread,
                             needed_bytes_in_flight_per_sm=float(needed_per_sm), available_bytes_in_flight_per_sm=available_per_sm,
                             covers_latency=Fraction(available_per_sm) >= needed_per_sm,
                             mma_instructions_per_tile=mma_per_tile, tile_flops=2 * tile_m * tile_n * tile_k),
                sm_limits_cc90=limits,
                block=dict(threads=threads_per_block, warps=warps_per_block, registers_per_thread=registers_per_thread,
                           declared_registers_per_thread=declared_registers_per_thread,
                           accumulator_registers_per_thread=accumulator_registers_per_thread,
                           registers_per_block=threads_per_block * registers_per_thread,
                           operand_shared_bytes=operand_bytes, accumulator_bytes=accumulator_bytes,
                           accumulator_in_shared=accumulator_in_shared, shared_bytes_per_block=shared_per_block,
                           shared_bytes_with_reservation=shared_per_block + limits['reserved_shared_per_block_bytes'],
                           gemm_tiles_reserved_working_bytes=tile['reserved_working_bytes']),
                residency=dict(blocks_by_limit=by, resident_blocks=resident_blocks, binding_limits=binding,
                               resident_warps=resident_warps, occupancy_exact=str(occupancy), occupancy=float(occupancy),
                               resident_threads=resident_warps * declared_warp_size),
                latency_hiding=dict(hbm_bytes_per_second_exact=str(hbm), declared_latency_ns=declared_latency_ns,
                                    needed_bytes_in_flight_gpu_exact=str(needed_in_flight), needed_bytes_in_flight_gpu=float(needed_in_flight),
                                    needed_bytes_in_flight_per_sm=float(needed_per_sm),
                                    available_bytes_in_flight_per_sm=available_per_sm,
                                    available_bytes_in_flight_gpu=available_gpu,
                                    request_bytes_per_warp=declared_warp_size * declared_load_bytes_per_thread,
                                    covers_latency=Fraction(available_per_sm) >= needed_per_sm,
                                    coverage_ratio=float(Fraction(available_per_sm) / needed_per_sm),
                                    minimum_resident_warps_to_cover=int(-(-needed_per_sm // (declared_outstanding_loads_per_warp * declared_warp_size * declared_load_bytes_per_thread)))),
                mma=dict(declared_shape=list(declared_mma_shape), instructions_per_tile=mma_per_tile,
                         instructions_per_warp_per_tile=Fraction(mma_per_tile, warps_per_block).numerator if mma_per_tile % warps_per_block == 0 else None,
                         instructions_per_warp_per_tile_exact=str(Fraction(mma_per_tile, warps_per_block)),
                         flops_per_instruction=flops_per_mma, tile_flops=2 * tile_m * tile_n * tile_k,
                         tile_next_level_bytes=tile['next_level_bytes'], tile_arithmetic_intensity=tile['arithmetic_intensity']),
                assumptions=[
                    'SM 限制取自归档的 Hopper 调优指南（每 SM 64 warp、64K 寄存器、32 个线程块、228 KB 共享内存，每块 227 KB 上限并预留 1 KB）；warp 宽度 32 为声明常量。寄存器按线程数×每线程寄存器直接相乘，不模拟分配粒度。',
                    '内核参数（每块线程数、每线程寄存器数、tile 形状）是声明的教学输入；96 KiB 工作集与第 4.3.2 节相同，由 gemm_tiles.account 复算。累加器放共享内存与放寄存器两种口径分别给出。',
                    '延迟隐藏用 Little 定律：需要在途字节 = HBM 带宽 × 声明延迟；可用在途字节 = 常驻 warp × 每 warp 未完成加载数 × 每次加载字节。延迟、未完成数与加载宽度均为声明值，未归档实测；TMA 批量拷贝不按此计。',
                    'MMA 指令数 = tile 各维除以声明指令形状之积，与 tile FLOPs 自洽；指令形状未在归档文本中出现，为声明输入，不代表 wgmma 的实际发射方式或吞吐。',
                ])
