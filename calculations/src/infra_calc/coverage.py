"""F01: map every captured text block to the work packages that claim it.

The inventory already captures each writing surface. What it has never had is a
link from a block back to the work package responsible for it, so nobody could
say which parts of the book still have no calculation behind them.

This builds that link mechanically from two things already written down: the
section references each work package carries in `PLAN.md`, and the section each
block sits under. It also records, per block, whether the text shows any sign of
a quantitative requirement and whether it already cites a generated result.

A mechanical map is not a review. Nothing here sets a block's `review_status`,
nothing here fills the reviewed `work_packages` field, and a block with a
candidate package is not thereby covered. The report exists so that the review
has a worklist and so that "unmapped" stops being invisible.
"""
from collections import Counter
import hashlib
import json
import re

from .paths import PROJECT

# A section reference must carry a dot, which is what separates "1.3.3" from the
# chapter numbers in phrases like "复用第 4、7 章" and the "2-2" in "实验 2-2".
SECTION = re.compile(r"(\d+(?:\.\d+)+)(?:[–—-](\d+))?")
HEADING = re.compile(r"^#{2,4}\s+(\d+(?:\.\d+)*)")
DETAIL_ANCHOR = re.compile(r'id="detail-(\d+(?:\.\d+)*)"')
RESULT_LINK = re.compile(r"calculations/results/([A-Za-z0-9._-]+)\.(?:md|json)")

# Signals that a block states a quantitative requirement. Each is recorded by
# name when it fires, so a reader can see why a block was flagged.
SIGNALS = {
    "magnitude": re.compile(r"\d[\d,]*(?:\.\d+)?\s*(?:B|KB|MB|GB|TB|KiB|MiB|GiB|"
                            r"ms|µs|us|ns|s\b|W\b|kW|kWh|mm²|mm2|"
                            r"[MGT]bit/s|[MGT]B/s|tok/s|token|FLOPs|TFLOPs|%)"),
    "formula": re.compile(r"`[^`\n]*[=×÷/+*][^`\n]*`"),
    "code_block": re.compile(r"```text\n[^`]*="),
    "verb": re.compile(r"计算|推算|估算|复算|求出|下界|上界|预算|交叉点|盈亏平衡|分位数|敏感性"),
    "table": re.compile(r"^\|[^\n]*\|\s*$", re.M),
}


# A bare number listed after a dotted reference is a sibling at the same depth,
# as in "10.4.1、3". A number carrying one of these markers is a chapter, an
# experiment or a figure instead, as in "复用第 4、7 章" and "实验 2-2".
NOT_A_SECTION = ("第", "章", "实验", "图", "节", "-", "—", "–")


def parse_section_references(text: str) -> list:
    """Sections a work-package line claims, expanding ranges and sibling shorthand."""
    found, last = [], None
    for token in re.split(r"[、，,；;]", text):
        token = token.strip().strip("（）()［］[]【】 ")
        if not token:
            continue
        match = SECTION.search(token)
        if match:
            base, end = match.group(1), match.group(2)
            found.append(base)
            last = base
            if end:
                parts = base.split(".")
                start, stop = int(parts[-1]), int(end)
                for value in range(start + 1, stop + 1):
                    found.append(".".join(parts[:-1] + [str(value)]))
                last = ".".join(parts[:-1] + [str(stop)])
            continue
        if last and token.isdigit() and not any(mark in token for mark in NOT_A_SECTION):
            parts = last.split(".")
            if len(parts) > 1:
                found.append(".".join(parts[:-1] + [token]))
    return sorted(dict.fromkeys(found))


def plan_entries() -> list:
    """Work packages, with the sections each one names."""
    lines = (PROJECT / "PLAN.md").read_text().splitlines()
    entries = []
    for line in lines:
        match = re.match(r"^- \[([ x])\] ([A-Z]\d+)\s+(.*)$", line)
        if not match:
            continue
        checked, identifier, body = match.groups()
        head = body.split("。")[0]
        entries.append({"work_package": identifier, "checked": checked == "x",
                        "sections": parse_section_references(head),
                        "headline": head[:160]})
    return entries


def plausible_section(value: str) -> bool:
    """Reject headings that merely start with a number, such as a year."""
    head = value.split(".")[0]
    return "." in value and head.isdigit() and 1 <= int(head) <= 99 or (
        "." not in value and value.isdigit() and 1 <= int(value) <= 12)


