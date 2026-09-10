"""Independent checks for the F01 source-to-work-package map."""
import json
import re
import unittest
from pathlib import Path
import sys

for ancestor in Path(__file__).resolve().parents:
    if (ancestor / "src/infra_calc/sources.py").is_file():
        sys.path.insert(0, str(ancestor / "src"))
        break
from infra_calc import coverage


class ReferenceParsingTests(unittest.TestCase):
    def test_plain_and_listed_sections(self):
        self.assertEqual(coverage.parse_section_references("1.2、1.3"), ["1.2", "1.3"])
        self.assertEqual(coverage.parse_section_references("8.1.4、11.3.2；阅读配套"),
                         ["11.3.2", "8.1.4"])

    def test_ranges_expand_on_the_last_component(self):
        self.assertEqual(coverage.parse_section_references("2.4.1–2"), ["2.4.1", "2.4.2"])
        self.assertEqual(coverage.parse_section_references("2.6.3–5"),
                         ["2.6.3", "2.6.4", "2.6.5"])
        self.assertEqual(coverage.parse_section_references("4.5–6"), ["4.5", "4.6"])

    def test_chapter_numbers_and_experiment_labels_are_not_sections(self):
        # "复用第 4、7 章" and "实验 2-2" must not become sections.
        self.assertEqual(coverage.parse_section_references("1.3.3，复用第 4、7 章"), ["1.3.3"])
        self.assertEqual(coverage.parse_section_references("2.2，实验 2-2"), ["2.2"])
        self.assertEqual(coverage.parse_section_references("没有任何小节号"), [])

    def test_a_year_is_not_a_section(self):
        self.assertFalse(coverage.plausible_section("2024"))
        self.assertFalse(coverage.plausible_section("2025"))
        self.assertTrue(coverage.plausible_section("12"))
        self.assertTrue(coverage.plausible_section("10.4.3"))


class ClaimTests(unittest.TestCase):
    def setUp(self):
        self.entries = [{"work_package": "CA", "sections": ["2.4.1", "2.4.2"], "checked": False,
                         "headline": ""},
                        {"work_package": "CB", "sections": ["12.5"], "checked": False, "headline": ""}]

    def test_a_named_section_and_its_descendants_claim_directly(self):
        self.assertEqual(coverage.claims("12.5", self.entries)["direct"], ["CB"])
        self.assertEqual(coverage.claims("12.5.2", self.entries)["direct"], ["CB"])
        self.assertEqual(coverage.claims("2.4.1", self.entries)["direct"], ["CA"])

    def test_a_parent_section_is_reported_separately_not_merged(self):
        related = coverage.claims("2.4", self.entries)
        self.assertEqual(related["direct"], [])
        self.assertEqual(related["parent_of_named"], ["CA"])

    def test_an_unrelated_or_missing_section_claims_nothing(self):
        self.assertEqual(coverage.claims("7.1", self.entries),
                         {"direct": [], "parent_of_named": []})
        self.assertEqual(coverage.claims(None, self.entries),
                         {"direct": [], "parent_of_named": []})

    def test_1_2_does_not_claim_1_25(self):
        entries = [{"work_package": "CX", "sections": ["1.2"], "checked": False, "headline": ""}]
        self.assertEqual(coverage.claims("1.25", entries)["direct"], [])


class SignalTests(unittest.TestCase):
    def test_signals_are_named_when_they_fire(self):
        self.assertIn("magnitude", coverage.signals("读取 147,456 B"))
        self.assertIn("verb", coverage.signals("先算下界再比较"))
        self.assertIn("formula", coverage.signals("按 `a = b × c` 展开"))
        self.assertEqual(coverage.signals("这一段只讲动机，没有任何数字。"), [])

    def test_evidence_separates_present_from_missing(self):
        found = coverage.evidence("见[结果](../calculations/results/queqiao-records-conditions.md)")
        self.assertEqual(found["present"], ["queqiao-records-conditions"])
        self.assertEqual(found["missing"], [])
        absent = coverage.evidence("见[结果](../calculations/results/no-such-result.md)")
        self.assertEqual(absent["present"], [])
        self.assertEqual(absent["missing"], ["no-such-result"])


