#!/usr/bin/env python3
"""Translate the Chinese labels baked into the chapter figure scripts.

The rendered figures cannot be edited: matplotlib is configured with
svg.fonttype='path', so every label is a vector outline in the .svg and is
embedded in the .pdf. The only route is to translate the string literals in the
build scripts and re-render.

Rather than ask a model to rewrite plotting code -- which risks silently moving a
coordinate, a colour, or a number -- this walks the AST, translates ONLY string
constants, and splices them back at their exact source offsets. `check` then
re-parses both versions and proves that nothing but string constants changed.

    ./translate_figures.py extract            # -> figure-strings.json catalog
    ./translate_figures.py translate          # fill in the English column
    ./translate_figures.py apply              # write *.en.py next to each script
    ./translate_figures.py check              # AST-equality proof
    ./translate_figures.py render --chapter 1 # re-run the translated scripts
"""

from __future__ import annotations

import argparse
import ast
import asyncio
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SRC = Path("manuscripts")
CATALOG = Path("figure-strings.json")
GLOSSARY = Path("glossary.json")
CJK = re.compile(r"[一-鿿]")

MODELS = {"claude-sonnet-5": "anthropic.claude-sonnet-5",
          "claude-haiku-4-5": "anthropic.claude-haiku-4-5"}
BEDROCK_REGION = "us-east-1"


# verify.py / browser-check.py assert properties of the rendered output; several
# match on Chinese text, so translating them would break the checks, not the book.
# Scripts that parse the Chinese manuscripts or validate output rather than
# draw. book_assets.py matches captions with a regex containing 图; translating
# that literal makes it match nothing and the figure-index assertion fails.
CHECKERS = ("verify", "check", "browser", "book_assets", "math_style",
            "teaching_reading")


def scripts(only: str | None = None) -> list[Path]:
    # Figure code lives both in chapter directories and in shared helpers at the
    # top of manuscripts/ (teaching_figures.py, parallel_figures.py, ...). The
    # shared ones draw figures for several chapters, so missing them leaves
    # Chinese labels in chapters whose own scripts are fully translated.
    candidates = list(SRC.glob("ch[0-9][0-9]/*.py")) + list(SRC.glob("*.py"))
    return sorted(
        p for p in candidates
        if CJK.search(p.read_text(encoding="utf-8"))
        and not p.name.endswith(".en.py")
        and not any(x in p.name for x in CHECKERS)
        and (only is None or only in str(p.parent.name))
    )


FILE_EXT = (".md", ".json", ".py", ".pdf", ".png", ".svg", ".csv", ".txt",
            ".jsonl", ".yaml", ".yml", ".ttf", ".otf", ".npz", ".npy")


def _disk_names() -> set[str]:
    """Every filename under manuscripts/, for the path test below."""
    try:
        return {p.name for p in SRC.rglob("*") if p.is_file()}
    except OSError:
        return set()


_NAMES: set[str] | None = None


def looks_like_path(s: str) -> bool:
    """A CJK string can name a file rather than label a chart, and translating
    it breaks the code. Two cases, both real:
      * the whole literal is a filename ('12-端边云协同.md')
      * the literal is a *fragment* a path is built from -- the chapter title
        '端边云协同', which the script formats into '12-<title>.md'
    The second cannot be recognised from the string alone, so it is tested
    against the filenames actually present on disk.
    """
    global _NAMES
    t = s.strip()
    if t.endswith(FILE_EXT):
        return True
    if len(t) < 2:
        return False
    if _NAMES is None:
        _NAMES = _disk_names()
    # Match only the chapter-manuscript shape "<NN>-<title>.<ext>". A plain
    # substring test is far too broad: a common word like 模型 ("model") occurs
    # inside 02-模型架构.md and would then go untranslated across the whole book.
    stem = re.compile(r"^\d+[-_]" + re.escape(t) + r"\.[A-Za-z0-9]+$")
    return any(stem.match(name) for name in _NAMES)