def resolve_sections(items: list) -> dict:
    """Section each block sits under, carried forward in file order."""
    resolved, current, previous_file = {}, None, None
    for item in items:
        if item["file"] != previous_file:
            current, previous_file = None, item["file"]
        heading = HEADING.match(item["title"])
        if heading and plausible_section(heading[1]):
            current = heading[1]
        elif item["section"]:
            current = item["section"]
        else:
            anchor = DETAIL_ANCHOR.search(item["text"])
            if anchor:
                current = anchor[1]
        resolved[item["id"]] = current
    return resolved


def claims(section: str | None, entries: list) -> dict:
    """Work packages related to this section, kept apart by how they relate.

    A package that names 2.4.1 does not name 2.4, but a section's own
    introduction belongs to the same subject as its subsections. Both relations
    are reported, never merged, so a reader can tell a direct claim from an
    inferred one.
    """
    if section is None:
        return {"direct": [], "parent_of_named": []}
    direct, parent = [], []
    for entry in entries:
        for named in entry["sections"]:
            if section == named or section.startswith(named + "."):
                direct.append(entry["work_package"])
                break
            if named.startswith(section + "."):
                parent.append(entry["work_package"])
                break
    return {"direct": sorted(dict.fromkeys(direct)),
            "parent_of_named": sorted(dict.fromkeys(parent))}


def signals(text: str) -> list:
    return sorted(name for name, pattern in SIGNALS.items() if pattern.search(text))


def evidence(text: str) -> dict:
    """Generated results this block already cites, and whether they exist."""
    present, missing = [], []
    for name in sorted(dict.fromkeys(RESULT_LINK.findall(text))):
        (present if (PROJECT / "results" / (name + ".md")).exists() else missing).append(name)
    return {"present": present, "missing": missing}


def build() -> dict:
    """One pass over the inventory, producing the F01 worklist."""
    inventory = json.loads((PROJECT / "inventory/sources.json").read_text())
    items = inventory["items"]
    entries = plan_entries()
    sections = resolve_sections(items)

    rows, chapters = [], {}
    for item in items:
        section = sections[item["id"]]
        found = signals(item["text"])
        cited = evidence(item["text"])
        related = claims(section, entries)
        candidates = related["direct"]
        chapter = section.split(".")[0] if section else None
        row = {"id": item["id"], "surface": item["surface"], "file": item["file"],
               "title": item["title"][:120], "section": section, "chapter": chapter,
               "exercise": item["exercise"], "sha256": item["sha256"],
               "candidate_work_packages": candidates,
               "packages_naming_a_subsection": related["parent_of_named"],
               "quantitative_signals": found,
               "quantitative_candidate": bool(found),
               "cited_results": cited["present"],
               "cited_results_missing": cited["missing"],
               "review_status": item["review_status"],
               "reviewed_work_packages": item["work_packages"]}
        rows.append(row)
        key = chapter or "unsectioned"
        bucket = chapters.setdefault(key, Counter())
        bucket["blocks"] += 1
        bucket["quantitative"] += bool(found)
        bucket["with_cited_results"] += bool(cited["present"])
        bucket["mapped"] += bool(candidates)
        bucket["unmapped_quantitative"] += bool(found) and not candidates and not related["parent_of_named"]

    unmapped = [row for row in rows if row["quantitative_candidate"]
                and not row["candidate_work_packages"]
                and not row["packages_naming_a_subsection"]]
    broken = [row for row in rows if row["cited_results_missing"]]
    uncovered_packages = sorted({entry["work_package"] for entry in entries}
                                - {name for row in rows for name in row["candidate_work_packages"]})
    without_sections = sorted(entry["work_package"] for entry in entries if not entry["sections"])

    return {
        "calculation": "f01-source-coverage-map",
        "inventory_files": len(inventory["files"]),
        "blocks": len(rows),
        "work_packages": len(entries),
        "work_packages_with_section_references": len(entries) - len(without_sections),
        "work_packages_without_section_references": without_sections,
        "work_packages_no_block_maps_to": uncovered_packages,
        "summary": {"quantitative_candidates": sum(row["quantitative_candidate"] for row in rows),
                    "blocks_citing_a_generated_result": sum(bool(row["cited_results"]) for row in rows),
                    "blocks_with_a_candidate_package": sum(bool(row["candidate_work_packages"]) for row in rows),
                    "blocks_related_only_through_a_subsection": sum(
                        bool(row["packages_naming_a_subsection"]) and not row["candidate_work_packages"]
                        for row in rows),
                    "quantitative_blocks_with_no_candidate_package": len(unmapped),
                    "blocks_citing_a_missing_result": len(broken),
                    "blocks_reviewed": sum(row["review_status"] != "pending" for row in rows)},
        "by_chapter": {key: dict(value) for key, value in sorted(
            chapters.items(), key=lambda pair: (pair[0] == "unsectioned", pair[0]))},
        "unmapped_quantitative_blocks": [
            {key: row[key] for key in ("id", "section", "title", "quantitative_signals", "surface")}
            for row in unmapped],
        "blocks_citing_a_missing_result": [
            {key: row[key] for key in ("id", "section", "cited_results_missing")} for row in broken],
        "rows": rows,
        "scope": [
            "A mechanical map, not a review: no block's review_status is set here and no reviewed assignment is written.",
            "A candidate package means a work package names that section, not that the block's requirement is implemented.",
            "Quantitative signals are heuristics; each firing signal is recorded so a reviewer can disagree with it.",
            "A cited result proves a link resolves, not that the citation answers what the block asks for.",
            "Blocks with no section (chapter leads, writing-material lists, case-study prose) map to nothing by construction and still need review.",
            "No work-package line names a case-study file, so every case-study block is unmapped here; that is a finding about how the packages are written, not a claim that the cases are uncalculated.",
        ],
    }


