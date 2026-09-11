"""Unified Bus fabric accounting from first principles: additive endpoint state,
on-chip cache fit, one round trip phase by phase, connection setup and silicon cost.

Every number is derived from declared per-record sizes and per-phase latencies.
The OpenURMA paper's simulator results are kept apart as reference points that
the derivation is checked against, never as inputs.
"""
from fractions import Fraction
import hashlib
import json
from ..paths import PROJECT
from ..units import positive_int

# Reference points measured by the paper's two-node SystemC simulator at
# link 100 ns, 64 B payload, concurrency 1 (OpenURMA revision 2026-06-02,
# Table 7 and §8). They validate the phase sums below and are not inputs.
PAPER_MEASURED_NS = {'ub_loadstore': 500, 'ub_urma': 757, 'roce_dma': 2236}
PAPER_CACHE_ENTRIES = {'roce_qp': 512, 'ub_channel': 2048}


def evidence():
    rows = json.loads((PROJECT / 'configs/ub-fabric.lock.json').read_text())
    for r in rows:
        b = (PROJECT / r['file']).read_bytes()
        if len(b) != r['bytes'] or hashlib.sha256(b).hexdigest() != r['sha256']:
            raise ValueError('UB fabric source changed: ' + r['file'])
    return rows


def _first_exceeding(cost, limit, start=1, stop=1 << 20):
    n = start
    while n < stop:
        if cost(n) > limit:
            return n
        n += 1
    raise ValueError('no cardinality exceeds the cache within the search range')


