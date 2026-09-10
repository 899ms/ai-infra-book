"""C73: what remains to move once the weights stop moving (4.6.5, 6.5.1).

The OpenTallas premise is that weights live in immutable on-die storage, so a
decode step no longer reads them across the memory interface. This module asks
what that leaves: how far each activation has to fan out to the tiles that hold
a layer, how much comes back to be reduced, how many hops that costs on a mesh,
what synchronisation span the token budget can afford, and what supply a target
rate demands once the arithmetic is run backwards.

Model geometry, weight bytes and session-state bytes come from the pinned
official config and are checked against the case study's own figures. Tile
capacity, hop latency, per-stack bandwidth, storage density and lane throughput
are declared teaching inputs. Nothing here is a measurement: OpenTallas has no
silicon, and no rate below is claimed as achieved.
"""
from fractions import Fraction
import json
import math

from ..sources import model_config, provenance
from ..units import positive_int, positive_number

SHARDINGS = ("column", "row")


def fraction(value: Fraction) -> dict:
    return {"numerator": value.numerator, "denominator": value.denominator}


def exact(value) -> Fraction:
    return Fraction(str(value))


def geometry(model: str) -> dict:
    """Parameter and byte counts rebuilt from the official config."""
    config = model_config(model)
    if config.get("model_type") != "qwen3":
        raise ValueError("This residency account covers the pinned dense Qwen3 config only")
    hidden = config["hidden_size"]
    inner = config["intermediate_size"]
    layers = config["num_hidden_layers"]
    heads = config["num_attention_heads"]
    kv_heads = config["num_key_value_heads"]
    head_dim = config["head_dim"]
    vocab = config["vocab_size"]
    if config.get("tie_word_embeddings"):
        raise ValueError("A tied output head changes the active-read split; not covered here")
    attention = hidden * heads * head_dim + 2 * hidden * kv_heads * head_dim + heads * head_dim * hidden
    feedforward = 3 * hidden * inner
    norms = 2 * hidden + 2 * head_dim
    per_layer = attention + feedforward + norms
    embedding = vocab * hidden
    checkpoint = per_layer * layers + 2 * embedding + hidden
    # Decode reads one embedding row, so the lookup table is not an active read;
    # the output head of the same shape is.
    active = per_layer * layers + embedding + hidden
    return {"hidden_size": hidden, "intermediate_size": inner, "num_hidden_layers": layers,
            "num_attention_heads": heads, "num_key_value_heads": kv_heads,
            "head_dim": head_dim, "vocab_size": vocab,
            "params_per_layer": per_layer, "params_embedding": embedding,
            "params_checkpoint": checkpoint, "params_active_decode": active,
            "checkpoint_bytes": checkpoint * 2, "active_decode_read_bytes": active * 2,
            "layer_bytes": per_layer * 2,
            "kv_bytes_per_token": 2 * 2 * layers * kv_heads * head_dim,
            "activation_bytes": hidden * 2}


def residency_split(model: str, context: int, batch: int) -> dict:
    """What the interface still carries once weights stop crossing it."""
    positive_int(context, "context")
    positive_int(batch, "batch")
    shape = geometry(model)
    kv_read = shape["kv_bytes_per_token"] * context
    weights = shape["active_decode_read_bytes"]
    crossover = Fraction(weights, kv_read)
    with_weights = weights + batch * kv_read
    without_weights = batch * kv_read
    return {"context": context, "batch": batch,
            "kv_bytes_per_token": shape["kv_bytes_per_token"],
            "kv_read_bytes_per_sequence_step": kv_read,
            "active_weight_read_bytes": weights,
            "step_bytes_with_resident_weights": with_weights,
            "step_bytes_without_weight_reads": without_weights,
            "crossover_batch_exact": fraction(crossover),
            "crossover_batch_first_integer": math.floor(crossover) + 1,
            "memory_service_speedup": fraction(Fraction(with_weights, without_weights)),
            "note": ("The speedup covers this memory service only. Arithmetic, immutable-store "
                     "service, communication and scheduling still have to be timed.")}


