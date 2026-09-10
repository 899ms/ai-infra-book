"""C76: uncertainty, the measurement worth taking, and a falsifiable record.

A decision made from declared inputs is only as good as the inputs' intervals.
This module takes a decision another topic already computes, moves each
uncertain input across its declared interval on its own, and reports three
things: whether that input's uncertainty can change the decision at all, how
far outside its interval the input would have to go before it did, and which
single measurement therefore buys the most.

It then states what the decision predicts for configurations deliberately held
out of it, as intervals a later measurement can fall outside of, and writes the
whole thing into the record fields the cross-chapter design record asks for:
candidates, first prediction, evidence type, observation, revised decision, the
next limit, the flip condition and the minimum measurement that would settle it.

Evidence is labelled. An analytical recomputation of the same model is never
counted as an independent measurement of it.
"""
from fractions import Fraction
import json

from ..units import positive_int, positive_number
from . import execution_dag, specialization_payback

EVIDENCE_KINDS = ("measured", "paper_reported", "teaching_input", "analytical_model")

# Bisection stops here; the result is reported as a bracket, never as a root.
FLIP_TOLERANCE = Fraction(1, 1000)
SEARCH_MULTIPLE = 64


def fraction(value: Fraction) -> dict:
    return {"numerator": value.numerator, "denominator": value.denominator}


def exact(value) -> Fraction:
    return Fraction(str(value))


def payback_outcome(scenario: str = "planned", **overrides) -> dict:
    """Does a named case repay the fixed cost, and by what margin?"""
    result = specialization_payback.calculate(**overrides)
    row = next((entry for entry in result["scenarios"] if entry["scenario"] == scenario), None)
    if row is None:
        raise ValueError("Unknown payback scenario: " + scenario)
    if "coverage" not in row:
        return {"label": "no_serving_period", "margin": Fraction(0)}
    return {"label": "pays_back" if row["pays_back"] else "does_not_pay_back",
            "margin": Fraction(**row["coverage"])}


def screening_outcome(action: str | None = None, **overrides) -> dict:
    """Which rewrite wins on cost per token, or how one named rewrite stands.

    With no action named this reports the winner and its lead over the runner-up.
    Naming an action reports that action's own standing instead, which is what a
    held-out candidate needs.
    """
    result = execution_dag.calculate(**overrides)
    rows = [row for row in result["screening"]["scored"] if row["admissible"]]
    if not rows:
        return {"label": "no_admissible_candidate", "margin": Fraction(0)}
    ordered = sorted(rows, key=lambda row: Fraction(**row["cost_per_token"]))
    best = Fraction(**ordered[0]["cost_per_token"])
    if action is None:
        runner = Fraction(**ordered[1]["cost_per_token"]) if len(ordered) > 1 else best
        return {"label": ordered[0]["action"], "margin": (runner / best) if best else Fraction(0)}
    named = next((row for row in result["screening"]["scored"] if row["action"] == action), None)
    if named is None:
        raise ValueError("Unknown screening action: " + action)
    if not named["admissible"]:
        return {"label": "excluded_by_caps", "margin": Fraction(0)}
    dominated = any(row["action"] == action for row in result["screening"]["dominated"])
    return {"label": "dominated" if dominated else "on_the_front",
            "margin": Fraction(**named["cost_per_token"]) / best if best else Fraction(0)}


