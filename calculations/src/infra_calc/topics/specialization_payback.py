"""C75: can operating savings pay off a specialisation (4.6.5, 11.4.1, 12.6.1).

A one-off engineering cost is repaid only by traffic that actually arrives, on
machines that are actually delivered, before the model they serve is replaced.
This module solves the break-even volume exactly, converts it into the machine
count and the calendar it implies, and then applies the three things that move
it: a delivery period that eats the economic life, an economic life that ends
sooner than planned, and an effective output rate that falls short.

It also prices the site the machines sit in -- electricity through a cooling
overhead, network and backup -- so that a per-token saving quoted before site
cost can be checked against one quoted after it.

Every amount here is a declared teaching input. None is a vendor price, a
project estimate, or a measurement.
"""
from fractions import Fraction
import json

from ..units import positive_int

SECONDS_PER_YEAR = 31_536_000
SECONDS_PER_WEEK = 604_800
MILLION = 10 ** 6


def fraction(value: Fraction) -> dict:
    return {"numerator": value.numerator, "denominator": value.denominator}


def exact(value) -> Fraction:
    return Fraction(str(value))


def payback_volume(fixed_cost, saving_per_million_tokens) -> Fraction:
    """Tokens the saving has to cover before the fixed cost is repaid."""
    fixed = exact(fixed_cost)
    saving = exact(saving_per_million_tokens)
    if fixed < 0:
        raise ValueError("An incremental fixed cost cannot be negative")
    if saving <= 0:
        raise ValueError("A payback needs a positive per-token saving")
    return fixed / (saving / MILLION)


def effective_output(machines: int, tokens_per_second: int, utilisation,
                     seconds: Fraction) -> Fraction:
    """Useful tokens a fleet delivers over a period at a declared utilisation."""
    positive_int(machines, "machines")
    positive_int(tokens_per_second, "tokens_per_second")
    share = exact(utilisation)
    if not 0 < share <= 1:
        raise ValueError("Utilisation must fall in (0, 1]")
    if seconds <= 0:
        raise ValueError("The serving period must be positive")
    return Fraction(machines) * tokens_per_second * share * seconds


def site_cost(machines: int, machine_power_kw, cooling_overhead,
              electricity_price_per_kwh, network_cost_per_year,
              backup_cost_per_year, seconds: Fraction) -> dict:
    """Electricity through cooling, plus network and backup, for one period."""
    power = exact(machine_power_kw)
    overhead = exact(cooling_overhead)
    price = exact(electricity_price_per_kwh)
    network = exact(network_cost_per_year)
    backup = exact(backup_cost_per_year)
    if power <= 0 or price < 0 or network < 0 or backup < 0:
        raise ValueError("Site inputs must be nonnegative, with positive machine power")
    if overhead < 1:
        raise ValueError("A cooling overhead below one would return energy to the grid")
    hours = seconds / 3600
    years = seconds / SECONDS_PER_YEAR
    facility_kw = Fraction(machines) * power * overhead
    energy = facility_kw * hours
    return {"machines": machines,
            "machine_power_kw": fraction(power), "cooling_overhead": fraction(overhead),
            "facility_power_kw": fraction(facility_kw),
            "energy_kwh": fraction(energy),
            "electricity_cost": fraction(energy * price),
            "network_cost": fraction(network * years),
            "backup_cost": fraction(backup * years),
            "total_site_cost": fraction(energy * price + (network + backup) * years),
            "note": ("Electricity is metered at the facility, so the cooling overhead applies "
                     "to it and not to the network or backup lines.")}


