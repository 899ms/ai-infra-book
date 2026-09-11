"""Energy per byte by memory level applied to one Qwen3-8B decode step, plus voltage, power-density, rack and phone rows.

Book-derived byte counts are read from results/qwen3-8b-decode-b1-s8192.json (the chapter 2/4 8K
single-request decode step): weight_read_once_per_operator_bytes (~15.14 GB),
kv_existing_history_unique_payload_bytes (~1.208 GB at 8192 tokens) and matrix_flops (~19.97 GFLOPs);
the chapter-1 2048-token KV row (~0.302 GB) is kv_bytes_per_token_per_request x 2048 from the same file.
Per-level energy per byte, the phone LPDDR5X pin rate and the MELTing-point measured energy per token
are read from research/gap-plan-2026-09-11/sources-extract.json (sources[id].values[]), each row carrying
its archived text file, line, date and process node:
- shared/L1 and L2: references/text/dally-hotchips2023.txt lines 697 and 690 ("5pJ/word" local SRAM, "50pJ/word"
  on-chip SRAM; the table states its energies come from Horowitz ISSCC 2014, 45 nm), 32-bit words.
- HBM: references/text/fgdram-micro17.txt line 124 ("The energy to access a bit in HBM2 is approximately 3.97 pJ/bit").
- NVLink: references/text/nvidia-grace-hopper-blog.txt ("NVLink-C2C also only uses 1.3 picojoules per bit").
- compute: references/text/dally-hotchips2023.txt line 204 ("HFMA 1.5pJ", 45 nm), one FMA = 2 FLOPs.
- register file and NIC energy per byte: not stated in any archived source, so those levels are absent.
- phone: references/text/micron-lpddr5x-page.txt line 273 ("top speed grade of 10.7 Gbps") per pin, x16 channel;
  channel count is declared because the SoC briefs do not state the bus width.
- MELTing point: references/text/melting-point.txt lines 1514-1515 (0.21/0.20/0.16 mWh per token) and line 2197.
- rack air cooling: references/text/ashrae-liquid-cooling.txt states no explicit rack limit (only 40-50 kW rack
  airflow versus a 1900 cfm floor tile), so any ceiling is a declared_ input.  Voltage scaling and power density follow case-studies/logicfolding-energy.md, quoting
references/text/logicfolding-energy.txt line 219 ("voltage could be reduced from 0.85 V to 0.55 V") and
lines 224-226 ("does the same work with 25% less power, but power density ... rose 24% ... folding
shrank the DSP's footprint by 40%").  The rack model is chapter 6.5.2 equation (6-11):
N <= floor((P_b - P_0)/P_c) with P_b = 120 kW, P_0 = 12 kW, P_c = 1.2 kW.
"""
from fractions import Fraction
import json

from ..declared import exact, input_sources as _sources
from ..paths import BOOK, PROJECT
from ..units import positive_int

LEVELS = ('register', 'shared_l1', 'l2', 'hbm', 'nvlink', 'nic')

# (level, source id in sources-extract.json, value name, conversion to pJ per byte)
# pJ/word rows are 32-bit words (Horowitz ISSCC 2014 table as reproduced in Dally's Hot Chips 2023 keynote);
# pJ/bit rows are multiplied by 8.  Register-file and NIC energy per byte are not stated in any archived
# source (ConnectX-7 datasheet gives no power figure), so those levels stay absent.
LEVEL_ROWS = (
    ('shared_l1', 'dally-hotchips2023', 'Local SRAM (KB level) access', Fraction(1, 4)),
    ('l2', 'dally-hotchips2023', 'On-chip SRAM (MB level) access', Fraction(1, 4)),
    ('hbm', 'fgdram-micro17', 'HBM2 access energy (total)', Fraction(8)),
    ('nvlink', 'nvidia-grace-hopper-blog', 'NVLink-C2C energy per bit', Fraction(8)),
)
REFERENCE_ROWS = (
    ('dram_lpddr_45nm', 'dally-hotchips2023', 'LPDDR DRAM (GB level) access', Fraction(1, 4)),
    ('dram_access_dally_aha', 'dally-aha2023', 'DRAM access energy of which the above is a part', Fraction(8)),
    ('hbm2_including_ecc', 'fgdram-micro17', 'HBM2 access energy incl. ECC', Fraction(8)),
    ('gddr5', 'fgdram-micro17', 'GDDR5 access energy (Figure 1a label)', Fraction(8)),
    ('on_die_wire_48mm_round_trip', 'dally-aha2023', 'on-die wire energy', Fraction(8 * 48, 100)),
)
COMPUTE_ROW = ('dally-hotchips2023', 'HFMA energy', Fraction(1, 2))  # one FMA = 2 FLOPs