DECISIONS = {
    "specialisation_payback": {
        "question": "Do the operating savings repay the specialisation before the model is replaced?",
        "outcome": payback_outcome,
        "section": "4.6.5",
        "nominal": {},
        "uncertain_inputs": {
            "saving_per_million_tokens": {"low": "0.30", "nominal": "0.50", "high": "0.80",
                                          "evidence": "teaching_input", "numeric": True},
            "utilisation": {"low": "0.3", "nominal": "0.5", "high": "0.7",
                            "evidence": "teaching_input", "numeric": True},
            "electricity_price_per_kwh": {"low": "0.04", "nominal": "0.08", "high": "0.15",
                                          "evidence": "teaching_input", "numeric": True},
            "machines": {"low": 60, "nominal": 100, "high": 160,
                         "evidence": "teaching_input", "numeric": True, "integer": True},
            "economic_life_months": {"low": 6, "nominal": 12, "high": 18,
                                     "evidence": "teaching_input", "numeric": True, "integer": True},
        },
        "held_out": [
            {"name": "life_halves", "selector": {"scenario": "life_halves"},
             "reason": "kept out of the decision so it can test it"},
            {"name": "output_rate_falls", "selector": {"scenario": "output_rate_falls"},
             "reason": "kept out of the decision so it can test it"},
        ],
        "candidates": ["build the specialisation", "stay on the general-purpose fleet"],
    },
    "execution_dag_screening": {
        "question": "Which graph rewrite wins on cost per token under the declared caps?",
        "outcome": screening_outcome,
        "section": "1.3, 9.6",
        "nominal": {},
        "uncertain_inputs": {
            "price_per_device_hour": {"low": "1.0", "nominal": "3.0", "high": "8.0",
                                      "evidence": "teaching_input", "numeric": True,
                                      "search_multiple": 8},
            "power_cap_watts": {"low": 700, "nominal": 1500, "high": 4000,
                                "evidence": "teaching_input", "numeric": True, "integer": True,
                                "search_multiple": 4},
            "history": {"low": 1024, "nominal": 4096, "high": 32768,
                        "evidence": "analytical_model", "numeric": True, "integer": True,
                        "search": False},
        },
        "held_out": [
            {"name": "disaggregate", "selector": {"action": "disaggregate"},
             "reason": "priced but never chosen, so its standing is a prediction"},
        ],
        "candidates": list(execution_dag.ACTIONS),
    },
}


def evaluate(decision: dict, overrides: dict) -> dict:
    call = dict(decision["nominal"])
    call.update(overrides)
    return decision["outcome"](**call)


def endpoint_scan(decision: dict) -> list:
    """Move one input at a time to each end of its declared interval."""
    base = evaluate(decision, {})
    rows = []
    for name, spec in decision["uncertain_inputs"].items():
        entries = {}
        for end in ("low", "nominal", "high"):
            outcome = evaluate(decision, {name: spec[end]})
            entries[end] = {"value": spec[end], "label": outcome["label"],
                            "margin": fraction(outcome["margin"])}
        labels = {entries[end]["label"] for end in ("low", "nominal", "high")}
        margins = [Fraction(**entries[end]["margin"]) for end in ("low", "nominal", "high")]
        rows.append({"input": name, "evidence": spec["evidence"],
                     "interval": [spec["low"], spec["high"]], "nominal": spec["nominal"],
                     "points": entries,
                     "changes_the_decision_within_its_interval": len(labels) > 1,
                     "margin_swing": fraction(max(margins) - min(margins))})
    return {"baseline": {"label": base["label"], "margin": fraction(base["margin"])},
            "inputs": rows}


def flip_bracket(decision: dict, name: str, spec: dict) -> dict:
    """Smallest bracket outside which this input alone changes the decision.

    Bisection on one input with everything else nominal. The answer is a
    bracket at the declared tolerance, never a root: the decision function is
    not known to be continuous and is not claimed to be.
    """
    if spec.get("search") is False:
        return {"direction": None, "bracket": None, "outside_label": None,
                "inside_declared_interval": False, "searched": False,
                "reason": (f"{name} is not searched beyond its declared interval: each "
                           "evaluation rebuilds the whole graph, so the endpoint scan above "
                           "is the evidence for it")}
    baseline = evaluate(decision, {})["label"]
    integer = bool(spec.get("integer"))
    nominal = exact(spec["nominal"])
    multiple = spec.get("search_multiple", SEARCH_MULTIPLE)
    if nominal <= 0:
        raise ValueError("A nominal value must be positive to search around it")

    def label(value):
        cast = int(value) if integer else str(value)
        try:
            return evaluate(decision, {name: cast})["label"]
        except ValueError:
            return None

    for direction in (1, -1):
        far = nominal * multiple if direction > 0 else nominal / multiple
        if integer:
            far = Fraction(max(1, int(far)))
        outer = label(far)
        if outer is None or outer == baseline:
            continue
        low, high = (nominal, far) if direction > 0 else (far, nominal)
        while (high - low) > (FLIP_TOLERANCE * nominal if not integer else 1):
            middle = (low + high) / 2
            if integer:
                middle = Fraction(int(middle))
                if middle in (low, high):
                    break
            found = label(middle)
            if found == baseline:
                low, high = (middle, high) if direction > 0 else (low, middle)
            else:
                low, high = (low, middle) if direction > 0 else (middle, high)
        boundary = high if direction > 0 else low
        within = exact(spec["low"]) <= boundary <= exact(spec["high"])
        return {"direction": "above" if direction > 0 else "below",
                "bracket": [fraction(low), fraction(high)],
                "outside_label": outer, "searched": True,
                "inside_declared_interval": within,
                "reason": (f"Moving {name} {'above' if direction > 0 else 'below'} this bracket, "
                           f"with everything else nominal, changes the decision to {outer}")}
    return {"direction": None, "bracket": None, "outside_label": None,
            "inside_declared_interval": False, "searched": True,
            "reason": (f"Within a factor of {multiple} either way, {name} alone never "
                       "changes the decision")}