def supply_backsolve(model: str, context: int, tokens_per_second: int,
                     stack_bytes_per_second: int, density_bytes_per_mm2: int,
                     tensor_operations: int, token_budget_seconds,
                     arithmetic_budget_share, lane_utilisation,
                     lane_operations_per_second: int) -> dict:
    """Run the target backwards into bandwidth, stacks, area and lanes."""
    positive_int(tokens_per_second, "tokens_per_second")
    positive_int(stack_bytes_per_second, "stack_bytes_per_second")
    positive_int(density_bytes_per_mm2, "density_bytes_per_mm2")
    positive_int(tensor_operations, "tensor_operations")
    positive_int(lane_operations_per_second, "lane_operations_per_second")
    budget = exact(token_budget_seconds)
    share = exact(arithmetic_budget_share)
    utilisation = exact(lane_utilisation)
    for name, value in (("token_budget_seconds", budget), ("arithmetic_budget_share", share),
                        ("lane_utilisation", utilisation)):
        if value <= 0:
            raise ValueError(f"{name} must be positive")
    if share > 1 or utilisation > 1:
        raise ValueError("A budget share and a utilisation cannot exceed one")

    shape = geometry(model)
    kv_read = shape["kv_bytes_per_token"] * context
    demand = kv_read * tokens_per_second
    stacks = -(-demand // stack_bytes_per_second)
    area = Fraction(kv_read, density_bytes_per_mm2)
    ideal_lanes = -(-tensor_operations // int(lane_operations_per_second * budget))
    derated = Fraction(lane_operations_per_second) * budget * share * utilisation
    derated_lanes = -(-tensor_operations * derated.denominator // derated.numerator)
    return {"tokens_per_second": tokens_per_second,
            "kv_read_bandwidth_bytes_per_second": demand,
            "stack_bytes_per_second": stack_bytes_per_second,
            "stacks_required": stacks,
            "session_state_area_mm2": fraction(area),
            "density_bytes_per_mm2": density_bytes_per_mm2,
            "tensor_operations": tensor_operations,
            "ideal_lanes": ideal_lanes,
            "derated_lanes": derated_lanes,
            "derating": {"arithmetic_budget_share": fraction(share),
                         "lane_utilisation": fraction(utilisation)},
            "note": ("Every figure here is a lower bound on supply for one term. They do not "
                     "add up to a feasible design, and none of them is a measurement.")}


def fanout_fanin(model: str, tile_bytes: int, sharding: str, hop_latency_seconds) -> dict:
    """Activation traffic and hop counts once weights are pinned to tiles.

    With a layer's weights spread over tiles, a column shard sends every tile
    the whole activation and concatenates the answers, while a row shard sends
    each tile a slice and has to reduce full-width partials back.
    """
    if sharding not in SHARDINGS:
        raise ValueError("Sharding must be column or row")
    positive_int(tile_bytes, "tile_bytes")
    hop = exact(hop_latency_seconds)
    if hop <= 0:
        raise ValueError("hop_latency_seconds must be positive")
    shape = geometry(model)
    tiles = -(-shape["layer_bytes"] // tile_bytes)
    activation = shape["activation_bytes"]
    if sharding == "column":
        fan_out = tiles * activation
        fan_in = activation
        reduction_rounds = 0
    else:
        fan_out = activation
        fan_in = tiles * activation
        reduction_rounds = max(0, (tiles - 1).bit_length())
    side = math.isqrt(tiles)
    if side * side < tiles:
        side += 1
    diameter = 2 * (side - 1)
    spanning_hops = tiles - 1
    layers = shape["num_hidden_layers"]
    return {"sharding": sharding, "tile_bytes": tile_bytes,
            "layer_bytes": shape["layer_bytes"], "tiles_per_layer": tiles,
            "mesh_side": side, "mesh_diameter_hops": diameter,
            "activation_bytes": activation,
            "fan_out_bytes_per_layer": fan_out, "fan_in_bytes_per_layer": fan_in,
            "reduction_rounds_per_layer": reduction_rounds,
            "spanning_tree_hops_per_collective": spanning_hops,
            "total_hops_per_token": 2 * layers * spanning_hops,
            "critical_path_hops_per_token": 2 * layers * diameter,
            "propagation_lower_bound_seconds": fraction(2 * layers * diameter * hop),
            "note": ("Hop counts are a topology lower bound: a spanning tree cannot use fewer "
                     "edges and a diameter cannot be crossed in fewer hops. Serialisation, "
                     "reduction arithmetic, contention and tail delay are not included.")}


def sync_span(model: str, token_budget_seconds, communication_share,
              collectives_per_layer: int, diameter_hops: int, hop_latency_seconds) -> dict:
    """Per-collective budget against the propagation a topology already costs."""
    positive_int(collectives_per_layer, "collectives_per_layer")
    positive_int(diameter_hops, "diameter_hops", allow_zero=True)
    budget = exact(token_budget_seconds)
    share = exact(communication_share)
    hop = exact(hop_latency_seconds)
    if budget <= 0 or share <= 0 or hop <= 0:
        raise ValueError("Budget, share and hop latency must be positive")
    if share > 1:
        raise ValueError("A communication share cannot exceed one")
    layers = geometry(model)["num_hidden_layers"]
    events = layers * collectives_per_layer
    per_event = budget * share / events
    propagation = diameter_hops * hop
    total = events * propagation
    # Largest diameter each budget still admits, solved rather than searched.
    per_event_hops = int(per_event / hop)
    token_hops = int(budget / (events * hop))
    return {"layers": layers, "collectives_per_layer": collectives_per_layer,
            "collective_events_per_token": events,
            "largest_diameter_within_per_collective_budget": per_event_hops,
            "largest_diameter_within_token_budget": token_hops,
            "token_budget_seconds": fraction(budget),
            "communication_share": fraction(share),
            "budget_per_collective_seconds": fraction(per_event),
            "propagation_per_collective_seconds": fraction(propagation),
            "propagation_per_token_seconds": fraction(total),
            "fits_per_collective_budget": propagation <= per_event,
            "fits_token_budget": total <= budget,
            "overrun_factor_against_token_budget": fraction(total / budget),
            "note": ("Propagation alone. A design that already fails here cannot be rescued by "
                     "scheduling; the fabric, the number of events, the partition or the target "
                     "has to change.")}


OMITTED = [
    "KV writes, re-reads and allocator overhead are outside the read-side account.",
    "Immutable-store service time is not modelled; only its absence from the memory interface is.",
    "Hop counts carry no serialisation, reduction arithmetic, contention or tail delay.",
    "Lane counts leave out operand supply, accumulation, clocking, routing and timing closure.",
    "Area covers the named term only, with nothing reserved for weights, arithmetic or interconnect.",
    "Sparse attention needs resident state, per-step access and index scan counted separately.",
    "No figure here is measured: this design has no silicon, and its rates are not achieved rates.",
]


def calculate(model: str = "qwen3-8b", context: int = 8192, batch: int = 1,
              tokens_per_second: int = 10000,
              stack_bytes_per_second: int = 1_200_000_000_000,
              density_bytes_per_mm2: int = 3_009_000,
              tensor_operations: int = 15_134_641_792,
              token_budget_seconds: str = "0.0001",
              arithmetic_budget_share: str = "0.4",
              lane_utilisation: str = "0.6",
              lane_operations_per_second: int = 2_000_000_000,
              tile_bytes: int = 64 * 1024 * 1024,
              sharding: str = "column",
              hop_latency_seconds: str = "1e-7",
              collectives_per_layer: int = 2,
              communication_share: str = "0.3",
              diameter_hops: int | None = None) -> dict:
    """One residency account, its remaining traffic, and the supply it demands."""
    shape = geometry(model)
    split = residency_split(model, context, batch)
    supply = supply_backsolve(model, context, tokens_per_second, stack_bytes_per_second,
                              density_bytes_per_mm2, tensor_operations, token_budget_seconds,
                              arithmetic_budget_share, lane_utilisation,
                              lane_operations_per_second)
    traffic = {name: fanout_fanin(model, tile_bytes, name, hop_latency_seconds)
               for name in SHARDINGS}
    derived_diameter = traffic[sharding]["mesh_diameter_hops"]
    diameter = derived_diameter if diameter_hops is None else positive_int(
        diameter_hops, "diameter_hops")
    span = sync_span(model, token_budget_seconds, communication_share, collectives_per_layer,
                     diameter, hop_latency_seconds)
    scan = [dict(sync_span(model, token_budget_seconds, communication_share,
                           collectives_per_layer, hops, hop_latency_seconds),
                 diameter_hops=hops)
            for hops in (derived_diameter, span["largest_diameter_within_token_budget"],
                         span["largest_diameter_within_token_budget"] + 1, 15)]
    return {
        "calculation": "weight-resident-remaining-traffic",
        "inputs": {"model": model, "context": context, "batch": batch,
                   "tokens_per_second": tokens_per_second,
                   "stack_bytes_per_second": stack_bytes_per_second,
                   "density_bytes_per_mm2": density_bytes_per_mm2,
                   "tensor_operations": tensor_operations,
                   "token_budget_seconds": token_budget_seconds,
                   "arithmetic_budget_share": arithmetic_budget_share,
                   "lane_utilisation": lane_utilisation,
                   "lane_operations_per_second": lane_operations_per_second,
                   "tile_bytes": tile_bytes, "sharding": sharding,
                   "hop_latency_seconds": hop_latency_seconds,
                   "collectives_per_layer": collectives_per_layer,
                   "communication_share": communication_share,
                   "diameter_hops": diameter_hops},
        "sources": provenance(model),
        "geometry": shape,
        "residency_split": split,
        "supply_backsolve": supply,
        "fan_traffic": traffic,
        "selected_sharding": sharding,
        "diameter_hops_used": diameter,
        "diameter_hops_derived_from_mesh": derived_diameter,
        "synchronisation_span": span,
        "diameter_scan": [{"diameter_hops": row["diameter_hops"],
                           "propagation_per_token_seconds": row["propagation_per_token_seconds"],
                           "fits_per_collective_budget": row["fits_per_collective_budget"],
                           "fits_token_budget": row["fits_token_budget"],
                           "overrun_factor_against_token_budget": row["overrun_factor_against_token_budget"]}
                          for row in scan],
        "omitted_constraints": OMITTED,
        "assumptions": [
            "Weight, state and activation bytes are rebuilt from the pinned official config.",
            "Tile capacity, hop latency, per-stack bandwidth, storage density and lane rate are declared teaching inputs.",
            "Hop and lane figures are topology and arithmetic lower bounds, not schedules.",
            "The memory-service speedup covers one interface, never a whole machine.",
            "This design has no silicon; no rate here is presented as achieved.",
        ],
    }


def markdown(result: dict) -> str:
    def number(entry, places=3):
        return "—" if entry is None else f"{float(Fraction(**entry)):.{places}f}"

    split = result["residency_split"]
    supply = result["supply_backsolve"]
    span = result["synchronisation_span"]
    shape = result["geometry"]
    lines = ["# 权重驻留之后还剩什么要搬", "",
             "模型几何与字节量由固定官方配置重建；片上容量、跳延迟、每 stack 带宽、存储密度与 lane 速率是声明输入。"
             "本设计没有流片，下面没有任何一项是实测速率。", "",
             "## 驻留拆分", "",
             f"- 完整 checkpoint：{shape['checkpoint_bytes']} B；一步活跃权重读取：{shape['active_decode_read_bytes']} B。",
             f"- 每历史 token 的 KV：{split['kv_bytes_per_token']} B；上下文 {split['context']} 时每序列每步读取 {split['kv_read_bytes_per_sequence_step']} B。",
             f"- 权重／KV 交叉点 batch：{number(split['crossover_batch_exact'], 4)}，即从 batch {split['crossover_batch_first_integer']} 起 KV 读取超过权重读取。",
             f"- 权重移出该接口后，仅此内存服务的理想加速比：{number(split['memory_service_speedup'], 3)}（batch={split['batch']}）。",
             f"- {split['note']}", "",
             "## 供给倒推", "",
             f"- 维持 {supply['tokens_per_second']} tok/s 仅 KV 读就需 {supply['kv_read_bandwidth_bytes_per_second']} B/s，"
             f"按每 stack {supply['stack_bytes_per_second']} B/s 至少 {supply['stacks_required']} 个 stack。",
             f"- 按密度 {supply['density_bytes_per_mm2']} B/mm²，仅该状态需约 {number(supply['session_state_area_mm2'], 1)} mm²。",
             f"- {supply['tensor_operations']} 次运算在理想条件下需 {supply['ideal_lanes']} 条 lane；"
             f"只留 {number(supply['derating']['arithmetic_budget_share'], 2)} 预算、"
             f"利用率 {number(supply['derating']['lane_utilisation'], 2)} 时需 {supply['derated_lanes']} 条。",
             f"- {supply['note']}", "",
             "## 激活扇出／扇入与跳数", "",
             "| 切分 | 每层 tile 数 | 网格边长 | 直径跳 | 每层扇出 B | 每层扇入 B | 归约轮 | 每 token 总跳 | 每 token 关键路径跳 |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for name, row in result["fan_traffic"].items():
        lines.append("| " + " | ".join([
            name, str(row["tiles_per_layer"]), str(row["mesh_side"]), str(row["mesh_diameter_hops"]),
            str(row["fan_out_bytes_per_layer"]), str(row["fan_in_bytes_per_layer"]),
            str(row["reduction_rounds_per_layer"]), str(row["total_hops_per_token"]),
            str(row["critical_path_hops_per_token"])]) + " |")
    lines += ["", f"选定切分 {result['selected_sharding']}；"
                  f"{result['fan_traffic'][result['selected_sharding']]['note']}"]

    lines += ["", "## 同步跨度", "",
              f"- {span['layers']} 层 × 每层 {span['collectives_per_layer']} 次集合通信 = "
              f"{span['collective_events_per_token']} 次；token 预算 {number(span['token_budget_seconds'], 6)} s 的 "
              f"{number(span['communication_share'], 2)} 分给通信，每次可用 {number(span['budget_per_collective_seconds'], 9)} s。",
              f"- 直径传播每次 {number(span['propagation_per_collective_seconds'], 9)} s，"
              f"每 token 合计 {number(span['propagation_per_token_seconds'], 6)} s。",
              f"- 单次预算内：{'是' if span['fits_per_collective_budget'] else '否'}；"
              f"token 预算内：{'是' if span['fits_token_budget'] else '否'}，"
              f"超出倍数 {number(span['overrun_factor_against_token_budget'], 2)}。",
              f"- {span['note']}", "",
              f"预算允许的最大直径：单次预算 {span['largest_diameter_within_per_collective_budget']} 跳，"
              f"整 token 预算 {span['largest_diameter_within_token_budget']} 跳。超过后仅传播就不成立。", "",
              "| 直径跳 | 每 token 传播 s | 单次预算内 | token 预算内 | 超出倍数 |",
              "|---:|---:|---|---|---:|"]
    for row in result["diameter_scan"]:
        lines.append("| " + " | ".join([
            str(row["diameter_hops"]), number(row["propagation_per_token_seconds"], 8),
            "是" if row["fits_per_collective_budget"] else "否",
            "是" if row["fits_token_budget"] else "否",
            number(row["overrun_factor_against_token_budget"], 3)]) + " |")
    lines += ["", "## 明确未计入的约束", ""]
    lines += ["- " + item for item in result["omitted_constraints"]]
    lines += ["", "## 口径与限制", ""]
    lines += ["- " + item for item in result["assumptions"]]
    lines += ["", "## 完整输入、来源与结果", "", "```json",
              json.dumps(result, ensure_ascii=False, indent=2), "```", ""]
    return "\n".join(lines)
