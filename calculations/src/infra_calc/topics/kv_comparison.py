"""Compare growth, resident history and per-layer decode reads in explicit layouts."""
from fractions import Fraction
from ..sources import model_config, provenance, read_source
from ..units import positive_int
from . import state


def calculate(length=8192, batch=1):
    positive_int(length,'length'); positive_int(batch,'batch')
    rows, sources, skipped = [], [], []

    def add(model, layout, slope, global_bytes, local_bytes=0, recurrent=0, conv=0,
            main_read=0, index_read=0, append=0, write=0, note='', recurrence_read=None):
        rows.append(dict(model=model,layout=layout,
            global_growth_bytes_per_token_per_request=str(Fraction(slope)),
            global_history_bytes=batch*global_bytes, local_window_bytes=batch*local_bytes,
            recurrent_state_bytes=batch*recurrent, convolution_state_bytes=batch*conv,
            accounted_resident_bytes=batch*(global_bytes+local_bytes+recurrent+conv),
            next_token_resident_growth_bytes=batch*append,
            next_token_cache_write_bytes=batch*write,
            decode_main_history_read_bytes=batch*main_read,
            decode_index_history_read_bytes=batch*index_read,
            decode_recurrent_read_bytes=batch*(recurrent if recurrence_read is None else recurrence_read),
            decode_recurrent_write_bytes=batch*recurrent,
            decode_conv_read_once_bytes=batch*conv,
            decode_selected_history_read_bytes=batch*(main_read+index_read),
            note=note))

    models=['qwen3-8b','qwen3-32b','qwen3-30b-a3b','qwen3-235b-a22b',
            'deepseek-r1-distill-llama-70b','qwen3.5-397b-a17b','qwen3.6-35b-a3b',
            'deepseek-v3','kimi-k3','deepseek-v4-flash','deepseek-v4-pro','deepseek-v4.1-flash']
    for model in models:
        root=model_config(model); c=root.get('text_config',root)
        if length>c['max_position_embeddings']:
            skipped.append(dict(model=model,reason='length exceeds pinned max_position_embeddings'))
            continue
        sources += provenance(model)
        kind=c['model_type']
        if kind in ('qwen3','qwen3_moe','llama'):
            d=c.get('head_dim',c['hidden_size']//c['num_attention_heads'])
            unit=2*c['num_hidden_layers']*c['num_key_value_heads']*d*2
            add(model,'BF16 GQA',unit,length*unit,main_read=length*unit,append=unit,write=unit,
                note='2 × layers × KV heads × head_dim × 2B; one logical K/V read per layer, no multiplier by query heads.')
        elif model in ('qwen3.5-397b-a17b','qwen3.6-35b-a3b'):
            full=c['layer_types'].count('full_attention'); linear=c['layer_types'].count('linear_attention')
            unit=full*2*c['num_key_value_heads']*c['head_dim']*2
            recurrent=linear*c['linear_num_value_heads']*c['linear_key_head_dim']*c['linear_value_head_dim']*4
            width=2*c['linear_num_key_heads']*c['linear_key_head_dim']+c['linear_num_value_heads']*c['linear_value_head_dim']
            conv=linear*width*c['linear_conv_kernel_dim']*2
            add(model,'BF16 full KV + FP32 recurrent',unit,length*unit,recurrent=recurrent,conv=conv,
                main_read=length*unit,append=unit,write=unit,
                note=f'{full} full-attention / {linear} linear layers. Linear recurrence is fixed state, read and written each step; BF16 convolution slots counted separately, implementation movement not inferred.')
        elif model=='deepseek-v3':
            unit=c['num_hidden_layers']*(c['kv_lora_rank']+c['qk_rope_head_dim'])*2
            add(model,'BF16 compact MLA',unit,length*unit,main_read=length*unit,append=unit,write=unit,
                note='Declared absorbed MLA layout; latent and RoPE stored once, not expanded K/V. No DSA indexer in V3.')
        elif model=='kimi-k3':
            for path in ('compact','expanded'):
                r=state.k3_state(c,length,1,2,4,path); x=r['components']; unit=r['summary']['next_token_mla_append_bytes']
                add(model,f'BF16 {path} MLA + FP32 KDA',unit,x['mla_history_bytes'],recurrent=x['kda_recurrent_bytes'],conv=x['short_conv_slots_bytes'],
                    main_read=x['mla_history_bytes'],append=unit,write=unit,
                    note='24 MLA + 69 KDA; compact is declared absorbed execution, expanded matches pinned HF cache. KDA fixed state and short convolution must not be described as per-token-growing KV.')
        elif model.startswith('deepseek-v4-'):
            ratios=c['compress_ratios'][:c['num_hidden_layers']]; h=c['head_dim']; d=c['index_head_dim']; win=c['sliding_window']
            for label,entry,index in [('BF16 reference',h*2,d*2),('FP8/BF16 main + MXFP4 index',584,68)]:
                slope=sum((Fraction(entry+(index if ratio==4 else 0),ratio) for ratio in ratios if ratio),Fraction())
                def size(n):return sum(n//r*(entry+(index if r==4 else 0)) for r in ratios if r)
                main=sum((min(length,win)+(min(length//r,c['index_topk']) if r==4 else length//r if r else 0))*entry for r in ratios)
                scan=sum(length//r*index for r in ratios if r==4)
                local=len(ratios)*min(length,win)*entry
                growth=size(length+1)-size(length)
                window_growth=len(ratios)*entry if length<win else 0
                add(model,label,slope,size(length),local_bytes=local,main_read=main,index_read=scan,
                    append=growth+window_growth,write=growth+len(ratios)*entry,
                    note='CSA top-k main read plus full index scan; HCA reads all compressed entries. Shared latent counted once per attention layer for QK/PV. Compressor buffers/updates excluded. Production main 584B includes scale padding; reference is BF16.')
        elif model=='deepseek-v4.1-flash':
            read_source('sources/deepseek-v4.1-flash/FlashMLA-README.md')
            ratios=c['compress_ratios'][:c['num_hidden_layers']]; owners=c['kv_source_layer_ids']; indexers=c['index_source_layer_ids']; win=c['sliding_window']
            def size(n):return sum(n//ratios[l]*(288+68) for l in owners)
            main=sum(min(length,win)*528+(min(length//r,c['index_topk'])*288 if r else 0) for r in ratios)
            cap=c['candidate_topk_blocks']*c['candidate_block_size']
            scan=sum((length//ratios[l] if l<=c['candidate_source_layer_id'] else min(length//ratios[l],cap))*68 for l in indexers)
            reference_scan=sum(length//ratios[l]*c['index_head_dim']*2 for l in indexers)
            growth=size(length+1)-size(length); window_growth=len(ratios)*528 if length<win else 0
            add(model,'FP4 global + FP8 SWA + MXFP4 index',sum(Fraction(356,ratios[l]) for l in owners),size(length),local_bytes=len(ratios)*min(length,win)*528,
                main_read=main,index_read=scan,append=growth+window_growth,write=growth+len(ratios)*528,
                note=f'4 KV owners, 8 indexing layers, 30 reuse layers; production candidate-limited index read (<= {cap} entries for later indexers). Per-layer logical reads count shared cache repeatedly; unique union/actual HBM unknown. Released reference scans full BF16 index before masking ({batch*reference_scan} B), unlike production selective read. Compressor/candidate/top-k metadata excluded.')
        else:
            raise ValueError(f'Unhandled cache architecture: {model}')
    return dict(schema_version=1,calculation='kv-comparison',scenario=dict(length=length,batch=batch),rows=rows,skipped=skipped,
        sources=list({s['file']:s for s in sources}.values()),
        definitions=[
            'N is visible cached length for the last-position query (includes its current token); reads are a single decode query over that snapshot. Next-token growth/write refer to N→N+1. B independent equal-length requests, no prefix sharing.',
            'Global growth is asymptotic amortized bytes/token/request. Compression completion makes instantaneous growth discontinuous. Local windows overwrite slots after saturation, so writes are not resident growth.',
            'Decode main reads assume one logical fetch of each selected latent or K/V per attention layer, reused across heads and QK/PV. Index scans are additional. These are operand payloads, not measured HBM bytes: fusion, L2, tiling and cross-layer retention change physical traffic.',
            'Resident total here includes global history, effective SWA and declared recurrent/conv state only; not a complete runtime capacity budget. Compressor and allocator buffers, page metadata, candidate/top-k arrays, weights, workspaces and parallel copies are excluded.',
            'Recurrent read/write and convolution read-once payload are separate from growing history. Convolution update implementation traffic is not claimed.',
            'Precision/layout is part of each row. BF16 baselines and production compressed layouts are not equal-quality or equal-speed benchmark results. Models beyond their pinned context limit are explicitly skipped.',
            'Official V4 chart 3514 is rounded from 3514.25 B/token; V4.1 gives exactly 890 at even lengths. Their ratio is 3.9485955, not a whole-model memory or decode-speed ratio.'
        ])


def per_token_bytes(model, layout):
    """Per-token KV bytes (one request) in an explicit layout, same formulas as calculate()."""
    root=model_config(model); c=root.get('text_config',root)
    if layout=='gqa':
        if c['model_type'] not in ('qwen3','qwen3_moe','llama'):
            raise ValueError('gqa layout requires a Qwen3/Llama GQA config')
        d=c.get('head_dim',c['hidden_size']//c['num_attention_heads'])
        return 2*c['num_hidden_layers']*c['num_key_value_heads']*d*2
    if layout=='mla':
        if model!='deepseek-v3':
            raise ValueError('compact MLA layout is implemented for the locked deepseek-v3 config')
        return c['num_hidden_layers']*(c['kv_lora_rank']+c['qk_rope_head_dim'])*2
    raise ValueError('layout must be gqa or mla')


def mla_compact_extra_flops_per_token(model='deepseek-v3'):
    """Chapter 2 compact-path work per query token: query absorb (d_h x d_c) and value restore (d_c x d_v) per head, all layers."""
    c=model_config(model)
    if model!='deepseek-v3':
        raise ValueError('compact MLA extra work is implemented for the locked deepseek-v3 config')
    heads=c['num_attention_heads']; layers=c['num_hidden_layers']
    absorb=2*heads*c['qk_nope_head_dim']*c['kv_lora_rank']
    restore=2*heads*c['kv_lora_rank']*c['v_head_dim']
    return dict(layers=layers,heads=heads,d_c=c['kv_lora_rank'],d_r=c['qk_rope_head_dim'],
                query_absorb_flops_per_layer=absorb,value_restore_flops_per_layer=restore,
                extra_flops_per_token_per_layer=absorb+restore,extra_flops_per_token=(absorb+restore)*layers)


def markdown(r):
    lines=['# 跨模型 KV 存储与单次 decode 读取', '',f"B={r['scenario']['batch']}，可见长度 N={r['scenario']['length']}；所有数值为 bytes，单 token 增长列为每请求。",'',
        '| 模型 / 缓存格式 | 全局增长 B/token | 全局历史 | 固定/窗口状态 | decode 主历史读 | decode index 读 | 下个 token 容量增长 |',
        '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
    for x in r['rows']:
        lines.append(f"| {x['model']} / {x['layout']} | {format(float(Fraction(x['global_growth_bytes_per_token_per_request'])), ',.4f').rstrip('0').rstrip('.')} | {x['global_history_bytes']:,} | {x['local_window_bytes']+x['recurrent_state_bytes']+x['convolution_state_bytes']:,} | {x['decode_main_history_read_bytes']:,} | {x['decode_index_history_read_bytes']:,} | {x['next_token_resident_growth_bytes']:,} |")
    lines+=['','## 固定状态与写入（均为单次 decode、全 batch）','','| 模型 / 格式 | recurrent 读 | recurrent 写 | conv read-once | 新 KV / SWA 写 |','| --- | ---: | ---: | ---: | ---: |']
    for x in r['rows']:
        lines.append(f"| {x['model']} / {x['layout']} | {x['decode_recurrent_read_bytes']:,} | {x['decode_recurrent_write_bytes']:,} | {x['decode_conv_read_once_bytes']:,} | {x['next_token_cache_write_bytes']:,} |")
    lines+=['','## 定义与限制','']+['- '+s for s in r['definitions']]
    lines+=['','## 各路径说明','']+['- '+x['model']+' / '+x['layout']+': '+x['note'] for x in r['rows']]
    if r['skipped']:lines+=['','跳过超出配置上下文上限的模型：'+', '.join(x['model'] for x in r['skipped'])]
    return '\n'.join(lines)+'\n'
