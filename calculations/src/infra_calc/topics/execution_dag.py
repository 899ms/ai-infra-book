"""C72: one complete execution DAG, its resource bound, and candidate screening.

Section 1.3.4 asks for a graph whose work nodes carry an operation and a
location, whose data edges carry an interface, a byte count and a repetition
count, and whose state is followed from production to release. Section 9.6.2
then asks which deployment candidate to keep once latency, throughput and cost
per useful token are weighed under a power or area cap.

Node work comes from the pinned stage accounting on official model configs, and
device rates, capacity and power come from the source-checked hardware catalog.
A stage whose resources include a rate the catalog does not publish keeps its
gap visible: the bound is over the resources that are known, and the unknown
ones are listed rather than filled in. Area caps and prices are declared inputs.
"""
from fractions import Fraction
import json

from .. import hardware
from ..units import positive_int, positive_number
from . import request_dag, stage_resource_bounds
from .region_placement import kv_bytes_per_token

# 1.3.4's candidate actions. Each rewrites the graph; each has a counterexample.
ACTIONS = ("baseline", "cache_prefix", "compress_state", "batch", "disaggregate")


def fraction(value: Fraction) -> dict:
    return {"numerator": value.numerator, "denominator": value.denominator}


def exact(value) -> Fraction:
    return Fraction(str(value))


def stage_nodes(bounds: dict, location: str) -> list:
    """Work nodes with their operation, location, and bound over known resources."""
    nodes = []
    for stage, bound in zip(bounds["stages"], bounds["resource_bounds"]["stages"]):
        if stage["id"] != bound["id"]:
            raise ValueError("Stage accounting and resource bounds are not aligned")
        seconds = bound["known_resource_max_seconds"]
        if seconds is None:
            raise ValueError("A stage reported no known resource at all: " + stage["id"])
        limiting = max(bound["resource_seconds"], key=bound["resource_seconds"].get)
        nodes.append({
            "id": stage["id"], "location": location,
            "operations": [row["name"] for row in stage.get("operations", [])],
            "interface_bytes": stage["work"].get("interface_bytes", 0),
            "resource_seconds": bound["resource_seconds"],
            "limiting_known_resource": limiting,
            "bound_seconds": seconds,
            "resources_without_a_published_rate": [row["resource"] for row in bound["missing"]]})
    return nodes


def chain(nodes: list, transfer=None) -> list:
    """Serial dependency chain, optionally cut by one cross-device transfer."""
    tasks, previous = [], None
    for node in nodes:
        deps = [previous] if previous else []
        tasks.append({"id": node["id"], "deps": deps,
                      "duration_ns": max(1, round(node["bound_seconds"] * 10 ** 9)),
                      "resource": node["location"]})
        previous = node["id"]
    if transfer is not None:
        tasks.append({"id": transfer["id"], "deps": [transfer["after"]],
                      "duration_ns": max(1, round(transfer["seconds"] * 10 ** 9)),
                      "resource": transfer["interface"]})
        for task in tasks:
            if task["id"] != transfer["id"] and transfer["after"] in task["deps"]:
                task["deps"] = [transfer["id"]]
    return tasks


def graph_bound(bounds: dict, location: str, transfer=None) -> dict:
    """Critical path over the stage graph, in seconds."""
    nodes = stage_nodes(bounds, location)
    tasks = chain(nodes, transfer)
    schedule = request_dag.schedule(tasks)
    gaps = sorted({name for node in nodes
                   for name in node["resources_without_a_published_rate"]})
    return {"nodes": nodes, "schedule": schedule,
            "critical_path": schedule["critical_path"],
            "bound_seconds": Fraction(schedule["finish_ns"], 10 ** 9),
            "interface_bytes_total": sum(node["interface_bytes"] for node in nodes),
            "resources_without_a_published_rate": gaps}


def split_capacity(bounds: dict, model: str) -> dict:
    """Weights against session state, derived from the official attention geometry.

    The stage accounting publishes one combined figure, so the K/V share is
    recomputed here from the config rather than read out of it.
    """
    scenario = bounds["scenario"]
    positions = scenario["history"] + scenario["tokens"]
    per_request = kv_bytes_per_token(model, 16) * positions
    kv = per_request * scenario["batch"]
    weights = bounds["capacity"]["comparison_bytes"] - kv
    if weights <= 0:
        raise ValueError("Session state cannot exceed the combined capacity figure")
    return {"weight_bytes": weights, "kv_bytes": kv,
            "kv_bytes_per_request": per_request, "positions": positions}


