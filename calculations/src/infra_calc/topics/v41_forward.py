"""V4.1 text matrix graph, CED schedule and cache accounting from pinned sources.

FMA=2, unpadded GEMMs and valid sparse QK/PV pairs. The reference indexer
computes a rectangle before masking; the CED schedule uses causal candidate
reads. Neither is a GPU timing model. Vision/DSpark are separate entry points.
"""
from collections import Counter
from functools import lru_cache
import json
from math import prod

from ..sources import model_config, provenance, read_source
from ..units import positive_int
from . import v41_flash

MODEL = v41_flash.MODEL


@lru_cache(maxsize=1)
def parameter_inventory():
    """Check every text tensor; keep Engram separate from the ordinary FFN."""
    checked = v41_flash.checkpoint()
    index = json.loads(read_source(f'sources/{MODEL}/model.safetensors.index.json'))
    tensors, groups = {}, Counter()
    for shard in sorted(set(index['weight_map'].values())):
        header = json.loads(read_source(f'sources/{MODEL}/headers/{shard}.header.bin')[8:])
        for name, tensor in header.items():
            if name == '__metadata__' or name.endswith('.scale') or name.startswith(('mtp.', 'vision.', 'aligner.', 'image_')):
                continue
            shape = list(tensor['shape'])
            if tensor['dtype'] == 'I8':
                shape[-1] *= 2  # FP4: two logical values in each int8 container.
            tensors[name] = shape
            group = ('engram' if '.engram.' in name else
                     'embedding_head' if name in ('embed.weight', 'head.weight') else
                     'attention_projection' if '.attn.' in name and len(shape) == 2 else
                     'dense_shared_ffn' if '.ffn.shared_experts.' in name else
                     'routed_experts' if '.ffn.experts.' in name else 'other')
            groups[group] += prod(shape)
    total = sum(groups.values())
    if total != sum(checked['logical_parameters_by_component'][x] for x in ('backbone', 'engram')):
        raise ValueError('Text parameter partition does not conserve checkpoint total')
    return tensors, dict(groups), checked


