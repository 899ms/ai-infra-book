"""PP4 Qwen3-8B synchronous GPipe/1F1B conditional event schedules."""

import math
from collections import Counter
from fractions import Fraction
from . import training_nonmatrix
from ..models import qwen3
from ..sources import model_config, provenance
from ..units import positive_int


def _vector(value, length, name):
    if not isinstance(value, (list, tuple)) or len(value) != length:
        raise ValueError(f"{name} requires {length} finite nonnegative values")
    if any(type(x) not in (int, float) or not math.isfinite(x) or x < 0 for x in value):
        raise ValueError(f"{name} requires finite nonnegative values")
    return list(value)


def _work(batch, tokens, policy):
    source = training_nonmatrix.calculate(
        batch=batch, tokens=tokens, activation_policy=policy
    )
    config = model_config("qwen3-8b")
    if config["num_hidden_layers"] != 36:
        raise ValueError("This fixed PP4 partition requires exactly 36 layers")
    stages = [
        dict(
            stage=s,
            layers=list(range(9 * s, 9 * (s + 1))),
            matrices=[],
            nonmatrix=[],
            parameters=0,
            saved_objects=[],
        )
        for s in range(4)
    ]
    for op in source["training_matrix_original"]["training_matrix_rows"]:
        owners = range(4) if op["repeats"] == 36 else [3]
        copies = 9 if op["repeats"] == 36 else 1
        for s in owners:
            stages[s]["matrices"].append(
                dict(
                    name=op["name"],
                    shapes=op["shapes"],
                    copies=copies,
                    forward_flops=op["forward_flops"] * copies,
                    backward_flops=2 * op["forward_flops"] * copies,
                )
            )
    setup = []
    for op in source["nonmatrix_operations"]:
        if op["name"] == "rotary_table_per_step":
            setup.append(op)
            continue
        if op["name"] == "embedding_scatter_add":
            owners, divisor = [0], 1
        elif op["name"] in ("final_rmsnorm", "mean_cross_entropy"):
            owners, divisor = [3], 1
        else:
            owners, divisor = range(4), 4
        for s in owners:
            row = dict(
                name=op["name"],
                forward_scalar_flops=op["forward_scalar_flops"] // divisor,
                backward_scalar_flops=op["backward_scalar_flops"] // divisor,
                forward_special_ops={
                    k: v // divisor for k, v in op["forward_special_ops"].items()
                },
                backward_special_ops={
                    k: v // divisor for k, v in op["backward_special_ops"].items()
                },
            )
            stages[s]["nonmatrix"].append(row)
    for item in source["saved_objects"]:
        stage = 3 if item["layer"] is None else item["layer"] // 9
        stages[stage]["saved_objects"].append(item)
    for weight in qwen3.weights(config):
        if weight.copies == 36:
            for stage in stages:
                stage["parameters"] += weight.parameters // 4
        else:
            owner = 0 if "embed_tokens" in weight.name else 3
            stages[owner]["parameters"] += weight.parameters
    for stage in stages:
        stage["forward_matrix_flops"] = sum(
            x["forward_flops"] for x in stage["matrices"]
        )
        stage["backward_matrix_flops"] = sum(
            x["backward_flops"] for x in stage["matrices"]
        )
        stage["forward_scalar_flops"] = sum(
            x["forward_scalar_flops"] for x in stage["nonmatrix"]
        )
        stage["backward_scalar_flops"] = sum(
            x["backward_scalar_flops"] for x in stage["nonmatrix"]
        )
        stage["nonlinear_saved_bytes_per_microbatch"] = sum(
            x["bytes"] for x in stage["saved_objects"]
        )
    return stages, setup, source


def _orders(microbatches, policy):
    if policy == "gpipe":
        return [
            [("F", m) for m in range(microbatches)]
            + [("B", m) for m in reversed(range(microbatches))]
            for _ in range(4)
        ]
    orders = []
    for stage in range(4):
        warmup = min(3 - stage, microbatches)
        order = [("F", m) for m in range(warmup)]
        for i in range(microbatches - warmup):
            order.extend([("F", i + warmup), ("B", i)])
        order.extend(("B", i) for i in range(microbatches - warmup, microbatches))
        orders.append(order)
    return orders


def _schedule(nodes):
    """Deterministic nonpreemptive earliest-ready list scheduling on unary resources."""
    pending = dict(nodes)
    done, free = {}, {}
    while pending:
        ready = []
        for name, node in pending.items():
            if all(dep in done for dep in node["dependencies"]):
                start = max(
                    [free.get(node["resource"], 0.0)]
                    + [done[d]["end"] for d in node["dependencies"]]
                )
                ready.append((start, node["priority"], name))
        if not ready:
            raise ValueError("Pipeline ordering contains a dependency cycle")
        start, _, name = min(ready)
        node = pending.pop(name)
        end = start + node["duration"]
        if not math.isfinite(end):
            raise ValueError("Schedule time exceeds finite numeric range")
        done[name] = dict(node, id=name, start=start, end=end)
        free[node["resource"]] = end
    return done


def _peaks(intervals):
    result = []
    for stage in range(4):
        events = []
        for item in intervals:
            if item["stage"] != stage or item["start"] == item["end"]:
                continue
            events.extend(
                [
                    (item["start"], 1, item["bytes"], item["id"]),
                    (item["end"], 0, -item["bytes"], item["id"]),
                ]
            )
        live = peak = 0
        timeline = []
        for time, _, delta, identity in sorted(events):
            live += delta
            if live < 0:
                raise AssertionError("Negative reserved activation bytes")
            peak = max(peak, live)
            timeline.append(
                dict(time=time, object=identity, delta_bytes=delta, live_bytes=live)
            )
        if live:
            raise AssertionError("Activation reservations did not drain")
        result.append(
            dict(stage=stage, peak_declared_reserved_bytes=peak, events=timeline)
        )
    return result