def state_edges(bounds: dict, model: str) -> list:
    """State followed from production to release, as 1.3.4 requires."""
    split = split_capacity(bounds, model)
    return [
        {"state": "weights", "produced": "offline training", "reused": "every stage",
         "updated": "never during serving", "released": "on instance teardown",
         "bytes": split["weight_bytes"]},
        {"state": "kv", "produced": "each attention stage", "reused": "every later position",
         "updated": "appended per step", "released": "on request completion",
         "bytes": split["kv_bytes"]},
        {"state": "activations", "produced": "each stage", "reused": "the next stage only",
         "updated": "never", "released": "as soon as the next stage reads them",
         "bytes": None},
    ]


def candidate(action: str, model: str, device: str, tokens: int, history: int,
              batch: int, state_bits: int, decode_device: str | None) -> dict:
    """One rewritten graph, with what it removes and what it adds."""
    if action not in ACTIONS:
        raise ValueError("Unknown candidate action: " + action)
    call = {"model": model, "device": device, "batch": batch,
            "tokens": tokens, "history": history}
    transfer, note, added = None, "", []

    if action == "cache_prefix":
        if history == 0:
            raise ValueError("Caching a prefix needs a prefix to cache")
        call["tokens"], call["history"] = 1, history + tokens - 1
        note = "Prefill only the position the cache does not hold."
        added = ["holding the prefix occupies capacity between calls"]
    elif action == "compress_state":
        note = "Hold session state at a narrower width."
        added = ["a narrower state changes numerics and needs its own quality evidence"]
    elif action == "batch":
        call["batch"] = batch * 8
        note = "Amortise one weight read across more requests in the same step."
        added = ["every request in the batch waits for the slowest one"]
    elif action == "disaggregate":
        note = "Prefill and decode on separate devices."
        added = ["the session state now crosses an interface between the two"]

    bounds = stage_resource_bounds.calculate(**call)
    split = split_capacity(bounds, model)
    location = device if action != "disaggregate" else device + "->prefill"

    if action == "disaggregate":
        if decode_device is None:
            raise ValueError("Disaggregation needs a second device")
        moved = split["kv_bytes"]
        link = hardware.select_device(decode_device)["memory"]["bandwidth_bytes_per_second"]
        transfer = {"id": "state_transfer", "after": bounds["stages"][-1]["id"],
                    "interface": "device-to-device", "link_bytes_per_second": int(link),
                    "seconds": float(Fraction(int(moved), int(link))),
                    "bytes": moved,
                    "note": ("Priced at the destination's own memory bandwidth, which is an "
                             "optimistic stand-in: no published figure covers this link")}

    profile = hardware.select_device(device)
    capacity_bytes = bounds["capacity"]["comparison_bytes"]
    if action == "compress_state":
        if state_bits not in (16, 8):
            raise ValueError("Compressed state must be 16 or 8 bits")
        capacity_bytes = split["weight_bytes"] + split["kv_bytes"] * state_bits // 16
    graph = graph_bound(bounds, location, transfer)
    available = bounds["capacity"]["device_nominal_bytes"]
    devices = 1 if action != "disaggregate" else 2

    tokens_produced = call["batch"] * max(1, call["tokens"])
    return {
        "action": action, "note": note, "added_cost": added,
        "call": call, "location": location, "devices": devices,
        "graph": {"critical_path": graph["critical_path"],
                  "bound_seconds": fraction(graph["bound_seconds"]),
                  "interface_bytes_total": graph["interface_bytes_total"],
                  "resources_without_a_published_rate": graph["resources_without_a_published_rate"],
                  "node_count": len(graph["nodes"])},
        "nodes": graph["nodes"],
        "state_transfer": transfer,
        "state_edges": state_edges(bounds, model),
        "capacity_bytes": capacity_bytes,
        "capacity_split": split,
        "device_nominal_bytes": available,
        "fits_capacity": capacity_bytes <= available * devices,
        "power_watts": (profile.get("power_watts") or 0) * devices,
        "power_published": profile.get("power_watts") is not None,
        "tokens_per_call": tokens_produced,
        "sources": bounds["sources"],
    }


