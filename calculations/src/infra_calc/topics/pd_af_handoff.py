"""PD snapshot versus serial AF activation handoffs, with explicit staging hops.

This is a communication ledger, not an engine scheduler. Every message completes
all hops before the next starts; compute and overlap require separate evidence.
"""
from fractions import Fraction
from ..sources import model_config, provenance
from ..units import positive_int
from . import state
from . import kv_comparison
from ..paths import PROJECT
import json


def transfer_ledger(total_bytes, messages, hops, startup_ns):
    """Even partition for the byte-controlled experiment; no padding assumed."""
    positive_int(total_bytes, 'total_bytes')
    positive_int(messages, 'messages')
    if messages > total_bytes:
        raise ValueError('Every message must contain at least one byte')
    small, extra = divmod(total_bytes, messages)
    rows = []
    elapsed = Fraction(0)
    for name, bandwidth in hops:
        payload_ns = Fraction(total_bytes * 10**9, bandwidth)
        launch_ns = messages * startup_ns
        elapsed += payload_ns + launch_ns
        rows.append(dict(resource=name, transmitted_bytes=total_bytes,
                         launches=messages, payload_ns_exact=str(payload_ns),
                         startup_ns=launch_ns))
    return dict(payload_bytes=total_bytes, messages=messages,
                smallest_message_bytes=small, largest_message_bytes=small+bool(extra),
                larger_messages=extra, resource_demands=rows,
                serialized_ns_exact=str(elapsed))