def _extract(path):
    file = PROJECT / path
    if not file.is_file():
        file = BOOK / path  # the extract lives in the book repository, beside references/
    if not file.is_file():
        return None
    data = json.loads(file.read_text())
    if not isinstance(data, dict) or not isinstance(data.get('sources'), dict):
        raise ValueError('sources-extract.json must contain a sources object')
    return data


def _lookup(extract, source_id, name):
    source = extract['sources'].get(source_id)
    if not source:
        return None
    for row in source.get('values', []):
        if row.get('name') == name and row.get('value') not in (None, 'not stated'):
            return dict(row, source_id=source_id, date=source.get('date'), process_node=source.get('process_node'),
                        archive_file=source.get('text'))
    return None


def _pj_rows(extract, table):
    rows = {}
    if not extract:
        return rows
    for level, source_id, name, factor in table:
        row = _lookup(extract, source_id, name)
        if row is None:
            continue
        value = exact(str(row['value']), f'{source_id}:{name}')
        rows[level] = dict(pj_per_byte_exact=str(value * factor), pj_per_byte=float(value * factor),
                           quoted_value=row['value'], quoted_unit=row.get('unit'), conversion_factor_exact=str(factor),
                           quote=row.get('quote'), source=row['archive_file'], file=row.get('file'), line=row.get('line'),
                           page=row.get('page'), date=row.get('date'), process_node=row.get('process_node'),
                           note=row.get('note'))
    return rows


