"""Pinned V4.1 checkpoint, global-cache layout and stage-specific MoE work.

This is deliberately not the V4 forward adapter: the paper's CED serving path
and the released reference's all-layer forward are different execution scopes.
"""
import json
import struct
from collections import Counter
from math import prod

from ..sources import model_config, provenance, read_source
from ..units import positive_int
from . import v4_checkpoint

MODEL = 'deepseek-v4.1-flash'


def checkpoint():
    index = json.loads(read_source(f'sources/{MODEL}/model.safetensors.index.json'))
    sizes = {'F32': 4, 'BF16': 2, 'F8_E4M3': 1, 'F8_E8M0': 1, 'I8': 1, 'I64': 8, 'I32': 4}
    tensors, groups, parameters, scales = {}, Counter(), Counter(), Counter()
    header_bytes = 0
    for shard in sorted(set(index['weight_map'].values())):
        raw = read_source(f'sources/{MODEL}/headers/{shard}.header.bin')
        if struct.unpack('<Q', raw[:8])[0] != len(raw)-8:
            raise ValueError('Safetensors header length mismatch')
        header_bytes += len(raw)
        end_previous = 0
        entries = json.loads(raw[8:])
        for name, t in sorted(((k,v) for k,v in entries.items() if k != '__metadata__'), key=lambda item: item[1]['data_offsets'][0]):
            if name in tensors or index['weight_map'].get(name) != shard:
                raise ValueError(f'Index/shard mismatch: {name}')
            start, end = t['data_offsets']
            n = prod(t['shape'])
            if start != end_previous or end-start != n*sizes[t['dtype']]:
                raise ValueError(f'Noncontiguous or invalid tensor bytes: {name}')
            end_previous = end
            tensors[name] = t
            owner = ('dspark' if name.startswith('mtp.') else 'engram' if '.engram.' in name
                     else 'vision' if name.startswith(('vision.', 'aligner.', 'image_')) else 'backbone')
            groups[owner] += end-start
            if name.endswith('.scale'):
                scales[owner] += end-start
            else:
                if t['dtype'] == 'I8':
                    if '.ffn.experts.' not in name or not name.endswith('.weight'):
                        raise ValueError(f'Unknown packed tensor: {name}')
                    n *= 2
                parameters[owner] += n
    if tensors.keys() != index['weight_map'].keys() or sum(groups.values()) != index['metadata']['total_size']:
        raise ValueError('Checkpoint coverage/total mismatch')
    c = model_config(MODEL)['text_config']
    # Check every backbone expert against the official configuration, not labels.
    h, f = c['hidden_size'], c['moe_intermediate_size']
    for layer in range(c['num_hidden_layers']):
        for expert in range(c['n_routed_experts']):
            for projection, shape in (('w1', [f,h//2]), ('w2', [h,f//2]), ('w3', [f,h//2])):
                t = tensors[f'layers.{layer}.ffn.experts.{expert}.{projection}.weight']
                if t['shape'] != shape or t['dtype'] != 'I8':
                    raise ValueError('Expert shape/config mismatch')
    for layer, rows in zip(c['engram_layer_ids'], c['engram_num_embeddings']):
        if tensors[f'layers.{layer}.engram.embed.weight']['shape'] != [rows,c['engram_head_dim']]:
            raise ValueError('Engram shape/config mismatch')
    return dict(shards=len(set(index['weight_map'].values())), tensors=len(tensors),
                tensor_payload_bytes=sum(groups.values()), header_bytes=header_bytes,
                checkpoint_file_bytes=sum(groups.values())+header_bytes,
                bytes_by_component=dict(groups), scale_bytes_by_component=dict(scales),
                logical_parameters_by_component=dict(parameters),
                logical_parameters=sum(parameters.values()),
                validation='All indexed tensors, shard assignments, contiguous offsets and dtype/shape bytes verified; all backbone routed expert and Engram table shapes checked against config.',
                scope='Downloaded headers only; tensor values and numerical inference not validated. File storage is not runtime residency.')


def calculate(length=8192, batch=1):
    positive_int(length, 'length')
    positive_int(batch, 'batch')
    c = model_config(MODEL)['text_config']
    if length > c['max_position_embeddings']:
        raise ValueError('Length exceeds official context limit')
    old = model_config('deepseek-v4-flash')
    # Paper §2.4: main E2M1 + one E4M3 scale/16 channels;
    # index MXFP4 + one E8M0 scale/32 channels. One shared latent, no K/V x2.
    main_entry = c['head_dim']//2 + c['head_dim']//16
    index_entry = c['index_head_dim']//2 + c['index_head_dim']//32
    rows = []
    for layer in c['kv_source_layer_ids']:
        ratio = c['compress_ratios'][layer]
        entries = length//ratio
        rows.append(dict(source_layer=layer, compression_ratio=ratio, entries=entries,
                         main_bytes=batch*entries*main_entry, index_bytes=batch*entries*index_entry))
    global_bytes = sum(r['main_bytes']+r['index_bytes'] for r in rows)
    # Reference buffers use the PyTorch default (BF16 in the reference setup),
    # while the production paper describes compressed cache storage.
    reference_global = batch * sum(length//c['compress_ratios'][l] for l in c['kv_source_layer_ids']) * (c['head_dim']+c['index_head_dim'])*2
    layers, half = c['num_hidden_layers'], c['num_hidden_layers']//2
    per_layer = 2*3*c['hidden_size']*c['moe_intermediate_size']*(c['num_experts_per_tok']+c['n_shared_experts'])
    v4_per_layer = 2*3*old['hidden_size']*old['moe_intermediate_size']*(old['num_experts_per_tok']+old['n_shared_experts'])
    work = dict(
        expert_matrix_flops_per_token_per_layer=per_layer,
        decode_expert_matrix_flops=batch*layers*per_layer,
        reference_full_prefill_expert_matrix_flops=batch*length*layers*per_layer,
        ced_bounded_replay_prefill_expert_matrix_flops=batch*(length*half+min(length,c['sliding_window'])*half)*per_layer,
        ced_encoder_token_layers=batch*length*half,
        ced_decoder_replay_token_layers=batch*min(length,c['sliding_window'])*half,
        v4_decode_expert_matrix_flops=batch*old['num_hidden_layers']*v4_per_layer,
        v4_prefill_expert_matrix_flops=batch*length*old['num_hidden_layers']*v4_per_layer,
    )
    return dict(schema_version=1, calculation='v41-flash', model=MODEL,
        scenario=dict(length=length,batch=batch), sources=provenance(MODEL),
        checkpoint=checkpoint(), v4_checkpoint=v4_checkpoint.calculate('deepseek-v4-flash'),
        architecture=dict(layers=layers,encoder_layers=half,decoder_layers=half,
            full_layers=c['kv_source_layer_ids'],reindex_layers=[l for l in c['index_source_layer_ids'] if l not in c['kv_source_layer_ids']],
            reuse_layers=[l for l in range(layers) if c['compress_ratios'][l] and l not in c['index_source_layer_ids']],
            swa_only_layers=[l for l in range(layers) if not c['compress_ratios'][l]],
            engram_table_parameters=sum(c['engram_num_embeddings'])*c['engram_head_dim'],
            hidden_size=c['hidden_size'], routed_experts=c['n_routed_experts'], top_k=c['num_experts_per_tok']),
        global_cache=dict(main_entry_bytes=main_entry,index_entry_bytes=index_entry, rows=rows,
            bytes=global_bytes,bytes_per_token_at_even_lengths=890,
            reference_bf16_global_bytes=reference_global,
            swa_fp8_values_only_bytes=batch*layers*min(length,c['sliding_window'])*c['head_dim'],
            swa_fp8_with_scales_bytes=batch*layers*min(length,c['sliding_window'])*(c['head_dim']+c['head_dim']//32),
            reference_bf16_swa_allocated_bytes=batch*layers*c['sliding_window']*c['head_dim']*2),
        expert_work=work,
        coverage=dict(complete_forward=False,complete_runtime_capacity=False,measured_performance=False),
        assumptions=[
            'Global KV uses paper production FP4 formats; 3 half-rate sources + 1 full-rate source, not 40 independent caches. Odd lengths use floor per source.',
            '890 B/token includes main and index global cache only. SWA values listed separately exclude scales; compressor state, candidate/top-k buffers, allocator, replication and workspace are not included.',
            'Reference BF16 figures assume torch default BF16 and logical history length; its buffers allocate max_seq_len, which may be larger.',
            'CED prefill is the paper serving schedule with last min(N,128) decoder replay, not the released all-layer Transformer.forward. MoE subtotal excludes attention, router, Engram, mHC, output head, vision and DSpark.',
            'Every selected expert includes three matrices; FMA=2. Routing union and actual HBM traffic are not inferred from top-k.',
            'Paper rounded labels: 552B backbone + 196B Engram, 8B prefill / 16B decode activated. They are not exact checkpoint totals or latency measurements.',
            'The paper persistent-cache ~1/8 comparison depends on workload/replay policy and is not a universal capacity multiplier.'
        ])


def markdown(r):
    c, g, w = r['checkpoint'], r['global_cache'], r['expert_work']
    lines = ['# DeepSeek V4.1 Flash：权重、共享 KV 与专家工作', '',
             f"场景：B={r['scenario']['batch']}，N={r['scenario']['length']}。固定官方 revision；非完整前向或实测性能。", '',
             '| 权重组件 | 逻辑参数（不含量化 scales） | checkpoint 字节（含 scales） |', '| --- | ---: | ---: |']
    for key, value in c['bytes_by_component'].items():
        lines.append(f"| {key} | {c['logical_parameters_by_component'][key]:,} | {value:,} |")
    lines += ['', f"核对 {c['shards']} 个分片、{c['tensors']:,} 个张量；payload 共 {c['tensor_payload_bytes']:,} B，含文件头 {c['checkpoint_file_bytes']:,} B。", '',
              '| 计算项 | 结果 |','| --- | ---: |',
              f"| 全局 KV（含 index） | {g['bytes']:,} B |",
              f"| main / index 每条 entry | {g['main_entry_bytes']} / {g['index_entry_bytes']} B |",
              f"| SWA FP8 值载荷，未含 scales | {g['swa_fp8_values_only_bytes']:,} B |",
              f"| 参考 BF16 全局 KV 逻辑载荷 | {g['reference_bf16_global_bytes']:,} B |"]
    for key,value in w.items():
        lines.append(f'| {key} | {value:,} |')
    lines += ['', '## 边界与来源', ''] + ['- '+s for s in r['assumptions']]
    lines += ['', '- 官方配置、技术报告、源码、48 分片头及索引均在 `configs/sources.lock.json` 锁定。',
              '- 研究与版本选择建议：[README](../research/deepseek-v41-flash/README.md)。', '']
    return '\n'.join(lines)
