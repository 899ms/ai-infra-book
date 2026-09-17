#!/usr/bin/env python3
"""Translate the ai-infra-book manuscripts (Chinese -> English) via the Batch API.

    ./translate_book.py estimate                    # cost, no API calls
    ./translate_book.py glossary                    # bilingual term list (1 call)
    ./translate_book.py translate --only 00         # try one chapter first
    ./translate_book.py translate                   # whole book
    ./translate_book.py verify                      # structural diff vs source

`translate` submits one batch and polls. It is resumable: re-running picks up an
in-flight batch from .batch_state.json instead of resubmitting, and chunks
already written to .tcache/ are never re-requested.

The book is Apache-2.0, so the translation may be redistributed with attribution
and a note stating that the files were changed.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
import sys
import time
from pathlib import Path

import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

SRC = Path("manuscripts")
OUT = Path("manuscripts-en")
CACHE = Path(".tcache")
GLOSSARY = Path("glossary.json")
STATE = Path(".batch_state.json")

# Thinking is off: translation is mechanical, and reasoning tokens are billed as
# output. Haiku 4.5 has no thinking by default, so it is simply omitted there.
MODELS = {
    "claude-sonnet-5": {"in": 3.00, "out": 15.00, "thinking": {"type": "disabled"}},
    "claude-haiku-4-5": {"in": 1.00, "out": 5.00, "thinking": None},
}
DEFAULT_MODEL = "claude-sonnet-5"
BATCH_DISCOUNT = 0.5
MAX_TOKENS = 16000

# Bedrock is partner-operated: its model ids differ and the Message Batches API
# is not available there, so --provider bedrock runs concurrent requests instead.
# Bedrock token pricing is AWS's, not the first-party rates in MODELS above.
# The Mantle endpoint takes bare ids; the dated "...-20251001-v1:0" snapshot
# names from `aws bedrock list-foundation-models` are the legacy InvokeModel
# form and 404 here.
BEDROCK_IDS = {
    "claude-sonnet-5": "anthropic.claude-sonnet-5",
    "claude-haiku-4-5": "anthropic.claude-haiku-4-5",
}
BEDROCK_REGION = "us-east-1"

TOK_PER_CJK = 1.0
CHARS_PER_TOK_OTHER = 3.0
TARGET_CHUNK = 9000  # source characters per request

RULES = """\
You translate technical books from Chinese to English. This is a book on AI
infrastructure: quantitative analysis and system design for LLM inference and
training. The audience is practising systems engineers.

Translate the Markdown passage you are given into English. Return ONLY the
translated Markdown — no preamble, no surrounding code fence, no commentary.

Absolute requirements:

1. Preserve every piece of non-prose syntax exactly as written:
   - LaTeX, both inline `$...$` and display `$$...$$`. Never translate, reorder,
     or reformat anything between math delimiters. Variable names, subscripts,
     and operators are copied character for character.
   - Fenced code blocks. Translate a Chinese prose comment inside one; leave all
     code, identifiers, and string literals untouched.
   - Image and link targets: in `![alt](path)` translate `alt`, never `path`.
   - Footnote markers, anchors, and raw HTML.
1b. Markdown links are load-bearing and must survive. Every `[text](target)` in
   the source appears in your output as a `[text](target)` link: translate the
   bracketed text, copy the parenthesised target character for character, and
   keep the link where it sits in the sentence. NEVER flatten a link into plain
   text, never drop it, never move it to a footnote or a list at the end, and
   never invent one. The passage you return must contain exactly as many `](`
   link openings as the passage you were given.
2. Preserve structure exactly: the same heading levels in the same order, the
   same number of table rows and columns, the same list nesting. Table cells
   holding only numbers, units, or identifiers are copied unchanged.
2a. Never ADD markup that the source does not have. This is a translation, not
   an edit: do not promote a bold lead-in or a run-in phrase into a heading, do
   not introduce a new section, do not wrap a variable, unit, or number in
   `$...$` unless it was already inside math delimiters, and do not convert a
   paragraph into a list or a table. Your output must contain exactly the same
   number of headings, display-math blocks, inline-math spans, table rows, and
   code fences as the source passage — no more and no fewer. Improving the
   formatting is a defect here, not a contribution.
