"""Dry-run evidence synchronization on a copy of the author's twelve chapters.

This checks editorial ownership, not numerical artifact validity: that separate
preflight is bypassed only inside the temporary-copy run below.
"""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "calculations/src"))
from infra_calc import outline


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


catalog = json.loads((ROOT / "outlines/chapters.json").read_text())
assert [row["number"] for row in catalog] == list(range(1, 13))
paths = list((ROOT / "outlines").rglob("*.md")) + [ROOT / "outlines/chapters.json"]
original_hashes = {str(p.relative_to(ROOT)): digest(p) for p in paths}
with tempfile.TemporaryDirectory() as directory:
    book = Path(directory)
    shutil.copytree(ROOT / "outlines", book / "outlines")
    main_before = {row["file"]: (book / "outlines" / row["file"]).read_bytes() for row in catalog}
    owners_before = {}
    for path in (book / "outlines/extensions").glob("*.md"):
        for line in path.read_text().splitlines():
            if line.startswith("**已复算（"):
                key = line.split("）：**", 1)[0]
                owners_before.setdefault(key, []).append(path.name)
    with patch.object(outline, "BOOK", book), patch("infra_calc.reproduce.verify_results", return_value=None):
        result = outline.sync()
    assert not list((book / "outlines").glob("13-*.md"))
    assert not list((book / "outlines/extensions").glob("13-*.md"))
    changed_main = [name for name, data in main_before.items() if (book / "outlines" / name).read_bytes() != data]
    assert not changed_main, changed_main
    owners_after = {}
    for path in (book / "outlines/extensions").glob("*.md"):
        for line in path.read_text().splitlines():
            if line.startswith("**已复算（"):
                key = line.split("）：**", 1)[0]
                owners_after.setdefault(key, []).append(path.name)
    moved = {key: dict(before=value, after=owners_after.get(key)) for key, value in owners_before.items()
             if owners_after.get(key) != value}
    assert not moved, moved
assert original_hashes == {str(p.relative_to(ROOT)): digest(p) for p in paths}
report = dict(status="passed", chapters=12, main_chapters_preserved=12,
              existing_evidence_owners_preserved=len(owners_before), chapter_13_recreated=False,
              actual_outline_files_unchanged=True,
              limitation="Temporary-copy editorial synchronization only; numerical verify_results preflight bypassed, no full calculation revalidation claimed.",
              inputs=original_hashes, sync_result=result)
(Path(__file__).parent / "result.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: v for k, v in report.items() if k not in ("inputs", "sync_result")}, ensure_ascii=False, indent=2))