def state(length, batch=1, layout='bf16'):
    """Live logical history + fixed compressor slots; no workspace/weight total.

    All four source KV/index arrays are counted once, never once per reader.
    Engram's reference token cache is included; max_seq_len reservations are
    reported separately from the currently populated length.
    """
    positive_int(length, 'length', allow_zero=True)
    positive_int(batch, 'batch')
    if layout not in ('bf16', 'production'):
        raise ValueError('layout must be bf16 or production')
    c = model_config(MODEL)['text_config']
    if length > c['max_position_embeddings']:
        raise ValueError('Length exceeds pinned context limit')
    h, d, win = c['head_dim'], c['index_head_dim'], c['sliding_window']
    main, index, local = (h*2, d*2, h*2) if layout == 'bf16' else (h//2+h//16, d//2+d//32, h+h//32)
    owners = c['kv_source_layer_ids']
    ratios = c['compress_ratios'][:c['num_hidden_layers']]
    entries = sum(length//ratios[layer] for layer in owners)
    buffers = sum(2*batch*ratios[layer]*h*4 for layer in owners if ratios[layer] > 1)
    parts = dict(global_main_bytes=batch*entries*main,
                 global_index_bytes=batch*entries*index,
                 window_bytes=batch*len(ratios)*min(length,win)*local,
                 compressor_fp32_bytes=buffers,
                 engram_token_ids_bytes=batch*length*8)
    cap=c['candidate_topk_blocks']*c['candidate_block_size']
    main_read=batch*sum(min(length,win)*local+(min(length//r,c['index_topk'])*main if r else 0) for r in ratios)
    index_read=batch*sum((min(length//ratios[l],cap) if l>c['candidate_source_layer_id'] else length//ratios[l])*index for l in c['index_source_layer_ids'])
    return dict(length=length,batch=batch,layout=layout,components=parts,
                selected_history_payload_bytes=main_read+index_read,
                resident_bytes=sum(parts.values()),
                reference_bf16_max_length_buffer_bytes=batch*(
                    sum(c['max_position_embeddings']//ratios[l] for l in owners)*(h+d)*2
                    + len(ratios)*win*h*2+c['max_position_embeddings']*8)+buffers,
                scope='Logical populated KV/index/SWA + allocated FP32 compressor slots + populated int64 Engram token IDs; excludes weights, workspace, static RoPE/token-map tables and allocator. Production changes KV encoding, retaining reference compressor/hash state for comparison.')


def calculate(batch=1, tokens=8192, history=0, execution='ced', index_algorithm=None):
    for key,value in (('batch',batch),('tokens',tokens),('history',history)):
        positive_int(value,key,allow_zero=key=='history')
    if history and tokens != 1:
        raise ValueError('Pinned reference supports fresh prefill or single-token continuation only')
    if execution not in ('reference','ced'):
        raise ValueError('execution must be reference or ced')
    index_algorithm = index_algorithm or ('reference' if execution=='reference' else 'candidate')
    if index_algorithm not in ('reference','candidate'):
        raise ValueError('index_algorithm must be reference or candidate')
    c = model_config(MODEL)['text_config']
    n = history+tokens
    if n > c['max_position_embeddings']:
        raise ValueError('Request exceeds pinned context limit')
    tensors, groups, checkpoint = parameter_inventory()
    h, f, layers, heads, width = (c[k] for k in ('hidden_size','moe_intermediate_size','num_hidden_layers','num_attention_heads','head_dim'))
    half, win, copies = layers//2,c['sliding_window'],c['hc_mult']
    owners, indexers = c['kv_source_layer_ids'],c['index_source_layer_ids']
    cap = c['candidate_topk_blocks']*c['candidate_block_size']
    replay = execution=='ced' and history==0
    decoder_start = max(0,n-win) if replay else history
    ops, schedules, used_matrices = [], [], set()

    def gemm(name, rows, in_width, out_width, repeats=1, component='attention_projection', layer=None):
        # Check mathematical matrix orientation against saved [out,in] tensors.
        expected = [out_width,in_width]
        if tensors.get(name) != expected:
            raise ValueError(f'Matrix shape mismatch: {name}: {tensors.get(name)} != {expected}')
        used_matrices.add(name)
        ops.append(dict(name=name,component=component,layer=layer,rows=rows,
                        weight_math=[in_width,out_width],repeats=repeats,
                        matrix_flops=2*rows*in_width*out_width*repeats))

    def work(name, flops, component, layer, **details):
        ops.append(dict(name=name,component=component,layer=layer,matrix_flops=flops,**details))

    for layer in range(layers):
        prefix=f'layers.{layer}.'
        start=decoder_start if layer>=half else history
        count=n-start; m=batch*count
        ratio=c['compress_ratios'][layer]
        # CED builds layer-20 global KV for ALL prompt positions only once.
        source_start=history if replay and layer==half else start
        source_count=n-source_start
        published=n//ratio-source_start//ratio if ratio else 0
        schedules.append(dict(layer=layer,stage='encoder' if layer<half else 'decoder',query_start=start,
                              query_tokens=count,global_projection_tokens=source_count if layer in owners else 0,
                              new_global_entries=published if layer in owners else 0,
                              local_window_start=start if replay and layer>=half else 0))
        if layer in c['engram_layer_ids']:
            hash_width=(c['engram_max_ngram_size']-1)*c['engram_n_heads']*c['engram_head_dim']
            gemm(prefix+'engram.wkv.weight',m,hash_width,(copies+1)*h,component='engram',layer=layer)
            # Gate dot products are source elementwise multiply/reduce, counted
            # separately below, consistent with mHC weighted reductions.
        for branch in ('attn','ffn'):
            gemm(prefix+f'hc_{branch}_fn',m,copies*h,(copies+2)*copies,component='hyper_connections',layer=layer)
        a=prefix+'attn.'
        gemm(a+'wq_a.weight',m,h,c['q_lora_rank'],layer=layer)
        gemm(a+'wq_b.weight',m,c['q_lora_rank'],heads*width,layer=layer)
        gemm(a+'wkv.weight',m,h,width,layer=layer)
        # wo_a is stored as [groups*rank, heads*width/groups], but is a
        # block-diagonal projection, NOT a dense [heads*width,groups*rank].
        gemm(a+'wo_a.weight',m,heads*width//c['o_groups'],c['o_groups']*c['o_lora_rank'],layer=layer)
        gemm(a+'wo_b.weight',m,c['o_groups']*c['o_lora_rank'],h,layer=layer)
        if layer in owners:
            gemm(a+'compressor.wkv.weight',batch*source_count,h,width,component='compressor',layer=layer)
            if ratio>1:
                gemm(a+'compressor.wgate.weight',batch*source_count,h,width,component='compressor',layer=layer)
            gemm(a+'indexer.wk.weight',batch*published,width,c['index_head_dim'],component='index_projection',layer=layer)
        window_floor=start if replay and layer>=half else 0
        pairs=sum(min(win,t-window_floor+1) for t in range(start,n))
        global_pairs=sum(min((t+1)//ratio,c['index_topk']) for t in range(start,n)) if ratio else 0
        work(a+'qk_pv',4*batch*heads*width*(pairs+global_pairs),'attention_interaction',layer,
             window_pairs_per_request=pairs,global_pairs_per_request=global_pairs)
        if layer in indexers:
            # The source skips the entire indexer when no compressed key exists.
            active=m if n//ratio else 0
            gemm(a+'indexer.wq_b.weight',active,c['q_lora_rank'],c['index_n_heads']*c['index_head_dim'],component='index_projection',layer=layer)
            gemm(a+'indexer.weights_proj.weight',active,h,c['index_n_heads'],component='index_projection',layer=layer)
            scans=(count*(n//ratio) if index_algorithm=='reference' else
                   sum(min((t+1)//ratio,cap) if layer>c['candidate_source_layer_id'] else (t+1)//ratio for t in range(start,n)))
            work(a+'index_dot',2*batch*c['index_n_heads']*c['index_head_dim']*scans,'index_interaction',layer,
                 index_pairs_per_request=scans,index_algorithm=index_algorithm)
        gemm(prefix+'ffn.gate.weight',m,h,c['n_routed_experts'],component='router',layer=layer)
        for branch,rows in [('shared_experts',m),('experts.0',m*c['num_experts_per_tok'])]:
            for proj,iw,ow in [('w1',h,f),('w3',h,f),('w2',f,h)]:
                gemm(prefix+f'ffn.{branch}.{proj}.weight',rows,iw,ow,
                     component='shared_expert' if branch=='shared_experts' else 'routed_expert',layer=layer)
                # Every expert has the same shape; total assignment rows=m*k.
                if branch=='experts.0':
                    for expert in range(c['n_routed_experts']):
                        name=prefix+f'ffn.experts.{expert}.{proj}.weight'
                        if tensors[name] != [ow,iw]:raise ValueError(f'Expert shape mismatch: {name}')
                        used_matrices.add(name)
    gemm('head.weight',batch,h,c['vocab_size'],component='vocabulary_head')
    exempt={'embed.weight'} | {name for name in tensors if '.engram.' in name and not name.endswith('.wkv.weight')}
    unmatched={name for name,shape in tensors.items() if len(shape)==2}-used_matrices-exempt
    if unmatched:raise ValueError('Unaccounted text matrices: '+str(sorted(unmatched)))
    by_component=Counter()
    for op in ops:by_component[op['component']]+=op['matrix_flops']
    nonmatrix=non_matrix_work(c,schedules,batch,n,index_algorithm)
    state_before=state(history,batch)
    state_after=state(n,batch)
    parameters=sum(groups.values())
    return dict(schema_version=1,calculation='v41-forward',model=MODEL,
                scenario=dict(batch=batch,tokens=tokens,history=history,execution=execution,index_algorithm=index_algorithm,output_head='last'),
                sources=provenance(MODEL),parameter_groups=groups,checkpoint=checkpoint,
                layer_schedule=schedules,operations=ops,non_matrix=nonmatrix,
                state_before=state_before,state_after=state_after,production_state_after=state(n,batch,'production'),
                summary=dict(logical_text_parameters=parameters,uniform_bf16_bytes=parameters*2,
                             matrix_flops=sum(by_component.values()),matrix_components=dict(by_component),
                             context_interaction_flops=by_component['attention_interaction']+by_component['index_interaction'],
                             accounted_scalar_flops=nonmatrix['scalar_flops'],special_ops=nonmatrix['special_ops'],
                             state_before_bytes=state_before['resident_bytes'],state_after_bytes=state_after['resident_bytes'],
                             selected_routed_expert_bf16_bytes=2*layers*c['num_experts_per_tok']*3*h*f,
                             engram_lookup_bytes=batch*sum(s['query_tokens'] for s in schedules if s['layer'] in c['engram_layer_ids'])*(c['engram_max_ngram_size']-1)*c['engram_n_heads']*c['engram_head_dim']*2),
                coverage=dict(text_matrix_graph=True,all_checkpoint_text_matrices_accounted=True,
                              scalar_scope='Logical norms, RoPE, gates, reductions, mHC and pooling; no quantization/backend instruction total',
                              excluded=['vision encoder/projector (text-only input)','DSpark speculative entry point (ordinary autoregressive generation)','sampling and tokenizer CPU work','quantization, sorting algorithms, compiled tile padding, actual HBM and latency']),
                assumptions=[
                    'All text parameters include Engram tables and projections; exclude vision, DSpark and quantization scales. Shapes validated against all 48 pinned checkpoint headers.',
                    'Reference: all 40 layers over fresh prompt, rectangular index einsum before causal/candidate masking. CED: 20 encoder layers over all prompt positions, decoder KV/index-key projection over all positions, 20 decoder layers over last min(P,128) positions.',
                    'CED decoder SWA replay truncates local attention to the replay segment; it reconstructs approximate states, not mathematically identical full-prefix states (paper 3.2.2). Global attention remains causal with original absolute positions.',
                    'Candidate index mode counts causally reachable entries; later decoder indexers scan at most 16384 entries. Selection/pooling comparisons are not matrix FLOPs.',
                    'One call with history>0 requires one token, matching the released source. Chunked prefix continuation and encoder cache-miss replay are not modeled by this entry point.',
                    'Matrix FLOPs use FMA=2 and effective sparse pairs; scalar/special work is reported separately. These are resource demands, not measured time or throughput.'
                ])


def non_matrix_work(c,schedules,batch,n,index_algorithm):
    """Source-level arithmetic; comparison/sort/quantization remain separate.

    Weighted reductions follow literal broadcast expressions, not GEMM FLOPs.
    """
    from .hyper_connections import sinkhorn_work
    totals, special, details = Counter(), Counter(), []
    h, copies, width = c['hidden_size'],c['hc_mult'],c['head_dim']
    def add(name,scalar=0,**functions):
        totals[name]+=scalar; special.update(functions)
    def norm(name,rows,dim):
        add(name,rows*(4*dim+1),rsqrt=rows)
    for s in schedules:
        layer=s['layer'];m=batch*s['query_tokens'];a=f'layer.{layer}.'
        norm(a+'sublayer_norms',2*m,h)
        norm(a+'q_norm',m,c['q_lora_rank']);norm(a+'local_kv_norm',m,width)
        # Q/K and inverse output RoPE: complex pair multiply = 6 real ops.
        add(a+'rope',3*c['qk_rope_head_dim']*m*(2*c['num_attention_heads']+1))
        sink=sinkhorn_work(copies,c['hc_sinkhorn_iters']);j=(copies+2)*copies
        add(a+'hc_rms_and_scale',2*m*(2*copies*h+1+j),rsqrt=2*m)
        add(a+'hc_sinkhorn',2*m*sink['scalar_flops'],**{k:2*m*v for k,v in sink['special_ops'].items()})
        add(a+'hc_pre_post',2*m*((2*copies-1)*h+(2*copies*copies+copies)*h))
        E,k,f=c['n_routed_experts'],c['num_experts_per_tok'],c['moe_intermediate_size']
        add(a+'router',m*(3*E+3*k),softplus=m*E,sqrt=m*E,topk_rows=m)
        add(a+'swiglu_and_weighting',m*((k+1)*2*f+k*f+(k+1)*h),sigmoid=m*(k+1)*f,clamp=m*(k+1)*2*f)
        if layer in c['engram_layer_ids']:
            add(a+'engram_gate',copies*h+m*copies*(9*h+6),rsqrt=2*m*copies,sqrt=m*copies,sigmoid=m*copies)
        ratio=c['compress_ratios'][layer]
        if layer in c['kv_source_layer_ids']:
            entries=batch*s['new_global_entries'];norm(a+'global_norm',entries,width)
            norm(a+'index_key_norm',entries,c['index_head_dim'])
            add(a+'global_rope',entries*6*c['qk_rope_head_dim'])
            if ratio>1:
                add(a+'pool',entries*width*(6*ratio-3),exp=entries*width*ratio,compare_max=entries*width*(ratio-1))
        if layer in c['index_source_layer_ids'] and n//ratio:
            add(a+'index_query_rope_scale',m*(3*c['qk_rope_head_dim']*c['index_n_heads']+c['index_n_heads']))
    last_rows=batch*schedules[-1]['query_tokens']
    add('final_hc_pre',last_rows*(2*copies-1)*h);norm('final_norm',last_rows,h)
    return dict(scalar_flops=sum(totals.values()),components=dict(totals),special_ops=dict(special),
                excluded='Sparse softmax/index reduction/sorting, quantization and source casts/copies are not included in this scalar subtotal; full MATRIX graph is independently complete.')


def markdown(r):
    s=r['summary'];lines=['# DeepSeek V4.1 Flash：完整文本矩阵计算', '',str(r['scenario']),'',
        '| 项目 | 结果 |','| --- | ---: |',f"| 文本逻辑参数（含 Engram） | {s['logical_text_parameters']:,} |",
        f"| 完整矩阵 FLOPs | {s['matrix_flops']:,} |",f"| 上下文交互 FLOPs | {s['context_interaction_flops']:,} |",
        f"| 调用前 BF16 逻辑状态（B） | {s['state_before_bytes']:,} |",f"| 调用后 BF16 逻辑状态（B） | {s['state_after_bytes']:,} |",'',
        '| 组件 | 矩阵 FLOPs |','| --- | ---: |']
    lines += [f'| {k} | {v:,} |' for k,v in s['matrix_components'].items()]
    lines += ['', '## 逐层执行', '', '| 层（从零编号） | 查询位置数 | 全局投影位置数 | 新全局条目 |','| --- | ---: | ---: | ---: |']
    lines += [f"| {x['layer']} | {x['query_tokens']} | {x['global_projection_tokens']} | {x['new_global_entries']} |" for x in r['layer_schedule']]
    lines += ['', '## 口径', '']+['- '+x for x in r['assumptions']]
    lines += ['','完整运算记录、各矩阵形状与来源哈希见同名 JSON。非矩阵算术仅为已列明分项，不作为完整标量或 GPU 指令总量。','']
    return '\n'.join(lines)