def calculate(model='teaching-gqa', length=8192, batch=1, decode_steps=1,
              element_bytes=2, network_bandwidth=25*10**9,
              staging_bandwidth=25*10**9, startup_ns=5000, path='direct',
              kv_layout='gqa', kv_model='deepseek-v3'):
    inputs = locals().copy()
    if kv_layout not in ('gqa', 'mla'):
        raise ValueError('kv_layout must be gqa or mla')
    for name, value in inputs.items():
        if name not in ('model', 'path', 'kv_layout', 'kv_model'):
            positive_int(value, name, allow_zero=name=='startup_ns')
    if element_bytes not in (1, 2, 4):
        raise ValueError('Element size must be 1, 2 or 4 bytes; no packed format')
    if path not in ('direct', 'host-staged'):
        raise ValueError('Path must be direct or host-staged')
    if model == 'teaching-gqa':
        layers, width, kv_heads, head_dim = 32, 4096, 8, 128
        kv_bytes = batch*length*2*layers*kv_heads*head_dim*element_bytes
        sources = []
    else:
        config = model_config(model)
        if config['model_type'] not in ('qwen3', 'qwen3_moe'):
            raise ValueError('AF boundary is implemented only for full-hidden Qwen GQA')
        layers, width = config['num_hidden_layers'], config['hidden_size']
        kv_heads, head_dim = config['num_key_value_heads'], config['head_dim']
        kv_bytes = state.calculate(model,length,batch,element_bytes)['summary']['resident_bytes']
        sources = provenance(model)
    mla = None
    if kv_layout == 'mla':
        unit = kv_comparison.per_token_bytes(kv_model, 'mla')
        kv_bytes = batch*length*unit
        sources = list({s['file']: s for s in sources+provenance(kv_model)}.values())
        extra = kv_comparison.mla_compact_extra_flops_per_token(kv_model)
        reference = PROJECT/'results/v3-forward-decode.json'
        check = None
        if reference.is_file():
            ops = json.loads(reference.read_text())['operators']
            row = next((op for op in ops if op['name'] == 'kv_b_proj'), None)
            if row is not None:
                check = dict(result_file='results/v3-forward-decode.json', operator='kv_b_proj',
                             expanded_path_matrix_flops_per_layer=row['matrix_flops'],
                             equals_compact_extra_per_layer=row['matrix_flops'] == extra['extra_flops_per_token_per_layer'])
        mla = dict(kv_bytes_per_token=unit, decode_steps=decode_steps, batch=batch,
                   extra_flops_per_step=batch*extra['extra_flops_per_token'], per_token=extra, expanded_path_reference=check)
    hops = [('network', network_bandwidth)]
    if path == 'host-staged':
        hops = [('source_d2h', staging_bandwidth), *hops,
                ('destination_h2d', staging_bandwidth)]
    activation = batch*width*element_bytes
    count = 2*layers*decode_steps
    af_bytes = activation*count
    pd = transfer_ledger(kv_bytes,1,hops,startup_ns)
    af = transfer_ledger(af_bytes,count,hops,startup_ns)
    # The artificial byte-matched control changes only granularity, not payload.
    control = transfer_ledger(kv_bytes,count,hops,startup_ns)
    transfer_difference = sum((Fraction((kv_bytes-af_bytes)*10**9,bw)
                               for _,bw in hops),Fraction(0))
    startup_coefficient = (count-1)*len(hops)
    crossover = transfer_difference/startup_coefficient
    def buffers(payload):
        return dict(source_gpu_live_bytes=payload,destination_gpu_live_bytes=payload,
                    source_host_staging_bytes=payload if path=='host-staged' else 0,
                    destination_host_staging_bytes=payload if path=='host-staged' else 0)
    return dict(schema_version=1,calculation='pd-af-handoff',scenario=inputs,sources=sources,
                summary=dict(layers=layers,hidden_size=width,kv_heads=kv_heads,head_dim=head_dim,
                             kv_layout=kv_layout,kv_bytes_per_token=kv_bytes//(batch*length),
                             pd_snapshot_bytes=kv_bytes,af_one_direction_bytes=activation,
                             af_total_bytes=af_bytes,af_directional_messages=count,
                             hops_per_message=len(hops),
                             pd_serialized_ns_exact=pd['serialized_ns_exact'],
                             af_serialized_ns_exact=af['serialized_ns_exact'],
                             byte_matched_extra_ns_exact=str(Fraction(control['serialized_ns_exact'])-Fraction(pd['serialized_ns_exact'])),
                             equal_time_startup_ns_exact=str(crossover) if crossover>=0 else None,
                             af_faster_at_selected_startup=Fraction(af['serialized_ns_exact'])<Fraction(pd['serialized_ns_exact'])),
                handoff_cases=[dict(name='PD snapshot',**pd),dict(name='AF decode activations',**af),
                               dict(name='byte-matched repeated handoffs',**control)],
                endpoint_buffers=dict(pd=buffers(kv_bytes),af_one_message=buffers(activation)),
                mla_compact_path=mla,
                assumptions=[
                    'teaching-gqa为正文32层示例；Qwen从官方config读取完整GQA。PD每请求一次完整未切分KV，AF仅指定decode_steps次模型调用；两项不代表同一完整请求的替代总成本。',
                    'AF每层将完整hidden激活送到FFN侧，聚合完整结果返回；一次方向交接载荷B*H*element_bytes。MoE路由元数据、top-k复制、跨专家节点dispatch及共享专家的分支未计，不能套用潜空间V4/K3边界。',
                    '每条消息按hop完全串行，前条全部完成才开始后条；每hop加相同startup_ns，显式包含其启动／同步假设。host-staged为D2H→network→H2D，接口各计发送一次，不把收端重复加到网络。',
                    '带宽与启动均为教学有效服务输入，不是A100/H20或其他具体机器实测；不推算池服务率、排队、计算、TTFT或TPOT。',
                    '缓冲为明确的整消息双端分配上界：源GPU载荷、目的GPU载荷和两侧host槽共存；PD源KV与目的KV已包含在这里，不再另加为temporary。AF结果返回复用槽，FFN工作区及原激活保留不在此子账。',
                    '两端采用相同元素格式，未包含压缩元数据、格式转换、页索引、对齐和重传；不把1-byte存储自动称为受支持FP8执行。',
                    '相同总字节对照仅均分PD载荷到AF次数，有余数的消息多1byte。它用于隔离启动开销，不是实际KV分层协议。交叉点为上述串行通信模型的等时启动值，严格更快需在相应一侧。',
                    'kv_layout=mla：PD 快照按锁定 DeepSeek-V3 config 的紧凑 MLA 每 token 字节（层数×(d_c+d_r)×element_bytes）乘长度，AF 激活字节仍按所选 model 的层数与 hidden 不变；紧凑路径每步额外查询变换与值恢复 FLOPs 按第 2 章公式由 V3 config 计算，并与 v3-forward-decode 的 kv_b_proj 算子核对。',
                ])