def screen(rows: list, power_cap_watts: int | None, area_cap_mm2: int | None,
           area_mm2_per_device: int | None, price_per_device_hour: str) -> dict:
    """Keep the candidates no other candidate beats on every objective at once.

    Latency is the graph bound, throughput is tokens over that bound, and cost
    is device time priced per hour. Capacity, power and area are caps, applied
    before any objective is compared.
    """
    price = exact(price_per_device_hour)
    if price < 0:
        raise ValueError("price_per_device_hour must be nonnegative")
    scored = []
    for row in rows:
        bound = Fraction(**row["graph"]["bound_seconds"])
        if bound <= 0:
            raise ValueError("A candidate reported a nonpositive bound")
        throughput = Fraction(row["tokens_per_call"]) / bound
        cost = bound * Fraction(row["devices"]) * price / 3600
        area = None if area_mm2_per_device is None else area_mm2_per_device * row["devices"]
        reasons = []
        if not row["fits_capacity"]:
            reasons.append("does not fit the device capacity")
        if power_cap_watts is not None and row["power_watts"] > power_cap_watts:
            reasons.append(f"needs {row['power_watts']} W against a {power_cap_watts} W cap")
        if area_cap_mm2 is not None and area is not None and area > area_cap_mm2:
            reasons.append(f"needs {area} mm2 against a {area_cap_mm2} mm2 cap")
        scored.append({
            "action": row["action"], "devices": row["devices"],
            "latency_bound_seconds": fraction(bound),
            "throughput_tokens_per_second": fraction(throughput),
            "cost_per_call": fraction(cost),
            "cost_per_token": fraction(cost / row["tokens_per_call"]),
            "power_watts": row["power_watts"], "area_mm2": area,
            "capacity_bytes": row["capacity_bytes"],
            "admissible": not reasons,
            "reasons": reasons or ["within every declared cap"]})

    admissible = [row for row in scored if row["admissible"]]

    def better(left, right):
        """Right dominates left when it is at least as good everywhere and better once."""
        pairs = ((Fraction(**right["latency_bound_seconds"]), Fraction(**left["latency_bound_seconds"])),
                 (Fraction(**left["throughput_tokens_per_second"]), Fraction(**right["throughput_tokens_per_second"])),
                 (Fraction(**right["cost_per_token"]), Fraction(**left["cost_per_token"])))
        return all(a <= b for a, b in pairs) and any(a < b for a, b in pairs)

    front, dominated = [], []
    for row in admissible:
        beaten_by = [other["action"] for other in admissible
                     if other["action"] != row["action"] and better(row, other)]
        (dominated if beaten_by else front).append(
            dict(row, dominated_by=beaten_by) if beaten_by else row)

    def best(key, largest):
        if not admissible:
            return None
        chosen = (max if largest else min)(admissible, key=lambda row: Fraction(**row[key]))
        return chosen["action"]

    return {"scored": scored,
            "pareto_front": [row["action"] for row in front],
            "dominated": [{"action": row["action"], "dominated_by": row["dominated_by"]}
                          for row in dominated],
            "excluded_by_caps": [{"action": row["action"], "reasons": row["reasons"]}
                                 for row in scored if not row["admissible"]],
            "lowest_latency": best("latency_bound_seconds", False),
            "highest_throughput": best("throughput_tokens_per_second", True),
            "lowest_cost_per_token": best("cost_per_token", False)}


def calculate(model: str = "qwen3-8b", device: str = "h100-sxm",
              decode_device: str = "h100-sxm",
              tokens: int = 128, history: int = 4096, batch: int = 1,
              state_bits: int = 8,
              power_cap_watts: int | None = 1500,
              area_cap_mm2: int | None = None,
              area_mm2_per_device: int | None = None,
              price_per_device_hour: str = "3.0",
              actions: tuple = ACTIONS) -> dict:
    """Build the execution graph, rewrite it per action, then screen the results."""
    for name, value in (("tokens", tokens), ("batch", batch)):
        positive_int(value, name)
    positive_int(history, "history", allow_zero=True)
    if power_cap_watts is not None:
        positive_int(power_cap_watts, "power_cap_watts")
    if area_cap_mm2 is not None:
        positive_int(area_cap_mm2, "area_cap_mm2")
    if area_mm2_per_device is not None:
        positive_int(area_mm2_per_device, "area_mm2_per_device")
    chosen = tuple(actions)
    if not chosen or any(action not in ACTIONS for action in chosen):
        raise ValueError("Unknown candidate action requested")
    if "baseline" not in chosen:
        raise ValueError("Screening needs the baseline graph to compare against")

    rows = [candidate(action, model, device, tokens, history, batch, state_bits, decode_device)
            for action in chosen]
    result = screen(rows, power_cap_watts, area_cap_mm2, area_mm2_per_device,
                    price_per_device_hour)
    baseline = next(row for row in rows if row["action"] == "baseline")

    return {
        "calculation": "execution-dag-screening",
        "inputs": {"model": model, "device": device, "decode_device": decode_device,
                   "tokens": tokens, "history": history, "batch": batch,
                   "state_bits": state_bits, "power_cap_watts": power_cap_watts,
                   "area_cap_mm2": area_cap_mm2, "area_mm2_per_device": area_mm2_per_device,
                   "price_per_device_hour": price_per_device_hour,
                   "actions": list(chosen)},
        "sources": baseline["sources"],
        "baseline_graph": {"critical_path": baseline["graph"]["critical_path"],
                           "node_count": baseline["graph"]["node_count"],
                           "interface_bytes_total": baseline["graph"]["interface_bytes_total"],
                           "bound_seconds": baseline["graph"]["bound_seconds"]},
        "state_edges": baseline["state_edges"],
        "nodes": baseline["nodes"],
        "candidates": [{key: row[key] for key in
                        ("action", "note", "added_cost", "call", "location", "devices",
                         "graph", "state_transfer", "capacity_bytes", "capacity_split",
                         "device_nominal_bytes", "fits_capacity", "power_watts",
                         "power_published", "tokens_per_call")}
                       for row in rows],
        "screening": result,
        "area_status": ("declared per-device footprint" if area_mm2_per_device is not None
                        else "no area figure declared, so the area axis is not screened"),
        "coverage_gaps": sorted({name for row in rows
                                 for name in row["graph"]["resources_without_a_published_rate"]}),
        "assumptions": [
            "Node work is the pinned stage accounting on an official model config; device rates, capacity and power come from the source-checked catalog.",
            "A stage bound covers only resources whose rate the catalog publishes; the rest are listed as gaps and never filled in.",
            "The graph bound assumes each node's resources may overlap inside the node and that nodes on one location run serially; it is a lower bound, not an achievable latency.",
            "Die area is not published for these parts, so area is screened only when a footprint is declared.",
            "Prices are declared teaching inputs; no vendor tariff is claimed.",
            "Every rewrite lists what it adds as well as what it removes, and a rewrite that fails a cap is excluded before any objective is compared.",
        ],
    }