def value_of_information(scan: dict, brackets: dict) -> list:
    """Rank inputs by whether measuring one could change what is decided."""
    rows = []
    for entry in scan["inputs"]:
        name = entry["input"]
        bracket = brackets[name]
        if entry["changes_the_decision_within_its_interval"]:
            rank, verdict = 0, "measuring this can change the decision inside its own interval"
        elif bracket["direction"] is not None:
            rank, verdict = 1, ("the decision only changes outside this input's declared "
                                "interval, so measuring it settles confidence, not the choice")
        elif bracket.get("searched") is False:
            rank, verdict = 2, ("not searched beyond its interval; the endpoint scan is the "
                                "evidence, and it did not change the decision")
        else:
            rank, verdict = 3, "this input alone never changes the decision in the searched range"
        rows.append({"input": name, "evidence": entry["evidence"], "rank": rank,
                     "margin_swing": entry["margin_swing"],
                     "flip": bracket, "verdict": verdict})
    return sorted(rows, key=lambda row: (row["rank"], -Fraction(**row["margin_swing"])))


def held_out_predictions(decision: dict) -> list:
    """What the decision predicts for cases it was not allowed to use.

    The interval comes from the same input intervals, so a later measurement
    landing outside it refutes the account rather than merely surprising it.
    """
    rows = []
    for entry in decision["held_out"]:
        corners = [evaluate(decision, dict(entry["selector"]))]
        for name, spec in decision["uncertain_inputs"].items():
            for end in ("low", "high"):
                corners.append(evaluate(decision, dict(entry["selector"], **{name: spec[end]})))
        labels = sorted({outcome["label"] for outcome in corners})
        margins = [outcome["margin"] for outcome in corners]
        rows.append({"configuration": entry["name"], "reason": entry["reason"],
                     "predicted_labels": labels,
                     "predicted_margin_interval": [fraction(min(margins)), fraction(max(margins))],
                     "falsified_if": ("an observation of this configuration lands outside the "
                                      "predicted margin interval, or produces a label not listed")})
    return rows


def record(name: str, decision: dict, scan: dict, ranked: list, predictions: list) -> dict:
    """The cross-chapter record fields, filled from this decision."""
    best = ranked[0] if ranked else None
    decisive = [row for row in ranked if row["rank"] == 0]
    return {
        "decision": name, "section": decision["section"], "question": decision["question"],
        "candidates": decision["candidates"],
        "first_prediction": scan["baseline"]["label"],
        "evidence_kinds": sorted({row["evidence"] for row in ranked}),
        "observation": ("None yet. Every input above is a declared teaching value or an "
                        "analytical recomputation, and a recomputation of the same model is "
                        "not an independent measurement of it."),
        "revised_decision": scan["baseline"]["label"],
        "revision_reason": ("Unchanged: nothing here is new evidence, only the same account "
                            "moved across its declared intervals."),
        "next_limit": (decisive[0]["input"] if decisive else
                       (best["input"] if best else None)),
        "flip_condition": (best["flip"]["reason"] if best else None),
        "minimum_measurement": (
            f"Measure {decisive[0]['input']} well enough to place it inside or outside its "
            f"declared interval; it is the only input whose own interval changes the decision."
            if decisive else
            f"No declared interval changes this decision on its own. The cheapest useful "
            f"measurement is still {best['input']}, and it buys confidence rather than a "
            f"different choice." if best else None),
        "held_out_predictions": predictions,
    }