def calculate(decode_result='results/qwen3-8b-decode-b1-s8192.json', chapter1_context_tokens=2048,
              sources_extract='research/gap-plan-2026-09-11/sources-extract.json',
              voltage_before='0.85', voltage_after='0.55', power_after_over_before='0.75', area_after_over_before='0.60',
              rack_budget_kw='120', rack_fixed_kw='12', rack_per_card_kw='1.2', rack_card_counts=(64, 72, 96),
              declared_air_cooling_kw_per_rack=None, declared_phone_channels_x16=4, input_sources=None):
    inputs = {k: v for k, v in locals().items() if k != 'input_sources'}
    sources = _sources(inputs, input_sources)
    positive_int(chapter1_context_tokens, 'chapter1_context_tokens')
    positive_int(declared_phone_channels_x16, 'declared_phone_channels_x16')
    decode_path = PROJECT / decode_result
    decode = json.loads(decode_path.read_text())
    summary = decode['summary']
    weight_bytes = summary['weight_read_once_per_operator_bytes']
    kv_bytes = summary['kv_existing_history_unique_payload_bytes']
    flops = summary['matrix_flops']
    per_token = summary['kv_bytes_per_token_per_request']
    kv_2k = per_token * chapter1_context_tokens
    step = dict(result_file=decode_result, scenario=decode['scenario'], weight_read_bytes=weight_bytes,
                kv_read_bytes=kv_bytes, kv_read_bytes_at_chapter1_context=kv_2k, matrix_flops=flops,
                weight_plus_kv_bytes=weight_bytes + kv_bytes)
    extract = _extract(sources_extract)
    levels = _pj_rows(extract, LEVEL_ROWS)
    references = _pj_rows(extract, REFERENCE_ROWS)
    compute = None
    if extract:
        row = _lookup(extract, COMPUTE_ROW[0], COMPUTE_ROW[1])
        if row is not None:
            per_fma = exact(str(row['value']), 'HFMA energy')
            pj_flop = per_fma * COMPUTE_ROW[2]
            compute = dict(pj_per_flop_exact=str(pj_flop), pj_per_flop=float(pj_flop), quoted_value=row['value'],
                           quoted_unit='pJ per HFMA (2 FLOPs)', quote=row.get('quote'), source=row['archive_file'],
                           line=row.get('line'), page=row.get('page'), process_node=row.get('process_node'),
                           joules=float(pj_flop * flops / 10**12))
    joules = None
    if levels:
        ladder = {}
        for level, row in {**levels, **references}.items():
            pj = Fraction(row['pj_per_byte_exact'])
            ladder[level] = dict(pj_per_byte_exact=row['pj_per_byte_exact'], source=row['source'], line=row['line'],
                                 weight_read_joules=float(pj * weight_bytes / 10**12),
                                 kv_read_joules=float(pj * kv_bytes / 10**12),
                                 kv_read_joules_at_chapter1_context=float(pj * kv_2k / 10**12),
                                 weight_plus_kv_joules=float(pj * (weight_bytes + kv_bytes) / 10**12))
        joules = dict(by_level_if_all_bytes_came_from_that_level=ladder, compute=compute)
        if 'hbm' in levels:
            hbm = Fraction(levels['hbm']['pj_per_byte_exact'])
            split = dict(weight_joules=float(hbm * weight_bytes / 10**12), kv_joules=float(hbm * kv_bytes / 10**12),
                         kv_joules_at_chapter1_context=float(hbm * kv_2k / 10**12),
                         compute_joules=compute['joules'] if compute else None, compute_included=compute is not None)
            split['total_joules_per_token'] = split['weight_joules'] + split['kv_joules'] + (split['compute_joules'] or 0.0)
            split['weight_fraction'] = split['weight_joules'] / split['total_joules_per_token']
            split['hbm_source'] = levels['hbm']['source']
            joules['per_token_split_weights_kv_compute'] = split
    v0, v1 = exact(voltage_before, 'voltage_before'), exact(voltage_after, 'voltage_after')
    ratio = (v1 / v0) ** 2
    power = exact(power_after_over_before, 'power_after_over_before')
    area = exact(area_after_over_before, 'area_after_over_before')
    density = power / area
    budget, fixed, per_card = (exact(rack_budget_kw, 'rack_budget_kw'), exact(rack_fixed_kw, 'rack_fixed_kw'),
                               exact(rack_per_card_kw, 'rack_per_card_kw'))
    max_cards = int((budget - fixed) // per_card)
    rack_rows = []
    for count in rack_card_counts:
        positive_int(count, 'rack card count')
        total = fixed + count * per_card
        row = dict(cards=count, power_kw_exact=str(total), power_kw=float(total), within_budget=total <= budget)
        if declared_air_cooling_kw_per_rack is not None:
            ceiling = exact(declared_air_cooling_kw_per_rack, 'declared_air_cooling_kw_per_rack')
            row['within_declared_air_cooling'] = total <= ceiling
        rack_rows.append(row)
    rack = dict(formula='N <= floor((P_b - P_0)/P_c)', budget_kw=str(budget), fixed_kw=str(fixed), per_card_kw=str(per_card),
                max_cards=max_cards, rows=rack_rows, declared_air_cooling_kw_per_rack=declared_air_cooling_kw_per_rack,
                max_cards_under_air_cooling=(int((exact(declared_air_cooling_kw_per_rack, 'air') - fixed) // per_card)
                                             if declared_air_cooling_kw_per_rack is not None else None))
    phone = None
    if extract:
        pin = _lookup(extract, 'micron-lpddr5x-page', 'LPDDR5X top data rate')
        soc = _lookup(extract, 'qualcomm-8elite-brief', 'LPDDR5X speed')
        phone = dict(lpddr5x_pin_rate=pin, soc_memory_clock=soc, declared_phone_channels_x16=declared_phone_channels_x16)
        if pin is not None:
            rate = exact(str(pin['value']), 'LPDDR5X pin rate') * 10**9  # bit/s per pin
            channel = rate * 16 / 8
            bus = channel * declared_phone_channels_x16
            phone.update(x16_channel_bytes_per_second_exact=str(channel), x16_channel_gb_per_second=float(channel / 10**9),
                         declared_bus_bits=16 * declared_phone_channels_x16,
                         bus_bytes_per_second_exact=str(bus), bus_gb_per_second=float(bus / 10**9),
                         weight_read_seconds_for_decode_step=float(Fraction(weight_bytes) / bus),
                         note='bus width of the phone SoC is not stated in the archived briefs; channel count is declared')
        melting = []
        for name in ('energy per token, Zephyr-3B 4-bit, six-prompt conversation',
                     'Table 6: Orin AGX @50W, Llama2-7B q4_k, llama.cpp CPU'):
            row = _lookup(extract, 'melting-point', name)
            if row is not None:
                melting.append(dict(name=name, value=row['value'], unit=row.get('unit'), quote=row.get('quote'),
                                    source=row['archive_file'], line=row.get('line'), page=row.get('page')))
        mwh_rows = {'S23/MLCChat': '0.21', 'iPhone 14 Pro/MLCChat': '0.20', 'iPhone 14 Pro/LLMFarm': '0.16'}
        if melting:
            phone['melting_point_reference_rows'] = melting
            phone['melting_point_joules_per_token'] = {k: float(Fraction(v) * Fraction(36, 10)) for k, v in mwh_rows.items()}
            phone['mwh_to_joule'] = '1 mWh = 3.6 J'
    air = None
    if extract:
        air = dict(explicit_limit=_lookup(extract, 'ashrae-liquid-cooling', 'explicit rack-level air-cooling power limit'),
                   airflow_statement=_lookup(extract, 'ashrae-liquid-cooling', 'airflow of a 40–50 kW rack vs floor tile'),
                   fan_power_statement=_lookup(extract, 'ashrae-liquid-cooling', 'fan power share in a 50 kW rack'),
                   superpod_rack_power=_lookup(extract, 'dgx-superpod-h100-ra', 'rack power in example SU layout'),
                   dgx_h200_system_power=_lookup(extract, 'nvidia-dgx-h200-datasheet', 'system power (standard)'))
    rack['air_cooling_references'] = air
    split = (joules or {}).get('per_token_split_weights_kv_compute') or {}
    summary = dict(weight_read_bytes=weight_bytes, kv_read_bytes=kv_bytes, kv_read_bytes_at_chapter1_context=kv_2k,
                   matrix_flops=flops, extract_present=extract is not None,
                   hbm_pj_per_byte=levels['hbm']['pj_per_byte'] if 'hbm' in levels else None,
                   joules_per_token_weights=split.get('weight_joules'), joules_per_token_kv=split.get('kv_joules'),
                   joules_per_token_compute=split.get('compute_joules'), joules_per_token_total=split.get('total_joules_per_token'),
                   dynamic_power_ratio=float(ratio), power_density_ratio=float(density), rack_max_cards=max_cards,
                   phone_bus_gb_per_second=(phone or {}).get('bus_gb_per_second'))
    return dict(schema_version=1, calculation='energy-ledger', scenario=inputs, declared_input_sources=sources, summary=summary,
                sources_extract=dict(path=sources_extract, present=extract is not None,
                                     generated=extract.get('generated') if extract else None,
                                     levels_present=sorted(levels), levels_absent=[l for l in LEVELS if l not in levels],
                                     compute_present=compute is not None, phone_present=phone is not None),
                decode_step=step, energy_per_byte=levels, energy_per_byte_references=references, joules_per_token=joules,
                voltage_scaling=dict(formula='P_dynamic ~ alpha C V^2 f; only the V^2 term changes',
                                     before_v=str(v0), after_v=str(v1), dynamic_power_ratio_exact=str(ratio),
                                     dynamic_power_ratio=float(ratio), reduction_fraction=float(1 - ratio),
                                     paper_reported_power_reduction='66% (logicfolding-energy.txt line 219; includes wiring changes, not voltage alone)'),
                power_density=dict(power_ratio=str(power), projected_area_ratio=str(area),
                                   density_ratio_exact=str(density), density_ratio=float(density),
                                   paper_reported_density_increase='24% (lines 224-226)'),
                rack=rack, phone=phone,
                assumptions=[
                    '一步 decode 的权重、KV 读取字节与矩阵 FLOPs 直接读取已有结果文件，本模块不重算前向；第 1 章的 2048 token KV 行按同一文件的每 token 字节乘 2048。',
                    '各层次每字节能耗、每 FLOP 能耗、手机总线与 MELTing point 参考行只在 sources-extract.json 存在且给出该行时出现，附带其 node/date/source；缺失时对应字段为空，不用占位数。',
                    '按层次的 J/token 阶梯是"若全部字节都来自该层次"的对照，不是真实数据路径；权重/KV/计算三分账按 HBM 每字节能耗与每 FLOP 能耗相加，不含控制、时钟或静态功耗。',
                    '电压项只解释 V^2 的影响，不能单独复现论文的 66%；功率密度用投影面积，不与各层硅面积之和混用。',
                    '机柜线性功率模型与第 6.5.2 节一致；风冷上限为声明输入（来自归档冷却指南时在场景中注明来源），缺省时不做判断。',
                ])