def calculate(
    microbatches=8,
    microbatch_size=1,
    tokens=128,
    policy="1f1b",
    forward_seconds=(0.01, 0.01, 0.01, 0.01),
    backward_seconds=(0.02, 0.02, 0.02, 0.02),
    activation_transfer_seconds=(0.001, 0.001, 0.001),
    gradient_transfer_seconds=(0.001, 0.001, 0.001),
    link_mode="independent_directional",
    activation_policy="save_nonlinear",
    additional_saved_bytes=(0, 0, 0, 0),
    optimizer_seconds=(0.001, 0.001, 0.001, 0.001),
    setup_seconds=0.0,
    virtual_stages=2,
    declared_weight_backward_fraction="1/2",
    wraparound_transfer_seconds=0.001,
):
    for name, value in [
        ("microbatches", microbatches),
        ("microbatch_size", microbatch_size),
        ("tokens", tokens),
    ]:
        positive_int(value, name)
    if policy in EXTENDED_POLICIES:
        return _extended(
            microbatches, microbatch_size, tokens, policy, forward_seconds, backward_seconds,
            activation_transfer_seconds, gradient_transfer_seconds, link_mode, activation_policy,
            additional_saved_bytes, optimizer_seconds, setup_seconds, virtual_stages,
            declared_weight_backward_fraction, wraparound_transfer_seconds,
        )
    if policy not in ("gpipe", "1f1b"):
        raise ValueError("policy must be gpipe, 1f1b, interleaved_1f1b, zero_bubble or dualpipe")
    if link_mode not in ("independent_directional", "shared_half_duplex"):
        raise ValueError("Unknown link serialization contract")
    forward_seconds = _vector(forward_seconds, 4, "forward_seconds")
    backward_seconds = _vector(backward_seconds, 4, "backward_seconds")
    activation_transfer_seconds = _vector(
        activation_transfer_seconds, 3, "activation_transfer_seconds"
    )
    gradient_transfer_seconds = _vector(
        gradient_transfer_seconds, 3, "gradient_transfer_seconds"
    )
    optimizer_seconds = _vector(optimizer_seconds, 4, "optimizer_seconds")
    additional_saved_bytes = _vector(
        additional_saved_bytes, 4, "additional_saved_bytes"
    )
    if any(type(x) is not int for x in additional_saved_bytes):
        raise ValueError("additional_saved_bytes must contain integer byte counts")
    _vector([setup_seconds], 1, "setup_seconds")
    stages, setup, source = _work(microbatch_size, tokens, activation_policy)
    config = model_config("qwen3-8b")
    orders = _orders(microbatches, policy)
    nodes = {}

    def add(name, kind, stage, mb, duration, resource, deps, priority):
        nodes[name] = dict(
            kind=kind,
            stage=stage,
            microbatch=mb,
            duration=duration,
            resource=resource,
            dependencies=list(dict.fromkeys(deps)),
            priority=priority,
        )

    add("setup", "setup", None, None, setup_seconds, "setup", [], 0)
    for stage, order in enumerate(orders):
        previous = "setup"
        for kind, mb in order:
            name = f"{kind}:{stage}:{mb}"
            deps = [previous]
            if kind == "F" and stage:
                deps.append(f"A:{stage-1}:{mb}")
            if kind == "B":
                deps.append(f"F:{stage}:{mb}")
                if stage < 3:
                    deps.append(f"G:{stage+1}:{mb}")
                if policy == "gpipe":
                    deps.append(f"F:3:{microbatches-1}")
            add(
                name,
                kind,
                stage,
                mb,
                (forward_seconds if kind == "F" else backward_seconds)[stage],
                f"compute:{stage}",
                deps,
                2 if kind == "B" else 3,
            )
            previous = name
    for stage in range(3):
        for mb in range(microbatches):
            resource = (
                "link:shared"
                if link_mode == "shared_half_duplex"
                else f"link:A:{stage}"
            )
            add(
                f"A:{stage}:{mb}",
                "A",
                stage,
                mb,
                activation_transfer_seconds[stage],
                resource,
                [f"F:{stage}:{mb}"],
                1,
            )
            resource = (
                "link:shared"
                if link_mode == "shared_half_duplex"
                else f"link:G:{stage}"
            )
            add(
                f"G:{stage+1}:{mb}",
                "G",
                stage + 1,
                mb,
                gradient_transfer_seconds[stage],
                resource,
                [f"B:{stage+1}:{mb}"],
                1,
            )
    all_gradients = [
        f"B:{stage}:{mb}" for stage in range(4) for mb in range(microbatches)
    ]
    for stage in range(4):
        add(
            f"U:{stage}",
            "update",
            stage,
            None,
            optimizer_seconds[stage],
            f"compute:{stage}",
            all_gradients,
            4,
        )
    events = _schedule(nodes)
    gradient_ready = max(events[name]["end"] for name in all_gradients)
    makespan = max(e["end"] for e in events.values())
    intervals = []

    def reserve(identity, stage, start, end, amount, kind):
        intervals.append(
            dict(
                id=identity, stage=stage, start=start, end=end, bytes=amount, kind=kind
            )
        )

    for stage in range(4):
        saved = (
            stages[stage]["nonlinear_saved_bytes_per_microbatch"]
            + additional_saved_bytes[stage]
        )
        for mb in range(microbatches):
            f, b = events[f"F:{stage}:{mb}"], events[f"B:{stage}:{mb}"]
            reserve(
                f"saved:{stage}:{mb}",
                stage,
                f["start"],
                b["end"],
                saved,
                "declared_saved_reservation",
            )
            if activation_policy == "recompute_silu":
                # One layer's two FP32 temporary vectors at a time; reserve for whole stage B.
                amount = 8 * microbatch_size * tokens * config["intermediate_size"]
                reserve(
                    f"recompute:{stage}:{mb}",
                    stage,
                    b["start"],
                    b["end"],
                    amount,
                    "recompute_workspace_reservation",
                )
    activation_bytes = 2 * microbatch_size * tokens * config["hidden_size"]
    gradient_bytes = 4 * microbatch_size * tokens * config["hidden_size"]
    for event in events.values():
        if event["kind"] not in ("A", "G"):
            continue
        kind, stage, mb = event["kind"], event["stage"], event["microbatch"]
        target = stage + 1 if kind == "A" else stage - 1
        compute_kind = "F" if kind == "A" else "B"
        amount = activation_bytes if kind == "A" else gradient_bytes
        reserve(
            event["id"] + ":send",
            stage,
            events[f"{compute_kind}:{stage}:{mb}"]["end"],
            event["end"],
            amount,
            "send_buffer",
        )
        reserve(
            event["id"] + ":receive",
            target,
            event["start"],
            events[f"{compute_kind}:{target}:{mb}"]["start"],
            amount,
            "receive_buffer",
        )
    peaks = _peaks(intervals)
    zero_nodes = {
        name: dict(node, duration=0 if node["kind"] in ("A", "G") else node["duration"])
        for name, node in nodes.items()
    }
    no_transfer = max(e["end"] for e in _schedule(zero_nodes).values())
    stage_summary = []
    for stage in range(4):
        useful = microbatches * (forward_seconds[stage] + backward_seconds[stage])
        stage_summary.append(
            dict(
                stage=stage,
                forward_backward_service_seconds=useful,
                idle_during_training_seconds=gradient_ready - setup_seconds - useful,
                update_seconds=optimizer_seconds[stage],
                peak_declared_reserved_bytes=peaks[stage][
                    "peak_declared_reserved_bytes"
                ],
            )
        )
    params = sum(stage["parameters"] for stage in stages)
    for stage in stages:
        stage["microbatch_gradient_accumulation_additions"] = (
            microbatches - 1
        ) * stage["parameters"]
        stage["mean_gradient_scale_operations"] = (
            stage["parameters"] if microbatches > 1 else 0
        )
        stage["optimizer_parameter_scalar_flops"] = 14 * stage["parameters"]
    scenario = dict(
        microbatches=microbatches,
        microbatch_size=microbatch_size,
        tokens=tokens,
        policy=policy,
        forward_seconds=forward_seconds,
        backward_seconds=backward_seconds,
        activation_transfer_seconds=activation_transfer_seconds,
        gradient_transfer_seconds=gradient_transfer_seconds,
        link_mode=link_mode,
        activation_policy=activation_policy,
        additional_saved_bytes=additional_saved_bytes,
        optimizer_seconds=optimizer_seconds,
        setup_seconds=setup_seconds,
    )
    return dict(
        calculation="qwen8-training-pipeline-schedule",
        schema_version=1,
        scenario=scenario,
        sources=provenance("qwen3-8b"),
        partition=dict(model="qwen3-8b", stages=4, layers_per_stage=9),
        work=dict(
            per_microbatch_stages=stages,
            once_per_step_rotary_setup=setup,
            per_microbatch_public_data_operations=source["data_operations"],
            all_microbatches_forward_matrix_flops=microbatches
            * sum(s["forward_matrix_flops"] for s in stages),
            all_microbatches_backward_matrix_flops=microbatches
            * sum(s["backward_matrix_flops"] for s in stages),
            all_microbatches_forward_scalar_flops=microbatches
            * sum(s["forward_scalar_flops"] for s in stages)
            + sum(s["forward_scalar_flops"] for s in setup),
            all_microbatches_backward_scalar_flops=microbatches
            * sum(s["backward_scalar_flops"] for s in stages),
            step_parameter_accumulation_and_mean_scalar_flops=(microbatches - 1)
            * params
            + (params if microbatches > 1 else 0),
            total_parameters=params,
            once_per_step_optimizer=source["optimizer"],
            gradient_accumulation="First microbatch initializes dense stage parameter gradient; remaining M-1 add, then divide by M once. Equal token/label counts per microbatch.",
        ),
        stage_orders=[
            [dict(kind=k, microbatch=mb) for k, mb in order] for order in orders
        ],
        events=sorted(
            events.values(), key=lambda e: (e["start"], e["priority"], e["id"])
        ),
        activation_intervals=intervals,
        activation_timelines=peaks,
        stages=stage_summary,
        transfers=dict(
            activation_bytes_per_boundary=activation_bytes,
            gradient_bytes_per_boundary=gradient_bytes,
            forward_messages=3 * microbatches,
            backward_messages=3 * microbatches,
            total_payload_bytes=3 * microbatches * (activation_bytes + gradient_bytes),
        ),
        summary=dict(
            total_sequences=microbatches * microbatch_size,
            total_tokens=microbatches * microbatch_size * tokens,
            gradient_ready_seconds=gradient_ready,
            step_makespan_seconds=makespan,
            zero_transfer_counterfactual_seconds=no_transfer,
            exposed_transfer_makespan_delta_seconds=makespan - no_transfer,
            useful_forward_backward_device_seconds=sum(
                s["forward_backward_service_seconds"] for s in stage_summary
            ),
            reserved_activation_scope_peak_bytes=[
                s["peak_declared_reserved_bytes"] for s in stage_summary
            ],
            complete_training_activation_peak_bytes=None,
            measured_runtime_seconds=None,
        ),
        assumptions=[
            "Fixed non-interleaved synchronous PP4; one compute stream per stage, nonpreemptive events. Optimizer is one logical update after every microbatch gradient, with parallel stage-local updates. No stale weights.",
            "Service times are explicit conditional inputs, not vendor peaks or measurements. F/B services include the selected nonlinear recompute policy, parameter accumulation, label handling and any unexpanded kernels; the scalar/matrix work ledger does not derive these seconds.",
            "GPipe runs all forwards before reverse-order backwards. 1F1B uses stage-dependent warmup, FIFO microbatch backwards and cooldown. Compute and links overlap subject to dependencies and declared unary resources.",
            "Independent directional mode gives each boundary/direction a dedicated serialized link. Shared half duplex uses one resource for every boundary and direction. Deterministic earliest-ready tie ordering is part of the contract; no claim of globally optimal communication arbitration.",
            "Saved bytes reuse public nonlinear objects and optional explicit extra bytes. Reserve the entire per-stage subset from forward START through backward END. This is a deliberate conservative reservation, not exact within-stage allocation times or full model peak.",
            "Recompute_silu only replaces saved nonlinear SiLU state and reserves one layer temporary pair throughout B. It is not full-layer checkpointing. Do not infer lower service time from reduced saved bytes.",
            "Transfers use separate packed BF16 hidden activation and FP32 hidden-gradient buffers. Receiver buffer starts at transfer START and is released at consumer START; sender is live from producer END to transfer END. Copies into internal backward state are outside the partial memory ledger.",
            "RoPE table work is once per step; setup_seconds includes distribution or an explicitly supplied local preparation strategy. Embedding belongs to stage0, head/final norm/loss to stage3. Dense full-token supervision, no historical KV, no MoE.",
            "Gradient contributions use equal per-microbatch mean losses then average gradients once before update. Accumulation counts are separate from each public per-microbatch VJP; update hyperparameter coefficients execute once, not M times.",
            "Idle time includes fill/drain, ordering and dependency waits; exposed transfer is a counterfactual makespan difference, not the sum of link busy times. Parameter/optimizer state, GEMM saved inputs not explicitly supplied, full temporary gradients and allocator workspaces are excluded from reported activation peak.",
        ],
    )


