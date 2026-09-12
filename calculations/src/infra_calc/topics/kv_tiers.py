"""Multi-tier KV storage for one A100 slice of a DGX A100: capacity, retention, read paths and overlap.

Per-GPU tiers follow the DGX A100 640GB datasheet (80 GB HBM, 2 TB DIMM / 8 GPUs,
one 3.84 TB U.2 NVMe per GPU, one 200 Gb/s NIC per GPU). The NVMe rates and
endurance are the Solidigm D7-P5520 3.84 TB product-brief maxima. Compute times
use matrix FLOPs over a declared fraction of the A100 BF16 dense peak, as in
cache-route and pd-pool.
"""
from fractions import Fraction as F
from ..models import forward
from ..schema import Scenario
from .. import hardware
from ..sources import model_config
from .state import calculate as state_calculate
from .capacity_scan import calculate as capacity_calculate
from .pd_pool import exact_rate

DAY_S = 86400
SOURCE_IDS = ('nvidia-dgx-a100-datasheet', 'solidigm-d7-p5520-brief', 'cachedattention', 'kvcache-in-the-wild', 'mooncake')


def archived_sources():
    import json
    from pathlib import Path
    manifest = json.loads((Path(__file__).resolve().parents[4] / 'references/manifest.json').read_text())
    known = {row['id']: row for row in manifest}
    return [dict(file='references/' + known[i]['file'], url=known[i]['url'], sha256=known[i]['sha256']) for i in SOURCE_IDS]