def _path_context_nodes(tree: ast.AST) -> set:
    """Constants used to build a filename, identified by context rather than text.

    A bare chapter title such as 数据中心网络 is both a real figure label and the
    stem of 07-数据中心网络.md. Judging by the string alone excludes the label
    everywhere it is used. Judging by context keeps the filename intact while
    still translating the label: only a constant sitting in an f-string that also
    carries a file extension, or passed to a path/IO call, is treated as a path.
    """
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            literal = "".join(v.value for v in node.values
                              if isinstance(v, ast.Constant) and isinstance(v.value, str))
            if re.search(r"\.[A-Za-z0-9]{1,6}$", literal.strip()):
                for v in ast.walk(node):
                    if isinstance(v, ast.Constant):
                        out.add(id(v))
        if isinstance(node, ast.Call):
            name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
            if name in {"Path", "open", "glob", "rglob", "read_text", "read_bytes",
                        "write_text", "joinpath"}:
                for v in ast.walk(node):
                    if isinstance(v, ast.Constant):
                        out.add(id(v))
        # A string compared with ==/!= or used as a dict key is matched against
        # data loaded from disk, not drawn. ch09 asserts a stage name against a
        # JSON file whose value stays Chinese; translating the literal makes the
        # assertion unsatisfiable. Labels are passed to drawing calls, never
        # compared.
        if isinstance(node, ast.Compare):
            for v in ast.walk(node):
                if isinstance(v, ast.Constant):
                    out.add(id(v))
        # NOTE: subscript keys and dict-literal keys are deliberately NOT
        # excluded. A string can be both a displayed title and the key it is
        # filed under -- ch12 builds comp[title] from a label and reads it back
        # by the same literal. Translating both sides keeps them consistent;
        # protecting only one side breaks the lookup. Comparisons are different:
        # those match data loaded from disk, which stays Chinese.
    return out


def cjk_constants(tree: ast.AST) -> list[ast.Constant]:
    """Every string constant containing CJK, excluding docstrings and paths."""
    docstrings = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = getattr(node, "body", None)
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                    and isinstance(body[0].value.value, str):
                docstrings.add(id(body[0].value))
    paths = _path_context_nodes(tree)
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) \
                and CJK.search(node.value) and id(node) not in docstrings \
                and id(node) not in paths \
                and not node.value.strip().endswith(FILE_EXT):
            out.append(node)
    return out


def cmd_extract(args: argparse.Namespace) -> None:
    # carry over anything already translated so re-extracting is non-destructive
    prior = {}
    if CATALOG.exists():
        prior = {k: v.get("en", "") for k, v in
                 json.loads(CATALOG.read_text(encoding="utf-8")).items()}
    catalog: dict[str, dict] = {}
    per_file = []
    for path in scripts(args.only):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        consts = cjk_constants(tree)
        per_file.append((path, len(consts)))
        for node in consts:
            entry = catalog.setdefault(
                node.value,
                {"en": prior.get(node.value, ""), "seen": 0, "files": []},
            )
            entry["seen"] += 1
            rel = str(path.relative_to(SRC))
            if rel not in entry["files"]:
                entry["files"].append(rel)
    for path, n in per_file:
        print(f"{str(path.relative_to(SRC)):34s} {n:4d} strings")
    total = sum(n for _, n in per_file)
    print(f"\n{len(per_file)} scripts, {total} CJK string literals, "
          f"{len(catalog)} unique ({total - len(catalog)} duplicates collapsed)")
    longest = max(catalog, key=len)
    print(f"longest label: {len(longest)} chars")
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {CATALOG}")