def calculate(decisions: tuple = tuple(DECISIONS)) -> dict:
    """Run the uncertainty, value-of-information and record pass over decisions."""
    chosen = tuple(decisions)
    if not chosen or any(name not in DECISIONS for name in chosen):
        raise ValueError("Unknown decision requested")
    rows = []
    for name in chosen:
        decision = DECISIONS[name]
        scan = endpoint_scan(decision)
        brackets = {input_name: flip_bracket(decision, input_name, spec)
                    for input_name, spec in decision["uncertain_inputs"].items()}
        ranked = value_of_information(scan, brackets)
        predictions = held_out_predictions(decision)
        rows.append({"name": name, "scan": scan, "value_of_information": ranked,
                     "record": record(name, decision, scan, ranked, predictions)})
    return {
        "calculation": "design-record-uncertainty",
        "inputs": {"decisions": list(chosen),
                   "flip_tolerance": fraction(FLIP_TOLERANCE),
                   "search_multiple": SEARCH_MULTIPLE},
        "evidence_kinds": list(EVIDENCE_KINDS),
        "decisions": rows,
        "assumptions": [
            "Each input is moved on its own with the others at nominal; joint moves are not covered.",
            "A flip is reported as a bisection bracket at the declared tolerance, never as a root.",
            "The search covers a bounded factor either way; outside it nothing is claimed.",
            "Evidence kind is recorded per input, and an analytical recomputation of the same model is not an independent measurement of it.",
            "Held-out predictions are intervals a later measurement can fall outside of; they are refutable, not confirmed.",
            "No observation has been entered yet, so no revised decision here rests on new evidence.",
        ],
    }


def markdown(result: dict) -> str:
    def number(entry, places=4):
        return "—" if entry is None else f"{float(Fraction(**entry)):.{places}f}"

    def bounds(pair):
        return "—" if pair is None else f"[{number(pair[0])}, {number(pair[1])}]"

    lines = ["# 输入区间、最有价值的补测与可证伪预测", "",
             "每次只移动一个输入，其余保持标称值。翻转以二分区间给出，不写成精确根。"
             "证据类型逐项标注；对同一模型的复算不充当该模型的独立测量。", ""]
    for entry in result["decisions"]:
        record = entry["record"]
        lines += [f"## {record['decision']}（{record['section']}）", "",
                  f"问题：{record['question']}", "",
                  f"- 候选：{'、'.join(record['candidates'])}",
                  f"- 初次预测：{record['first_prediction']}",
                  f"- 证据类型：{'、'.join(record['evidence_kinds'])}",
                  f"- 观察：{record['observation']}",
                  f"- 修改后的决定：{record['revised_decision']}（{record['revision_reason']}）",
                  f"- 下一个限制：{record['next_limit']}",
                  f"- 翻转条件：{record['flip_condition']}",
                  f"- 最小补测：{record['minimum_measurement']}", "",
                  "| 输入 | 证据 | 区间 | 低端 | 标称 | 高端 | 区间内可改变决定 | 余量摆幅 |",
                  "|---|---|---|---|---|---|---|---:|"]
        for row in entry["scan"]["inputs"]:
            points = row["points"]
            lines.append("| " + " | ".join([
                row["input"], row["evidence"], f"[{row['interval'][0]}, {row['interval'][1]}]",
                points["low"]["label"], points["nominal"]["label"], points["high"]["label"],
                "是" if row["changes_the_decision_within_its_interval"] else "否",
                number(row["margin_swing"])]) + " |")

        lines += ["", "| 补测优先级 | 输入 | 结论 | 翻转方向 | 翻转区间 |", "|---:|---|---|---|---|"]
        for index, row in enumerate(entry["value_of_information"], start=1):
            flip = row["flip"]
            lines.append("| " + " | ".join([
                str(index), row["input"], row["verdict"],
                flip["direction"] or "—", bounds(flip["bracket"])]) + " |")

        lines += ["", "### 留出配置的可证伪预测", "",
                  "| 配置 | 留出理由 | 预测标签 | 预测余量区间 | 何时被证伪 |", "|---|---|---|---|---|"]
        for row in record["held_out_predictions"]:
            lines.append("| " + " | ".join([
                row["configuration"], row["reason"], "、".join(row["predicted_labels"]),
                bounds(row["predicted_margin_interval"]), row["falsified_if"]]) + " |")
        lines.append("")

    lines += ["## 口径与限制", ""]
    lines += ["- " + item for item in result["assumptions"]]
    lines += ["", "## 完整输入与结果", "", "```json",
              json.dumps(result, ensure_ascii=False, indent=2), "```", ""]
    return "\n".join(lines)