def calculate(model='qwen3-8b', prefix_tokens=8192, suffix_tokens=256, device='a100-80gb-sxm',
              compute_efficiency='1/2', hbm_bytes=80*10**9, host_dram_bytes=2*1024**4, gpus_per_server=8,
              ssd_bytes=384*10**10, ssd_read_bytes_per_second=71*10**8, ssd_write_bytes_per_second=42*10**8,
              ssd_dwpd=1, pcie_bytes_per_second=25*10**9, nic_bytes_per_second=25*10**9,
              reuse_windows_s=(10, 600), mooncake_block_tokens=512,
              mooncake_lru=((1000, '0.30'), (10000, '0.40'), (30000, '0.48'), (50000, '0.50'), (100000, '0.51'))):
    inputs = {k: (list(v) if isinstance(v, tuple) else v) for k, v in locals().items()}
    eta = exact_rate(compute_efficiency, 'compute_efficiency', False)
    dev = hardware.select_device(device)
    peak = hardware.select_peak(dev, 'BF16', 'FP32', 'tensor', 'dense')
    rate = F(str(peak['tera_ops_per_second'])) * 10**12 * eta
    state = state_calculate(model, prefix_tokens)['summary']
    per_token = state['kv_bytes_per_token_per_request']
    prefix = state['resident_bytes']
    n_layers = model_config(model)['num_hidden_layers']
    per_layer = F(prefix, n_layers)
    weights = capacity_calculate(model, prefix_tokens)['summary']['bf16_weight_bytes']

    def seconds(flops):
        return F(flops) / rate

    prefill = seconds(forward(model, Scenario(tokens=prefix_tokens, output_head='last'))['summary']['matrix_flops'])
    warm = seconds(forward(model, Scenario(history=prefix_tokens, tokens=suffix_tokens, output_head='last'))['summary']['matrix_flops'])
    produce = F(prefix) / prefill  # bytes/s of new KV while one GPU runs back-to-back uncached prefill

    hbm_kv = hbm_bytes - weights
    dram = F(host_dram_bytes, gpus_per_server)
    tiers = [
        dict(tier='HBM', capacity_bytes=str(hbm_kv), read_bytes_per_second=None, write_bytes_per_second=None,
             read_path='already on GPU'),
        dict(tier='host DRAM', capacity_bytes=str(dram), read_bytes_per_second=pcie_bytes_per_second,
             write_bytes_per_second=pcie_bytes_per_second, read_path='PCIe 4.0 x16'),
        dict(tier='local NVMe', capacity_bytes=str(ssd_bytes), read_bytes_per_second=ssd_read_bytes_per_second,
             write_bytes_per_second=ssd_write_bytes_per_second, read_path='NVMe drive limits the path'),
        dict(tier='remote pool', capacity_bytes=None, read_bytes_per_second=nic_bytes_per_second,
             write_bytes_per_second=nic_bytes_per_second, read_path='NIC to host, then PCIe (serial whole object)'),
    ]
    for t in tiers:
        cap = F(t['capacity_bytes']) if t['capacity_bytes'] else None
        t['retention_s_exact'] = str(cap / produce) if cap is not None else None
        if t['tier'] == 'HBM':
            t['read_s_exact'] = '0'; t['write_s_exact'] = '0'; continue
        if t['tier'] == 'remote pool':
            read = F(prefix, nic_bytes_per_second) + F(prefix, pcie_bytes_per_second)
            write = read
        else:
            read = F(prefix, t['read_bytes_per_second']); write = F(prefix, t['write_bytes_per_second'])
        t['read_s_exact'] = str(read); t['write_s_exact'] = str(write)
        # Save once, read k times: T_write + k T_read < k T_recompute.
        gain = prefill - read
        t['break_even_reuses'] = None if gain <= 0 else int(write // gain) + 1
        # Layer-wise preloading of the history while the suffix is computed.
        load_layer = read / n_layers
        comp_layer = warm / n_layers
        serial = read + warm
        def finish(k):
            # k layers already in HBM before compute starts; remaining loads run back to back.
            done_compute = F(0)
            for i in range(n_layers):
                ready = 0 if i < k else (i - k + 1) * load_layer
                done_compute = max(done_compute, ready) + comp_layer
            return done_compute
        pipelined = finish(0)
        k_min = next(k for k in range(n_layers + 1) if finish(k) == warm)
        t.update(load_per_layer_s_exact=str(load_layer), compute_per_layer_s_exact=str(comp_layer),
                 serial_s_exact=str(serial), layer_pipelined_s_exact=str(pipelined),
                 preload_layers_for_full_overlap=k_min, preload_bytes=str(k_min * per_layer),
                 # CachedAttention: S_buf = B (T_load L_hist - T_pref L_new), B the effective path rate.
                 cachedattention_buffer_bytes_exact=str(max(F(0), (read - warm) * F(prefix) / read)))
        # Smallest suffix whose compute covers the whole history read (per-layer compute >= per-layer load).
        lo, hi = 1, 1
        cover = lambda n: seconds(forward(model, Scenario(history=prefix_tokens, tokens=n, output_head='last'))['summary']['matrix_flops']) >= read
        while not cover(hi): hi *= 2
        while lo < hi:
            mid = (lo + hi) // 2
            if cover(mid): hi = mid
            else: lo = mid + 1
        t['min_suffix_tokens_to_hide_read'] = lo
    ssd_allowed = F(ssd_dwpd * ssd_bytes, DAY_S)
    windows = [dict(window_s=w, required_bytes_exact=str(produce * w)) for w in reuse_windows_s]
    moon = [dict(blocks=b, tokens=b * mooncake_block_tokens, qwen_bytes=b * mooncake_block_tokens * per_token,
                 lru_hit_rate=h) for b, h in mooncake_lru]
    return dict(schema_version=1, calculation='kv-tiers', scenario=inputs,
                sources=archived_sources(),
                summary=dict(kv_bytes_per_token=per_token, prefix_bytes=prefix, layers=n_layers,
                             per_layer_bytes_exact=str(per_layer), weight_bytes=weights,
                             prefill_prefix_s_exact=str(prefill), warm_suffix_s_exact=str(warm),
                             kv_production_bytes_per_second_exact=str(produce),
                             hbm_kv_bytes=hbm_kv, dram_per_gpu_bytes=str(dram),
                             prefetch_window_prefixes=int(dram // prefix),
                             ssd_endurance_bytes_per_second_exact=str(ssd_allowed),
                             ssd_write_over_endurance_exact=str(produce / ssd_allowed),
                             ssd_admissible_fraction_exact=str(ssd_allowed / produce),
                             ssd_write_bandwidth_fraction_exact=str(produce / ssd_write_bytes_per_second),
                             dram_write_bandwidth_fraction_exact=str(produce / pcie_bytes_per_second)),
                tiers=tiers, reuse_windows=windows, mooncake_lru_capacity=moon,
                assumptions=[
                    '每卡一份：DGX A100 的 2 TB DIMM 按 8 张 GPU 均分（按二进制 TiB 计），每卡一块 3.84 TB U.2 NVMe 与一张 200 Gb/s 网卡。HBM 容量按厂商 80 GB 十进制计并扣除 BF16 权重，未扣激活与工作区，是 KV 可用空间的上限。',
                    'NVMe 读写带宽与耐久度取 Solidigm D7-P5520 3.84 TB 产品简介的最大值；路径时间只受盘本身限制，不计文件系统与 PCIe 争用。',
                    'KV 产生率 = 一张 GPU 连续执行无命中 8192-token prefill 时每秒产生的 KV 字节；保留时间 = 容量 / 产生率，对应只按时间先后淘汰、全部写入该层的情形。',
                    '远端池整份先经网卡到主机再经 PCIe 到 GPU，两段串行；逐层预加载按总读取时间均分到各层。',
                    '逐层计算时间按命中后 suffix 的矩阵 FLOPs 均分到各层；预加载层数 k 指计算开始前已在 HBM 的层数。',
                    'Mooncake 表 1 的块数按每块 512 token 换算为 Qwen3-8B 的 KV 字节；命中率属于该一小时采样 trace，容量随真实流量同比例放大。',
                ])