2b. Two conventions the PDF build depends on, so keep them exactly:
   - A chapter heading of the form `# 第 N 章 Title` becomes `# Chapter N Title`
     — keep the number and that exact word order, on one line.
   - Where an image is immediately followed by a line holding only italic text,
     that is the figure caption. Keep it on its own line, still italic, still
     directly after the image, with no blank line inserted between them.
3. Every number, unit, and quantitative claim carries over exactly. This book is
   built on calculations; a changed digit is a serious error.
4. Keep established English technical terms in English rather than
   back-translating them literally. Follow the glossary for consistency.
5. Register: clear technical prose, active voice, the way a well-edited English
   systems book reads. Do not pad, summarise, or add translator's notes.
   Translate every sentence of the passage.
"""


def system_prompt(glossary: dict[str, str]) -> str:
    if not glossary:
        return RULES
    terms = "\n".join(f"  {zh} -> {en}" for zh, en in sorted(glossary.items()))
    return f"{RULES}\nGlossary (use these renderings consistently):\n{terms}\n"


# --------------------------------------------------------------------------
# chunking — never split inside a fence, a display-math block, or a table
# --------------------------------------------------------------------------

def atomic_blocks(text: str) -> list[str]:
    lines = text.split("\n")
    blocks: list[list[str]] = []
    cur: list[str] = []
    in_fence = in_math = False

    def flush() -> None:
        nonlocal cur
        if cur:
            blocks.append(cur)
            cur = []

    for line in lines:
        s = line.strip()
        if in_fence:
            cur.append(line)
            if s.startswith("```"):
                in_fence = False
                flush()
            continue
        if in_math:
            cur.append(line)
            if s.endswith("$$"):
                in_math = False
                flush()
            continue
        if s.startswith("```"):
            flush()
            cur.append(line)
            in_fence = True
            continue
        if s == "$$" or (s.startswith("$$") and not s.endswith("$$")):
            flush()
            cur.append(line)
            in_math = True
            continue
        if not s:
            cur.append(line)
            flush()
            continue
        if s.startswith("#"):
            flush()
            cur.append(line)
            flush()
            continue
        cur.append(line)
    flush()
    return ["\n".join(b) for b in blocks]


def chunk(text: str, target: int = TARGET_CHUNK) -> list[str]:
    out: list[str] = []
    cur: list[str] = []
    size = 0
    for block in atomic_blocks(text):
        is_heading = block.lstrip().startswith("#")
        if cur and size + len(block) > target and (is_heading or size > target * 1.4):
            out.append("\n".join(cur))
            cur, size = [], 0
        cur.append(block)
        size += len(block) + 1
    if cur:
        out.append("\n".join(cur))
    return out


def chapters() -> list[Path]:
    return sorted(SRC.glob("*.md"))


def build_prompt(chunks: list[str], i: int) -> str:
    parts = []
    if i > 0:
        parts.append(
            "The Chinese passage immediately BEFORE this one, for context only. "
            f"Do not translate it:\n\n{chunks[i-1][-800:]}\n"
        )
    if i + 1 < len(chunks):
        parts.append(
            "The Chinese passage immediately AFTER this one, for context only. "
            f"Do not translate it:\n\n{chunks[i+1][:500]}\n"
        )
    parts.append(f"Translate this passage:\n\n{chunks[i]}")
    return "\n\n".join(parts)


def cache_path(model: str, sys_prompt: str, prompt: str) -> Path:
    key = hashlib.sha256((model + sys_prompt + prompt).encode()).hexdigest()[:16]
    return CACHE / f"{key}.md"


# --------------------------------------------------------------------------
# structural fingerprint, used by verify
# --------------------------------------------------------------------------

INLINE_MATH = re.compile(r"(?<!\$)\$[^$\n]+\$(?!\$)")
IMG = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def fingerprint(text: str) -> dict:
    return {
        "display_math": text.count("$$") // 2,
        "inline_math": len(INLINE_MATH.findall(text)),
        "fences": text.count("```") // 2,
        "table_rows": sum(1 for l in text.split("\n") if l.strip().startswith("|")),
        "headings": re.findall(r"^(#+)\s", text, re.M),
        "image_targets": IMG.findall(text),
        "link_targets": LINK.findall(text),
    }


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def cmd_estimate(args: argparse.Namespace) -> None:
    tot_in = tot_chunks = 0
    for f in chapters():
        t = f.read_text(encoding="utf-8")
        cjk = sum(1 for c in t if "一" <= c <= "鿿")
        toks = cjk * TOK_PER_CJK + (len(t) - cjk) / CHARS_PER_TOK_OTHER
        n = len(chunk(t))
        tot_in += toks
        tot_chunks += n
        print(f"{f.name:34s} {len(t):7d} chars  ~{int(toks):6d} tok  {n:3d} chunks")

    # Each request also carries the cached system prompt and ~1.3k chars of
    # neighbouring context; English output of Chinese technical prose runs longer.
    tot_in *= 1.25
    tot_out = tot_in * 1.15
    print(f"\n  {tot_chunks} chunks   ~{int(tot_in):,} in / ~{int(tot_out):,} out tokens\n")
    print(f"  {'model':20s} {'standard':>10s} {'batch (-50%)':>14s}")
    for name, p in MODELS.items():
        full = tot_in / 1e6 * p["in"] + tot_out / 1e6 * p["out"]
        print(f"  {name:20s} {'$%.2f' % full:>10s} {'$%.2f' % (full * BATCH_DISCOUNT):>14s}")
    print("\n  Estimates only — no tokenizer call. Prompt caching on the system")
    print("  prompt reduces the input side further.")


def cmd_glossary(args: argparse.Namespace) -> None:
    """One call over every heading in the book -> a stable bilingual term list."""
    heads: list[str] = []
    for f in chapters():
        heads += re.findall(r"^#+\s+(.*)$", f.read_text(encoding="utf-8"), re.M)
    if getattr(args, "provider", "bedrock") == "bedrock":
        from anthropic import AnthropicBedrockMantle

        client = AnthropicBedrockMantle(aws_region=BEDROCK_REGION)
        model_id = BEDROCK_IDS[args.model]
    else:
        client = anthropic.Anthropic()
        model_id = args.model
    resp = client.messages.create(
        model=model_id,
        max_tokens=MAX_TOKENS,
        system="You build bilingual glossaries for technical translation. Return only JSON.",
        messages=[{
            "role": "user",
            "content": (
                "These are all the section headings from a Chinese book on AI "
                "infrastructure (LLM inference and training systems). Extract the "
                "recurring technical terms and give the standard English rendering "
                "each should receive throughout the translation. Prefer the term an "
                "English systems paper would use. Return a JSON object mapping "
                "Chinese term to English term, and nothing else.\n\n" + "\n".join(heads)
            ),
        }],
    )
    text = "".join(b.text for b in resp.content if b.type == "text").strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.M).strip()
    data = json.loads(text)
    GLOSSARY.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {GLOSSARY} with {len(data)} terms")


def plan(model: str, only: str | None) -> tuple[str, list[dict]]:
    """Return the system prompt and one work item per chunk."""
    glossary = json.loads(GLOSSARY.read_text(encoding="utf-8")) if GLOSSARY.exists() else {}
    if not glossary:
        print("note: no glossary.json — run `glossary` first for consistent terminology\n")
    sys_prompt = system_prompt(glossary)

    items = []
    for ci, f in enumerate(chapters()):
        if only and only not in f.name:
            continue
        chunks = chunk(f.read_text(encoding="utf-8"))
        for i in range(len(chunks)):
            prompt = build_prompt(chunks, i)
            items.append({
                "custom_id": f"c{ci:02d}-{i:03d}",
                "file": f.name,
                "idx": i,
                "total": len(chunks),
                "prompt": prompt,
                "source": chunks[i],
                "cache": str(cache_path(model, sys_prompt, prompt)),
            })
    return sys_prompt, items


def unwrap_extra_math(source: str, out: str) -> str:
    """Remove $...$ the model added around text the source left unwrapped.

    Translations sometimes tidy notation, wrapping a bare mention of a variable
    that the source wrote as plain prose. That changes nothing semantically but
    breaks fidelity, and the source is authoritative about what is mathematics.
    Only occurrences beyond the source's own count for that exact token are
    unwrapped, so genuine repeats survive.
    """
    from collections import Counter
    want = Counter(INLINE_MATH.findall(source))
    have = Counter(INLINE_MATH.findall(out))
    excess = {tok: have[tok] - want.get(tok, 0)
              for tok in have if have[tok] > want.get(tok, 0)}
    if not excess:
        return out

    def repl(m):
        tok = m.group(0)
        if excess.get(tok, 0) > 0:
            excess[tok] -= 1
            return tok[1:-1]          # drop the surrounding $
        return tok
    return INLINE_MATH.sub(repl, out)


CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def chunk_issues(source: str, out: str) -> list[str]:
    """Structural defects in one translated chunk, phrased for a retry prompt."""
    a, b = fingerprint(source), fingerprint(out)
    issues = []

    # Did it actually translate? A chunk can keep every heading, table row and
    # equation in place and still hand back Chinese -- table cells and captions
    # are the usual survivors. A little CJK is legitimate (a cited Chinese title,
    # a product name), so allow a small margin rather than demanding zero.
    # Some places must never keep Chinese, whatever the overall ratio: a
    # percentage tolerance happily passes a chapter whose headings are all still
    # Chinese. A link *target* is the exception -- filenames must not change.
    def strip_targets(text):
        return re.sub(r"\]\([^)]*\)", "]()", text)

    hard = []
    for line in strip_targets(out).split("\n"):
        st = line.strip()
        if not CJK_RE.search(st):
            continue
        if re.match(r"^#{1,6}\s", st):
            hard.append(f"heading still in Chinese: {st[:60]}")
        elif st.startswith("|"):
            hard.append(f"table row still in Chinese: {st[:60]}")
    # match CJK punctuation (。，、；) before the arrow too, not just ideographs
    if re.search(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef][\s\u3000]*(?:→|->)[\s\u3000]*[A-Za-z]", out):
        hard.append("a line keeps the Chinese and appends an English gloss after "
                    "an arrow; replace the Chinese instead of annotating it")
    if re.search(r"\\text\{[^}]*[\u4e00-\u9fff][^}]*\}", out):
        hard.append("Chinese remains inside a LaTeX \\text{...}; the words inside "
                    "\\text{} are prose and must be translated, even though the "
                    "surrounding math is copied verbatim")
    issues.extend(hard[:4])

    src_cjk = len(CJK_RE.findall(source))
    out_cjk = len(CJK_RE.findall(strip_targets(out)))
    if src_cjk and out_cjk > max(5, src_cjk * 0.02):
        issues.append(
            f"{out_cjk} Chinese characters remain untranslated (the source has "
            f"{src_cjk}). Translate ALL of them, including table cells, figure "
            f"captions and headings. Do not leave the Chinese in place and do "
            f"not append an English gloss after it -- replace it."
        )
    for k, label in (("display_math", "display-math $$ blocks"),
                     ("inline_math", "inline $...$ spans"),
                     ("fences", "code fences"),
                     ("table_rows", "table rows")):
        if a[k] != b[k]:
            verb = "dropped" if b[k] < a[k] else "invented"
            issues.append(f"the source has {a[k]} {label}, your translation has "
                          f"{b[k]} — you {verb} {abs(a[k]-b[k])}")
    if len(a["headings"]) != len(b["headings"]):
        issues.append(f"the source has {len(a['headings'])} headings, yours has "
                      f"{len(b['headings'])}")
    for k, label in (("link_targets", "markdown link"), ("image_targets", "image")):
        miss = [t for t in a[k] if t not in set(b[k])]
        if miss:
            issues.append(
                f"{len(miss)} {label} target(s) are missing entirely. Restore each "
                f"as a real [text](target) link, in place: {miss[:6]}"
            )
    return issues


async def run_concurrent(
    model: str, sys_prompt: str, pending: list[dict], concurrency: int, retries: int = 2
) -> int:
    """Bedrock has no Batches API, so fan out concurrent requests instead."""
    from anthropic import AsyncAnthropicBedrockMantle

    spec = MODELS[model]
    client = AsyncAnthropicBedrockMantle(aws_region=BEDROCK_REGION)
    sem = asyncio.Semaphore(concurrency)
    done = 0
    errors = 0

    async def one(it: dict) -> None:
        nonlocal done, errors
        kwargs = {
            "model": BEDROCK_IDS[model],
            "max_tokens": MAX_TOKENS,
            "system": [{
                "type": "text",
                "text": sys_prompt,
                "cache_control": {"type": "ephemeral"},
            }],
            "messages": [{"role": "user", "content": it["prompt"]}],
        }
        if spec["thinking"] is not None:
            kwargs["thinking"] = spec["thinking"]
        history = [{"role": "user", "content": it["prompt"]}]
        try:
            for attempt in range(retries + 1):
                async with sem:
                    async with client.messages.stream(**{**kwargs, "messages": history}) as stream:
                        msg = await stream.get_final_message()
                if msg.stop_reason == "max_tokens":
                    print(f"  {it['custom_id']}: hit max_tokens — lower TARGET_CHUNK")
                    errors += 1
                    return
                text = "".join(b.text for b in msg.content if b.type == "text").strip()
                text = unwrap_extra_math(it["source"], text)

                issues = chunk_issues(it["source"], text)
                if not issues:
                    Path(it["cache"]).write_text(text, encoding="utf-8")
                    done += 1
                    tag = "" if attempt == 0 else f" (fixed on retry {attempt})"
                    print(f"  {it['custom_id']} {it['file'][:18]:18s} "
                          f"{len(it['source']):5d}ch -> {len(text):5d}ch"
                          f"  [{done}/{len(pending)}]{tag}", flush=True)
                    return
                if attempt == retries:
                    break
                print(f"  {it['custom_id']}: retry {attempt+1} — {issues[0][:90]}", flush=True)
                # Show the model its own output and the specific defects. Not
                # cached, so a later run retries rather than keeping a bad chunk.
                history = history + [
                    {"role": "assistant", "content": text},
                    {"role": "user", "content":
                        "Your translation changed the structure of the passage. "
                        "Problems found:\n- " + "\n- ".join(issues) +
                        "\n\nReturn the COMPLETE corrected translation of the same "
                        "passage, fixing exactly these problems and changing nothing "
                        "else. Output only the Markdown."},
                ]
            errors += 1
            print(f"  {it['custom_id']}: STILL BROKEN after {retries} retries — "
                  f"{issues[0][:90]}")
        except Exception as exc:  # keep the other chunks going
            errors += 1
            print(f"  {it['custom_id']}: {type(exc).__name__}: {exc}")

    await asyncio.gather(*(one(it) for it in pending))
    return errors


def cmd_translate(args: argparse.Namespace) -> None:
    model = args.model
    spec = MODELS[model]
    sys_prompt, items = plan(model, args.only)
    CACHE.mkdir(exist_ok=True)

    pending = [it for it in items if not Path(it["cache"]).exists()]
    print(f"{len(items)} chunks, {len(items) - len(pending)} already cached, {len(pending)} to request")

    if pending and args.provider == "bedrock":
        print(f"bedrock: {BEDROCK_IDS[model]} in {BEDROCK_REGION}, {args.concurrency} concurrent")
        errors = asyncio.run(run_concurrent(model, sys_prompt, pending, args.concurrency))
        print(f"done — {errors} failed" if errors else "done")
        if errors:
            print("re-run to retry just the failures (successes are cached)")
    elif pending:
        state = json.loads(STATE.read_text()) if STATE.exists() else {}
        batch_id = state.get("batch_id")
        if batch_id and state.get("model") == model:
            print(f"resuming in-flight batch {batch_id}")
        else:
            requests = []
            for it in pending:
                params = {
                    "model": model,
                    "max_tokens": MAX_TOKENS,
                    "system": [{
                        "type": "text",
                        "text": sys_prompt,
                        "cache_control": {"type": "ephemeral"},
                    }],
                    "messages": [{"role": "user", "content": it["prompt"]}],
                }
                if spec["thinking"] is not None:
                    params["thinking"] = spec["thinking"]
                requests.append(
                    Request(
                        custom_id=it["custom_id"],
                        params=MessageCreateParamsNonStreaming(**params),
                    )
                )
            client = anthropic.Anthropic()
            batch = client.messages.batches.create(requests=requests)
            batch_id = batch.id
            STATE.write_text(json.dumps({"batch_id": batch_id, "model": model}))
            print(f"submitted batch {batch_id} ({len(requests)} requests)")

        client = anthropic.Anthropic()
        while True:
            batch = client.messages.batches.retrieve(batch_id)
            c = batch.request_counts
            if batch.processing_status == "ended":
                break
            print(
                f"  {batch.processing_status}: {c.processing} processing, "
                f"{c.succeeded} ok, {c.errored} errored",
                flush=True,
            )
            time.sleep(args.poll)

        by_id = {it["custom_id"]: it for it in pending}
        errors = 0
        for result in client.messages.batches.results(batch_id):
            it = by_id.get(result.custom_id)
            if it is None:
                continue
            if result.result.type == "succeeded":
                msg = result.result.message
                if msg.stop_reason == "max_tokens":
                    print(f"  {result.custom_id}: hit max_tokens — lower TARGET_CHUNK")
                    errors += 1
                    continue
                text = "".join(b.text for b in msg.content if b.type == "text").strip()
                Path(it["cache"]).write_text(text, encoding="utf-8")
            else:
                detail = getattr(result.result, "error", result.result.type)
                print(f"  {result.custom_id}: {result.result.type} — {detail}")
                errors += 1
        STATE.unlink(missing_ok=True)
        print(f"batch done — {errors} failed" if errors else "batch done")
        if errors:
            print("re-run to retry just the failures (successes are cached)")

    # reassemble whatever is complete
    OUT.mkdir(exist_ok=True)
    by_file: dict[str, list[dict]] = {}
    for it in items:
        by_file.setdefault(it["file"], []).append(it)
    for name, its in by_file.items():
        its.sort(key=lambda x: x["idx"])
        if not all(Path(i["cache"]).exists() for i in its):
            missing = sum(1 for i in its if not Path(i["cache"]).exists())
            print(f"skip {name}: {missing}/{len(its)} chunks missing")
            continue
        body = "\n\n".join(Path(i["cache"]).read_text(encoding="utf-8") for i in its)
        (OUT / name).write_text(body + "\n", encoding="utf-8")
        print(f"wrote {OUT / name}")


def cmd_verify(args: argparse.Namespace) -> None:
    bad = 0
    for src in chapters():
        dst = OUT / src.name
        if not dst.exists():
            continue
        a = fingerprint(src.read_text(encoding="utf-8"))
        b = fingerprint(dst.read_text(encoding="utf-8"))
        issues = []
        for k in ("display_math", "inline_math", "fences", "table_rows"):
            if a[k] != b[k]:
                issues.append(f"{k}: {a[k]} -> {b[k]}")
        if a["headings"] != b["headings"]:
            issues.append(f"heading structure: {len(a['headings'])} -> {len(b['headings'])}")
        for k in ("image_targets", "link_targets"):
            missing = set(a[k]) - set(b[k])
            if missing:
                # Report the scale first: a truncated sample once hid the fact
                # that every link in a chapter had been dropped, not just three.
                issues.append(
                    f"{k}: {len(missing)} of {len(set(a[k]))} dropped or changed"
                    + (" (ALL)" if not set(b[k]) else "")
                    + f" e.g. {sorted(missing)[:2]}"
                )
        bad += bool(issues)
        print(f"{'OK' if not issues else 'CHECK':5s} {src.name}")
        for i in issues:
            print(f"        {i}")
    print("\nall chapters match" if not bad else f"\n{bad} chapter(s) need review")


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--model", default=DEFAULT_MODEL, choices=sorted(MODELS))
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("estimate").set_defaults(fn=cmd_estimate)
    g = sub.add_parser("glossary")
    g.add_argument("--provider", default="bedrock", choices=("bedrock", "api"))
    g.set_defaults(fn=cmd_glossary)
    t = sub.add_parser("translate")
    t.add_argument("--only", help="substring match on filename, e.g. --only 00")
    t.add_argument("--poll", type=int, default=30, help="seconds between polls (batch only)")
    t.add_argument(
        "--provider",
        default="bedrock",
        choices=("bedrock", "api"),
        help="bedrock: concurrent requests (no Batches API on Bedrock). "
             "api: first-party Message Batches at 50%% off.",
    )
    t.add_argument("--concurrency", type=int, default=6, help="bedrock only")
    t.set_defaults(fn=cmd_translate)
    sub.add_parser("verify").set_defaults(fn=cmd_verify)
    args = p.parse_args()
    args.fn(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