def cmd_translate(args: argparse.Namespace) -> None:
    from anthropic import AnthropicBedrockMantle

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    todo = [k for k, v in catalog.items() if not v["en"]
            and (not args.only or any(args.only in f for f in v["files"]))]
    if not todo:
        print("nothing untranslated")
        return
    glossary = json.loads(GLOSSARY.read_text(encoding="utf-8")) if GLOSSARY.exists() else {}
    terms = "\n".join(f"  {zh} -> {en}" for zh, en in sorted(glossary.items())[:400])
    system = (
        "You translate labels for technical diagrams in a book on AI "
        "infrastructure, from Chinese to English.\n\n"
        "These strings are drawn inside fixed-size boxes, axes, and legends, so "
        "LENGTH IS THE BINDING CONSTRAINT. Use the shortest accurate English "
        "term. Prefer a noun phrase over a sentence, drop articles, and use the "
        "standard abbreviation an English systems diagram would use (KV cache, "
        "GPU, TP/PP, QPS). Never pad. If the Chinese is two words, the English "
        "should usually be two words.\n\n"
        "Some strings carry printf/format placeholders ({}, %s, {x:.1f}) or "
        "trailing units. Preserve every placeholder and unit exactly.\n\n"
        "Return ONLY a JSON object mapping each input string to its English "
        "rendering. No commentary.\n\n"
        f"Glossary for consistency with the translated prose:\n{terms}\n"
    )

    # Batch by character budget, not by count: a handful of long strings (HTML
    # fragments, multi-line prose) would otherwise overflow max_tokens and come
    # back as truncated, unparseable JSON.
    BUDGET, MAX_ITEMS = 2500, 60
    batches, cur, size = [], [], 0
    for s in todo:
        if cur and (size + len(s) > BUDGET or len(cur) >= MAX_ITEMS):
            batches.append(cur)
            cur, size = [], 0
        cur.append(s)
        size += len(s)
    if cur:
        batches.append(cur)
    print(f"{len(todo)} labels to translate in {len(batches)} batches, "
          f"{args.concurrency} concurrent")

    async def run() -> None:
        from anthropic import AsyncAnthropicBedrockMantle

        client = AsyncAnthropicBedrockMantle(aws_region=BEDROCK_REGION)
        sem = asyncio.Semaphore(args.concurrency)
        done = 0

        async def one(n: int, part: list[str]) -> None:
            nonlocal done
            try:
                async with sem:
                    resp = await client.messages.create(
                        model=MODELS[args.model], max_tokens=16000, system=system,
                        messages=[{"role": "user",
                                   "content": json.dumps(part, ensure_ascii=False, indent=1)}],
                    )
                text = "".join(b.text for b in resp.content if b.type == "text").strip()
                text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.M).strip()
                got = json.loads(text)
            except Exception as exc:
                print(f"  batch {n}: {type(exc).__name__}: {str(exc)[:90]}")
                return
            hit = 0
            for zh, en in got.items():
                if zh in catalog and isinstance(en, str) and en.strip():
                    catalog[zh]["en"] = en
                    hit += 1
            done += hit
            missed = len(part) - hit
            print(f"  batch {n:2d}: {hit}/{len(part)}"
                  f"{f' ({missed} unreturned)' if missed else ''}"
                  f"  [{done}/{len(todo)}]", flush=True)

        await asyncio.gather(*(one(n, p) for n, p in enumerate(batches)))

    asyncio.run(run())
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    still = sum(1 for v in catalog.values() if not v["en"])
    if still:
        print(f"\n{still} label(s) still untranslated — re-run to retry just those")

    # length report: the main failure mode is English overflowing a fixed box
    ratios = [(len(v["en"]) / max(1, len(k)), k, v["en"])
              for k, v in catalog.items() if v["en"]]
    ratios.sort(reverse=True)
    print(f"\nwidest expansions (English chars per Chinese char):")
    for r, zh, en in ratios[:8]:
        print(f"  {r:4.1f}x  {len(zh):2d}->{len(en):3d}  {en[:52]}")