def markdown(result: dict) -> str:
    def seconds(entry):
        return "—" if entry is None else f"{float(Fraction(**entry)):.6f}"

    lines = ["# 完整执行 DAG 的资源下界与候选筛选", "",
             f"节点工作取自固定配置的逐阶段账，设备速率／容量／功率取自来源核对的硬件表。"
             f"关键路径共 {result['baseline_graph']['node_count']} 个节点，"
             f"接口字节合计 {result['baseline_graph']['interface_bytes_total']}，"
             f"基线下界 {seconds(result['baseline_graph']['bound_seconds'])} s。", "",
             "## 状态的产生、复用、更新与释放", "",
             "| 状态 | 产生 | 复用 | 更新 | 释放 | 字节 |", "|---|---|---|---|---|---:|"]
    for row in result["state_edges"]:
        lines.append("| " + " | ".join([
            row["state"], row["produced"], row["reused"], row["updated"], row["released"],
            "—" if row["bytes"] is None else str(row["bytes"])]) + " |")

    lines += ["", "## 候选动作：去掉什么、又增加什么", "",
              "| 动作 | 说明 | 新增代价 | 设备数 | 下界 s | 容量 B | 适配 |",
              "|---|---|---|---:|---:|---:|---|"]
    for row in result["candidates"]:
        lines.append("| " + " | ".join([
            row["action"], row["note"] or "基线", "；".join(row["added_cost"]) or "—",
            str(row["devices"]), seconds(row["graph"]["bound_seconds"]),
            str(row["capacity_bytes"]), "是" if row["fits_capacity"] else "否"]) + " |")

    screening = result["screening"]
    lines += ["", "## 多目标筛选", "",
              "上限先于目标：不满足容量、功率或面积上限的候选在比较之前排除。", "",
              "| 动作 | 下界 s | 吞吐 tok/s | 每 token 成本 | 功率 W | 面积 mm² | 可选 | 原因 |",
              "|---|---:|---:|---:|---:|---:|---|---|"]
    for row in screening["scored"]:
        lines.append("| " + " | ".join([
            row["action"], seconds(row["latency_bound_seconds"]),
            f"{float(Fraction(**row['throughput_tokens_per_second'])):.1f}",
            f"{float(Fraction(**row['cost_per_token'])):.9f}",
            str(row["power_watts"]), "—" if row["area_mm2"] is None else str(row["area_mm2"]),
            "是" if row["admissible"] else "否", "；".join(row["reasons"])]) + " |")

    lines += ["", f"- 帕累托前沿：{'、'.join(screening['pareto_front']) or '空'}",
              f"- 被支配：{'；'.join(row['action'] + ' ← ' + '、'.join(row['dominated_by']) for row in screening['dominated']) or '无'}",
              f"- 因上限排除：{'；'.join(row['action'] for row in screening['excluded_by_caps']) or '无'}",
              f"- 最低延迟：{screening['lowest_latency']}；最高吞吐：{screening['highest_throughput']}；"
              f"最低每 token 成本：{screening['lowest_cost_per_token']}", "",
              f"面积口径：{result['area_status']}。"]
    if result["coverage_gaps"]:
        lines += ["", f"未公布速率因而未计入下界的资源：{'、'.join(result['coverage_gaps'])}。"]
    lines += ["", "## 口径与限制", ""]
    lines += ["- " + item for item in result["assumptions"]]
    lines += ["", "## 完整输入、来源与结果", "", "```json",
              json.dumps(result, ensure_ascii=False, indent=2), "```", ""]
    return "\n".join(lines)