def write() -> dict:
    """Save the worklist beside the inventory it audits."""
    report = build()
    path = PROJECT / "inventory/f01-coverage.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {**{key: value for key, value in report.items() if key not in ("rows",)},
            "file": str(path.relative_to(PROJECT)), "sha256": digest}


def markdown(report: dict) -> str:
    lines = ["# F01：原文到工作包的覆盖清单", "",
             f"{report['inventory_files']} 份写作原件、{report['blocks']} 个文本块，"
             f"对照 {report['work_packages']} 个工作包（其中 "
             f"{report['work_packages_with_section_references']} 个带明确小节引用）。", "",
             "这是机械映射，不是审查：本表不设置任何块的 review_status，也不写入已审查的工作包归属。"
             "候选工作包只表示某个工作包声称了这个小节，不表示该块的要求已经实现。", "",
             "## 总计", ""]
    for key, value in report["summary"].items():
        lines.append(f"- {key}：{value}")
    lines += ["", "## 逐章", "",
              "| 章 | 文本块 | 有量化信号 | 已引用结果 | 有候选工作包 | 有量化但无候选 |",
              "|---|---:|---:|---:|---:|---:|"]
    for chapter, counts in report["by_chapter"].items():
        lines.append("| " + " | ".join([
            chapter, str(counts.get("blocks", 0)), str(counts.get("quantitative", 0)),
            str(counts.get("with_cited_results", 0)), str(counts.get("mapped", 0)),
            str(counts.get("unmapped_quantitative", 0))]) + " |")

    if report["work_packages_no_block_maps_to"]:
        lines += ["", "## 没有任何文本块映射到的工作包", "",
                  "、".join(report["work_packages_no_block_maps_to"]),
                  "", "它们要么引用的小节号已随改写变动，要么本就不按小节划分；两种情况都需要人工确认。"]
    if report["work_packages_without_section_references"]:
        lines += ["", "## 没有写出小节引用的工作包", "",
                  "、".join(report["work_packages_without_section_references"])]

    lines += ["", "## 有量化信号却没有候选工作包的块（前 40 条）", "",
              "| 块 | 小节 | 信号 | 标题 |", "|---|---|---|---|"]
    for row in report["unmapped_quantitative_blocks"][:40]:
        lines.append("| " + " | ".join([
            row["id"], row["section"] or "—", "、".join(row["quantitative_signals"]),
            row["title"].replace("|", "\\|")]) + " |")

    lines += ["", "## 口径与限制", ""]
    lines += ["- " + item for item in report["scope"]]
    return "\n".join(lines)