def apply_to(path: Path) -> tuple[str, int]:
    """Splice translated literals in at their exact source offsets."""
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    raw = path.read_bytes()
    source = raw.decode("utf-8")
    # ast reports col_offset as a UTF-8 BYTE offset, not a character index. With
    # 3-byte CJK on the line those differ, so all splicing happens in bytes.
    offsets = [0]
    for line in source.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line.encode("utf-8")))

    tree = ast.parse(source)
    # A literal segment of an f-string is its own Constant node, but it is NOT a
    # standalone expression: wrapping it in quotes terminates the f-string early
    # and corrupts the line. Those get spliced as raw text instead.
    in_fstring = {id(c) for n in ast.walk(tree) if isinstance(n, ast.JoinedStr)
                  for c in ast.walk(n) if isinstance(c, ast.Constant)}

    edits, skipped = [], []
    for node in cjk_constants(tree):
        en = catalog.get(node.value, {}).get("en")
        if not en:
            continue
        start = offsets[node.lineno - 1] + node.col_offset
        end = offsets[node.end_lineno - 1] + node.end_col_offset
        if id(node) in in_fstring:
            # raw text: double the braces so they stay literal, and refuse any
            # character that could close the f-string or start an escape
            if any(ch in en for ch in ('"', "'", "\\")):
                skipped.append(en)
                continue
            # braces stay literal; control characters become escape sequences,
            # which the literal portion of an f-string accepts. A real newline
            # spliced in would leave the string unterminated.
            rep = (en.replace("{", "{{").replace("}", "}}")
                     .replace("\n", "\\n").replace("\r", "\\r")
                     .replace("\t", "\\t")).encode("utf-8")
        else:
            rep = json.dumps(en, ensure_ascii=False).encode("utf-8")
        edits.append((start, end, rep))
    if skipped:
        print(f"    note: {len(skipped)} f-string label(s) left in Chinese "
              f"(contain a quote or backslash): {skipped[:2]}")

    out = raw
    for start, end, rep in sorted(edits, reverse=True):
        out = out[:start] + rep + out[end:]
    return out.decode("utf-8"), len(edits)


def normalised(tree: ast.AST) -> str:
    """AST dump with every string constant blanked, for structural comparison."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            node.value = "<STR>"
    return ast.dump(tree)


def cmd_apply(args: argparse.Namespace) -> None:
    total = 0
    for path in scripts(args.only):
        translated, n = apply_to(path)
        out = path.with_suffix(".en.py")
        out.write_text(translated, encoding="utf-8")
        total += n
        print(f"{str(path.relative_to(SRC)):34s} {n:4d} literals -> {out.name}")
    print(f"\n{total} literals replaced")


def cmd_check(args: argparse.Namespace) -> None:
    bad = 0
    for path in scripts(args.only):
        en_path = path.with_suffix(".en.py")
        if not en_path.exists():
            continue
        a = normalised(ast.parse(path.read_text(encoding="utf-8")))
        b = normalised(ast.parse(en_path.read_text(encoding="utf-8")))
        ok = a == b
        leftover = len(cjk_constants(ast.parse(en_path.read_text(encoding="utf-8"))))
        bad += not ok
        print(f"{'OK   ' if ok else 'DIFF '} {str(path.relative_to(SRC)):34s} "
              f"{'structure identical' if ok else 'STRUCTURE CHANGED'}"
              f"{f', {leftover} CJK strings remain' if leftover else ''}")
    print("\nall scripts structurally identical to their originals"
          if not bad else f"\n{bad} script(s) changed structure — do not render these")


def cmd_render(args: argparse.Namespace) -> None:
    pat = f"ch{args.chapter:02d}/*.en.py"
    for path in sorted(SRC.glob(pat)):
        print(f"rendering {path.relative_to(SRC)} ...", flush=True)
        # the scripts do `from figure_style import ...`, which lives one level
        # up in manuscripts/, so that directory has to be importable
        env = {**os.environ, "PYTHONPATH": str(SRC.resolve())}
        r = subprocess.run([sys.executable, path.name], cwd=path.parent,
                           capture_output=True, text=True, env=env)
        if r.returncode:
            print(f"  FAILED: {(r.stderr or r.stdout)[-600:]}")
        else:
            print(f"  ok")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", default="claude-sonnet-5", choices=sorted(MODELS))
    sub = p.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract"); e.add_argument("--only"); e.set_defaults(fn=cmd_extract)
    t = sub.add_parser("translate"); t.add_argument("--only")
    t.add_argument("--concurrency", type=int, default=6); t.set_defaults(fn=cmd_translate)
    a = sub.add_parser("apply"); a.add_argument("--only"); a.set_defaults(fn=cmd_apply)
    c = sub.add_parser("check"); c.add_argument("--only"); c.set_defaults(fn=cmd_check)
    r = sub.add_parser("render")
    r.add_argument("--chapter", type=int, default=1)
    r.set_defaults(fn=cmd_render)
    args = p.parse_args()
    args.fn(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
