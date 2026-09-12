"""Which FP32 sum a split reduction returns: partition count and merge order."""
from fractions import Fraction
import itertools
import math
import struct
from ..sources import model_config, provenance
from ..models import qwen3
from ..units import positive_int

LADDER = (1, 2, 4, 8, 16, 32)


def f32(value):
    return struct.unpack('f', struct.pack('f', value))[0]


def bf16(value):
    """Round to bfloat16 by truncating the FP32 payload; the teaching row needs no ties."""
    return struct.unpack('f', struct.pack('I', struct.unpack('I', struct.pack('f', value))[0] & 0xFFFF0000))[0]


def bits(value):
    return struct.unpack('I', struct.pack('f', value))[0]


def sequential(values):
    """One accumulator, one pass; every intermediate result is rounded to FP32."""
    total = 0.0
    for value in values:
        total = f32(total + value)
    return total


def partitions(width, splits):
    positive_int(width, 'width'); positive_int(splits, 'splits')
    if splits > width: raise ValueError('Cannot create empty reduction partitions')
    quotient, remainder = divmod(width, splits)
    return [quotient + (index < remainder) for index in range(splits)]


def partial_sums(squares, splits):
    result = []; offset = 0
    for size in partitions(len(squares), splits):
        result.append(sequential(squares[offset:offset + size])); offset += size
    return result


def calculate(model: str = 'qwen3-8b', splits: int = 8, width_multiplier: int = 1) -> dict:
    c = model_config(model); qwen3.validate(c)
    positive_int(splits, 'splits'); positive_int(width_multiplier, 'width_multiplier')
    if splits not in LADDER: raise ValueError(f'splits must be one of {LADDER}')
    if splits > 8: raise ValueError('Enumerating every merge order is limited to at most eight partial sums')
    width = c['hidden_size'] * width_multiplier; epsilon = c['rms_norm_eps']
    # Teaching row: a stated deterministic sequence rounded to BF16, not a captured activation.
    row = [bf16(math.sin(index + 1)) for index in range(width)]
    squares = [f32(x * x) for x in row]
    if any(Fraction(x) * Fraction(x) != Fraction(s) for x, s in zip(row, squares)):
        raise ValueError('A BF16 square must be exact in FP32 for order to be the only difference')
    exact = sum(Fraction(s) for s in squares)
    exponent = math.frexp(float(exact))[1] - 1
    ulp = Fraction(2) ** (exponent - 23)
    scale = lambda total: f32(1.0 / math.sqrt(f32(f32(total / width) + epsilon)))
    variants = []
    for count in LADDER:
        if count > width: continue
        total = sequential(partial_sums(squares, count)) if count > 1 else sequential(squares)
        variants.append(dict(splits=count, partition_width=partitions(width, count)[0], total=total,
                             offset_ulp=float((Fraction(total) - exact) / ulp), scale=scale(total),
                             first_output=f32(row[0] * scale(total))))
    fused, split = variants[0], next(v for v in variants if v['splits'] == splits)
    orders = sorted({sequential(order) for order in itertools.permutations(partial_sums(squares, splits))})
    identity = dict(inputs=['1', '2**-24', '2**-24'], left=f32(f32(1.0 + 2.0 ** -24) + 2.0 ** -24),
                    right=f32(1.0 + f32(2.0 ** -24 + 2.0 ** -24)), spacing_at_one=2.0 ** -23)
    if identity['left'] == identity['right']:
        raise ValueError('The associativity witness must separate the two groupings')
    return dict(schema_version=1, calculation='split-reduction-order', model=model,
                scenario=dict(splits=splits, width_multiplier=width_multiplier,
                              row='bf16(sin(i+1)) for i in range(width)'),
                sources=provenance(model), associativity=identity, variants=variants,
                merge_order=dict(splits=splits, orders=math.factorial(splits), distinct_results=len(orders),
                                 values=orders, spread_ulp=bits(orders[-1]) - bits(orders[0])),
                summary=dict(width=width, epsilon=epsilon, exact_sum=float(exact), ulp=float(ulp),
                             fused_total=fused['total'], split_total=split['total'],
                             total_ulp_gap=bits(split['total']) - bits(fused['total']),
                             relative_gap=(split['total'] - fused['total']) / fused['total'],
                             scale_ulp_gap=bits(split['scale']) - bits(fused['scale']),
                             first_output_ulp_gap=bits(split['first_output']) - bits(fused['first_output']),
                             merge_orders=math.factorial(splits), distinct_merge_results=len(orders),
                             merge_spread_ulp=bits(orders[-1]) - bits(orders[0])),
                assumptions=[
                    '教学行由给定公式生成并舍入到 BF16，不是采集到的激活。平方在 FP32 中精确，因此各路径的差异只来自加法次序。',
                    '每段内部按顺序累加，段间再合并；exact_sum 用有理数求得，只作比较基准，不是任何 kernel 的输出。',
                    'ULP 取 FP32 在该和所在区间上的间距；offset_ulp 是与精确值的距离，不是误差上界，拆得更细也不保证更准。',
                    '枚举全部合并次序覆盖原子加可能出现的次序，不代表某个后端的实际分布；并发调度还可能改变段内划分。',
                    '缩放因子与输出按官方 rms_norm_eps 计算，只取一行，不乘层数，也不换算为端到端的质量差异。',
                ])


def markdown(result: dict) -> str:
    s = result['summary']
    lines = [f"# {result['calculation']} — {result['model']}", '',
             '输入：`' + __import__('json').dumps(result['scenario'], ensure_ascii=False, sort_keys=True) + '`', '',
             '数值为精确浮点复算；ULP 为 FP32 间距，不是硬件测量。', '',
             '| 结果 | 值 |', '| --- | ---: |']
    for key, value in s.items():
        lines.append(f'| {key} | ' + (f'{value:,}' if isinstance(value, int) and not isinstance(value, bool) else f'{value!r}') + ' |')
    lines += ['', '| 切分段数 | 每段宽度 | 平方和 | 与精确值相距 / ULP | 缩放因子 | 首个输出 |',
              '| ---: | ---: | ---: | ---: | ---: | ---: |']
    for v in result['variants']:
        lines.append(f"| {v['splits']} | {v['partition_width']} | {v['total']!r} | {v['offset_ulp']:.1f} | {v['scale']!r} | {v['first_output']!r} |")
    m = result['merge_order']
    lines += ['', f"{m['splits']} 个局部和的 {m['orders']:,} 种合并次序共给出 {m['distinct_results']} 个不同的 FP32 结果，"
              f"彼此相距 {m['spread_ulp']} ULP：`" + ', '.join(repr(v) for v in m['values']) + '`。', '',
              '结合律反例：`(1 + 2⁻²⁴) + 2⁻²⁴ = ' + repr(result['associativity']['left']) +
              '`，`1 + (2⁻²⁴ + 2⁻²⁴) = ' + repr(result['associativity']['right']) + '`。', '', '计量条件：', '']
    lines += [f'- {item}' for item in result['assumptions']]
    lines += ['', '固定来源：', '']
    for item in result['sources']:
        lines.append(f"- [{item['file']}]({item['url']})，SHA256 `{item['sha256']}`。")
    return '\n'.join(lines) + '\n'