class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = coverage.build()

    def test_every_inventory_block_appears_exactly_once(self):
        inventory = json.loads((coverage.PROJECT / "inventory/sources.json").read_text())
        self.assertEqual(len(self.report["rows"]), len(inventory["items"]))
        identifiers = [row["id"] for row in self.report["rows"]]
        self.assertEqual(len(set(identifiers)), len(identifiers))

    def test_no_block_is_marked_reviewed_by_this_pass(self):
        self.assertEqual(self.report["summary"]["blocks_reviewed"], 0)
        for row in self.report["rows"]:
            self.assertEqual(row["review_status"], "pending")
            self.assertEqual(row["reviewed_work_packages"], [])

    def test_every_cited_result_resolves(self):
        self.assertEqual(self.report["summary"]["blocks_citing_a_missing_result"], 0)
        self.assertEqual(self.report["blocks_citing_a_missing_result"], [])
        for row in self.report["rows"]:
            for name in row["cited_results"]:
                self.assertTrue((coverage.PROJECT / "results" / (name + ".md")).exists(), name)

    def test_chapter_totals_add_up(self):
        self.assertEqual(sum(counts["blocks"] for counts in self.report["by_chapter"].values()),
                         self.report["blocks"])
        self.assertEqual(sum(counts["quantitative"] for counts in self.report["by_chapter"].values()),
                         self.report["summary"]["quantitative_candidates"])

    def test_packages_without_section_references_are_exactly_the_unmapped_ones(self):
        # Every package no block maps to is one that names no section at all.
        self.assertEqual(set(self.report["work_packages_no_block_maps_to"]),
                         set(self.report["work_packages_without_section_references"]))

    def test_the_only_sectioned_hole_left_is_the_orientation_section(self):
        gaps = {row["section"] for row in self.report["unmapped_quantitative_blocks"]
                if row["section"]}
        # Chapter 1's panorama is named by no work package. Everything else that
        # once looked like a hole was stale numbering in PLAN.md and is now fixed.
        self.assertTrue(gaps <= {"1.1", "1.1.1", "1.1.2"}, sorted(gaps))
        self.assertIn("1.1.1", gaps)

    def test_the_renumbered_sections_are_claimed_again(self):
        claimed = {name for row in self.report["rows"] for name in row["candidate_work_packages"]}
        by_section = {}
        for row in self.report["rows"]:
            if row["section"]:
                by_section.setdefault(row["section"], set()).update(row["candidate_work_packages"])
        # Chapter 3's rewrite moved these; PLAN.md now names where they went.
        for section, package in (("3.3.1", "C16"), ("3.3.3", "C17"), ("3.4.3", "C18"),
                                 ("3.6.1", "C19"), ("3.6.2", "C20"), ("10.4.3", "C56")):
            self.assertIn(package, by_section.get(section, set()), f"{section} -> {package}")
        self.assertIn("C56", claimed)

    def test_sibling_shorthand_and_chapter_words_are_told_apart(self):
        # "10.4.1、3" means two sections; "复用第 4、7 章" means none.
        self.assertEqual(coverage.parse_section_references("链路（10.4.1、3）"),
                         ["10.4.1", "10.4.3"])
        self.assertEqual(coverage.parse_section_references("（1.3.3，复用第 4、7 章）"), ["1.3.3"])

    def test_scope_states_that_this_is_not_a_review(self):
        joined = " ".join(self.report["scope"])
        self.assertIn("not a review", joined)
        self.assertIn("case-study", joined)

    def test_result_is_json_serialisable(self):
        text = json.dumps(self.report, ensure_ascii=False, allow_nan=False)
        self.assertIn("f01-source-coverage-map", text)

    def test_markdown_keeps_the_disclaimer_and_the_gap_table(self):
        text = coverage.markdown(self.report)
        self.assertIn("机械映射，不是审查", text)
        self.assertIn("有量化信号却没有候选工作包的块", text)


class WriteTests(unittest.TestCase):
    def test_writing_the_report_is_deterministic(self):
        first = coverage.write()
        second = coverage.write()
        self.assertEqual(first["sha256"], second["sha256"])
        self.assertEqual(first["file"], "inventory/f01-coverage.json")
        self.assertNotIn("rows", first)
        saved = json.loads((coverage.PROJECT / first["file"]).read_text())
        self.assertEqual(len(saved["rows"]), first["blocks"])


if __name__ == "__main__":
    unittest.main()