def markdown(result):
    lines = [
        "# Qwen3-8B PP4 training schedule",
        "",
        "Conditional GPipe/1F1B event execution and declared activation reservations; not measured runtime.",
        "",
        "| Field | Value |",
        "|---|---|",
    ]

    def visit(value, path=""):
        if isinstance(value, dict) and value:
            for key, item in value.items():
                visit(item, f"{path}.{key}" if path else key)
        elif isinstance(value, list) and value:
            for i, item in enumerate(value):
                visit(item, f"{path}[{i}]")
        else:
            text = "unknown (null)" if value is None else str(value)
            lines.append(
                f"| {path} | "
                + text.replace("|", "&#124;").replace("\n", "<br>")
                + " |"
            )

    visit(result)
    return "\n".join(lines) + "\n"


# ----------------------------------------------------------------------------------------------
# Extended schedules: interleaved 1F1B (virtual stages), zero-bubble (split backward), DualPipe.
#
# Schedule rules and where they come from:
# - 1F1B itself: references/text/pipedream.txt line 447-449 ("this mechanism one-forward-one-backward (1F1B).
#   In a balanced pipeline, 1F1B ensures that no GPU is idle in" steady state); non-interleaved bubble
#   t_pb = (p-1)(t_f + t_b), references/text/megatron-scale.txt line 231.
# - Interleaved 1F1B with v model chunks per GPU: references/text/megatron-scale.txt line 286 ("for a
#   microbatch for each stage or chunk will now be t_f/v and t_b/v"), line 293 (bubble fraction
#   (1/v)(p-1)/m) and line 234 ("amount of communication also increases by v").  The archived text gives
#   the chunk timing and bubble formula but not the per-GPU slot order, so the ordering below (warmup =
#   (p-g-1)*2 + (v-1)*p forwards, then 1F1B, chunk of the k-th forward = (k // p) mod v, microbatch =
#   (k // (p v)) p + k mod p, Megatron-LM's implementation) is recorded as declared_schedule_rule.
# - Zero bubble: references/text/zero-bubble.txt line 254 ("TW < TF < TB and TB + TW = 2TF"), line 282-284
#   (Table 2: 1F1B (p-1)(TF+TB+TW), ZB-H1 (p-1)(TF+TB-TW) with memory pMB, ZB-H2 (p-1)(TF+TB-2TW) with
#   memory (2p-1)MB, where TB is the input-gradient part and TW the weight-gradient part of the backward),
#   lines 222-229 (ZB-H1 "generally follows the 1F1B schedule, but it adjusts the starting points of W
#   depending on the number of warm-up microbatches. This ensures all workers maintain the same number
#   of in-flight microbatches") and the Figure 3 (top) slot table at lines 192-199: device g (0-indexed)
#   runs F/B in 1F1B order with p-1-g warmup forwards and places W of microbatch i right after B of
#   microbatch i+g (device 1: B1 W1 F5 B2 W2 ...; device 2: B2 W1 F5 B3 W2 ...; device 4: B4 W1 F5 B5 W2 ...),
#   the last g W's after the final B.  With TF = TB = TW (the module's default 10/10/10 ms) this order is
#   reproduced exactly; its bubble is the Table 2 bound (p-1)(TF+TB-TW).  references/text/deepseek-v3.txt
#   lines 653-655 ("both attention and MLP are further split into two parts, backward for input and
#   backward for weights, like in ZeroBubble").
# - DualPipe: references/text/deepseek-v3.txt lines 660-663 ("bidirectional pipeline scheduling, which
#   feeds micro-batches from both ends of the pipeline simultaneously"), line 704-705 ("DualPipe requires
#   keeping two copies of the model parameters") and Table 2 ("(PP/2-1)(F&B+B-3W)", parameters 2x,
#   activation PP+1).  Figure 5's exact slot order is not reproduced; each direction runs a split-backward
#   1F1B order on its own stage copy (W of microbatch i after X of microbatch i+(p-1-g) in that direction,
#   remaining W in the cooldown) and the GPU's compute stream arbitrates between the two directions with
#   the module's earliest-ready rule.  This is a declared_schedule_rule as well.
# - Bubble bounds recorded in summary: 1F1B (p-1)(TF+TB+TW); interleaved (p-1)(TF+TB+TW)/v, fraction
#   (1/v)(p-1)/m; ZB-H1 (p-1)(TF+TB-TW); ZB-H2 (p-1)(TF+TB-2TW); DualPipe (p/2-1)(F&B+B-3W) with
#   F&B = F + B and DeepSeek's full backward B = TB + TW.  TB/TW split by declared_weight_backward_fraction.
# ----------------------------------------------------------------------------------------------
EXTENDED_POLICIES = ("interleaved_1f1b", "zero_bubble", "dualpipe")