def calculate(jetty_bytes=20, segment_bytes=32, channel_bytes=56, qp_bytes=512,
              endpoint_counts=(1, 8, 64, 256, 1024), context_cache_bytes=262144,
              apps_per_host=8, host_counts=(2, 8, 64, 192, 384, 1024),
              membus_ns=30, pcie_mmio_ns=150, pcie_dma_read_ns=500, pcie_dma_write_ns=250,
              verb_post_ns=50, wqe_construct_ns=30, cqe_poll_host_ns=70, cqe_poll_onchip_ns=5,
              verb_poll_ns=30, psn_serialize_ns=50, dram_row_ns=30, local_dram_ns=70,
              link_ns=100, link_sweep_ns=(50, 100, 200, 500), clock_hz=322_000_000,
              ldst_pipeline_cycles=8, urma_pipeline_cycles=25, roce_pipeline_cycles=9,
              ub_initiation_interval_cycles=2, roce_cycles_per_request=6,
              ioctl_ns=5000, oob_rtt_ns=500000, setup_cores=32,
              directory_lines=1048576, directory_tag_bytes=8,
              gating_max_cycles=50, isolation_release_cycles=78, roce_cadence_cycles=8,
              ub_luts=122710, roce_luts=46636, fpga_luts=871680, ub_bram=328, roce_bram=67,
              ub_flipflops=194266, roce_flipflops=91900, ub_cold_cycles=24, roce_cold_cycles=9):
    scenario = {k: (list(v) if isinstance(v, tuple) else v) for k, v in locals().items()}
    for name in ('jetty_bytes', 'segment_bytes', 'channel_bytes', 'qp_bytes', 'context_cache_bytes',
                 'apps_per_host', 'clock_hz', 'ldst_pipeline_cycles', 'urma_pipeline_cycles',
                 'roce_pipeline_cycles', 'ub_initiation_interval_cycles', 'roce_cycles_per_request',
                 'ioctl_ns', 'oob_rtt_ns', 'setup_cores', 'directory_lines', 'link_ns',
                 'ub_luts', 'roce_luts', 'fpga_luts', 'ub_cold_cycles', 'roce_cold_cycles'):
        positive_int(scenario[name], name)
    for name in ('membus_ns', 'pcie_mmio_ns', 'pcie_dma_read_ns', 'pcie_dma_write_ns', 'verb_post_ns',
                 'wqe_construct_ns', 'cqe_poll_host_ns', 'cqe_poll_onchip_ns', 'verb_poll_ns',
                 'psn_serialize_ns', 'dram_row_ns', 'local_dram_ns', 'directory_tag_bytes',
                 'gating_max_cycles', 'isolation_release_cycles', 'roce_cadence_cycles',
                 'ub_bram', 'roce_bram', 'ub_flipflops', 'roce_flipflops'):
        positive_int(scenario[name], name, allow_zero=True)
    for name in ('endpoint_counts', 'host_counts', 'link_sweep_ns'):
        if not scenario[name] or any(positive_int(v, name) for v in scenario[name] if False):
            raise ValueError(name + ' must be a non-empty list')
        for v in scenario[name]:
            positive_int(v, name)
    if any(h < 2 for h in host_counts):
        raise ValueError('host_counts must contain at least two hosts per entry')
    cycle_ns = Fraction(10 ** 9, clock_hz)

    # 1. Endpoint state, N local endpoints × M = N remote endpoints.
    def ub_state(n, m):
        return n * (jetty_bytes + segment_bytes) + m * channel_bytes

    def roce_state(n, m):
        return n * m * qp_bytes + n * segment_bytes

    state_rows = []
    for n in endpoint_counts:
        ub, roce = ub_state(n, n), roce_state(n, n)
        state_rows.append(dict(endpoints=n, ub_bytes=ub, roce_bytes=roce, ratio=round(roce / ub, 1),
                               ub_fits_cache=ub <= context_cache_bytes, roce_fits_cache=roce <= context_cache_bytes))

    # 2. Cache fit: the first symmetric cardinality whose state exceeds the context cache.
    roce_spill = _first_exceeding(lambda n: roce_state(n, n), context_cache_bytes)
    ub_spill = _first_exceeding(lambda n: ub_state(n, n), context_cache_bytes)
    roce_refetch = 2 * pcie_dma_read_ns
    ub_refetch = 2 * (membus_ns + local_dram_ns)

    # 3. One 64 B remote read, phase by phase on the critical path.
    ldst_nic = ldst_pipeline_cycles * cycle_ns
    urma_nic = urma_pipeline_cycles * cycle_ns
    roce_nic = roce_pipeline_cycles * cycle_ns
    phases = {
        'ub_loadstore': [
            ('片上总线提交', '片上总线', membus_ns), ('NIC 发送流水线', 'NIC 流水线', ldst_nic),
            ('线路去程', '线路', link_ns), ('NIC 接收流水线', 'NIC 流水线', ldst_nic),
            ('目标片上总线到内存', '片上总线', membus_ns), ('目标 DRAM 行命中', '内存与完成', dram_row_ns),
            ('NIC 响应流水线', 'NIC 流水线', ldst_nic), ('线路回程', '线路', link_ns),
            ('NIC 响应接收', 'NIC 流水线', ldst_nic), ('片上总线完成', '片上总线', membus_ns)],
        'ub_urma': [
            ('接口库提交', '软件提交', verb_post_ns), ('构造请求项', '软件提交', wqe_construct_ns),
            ('片上总线提交', '片上总线', membus_ns), ('NIC 发送流水线', 'NIC 流水线', urma_nic),
            ('线路去程', '线路', link_ns), ('NIC 接收流水线', 'NIC 流水线', urma_nic),
            ('目标片上总线到内存', '片上总线', membus_ns), ('目标 DRAM 行命中', '内存与完成', dram_row_ns),
            ('NIC 响应流水线', 'NIC 流水线', urma_nic), ('线路回程', '线路', link_ns),
            ('NIC 响应接收', 'NIC 流水线', urma_nic), ('片上总线完成', '片上总线', membus_ns),
            ('片上完成队列轮询', '内存与完成', cqe_poll_onchip_ns), ('接口库轮询', '内存与完成', verb_poll_ns)],
        'roce_dma': [
            ('接口库提交', '软件提交', verb_post_ns), ('构造请求项', '软件提交', wqe_construct_ns),
            ('门铃 MMIO 写', 'PCIe 穿越', pcie_mmio_ns), ('DMA 读取请求项', 'PCIe 穿越', pcie_dma_read_ns),
            ('NIC 发送流水线', 'NIC 流水线', roce_nic), ('线路去程', '线路', link_ns),
            ('NIC 接收流水线', 'NIC 流水线', roce_nic), ('目标 NIC DMA 读主机内存', 'PCIe 穿越', pcie_dma_read_ns),
            ('目标 DRAM 行命中', '内存与完成', dram_row_ns), ('NIC 响应流水线', 'NIC 流水线', roce_nic),
            ('线路回程', '线路', link_ns), ('NIC 响应接收', 'NIC 流水线', roce_nic),
            ('响应载荷 DMA 写', 'PCIe 穿越', pcie_dma_write_ns), ('完成项 DMA 写', 'PCIe 穿越', pcie_dma_write_ns),
            ('主机完成队列轮询', '内存与完成', cqe_poll_host_ns), ('接口库轮询', '内存与完成', verb_poll_ns),
            ('序号串行化', '内存与完成', psn_serialize_ns)]}
    groups = ['软件提交', 'PCIe 穿越', '片上总线', 'NIC 流水线', '线路', '内存与完成']
    round_trip = {}
    for stack, rows in phases.items():
        total = sum(Fraction(v) for _, _, v in rows)
        wire = sum(Fraction(v) for _, g, v in rows if g == '线路')
        group_ns = {g: float(sum(Fraction(v) for _, gg, v in rows if gg == g)) for g in groups}
        round_trip[stack] = dict(phases=[dict(phase=p, group=g, ns=round(float(v), 2)) for p, g, v in rows],
                                 group_ns={g: round(v, 2) for g, v in group_ns.items()}, total_ns=round(float(total), 1), fixed_ns=round(float(total - wire), 1),
                                 paper_measured_ns=PAPER_MEASURED_NS[stack],
                                 link_sweep=[dict(link_ns=L, total_ns=round(float(total - wire + 2 * L), 1)) for L in link_sweep_ns])
    pcie_total = round_trip['roce_dma']['group_ns']['PCIe 穿越']

    # 4. Latency against active endpoint count: base round trip plus refetch once the cache spills.
    sweep_points = sorted({1, 2, 4, 8, 16, roce_spill - 1, roce_spill, 32, 64, 128, 256, 512, 1024, 2048, 4096,
                           ub_spill - 1, ub_spill})
    cache_sweep = [dict(endpoints=n,
                        ub_loadstore_ns=round_trip['ub_loadstore']['total_ns'] + (ub_refetch if ub_state(n, n) > context_cache_bytes else 0),
                        roce_dma_ns=round_trip['roce_dma']['total_ns'] + (roce_refetch if roce_state(n, n) > context_cache_bytes else 0))
                   for n in sweep_points]

    # 5. Hosts in one fabric: A endpoints on every host, all-to-all.
    a = apps_per_host

    def ub_host(h):
        return a * (jetty_bytes + segment_bytes) + (h - 1) * channel_bytes

    def roce_host(h):
        return a * a * (h - 1) * qp_bytes + a * segment_bytes

    def directory_host(h):
        return directory_lines * (Fraction(h - 1, 8) + directory_tag_bytes)

    host_rows = [dict(hosts=h, ub_bytes=ub_host(h), roce_bytes=roce_host(h), directory_bytes=float(directory_host(h)),
                      ub_cache_share=round(ub_host(h) / context_cache_bytes, 4), roce_cache_share=round(roce_host(h) / context_cache_bytes, 2))
                 for h in host_counts]
    roce_max_hosts = (context_cache_bytes - a * segment_bytes) // (a * a * qp_bytes) + 1 if context_cache_bytes >= a * segment_bytes else 0
    ub_max_hosts = (context_cache_bytes - a * (jetty_bytes + segment_bytes)) // channel_bytes + 1 if context_cache_bytes >= a * (jetty_bytes + segment_bytes) else 0

    # 6. Bringing up N × N relations: per-object control operations.
    def roce_setup(n):
        return n * n * (4 * ioctl_ns + oob_rtt_ns)

    def ub_setup(n):
        return n * ioctl_ns + n * (ioctl_ns + oob_rtt_ns)

    setup_rows = [dict(endpoints=n, roce_objects=n * n, ub_objects=2 * n, roce_serial_s=roce_setup(n) / 1e9,
                       ub_serial_s=ub_setup(n) / 1e9, roce_parallel_s=roce_setup(n) / 1e9 / setup_cores,
                       ub_parallel_s=ub_setup(n) / 1e9 / setup_cores, ratio=round(roce_setup(n) / ub_setup(n), 1))
                  for n in endpoint_counts]

    # 7. Request rate from the slowest pipeline stage.
    ub_interval = ub_initiation_interval_cycles * cycle_ns
    roce_interval = roce_cycles_per_request * cycle_ns
    throughput = {k: round(float(v), 2) for k, v in dict(ub_interval_ns=ub_interval, roce_interval_ns=roce_interval,
                      ub_requests_per_us=1000 / ub_interval, roce_requests_per_us=1000 / roce_interval,
                      ub_GBps_64B=64 / ub_interval, roce_GBps_64B=64 / roce_interval,
                      ub_GBps_4KiB=4096 / ub_interval, roce_GBps_4KiB=4096 / roce_interval).items()}

    # 8. Ordering surface, converted from cycles.
    ordering = dict(gating_max_ns=round(float(gating_max_cycles * cycle_ns), 1),
                    eight_requests_four_initiators_ns=round(float(isolation_release_cycles * cycle_ns), 1),
                    roce_eighth_in_order_ns=round(float((roce_pipeline_cycles + 7 * roce_cadence_cycles) * cycle_ns), 1))

    # 9. Fixed silicon cost against the per-operation PCIe budget it removes.
    cost = dict(ub_lut_share=round(ub_luts / fpga_luts, 4), roce_lut_share=round(roce_luts / fpga_luts, 4),
                lut_ratio=round(ub_luts / roce_luts, 2), bram_ratio=round(ub_bram / roce_bram, 2) if roce_bram else None,
                flipflop_ratio=round(ub_flipflops / roce_flipflops, 2) if roce_flipflops else None,
                extra_cold_cycles=ub_cold_cycles - roce_cold_cycles,
                extra_cold_ns=round(float((ub_cold_cycles - roce_cold_cycles) * cycle_ns), 1),
                extra_cold_share_of_one_dma_read=round(float((ub_cold_cycles - roce_cold_cycles) * cycle_ns) / pcie_dma_read_ns, 3))

    top = state_rows[-1]
    summary = dict(endpoints_max=top['endpoints'], ub_state_bytes_max=top['ub_bytes'], roce_state_bytes_max=top['roce_bytes'],
                   state_ratio_max=top['ratio'], roce_spill_endpoints=roce_spill, ub_spill_endpoints=ub_spill,
                   roce_refetch_ns=roce_refetch, ub_refetch_ns=ub_refetch,
                   ub_loadstore_round_trip_ns=round_trip['ub_loadstore']['total_ns'],
                   ub_urma_round_trip_ns=round_trip['ub_urma']['total_ns'],
                   roce_dma_round_trip_ns=round_trip['roce_dma']['total_ns'],
                   roce_pcie_ns=pcie_total, round_trip_ratio=round(round_trip['roce_dma']['total_ns'] / round_trip['ub_loadstore']['total_ns'], 2),
                   apps_per_host=a, roce_max_hosts_in_cache=roce_max_hosts, ub_max_hosts_in_cache=ub_max_hosts,
                   roce_setup_parallel_s_max=setup_rows[-1]['roce_parallel_s'], ub_setup_parallel_s_max=setup_rows[-1]['ub_parallel_s'],
                   setup_ratio_max=setup_rows[-1]['ratio'], ub_requests_per_us=throughput['ub_requests_per_us'],
                   roce_requests_per_us=throughput['roce_requests_per_us'], ub_lut_share=cost['ub_lut_share'],
                   extra_cold_ns=cost['extra_cold_ns'])
    return dict(schema_version=1, calculation='ub-fabric', scenario=scenario, sources=evidence(),
                state=state_rows, cache=dict(context_cache_bytes=context_cache_bytes, roce_spill_endpoints=roce_spill,
                                             ub_spill_endpoints=ub_spill, roce_refetch_ns=roce_refetch, ub_refetch_ns=ub_refetch,
                                             paper_cache_entries=PAPER_CACHE_ENTRIES, sweep=cache_sweep),
                round_trip=round_trip, groups=groups, hosts=host_rows, setup=setup_rows, throughput=throughput,
                ordering=ordering, cost=cost, summary=summary,
                assumptions=[
                    '每条记录的字节数取自 OpenURMA 实现的状态结构（Jetty 20 B、内存段 32 B、TP 通道 56 B）与其 RoCE RC 对照的 QP 上下文 512 B；同类字段的正式规范可能更大，比例的量级不变。',
                    '端点状态按 N 个本地端点访问 M=N 个远端端点的全连接计算：UB 为 N(Jetty+段)+M×通道，RoCE 为 N×M×QP+N×段。这是可共享的核心硬件状态，不含页表、未完成请求和软件映射。',
                    '上下文缓存按字节容量判断是否溢出；论文仿真器按条目数（RoCE 512 条 QP、UB 2048 条通道）判断，因此 UB 的溢出点在论文中为 1024 端点，这里为字节口径的结果。溢出后每次操作在两端各多一次上下文重取。',
                    '一次 64 B 远程读取的各阶段延迟为声明值：片上总线 30 ns、PCIe MMIO 150 ns、PCIe DMA 读 500 ns、写 250 ns、线路单程 100 ns，NIC 流水线按周期数乘 322 MHz 时钟。各阶段全部串行在关键路径上；论文仿真值作为对照记录，不参与推导。',
                    '主机数算例假设每台主机 A 个应用端点、主机之间全连接，每台主机的 NIC 只保存自己发起方向的状态；目录式一致互联按每缓存行为每个对端保留 1 bit 加固定标签计算。',
                    '连接建立按每个对象的控制操作计数：RoCE 每条 QP 需 4 次系统调用与 1 次带外往返，UB 每个 Jetty 1 次系统调用、每条通道 1 次系统调用与 1 次往返；并行核数只把串行总时间等分，不建模内核锁竞争。',
                    '请求速率由流水线最慢级的启动间隔决定，UB 取 II=2 周期；RoCE 取每请求 6 周期的序号分配依赖。面积与周期数为论文报告的综合结果，不是推导值，用来与推导出的每操作节省作比较。',
                ])