def scenario(name: str, fixed_cost, saving_per_million_tokens, machines: int,
             tokens_per_second: int, utilisation, life_seconds: Fraction,
             delivery_seconds: Fraction, site: dict | None) -> dict:
    """One payback case: volume required, volume delivered, and the gap."""
    if delivery_seconds < 0:
        raise ValueError("A delivery period cannot be negative")
    serving = life_seconds - delivery_seconds
    if serving <= 0:
        return {"scenario": name, "serving_seconds": fraction(serving), "pays_back": False,
                "reason": "Delivery consumes the whole economic life; nothing is served"}
    required = payback_volume(fixed_cost, saving_per_million_tokens)
    delivered = effective_output(machines, tokens_per_second, utilisation, serving)
    per_machine = effective_output(1, tokens_per_second, utilisation, serving)
    needed = -(-required.numerator * per_machine.denominator
               // (required.denominator * per_machine.numerator))
    row = {"scenario": name,
           "life_seconds": fraction(life_seconds),
           "delivery_seconds": fraction(delivery_seconds),
           "serving_seconds": fraction(serving),
           "machines": machines, "tokens_per_second": tokens_per_second,
           "utilisation": fraction(exact(utilisation)),
           "required_tokens": fraction(required),
           "delivered_tokens": fraction(delivered),
           "coverage": fraction(delivered / required),
           "pays_back": delivered >= required,
           "machines_required": needed,
           "machine_shortfall": max(0, needed - machines),
           "reason": ("The declared fleet delivers enough over this life"
                      if delivered >= required else
                      f"This life needs {needed} machines of the same output, and the demand to fill them")}
    if site is not None:
        cost = site_cost(machines, site["machine_power_kw"], site["cooling_overhead"],
                         site["electricity_price_per_kwh"], site["network_cost_per_year"],
                         site["backup_cost_per_year"], serving)
        gross = exact(saving_per_million_tokens)
        per_token_site = Fraction(**cost["total_site_cost"]) / delivered if delivered else None
        net = gross - (per_token_site * MILLION if per_token_site is not None else Fraction(0))
        row["site"] = cost
        row["site_cost_per_million_tokens"] = (None if per_token_site is None
                                               else fraction(per_token_site * MILLION))
        row["net_saving_per_million_tokens"] = fraction(net)
        row["saving_survives_site_cost"] = net > 0
        if net > 0:
            net_required = payback_volume(fixed_cost, net)
            row["required_tokens_net_of_site"] = fraction(net_required)
            row["pays_back_net_of_site"] = delivered >= net_required
        else:
            row["required_tokens_net_of_site"] = None
            row["pays_back_net_of_site"] = False
    return row


def calculate(fixed_cost: str = "20000000",
              saving_per_million_tokens: str = "0.50",
              machines: int = 100,
              tokens_per_second: int = 10000,
              utilisation: str = "0.5",
              economic_life_months: int = 12,
              delivery_weeks: int = 0,
              shortened_life_months: int = 6,
              delayed_delivery_weeks: int = 26,
              degraded_output_tokens_per_second: int = 6000,
              machine_power_kw: str = "10",
              cooling_overhead: str = "1.3",
              electricity_price_per_kwh: str = "0.08",
              network_cost_per_year: str = "250000",
              backup_cost_per_year: str = "150000",
              include_site: bool = True) -> dict:
    """Solve the payback, then move it with delivery, life and output-rate risk."""
    for name, value in (("machines", machines), ("tokens_per_second", tokens_per_second),
                        ("economic_life_months", economic_life_months),
                        ("shortened_life_months", shortened_life_months),
                        ("degraded_output_tokens_per_second", degraded_output_tokens_per_second)):
        positive_int(value, name)
    positive_int(delivery_weeks, "delivery_weeks", allow_zero=True)
    positive_int(delayed_delivery_weeks, "delayed_delivery_weeks", allow_zero=True)
    if shortened_life_months > economic_life_months:
        raise ValueError("The shortened life must not exceed the planned one")

    site = ({"machine_power_kw": machine_power_kw, "cooling_overhead": cooling_overhead,
             "electricity_price_per_kwh": electricity_price_per_kwh,
             "network_cost_per_year": network_cost_per_year,
             "backup_cost_per_year": backup_cost_per_year} if include_site else None)

    def life(months):
        return Fraction(SECONDS_PER_YEAR) * months / 12

    def delivery(weeks):
        return Fraction(SECONDS_PER_WEEK) * weeks

    cases = [
        ("planned", saving_per_million_tokens, machines, tokens_per_second,
         life(economic_life_months), delivery(delivery_weeks)),
        ("life_halves", saving_per_million_tokens, machines, tokens_per_second,
         life(shortened_life_months), delivery(delivery_weeks)),
        ("delivery_slips", saving_per_million_tokens, machines, tokens_per_second,
         life(economic_life_months), delivery(delayed_delivery_weeks)),
        ("output_rate_falls", saving_per_million_tokens, machines,
         degraded_output_tokens_per_second, life(economic_life_months), delivery(delivery_weeks)),
    ]
    rows = [scenario(name, fixed_cost, saving, count, rate, utilisation, span, wait, site)
            for name, saving, count, rate, span, wait in cases]

    planned = rows[0]
    baseline = payback_volume(fixed_cost, saving_per_million_tokens)
    return {
        "calculation": "specialisation-payback",
        "inputs": {"fixed_cost": fixed_cost,
                   "saving_per_million_tokens": saving_per_million_tokens,
                   "machines": machines, "tokens_per_second": tokens_per_second,
                   "utilisation": utilisation,
                   "economic_life_months": economic_life_months,
                   "delivery_weeks": delivery_weeks,
                   "shortened_life_months": shortened_life_months,
                   "delayed_delivery_weeks": delayed_delivery_weeks,
                   "degraded_output_tokens_per_second": degraded_output_tokens_per_second,
                   "machine_power_kw": machine_power_kw,
                   "cooling_overhead": cooling_overhead,
                   "electricity_price_per_kwh": electricity_price_per_kwh,
                   "network_cost_per_year": network_cost_per_year,
                   "backup_cost_per_year": backup_cost_per_year,
                   "include_site": include_site},
        "payback_volume_tokens": fraction(baseline),
        "scenarios": rows,
        "pays_back_anywhere": [row["scenario"] for row in rows if row["pays_back"]],
        "fails_everywhere": not any(row["pays_back"] for row in rows),
        "planned_case": planned["scenario"],
        "assumptions": [
            "Every amount is a declared teaching input, not a vendor price or a project estimate.",
            "The fixed cost is incremental, so the per-token saving must not already amortise it.",
            "Machine count is an output conversion; the demand to fill those machines is a separate condition.",
            "Delivery time is taken out of the economic life rather than added to it.",
            "The cooling overhead multiplies metered electricity only, not the network or backup lines.",
            "Site cost is charged against delivered tokens, so a saving quoted before it is not the saving that repays anything.",
            "Maintenance, spare capacity, downtime and model-quality change are outside this account.",
            "Changing the machine count may change unit price or utilisation, which would require repricing.",
        ],
    }


def markdown(result: dict) -> str:
    def money(entry, places=2):
        return "—" if entry is None else f"{float(Fraction(**entry)):,.{places}f}"

    def tokens(entry):
        return "—" if entry is None else f"{float(Fraction(**entry)):.4g}"

    lines = ["# 专用化的固定费用能否被节省付清", "",
             f"回本 token 数 = 固定费用 ÷ 每 token 节省 = {tokens(result['payback_volume_tokens'])} token。"
             "下列金额全部是教学假设，不是供应商价格或项目预测。", "",
             "## 四种情形", "",
             "| 情形 | 服务期 s | 机器 | 有效速率 tok/s | 需要 token | 交付 token | 覆盖率 | 回本 | 需要机器数 |",
             "|---|---:|---:|---:|---:|---:|---:|---|---:|"]
    for row in result["scenarios"]:
        if "required_tokens" not in row:
            lines.append(f"| {row['scenario']} | — | — | — | — | — | — | 否 | — |")
            continue
        lines.append("| " + " | ".join([
            row["scenario"], f"{float(Fraction(**row['serving_seconds'])):.0f}",
            str(row["machines"]), str(row["tokens_per_second"]),
            tokens(row["required_tokens"]), tokens(row["delivered_tokens"]),
            f"{float(Fraction(**row['coverage'])):.3f}",
            "是" if row["pays_back"] else "否", str(row["machines_required"])]) + " |")

    if any("site" in row for row in result["scenarios"]):
        lines += ["", "## 整站费用与净节省", "",
                  "电费按设施计量，散热系数只乘电费，不乘网络与备份。", "",
                  "| 情形 | 设施功率 kW | 电费 | 网络 | 备份 | 站点合计 | 站点每百万 token | 净节省每百万 token | 扣除后回本 |",
                  "|---|---:|---:|---:|---:|---:|---:|---:|---|"]
        for row in result["scenarios"]:
            if "site" not in row:
                continue
            site = row["site"]
            lines.append("| " + " | ".join([
                row["scenario"], f"{float(Fraction(**site['facility_power_kw'])):.1f}",
                money(site["electricity_cost"], 0), money(site["network_cost"], 0),
                money(site["backup_cost"], 0), money(site["total_site_cost"], 0),
                money(row["site_cost_per_million_tokens"], 4),
                money(row["net_saving_per_million_tokens"], 4),
                "是" if row["pays_back_net_of_site"] else "否"]) + " |")

    lines += ["", f"能够回本的情形：{'、'.join(result['pays_back_anywhere']) or '无'}。",
              "机器数只是产出折算，还需要真实需求把它消化掉。", "",
              "## 口径与限制", ""]
    lines += ["- " + item for item in result["assumptions"]]
    lines += ["", "## 完整输入与结果", "", "```json",
              json.dumps(result, ensure_ascii=False, indent=2), "```", ""]
    return "\n".join(lines)