def _work_groups(batch, tokens, policy, groups):
    """Generalized _work for arbitrary contiguous layer groups (one per virtual stage)."""
    source = training_nonmatrix.calculate(batch=batch, tokens=tokens, activation_policy=policy)
    config = model_config("qwen3-8b")
    layers = config["num_hidden_layers"]
    if sorted(layer for group in groups for layer in group) != list(range(layers)):
        raise ValueError("Layer groups must partition the model layers exactly once")
    first = next(i for i, g in enumerate(groups) if 0 in g)
    last = next(i for i, g in enumerate(groups) if layers - 1 in g)
    stages = [dict(stage=i, layers=list(g), matrices=[], nonmatrix=[], parameters=0, saved_objects=[])
              for i, g in enumerate(groups)]
    for op in source["training_matrix_original"]["training_matrix_rows"]:
        if op["repeats"] == layers:
            owners = [(i, len(g)) for i, g in enumerate(groups)]
        else:
            owners = [(last, 1)]
        for s, copies in owners:
            stages[s]["matrices"].append(dict(name=op["name"], shapes=op["shapes"], copies=copies,
                                              forward_flops=op["forward_flops"] * copies,
                                              backward_flops=2 * op["forward_flops"] * copies))
    setup = []
    for op in source["nonmatrix_operations"]:
        if op["name"] == "rotary_table_per_step":
            setup.append(op)
            continue
        if op["name"] == "embedding_scatter_add":
            owners = [(first, 1, 1)]
        elif op["name"] in ("final_rmsnorm", "mean_cross_entropy"):
            owners = [(last, 1, 1)]
        else:
            owners = [(i, len(g), layers) for i, g in enumerate(groups)]
        for s, numerator, divisor in owners:
            stages[s]["nonmatrix"].append(dict(
                name=op["name"],
                forward_scalar_flops=op["forward_scalar_flops"] // divisor * numerator,
                backward_scalar_flops=op["backward_scalar_flops"] // divisor * numerator,
                forward_special_ops={k: v // divisor * numerator for k, v in op["forward_special_ops"].items()},
                backward_special_ops={k: v // divisor * numerator for k, v in op["backward_special_ops"].items()}))
    for item in source["saved_objects"]:
        stage = last if item["layer"] is None else next(i for i, g in enumerate(groups) if item["layer"] in g)
        stages[stage]["saved_objects"].append(item)
    for weight in qwen3.weights(config):
        if weight.copies == layers:
            for s, g in enumerate(groups):
                stages[s]["parameters"] += weight.parameters // layers * len(g)
        else:
            stages[first if "embed_tokens" in weight.name else last]["parameters"] += weight.parameters
    for stage in stages:
        stage["forward_matrix_flops"] = sum(x["forward_flops"] for x in stage["matrices"])
        stage["backward_matrix_flops"] = sum(x["backward_flops"] for x in stage["matrices"])
        stage["forward_scalar_flops"] = sum(x["forward_scalar_flops"] for x in stage["nonmatrix"])
        stage["backward_scalar_flops"] = sum(x["backward_scalar_flops"] for x in stage["nonmatrix"])
        stage["nonlinear_saved_bytes_per_microbatch"] = sum(x["bytes"] for x in stage["saved_objects"])
    return stages, setup, source


def _one_f1b_order(position, stages, count, split, deferral):
    """Per-stage 1F1B order with optional split backward; W_i follows X_(i+deferral).

    deferral = position reproduces ZB-H1 (zero-bubble.txt Figure 3 top): stage g keeps g deferred
    W's plus p-1-g warmup forwards in flight, the same p-1 count on every stage.
    """
    warmup = min(stages - 1 - position, count)
    order = [("F", m) for m in range(warmup)]
    for i in range(count - warmup):
        order.extend([("F", i + warmup), ("X" if split else "B", i)])
    order.extend(("X" if split else "B", i) for i in range(count - warmup, count))
    if not split:
        return order
    result, placed = [], set()
    for kind, m in order:
        result.append((kind, m))
        if kind == "X" and m - deferral >= 0:
            result.append(("W", m - deferral))
            placed.add(m - deferral)
    result.extend(("W", m) for m in range(count) if m not in placed)
    return result


def _interleaved_order(gpu, gpus, chunks, count):
    """Megatron interleaved 1F1B order for one GPU (declared rule; see module comment)."""
    if count % gpus:
        raise ValueError("interleaved_1f1b requires microbatches divisible by the pipeline depth")
    total = chunks * count

    def forward_item(k):
        return (k // gpus) % chunks, (k // (gpus * chunks)) * gpus + k % gpus

    def backward_item(k):
        return chunks - 1 - (k // gpus) % chunks, (k // (gpus * chunks)) * gpus + k % gpus

    warmup = min((gpus - gpu - 1) * 2 + (chunks - 1) * gpus, total)
    order = [("F",) + forward_item(k) for k in range(warmup)]
    for k in range(total - warmup):
        order.append(("F",) + forward_item(k + warmup))
        order.append(("B",) + backward_item(k))
    order.extend(("B",) + backward_item(k) for k in range(total - warmup, total))
    return order


def _extended(microbatches, microbatch_size, tokens, policy, forward_seconds, backward_seconds,
              activation_transfer_seconds, gradient_transfer_seconds, link_mode, activation_policy,
              additional_saved_bytes, optimizer_seconds, setup_seconds, virtual_stages,
              declared_weight_backward_fraction, wraparound_transfer_seconds):
    gpus = 4
    if link_mode not in ("independent_directional", "shared_half_duplex"):
        raise ValueError("Unknown link serialization contract")
    forward_seconds = _vector(forward_seconds, gpus, "forward_seconds")
    backward_seconds = _vector(backward_seconds, gpus, "backward_seconds")
    activation_transfer_seconds = _vector(activation_transfer_seconds, 3, "activation_transfer_seconds")
    gradient_transfer_seconds = _vector(gradient_transfer_seconds, 3, "gradient_transfer_seconds")
    optimizer_seconds = _vector(optimizer_seconds, gpus, "optimizer_seconds")
    additional_saved_bytes = _vector(additional_saved_bytes, gpus, "additional_saved_bytes")
    if any(type(x) is not int for x in additional_saved_bytes):
        raise ValueError("additional_saved_bytes must contain integer byte counts")
    _vector([setup_seconds, wraparound_transfer_seconds], 2, "setup/wraparound seconds")
    positive_int(virtual_stages, "virtual_stages")
    split = policy in ("zero_bubble", "dualpipe")
    fraction = Fraction(declared_weight_backward_fraction)
    if not 0 < fraction < 1:
        raise ValueError("declared_weight_backward_fraction must lie strictly between 0 and 1")
    config = model_config("qwen3-8b")
    layers = config["num_hidden_layers"]
    per_gpu = layers // gpus
    if per_gpu * gpus != layers:
        raise ValueError("This fixed PP4 partition requires layers divisible by four")
    # Virtual stage table: stage id -> gpu, chunk, direction, layer group, flow position.
    virtual, flows = [], {}
    if policy == "interleaved_1f1b":
        chunks = virtual_stages
        if chunks < 1 or chunks > per_gpu:
            raise ValueError("virtual_stages must lie between 1 and the layers per GPU")
        sizes = [per_gpu // chunks + (1 if c < per_gpu % chunks else 0) for c in range(chunks)]
        groups, cursor = [], 0
        for s in range(gpus * chunks):
            size = sizes[s // gpus]
            groups.append(list(range(cursor, cursor + size)))
            cursor += size
        virtual = [dict(stage=s, gpu=s % gpus, chunk=s // gpus, direction=0, layers=groups[s]) for s in range(gpus * chunks)]
        flows = {0: list(range(gpus * chunks))}
        counts = {0: microbatches}
    else:
        chunks = 1
        groups = [list(range(per_gpu * g, per_gpu * (g + 1))) for g in range(gpus)]
        virtual = [dict(stage=s, gpu=s, chunk=0, direction=0, layers=groups[s]) for s in range(gpus)]
        flows = {0: list(range(gpus))}
        counts = {0: microbatches}
        if policy == "dualpipe":
            if microbatches % 2:
                raise ValueError("dualpipe requires an even number of microbatches (half per direction)")
            virtual += [dict(stage=gpus + s, gpu=gpus - 1 - s, chunk=1, direction=1, layers=groups[s]) for s in range(gpus)]
            flows = {0: list(range(gpus)), 1: list(range(gpus, 2 * gpus))}
            counts = {0: microbatches // 2, 1: microbatches // 2}
    stages, setup, source = _work_groups(microbatch_size, tokens, activation_policy, groups)
    group_of = {v["stage"]: (v["stage"] if v["direction"] == 0 else v["stage"] - gpus) for v in virtual}
    by_stage = {v["stage"]: v for v in virtual}
    nodes = {}

    def add(name, kind, gpu, mb, duration, resource, deps, priority, stage=None, direction=0):
        nodes[name] = dict(kind=kind, stage=gpu, virtual_stage=stage, direction=direction, microbatch=mb,
                           duration=duration, resource=resource, dependencies=list(dict.fromkeys(deps)),
                           priority=priority)

    def link(a, b, kind):
        if link_mode == "shared_half_duplex":
            resource = "link:shared"
        else:
            resource = f"link:{a}->{b}"
        boundary = min(a, b)
        if abs(a - b) == 1:
            duration = (activation_transfer_seconds if kind == "A" else gradient_transfer_seconds)[boundary]
        else:
            duration = wraparound_transfer_seconds
        return resource, duration

    def duration(stage, kind):
        v = by_stage[stage]
        scale = len(v["layers"]) / per_gpu
        base = (forward_seconds if kind == "F" else backward_seconds)[v["gpu"]] * scale
        if kind == "F" or kind == "B":
            return base
        if kind == "X":
            return base * float(1 - fraction)
        return base * float(fraction)

    add("setup", "setup", None, None, setup_seconds, "setup", [], 0)
    orders = {}
    for direction, flow in flows.items():
        count = counts[direction]
        for position, stage in enumerate(flow):
            v = by_stage[stage]
            if policy == "interleaved_1f1b":
                if v["chunk"] != 0:
                    continue  # one order per GPU covers all its chunks
                order = [(kind, flow[chunk * gpus + v["gpu"]], mb) for kind, chunk, mb in _interleaved_order(v["gpu"], gpus, chunks, count)]
                orders[(v["gpu"], direction)] = order
            else:
                # ZB-H1: stage g defers W by g microbatches (Figure 3 top).  DualPipe keeps its
                # declared per-direction rule (W_i after X_(i+p-1-g)); see the module comment.
                deferral = position if policy == "zero_bubble" else len(flow) - 1 - position
                orders[(v["gpu"], direction)] = [(kind, stage, mb) for kind, mb in _one_f1b_order(position, len(flow), count, split, deferral)]
    for (gpu, direction), order in orders.items():
        previous = "setup"
        flow = flows[direction]
        for kind, stage, mb in order:
            name = f"{kind}:{stage}:{mb}:{direction}"
            position = flow.index(stage)
            deps = [previous]
            if kind == "F" and position:
                deps.append(f"A:{flow[position-1]}:{mb}:{direction}")
            if kind in ("B", "X"):
                deps.append(f"F:{stage}:{mb}:{direction}")
                if position < len(flow) - 1:
                    deps.append(f"G:{stage}:{mb}:{direction}")
            if kind == "W":
                deps.append(f"X:{stage}:{mb}:{direction}")
            priority = {"F": 3, "B": 2, "X": 2, "W": 4}[kind]
            add(name, kind, gpu, mb, duration(stage, kind), f"compute:{gpu}", deps, priority, stage, direction)
            previous = name
    for direction, flow in flows.items():
        for position in range(len(flow) - 1):
            sender, receiver = flow[position], flow[position + 1]
            a, b = by_stage[sender]["gpu"], by_stage[receiver]["gpu"]
            for mb in range(counts[direction]):
                resource, seconds = link(a, b, "A")
                add(f"A:{sender}:{mb}:{direction}", "A", a, mb, seconds, resource, [f"F:{sender}:{mb}:{direction}"], 1, sender, direction)
                resource, seconds = link(b, a, "G")
                back = "X" if split else "B"
                add(f"G:{sender}:{mb}:{direction}", "G", b, mb, seconds, resource, [f"{back}:{receiver}:{mb}:{direction}"], 1, receiver, direction)
    backward_nodes = [name for name, node in nodes.items() if node["kind"] in ("B", "X", "W")]
    for gpu in range(gpus):
        add(f"U:{gpu}", "update", gpu, None, optimizer_seconds[gpu], f"compute:{gpu}", backward_nodes, 5)
    events = _schedule(nodes)
    gradient_ready = max(events[name]["end"] for name in backward_nodes)
    makespan = max(e["end"] for e in events.values())
    intervals = []

    def reserve(identity, gpu, start, end, amount, kind):
        intervals.append(dict(id=identity, stage=gpu, start=start, end=end, bytes=amount, kind=kind))

    for v in virtual:
        stage, gpu, direction = v["stage"], v["gpu"], v["direction"]
        saved = stages[group_of[stage]]["nonlinear_saved_bytes_per_microbatch"] + additional_saved_bytes[gpu]
        for mb in range(counts[direction]):
            f = events[f"F:{stage}:{mb}:{direction}"]
            last = events[f"{'W' if split else 'B'}:{stage}:{mb}:{direction}"]
            reserve(f"saved:{stage}:{mb}:{direction}", gpu, f["start"], last["end"], saved, "declared_saved_reservation")
            if activation_policy == "recompute_silu":
                amount = 8 * microbatch_size * tokens * config["intermediate_size"]
                first = events[f"{'X' if split else 'B'}:{stage}:{mb}:{direction}"]
                reserve(f"recompute:{stage}:{mb}:{direction}", gpu, first["start"], last["end"], amount, "recompute_workspace_reservation")
    activation_bytes = 2 * microbatch_size * tokens * config["hidden_size"]
    gradient_bytes = 4 * microbatch_size * tokens * config["hidden_size"]
    for event in events.values():
        if event["kind"] not in ("A", "G"):
            continue
        kind, stage, mb, direction = event["kind"], event["virtual_stage"], event["microbatch"], event["direction"]
        flow = flows[direction]
        position = flow.index(stage)
        if kind == "A":
            producer, consumer = f"F:{stage}:{mb}:{direction}", f"F:{flow[position+1]}:{mb}:{direction}"
            source_gpu, target_gpu = by_stage[stage]["gpu"], by_stage[flow[position + 1]]["gpu"]
            amount = activation_bytes
        else:
            back = "X" if split else "B"
            producer, consumer = f"{back}:{stage}:{mb}:{direction}", f"{back}:{flow[position-1]}:{mb}:{direction}"
            source_gpu, target_gpu = by_stage[stage]["gpu"], by_stage[flow[position - 1]]["gpu"]
            amount = gradient_bytes
        reserve(event["id"] + ":send", source_gpu, events[producer]["end"], event["end"], amount, "send_buffer")
        reserve(event["id"] + ":receive", target_gpu, event["start"], events[consumer]["start"], amount, "receive_buffer")
    peaks = _peaks(intervals)
    zero_nodes = {name: dict(node, duration=0 if node["kind"] in ("A", "G") else node["duration"]) for name, node in nodes.items()}
    zero_events = _schedule(zero_nodes)
    no_transfer = max(e["end"] for e in zero_events.values())
    zero_gradient_ready = max(zero_events[name]["end"] for name in backward_nodes)
    # Bubble bounds (see module comment).  T_F = stage-0 forward, T_B = input-gradient part of the
    # stage-0 backward, T_W = weight-gradient part; DeepSeek's full backward B = T_B + T_W, F&B = F + B.
    t_f, t_full = forward_seconds[0], backward_seconds[0]
    t_w = t_full * float(fraction)
    t_b = t_full - t_w
    bounds = dict(
        bubble_bound_1f1b_seconds=(gpus - 1) * (t_f + t_b + t_w),
        bubble_bound_1f1b_fraction=(gpus - 1) / microbatches,
        bubble_bound_interleaved_seconds=(gpus - 1) * (t_f + t_b + t_w) / chunks if policy == "interleaved_1f1b" else None,
        bubble_bound_interleaved_fraction=(gpus - 1) / microbatches / chunks if policy == "interleaved_1f1b" else None,
        bubble_bound_zb_h1_seconds=(gpus - 1) * (t_f + t_b - t_w),
        bubble_bound_zb_h2_seconds=(gpus - 1) * (t_f + t_b - 2 * t_w),
        bubble_bound_dualpipe_seconds=(gpus / 2 - 1) * ((t_f + t_full) + t_full - 3 * t_w) if policy == "dualpipe" else None,
    )
    policy_bound = {"interleaved_1f1b": bounds["bubble_bound_interleaved_seconds"],
                    "zero_bubble": bounds["bubble_bound_zb_h1_seconds"],
                    "dualpipe": bounds["bubble_bound_dualpipe_seconds"]}[policy]
    stage_summary = []
    for gpu in range(gpus):
        useful = sum(e["duration"] for e in events.values() if e["kind"] in ("F", "B", "X", "W") and e["stage"] == gpu)
        stage_summary.append(dict(stage=gpu, forward_backward_service_seconds=useful,
                                  idle_during_training_seconds=gradient_ready - setup_seconds - useful,
                                  idle_zero_transfer_counterfactual_seconds=zero_gradient_ready - setup_seconds - useful,
                                  bubble_bound_policy_seconds=policy_bound,
                                  bubble_bound_zb_h1_seconds=bounds["bubble_bound_zb_h1_seconds"],
                                  bubble_bound_zb_h2_seconds=bounds["bubble_bound_zb_h2_seconds"],
                                  update_seconds=optimizer_seconds[gpu],
                                  peak_declared_reserved_bytes=peaks[gpu]["peak_declared_reserved_bytes"],
                                  virtual_stages=[v["stage"] for v in virtual if v["gpu"] == gpu],
                                  parameter_copies=sum(stages[group_of[v["stage"]]]["parameters"] for v in virtual if v["gpu"] == gpu)))
    params = sum(stage["parameters"] for stage in stages)
    for stage in stages:
        stage["microbatch_gradient_accumulation_additions"] = (microbatches - 1) * stage["parameters"]
        stage["mean_gradient_scale_operations"] = stage["parameters"] if microbatches > 1 else 0
        stage["optimizer_parameter_scalar_flops"] = 14 * stage["parameters"]
    messages = sum((len(flow) - 1) * counts[d] for d, flow in flows.items())
    reference = dict(
        t_f_seconds=t_f, t_b_input_gradient_seconds=t_b, t_w_weight_gradient_seconds=t_w,
        full_backward_seconds=t_full,
        one_f1b_bubble=bounds["bubble_bound_1f1b_seconds"],
        one_f1b_bubble_fraction=bounds["bubble_bound_1f1b_fraction"],
        interleaved_bubble=bounds["bubble_bound_interleaved_seconds"],
        interleaved_bubble_fraction=bounds["bubble_bound_interleaved_fraction"],
        zb_h1_or_zb1p_bubble=bounds["bubble_bound_zb_h1_seconds"],
        zb_h2_bubble=bounds["bubble_bound_zb_h2_seconds"],
        dualpipe_bubble_with_fb_equal_f_plus_b=(gpus / 2 - 1) * ((t_f + t_full) + t_full - 3 * t_w),
        source="megatron-scale.txt lines 231/293 ((p-1)(t_f+t_b), (1/v)(p-1)/m); zero-bubble.txt lines 282-284 (1F1B (p-1)(TF+TB+TW), ZB-H1 (p-1)(TF+TB-TW), ZB-H2 (p-1)(TF+TB-2TW); TB = input-gradient pass, TW = weight-gradient pass); deepseek-v3.txt Table 2 line 688-691 (ZB1P (PP-1)(F+B-2W) with full backward B = TB+TW, i.e. the ZB-H1 bound; DualPipe (PP/2-1)(F&B+B-3W)); uniform stage-0 times, TW = declared fraction x full backward, F&B taken as F+B (no compute overlap modeled)")
    rule = {
        "interleaved_1f1b": f"Megatron interleaved 1F1B: v={chunks} chunks per GPU; warmup forwards = (p-g-1)*2+(v-1)*p; k-th forward is chunk (k//p) mod v of microbatch (k//(p*v))*p + k mod p; backward mirrors with chunks reversed.",
        "zero_bubble": "ZB-H1 (zero-bubble.txt Figure 3 top, Table 2): stage g (0-indexed) runs the 1F1B order for F and the input-gradient backward X (the paper's B) with p-1-g warmup forwards; the weight-gradient backward W of microbatch i is placed immediately after X of microbatch i+g, so every stage holds the same p-1 microbatches of deferred work in flight (stage 0: X0 W0 F4 X1 W1 ...; stage 3: X3 W0 F4 X4 W1 ...); the last g W's run after the final X. Steady state is F, X, W per microbatch; the remaining bubble is the Table 2 bound (p-1)(T_F+T_B-T_W) plus transfer exposure.",
        "dualpipe": "Bidirectional: half the microbatches enter at stage 0 and half at stage 3 on a second parameter copy; each direction follows a split-backward 1F1B order on its own stage copy (W of microbatch i after X of microbatch i+(p-1-g) in that direction, remaining W in the cooldown); one compute stream per GPU arbitrates by the module's earliest-ready rule. Figure 5's slot order is not reproduced.",
    }[policy]
    scenario = dict(microbatches=microbatches, microbatch_size=microbatch_size, tokens=tokens, policy=policy,
                    forward_seconds=forward_seconds, backward_seconds=backward_seconds,
                    activation_transfer_seconds=activation_transfer_seconds, gradient_transfer_seconds=gradient_transfer_seconds,
                    link_mode=link_mode, activation_policy=activation_policy, additional_saved_bytes=additional_saved_bytes,
                    optimizer_seconds=optimizer_seconds, setup_seconds=setup_seconds, virtual_stages=virtual_stages,
                    declared_weight_backward_fraction=declared_weight_backward_fraction,
                    wraparound_transfer_seconds=wraparound_transfer_seconds)
    return dict(
        calculation="qwen8-training-pipeline-schedule", schema_version=1, scenario=scenario,
        sources=provenance("qwen3-8b"),
        partition=dict(model="qwen3-8b", stages=gpus, layers_per_stage=per_gpu, virtual_stages=virtual,
                       parameter_copies_per_gpu=2 if policy == "dualpipe" else 1),
        declared_schedule_rule=rule,
        work=dict(per_microbatch_stages=stages, once_per_step_rotary_setup=setup,
                  per_microbatch_public_data_operations=source["data_operations"],
                  all_microbatches_forward_matrix_flops=microbatches * sum(s["forward_matrix_flops"] for s in stages),
                  all_microbatches_backward_matrix_flops=microbatches * sum(s["backward_matrix_flops"] for s in stages),
                  all_microbatches_forward_scalar_flops=microbatches * sum(s["forward_scalar_flops"] for s in stages)
                  + sum(s["forward_scalar_flops"] for s in setup),
                  all_microbatches_backward_scalar_flops=microbatches * sum(s["backward_scalar_flops"] for s in stages),
                  step_parameter_accumulation_and_mean_scalar_flops=(microbatches - 1) * params + (params if microbatches > 1 else 0),
                  total_parameters=params, once_per_step_optimizer=source["optimizer"],
                  gradient_accumulation="First microbatch initializes dense stage parameter gradient; remaining M-1 add, then divide by M once. Equal token/label counts per microbatch. DualPipe's second parameter copy holds the same gradient, reduced once."),
        stage_orders={f"gpu{g}:direction{d}": [dict(kind=k, virtual_stage=s, microbatch=mb) for k, s, mb in order] for (g, d), order in orders.items()},
        events=sorted(events.values(), key=lambda e: (e["start"], e["priority"], e["id"])),
        activation_intervals=intervals, activation_timelines=peaks, stages=stage_summary,
        transfers=dict(activation_bytes_per_boundary=activation_bytes, gradient_bytes_per_boundary=gradient_bytes,
                       forward_messages=messages, backward_messages=messages,
                       total_payload_bytes=messages * (activation_bytes + gradient_bytes),
                       boundary_crossings_per_microbatch=max(len(flow) - 1 for flow in flows.values())),
        bubble_reference=reference,
        summary=dict(total_sequences=microbatches * microbatch_size, total_tokens=microbatches * microbatch_size * tokens,
                     gradient_ready_seconds=gradient_ready, step_makespan_seconds=makespan,
                     zero_transfer_counterfactual_seconds=no_transfer,
                     exposed_transfer_makespan_delta_seconds=makespan - no_transfer,
                     useful_forward_backward_device_seconds=sum(s["forward_backward_service_seconds"] for s in stage_summary),
                     idle_device_seconds=sum(s["idle_during_training_seconds"] for s in stage_summary),
                     idle_per_stage_seconds=[s["idle_during_training_seconds"] for s in stage_summary],
                     idle_per_stage_zero_transfer_counterfactual_seconds=[s["idle_zero_transfer_counterfactual_seconds"] for s in stage_summary],
                     bubble_bound_policy_seconds=policy_bound,
                     **bounds,
                     reserved_activation_scope_peak_bytes=[s["peak_declared_reserved_bytes"] for s in stage_summary],
                     complete_training_activation_peak_bytes=None, measured_runtime_seconds=None),
        assumptions=[
            "Fixed PP4 on four GPUs; interleaved_1f1b places v contiguous layer chunks per GPU (chunk c of GPU g is virtual stage c*4+g); zero_bubble keeps 9 layers per GPU and splits every backward into input part X and weight part W by the declared fraction; dualpipe adds a second stage copy per GPU for the reverse direction (parameters 2x) and splits backward the same way.",
            "Service times scale with the layers in each virtual stage relative to 9; transfer times reuse the per-boundary inputs of the base schedule, and the interleaved wrap-around link 3->0 uses wraparound_transfer_seconds. Links are physical directed edges shared by both DualPipe directions.",
            "Per-GPU orders follow the declared_schedule_rule recorded in the output. zero_bubble reproduces the ZB-H1 slot order of zero-bubble.txt Figure 3 (top); for interleaved_1f1b and dualpipe the archived texts give the idea (chunked stages, bidirectional feeding) and the exact slot placement is this module's rule, not the paper's figure. The scheduler is the same nonpreemptive earliest-ready list scheduler as GPipe/1F1B.",
            "Saved activations are reserved from forward start to the end of the last backward part (W when split), so a stage holding g deferred W's reserves their full saved set rather than the paper's smaller M_W; send/receive buffers as in the base schedule. Idle time = gradient-ready time minus setup minus useful compute per GPU; the zero-transfer counterfactual idle isolates the schedule bubble from transfer exposure.",
            "bubble_bound_* fields evaluate the archived bubble formulas (megatron-scale, zero-bubble Table 2, DeepSeek-V3 Table 2) with uniform stage-0 service times, T_B/T_W split by the declared fraction and F&B = F + B; they are bounds without communication, not this schedule's measured idle. bubble_bound_policy_seconds is the bound for the selected policy.",
        ],
    )
